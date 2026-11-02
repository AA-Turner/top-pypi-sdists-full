"""Check, before a Session starts, that each Hook can be rebuilt from its saved fields.

Each Hook runs through a ``StatefulRow``: a Hook with fields runs each call on a copy rebuilt from
its Session's saved value, and a Hook without fields runs on its one authored object.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from collections.abc import Set as AbstractSet

from mistralai.vibe_agents.sdk.authoring import contracts, stateful
from mistralai.vibe_agents.sdk.authoring.errors import SdkError

from .stateful import SavedStateTooLargeError, check_rebuildable, check_starting_values


def check_hooks_rebuildable(layers: Iterable[tuple[tuple[str, ...], Sequence[contracts.Hook]]]) -> None:
    """Fail at assembly, on every host, for a Hook that could not be rebuilt from its saved fields.

    ``layers`` gives the Hooks of the root, under the path ``()``, and of each subagent, under its
    path. Importing the path of each Hook class must give the class back. A Hook with fields is
    rebuilt on each call, so the path of each stateful class its fields hold must give the class
    back too, its fields must hold no cycle, no old-style Hook and no set of Hooks, and the rebuilt
    Hook must hold the same values. The starting state of the Hooks of one layer must be within the
    size limits of saved state.
    """

    checked: set[type] = set()
    for path, hooks in layers:
        owner = f" on subagent {'/'.join(path)!r}" if path else ""
        saved: list[contracts.Hook] = []
        for hook in hooks:
            label = f"Hook {type(hook).__name__}{owner}"
            try:
                stateful.check_importable(type(hook))
            except TypeError as error:
                raise SdkError(f"{label} cannot be rebuilt: {error}") from error
            checked.add(type(hook))
            if not type(hook).model_fields:
                continue
            try:
                _check_held_values(hook, label, checked)
                check_rebuildable(hook)
            except TypeError as error:
                raise SdkError(f"{label} cannot be rebuilt from its fields: {error}") from error
            saved.append(hook)
        try:
            check_starting_values(saved)
        except SavedStateTooLargeError as error:
            raise SdkError(f"Hooks{owner} start with state too large to save: {error}") from error


def _check_held_values(hook: contracts.Hook, label: str, checked: set[type]) -> None:
    for place, value in stateful.walk(hook, type(hook).__name__):
        if isinstance(value, AbstractSet) and any(
            isinstance(item, contracts.Hook) for _, item in stateful.walk(value, place)
        ):
            # A Hook hashes by identity, so a copy of the set lists its Hooks in another order, and
            # the copy's saved value differs.
            raise SdkError(f"{label} keeps Hooks in a set in {place}; keep them in a list or a tuple")
        if isinstance(value, stateful.StatefulModel) and type(value) not in checked:
            stateful.check_importable(type(value))
            checked.add(type(value))
        reason = contracts.legacy_hook_reason(value) if isinstance(value, contracts.Hook) else None
        if reason is not None:
            raise SdkError(
                f"{label} cannot keep an old-style Hook in {place}: {reason}; declare it as a field or a PrivateAttr"
            )


__all__ = ["check_hooks_rebuildable"]
