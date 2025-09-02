from decimal import Decimal
from t_object import ThoughtfulObject
from t_desktop.config import IS_WINDOWS_OS

if IS_WINDOWS_OS:
    from pywinauto.controls.uia_controls import EditWrapper

from typing import Optional


class COBDetails(ThoughtfulObject):
    """Represents details of a COB entry."""

    rsn_code: str = ""
    rsn_amt: Decimal = Decimal(0)
    rsn_amt_element: Optional[EditWrapper] = None
