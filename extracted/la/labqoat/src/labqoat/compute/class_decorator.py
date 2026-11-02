"""Class declarations retain typed Python constructors and expose explicit remote methods."""

from dataclasses import dataclass, replace
from pathlib import Path
import inspect
from typing import TypeVar, cast

from labqoat.compute.class_metadata import ClassMetadata
from labqoat.compute.class_options import ClassOptions
from labqoat.compute.images.declared_image import DeclaredImage
from labqoat.compute.method_descriptor import MethodDescriptor
from labqoat.training.budgets.fit_allowance import FitAllowance

T = TypeVar("T")


@dataclass(frozen=True)
class ClassDecorator:
    """Attach execution configuration without creating an instance or running its initializer."""

    options: ClassOptions

    def with_fit_budget(self, milliseconds: int) -> "ClassDecorator":
        """Retain the same immutable scientific allowance on every declared class method."""
        allowance = FitAllowance(milliseconds)
        allowance.validate_isolation(self.options.workers)
        return replace(self, options=replace(self.options, fit_allowance=allowance))

    def __call__(self, service: type[T]) -> type[T]:
        """Keep constructor typing; host constructors bind data and worker initializers own runtime effects."""
        cast(ClassMetadata, service).__labqoat_class__ = self.options
        for method in vars(service).values():
            if isinstance(method, MethodDescriptor):
                local = method.local
                self.options.registry.register(
                    DeclaredImage(
                        local.__module__, local.__qualname__, Path(inspect.getfile(local)), self.options.image
                    )
                )
        return service
