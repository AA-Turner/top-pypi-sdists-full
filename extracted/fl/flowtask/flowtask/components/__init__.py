from typing import Any
import asyncio
from pathlib import Path
import importlib
from concurrent.futures import ThreadPoolExecutor
from navconfig.logging import logging, logger
from ..exceptions import NotSupported, ComponentError
from ..download import download_component
from .abstract import AbstractFlow
from .flow import FlowComponent
from .user import UserComponent
from .group import GroupComponent


__all__ = (
    "AbstractFlow",
    "FlowComponent",
    "UserComponent",
    "GroupComponent",
)

_COMPONENTS: dict[str, Any] = {}


def importComponent(component: str, classpath: str = None, package: str = "components"):
    if not classpath:
        classpath = f"flowtask.components.{component}"
    module = importlib.import_module(classpath, package=package)
    obj = getattr(module, component)
    return obj


def _download_helper(coroutine):
    def _run_coro(coro):
        event_loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(event_loop)
            return event_loop.run_until_complete(coro)
        finally:
            event_loop.close()

    with ThreadPoolExecutor(max_workers=1) as pool:
        result = pool.submit(_run_coro, coroutine).result()
    return result


def downloadComponent(component: str):
    # Create a coroutine object
    coro = download_component(component)
    # Run the coroutine in a new event loop in a separate thread
    result = _download_helper(coro)
    return result


def loadComponent(component, program: str = None):
    try:
        # Getting Basic Components
        classpath = f"flowtask.components.{component}"
        return importComponent(component, classpath, package="components")
    except ImportError as ex:
        logging.warning(
            f"Error Importing Component {component}: {ex}"
        )
        cpath = Path(__file__).parent.joinpath(f"{component}.py")
        if cpath.exists():
            logger.error(ex)
            raise ComponentError(
                f"Error Importing Component {component}: {ex}"
            ) from ex
    try:
        # another, check if task is an User-Defined Component
        classpath = f"flowtask.plugins.components.{component}"
        obj = importComponent(component, classpath, package="components")
        if issubclass(obj, (UserComponent, FlowComponent)):
            return obj
        raise ImportError(
            f"Cannot import {component} Hint: Component need inherits from UserComponent"
        )
    except ImportError as e:
        ### TODO: Download Component From Marketplace, installed on "plugins" folder.
        if downloadComponent(component) is True:
            ## re-import from plugins path
            return importComponent(component, classpath, package="components")
        raise NotSupported(
            f"Error: No Component {component!r} was Found: {e}"
        ) from e


def getComponent(component: str, program: str = None):
    try:
        if component in _COMPONENTS:
            return _COMPONENTS[component]
        else:
            cls = loadComponent(component, program=program)
            _COMPONENTS[component] = cls
            return cls
    except KeyError as err:
        logger.exception(
            f"Error loading component {component}: {err}",
            stack_info=True
        )
        raise ComponentError(
            f"Error loading component {component}: {err}"
        ) from err
