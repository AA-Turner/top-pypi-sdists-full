from typing import Union, Any
from collections.abc import Callable, Awaitable
import importlib
from navconfig.logging import logging
from ..exceptions import ConfigError, FlowTaskError, ComponentError, NotSupported
from ..components import getComponent, importComponent
from ..components.abstract import AbstractFlow
from .actions.abstract import AbstractAction


_ACTIONS: dict[str, Any] = {}


def import_component(component: str, classpath: str, package: str = "components"):
    module = importlib.import_module(classpath, package=package)
    # module = importlib.import_module(f".{name.lower()}", package=module_path)
    obj = getattr(module, component, None)
    return obj


class StepAction:
    def __init__(self, action: str, params: dict, **kwargs) -> None:
        self.name = action
        self._step: Union[Callable, Awaitable] = None
        try:
            # Check if the action is already loaded
            if hasattr(self, "_action"):
                return
            # Check if the action is a function or a class
            action_cls = None
            if callable(action):
                self._action = action
            elif _ACTIONS.get(action):
                action_cls = _ACTIONS[action]
            else:
                # Load the action from the components module
                try:
                    action_cls = importComponent(action)
                except (NotSupported, ImportError):
                    pass
            if not action_cls:
                # Load the action from the actions module
                action_cls: AbstractAction = import_component(
                    action,
                    "flowtask.hooks.actions",
                    "actions"
                )
                if not action_cls:
                    raise ConfigError(
                        f"Unable to load Action: {action}"
                    )
            args = {**kwargs, **params}
            self._action = action_cls(**args)
            # saving into _ACTIONS variable
            _ACTIONS[action] = action_cls
        except (ImportError, RuntimeError) as exc:
            raise FlowTaskError(
                f"Unable to load Action {action}: {exc}"
            ) from exc
        self.params = args

    def __repr__(self) -> str:
        return f"<StepAction.{self.name}: {self.params!r}>"

    @property
    def component(self):
        return self._action

    async def run(self, hook, *args, **kwargs):
        """Run action involved"""
        try:
            try:
                async with self._action as step:
                    # Check if Step is a AbstractFlow to set the "self.data" property
                    if isinstance(step, AbstractFlow):
                        # Passing all arguments to the Flowtask component
                        step.data = kwargs
                        step.result = kwargs.get('result')
                        result = await step.run()
                    else:
                        result = await step.run(hook, *args, **kwargs)
                return result
            except Exception as exc:
                logging.error(
                    f"Error running action {self._action!s}: {exc}"
                )
        except Exception as exc:
            logging.error(
                f"Unable to load Action {self._action}: {exc}"
            )
            raise
