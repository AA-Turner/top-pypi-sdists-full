#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Content checks for a translated prediction JSON file against the English source.

Complements a key/value COUNT check: this compares each English string with the string at the SAME
position in the translated file (dicts are walked in order, lists by index - so it works even though
keys without '_' are translated) and flags:
  UNTRANSLATED   text is identical to the English, or still mostly Latin letters
  TRUNCATED?     translation is much shorter than the English (likely cut off / sentences dropped)
  SENTENCES?     translation has clearly fewer sentence endings (. ! ? ।) than the English
  NUMBERS        numbers in the English (houses, degrees, years...) missing in the translation
                 (native-script digits like ३, ૩, ୩ are treated as the same digit)
  MARKUP         <br>, &lt; / &gt;, {placeholders} differ between English and translation
  STRUCTURE      the two files do not line up at this position (different shape / type)

HOW TO RUN
  VSCode : edit ENGLISH_FILE and TRANSLATED_FILES below, open this file and press Run (the play button)
           or F5. Nothing else is needed.
  Command line (optional, overrides the settings below):
           python check_translation_quality.py prediction_msgs_en.json prediction_msgs_mr.json [more files...]
Writes one CSV report per translated file (<file>.check.csv, opens in Excel) and prints a summary.
"""
import csv
import json
import os
import re
import sys
import unicodedata

# ===================================================================================================
# SETTINGS - edit these for VSCode (ignored when file names are given on the command line)
# ===================================================================================================
# Folder that holds the files. None = the jhora language folder (const._LANGUAGE_PATH) if jhora can be
# imported, otherwise the folder this script is in.
LANGUAGE_FOLDER = None
ENGLISH_FILE = "prediction_msgs_en.json"
TRANSLATED_FILES = [
    "prediction_msgs_sa.json",
    # "prediction_msgs_mr.json",
    # "prediction_msgs_gu.json",
    # "prediction_msgs_pa.json",
]
# Thresholds
MIN_LEN_FOR_RATIO = 80        # only length-check English strings at least this long
LENGTH_RATIO_MIN = 0.60       # translation shorter than 60% of the English -> TRUNCATED?
SENTENCE_RATIO_MIN = 0.60     # fewer than 60% of the English sentence endings -> SENTENCES?
MIN_SENTENCES_FOR_CHECK = 3   # only sentence-check English strings with at least this many sentences
LATIN_RATIO_MAX = 0.50        # more than 50% Latin letters in the translation -> UNTRANSLATED
# ===================================================================================================

_SENT_END = re.compile(r"[.!?\u0964\u0965](?=\s|$)")        # . ! ? ।  ॥
_MARKUP = re.compile(r"<[^>]+>|&[a-z]+;|\{[^}]*\}")
_ISSUES = ("STRUCTURE", "UNTRANSLATED", "TRUNCATED?", "SENTENCES?", "NUMBERS", "MARKUP")


def _norm_digits(s):
    """Converts any Unicode decimal digit (Devanagari, Gujarati, Odia, ...) to ASCII."""
    return "".join(str(unicodedata.digit(c)) if c.isdigit() else c for c in s)


def _numbers(s):
    return sorted(re.findall(r"\d+", _norm_digits(s)))


def _letters(s):
    return [c for c in s if c.isalpha()]


def _latin_ratio(s):
    letters = _letters(s)
    if not letters:
        return 0.0
    return sum(1 for c in letters if "LATIN" in unicodedata.name(c, "")) / len(letters)


def check_pair(en, tr):
    """Returns a list of (issue, detail) for one English / translated string pair."""
    issues = []
    if not _letters(en):
        return issues                                   # nothing translatable (numbers, symbols)
    if tr.strip() == en.strip():
        return [("UNTRANSLATED", "identical to English")]
    lr = _latin_ratio(tr)
    if lr > LATIN_RATIO_MAX:
        issues.append(("UNTRANSLATED", f"{lr:.0%} Latin letters"))
    if len(en) >= MIN_LEN_FOR_RATIO and len(tr) < LENGTH_RATIO_MIN * len(en):
        issues.append(("TRUNCATED?", f"length {len(tr)} vs English {len(en)} ({len(tr)/len(en):.0%})"))
    en_s, tr_s = len(_SENT_END.findall(en)), len(_SENT_END.findall(tr))
    if en_s >= MIN_SENTENCES_FOR_CHECK and tr_s < SENTENCE_RATIO_MIN * en_s:
        issues.append(("SENTENCES?", f"{tr_s} sentence endings vs English {en_s}"))
    missing = list(_numbers(en))
    for n in _numbers(tr):
        if n in missing:
            missing.remove(n)
    if missing:
        issues.append(("NUMBERS", "missing: " + ", ".join(missing)))
    en_m, tr_m = sorted(_MARKUP.findall(en)), sorted(_MARKUP.findall(tr))
    if en_m != tr_m:
        issues.append(("MARKUP", f"English {en_m} vs translation {tr_m}"))
    return issues


def walk(en, tr, path, out):
    """Walks both trees in parallel by position, appending (path, issue, detail, en, tr) to out."""
    if isinstance(en, dict) and isinstance(tr, dict):
        en_items, tr_items = list(en.items()), list(tr.items())
        if len(en_items) != len(tr_items):
            out.append((path, "STRUCTURE", f"{len(en_items)} vs {len(tr_items)} keys", "", ""))
        for (ek, ev), (tk, tv) in zip(en_items, tr_items):
            p = f"{path}/{ek}"
            if "_" in ek or ek.isdigit():
                if ek != tk:
                    out.append((p, "STRUCTURE", f"key changed to {tk!r}", ek, tk))
            else:
                for issue, detail in check_pair(ek, tk):
                    out.append((p + " (key)", issue, detail, ek, tk))
            walk(ev, tv, p, out)
    elif isinstance(en, list) and isinstance(tr, list):
        if len(en) != len(tr):
            out.append((path, "STRUCTURE", f"{len(en)} vs {len(tr)} items", "", ""))
        for i, (ev, tv) in enumerate(zip(en, tr)):
            walk(ev, tv, f"{path}[{i}]", out)
    elif isinstance(en, str) and isinstance(tr, str):
        for issue, detail in check_pair(en, tr):
            out.append((path, issue, detail, en, tr))
    elif type(en) is not type(tr):
        out.append((path, "STRUCTURE", f"{type(en).__name__} vs {type(tr).__name__}", "", ""))


def _language_folder():
    if LANGUAGE_FOLDER:
        return LANGUAGE_FOLDER
    try:
        from jhora import const
        return const._LANGUAGE_PATH
    except Exception:
        return os.path.dirname(os.path.abspath(__file__))


def _resolve(name, folder):
    """A bare file name is looked up in the language folder; a path is used as it is."""
    if os.path.isabs(name) or os.path.dirname(name):
        return name
    return os.path.join(folder, name)


def _load(path):
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    folder = _language_folder()
    if len(argv) >= 2:                       # command line: <english file> <translated file> [more...]
        english, translated = argv[0], argv[1:]
    else:                                    # VSCode / no arguments: use the settings at the top
        english, translated = ENGLISH_FILE, TRANSLATED_FILES
    if not translated:
        print("No translated files listed - edit TRANSLATED_FILES at the top of the script.")
        return 1
    english = _resolve(english, folder)
    print(f"English file: {english}")
    try:
        en = _load(english)
    except Exception as e:
        print(f"❌ Cannot read the English file: {type(e).__name__}: {e}")
        return 1
    status = 0
    for name in translated:
        tr_file = _resolve(name, folder)
        print(f"\n=== {tr_file} ===")
        try:
            tr = _load(tr_file)
        except Exception as e:
            print(f"  ❌ Cannot read this file: {type(e).__name__}: {e}")
            status = 1
            continue
        rows = []
        walk(en, tr, "", rows)
        report = tr_file + ".check.csv"
        try:
            with open(report, "w", encoding="utf-8-sig", newline="") as f:   # utf-8-sig: opens cleanly in Excel
                w = csv.writer(f)
                w.writerow(["path", "issue", "detail", "english", "translation"])
                w.writerows(rows)
        except PermissionError:
            print(f"  ❌ Cannot write {report} - close it in Excel and run again.")
            status = 1
            continue
        counts = {}
        for r in rows:
            counts[r[1]] = counts.get(r[1], 0) + 1
        if not rows:
            print("  No issues found.")
        for issue in _ISSUES:
            if issue in counts:
                print(f"  {issue:<13} {counts[issue]}")
        print(f"  Report: {report}")
    return status


if __name__ == "__main__":
    sys.exit(main())
