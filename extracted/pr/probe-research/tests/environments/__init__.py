"""The opt-in environment suite (README.md).

A package ON PURPOSE: without this file pytest imports ``conftest.py`` here as
the bare module ``conftest``, which replaces agent/tests/conftest.py in
``sys.modules`` and breaks every ``from conftest import FakeApp`` in the agent
suite that is collected after this directory."""
