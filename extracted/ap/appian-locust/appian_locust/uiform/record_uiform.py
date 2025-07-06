from typing import Any, Dict

from .._interactor import _Interactor
from .._records_helper import get_record_header_response, get_record_summary_view_response
from .uiform import SailUiForm


class RecordInstanceUiForm(SailUiForm):
    """
    UiForm representing a Record Instance UI. Supports both summary and header record views. Defaults to summary view
    """

    def __init__(self, interactor: _Interactor, state: Dict[str, Any], summary_view: bool = True, breadcrumb: str = "RecordUi"):
        active_state = get_record_summary_view_response(state) if summary_view else get_record_header_response(state)
        super().__init__(interactor, active_state, breadcrumb)
        self.__feed_state = state

    def get_summary_view(self) -> 'RecordInstanceUiForm':
        """
        Get the summary view of the record instance
        Returns (RecordInstanceUiForm): UiForm updated to summary view

        """
        self._reconcile_state(get_record_summary_view_response(self.__feed_state), skipValidations=True)
        return self

    def get_header_view(self) -> 'RecordInstanceUiForm':
        """
        Get the header view of the record instance
        Returns (RecordInstanceUiForm): UiForm updated to header view

        """
        self._reconcile_state(get_record_header_response(self.__feed_state), skipValidations=True)
        return self
