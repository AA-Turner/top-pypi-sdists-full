"""User configuration for pysae-ai-tools.

Paths follow OS conventions via ``platformdirs``:

- Config:   Linux ``~/.config/pysae-ai-tools/`` ;
            macOS ``~/Library/Application Support/pysae-ai-tools/`` ;
            Windows ``~/AppData/Local/pysae-ai-tools/``
- Cache:    Linux ``~/.cache/pysae-ai-tools/`` ;
            macOS ``~/Library/Caches/pysae-ai-tools/`` ;
            Windows ``~/AppData/Local/pysae-ai-tools/Cache/``
- Data:     Linux ``~/.local/share/pysae-ai-tools/`` ;
            macOS ``~/Library/Application Support/pysae-ai-tools/`` ;
            Windows ``~/AppData/Local/pysae-ai-tools/``

Read/write goes through ``tomlkit`` which preserves comments and formatting.
The config file is created with default values on first access. Existing
files are auto-migrated: any expected key missing from the file is appended
with its comment block on the next read. Unknown keys are ignored.

Every top-level key is declared exactly once, as a field of the :class:`Config`
model. The field's annotation carries a :class:`KeyMeta` describing its on-disk
comment block and, when the key is user-facing, the interactive prompt used by
``tools configure``. The TOML scaffolding (defaults, migration, upsert) and the
interactive parameter list (:data:`CONFIG_PARAMS`) are derived from that single
declaration, so adding a key means adding one field and nothing else.
"""

import os
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Literal

import tomlkit
from platformdirs import user_cache_path, user_config_path, user_data_path
from pydantic import BaseModel, ConfigDict, ValidationError
from pydantic_core import PydanticUndefined
from tomlkit import TOMLDocument, comment, document, item, nl, table
from tomlkit.exceptions import TOMLKitError

_APP_NAME = "pysae-ai-tools"

CONFIG_DIR = user_config_path(_APP_NAME)
CONFIG_FILE = CONFIG_DIR / "config.toml"
CACHE_DIR = user_cache_path(_APP_NAME)
DATA_DIR = user_data_path(_APP_NAME)


def assistant_data_dir(name: str) -> Path:
    """Data directory scoped to one assistant (e.g. ``claude``), for its account-specific state."""
    return DATA_DIR / "assistants" / name


def assistant_cache_dir(name: str) -> Path:
    """Cache directory scoped to one assistant (e.g. ``claude``), for its regenerable files."""
    return CACHE_DIR / "assistants" / name


_DefaultValue = bool | int | float | str | list[str] | None

ParamKind = Literal["bool", "string", "path"]
ParamValue = bool | str


@dataclass(frozen=True)
class KeyMeta:
    """On-disk and UI metadata attached to a :class:`Config` field.

    ``comment`` is the multi-line block written above the key in ``config.toml``
    (no leading ``# ``). When ``kind`` is set the key is a user-facing parameter
    prompted by ``tools configure`` (see :class:`ConfigParam`); ``relevant_when_tool``
    then restricts the prompt to installs that selected the named tool (``None`` =
    always relevant).
    """

    comment: str
    kind: ParamKind | None = None
    prompt: str = ""
    description: str = ""
    relevant_when_tool: str | None = None


