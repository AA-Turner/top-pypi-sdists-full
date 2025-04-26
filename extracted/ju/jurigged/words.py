from collections import Counter


def scrabble(words, letters):
    letters = Counter(letters)
    matches = [w for w in words if (wc := Counter(w)) & letters == wc]
    matches.sort(key=len)
    for m in matches:
        print(m)
    print(f"\x1b[1;32m{len(matches) = }")
    return matches[-1] if matches else None


def main(words):
    return scrabble(words, "develoop")


if __name__ == "__main__":
    print("Reading words...")
    wfile = "/usr/share/dict/words"
    words = [w.strip() for w in open(wfile).readlines()]
    print(f"{len(words)} words read!")
    print(main(words=words))
