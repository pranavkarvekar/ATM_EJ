# from datetime import datetime
# from .regex_patterns import *


# def build_transaction(txn_block: str) -> dict:
#     """
#     Takes ONE transaction block (from ej_split)
#     Returns a fully structured transaction dictionary
#     """

#     txn = {
#         "start_time": None,
#         "end_time": None,
#         "card_masked": None,
#         "card_full": None,
#         "txn_no": None,
#         "tno": None,
#         "ssn": None,
#         "txn_type": None,
#         "amount_requested": None,
#         "amount_authorized": None,
#         "amount_dispensed": None,
#         "rsp_code": None,
#         "host_state": None,
#         "host_fid": None,
#         "denomination": None,
#         "cash_taken": False,
#         "status": "UNKNOWN",
#         "failure_reason": None,
#         "events": [],
#         "raw_block": txn_block
#     }

#     lines = txn_block.splitlines()

#     for line in lines:

#         # -----------------------------
#         # Transaction START
#         # -----------------------------
#         m = TXN_START_RE.search(line)
#         if m:
#             txn["start_time"] = f"{m.group('date')} {m.group('time')}"
#             continue

#         # -----------------------------
#         # Transaction END
#         # -----------------------------
#         m = TXN_END_RE.search(line)
#         if m:
#             txn["end_time"] = m.group("time")
#             continue

#         # -----------------------------
#         # Card Numbers
#         # -----------------------------
#         m = CARD_MASKED_RE.search(line)
#         if m:
#             txn["card_masked"] = m.group("card_masked")

#         m = CARD_FULL_RE.search(line)
#         if m:
#             txn["card_full"] = m.group("card_full")

#         # -----------------------------
#         # IDs
#         # -----------------------------
#         m = TXN_NO_RE.search(line)
#         if m:
#             txn["txn_no"] = m.group("txn_no")

#         m = TNO_RE.search(line)
#         if m:
#             txn["tno"] = m.group("tno")

#         m = SSN_RE.search(line)
#         if m:
#             txn["ssn"] = m.group("ssn")

#         # -----------------------------
#         # Transaction Type
#         # -----------------------------
#         m = TX_TYPE_RE.search(line)
#         if m:
#             txn["txn_type"] = m.group("txn_type").strip()

#         # -----------------------------
#         # Amounts
#         # -----------------------------
#         m = GP_BUFFER_RE.search(line)
#         if m and txn["amount_requested"] is None:
#             txn["amount_requested"] = int(m.group("amount"))

#         m = AMT_REQ_RE.search(line)
#         if m:
#             txn["amount_requested"] = float(m.group("amount").replace(",", ""))

#         m = AMT_AUTH_RE.search(line)
#         if m:
#             txn["amount_authorized"] = float(m.group("amount").replace(",", ""))

#         m = AMT_DISP_RE.search(line)
#         if m:
#             txn["amount_dispensed"] = float(m.group("amount").replace(",", ""))

#         # -----------------------------
#         # Host Response
#         # -----------------------------
#         m = HOST_RESP_RE.search(line)
#         if m:
#             txn["host_state"] = m.group("state")
#             txn["host_fid"] = m.group("fid")

#         m = RSP_CODE_RE.search(line)
#         if m:
#             txn["rsp_code"] = m.group("rsp_code")

#         # -----------------------------
#         # Cash / Denomination
#         # -----------------------------
#         m = TO_DISPENSE_RE.search(line)
#         if m:
#             txn["denomination"] = m.group("details").strip()

#         if CASH_TAKEN_RE.search(line):
#             txn["cash_taken"] = True

#         # -----------------------------
#         # Failures
#         # -----------------------------
#         if SWITCH_TIMEOUT_RE.search(line):
#             txn["failure_reason"] = "SWITCH_TIMEOUT"

#         if USER_CANCEL_RE.search(line):
#             txn["failure_reason"] = "USER_CANCELLED"

#         # -----------------------------
#         # Timeline Events
#         # -----------------------------
#         m = TIMESTAMP_EVENT_RE.search(line)
#         if m:
#             txn["events"].append({
#                 "time": m.group("time"),
#                 "event": m.group("event").strip()
#             })

#     # -----------------------------
#     # FINAL STATUS CLASSIFICATION
#     # -----------------------------
#     if txn["amount_dispensed"] and txn["cash_taken"]:
#         txn["status"] = "SUCCESS"

#     elif txn["rsp_code"] in {"14", "51", "55", "91"}:
#         txn["status"] = "FAILED"
#         if not txn["failure_reason"]:
#             txn["failure_reason"] = "HOST_DECLINE"

#     elif txn["failure_reason"]:
#         txn["status"] = "FAILED"

#     elif txn["amount_requested"] and not txn["amount_dispensed"]:
#         txn["status"] = "FAILED"

#     return txn


from .regex_patterns import (
    TXN_START_RE,
    CARD_RE,
    TXN_CODE_RE,
    TXN_TYPE_RE,
    AMT_REQ_RE,
    AMOUNT_RE,
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
        "txn_code":None,
        "txn_type":None,
        "amount": None,
        "status": None,
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

    # --- STATUS (delegated) ---
    txn["status"] = classify_status(lines)

    return txn
