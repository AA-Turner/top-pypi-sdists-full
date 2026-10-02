#!/usr/bin/env python
"""A first pass over every page of the documentation, before reading them.

For each page in docs/source -- its own text, or the module docstring an
``automodule`` directive pulls in -- reports:

  * its section titles, in order, so the pages that leave the common
    pattern stand out;
  * whether a module page opens with the quick start (wget, chmod, run);
  * leftovers of things that changed: the F-test as the test of matched
    runs, removed helpers, old folders and addresses;
  * its size, in lines and words.

    python doc_audit.py                  # every page
    python doc_audit.py zone scatter     # some
"""
import ast
import glob
import os
import re
import sys

SRC = "docs/source"

STALE = [
    (r"ftest_confidence", "helper replaced by sigma_confidence"),
    (r"_PAIR_KEY", "constant removed, the key is pikobs.match's"),
    (r"\bpsmon\b", "psmon reference"),
    (r"F-test on the sigma|sigma.{0,20}F-test|F = σ²", "F-test presented for the sigma"),
    (r"sample_std", "helper removed"),
    (r"PATHWORK#/home", "old Web address line"),
    (r"saska", "old F-test name"),
    (r'"(paired t and )?F"\]|\bpaired t and F\b', "F named as the test of matched runs"),
    (r"TODO|FIXME|XXX", "note left in the text"),
]

MODULE_PAGES = {"scatter", "zone", "cardio", "vdedr", "flag", "flags", "mapobs",
                "obscountdb", "histogram", "profile", "verifprofile",
                "timeserie"}


import glob as _glob
WRAPPER_DIRS = set()
for _w in _glob.glob("pikobs/script/run_*.sh"):
    _m = re.search(r'(?m)^PATHWORK="?/home/\$\{USER\}/sites8/([\w.-]+)', open(_w).read())
    if _m:
        WRAPPER_DIRS.add(_m.group(1))
FOLDER = re.compile(r"sites8/(pikobs_[\w.-]+)/")


def page_text(rst_path):
    """The page's text, following an automodule directive to its docstring."""
    text = open(rst_path).read()
    m = re.search(r"\.\.\s+automodule::\s+([\w.]+)", text)
    if not m:
        return text, None
    mod = m.group(1)
    path = os.path.join(*mod.split(".")) + ".py"
    if not os.path.isfile(path):
        path = os.path.join(*mod.split("."), "__init__.py")
    if not os.path.isfile(path):
        print(f"   ! MISSING MODULE: {mod} (the page will be empty)")
        return text, mod
    try:
        doc = ast.get_docstring(ast.parse(open(path).read())) or ""
    except SyntaxError:
        doc = ""
    return text + "\n" + doc, mod


def sections(text):
    """Titles underlined (or over- and underlined) with = - ~ ^ characters."""
    lines = text.splitlines()
    out = []
    for i in range(1, len(lines)):
        u = lines[i].strip()
        t = lines[i - 1].strip()
        if (len(u) >= 3 and len(set(u)) == 1 and u[0] in "=-~^*"
                and t and len(set(t)) > 1 and len(u) >= len(t) - 2):
            out.append((u[0], t))
    return out


def main():
    want = set(sys.argv[1:])
    pages = sorted(glob.glob(os.path.join(SRC, "*.rst")))
    for p in pages:
        name = os.path.splitext(os.path.basename(p))[0]
        if want and name not in want:
            continue
        text, mod = page_text(p)
        words = len(text.split())
        lines = text.count("\n")
        print(f"\n=== {name}  ({mod or 'rst'})  {lines} lines, {words} words")
        secs = sections(text)
        if secs:
            print("   sections: " + " | ".join(t for _, t in secs[:14])
                  + (" ..." if len(secs) > 14 else ""))
        if name in MODULE_PAGES:
            head = "\n".join(text.splitlines()[:80])
            quick = all(k in head for k in ("wget", "chmod"))
            print(f"   quick start in the first 80 lines: {'yes' if quick else 'NO'}")
        odd = [i + 1 for i, l in enumerate(text.splitlines())
               for d in FOLDER.findall(l)
               if not d.startswith(("pikobs_doc_", "pikobs_bench_", "pikobs_coh_", "pikobs_regions"))
               and d not in WRAPPER_DIRS]
        if odd:
            print(f"   ! folder that no wrapper writes to: line(s) {', '.join(map(str, odd[:6]))}")
        for pat, why in STALE:
            hits = [i + 1 for i, l in enumerate(text.splitlines()) if re.search(pat, l)]
            if hits:
                print(f"   ! {why}: line(s) {', '.join(map(str, hits[:6]))}"
                      f"{' ...' if len(hits) > 6 else ''}")


if __name__ == "__main__":
    main()
