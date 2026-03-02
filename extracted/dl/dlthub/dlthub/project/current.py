"""Access to entities and configuration of a project that is current for a calling Python module."""

import os
import inspect
from typing import Optional

from dlthub.project.catalog import Catalog
from dlthub.project.config.config import Project
from dlthub.project.entity_factory import EntityFactory
from dlthub.project.pipeline_manager import PipelineManager
from dlthub.project.project_context import ProjectRunContext, ensure_project


def context(profile: Optional[str] = None) -> ProjectRunContext:
    """Ensures and returns the context of current project, including run directory,
    data directory and project config.
    This functions inspects calling module location, finds out if it is associated with a
    dlt project and then activates its context.
    """
    calling_module_dir = _get_calling_module_dir()
    return ensure_project(run_dir=calling_module_dir, profile=profile)


def config(context_: ProjectRunContext = None) -> Project:
    """Returns project configuration and getters of entities like sources, destinations
    and pipelines"""
    return (context_ or context()).project


def entities(context_: ProjectRunContext = None) -> EntityFactory:
    """Returns methods to create entities in this package likes sources, pipelines etc."""
    return EntityFactory(config(context_))


def runner(context_: ProjectRunContext = None) -> PipelineManager:
    """Returns a PipelineManager that can run pipelines of the current project"""
    return PipelineManager(config(context_))


def catalog(context_: ProjectRunContext = None) -> Catalog:
    """Returns a catalogue with available datasets, which can be read and written to"""
    return Catalog(context_ or context())


def _get_calling_module_dir() -> Optional[str]:
    """
    Returns the directory of the calling module.
    This searches the call stack for the first module that
    has a __file__ attribute and that is not the current module.
    In an interactive session (or if __file__ is not defined),
    it returns None.
    """
    # Get the absolute path of the current file, if available.
    current_file = os.path.abspath(__file__) if "__file__" in globals() else None

    # Skip the current frame (index 0) and look at the caller frames.
    for frame_info in inspect.stack()[1:]:
        module = inspect.getmodule(frame_info.frame)
        if module is None:
            continue  # Could be an internal frame without a module.
        module_file = getattr(module, "__file__", None)
        if module_file is None:
            continue  # Likely an interactive session or built-in module.
        module_file = os.path.abspath(module_file)
        # Return the directory if this module is not the current one.
        if current_file is None or module_file != current_file:
            return os.path.dirname(module_file)  # type: ignore[no-any-return]
    return None  # Fallback if no suitable module was found.
