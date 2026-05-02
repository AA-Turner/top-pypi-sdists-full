from datetime import datetime
from typing import Optional
from datamodel import Field
from .abstract import AbstractNotificationLog


class ZoomLog(AbstractNotificationLog):
    """Log entry for SMS messages sent via Zoom Phone API.

    Captures the full Zoom response: message_id, session_id and sent_at,
    plus the business-level scenario_id (e.g. LC_WELCOME, LC_5_SHIFTS).

    Table: navigator.zoom_log
    """
    message_id:   str           = Field(primary_key=True, required=True)
    session_id:   Optional[str] = Field(required=False, default=None)
    sent_at:      datetime
    scenario_id:  Optional[str] = Field(required=False, default=None)
    associate_id: Optional[str] = Field(required=False, default=None)
    token:        Optional[str] = Field(required=False, default=None)
    clicked_at:   Optional[datetime] = Field(required=False, default=None)
    ip_address:   Optional[str] = Field(required=False, default=None)
    user_agent:   Optional[str] = Field(required=False, default=None)

    class Meta:
        name   = 'zoom_log'
        schema = 'navigator'
