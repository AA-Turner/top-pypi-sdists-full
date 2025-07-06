from typing import Any, Dict, Optional

from .InterfaceDesignerUiForm import InterfaceDesignerUiForm
from .._design import _Design, get_available_design_objects, validate_design_object_access_method
from .._rdo_interactor import _RDOInteractor
from .._interactor import _Interactor
from ..uiform import AISkillUiForm, DesignObjectUiForm, SailUiForm
from ..objects import DesignObject, DesignObjectType, AISkillObjectType

_RDO_TYPE_TO_APPLICATION_METHOD = {
    "aiSkill": "click_ai_skill"
}


class ApplicationUiForm(SailUiForm):

    def __init__(self, interactor: _Interactor, state: Dict[str, Any], breadcrumb: str = "ApplicationUi"):
        super().__init__(interactor, state, breadcrumb)
        self.__design = _Design(interactor)

    def __get_design_object_info(self, design_object_name: str, locust_request_label: Optional[str] = None) -> tuple[str, Dict[str, Any]]:
        opaque_id = self.__design.find_design_object_opaque_id_in_grid(design_object_name, self._state)
        locust_request_label = locust_request_label or f"Application.Object.{opaque_id[:10]}.Click"
        design_object_json = self.__design.fetch_design_object_json(opaque_id, locust_request_label=locust_request_label)
        validate_design_object_access_method(design_object_json, _RDO_TYPE_TO_APPLICATION_METHOD)
        return opaque_id, design_object_json

    def click_design_object(self, design_object_name: str, locust_request_label: Optional[str] = None) -> DesignObjectUiForm:
        """
        Click on a design object in the design object grid. The current view of the grid must contain the object you wish
        to click.
        Args:
            design_object_name: The name of the design object to click on

        Returns (DesignObjectUiForm): UiForm representing UI of design object

        """
        opaque_id, design_object_json = self.__get_design_object_info(design_object_name, locust_request_label)
        breadcrumb = f"Design.SelectedObject.{opaque_id[:10]}.SailUi"
        return DesignObjectUiForm(self._interactor, design_object_json, breadcrumb)

    def click_interface(self, interface_name: str, locust_request_label: Optional[str] = None) -> InterfaceDesignerUiForm:
        """
        Click on an interface design object in the design object grid. The grid is filtered to only show interface before
        clicking on the object.
        Args:
            interface_name: The name of the interface to click on
            locust_request_label: A locust request label to use in place of the default

        Returns (InterfaceDesignerUiForm): UiForm representing the UI of Interface Designer
        """
        self.filter_design_objects([DesignObjectType.INTERFACE])
        opaque_id, design_object_json = self.__get_design_object_info(interface_name, locust_request_label)
        breadcrumb = f"Design.SelectedInterface.{opaque_id[:10]}.SailUi"
        return InterfaceDesignerUiForm(self._interactor, design_object_json, breadcrumb)

    def click_ai_skill(self, ai_skill_name: str, locust_request_label: Optional[str] = None) -> AISkillUiForm:
        """
        Click on an AI Skill in the design object grid. The current view of the grid must contain the skill you wish
        to click.
        Args:
            ai_skill_name: The name of the AI Skill to click on

        Returns (AISkillUiForm): UiForm representing UI of AI Skill

        """
        opaque_id = self.__design.find_design_object_opaque_id_in_grid(ai_skill_name, self._state)
        locust_request_label = locust_request_label or f"Application.AiSkill.{opaque_id[:10]}.Click"
        object_json = self.__design.fetch_design_object_json(opaque_id=opaque_id,
                                                             locust_request_label=f"{locust_request_label}.DesignObject")
        ai_skill_info = self.__design.extract_ai_skill_info(object_json=object_json)

        rdo_interactor = _RDOInteractor(interactor=self._interactor, rdo_host=ai_skill_info.host_url)
        ai_skill_json = rdo_interactor.fetch_ai_skill_designer_json(ai_skill_id=ai_skill_info.object_uuid)
        breadcrumb = f"Design.SelectedAiSkill.{opaque_id[:10]}.SailUi"
        return AISkillUiForm(rdo_interactor=rdo_interactor,
                             rdo_state=ai_skill_json,
                             ai_skill_id=ai_skill_info.object_uuid,
                             breadcrumb=breadcrumb,
                             )

    def create_ai_skill_object(self, ai_skill_name: str, ai_skill_type: AISkillObjectType) -> 'ApplicationUiForm':
        """
        Creates an AI Skill with the given name

        Returns: The SAIL UI Form after the record type is created

        """
        self.__design.create_ai_skill_object(self, ai_skill_name=ai_skill_name, ai_skill_type=ai_skill_type)
        return self

    def create_record_type(self, record_type_name: str) -> 'ApplicationUiForm':
        """
        Creates a record type with the given name

        Returns: The SAIL UI Form after the record type is created

        """
        self.__design.create_object(self, link_name='Record Type', object_name=record_type_name)
        return self

    def create_interface(self, interface_name: str) -> 'ApplicationUiForm':
        """
        Creates an interface with the given name

        Returns: The SAIL UI Form after the interface is created

        """
        self.click('Interface').fill_text_field('Name', interface_name).click('Create')
        return self

    def create_report(self, report_name: str) -> 'ApplicationUiForm':
        """
        Creates a report with the given name

        Returns: The SAIL UI Form after the report is created

        """
        self.__design.create_object(self, link_name='Report', object_name=report_name)
        return self

    def get_available_design_objects(self) -> Dict[str, DesignObject]:
        """
        Retrieve all available design objects in the application, must be on page with design object list

        Returns (dict): Dictionary mapping design object names to DesignObject
        """
        return get_available_design_objects(self._state)

    def search_objects(self, search_str: str, locust_label: Optional[str] = None) -> 'ApplicationUiForm':
        """
            Search the design object list in an Application, must be on page with design object list
            Args:
                search_str (str): The string to search
                locust_label (str): Label to associate request with

            Returns (ApplicationUiForm): A UiForm with updated state after the search is complete

        """
        new_state = self.__design.search_design_grid(
            search_str, self._get_update_url_for_reeval(self._state), self._state, self.context, self.uuid,
            locust_label if locust_label else f"{self.breadcrumb}.ObjectSearch"
        )
        self._reconcile_state(new_state, skipValidations=True)
        return self

    def filter_design_objects(self, design_object_types: list[DesignObjectType]) -> 'ApplicationUiForm':
        """
        Filter the design object list in an Application, must be on page with design object list
        Args:
            design_object_types (DesignObjectType): List of the types of objects you wish to filter on

        Returns (ApplicationUiForm): ApplicationUiForm with filtered list of design objects

        """
        indices = self.__design.find_design_object_type_indices(current_state=self._state,
                                                                design_object_types=[design_object_type.value for design_object_type in design_object_types])
        self.check_checkbox_by_test_label(test_label="object-type-checkbox", indices=indices)
        return self
