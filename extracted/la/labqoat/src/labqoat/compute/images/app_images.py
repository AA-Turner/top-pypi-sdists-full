"""App-owned declaration registration for automatic child and model image capture."""

import sys

from labqoat.compute.images.declared_image import DeclaredImage


class AppImages:
    """Retain the App's explicitly decorated callables without process-global discovery."""

    def __init__(self) -> None:
        """Create an empty registry owned by exactly one App."""
        self._declarations: dict[str, DeclaredImage] = {}

    def register(self, declaration: DeclaredImage) -> None:
        """Register each importable callable once and reject ambiguous redeclarations."""
        previous = self._declarations.get(declaration.key)
        if previous is not None and previous != declaration:
            raise ValueError(f"Conflicting App declaration: {declaration.key}")
        self._declarations[declaration.key] = declaration

    def declarations(self) -> tuple[DeclaredImage, ...]:
        """Snapshot stable registration order without exposing mutable registry state."""
        return tuple(self._declarations[key] for key in sorted(self._declarations))

    def closure(self) -> tuple[DeclaredImage, ...]:
        """This App's callables and those of every other App its modules import, so a run can call any of them.

        Only names bound at the top level of the declaring modules are followed, transitively; an App imported
        inside a function body is not seen.
        """
        found: dict[int, AppImages] = {id(self): self}
        pending = [self]
        while pending:
            for registry in pending.pop().imported():
                if id(registry) not in found:
                    found[id(registry)] = registry
                    pending.append(registry)
        merged = {item.key: item for registry in found.values() for item in registry.declarations()}
        return tuple(merged[key] for key in sorted(merged))

    def imported(self) -> list["AppImages"]:
        """Registries of the Apps and functions bound at the top level of this App's declaring modules."""
        from labqoat.compute.app import App
        from labqoat.compute.function import Function

        modules = [sys.modules[name] for name in {item.module for item in self.declarations()} if name in sys.modules]
        values = [value for module in modules for value in vars(module).values()]
        return [value.registry for value in values if isinstance(value, (App, Function))]
