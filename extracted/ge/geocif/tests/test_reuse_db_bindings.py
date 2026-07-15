"""Regression test for the reuse_db UnboundLocalError in yield_outlook.run().

Root cause (fixed 0.4.853): ``inputs``, ``crops`` and ``models`` were assigned
only inside the ``else`` branch of ``if reuse_db is not None:``.  A reuse_db
rerun skips that branch (it reuses an existing DB instead of gathering ML
inputs), so those three names were never bound -- yet the optional
report / report_lite blocks at the end of ``run()`` reference all three.  The
result was ``UnboundLocalError: cannot access local variable 'inputs'`` at the
report step (yield_outlook.py ~4310).  The ``... if inputs else models`` guard
could not help: an unbound name raises before the truthiness test, and the
fallback ``models`` / ``crops`` were themselves unbound on that path.

The fix binds all three at the top of ``run()`` (before the reuse_db branch);
the normal path still overwrites them from gathered inputs.  This test asserts
that contract structurally via AST, so it fails on the pre-fix source without
having to execute the full (slow) pipeline.
"""
import ast
from pathlib import Path

# Parse the source file directly rather than importing geocif: the module
# pulls in heavy runtime deps (pygeoutil, ML libs) that need not be installed
# to check a structural contract.
_YIELD_OUTLOOK = Path(__file__).resolve().parent.parent / "geocif" / "yield_outlook.py"


def _assigned_top_level_names(node):
    """Return the set of plain ``Name`` targets assigned by a statement."""
    names = set()
    if isinstance(node, ast.Assign):
        for tgt in node.targets:
            if isinstance(tgt, ast.Name):
                names.add(tgt.id)
    elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
        names.add(node.target.id)
    return names


def _run_functiondef():
    tree = ast.parse(_YIELD_OUTLOOK.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "run":
            return node
    raise AssertionError("could not find top-level run() in yield_outlook.py")


def test_inputs_crops_models_bound_before_reuse_db_branch():
    fn = _run_functiondef()

    # Locate the top-level `if reuse_db is not None:` statement.
    reuse_if_idx = None
    for i, node in enumerate(fn.body):
        if (
            isinstance(node, ast.If)
            and isinstance(node.test, ast.Compare)
            and isinstance(node.test.left, ast.Name)
            and node.test.left.id == "reuse_db"
        ):
            reuse_if_idx = i
            break

    assert reuse_if_idx is not None, (
        "could not find `if reuse_db is not None:` at the top level of "
        "yield_outlook.run() -- the test's assumption about run()'s structure "
        "is stale"
    )

    # Names assigned at the top level of run() BEFORE that if-statement.
    bound_before = set()
    for node in fn.body[:reuse_if_idx]:
        bound_before |= _assigned_top_level_names(node)

    for name in ("inputs", "crops", "models"):
        assert name in bound_before, (
            f"{name!r} must be bound before the `if reuse_db is not None:` "
            f"branch so a reuse_db rerun cannot raise UnboundLocalError at the "
            f"report / report_lite step"
        )
