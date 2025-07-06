from typing import Any, Dict, Optional

from ._interactor import _Interactor
from ._rdo_interactor import _RDOInteractor
from .exceptions import IncorrectDesignAccessException
from .objects import DesignObject, AISkillObjectType
from .objects.ai_skill import AiSkill
from .utilities import find_component_by_attribute_and_type_in_dict, find_component_by_type_and_attribute_and_index_in_dict, find_component_by_attribute_in_dict
from .uiform import SailUiForm, AISkillUiForm
from urllib.parse import urlparse

DESIGN_URI_PATH: str = "/suite/rest/a/applications/latest/app/design"
AI_SKILL_DESCRIPTOR: str = "AI Skill"


def get_available_design_objects(state: Dict[str, Any]) -> Dict[str, DesignObject]:
    name_column = find_component_by_attribute_and_type_in_dict(type="GridFieldColumn", attribute="label", value="Name",
                                                               component_tree=state)
    design_objects = {}
    for element in name_column["data"]:
        link = element["contents"]["items"][0]["item"]["value"]["values"][0]["link"]
        name = link["testLabel"]
        uri_split = link["uri"].split("/")
        design_objects[name] = DesignObject(name, uri_split[len(uri_split) - 1])
    return design_objects


def validate_design_object_access_method(design_object_json: Dict[str, Any], object_type_to_method_dict: Dict[str, Any]) -> None:
    potential_rdo_info = find_component_by_attribute_in_dict(attribute="testLabel",
                                                             value="RemoteDesignObjectInterface",
                                                             component_tree=design_object_json,
                                                             raise_error=False)
    if potential_rdo_info:
        rdo_object_type = potential_rdo_info["objectType"]
        raise IncorrectDesignAccessException(rdo_object_type, object_type_to_method_dict[rdo_object_type])


