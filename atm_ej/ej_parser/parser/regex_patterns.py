# import re

# # -------------------------------------------------
# # Transaction Boundary
# # -------------------------------------------------
# TXN_START_RE = re.compile(
#     r'(?P<date>\d{2}/\d{2}/\d{2})\s+'
#     r'(?P<time>\d{2}:\d{2}:\d{2})\s+->\s*TRANSACTION START'
# )

# TXN_END_RE = re.compile(
#     r'(?P<time>\d{2}:\d{2}:\d{2})\s+<-\s*TRANSACTION END'
# )

# # -------------------------------------------------
# # Card Details
# # -------------------------------------------------
# CARD_MASKED_RE = re.compile(
#     r'CARD NO:(?P<card_masked>\d{6}X+\d{4})'
# )

# CARD_FULL_RE = re.compile(
#     r'CRD\s+:\s*(?P<card_full>\d{16,19})'
# )

# # -------------------------------------------------
# # Transaction Identity
# # -------------------------------------------------
# TXN_NO_RE = re.compile(
#     r'TXN NO\s*:\s*(?P<txn_no>\d+)'
# )

# TNO_RE = re.compile(
#     r'TNO\s+:\s*(?P<tno>\d+)'
# )

# SSN_RE = re.compile(
#     r'SSN\s+:\s*(?P<ssn>\d+)'
# )

# # -------------------------------------------------
# # Transaction Type
# # -------------------------------------------------
# TX_TYPE_RE = re.compile(
#     r'TX\s*:\s*(?P<txn_type>[A-Z ]+)'
# )

# # -------------------------------------------------
# # Amounts
# # -------------------------------------------------
# GP_BUFFER_RE = re.compile(
#     r'GP_BUFFERB\s*:\s*(?P<amount>\d+)'
# )

# AMT_REQ_RE = re.compile(
#     r'AMT REQ\s*:\s*(?P<amount>[\d,]+\.\d{2})'
# )

# AMT_AUTH_RE = re.compile(
#     r'AMT AUTH\s*:\s*(?P<amount>[\d,]+\.\d{2})'
# )

# AMT_DISP_RE = re.compile(
#     r'AMT DISP\s*:\s*(?P<amount>[\d,]+\.\d{2})'
# )

# # -------------------------------------------------
# # Response / Status
# # -------------------------------------------------
# RSP_CODE_RE = re.compile(
#     r'RSP CODE\s*:\s*(?P<rsp_code>\d{2})'
# )

# HOST_RESP_RE = re.compile(
#     r'RESP:\s*STATE:(?P<state>\d+),FID:(?P<fid>[\d:]+)'
# )

# # -------------------------------------------------
# # Cash Handling Events
# # -------------------------------------------------
# TO_DISPENSE_RE = re.compile(
#     r'TO DISPENSE\s*:\s*(?P<details>.+)'
# )

# PRESENTED_RE = re.compile(
#     r'PRESENTED\s*:\s*(?P<details>.+)'
# )

# CASH_TAKEN_RE = re.compile(
#     r'STATUS\s*:\s*CASH TAKEN'
# )

# STACKED_RE = re.compile(
#     r'STACKED'
# )

# # -------------------------------------------------
# # Outcome Markers
# # -------------------------------------------------
# REQ_SERVED_RE = re.compile(
#     r'REQ SERVICED'
# )

# REQ_NOT_SERVED_RE = re.compile(
#     r'REQ NOT SERVICED'
# )

# # -------------------------------------------------
# # Failure / Exception Events
# # -------------------------------------------------
# SWITCH_TIMEOUT_RE = re.compile(
#     r'SWITCH RESP\. TIMEOUT'
# )

# PRINTER_NO_PAPER_RE = re.compile(
#     r'PRINT RECEIPT\s*-\s*NO PAPER'
# )

# USER_CANCEL_RE = re.compile(
#     r'USER\s*-\s*(PIN ENTRY CANCELLED|NO OPTION SELECTED)'
# )

# # -------------------------------------------------
# # Timeline Event (Generic)
# # -------------------------------------------------
# TIMESTAMP_EVENT_RE = re.compile(
#     r'(?P<time>\d{2}:\d{2}:\d{2})\s+(?P<event>.+)'
# )


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

