#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Compares amsa_rulers_en.json with amsa_rulers_hi.json position by position and writes amsa_compare.csv.

amsa_rulers lists are looked up BY POSITION (e.g. the 150 nadiamsa names), so every language's list must be in the same
order as the English one. A list can have the right number of names and still be shifted - one name skipped here,
two names merged there. This script transliterates each Hindi name to Latin letters, compares it with the English name
at the same position, and reports:
  * per key: how many positions look different, and whether the Hindi list fits the English better when shifted by 1 or 2
  * amsa_compare.csv: key, position, English, Hindi, similarity, flag  (open it in Excel; sort/filter the flag column)
A low similarity can also be a different spelling of the same name - the shift test is the reliable signal.

HOW TO RUN (VSCode: press Run). Needs:  python -m pip install aksharamukha
"""
import csv
import difflib
import json
import os
import re
import sys
import warnings

EN_FILE, HI_FILE, OUT = "amsa_rulers_en.json", "amsa_rulers_hi.json", "amsa_compare.csv"
LOW = 0.55          # similarity below this is flagged
WINDOW = 12         # shift test window


def _folder():
    try:
        from jhora import const
        return const._LANGUAGE_PATH
    except Exception:
        return os.path.dirname(os.path.abspath(__file__)) + os.sep


_FOLD = (("sh", "s"), ("ch", "c"), ("th", "t"), ("dh", "d"), ("bh", "b"), ("kh", "k"), ("gh", "g"), ("ph", "p"))


def _fold(s):
    for a, b in _FOLD:
        s = s.replace(a, b)
    return re.sub(r"[^a-z]", "", s)


def norm_en(s):
    s = re.sub(r"\(.*?\)", "", s).lower().replace("w", "v").replace("ee", "i").replace("oo", "u").replace("aa", "a")
    return _fold(s)


def norm_hi(s, T):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = T.process("Devanagari", "ISO", re.sub(r"\(.*?\)", "", s)).lower()
    for a, b in (("ā", "a"), ("ī", "i"), ("ū", "u"), ("ṛ", "ri"), ("ś", "s"), ("ṣ", "s"), ("ṇ", "n"), ("ṭ", "t"), ("ḍ", "d"),
                 ("ṃ", "n"), ("ṅ", "n"), ("ñ", "n"), ("ḥ", "h"), ("ḷ", "l"), ("ṁ", "n")):
        r = r.replace(a, b)
    return _fold(r)


sim = lambda a, b: difflib.SequenceMatcher(None, a, b).ratio()


def main():
    try:
        from aksharamukha import transliterate as T
    except ImportError:
        sys.exit("Needs aksharamukha:  python -m pip install aksharamukha")
    folder = _folder()
    en = json.load(open(os.path.join(folder, EN_FILE), encoding="utf-8-sig"))
    hi = json.load(open(os.path.join(folder, HI_FILE), encoding="utf-8-sig"))
    rows, summary = [], []
    for k in en:
        if k not in hi:
            print(f"key {k}: missing in {HI_FILE}")
            continue
        E = [norm_en(x) for x in en[k]]
        H = [norm_hi(x, T) for x in hi[k]]
        n = min(len(E), len(H))
        s0 = [sim(E[i], H[i]) for i in range(n)]
        for i in range(n):
            rows.append([k, i, en[k][i], hi[k][i], f"{s0[i]:.2f}", "LOW" if s0[i] < LOW else ""])
        low = sum(x < LOW for x in s0)
        msg = ""
        if len(E) >= 20:
            worst = []
            for w in range(0, n - WINDOW + 1, WINDOW):
                best = {}
                for off in (-2, -1, 0, 1, 2):
                    sc = [sim(E[i], H[i + off]) for i in range(w, w + WINDOW) if 0 <= i + off < len(H)]
                    best[off] = sum(sc) / max(1, len(sc))
                bo = max(best, key=best.get)
                if bo != 0 and best[bo] > best[0] + 0.12:
                    worst.append(f"positions {w}-{w + WINDOW - 1}: fits better shifted by {bo:+d}")
            msg = "; ".join(worst)
        summary.append((k, len(en[k]), len(hi[k]), low, msg))
    with open(os.path.join(folder, OUT), "w", encoding="utf-8-sig", newline="") as f:
        csv.writer(f).writerows([["key", "position", "English", "Hindi", "similarity", "flag"]] + rows)
    print(f"{'key':>4} {'EN':>4} {'HI':>4} {'low':>4}  shifted stretches")
    for k, a, b, low, msg in summary:
        print(f"{k:>4} {a:>4} {b:>4} {low:>4}  {msg or '-'}")
    print(f"\nwritten: {OUT}")


if __name__ == "__main__":
    main()
