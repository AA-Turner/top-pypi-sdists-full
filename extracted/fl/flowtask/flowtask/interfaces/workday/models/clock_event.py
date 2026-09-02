"""Clock-event Pydantic models for Workday Time Tracking write operations.

These are pure data models with no SOAP coupling.  They are used by the
write handlers (PutTimeClockEventsType, ImportTimeClockEventsType,
ImportReportedTimeBlocksType) and by the Workday component for input
validation before any SOAP call (G7).
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, Field, model_validator


# ---------------------------------------------------------------------------
# Clock_Event_Type constraint
# ---------------------------------------------------------------------------

ClockEventType = Literal["In", "Break", "Meal", "Out"]
"""Valid values for Clock_Event_Type_Reference per Workday WWS v46.1 docs.

This is a BUSINESS RULE, NOT a WSDL xsd:enumeration.  The Literal enforces
it at Pydantic-validation time so invalid values are rejected before any
SOAP call (G7).
"""


# ---------------------------------------------------------------------------
# ClockEvent — one time-clock event for Put_/Import_Time_Clock_Events
# ---------------------------------------------------------------------------

class ClockEvent(BaseModel):
    """One Time Clock Event for Put_Time_Clock_Events / Import_Time_Clock_Events.

    Field names mirror the Workday Time Tracking operation; all references
    are resolved to ID-typed SOAP structures inside the handler.

    Args:
        employee_id: Workday Employee_ID (required, plain xsd:string).
        event_datetime: Time_Clock_Event_Date_Time (required, xsd:dateTime).
        clock_event_type: Clock_Event_Type_Reference value — one of
            ``In``, ``Break``, ``Meal``, ``Out`` (required).
        time_clock_event_id: CLIENT-assigned Time_Clock_Event_ID.  Leave
            ``None`` to let Workday auto-generate.  This is the per-event
            identifier; Workday returns NO WID in the Put response (v46.1).
            **Required when ``delete=True``** — you can only delete an event
            you can identify by its ID.
        position_id: Optional Position_ID (plain xsd:string).
        time_zone: Optional Time_Zone_Reference value (``type="Time_Zone_ID"``).
        time_entry_code: Optional Time_Entry_Code (plain xsd:string, NOT a
            reference wrapper).
        auto_submit: Whether to auto-submit for approval (default ``False``).
        delete: Set ``True`` to DELETE an existing Time Clock Event instead of
            adding one.  Emits ``Delete_Time_Clock_Event=Y`` via the same
            ``Put_Time_Clock_Events`` operation; requires ``time_clock_event_id``
            (the soft-delete leaves the block visible with ``Is_Deleted=true``
            on read).  Default ``False``.
        location: Optional Workday ``Location`` (the ``Location`` field on the
            clock event — an ORGANIZATIONAL location id, plain xsd:string, NOT
            geo coordinates).  This is the location the worker ACTUALLY worked
            at and acts as the OVERRIDE over their default/assigned location:
            Workday derives the worker's default location from their position,
            and if this value differs it is surfaced as the "override location"
            on reports (e.g. the Custom Punch report's ``Override_Location`` vs
            ``Default_Location``).  Leave ``None`` to keep the worker's default.
            There is NO separate override field on the write side (verified in
            the WSDL + Put_Time_Clock_Events docs v46.1) — this single field is
            the override.  Sent to Workday when set.
        latitude: Optional GPS latitude captured by a mobile client.  NOT a
            Workday clock-event field (the Time Tracking WSDL has no geo field
            in any version), so it is NEVER sent to Workday — it is carried on
            the model for the calling API to persist in its own store.
        longitude: Optional GPS longitude — same handling as ``latitude``
            (model metadata only, not sent to Workday).
        cost_center: Optional Workday ``Cost_Center`` (the ``Cost_Center`` field
            on the clock event — plain xsd:string, an organizational cost-center
            id, NOT geo). Acts as the override cost center for this punch; leave
            ``None`` to keep the worker's default. Sent to Workday when set.
        override_rate: Override Rate used while reporting time; presence-based
            — a value incl. 0 is sent, None omits it. Currency derived by Workday.
        comment: Optional free-text comment.
    """

    employee_id: str
    event_datetime: datetime
    clock_event_type: ClockEventType
    time_clock_event_id: Optional[str] = None
    position_id: Optional[str] = None
    time_zone: Optional[str] = None
    time_entry_code: Optional[str] = None
    auto_submit: bool = False
    delete: bool = False
    location: Optional[str] = None
    cost_center: Optional[str] = None
    # GPS — captured by mobile clients, persisted by the caller; Workday's clock
    # event has NO geo field, so these are intentionally NOT sent over SOAP.
    latitude: Optional[float] = Field(default=None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(default=None, ge=-180.0, le=180.0)
    override_rate: Optional[float] = Field(default=None, ge=0)
    comment: Optional[str] = None

    @model_validator(mode="after")
    def _delete_requires_event_id(self) -> "ClockEvent":
        """A delete must identify the target event by its Time_Clock_Event_ID."""
        if self.delete and not self.time_clock_event_id:
            raise ValueError(
                "delete=True requires time_clock_event_id "
                "(the Time_Clock_Event_ID of the event to delete)."
            )
        return self

    class Config:
        extra = "allow"


# ---------------------------------------------------------------------------
# ReportedTimeBlock — one reported time block for Import_Reported_Time_Blocks
# ---------------------------------------------------------------------------

class ReportedTimeBlock(BaseModel):
    """One reported time block for Import_Reported_Time_Blocks.

    Args:
        employee_id: Workday Employee_ID (required).
        position_id: Optional Position_ID.
        start_datetime: Block start date/time (required).
        end_datetime: Block end date/time (optional; ISO-8601 string accepted).
        time_entry_code: Optional Time_Entry_Code (plain string).
        reported_quantity: Optional duration/quantity of time.
        override_rate: Override Rate used while reporting time; presence-based
            — a value incl. 0 is sent, None omits it. Currency derived by Workday.
        comment: Optional free-text comment.
    """

    employee_id: str
    position_id: Optional[str] = None
    start_datetime: datetime
    end_datetime: Optional[str] = None
    time_entry_code: Optional[str] = None
    reported_quantity: Optional[float] = None
    override_rate: Optional[float] = Field(default=None, ge=0)
    comment: Optional[str] = None

    class Config:
        extra = "allow"


# ---------------------------------------------------------------------------
# ClockEventResult — per-row submission outcome
# ---------------------------------------------------------------------------

class ClockEventResult(BaseModel):
    """Per-row submission outcome echoed back into the flow (G6).

    Notes:
        - ``Put_Time_Clock_Events`` returns ONLY ``Response_Text`` — no
          per-event WID (verified Workday WWS v46.1).  ``event_id`` carries
          the CLIENT-assigned ``Time_Clock_Event_ID`` we sent (echoed back);
          ``submitted``/``error`` are atomic per batch.
        - ``Import_*`` responses return a single ``Import_Process_Reference``
          (async — not awaited, see Non-Goals).  ``event_id`` is that
          reference, repeated on every row.

    Args:
        submitted: ``True`` if the event was accepted; ``False`` on fault.
        event_id: For Put — the client-assigned ``Time_Clock_Event_ID``.
            For Import — the batch ``Import_Process_Reference``.
        error: Fault message when ``submitted=False``; ``None`` on success.
    """

    submitted: bool
    event_id: Optional[str] = None
    error: Optional[str] = None
