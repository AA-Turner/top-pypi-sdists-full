"""Regression test: MechanicalRename must implement BaseTool.run (not invoke).

Prior to the fix, MechanicalRename overrode BaseTool.invoke instead of the
abstract BaseTool.run, making inspect.isabstract(MechanicalRename) return True
and causing the tool manager to silently drop it from active_tools.
"""
import inspect
import pytest
from drydock.core.tools.builtins.mechanical_rename import MechanicalRename
from drydock.core.tools.base import BaseTool


def test_mechanical_rename_is_not_abstract():
    """Tool manager uses inspect.isabstract to filter — must be False."""
    assert not inspect.isabstract(MechanicalRename), (
        "MechanicalRename is abstract; it must implement BaseTool.run"
    )


def test_mechanical_rename_implements_run():
    """run() must be defined directly on MechanicalRename, not inherited as abstract."""
    assert "run" in MechanicalRename.__dict__, (
        "MechanicalRename does not define run(); only invoke() was defined before fix"
    )


def test_mechanical_rename_instantiates():
    """Should be instantiable with default config and state."""
    from drydock.core.tools.base import BaseToolState
    from drydock.core.tools.builtins.mechanical_rename import MechanicalRenameConfig
    tool = MechanicalRename(config=MechanicalRenameConfig(), state=BaseToolState())
    assert isinstance(tool, BaseTool)
