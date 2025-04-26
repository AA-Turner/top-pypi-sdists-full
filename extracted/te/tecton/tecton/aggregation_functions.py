from types import MappingProxyType
from typing import Any
from typing import Mapping

from tecton._internals.tecton_pydantic import StrictModel


class AggregationFunction(StrictModel):
    base_name: str
    resolved_name: str
    # Use Any for the Mapping value instead of Union[int, float] to avoid automatic Pydantic V1 coercion from int to
    # float. Pydantic V1 will attempt to coerce values in the union in order.
    params: Mapping[str, Any]


# Last N aggregation that doesn't allow duplicates.
def last_distinct(n: int) -> AggregationFunction:
    if not isinstance(n, int):
        msg = "The parameter `n` of the last_distinct aggregation must be an integer."
        raise ValueError(msg)
    return AggregationFunction(base_name="lastn", resolved_name=f"last_distinct_{n}", params=MappingProxyType({"n": n}))


# Last N aggregation that allows duplicates.
def last(n: int) -> AggregationFunction:
    if not isinstance(n, int):
        msg = "The parameter `n` of the last aggregation must be an integer."
        raise ValueError(msg)
    return AggregationFunction(
        base_name="last_non_distinct_n", resolved_name=f"last_{n}", params=MappingProxyType({"n": n})
    )


# First N aggregation that doesn't allow duplicates.
def first_distinct(n: int) -> AggregationFunction:
    if not isinstance(n, int):
        msg = "The parameter `n` of the first_distinct aggregation must be an integer."
        raise ValueError(msg)
    return AggregationFunction(
        base_name="first_distinct_n", resolved_name=f"first_distinct_{n}", params=MappingProxyType({"n": n})
    )


# First N aggregation that allows duplicates.
def first(n: int) -> AggregationFunction:
    if not isinstance(n, int):
        msg = "The parameter `n` of the first aggregation must be an integer."
        raise ValueError(msg)
    return AggregationFunction(
        base_name="first_non_distinct_n", resolved_name=f"first_{n}", params=MappingProxyType({"n": n})
    )


def approx_count_distinct(precision: int = 8) -> AggregationFunction:
    if not isinstance(precision, int):
        msg = "The parameter `precision` of the approx_count_distinct aggregation must be an integer."
        raise ValueError(msg)
    return AggregationFunction(
        base_name="approx_count_distinct",
        resolved_name="approx_count_distinct",
        params=MappingProxyType({"precision": precision}),
    )


def approx_percentile(percentile: float, precision: int = 100) -> AggregationFunction:
    if not isinstance(percentile, float):
        msg = "The parameter `percentile` of the approx_percentile aggregation must be a float."
        raise ValueError(msg)
    if not isinstance(precision, int):
        msg = "The parameter `precision` of the approx_percentile aggregation must be an integer."
        raise ValueError(msg)
    return AggregationFunction(
        base_name="approx_percentile",
        resolved_name=f"approx_percentile_p{str(percentile).replace('.', '_')}",
        params=MappingProxyType({"percentile": percentile, "precision": precision}),
    )
