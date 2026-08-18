"""
Feature-name ordering must be deterministic across processes.

create_feature_names() used `list(set(...))` to dedup, whose iteration order
is PYTHONHASHSEED-randomized. Two identical runs therefore built X_train with
different column orders, which (a) changes gOMP tie-breaking and (b) gives the
feature-selection cache a different key every run, so nothing was ever reused
between runs.
"""

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

GEOCIF_PY = Path(__file__).resolve().parents[1] / "geocif" / "geocif.py"


def test_feature_names_are_deduped_order_preservingly():
    """The dedup must be dict.fromkeys, never list(set(...))."""
    source = GEOCIF_PY.read_text(encoding="utf-8", errors="replace")
    assert "self.feature_names = list(dict.fromkeys(self.feature_names))" in source
    assert "self.feature_names = list(set(self.feature_names))" not in source


def test_no_set_based_dedup_of_feature_names_anywhere():
    source = GEOCIF_PY.read_text(encoding="utf-8", errors="replace")
    offenders = re.findall(r"feature_names\s*=\s*list\(set\(", source)
    assert offenders == []


def test_dict_fromkeys_dedup_is_stable_across_hash_seeds():
    """The chosen construct is seed-independent; list(set(...)) is not."""
    names = [f"CID_{i}_feature" for i in range(40)] * 2
    program = (
        "names = [f'CID_{i}_feature' for i in range(40)] * 2\n"
        "print(','.join(list(dict.fromkeys(names))))\n"
        "print(','.join(list(set(names))))\n"
    )

    outputs = []
    for seed in ("1", "2", "3"):
        result = subprocess.run(
            [sys.executable, "-c", program],
            capture_output=True, text=True, env={"PYTHONHASHSEED": seed, "PATH": ""},
        )
        assert result.returncode == 0, result.stderr
        outputs.append(result.stdout.splitlines())

    ordered = [o[0] for o in outputs]
    assert len(set(ordered)) == 1, "dict.fromkeys must be seed-independent"
    assert ordered[0] == ",".join(dict.fromkeys(names))

    # Sanity: the construct we replaced really did vary (guards the premise).
    set_based = [o[1] for o in outputs]
    assert len(set(set_based)) > 1, "expected list(set(...)) to vary across seeds"
