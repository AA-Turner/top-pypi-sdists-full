#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see https://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Utilities for deterministic ordering of service components.

This module provides a mixin that reorders service components while
respecting ``affects`` and ``depends_on`` relationships declared on the
component classes. It supports wildcard semantics (``"*"``) and preserves
the input order whenever it does not conflict with the declared constraints.
"""

from __future__ import annotations

import heapq
import inspect
from collections import defaultdict
from functools import cached_property, partial
from itertools import chain
from typing import TYPE_CHECKING, Any, Literal, override

from invenio_base.utils import obj_or_import_string
from invenio_records_resources.services.records.components import ServiceComponent

if TYPE_CHECKING:
    from collections.abc import Callable, Generator, Iterable

    from invenio_records_resources.services.records.config import RecordServiceConfig
    from invenio_records_resources.services.records.service import RecordService

else:
    # for mixin typing
    RecordServiceConfig = object
    RecordService = object


class ComponentData:
    """Normalized metadata extracted from a service component.

    Instances of this helper encapsulate the resolved component class, its
    relevant MRO, and the parsed ``affects``/``depends_on`` declarations for
    use by the ordering algorithm.
    """

    original_component: Any
    """The original component entry as provided in ``config.components``."""

    component_class: type[ServiceComponent]
    """The resolved class used for ordering comparisons.

    If the original component is a class, this is that class (validated to be a
    ``ServiceComponent`` subclass). If the original component is a
    ``functools.partial``, this is ``partial.func``. If it is a factory/callable,
    the callable is invoked and the result's type is used.
    """

    component_mro: set[type[ServiceComponent]]
    """Set containing ``component_class`` and its mixins/base classes.

    Classes from the ``ServiceComponent`` hierarchy (including ``object``) are
    excluded. This set is used for efficient membership checks when matching
    dependencies/affects to other components.
    """

    replaces: set[type[ServiceComponent]]
    """Classes that this component replaces."""

    replaced_by: set[type[ServiceComponent]]
    """Classes that replace this component."""

    affects_all: bool
    """Whether the component declares ``affects = "*"`` (i.e., affects all)."""

    depends_on_all: bool
    """Whether the component declares ``depends_on = "*"`` (i.e., depends on all)."""

    affects: set[type[ServiceComponent]]
    """Classes that this component affects."""

    depends_on: set[type[ServiceComponent]]
    """Classes that this component depends on."""

    idx: int
    """Position of the item within the current working list during sort.

    This is assigned later by the sorting algorithm and refers to the index in
    the local subset being processed (not necessarily the original input list).
    """

    indeg: int = 0
    """Number of incoming edges in the dependency graph (direct prerequisites)."""

    def __init__(
        self,
        original_component: Any,
        service: RecordService,
    ) -> None:
        """Resolve and validate metadata from the provided component entry.

        Also validates that a component cannot both affect all and depend on all
        at the same time (mutually exclusive wildcards).
        """
        self.original_component = original_component
        self.component_class = self._extract_class_from_component(original_component, service)

        self.component_mro = self._get_service_mro(self.component_class)

        self.affects_all = "*" in getattr(self.component_class, "affects", [])
        self.depends_on_all = "*" in getattr(self.component_class, "depends_on", [])

        if self.affects_all and self.depends_on_all:
            raise ValueError(
                f"Component {self.original_component} cannot affect and depend on all components at the same time."
            )

        self.affects = self._convert_to_classes(getattr(self.component_class, "affects", None) or [])
        self.depends_on = self._convert_to_classes(getattr(self.component_class, "depends_on", None) or [])
        self.replaces = self._convert_to_classes(getattr(self.component_class, "replaces", None) or [])
        self.replaced_by = self._convert_to_classes(getattr(self.component_class, "replaced_by", None) or [])

    def _extract_class_from_component(self, component: Any, service: RecordService) -> type[ServiceComponent]:
        """Resolve a comparable class from the component entry.

        Supported forms:
        - a class that subclasses ``ServiceComponent``;
        - a ``functools.partial`` whose ``func`` ultimately resolves to the class;
        - a factory/callable returning a ``ServiceComponent`` instance when
            called (the returned instance's type is used).
        """
        # if it is a class, return it
        if inspect.isclass(component):
            if not issubclass(component, ServiceComponent):
                raise TypeError(f"Component {component} is not a subclass of ServiceComponent")
            return component

        # it might be a partial, so check that out
        if isinstance(component, partial):
            return self._extract_class_from_component(component.func, service)

        # as a last option, instantiate the component and return its type
        inst = component(service)
        return type(inst)

    def _get_service_mro(self, component_class: type[ServiceComponent]) -> set[type]:
        """Get the relevant MRO for ordering comparisons.

        Returns the component class and its base classes/mixins, excluding the
        ``ServiceComponent`` hierarchy (and thus also ``object``).
        """
        return {x for x in component_class.mro() if x not in ServiceComponent.mro()}

    def _convert_to_classes(self, items: Any) -> set[type[ServiceComponent]]:
        """Normalize an input list/tuple to a set of component classes.

        Accepts classes or import strings. The special value ``"*"`` is handled
        by the caller via ``affects_all``/``depends_on_all`` and is not included
        in the returned set.
        """
        ret: set[type[ServiceComponent]] = set()

        if not isinstance(items, (list, tuple)):
            if items == "*":
                return ret
            raise TypeError(f"Expected list or tuple, got {type(items)}")
        for item in items:
            if isinstance(item, str):
                item = obj_or_import_string(item)  # noqa PLW2901

            if inspect.isclass(item):
                if not issubclass(item, ServiceComponent):
                    raise TypeError(f"Item {item} is not a ServiceComponent subclass")
                ret.add(item)
            else:
                raise TypeError(
                    f"affects or depends_on needs to contain classes, item {item} ({type(item)}) is not a class"
                )
        return ret

    @override
    def __hash__(self):
        return hash(self.component_class)

    @override
    def __eq__(self, other: object) -> bool:
        return self.component_class == other.component_class if isinstance(other, ComponentData) else False

    @override
    def __repr__(self):
        return f"CD({self.component_class.__name__})"

    @override
    def __str__(self):
        ret = [f"CD({self.component_class.__name__}"]
        if self.affects_all:
            ret.append(",a*")
        if self.depends_on_all:
            ret.append(",d*")
        if self.affects:
            ret.append(f",a={{{', '.join(sorted(c.__name__ for c in self.affects))}}}")
        if self.depends_on:
            ret.append(f",d={{{', '.join(sorted(c.__name__ for c in self.depends_on))}}}")
        ret.append(")")
        return "".join(ret)


class ComponentsOrderingMixin(RecordService):
    """Order ``config.components`` while honoring declared relationships.

        Component classes can declare two optional class attributes:
        - ``depends_on``: a class or a list of classes that must appear before it;
        - ``affects``: a class or a list of classes that must appear after it.

    Both attributes may also be the wildcard ``"*"`` to express a relationship
    with all other components. For example:
    - if ``A.affects = "*"`` and ``B.affects = A``, then the order must be
        ``B, A, *`` (i.e., ``B`` comes before ``A``);
    - if ``A.depends_on = "*"`` and ``B.depends_on = A``, then the order must be
        ``*, B, A`` (i.e., everything before ``B`` before ``A``).

    The algorithm performs:
        1) class deduplication (keep only one occurrence of each class),
        2) inheritance deduplication (prefer the most specific subclass over its base),
        3) stable topological sorting that preserves input order whenever possible.
    """

    @cached_property
    def component_classes(self) -> tuple[type[ServiceComponent], ...]:
        """Return the ordered component classes as an immutable tuple."""
        return self._order_components(self.config.components)

    @property
    def components(self) -> Generator[ServiceComponent]:
        """Instantiate and yield components in the computed order."""
        return (c(self) for c in self.component_classes)

    def _order_components(
        self,
        components: Iterable[Any],
    ) -> tuple[Any, ...]:
        """Order components based on ``affects``/``depends_on`` semantics.

        Splits components into three groups (``affects_all``, ``rest``,
        ``depends_on_all``), propagates transitive relationships into the edge
        groups, topologically sorts each group, and finally concatenates them
        in that order. Returns a tuple of the original component entries.
        """
        component_data = self._deduplicate_components(components)

        affects_all = [x for x in component_data if x.affects_all]
        depends_on_all = [x for x in component_data if x.depends_on_all]
        rest = [x for x in component_data if not x.affects_all and not x.depends_on_all]

        # if A is from affects_all
        #     * and A[depends_on=B], add B to the affects_all set
        #     * and B[affects=A], add B to the affects_all set
        self._propagate_dependencies(affects_all, rest, lambda x: x.depends_on, lambda x: x.affects)
        # if A is from depends_on_all
        #     * and A[affects=B], add B to the depends_on_all set
        #     * and B[depends_on=A], add B to the depends_on_all set
        self._propagate_dependencies(depends_on_all, rest, lambda x: x.affects, lambda x: x.depends_on)

        # now the affects_all, rest, depends_on_all are completed and can be sorted
        affects_all = self._topo_sort(affects_all)
        rest = self._topo_sort(rest)
        depends_on_all = self._topo_sort(depends_on_all)

        return tuple(x.original_component for x in chain(affects_all, rest, depends_on_all))

    def _topo_sort(self, components: list[ComponentData]) -> list[ComponentData]:
        """Topologically sort by dependencies while preserving relative order.

        Uses indegree counting with a min-heap keyed by the original index to
        prefer earlier items when multiple nodes become available. Detects and
        raises a ``ValueError`` with the cyclic subgraph if a cycle exists.
        """
        if not components or len(components) == 1:
            return components

        for idx, comp in enumerate(components):
            comp.idx = idx  # set the index for later use

        graph = self._create_topo_graph(components)

        # graph gives a mapping of each component to its dependencies, we need to build
        # an inverse as well
        inverse_graph = defaultdict(set)
        for comp, deps in graph.items():
            comp.indeg = len(deps)  # set the indegree
            for dep in deps:
                inverse_graph[dep].add(comp)

        # create a queue of all nodes that have no dependencies on other nodes
        heap = [component.idx for component in components if component.indeg == 0]
        heapq.heapify(heap)

        ordered: list[ComponentData] = []
        while heap:
            # take the top of the heap and take the associated component and add it to
            # the output sequence
            idx = heapq.heappop(heap)
            component = components[idx]
            ordered.append(component)

            # for each of the items that depend directly on this one, decrease the indeg
            # of the item. If it reaches zero, add it to the heap. This will reorder
            # the heap in a way that the next heappop will return the item with the
            # lowest index (thus handling B->C, C, D will be returned in C, B, D rather
            # than C, D, B if only indeg would be used).
            for v in inverse_graph[component]:
                v.indeg -= 1
                if v.indeg == 0:
                    heapq.heappush(heap, v.idx)

        if len(ordered) != len(components):
            # get a list of components that form a cycle
            cycle_forming_components = {cd for cd in components if cd.indeg > 0}
            cycled_dependencies = {
                comp: {dep for dep in deps if dep in cycle_forming_components}
                for comp, deps in graph.items()
                if comp in cycle_forming_components
            }
            raise ValueError(f"Cycle detected in dependencies: {cycled_dependencies}")

        return ordered

    def _create_topo_graph(self, components: list[ComponentData]) -> dict[ComponentData, set[ComponentData]]:
        """Build a dependency graph suitable for topological sorting.

        The resulting mapping has nodes as keys and a set of their direct
        prerequisites as values. Specifically:
        - if ``A`` appears in ``B.depends_on``, then ``graph[B]`` contains ``A``;
        - if ``A`` appears in ``B.affects``, then ``graph[A]`` contains ``B``.
        """
        graph: dict[ComponentData, set[ComponentData]] = {}
        for comp in components:
            graph[comp] = set()

        for comp in components:
            for dep in comp.depends_on:
                for other in self._find_components(components, dep):
                    graph[comp].add(other)
            for aff in comp.affects:
                for other in self._find_components(components, aff):
                    graph[other].add(comp)
        return graph

    def _find_components(self, components: list[ComponentData], cls: type) -> list[ComponentData]:
        """Return components whose ``component_mro`` includes the given class."""
        return [comp for comp in components if cls in comp.component_mro]

    def _propagate_dependencies(
        self,
        selected: list[ComponentData],
        potential_dependencies: list[ComponentData],
        selected_dependency_getter: Callable[[ComponentData], set[type[ServiceComponent]]],
        potential_dependency_getter: Callable[[ComponentData], set[type[ServiceComponent]]],
    ) -> None:
        """Enrich the edge groups with items they require or that require them.

        - If any item in ``selected`` depends on an item in ``potential_dependencies``
            (via ``selected_dependency_getter``), move that dependency into
            ``selected``.
        - If any item in ``potential_dependencies`` declares it must be together
            with something in ``selected`` (via ``potential_dependency_getter``),
            move it into ``selected`` as well.

        Both ``selected`` and ``potential_dependencies`` are modified in place,
        and propagation continues until a fixed point is reached (transitive closure).
        """
        modified = True
        already_checked_selected: set[ComponentData] = set()
        while modified:
            modified = False

            moved_indices = sorted(
                self._get_dependencies_from_selected(
                    list(set(selected) - already_checked_selected),
                    potential_dependencies,
                    selected_dependency_getter,
                )
                | self._get_dependencies_from_potentials(selected, potential_dependencies, potential_dependency_getter)
            )
            already_checked_selected.update(selected)
            if moved_indices:
                modified = True  # do another round for transitive dependencies
                selected.extend(potential_dependencies[idx] for idx in moved_indices)
                for idx in reversed(moved_indices):
                    del potential_dependencies[idx]

    def _get_dependencies_from_selected(
        self,
        selected: list[ComponentData],
        potential_dependencies: list[ComponentData],
        selected_dependency_getter: Callable[[ComponentData], set[type[ServiceComponent]]],
    ) -> set[int]:
        """Get indices of potential dependencies required by items in ``selected``.

        Handles these cases (A in ``selected``, B in ``potential_dependencies``):
        - A in ``affects_all`` and A.depends_on contains B -> move B to ``affects_all``;
        - A in ``depends_on_all`` and A.affects contains B -> move B to ``depends_on_all``.
        """
        additional_selected_items = set[int]()

        for s in selected:
            additional_selected_from_s = selected_dependency_getter(s)
            if not additional_selected_from_s:
                continue
            for idx, dep in enumerate(potential_dependencies):
                if additional_selected_from_s & dep.component_mro:
                    # the dependency matches, so should be in selected
                    additional_selected_items.add(idx)

        return additional_selected_items

    def _get_dependencies_from_potentials(
        self,
        selected: list[ComponentData],
        potential_dependencies: list[ComponentData],
        potential_dependency_getter: Callable[[ComponentData], set[type[ServiceComponent]]],
    ) -> set[int]:
        """Get indices of potentials that explicitly belong to the edge group.

        Handles these cases (A in ``selected``, B in ``potential_dependencies``):
        - A in ``affects_all`` and B.affects contains A -> move B to ``affects_all``;
        - A in ``depends_on_all`` and B.depends_on contains A -> move B to ``depends_on_all``.
        """
        additional_selected_items = set[int]()

        for idx, p in enumerate(potential_dependencies):
            p_should_be_with = potential_dependency_getter(p)
            if not p_should_be_with:
                continue
            for s in selected:
                if p_should_be_with & s.component_mro:
                    # the dependency matches, so should be in selected
                    additional_selected_items.add(idx)

        return additional_selected_items

    def _deduplicate_components(
        self,
        components: Iterable[Any],
    ) -> list[ComponentData]:
        """Build normalized component data and deduplicate by class/inheritance.

        Rules:
        - keep only one occurrence of a class (class deduplication);
        - if both a base class and its subclass appear, keep the most specific
            subclass and drop the base (inheritance deduplication);
        - otherwise preserve the original input order.
        """
        data: list[ComponentData] = []

        for candidate_component in components:
            cd = ComponentData(original_component=candidate_component, service=self)

            replaced_indices = []
            skipped = False
            for idx, component in enumerate(data):
                deduplication_action = self._deduplication_action(cd, component)
                match deduplication_action:
                    case "skip":
                        skipped = True
                    case "replace":
                        replaced_indices.append(idx)
                    case "ok":
                        pass

            if skipped:
                if replaced_indices:
                    # we have replaced indices and at the same time, the replacement
                    # should be skipped, so just remove the components at those indices
                    # probably never happens, just for sure
                    self._remove_indices_from_data(data, replaced_indices)
                continue

            if replaced_indices:
                # we have replaced indices. Remove all but the first index
                self._remove_indices_from_data(data, replaced_indices[1:])
                # and replace the first index with this component
                data[replaced_indices[0]] = cd
            else:
                # if no replaced indices, append the new component to the end of the list
                data.append(cd)

        return data

    def _deduplication_action(
        self, new_component: ComponentData, existing_component: ComponentData
    ) -> Literal["skip", "replace", "ok"]:
        """Get a deduplication action for the given components.

        :param new_component the component that is being added to the list of components
        :param existing_component the component that is already in the list of components

        :return: the deduplication action to take
                 skip: do not add the new_component to the list of components
                 replace: replace the existing_component with the new_component
                 ok: it is ok to add the new_component to the list of components as
                      it does not interfere with the existing component
        """
        if new_component.component_class == existing_component.component_class:
            # already inside the data, do not include it twice
            return "skip"
        if existing_component.component_class in new_component.replaced_by:
            # already replaced by something in the data, do not include it
            return "skip"
        if existing_component.component_class in new_component.replaces:
            # the class in data is replaced by this one
            return "replace"
        if new_component.component_class in existing_component.replaces:
            # component says that it replaces me, so skip
            return "skip"
        if new_component.component_class in existing_component.replaced_by:
            # component says it is replaced by myself
            return "replace"
        return "ok"

    def _remove_indices_from_data(self, data: list[ComponentData], indices: list[int]) -> None:
        """Remove items at the given (sorted) indices from ``data`` in place."""
        for idx in reversed(indices):
            del data[idx]
