r"""Hatchling metadata hook to automatically generate 'all' extras.

Properties of the hook:

- **Union of the extras**: the generated extra contains every
  dependency string of every non-excluded extra, and nothing else. It
  never contains its own previous content. The strings are copied, not
  interpreted (see the self-references below). If there is nothing to
  collect, the generated extra is empty, so that ``pkg[all]`` stays
  installable.
- **Deterministic**: the output is the list of the distinct stripped
  dependency strings, sorted as strings (code point order, so ``Zed``
  comes before ``alpha``), whatever the order of the extras. The
  generated extra is always the last key of the table, whether it is
  new, replaced or renamed by ``overwrite``.
- **Additive**: the original extras are never modified, reordered or
  removed. Only the generated extra is added (or replaced when
  ``overwrite = true``).
- **Atomic**: ``update`` either completes or raises with ``metadata``
  unchanged.
- **Idempotent on request**: with ``overwrite = true``, running
  ``update`` again on its own output gives the same metadata. With
  ``overwrite = false`` the second run raises, because the extra exists.
- **Name-normalized**: the extra names are compared after the
  normalization of PEP 685 (``Dev_Extra``, ``dev-extra`` and
  ``dev.extra`` are the same extra).
- **Strict**: by default, an unknown option, a wrong type, an invalid
  name, a non-string or blank dependency and an ``exclude`` entry that
  matches no extra raise. Nothing is ignored silently.
- **Lenient on request**: with ``HATCHLING_AUTOEXTRAS_WARN_ONLY=1``,
  the two recoverable problems (unknown option, unmatched ``exclude``
  entry) emit a ``UserWarning``. Every other problem still raises.
- **Output-invariant**: the warn-only mode never changes the generated
  extra. A build that succeeds in both modes produces the same
  metadata: the mode only turns an error into a warning for a problem
  that has no effect on the result.
- **Early and named errors**: the configuration errors are raised when
  the hook is created, before any metadata is read. Every message of a
  configuration problem names the option and the table
  ``[tool.hatch.metadata.hooks.autoextras]``. The metadata errors name
  the extra and the position of the faulty entry.
- **Pure besides ``metadata``**: ``update`` reads the validated options
  and mutates only ``metadata``. No file access, no global state, no
  state kept between calls. The only environment read is
  ``HATCHLING_AUTOEXTRAS_WARN_ONLY``, once, when the hook is created.
- **Minimal**: one runtime dependency (``hatchling``). One hook class,
  one entry point, ``__version__``. Three options, all keyword-style
  entries of the ``pyproject.toml`` hook table.
- **Observable**: what was generated is logged at ``DEBUG`` level.

Not guaranteed: the validity of a requirement (the requirements are not
parsed: an invalid one is copied and rejected by hatchling), the
semantic deduplication (``numpy>=2`` and ``numpy >= 2`` are two strings,
hatchling merges them afterwards), the self-references (``docs =
["pkg[dev]"]`` is a string like any other: with ``exclude = ["dev"]``,
the generated extra contains ``pkg[dev]`` or the dependencies of
``dev``, depending on whether the hatchling version resolves the
reference), PEP 735 dependency groups, the hatchling option
``allow-ambiguous-features``, and the runs of the hook: hatchling runs a
metadata hook only when ``project.dynamic`` is not empty, and the hook
cannot detect that it was not called.
"""

from __future__ import annotations

__all__ = ["AutoExtrasMetadataHook"]

import copy
import logging
import os
import re
import warnings
from typing import Any

from hatchling.metadata.plugin.interface import MetadataHookInterface
from hatchling.plugin import hookimpl

logger: logging.Logger = logging.getLogger(__name__)

# The options of the hook and their default values. This table is the single
# source of truth for the allowed keys of the hook table.
_DEFAULTS: dict[str, Any] = {"extra-name": "all", "exclude": [], "overwrite": False}

# The table of the configuration, named by the messages of the configuration problems.
_TABLE = "[tool.hatch.metadata.hooks.autoextras]"

