from enum import Enum
from typing import Any, Dict

from .._interactor import _Interactor
from ..client_mode import ClientMode
from ..uiform import DesignObjectUiForm
from ..exceptions import DisabledComponentException, ComponentNotFoundException
from ..utilities import logger, get_in_dict

from ..utilities.helper import (find_component_by_attribute_in_dict,
                                find_component_by_attribute_and_index_in_dict,
                                find_component_by_type_and_attribute_and_index_in_dict)

log = logger.getLogger(__name__)

class SourceType(Enum):
    LIVE_VIEW = "LIVE_VIEW"
    PALETTE = "PALETTE"
    ADD_COMPONENT_HELPER = "ADD_COMPONENT_HELPER"


class DropType(Enum):
    EMPTY_LIVE_VIEW = "EMPTY_LIVE_VIEW"
    PLACEHOLDER = "PLACEHOLDER"
    COMPONENT = "COMPONENT"


class InterfaceDesignerUiForm(DesignObjectUiForm):

    def __init__(self, interactor: _Interactor, state: Dict[str, Any], breadcrumb: str = "InterfaceDesignerUi"):
        super().__init__(interactor, state, breadcrumb)
        interactor.set_client_mode(client_mode=ClientMode.INTERFACE_DESIGN)

    def delete_component(self, component_label: str,  index: int = 1, locust_request_label: str = "") -> None:
        """
            Delete a component from the live view area in Interface Designer.
            Args:
                component_label (str): The component type/label to delete. E.g., "Box Layout".
                index (str): the index of the component to select in the case where there are multiple components of the
                same type or same label exist in the live view. Default is set to 1
                locust_request_label(str): Label used to identify the request for locust statistics
            Returns: None
        """
        component_id, _ = self.__get_live_view_component_info(component_label, index)
        new_value = {
            "action": "DELETE",
            "targetNodeId": component_id
        }
        locust_label = locust_request_label or f"Delete {component_label}"
        self.__send_interface_designer_manager_request(new_value, locust_label)

    def duplicate_component(self, component_label: str, index: int = 1, locust_request_label: str = "") -> None:
        """
            Duplicate a component in the live view area in Interface Designer.
            Args:
                component_label (str): The component type/label to Duplicate. E.g., "Box Layout".
                index (str): the index of the component to select in the case where there are multiple components of the
                same type or same label exist in the live view. Default is set to 1
                locust_request_label(str): Label used to identify the request for locust statistics
            Returns: None
        """
        component_id, _ = self.__get_live_view_component_info(component_label, index)

        new_value = {
            "action": "DUPLICATE",
            "tempNodeMap": {},
            "targetNodeId": component_id,
            "newHighlightId": f"{component_id}"
        }
        locust_label = locust_request_label or f"Duplicate {component_label}"
        self.__send_interface_designer_manager_request(new_value, locust_label)

    def select_component(self, component_label: str, index: int = 1, locust_request_label: str = "") -> None:
        """
            Select a component in the live view area in Interface Designer.
            Args:
                component_label (str): The component type/label to select. E.g., "Box Layout".
                index (str): the index of the component to select in the case where there are multiple components of the
                same type or same label exist in the live view. Default is set to 1.
                locust_request_label(str): Label used to identify the request for locust statistics
            Returns: None
        """
        component_id, _ = self.__get_live_view_component_info(component_label, index)
        new_value = {
            "action": "HIGHLIGHT_COMPONENT",
            "id": component_id
        }
        locust_label = locust_request_label or f"Select {component_label}"
        self.__send_interface_designer_manager_request(new_value, locust_label)

    def drag_and_drop_from_palette_to_empty_live_view(self, source_palette_label: str, is_user_interface: bool = False,
                                                      locust_request_label: str = "") -> None:
        """
            Drag a component from the palette area and drop it to the empty live view area in Interface Designer.
            Args:
                source_palette_label (str): The component type to drag and drop into the live view. E.g., "Box Layout".
                is_user_interface (bool): whether the component to drag and drop is an user defined interface.
                locust_request_label(str): Label used to identify the request for locust statistics
            Returns: None
        """
        new_value = self.__get_palette_to_empty_live_view_save_value(source_palette_label, is_user_interface)
        locust_label = locust_request_label or f"Drag '{source_palette_label}' from the Palette and drop in Empty Live View"
        self.__send_interface_designer_manager_request(new_value, locust_label)

    def drag_and_drop_from_palette_to_component(self, source_palette_label: str, target_component: str, add_above: bool,
                                                is_user_interface: bool = False,
                                                locust_request_label: str = "") -> None:
        """
            Drag a component from the palette area and drop it next to a component in the live view area in Interface
            Designer.
            Args:
                source_palette_label (str): The component type to drag and drop into the live view. E.g., "Box Layout".
                target_component (str): The existing component in the live view to drop the new component to.
                add_above (str): If True, drop the new component on top of the existing component, if False, drop it below.
                is_user_interface (bool): whether the component to drag and drop is an user defined interface.
                locust_request_label(str): Label used to identify the request for locust statistics
            Returns: None
        """
        new_value = self.__get_palette_to_component_save_value(source_palette_label, target_component, add_above,
                                                               is_user_interface)
        direction = "above" if add_above else "below"
        locust_label = locust_request_label or f"Drag '{source_palette_label}' from the Palette and drop {direction} {target_component}"
        self.__send_interface_designer_manager_request(new_value, locust_label)

    def drag_and_drop_from_palette_to_placeholder(self, source_palette_label: str, parent_target_component: str,
                                                  is_user_interface: bool = False,
                                                  locust_request_label: str = "") -> None:
        """
            Drag a component from the palette area and drop it into an existing component holder in the live view area in
            Interface Designer.
            Args:
                source_palette_label (str): The component type to drag and drop into the live view. E.g., "Box Layout".
                parent_target_component (str): The existing component holder in the live view to drop the new component into.
                is_user_interface (bool): whether the component to drag and drop is an user defined interface.
                locust_request_label(str): Label used to identify the request for locust statistics
            Returns: None
        """
        new_value = self.__get_palette_to_placeholder_save_value(source_palette_label, parent_target_component,
                                                                 is_user_interface)
        locust_label = locust_request_label or f"Drag '{source_palette_label}' from the Palette and drop in the placeholder of {parent_target_component}"
        self.__send_interface_designer_manager_request(new_value, locust_label)

    def drag_and_drop_from_live_view_to_component(self, source_component: str, target_component: str, add_above: bool,
                                                  source_index: int = 1, target_index: int = 1,
                                                  locust_request_label: str = "") -> None:
        """
            Drag a component from the live view area and drop it next to an existing component in the live view area in
            Interface Designer.
            Args:
                source_component (str): The source component type to drag and drop in the live view. E.g., "Box Layout".
                target_component (str): The component in the live view to drop the source component to.
                add_above (bool): If True, drop the new component on top of the existing component, if False, drop it below.
                source_index (int): the index of the source component to select in the case where there are multiple
                components of the same type or same label. Default is set to 1.
                target_index (int): the index of the target component to select in the case where there are multiple
                components of the same type or same label. Default is set to 1.
                locust_request_label(str): Label used to identify the request for locust statistics
        """
        new_value = self.__get_live_view_to_component_save_value(source_component, target_component, add_above,
                                                                 source_index, target_index)
        direction = "above" if add_above else "below"
        locust_label = locust_request_label or f"Drag {source_component} from the Live View and drop {direction} {target_component}"
        self.__send_interface_designer_manager_request(new_value, locust_label)

    def drag_and_drop_from_live_view_to_placeholder(self, source_component: str, parent_target_component: str,
                                                    locust_request_label: str = "") -> None:
        """
           Drag a component from the live view area and drop it into an existing component holder in the live view area in
           Interface Designer.
           Args:
               source_component (str): The source component type to drag and drop in the live view. E.g., "Box Layout".
              parent_target_component (str): The existing component holder in the live view to drop the new component into.
              locust_request_label(str): Label used to identify the request for locust statistics
       """
        new_value = self.__get_live_view_to_placeholder_save_value(source_component, parent_target_component)
        locust_label = locust_request_label or f"Drag {source_component} from the Live View and drop in the placeholder of {parent_target_component}"
        self.__send_interface_designer_manager_request(new_value, locust_label)

    def __get_palette_component_info(self, source_palette_label: str) -> tuple[str, str]:
        component_palette_button = find_component_by_type_and_attribute_and_index_in_dict(self._state,
                                                                                          type="ComponentPaletteButton",
                                                                                          attribute="label",
                                                                                          value=source_palette_label)
        if component_palette_button is None:
            raise Exception(f"Could not find {source_palette_label} in the Component Palette")
        template_id = component_palette_button["templateId"]
        # Design Library Interfaces do not have templateComponentType and default to null
        template_component_type = component_palette_button.get("templateComponentType")
        return template_id, template_component_type

    def __get_live_view_component_info(self, component_label: str, index: int = 1) -> tuple[str, str]:
        try:
            component_selector = find_component_by_type_and_attribute_and_index_in_dict(
                component_tree=self._state, attribute="_iddesign_label", value=component_label, index=index)
        except:
            component_selector = find_component_by_type_and_attribute_and_index_in_dict(
                component_tree=self._state, attribute="_iddesign_listLabels", value=component_label, index=index)
            if component_selector is None:
                raise Exception(f"Could not find {component_label} in the Live View")

        component_id = component_selector.get("_iddesign_id")
        if not component_id:
            component_id = component_selector["_iddesign_listIds"][0]
        component_type = component_selector["#t"]
        return component_id, component_type

    def __get_child_placeholder_info(self, parent_component_label: str) -> str:
        try:
            component_selector = find_component_by_attribute_in_dict("_iddesign_label", parent_component_label,
                                                                     self._state)
        except:
            component_selector = find_component_by_attribute_in_dict("_iddesign_listLabels", parent_component_label,
                                                                     self._state)
            if component_selector is None:
                raise Exception(f"Could not find {parent_component_label} in the Live View")
        child_list_id = component_selector["_iddesign_childComponentListIds"].split(" ")[0]  # For now, assume always the first id
        return child_list_id

    @staticmethod
    def __get_base_drag_and_drop_save_value(source_id: str, source_component_type: str, action: str,
                                            source_type: SourceType, drop_type: DropType) -> Dict[str, Any]:
        return {
            "shouldClearTempIds": True,
            "action": action,
            "sourceType": source_type.value,
            "targetType": drop_type.value,
            "newHighlightId": source_id,
            "sourceComponentTypes": [source_component_type]
        }

    def __get_palette_to_empty_live_view_save_value(self, source_palette_label: str, is_user_interface: bool) -> Dict[
        str, Any]:
        template_id, template_component_type = self.__get_palette_component_info(source_palette_label)
        temp_id = "1-2"
        base_value = self.__get_base_drag_and_drop_save_value(temp_id, template_component_type, "UPDATE",
                                                              SourceType.PALETTE, DropType.EMPTY_LIVE_VIEW)
        new_value = base_value | {
            "paletteSearchTerm": "",
            "isUserInterface": is_user_interface,
            "tempNodeMap": {
                temp_id: []
            },
            "templateId": template_id
        }
        return new_value

    def __get_palette_to_component_save_value(self, source_palette_label: str, target_component: str, add_above: bool,
                                              is_user_interface: bool) -> Dict[str, Any]:
        template_id, template_component_type = self.__get_palette_component_info(source_palette_label)
        target_component_id, target_component_type = self.__get_live_view_component_info(target_component)
        temp_id = "1-2"
        action = "ADD_ABOVE" if add_above else "ADD_BELOW"
        base_value = self.__get_base_drag_and_drop_save_value(temp_id, template_component_type, action,
                                                              SourceType.PALETTE,
                                                              DropType.COMPONENT)
        new_value = base_value | {
            "paletteSearchTerm": "",
            "isUserInterface": is_user_interface,
            "tempNodeMap": {
                temp_id: []
            },
            "templateId": template_id,
            "targetComponentTypes": [target_component_type],
            "targetNodeId": target_component_id
        }
        return new_value

    def __get_palette_to_placeholder_save_value(self, source_palette_label: str, parent_target_component: str,
                                                is_user_interface: bool) -> Dict[str, Any]:
        template_id, template_component_type = self.__get_palette_component_info(source_palette_label)
        placeholder_id = self.__get_child_placeholder_info(parent_target_component)
        temp_id = "1-2"
        base_value = self.__get_base_drag_and_drop_save_value(temp_id, template_component_type, "CUT_PASTE_ABOVE",
                                                              SourceType.PALETTE,
                                                              DropType.COMPONENT)
        new_value = base_value | {
            "paletteSearchTerm": "",
            "isUserInterface": is_user_interface,
            "tempNodeMap": {
                temp_id: []
            },
            "templateId": template_id,
            "targetComponentTypes": [],
            "targetNodeId": placeholder_id
        }
        return new_value

    def __get_live_view_to_component_save_value(self, source_component: str, target_component: str, add_above: bool,
                                                source_index: int, target_index: int) -> Dict[str, Any]:
        source_component_id, source_component_type = self.__get_live_view_component_info(source_component, source_index)
        target_component_id, target_component_type = self.__get_live_view_component_info(target_component, target_index)
        action = "CUT_PASTE_ABOVE" if add_above else "CUT_PASTE_BELOW"
        base_value = self.__get_base_drag_and_drop_save_value(source_component_id, source_component_type, action,
                                                              SourceType.LIVE_VIEW, DropType.COMPONENT)
        new_value = base_value | {
            "targetComponentTypes": [target_component_type],
            "targetNodeId": target_component_id,
            "cutNodeId": source_component_id
        }
        return new_value

    def __get_live_view_to_placeholder_save_value(self, source_component: str, parent_target_component: str) -> Dict[str, Any]:
        source_component_id, source_component_type = self.__get_live_view_component_info(source_component)
        placeholder_id = self.__get_child_placeholder_info(parent_target_component)
        base_value = self.__get_base_drag_and_drop_save_value(source_component_id, source_component_type,
                                                              "CUT_PASTE_ABOVE", SourceType.LIVE_VIEW,
                                                              DropType.PLACEHOLDER)
        new_value = base_value | {
            "targetComponentTypes": [],
            "targetNodeId": placeholder_id,
            "cutNodeId": source_component_id
        }
        return new_value

    def __send_interface_designer_manager_request(self, new_value: Dict[str, Any], locust_label: str) -> None:
        interface_designer_manager_component = \
            find_component_by_type_and_attribute_and_index_in_dict(self._state, type="InterfaceDesignerManager")
        new_value_dictionary = {
            "#t": "Dictionary",
            "#v": new_value
        }
        new_state = self._interactor.click_generic_element(post_url=self.form_url,
                                                           component=interface_designer_manager_component,
                                                           context=self.context,
                                                           uuid=self.uuid,
                                                           new_value=new_value_dictionary,
                                                           label=locust_label)
        self._reconcile_state(new_state, skipValidations=True)

    def _find_literal_view_model_by_label(self, label: str) -> Dict[str, Any]:
        trees_to_search = [self._state]
        while trees_to_search:
            tree = trees_to_search.pop(0)

            if not isinstance(tree, (dict, list)):
                continue

            if isinstance(tree, list):
                trees_to_search = tree + trees_to_search
                continue

            if tree.get('#t') == 'LiteralViewModel' and get_in_dict(tree, ['componentViewModel', 'title', '#v']) == label:
                return tree

            trees_to_search = list(tree.values()) + trees_to_search

        raise Exception(f'Literal View Model with label {label} not found')

    def select_designview_choice_component(self, label: str, choice_label: str, locust_request_label: str = '',
                                           is_test_label: bool = True) -> None:
        try: # pre 25.3
            self.select_dropdown_item(label=label, choice_label=choice_label,
                                      is_test_label=is_test_label, locust_request_label=locust_request_label)
        except ComponentNotFoundException: # 25.3 and after
            literal_view_model_label = self._test_label_to_label(label) if is_test_label else label
            component = self._find_literal_view_model_by_label(literal_view_model_label)

            client_params = get_in_dict(component, ['componentViewModel', 'additionalClientParameters'], {})
            choice_label_index = client_params.get('choiceLabels', []).index(choice_label)
            choice_value = client_params.get('choiceValues', [])[choice_label_index]

            self._update_client_view_model(component, choice_value, locust_request_label)

    def fill_designview_text_field(self, label: str, value: str, locust_request_label: str = '',
                                   is_test_label: bool = True) -> None:
        try: # pre 25.3
            self.fill_text_field(label=label, value=value, is_test_label=is_test_label, locust_request_label=locust_request_label)
        except ComponentNotFoundException: # 25.3 and after
            literal_view_model_label = self._test_label_to_label(label) if is_test_label else label
            self.update_client_view_model_with_label(label=literal_view_model_label, value=value, locust_request_label=locust_request_label)

    def fill_designview_paragraph_field(self, label: str, value: str, locust_request_label: str = '',
                                        is_test_label: bool = True) -> None:
        try: # pre 25.3
            self.fill_paragraph_field(label=label, value=value, is_test_label=is_test_label, locust_request_label=locust_request_label)
        except ComponentNotFoundException: # 25.3 and after
            literal_view_model_label = self._test_label_to_label(label) if is_test_label else label
            self.update_client_view_model_with_label(label=literal_view_model_label, value=value, locust_request_label=locust_request_label)

    def toggle_designview_boolean_field(self, label: str, checked: bool, locust_request_label: str = '',
                                        is_test_label: bool = True) -> None:
        try: # pre 25.3
            indices = [1] if checked else [0]
            if is_test_label:
                self.check_checkbox_by_test_label(test_label=label, indices=indices, locust_request_label=locust_request_label)
            else:
                self.check_checkbox_by_label(label=label, indices=indices, locust_request_label=locust_request_label)
        except ComponentNotFoundException: # 25.3 and after
            literal_view_model_label = self._test_label_to_label(label) if is_test_label else label
            self.update_client_view_model_with_label(label=literal_view_model_label, value=checked, locust_request_label=locust_request_label)

    def update_client_view_model_with_label(self, label: str, value: Any, locust_request_label: str = '') -> None:
        component = self._find_literal_view_model_by_label(label)
        self._update_client_view_model(component, value, locust_request_label)

    def _test_label_to_label(self, test_label: str) -> str:
        # Test labels for common components in the design view all have the format "{label} - {path}"
        dash_index = test_label.find('-')
        return test_label[:dash_index-1]

    def _update_client_view_model(self, component: Dict[str, Any], value: str, locust_request_label: str = '') -> None:
        if get_in_dict(component, ['componentViewModel', 'readOnly', '#v'], False):
            raise DisabledComponentException(label=get_in_dict(component, ['componentViewModel', 'title', '#v']))

        interface_designer_manager = find_component_by_type_and_attribute_and_index_in_dict(
            component_tree=self._state,
            type='InterfaceDesignerManager'
        )
        manager_actions = interface_designer_manager.get('actions', [])
        client_view_model_link = [a for a in manager_actions if a.get('_actionName') == 'clientViewModelUpdate'][0]

        value_dictionary = {
            "#t": "Dictionary",
            "#v": {
                'path': get_in_dict(component, ['componentViewModel', 'path', '#v']),
                'comments': get_in_dict(component, ['componentViewModel', 'comments', '#v']),
                'value': value
            }
        }

        new_state = self._interactor.click_component(self.form_url, client_view_model_link, self.context, self.uuid,
                                                     label=locust_request_label, value=value_dictionary)
        if not new_state:
            raise Exception(f"No response returned when trying to activate the clientViewModelUpdate link")
        self._reconcile_state(new_state)

    def click_design_view_navigation_link(self, label: str, is_test_label: bool = False, locust_request_label: str = '', index: int = 1) -> None:
        """
            Clicks on a navigation link within Interface Designer's Configuration Panel (also called Design View).

            Args:
                label(str): Label of the navigation link to click
                is_test_label(bool): If you are clicking a link via a test label instead of a label, set this boolean to true
                locust_request_label(str): Label used to identify the request for locust statistics
                index(int): Index of the link to click if more than one match the label criteria (default: 1)
        """
        attribute_to_find = 'testLabel' if is_test_label else 'label'
        component = find_component_by_attribute_and_index_in_dict(attribute_to_find, label, index, self._state)
        if component.get('#t') == 'InterfaceDesignerManagerLink':
            self._update_design_view_navigation(component, locust_request_label)
        else:
            self.click(label, is_test_label, locust_request_label)

    def _update_design_view_navigation(self, component: Dict[str, Any], locust_request_label: str = '') -> None:
        """
            Given the InterfaceDesignerManagerLink component that's been clicked, constructs a link value and
            activates the designViewNavigation link on the InterfaceDesignerManager instead.

            Args:
                component(Dict[str, Any]): InterfaceDesignerManagerLink component that was clicked
                locust_request_label(str): Label used to identify the request for locust statistics
        """
        interface_designer_manager = find_component_by_type_and_attribute_and_index_in_dict(
            component_tree=self._state,
            type='InterfaceDesignerManager'
        )
        manager_actions = interface_designer_manager.get('actions', [])
        design_view_navigation_link = [a for a in manager_actions if a.get('_actionName') == 'designViewNavigation'][0]

        id_action_name = get_in_dict(component, ['idActionName'])
        nav_value = get_in_dict(component, ['idActionData', 'path', '#v']) if id_action_name == 'navigation' else get_in_dict(component, ['idActionData', '#v'])
        value_dictionary = {
            "#t": "Dictionary",
            "#v": {
                'idActionName': id_action_name,
                'value': nav_value
            }
        }

        new_state = self._interactor.click_component(self.form_url, design_view_navigation_link, self.context, self.uuid,
                                                     label=locust_request_label, value=value_dictionary)
        if not new_state:
            raise Exception(f"No response returned when trying to activate the designViewNavigation link")
        self._reconcile_state(new_state)
