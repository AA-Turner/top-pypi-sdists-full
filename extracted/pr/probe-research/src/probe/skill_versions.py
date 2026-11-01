"""Moved to `probe.foundation.skills.skills` (agent:3); `python -m probe.skill_versions` keeps working for one release."""

# restructure-shim: probe.foundation.skills.skills
import importlib
import runpy
import sys

if __name__ == "__main__":
    runpy.run_module("probe.foundation.skills.skills", run_name="__main__", alter_sys=True)
else:
    sys.modules[__name__] = importlib.import_module("probe.foundation.skills.skills")