# Valid name of an extra: the rule of hatchling (`is_valid_project_name`). It is
# copied because `hatchling.metadata.utils` is not public API.
_NAME_PATTERN = re.compile(r"^([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9._-]*[A-Za-z0-9])$")

# Environment variable that downgrades the recoverable problems to warnings.
_WARN_ONLY_ENV = "HATCHLING_AUTOEXTRAS_WARN_ONLY"
_WARN_ONLY_TRUE = frozenset({"1", "true", "yes", "on"})
_WARN_ONLY_FALSE = frozenset({"0", "false", "no", "off", ""})


class AutoExtrasMetadataHook(MetadataHookInterface):
    r"""Metadata hook that automatically generates an 'all' extra.

    This hook collects all optional dependencies defined in the project
    and creates an 'all' extra that includes all of them.

    Configuration options (in pyproject.toml):
        extra-name: Name of the generated extra (default: "all")
        exclude: List of extra names to exclude from the generated extra (default: [])
        overwrite: Whether to overwrite an existing extra (default: False)

    Extra names are compared after the normalization of PEP 685, like
    hatchling does: ``Dev_Extra``, ``dev-extra`` and ``dev.extra`` are
    the same extra. This applies to ``extra-name``, ``exclude`` and to
    the check of an existing extra with the generated name.

    Unknown options are rejected with a ``ValueError``. The environment
    variable ``HATCHLING_AUTOEXTRAS_WARN_ONLY`` downgrades the
    recoverable problems to a ``UserWarning``: see the properties in the
    module docstring and "Strict and warn-only modes" in the README for
    the accepted values.

    Example configuration:
        [tool.hatch.metadata.hooks.autoextras]
        extra-name = "complete"
        exclude = ["dev", "test"]
        overwrite = false

    Example usage:

    ```pycon

    >>> from hatchling_autoextras_hook import AutoExtrasMetadataHook
    >>> metadata = {
    ...     "optional-dependencies": {
    ...         "dev": ["pytest>=7.0", "black>=22.0"],
    ...     }
    ... }
    >>> hook = AutoExtrasMetadataHook("test", {})
    >>> hook.update(metadata)
    >>> metadata
    {'optional-dependencies': {'dev': ['pytest>=7.0', 'black>=22.0'],
     'all': ['black>=22.0', 'pytest>=7.0']}}

    ```
    """

    PLUGIN_NAME: str = "autoextras"

    def __init__(self, root: str, config: dict[str, Any]) -> None:
        """Initialize the hook and validate configuration.

        Args:
            root: The root directory of the project.
            config: The plugin configuration dictionary.

        Raises:
            ValueError: If an unknown option is given (a warning in the
                warn-only mode), if ``extra-name`` is not a valid extra
                name, if ``exclude`` contains the generated extra, or
                if the environment variable
                ``HATCHLING_AUTOEXTRAS_WARN_ONLY`` has an unrecognized
                value.
            TypeError: If ``extra-name`` is not a string, ``exclude`` is
                not a list of strings or ``overwrite`` is not a boolean.
        """
        self._warn_only: bool = _read_warn_only()
        unknown = sorted(config.keys() - _DEFAULTS.keys())
        if unknown:
            self._report(
                f"Unknown option(s) in {_TABLE}: {unknown}. Valid options: {sorted(_DEFAULTS)}"
            )
        known = {key: value for key, value in config.items() if key in _DEFAULTS}
        super().__init__(root, copy.deepcopy(_DEFAULTS) | known)
        self._validate_config()

    def _report(self, msg: str) -> None:
        """Report a recoverable problem.

        The problem raises a ``ValueError`` by default. In warn-only
        mode, it emits a ``UserWarning`` and the build continues.

        Args:
            msg: The message that describes the problem.

        Raises:
            ValueError: If the warn-only mode is not enabled.
        """
        if not self._warn_only:
            raise ValueError(msg)
        warnings.warn(msg, UserWarning, stacklevel=2)

    def _validate_config(self) -> None:
        """Validate the plugin configuration.

        Raises:
            ValueError: If any configuration option is invalid, or if
                ``exclude`` contains the generated extra.
            TypeError: If any configuration option has a wrong type.
        """
        extra_name = self.config["extra-name"]
        if not isinstance(extra_name, str):
            msg = f"'extra-name' in {_TABLE} must be a string"
            raise TypeError(msg)
        if not _NAME_PATTERN.fullmatch(extra_name):
            msg = (
                f"'extra-name' in {_TABLE} must be a valid extra name (letters, digits, '-', "
                f"'_' and '.', starting and ending with a letter or a digit), got {extra_name!r}"
            )
            raise ValueError(msg)

        exclude = self.config["exclude"]
        if not isinstance(exclude, list) or not all(isinstance(name, str) for name in exclude):
            msg = f"'exclude' in {_TABLE} must be a list of extra names"
            raise TypeError(msg)

        overwrite = self.config["overwrite"]
        if not isinstance(overwrite, bool):
            msg = f"'overwrite' in {_TABLE} must be a boolean"
            raise TypeError(msg)

        # The validated options are stored once: `update` never reads `self.config`
        self._extra_name: str = extra_name  # written to the metadata, as spelled by the user
        self._extra: str = _normalize(extra_name)  # compared
        self._exclude: frozenset[str] = frozenset(_normalize(name) for name in exclude)
        self._overwrite: bool = overwrite
        if self._extra in self._exclude:
            msg = f"'exclude' in {_TABLE} must not contain the generated extra '{extra_name}'"
            raise ValueError(msg)

    def update(self, metadata: dict[str, Any]) -> None:
        r"""Update the project metadata to add the configured extra.

        This method collects all dependencies from all optional extras
        (excluding any existing extra with the configured name and any
        extras in the exclude list), removes duplicate strings, sorts
        them as strings, and creates/updates the generated extra with
        the combined list. Two dependencies are duplicates if they are
        the same string after stripping the whitespace around them:
        the requirements are not parsed, hatchling merges the
        equivalent ones afterwards.

        Everything is validated before ``metadata`` is modified, so
        ``metadata`` is unchanged if this method raises.

        Args:
            metadata: The project metadata dictionary to update. This
                dictionary is modified in place.

        Raises:
            ValueError: If an extra with the configured extra name
                already exists and overwrite is False, if ``exclude``
                contains a name that matches no extra (a warning in the
                warn-only mode), or if a dependency is a blank string.
            TypeError: If optional dependencies are not in the expected
                format: the table of extras, the dependencies of an
                extra and each dependency must be a table, a list and a
                string respectively.

        Note:
            If no optional dependencies exist, an empty extra is
            created. Any pre-existing extra with that name is completely
            replaced if overwrite is True. The dependencies of an
            excluded extra are not inspected.
        """
        optional_dependencies = metadata.get("optional-dependencies", {})
        if not isinstance(optional_dependencies, dict):
            msg = "'optional-dependencies' must be a table of extras"
            raise TypeError(msg)

        by_name = {_normalize(name): name for name in optional_dependencies}
        existing = by_name.get(self._extra)
        if existing is not None and not self._overwrite:
            msg = (
                f"Cannot create the '{self._extra_name}' extra: '{existing}' already exists. "
                f"Existing extras: {list(optional_dependencies)}. "
                f"Configure a different 'extra-name' in pyproject.toml or set 'overwrite = true'"
            )
            raise ValueError(msg)
        unmatched = sorted(self._exclude - by_name.keys())
        if unmatched:
            self._report(f"'exclude' in {_TABLE} contains names that match no extra: {unmatched}")

        # Collect the dependencies of the extras that are not excluded
        sources = [
            name
            for name in optional_dependencies
            if (key := _normalize(name)) != self._extra and key not in self._exclude
        ]
        dependencies = {
            dep for name in sources for dep in _dependencies(name, optional_dependencies[name])
        }

        # Everything is valid: the metadata is modified in one last step
        if existing is not None:
            logger.debug("Overwriting existing '%s' extra", existing)
            del optional_dependencies[existing]
        optional_dependencies[self._extra_name] = sorted(dependencies)
        # The key is absent from the metadata only if `optional_dependencies` is a new dict
        metadata["optional-dependencies"] = optional_dependencies

        logger.debug(
            "Created '%s' with %d dependencies from %d extras: %s",
            self._extra_name,
            len(dependencies),
            len(sources),
            sources,
        )


