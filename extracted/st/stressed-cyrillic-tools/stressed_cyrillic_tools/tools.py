import re
from typing import List
import unicodedata


def is_accented(word: str):
    """Returns True if the word has an accent (also detects if the word has a grave accent."""
    return unaccentify(word) != word


def is_acute_accented(phrase: str):
    """Returns True if the phrase has an acute accent."""
    return "\u0301" in phrase


def has_only_one_syllable(word: str):
    """Returns True if the word has only one syllable ( == at most one vowel)
    Accepts only one word without spaces."""
    if word == " ":
        return True # No idea when this happens, but it does
    if " " in word:
        print(f"Warning: has_only_one_syllable() was called with {word}, containing spaces. ")

    word_lower = word.lower()
    vowels = 0
    for char in word_lower:
        if char in "аоэуыяеёюи":
            vowels += 1
    return vowels <= 1


def has_acute_accent_or_only_one_syllable(word: str):
    """Returns True if the word (probably) has been stressed or does not need to be stressed:
    This is the case if it has an acute accent or only one syllable"""
    return is_acute_accented(word) or has_only_one_syllable(word)


# Unaccentifier written by Roman Susi
# Taken from https://stackoverflow.com/questions/35942129/remove-accent-marks-from-characters-while-preserving-other-diacritics
ACCENT_MAPPING_BASE = {
    "́": "",
    "̀": "",
    "а́": "а",
    "а̀": "а",
    "е́": "е",
    "ѐ": "е",
    "и́": "и",
    "ѝ": "и",
    "о́": "о",
    "о̀": "о",
    "у́": "у",
    "у̀": "у",
    "ы́": "ы",
    "ы̀": "ы",
    "э́": "э",
    "э̀": "э",
    "ю́": "ю",
    "̀ю": "ю",
    "я́́": "я",
    "я̀": "я",
}

ACCENT_MAPPING = {
    unicodedata.normalize("NFKC", i): j for i, j in ACCENT_MAPPING_BASE.items()
}


def unaccentify(s: str):
    source = unicodedata.normalize("NFKC", s)
    for old, new in ACCENT_MAPPING.items():
        source = source.replace(old, new)
    return source


def remove_accent_if_only_one_syllable(s: str):
    """Removes the accent from words like что́, which are usually not set in texts.
    Also works with complete texts (splits by space)
    Warning: replaces no-breaking spaces with normal spaces."""
    if " " in s:
        words = s.replace("\xa0", " ").split(" ")

        fixed_words: List[str] = []
        for word in words:
            fixed_words.append(remove_accent_if_only_one_syllable(word))
        return " ".join(fixed_words)

    s_unaccented = unaccentify(s)
    if has_only_one_syllable(s_unaccented):
        return s_unaccented
    else:
        return s


def has_cyrillic_letters(s: str):
    """Returns True if the string has at least one Cyrillic letter."""
    m = re.findall(r"[А-я]+", s)
    return m != []


def convert_ap_accent_to_real(word: str) -> str:
    """This replaces the accents marked with apostrophes with a real acute accent."""
    return word.replace("'", "\u0301")


def remove_apostrophes(word: str) -> str:
    """Removes apostrophes from words like удар'ения."""
    return word.replace("'", "")


def remove_yo(word: str) -> str:
    """This replaces ё with the letter е (also works for upper case)."""
    return word.replace("ё", "е").replace("Ё", "Е")


def get_lower_and_without_yo(word: str) -> str:
    """Returns the lower case, unaccentified version of the word without yo."""
    return remove_yo(unaccentify(word)).lower()


def has_two_stress_marks(word: str) -> bool:
    """Returns True if the word has at least two accent marks.
    For strings with spaces, returns True if at least one word has at least two accent marks."""

    if " " in word:
        return any(has_two_stress_marks(word) for word in word.split(" "))
    if "-" in word:
        return any(has_two_stress_marks(word) for word in word.split("-"))

    # Bake in accent marks as much as possible, in theory this prevents editing of integral stress marks
    word = unicodedata.normalize("NFKC", word)

    num_combining_accent_marks = word.count("\u0301") + word.count("\u0300")
    word_with_only_baked_in_accents = word.replace("\u0301", "").replace("\u0300", "")
    if num_combining_accent_marks >= 2:
        return True
    else:
        # This handles also the grave accents
        unaccented = unaccentify(word_with_only_baked_in_accents)
        # Assert that the word and the unaccented version have the same length, otherwise we have a bug
        assert len(word_with_only_baked_in_accents) == len(unaccented)
        # Calculate how many characters differ by iterating over the word
        num_differences = 0
        for char1, char2 in zip(word_with_only_baked_in_accents, unaccented):
            if char1 != char2:
                num_differences += 1
        return num_combining_accent_marks + num_differences >= 2


def fix_two_accent_marks(word: str) -> str:
    """Fixes words with two accent marks (acute and grave) by removing the grave accent.
    If the word has multiple acute accents, it keeps the first one.
    Also works for complete texts (splits by space)."""

    if not has_two_stress_marks(word):
        return word

    if " " in word:
        words = word.split(" ")
        fixed_words: List[str] = []
        for word in words:
            fixed_words.append(fix_two_accent_marks(word))
        return " ".join(fixed_words)

    if "-" in word:
        words = word.split("-")
        fixed_words = []
        for word in words:
            fixed_words.append(fix_two_accent_marks(word))
        return "-".join(fixed_words)
    # TODO: This breaks if the word has a dash and a space

    # Decompose everything
    word = unicodedata.normalize("NFKD", word)

    # Count the number of acute accents
    num_acute_accents = word.count("\u0301")

    if num_acute_accents == 1:
        # If there is only one acute accent, remove all grave accents
        return word.replace("\u0300", "")
    elif num_acute_accents == 0:
        #word = word.split("\u0300")[0] + "\u0300" + "".join(word.split("\u0300")[1:])
        #print("Potentially malformed word: ", word)
        # This is usually caused by it being a part of a word with a dash
        return word.replace("\u0300", "")

        #return word
    else:
        # Keep the first acute accent and remove the rest
        word = word.split("\u0301")[0] + "\u0301" + "".join(word.split("\u0301")[1:])
        return word.replace("\u0300", "")

WORDS_WITHOUT_STRESS = ["обо"]

def is_unhelpfully_unstressed(word: str) -> bool:
    """Returns True if the word would be of no use in a stress dictionary. This filters out mostly unstressed words,
    but also words with one syllable where the stress is clear"""

    if " " in word:
        # Return True if all of the words in the phrase are unhelpfully unstressed
        return all(is_unhelpfully_unstressed(word) for word in word.split(" "))

    # Check if word is in the list of words without stress
    if word.lower() in WORDS_WITHOUT_STRESS:
        return False

    if "ё" in word or "Ё" in word:
        return False
    if has_only_one_syllable(word):
        if "е" in word or "Е" in word:
            # The word лес tells us that it is not written like "лёс"
            return False
        else:
            # Words with only one syllable are never marked with an accent
            return True
    return not is_accented(word)
