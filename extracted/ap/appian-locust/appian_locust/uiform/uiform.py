import datetime
import enum
import errno
import json
import os
import random
import warnings
from datetime import date
from typing import Any, Dict, List, Union, Optional, TYPE_CHECKING
from urllib.parse import quote, urlparse
from copy import deepcopy

from .. import ComponentNotFoundException
from ..utilities import logger
from .._grid_interactor import GridInteractor
from .._interactor import _Interactor, TEMPO_SITE_STUB
from .._task_opener import _TaskOpener
from .._ui_reconciler import UiReconciler
from ..exceptions import InvalidComponentException, InvalidDateRangeException, ChoiceNotFoundException, DisabledComponentException, IgnoredValidationException
from ..utilities.helper import (extract_all_by_label, find_component_by_attribute_and_index_in_dict,
                                find_component_by_attribute_in_dict, find_component_by_index_in_dict,
                                find_component_by_attribute_and_type_in_dict, find_component_by_type_and_attribute_and_index_in_dict)
from .._records_helper import _is_grid

if TYPE_CHECKING:
    from ..uiform import RecordInstanceUiForm

KEY_UUID = "uuid"
KEY_CONTEXT = "context"
START_PROCESS_LINK_TYPE = 'StartProcessLink'
PROCESS_TASK_LINK_TYPE = 'ProcessTaskLink'

log = logger.getLogger(__name__)


