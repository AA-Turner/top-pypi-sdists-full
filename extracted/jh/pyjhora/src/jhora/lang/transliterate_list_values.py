#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Creates list_values_<lang>.txt for MULTIPLE target languages in one run, by TRANSLITERATING
list_values_hi.txt (Devanagari) into each target script, instead of machine-translating it.

Why: list_values holds proper names (planets, rasis, nakshatras, tithis, years, and now the Nanakshahi /
Bangladesh / Nepal Bikram Sambat civil-calendar month names). Translation models turn them into ordinary
words ("Sagittarius" -> "straw", "Dhuma" -> "poisonous"). The Hindi file already has the correct Sanskrit /
regional-calendar names; converting them letter by letter keeps them correct. English Romanized spelling
(e.g. "Harh", "Chet") is NOT used as a source: it is phonemically ambiguous (aspirated/retroflex/vowel
length are all lost), so aksharamukha is only ever given the Devanagari text to convert.

Rules, unchanged from the single-language version:
  - lines starting with '#', blank lines and lines without '=' are copied unchanged
  - "key=value": the key stays as it is; only the value is transliterated
  - symbols (♈ ☉ ...), Latin text, digits, commas and spaces are kept, so list item counts never change
  - LANGUAGE_OVERRIDES[lang] replaces whole values with forms that differ in that language (e.g. Punjabi
    day names); an override with a different item count is skipped with a warning, per language

NEW in this version: TARGETS is a list of {lang, script} dicts instead of one LANG_SUFFIX/TARGET_SCRIPT pair.
The script loops over every target in one run and prints one summary table at the end. Nothing else about
the single-language behaviour changes - a target with a problem does not stop the others.

