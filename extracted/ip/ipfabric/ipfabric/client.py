import json
import logging
import re
from datetime import datetime
from typing import Optional, Any, Union, Literal, overload

from httpx import InvalidURL, URL
from pydantic import ConfigDict, BaseModel

from ipfabric.api import IPFabricAPI, check_deprecated
from ipfabric.diagrams import Diagram
from ipfabric.models import Technology, Inventory, Jobs, Intent, Devices, Extensions
from ipfabric.models.oas import Methods
from ipfabric.settings import Settings
from ipfabric.tools import TIMEZONES, raise_for_status, valid_snapshot

try:
    from pandas import DataFrame
except ImportError:
    DataFrame = None

logger = logging.getLogger("ipfabric")

RE_TABLE = re.compile(r"^tables/")
EXPORT_FORMAT = Literal["json", "csv", "df"]


class IPFClient(IPFabricAPI, BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    _inventory: Optional[Inventory] = None
    _technology: Optional[Technology] = None
    _jobs: Optional[Jobs] = None
    _diagram: Optional[Diagram] = None
    _intent: Optional[Intent] = None
    _devices: Optional[Devices] = None
    _settings: Optional[Settings] = None
    _last_snapshot_update: Optional[datetime] = None
    _extensions: Optional[Extensions] = None

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(self)
        self._inventory = Inventory(client=self)
        self._technology = Technology(client=self)
        self._jobs = Jobs(client=self)
        self._diagram = Diagram(ipf=self)
        self._intent = Intent(client=self)
        self._settings = Settings(client=self)
        self._extensions = Extensions(client=self)

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "timeout":
            self._client.timeout = value
        elif name == "snapshot_id":
            value = self._switch_snapshot(value)
            self.__dict__[name] = value
            if value and self.snapshot.disabled_intent_verification is False and self._intent:
                self._intent = Intent(client=self)
            if value and self._devices:
                self._devices = self.load_devices(device_attr_filters=self.attribute_filters)
            return None
        super().__setattr__(name, value)
        if name == "_attribute_filters" and self._devices:
            self._devices = self.load_devices(device_attr_filters=self.attribute_filters)

    def __repr__(self):
        return f"IPFClient(base_url='{str(self.base_url)}')"

    @property
    def inventory(self) -> Inventory:
        return self._inventory

    @property
    def technology(self) -> Technology:
        return self._technology

    @property
    def jobs(self) -> Jobs:
        return self._jobs

    @property
    def diagram(self) -> Diagram:
        return self._diagram

    @property
    def intent(self) -> Intent:
        return self._intent

    @property
    def settings(self) -> Settings:
        return self._settings

    @property
    def devices(self) -> Devices:
        """get devices"""
        if not self._devices:
            logger.info("Devices not loaded, loading devices.")
            self._devices = self.load_devices(device_attr_filters=self.attribute_filters)
        return self._devices

    @devices.setter
    def devices(self, devices: Devices):
        self._devices = devices

    @property
    def extensions(self) -> Extensions:
        return self._extensions

    def update(self) -> None:
        self._snapshots.update()
        if self.snapshot_id not in self.loaded_snapshots:
            logger.warning(f"Snapshot {self.snapshot_id} is no longer loaded switching to `$last`.")
            self.snapshot_id = "$last"

    def load_devices(self, device_filters: dict = None, device_attr_filters: dict = None) -> Devices:
        if device_attr_filters:
            logger.warning(
                f"Global Attribute Filter is applied, only returning devices matching: {self.attribute_filters}."
            )
        devices = Devices(
            client=self,
            snapshot_id=self.snapshot_id,
            device_filters=device_filters,
            device_attr_filters=device_attr_filters,
        )
        return devices

    def _create_payload(
        self,
        url: str,
        snapshot_id: Optional[str],
        filters: Optional[dict],
        sort: Optional[dict],
        attr_filters: Optional[dict],
    ) -> dict:
        """Optimized payload creation with reduced conditionals"""
        payload = {
            "format": {"dataType": "json"},
            "filters": filters or {},
            "sort": sort or {},
        }

        if snapshot_id:
            payload["snapshot"] = snapshot_id

        if RE_TABLE.match(url) and (attr_filters or self.attribute_filters):
            payload["attributeFilters"] = attr_filters or self.attribute_filters

        return payload

    def _check_url_payload(self, url, snapshot_id, filters, reports, sort, attr_filters, export, csv_tz):
        url = self._check_url(url)
        payload = self._create_payload(url, snapshot_id, filters, sort, attr_filters)
        oas_data = self.oas.get(url, Methods(full_api_endpoint="")).post

        if export != "csv":
            if isinstance(reports, (str, list)):
                payload["reports"] = reports
            elif reports is True and oas_data and oas_data.web_endpoint:
                payload["reports"] = oas_data.web_endpoint
            elif reports is True and (not oas_data or not oas_data.web_endpoint):
                logger.warning(
                    f"Could not automatically discover Web Endpoint for Intent Data for table '/{url}'.\n"
                    f"Returning results without Intent Rules."
                )
        else:
            if reports:
                logger.warning("CSV export does not return reports, parameter has been excluded.")
            payload["format"] = {"exportToFile": True, "dataType": "csv"}
            if csv_tz and csv_tz.lower() not in TIMEZONES:
                raise ValueError(
                    f"CSV timezone '{csv_tz}' not in available timezones; see `ipfabric.tools.shared.TIMEZONES`"
                )
            elif csv_tz:
                payload["format"]["options"] = {"timezone": TIMEZONES[csv_tz.lower()]}
        return url, payload

    def _get_payload(self, url, payload) -> Union[str, bool]:
        snapshot_id = payload.pop("snapshot", None)
        reports = payload.pop("reports") if "reports" in payload and isinstance(payload["reports"], str) else None
        p = "&".join([f"{k}={json.dumps(v, separators=(',', ':'))}" for k, v in payload.items()])
        if snapshot_id:
            p += f"&snapshot={snapshot_id}"
        if reports:
            p += f"&reports={reports}"
        url = self.base_url.join(url + f"?{p}")
        if len(str(url)) > 4096:
            return False
        return url

    @check_deprecated("post")
    def _stream(self, url, payload, export):
        get_url = self._get_payload(url, payload)
        if get_url is False and export == "csv":
            raise InvalidURL("URL exceeds max character limit of 4096 cannot export to CSV.")
        elif get_url is False:
            logger.warning("URL exceeds max character limit of 4096 switching to pagination.")
            return False
        with self.stream("GET", get_url) as stream_resp:
            data = stream_resp.read()
            raise_for_status(stream_resp)
        return data if export == "csv" else json.loads(data)["data"]

    def query(self, url: str, payload: Union[str, dict], get_all: bool = True) -> Union[list[dict], bytes]:
        """Submits a query, does no formatting on the parameters.  Use for copy/pasting from the webpage.

        Args:
            url: Example: https://demo1.ipfabric.io/api/v1/tables/vlan/device-summary or tables/vlan/device-summary
            payload: Dictionary to submit in POST or can be JSON string (i.e. read from file).
            get_all: Default use pager to get all results and ignore pagination information in the payload

        Returns:
            list or bytes: List of Dictionary objects or bytes if csv.
        """
        url = self._check_url(url)
        if isinstance(payload, str):
            payload = json.loads(payload)
        export = payload.get("format", {}).get("dataType", "json")
        data = False
        if export == "csv" or (self.streaming and get_all):
            data = self._stream(url, payload, export)
        elif get_all and data is False:
            data = list(self._ipf_pager(url, payload))
        elif data is False:
            res = raise_for_status(self.post(url, json=payload))
            data = res.json()["data"]
        return data

    def get_columns(self, url: str, ui: bool = False) -> list[str]:
        """Checks OAS to find available columns.

        Args:
            url: API url to post
            ui: True to return columns available in the UI, default False

        Returns:
            list: List of column names
        """
        ctype = "ui_columns" if ui else "columns"
        oas_data = getattr(self.oas.get(url, {}), "post", None)
        if oas_data and getattr(oas_data, ctype):
            return getattr(oas_data, ctype)
        raise LookupError(f"Could not find {'UI' if ui else 'API'} columns for table '/{url}'.")

    def get_count(
        self,
        url: str,
        filters: Optional[Union[dict, str]] = None,
        attr_filters: Optional[dict[str, list[str]]] = None,
        snapshot_id: Optional[str] = None,
        snapshot: bool = True,
        reports: Optional[Union[bool, list, str]] = False,
    ) -> int:
        """Get a total number of rows
        Args:
            url: API URL to post to
            filters: Optional dictionary of filters
            attr_filters: Optional dictionary of attribute filters
            snapshot_id: Optional snapshot_id to override default
            snapshot: Set to False for some tables like management endpoints.
            reports: Boolean to return default reports, string of frontend URL where the reports are displayed,
                     or a list of report IDs
        Returns:
            int: a count of rows
        """
        snapshot_id = snapshot_id or self.snapshot_id if snapshot else None
        url, payload = self._fetch_setup(
            url, "json", None, snapshot_id, filters, reports, None, attr_filters, None, snapshot
        )
        payload.update({"columns": ["id"], "pagination": {"limit": 1, "start": 0}})
        res = raise_for_status(self.post(url, json=payload))
        return res.json()["_meta"]["count"]

    def _fetch_setup(self, url, export, columns, snapshot_id, filters, reports, sort, attr_filters, csv_tz, snapshot):
        if export == "df" and DataFrame is None:
            raise ImportError("pandas not installed. Run `pip install ipfabric[pd]`.")
        snapshot_id = snapshot_id or self.snapshot_id if snapshot else None
        if filters:
            filters = json.loads(filters) if isinstance(filters, str) else filters
        if "color" in json.dumps(filters) and not reports:
            reports = True
        url, payload = self._check_url_payload(url, snapshot_id, filters, reports, sort, attr_filters, export, csv_tz)
        payload["columns"] = self.get_columns(url) if not columns else list(columns)
        cols = set(payload["columns"])
        oas_data = self.oas.get(url, Methods(full_api_endpoint="")).post
        if oas_data and cols.intersection(oas_data.deprecated_columns):
            logger.warning(
                f"API columns '{cols.intersection(oas_data.deprecated_columns)}' for endpoint "
                f"'/{oas_data.api_endpoint}' are marked deprecated in the OpenAPI specification."
            )
        return url, payload

    @overload
    def fetch(
        self,
        url,
        export: Literal["json"] = ...,
        columns: Optional[Union[list[str], set[str]]] = None,
        filters: Optional[Union[dict, str]] = None,
        limit: Optional[int] = 1000,
        start: Optional[int] = 0,
        snapshot_id: Optional[str] = None,
        reports: Optional[Union[bool, list, str]] = False,
        sort: Optional[dict] = None,
        attr_filters: Optional[dict[str, list[str]]] = None,
        snapshot: bool = True,
    ) -> list[dict]: ...

    @overload
    def fetch(
        self,
        url,
        export: Literal["csv"],
        columns: Optional[Union[list[str], set[str]]] = None,
        filters: Optional[Union[dict, str]] = None,
        limit: Optional[int] = 1000,
        start: Optional[int] = 0,
        snapshot_id: Optional[str] = None,
        sort: Optional[dict] = None,
        attr_filters: Optional[dict[str, list[str]]] = None,
        snapshot: bool = True,
        csv_tz: Optional[str] = None,
    ) -> bytes: ...

    @overload
    def fetch(
        self,
        url,
        export: Literal["df"] = ...,
        columns: Optional[Union[list[str], set[str]]] = None,
        filters: Optional[Union[dict, str]] = None,
        limit: Optional[int] = 1000,
        start: Optional[int] = 0,
        snapshot_id: Optional[str] = None,
        reports: Optional[Union[bool, list, str]] = False,
        sort: Optional[dict] = None,
        attr_filters: Optional[dict[str, list[str]]] = None,
        snapshot: bool = True,
    ) -> DataFrame: ...

    def fetch(
        self,
        url,
        export: EXPORT_FORMAT = "json",
        columns: Optional[Union[list[str], set[str]]] = None,
        filters: Optional[Union[dict, str]] = None,
        limit: Optional[int] = 1000,
        start: Optional[int] = 0,
        snapshot_id: Optional[str] = None,
        reports: Optional[Union[bool, list, str]] = False,
        sort: Optional[dict] = None,
        attr_filters: Optional[dict[str, list[str]]] = None,
        snapshot: bool = True,
        csv_tz: Optional[str] = None,
    ):
        """Gets data from IP Fabric for specified endpoint

        Args:
            url: Example tables/vlan/device-summary
            export: str: Export format to return [json, csv]; default is json.
            columns: Optional list of columns to return, None will return all
            filters: Optional dictionary of filters
            limit: Default to 1,000 rows
            start: Starts at 0
            snapshot_id: Optional snapshot_id to override default
            reports: Boolean to return default reports, string of frontend URL where the reports are displayed,
                     or a list of report IDs
            sort: Dictionary to apply sorting: {"order": "desc", "column": "lastChange"}
            attr_filters: Optional dictionary to apply an Attribute filter
            snapshot: Set to False for some tables like management endpoints.
            csv_tz: str: Default None, set a timezone to return human-readable dates when using CSV;
                         see `ipfabric.tools.shared.TIMEZONES`
        Returns:
            Union[list[dict], bytes, pandas.DataFrame]: List of dict if json, bytes string if CSV, DataFrame is df
        """
        url, payload = self._fetch_setup(
            url, export, columns, snapshot_id, filters, reports, sort, attr_filters, csv_tz, snapshot
        )
        payload["pagination"] = dict(start=start, limit=limit)
        data = False
        if export == "csv" or self.streaming:
            data = self._stream(url, payload, export)
        if data is False:
            res = raise_for_status(self.post(url, json=payload))
            data = res.json()["data"]
        if export == "df":
            data = DataFrame.from_records(data) if export == "df" else data
        return data

    @overload
    def fetch_all(
        self,
        url: str,
        export: Literal["json"] = ...,
        columns: Optional[Union[list[str], set[str]]] = None,
        filters: Optional[Union[dict, str]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[Union[bool, list, str]] = False,
        sort: Optional[dict] = None,
        attr_filters: Optional[dict[str, list[str]]] = None,
        snapshot: bool = True,
    ) -> list[dict]: ...

    @overload
    def fetch_all(
        self,
        url: str,
        export: Literal["csv"],
        columns: Optional[Union[list[str], set[str]]] = None,
        filters: Optional[Union[dict, str]] = None,
        snapshot_id: Optional[str] = None,
        sort: Optional[dict] = None,
        attr_filters: Optional[dict[str, list[str]]] = None,
        snapshot: bool = True,
        csv_tz: Optional[str] = None,
    ) -> bytes: ...

    @overload
    def fetch_all(
        self,
        url: str,
        export: Literal["df"],
        columns: Optional[Union[list[str], set[str]]] = None,
        filters: Optional[Union[dict, str]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[Union[bool, list, str]] = False,
        sort: Optional[dict] = None,
        attr_filters: Optional[dict[str, list[str]]] = None,
        snapshot: bool = True,
    ) -> DataFrame: ...

    def fetch_all(
        self,
        url: str,
        export: EXPORT_FORMAT = "json",
        columns: Optional[Union[list[str], set[str]]] = None,
        filters: Optional[Union[dict, str]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[Union[bool, list, str]] = False,
        sort: Optional[dict] = None,
        attr_filters: Optional[dict[str, list[str]]] = None,
        snapshot: bool = True,
        csv_tz: Optional[str] = None,
    ):
        """Gets all data from IP Fabric for specified endpoint

        Args:
            url: Example tables/vlan/device-summary
            export: str: Export format to return [json, csv]; default is json.
            columns: Optional list of columns to return, None will return all
            filters: Optional dictionary of filters
            snapshot_id: Optional snapshot_id to override default
            reports: Boolean to return default reports, string of frontend URL where the reports are displayed,
                     or a list of report IDs
            sort: Optional dictionary to apply sorting: {"order": "desc", "column": "lastChange"}
            attr_filters: Optional dictionary to apply an Attribute filter
            snapshot: Set to False for some tables like management endpoints.
            csv_tz: str: Default None, set a timezone to return human-readable dates when using CSV;
                         see `ipfabric.tools.shared.TIMEZONES`
        Returns:
            Union[list[dict], bytes, pandas.DataFrame]: List of dict if json, bytes string if CSV, DataFrame is df
        """
        url, payload = self._fetch_setup(
            url, export, columns, snapshot_id, filters, reports, sort, attr_filters, csv_tz, snapshot
        )
        data = False
        if export == "csv" or self.streaming:
            data = self._stream(url, payload, export)
        if data is False:
            data = list(self._ipf_pager(url, payload))
        if export == "df":
            data = DataFrame.from_records(data)
        return data

    def _shared_url(self, url: Union[int, str], table: bool = True) -> tuple[dict, str]:
        snapshot = None
        try:
            url_id = str(int(url))
        except ValueError:
            parsed_url = URL(url)
            snapshot = parsed_url.params.get("selectSnapshot", None)
            if table and parsed_url.params.get("copyId"):
                url_id = parsed_url.params.get("copyId")
            elif not table:
                url_id = parsed_url.path.split("/")[-1]
            else:
                raise SyntaxError("Wrong endpoint selected.")
        if table:
            resp = self.get(f"/tables/url/{url_id}")
        else:
            resp = self.get(f"/graphs/urls/{url_id}")
        return raise_for_status(resp).json(), snapshot

    def shared_view(self, url: Union[int, str], data=True, reports: bool = True) -> Union[str, list]:
        """Takes a shared table view link and returns the data or the code to implement in python.

        Args:
            url: Id of the shared view (1453653298) or full/partial URL (`/inventory/devices?copyId=1453653298`)
            data: Defaults to return the data instead of printing the code
            reports: True to return Intent Verification data

        Returns: List of dictionaries of the data or a string representing the code.
        """
        query, snapshot = self._shared_url(url, True)
        url = self.web_to_api[query["webEndpoint"]].api_endpoint
        hidden = {k for k, v in query.get("columnVisibility", {}).items() if not v}
        columns = {k for k, v in query.get("columnVisibility", {}).items() if v}
        columns.update({_ for _ in query.get("columnWidth", {}) if _ not in hidden})
        columns.update({_ for _ in self.get_columns(url, ui=True) if _ not in hidden})
        columns = sorted(list(columns))

        filters, sort = query.get("filters", {}), query.get("sort", {})
        filters.pop("selectedFilter", None)

        if data:
            return self.fetch_all(
                url=url,
                columns=columns,
                filters=filters,
                sort=sort,
                reports=query["webEndpoint"] if reports else False,
                snapshot_id=snapshot if snapshot else self.snapshot_id,
            )
        code = f"{url.split('/')[-1]} = ipf.fetch_all(\n    {url=},\n    {columns=},"
        code += f"\n    {filters=}," if filters else ""
        code += f"\n    {sort=}," if sort else ""
        code += f"\n    reports='{query['webEndpoint']}'," if reports else ""
        code += f"\n    snapshot_id='{snapshot}'," if snapshot else ""
        code += "\n)"
        return code

    def share_link(  # noqa: C901
        self,
        url: str,
        filters: Union[dict, str],
        columns: Optional[Union[list[str], set[str]]] = None,
        sort: Optional[dict] = None,
        snapshot: Optional[Union[bool, str]] = False,
    ) -> str:
        """Creates a shareable link for a table.

        Args:
            url: Example tables/vlan/device-summary
            filters: Filter dictionary to create view for
            columns: Optional list of columns to display, defaults to all. Some columns are hidden in the UI and will
                     not be displayed.
            sort: Dict of column to sort on
            snapshot: Default False do not add selector, True use IPFClient snapshot, string specific snapshot.
        Returns:
            URL string
        """
        url = self._check_url(url)
        try:
            web_endpoint = self.oas[url].post.web_endpoint
        except KeyError:
            raise NotImplementedError(f"Cannot create Shared View URL for table `{url}` as it has no web endpoint.")
        _columns = {_: True for _ in self.get_columns(url)}

        if columns:
            _columns.update({_: False for _ in _columns if _ not in columns})
        try:
            hidden = list(
                {k for k, v in _columns.items() if v and k != "id"}.difference(set(self.get_columns(url, ui=True)))
            )
            if hidden:
                logger.warning(
                    f"Column(s) `{hidden}` are hidden in the UI and will not be displayed using the shared view link."
                )
        except LookupError:
            pass
        try:
            user = self.get("tables/settings", params={"name": web_endpoint}).json()["userSettings"]
            auto_size, col_width = user.get("autoSizedColumns", True), user.get("columnWidth", {})
        except KeyError:
            auto_size, col_width = True, {}
        payload = {
            "autoSizedColumns": auto_size,
            "columnVisibility": _columns,
            "webEndpoint": web_endpoint,
            "filters": json.loads(filters) if isinstance(filters, str) else filters,
        }
        payload.update({"columnWidth": col_width} if col_width else {})
        payload.update({"sort": sort} if sort else {})
        resp = raise_for_status(self.post("tables/url", json=payload))
        if not snapshot:
            select_snap = ""
        elif snapshot is True:
            select_snap = f"&selectSnapshot={self.snapshot_id}"
        elif valid_snapshot(snapshot) and snapshot in self.snapshots:
            select_snap = f"&selectSnapshot={snapshot}"
        return str(self.base_url.join(web_endpoint)) + f"?copyId={resp.json()['id']}" + select_snap

    def post_to_get(self, url: str, payload: Union[dict, str], ignore_reports: bool = False):
        """

        Args:
            url: str: API or Frontend URL
            payload: Union[str, dict]: Copy/Paste payload from API description in UI, only required object is 'snapshot'
            ignore_reports: bool: Remove the reports from the payload (intent data) from being included.

        Returns: str: Get URL to return table data instead of pagination

        """
        if isinstance(payload, str):
            payload = json.loads(payload)
        snapshot = payload.get("snapshot", None)
        url, payload = self._fetch_setup(
            url,
            "json",
            payload.get("columns", None),
            snapshot,
            payload.get("filters", None),
            None if ignore_reports else payload.get("reports", None),
            payload.get("sort", None),
            payload.get("attributeFilters", None),
            None,
            True if snapshot else False,
        )
        return str(self._get_payload(url, payload))
