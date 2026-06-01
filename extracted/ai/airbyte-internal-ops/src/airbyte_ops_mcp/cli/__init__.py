# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""CLI module for `airbyte-ops` command-line interface.

## Installation

**Prerequisites:** Install [uv](https://docs.astral.sh/uv/) (the fast Python
package manager):

```bash
brew install uv          # macOS / Linux (Homebrew)
```

**Install the CLI** as a persistent tool:

```bash
uv tool install airbyte-internal-ops
```

**Run without installing** (uses the latest version each time):

```bash
uvx airbyte-internal-ops@latest --help
```

**Upgrade to the latest version:**

```bash
uv tool upgrade airbyte-internal-ops
```

**Troubleshooting:** If you hit interpreter conflicts, you can tell `uv` to
bundle its own Python instead of using whichever `python` is on your `PATH`.
See [The Modern Ways to Not Install Python](https://dev.to/aaronsteers/the-modern-ways-to-not-install-python-1e85)
for background.

```bash
uv tool install airbyte-internal-ops --python-preference=only-managed
```

## CLI reference

Each command group is documented in its own submodule page — select a
submodule below for the full command reference.

The combined CLI reference can also be regenerated locally via
`poe docs-generate`; see `docs/generate_cli.py`.
"""

# Expose only the domain submodules to pdoc / docs auto-rendering.
# Without this, every command function defined in sibling modules would
# appear on the top-level `cli` docs page.
__all__: list[str] = [
    "cloud",
    "devin",
    "dockerhub",
    "gh",
    "local",
    "registry",
    "roster",
    "secrets",
]
