from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from typing import (
    TypeVar,
)

import grimp
from grimp.application.ports.graph import (
    ImportGraph as GrimpImportGraph,
)

from . import (
    _utils,
)
from ._full_path import (
    FullPathModule,
)

_T = TypeVar("_T")


def _assert_bool(raw: _T) -> bool | Exception:
    if isinstance(raw, bool):
        return raw
    return TypeError(
        f"Expected `bool` but got `{type(raw)}`; This is a lib bug and should be reported.",
    )


def _assert_str(raw: _T) -> str | Exception:
    if isinstance(raw, str):
        return raw
    return TypeError(
        f"Expected `str` but got `{type(raw)}`; This is a lib bug and should be reported.",
    )


def _assert_opt_str_tuple(
    raw: _T | None,
) -> tuple[str, ...] | None | Exception:
    if raw is None:
        return raw
    if isinstance(raw, tuple):
        return _utils.transform_items(raw, _assert_str)
    return TypeError(
        f"Expected `Optional[Tuple[str, ...]]` but got `{type(raw)}`; "
        "This is a lib bug and should be reported.",
    )


@dataclass(frozen=True)
class _ImportGraph:
    graph: GrimpImportGraph


@dataclass(frozen=True)
class ImportGraph:
    """Graph of modules that represents their import relationships."""

    _inner: _ImportGraph
    roots: frozenset[FullPathModule]

    @staticmethod
    def from_modules(
        root_modules: FullPathModule | frozenset[FullPathModule],
        external_packages: bool,
    ) -> ImportGraph:
        _root_modules = (
            root_modules if isinstance(root_modules, frozenset) else frozenset([root_modules])
        )
        raw_modules = frozenset(r.module for r in _root_modules)
        graph = grimp.build_graph(
            *raw_modules,
            include_external_packages=external_packages,
        )
        return ImportGraph(_ImportGraph(graph), _root_modules)

    @classmethod
    def build_graph(
        cls,
        raw_roots: str | frozenset[str],
        external_packages: bool,
    ) -> ImportGraph:
        roots = raw_roots if isinstance(raw_roots, frozenset) else frozenset([raw_roots])
        modules = frozenset(FullPathModule.assert_module(r) for r in roots)
        return cls.from_modules(modules, external_packages)

    def chain_exists(
        self,
        importer: FullPathModule,
        imported: FullPathModule,
        as_packages: bool,
    ) -> bool:
        result = _assert_bool(
            self._inner.graph.chain_exists(
                importer.module,
                imported.module,
                as_packages,
            ),
        )
        return _utils.raise_or_value(result)

    def find_shortest_chain(
        self,
        importer: FullPathModule,
        imported: FullPathModule,
    ) -> tuple[FullPathModule, ...] | None:
        _raw = _assert_opt_str_tuple(
            self._inner.graph.find_shortest_chain(
                importer.module,
                imported.module,
            ),
        )
        raw = _utils.raise_or_value(_raw)
        if raw is None:
            return None
        return tuple(FullPathModule.assert_module(r) for r in raw)

    def find_children(self, module: FullPathModule) -> frozenset[FullPathModule]:
        items: frozenset[str] = frozenset(
            self._inner.graph.find_children(module.module),
        )
        return frozenset(FullPathModule.assert_module(i) for i in items)

    def find_modules_that_directly_import(
        self,
        module: FullPathModule,
    ) -> frozenset[FullPathModule]:
        items: frozenset[str] = frozenset(
            self._inner.graph.find_modules_that_directly_import(module.module),
        )
        return frozenset(FullPathModule.assert_module(i) for i in items)

    def find_modules_directly_imported_by(
        self,
        module: FullPathModule,
    ) -> frozenset[FullPathModule]:
        items: frozenset[str] = frozenset(
            self._inner.graph.find_modules_directly_imported_by(module.module),
        )
        return frozenset(FullPathModule.assert_module(i) for i in items)

    def find_modules_that_import(
        self,
        module: FullPathModule,
        as_package: bool,
    ) -> frozenset[FullPathModule]:
        """
        Find modules importing the supplied module.

        as_package: set true to include only external modules relative to the supplied one.
        """
        items: frozenset[str] = frozenset(
            self._inner.graph.find_downstream_modules(
                module.module,
                as_package,
            ),
        )
        return frozenset(FullPathModule.assert_module(i) for i in items)


__all__ = [
    "FullPathModule",
]
