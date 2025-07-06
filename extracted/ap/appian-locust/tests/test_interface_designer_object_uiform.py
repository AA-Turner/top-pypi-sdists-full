import unittest
from unittest.mock import MagicMock, patch

from locust import TaskSet, Locust

from .mock_client import CustomLocust
from .mock_reader import read_mock_file
from appian_locust import AppianTaskSet
from appian_locust.uiform.InterfaceDesignerUiForm import InterfaceDesignerUiForm


class TestInterfaceDesignerUiform(unittest.TestCase):
    interface_designer_simple_interface = read_mock_file("interface_designer_simple_interface.json")
    interface_designer_empty_interface = read_mock_file("interface_designer_empty_interface.json")
    default_object_id = "lIBLQLGU6pYkw0C5Zw-W_VRdOG8QydZTNbKM1Jnrko8WXRBdyVgpItPs0IjjSIHPfdUsgKHxzHW7K-WKYaM3Xi3H7ahNzAc2p6JHQiRJeko9xrc"

    def setUp(self) -> None:
        self.maxDiff = None
        self.custom_locust = CustomLocust(Locust())
        parent_task_set = TaskSet(self.custom_locust)
        setattr(parent_task_set, "host", "")
        setattr(parent_task_set, "auth", ["", ""])
        self.task_set = AppianTaskSet(parent_task_set)
        self.task_set.host = ""

        # test_on_start_auth_success is covered here.
        self.custom_locust.set_response("auth?appian_environment=tempo", 200, "{}")
        self.task_set.on_start()

    def tearDown(self) -> None:
        self.task_set.on_stop()

    @patch("appian_locust._interactor._Interactor.click_generic_element")
    def test_delete_component(self, click_generic_mock: MagicMock) -> None:
        sail_form = self.get_interface_sail_form()
        # Delete Text
        sail_form.delete_component("Text")
        _, kwargs = click_generic_mock.call_args_list[0]
        value = kwargs["new_value"]
        self.assertEqual(value, {
            "#t": "Dictionary",
            "#v": {
                "action": "DELETE",
                "targetNodeId": "31"
            }
        })

    @patch("appian_locust._interactor._Interactor.click_generic_element")
    def test_duplicate_component(self, click_generic_mock: MagicMock) -> None:
        sail_form = self.get_interface_sail_form()
        # Duplicate Text
        sail_form.duplicate_component("Text")
        _, kwargs = click_generic_mock.call_args_list[0]
        value = kwargs["new_value"]
        self.assertEqual(value, {
            "#t": "Dictionary",
            "#v": {
                "action": "DUPLICATE",
                "newHighlightId": "31",
                "targetNodeId": "31",
                "tempNodeMap": {}
            }
        })

    @patch("appian_locust._interactor._Interactor.click_generic_element")
    def test_select_component(self, click_generic_mock: MagicMock) -> None:
        sail_form = self.get_interface_sail_form()
        # Select Text
        sail_form.select_component("Text", index=2)
        _, kwargs = click_generic_mock.call_args_list[0]
        value = kwargs["new_value"]
        self.assertEqual(value, {
            "#t": "Dictionary",
            "#v": {
                "action": "HIGHLIGHT_COMPONENT",
                "id": "310"
            }
        })

    @patch("appian_locust._interactor._Interactor.click_generic_element")
    def test_drag_and_drop_from_palette_to_empty_live_view(self, click_generic_mock: MagicMock) -> None:
        sail_form = self.get_interface_sail_form()
        # Drag Text to empty Live View
        sail_form.drag_and_drop_from_palette_to_empty_live_view("Text", False)
        _, kwargs = click_generic_mock.call_args_list[0]
        value = kwargs["new_value"]
        self.assertEqual(value, {
            "#t": "Dictionary",
            "#v": {
                "action": "UPDATE",
                "isUserInterface": False,
                "newHighlightId": "1-2",
                "paletteSearchTerm": "",
                "shouldClearTempIds": True,
                "sourceComponentTypes": ["TextField"],
                "sourceType": "PALETTE",
                "targetType": "EMPTY_LIVE_VIEW",
                "tempNodeMap": {"1-2": []},
                "templateId": "textField"
            }
        })

    @patch("appian_locust._interactor._Interactor.click_generic_element")
    def test_drag_and_drop_from_palette_to_empty_live_view_user_interface(self, click_generic_mock: MagicMock) -> None:
        sail_form = self.get_interface_sail_form()
        # Drag Text to empty Live View
        sail_form.drag_and_drop_from_palette_to_empty_live_view("Text", True)
        _, kwargs = click_generic_mock.call_args_list[0]
        value = kwargs["new_value"]
        self.assertEqual(value, {
            "#t": "Dictionary",
            "#v": {
                "action": "UPDATE",
                "isUserInterface": True,
                "newHighlightId": "1-2",
                "paletteSearchTerm": "",
                "shouldClearTempIds": True,
                "sourceComponentTypes": ["TextField"],
                "sourceType": "PALETTE",
                "targetType": "EMPTY_LIVE_VIEW",
                "tempNodeMap": {"1-2": []},
                "templateId": "textField"
            }
        })

    @patch("appian_locust._interactor._Interactor.click_generic_element")
    def test_drag_and_drop_from_palette_to_component_below(self, click_generic_mock: MagicMock) -> None:
        sail_form = self.get_interface_sail_form()
        # Drag Card to below Text
        sail_form.drag_and_drop_from_palette_to_component("Card", "Text", False, False)
        _, kwargs = click_generic_mock.call_args_list[0]
        value = kwargs["new_value"]
        self.assertEqual(value, {
            "#t": "Dictionary",
            "#v": {
                "action": "ADD_BELOW",
                "isUserInterface": False,
                "newHighlightId": "1-2",
                "paletteSearchTerm": "",
                "shouldClearTempIds": True,
                "sourceComponentTypes": ["CardLayout"],
                "sourceType": "PALETTE",
                "targetComponentTypes": ["TextField"],
                "targetNodeId": "31",
                "targetType": "COMPONENT",
                "tempNodeMap": {"1-2": []},
                "templateId": "cardLayout"
            }
        })

    @patch("appian_locust._interactor._Interactor.click_generic_element")
    def test_drag_and_drop_from_palette_to_component_above(self, click_generic_mock: MagicMock) -> None:
        sail_form = self.get_interface_sail_form()
        # Drag Card to above Text
        sail_form.drag_and_drop_from_palette_to_component("Card", "Text", True, False)
        _, kwargs = click_generic_mock.call_args_list[0]
        value = kwargs["new_value"]
        self.assertEqual(value, {
            "#t": "Dictionary",
            "#v": {
                "action": "ADD_ABOVE",
                "isUserInterface": False,
                "newHighlightId": "1-2",
                "paletteSearchTerm": "",
                "shouldClearTempIds": True,
                "sourceComponentTypes": ["CardLayout"],
                "sourceType": "PALETTE",
                "targetComponentTypes": ["TextField"],
                "targetNodeId": "31",
                "targetType": "COMPONENT",
                "tempNodeMap": {"1-2": []},
                "templateId": "cardLayout"
            }
        })

    @patch("appian_locust._interactor._Interactor.click_generic_element")
    def test_drag_and_drop_from_palette_to_component_below_user_interface(self, click_generic_mock: MagicMock) -> None:
        sail_form = self.get_interface_sail_form()
        # Drag Card to below Text
        sail_form.drag_and_drop_from_palette_to_component("Card", "Text", False, True)
        _, kwargs = click_generic_mock.call_args_list[0]
        value = kwargs["new_value"]
        self.assertEqual(value, {
            "#t": "Dictionary",
            "#v": {
                "action": "ADD_BELOW",
                "isUserInterface": True,
                "newHighlightId": "1-2",
                "paletteSearchTerm": "",
                "shouldClearTempIds": True,
                "sourceComponentTypes": ["CardLayout"],
                "sourceType": "PALETTE",
                "targetComponentTypes": ["TextField"],
                "targetNodeId": "31",
                "targetType": "COMPONENT",
                "tempNodeMap": {"1-2": []},
                "templateId": "cardLayout"
            }
        })

    @patch("appian_locust._interactor._Interactor.click_generic_element")
    def test_drag_and_drop_from_palette_to_placeholder(self, click_generic_mock: MagicMock) -> None:
        sail_form = self.get_interface_sail_form()
        # Drag Card into Box contents
        sail_form.drag_and_drop_from_palette_to_placeholder("Card", "Box Layout", False)
        _, kwargs = click_generic_mock.call_args_list[0]
        value = kwargs["new_value"]
        self.assertEqual(value, {
            "#t": "Dictionary",
            "#v": {
                "action": "CUT_PASTE_ABOVE",
                "isUserInterface": False,
                "newHighlightId": "1-2",
                "paletteSearchTerm": "",
                "shouldClearTempIds": True,
                "sourceComponentTypes": ["CardLayout"],
                "sourceType": "PALETTE",
                "targetComponentTypes": [],
                "targetNodeId": "89",
                "targetType": "COMPONENT",
                "tempNodeMap": {"1-2": []},
                "templateId": "cardLayout"
            }
        })

    @patch("appian_locust._interactor._Interactor.click_generic_element")
    def test_drag_and_drop_from_palette_to_placeholder_user_interface(self, click_generic_mock: MagicMock) -> None:
        sail_form = self.get_interface_sail_form()
        # Drag Card into Box contents
        sail_form.drag_and_drop_from_palette_to_placeholder("Card", "Box Layout", True)
        _, kwargs = click_generic_mock.call_args_list[0]
        value = kwargs["new_value"]
        self.assertEqual(value, {
            "#t": "Dictionary",
            "#v": {
                "action": "CUT_PASTE_ABOVE",
                "isUserInterface": True,
                "newHighlightId": "1-2",
                "paletteSearchTerm": "",
                "shouldClearTempIds": True,
                "sourceComponentTypes": ["CardLayout"],
                "sourceType": "PALETTE",
                "targetComponentTypes": [],
                "targetNodeId": "89",
                "targetType": "COMPONENT",
                "tempNodeMap": {"1-2": []},
                "templateId": "cardLayout"
            }
        })

    @patch("appian_locust._interactor._Interactor.click_generic_element")
    def test_drag_and_drop_from_live_view_to_component_below(self, click_generic_mock: MagicMock) -> None:
        sail_form = self.get_interface_sail_form()
        # Drag Text to below Paragraph
        sail_form.drag_and_drop_from_live_view_to_component("Text", "Paragraph",
                                                            False, source_index=2, target_index=1)
        _, kwargs = click_generic_mock.call_args_list[0]
        value = kwargs["new_value"]
        self.assertEqual(value, {
            "#t": "Dictionary",
            "#v": {
                "action": "CUT_PASTE_BELOW",
                "cutNodeId": "310",
                "newHighlightId": "310",
                "shouldClearTempIds": True,
                "sourceComponentTypes": ["TextField"],
                "sourceType": "LIVE_VIEW",
                "targetComponentTypes": ["ParagraphField"],
                "targetNodeId": "72",
                "targetType": "COMPONENT"
            }
        })

    @patch("appian_locust._interactor._Interactor.click_generic_element")
    def test_drag_and_drop_from_live_view_to_component_above(self, click_generic_mock: MagicMock) -> None:
        sail_form = self.get_interface_sail_form()
        # Drag Text to above Paragraph
        sail_form.drag_and_drop_from_live_view_to_component("Text", "Paragraph", True)
        _, kwargs = click_generic_mock.call_args_list[0]
        value = kwargs["new_value"]
        self.assertEqual(value, {
            "#t": "Dictionary",
            "#v": {
                "action": "CUT_PASTE_ABOVE",
                "cutNodeId": "31",
                "newHighlightId": "31",
                "shouldClearTempIds": True,
                "sourceComponentTypes": ["TextField"],
                "sourceType": "LIVE_VIEW",
                "targetComponentTypes": ["ParagraphField"],
                "targetNodeId": "72",
                "targetType": "COMPONENT"
            }
        })

    @patch("appian_locust._interactor._Interactor.click_generic_element")
    def test_drag_and_drop_from_live_view_to_placeholder(self, click_generic_mock: MagicMock) -> None:
        sail_form = self.get_interface_sail_form()
        # Drag Text to below Paragraph
        sail_form.drag_and_drop_from_live_view_to_placeholder("Text", "Box Layout")
        _, kwargs = click_generic_mock.call_args_list[0]
        value = kwargs["new_value"]
        self.assertEqual(value, {
            "#t": "Dictionary",
            "#v": {
                "action": "CUT_PASTE_ABOVE",
                "cutNodeId": "31",
                "newHighlightId": "31",
                "shouldClearTempIds": True,
                "sourceComponentTypes": ["TextField"],
                "sourceType": "LIVE_VIEW",
                "targetComponentTypes": [],
                "targetNodeId": "89",
                "targetType": "PLACEHOLDER"
            }
        })

    def get_interface_sail_form(self,
                                design_object_id: str = default_object_id) -> InterfaceDesignerUiForm:
        # Visit the interface
        self.custom_locust.set_response(
            f"/suite/rest/a/applications/latest/app/design/{design_object_id}", 200,
            self.interface_designer_simple_interface)
        return self.task_set.appian.visitor.visit_interface_object_by_id(design_object_id)
