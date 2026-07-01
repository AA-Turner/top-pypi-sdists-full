import random
import re
import typing as t

from dreadnode.core.transforms import Transform


def substitute(
    mapping: t.Mapping[str, str | list[str]],
    *,
    unit: t.Literal["char", "word"] = "word",
    case_sensitive: bool = False,
    deterministic: bool = False,
    seed: int | None = None,
    name: str = "substitute",
) -> Transform[str, str]:
    """
    Substitutes characters or words based on a provided mapping.

    Args:
        mapping: A dictionary where keys are units to be replaced and
                 values are a list of possible replacements.
        unit: The unit of text to operate on ('char' or 'word').
        case_sensitive: If False, matching is case-insensitive.
        deterministic: If True, always picks the first replacement option.
        seed: Seed for the random number generator for reproducibility.
        name: The name of the transform.
    """

    rand = random.Random(seed)  # nosec

    def transform(text: str) -> str:
        # Normalize mapping keys for case-insensitive matching if needed
        lookup_map = mapping if case_sensitive else {k.lower(): v for k, v in mapping.items()}

        def get_replacement(item: str) -> str:
            key = item if case_sensitive else item.lower()
            if key in lookup_map:
                options = lookup_map[key]
                if isinstance(options, str):
                    return options
                if deterministic:
                    return options[0]
                return rand.choice(options)
            return item

        if unit == "char":
            return "".join(get_replacement(char) for char in text)

        # For 'word' unit, we use regex to preserve punctuation and spacing
        words = re.findall(r"\w+|\S+", text)
        substituted_words = [get_replacement(word) for word in words]

        # Rejoin intelligently to handle spacing around punctuation
        result = " ".join(substituted_words)
        return re.sub(r'\s([?.!,"\'`])', r"\1", result).strip()

    return Transform(transform, name=name, modality="text")


# fmt: off
BRAILLE_MAP = {
    "a": "⠁", "b": "⠃", "c": "⠉", "d": "⠙", "e": "⠑", "f": "⠋", "g": "⠛", "h": "⠓",
    "i": "⠊", "j": "⠚", "k": "⠅", "l": "⠇", "m": "⠍", "n": "⠝", "o": "⠕", "p": "⠏",
    "q": "⠟", "r": "⠗", "s": "⠎", "t": "⠞", "u": "⠥", "v": "⠧", "w": "⠺", "x": "⠭",
    "y": "⠽", "z": "⠵", "1": "⠼⠁", "2": "⠼⠃", "3": "⠼⠉", "4": "⠼⠙", "5": "⠼⠑",
    "6": "⠼⠋", "7": "⠼⠛", "8": "⠼⠓", "9": "⠼⠊", "0": "⠼⠚", ".": "⠲", ",": "⠂",
    ";": "⠆", ":": "⠒", "?": "⠦", "!": "⠖", "(": "⠐⠣", ")": "⠐⠜", "'": "⠄",
    "-": "⠤", "/": "⠌", " ": "⠀",
}
BRAILLE_CAPITAL_INDICATOR = "⠠"
# fmt: on


def braille(*, name: str = "braille") -> Transform[str, str]:
    """Converts ASCII text to Grade 1 Braille."""

    def transform(text: str) -> str:
        result = []
        for char in text:
            if "A" <= char <= "Z":
                result.append(BRAILLE_CAPITAL_INDICATOR)
                result.append(BRAILLE_MAP.get(char.lower(), char.lower()))
            else:
                result.append(BRAILLE_MAP.get(char, char))
        return "".join(result)

    return Transform(transform, name=name, modality="text")


# fmt: off
BUBBLE_MAP = {
    "a": "ⓐ", "b": "ⓑ", "c": "ⓒ", "d": "ⓓ", "e": "ⓔ", "f": "ⓕ", "g": "ⓖ",
    "h": "ⓗ", "i": "ⓘ", "j": "ⓙ", "k": "ⓚ", "l": "ⓛ", "m": "ⓜ", "n": "ⓝ",
    "o": "ⓞ", "p": "ⓟ", "q": "ⓠ", "r": "ⓡ", "s": "ⓢ", "t": "ⓣ", "u": "ⓤ",
    "v": "ⓥ", "w": "ⓦ", "x": "ⓧ", "y": "ⓨ", "z": "ⓩ", "A": "Ⓐ", "B": "Ⓑ",
    "C": "Ⓒ", "D": "Ⓓ", "E": "Ⓔ", "F": "Ⓕ", "G": "Ⓖ", "H": "Ⓗ", "I": "Ⓘ",
    "J": "Ⓙ", "K": "Ⓚ", "L": "Ⓛ", "M": "Ⓜ", "N": "Ⓝ", "O": "Ⓞ", "P": "Ⓟ",
    "Q": "Ⓠ", "R": "Ⓡ", "S": "Ⓢ", "T": "Ⓣ", "U": "Ⓤ", "V": "Ⓥ", "W": "Ⓦ",
    "X": "Ⓧ", "Y": "Ⓨ", "Z": "Ⓩ", "0": "⓪", "1": "①", "2": "②", "3": "③",
    "4": "④", "5": "⑤", "6": "⑥", "7": "⑦", "8": "⑧", "9": "⑨",
}
# fmt: on


