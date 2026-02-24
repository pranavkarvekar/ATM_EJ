def reconcile_transactions(transactions):
    total_requested = 0.0
    total_dispensed = 0.0
    total_failed_amount = 0.0
    phantom_risk = 0.0

    mismatches = []

    for txn in transactions:

        requested = float(txn.get("amount") or 0)
        dispensed = float(txn.get("dispensed_amount") or 0)
        status = txn.get("status")

        total_requested += requested
        total_dispensed += dispensed

        # ------------------------------
        # FAILED BUT MONEY DISPENSED
        # ------------------------------
        if status == "FAILED" and dispensed > 0:
            phantom_risk += dispensed
            mismatches.append({
                "reason": "FAILED BUT CASH DISPENSED",
                "txn": txn
            })

        # ------------------------------
        # SUCCESS BUT AMOUNT MISMATCH
        # ------------------------------
        if status == "SUCCESS" and requested != dispensed:
            mismatches.append({
                "reason": "SUCCESS BUT AMOUNT MISMATCH",
                "txn": txn
            })

        # ------------------------------
        # FAILED AMOUNT
        # ------------------------------
        if status == "FAILED":
            total_failed_amount += requested

    audit_status = "BALANCED"
    if mismatches or phantom_risk > 0:
        audit_status = "MISMATCH"

    return {
        "total_requested": total_requested,
        "total_dispensed": total_dispensed,
        "total_failed_amount": total_failed_amount,
        "phantom_risk": phantom_risk,
        "audit_status": audit_status,
        "mismatches": mismatches
    }