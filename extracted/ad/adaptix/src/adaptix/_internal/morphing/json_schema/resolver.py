from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Container, Mapping, Sequence
from typing import TypeVar

from ...datastructures import OrderedUniqueGrouper
from ...provider.loc_stack_filtering import LocStack
from ...provider.loc_stack_tools import format_loc_stack
from .definitions import JSONSchema, LocalRefSource, ResolvedJSONSchema
from .schema_tools import approx_hash_json_schema, replace_json_schema_ref, traverse_json_schema


class JSONSchemaResolver(ABC):
    @abstractmethod
    def resolve(
        self,
        root_schemas: Sequence[JSONSchema],
        *,
        local_ref_prefix: str,
        occupied_refs: Container[str],
    ) -> tuple[Mapping[str, ResolvedJSONSchema], Sequence[ResolvedJSONSchema]]:
        ...


class LocalRefSourceGroup:
    def __init__(self, sources: Sequence[LocalRefSource[JSONSchema]]):
        self.sources = sources


class RefGenerator(ABC):
    @abstractmethod
    def generate_ref(self, json_schema: JSONSchema, loc_stack: LocStack) -> str:
        ...


class RefMangler(ABC):
    @abstractmethod
    def mangle_refs(
        self,
        occupied_refs: Container[str],
        common_ref: str,
        sources_groups: Sequence[LocalRefSourceGroup],
    ) -> Mapping[LocalRefSourceGroup, str]:
        ...


T = TypeVar("T")


class _ContainerWithExtra(Container[T]):
    __slots__ = ("_extra", "_original")

    def __init__(self, original: Container[T], extra: T):
        self._original = original
        self._extra = extra

    def __contains__(self, item):
        return item == self._extra or item in self._original


class CustomJSONSchemaHasher:
    __slots__ = ("_extra", "_json_schema")

    def __init__(self, json_schema: JSONSchema):
        self._json_schema = json_schema

    def __hash__(self):
        return approx_hash_json_schema(self._json_schema)

    def __eq__(self, other):
        return self._json_schema == other._json_schema


class BuiltinJSONSchemaResolver(JSONSchemaResolver):
    def __init__(self, ref_generator: RefGenerator, ref_mangler: RefMangler):
        self._ref_generator = ref_generator
        self._ref_mangler = ref_mangler

    def resolve(
        self,
        root_schemas: Sequence[JSONSchema],
        *,
        local_ref_prefix: str,
        occupied_refs: Container[str],
    ) -> tuple[Mapping[str, ResolvedJSONSchema], Sequence[ResolvedJSONSchema]]:
        ref_to_sources = self._collect_ref_to_sources(root_schemas)
        source_determinator = self._get_source_determinator(occupied_refs, ref_to_sources)
        defs = {
            ref: replace_json_schema_ref(source.json_schema, local_ref_prefix, source_determinator)
            for source, ref in source_determinator.items()
        }
        schemas = [
            replace_json_schema_ref(root, local_ref_prefix, source_determinator)
            for root in root_schemas
        ]
        return defs, schemas

    def _collect_ref_to_sources(self, root_schemas: Sequence[JSONSchema]) -> Mapping[str, Sequence[LocalRefSource]]:
        grouper = OrderedUniqueGrouper[str, LocalRefSource[JSONSchema]]()
        for root in root_schemas:
            for schema in traverse_json_schema(root):
                ref_source = schema.ref
                if isinstance(ref_source, LocalRefSource):
                    ref = (
                        self._ref_generator.generate_ref(ref_source.json_schema, ref_source.loc_stack)
                        if ref_source.value is None else
                        ref_source.value
                    )
                    grouper.add(ref, ref_source)
        return grouper.finalize()

    def _get_source_determinator(
        self,
        occupied_refs: Container[str],
        ref_to_sources: Mapping[str, Sequence[LocalRefSource]],
    ) -> Mapping[LocalRefSource, str]:
        source_group_to_ref: dict[LocalRefSourceGroup, str] = {}

        for common_ref, sources in ref_to_sources.items():
            sources_groups = self._group_sources(sources)
            source_group_to_ref.update(
                self._apply_mangling(occupied_refs, common_ref, sources_groups),
            )

        self._validate_mangling(source_group_to_ref)
        return {
            source: ref
            for source_group, ref in source_group_to_ref.items()
            for source in source_group.sources
        }

    def _group_sources(self, sources: Sequence[LocalRefSource]) -> Sequence[LocalRefSourceGroup]:
        grouper = OrderedUniqueGrouper[CustomJSONSchemaHasher, LocalRefSource]()
        for source in sources:
            grouper.add(CustomJSONSchemaHasher(source.json_schema), source)

        return [
            LocalRefSourceGroup(sources)
            for _json_schema, sources in grouper.finalize().items()
        ]

    def _apply_mangling(
        self,
        occupied_refs: Container[str],
        common_ref: str,
        sources_groups: Sequence[LocalRefSourceGroup],
    ) -> Mapping[LocalRefSourceGroup, str]:
        if len(sources_groups) == 1 and common_ref not in occupied_refs:
            return {sources_groups[0]: common_ref}

        manglable, pinned = self._validate_pining_conflict(common_ref, sources_groups)
        if pinned is None:
            return self._ref_mangler.mangle_refs(occupied_refs, common_ref, manglable)

        mangling_result = self._ref_mangler.mangle_refs(
            _ContainerWithExtra(occupied_refs, common_ref), common_ref, manglable,
        )
        return {**mangling_result, pinned: common_ref}

    def _validate_pining_conflict(
        self,
        common_ref: str,
        sources_groups: Sequence[LocalRefSourceGroup],
    ) -> tuple[Sequence[LocalRefSourceGroup], LocalRefSourceGroup | None]:
        pinned_groups = [
            source_group
            for source_group in sources_groups
            if any(source for source in source_group.sources if source.value is not None)
        ]
        if len(pinned_groups) > 1:
            text = ", ".join(
                ", ".join(f"`{format_loc_stack(source.loc_stack)}`" for source in pinned.sources)
                for pinned in pinned_groups
            )
            raise ValueError(
                f"Cannot create consistent json schema,"
                f" there are different sub schemas with pinned ref {common_ref!r}."
                f" {text}",
            )
        if len(pinned_groups) == 0:
            return sources_groups, None

        pinned = pinned_groups[0]
        return list(filter(lambda x: x != pinned, sources_groups)), pinned

    def _validate_mangling(self, source_determinator: Mapping[LocalRefSourceGroup, str]) -> None:
        ref_to_sources_groups = defaultdict(list)
        for source_group, ref in source_determinator.items():
            ref_to_sources_groups[ref].append(source_group)

        unmangled = [
            (ref, sources_groups)
            for ref, sources_groups in ref_to_sources_groups.items()
            if len(sources_groups) > 1
        ]
        if unmangled:
            unmangled_desc = "; ".join(
                f"For ref {ref!r} at "
                + ", and at ".join(
                    f"`{format_loc_stack(source.loc_stack)}`"
                    for source_group in sources_groups
                    for source in source_group.sources
                )
                for ref, sources_groups in unmangled
            )
            raise ValueError(
                f"Cannot create consistent json schema,"
                f" cannot mangle some refs."
                f" {unmangled_desc}",
            )
