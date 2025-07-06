import unittest

from appian_locust._records_helper import (get_url_stub_from_record_list_url_path,
                                           get_url_stub_from_record_list_post_request_url)
from appian_locust import _records_helper


class TestHelper(unittest.TestCase):
    def test_get_url_stub_of_record_list_from_expected_state(self) -> None:
        self.assertEqual(get_url_stub_from_record_list_url_path('tempo/records/type/url_stub123/view/all'),
                         'url_stub123')

    def test_get_url_stub_of_record_list_from_no_url(self) -> None:
        self.assertIsNone(get_url_stub_from_record_list_url_path(None))

    def test_get_url_stub_of_record_list_from_unexpected_url(self) -> None:
        self.assertIsNone(get_url_stub_from_record_list_url_path('tempo/reports/view/url_stub123/view/all'))

    def test_get_url_stub_from_record_list_post_request_url_from_record_instance_list_url(self) -> None:
        # Given a record instance list url
        record_instance_list_url = '/suite/rest/a/sites/latest/D6JMim/pages/records/recordType/1vM_9A'

        # Attempt to get url stub
        record_instance_list_url_stub = get_url_stub_from_record_list_post_request_url(record_instance_list_url)

        # Then the record instance list url has its stub returned
        self.assertEqual(record_instance_list_url_stub, '1vM_9A')

    def test_get_url_stub_from_record_list_post_request_url_from_record_type_list_url(self) -> None:
        # Given a record type list url
        record_type_list_url = '/suite/rest/a/applications/latest/legacy/sites/D6JMim/page/records'

        # Attempt to get url stub
        record_type_list_url_stub = get_url_stub_from_record_list_post_request_url(record_type_list_url)

        # Then None is returned
        self.assertIsNone(record_type_list_url_stub)

    def test_get_url_stub_from_record_list_post_request_url_from_record_instance_url(self) -> None:
        # Given a record instance url
        record_instance_url = '/suite/rest/a/sites/latest/D6JMim/page/records/record/lQBU8YV4nEFVwMuczMM/view/summary'

        # Attempt to get url stub
        record_instance_url_stub = get_url_stub_from_record_list_post_request_url(record_instance_url)

        # Then None is returned
        self.assertIsNone(record_instance_url_stub)

    def test_get_record_header_response(self) -> None:
        form_dict = {
            "feed": {
                "lang": "en_US",
                "id": "record",
                "title": "Customer Service Request #I49K-V46X",
                "generator": {
                    "version": "21.1.0.210",
                    "uri": "https://an-appian-instance.host.net/suite/",
                    "value": "Appian"
                },
                "icon": "https://an-appian-instance.host.net/suite/framework/img/favicon.ico",
                "logo": "https://an-appian-instance.host.net/suite/portal/img/skins/default/companylogo.png",
                "links": [{
                    "href": "#",
                    "rel": "x-embedded-uis",
                    "extensions": [{
                        "name": "x-embedded-header",
                        "attributes": {
                            "xmlns": ""
                        },
                        "children": ['{ "name":"John"}', '{"city":"New York"}']
                    },
                        {
                            "name": "x-embedded-summary",
                            "attributes": {
                                "xmlns": ""
                            },
                            "children": ['{ "name":"Sam"}']
                    }]
                }]
            }}
        obj = _records_helper.get_record_header_response(form_dict)

        # assert that we get first child of ui component
        self.assertEqual(obj, {"name": "John"})

    def test_get_record_header_response_with_no_child_ui_component_throws_exception(self) -> None:
        form_dict = {
            "feed": {
                "lang": "en_US",
                "id": "record",
                "title": "Customer Service Request #I49K-V46X",
                "generator": {
                    "version": "21.1.0.210",
                    "uri": "https://an-appian-instance.host.net/suite/",
                    "value": "Appian"
                },
                "icon": "https://an-appian-instance.host.net/suite/framework/img/favicon.ico",
                "logo": "https://an-appian-instance.host.net/suite/portal/img/skins/default/companylogo.png",
                "links": [{
                    "href": "#",
                    "rel": "x-embedded-uis",
                    "extensions": [{
                        "name": "x-embedded-header",
                        "attributes": {
                            "xmlns": ""
                        },
                        "children": []
                    },
                        {
                            "name": "x-embedded-summary",
                            "attributes": {
                                "xmlns": ""
                            },
                            "children": ['{ "name":"Sam"}']
                    }]
                }]
            }}
        exception_msg = ("Parser was not able to find embedded SAIL code within JSON response for the requested Record "
                         "Instance")
        # assert the exception get thrown
        with self.assertRaises(Exception) as exc:
            obj = _records_helper.get_record_header_response(form_dict)

        self.assertEqual(exc.exception.__str__(), exception_msg)

    def test_get_record_summary_view_response(self) -> None:
        form_dict = {
            "feed": {
                "lang": "en_US",
                "id": "record",
                "title": "Customer Service Request #I49K-V46X",
                "generator": {
                    "version": "21.1.0.210",
                    "uri": "https://an-appian-instance.host.net/suite/",
                    "value": "Appian"
                },
                "icon": "https://an-appian-instance.host.net/suite/framework/img/favicon.ico",
                "logo": "https://an-appian-instance.host.net/suite/portal/img/skins/default/companylogo.png",
                "links": [{
                    "href": "#",
                    "rel": "x-embedded-uis",
                    "extensions": [{
                        "name": "x-embedded-header",
                        "attributes": {
                            "xmlns": ""
                        },
                        "children": ['{ "name":"John"}', '{"city":"New York"}']
                    },
                        {
                            "name": "x-embedded-summary",
                            "attributes": {
                                "xmlns": ""
                            },
                            "children": ['{ "name":"Sam"}']
                    }]
                }]
            }
        }
        obj = _records_helper.get_record_summary_view_response(form_dict)

        # assert that we get first child of ui component
        self.assertEqual(obj, {"name": "Sam"})

    def test_get_record_summary_view_response_with_no_child_ui_component_throws_exception(self) -> None:
        form_dict = {
            "feed": {
                "lang": "en_US",
                "id": "record",
                "title": "Customer Service Request #I49K-V46X",
                "generator": {
                    "version": "21.1.0.210",
                    "uri": "https://an-appian-instance.host.net/suite/",
                    "value": "Appian"
                },
                "icon": "https://an-appian-instance.host.net/suite/framework/img/favicon.ico",
                "logo": "https://an-appian-instance.host.net/suite/portal/img/skins/default/companylogo.png",
                "links": [{
                    "href": "#",
                    "rel": "x-embedded-uis",
                    "extensions": [{
                        "name": "x-embedded-header",
                        "attributes": {
                            "xmlns": ""
                        },
                        "children": ['{ "name":"John"}', '{"city":"New York"}']
                    },
                        {
                            "name": "x-embedded-summary",
                            "attributes": {
                                "xmlns": ""
                            },
                            "children": []
                    }]
                }]
            }
        }
        exception_msg = ("Parser was not able to find embedded SAIL code within JSON response for the requested Record "
                         "Instance")
        # assert the exception get thrown
        with self.assertRaises(Exception) as exc:
            obj = _records_helper.get_record_summary_view_response(form_dict)

        self.assertEqual(exc.exception.__str__(), exception_msg)


if __name__ == '__main__':
    unittest.main()
