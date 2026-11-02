"""Prevent ambiguous local and stage copies from overwriting each other or managed runtime files."""

from pathlib import PurePosixPath
from typing import ClassVar

from labqoat.compute.images.copy_step import CopyStep
from labqoat.compute.images.operation import Operation
from labqoat.compute.images.stage_step import StageStep


class CopyDestinations:
    """Validate explicit destination ownership independently for each authored stage."""

    managed: ClassVar[tuple[str, ...]] = (
        "/opt/app",
        "/opt/runtime",
        "/opt/labqoat-sdk",
        "/opt/labqoat-runtime",
        "/opt/labqoat-projects",
        "/opt/labqoat-workspaces",
        "/opt/labqoat-requirements",
    )

    @classmethod
    def validate(cls, operations: tuple[Operation, ...]) -> None:
        """Reject overlapping explicit copies with the conflicting destinations identified."""
        paths = list(cls.managed)
        for operation in operations:
            if isinstance(operation, (CopyStep, StageStep)):
                destination = operation.destination
                cls._check(paths, destination)
                paths.append(destination)

    @classmethod
    def _check(cls, paths: list[str], destination: str) -> None:
        """Name both conflicting paths before any image bytes are published."""
        for previous in paths:
            if cls._overlap(previous, destination):
                raise ValueError(f"Conflicting image destinations: {previous} and {destination}")

    @staticmethod
    def _overlap(left: str, right: str) -> bool:
        """Containment makes directory copies ambiguous even when exact spellings differ."""
        first, second = PurePosixPath(left), PurePosixPath(right)
        return first == second or first in second.parents or second in first.parents