class _Design:
    def __init__(self, interactor: _Interactor):
        self.interactor = interactor

    def fetch_design_json(self, locust_request_label: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetches the JSON of /design UI

        Returns: JSON Dictionary

        Example:

            >>> design.fetch_design_json()

        """
        headers = self.interactor.setup_sail_headers()
        headers['X-Client-Mode'] = 'DESIGN'
        label = locust_request_label or "Design.ApplicationList"
        response = self.interactor.get_page(DESIGN_URI_PATH, headers=headers, label=label)
        response.raise_for_status()
        return response.json()

    def fetch_application_json(self, app_id: str, locust_request_label: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetches the JSON of the UI for a specific application within the /design environment

        Returns: JSON Dictionary

        Example:

            >>> design.fetch_application_json("AADZeglVgAAgfpsAAJsAAAAAAdA")

        """
        application_uri = f"{DESIGN_URI_PATH}/app/{app_id}"
        headers = self.interactor.setup_sail_headers()
        headers['X-Client-Mode'] = 'DESIGN'
        label = locust_request_label or f"Design.SelectedApplication.{app_id}"
        response = self.interactor.get_page(application_uri, headers=headers, label=label)
        response.raise_for_status()
        return response.json()

    def fetch_design_object_json(self, opaque_id: str, locust_request_label: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetches the JSON of the UI for a specific object within the /design environment

        Returns: JSON Dictionary

        Example:

             >>> design.fetch_design_object_json("lABD1iTIu_lxy_3T_90Is2fs63uh52xESYi6-fun7FBWshlrBQ0EptlFUdGyIRzSSluPyVdvOhvGgL6aBlnjlkWfQlALYR2aRZ_AIliJ4lc3g")

        """
        headers = self.interactor.setup_sail_headers()
        headers['X-Client-Mode'] = 'DESIGN'
        uri = DESIGN_URI_PATH + '/' + opaque_id
        label = locust_request_label or "Design.SelectedObject." + opaque_id[0:10]
        response = self.interactor.get_page(uri, headers=headers, label=label)
        response.raise_for_status()
        return response.json()

    def extract_ai_skill_info(self, object_json: Dict[str, Any]) -> AiSkill:
        object_info = find_component_by_attribute_in_dict(
            attribute="testLabel",
            value="RemoteDesignObjectInterface",
            component_tree=object_json,
            raise_error=False
        )
        if not object_info or object_info["objectType"] != "aiSkill":
            raise Exception(f"Selected Design Object was not an AI Skill")

        auth_url = object_info["authUrl"]
        parsed_url = urlparse(auth_url)
        rdo_host = parsed_url._replace(path="").geturl()
        return AiSkill(host_url=rdo_host, object_uuid=object_info["objectUuid"])

    def find_design_grid(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return find_component_by_type_and_attribute_and_index_in_dict(state, "GridField", "testLabel", "GRID-LABEL")

    def click_expression_editor_toolbar_button(self, button_action: str, post_url: str, state: Dict[str, Any], context: Dict[str, Any], uuid: str,
                                               label: Optional[str] = None) -> Dict[str, Any]:

        expression_editor_component = find_component_by_type_and_attribute_and_index_in_dict(state, type="ExpressionInfoPanel")["editorWidget"]
        expression = expression_editor_component["value"]

        new_value = {
            "#t": "Dictionary",
            "#v": {
                "actionType": button_action,
                "hasMatchingBracketError": False,
                "launchOrigin": "toolbarButton",
                "queryFnType": "queryRecordType",
                "queryFnStartIndex": 0,
                "queryFnEndIndex": len(expression),
                "value": {
                    "#t": "Text",
                    "#v": expression
                }
            }
        }

        locust_label = label or f'Click \'{button_action}\' Expression Editor Widget Button'
        return self.interactor.click_generic_element(post_url, expression_editor_component, context, uuid, new_value, locust_label)

    def search_design_grid(self, search_str: str, reeval_url: str,
                           state: Dict[str, Any], context: Dict[str, Any], uuid: str, locust_label: str = "Design.Search") -> Dict[str, Any]:
        """
        Search a grid in /design
        Args:
            search_str (str): string to search
            reeval_url (str): url to send request to
            state (str): current state of UI, which contains the search bar
            context (str): current context
            uuid (str): UUID of search component
            locust_label (str): label to associate request with

        Returns:

        """
        search_component = find_component_by_attribute_in_dict(attribute="#t", value="SearchBoxWidget",
                                                               component_tree=state)
        search_component["#t"] = "TextWidget"
        return self.interactor.click_generic_element(
            reeval_url, search_component, context, uuid, new_value={"#t": "Text", "#v": search_str},
            label=locust_label)

    def find_design_object_opaque_id_in_grid(self, design_object_name: str, current_state: Dict[str, Any]) -> str:
        grid_component = self.find_design_grid(current_state)
        link_component = find_component_by_attribute_in_dict('testLabel', design_object_name, grid_component, throw_attribute_exception=True)
        return link_component.get("uri").split('/')[-1]

    def find_design_object_type_indices(self, current_state: Dict[str, Any], design_object_types: list[str]) -> list[int]:
        checkbox = find_component_by_attribute_in_dict(attribute="testLabel", value="object-type-checkbox", component_tree=current_state)
        choices = checkbox["choices"]
        indices = []
        for design_object_type in design_object_types:
            indices.append(choices.index(design_object_type) + 1)
        return indices

    def create_object(self, ui_form: SailUiForm, link_name: str, object_name: str) -> SailUiForm:
        return ui_form.click(link_name)\
            .fill_text_field('Name', object_name)\
            .click('Create')\
            .click('Save')

    def create_ai_skill_object(self, ui_form: SailUiForm, ai_skill_name: str, ai_skill_type: AISkillObjectType) -> SailUiForm:
        resp = ui_form.click('AI Skill')
        auth_url = resp.get_latest_state()["ui"]["contents"][0]["contents"][0]["authUrl"]
        parsed_url = urlparse(auth_url)
        rdo_host = parsed_url._replace(path="").geturl()
        app_prefix = resp.get_latest_state()["ui"]["contents"][0]["contents"][0]["applicationPrefix"]
        rdo_interactor = _RDOInteractor(interactor=self.interactor, rdo_host=rdo_host)
        create_ai_skill_json = rdo_interactor.fetch_ai_skill_creation_dialog_json(app_prefix=app_prefix)
        # passing in a temporary id because we need one to create the uiform, but one has not been assigned to the object yet
        ai_skill_temp_id = "temp_id"
        ai_skill_ui_form = AISkillUiForm(rdo_interactor=rdo_interactor,
                                         rdo_state=create_ai_skill_json,
                                         ai_skill_id=ai_skill_temp_id)
        ai_skill_ui_form.click_card_layout_by_index(index=ai_skill_type.value)
        ai_skill_ui_form.fill_text_field(label="Name", value=ai_skill_name)
        ai_skill_ui_form.click_button(label="Create")
        creation_save_dialog_ui_form = SailUiForm(interactor=self.interactor,
                                                  state=rdo_interactor.fetch_ai_skill_creation_save_dialog_json(state=ui_form.get_latest_state(), rdo_state=ai_skill_ui_form.get_latest_state()))
        creation_save_dialog_ui_form.click("Save", locust_request_label="AiSkill.Save")
        ui_form._reconcile_state(creation_save_dialog_ui_form.get_latest_state(), skipValidations=True)
        return ui_form
