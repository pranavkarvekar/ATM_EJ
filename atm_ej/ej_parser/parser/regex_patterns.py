import re

# --------------------------------------------------
# TRANSACTION START
# Example:
# 17/09/01 08:24:40 -> TRANSACTION START
# --------------------------------------------------
TXN_START_RE = re.compile(
    r"(?P<date>\d{2}/\d{2}/\d{2})\s+"
    r"(?P<time>\d{2}:\d{2}:\d{2})\s+->\s+TRANSACTION START"
)

TXN_END_RE = re.compile(r"<-TRANSACTION END")


# --------------------------------------------------
# CARD NUMBER
# Example:
# 08:24:40 CARD NO:652229XXXXXX0669
# --------------------------------------------------
CARD_RE = re.compile(
    r"CARD NO:(?P<card>\d{6}X+?\d{4})"
)

# --------------------------------------------------
# TRANSACTION REQUEST CODE (protocol / routing)
# Example: TRANS REQ:CBC   AB
# --------------------------------------------------
TXN_CODE_RE = re.compile(
    r"TRANS REQ:(?P<code>[A-Z ]{3,10})"
)

# --------------------------------------------------
# TRANSACTION BUSINESS TYPE
# Example: TX        :WITHDRAWAL
# --------------------------------------------------
TXN_TYPE_RE = re.compile(
    r"TX\s*:\s*(?P<type>[A-Z ]+)"
)

# --------------------------------------------------
# AMOUNT REQUESTED
# Example:
# AMT REQ :          5,500.00
# --------------------------------------------------
AMT_REQ_RE = re.compile(
    r"AMT REQ\s*:\s*(?P<amount>[\d,]+\.\d{2})"
)

# --------------------------------------------------
# AMOUNT (fallback)
# Example:
# AMOUNT:4000
# --------------------------------------------------
AMOUNT_RE = re.compile(
    r"AMOUNT\s*:\s*(?P<amount>[\d,]+)"
)

# --------------------------------------------------
# CASH DISPENSED
# Example:
# AMT DISP:        4,000.00
# --------------------------------------------------
AMT_DISP_RE = re.compile(
    r"AMT DISP\s*:\s*(?P<amount>[\d,]+\.\d{2})"
)


# --------------------------------------------------
# ERROR / RESPONSE CODE
# Example:
# RSP CODE  :14
# --------------------------------------------------
ERROR_CODE_RE = re.compile(
    r"RSP\s+CODE\s*:\s*(?P<code>\d+)"
)


# --------------------------------------------------
# ERROR REASON
# Example:
# REQ NOT SERVICED
# --------------------------------------------------
ERROR_REASON_RE = re.compile(
    r"\bREQ\s+NOT\s+SERVICED\b"
)

# --------------------------------------------------
# SWITCH RESPONSE TIMEOUT
# Example:
# SWITCH RESP. TIMEOUT
# --------------------------------------------------
SWITCH_TIMEOUT_RE = re.compile(
    r"SWITCH\s+RESP\.?\s+TIMEOUT",
    re.IGNORECASE
)


