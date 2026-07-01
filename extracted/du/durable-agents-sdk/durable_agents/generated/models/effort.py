from enum import Enum

class Effort(str, Enum):
    Quick = "quick",
    Standard = "standard",
    Deep = "deep",
    Exhaustive = "exhaustive",

