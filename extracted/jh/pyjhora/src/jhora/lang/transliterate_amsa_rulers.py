#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Creates amsa_rulers_<lang>.json for several languages by TRANSLITERATING amsa_rulers_hi.json (Devanagari).

amsa_rulers holds only proper names (deities, sages, nadiamsa names), so a translation model would turn them into
ordinary words; converting the Hindi names letter by letter keeps them correct - the same idea as
transliterate_list_values.py.

Kept unchanged: the JSON keys ("2", "3" ... "150"), the number of names in every list, symbols, digits, Latin text.
A target language whose script is Devanagari (mr, ne, sa ...) gets a plain copy of the Hindi file.
An existing output file is backed up as <file>.bak. A language whose output would not have the same structure
is skipped with a message, nothing written for it.

HOW TO RUN (VSCode: press Run).  Needs:  python -m pip install aksharamukha
"""
import json
import os
import shutil
import sys
import warnings

SOURCE_FILE = "amsa_rulers_hi.json"
TARGETS = [                                   # aksharamukha script names - "Santali" is Ol Chiki
    {"lang": "sat", "script": "Santali"},
]
DRY_RUN = False


def _lang_path():
    try:
        from jhora import const
        return const._LANGUAGE_PATH
    except Exception:
        return os.path.dirname(os.path.abspath(__file__)) + os.sep


def _convert(transliterate, text, script):
    if script == "Devanagari":
        return text
    if script == "Gurmukhi":                  # same clean-up as transliterate_list_values.py
        text = text.replace("ष", "श").replace("ृ", "्रि").replace("ऋ", "रि")
    with warnings.catch_warnings():
        warnings.simplefilter("error")        # an unknown script name must stop, not silently return Hindi
        return transliterate.process("Devanagari", script, text)


def main():
    try:
        from aksharamukha import transliterate
    except ImportError:
        sys.exit("Needs aksharamukha:  python -m pip install aksharamukha")
    folder = _lang_path()
    with open(os.path.join(folder, SOURCE_FILE), encoding="utf-8-sig") as f:
        src = json.load(f)
    print(f"{SOURCE_FILE}: {len(src)} keys, {sum(len(v) for v in src.values())} names")
    for t in TARGETS:
        lang, script = t["lang"], t["script"]
        try:
            out = {k: [_convert(transliterate, name, script) for name in v] for k, v in src.items()}
        except Exception as e:
            print(f"   {lang}: SKIPPED - {type(e).__name__}: {e}  (check the script name)")
            continue
        bad = [k for k in src if len(out[k]) != len(src[k])]
        same = sum(a == b for k in src for a, b in zip(src[k], out[k]))
        if bad:
            print(f"   {lang}: SKIPPED - list lengths changed for keys {bad}")
            continue
        if script != "Devanagari" and same == sum(len(v) for v in src.values()):
            print(f"   {lang}: SKIPPED - nothing was converted (wrong script name?)")
            continue
        path = os.path.join(folder, f"amsa_rulers_{lang}.json")
        if not DRY_RUN:
            if os.path.exists(path):
                shutil.copy2(path, path + ".bak")
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                json.dump(out, f, ensure_ascii=False, indent=4)
        first = next(iter(out))
        print(f"   {lang} ({script}): written {os.path.basename(path)}  e.g. {src[first][:2]} -> {out[first][:2]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
