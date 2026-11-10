#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Adds the resource string  nepal_bikram_sambat_str  (the name of the Nepal Bikram Sambat calendar) to every
msg_strings_<code>.txt of the lang folder.

vedic_calendar.py and calendar_tab.py already ask for this key with the English text "Nepal Bikram Sambat" as the
fallback, so nothing breaks without it - but every language would show the English name. The key is the calendar name in
the calendar drop-down ("<name> <calendar_str>") and inside the date text of a day: "Kartik 1 (<name>)".

The line is inserted after the  bangladesh_str=  line (the other calendar names), or appended when that line is missing.
A language that is not in NAMES gets the English name and a warning. A key that is already there is kept unless
OVERWRITE_EXISTING = True. Line endings, the encoding and everything else in the file are kept; running the script again
changes nothing.

These translations are mine: a reader of each language should check them. Month names are NOT resources here: they are
constants in the two calendar files (English transliteration; Devanagari when the UI language is Nepali).

HOW TO RUN (VSCode: press Run). The lang folder is taken from jhora (const._LANGUAGE_PATH), else the folder of this script.
Set DRY_RUN = True to only list what would change. MAKE_BACKUP = True writes <file>.bak next to each changed file (the
lang folder is synced to GitHub, so git is normally the backup).
"""
import glob
import os
import re
import shutil
import sys

KEY = "nepal_bikram_sambat_str"
AFTER_KEY = "bangladesh_str"
OVERWRITE_EXISTING = False
DRY_RUN = False
MAKE_BACKUP = False
LANGUAGE_FOLDER = None            # None = const._LANGUAGE_PATH if jhora can be imported, else this script's folder

NAMES = {
    "en": "Nepal Bikram Sambat",
    "ne": "नेपाल विक्रम सम्वत्",
    "hi": "नेपाल विक्रम संवत",
    "mr": "नेपाळ विक्रम संवत",
    "sa": "नेपालविक्रमसंवत्",
    "bn": "নেপাল বিক্রম সংবৎ",
    "as": "নেপাল বিক্ৰম সংবৎ",
    "gu": "નેપાળ વિક્રમ સંવત",
    "or": "ନେପାଳ ବିକ୍ରମ ସମ୍ବତ",
    "pa": "ਨੇਪਾਲ ਬਿਕਰਮ ਸੰਮਤ",
    "ta": "நேபாள விக்ரம் சம்வத்",
    "te": "నేపాల్ విక్రమ సంవత్",
    "ka": "ನೇಪಾಳ ವಿಕ್ರಮ ಸಂವತ್",
    "ml": "നേപ്പാൾ വിക്രം സംവത്",
    "ur": "نیپال بکرمی سمت",
}


def _folder():
    if LANGUAGE_FOLDER:
        return LANGUAGE_FOLDER
    try:
        from jhora import const
        return const._LANGUAGE_PATH
    except Exception:
        return os.path.dirname(os.path.abspath(__file__))


def process(path, code):
    with open(path, "rb") as f:
        raw = f.read()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw[3:].decode("utf-8") if bom else raw.decode("utf-8")
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = text.splitlines(keepends=True)
    name = NAMES.get(code)
    warn = ""
    if name is None:
        name, warn = NAMES["en"], f" (no translation for '{code}' in NAMES - English name used)"
    key_rx = re.compile(r"^\s*" + re.escape(KEY) + r"\s*=(.*)$")
    after_rx = re.compile(r"^\s*" + re.escape(AFTER_KEY) + r"\s*=")
    found = [i for i, l in enumerate(lines) if key_rx.match(l.rstrip("\r\n"))]
    if found:
        i = found[0]
        old = key_rx.match(lines[i].rstrip("\r\n")).group(1)
        if old.strip() == name:
            return "already there", warn
        if not OVERWRITE_EXISTING:
            return f"kept existing value {old.strip()!r}", warn
        body = lines[i].rstrip("\r\n")
        eol = lines[i][len(body):]
        lines[i] = f"{KEY}={name}{eol}"
        action = "value replaced"
    else:
        pos = next((i for i, l in enumerate(lines) if after_rx.match(l)), None)
        new = f"{KEY}={name}{nl}"
        if pos is None:
            if lines and not lines[-1].endswith(("\n", "\r")):
                lines[-1] += nl
            lines.append(new)
            action = f"added at the end ({AFTER_KEY} not found)"
        else:
            if not lines[pos].endswith(("\n", "\r")):          # the anchor line is the last line without a newline
                lines[pos] += nl
                new = f"{KEY}={name}"
            lines.insert(pos + 1, new)
            action = f"added after {AFTER_KEY}"
    out = "".join(lines).encode("utf-8")
    if bom:
        out = b"\xef\xbb\xbf" + out
    if not DRY_RUN:
        if MAKE_BACKUP:
            shutil.copy2(path, path + ".bak")
        with open(path, "wb") as f:
            f.write(out)
    return action, warn


def main():
    folder = _folder()
    files = sorted(glob.glob(os.path.join(folder, "msg_strings_*.txt")))
    print(f"{KEY}  ->  {len(files)} msg_strings files in {folder}" + ("   [DRY RUN - nothing is written]" if DRY_RUN else ""))
    if not files:
        print("No msg_strings_*.txt found - check LANGUAGE_FOLDER.")
        return 1
    changed = 0
    for p in files:
        code = re.match(r"msg_strings_(.+)\.txt$", os.path.basename(p)).group(1)
        action, warn = process(p, code)
        if not (action.startswith("already") or action.startswith("kept")):
            changed += 1
        print(f"   {code:4} {action}{warn}")
    print(f"\n{changed} file(s) {'would be ' if DRY_RUN else ''}changed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
