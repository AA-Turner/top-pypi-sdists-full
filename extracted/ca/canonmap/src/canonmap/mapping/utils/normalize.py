import re
import unicodedata


def normalize(text: str) -> str:
    """
    Normalize input text for matching:
    - Unicode NFKD to ASCII
    - Remove punctuation
    - Collapse whitespace
    - Lowercase
    """
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()