def _dependencies(name: str, value: object) -> list[str]:
    r"""Validate the dependencies of an extra and strip them.

    Args:
        name: The name of the extra, used in the error messages.
        value: The value of the extra in the metadata.

    Returns:
        The dependencies, stripped, in their original order.

    Raises:
        TypeError: If ``value`` is not a list, or if one of its items
            is not a string.
        ValueError: If one of the items is blank.

    Example usage:

    ```pycon

    >>> from hatchling_autoextras_hook.hooks import _dependencies
    >>> _dependencies("dev", [" pytest>=7.0 ", "black"])
    ['pytest>=7.0', 'black']

    ```
    """
    if not isinstance(value, list):
        msg = f"Dependencies of extra '{name}' must be a list of strings"
        raise TypeError(msg)
    dependencies = []
    for position, dep in enumerate(value, start=1):
        if not isinstance(dep, str):
            msg = f"Dependency #{position} of extra '{name}' must be a string, got {dep!r}"
            raise TypeError(msg)
        if not (stripped := dep.strip()):
            msg = f"Dependency #{position} of extra '{name}' must not be blank"
            raise ValueError(msg)
        dependencies.append(stripped)
    return dependencies


def _normalize(name: str) -> str:
    r"""Normalize the name of an extra (PEP 685 and PEP 503).

    Args:
        name: The name of the extra.

    Returns:
        The normalized name: lowercase, with every run of ``-``, ``_``
            and ``.`` replaced by one ``-``.

    Example usage:

    ```pycon

    >>> from hatchling_autoextras_hook.hooks import _normalize
    >>> _normalize("Dev_Extra")
    'dev-extra'

    ```
    """
    return re.sub(r"[-_.]+", "-", name).lower()


