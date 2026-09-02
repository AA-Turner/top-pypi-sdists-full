"""Single source of truth for the package version.

Hatchling reads ``__version__`` from this file at build time — see
``[tool.hatch.version]`` in ``pyproject.toml``. The release workflow
also greps this file when verifying that a ``v*-py`` tag matches the
package version (see ``.github/workflows/python-release.yml``).

Bumping a release is therefore a single-file edit: change the literal
below, commit, tag ``v<new>-py``, push.
"""

__version__ = "0.4.1"
