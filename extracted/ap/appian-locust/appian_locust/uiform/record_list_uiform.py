from typing import Any, Dict, Optional
from urllib.parse import quote

from .._interactor import _Interactor
from .._records_helper import get_all_records_from_json, get_records_from_json_by_column
from ..utilities.helper import find_component_by_attribute_and_type_in_dict
from .uiform import SailUiForm, START_PROCESS_LINK_TYPE

IDENTIFIER_CONTEXT = "identifier"


class RecordListUiForm(SailUiForm):
    """
    UiForm representing a Record List from Tempo Records
    """

    def __init__(self, interactor: _Interactor, state: Dict[str, Any], breadcrumb: str = "RecordListUi"):
        super().__init__(interactor, state, breadcrumb)
        self._identifier = self._state[IDENTIFIER_CONTEXT]

    def filter_records_using_searchbox(self, search_term: str = "", locust_request_label: str = "") -> 'RecordListUiForm':
        """
        This method allows you to Filter the Record Type List (displaying record instance for a specific record type)
        which makes the same request when typing something in the search box and reloading the page.
        More interactions (with the filtered list) can be performed on the returned SailUiForm Object.

        Note: This function does not require unfocusing from the search box as you would in the UI.

        Args:
            search_term(str, optional): Term to filter records list to
            locust_label (str, optional): label to associate request with

        Examples:

            >>> form.filter_records_using_searchbox('Donuts')

        Returns (RecordListUiForm): The record type list UiForm with the filtered results.
        """
        context_label = locust_request_label or f"{self.breadcrumb}.RecordType.SearchByText"
        search_uri = f"{self.form_url}?searchTerm={quote(search_term)}"

        headers = self._interactor.setup_sail_headers()
        response = self._interactor.get_page(uri=search_uri, headers=headers, label=context_label)
        return RecordListUiForm(self._interactor, response.json(), breadcrumb=context_label)

    def clear_records_search_filters(self) -> 'RecordListUiForm':
        """
        Clear any search filters on the records list

        Returns: Unfiltered RecordsListUiForm
        """
        context_label = f"{self.breadcrumb}.RecordType.ClearFilters"
        clear_uri = self.form_url

        headers = self._interactor.setup_sail_headers()
        response = self._interactor.get_page(uri=clear_uri, headers=headers, label=context_label)
        return RecordListUiForm(self._interactor, response.json(), breadcrumb=context_label)

    def get_visible_record_instances(self, column_index: Optional[int] = None) -> Dict[str, Any]:
        """
        Retrieve information about all visible records on the page.
        Args:
            column_index: Which column to retrieve record information for. If no column is selected, every record link in the UI will be retrieved.

        Returns: Dictionary with record instance information
        """
        if column_index is not None:
            record_instances, _ = get_records_from_json_by_column(self._state, column_index)
        else:
            record_instances, _ = get_all_records_from_json(self._state)
        return record_instances

    def click_record_list_action(self, label: str, locust_request_label: Optional[str] = None) -> 'RecordListUiForm':
        """
        Click on an action in a record list
        Args:
            label: The label of the record list action to click
            locust_request_label: The label locust should associate with this request

        Returns: UiForm with action clicked

        """
        component = find_component_by_attribute_and_type_in_dict('label', label, START_PROCESS_LINK_TYPE, self._state)
        process_model_uuid = component.get("pmUuid", "")
        cache_key = component.get("cacheKey", "")
        if not process_model_uuid:
            raise Exception(f"Record List Action component does not have process model UUID set.")
        elif not cache_key:
            raise Exception(f"Record List Action component does not have cache key set.")

        locust_request_label = locust_request_label or f"RecordListUiform.ClickAction.{label}"
        new_state = self._interactor.click_record_list_action(component_label=label, process_model_uuid=process_model_uuid,
                                                              cache_key=cache_key, locust_request_label=locust_request_label)
        self._reconcile_state(new_state, skipValidations=True)
        return self

    def _get_record_list_identifier(self) -> Optional[Dict[str, Any]]:
        return self._identifier
