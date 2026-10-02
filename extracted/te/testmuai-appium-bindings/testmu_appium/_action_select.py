"""select — picker widgets.

Three modes ship, chosen from the widget's class:

- spinner / dropdown → tap to open, then tap the option whose text matches. Native
  Android spinners render their options as a list, so this is a two-tap interaction
  rather than a value assignment.
- NumberPicker → scroll the wheel toward the target, re-reading the displayed value
  each round. Bounded, and it gives up when a full pass makes no progress: a target
  that is not in the picker's range would otherwise scroll forever.
- SeekBar / slider (plain) → drag the thumb to the requested percentage of the track.

Two modes are DEFERRED and raise PickerModeNotSupported naming the widget class:

- SeekBar wheel-COLUMN pickers (the AM/PM, month and other cyclic columns rendered as
  a SeekBar): the legacy implementation walks the column with a cycle guard and
  ordering rules per column type, and porting it faithfully needs the legacy
  ordering tables.
- Clock-face DIAL pickers: the legacy implementation converts the target value to an
  angle on the dial and drags to it; the value→angle mapping differs per dial mode
  (hour, minute, 12 vs 24 hour).
"""
from dataclasses import dataclass
from typing import Optional

from testmu_appium._action_engine import _ActionSpec, _run_action
from testmu_appium._helpers.picker import select_picker
from testmu_appium._vars import var


@dataclass(frozen=True)
class _Target:
    """The recorded ways of naming an option, kept apart until the mode is known.

    SelectAction records up to three, and which one applies depends on the widget, so
    all three are carried to the mode that picks between them. Empty strings mean "not
    recorded"; `index` uses None for the same, so a recorded index of 0 stays a real
    target rather than a falsy miss.
    """

    value: str = ""
    label: str = ""
    index: Optional[int] = None

    @property
    def visible_text(self) -> str:
        """What the screen renders — the label, else the value.

        For a spinner the option is matched by its on-screen text, so the LABEL is the
        better guess and the value is the fallback for a recording that carried no
        label at all.
        """
        return self.label or self.value

    @property
    def data_text(self) -> str:
        """The option's data — the value, else the label.

        A NumberPicker or a slider is set to a NUMBER, which is what `value` carries;
        the label is its rendering ("50%", "Half") and only stands in when no value
        was recorded.
        """
        return self.value or self.label


def _text(recorded) -> str:
    """A recorded target field as resolved text, or "" when nothing was recorded."""
    if recorded is None or str(recorded) == "":
        return ""
    return var(str(recorded))


def _resolve_target(value, label, index) -> _Target:
    """Carry SelectAction's three target fields through, resolving `{{var}}` tokens."""
    target = _Target(
        value=_text(value),
        label=_text(label),
        index=int(index) if index is not None else None,
    )
    if not target.value and not target.label and target.index is None:
        raise ValueError(
            "select() requires one of value, label or index — none was recorded"
        )
    return target


def _runner(element, ctx):
    return select_picker(
        ctx["driver"], element, ctx["target"], ctx.get("mode") or "auto"
    )


# No coordinate fallback: a picker interaction is a sequence against a widget whose
# geometry is the whole point — a single recorded point cannot stand in for it.
_SELECT_SPEC = _ActionSpec(runner=_runner, target_mode="element", op_type="select")


def select(driver, *, selectors, value=None, label=None, index=None,
           description: str = "", mode: str = "auto",
           fallback_coordinates: dict | None = None):
    """Set a picker widget to the recorded target.

    SelectAction records up to three ways of naming the option; at least one is
    required, and all three are carried through to the mode that knows which one
    applies. A spinner matches on the text the screen RENDERS, so it prefers `label`
    and falls back to `value`; a NumberPicker or slider is set to a NUMBER, so it
    prefers `value` and falls back to `label`. `index` is positional, applies to
    list-style pickers only, and is used only when no text was recorded at all.

    mode: "auto" (detect from the widget class), or one of "spinner",
    "number_picker", "slider". "wheel_column" and "dial" are recognised and raise
    PickerModeNotSupported.
    """
    return _run_action(
        driver, _SELECT_SPEC, selectors,
        description=description,
        fallback_coordinates=fallback_coordinates,
        target=_resolve_target(value, label, index), mode=mode,
    )
