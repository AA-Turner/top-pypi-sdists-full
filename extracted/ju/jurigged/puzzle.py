"""________________
______________
_______,_______
______.___________
_____________
_______________,
_________________
___________,______
________________."""

orig_code = """
debcb gi khjbc ebcb
sbbk qbnbade deb
ilcoamb, a ihlcmb
bXgidi. jb eaVb qlgfd
decbb cbibacme
oamgfgdgbi ih oac,
qld go tp mhffbarlbi
rbd debgc jap, jb jgff
mhtb aWap jgde ?bch.

THEY JUST ARE NOT
ABLE TO SEE MY VISION.
THIS COULD CHANGE
EVERYTHING, BUT SOME
ARE _UIC_ TO FEAR
WE NEED DOUBLE THE
RESEARCH

PROJECT
SOURCE
"""


mapping = {
    "a": "A",
    "b": "E",
    "c": "R",
    "d": "T",
    "e": "H",
    "f": "L",
    "g": "I",
    "h": "O",
    "i": "S",
    "j": "W",
    "k": "P",
    "l": "U",
    "m": "C",
    "n": "N",
    "o": "F",
    "p": "Y",
    "q": "B",
    "r": "G",
    "s": "D",
    "t": "M",
    "u": "u",
}


def main():
    code = orig_code
    for k, v in mapping.items():
        code = code.replace(k, v)
    print(code)


if __name__ == "__main__":
    main()
