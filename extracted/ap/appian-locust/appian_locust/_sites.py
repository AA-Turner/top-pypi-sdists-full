import enum
import random
from typing import Any, Dict, List, Union, Optional

from .utilities import logger
from ._base import _Base
from ._interactor import _Interactor
from .utilities.helper import extract_values, format_label
from .objects import TEMPO_NEWS_PAGE, TEMPO_SITE_STUB
from ._records_helper import get_all_records_from_json
from .objects import Site, Page, PageType
from .exceptions import (PageNotFoundException,
                         InvalidSiteException,
                         SiteNotFoundException)

log = logger.getLogger(__name__)


class _Sites(_Base):
    BROWSER_ACCEPT_HEADER = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"

    def __init__(self, interactor: _Interactor) -> None:
        """
        Sites class wrapping a list of possible activities that can be performed with the Appian Sites Environment

        Warnings: This class is internal and should not be accessed by tests directly. It can be accessed via the "appian" object

        Note: "appian" is created as part of ``AppianTaskSet``'s ``on_start`` function

        Args:
            session: Locust session/client object
            host (str): Host URL

        """
        self.interactor = interactor

        self._sites: Dict[str, Site] = {}
        self._sites_records: Dict[str, Dict[str, Any]] = {}

    def fetch_site_tab_json(self, site_name: str, page_name: str, locust_request_label: Optional[str] = None) -> Dict[str, Any]:
        """
        Navigates to a site page, either a record, action or report.

        Args:
            site_name: Site Url stub
            page_name: Page Url stub
            locust_request_label (str, optional): Label locust should associate this request with

        Returns: Response of report/action/record
        """

        page = self.get_site_page(site_name, page_name)
        headers = self._setup_headers_with_sail_json()

        nav_uri = self.interactor.get_url_provider().get_page_nav_path(page)

        locust_label = locust_request_label or f"Sites.{site_name}.{page_name}"
        self.interactor.get_page(nav_uri, headers=headers, label=f"{locust_label}.Nav")
        page_url = self.interactor.get_url_provider().get_page_path(page)
        resp = self.interactor.get_page(page_url, headers=headers, label=f"{locust_label}.Ui")
        return resp.json()

    def fetch_site_tab_record_json(self, site_name: str, page_name: str, locust_request_label: Optional[str] = None) -> Dict[str, Any]:
        """
        Navigate to a recordList page on a site, then grab a random page from that site

        Note: Any record available in the record list as a recordLink will be hit using this function.  There is no
        guarantee that this record will be of any specific type and may not point to a record view.

        Args:
            site_name: Site Url stub
            page_name: Page Url stub
            locust_request_label (str, optional): Label locust should associate this request with

        Returns: Response of report/action, or in the case of a record, response of record object
        """
        resp_json = self.fetch_site_tab_json(site_name, page_name)
        if not self._sites[site_name].pages[page_name].page_type == PageType.RECORD:
            raise Exception(f"Page {page_name} on site {site_name} is not of type record")
        headers = self._setup_headers_with_sail_json()
        if page_name not in self._sites_records:
            records_for_page, errors = get_all_records_from_json(resp_json)
            self._sites_records[page_name] = records_for_page
        records = list(self._sites_records[page_name])
        if not records:
            raise Exception(f"No records found for site={site_name}, page={page_name}")
        record_key = random.choice(list(self._sites_records[page_name]))
        label = locust_request_label or f"Sites.{site_name}.{page_name}." + format_label(record_key, "::", 0)[:30]
        record_id = record_key.split("::")[1]
        page = self.get_site_page(site_name, page_name)

        page_nav_url = self.interactor.get_url_provider().get_page_nav_path(page)
        record_resp = self.interactor.get_page(
            page_nav_url,
            headers=headers,
            label=label + ".Nav")
        # TODO: Add ability to go to arbitrary stubs
        headers = self.interactor.setup_feed_headers()
        record_url = self.interactor.get_url_provider().get_record_path(page, record_id, "summary")
        record_resp = self.interactor.get_page(
            record_url,
            headers=headers,
            label=label + ".View")
        return record_resp.json()

    def get_all(self, search_string: Optional[str] = None, locust_request_label: Optional[str] = None) -> Dict[str, Any]:
        """
        Gets and stores data for all sites, including all of their url stubs
        """
        all_site_stubs = self.get_site_stubs()
        for site_url_stub in all_site_stubs:
            self.get_site_data_by_site_name(site_url_stub)
        return self._sites

    def get_site_stubs(self) -> List[str]:
        redirect_resp = self.interactor.get_page("/suite/")
        # Redirect is handled automatically, so we need to look at the url the response was sent to
        redirect_location: str = redirect_resp.request.path_url
        if "tempo" in redirect_location:
            landing_site_stub = TEMPO_SITE_STUB
        else:
            landing_site_stub = redirect_location.split("/")[-1]

        landing_site_nav_url = self.interactor.get_url_provider().get_site_nav_path(landing_site_stub)
        headers = self._setup_headers_with_sail_json()
        all_site_resp = self.interactor.get_page(landing_site_nav_url, headers=headers, label="Sites.SiteNames")
        all_site_json = all_site_resp.json()
        all_site_stubs = []
        for site_info in extract_values(all_site_json, '#t', 'SitePageLink'):
            if 'siteUrlStub' in site_info:
                all_site_stubs.append(site_info["siteUrlStub"])
        if landing_site_stub != TEMPO_SITE_STUB:
            all_site_stubs.append(landing_site_stub)
        return all_site_stubs

    def get_site_data_by_site_name(self, site_name: str) -> Site:
        """
        Gets site data from just the site url stub

        Args:
            site_name: Site url stub
        Returns: Site object, containing the site name and pages
        """
        headers = self._setup_headers_with_accept()
        # First get site pages
        initial_nav_resp = self.interactor.get_page(self.interactor.get_url_provider().get_site_nav_path(site_name),
                                                    headers=headers,
                                                    label=f"Sites.{site_name}.Nav")
        initial_nav_json = initial_nav_resp.json()
        ui = initial_nav_json['ui']

        display_name = ui.get('siteName')

        # Invalid case
        if not display_name:
            raise InvalidSiteException(f"JSON response for navigating to site '{site_name}' was invalid")

        site = self._get_and_memoize_site_data_from_ui(initial_nav_json, site_name, display_name)
        return site

    def fetch_site_page_metadata(self, site_name: str, page_name: str, group_name: Optional[str] = None) -> Union['Page', None]:
        """
        Gets site page from the site url stub and page url stub

        Args:
            site_name: Site url stub
            page_name: Page url stub
            group_name: Group url stub, if there is one
        Returns: Page object, representing an individual page of a site
        """
        # Group pages can only be interfaces
        if group_name:
            return Page(page_name, PageType.INTERFACE, site_name, group_name)
        headers = self._setup_headers_with_sail_json()
        headers['X-Appian-Features-Extended'] = 'e4bc'  # Required by legacy url to return successfully
        url = self.interactor.get_url_provider().get_site_page_redirect_path(site_name, page_name)
        page_resp = self.interactor.get_page(url, headers=headers, label=f"Sites.{site_name}.{page_name}.Nav")
        page_resp_json = page_resp.json()
        if 'redirect' not in page_resp_json:
            raise InvalidSiteException(f"Could not find page data with a redirect for site {site_name} page {page_name}")
        link_type_raw = page_resp_json['redirect']['#t']
        page_type = self._get_type_from_link_type(link_type_raw)
        return Page(page_name, page_type, site_name, group_name)

    def get_site_page(self, site_name: str, page_name: str) -> 'Page':
        if site_name not in self._sites:
            self.get_site_data_by_site_name(site_name)

        if site_name not in self._sites:
            raise SiteNotFoundException(f"The site with name '{site_name}' could not be found")
        site: Site = self._sites[site_name]
        if page_name not in [page.page_name for page in site.pages.values()]:
            raise PageNotFoundException(f"The site with name '{site_name}' does not contain the page {page_name}")
        return site.pages[page_name]

    def get_site_page_type(self, site_name: str, page_name: str) -> 'PageType':
        page = self.get_site_page(site_name, page_name)
        return page.page_type

    def _get_and_memoize_site_data_from_ui(self, initial_nav_json: Dict[str, Any], site_name: str, display_name: str) -> 'Site':
        ui = initial_nav_json.get("ui", {})
        pages = {}
        for tab in ui.get("tabs", []):
            if tab.get("isGroup"):
                for child in tab.get("children", []):
                    page = self._get_page_from_json(site_name, child)
                    if page:
                        pages[page.page_name] = page
            else:
                page = self._get_page_from_json(site_name, tab)
                if page:
                    pages[page.page_name] = page

        site = Site(site_name, display_name, pages)
        self._sites[site_name] = site
        return site

    def _get_page_from_json(self, site_name: str, page_info_json: Dict[str, Any]) -> Optional[Page]:
        group_name = page_info_json['link'].get('groupUrlStub')
        page_name = page_info_json['link']['pageUrlStub']
        return self.fetch_site_page_metadata(site_name=site_name, page_name=page_name, group_name=group_name if group_name else None)

    def _get_type_from_link_type(self, link_type: str) -> 'PageType':
        if "InternalActionLink" in link_type:
            return PageType.ACTION
        elif "InternalReportLink" in link_type:
            return PageType.REPORT
        elif "SiteRecordTypeLink" in link_type:
            return PageType.RECORD
        elif "SiteInterfaceLink" in link_type:
            return PageType.INTERFACE
        else:
            raise Exception(f"Invalid Link Type: {link_type}")

    def _setup_headers_with_accept(self) -> dict:
        headers = self.interactor.setup_request_headers()
        headers["Accept"] = self.BROWSER_ACCEPT_HEADER
        return headers

    def _setup_headers_with_sail_json(self) -> dict:
        headers = self.interactor.setup_sail_headers()
        headers["Accept"] = "application/vnd.appian.tv.ui+json"
        return headers