def bubble_text(*, name: str = "bubble_text") -> Transform[str, str]:
    """Converts alphanumeric characters to their Unicode bubble equivalents."""

    return substitute(
        mapping=BUBBLE_MAP,
        unit="char",
        name=name,
    )


# fmt: off
CURSIVE_MAP = {
    "A": "𝒜", "B": "ℬ", "C": "𝒞", "D": "𝒟", "E": "ℰ", "F": "ℱ", "G": "𝒢",
    "H": "ℋ", "I": "ℐ", "J": "𝒥", "K": "𝒦", "L": "ℒ", "M": "ℳ", "N": "𝒩",
    "O": "𝒪", "P": "𝒫", "Q": "𝒬", "R": "ℛ", "S": "𝒮", "T": "𝒯", "U": "𝒰",
    "V": "𝒱", "W": "𝒲", "X": "𝒳", "Y": "𝒴", "Z": "𝒵", "a": "𝒶", "b": "𝒷",
    "c": "𝒸", "d": "𝒹", "e": "ℯ", "f": "𝒻", "g": "ℊ", "h": "𝒽", "i": "𝒾",
    "j": "𝒿", "k": "𝓀", "l": "𝓁", "m": "𝓂", "n": "𝓃", "o": "ℴ", "p": "𝓅",
    "q": "𝓆", "r": "𝓇", "s": "𝓈", "t": "𝓉", "u": "𝓊", "v": "𝓋", "w": "𝓌",
    "x": "𝓍", "y": "𝓎", "z": "𝓏",
}
# fmt: on


def cursive(*, name: str = "cursive") -> Transform[str, str]:
    """Converts text to a cursive style using Unicode."""

    return substitute(
        mapping=CURSIVE_MAP,
        unit="char",
        name=name,
    )


# fmt: off
DOUBLE_STRUCK_MAP = {
    "A": "𝔸", "B": "𝔹", "C": "ℂ", "D": "𝔻", "E": "𝔼", "F": "𝔽", "G": "𝔾", "H": "ℍ", "I": "𝕀", "J": "𝕁",
    "K": "𝕂", "L": "𝕃", "M": "𝕄", "N": "ℕ", "O": "𝕆", "P": "ℙ", "Q": "ℚ", "R": "ℝ", "S": "𝕊", "T": "𝕋",
    "U": "𝕌", "V": "𝕍", "W": "𝕎", "X": "𝕏", "Y": "𝕐", "Z": "ℤ", "a": "𝕒", "b": "𝕓", "c": "𝕔", "d": "𝕕",
    "e": "𝕖", "f": "𝕗", "g": "𝕘", "h": "𝕙", "i": "𝕚", "j": "𝕛", "k": "𝕜", "l": "𝕝", "m": "𝕞", "n": "𝕟",
    "o": "𝕠", "p": "𝕡", "q": "𝕢", "r": "𝕣", "s": "𝕤", "t": "𝕥", "u": "𝕦", "v": "𝕧", "w": "𝕨", "x": "𝕩",
    "y": "𝕪", "z": "𝕫", "0": "𝟘", "1": "𝟙", "2": "𝟚", "3": "𝟛", "4": "𝟜", "5": "𝟝", "6": "𝟞", "7": "𝟟",
    "8": "𝟠", "9": "𝟡",
}
# fmt: on


def double_struck(*, name: str = "double_struck") -> Transform[str, str]:
    """Converts text to a double-struck (blackboard bold) style."""

    return substitute(
        mapping=DOUBLE_STRUCK_MAP,
        unit="char",
        name=name,
    )


