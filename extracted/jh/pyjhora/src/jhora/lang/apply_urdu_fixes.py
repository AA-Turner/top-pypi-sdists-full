#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Replaces the English / half-English values of selected keys in msg_strings_ur.txt with Urdu.

Only the VALUE after the first '=' of a listed key is changed. Keys, other lines, '#' lines, line endings and the
leading spaces of a value are kept. A backup (msg_strings_ur.txt.bak) is written first. Running it again changes nothing.

HOW TO RUN (VSCode: press Run).  The file is looked up in the jhora language folder (const._LANGUAGE_PATH) if jhora
can be imported, otherwise next to this script. To use it on another file, change FILE below.
To add more fixes later, add more  "key": "urdu value"  lines to FIXES and run it again.
"""
import os
import re
import shutil
import sys

# ===================================================================================================
FILE = "msg_strings_ur.txt"
LANGUAGE_FOLDER = None            # None = jhora language folder if importable, else this script's folder
ADD_MISSING_KEYS = False          # True: a listed key that is not in the file is appended at the end
FIXES = {
    "vimsamsa_str": "وِنشانش (D20)",
    "akshavedamsa_str": "اکشویدانش (D45)",
    "dwadas_dwadasamsa_str": "دوادش دوادشانش (D144)",
    "ayanamsa_tooltip_str": "فہرست میں سے ایانانش کا طریقہ منتخب کریں",
    "sthree_dheerga_match_str": "اسٹری دیرگھ کوٹ",
    "amatya_karaka_str": "امتیہ کارک",
    "putra_karaka_str": "پُتر کارک",
    "vimsottari_str": "وِنشوتری",
    "60hourly_str": "ششٹی ہورا پرویش",
    "bhava_arudha_a7_str": "دارا پد",
    "bhava_arudha_a11_str": "لابھ پد",
    "vimsopaka_bala_str": "ورگ انش وِنشوپک بل",
    "vimsopaka_score_str": "وِنشوپک بل",
    "naisargika_str": "نیسرگک",
    "navamsa_str": "نوانش",
    "gl_panchang_str": "گرہ لاگھَو",
    "kshaya_month_str": "(کشے)",
    "pitru_dosha_str": "پتر دوش",
    "vakra_gathi_change_str": "وکر گتی تبدیلی",
    "vaiseshikamsa_bala_str": "ورگ انش وَیشیشکانش بل",
    "vaiseshikamsa_score_str": "وِنشوپک بل",
    "nisargayu_str": "نیسرگایو",
    "nisargika_dhasa_option1_str": "نیسرگک دشا کے انتر دشا کے اختیارات درج ذیل ہیں:",
    "rbv_dhasa_option_str": "راشی بھُکتی ویریشن کا استعمال کریں",
}
# ===================================================================================================

_ALLOWED_LATIN = re.compile(r"\bD\d+\b")          # divisional-chart codes stay in Latin letters


def _folder():
    if LANGUAGE_FOLDER:
        return LANGUAGE_FOLDER
    try:
        from jhora import const
        return const._LANGUAGE_PATH
    except Exception:
        return os.path.dirname(os.path.abspath(__file__))


def main():
    path = os.path.join(_folder(), FILE)
    if not os.path.exists(path):
        print(f"❌ {path} not found.")
        return 1
    # sanity check of the fixes themselves
    for k, v in FIXES.items():
        left = _ALLOWED_LATIN.sub("", v)
        if re.search(r"[A-Za-z]", left):
            print(f"❌ the fix for {k!r} still contains Latin letters: {v!r} - nothing was changed.")
            return 1
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        text = f.read()
    lines = text.splitlines(keepends=True)
    changed, same, seen = [], [], set()
    out = []
    for raw in lines:
        body = raw.rstrip("\r\n")
        eol = raw[len(body):]
        if body.lstrip().startswith("#") or "=" not in body:
            out.append(raw)
            continue
        key, value = body.split("=", 1)
        k = key.strip()
        if k in FIXES:
            seen.add(k)
            lead = value[:len(value) - len(value.lstrip())]          # keep the value's own leading spaces
            new_value = lead + FIXES[k]
            # protected pieces of the old value must survive: (D20) style codes
            for tok in _ALLOWED_LATIN.findall(value):
                if tok not in new_value:
                    print(f"⚠️ {k}: the old value had {tok}, the fix does not - kept as is.")
                    new_value = value
            if new_value == value:
                same.append(k)
                out.append(raw)
            else:
                changed.append((k, value, new_value))
                out.append(f"{key}={new_value}{eol}")
        else:
            out.append(raw)
    missing = [k for k in FIXES if k not in seen]
    if missing and ADD_MISSING_KEYS:
        eol = "\r\n" if "\r\n" in text else "\n"
        if out and not out[-1].endswith(("\n", "\r")):
            out[-1] += eol
        for k in missing:
            out.append(f"{k}={FIXES[k]}{eol}")
    new_text = "".join(out)
    # verification: same keys in the same order, only listed keys differ
    def keys(t): return [l.split("=", 1)[0].strip() for l in t.splitlines() if "=" in l and not l.lstrip().startswith("#")]
    if not ADD_MISSING_KEYS and keys(new_text) != keys(text):
        print("❌ internal check failed (keys changed) - nothing was written.")
        return 1
    if changed:
        shutil.copy2(path, path + ".bak")
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new_text)
    print(f"File: {path}")
    print(f"  changed: {len(changed)} | already correct: {len(same)} | listed key not in the file: {len(missing)}")
    for k, old, new in changed:
        print(f"   {k}:  {old.strip()!r}  ->  {new.strip()!r}")
    if missing:
        print("   not found in the file" + (" (appended)" if ADD_MISSING_KEYS else " (left out - set ADD_MISSING_KEYS = True to add them)") + ":",
              ", ".join(missing))
    if changed:
        print(f"  backup: {FILE}.bak")
    return 0


if __name__ == "__main__":
    sys.exit(main())