Needs:  python -m pip install aksharamukha
Afterwards: check the file(s) and edit the *_SHORT_* lines by hand, as before.
"""
import os
import shutil
import sys

# ===================================================================================================
# CONFIGURATION
# ===================================================================================================
SOURCE_FILE = "list_values_hi.txt"
ENGLISH_FILE = "list_values_en.txt"   # only used to check that no key is missing

# Which keys to process from SOURCE_FILE. None = every key (full regenerate of each target file - this is
# what earlier revisions of this script did). A list of key names = ONLY those keys are transliterated;
# every other line of each existing list_values_<lang>.txt is left completely untouched, and if a target
# file does not exist yet it is created containing only these keys (with a note at the top).
# Default here is the 3 new civil-calendar month lists only, so previously hand-corrected files
# (rasi/nakshatra names etc., corrected earlier in this project) are never touched or regenerated.
ONLY_KEYS = ["NANAKSHAHI_MONTH_LIST", "BANGLADESH_MONTH_LIST", "NEPAL_BS_MONTH_LIST"]

# Each target: output file list_values_<lang>.txt, using aksharamukha script `script`.
# Devanagari-script languages (mr, ne, sa, mai, kok ...) need no transliteration - they are copied verbatim
# from the Hindi file (script="Devanagari" below does exactly that, with language-specific NAME overrides
# still applied, e.g. Nepal's own civil-calendar spelling for ne).
TARGETS = [
    {"lang": "as", "script": "Assamese"},
    {"lang": "bn", "script": "Bengali"},
    {"lang": "gu", "script": "Gujarati"},
    {"lang": "ka", "script": "Kannada"},
    {"lang": "ml", "script": "Malayalam"},
    {"lang": "mr", "script": "Devanagari"},   # same script as the source: a checked copy, not a transliteration
    {"lang": "ne", "script": "Devanagari"},
    {"lang": "or", "script": "Oriya"},
    {"lang": "sat", "script": "Santali"},
    {"lang": "pa", "script": "Gurmukhi"},
    {"lang": "sa", "script": "Devanagari"},
    {"lang": "ta", "script": "Tamil"},        # Tamil cannot show all Sanskrit sounds (no aspirated letters) - check carefully
    {"lang": "te", "script": "Telugu"},
    {"lang": "ur", "script": "Urdu"},         # right-to-left Perso-Arabic script - no established reading convention
]                                              # for the 3 new civil-calendar lists; flagged again in the per-language notes below

# Whole values that differ in a language (same number of comma-separated items as the Hindi line).
# Keyed by lang, then by list KEY.
LANGUAGE_OVERRIDES = {
    "pa": {
        "DAYS_LIST": "ਐਤਵਾਰ,ਸੋਮਵਾਰ,ਮੰਗਲਵਾਰ,ਬੁੱਧਵਾਰ,ਵੀਰਵਾਰ,ਸ਼ੁੱਕਰਵਾਰ,ਸ਼ਨੀਵਾਰ",
    },
}

DRY_RUN = False
# ===================================================================================================


_COMMA_GUARD = "\x01"   # a byte that cannot occur in the source file, used to shield ',' from the transliterator


def _pre_process(text, target_script):
    """Script-specific clean-up of the Devanagari before transliterating."""
    if target_script == "Gurmukhi":
        # Punjabi writes ष as ਸ਼ and ऋ / ृ as ਰਿ / ੍ਰਿ (aksharamukha would give the scholarly ਸ਼਼ and ੍ਰੁ).
        text = text.replace("ष", "श").replace("ृ", "्रि").replace("ऋ", "रि")
    return text


def _transliterate_value(transliterate, value, target_script):
    """Converts one comma-separated value, protecting ',' from scripts whose transliterator rewrites it
    (e.g. Urdu replaces every ',' with the Urdu-script '،', which would silently break every list's item
    count - caught once already in testing, guarded against here so it can never happen again)."""
    protected = value.replace(",", _COMMA_GUARD)
    out = transliterate.process("Devanagari", target_script, _pre_process(protected, target_script))
    return out.replace(_COMMA_GUARD, ",")


def _read_source(lang_path):
    src_path = os.path.join(lang_path, SOURCE_FILE)
    with open(src_path, "r", encoding="utf-8-sig", newline="") as f:
        return f.read()


def _check_english_keys(lang_path, keys):
    en_path = os.path.join(lang_path, ENGLISH_FILE)
    if not os.path.exists(en_path):
        return None
    with open(en_path, "r", encoding="utf-8-sig") as f:
        en_keys = [l.split("=", 1)[0].strip() for l in f
                   if l.strip() and not l.lstrip().startswith("#") and "=" in l]
    missing = [k for k in en_keys if k not in keys]
    return missing


def _transliterate_source_lines(content, script, lang, transliterate, only_keys):
    """Walks SOURCE_FILE once. Returns (lines_out, keys_seen, item_warnings, override_count) where
    lines_out is the full re-rendered source content (every '#'/blank line kept, every KEY=value line
    transliterated) - used for full-regenerate mode. When `only_keys` is given, lines_out still contains
    every line (so callers can still extract exactly the requested KEY=value lines from it), but keys
    not in `only_keys` are passed through from the Hindi text WITHOUT being transliterated, and are
    never written to a target file - only the lines whose key is in `only_keys` are used by the caller."""
    overrides = LANGUAGE_OVERRIDES.get(lang, {})
    out, keys, item_warnings, override_count = [], [], [], 0
    for raw in content.splitlines(keepends=True):
        body = raw.rstrip("\r\n")
        eol = raw[len(body):]
        if not body.strip() or body.lstrip().startswith("#") or "=" not in body:
            out.append(raw)
            continue
        key, value = body.split("=", 1)
        k = key.strip()
        keys.append(k)
        if only_keys is not None and k not in only_keys:
            out.append(raw)       # not a key we were asked to process: carry the Hindi line through untouched
            continue
        if script == "Devanagari":
            new_value = value                      # same script as the source: no conversion needed
        else:
            new_value = _transliterate_value(transliterate, value, script)
        if k in overrides:
            if overrides[k].count(",") == value.count(","):
                new_value = overrides[k]
                override_count += 1
            else:
                item_warnings.append(f"{k}: override has {overrides[k].count(',') + 1} items, "
                                      f"Hindi has {value.count(',') + 1} - override skipped")
        if new_value.count(",") != value.count(","):
            item_warnings.append(f"{k}: item count changed - kept the Hindi value, please fix by hand")
            new_value = value
        out.append(f"{key}={new_value}{eol}")
    return out, keys, item_warnings, override_count


def _merge_into_existing(out_path, new_lines_by_key, key_comments):
    """Inserts/updates ONLY the given keys inside an existing list_values_<lang>.txt, leaving every other
    line (and the file's own line-ending style) untouched. A key already present is replaced in place
    (its own comment line above it, if any, is left as it was). A key not yet present is appended at the
    end, each preceded by its '#'-comment line taken from the Hindi source. If the target file does not
    exist yet, it is created containing only the given keys."""
    added, replaced = [], []
    if os.path.exists(out_path):
        with open(out_path, "r", encoding="utf-8-sig", newline="") as f:
            existing = f.read()
        nl = "\r\n" if "\r\n" in existing else "\n"
        lines = existing.splitlines(keepends=True)
    else:
        existing, nl, lines = "", "\n", []

    remaining = dict(new_lines_by_key)
    for i, raw in enumerate(lines):
        body = raw.rstrip("\r\n")
        if "=" in body and not body.lstrip().startswith("#"):
            k = body.split("=", 1)[0].strip()
            if k in remaining:
                eol = raw[len(body):] or nl
                lines[i] = remaining.pop(k) + eol
                replaced.append(k)

    if remaining:
        if lines and not lines[-1].endswith(("\n", "\r")):
            lines[-1] += nl
        for k, new_line in remaining.items():
            lines.append(f"{key_comments.get(k, '### ' + k)}{nl}")
            lines.append(f"{new_line}{nl}")
            added.append(k)

    text = "".join(lines)
    backed_up = os.path.exists(out_path) and not DRY_RUN
    if not DRY_RUN:
        if os.path.exists(out_path):
            shutil.copy2(out_path, out_path + ".bak")
        with open(out_path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
    return added, replaced, backed_up


def process_one(target, content, transliterate, lang_path, en_keys_missing_template):
    lang = target["lang"]
    script = target["script"]

    out, keys, item_warnings, override_count = _transliterate_source_lines(
        content, script, lang, transliterate, ONLY_KEYS)
    missing_keys = [k for k in en_keys_missing_template if k not in keys] if en_keys_missing_template else []
    out_path = os.path.join(lang_path, f"list_values_{lang}.txt")

    if ONLY_KEYS is None:
        # full regenerate: write the whole re-rendered file, exactly as earlier revisions of this script did
        text = "".join(out)
        done = sum(1 for l in out if "=" in l.rstrip("\r\n") and not l.lstrip().startswith("#"))
        backed_up = os.path.exists(out_path) and not DRY_RUN
        if not DRY_RUN:
            if os.path.exists(out_path):
                shutil.copy2(out_path, out_path + ".bak")
            with open(out_path, "w", encoding="utf-8", newline="") as f:
                f.write(text)
        added, replaced = [], keys
    else:
        # surgical mode: extract just the transliterated KEY=value lines for ONLY_KEYS, and the comment
        # line that precedes each of them in the Hindi source, then merge into the existing target file
        new_lines_by_key, key_comments, pending_comment = {}, {}, None
        for raw in out:
            body = raw.rstrip("\r\n")
            if body.lstrip().startswith("#"):
                pending_comment = body
                continue
            if "=" in body:
                k = body.split("=", 1)[0].strip()
                if k in ONLY_KEYS:
                    new_lines_by_key[k] = body
                    if pending_comment is not None:
                        key_comments[k] = pending_comment
            pending_comment = None
        added, replaced, backed_up = _merge_into_existing(out_path, new_lines_by_key, key_comments)
        done = len(added) + len(replaced)
        item_warnings = [w for w in item_warnings if w.split(":", 1)[0] in ONLY_KEYS]

    return {
        "lang": lang, "script": script, "done": done, "item_warnings": item_warnings,
        "override_count": override_count, "missing_en_keys": missing_keys,
        "out_path": out_path, "backed_up": backed_up, "added": added,
        "replaced": replaced if ONLY_KEYS is not None else [],
    }


def main():
    try:
        from aksharamukha import transliterate
    except ImportError:
        sys.exit("Needs aksharamukha:  python -m pip install aksharamukha")
    try:
        from jhora import const
        lang_path = const._LANGUAGE_PATH
    except Exception:
        lang_path = os.path.dirname(os.path.abspath(__file__)) + os.sep

    content = _read_source(lang_path)
    all_keys = [l.split("=", 1)[0].strip() for l in content.splitlines()
                if l.strip() and not l.lstrip().startswith("#") and "=" in l]
    missing_in_en = _check_english_keys(lang_path, all_keys)

    print(f"{SOURCE_FILE}  ({len(all_keys)} keys)  ->  {len(TARGETS)} target language(s)")
    if missing_in_en:
        print(f"⚠️ keys in {ENGLISH_FILE} but not in {SOURCE_FILE}: {missing_in_en}")
    if DRY_RUN:
        print("[DRY RUN - no files will be written]")
    print()

    results = []
    for target in TARGETS:
        r = process_one(target, content, transliterate, lang_path, missing_in_en)
        results.append(r)
        status = "OK" if not r["item_warnings"] else f"{len(r['item_warnings'])} warning(s)"
        if ONLY_KEYS is not None:
            detail = f"{len(r['added'])} added, {len(r['replaced'])} updated (all other lines untouched)"
        else:
            detail = f"{r['done']} values (full file regenerated)"
        print(f"   {r['lang']:4} ({r['script']:10}) -> {os.path.basename(r['out_path'])}  "
              f"{detail}  [{status}]"
              + (f"  (backup of existing file saved)" if r["backed_up"] and not DRY_RUN else ""))
        for w in r["item_warnings"]:
            print(f"        ⚠️ {w}")

    print(f"\n{'lang':4} {'values':>7} {'overrides':>10} {'warnings':>9}  file")
    for r in results:
        print(f"{r['lang']:4} {r['done']:>7} {r['override_count']:>10} {len(r['item_warnings']):>9}  {r['out_path']}")

    total_warnings = sum(len(r["item_warnings"]) for r in results)
    print(f"\n{len(results)} language(s) processed, {total_warnings} total warning(s).")
    if total_warnings:
        print("Review the ⚠️ lines above before using the affected files.")


if __name__ == "__main__":
    main()
