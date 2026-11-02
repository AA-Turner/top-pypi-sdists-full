# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable, Optional
from typing_extensions import Required, TypedDict

from ..case_value_param import CaseValueParam

__all__ = ["RowAddParams", "Row"]


class RowAddParams(TypedDict, total=False):
    namespace: str
    """Namespace that assigned the scope reference."""

    scope_id: str
    """Project reference assigned by the namespace.

    For wandb, use the internal W&B project ID, not the project name or
    entity/project path.

    Percent-encode reserved characters so the reference occupies one URL path
    segment. Only printable ASCII is accepted. References are compared exactly,
    without parsing.
    """

    rows: Required[Iterable[Row]]


class Row(TypedDict, total=False):
    scores: Required[Dict[str, object]]
    """Score values keyed by scorer name.

    Use an empty object for a row with no scores. Keys must not have leading or
    trailing whitespace.
    """

    attributes: Dict[str, object]

    example_key: Optional[str]
    """
    Reference to the row's example in external data, such as a row index, for a row
    without input.

    - The service stores the reference but does not fetch the example.
    - Example keys need not be unique. Row comparison matches rows by example key.
    - A row with an input must omit it. The service derives that row's example key
      from a hash of its input, so row comparison matches rows by input. Each
      top-level extension field hashes by its identity, which leaves out file
      locations. Numbers hash as float64, so integers that differ only beyond 2^53
      derive the same example key, and a number never matches a string. Log numeric
      identifiers as strings.
    - A row with neither matches only itself, in versions of the same eval table.

    Omit or send null when no example reference applies.
    """

    input: Optional[CaseValueParam]
    """Input data for this case, such as a prompt or feature values.

    For JSON objects:

    - Top-level field names must contain 1 to 512 Unicode characters, with no
      leading or trailing whitespace.
    - All numeric fields are inferred as number, even whole-valued literals.
    - Queries use float64 numbers, which can round integers beyond 2^53. The stored
      JSON remains exact.

    Omit to store null.
    """

    output: Optional[CaseValueParam]
    """Output recorded for this case, such as a model response.

    For JSON objects:

    - Top-level field names must contain 1 to 512 Unicode characters, with no
      leading or trailing whitespace.
    - All numeric fields are inferred as number, even whole-valued literals.
    - Queries use float64 numbers, which can round integers beyond 2^53. The stored
      JSON remains exact.

    Omit to store null.
    """

    variant: Optional[str]
    """Model, agent, prompt, or checkpoint this case evaluates.

    Leading and trailing whitespace are not allowed. Omit or send null when no
    variant applies.
    """
