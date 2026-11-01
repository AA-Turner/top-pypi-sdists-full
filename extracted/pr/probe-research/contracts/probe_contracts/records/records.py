"""Record: the one base class of every shared domain concept, and the named projections cut from it."""

from __future__ import annotations

import copy
from typing import Any

from pydantic import BaseModel, ConfigDict, create_model


class Record(BaseModel):
    """A shared domain concept, defined once (Run, Experiment, Project, ...).

    A record is never a wire shape itself. Each request or response is a NAMED
    PROJECTION of it (`project`): the projection picks fields by name, so a field
    added here reaches no response until a projection names it. That is how the
    frozen ingest `RunOut` keeps its exact field set while `Run` grows.
    """

    model_config = ConfigDict(frozen=True, from_attributes=True, populate_by_name=True)

    @classmethod
    def from_row(cls, row: Any) -> Record:
        """Build the record from a database row (a mapping or an object with attributes)."""
        return cls.model_validate(dict(row) if hasattr(row, "keys") else row)

    @classmethod
    def project(cls, *names: str, **overrides: Any) -> type[BaseModel]:
        """A plain model holding `names`, in that order, each copied from this record.

        `overrides` replaces a named field as `name=(annotation, default)` (a validator, a looser type).
        Subclass the result under the wire name; its name, docstring, config and validators stay its own,
        so no schema changes. Why: contracts/DESIGN.md (Records and projections).
        """
        unknown = sorted(set(names) - set(cls.model_fields))
        if unknown:
            raise ValueError(f"{cls.__name__} has no field(s) {unknown}")
        stray = sorted(set(overrides) - set(names))
        if stray:
            raise ValueError(f"overrides must name projected fields: {stray}")
        if len(set(names)) != len(names):
            raise ValueError(f"a field is named twice in a projection of {cls.__name__}")
        fields: dict[str, Any] = {}
        for name in names:
            if name in overrides:
                fields[name] = overrides[name]
            else:
                info = cls.model_fields[name]
                fields[name] = (info.annotation, copy.copy(info))
        return create_model(f"{cls.__name__}Projection", **fields)
