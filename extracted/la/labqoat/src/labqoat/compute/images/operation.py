"""Closed typed operation vocabulary for immutable Python-authored images."""

from typing import TypeAlias

from labqoat.compute.images.command_step import CommandStep
from labqoat.compute.images.dependency_command_step import DependencyCommandStep
from labqoat.compute.images.copy_step import CopyStep
from labqoat.compute.images.env_step import EnvStep
from labqoat.compute.images.workdir_step import WorkdirStep
from labqoat.compute.images.pip_step import PipStep
from labqoat.compute.images.sync_step import SyncStep
from labqoat.compute.images.apt_step import AptStep
from labqoat.compute.images.stage_step import StageStep

Operation: TypeAlias = (
    CommandStep | DependencyCommandStep | CopyStep | EnvStep | WorkdirStep | PipStep | SyncStep | AptStep | StageStep
)
