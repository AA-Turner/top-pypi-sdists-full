"""Marker to be imported and used in plugins (and for own implementations)."""

from typing import Any, Callable, TypeVar, cast

import pluggy

# Improvement suggested by @oremanj on python/typing gitter
F = TypeVar("F", bound=Callable[..., Any])

# Distinct from upstream sqlfluff's "sqlfluff" group so that, when both are installed,
# each only loads its own plugins.
project_name = "collate_sqlfluff"
plugin_base_name = f"{project_name}-plugin"
hookimpl = cast(Callable[[F], F], pluggy.HookimplMarker(plugin_base_name))
