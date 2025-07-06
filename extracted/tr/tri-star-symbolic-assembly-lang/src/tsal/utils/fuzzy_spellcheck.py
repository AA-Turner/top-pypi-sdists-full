from difflib import get_close_matches
from typing import List

def fuzzy_correct(token: str, op_list: List[str]) -> str:
    """Suggest correction for code typos using ops from JSON schema."""
    matches = get_close_matches(token, op_list, n=1, cutoff=0.7)
    return matches[0] if matches else token
