from locust import TaskSet, Locust
from .mock_client import CustomLocust
from .mock_reader import read_mock_file
from requests.exceptions import HTTPError
from appian_locust import AppianTaskSet
from appian_locust._interactor import _Interactor
from appian_locust._sites import _Sites
from appian_locust.objects import PageType, Page, Site
from appian_locust import PageNotFoundException, InvalidSiteException
import json
import unittest


class TestSites(unittest.TestCase):

    def setUp(self) -> None:
        self.custom_locust = CustomLocust(Locust())
        setattr(self.custom_locust.client, "feature_flag", "")
        setattr(self.custom_locust.client, "feature_flag_extended", "")
        parent_task_set = TaskSet(self.custom_locust)

        setattr(parent_task_set, "host", "")
        setattr(parent_task_set, "auth", ["", ""])
        self.task_set = AppianTaskSet(parent_task_set)
        self.task_set.host = ""

        # test_on_start_auth_success is covered here.
        self.custom_locust.set_response("auth?appian_environment=tempo", 200, '{}')
        self.interactor = _Interactor(self.custom_locust.client, "")
        self.interactor.login(["", ""])
        self.sites_interactor = _Sites(self.interactor)
        self.task_set.on_start()

        all_sites_str = read_mock_file("all_sites.json")
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/page/news/nav", 200, all_sites_str)

        # Default responses are page responses
        page_resp_json = read_mock_file("page_resp.json")
        self.custom_locust.client.set_default_response(200, page_resp_json)

    def tearDown(self) -> None:
        self.task_set.on_stop()

    def test_sites_get_all(self) -> None:
        page_resp_json = read_mock_file("page_resp.json")
        site_nav_resp = read_mock_file("sites_nav_resp.json")
        all_sites_str = read_mock_file("all_sites.json")
        self.custom_locust.client.enqueue_response(200, all_sites_str, redirected_path="suite/sites/tempo")
        self.custom_locust.client.enqueue_response(200, all_sites_str)
        for i in range(136):
            self.custom_locust.client.enqueue_response(200, site_nav_resp)
            for i in range(5):
                self.custom_locust.client.enqueue_response(200, page_resp_json)

        self.sites_interactor.get_all()
        all_sites = self.sites_interactor._sites
        self.assertEqual(136, len(all_sites.keys()))
        self.assertTrue("rla" in all_sites, "rla not found in list of sites")

        # Spot check
        rla_site = all_sites["rla"]
        self.assertEqual(5, len(rla_site.pages.keys()))
        self.assertEqual(PageType.REPORT, rla_site.pages['create-mrn'].page_type)

    def set_sites_json(self, site_name: str) -> None:
        sites_nav_resp = read_mock_file("sites_nav_resp.json")
        self.custom_locust.set_response(f"/suite/rest/a/sites/latest/{site_name}/nav", 200, sites_nav_resp)

    def test_sites_get(self) -> None:
        site_name = 'mrn'
        self.set_sites_json(site_name)
        site = self.sites_interactor.get_site_data_by_site_name('mrn')
        self.assertEqual('Modern Record News ', site.display_name)

    def test_sites_get_with_invalid_name(self) -> None:
        actual_site_name = 'mrn'
        invalid_site_name = 'oops'
        self.set_sites_json(actual_site_name)
        with self.assertRaises(InvalidSiteException) as e:
            self.sites_interactor.get_site_data_by_site_name(invalid_site_name)
        self.assertEqual(f"JSON response for navigating to site '{invalid_site_name}' was invalid", e.exception.args[0])

    def test_sites_fetch_site_page_metadata(self) -> None:
        site_name = 'mrn'
        page_name = 'foo'

        page_resp = read_mock_file("sites_record_page_resp.json")
        self.custom_locust.set_response(
            f"/suite/rest/a/applications/latest/legacy/sites/{site_name}/page/{page_name}",
            200,
            page_resp)

        page = self.sites_interactor.fetch_site_page_metadata(site_name, page_name)
        self.assertIsNotNone(page)
        assert page
        self.assertEqual(PageType.RECORD, page.page_type)

    def test_sites_fetch_site_page_metadata_for_group(self) -> None:
        site_name = 'mrn'
        page_name = 'foo'
        group_name = "bar"

        page = self.sites_interactor.fetch_site_page_metadata(site_name, page_name, group_name=group_name)
        self.assertIsNotNone(page)
        assert page
        self.assertEqual(PageType.INTERFACE, page.page_type)
        self.assertEqual(group_name, page.group_name)

    def test_sites_fetch_site_page_metadata_missing_redirect(self) -> None:
        site_name = 'mrn'
        page_name = 'foo'

        page_resp = read_mock_file("all_sites.json")
        self.custom_locust.set_response(
            f"/suite/rest/a/applications/latest/legacy/sites/{site_name}/page/{page_name}",
            200,
            page_resp)

        with self.assertRaises(InvalidSiteException) as e:
            self.sites_interactor.fetch_site_page_metadata(site_name, page_name)
        self.assertEqual(f"Could not find page data with a redirect for site {site_name} page {page_name}", e.exception.args[0])

    def test_sites_link_type(self) -> None:
        for type_pair in [('InternalActionLink', 'action'),
                          ('InternalReportLink', 'report'),
                          ('SiteRecordTypeLink', 'recordType'),
                          ('SiteInterfaceLink', 'interface'),
                          ('SiteDataFabricInsightsLink', 'processHQ')]:
            original_link_type = type_pair[0]
            expected_link_type = type_pair[1]
            link_full = f"{{http://www.host.net/ae/types/2009}}{original_link_type}"
            link_type = self.sites_interactor._get_type_from_link_type(link_full)
            self.assertEqual(expected_link_type, link_type.value)

    def test_sites_bad_link_type(self) -> None:
        with self.assertRaises(Exception) as e:
            bad_link_type = "this is garbage"
            self.sites_interactor._get_type_from_link_type(bad_link_type)
        self.assertEqual(f"Invalid Link Type: {bad_link_type}", e.exception.args[0])

    def test_navigate_to_tab_error_cases(self) -> None:
        site_name = "abc"
        self.set_sites_json(site_name)
        self.custom_locust.set_response(f"/suite/rest/a/sites/latest/other_site/nav", 404, "no site found")
        with self.assertRaises(HTTPError):
            self.sites_interactor.fetch_site_tab_json("other_site", "123")
        with self.assertRaises(PageNotFoundException):
            self.sites_interactor.fetch_site_tab_json(site_name, "123")

    def test_navigate_to_tab_success(self) -> None:
        site_name = "abc"
        page_name = "create-mrn"
        link_type = "report"  # Default Page Info

        self.set_sites_json(site_name)

        self.custom_locust.set_response(f"/suite/rest/a/sites/latest/{site_name}/pages/{page_name}/{link_type}",
                                        200,
                                        '{"test":"abc"}')
        tab_resp = self.sites_interactor.fetch_site_tab_json(site_name, page_name)
        self.assertEqual({'test': 'abc'}, tab_resp)

    def test_get_sites_records(self) -> None:
        site_name = "orders"
        page_name = "orders"
        link_type = "recordType"

        nav_resp = read_mock_file("sites_record_nav.json")
        page_resp = read_mock_file("sites_record_page_resp.json")
        record_resp = read_mock_file("sites_record_recordType_resp.json")

        for endpoint in [f"/suite/rest/a/sites/latest/{site_name}/nav",
                         f"/suite/rest/a/sites/latest/{site_name}/pages/{page_name}/nav"]:
            self.custom_locust.set_response(endpoint, 200, nav_resp)

        nav_ui = json.loads(nav_resp)
        mocked_pages_names = ["orders", "new-order", "product-catalogue", "reports", "tasks"]
        for mocked_page_name in mocked_pages_names:
            self.custom_locust.set_response(f"/suite/rest/a/applications/latest/legacy/sites/{site_name}/page/{mocked_page_name}",
                                            200,
                                            page_resp)
        self.custom_locust.set_response(f"/suite/rest/a/sites/latest/{site_name}/pages/{page_name}/{link_type}",
                                        200,
                                        record_resp)

        self.custom_locust.set_default_response(200, record_resp)

        resp = self.sites_interactor.fetch_site_tab_record_json(site_name, page_name)

        self.assertEqual(json.loads(record_resp), resp)

    def test_fetch_site_tab_with_no_records(self) -> None:
        site_name = "orders"
        page_name = "orders"

        nav_resp = read_mock_file("sites_record_nav.json")
        page_resp = read_mock_file("sites_record_page_resp.json")

        for endpoint in [f"/suite/rest/a/sites/latest/{site_name}/nav",
                         f"/suite/rest/a/sites/latest/{site_name}/pages/{page_name}/nav"]:
            self.custom_locust.set_response(endpoint, 200, nav_resp)

        self.custom_locust.set_response(f"/suite/rest/a/applications/latest/legacy/sites/{site_name}/page/{page_name}",
                                        200,
                                        page_resp)

        with self.assertRaises(Exception) as e:
            self.sites_interactor.fetch_site_tab_record_json(site_name, page_name)
        self.assertEqual(f"No records found for site={site_name}, page={page_name}", e.exception.args[0])

    def test_get_sites_process_hq(self) -> None:
        site_name = "ssa-owl"
        page_name = "page1"
        link_type = "processHQ"

        nav_resp = read_mock_file("sites_processHQ_nav.json")
        page_resp = read_mock_file("sites_processHQ_page_resp.json")
        ui_resp = read_mock_file("sites_processHQ_home_resp.json")

        for endpoint in [f"/suite/rest/a/sites/latest/{site_name}/nav",
                         f"/suite/rest/a/sites/latest/{site_name}/pages/{page_name}/nav"]:
            self.custom_locust.set_response(endpoint, 200, nav_resp)

        nav_ui = json.loads(nav_resp)
        self.custom_locust.set_response(
            f"/suite/rest/a/applications/latest/legacy/sites/{site_name}/page/{page_name}", 200, page_resp)
        self.custom_locust.set_response(
            f"/suite/rest/a/sites/latest/{site_name}/pages/{page_name}/{link_type}", 200, ui_resp)
        self.custom_locust.set_default_response(200, ui_resp)

        resp = self.sites_interactor.fetch_site_tab_json(site_name, page_name)

        self.assertEqual(json.loads(page_resp), resp)

    def test_get_all_sites_with_groups(self) -> None:
        site_name = "test_site"
        all_sites_str = read_mock_file("sites_groups_nav.json")
        self.custom_locust.set_response("/suite/", 200, all_sites_str, redirected_path="suite/sites/tempo")
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/nav", 200, all_sites_str)

        nav_resp = all_sites_str
        self.custom_locust.set_response(f"/suite/rest/a/sites/latest/{site_name}/nav", 200, nav_resp)
        page_names = ["test2", "test3", "test4", "test"]
        page_types = ["InternalReportLink", "SiteInterfaceLink", "SiteRecordTypeLink", "InternalActionLink"]
        for idx in range(0, 4):
            page_name = page_names[idx]
            page_response = {
                "redirect": {
                    "#t": page_types[idx]
                }
            }
            self.custom_locust.set_response(f"/suite/rest/a/sites/latest/{site_name}/pages/p.{page_name}/nav", 200, nav_resp)
            self.custom_locust.set_response(f"/suite/rest/a/applications/latest/legacy/sites/{site_name}/page/{page_name}", 200, json.dumps(page_response))

        all_sites = self.sites_interactor.get_all()

        pages = {
            "test2": Page("test2", PageType.REPORT, "test_site"),
            "test3": Page("test3", PageType.INTERFACE, "test_site"),
            "test4": Page("test4", PageType.RECORD, "test_site"),
            "do": Page("do", PageType.INTERFACE, "test_site", "first"),
            "it": Page("it", PageType.INTERFACE, "test_site", "first"),
            "test": Page("test", PageType.ACTION, "test_site"),
        }
        sites = {"test_site": Site("test_site", "Test Site", pages)}
        self.assertEqual(all_sites, sites)

    def test_sites_get_site_page(self) -> None:
        site_name = "abc"
        page_name = "new-order"

        nav_resp = read_mock_file("sites_record_nav.json")
        page_resp = read_mock_file("sites_record_page_resp.json")
        self.custom_locust.set_response(
            f"/suite/rest/a/applications/latest/legacy/sites/{site_name}/page/{page_name}",
            200,
            page_resp)
        for endpoint in [f"/suite/rest/a/sites/latest/{site_name}/nav",
                         f"/suite/rest/a/sites/latest/{site_name}/pages/{page_name}/nav"]:
            self.custom_locust.set_response(endpoint, 200, nav_resp)

        page = self.sites_interactor.get_site_page(site_name, page_name)
        self.assertEqual(page_name, page.page_name)
        self.assertEqual(PageType.RECORD, page.page_type)

    def test_sites_get_site_page_page_not_found(self) -> None:
        site_name = "abc"
        page_name = "does-not-exist"

        nav_resp = read_mock_file("sites_record_nav.json")
        page_resp = read_mock_file("sites_record_page_resp.json")
        self.custom_locust.set_response(
            f"/suite/rest/a/applications/latest/legacy/sites/{site_name}/page/{page_name}",
            200,
            page_resp)
        for endpoint in [f"/suite/rest/a/sites/latest/{site_name}/nav",
                         f"/suite/rest/a/sites/latest/{site_name}/pages/{page_name}/nav"]:
            self.custom_locust.set_response(endpoint, 200, nav_resp)

        with self.assertRaises(PageNotFoundException) as e:
            self.sites_interactor.get_site_page(site_name, page_name)
        self.assertEqual(f"The site with name '{site_name}' does not contain the page {page_name}", e.exception.args[0])


if __name__ == '__main__':
    unittest.main()
