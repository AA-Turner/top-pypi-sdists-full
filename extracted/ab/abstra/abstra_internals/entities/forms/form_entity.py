from typing import List, Optional, TypedDict

from abstra_internals.entities.forms.form_state import State
from abstra_internals.entities.forms.steps import (
    ComputationStep,
    EndPageStep,
    GeneratorStep,
    PageStep,
    Step,
)
from abstra_internals.entities.forms.template import (
    BackButton,
    Button,
    ExitButton,
    NextButton,
    TemplateRenderer,
)
from abstra_internals.logger import AbstraLogger

BACK_ACTION_LABEL = BackButton().safe_get_key()
NEXT_ACTION_LABEL = NextButton().safe_get_key()
EXIT_ACTION_LABEL = ExitButton().safe_get_key()


class StepsInfo(TypedDict):
    current: int
    total: int
    disabled: Optional[bool]


class RenderedForm(TypedDict):
    widgets: List[dict]
    end_page: bool
    steps_info: StepsInfo
    buttons: List[Button]
    yielding: bool


class ButtonAction(TypedDict):
    key: str
    label: str


def _is_empty(value) -> bool:
    return value is None or value == "" or value == [] or value == {}


class NavigationAction:
    pass


class ExitNavigationAction(NavigationAction):
    pass


class FormEntity:
    steps: List[Step]
    current_step_idx: int
    state: State
    hide_steps: bool

    def __init__(self, steps: List[Step], state: State, *, force_hide_steps: bool):
        self.steps = steps
        self.state = state
        self.hide_steps = force_hide_steps or self.total_pages == 1
        self.current_step_idx = 0

    def get_previous_page_idx(self) -> int:
        return next(
            self.current_step_idx - 1 - idx
            for idx, s in enumerate(self.steps[: self.current_step_idx][::-1])
            if isinstance(s, PageStep)
        )

    @property
    def total_pages(self) -> int:
        return len(list(filter(lambda s: isinstance(s, PageStep), self.steps)))

    @property
    def current_page_idx(self) -> int:
        return len(
            list(
                filter(
                    lambda s: isinstance(s, PageStep),
                    self.steps[: self.current_step_idx],
                )
            )
        )

    def get_default_buttons(self, step_idx: int) -> List[Button]:
        if isinstance(self.steps[step_idx], (EndPageStep, ComputationStep)):
            return []
        if step_idx == 0:
            return [NextButton()]
        return [BackButton(), NextButton()]

    def run(self) -> Optional[RenderedForm]:
        steps_info = StepsInfo(
            current=self.current_page_idx + 1,
            total=self.total_pages,
            disabled=self.hide_steps,
        )

        if self.current_step_idx >= len(self.steps):
            return None

        step = self.steps[self.current_step_idx]
        result = step.run(self.state)

        if result is None:
            self.current_step_idx += 1
            return self.run()

        template, buttons = result

        if buttons is None:
            buttons = self.get_default_buttons(self.current_step_idx)

        renderer = TemplateRenderer(template)
        output = renderer.render(self.state)

        return RenderedForm(
            widgets=output["widgets"],
            end_page=isinstance(step, EndPageStep),
            steps_info=steps_info,
            buttons=buttons,
            yielding=isinstance(step, GeneratorStep),
        )

    def handle_navigation(self, dto: dict) -> Optional[NavigationAction]:
        step = self.steps[self.current_step_idx]

        if not isinstance(step, PageStep):
            raise Exception(f"Internal error: navigation on non-page step {step}")

        if dto["action"] == BACK_ACTION_LABEL:
            if self.current_step_idx == 0:
                raise Exception("Internal error: reached negative step index")
            self.current_step_idx = self.get_previous_page_idx()
            return

        if dto["action"] == EXIT_ACTION_LABEL:
            return ExitNavigationAction()

        if dto["action"] == NEXT_ACTION_LABEL:
            result = step.run(self.state)

            if result is None:
                raise Exception("Internal error: next action None result")

            template, _ = result

            renderer = TemplateRenderer(template)
            parsed = renderer.parse_state(
                raw_state=dto["payload"], include_missing=True
            )
            payload = dto["payload"]
            # TEMP diagnostic (no PII): snapshot which keys already held a value
            # in the state right before the navigation payload overwrites it, so
            # the error diagnostic below can distinguish a value lost by
            # navigation from one the client cleared. Remove once the
            # form-not-detecting-filled-fields investigation is closed.
            state_had_value = {
                key: not _is_empty(self.state.get(key)) for key in parsed
            }
            self.state.update(parsed)

            output = renderer.render(self.state)

            if output["has_errors"]:
                self._log_navigation_validation_diagnostics(
                    output["widgets"], payload, state_had_value
                )
                return

            self.current_step_idx += 1
            return
        else:
            self.state[dto["action"]] = True
            return

    def _log_navigation_validation_diagnostics(
        self, widgets: List[dict], payload: dict, state_had_value: dict
    ) -> None:
        # TEMP diagnostic (no PII): when a field blocks navigation with a
        # required error, record — from backend logs only — whether the client
        # omitted the key (value lost in transit), sent it empty (frontend
        # cleared it), and whether the state held a value just before the merge.
        # Lets us tell, without any frontend logs, a navigation-side value loss
        # from a frontend race. Remove once the form-not-detecting-filled-fields
        # investigation is closed.
        for widget in widgets:
            errors = widget.get("errors") or []
            if not errors:
                continue
            key = widget.get("key")
            AbstraLogger.lifecycle(
                "form_nav_required_error",
                attrs={
                    "widget_key": key,
                    "widget_type": widget.get("type"),
                    "present_in_payload": key in payload,
                    "payload_value_empty": _is_empty(payload.get(key)),
                    "state_had_value_before": state_had_value.get(key, False),
                    "page": self.current_page_idx,
                },
            )

    def handle_input(self, dto: dict) -> None:
        step = self.steps[self.current_step_idx]

        if not isinstance(step, PageStep):
            raise Exception(f"Internal error: input on non-page step {step}")

        result = step.run(self.state)

        if result is None:
            raise Exception("Internal error: input None result")

        template, _ = result
        renderer = TemplateRenderer(template)

        parsed = renderer.parse_state(raw_state=dto["payload"], include_missing=False)
        # TEMP diagnostic (no PII): log when the client clears a field that
        # currently holds a value in the state. This is the backend-visible
        # signature of the reactive "value clobber" — e.g. a DropdownInput
        # emitting an empty value on a keystroke/blur — which then renders as a
        # spurious required error on an otherwise-filled field. Remove once the
        # form-not-detecting-filled-fields investigation is closed.
        for key, value in parsed.items():
            if _is_empty(value) and not _is_empty(self.state.get(key)):
                AbstraLogger.lifecycle(
                    "form_input_value_cleared",
                    attrs={"widget_key": key, "page": self.current_page_idx},
                )
        self.state.update(parsed)
