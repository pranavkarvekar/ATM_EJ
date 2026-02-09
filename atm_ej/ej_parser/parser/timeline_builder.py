from .regex_patterns import TIMESTAMP_EVENT_RE


def build_timeline(txn_block: str) -> list:
    """
    Build ordered timeline events from a transaction block.
    Returns list of {time, event}
    """

    timeline = []
    lines = txn_block.splitlines()

    for line in lines:
        match = TIMESTAMP_EVENT_RE.search(line)
        if match:
            timeline.append({
                "time": match.group("time"),
                "event": match.group("event").strip()
            })

    return timeline
