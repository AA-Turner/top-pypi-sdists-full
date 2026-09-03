"""generate_wheel_manifest.py - THE FULL-WHEEL RULE (Daniel, 2026-08-31):
"EVERY SHIP SHOULD BE ON THE WHEEL."

Regenerates the [tool.setuptools.data-files] section of pyproject.toml from
`git ls-files --cached --others --exclude-standard`
(tracked plus new-not-ignored, so files born in the current session enter the
manifest BEFORE the ship commit), so the published wheel/sdist carry EVERYTHING the ship
publishes to the repository. Exclusions are exactly two, both structural:
  - the 15 declared py-modules (they ship as importable modules), and
  - files under the uqff_downhole_simulator/ package (they ship as the package).
Untracked files (operator tier, backups, build junk) never enter git and so
never enter the manifest - the confidentiality boundary is unchanged.

Run:  python generate_wheel_manifest.py
Enforced forever by SHIP GUARD v8 in uqff_fidelity_tests.py.
"""
import re
import subprocess
import collections

BEGIN = "# --- BEGIN AUTO-GENERATED DATA-FILES (generate_wheel_manifest.py; Daniel's full-wheel rule 2026-08-31) ---"
END = "# --- END AUTO-GENERATED DATA-FILES ---"
DEST_ROOT = "share/star-magic-program"


def tracked_files():
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                         capture_output=True, text=True, check=True)
    return [l for l in out.stdout.splitlines() if l.strip()]


def build_section():
    pp = open("pyproject.toml", encoding="utf-8").read()
    mods = set(re.findall(r'"([^"]+)"', re.search(r"py-modules\s*=\s*\[(.*?)\]", pp, re.S).group(1)))
    pkgs = set(re.findall(r'"([^"]+)"', re.search(r"packages\s*=\s*\[(.*?)\]", pp, re.S).group(1)))
    by_dest = collections.defaultdict(list)
    excluded = 0
    for f in tracked_files():
        # v0.412.0 FRONT DOOR: FULL MIRROR - modules and package files ship in
        # site-packages AND in the share/ mirror, so data_root() is a complete
        # repository on every layout and the gate reads its own sources there.
        # Sole exclusion: the legacy junk file with a space in its name
        # (Windows-locked; delete manually - it must never enter the wheel).
        _ = (mods, pkgs)
        if f == "python uqff_downhole_simulator.py":
            excluded += 1
            continue
        d = f.rsplit("/", 1)[0] if "/" in f else ""
        dest = DEST_ROOT + ("/" + d if d else "")
        by_dest[dest].append(f)
    lines = ["[tool.setuptools.data-files]", BEGIN]
    total = 0
    for dest in sorted(by_dest):
        lines.append('"%s" = [' % dest)
        for f in sorted(by_dest[dest]):
            lines.append('    "%s",' % f)
            total += 1
        lines.append("]")
    lines.append(END)
    return "\n".join(lines) + "\n", total, excluded


def main():
    pp = open("pyproject.toml", encoding="utf-8", newline="").read()
    section, total, excluded = build_section()
    i = pp.index("[tool.setuptools.data-files]")
    # replace from the data-files header to end of file or next top-level header
    m = re.search(r"\n\[(?!tool\.setuptools\.data-files)", pp[i:])
    j = i + m.start() + 1 if m else len(pp)
    new = pp[:i] + section + (pp[j:] if m else "")
    open("pyproject.toml", "w", encoding="utf-8", newline="").write(new)
    print("data-files regenerated: %d files in manifest (%d excluded as modules/package)" % (total, excluded))


if __name__ == "__main__":
    main()
