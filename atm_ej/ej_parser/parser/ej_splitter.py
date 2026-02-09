# def split_transactions(ej_text):
#     blocks = []
#     current = []

#     for line in ej_text.splitlines():
#         if "-> TRANSACTION START" in line:
#             current = [line]
#         elif "<-TRANSACTION END" in line:
#             current.append(line)
#             blocks.append("\n".join(current))
#             current = []
#         else:
#             if current:
#                 current.append(line)

#     return blocks

# def split_transactions(ej_text):
#     blocks = []
#     current = []
#     in_txn = False

#     for line in ej_text.splitlines():

#         if "TRANSACTION START" in line:
#             current = [line]
#             in_txn = True

#         elif "TRANSACTION END" in line and in_txn:
#             current.append(line)
#             blocks.append("\n".join(current))
#             current = []
#             in_txn = False

#         elif in_txn:
#             current.append(line)

#     # handle incomplete transaction
#     if current:
#         current.append("<<INCOMPLETE TRANSACTION>>")
#         blocks.append("\n".join(current))

#     return blocks

# def split_transactions(ej_text):
#     blocks = []
#     current = []

#     for line in ej_text.splitlines():

#         # START detected
#         if "TRANSACTION START" in line:
#             # safety: close previous txn if still open
#             if current:
#                 current.append("<<FORCED END: NEW TRANSACTION START>>")
#                 blocks.append("\n".join(current))
#             current = [line]

#         # END detected
#         elif "TRANSACTION END" in line:
#             if current:
#                 current.append(line)
#                 blocks.append("\n".join(current))
#                 current = []

#         # inside transaction
#         elif current:
#             current.append(line)

#     # safety: incomplete transaction at EOF
#     if current:
#         current.append("<<INCOMPLETE TRANSACTION>>")
#         blocks.append("\n".join(current))

#     return blocks




import re

START_RE = re.compile(r'->\s*TRANSACTION START')
END_RE   = re.compile(r'<-\s*TRANSACTION END')

def split_transactions(ej_text):
    blocks = []
    current = []

    for line in ej_text.splitlines():

        if START_RE.search(line):
            if current:
                current.append("<<FORCED END: NEW TRANSACTION START>>")
                blocks.append("\n".join(current))
            current = [line]

        elif END_RE.search(line):
            if current:
                current.append(line)
                blocks.append("\n".join(current))
                current = []

        elif current:
            current.append(line)

    if current:
        current.append("<<INCOMPLETE TRANSACTION>>")
        blocks.append("\n".join(current))

    return blocks
