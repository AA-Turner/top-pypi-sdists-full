"""The package-root constants that tell Probe's own frames from the caller's are read from the
`probe` package, not by counting parents of their file, so moving a module deeper keeps them right."""

from __future__ import annotations

import os

import probe
from probe.sdk import diagnostics
from probe.sdk.run.launch import preempt

ROOT = os.path.dirname(os.path.abspath(probe.__file__))


def test_both_roots_are_the_probe_package_wherever_their_module_sits() -> None:
    assert diagnostics._PKG_ROOT == ROOT
    assert preempt._SDK_ROOT == ROOT + os.sep


def test_a_frame_in_a_deep_sdk_module_counts_as_ours() -> None:
    deep = os.path.join(ROOT, "sdk", "run", "launch", "preempt.py")
    assert diagnostics._is_ours(deep)
    assert deep.startswith(preempt._SDK_ROOT)
