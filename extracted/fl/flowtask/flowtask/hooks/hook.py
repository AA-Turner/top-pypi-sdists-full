from uuid import uuid4
from navconfig.logging import logging
from ..exceptions import ConfigError
from .step import StepAction, import_component


class Hook:
    """Hook.

    Compile a Hook (Triggers and Actions) and got every step on the hook.
    """

    def __init__(self, hook: dict):
        self.triggers: list = []
        self.logger = logging.getLogger(name='Flowtask.Hook')
        self._id = hook.pop("id", uuid4())
        self.name = hook.pop("name")
        try:
            triggers = hook["When"]
        except KeyError as exc:
            raise ConfigError(
                "Hook Error: Unable to find Trigger: *When* parameter"
            ) from exc
        try:
            actions = hook["Then"]
        except KeyError as exc:
            raise ConfigError(
                "Hook Error: Unable to get list of Actions: *Then* parameter"
            ) from exc
        ## build Hook Component:
        self.build(triggers, actions)

    def build(self, triggers: list, actions: list):
        self._actions: list = []
        # "Then": Load Actions
        for step in actions:
            for step_name, params in step.items():
                action = StepAction(step_name, params)
                self._actions.append(action)
        for step in triggers:
            # When: Load Triggers
            # Triggers are listener for events.
            for step_name, params in step.items():
                trigger_cls = import_component(step_name, "flowtask.hooks.types", "types")
                if trigger_cls:
                    # start trigger:
                    args = {"name": self.name, "actions": self._actions}
                    args = {**args, **params}
                    try:
                        hook = trigger_cls(**args)
                        self.triggers.append(hook)
                        self.logger.debug(
                            f":: Loading Hook {self.name}"
                        )
                    except Exception as exc:
                        self.logger.error(
                            f"Unable to load Trigger {step_name}: {exc}"
                        )
                else:
                    self.logger.warning(
                        f"Unable to load Trigger: {step_name}"
                    )
