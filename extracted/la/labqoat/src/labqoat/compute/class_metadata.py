"""Typed metadata attached to an App-owned class declaration."""

from typing import Protocol

from labqoat.compute.class_options import ClassOptions


class ClassMetadata(Protocol):
    """Describe the execution options installed by the class decorator."""

    __labqoat_class__: ClassOptions
