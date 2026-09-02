from typing import List, Optional, Dict, Any
from decimal import Decimal
from pydantic import BaseModel, Field, validator
from datetime import date, datetime

class TimeBlock(BaseModel):
    """
    Pydantic model for a Workday calculated time block record.
    `raw_data` holds the full SOAP response dict for any extra fields.
    """
    # Basic identification
    # NOTE: every field below is genuinely optional — Workday omits many of them
    # depending on the worker/time-block (e.g. unprocessed clock events, or
    # tenants that don't populate is_deleted). In Pydantic v2 ``Optional[X]``
    # WITHOUT a default is still REQUIRED, so each carries ``= None`` to stay
    # tolerant of partial responses (only ``raw_data`` is mandatory).
    time_block_id: Optional[str] = None
    time_block_wid: Optional[str] = None
    worker_id: Optional[str] = None
    worker_name: Optional[str] = None

    # Date and time information
    calculated_date: Optional[date] = None
    calculated_in_time: Optional[datetime] = None
    calculated_out_time: Optional[datetime] = None
    shift_date: Optional[date] = None

    # Quantity and calculations
    calculated_quantity: Optional[float] = None

    # Status information
    status: Optional[str] = None
    is_deleted: Optional[bool] = None

    # Calculation details
    calculation_tags: Optional[List[str]] = None
    last_updated: Optional[datetime] = None

    # Worktags (additional categorization)
    worktags: Optional[Dict[str, Any]] = None
    
    # Raw payload
    raw_data: Dict[str, Any] = Field(..., exclude=True)

    @validator("*", pre=True)
    def _convert_decimal(cls, v):
        if isinstance(v, Decimal):
            return float(v)
        return v

    class Config:
        extra = "ignore"
