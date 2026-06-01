"""Composable step wizard with automatic back-navigation."""

from collections.abc import Callable
from contextlib import suppress

from .exceptions import GoBack

# Each step callable receives the accumulated state dict and either:
#   - returns normally (step advances)
#   - raises GoBack   (step goes back)
# Steps mutate the shared state dict to pass data between steps.

WizardStep = Callable[[dict[str, object]], None]
WizardCleanup = Callable[[dict[str, object]], None]

WIZARD_INTERRUPTED = "INTERRUPTED"


def run_wizard(
    steps: list[WizardStep],
    *,
    on_cancel: WizardCleanup | None = None,
    initial_state: dict[str, object] | None = None,
) -> dict[str, object] | None:
    """Execute a sequence of prompt steps with automatic back-navigation.

    Each step is a callable that receives a shared ``state`` dict and
    mutates it to record collected values.  Steps communicate through
    the state dict (e.g. ``state["name"] = "my-workspace"``).

    - If a step returns normally, the wizard advances to the next step.
    - If a step raises ``GoBack``, the wizard moves back one step.
    - ``GoBack`` at step 0 returns ``None`` (cancel).
    - ``KeyboardInterrupt`` at any step returns a state dict with
      ``_interrupted = True`` and prints ``"Cancelled."``.

    *on_cancel* is an optional cleanup callback invoked with the current
    state dict whenever the wizard is cancelled (Escape at step 0) or
    interrupted (Ctrl-C).  Use it to remove partially-created artifacts.

    *initial_state* is an optional dict to pre-populate the wizard state.

    Returns the final state dict on success, ``None`` on Escape-cancel,
    or a state with ``_interrupted`` flag on Ctrl-C.
    """

    state: dict[str, object] = dict(initial_state) if initial_state else {}
    idx = 0

    try:
        while idx < len(steps):
            try:
                steps[idx](state)
                idx += 1
            except GoBack:
                if idx == 0:
                    if on_cancel is not None:
                        on_cancel(state)
                    print("Cancelled.")
                    return None
                idx -= 1
    except KeyboardInterrupt:
        if on_cancel is not None:
            on_cancel(state)
        with suppress(KeyboardInterrupt):
            print("\nCancelled.")
        state[WIZARD_INTERRUPTED] = True
        return state

    return state
