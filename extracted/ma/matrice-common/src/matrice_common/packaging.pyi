"""Auto-generated stub for module: packaging."""
from typing import Any, List, Union

# Functions
def dependencies_check(package_names: Union[List[str], str]) -> bool:
    """
    Check and (optionally) install required dependencies. NEVER raises.
    
        Each entry is either a bare package name or a dict declaring a version mode:
    
          "httpx"
              Install the latest ONLY if the package is entirely missing; if any
              version is already present (e.g. shipped by the Docker image / env),
              leave it untouched.
          {"name": "httpx", "suggested": "0.28.1"}
              Same "install-only-if-missing" behaviour, but install ==0.28.1 when
              absent. Image/env-safe: a version the image already provides is never
              overridden — the suggestion is a fallback for standalone installs.
          {"name": "cryptography", "exact": "48.0.1"}
              Force ==48.0.1 regardless of what is installed (may conflict with a
              system/Debian-managed package — use only when the exact version is
              truly required).
    
        Any per-entry failure is logged as a warning and swallowed — a missing or
        un-installable dependency must never crash the importing service.
    """
    ...
