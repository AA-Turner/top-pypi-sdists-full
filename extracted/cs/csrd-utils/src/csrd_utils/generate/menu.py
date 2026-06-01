"""Generate menu orchestration for csrd CLI.

Menu items are declared up-front in ``IN_WORKSPACE_ITEMS``.  Each entry
carries an optional ``visible`` predicate so the set of choices adapts
to context (e.g. whether infra slots remain) without imperative branching.
"""

from pathlib import Path

from ..compose import SPEC_FILENAME, available_infra, configured_infra, load_spec, spec_file_path
from .handlers import (
    add_augment_interactive,
    add_frontend_direct,
    add_frontend_interactive,
    add_infra_direct,
    add_infra_interactive,
    add_service_direct,
    add_service_interactive,
    add_version_direct,
    add_version_interactive,
    cancel_ok,
    create_workspace,
    create_workspace_direct,
    list_augments,
    remove_infra_direct,
    remove_infra_interactive,
    remove_service_direct,
    remove_service_interactive,
    rename_service_direct,
    rename_service_interactive,
)
from .helpers import (
    MenuItem,
    filter_visible,
    run_menu,
)

# ---------------------------------------------------------------------------
# Context predicates
# ---------------------------------------------------------------------------


def _has_workspace() -> bool:
    """Check whether ``cwd`` contains a ``csrd-compose.yaml``."""

    return (Path.cwd() / SPEC_FILENAME).is_file()


def _has_available_infra() -> bool:
    """True when the current workspace still has un-configured infra types."""

    return _has_workspace() and bool(available_infra(Path.cwd().resolve()))


def _has_configured_infra() -> bool:
    """True when the current workspace has at least one configured infra type."""

    return _has_workspace() and bool(configured_infra(Path.cwd().resolve()))


def _has_services() -> bool:
    """True when the current workspace has at least one service."""

    if not _has_workspace():
        return False
    sp = spec_file_path(Path.cwd().resolve())
    if not sp.is_file():
        return False
    spec = load_spec(sp)
    return bool(spec.services)


def _frontend_disabled() -> str:
    """Return a disabled hint if the workspace already has a frontend."""

    if not _has_workspace():
        return ""
    frontend_dir = Path.cwd() / "src" / "frontend"
    if frontend_dir.exists():
        return "already added"
    return ""


# ---------------------------------------------------------------------------
# Declarative menu definitions
# ---------------------------------------------------------------------------

#: Items shown when the user is *inside* an existing workspace.
IN_WORKSPACE_ITEMS: list[MenuItem] = [
    MenuItem(
        label="add service",
        aliases=("add service", "add-service", "service", "s"),
        handler=add_service_interactive,
    ),
    MenuItem(
        label="add augment",
        aliases=("add augment", "add-augment", "augment", "a"),
        handler=add_augment_interactive,
    ),
    MenuItem(
        label="remove service",
        aliases=("remove service", "remove-service", "rm-service", "rs"),
        handler=remove_service_interactive,
        visible=_has_services,
    ),
    MenuItem(
        label="rename service",
        aliases=("rename service", "rename-service", "rn-service", "mv-service"),
        handler=rename_service_interactive,
        visible=_has_services,
    ),
    MenuItem(
        label="add version",
        aliases=("add version", "add-version", "version", "v"),
        handler=add_version_interactive,
        visible=_has_services,
    ),
    MenuItem(
        label="add frontend",
        aliases=("add frontend", "add-frontend", "frontend", "fe"),
        handler=add_frontend_interactive,
        disabled=_frontend_disabled,
    ),
    MenuItem(
        label="add infra",
        aliases=("add infra", "add-infra", "infra", "i"),
        handler=add_infra_interactive,
        visible=_has_available_infra,
    ),
    MenuItem(
        label="remove infra",
        aliases=("remove infra", "remove-infra", "rm-infra", "ri"),
        handler=remove_infra_interactive,
        visible=_has_configured_infra,
    ),
    MenuItem(label="cancel", aliases=("cancel", "q"), handler=cancel_ok),
]

#: Shared cancel item for the no-workspace menu.
_CANCEL_ITEM = MenuItem(label="cancel", aliases=("cancel", "q"), handler=cancel_ok)


def _build_no_workspace_items(default_name: str, *, name_provided: bool) -> list[MenuItem]:
    """Build menu items for the no-workspace context.

    The workspace handler needs ``default_name`` at construction time,
    so this is the one part that cannot be a static list.  Everything
    else (labels, aliases, cancel) is still declarative.

    Menu: workspace / cancel
    """

    if name_provided:
        ws_handler = lambda: create_workspace_direct(default_name)  # noqa: E731
    else:
        ws_handler = lambda: create_workspace(default_name)  # noqa: E731

    return [
        MenuItem("workspace", ("workspace", "ws", "w"), ws_handler),
        _CANCEL_ITEM,
    ]


# ---------------------------------------------------------------------------
# Public entry-point
# ---------------------------------------------------------------------------


def run_generate_menu(
    target: str | None = None,
    name: str | None = None,
    *,
    git_init: bool = False,
    # add-service direct flags
    features: list[str] | None = None,
    port: int | None = None,
    # add-infra direct flag
    infra_type: str | None = None,
    # remove-service / rename-service direct flags
    service_name: str | None = None,
    new_name: str | None = None,
    # add-version direct flag
    version_date: str | None = None,
) -> int:
    """Run the generator menu.

    Direct-mode targets (``workspace``, ``add-service``, ``add-infra``,
    ``remove-infra``, ``add-augment``, ``remove-service``, ``empty``)
    are dispatched immediately.  Otherwise the interactive menu is
    presented, built declaratively from the item lists above.
    """

    default_name = (name or "my-workspace").strip() or "my-workspace"

    # ---- direct-mode dispatch ----
    if target == "workspace":
        return create_workspace_direct(default_name, git_init=git_init)

    if target == "preset":
        return create_workspace(default_name)

    if target == "add-service":
        if name is None:
            return add_service_interactive()
        return add_service_direct(
            name=name,
            features=features or [],
            port=port or 8080,
        )

    if target == "add-infra":
        if infra_type is None:
            return add_infra_interactive()
        return add_infra_direct(infra_type=infra_type)

    if target == "remove-infra":
        if infra_type is None:
            return remove_infra_interactive()
        return remove_infra_direct(infra_type=infra_type)

    if target == "add-augment":
        return add_augment_interactive()

    if target == "list-augments":
        return list_augments()

    if target == "remove-service":
        if service_name is None:
            return remove_service_interactive()
        return remove_service_direct(service_name=service_name)

    if target == "rename-service":
        if service_name is None or new_name is None:
            return rename_service_interactive()
        return rename_service_direct(old_name=service_name, new_name=new_name)

    if target == "add-version":
        if service_name is None:
            return add_version_interactive()
        return add_version_direct(service_name=service_name, date_str=version_date)

    if target == "add-frontend":
        return add_frontend_direct()

    # Legacy alias
    if target == "empty":
        return create_workspace_direct(default_name, git_init=git_init)

    # ---- interactive menu ----
    if _has_workspace():
        items = filter_visible(IN_WORKSPACE_ITEMS)
    else:
        items = _build_no_workspace_items(default_name, name_provided=name is not None)

    result: int = run_menu("csrd generate", "? What would you like to generate?", items)
    return result
