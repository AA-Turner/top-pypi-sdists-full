from difflib import SequenceMatcher
from random import randint, choice
from string import ascii_letters, digits


def compute_similarity_score(s1: str, s2: str) -> float:
    s1_processed = s1.lower().strip()
    s2_processed = s2.lower().strip()

    return SequenceMatcher(None, s1_processed, s2_processed).ratio()


def random_alphanumeric_string(min_length: int = 1, max_length: int = 20) -> str:
    n_chars = randint(min_length, max_length)
    characters = ascii_letters + digits

    return "".join(choice(characters) for _ in range(n_chars))
