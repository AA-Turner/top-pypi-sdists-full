import json
import unittest
from requests import Response

from appian_locust._design import _Design, DESIGN_URI_PATH
from appian_locust._interactor import _Interactor
from appian_locust.objects import DesignObjectType
from .mock_reader import read_mock_file

integration_url = ""
auth = ["fake_user", ""]


class TestDesign(unittest.TestCase):

    def setUp(self) -> None:
        self.interactor: _Interactor = _Interactor("", "ase")
        setup_headers_mock = unittest.mock.Mock(return_value={})
        setattr(self.interactor, 'setup_sail_headers', setup_headers_mock)
        setattr(self.interactor, 'setup_request_headers', setup_headers_mock)
        self.design_interactor: _Design = _Design(self.interactor)

    def test_fetch_design_json(self) -> None:
        response_mock = unittest.mock.Mock(return_value={"ase": "ase2"})
        response_all_ok_mock = unittest.mock.Mock(return_value="")
        response = Response()
        setattr(response, 'json', response_mock)
        setattr(response, 'raise_for_status', response_all_ok_mock)  # ensure response.ok returns true
        get_page_mock = unittest.mock.Mock(
            side_effect=lambda uri, headers, label: response if uri == DESIGN_URI_PATH else "",
        )
        setattr(self.interactor, 'get_page', get_page_mock)

        output = self.design_interactor.fetch_design_json()
        self.assertEqual(output, {"ase": "ase2"})

    def test_fetch_application_json(self) -> None:
        application_id = "someApplicationId"
        response_mock = unittest.mock.Mock(return_value={"ase": "ase2"})
        response_all_ok_mock = unittest.mock.Mock(return_value="")
        response = Response()
        setattr(response, 'json', response_mock)
        setattr(response, 'raise_for_status', response_all_ok_mock)  # ensure response.ok returns true
        get_page_mock = unittest.mock.Mock(
            side_effect=lambda uri, headers, label: response if uri == f"{DESIGN_URI_PATH}/app/{application_id}" else "",
        )
        setattr(self.interactor, 'get_page', get_page_mock)

        output = self.design_interactor.fetch_application_json(application_id)
        self.assertEqual(output, {"ase": "ase2"})

    def test_fetch_design_object_json(self) -> None:
        design_object_id = "someDesignId"
        response_mock = unittest.mock.Mock(return_value={"ase": "ase2"})
        response_all_ok_mock = unittest.mock.Mock(return_value="")
        response = Response()
        setattr(response, 'json', response_mock)
        setattr(response, 'raise_for_status', response_all_ok_mock)  # ensure response.ok returns true
        get_page_mock = unittest.mock.Mock(
            side_effect=lambda uri, headers, label: response if uri == f"{DESIGN_URI_PATH}/{design_object_id}" else "",
        )
        setattr(self.interactor, 'get_page', get_page_mock)

        output = self.design_interactor.fetch_design_object_json(design_object_id)
        self.assertEqual(output, {"ase": "ase2"})

    def test_find_design_object_filter_index(self) -> None:
        design_objects_mock = read_mock_file("design_objects.json")
        design_objects_state = json.loads(design_objects_mock)
        indices = self.design_interactor.find_design_object_type_indices(design_objects_state, [DesignObjectType.INTERFACE.value, DesignObjectType.DATA_TYPE.value])
        self.assertEqual([13, 5], indices)


if __name__ == '__main__':
    unittest.main()
