# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["AdmeEstimateCostParams", "Input", "InputMolecule"]


class AdmeEstimateCostParams(TypedDict, total=False):
    input: Required[Input]

    model: Required[Literal["adme-v1"]]
    """Model to use for prediction"""

    idempotency_key: str
    """Client-provided key to prevent duplicate submissions on retries"""

    workspace_id: str
    """Target workspace ID (admin keys only; ignored for workspace keys)"""


class InputMolecule(TypedDict, total=False):
    smiles: Required[str]
    """SMILES string of the molecule to predict ADME properties for."""

    id: str
    """Optional client-provided identifier.

    Returned as `external_id` in the matching output item.
    """


class Input(TypedDict, total=False):
    molecules: Required[Iterable[InputMolecule]]
    """Molecules to score (1-128 per request).

    Results are returned in the same order as this list.
    """
