import os

import dlt as dlt

from dlthub.project import Catalog, EntityFactory, ProjectRunContext, Project, PipelineManager


def access_profile() -> str:
    """Implement this function to select profile assigned to users that import this Python package
    into their own scripts or other modules.
    """
    return "access"


def context() -> ProjectRunContext:
    """Returns the context of this package, including run directory,
    data directory and project config
    """
    from dlthub.project.project_context import ensure_project

    return ensure_project(run_dir=os.path.dirname(__file__), profile=access_profile())


def config() -> Project:
    """Returns project configuration and getters of entities like sources, destinations
    and pipelines"""
    return context().project


def entities() -> EntityFactory:
    """Returns methods to create entities in this package likes sources, pipelines etc."""
    return EntityFactory(config())


def runner() -> PipelineManager:
    return PipelineManager(config())


def catalog() -> Catalog:
    """Returns a catalogue with available datasets, which can be read and written to"""
    return Catalog(context())