class Config(BaseModel):
    """The complete user configuration — the single source of truth for every key.

    ``tools_to_install`` / ``tools_known_at_save`` default to ``None`` (absent by
    design): the key is not written on first run so the install command can tell
    "never configured" from "configured to install nothing" (an empty list).
    """

    model_config = ConfigDict(frozen=True)

    auto_update: Annotated[
        bool,
        KeyMeta(
            comment=(
                "Automatically install updates when a newer version is detected, and\n"
                "hourly re-apply tool configuration (auth, MCP, contexts) so rotated\n"
                "secrets are picked up. When false, a notification is shown instead\n"
                "and you update manually with `pysae-ai-tools self-update`."
            )
        ),
    ] = True
    git_clone_dir: Annotated[
        str,
        KeyMeta(
            comment=(
                "Base directory where Pysae projects are cloned by\n"
                "`pysae-ai-tools code ensure-repo` and the support-* skills.\n"
                "Empty string = ask interactively on first use, fall back to the\n"
                "OS-standard data dir when running non-interactively.\n"
                "The PYSAE_AI_TOOLS_GIT_CLONE_DIR env var, when set, takes precedence."
            ),
            kind="path",
            description="Répertoire racine où sont clonés les projets Pysae",
            prompt="📂 Où veux-tu cloner les projets Pysae ?",
        ),
    ] = ""
    tools_to_install: Annotated[
        list[str] | None,
        KeyMeta(
            comment=(
                "List of tools selected for `pysae-ai-tools tools install`.\n"
                "Set interactively the first time you run the command, or with the\n"
                "--configure flag. Tools not in this list are skipped (but still\n"
                "detected if already installed manually)."
            )
        ),
    ] = None
    tools_known_at_save: Annotated[
        list[str] | None,
        KeyMeta(
            comment=(
                "List of tools that existed when `tools_to_install` was last saved.\n"
                "Used to distinguish 'tool was explicitly deselected last time' from\n"
                "'tool didn't exist yet': a tool currently in TOOLS but absent from\n"
                "this list is treated as new and falls back to its default_selected\n"
                "value rather than being silently unchecked."
            )
        ),
    ] = None


def _key_meta(name: str) -> KeyMeta:
    for meta in Config.model_fields[name].metadata:
        if isinstance(meta, KeyMeta):
            return meta
    raise KeyError(f"config field {name!r} has no KeyMeta")


def _key_default(name: str) -> _DefaultValue:
    default = Config.model_fields[name].default
    return None if default is PydanticUndefined else default


def _iter_keys() -> Iterator[tuple[str, KeyMeta, _DefaultValue]]:
    """Yield ``(name, meta, default)`` for every declared config key, in order."""
    for name in Config.model_fields:
        yield name, _key_meta(name), _key_default(name)


# ---------------------------------------------------------------------------
# Configurable parameters — interactive prompts in `tools configure`
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ConfigParam:
    """A user-facing configuration parameter prompted in ``tools configure``.

    The phase-2 step of ``tools configure`` walks :data:`CONFIG_PARAMS` and asks
    one question per relevant entry, pre-filling the current value as default.
    Stored alongside the rest of the user config in ``config.toml`` — never in
    env-cache, never in env vars.

    ``relevant_when_tool``: when set, the parameter is only surfaced if the
    matching tool is part of the user's selected install set. ``None`` means
    "always relevant".
    """

    name: str
    kind: ParamKind
    description: str
    prompt: str
    relevant_when_tool: str | None = None


def _build_config_params() -> tuple[ConfigParam, ...]:
    params: list[ConfigParam] = []
    for name, meta, _default in _iter_keys():
        if meta.kind is None:
            continue
        params.append(
            ConfigParam(
                name=name,
                kind=meta.kind,
                description=meta.description,
                prompt=meta.prompt,
                relevant_when_tool=meta.relevant_when_tool,
            )
        )
    return tuple(params)


CONFIG_PARAMS: tuple[ConfigParam, ...] = _build_config_params()


def iter_params(*, tools_selected: set[str] | None = None) -> Iterator[ConfigParam]:
    """Yield params relevant to ``tools_selected`` (or all when ``None``)."""
    for p in CONFIG_PARAMS:
        if p.relevant_when_tool is None:
            yield p
            continue
        if tools_selected is None or p.relevant_when_tool in tools_selected:
            yield p


def get_param_spec(name: str) -> ConfigParam:
    spec = next((p for p in CONFIG_PARAMS if p.name == name), None)
    if spec is None:
        raise KeyError(f"unknown config parameter: {name}")
    return spec


def get_param(name: str, path: Path | None = None) -> ParamValue:
    """Return the persisted value for ``name`` (or its default when absent)."""
    spec = get_param_spec(name)
    value = getattr(load_config(path), name)
    if spec.kind == "bool":
        return bool(value)
    return str(value if value is not None else "")


