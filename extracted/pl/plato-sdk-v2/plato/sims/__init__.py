"""Plato simulation SDK namespace package.

Sim SDKs are published as separate packages and install into this namespace.

## Installation

```bash
# Configure the Plato PyPI index in pyproject.toml:
# [[tool.uv.index]]
# name = "plato-sims"
# url = "https://plato.so/api/v2/pypi/sims/simple/"
#
# [tool.uv.sources]
# espocrm = { index = "plato-sims" }

uv add espocrm
```

## Usage

```python
from plato.sims import espocrm

# Create client with Basic auth
client = await espocrm.AsyncClient.create(base_url="https://.../api/v1")

# Use generated API functions
from plato.sims.espocrm.api.account import get_account
accounts = await get_account.asyncio(client.httpx)
```
"""

# Allow external packages to contribute to this namespace
import os
import sys
from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)

# For editable installs, extend_path may not find site-packages.
# Explicitly add it so `import plato.sims.espocrm` works.
for site_path in sys.path:
    if "site-packages" in site_path:
        candidate = os.path.join(site_path, "plato", "sims")
        if os.path.isdir(candidate) and candidate not in __path__:
            __path__.append(candidate)


def __getattr__(name: str):
    """Lazy import sim modules."""
    import importlib

    # Allow any submodule to be imported lazily
    try:
        return importlib.import_module(f".{name}", __name__)
    except ImportError:
        raise AttributeError(f"module 'plato.sims' has no attribute '{name}'")
