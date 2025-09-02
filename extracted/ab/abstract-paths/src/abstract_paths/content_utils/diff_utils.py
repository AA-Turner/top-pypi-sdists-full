import os
from typing import *
def apply_replacements_to_lines(og_lines: List[str], matches: List[Dict[str, Any]], adds: List[str]) -> List[str]:
    """Replace matched lines (1-based) with adds.
       - If len(adds) == 1: reuse for all matches.
       - If len(adds) == len(matches): zip 1:1 in order.
       - Else: fall back to reusing the first add (or raise/log).
    """
    if not matches:
        return og_lines

    if not adds:
        return og_lines  # nothing to apply

    if len(adds) == 1:
        rep = adds[0]
        for m in matches:
            og_lines[m["line"] - 1] = rep
        return og_lines

    if len(adds) == len(matches):
        for m, rep in zip(matches, adds):
            og_lines[m["line"] - 1] = rep
        return og_lines

    # mismatch; be forgiving: reuse first add
    rep = adds[0]
    for m in matches:
        og_lines[m["line"] - 1] = rep
    return og_lines


def write_text_atomic(path: str, text: str):
    tmp = f"{path}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)
