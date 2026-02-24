from .regex_patterns import (
    TXN_START_RE,
    TXN_END_RE,
    CARD_RE,
    TXN_CODE_RE,
    TXN_TYPE_RE,
    AMT_REQ_RE,
    AMOUNT_RE,
    AMT_DISP_RE,          # ✅ ADD
    ERROR_CODE_RE,
    ERROR_REASON_RE,
    SWITCH_TIMEOUT_RE,
)

from .status_classifier import classify_status


def build_transaction(txn_block: str, atm_id: str = None) -> dict:
    """
    Build structured transaction record from one EJ transaction block
    """

    txn = {
        "date": None,
        "time": None,
        "card_no": None,
        "terminal_id": "ATM-UNKNOWN",
        "txn_code": None,
        "txn_type": None,
        "amount": None,              # requested
        "dispensed_amount": 0.0,     # ✅ ADDED
        "status": None,
        "error_code": None,
        "error_reason": None,
        "is_timeout": False,         # ✅ ADDED
        "raw": txn_block
    }


    lines = txn_block.splitlines()

    # --- DATE & TIME ---
    for line in lines:
        m = TXN_START_RE.search(line)
        if m:
            txn["date"] = m.group("date")
            txn["time"] = m.group("time")
            break

    # --- CARD NUMBER ---
    for line in lines:
        m = CARD_RE.search(line)
        if m:
            txn["card_no"] = m.group("card")
            break

    #---txn_code-----
    for line in lines:
        m = TXN_CODE_RE.search(line)
        if m:
            txn["txn_code"] = m.group("code").strip()
            break


    # --- TRANSACTION TYPE ---
    for line in lines:
        m = TXN_TYPE_RE.search(line)
        if m:
            txn["txn_type"] = m.group("type").strip()
            break

    # -----------------------------
    # FALLBACK LOGIC (CRITICAL)
    # -----------------------------
    if not txn["txn_type"]:
        joined = " ".join(lines).upper()

        # Strong evidence of cash withdrawal
        if "GP_BUFFERB" in joined or "AMT REQ" in joined or "AMT DISP" in joined:
            txn["txn_type"] = "WITHDRAWAL"
        else:
            txn["txn_type"] = "UNKNOWN"

    # --- AMOUNT ---
    for line in lines:
        m = AMT_REQ_RE.search(line)
        if m:
            txn["amount"] = float(m.group("amount").replace(",", ""))
            break

        m = AMOUNT_RE.search(line)
        if m:
            txn["amount"] = float(m.group("amount").replace(",", ""))
            break
    
    # --- ERROR CODE ---
    for line in lines:
        m = ERROR_CODE_RE.search(line)
        if m:
            txn["error_code"] = m.group("code")
            break

    # --- ERROR REASON ---
    for line in lines:
        if ERROR_REASON_RE.search(line):
            txn["error_reason"] = "REQ NOT SERVICED"
            break
    
    # --- SWITCH TIMEOUT ---
    for line in lines:
        if SWITCH_TIMEOUT_RE.search(line):
            txn["error_code"] = "TIMEOUT"
            txn["error_reason"] = "SWITCH RESPONSE TIMEOUT"
            txn["is_timeout"] = True        # ✅ ADD
            break

    # # --- CASH DISPENSED AMOUNT ---
    # for line in lines:
    #     m = AMT_DISP_RE.search(line)
    #     if m:
    #         txn["dispensed_amount"] = float(m.group("amount").replace(",", ""))
    #         break


    # # -----------------------------
    # # FINAL NORMALIZATION (ADD)
    # # -----------------------------

    # # If dispensed amount exists but requested missing
    # if txn["dispensed_amount"] > 0 and not txn["amount"]:
    #     txn["amount"] = txn["dispensed_amount"]

    # # If requested exists but no dispense → failed
    # if txn["amount"] and txn["dispensed_amount"] == 0 and txn["status"] == "SUCCESS":
    #     txn["status"] = "FAILED"

        # --- DISPENSED AMOUNT ---
    txn["dispensed_amount"] = 0.0

    for line in lines:
        m = AMT_DISP_RE.search(line)
        if m:
            txn["dispensed_amount"] = float(
                m.group("amount").replace(",", "")
            )
            break

    # --- STATUS (delegated) ---
    txn["status"] = classify_status(lines)

    # -----------------------------
    # FINAL NORMALIZATION
    # -----------------------------

    # If dispensed amount exists but requested missing
    if txn["dispensed_amount"] > 0 and not txn["amount"]:
        txn["amount"] = txn["dispensed_amount"]

    # If requested exists but no dispense but marked success → fix it
    if txn["amount"] and txn["dispensed_amount"] == 0 and txn["status"] == "SUCCESS":
        txn["status"] = "FAILED"


    # --- STATUS (delegated) ---
    txn["status"] = classify_status(lines)

    return txn