def set_param(name: str, value: ParamValue, path: Path | None = None) -> None:
    """Persist ``value`` for parameter ``name`` to ``config.toml``."""
    spec = get_param_spec(name)
    if spec.kind == "bool":
        coerced: ParamValue = bool(value)
    else:
        coerced = str(value)
    doc = _load_doc(path)
    _upsert_key(doc, name, coerced)
    _save_doc(doc, path)


def os_default_clone_dir() -> Path:
    """Return the OS-standard data directory for cloned Pysae projects.

    Linux:   ~/.local/share/pysae-ai-tools/projects
    macOS:   ~/Library/Application Support/pysae-ai-tools/projects
    Windows: ~/AppData/Local/pysae-ai-tools/projects
    """
    return user_data_path(_APP_NAME) / "projects"


def _new_default_doc() -> TOMLDocument:
    doc = document()
    doc.add(comment("Pysae AI tools — user configuration"))
    doc.add(comment(""))
    doc.add(comment("This file is created automatically on first run. Missing keys are"))
    doc.add(comment("auto-appended on subsequent reads. Edit freely; unknown keys are"))
    doc.add(comment("ignored and missing keys fall back to defaults."))
    for name, meta, default in _iter_keys():
        if default is None:
            continue  # absent-by-design (e.g. tools_to_install)
        doc.add(nl())
        for line in meta.comment.splitlines():
            doc.add(comment(line))
        doc.add(name, item(default))
    return doc


def _load_doc(path: Path | None = None) -> TOMLDocument:
    """Read the config file as a tomlkit Document, creating defaults on first access.

    Returns a fresh default Document when the file is missing or unreadable.
    Auto-appends any expected key (with default value) that is missing from
    an existing file.
    """
    target = path if path is not None else CONFIG_FILE
    try:
        if path is None:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            doc = _new_default_doc()
            target.write_text(tomlkit.dumps(doc), encoding="utf-8")
            return doc
        try:
            doc = tomlkit.parse(target.read_text(encoding="utf-8"))
        except TOMLKitError:
            return _new_default_doc()

        appended = False
        for name, meta, default in _iter_keys():
            if default is None:
                continue
            if name in doc:
                continue
            doc.add(nl())
            for line in meta.comment.splitlines():
                doc.add(comment(line))
            doc.add(name, item(default))
            appended = True
        if appended:
            try:
                target.write_text(tomlkit.dumps(doc), encoding="utf-8")
            except OSError:
                pass
        return doc
    except OSError:
        return _new_default_doc()


def _save_doc(doc: TOMLDocument, path: Path | None = None) -> None:
    target = path if path is not None else CONFIG_FILE
    try:
        if path is None:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        target.write_text(tomlkit.dumps(doc), encoding="utf-8")
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Sub-tables — for grouped settings owned by a feature (e.g. the usage hook)
# ---------------------------------------------------------------------------


