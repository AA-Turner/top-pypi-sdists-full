"""Verify generated client code is importable."""


def test_generated_config_importable():
    """Generated config client should be importable."""
    import smplkit._generated.config  # noqa: F401


def test_generated_flags_importable():
    """Generated flags client should be importable."""
    import smplkit._generated.flags  # noqa: F401


def test_generated_logging_importable():
    """Generated logging client should be importable."""
    import smplkit._generated.logging  # noqa: F401


def test_generated_app_importable():
    """Generated app client should be importable."""
    import smplkit._generated.app  # noqa: F401
