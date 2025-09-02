"""NextGen Insurance Listing model."""
from t_desktop.config import IS_WINDOWS_OS
from typing import Optional

if IS_WINDOWS_OS:
    from pywinauto.controls.uia_controls import EditWrapper
from t_object import ThoughtfulObject


class InsuranceListing(ThoughtfulObject):
    """Insurance Listing Model."""

    payer_row: Optional[EditWrapper] = None
    payer: str = ""
    policy_number: str = ""
