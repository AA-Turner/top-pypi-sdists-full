# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

from ..case_value_param import CaseValueParam

__all__ = ["CaseAddParams", "Case"]


class CaseAddParams(TypedDict, total=False):
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

    cases: Required[Iterable[Case]]

    example_key_fields: List[Literal["input"]]
    """
    Derives an example key for each case from a hash of its input, so row comparison
    can match cases by input. Each top-level extension field hashes by its identity,
    which leaves out file locations. Numbers hash as float64, so integers that
    differ only beyond 2^53 derive the same example key, and a number never matches
    a string. Log numeric identifiers as strings. A case with a null input gets no
    example key. Without it, a case logged without an example key matches only
    itself, in versions that read its dataset.
    """


class Case(TypedDict, total=False):
    attributes: Dict[str, object]

    example_key: Optional[str]
    """
    Reference to the case's example in external data, such as an S3 object key or
    row index.

    - The service stores the reference but does not fetch the example.
    - Example keys need not be unique. Row comparison matches cases by example key.
    - A case with no input can use this reference to identify its example.

    Omit or send null when no example reference applies. Omit on every case when the
    request sets example_key_fields.
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

    trajectory_id: Optional[str]
    """Trajectory to add this case to.

    It must belong to the same dataset. Omit or send null for a case outside any
    trajectory.
    """

    variant: Optional[str]
    """Model, agent, prompt, or checkpoint this case evaluates.

    Leading and trailing whitespace are not allowed. Omit or send null when no
    variant applies.
    """
