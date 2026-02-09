def classify_status(lines: list) -> str:
    """
    Classify transaction status using EJ evidence
    """

    joined = " ".join(lines).upper()

    # --- SUCCESS CONDITIONS ---
    if "STATUS:CASH TAKEN" in joined:
        return "SUCCESS"

    if "REQ SERVICED" in joined:
        return "SUCCESS"

    # --- FAILURE CONDITIONS ---
    failure_signals = [
        "REQ NOT SERVICED",
        "SWITCH RESP. TIMEOUT",
        "DISPENSER FAILURE",
        "COMMAND REJECT",
        "USER - PIN ENTRY CANCELLED"
    ]

    for signal in failure_signals:
        if signal in joined:
            return "FAILED"

    # --- INCOMPLETE / FORCED ---
    if "<<FORCED END" in joined or "<<INCOMPLETE TRANSACTION>>" in joined:
        return "INCOMPLETE"

    # --- DEFAULT ---
    return "ABANDONED"

