from ..src import *
def _tiktoken_split(word: str):
    token_ids = ENC.encode(word)
    pieces = [ENC.decode([tid]) for tid in token_ids]
    merged, buf = [], ""

    for p in pieces:
        if p.isalpha():
            buf += p
        else:
            if buf:
                merged.append(buf)
                buf = ""
    if buf:
        merged.append(buf)

    return merged or [word]

def tokenize_string(domain: str):
    primary=[""]
    if domain:
        domain = domain.lower().strip()
        root = re.sub(r"\.[a-z0-9]{2,6}$", "", domain)

        primary = segment(root)

        if len(primary) <= 1:
            return _tiktoken_split(root)

    return primary
tokenize_domain = tokenize_string