# fmt: off
ELDER_FUTHARK_MAP = {
    "TH": "ᚦ", "NG": "ᛜ", "EO": "ᛇ", "A": "ᚨ", "B": "ᛒ", "C": "ᚲ", "K": "ᚲ", "D": "ᛞ", "E": "ᛖ",
    "F": "ᚠ", "G": "ᚷ", "H": "ᚺ", "I": "ᛁ", "J": "ᛃ", "Y": "ᛃ", "L": "ᛚ", "M": "ᛗ", "N": "ᚾ",
    "O": "ᛟ", "P": "ᛈ", "Q": "ᚲ", "R": "ᚱ", "S": "ᛊ", "T": "ᛏ", "U": "ᚢ", "V": "ᚹ", "W": "ᚹ",
    "X": "ᛉ", "Z": "ᛉ",
}
# fmt: on


def elder_futhark(*, name: str = "elder_futhark") -> Transform[str, str]:
    """Converts Latin text to Elder Futhark runes."""

    sorted_map_keys = sorted(ELDER_FUTHARK_MAP.keys(), key=len, reverse=True)

    def transform(text: str) -> str:
        upper_text = text.upper()
        result = []
        i = 0
        while i < len(upper_text):
            for key in sorted_map_keys:
                if upper_text.startswith(key, i):
                    result.append(ELDER_FUTHARK_MAP[key])
                    i += len(key)
                    break
            else:
                result.append(upper_text[i])
                i += 1
        return "".join(result)

    return Transform(transform, name=name, modality="text")


# fmt: off
GREEK_MAP = {
    "A": "Α", "B": "Β", "E": "Ε", "Z": "Ζ", "H": "Η", "I": "Ι", "K": "Κ",
    "M": "Μ", "N": "Ν", "O": "Ο", "P": "Ρ", "T": "Τ", "Y": "Υ", "X": "Χ",
    "a": "α", "b": "β", "e": "ε", "z": "ζ", "h": "η", "i": "ι", "k": "κ",
    "m": "μ", "n": "ν", "o": "ο", "p": "ρ", "r": "ρ", "s": "σ", "t": "τ",
    "u": "υ", "y": "γ", "x": "χ", "w": "ω", "c": "ς", "d": "δ", "f": "φ",
    "g": "γ", "l": "λ", "v": "β", "ph": "φ", "th": "θ", "ps": "ψ",
    "ch": "χ", "ks": "ξ",
}
# fmt: on


def greek_letters(*, name: str = "greek_letters") -> Transform[str, str]:
    """Replaces Latin letters with visually similar Greek letters."""

    sorted_map_keys = sorted(GREEK_MAP.keys(), key=len, reverse=True)

    def transform(text: str) -> str:
        result = ""
        i = 0
        while i < len(text):
            for key in sorted_map_keys:
                if text.startswith(key, i):
                    result += GREEK_MAP[key]
                    i += len(key)
                    break
            else:
                result += text[i]
                i += 1
        return result

    return Transform(transform, name=name, modality="text")


# fmt: off
FRAKTUR_MAP = {
    "A": "𝔄", "B": "𝔅", "C": "ℭ", "D": "𝔇", "E": "𝔈", "F": "𝔉", "G": "𝔊", "H": "ℌ",
    "I": "ℑ", "J": "𝔍", "K": "𝔎", "L": "𝔏", "M": "𝔐", "N": "𝔑", "O": "𝔒", "P": "𝔓",
    "Q": "𝔔", "R": "ℜ", "S": "𝔖", "T": "𝔗", "U": "𝔘", "V": "𝔙", "W": "𝔚", "X": "𝔛",
    "Y": "𝔜", "Z": "ℨ", "a": "𝔞", "b": "𝔟", "c": "𝔠", "d": "𝔡", "e": "𝔢", "f": "𝔣",
    "g": "𝔤", "h": "𝔥", "i": "𝔦", "j": "𝔧", "k": "𝔨", "l": "𝔩", "m": "𝔪", "n": "𝔫",
    "o": "𝔬", "p": "𝔭", "q": "𝔮", "r": "𝔯", "s": "𝔰", "t": "𝔱", "u": "𝔲", "v": "𝔳",
    "w": "𝔴", "x": "𝔵", "y": "𝔶", "z": "𝔷",
}
# fmt: on


def medieval(*, name: str = "medieval") -> Transform[str, str]:
    """Converts text to a Medieval (Fraktur/Blackletter) style."""

    return substitute(
        mapping=FRAKTUR_MAP,
        unit="char",
        name=name,
    )


