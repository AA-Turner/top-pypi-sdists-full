"""Auto-generated stub for module: test_ultralytics_harness_guard."""

# Functions
def test_conftest_lists_every_ultralytics_harness() -> None:
    """
    `collect_ignore` must name every harness that imports ultralytics.
    
        A harness added later without a ``conftest`` entry would break the directory
        walk for anyone without the dependency -- the exact failure the guard was
        added to prevent.
    """
    ...
def test_ultralytics_harnesses_are_guarded_either_way() -> None:
    """
    The six harnesses must stay importable-or-skipped, never a hard error.
    
        Asserts the property the guards exist to provide rather than the mechanism:
        ``ultralytics`` is either present (the harnesses run) or absent (they skip).
        Both are valid; what must never happen is a collection error.
    """
    ...
