from collections.abc import Mapping, Sequence
from typing import Any, cast


def sort_json_patch(patch: list) -> list:
    return sorted(patch, key=lambda x: (x.get("op", ""), x.get("path", ""), str(x.get("value", ""))))


def compare_itemwise(
    ref_list: Sequence[Any],
    other_list: Sequence[Any],
    order_independent_paths: set[str] | None = None,
    exclude_paths: set[str] | None = None,
) -> list[str]:
    if order_independent_paths is None:
        order_independent_paths = set()
    if exclude_paths is None:
        exclude_paths = set()

    def to_dict(x: Any) -> Mapping[str, Any]:
        if isinstance(x, Mapping):
            return cast(Mapping[str, Any], x)
        if hasattr(x, "model_dump"):
            return cast(Mapping[str, Any], x.model_dump())
        raise TypeError(f"Unsupported type: {type(x)}")

    def compare(ref: Any, other: Any, path: str = "") -> str | None:
        if path in exclude_paths:
            return None

        if isinstance(ref, Mapping) or hasattr(ref, "model_dump"):
            if not (isinstance(other, Mapping) or hasattr(other, "model_dump")):
                return f"type mismatch at {path or '<root>'}: expected mapping or model"
            ref_map = to_dict(ref)
            other_map = to_dict(other)
            for k, rv in ref_map.items():
                new_path = f"{path}.{k}" if path else str(k)
                if new_path in exclude_paths:
                    continue
                if k not in other_map:
                    return f"missing key {k!r} at {path or '<root>'}"
                res = compare(rv, other_map[k], new_path)
                if res:
                    return res
            return None

        if isinstance(ref, Sequence) and not isinstance(ref, (str, bytes, bytearray)):
            if not (isinstance(other, Sequence) and not isinstance(other, (str, bytes, bytearray))):
                return f"type mismatch at {path or '<root>'}: expected sequence"
            if len(ref) != len(other):
                return f"length mismatch at {path or '<root>'}: {len(ref)} != {len(other)}"

            if path in order_independent_paths:
                ref_sorted = sort_json_patch(list(ref))
                other_sorted = sort_json_patch(list(other))
                for i, (rv, ov) in enumerate(zip(ref_sorted, other_sorted)):
                    new_path = f"{path}[{i}]" if path else f"[{i}]"
                    res = compare(rv, ov, new_path)
                    if res:
                        return res
            else:
                for i, (rv, ov) in enumerate(zip(ref, other)):
                    new_path = f"{path}[{i}]" if path else f"[{i}]"
                    res = compare(rv, ov, new_path)
                    if res:
                        return res
            return None

        if ref != other:
            return f"value mismatch at {path or '<root>'}: {ref!r} != {other!r}"
        return None

    if len(ref_list) != len(other_list):
        return [f"list length mismatch: {len(ref_list)} != {len(other_list)} ({ref_list!r} vs {other_list!r})"]

    errors: list[str] = []
    for i, (r, o) in enumerate(zip(ref_list, other_list)):
        err = compare(r, o)
        if err:
            errors.append(f"index {i}: {err}")

    return errors
