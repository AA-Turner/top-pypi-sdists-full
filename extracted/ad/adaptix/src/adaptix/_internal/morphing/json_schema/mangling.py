from collections import defaultdict
from collections.abc import Container, Mapping, Sequence
from itertools import count

from .resolver import LocalRefSourceGroup, RefMangler


class IndexRefMangler(RefMangler):
    def __init__(self, start: int = 1, separator: str = "-"):
        self._start = start
        self._separator = separator

    def mangle_refs(
        self,
        occupied_refs: Container[str],
        common_ref: str,
        sources_groups: Sequence[LocalRefSourceGroup],
    ) -> Mapping[LocalRefSourceGroup, str]:
        result = {}
        counter = count(self._start)
        for sources_group in sources_groups:
            while True:
                idx = next(counter)
                mangled = self._with_index(common_ref, idx)
                if mangled not in occupied_refs:
                    result[sources_group] = mangled
                    break

        return result

    def _with_index(self, common_ref: str, index: int) -> str:
        return f"{common_ref}{self._separator}{index}"


class QualnameRefMangler(RefMangler):
    def mangle_refs(
        self,
        occupied_refs: Container[str],
        common_ref: str,
        sources_groups: Sequence[LocalRefSourceGroup],
    ) -> Mapping[LocalRefSourceGroup, str]:
        return {
            sources_group: self._generate_name(sources_group) or common_ref
            for sources_group in sources_groups
        }

    def _generate_name(self, sources_group: LocalRefSourceGroup) -> str | None:
        if len(sources_group.sources) > 1:
            tps = {source.loc_stack.last.type for source in sources_group.sources}
            if len(tps) > 1:
                return None

        tp = sources_group.sources[0].loc_stack.last.type
        return getattr(tp, "__qualname__", None)


class CompoundRefMangler(RefMangler):
    def __init__(self, base: RefMangler, wrapper: RefMangler):
        self._base = base
        self._wrapper = wrapper

    def mangle_refs(
        self,
        occupied_refs: Container[str],
        common_ref: str,
        sources_groups: Sequence[LocalRefSourceGroup],
    ) -> Mapping[LocalRefSourceGroup, str]:
        mangled = self._base.mangle_refs(occupied_refs, common_ref, sources_groups)

        grouper = defaultdict(list)
        for source_group, ref in mangled.items():
            grouper[ref].append(source_group)

        for ref, ref_sources_groups in grouper.items():
            if len(ref_sources_groups) > 1:
                mangled = {
                    **mangled,
                    **self._wrapper.mangle_refs(occupied_refs, ref, ref_sources_groups),
                }

        return mangled
