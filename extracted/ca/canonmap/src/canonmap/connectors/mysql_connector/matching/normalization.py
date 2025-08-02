# src/canonmap/connectors/mysql_connector/matching/normalization.py

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

def to_initialism(text: str) -> str:
    """
    Returns the initialism (first letter of each word, uppercased).
    Example: "Advanced AI Solutions" -> "AAS"
    """
    if not text:
        return ""
    return "".join(w[0].upper() for w in text.split() if w)

def tokenize(text: str) -> list:
    """
    Splits normalized text into tokens (words).
    """
    return normalize(text).split()