# fmt: off
MONOSPACE_MAP = {
    "A": "𝙰", "B": "𝙱", "C": "𝙲", "D": "𝙳", "E": "𝙴", "F": "𝙵", "G": "𝙶", "H": "𝙷",
    "I": "𝙸", "J": "𝙹", "K": "𝙺", "L": "𝙻", "M": "𝙼", "N": "𝙽", "O": "𝙾", "P": "𝙿",
    "Q": "𝚀", "R": "𝚁", "S": "𝚂", "T": "𝚃", "U": "𝚄", "V": "𝚅", "W": "𝚆", "X": "𝚇",
    "Y": "𝚈", "Z": "𝚉", "a": "𝚊", "b": "𝚋", "c": "𝚌", "d": "𝚍", "e": "𝚎", "f": "𝚏",
    "g": "𝚐", "h": "𝚑", "i": "𝚒", "j": "𝚓", "k": "𝚔", "l": "𝚕", "m": "𝚖", "n": "𝚗",
    "o": "𝚘", "p": "𝚙", "q": "𝚚", "r": "𝚛", "s": "𝚜", "t": "𝚝", "u": "𝚞", "v": "𝚟",
    "w": "𝚠", "x": "𝚡", "y": "𝚢", "z": "𝚣", "0": "𝟶", "1": "𝟷", "2": "𝟸", "3": "𝟹",
    "4": "𝟺", "5": "𝟻", "6": "𝟼", "7": "𝟽", "8": "𝟾", "9": "𝟿",
}
# fmt: on


def monospace(*, name: str = "monospace") -> Transform[str, str]:
    """Converts text to a Monospace style using Unicode."""

    return substitute(
        mapping=MONOSPACE_MAP,
        unit="char",
        name=name,
    )


# fmt: off
SMALL_CAPS_MAP = {
    "a": "ᴀ", "b": "ʙ", "c": "ᴄ", "d": "ᴅ", "e": "ᴇ", "f": "ꜰ", "g": "ɢ",
    "h": "ʜ", "i": "ɪ", "j": "ᴊ", "k": "ᴋ", "l": "ʟ", "m": "ᴍ", "n": "ɴ",
    "o": "ᴏ", "p": "ᴘ", "q": "ǫ", "r": "ʀ", "s": "s", "t": "ᴛ", "u": "ᴜ",
    "v": "ᴠ", "w": "ᴡ", "x": "x", "y": "ʏ", "z": "ᴢ",
}
# fmt: on


def small_caps(*, name: str = "small_caps") -> Transform[str, str]:
    """Converts lowercase letters to Unicode small caps."""

    def transform(text: str) -> str:
        return "".join(SMALL_CAPS_MAP.get(char.lower(), char) for char in text)

    return Transform(transform, name=name, modality="text")


# fmt: off
WINGDINGS_MAP = {
    "A": "✌", "B": "👌", "C": "👍", "D": "👎", "E": "☜", "F": "☞", "G": "☝", "H": "☟", "I": "✋",
    "J": "☺", "K": "😐", "L": "☹", "M": "💣", "N": "☠", "O": "⚐", "P": "✈", "Q": "✏", "R": "✂",
    "S": "☎", "T": "✉", "U": "☔", "V": "✔", "W": "✖", "X": "✘", "Y": "✨", "Z": "⚡", "0": "⓪",
    "1": "①", "2": "②", "3": "③", "4": "④", "5": "⑤", "6": "⑥", "7": "⑦", "8": "⑧", "9": "⑨",
    "!": "❗", "?": "❓", ".": "●",
}
# fmt: on


def wingdings(*, name: str = "wingdings") -> Transform[str, str]:
    """Converts text to Wingdings-like symbols using a best-effort Unicode mapping."""

    def transform(text: str) -> str:
        return "".join(WINGDINGS_MAP.get(char.upper(), char) for char in text)

    return Transform(transform, name=name, modality="text")


# fmt: off
MORSE_MAP = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.",
    "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.",
    "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-",
    "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--", "Z": "--..", "0": "-----",
    "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....",
    "7": "--...", "8": "---..", "9": "----.", "'": ".----.", '"': ".-..-.", ":": "---...",
    "@": ".--.-.", ",": "--..--", ".": ".-.-.-", "!": "-.-.--", "?": "..--..", "-": "-....-",
    "/": "-..-.", "+": ".-.-.", "=": "-...-", "(": "-.--.", ")": "-.--.-", "&": ".-...",
    " ": "/",
}
MORSE_ERROR = "........"
# fmt: on


def morse_code(*, name: str = "morse_code") -> Transform[str, str]:
    """Converts text to Morse code."""

    def transform(text: str) -> str:
        text_clean = " ".join([line.strip() for line in str.splitlines(text)])
        return " ".join([MORSE_MAP.get(char, MORSE_ERROR) for char in text_clean.upper()])

    return Transform(transform, name=name, modality="text")