def _read_warn_only() -> bool:
    r"""Read the warn-only mode from the environment.

    Returns:
        ``True`` if ``HATCHLING_AUTOEXTRAS_WARN_ONLY`` is set to ``1``,
            ``true``, ``yes`` or ``on`` (case-insensitive), ``False`` if
            it is unset, empty or set to ``0``, ``false``, ``no`` or
            ``off``.

    Raises:
        ValueError: If the variable has any other value.

    Example usage:

    ```pycon

    >>> import os
    >>> from hatchling_autoextras_hook.hooks import _read_warn_only
    >>> os.environ["HATCHLING_AUTOEXTRAS_WARN_ONLY"] = "On"
    >>> _read_warn_only()
    True
    >>> del os.environ["HATCHLING_AUTOEXTRAS_WARN_ONLY"]
    >>> _read_warn_only()
    False

    ```
    """
    value = os.environ.get(_WARN_ONLY_ENV, "").strip().lower()
    if value in _WARN_ONLY_TRUE:
        return True
    if value in _WARN_ONLY_FALSE:
        return False
    msg = (
        f"Invalid value {os.environ[_WARN_ONLY_ENV]!r} for the environment variable "
        f"{_WARN_ONLY_ENV}. Use one of {sorted(_WARN_ONLY_TRUE | _WARN_ONLY_FALSE - {''})} "
        "(or leave it unset)"
    )
    raise ValueError(msg)


@hookimpl
def hatch_register_metadata_hook() -> type[MetadataHookInterface]:
    r"""Register the autoextras metadata hook with hatchling.

    This function is called by Hatchling's plugin system to register
    the AutoExtrasMetadataHook as a metadata hook plugin.

    Returns:
        The AutoExtrasMetadataHook class that implements the metadata
        hook interface.
    """
    return AutoExtrasMetadataHook
