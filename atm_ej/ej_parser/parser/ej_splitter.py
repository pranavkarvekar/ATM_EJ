
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
