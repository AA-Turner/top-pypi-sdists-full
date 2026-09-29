import flufl.i18n


def test_all_names_defined():
    # ruff's F822 skips __init__.py, so nothing else catches a name listed in __all__ that the
    # module doesn't define -- until a star import raises AttributeError in someone else's code.
    missing = [name for name in flufl.i18n.__all__ if not hasattr(flufl.i18n, name)]
    assert missing == []
