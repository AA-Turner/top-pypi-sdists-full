"""Name the ``AGENTS_SDK_`` environment variables that no setting reads.

The settings classes ignore extra variables, so a misspelt or retired name would
otherwise change nothing without a word. This module warns about each one, or
refuses them all when ``AGENTS_SDK_STRICT_SETTINGS`` is on.
"""

from __future__ import annotations

import difflib
import os
import warnings
from collections.abc import Iterable, Mapping

from pydantic import AliasChoices
from pydantic_settings import BaseSettings

ENV_PREFIX = "AGENTS_SDK_"
STRICT_ENV = "AGENTS_SDK_STRICT_SETTINGS"
# Read with os.environ or by a CLI option, outside any settings class.
READ_DIRECTLY = frozenset(
    {"AGENTS_SDK_DEBUG", "AGENTS_SDK_EXPERIMENTAL_WARNINGS", STRICT_ENV, "AGENTS_SDK_SERVE_SEND_CONFIG"}
)
# Owned by the agents_sdk end-to-end tests, never by the SDK.
TEST_PREFIX = "AGENTS_SDK_E2E_"
# The values AGENTS_SDK_STRICT_SETTINGS accepts; any other refuses to start.
_TRUE = frozenset({"1", "true", "yes", "on"})
_FALSE = frozenset({"", "0", "false", "no", "off"})
# Names the SDK once read, with what to do now.
RETIRED = {
    "AGENTS_SDK_REMOTE_RUNTIME": "the SDK no longer reads it; remove it",
}


class UnusedEnvironmentError(ValueError):
    """Strict mode refuses variables the SDK does not read, or the strict switch is not a boolean."""


def settings_env_names(classes: Iterable[type[BaseSettings]]) -> frozenset[str]:
    """Every ``AGENTS_SDK_`` variable a field of ``classes`` reads, in upper case."""

    names: set[str] = set()
    for settings_class in classes:
        prefix = str(settings_class.model_config.get("env_prefix") or "")
        for field_name, field in settings_class.model_fields.items():
            alias = field.validation_alias
            if isinstance(alias, AliasChoices):
                names.update(choice for choice in alias.choices if isinstance(choice, str))
            elif isinstance(alias, str):
                names.add(alias)
            else:
                names.add(prefix + (field.alias or field_name))
    return frozenset(name.upper() for name in names if name.upper().startswith(ENV_PREFIX))


def unused_env_messages(environ: Mapping[str, str], known: frozenset[str]) -> list[str]:
    """One line for each ``AGENTS_SDK_`` variable in ``environ`` that nothing reads."""

    messages: list[str] = []
    for name in sorted(environ):
        upper = name.upper()
        if not upper.startswith(ENV_PREFIX) or upper.startswith(TEST_PREFIX):
            continue
        if upper in known or upper in READ_DIRECTLY:
            continue
        if upper in RETIRED:
            messages.append(f"{name}: {RETIRED[upper]}")
            continue
        close = difflib.get_close_matches(upper, sorted(known | READ_DIRECTLY), n=1, cutoff=0.8)
        hint = f" (did you mean {close[0]}?)" if close else ""
        messages.append(f"{name} is not an agents SDK setting{hint}")
    return messages


def strict_mode(environ: Mapping[str, str]) -> bool:
    """Whether ``AGENTS_SDK_STRICT_SETTINGS`` is on; a value that is not a boolean is refused, not read as off.

    Read like the settings classes read their variables: in any casing, and of
    two casings the last one in the environment counts. A casing whose value is
    not a boolean is refused even when another one counts.
    """

    value = ""
    for name, raw in environ.items():
        if name.upper() != STRICT_ENV:
            continue
        value = raw.strip().lower()
        if value not in _TRUE | _FALSE:
            raise UnusedEnvironmentError(
                f"{name}={raw!r} is not a boolean. Use 1, true, yes or on to refuse unread variables, "
                "or 0, false, no or off to warn about them."
            )
    return value in _TRUE


def check_environment(
    classes: Iterable[type[BaseSettings]],
    environ: Mapping[str, str] | None = None,
) -> None:
    """Warn about each ``AGENTS_SDK_`` variable nothing reads, or refuse them in strict mode."""

    environ = os.environ if environ is None else environ
    strict = strict_mode(environ)
    messages = unused_env_messages(environ, settings_env_names(classes))
    if not messages:
        return
    listed = "\n".join(f"- {message}" for message in messages)
    if strict:
        raise UnusedEnvironmentError(
            f"{STRICT_ENV} is on and the environment sets variables the agents SDK does not read:\n{listed}"
        )
    warnings.warn(
        f"The agents SDK ignores these environment variables:\n{listed}",
        UserWarning,
        stacklevel=3,
    )
