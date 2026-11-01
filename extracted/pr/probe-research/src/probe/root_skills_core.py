"""Moved to `probe.foundation.skills.root_skills_core` (agent:3); this path stays importable for one release."""

# restructure-shim: probe.foundation.skills.root_skills_core
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.foundation.skills.root_skills_core")