class SailUiForm:
    def __init__(self, interactor: _Interactor, state: Dict[str, Any], breadcrumb: str = "SailUi"):
        """
        Appian rendered UI that provides page interactivity. ``SailUiForm`` is a base class that is abstracted
        by specific Appian form types to handle requirements or provide metadata unique to that page.

        Args:
            base: Action, Record, etc.. interactor object
            state: JSON representation of the initial form
            latest_state: JSON representation of the last to the the form
            url: Url to make updates to the form
            breadcrumbs: Path used to create locust labels

        """
        self._interactor: _Interactor = interactor
        self.task_opener: _TaskOpener = _TaskOpener(self._interactor)
        self._state: Dict[str, Any] = state
        self.form_url = ""
        self.form_url = self._get_update_url_for_reeval(state)
        if any(key not in self._state for key in (KEY_CONTEXT, KEY_UUID)):
            return None
        self.context: dict = self._state[KEY_CONTEXT]
        self.uuid: str = self._state[KEY_UUID]
        self.grid_interactor: GridInteractor = GridInteractor()
        self.reconciler: UiReconciler = UiReconciler()
        self.breadcrumb = breadcrumb

        # Cache data types on opening new form
        self._interactor.datatype_cache.cache(self._state)

    def get_latest_state(self) -> Dict[str, Any]:
        """
        Provides a deep copy of latest state of UI form.

        Returns (dict): deep copy of last recorded response.

        """
        return deepcopy(self._state)

    def __str__(self) -> str:
        return f"self_state={json.dumps(self._state,indent=4)}"

    def fill_field_by_attribute_and_index(self, attribute: str, attribute_value: str, fill_value: str, index: int = 1, locust_request_label: str = "") -> 'SailUiForm':
        """
        Selects a Field by "attribute" and its value provided "attribute_value" and an index if more than one Field is found
        and fills it with text "fill_value"

        Args:
            attribute(str): Name of the field to fill
            attribute_value(str): Value for the attribute passed in to this function
            fill_value(str): Value to fill in the field

        Keyword Args:
            index(int): Index of the field to fill if more than one match the attribute and attribute_value criteria (default: 1)
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.fill_field_by_attribute_and_index("label", "Write a comment", "Hello, Testing")
            # selects the first Component with the "label" attribute having "Write a comment" value
            # and fills it with "Hello, Testing"

            >>> form.fill_field_by_attribute_and_index("label", "Write a comment", "Hello, Testing", 2)
            # selects the second Component with the "label" attribute having "Write a comment" value
            # and fills it with "Hello, Testing"

        """
        component = find_component_by_attribute_and_index_in_dict(attribute, attribute_value, index, self._state)

        reeval_url = self._get_update_url_for_reeval(self._state)
        locust_label = locust_request_label or f"{self.breadcrumb}.FillTextFieldByAttribute.{attribute}"
        new_state = self._interactor.fill_textfield(
            reeval_url, component, fill_value, self.context, self.uuid, label=locust_label)
        if not new_state:
            raise Exception(f"No response returned when trying to update the field with '{attribute}' = '{attribute_value}' at index '{index}'")

        return self._reconcile_state(new_state)

    def fill_text_field(self, label: str, value: str, is_test_label: bool = False, locust_request_label: str = "", index: int = 1) -> 'SailUiForm':
        """
        Fills a field on the form, if there is one present with the following label (case sensitive)
        Otherwise throws a NotFoundException

        Args:
            label(str): Label of the field to fill out
            value(str): Value to fill the field with

        Keyword Args:
            is_test_label(bool): If you are filling a text field via a test label instead of a label, set this boolean to true
            locust_request_label(str): Label used to identify the request for locust statistics
            index(int): Index of the field to fill if more than one match the label criteria (default: 1)

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.fill_text_field('Title','My New Novel')

        """
        attribute_to_find = 'testLabel' if is_test_label else 'label'
        return self.fill_field_by_attribute_and_index(attribute_to_find, label, value, index, locust_request_label)

    def fill_field_by_index(self, type_of_component: str, index: int, text_to_fill: str, locust_request_label: str = "") -> 'SailUiForm':
        """
        Selects a Field by its index and fills it with a text value

        Args:
            type_of_component(str): Name of the component to fill
            index(int): Index of the field on the page (is it the first one found, or second etc.)
            value(int): Value to fill in the field of type 'type_of_component'

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.fill_field_by_index("ParagraphField", 1, "Hello, Testing")
            # selects the first ParagraphField with the value "Hello, Testing"

        """
        component = find_component_by_index_in_dict(type_of_component, index, self._state)
        reeval_url = self._get_update_url_for_reeval(self._state)
        locust_label = locust_request_label or f"{self.breadcrumb}.FillTextFieldByIndex.{index}"
        new_state = self._interactor.fill_textfield(
            reeval_url, component, text_to_fill, self.context, self.uuid, label=locust_label)
        if not new_state:
            raise Exception(
                f'''
                    No response returned when trying to fill: '{text_to_fill}' in the component: '{type_of_component}'
                    with index: '{index}' on the current page")
                ''')

        return self._reconcile_state(new_state)

    def fill_field_by_any_attribute(self, attribute: str, value_for_attribute: str, text_to_fill: str, locust_request_label: str = "", index: int = 1) -> 'SailUiForm':
        """
        Selects a Field by "attribute" and its value provided "value_for_attribute"
        and fills it with text "text_to_fill"

        Args:
            attribute(str): Name of the component to fill
            value_for_attribute(str): Value for the attribute passed in to this function
            text_to_fill(str): Value to fill the field with

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics
            index(int): Index of the field to fill if more than one match the label criteria (default: 1)

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.fill_field_by_any_attribute("placeholder", "Write a comment", "Hello, Testing")
            # selects the Component with the "placeholder" attribute having "Write a comment" value
            # and fills it with "Hello, Testing"

        """
        return self.fill_field_by_attribute_and_index(attribute, value_for_attribute, text_to_fill, index, locust_request_label)

    # Aliases for fill_text_field() function
    fill_paragraph_field = fill_text_field

    def fill_picker_field(self, label: str, value: str, identifier: str = 'id', format_test_label: bool = True,
                          fill_request_label: str = "", pick_request_label: str = "") -> 'SailUiForm':
        """
        Enters the value in the picker widget and selects one of the suggested items
        if the widget is present with the following label (case sensitive)

        If there is more than one suggestion, this method will select a random one out of the list

        Otherwise this throws a NotFoundException

        The mechanism it uses to find a pickerWidget is prefixing the picker field label with test- and looking for a testLabel

        Args:
            label(str): Label of the field to fill out
            value(str): Value to update the label to

        Keyword Args:
            identifier(str): Key to select the field to filter on, defaults to 'id'
            format_test_label(bool): If you don't want to prepend a "test-" to the testLabel, set this to False
            fill_request_label(str): Label to associate in locust statistics with filling the picker field
            pick_request_label(str): Label to associate in locust statistics with selecting the picker suggestion

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.fill_picker_field('Title','My New Novel')
            >>> form.fill_picker_field('People','Jeff George')
            >>> form.fill_picker_field('Customer', 'GAC Guyana', identifier='code')

        """
        # pickerFieldCustom will add a test-Label at the level where the suggestions/saveInto exist
        if not format_test_label:
            test_label = label
        else:
            test_label = f'test-{label}'
        component = find_component_by_attribute_and_type_in_dict('testLabel', test_label, 'PickerWidget', self._state)

        locust_label = fill_request_label or f"{self.breadcrumb}.FillPickerField.{label}"
        new_state = self._interactor.fill_pickerfield_text(
            self.form_url, component, value, self.context, self.uuid, label=locust_label)

        if not new_state:
            raise Exception(f"No response returned when trying to update field with label '{label}'")

        self._reconcile_state(new_state)

        component = find_component_by_attribute_and_type_in_dict('testLabel', test_label, 'PickerWidget', self._state)

        suggestions_list = extract_all_by_label(component, 'suggestions')

        if not suggestions_list:
            raise Exception(f"No suggestions returned when '{value}' was entered in the picker field.")

        identifiers = extract_all_by_label(suggestions_list, 'identifier')

        if not identifiers:
            raise Exception(f"No identifiers found when '{value}' was entered in the picker field.")

        # Introspect to see if there's an ID
        index_by_id = identifiers[0].get(identifier) is not None
        id_index = identifier if index_by_id else '#v'

        v_or_id = [identifier.get(id_index) for identifier in identifiers if identifier.get(id_index)]

        if not v_or_id:
            raise Exception(f"Could not extract picker values '{id_index}' from suggestions_list {suggestions_list}")

        v_choice = random.choice(range(len(v_or_id)))

        dict_value = identifiers[v_choice]

        locust_label = pick_request_label or f"{self.breadcrumb}.SelectPickerSuggestion.{label}"
        newer_state = self._interactor.select_pickerfield_suggestion(
            self.form_url, component, dict_value, self.context, self.uuid, label=locust_label)

        if not newer_state:
            raise Exception(f"No response returned when trying to update field with label '{label}'")

        return self._reconcile_state(newer_state)

    def fill_cascading_pickerfield(self, label: str, selections: List[str], format_test_label: bool = True,
                                   locust_request_label: str = "") -> 'SailUiForm':
        """
        Select a choice for a cascading pickerfield, one where multiple choices can be chained together

        Args:
            label(str): Label of the field to fill out
            selections(str): The series of options to select through

        Keyword Args:
            format_test_label(bool): If you don't want to prepend a "test-" to the testLabel, set this to False
            locust_request_label(str): Label to associate in locust statistics with selecting the picker choice
        """
        # pickerFieldCustom will add a test-Label at the level where the suggestions/saveInto exist
        if not format_test_label:
            test_label = label
        else:
            test_label = f'test-{label}'
        component = find_component_by_attribute_and_type_in_dict('testLabel', test_label, 'PickerWidget', self._state)

        locust_request_label = locust_request_label or f"{self.breadcrumb}.SelectCascadingPickerField.{label}"
        choices = component["inlineChoices"]

        for selection in selections[:-1]:
            selection_details = self._interactor.find_selection_from_choices(selection, choices)

            if not selection_details:
                raise ChoiceNotFoundException(f"Selection {selection} not found among choices for cascading pickerfield {label}")

            request_payload = self._interactor.initialize_cascading_pickerfield_request(component)
            request_payload = self._interactor.fill_cascading_pickerfield_request(request_payload, selection_details)

            choices = self._interactor.fetch_new_cascading_pickerfield_selection(request_payload, locust_request_label)

        # At this point, we should have the final list of choices
        selection_details = self._interactor.find_selection_from_choices(selections[-1], choices)
        if not selection_details:
            raise ChoiceNotFoundException(
                f"Selection {selections[-1]} not found among choices for cascading pickerfield {label}")

        new_state = self._interactor.select_pickerfield_suggestion(
            self.form_url,
            component,
            selection_details["id"],
            self.context,
            self.uuid,
            label=locust_request_label
        )

        if not new_state:
            raise Exception(f"No response returned when trying to update selection for pickerfield with label '{label}'")

        return self._reconcile_state(new_state)

    def fill_cascading_pickerfield_with_attribute(self, attribute: str, attribute_value: str,
                                                  selections: List[str],
                                                  locust_request_label: str = "") -> 'SailUiForm':
        """
        Select a choice for a cascading pickerfield using any attribute, one where multiple choices can be chained
        together
        Args:
            attribute(str): Name of the component to fill
            attribute_value(str): Value for the attribute passed in to this function
            selections(str): The series of options to select through

        Keyword Args:
            locust_request_label(str): Label to associate in locust statistics with selecting the picker choice
        """
        # pickerFieldCustom will add a test-Label at the level where the suggestions/saveInto exist
        component = find_component_by_attribute_and_type_in_dict(attribute, attribute_value, 'PickerWidget', self._state)

        locust_request_label = locust_request_label or f"{self.breadcrumb}.SelectCascadingPickerFieldWithAttribute{attribute}"
        choices = component["inlineChoices"]

        for selection in selections[:-1]:
            selection_details = self._interactor.find_selection_from_choices(selection, choices)

            if not selection_details:
                raise ChoiceNotFoundException(f"Selection {selection} not found among choices for cascading pickerfield having attribute: {attribute} with value {attribute_value}")

            request_payload = self._interactor.initialize_cascading_pickerfield_request(component)
            request_payload = self._interactor.fill_cascading_pickerfield_request(request_payload, selection_details)

            choices = self._interactor.fetch_new_cascading_pickerfield_selection(request_payload, locust_request_label)

        # At this point, we should have the final list of choices
        selection_details = self._interactor.find_selection_from_choices(selections[-1], choices)
        if not selection_details:
            raise ChoiceNotFoundException(
                f"Selection {selections[-1]} not found among choices for cascading pickerfield having attribute: {attribute} with value {attribute_value}")

        new_state = self._interactor.select_pickerfield_suggestion(
            self.form_url,
            component,
            selection_details["id"],
            self.context,
            self.uuid,
            label=locust_request_label
        )

        if not new_state:
            raise Exception(f"No response returned when trying to update selection for pickerfield having attribute: {attribute} with value {attribute_value}")

        return self._reconcile_state(new_state)

    def click(self, label: str, is_test_label: bool = False, locust_request_label: str = "", index: int = 1) -> 'SailUiForm':
        """
        Clicks on a component on the form, if there is one present with the following label (case sensitive)
        Otherwise throws a NotFoundException

        Can also be called as 'click_link' or 'click_button' to convey intent

        This can also click StartProcessLinks or ProcessTaskLinks

        Args:
            label(str): Label of the component to click
            is_test_label(bool): If you are clicking a button or link via a test label instead of a label, set this boolean to true

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics
            index(int): Index of the component to click if more than one match the label criteria (default: 1)

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.click('Submit')
            >>> form.click('SampleTestLabel', is_test_label = True)

        """
        locust_label = locust_request_label or f"{self.breadcrumb}.Click.{label}"
        return self._click(label, is_test_label=is_test_label, locust_request_label=locust_label, index=index)

    def click_button(self, label: str, is_test_label: bool = False, locust_request_label: str = "", index: int = 1) -> 'SailUiForm':
        """
        Clicks on a component on the form, if there is one present with the following label (case sensitive)
        Otherwise throws a NotFoundException

        This can also click StartProcessLinks or ProcessTaskLinks

        Args:
            label(str): Label of the component to click
            is_test_label(bool): If you are clicking a button via a test label instead of a label, set this boolean to true

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics
            index(int): Index of the component to click if more than one match the label criteria (default: 1)

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.click_button('Save')
            >>> form.click_link('Update')

        """
        locust_label = locust_request_label or f"{self.breadcrumb}.ClickButton.{label}"
        return self._click(label, is_test_label=is_test_label, locust_request_label=locust_label, index=index)

    def click_link(self, label: str, is_test_label: bool = False, locust_request_label: str = "", index: int = 1) -> 'SailUiForm':
        """
        Clicks on a component on the form, if there is one present with the following label (case sensitive)
        Otherwise throws a NotFoundException

        This can also click StartProcessLinks or ProcessTaskLinks

        Args:
            label(str): Label of the component to click
            is_test_label(bool): If you are clicking a link via a test label instead of a label, set this boolean to true

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics
            index(int): Index of the component to click if more than one match the label criteria (default: 1)

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.click_link('Update')

        """
        locust_label = locust_request_label or f"{self.breadcrumb}.ClickLink.{label}"
        return self._click(label, is_test_label=is_test_label, locust_request_label=locust_label, index=index)

    def _click(self, label: str, is_test_label: bool = False, locust_request_label: str = "", index: int = 1) -> 'SailUiForm':
        """
        Internal function wrapped by various click methods
        """
        attribute_to_find = 'testLabel' if is_test_label else 'label'

        component = find_component_by_attribute_and_index_in_dict(attribute_to_find, label, index, self._state)

        disabled = component.get("disabled", False)
        if (disabled == True):
            raise DisabledComponentException(label=label)

        locust_label = locust_request_label or f"{self.breadcrumb}.Click.{label}"
        new_state = self._dispatch_click(component=component, locust_label=locust_label)

        # get the re-eval URI from links object of the response (new_state)
        reeval_url = self._get_update_url_for_reeval(new_state)

        if not new_state:
            raise Exception(f"No response returned when trying to click button with label '{label}'")
        return self._reconcile_state(new_state)

    def click_card_layout_by_index(self, index: int, locust_request_label: str = "") -> 'SailUiForm':
        """
        Clicks a card layout link by index.
        This method will find the CardLayout component on the UI by index and then perform
        the click behavior on its Link component.

        Args:
            index(int): Index of the card layout on which to click. (first found card layout , or second etc.)
                        (Indices start from 1)

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:
            This finds link field on the 2nd card layout on the page and clicks it. It handles StartProcessLink as well, so
            no need to call click_start_process_link() when it is on a CardLayout.

            >>> form.click_card_layout_by_index(2)

        """
        component = find_component_by_index_in_dict("CardLayout", index, self._state)

        if not component.get("link"):
            raise Exception(f"CardLayout found at index: {index} does not have a link on it")

        link_component = component.get('link')
        locust_label = locust_request_label or f"{self.breadcrumb}.ClickCardLayout.Index.{index}"
        if link_component["#t"] == "StartProcessLink":
            site_name = link_component["siteUrlStub"] or TEMPO_SITE_STUB
            page_name = link_component["sitePageUrlStub"]
            group_name = link_component.get("siteGroupUrlStub", None)
            new_state = self._click_start_process_link(site_name, page_name, group_name, False, link_component, locust_request_label=locust_label)
        else:
            new_state = self._interactor.click_component(self.form_url, link_component, self.context, self.uuid, label=locust_label)

        if not new_state:
            raise Exception(f"No response returned when trying to click card layout at index '{index}'")

        reeval_url = self._get_update_url_for_reeval(new_state)
        return self._reconcile_state(new_state, skipValidations=True)

    def click_record_link_by_attribute_and_index(self, attribute: str = "", attribute_value: str = "", index: int = 1, locust_request_label: str = "") -> 'RecordInstanceUiForm':
        """
        Click the index'th record link on the form if there is one present with an attribute matching attribute_value
        If no attribute is provided, the index'th record link is selected from all record links in the form
        Otherwise throws a ComponentNotFoundException

        NOTE: This method returns a NEW RecordInstanceUiForm object, so you must save its return value into a new variable, like so:

            >>> record_uiform = other_uiform.click_record_link_by_attribute_and_index(...)

        Keyword Args:
            attribute(str): Attribute to check for 'attribute_value' (default: "")
            attribute_value(str): Attribute value of record link to click (default: "")
            index(int): Index of record link to click (default: 1)
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The record form (feed) for the linked record.

        """
        component_type = 'RecordLink'
        component = find_component_by_type_and_attribute_and_index_in_dict(self._state, component_type, attribute, attribute_value, index)
        locust_label = locust_request_label or f"{self.breadcrumb}.ClickRecordLink"
        reeval_url = self._get_update_url_for_reeval(self._state)
        new_state = self._interactor.click_record_link(reeval_url, component, self.context, self.uuid,
                                                       locust_label=locust_label)
        from .record_uiform import RecordInstanceUiForm
        return RecordInstanceUiForm(self._interactor, new_state)

    def click_record_link(self, label: str, is_test_label: bool = False, locust_request_label: str = "") -> 'RecordInstanceUiForm':
        """
        Click a record link on the form if there is one present with the following label (case sensitive)
        Otherwise throws a ComponentNotFoundException

        Args:
            label(str): Label of the record link to click
            is_test_label(bool): If you are clicking a record link via a test label instead of a label, set this boolean to true

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        NOTE: This method returns a NEW RecordInstanceUiForm object, so you must save its return value into a new variable, like so:

            >>> record_uiform = other_uiform.click_record_link(...)

        Returns (RecordUiForm): The record form (feed) for the linked record.

        """
        attribute_to_find = 'testLabel' if is_test_label else 'label'
        return self.click_record_link_by_attribute_and_index(attribute=attribute_to_find, attribute_value=label, locust_request_label=locust_request_label)

    def click_record_link_by_index(self, index: int, locust_request_label: str = "") -> 'RecordInstanceUiForm':
        """
        Click the index'th record link on the form
        Otherwise throws a ComponentNotFoundException

        Args:
            index(int): Index of the record link to click (1-based)

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The record form (feed) for the linked record.

        """
        return self.click_record_link_by_attribute_and_index(index=index, locust_request_label=locust_request_label)

    def click_record_view_link(self, label: str, locust_request_label: str = "") -> 'RecordInstanceUiForm':
        """
        Click a record view link on the form if there is one present with the following label (case sensitive)
        Otherwise throws a ComponentNotFoundException

        Args:
            label(str): Label of the record link to click

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        NOTE: This method returns a NEW RecordInstanceUiForm object, so you must save its return value into a new variable, like so:

            >>> record_uiform = other_uiform.click_record_view_link(...)

        Returns (SailUiForm): The record form (feed) for the linked record.

        """
        view_tab_label = f"{label}_tab"
        outer_component = find_component_by_attribute_in_dict(attribute="testLabel", value=view_tab_label, component_tree=self._state)
        component = outer_component["link"]
        locust_label = locust_request_label or f"{self.breadcrumb}.ClickRecordLink"
        reeval_url = self._get_update_url_for_reeval(self._state)
        new_state = self._interactor.click_record_link(reeval_url, component, self.context, self.uuid,
                                                       locust_label=locust_label)
        from .record_uiform import RecordInstanceUiForm
        return RecordInstanceUiForm(self._interactor, new_state)

    def click_start_process_link(self, label: str, is_test_label: bool = False, is_mobile: bool = False, locust_request_label: str = "") -> 'SailUiForm':
        """
        Clicks a start process link on the form by label
        If no link is found, throws a ComponentNotFoundException

        Args:
            label(str): Label of the link

        Keyword Args:
            is_mobile(bool): Boolean to use the mobile form of the request
            locust_request_label(str): Label used to identify the request for locust statistics
            is_test_label(bool): Boolean indicating if label is a test label

        Returns (SailUiForm): The latest state of the UiForm

        Examples:
            >>> form.click_start_process_link('Request upgrade')

        """
        attribute_to_find = 'testLabel' if is_test_label else 'label'
        component = find_component_by_attribute_and_type_in_dict(attribute_to_find, label, START_PROCESS_LINK_TYPE, self._state)
        site_name = component["siteUrlStub"]
        page_name = component["sitePageUrlStub"]
        group_name = component.get("siteGroupUrlStub", None)

        locust_label = locust_request_label or f"{self.breadcrumb}.ClickStartProcessLink.{label}"
        new_state = self._click_start_process_link(site_name, page_name, group_name, is_mobile, component, locust_request_label=locust_label)

        return self._reconcile_state(new_state, skipValidations=True)

    def click_start_process_link_on_mobile(self, label: str, site_name: str, page_name: str, locust_request_label: str = "") -> 'SailUiForm':
        """
        Clicks a start process link on the form by label (for Mobile)
        If no link is found, throws a ComponentNotFoundException

        Args:
            label(str): Label of the link
            site_name(str): Name of the site (i.e. the Sites feature)
            page_name(str): Name of the page within the site

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.click_start_process_link_on_mobile('Open Issue')

        """
        locust_label = locust_request_label or f"{self.breadcrumb}.ClickStartProcessLink.Mobile.{label}"
        return self.click_start_process_link(label, is_mobile=True, locust_request_label=locust_label)

    def select_date_range_user_filter(
            self,
            filter_label: str,
            filter_start_date: date,
            filter_end_date: date,
            locust_request_label: Optional[str] = None
    ) -> 'SailUiForm':
        """
        Select a value on a date range user filter

        Args:
            filter_label(str): the testLabel of the filter to select a value for
            filter_start_date(date): the start date for the range
            filter_end_date(date): the end date for the range

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.select_date_range_user_filter(filter_label="userFilter", filter_start_date=datetime.date(2023, 10, 18), filter_end_date=datetime.date(2023,10,19))
        """
        if filter_start_date > filter_end_date:
            raise InvalidDateRangeException(filter_start_date, filter_end_date)
        locust_request_label = locust_request_label or f"{self.breadcrumb}.SelectDateUserFilter.{filter_label}"
        date_range_component = find_component_by_attribute_and_type_in_dict(attribute="testLabel", value=filter_label, type="DateRangeWidget", component_tree=self._state)
        new_value = {
            "startDate": {"#t": "date", "#v": f"{filter_start_date.isoformat()}Z"},
            "endDate": {"#t": "date", "#v": f"{filter_end_date.isoformat()}Z"}
        }

        new_state = self._interactor.click_generic_element(
            post_url=self.form_url,
            component=date_range_component,
            context=self.context,
            uuid=self.uuid,
            new_value=new_value,
            label=locust_request_label
        )

        return self._reconcile_state(new_state, skipValidations=True)

    def _click_start_process_link(self, site_name: str, page_name: str, group_name: Optional[str], is_mobile: bool,
                                  component: Dict[str, Any], locust_request_label: str) -> Dict[str, Any]:
        """
        This internal function is called by both click_start_process_link() and click_card_layout_by_index().
        It takes parameters needed for making a start process link call to the server and calls the interactor to do that.
        """
        process_model_opaque_id = component.get("processModelOpaqueId", "")
        cache_key = component.get("cacheKey", "")
        if not process_model_opaque_id:
            raise Exception(f"StartProcessLink component does not have process model opaque id set.")
        elif not cache_key:
            raise Exception(f"StartProcessLink component does not have cache key set.")

        return self._interactor.click_start_process_link(component=component, process_model_opaque_id=process_model_opaque_id,
                                                         cache_key=cache_key, site_name=site_name, page_name=page_name, group_name=group_name, is_mobile=is_mobile,
                                                         locust_request_label=locust_request_label)

    def _dispatch_click(self, component: Dict[str, Any], locust_label: str) -> Dict[str, Any]:
        """
        Dispatches the appropriate link interaction based on the link type if appropriate

        Args:
            link_component (Dict[str, Any]): Link component to interact with
            locust_label (str): Label used to identify the request for locust statistics

        Returns:
            Dict[str, Any]: State returned by the interaction
        """
        component_type = component.get('#t')
        # Check if component is already a supported link
        if component_type in [START_PROCESS_LINK_TYPE, PROCESS_TASK_LINK_TYPE]:
            link_component = component
            link_type = component_type
        else:
            link_component = component.get('link', {})
            link_type = link_component.get('#t')
        
        if link_type == START_PROCESS_LINK_TYPE:
            site_name = link_component["siteUrlStub"] or TEMPO_SITE_STUB
            page_name = link_component["sitePageUrlStub"]
            group_name = link_component.get("siteGroupUrlStub", None)
            new_state = self._click_start_process_link(site_name, page_name, group_name, False, link_component, locust_request_label=locust_label)
        elif link_type == PROCESS_TASK_LINK_TYPE:
            task_name = link_component.get('label') or 'Unnammed Task'
            task_id = link_component.get('opaqueTaskId')
            if not task_id:
                raise Exception(f"No task id found for task with name '{task_name}'")
            site_name = link_component.get("siteUrlStub") or TEMPO_SITE_STUB
            page_name = link_component.get("sitePageUrlStub")
            headers = {
                'X-Site-UrlStub': site_name,
                'X-Page-UrlStub': page_name,
                'X-Client-Mode': 'SITES'
            }
            new_state = self.task_opener.visit_by_task_id(task_name, task_id, extra_headers=headers)
        elif link_component:
            new_state = self._interactor.click_component(self.form_url, link_component, self.context, self.uuid, label=locust_label)

        # Add special handling for async_timer
        # A None here represents a 204 status code returned from the reevaluation request for the timer
        # When a 204/None is returned, the async operation has not finished yet, so the state should not change.
        # In this case, set the "new" state to be the current state
        elif component.get('label') == 'async_timer':
            timer_result = self._interactor.click_async_timer(self.form_url, component, self.context, self.uuid, label=locust_label)
            if timer_result is None:
                new_state = self._state
            else:
                new_state = timer_result
        else:
            new_state = self._interactor.click_component(self.form_url, component, self.context, self.uuid, label=locust_label)
        return new_state

    def click_related_action(self, label: str, is_test_label: bool = False, locust_request_label: str = "") -> 'SailUiForm':
        """
        Clicks a related action (either a related action button or link) on the form by label
        If no link is found, throws a ComponentNotFoundException

        Args:
            label(str): Label of the related action

        Keyword Args:
            is_test_label: If this label is a test label
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:
            How to use click_related_action():

            Use records function - visit_record_instance_and_get_feed_form() to get Record Instance SailUiForm, then get the header response
            and finally click on the related action by label.

            >>> feed_form = records.visit_record_instance_and_get_feed_form()

            We need to get the header response or view response  depending on if the related action is under the related actions dashboard
            or if it is a related action link on the summary view UI (which opens in a dialog).

            >>> header_form = feed_form.get_record_header_form() or feed_form.get_record_view_form()

            >>> header_form.click_related_action('Request upgrade')

        """
        attribute_to_find = 'testLabel' if is_test_label else 'label'
        component = find_component_by_attribute_in_dict(attribute_to_find, label, self._state)
        
        if is_test_label:
            component = component["recordAction"]

        # Support scenario where related action label is found within outer "ButtonWidget" rather than directly in "RelatedActionLink" component
        if "source" not in component:
            component = component.get("link", "")
        component_source = component.get("source", "")
        record_type_stub = component_source.get("recordTypeStub", "")
        opaque_related_action_id = component_source.get("opaqueRelatedActionId", "")
        open_actions_in = component.get("openActionsIn", "")
        open_action_in_a_dialog = open_actions_in == "DIALOG"

        opaque_identifier_key = "opaqueRecordRef" if open_action_in_a_dialog else "opaqueRecordId"
        opaque_record_id = component_source.get(opaque_identifier_key, "")

        if not record_type_stub or not opaque_record_id or not opaque_related_action_id:
            raise Exception(f'''
                            Related Action link component does not have recordTypeStub or opaqueRecordId or opaqueRelatedActionId set.
                            ''')
        locust_label = locust_request_label or f"{self.breadcrumb}.ClickRelatedActionLink.{label}"

        new_state = self._interactor.click_related_action(component, record_type_stub=record_type_stub, opaque_record_id=opaque_record_id,
                                                          opaque_related_action_id=opaque_related_action_id,
                                                          locust_request_label=locust_label, open_in_a_dialog=open_action_in_a_dialog)
        return self._reconcile_state(new_state, skipValidations=True)
    
    # Alias for click_related_action
    click_record_action = click_related_action

    def evaluate_record_action_field_security(self, test_label: str = "", format_test_label: bool = True, index: int = 1, locust_request_label: str = "") -> 'SailUiForm':
        """
        Triggers security evaluation to reveal record action items for a record action field

        Args:

        Keyword Args:
            test_label: Value of a record action field's testLabel attribute
                used to locate record action field with securityOnDemand to enable security evaluation prior
                to action item click. Appian will use accessibility text if it is defined to create this testLabel.
            format_test_label(bool): If you don't want to prepend a ``"test_recordActionWidget_"`` to the testLabel, set this to False
            index: Index of the record action field to evaluate security for (default: 1).  If no test_label is provided only index will be used.
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:
            How to use evaluate_record_action_field_security():

            >>> my_form.evaluate_record_action_field_security(index=2)            
            >>> my_form.evaluate_record_action_field_security(test_label="my-action-field-accessibility-text")
            >>> my_form.evaluate_record_action_field_security(format_test_label=False, test_label="test_recordActionWidget_my-action-field-accessibility-text")

        """
        
        locust_label = locust_request_label or f"{self.breadcrumb}.EvaluateRecordActionFieldSecurity"        

        if test_label:            
            # Find the record action field FieldLayout by test_label and index
            # and get the RecordActionWidget from its contents attribute.
            if format_test_label: test_label = f'test_recordActionWidget_{test_label}'
            action_field_layout_component = find_component_by_attribute_and_index_in_dict(attribute="testLabel", value=test_label, index=index, component_tree=self._state)
            if action_field_layout_component["#t"] == "RecordActionWidget":
                action_field_component = action_field_layout_component
            else:
                action_field_component = action_field_layout_component["contents"]
        else:
            action_field_component = find_component_by_index_in_dict(component_type="RecordActionWidget", index=index, component_tree=self._state)
        
        if not action_field_component["#t"] == "RecordActionWidget":
            raise Exception(f"RecordActionWidget not found in component with testLabel '{test_label}'" if 
                            test_label else f"RecordActionWidget not found at index {index}")
        if not action_field_component["securityOnDemand"]:
            raise Exception(f"RecordActionWidget found but securityOnDemand is not true")
        
        reeval_url = self._get_update_url_for_reeval(self._state)
        
        new_state = self._interactor.click_generic_element(
                                                            reeval_url, action_field_component, 
                                                            self.context, self.uuid, 
                                                            action_field_component["value"],
                                                            label=f"{locust_label}.securityOnDemand")
        
        if not new_state:
            raise Exception(f"No response returned when triggering security on demand for action field [index: {index}, testLabel: '{test_label}']")
        return self._reconcile_state(new_state)

    def click_menu_item_by_name(self, label: str, choice_name: str, is_test_label: bool = False,
                                locust_request_label: str = "") -> 'SailUiForm':
        """
        Clicks an item in a MenuLayout provided the primaryText of the chosen MenuItem
        ValueError is thrown if component found is NOT a MenuLayout,
        OR if the MenuLayout doesn't contain specified choice

        Args:
            label(str): Label of the MenuLayout
            choice_name(str): PrimaryText of the MenuItem to select
            is_test_label(bool): True if you are finding a MenuLayout by test label instead of a label, False o.w.

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:
            >>> form.click_menu_item_by_name("changeScopeMenu", "Scope 2", True, locust_request_label="Change Scope")
        """
        attribute_to_find = 'testLabel' if is_test_label else 'label'
        menu = find_component_by_attribute_in_dict(attribute_to_find, label, self._state)
        menu_item = find_component_by_attribute_and_type_in_dict(
            type="MenuItem", attribute="primaryText", value=choice_name, component_tree=menu)
        link_test_label = menu_item.get("link").get("testLabel")
        return self.click_link(label=link_test_label, is_test_label=True, locust_request_label=locust_request_label)

    def click_menu_item_by_choice_index(self, label: str, choice_index: int, is_test_label: bool = False,
                                        locust_request_label: str = "") -> 'SailUiForm':
        """
        Clicks an item in a MenuLayout provided the index of the chosen MenuItem
        ValueError is thrown if component found is NOT a MenuLayout,
        IndexError is thrown if the provided choice index is out of bounds for the available menu items

        Args:
            label(str): Label of the MenuLayout
            choice_index(str): Index of the MenuItem to select
            is_test_label(bool): True if you are finding a MenuLayout by test label instead of a label, False o.w.

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:
            >>> form.click_menu_item_by_choice_index("changeScopeMenu", 0, True, locust_request_label="Create Scope")
        """
        attribute_to_find = 'testLabel' if is_test_label else 'label'
        menu = find_component_by_attribute_in_dict(attribute_to_find, label, self._state)
        menu_item = find_component_by_index_in_dict(component_tree=menu, component_type="MenuItem", index=choice_index)
        link_test_label = menu_item.get("link").get("testLabel")
        return self.click_link(label=link_test_label, is_test_label=True, locust_request_label=locust_request_label)

    def get_dropdown_items(self, label: str, is_test_label: bool = False) -> List[str]:
        """
        Gets all dropdown items for the dropdown label provided on the form
        If no dropdown found, throws a NotFoundException
        If no element found, throws a ChoiceNotFoundException

        Args:
            label(str): Label of the dropdown
            is_test_label(bool): If you are interacting with a dropdown via a test label instead of a label, set this boolean to true.
                                 User filters on a record instance list use test labels.

        Returns (List): A list of all the choices in the dropdown

        Examples:

            >>> form.get_dropdown_items('MyDropdown')

        """
        attribute_to_find = 'testLabel' if is_test_label else 'label'
        try:
            component = find_component_by_attribute_and_type_in_dict(attribute_to_find, label, 'DropdownField',
                                                                     self._state)
        except ComponentNotFoundException:
            try:
                component = find_component_by_attribute_and_type_in_dict(attribute_to_find, label, 'DropdownWidget',
                                                                         self._state)
            except ComponentNotFoundException:
                raise ComponentNotFoundException(f"No components of type DropdownField or DropdownWidget with label '{label}' found on page")

        choices: list = component.get('choices')
        if choices is None or not isinstance(choices, list):
            raise InvalidComponentException(f"No choices found for component {label}, is the component a Dropdown?")
        return choices

    def select_dropdown_item(self, label: str, choice_label: str, locust_request_label: str = "", is_test_label: bool = False) -> 'SailUiForm':
        """
        Selects a dropdown item on the form
        If no dropdown found, throws a NotFoundException
        If no element found, throws a ChoiceNotFoundException

        Args:
            label(str): Label of the dropdown
            choice_label(str): Label of the dropdown item to select
            is_test_label(bool): If you are interacting with a dropdown via a test label instead of a label, set this boolean to true.
                                 User filters on a record instance list use test labels.

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.select_dropdown_item('MyDropdown', 'My First Choice')

        """
        attribute_to_find = 'testLabel' if is_test_label else 'label'
        try:
            component = find_component_by_attribute_and_type_in_dict(attribute_to_find, label, 'DropdownField',
                                                                     self._state)
        except ComponentNotFoundException:
            try:
                component = find_component_by_attribute_and_type_in_dict(attribute_to_find, label, 'DropdownWidget',
                                                                     self._state)
            except ComponentNotFoundException:
                raise ComponentNotFoundException(f"No components of type DropdownField or DropdownWidget with label '{label}' found on page")

        locust_label = locust_request_label or f'{self.breadcrumb}.Dropdown.SelectByLabel.{label}'
        reeval_url = self._get_update_url_for_reeval(self._state)
        exception_label = f"label {label}"

        new_state = self._interactor.construct_and_send_dropdown_update(
            component, choice_label, self.context, self._state, self.uuid, locust_label, exception_label, reeval_url, identifier=self._get_record_list_identifier())

        return self._reconcile_state(new_state)

    def select_dropdown_item_by_index(self, index: int, choice_label: str, locust_request_label: str = "") -> 'SailUiForm':
        """
        Selects a dropdown item on the form by index (1-based)
        If no dropdown found, throws a NotFoundException
        If no element found, throws a ChoiceNotFoundException

        Args:
            index(int): index(int): Index of the dropdown to select
            choice_label(str): Label of the dropdown item to select

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.select_dropdown_item_by_index(1, 'My First Choice')

        """
        component = find_component_by_index_in_dict(
            'DropdownField', index, self._state)
        locust_label = locust_request_label or f'{self.breadcrumb}.Dropdown.SelectByIndex.{index}'
        reeval_url = self._get_update_url_for_reeval(self._state)
        exception_label = f"index {index}"

        new_state = self._interactor.construct_and_send_dropdown_update(
            component, choice_label, self.context, self._state, self.uuid, locust_label, exception_label, reeval_url, identifier=self._get_record_list_identifier())

        return self._reconcile_state(new_state)

    def select_multi_dropdown_item(self, label: str, choice_label: List[str], locust_request_label: str = "", is_test_label: bool = False) -> 'SailUiForm':
        """
        Selects a multiple dropdown item on the form
        If no multiple dropdown found, throws a NotFoundException
        If no element found, throws a ChoiceNotFoundException

        Args:
            label(str): Label of the dropdown
            choice_label([str]): Label(s) of the multiple dropdown item to select
            is_test_label(bool): If you are interacting with a multiple dropdown via a test label instead of a label, set this boolean to true.
                                 User filters on a record instance list use test labels.

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.select_multi_dropdown_item('MyMultiDropdown', ['My First Choice','My Second Choice'])

        """
        attribute_to_find = 'testLabel' if is_test_label else 'label'
        try:
            component = find_component_by_attribute_and_type_in_dict(attribute_to_find, label, 'MultipleDropdownField',
                                                                     self._state)
        except ComponentNotFoundException:
            try:
                component = find_component_by_attribute_and_type_in_dict(attribute_to_find, label, 'MultipleDropdownWidget',
                                                                         self._state)
            except ComponentNotFoundException:
                raise ComponentNotFoundException(
                    f"No components of type MultipleDropdownField or MultipleDropdownWidget with label '{label}' found on page")

        locust_label = locust_request_label or f'{self.breadcrumb}.MultipleDropdown.SelectByLabel.{choice_label}'
        exception_label = f"label {label}"
        reeval_url = self._get_update_url_for_reeval(self._state)

        new_state = self._interactor.construct_and_send_multiple_dropdown_update(
            component, choice_label, self.context, self._state, self.uuid, locust_label, exception_label, reeval_url, identifier=self._get_record_list_identifier())

        return self._reconcile_state(new_state)

    def select_multi_dropdown_item_by_index(self, index: int, choice_label: List[str], locust_request_label: str = "") -> 'SailUiForm':
        """
        Selects a multiple dropdown item on the form by index (1-based)
        If no multiple dropdown found, throws a NotFoundException
        If no element found, throws a ChoiceNotFoundException

        Args:
            index(int): Index of the multiple dropdown to select
            choice_label([str]): Label(s) of the multiple dropdown item to select

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.select_multi_dropdown_item_by_index(2, ['My First Choice','My Second Choice'])

        """
        component = find_component_by_index_in_dict(
            'MultipleDropdownField', index, self._state)
        locust_label = locust_request_label or f'{self.breadcrumb}.MultipleDropdown.SelectByIndex.{choice_label}'
        exception_label = f"index {index}"
        reeval_url = self._get_update_url_for_reeval(self._state)

        new_state = self._interactor.construct_and_send_multiple_dropdown_update(
            component, choice_label, self.context, self._state, self.uuid, locust_label, exception_label, reeval_url, identifier=self._get_record_list_identifier())

        return self._reconcile_state(new_state)

    def _check_checkbox_by_attribute(self, attribute: str, value_for_attribute: str, indices: List[int], locust_request_label: str = "") -> 'SailUiForm':
        """
        Function that checks checkboxes.
        It finds checkboxes by the attribute and its value provided.

        Args:
            attribute(str): attribute to use to find the checkbox
            value_for_attribute(str): Value of the attribute used to find the checkbox
            indices(str): Indices of the checkbox to check. Pass None or empty to uncheck all

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm
        """
        component = find_component_by_attribute_and_type_in_dict(attribute, value_for_attribute, "CheckboxField", self._state)

        locust_label = locust_request_label or f'{self.breadcrumb}.CheckCheckboxByAttribute.{attribute}'
        reeval_url = self._get_update_url_for_reeval(self._state)
        new_state = self._interactor.select_checkbox_item(
            reeval_url, component, self.context, self.uuid, indices=indices, context_label=locust_label)
        if not new_state:
            raise Exception(f'''No response returned when trying to check checkbox which was found with attribute: '{attribute}'
                            and its value: '{value_for_attribute}' on the current page
                            ''')

        return self._reconcile_state(new_state)

    def check_checkbox_by_test_label(self, test_label: str, indices: List[int], locust_request_label: str = "") -> 'SailUiForm':
        """
        Checks a checkbox by its testLabel attribute
        Indices are positions to be checked

        Args:
            test_label(str): Value for the testLabel attribute of the checkbox
            indices(str): Indices of the checkbox to check. Pass None or empty to uncheck all

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.check_checkbox_by_test_label('myTestLabel', [1])  # checks the first item
            >>> form.check_checkbox_by_test_label('myTestLabel', None) # unchecks

        """
        if not test_label:
            raise Exception(f"No testLabel provided to select a checkbox")

        locust_label = locust_request_label or f'{self.breadcrumb}.CheckCheckboxByTestLabel.{test_label}'
        return self._check_checkbox_by_attribute('testLabel', test_label, indices, locust_request_label=locust_label)

    def check_checkbox_by_label(self, label: str, indices: List[int], locust_request_label: str = "") -> 'SailUiForm':
        """
        Checks a checkbox by its label
        Indices are positions to be checked

        Args:
            label(str): Value for label of the checkbox
            indices(str): Indices of the checkbox to check. Pass None or empty to uncheck all

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.check_checkbox_by_label('myLabel', [1])  # checks the first item
            >>> form.check_checkbox_by_label('myLabel', None) # unchecks

        """
        if not label:
            raise Exception(f"No label provided to select a checkbox")

        locust_label = locust_request_label or f'{self.breadcrumb}.CheckCheckboxByLabel.{label}'
        return self._check_checkbox_by_attribute('label', label, indices, locust_request_label=locust_label)

    def click_tab_by_label(self, tab_label: str, tab_group_test_label: str, locust_request_label: str = "") -> 'SailUiForm':
        """
        Selects a Tab by its label and its tab group's testLabel

        Args:
            tab_label(str): Label of the tab to select
            tab_group_test_label(str): Test Label of the tab group (tab is part of a tab group)
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

        """
        # find the TabButtonGroup, which is the  model we need for the SaveRequest
        reeval_url = self._get_update_url_for_reeval(self._state)

        tab_group_component = find_component_by_attribute_in_dict('testLabel', tab_group_test_label, self._state)
        new_state = self._interactor.click_selected_tab(
            reeval_url, tab_group_component, tab_label, self.context, self.uuid, locust_request_label)
        if not new_state:
            raise Exception(
                f'''No response returned when trying to click a tab with label: '{tab_label}'
                inside the TabButtonGroup component with testLabel: '{tab_group_test_label}'''
            )

        return self._reconcile_state(new_state, skipValidations=True)

    def upload_document_to_upload_field(self, label: str, file_path: str, index: int = 1, locust_request_label: str = "") -> 'SailUiForm':
        """
        Uploads a document to a named upload field
        There are two steps to this which can fail, one is the document upload, the other
        is finding the component and applying the update.

        Args:
            label(str): Label of the upload field
            file_path(str): File path to the document

        Keyword Args:
            index(int): Index of the field to fill if more than one match the attribute and attribute_value criteria (default: 1)
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.upload_document_to_upload_field('Upload File', "/usr/local/appian/File.zip")
            >>> form.upload_document_to_upload_field('Upload Properties', "/usr/local/appian/File.properties")

        """
        component = find_component_by_type_and_attribute_and_index_in_dict(
            component_tree=self._state,
            type="FileUploadWidget",
            attribute="label",
            value=label,
            index=index,
            raise_error=False
        )

        if not component:
            component = find_component_by_attribute_in_dict(
                'label', label, self._state)

        # Inner component can be the upload field
        if component.get('#t') != 'FileUploadWidget' and 'contents' in component:
            component = component['contents']

        # Check again to see if the wrong component
        if component.get('#t') != 'FileUploadWidget':
            if component.get('#t') == "MultipleFileUploadWidget":
                print("Selected FileUploadWidget is instead MultipleFileUploadWidget, continuing automatically")
                return self.upload_documents_to_multiple_file_upload_field(label, [file_path], index, locust_request_label)
            else:
                raise Exception(f"Provided component was not a FileUploadWidget, was instead of type '{component.get('#t')}'")

        if type(file_path) != str:
            raise Exception(f"Provided file_path {file_path} was not a string, was instead of type '{type(file_path)}'")

        is_encrypted = component.get("isEncrypted", False)

        if not os.path.exists(str(file_path)):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)
        validate_extensions = component.get("validateExtension", False)
        doc_info = self._interactor.upload_document_to_server(str(file_path), validate_extensions=validate_extensions, is_encrypted=is_encrypted)
        locust_label = locust_request_label or f"{self.breadcrumb}.FileUpload.{label}"
        new_state = self._interactor.upload_document_to_field(
            self.form_url, component, self.context, self.uuid, doc_info=doc_info, locust_label=locust_label)
        if not new_state:
            raise Exception(
                f"No response returned when trying to upload file to field '{label}'")
        return self._reconcile_state(new_state)

    def upload_documents_to_multiple_file_upload_field(self, label: str, file_paths: List[str], index: int = 1, locust_request_label: str = "") -> 'SailUiForm':
        """
        Uploads multiple documents to a named upload field
        There are two steps to this which can fail, one is the document uploads, the other
        is finding the component and applying the update.

        Args:
            label(str): Label of the upload field
            file_paths(list): List of document file paths in string form

        Keyword Args:
            index(int): Index of the field to fill if more than one match the attribute and attribute_value criteria (default: 1)
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Example:

            >>> form.multi_upload_document_to_upload_field('Upload Files', ["/usr/local/appian/File1.zip", "/usr/local/appian/File2.zip"])

        """
        component = find_component_by_type_and_attribute_and_index_in_dict(
            component_tree=self._state,
            type="MultipleFileUploadWidget",
            attribute="label",
            value=label,
            index=index,
            raise_error=False
        )

        if not component:
            component = find_component_by_attribute_in_dict(
                'label', label, self._state)

        # Inner component can be the upload field
        if component.get('#t') != 'MultipleFileUploadWidget' and 'contents' in component:
            component = component['contents']

        # Check again to see if the wrong component
        if component.get('#t') != 'MultipleFileUploadWidget':
            if component.get('#t') == "FileUploadWidget":
                print("Selected MultipleFileUploadWidget is instead FileUploadWidget, continuing automatically")
                return self.upload_document_to_upload_field(label, file_paths[0], index, locust_request_label)
            raise Exception(f"Provided component was not a MultipleFileUploadWidget, was instead of type '{component.get('#t')}'")

        is_encrypted = component.get("isEncrypted", False)

        doc_infos: List[Dict[str, Any]] = []
        validate_extensions = component.get("validateExtension", False)
        for file_path in file_paths:
            if not os.path.exists(file_path):
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)
            doc_infos.append(self._interactor.upload_document_to_server(file_path, validate_extensions=validate_extensions, is_encrypted=is_encrypted))
        locust_label = locust_request_label or f"{self.breadcrumb}.MultiFileUpload.{label}"
        new_state = self._interactor.upload_document_to_field(
            self.form_url, component, self.context, self.uuid, doc_info=doc_infos, locust_label=locust_label)
        if not new_state:
            raise Exception(
                f"No response returned when trying to upload file(s) to field '{label}'")
        return self._reconcile_state(new_state)

    def fill_date_field(self, label: str, date_input: datetime.date, index: int = 1, locust_request_label: str = "") -> 'SailUiForm':
        """
        Fills a date field with the specified date

        Args:
            label(str): Label of the date field
            date_input(date): Date used to fill the field

        Keyword Args:
            index(int): Index of the field to fill if more than one match the attribute and attribute_value criteria (default: 1)
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.fill_date_field('Today', datetime.date.today())
            >>> form.fill_date_field('Date of Birth', datetime.date(1992, 12, 30))

        """
        field_type = 'DatePickerField'
        date_field = find_component_by_type_and_attribute_and_index_in_dict(self._state, field_type, 'label', label, index)

        locust_label = locust_request_label or f'{self.breadcrumb}.FillDateField'
        reeval_url = self._get_update_url_for_reeval(self._state)

        new_state = self._interactor.update_date_field(
            reeval_url, date_field, date_input, self.context, self.uuid, locust_label=locust_label)
        if not new_state:
            raise Exception(f'''No response returned when trying to update: '{label}'
                            with its value: '{date_input}' on the current page
                            ''')

        return self._reconcile_state(new_state)

    def fill_datetime_field(self, label: str, datetime_input: datetime.datetime, index: int = 1, locust_request_label: str = "") -> 'SailUiForm':
        """
        Fills a datetime field with the specified datetime

        NOTE: this does one api call for both the date and time, whereas filling the elements on screen requires
        two separate evaluations, one to fill the date field and one to fill the time field. This is the
        way the request would look if one of the fields were already filled.

        Args:
            label(str): Label of the datetime field
            datetime_input(date): Date time used to fill the field

        Keyword Args:
            index(int): Index of the field to fill if more than one match the attribute and attribute_value criteria (default: 1)
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.fill_datetime_field('Now', datetime.datetime.now())
            >>> form.fill_datetime_field('Date and Time of Birth', datetime.datetime(1992, 12, 30, 12, 30, 5))

        """
        field_type = 'DateTimePickerField'
        datetime_field = find_component_by_type_and_attribute_and_index_in_dict(self._state, field_type, 'label', label, index)

        locust_label = locust_request_label or f'{self.breadcrumb}.FillDateTimeField'
        reeval_url = self._get_update_url_for_reeval(self._state)

        new_state = self._interactor.update_datetime_field(
            reeval_url, datetime_field, datetime_input, self.context, self.uuid, locust_label=locust_label)
        if not new_state:
            raise Exception(f'''No response returned when trying to update: '{label}'
                            with its value: '{datetime_input}' on the current page
                            ''')

        return self._reconcile_state(new_state)

    def select_rows_in_grid(self, rows: List[int], label: Optional[str] = None, index: Optional[int] = None, append_to_existing_selected: bool = False, locust_request_label: str = "") -> 'SailUiForm':
        """
        Selects rows in a grid
        Either a label or an index is required, indices are useful if there is no title for the grid

        Args:
            rows(List[int]): The rows to select
            label(str): Label of the grid
            index(int): Index of the grid
            append_to_existing_selected(bool): Flag to control appending row selections

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.select_rows_in_grid(rows=[1], label='my nice grid')
        """
        grid = self.grid_interactor.find_grid_by_label_or_index(self._state, label=label, index=index)
        grid_label = self.grid_interactor.format_grid_display_label(grid)

        new_grid_save = self.grid_interactor.select_rows(grid, rows, append_to_existing_selected)
        context_label = locust_request_label or f"{self.breadcrumb}.Grid.SelectRows.{grid_label}"

        reeval_url = self._get_update_url_for_reeval(self._state)
        new_state = self._interactor.update_grid_from_sail_form(reeval_url, grid, new_grid_save,
                                                                self.context, self.uuid, context_label=context_label)
        return self._reconcile_state(new_state, skipValidations=True)

    def move_to_end_of_paging_grid(self, label: Optional[str] = None, index: Optional[int] = None, locust_request_label: str = "") -> 'SailUiForm':
        """
        Moves to the end of a paging grid, if possible
        Either a label or an index is required, indices are useful if there is no title for the grid

        Args:
            label(str): Label of the grid
            index(int): Index of the grid

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.move_to_end_of_paging_grid(label='my nice grid')
        """
        grid = self.grid_interactor.find_grid_by_label_or_index(self._state, label=label, index=index)
        grid_label = self.grid_interactor.format_grid_display_label(grid)

        new_grid_save = self.grid_interactor.move_to_last_page(grid)
        context_label = locust_request_label or f"{self.breadcrumb}.Grid.MoveToEnd.{grid_label}"

        reeval_url = self._get_update_url_for_reeval(self._state)
        new_state = self._interactor.update_grid_from_sail_form(reeval_url, grid, new_grid_save,
                                                                self.context, self.uuid, context_label=context_label)
        return self._reconcile_state(new_state, skipValidations=True)

    def move_to_beginning_of_paging_grid(self, label: Optional[str] = None, index: Optional[int] = None, locust_request_label: str = "") -> 'SailUiForm':
        """
        Moves to the beginning of a paging grid, if possible
        Either a label or an index is required, indices are useful if there is no title for the grid

        Args:
            label(str): Label of the grid
            index(int): Index of the grid

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.move_to_beginning_of_paging_grid(label='my nice grid')
        """
        grid = self.grid_interactor.find_grid_by_label_or_index(self._state, label=label, index=index)
        grid_label = self.grid_interactor.format_grid_display_label(grid)

        new_grid_save = self.grid_interactor.move_to_first_page(grid)
        context_label = locust_request_label or f"{self.breadcrumb}.Grid.MoveToBeginning.{grid_label}"

        reeval_url = self._get_update_url_for_reeval(self._state)
        new_state = self._interactor.update_grid_from_sail_form(reeval_url, grid, new_grid_save,
                                                                self.context, self.uuid, context_label=context_label)
        return self._reconcile_state(new_state, skipValidations=True)

    def move_to_left_in_paging_grid(self, label: Optional[str] = None, index: Optional[int] = None, locust_request_label: str = "") -> 'SailUiForm':
        """
        Moves to the left in a paging grid, if possible
        It might require getting the state of the grid if you've moved to the end/ previous part of the grid
        Either a label or an index is required, indices are useful if there is no title for the grid

        Args:
            label(str): Label of the grid
            index(int): Index of the grid

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.move_to_left_in_paging_grid(label='my nice grid')
        """
        grid = self.grid_interactor.find_grid_by_label_or_index(self._state, label=label, index=index)
        grid_label = self.grid_interactor.format_grid_display_label(grid)

        new_grid_save = self.grid_interactor.move_to_the_left(grid)
        context_label = locust_request_label or f"{self.breadcrumb}.Grid.MoveLeft.{grid_label}"

        reeval_url = self._get_update_url_for_reeval(self._state)
        new_state = self._interactor.update_grid_from_sail_form(reeval_url, grid, new_grid_save,
                                                                self.context, self.uuid, context_label=context_label)
        return self._reconcile_state(new_state, skipValidations=True)

    def move_to_right_in_paging_grid(self, label: Optional[str] = None, index: Optional[int] = None, locust_request_label: str = "") -> 'SailUiForm':
        """
        Moves to the right in a paging grid, if possible
        It might require getting the state of the grid if you've moved within the grid
        Either a label or an index is required, indices are useful if there is no title for the grid

        Args:
            label(str): Label of the grid
            index(int): Index of the grid

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.move_to_right_in_paging_grid(index=0) # move to right in first grid on the page
        """
        grid = self.grid_interactor.find_grid_by_label_or_index(self._state, label=label, index=index)
        grid_label = self.grid_interactor.format_grid_display_label(grid)

        new_grid_save = self.grid_interactor.move_to_the_right(grid)
        context_label = locust_request_label or f"{self.breadcrumb}.Grid.MoveRight.{grid_label}"

        reeval_url = self._get_update_url_for_reeval(self._state)
        new_state = self._interactor.update_grid_from_sail_form(reeval_url, grid, new_grid_save,
                                                                self.context, self.uuid, context_label=context_label)
        return self._reconcile_state(new_state, skipValidations=True)

    def sort_paging_grid(self, label: Optional[str] = None, index: Optional[int] = None, field_name: str = "", ascending: bool = False, locust_request_label: str = "") -> 'SailUiForm':
        """
        Sorts a paging grid by the field name, which is not necessarily the same as the label of the column
        And might require inspecting the JSON to determine what the sort field is

        Sorts by ascending = False by default, override to set it to True

        Either a label or an index is required, indices are useful if there is no title for the grid

        Args:
            label(str): Label of the grid
            index(int): Index of the grid
            field_name(str): Field to sort on (not necessarily the same as the displayed one)
            ascending(bool): Whether to sort ascending, default is false

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.sort_paging_grid(index=0,field_name='Total',ascending=True)
        """
        if not field_name:
            raise Exception("Field to sort cannot be blank when sorting a grid")
        grid = self.grid_interactor.find_grid_by_label_or_index(self._state, label=label, index=index)
        grid_label = self.grid_interactor.format_grid_display_label(grid)

        new_grid_save = self.grid_interactor.sort_grid(field_name=field_name, paging_grid=grid, ascending=ascending)
        context_label = locust_request_label or f"{self.breadcrumb}.Grid.Sort.{grid_label}.{field_name}"

        reeval_url = self._get_update_url_for_reeval(self._state)
        new_state = self._interactor.update_grid_from_sail_form(reeval_url, grid, new_grid_save,
                                                                self.context, self.uuid, context_label=context_label)
        return self._reconcile_state(new_state, skipValidations=True)

    def click_grid_rich_text_link(self, column_name: str, row_index: int, grid_label: Optional[str] = None, grid_index: Optional[int] = None, locust_request_label: str = "") -> 'SailUiForm':
        """
        Click on a link in a grid with RichText values

        Either a label or an index is required, indices are useful if there is no title for the grid

        Args:
            column_name (str): The name of the column the link is in
            row_index (int): The row in the column to click on, 0 indexed
            grid_label (str): The label of the grid, if index is not supplied
            grid_index (str): the index of the grid, if label is not supplied
            locust_request_label (str, optional): The label locust should associate this request with

        Returns (SailUiForm): The latest state of the UiForm

        """
        grid = self.grid_interactor.find_grid_by_label_or_index(self._state, label=grid_label, index=grid_index)

        if not grid_label:
            grid_label = self.grid_interactor.format_grid_display_label(grid)
        locust_request_label = locust_request_label or f"{self.breadcrumb}.Grid.Click.{grid_label}.{column_name}.{row_index}"

        link_component = self.grid_interactor.find_rich_text_grid_link_component(grid=grid, column_name=column_name, row_index=row_index)
        if not link_component:
            raise Exception(f"Column with name {column_name} not found in grid with identifier {grid_label or grid_index}")

        new_state = self._dispatch_click(component=link_component, locust_label=locust_request_label)
        return self._reconcile_state(new_state, skipValidations=True)

    def click_grid_rich_text_record_link(self, column_name: str, row_index: int, grid_label: Optional[str] = None,
                                         grid_index: Optional[int] = None, locust_request_label: str = "") -> 'RecordInstanceUiForm':
        """
        Click on a Record link in a grid with RichText values

        Either a label or an index is required, indices are useful if there is no title for the grid

        NOTE: This method returns a NEW RecordInstanceUiForm object, so you must save its return value into a new variable, like so:

            >>> record_uiform = other_uiform.click_grid_rich_text_record_link(...)

        Args:
            column_name (str): The name of the column the link is in
            row_index (int): The row in the column to click on, 0 indexed
            grid_label (str): The label of the grid, if index is not supplied
            grid_index (str): the index of the grid, if label is not supplied
            locust_request_label (str, optional): The label locust should associate this request with

        Returns (SailUiForm): The latest state of the UiForm

        """
        grid = self.grid_interactor.find_grid_by_label_or_index(self._state, label=grid_label, index=grid_index)

        if not grid_label:
            grid_label = self.grid_interactor.format_grid_display_label(grid)
        locust_request_label = locust_request_label or f"{self.breadcrumb}.Grid.Click.{grid_label}.{column_name}.{row_index}"

        link_component = self.grid_interactor.find_rich_text_grid_link_component(grid=grid, column_name=column_name,
                                                                                 row_index=row_index)
        if not link_component:
            raise Exception(f"Column with name {column_name} not found in grid with identifier {grid_label or grid_index}")

        new_state = self._interactor.click_record_link(self.form_url, link_component, self.context, self.uuid,
                                                       locust_label=locust_request_label)

        from .record_uiform import RecordInstanceUiForm
        return RecordInstanceUiForm(self._interactor, new_state)

    def click_grid_plaintext_link(self, column_name: str, row_index: int, grid_label: Optional[str] = None,
                                  grid_index: Optional[int] = None, locust_request_label: str = "") -> 'SailUiForm':
        """
        Click on a link in a grid with plaintext values

        Either a label or an index is required, indices are useful if there is no title for the grid

        Args:
            column_name (str): The name of the column the link is in
            row_index (int): The row in the column to click on, 0 indexed
            grid_label (str): The label of the grid, if index is not supplied
            grid_index (str): the index of the grid, if label is not supplied
            locust_request_label (str, optional): The label locust should associate this request with

        Returns (SailUiForm): The latest state of the UiForm

        """
        grid = self.grid_interactor.find_grid_by_label_or_index(self._state, label=grid_label, index=grid_index)

        if not grid_label:
            grid_label = self.grid_interactor.format_grid_display_label(grid)
        locust_request_label = locust_request_label or f"{self.breadcrumb}.Grid.Click.{grid_label}.{column_name}.{row_index}"

        link_component = self.grid_interactor.find_plaintext_grid_link_component(grid=grid, column_name=column_name, row_index=row_index)
        if not link_component:
            raise Exception(f"Column with name {column_name} not found in grid with identifier {grid_label or grid_index}")

        new_state = self._dispatch_click(component=link_component, locust_label=locust_request_label)
        return self._reconcile_state(new_state, skipValidations=True)

    def click_grid_plaintext_record_link(self, column_name: str, row_index: int, grid_label: Optional[str] = None,
                                         grid_index: Optional[int] = None, locust_request_label: str = "") -> 'RecordInstanceUiForm':
        """
        Click on a Record link in a grid with plaintext values

        Either a label or an index is required, indices are useful if there is no title for the grid

        NOTE: This method returns a NEW RecordInstanceUiForm object, so you must save its return value into a new variable, like so:

            >>> record_uiform = other_uiform.click_grid_plaintext_record_link(...)

        Args:
            column_name (str): The name of the column the link is in
            row_index (int): The row in the column to click on, 0 indexed
            grid_label (str): The label of the grid, if index is not supplied
            grid_index (str): the index of the grid, if label is not supplied
            locust_request_label (str, optional): The label locust should associate this request with

        Returns (SailUiForm): The latest state of the UiForm

        """
        grid = self.grid_interactor.find_grid_by_label_or_index(self._state, label=grid_label, index=grid_index)

        if not grid_label:
            grid_label = self.grid_interactor.format_grid_display_label(grid)
        locust_request_label = locust_request_label or f"{self.breadcrumb}.Grid.Click.{grid_label}.{column_name}.{row_index}"

        link_component = self.grid_interactor.find_plaintext_grid_link_component(grid=grid, column_name=column_name,
                                                                                 row_index=row_index)
        if not link_component:
            raise Exception(f"Column with name {column_name} not found in grid with identifier {grid_label or grid_index}")

        new_state = self._interactor.click_record_link(self.form_url, link_component, self.context, self.uuid,
                                                       locust_label=locust_request_label)

        from .record_uiform import RecordInstanceUiForm
        return RecordInstanceUiForm(self._interactor, new_state)

    def select_card_choice_field_by_label(self, label: str, index: int, locust_request_label: str = "") -> 'SailUiForm':
        """
        Select a card by its label
        Index is position to be selected

        Args:
            label(str): Label of the card choice field
            index(int): Index of the card to select

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.select_card_choice_field_by_label('myLabel', 1)  # selects the first item

        """
        context_label = locust_request_label or f"{self.breadcrumb}.CardChoice.SelectByLabel.{label}"
        label = "cardChoiceField-" + label
        component = find_component_by_attribute_in_dict(
            'testLabel', label, self._state)

        reeval_url = self._get_update_url_for_reeval(self._state)
        new_value = {
            "#t": "Variant?list",
            "#v": [component["identifiers"][index - 1]]
        }
        new_state = self._interactor.click_generic_element(
            reeval_url, component, self.context, self.uuid, new_value=new_value, label=context_label)
        if not new_state:
            raise Exception(
                f"No response returned when trying to select card choice field with testLabel '{label}'")
        return self._reconcile_state(new_state)

    def select_radio_button_by_test_label(self, test_label: str, index: int, locust_request_label: str = "") -> 'SailUiForm':
        """
        Selects a radio button by its test label
        Index is position to be selected

        Args:
            test_label(str): Label of the radio button field
            index(int): Index of the radio button to select

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.select_radio_button_by_test_label('myTestLabel', 1)  # selects the first item

        """
        component = find_component_by_attribute_and_type_in_dict(
            'testLabel', test_label, 'RadioButtonField', self._state)

        reeval_url = self._get_update_url_for_reeval(self._state)
        context_label = locust_request_label or f"{self.breadcrumb}.RadioButton.SelectByTestLabel.{test_label}"
        new_state = self._interactor.select_radio_button(
            reeval_url, component, self.context, self.uuid, index=index, context_label=context_label)
        if not new_state:
            raise Exception(
                f"No response returned when trying to select radio button with testLabel '{test_label}'")
        return self._reconcile_state(new_state)

    def select_radio_button_by_label(self, label: str, index: int, locust_request_label: str = "") -> 'SailUiForm':
        """
        Selects a radio button by its label
        Index is position to be selected

        Args:
            label(str): Label of the radio button field
            index(int): Index of the radio button to select

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.select_radio_button_by_label('myLabel', 1)  # selects the first item

        """
        component = find_component_by_attribute_and_type_in_dict(
            'label', label, 'RadioButtonField', self._state)

        reeval_url = self._get_update_url_for_reeval(self._state)
        context_label = locust_request_label or f"{self.breadcrumb}.RadioButton.SelectByLabel.{label}"
        new_state = self._interactor.select_radio_button(
            reeval_url, component, self.context, self.uuid, index=index, context_label=context_label)
        if not new_state:
            raise Exception(
                f"No response returned when trying to select radio button with label '{label}'")
        return self._reconcile_state(new_state)

    def select_nav_card_by_index(self, nav_group_label: str, index: int, is_test_label: bool = False, locust_request_label: str = "") -> 'SailUiForm':
        """
        Selects an element of a navigation card group by its index

        Args:
            nav_group_label(str): Label of the navigation card group
            index(int): Index of the element starting at 0

        Keyword Args:
            is_test_label (bool): If this label is a test label
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm
        """
        attribute_to_find = 'testLabel' if is_test_label else 'label'
        component = find_component_by_attribute_and_index_in_dict(
            attribute_to_find, nav_group_label, index, self._state)

        reeval_url = self._get_update_url_for_reeval(self._state)
        context_label = locust_request_label or f"{self.breadcrumb}.NavCard.{nav_group_label}"
        new_state = self._interactor.select_radio_button(
            reeval_url, component, self.context, self.uuid, index=index, context_label=context_label)
        if not new_state:
            raise Exception(
                f"No response returned when trying to select nav card with label '{nav_group_label}' and index '{index}'")
        return self._reconcile_state(new_state)

    def select_radio_button_by_index(self, field_index: int, index: int, locust_request_label: str = "") -> 'SailUiForm':
        """
        Selects a radio button by its field index
        Index is position to be selected

        Args:
            field_index(int): Index of the radio button field on the page
            index(int): Index of the radio button to select

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.select_radio_button_by_index(1, 1)  # selects the first item in the first radio button field

        """
        component = find_component_by_index_in_dict(
            'RadioButtonField', field_index, self._state)

        reeval_url = self._get_update_url_for_reeval(self._state)
        context_label = locust_request_label or f"{self.breadcrumb}.RadioButton.SelectByIndex.{index}"
        new_state = self._interactor.select_radio_button(
            reeval_url, component, self.context, self.uuid, index=index, context_label=context_label)
        if not new_state:
            raise Exception(
                f"No response returned when trying to select radio button with index '{field_index}'")
        return self._reconcile_state(new_state)

    def go_to_next_record_grid_page(self, locust_request_label: str = "") -> 'SailUiForm':
        context_label = locust_request_label or f"{self.breadcrumb}.NextPage"
        headers = self._interactor.setup_request_headers()
        headers["Accept"] = "application/vnd.appian.tv.ui+json"
        reeval_url = self._get_update_url_for_reeval(self._state)
        label = 'NEXT'
        if not _is_grid(self._state):
            raise Exception("Not a grid record list")
        component = find_component_by_attribute_in_dict(
            'label', label, self._state)
        new_state = self._interactor.interact_with_record_grid(
            post_url=reeval_url, grid_component=component, context=self.context, uuid=self.uuid,
            identifier=self._get_record_list_identifier(), context_label=context_label
        )
        if not new_state:
            raise Exception(
                f"No response returned when navigating to next page on record list '{reeval_url}'")
        return self._reconcile_state(new_state, skipValidations=True)

    def assert_no_validations_present(self) -> 'SailUiForm':
        """
        Raises an exception if there are validations present on the form, otherwise, returns the form as is

        Returns (SailUiForm): Form as it was when validations were asserted
        """
        validations: list = extract_all_by_label(self._state, "validations")
        validation_present = False
        for validation in validations:
            if validation:
                log.error(f'Validations were found in the form {self.breadcrumb}, validation: {validation}')
                validation_present = True
        if validation_present:
            raise IgnoredValidationException(self.breadcrumb)
        return self

    def refresh_after_record_action(self, label: str, is_test_label: bool = False, locust_request_label: str = "") -> 'SailUiForm':
        """
        Refreshes a form after the completion of a record action.

        Args:
            label(str): Label of the record action that has just been completed
            is_test_label(bool): If you are referencing a record action via a test label instead of a label, set this boolean to true

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> initial_form = copy(form)
            >>> form.click('Request upgrade')
            >>> ...
            >>> form.click('Submit')
            >>> initial_form.refresh_after_record_action('Request upgrade')

        """

        attribute_to_find = 'testLabel' if is_test_label else 'label'

        record_action_component = find_component_by_attribute_in_dict(attribute_to_find, label, self._state)

        # testLabel is one level up from label for record actions, so if using testLabel we need to pull the record action component out
        if is_test_label:
            record_action_component = record_action_component["recordAction"]

        record_action_trigger_component = find_component_by_attribute_in_dict(
            '_actionName', 'sail:record-action-trigger', self._state)

        reeval_url = self._get_update_url_for_reeval(self._state)
        locust_label = locust_request_label or f"{self.breadcrumb}.RefreshAfterRecordAction.{label}"
        new_state = self._interactor.refresh_after_record_action(
            reeval_url, record_action_component, record_action_trigger_component, self.context, self.uuid, label=locust_label)

        if not new_state:
            raise Exception(f"No response returned when trying to refresh after record action '{label}'")

        return self._reconcile_state(new_state, skipValidations=True)

    def click_record_search_button_by_index(self, index: int = 1, locust_request_label: str = "") -> 'SailUiForm':
        """
        Clicks the Search button of a record grid.

        Args:
            index(int): Index of the record search button on the form

        Keyword Args:
            locust_request_label(str): Label used to identify the request for locust statistics

        Returns (SailUiForm): The latest state of the UiForm

        Examples:

            >>> form.click_record_search_button_by_index(1)

        """
        component = find_component_by_index_in_dict("SearchBoxWidget", index, self._state)

        reeval_url = self._get_update_url_for_reeval(self._state)
        locust_label = locust_request_label or f"{self.breadcrumb}.ClickRecordSearchButtonByIndex.{index}"
        new_state = self._interactor.click_record_search_button(
            reeval_url, component, self.context, self.uuid, label=locust_label)

        if not new_state:
            raise Exception(f"No response returned when trying to click record search button at index '{index}'")

        return self._reconcile_state(new_state, skipValidations=True)
    
    def check_if_component_disabled(self, label: str, is_test_label: bool = False) -> bool:
        """
        Checks if a component is disabled

        Args:
            label(str): Label of the component
            is_test_label(bool): If you are referencing a component via a test label instead of a label, set this boolean to true
            
        Returns (bool): True or False reflecting if disabled

        Examples:

            >>> form.check_if_component_disabled('myLabel')
        """
        attribute_to_find = 'testLabel' if is_test_label else 'label'
        component = find_component_by_attribute_in_dict(attribute=attribute_to_find, value=label, component_tree=self._state)
        return component.get("disabled", False)

    def _reconcile_state(self, new_state: dict, skipValidations: bool = False) -> 'SailUiForm':
        self._interactor.datatype_cache.cache(new_state)
        self._state = self.reconciler.reconcile_ui(self._state, new_state)
        self.form_url = self._get_update_url_for_reeval(self._state)
        self.uuid = self._state.get(KEY_UUID) or self.uuid
        self.context = self._state.get(KEY_CONTEXT) or self.context
        if not skipValidations:
            self.assert_no_validations_present()
        return self

    def _get_update_url_for_reeval(self, state: Dict[str, Any]) -> str:
        """
        This function looks at the links object in a SAIL response
        and finds the URL for "rel"="update", which is then used to do other
        interactions on the form.
        """

        # If state is None (usually for tests) we return empty string for re-eval url
        if not state:
            return ""
        reeval_url = self.form_url
        if "links" not in state:
            return reeval_url
        # get the re-eval URI from links object of the response (new_state)
        list_of_links = state["links"]
        for link_object in list_of_links:
            if link_object.get("rel") == "update":
                reeval_url = urlparse(link_object.get("href", "")).path
                break
        return reeval_url

    def _get_record_list_identifier(self) -> Optional[Dict[str, Any]]:
        # Base SailUiForm will not have a record_list identifier, return None
        return None
