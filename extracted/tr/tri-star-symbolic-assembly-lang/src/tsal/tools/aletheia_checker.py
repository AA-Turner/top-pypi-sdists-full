import difflib
import re
from pathlib import Path

TARGET = "aletheia"
# Known common misspellings that should be flagged immediately
COMMON_TYPOS = {
    "athalaya",  # seen in various docs
    "athaleia",
    "alethei",  # truncated
}

def is_typo(word: str) -> bool:
    lw = word.lower()
    if lw == TARGET:
        return False
    if lw in COMMON_TYPOS:
        return True
    ratio = difflib.SequenceMatcher(None, lw, TARGET).ratio()
    return ratio >= 0.7

def scan_file(path: Path) -> list[tuple[int, str]]:
    results = []
    pattern = re.compile(r"[A-Za-z_-]+")
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for lineno, line in enumerate(f, 1):
            for word in pattern.findall(line):
                if is_typo(word):
                    results.append((lineno, line.rstrip()))
                    break
    return results

def find_typos(root: Path) -> dict[str, list[tuple[int, str]]]:
    typos = {}
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in {
            ".py",
            ".md",
            ".txt",
            ".json",
            ".yaml",
            ".yml",
        }:
            found = scan_file(path)
            if found:
                typos[str(path)] = found
    return typos

if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[3]
    hits = find_typos(repo_root)
    for filepath, items in hits.items():
        for lineno, line in items:
            print(f"{filepath}:{lineno}: {line}")
