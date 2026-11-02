"""A sandbox template no host will ever start."""


class SandboxTemplateError(Exception):
    """The host refused the template itself, so every episode started from it would fail the same way."""