def _to_plain(value: object) -> object:
    """Coerce a tomlkit item back to a plain Python value (recursively for lists/tables)."""
    if isinstance(value, bool):
        return bool(value)
    if isinstance(value, int):
        return int(value)
    if isinstance(value, float):
        return float(value)
    if isinstance(value, str):
        return str(value)
    if isinstance(value, dict):
        return {str(k): _to_plain(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_to_plain(v) for v in value]
    return value


def get_subtable(name: str, path: Path | None = None) -> dict[str, object]:
    """Return the ``[name]`` table as a plain dict (empty when absent or not a table)."""
    raw = _load_doc(path).get(name)
    if isinstance(raw, dict):
        return {str(k): _to_plain(v) for k, v in raw.items()}
    return {}


def _fill_table(tbl: object, values: dict[str, object]) -> None:
    """Populate a tomlkit table from ``values``, recursing into nested dicts as sub-tables.

    Scalars are written before nested tables: in TOML, once a ``[parent.child]`` header is
    opened every following bare key belongs to it, so the parent's own scalars must come first.
    """
    scalars = {k: v for k, v in values.items() if not isinstance(v, dict)}
    nested = {k: v for k, v in values.items() if isinstance(v, dict)}
    for key, value in scalars.items():
        tbl[key] = value  # type: ignore[index]
    for key, value in nested.items():
        sub = table()
        _fill_table(sub, value)
        tbl[key] = sub  # type: ignore[index]


def set_subtable(
    name: str,
    values: dict[str, object],
    comment_lines: tuple[str, ...] = (),
    path: Path | None = None,
) -> None:
    """Write (replacing) the ``[name]`` table with ``values``, with an optional header comment.

    Nested dicts in ``values`` are written as ``[name.sub]`` sub-tables.
    """
    doc = _load_doc(path)
    tbl = table()
    for line in comment_lines:
        tbl.add(comment(line))
    _fill_table(tbl, values)
    doc[name] = tbl
    _save_doc(doc, path)


def remove_subtable(name: str, path: Path | None = None) -> None:
    """Delete the ``[name]`` table if present (no-op otherwise)."""
    doc = _load_doc(path)
    if name in doc:
        del doc[name]
        _save_doc(doc, path)


def _config_from_doc(doc: TOMLDocument) -> Config:
    """Build a :class:`Config` from a parsed document, dropping keys that fail validation.

    A syntactically valid file may still hold an out-of-schema value (e.g. a
    string where a list is expected); such a key is ignored so it falls back to
    its default rather than crashing the load.
    """
    data = {name: _to_plain(doc[name]) for name in Config.model_fields if name in doc}
    try:
        return Config.model_validate(data)
    except ValidationError:
        clean: dict[str, object] = {}
        for key, value in data.items():
            try:
                Config.model_validate({key: value})
            except ValidationError:
                continue
            clean[key] = value
        return Config.model_validate(clean)


def load_config(path: Path | None = None) -> Config:
    """Load the user config, creating the default file or migrating it if needed."""
    return _config_from_doc(_load_doc(path))


def resolve_clone_dir(path: Path | None = None) -> Path:
    """Effective base directory for cloned projects.

    Precedence: ``$PYSAE_AI_TOOLS_GIT_CLONE_DIR`` env var > the ``git_clone_dir`` config
    value > the OS-standard default (:func:`os_default_clone_dir`).
    """
    env = os.environ.get("PYSAE_AI_TOOLS_GIT_CLONE_DIR", "")
    if env:
        return Path(env).expanduser()
    configured = load_config(path).git_clone_dir
    if configured:
        return Path(configured).expanduser()
    return os_default_clone_dir()


def set_git_clone_dir(value: str, path: Path | None = None) -> None:
    """Persist a new value for ``git_clone_dir`` to the config file."""
    doc = _load_doc(path)
    doc["git_clone_dir"] = value
    _save_doc(doc, path)


def get_tools_to_install(path: Path | None = None) -> list[str] | None:
    """Return the persisted tool selection, or ``None`` when the key is absent.

    The absence sentinel is what lets the install command know it should
    prompt on first run. An empty list means "configured to install nothing".
    """
    return load_config(path).tools_to_install


def set_tools_to_install(
    value: list[str],
    *,
    known: list[str] | None = None,
    path: Path | None = None,
) -> None:
    """Persist the selected tool list and the snapshot of currently-known tools.

    ``known`` records every tool that was visible to the user at this save
    time (typically every entry in ``TOOLS``). On a future configure run,
    a tool present in ``TOOLS`` but absent from ``tools_known_at_save``
    can be detected as new and fall back to its ``default_selected`` value
    instead of being silently treated as deselected.
    """
    doc = _load_doc(path)
    _upsert_key(doc, "tools_to_install", list(value))
    if known is not None:
        _upsert_key(doc, "tools_known_at_save", list(known))
    _save_doc(doc, path)


def _upsert_key(doc: TOMLDocument, key: str, value: bool | int | float | str | list[str]) -> None:
    if key in doc:
        doc[key] = value
        return
    meta = _key_meta(key)
    doc.add(nl())
    for line in meta.comment.splitlines():
        doc.add(comment(line))
    doc.add(key, item(value))


def get_tools_known_at_save(path: Path | None = None) -> list[str] | None:
    """Return the tools known at the last configure save, or ``None`` when absent.

    ``None`` means the user hasn't configured yet (or has only ever saved
    under the legacy schema that didn't include this key) — callers should
    treat that as "no known set, every tool is potentially new".
    """
    return load_config(path).tools_known_at_save
