"""Public recovery command export."""

import importlib

from agentic_devtools.cli.speckit.progression_recovery import recover_stranded_progressions_command


def test_all_exports_recovery_command():
    module = importlib.reload(importlib.import_module("agentic_devtools.cli.speckit"))
    assert "recover_stranded_progressions_command" in module.__all__
    assert module.recover_stranded_progressions_command is recover_stranded_progressions_command
