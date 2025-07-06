from typing import Any, Dict, Optional

from .._design import _Design
from .._interactor import _Interactor
from ..uiform import SailUiForm

from ..utilities.helper import (find_component_by_attribute_in_dict)


class DesignObjectUiForm(SailUiForm):

    def __init__(self, interactor: _Interactor, state: Dict[str, Any], breadcrumb: str = "DesignObjectUi"):
        super().__init__(interactor, state, breadcrumb)
        self.__design = _Design(interactor)

    def edit_expression_rule(self, value: str, locust_request_label: str = "", label: str = "",
                             is_test_label: bool = False) -> 'DesignObjectUiForm':
        test_label = label if is_test_label else 'expression-editor'

        component = find_component_by_attribute_in_dict(
            attribute='testLabel', value=test_label, component_tree=self._state)
        locust_label = locust_request_label or f'{self.breadcrumb}.ExpressionEditor.update'
        reeval_url = self._get_update_url_for_reeval(self._state)

        new_state = self._interactor.send_expression_editor_update(
            reeval_url, value, component, self.context, self.uuid, locust_label)

        self._reconcile_state(new_state, skipValidations=True)
        return self

    def launch_query_editor(self) -> 'DesignObjectUiForm':
        """
        Calls the post operation to click on the LaunchVQD button in the toolbar for the ExpressionEditorWidget.
        This will launch the query editor with the expression currently in the expression editor.

        Returns (DesignObjectUiForm): UiForm updated with state representing launched query editor

        """
        query_editor_json = self.__design.click_expression_editor_toolbar_button("LaunchVQD", self.form_url, self._state, self.context, self.uuid)
        self._reconcile_state(query_editor_json, skipValidations=True)
        return self

    # existing __init__ and other methods...

    def click_record_type_application_navigation_tab(
            self,
            navigation_tab_label: str,
            locust_request_label: Optional[str] = None
    ) -> 'DesignObjectUiForm':
        """
        Interacts with an ApplicationNavigationLayout component. This interaction involves clicking the Section Items
        in the navigation sidebar tab of Record Type e.g. Actions, Views, etc.

        Args:
            navigation_tab_label (str): The label or identifier for the navigation component.

        Keyword Args:
            locust_request_label (str): Label used to identify the request for locust statistics.

        Returns (DesignObjectUiForm): The latest state of the UiForm.

        Examples:
            >>> form.click_record_type_application_navigation_tab(navigation_page_label="Actions")
        """
        application_navigation_tab_test_label = "rtdNavigation"
        component = find_component_by_attribute_in_dict(attribute="testLabel",
                                                        value=application_navigation_tab_test_label,
                                                        component_tree=self._state)

        # Initialize a dict to store section items with their config keys
        section_items_with_config_keys = {}

        # Loop through the component to find SectionItems and store them in the dict
        for content in component.get("contents", []):
            for item in content.get("contents", []):
                if item.get("testLabel", "").endswith("SectionItem"):
                    section_items_with_config_keys[item["label"]] = item["configKey"]

        # Find the configKey for the provided navigation_label
        selected_config_key = section_items_with_config_keys.get(navigation_tab_label)

        if not selected_config_key:
            raise Exception(f"Navigation label '{navigation_tab_label}' not found.")

        # Craft the new_value dict
        new_value = {"#t": "Text", "#v": f"{selected_config_key}"}

        # Perform the click operation
        new_state = self._interactor.click_generic_element(
            post_url=self.form_url,
            component=component,
            context=self.context,
            uuid=self.uuid,
            new_value=new_value,
            label=locust_request_label or f"{self.breadcrumb}.ClickRecordTypeApplicationNavigationTab.{navigation_tab_label}"
        )

        # Reconcile and return the updated state
        self._reconcile_state(new_state)
        return self
