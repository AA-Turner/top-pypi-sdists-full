"""What an overview page may load: the allowlist and its loader."""

from .overview_csp import ALLOWLIST_PATH, load_allowlist

__all__ = ["ALLOWLIST_PATH", "load_allowlist"]
