from __future__ import annotations

import typing as t
from collections.abc import Callable

from pydantic import BaseModel, ConfigDict, Field, model_validator

# Import directly from modules to avoid circular import through generated/__init__.py
from connector_sdk_types.generated.models.ticket_body_format import TicketBodyFormat
from connector_sdk_types.generated.models.ticket_destination_field import TicketDestinationField


class TicketInfo(BaseModel):
    """The ticket metadata one connection reports in `app_info`.

    Each field fills the `x-ticket-*` extension of the same name; a field left `None` stays
    unset. Frozen, so what the connector returns is what was validated.
    """

    model_config = ConfigDict(frozen=True)

    ticket_destination_fields: list[TicketDestinationField] | None = None
    ticket_description_formats: list[TicketBodyFormat] | None = None
    ticket_comment_formats: list[TicketBodyFormat] | None = None
    ticket_summary_max_length: int | None = Field(default=None, ge=1)
    ticket_description_max_length: int | None = Field(default=None, ge=1)

    @model_validator(mode="after")
    def _destination_fields_in_dependency_order(self) -> TicketInfo:
        # Fields are rendered in order and a dependent field's options are fetched with the
        # picks made so far, so a field can only depend on one declared before it.
        seen: set[str] = set()
        for field in self.ticket_destination_fields or []:
            if field.key in seen:
                raise ValueError(f"Duplicate ticket destination field key: {field.key!r}")
            if field.depends_on is not None and field.depends_on not in seen:
                raise ValueError(
                    f"Ticket destination field {field.key!r} depends on {field.depends_on!r}, "
                    "which is not declared before it"
                )
            seen.add(field.key)
        return self


TicketInfoCallable: t.TypeAlias = Callable[[t.Any], TicketInfo]
"""Describes one connection's ticketing from its validated settings (an instance of the
integration's `settings_model`). `app_info` carries no credentials, so this reads settings
only."""


class ItsmSettings(BaseModel):
    """Settings for the ItsmModule, for a connector that files tickets.

    `app_info` calls `ticket_info` whenever the request carries settings and reports what it
    returns in the `x-ticket-*` fields:

    ```python
    def ticket_info(settings: MySettings) -> TicketInfo:
        return TicketInfo(
            ticket_description_formats=[TicketBodyFormat(settings.body_format)],
            ticket_summary_max_length=255,
        )

    integration = Integration(
        ...,
        settings_model=MySettings,
        itsm_settings=ItsmSettings(ticket_info=ticket_info),
    )
    ```

    Without settings on the request, or when they don't validate or `ticket_info` fails,
    `app_info` leaves the `x-ticket-*` fields unset, as it does for a connector without the module.
    """

    ticket_info: TicketInfoCallable = Field(
        description="Describes one connection's ticketing, given its validated settings.",
    )


__all__ = [
    "ItsmSettings",
    "TicketBodyFormat",
    "TicketDestinationField",
    "TicketInfo",
    "TicketInfoCallable",
]
