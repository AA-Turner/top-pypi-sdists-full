"""NextGen Batch Posting Row model."""
from typing import Optional

from t_desktop.config import IS_WINDOWS_OS
from t_object import ThoughtfulObject

if IS_WINDOWS_OS:
    from pywinauto.controls.uia_controls import EditWrapper, ListItemWrapper


class BatchPostingRow(ThoughtfulObject):
    """Represents a row in Batch Posting Window."""

    text: Optional[str] = None
    visible: Optional[bool] = None
    description: Optional[str] = None
    edit_wrapper: Optional[EditWrapper] = None
    index: Optional[int] = None
    row_element: Optional[ListItemWrapper] = None
    member_count: Optional[str] = None
