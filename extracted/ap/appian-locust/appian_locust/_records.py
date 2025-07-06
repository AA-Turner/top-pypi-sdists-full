import json
import random
from typing import Any, Dict, Tuple, Optional
from urllib.parse import quote

import requests

from .objects import TEMPO_RECORDS_PAGE
from .utilities import logger

from ._base import _Base
from ._interactor import _Interactor
from ._records_helper import (get_all_records_from_json,
                              get_all_record_types_from_json, get_records_from_json_by_column)

log = logger.getLogger(__name__)

RECORDS_ALL_PATH = "/suite/rest/a/applications/latest/app/records/view/all"
RECORDS_INTERFACE_PATH = "/suite/rest/a/sites/latest/D6JMim/pages/records/interface"
RECORDS_MOBILE_PATH = "/suite/rest/a/applications/latest/legacy/tempo/records/type/"
RECORD_TYPE_VIEW_PATH = "/suite/rest/a/sites/latest/D6JMim/pages/records/recordType/"


class _Records(_Base):
    def __init__(self, interactor: _Interactor, is_mobile_client: bool = False) -> None:
        """
        Records class wrapping list of possible activities can be performed with Appian-Tempo-Records.

        Warnings: This class is internal and should not be accessed by tests directly. It can be accessed via the "appian" object

        Note: "appian" is created as part of ``AppianTaskSet``'s ``on_start`` function

        Args:
            session: Locust session/client object
            host (str): Host URL
            is_mobile_client(bool): If we are running from a mobile client
        """
        self.interactor = interactor

        # When Get All functions called, these variables will be used to cache the values
        self._record_types: Dict[str, Any] = dict()
        self._records: Dict[str, Any] = dict()
        self._errors: int = 0
        self._is_mobile_client = is_mobile_client

    def get_records_interface(self, locust_request_label: Optional[str] = "Records") -> Dict[str, Any]:
        uri = self.interactor.host + RECORDS_INTERFACE_PATH
        headers = self.interactor.setup_sail_headers()
        resp = self.interactor.get_page(uri, headers, f'{locust_request_label}.Interface')
        return resp.json()

    def get_records_nav(self, locust_request_label: Optional[str] = "Records") -> Dict[str, Any]:
        uri = self.interactor.get_url_provider().get_page_nav_path(TEMPO_RECORDS_PAGE)
        headers = self.interactor.setup_sail_headers()
        resp = self.interactor.get_page(uri, headers, f'{locust_request_label}.Nav')
        return resp.json()

    def get_all(self, search_string: Optional[str] = None, locust_request_label: str = "Records") -> Dict[str, Any]:
        """
        Retrieves all available "records types" and "records" and associated metadata from "Appian-Tempo-Records"

        Note: All the retrieved data about record types and records is stored in the private variables
        self._record_types and self._records respectively

        Returns (dict): List of records and associated metadata
        """
        try:
            self.get_records_interface(locust_request_label=locust_request_label)
            self.get_records_nav(locust_request_label=locust_request_label)
        except Exception as e:
            log.error(e)

        if search_string:
            # Format search string to be compatible with URLs
            search_string = quote(search_string)

        self.get_all_record_types(locust_request_label=locust_request_label)
        for record_type in self._record_types:
            try:
                self.get_all_records_of_record_type(record_type, search_string=search_string)
            except requests.exceptions.HTTPError as e:
                log.warning(e)
                continue

        return self._records

    def get_all_record_types(self, locust_request_label: str = "Records") -> Dict[str, Any]:
        """
        Navigate to Tempo Records Tab and load all metadata for associated list of record types into cache.

        Returns (dict): List of record types and associated metadata
        """

        json_response = self.fetch_all_records_json(locust_request_label)

        self._record_types = get_all_record_types_from_json(json_response)

        return self._record_types

    def fetch_all_records_json(self, locust_request_label: str = "Records") -> Dict[str, Any]:
        uri = RECORDS_ALL_PATH

        headers = self.interactor.setup_request_headers()
        headers['X-Appian-Features-Extended'] = 'e4bc'
        headers["Accept"] = "application/vnd.appian.tv.ui+json"
        response = self.interactor.get_page(uri=uri, headers=headers, label=locust_request_label)
        if not (self._is_response_good(response.text)):
            raise (Exception("Unexpected response on Get call of All Records"))
        return response.json()

    def get_all_records_of_record_type(self, record_type: str, column_index: Optional[int] = None, search_string: Optional[str] = None) -> Dict[str, Any]:
        """
        Navigate to the desired record type and load all metadata for the associated list of record views into cache.

        Args:
            record_type (str): Name of record type for which we want to enumerate the record instances.
            column_index (int, optional): Column index to only fetch record links from a specific column, starts at 0.

        Returns (dict): List of records and associated metadata

        Examples:

            >>> self.appian.records.get_all_records_of_record_type("record_type_name")
        """
        self._records[record_type] = dict()

        json_response = self._record_type_list_request(record_type, search_string=search_string, is_mobile=self._is_mobile_client)

        if column_index is not None:
            self._records[record_type], self._errors = get_records_from_json_by_column(json_response, column_index)
        else:
            self._records[record_type], self._errors = get_all_records_from_json(json_response)

        return self._records

    def fetch_record_instance(self, record_type: str, record_name: str, exact_match: bool = True) -> Dict[str, Any]:
        """
        Get the information about a specific record by specifying its name and its record type.

        Args:
            record_type (str): Name of the record type.
            record_name (str): Name of the record which should be available in the given record type
            exact_match (bool): Should record name match exactly or to be partial match. Default : True

        Returns (dict): Specific record's info

        Raises: In case of record is not found in the system, it throws an "Exception"

        Example:
            If full name of record type and record is known,

            >>> self.appian.records.get("record_type_name", "record_name")

            If only partial name is known,

            >>> self.appian.records.get("record_type_name", "record_name", exact_match=False)

        """

        self.fetch_record_type(record_type, exact_match=exact_match)
        _, current_record = super().get(self._records[record_type], record_name, exact_match,
                                        ignore_retry=True)
        if not current_record:
            self.get_all(search_string=record_name)
            _, current_record = super().get(self._records[record_type], record_name, exact_match,
                                            ignore_retry=True)
        if not current_record:
            raise Exception(f"There is no record with name {record_name} found in record type {record_type} (Exact match = {exact_match})")
        return current_record

    get_record = fetch_record_instance

    def fetch_record_type(self, record_type: str, exact_match: bool = True) -> Dict[str, Any]:
        """
            Fetch information about record type from the cache. Raises Exception if record type does not exist in cache.

        Args:
            record_type (str): Name of the record type.


        Returns (dict): Specific record type's info

        Raises: In case the record type is not found in the system, it throws an "Exception"

        Example:

            >>> self.appian.records.get_record_type("record_type_name")

        """
        _, current_record_type = super().get(self._record_types, record_type, exact_match)
        if not current_record_type:
            raise Exception(f"There is no record type with name {record_type} in the system under test (Exact match = {exact_match})")
        return current_record_type

    def visit_record_instance(self, record_type: str = "", record_name: str = "", view_url_stub: str = "", exact_match: bool = True, locust_request_label: Optional[str] = None) -> Dict[str, Any]:
        """
        This function calls the API for the specific record view/instance to get its response data.

        Note: This function is meant to only traverse to Record forms, not to interact with them. For that, use visit_record_instance_and_get_form()

        Args:
            record_type (str): Record Type Name. If not specified, a random record type will be selected.
            record_name (str): Name of the record to be called. If not specified, a random record will be selected.
            view_url_stub (str, optional): page/tab to be visited in the record. If not specified, "summary" dashboard will be selected.
            exact_match (bool, optional): Should record type and record name matched exactly as it is or partial match.
            locust_request_label(str,optional): Label used to identify the request for locust statistics

        Returns (dict): Responses of Record's Get UI call in a dictionary

        Examples:

            If full name of record type and record is known,

            >>> self.appian.records.visit_record_instance("record_type_name", "record_name", "summary")

            If only partial name is known,

            >>> self.appian.records.visit_record_instance("record_type_name", "record_name", "summary", exact_match=False)

            If a random record is desired,

            >>> self.appian.records.visit_record_instance()

            If random record of a specific record type is desired,

            >>> self.appian.records.visit_record_instance("record_type_name")

        """

        if not record_name:
            record_type, record_name = self._get_random_record_instance(record_type)
            # remove id from record name
            record_name = record_name.split("::")[0]

        if not record_type:
            raise Exception("If record_name parameter is specified, record_type must also be included")

        current_record = self.fetch_record_instance(record_type, record_name, exact_match)

        headers = self.interactor.setup_feed_headers()

        tempo_site_url_stub = current_record["siteUrlStub"]
        opaque_id = current_record["_recordRef"]
        record_label = current_record["label"]

        if not view_url_stub:
            dashboard_val = current_record.get("dashboard")
            view_url_stub = dashboard_val if dashboard_val else "summary"

        locust_label = locust_request_label or f'Records.{record_type}.{record_label}.{view_url_stub}'
        uri = self.interactor.get_url_provider().get_record_path(TEMPO_RECORDS_PAGE, opaque_id, view_url_stub)
        resp = self.interactor.get_page(uri=uri, headers=headers, label=locust_label)
        return resp.json()

    # Alias for the above function to allow backwards compatability
    visit = visit_record_instance

    def visit_record_type(self, record_type: str = "", locust_request_label: Optional[str] = None) -> Dict[str, Any]:
        """
        Navigate into desired record type and retrieve all metadata for associated list of record views.

        Returns (dict): List of records and associated metadata

        Examples:

            >>> self.appian.records.visit_record_type("record_type_name")
        """

        # Make sure caches are not empty
        if not self._records or not self._record_types:
            self.get_all()

        # If no record_type is specified, a random one will be assigned
        if not record_type:
            record_type = self._get_random_record_type()

        locust_request_label = locust_request_label or f'Records.{record_type}.ListView'

        return self._record_type_list_request(record_type, is_mobile=self._is_mobile_client, locust_request_label=locust_request_label)

    # ----- Private Functions ----- #

    def _is_response_good(self, response_text: str) -> bool:
        return ('"rel":"x-web-bookmark"' in response_text or '"#t":"CardLayout"' in response_text)

    def _get_random_record_instance(self, record_type: str = "") -> Tuple[str, str]:
        if not self._records or not self._record_types:
            self.get_all()
        if not record_type:
            record_type = self._get_random_record_type()
        record_name = random.choice(list(self._records[record_type].keys()))
        return record_type, record_name

    def _get_random_record_type(self) -> str:
        if not self._records or not self._record_types:
            self.get_all()
        return random.choice(list(self._records.keys()))

    def _record_type_list_request(self, record_type: str, is_mobile: bool = False, search_string: Optional[str] = None,
                                  locust_request_label: Optional[str] = None) -> Dict[str, Any]:
        if record_type not in self._record_types:
            raise Exception(f"There is no record type with name {record_type} in the system under test")
        record_type_component = self._record_types[record_type]
        record_type_url_stub = record_type_component['link']['value']['urlstub']
        locust_request_label = locust_request_label or f"Records.{record_type}"
        return self.fetch_record_type_json(record_type_url_stub, is_mobile, search_string, locust_request_label)

    def fetch_record_type_json(self, record_type_url_stub: str, is_mobile: bool = False, search_string: Optional[str] = None, label: Optional[str] = None) -> Dict[str, Any]:
        if not label:
            label = f"Records.{record_type_url_stub}"
        if is_mobile:
            uri = self._get_mobile_records_uri(record_type_url_stub)
        else:
            uri = f"{RECORD_TYPE_VIEW_PATH}{record_type_url_stub}"
            if search_string:
                uri = f"{uri}?searchTerm={search_string}"
        headers = self.interactor.setup_request_headers()
        headers["Accept"] = "application/vnd.appian.tv.ui+json"
        response = self.interactor.get_page(uri=uri, headers=headers, label=label)
        json_response = response.json()

        return json_response

    def _get_mobile_records_uri(self, record_type_url_stub: str, search_string: Optional[str] = None) -> str:
        if not record_type_url_stub:
            raise Exception("Mobile records uri must have a unique stub provided.")
        uri = f"{RECORDS_MOBILE_PATH}{record_type_url_stub}"
        if search_string:
            return f"{uri}/search/{search_string}"
        return f"{uri}/view/all"
