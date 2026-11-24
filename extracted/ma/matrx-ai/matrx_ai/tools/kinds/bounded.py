"""The ONE declaration of the keys ``self_bounded_result`` adds to a cut result.

A closed result kind (``extra="forbid"``) of any tool wrapped in
:func:`matrx_ai.tools.output_caps.self_bounded_result` inherits :class:`SelfBoundedFields`, so the
wrapper's ``truncated`` / ``more_available`` / ``size_note`` are declared optional keys of the
contract instead of ``tool_output_contract_drift`` (class sec_b1ae4f60). Add the base to the
kind's class bases; never redeclare the three fields by hand.
"""

from __future__ import annotations

from pydantic import BaseModel


class SelfBoundedFields(BaseModel):
    #: a cut was made to fit the size gate; the result says so.
    truncated: bool | None = None
    #: the rest exists and was not shown.
    more_available: bool | None = None
    #: plain-language account of what was cut and how to ask for less.
    size_note: str | None = None