# fmt: off
NATO_MAP = {
    "A": "Alpha", "B": "Bravo", "C": "Charlie", "D": "Delta", "E": "Echo", "F": "Foxtrot",
    "G": "Golf", "H": "Hotel", "I": "India", "J": "Juliett", "K": "Kilo", "L": "Lima",
    "M": "Mike", "N": "November", "O": "Oscar", "P": "Papa", "Q": "Quebec", "R": "Romeo",
    "S": "Sierra", "T": "Tango", "U": "Uniform", "V": "Victor", "W": "Whiskey",
    "X": "X-ray","Y": "Yankee", "Z": "Zulu", "0": "Zero", "1": "One", "2": "Two",
    "3": "Three", "4": "Four", "5": "Five", "6": "Six", "7": "Seven", "8": "Eight",
    "9": "Nine", ".": "Stop", ",": "Comma", " ": "Space",
}
# fmt: on


def nato_phonetic(*, name: str = "nato_phonetic") -> Transform[str, str]:
    """Converts a string to the NATO phonetic alphabet."""

    def transform(text: str) -> str:
        return " ".join(NATO_MAP.get(char.upper(), char) for char in text)

    return Transform(transform, name=name, modality="text")


# fmt: off
MIRROR_MAP = {
    "a": "ɒ", "b": "d", "c": "ɔ", "d": "b", "e": "ɘ", "f": "Ꮈ", "g": "ǫ", "h": "h", "i": "i",
    "j": "į", "k": "ʞ", "l": "l", "m": "m", "n": "n", "o": "o", "p": "q", "q": "p", "r": "ɿ",
    "s": "ƨ", "t": "ƚ", "u": "u", "v": "v", "w": "w", "x": "x", "y": "γ", "z": "ƹ", "A": "A",
    "B": "ᙠ", "C": "Ɔ", "D": "ᗡ", "E": "Ǝ", "F": "ꟻ", "G": "Ꭾ", "H": "H", "I": "I", "J": "L",
    "K": "ꓘ", "L": "J", "M": "M", "N": "И", "O": "O", "P": "ꟼ", "Q": "Ọ", "R": "Я", "S": "Ƨ",
    "T": "T", "U": "U", "V": "V", "W": "W", "X": "X", "Y": "Y", "Z": "Ƹ", "1": "Ɩ", "2": "S",
    "3": "Ɛ", "4": "ㄣ", "5": "ટ", "6": "9", "7": "Γ", "8": "8", "9": "6", "0": "0", "(": ")",
    ")": "(", "[": "]", "]": "[", "{": "}", "}": "{", "<": ">", ">": "<", "?": "؟", "!": "¡",
}
# fmt: on


def mirror(*, name: str = "mirror") -> Transform[str, str]:
    """Mirrors text horizontally using reversed string and Unicode counterparts."""

    def transform(text: str) -> str:
        reversed_text = text[::-1]
        return "".join(MIRROR_MAP.get(char, char) for char in reversed_text)

    return Transform(transform, name=name, modality="text")


# fmt: off
LEET_SPEAK_MAP = {
    "a": ["4", "@"], "b": ["8"], "e": ["3"], "g": ["9"], "i": ["1", "!"],
    "l": ["1", "|"], "o": ["0"], "s": ["5", "$"], "t": ["7"], "z": ["2"],
}
# fmt: on


def leet_speak(
    *,
    deterministic: bool = False,
    seed: int | None = None,
    name: str = "leet_speak",
) -> Transform[str, str]:
    """Converts text to leetspeak."""
    return substitute(
        mapping=LEET_SPEAK_MAP,
        unit="char",
        case_sensitive=False,
        deterministic=deterministic,
        seed=seed,
        name=name,
    )


def pig_latin(*, name: str = "pig_latin") -> Transform[str, str]:
    """Converts text to Pig Latin."""

    def _to_pig_latin_word(word: str) -> str:
        if not word or not word.isalpha():
            return word
        vowels = "aeiouAEIOU"
        if word[0] in vowels:
            return word + "way"
        for i, char in enumerate(word):
            if char in vowels:
                return word[i:] + word[:i] + "ay"
        return word + "ay"

    def transform(text: str) -> str:
        words = re.findall(r"\w+|[^\w\s]", text)
        return "".join(_to_pig_latin_word(word) for word in words)

    return Transform(transform, name=name, modality="text")
