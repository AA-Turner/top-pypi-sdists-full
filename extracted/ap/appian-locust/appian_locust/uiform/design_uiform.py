from typing import Any, Dict, Optional

from ..utilities import logger
from .._design import _Design, get_available_design_objects
from .._interactor import _Interactor
from ..objects import Application, DesignObjectType
from ..uiform import ApplicationUiForm, SailUiForm
from ..objects import DesignObject
from ..utilities.helper import find_component_by_attribute_in_dict

log = logger.getLogger(__name__)


class DesignUiForm(SailUiForm):

    def __init__(self, interactor: _Interactor, state: Dict[str, Any], breadcrumb: str = "DesignUi"):
        super().__init__(interactor, state, breadcrumb)
        self.__design = _Design(interactor)

    def click_application(self, application_name: str, locust_request_label: Optional[str] = None) -> 'ApplicationUiForm':
        """
        Click on an application in the /design application grid. Must be on the current page to be clicked.

        Args:
            application_name(str): The name of the application to click on
            locust_request_label (str, optional): label to be used within locust

        Returns (ApplicationUiForm): The latest state of the UiForm, representing the application clicked on
        """
        grid_component = self.__design.find_design_grid(self._state)
        column = find_component_by_attribute_in_dict('label', "Name", grid_component["columns"], throw_attribute_exception=True)
        for index in range(len(column["data"])):
            if column["data"][index] == application_name:
                return ApplicationUiForm(self._interactor, self._dispatch_click(column["links"][index], locust_request_label or "DesignGrid"), f"Application.{ application_name }.Ui")
        raise Exception(f"No Application with name { application_name } found in /design grid")

    def create_application(self, application_name: str) -> 'ApplicationUiForm':
        """
        Creates an application and returns a form within representing the app contents

        Returns: The SAIL UI Form

        """
        app_form = self.__design.create_object(self, link_name='New Application', object_name=application_name)
        app_form.breadcrumb = f"Design.SelectedApplicationByName.{application_name}"
        return ApplicationUiForm(self._interactor, self._state, self.breadcrumb)

    def import_application(self, app_file_path: str, customization_file_path: Optional[str] = None, inspect_and_import: bool = False) -> None:
        """
        Import an application into the Appian instance.
        Args:
            app_file_path: Local path to the application zip file
            customization_file_path: Local path to customization file
            inspect_and_import: Set to true if Appian Locust should "Inspect" before importing

        Returns: None

        """
        # Open the import modal
        self.click_button("Import")

        # Upload Package
        self.upload_document_to_upload_field("Package (ZIP)", app_file_path)

        # Optionally upload import cust file
        if customization_file_path:
            log.info("Adding customization file")
            self.check_checkbox_by_test_label("propertiesCheckboxField", [1])
            self.upload_document_to_upload_field("Import Customization File (PROPERTIES)", customization_file_path)

        if inspect_and_import:
            log.info("First inspecting and then importing the package")
            self.click_button("Inspect").click_button("Import Package")
        else:
            log.info("Simply importing the package")
            self.click_button("Import")

        self.click_button("Close")

    def search_applications(self, search_str: str, locust_label: Optional[str] = None) -> 'DesignUiForm':
        """
        Search the application list in /design, must be on page with application list
        Args:
            search_str (str): The string to search
            locust_label (str): Label to associate request with

        Returns (DesignUiForm): A UiForm with updated state after the search is complete

        """
        new_state = self.__design.search_design_grid(
            search_str, self._get_update_url_for_reeval(self._state), self._state, self.context, self.uuid,
            locust_label if locust_label else f"{self.breadcrumb}.ApplicationSearch"
        )
        self._reconcile_state(new_state, skipValidations=True)
        return self

    def search_objects(self, search_str: str, locust_label: Optional[str] = None) -> 'DesignUiForm':
        """
            Search the design object list in /design, must be on page with design object list
            Args:
                search_str (str): The string to search
                locust_label (str): Label to associate request with

            Returns (DesignUiForm): A UiForm with updated state after the search is complete

        """
        new_state = self.__design.search_design_grid(
            search_str, self._get_update_url_for_reeval(self._state), self._state, self.context, self.uuid,
            locust_label if locust_label else f"{self.breadcrumb}.ObjectSearch"
        )
        self._reconcile_state(new_state, skipValidations=True)
        return self

    def get_available_applications(self) -> Dict[str, Application]:
        """
            Retrieve all available applications in /design. Must be on page with application list

            Returns (dict): Dictionary mapping application names to Application
        """
        grid_field = self.__design.find_design_grid(self._state)
        applications = {}
        name_column = grid_field["columns"][0]
        num_applications = len(name_column["data"])
        for idx in range(num_applications):
            app_name = name_column["data"][idx]
            href_split = name_column["links"][idx]["href"].split("/")
            applications[app_name] = Application(app_name, href_split[len(href_split) - 1])
        return applications

    def get_available_design_objects(self) -> Dict[str, DesignObject]:
        """
            Retrieve all available design objects in the application. Must be on page with design object list

            Returns (dict): Dictionary mapping design object names to DesignObject
        """
        return get_available_design_objects(self._state)

    def filter_design_objects(self, design_object_types: list[DesignObjectType]) -> 'DesignUiForm':
        """
        Filter the design object list in /design, must be on page with design object list
        Args:
            design_object_types (DesignObjectType): List of the types of objects you wish to filter on

        Returns (DesignUiForm): DesignUiForm with filtered list of design objects

        """
        indices = self.__design.find_design_object_type_indices(current_state=self._state,
                                                                design_object_types=[design_object_type.value for design_object_type in design_object_types])
        self.check_checkbox_by_test_label(test_label="object-type-checkbox", indices=indices)
        return self