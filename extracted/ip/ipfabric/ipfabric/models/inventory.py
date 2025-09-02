import logging
from typing import Optional, Any, Union, overload, Literal

from pydantic import BaseModel, computed_field, Field

from .device import Devices
from .table import Table

try:
    from pandas import DataFrame
except ImportError:
    DataFrame = None
logger = logging.getLogger("ipfabric")

IGNORE_COLUMNS = {"id"}
EXPORT_FORMAT = Literal["json", "csv", "df"]
DEVICE_EXPORT_FORMAT = Literal["json", "csv", "object", "df"]


class DeviceTable(Table):
    """model for Device Table data"""

    endpoint: str = "tables/inventory/devices"

    def _as_model(self, devices, export):
        if export != "object":
            return devices
        return Devices(
            client=self.client,
            snapshot_id=self.client.snapshot_id,
            devices=devices,
        )

    @overload
    def fetch(
        self,
        export: Literal["json"] = ...,
        columns: Optional[Union[list[str], set[str]]] = None,
        filters: Optional[dict] = None,
        attr_filters: Optional[dict[str, list[str]]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[Union[bool, list, str]] = False,
        sort: Optional[dict] = None,
        limit: Optional[int] = 1000,
        start: Optional[int] = 0,
    ) -> list[dict]: ...

    @overload
    def fetch(
        self,
        export: Literal["csv"],
        columns: Optional[Union[list[str], set[str]]] = None,
        filters: Optional[dict] = None,
        attr_filters: Optional[dict[str, list[str]]] = None,
        snapshot_id: Optional[str] = None,
        sort: Optional[dict] = None,
        limit: Optional[int] = 1000,
        start: Optional[int] = 0,
        csv_tz: Optional[str] = None,
    ) -> bytes: ...

    @overload
    def fetch(
        self,
        export: Literal["df"],
        columns: Optional[Union[list[str], set[str]]] = None,
        filters: Optional[dict] = None,
        attr_filters: Optional[dict[str, list[str]]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[Union[bool, list, str]] = False,
        sort: Optional[dict] = None,
        limit: Optional[int] = 1000,
        start: Optional[int] = 0,
    ) -> DataFrame: ...

    @overload
    def fetch(
        self,
        export: Literal["object"],
        columns: Optional[Union[list[str], set[str]]] = None,
        filters: Optional[dict] = None,
        attr_filters: Optional[dict[str, list[str]]] = None,
        snapshot_id: Optional[str] = None,
        sort: Optional[dict] = None,
        limit: Optional[int] = 1000,
        start: Optional[int] = 0,
    ) -> Devices: ...

    def fetch(
        self,
        export: DEVICE_EXPORT_FORMAT = "json",
        columns: Optional[Union[list[str], set[str]]] = None,
        filters: Optional[dict] = None,
        attr_filters: Optional[dict[str, list[str]]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[Union[bool, list, str]] = False,
        sort: Optional[dict] = None,
        limit: Optional[int] = 1000,
        start: Optional[int] = 0,
        csv_tz: Optional[str] = None,
    ):
        """Gets all data from corresponding endpoint

        Args:
            export: str: Export format to return [json, csv, object]; default is json.
            columns: Optional columns to return, default is all
            filters: Optional filters'
            attr_filters: dict: Optional dictionary of Attribute filters
            snapshot_id: Optional snapshot ID to override class
            reports: True to return Intent Rules (also accepts string of frontend URL) or a list of report IDs
            sort: Dictionary to apply sorting: {"order": "desc", "column": "lastChange"}
            limit: Default to 1,000 rows
            start: Starts at 0
            csv_tz: str: Default None, set a timezone to return human-readable dates when using CSV;
                         see `ipfabric.tools.shared.TIMEZONES`
        Returns:
            Union[list[dict], Devices, bytes, DataFrame]: Default List of dicts 'json', Devices object if 'object',
                                                          bytes if 'csv', pandas.DataFrame if 'df'
        """
        devices = super(DeviceTable, self).fetch(
            export="json" if export in ["json", "object"] else export,
            columns=columns,
            filters=filters,
            attr_filters=attr_filters,
            snapshot_id=snapshot_id,
            reports=reports if export not in ["csv", "object"] else None,
            sort=sort,
            limit=limit,
            start=start,
            csv_tz=csv_tz,
        )
        return self._as_model(devices, export)

    @overload
    def all(
        self,
        export: Literal["json"] = ...,
        columns: Optional[Union[list[str], set[str]]] = None,
        filters: Optional[dict] = None,
        attr_filters: Optional[dict[str, list[str]]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[Union[bool, list, str]] = False,
        sort: Optional[dict] = None,
    ) -> list[dict]: ...

    @overload
    def all(
        self,
        export: Literal["csv"],
        columns: Optional[Union[list[str], set[str]]] = None,
        filters: Optional[dict] = None,
        attr_filters: Optional[dict[str, list[str]]] = None,
        snapshot_id: Optional[str] = None,
        sort: Optional[dict] = None,
        csv_tz: Optional[str] = None,
    ) -> bytes: ...

    @overload
    def all(
        self,
        export: Literal["df"],
        columns: Optional[Union[list[str], set[str]]] = None,
        filters: Optional[dict] = None,
        attr_filters: Optional[dict[str, list[str]]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[Union[bool, list, str]] = False,
        sort: Optional[dict] = None,
    ) -> DataFrame: ...

    @overload
    def all(
        self,
        export: Literal["object"],
        columns: Optional[Union[list[str], set[str]]] = None,
        filters: Optional[dict] = None,
        attr_filters: Optional[dict[str, list[str]]] = None,
        snapshot_id: Optional[str] = None,
        sort: Optional[dict] = None,
    ) -> Devices: ...

    def all(
        self,
        export: DEVICE_EXPORT_FORMAT = "json",
        columns: Optional[Union[list[str], set[str]]] = None,
        filters: Optional[dict] = None,
        attr_filters: Optional[dict[str, list[str]]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[Union[bool, list, str]] = False,
        sort: Optional[dict] = None,
        csv_tz: Optional[str] = None,
    ):
        """Gets all data from corresponding endpoint

        Args:
            export: str: Export format to return [json, csv, object]; default is json.
            columns: Optional columns to return, default is all
            filters: Optional filters
            attr_filters: dict: Optional dictionary of Attribute filters
            snapshot_id: Optional snapshot ID to override class
            reports: True to return Intent Rules (also accepts string of frontend URL) or a list of report IDs
            sort: Dictionary to apply sorting: {"order": "desc", "column": "lastChange"}
            csv_tz: str: Default None, set a timezone to return human-readable dates when using CSV;
                         see `ipfabric.tools.shared.TIMEZONES`
        Returns:
             Union[list[dict], Devices, bytes, DataFrame]: Default List of dicts 'json', Devices object if 'object',
                                                           bytes if 'csv', pandas.DataFrame if 'df'
        """
        devices = super(DeviceTable, self).all(
            export="json" if export in ["json", "object"] else export,
            columns=columns,
            filters=filters,
            attr_filters=attr_filters,
            snapshot_id=snapshot_id,
            reports=reports if export not in ["csv", "object"] else None,
            sort=sort,
            csv_tz=csv_tz,
        )
        return self._as_model(devices, export)


class Inventory(BaseModel):
    """model for inventories"""

    client: Any = Field(None, exclude=True)

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def sites(self) -> Table:
        return Table(client=self.client, endpoint="tables/inventory/sites")

    @computed_field
    @property
    def vendors(self) -> Table:
        return Table(client=self.client, endpoint="tables/inventory/summary/vendors")

    @computed_field
    @property
    def devices(self) -> Table:
        return DeviceTable(client=self.client)

    @computed_field
    @property
    def models(self) -> Table:
        return Table(client=self.client, endpoint="tables/inventory/summary/models")

    @computed_field
    @property
    def os_version_consistency_models(self) -> Table:
        return Table(client=self.client, endpoint="tables/inventory/os-version-consistency/models")

    @computed_field
    @property
    def os_version_consistency_platforms(self) -> Table:
        return Table(client=self.client, endpoint="tables/inventory/os-version-consistency/platforms")

    @computed_field
    @property
    def eol_summary(self) -> Table:
        return Table(client=self.client, endpoint="tables/reports/eof/summary")

    @computed_field
    @property
    def eol_details(self) -> Table:
        return Table(client=self.client, endpoint="tables/reports/eof/detail")

    @computed_field
    @property
    def platforms(self) -> Table:
        return Table(client=self.client, endpoint="tables/inventory/summary/platforms")

    @computed_field
    @property
    def pn(self) -> Table:
        return Table(client=self.client, endpoint="tables/inventory/pn")

    @computed_field
    @property
    def families(self) -> Table:
        return Table(client=self.client, endpoint="tables/inventory/summary/families")

    @computed_field
    @property
    def interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/inventory/interfaces")

    @computed_field
    @property
    def hosts(self) -> Table:
        return Table(client=self.client, endpoint="tables/addressing/hosts")

    @computed_field
    @property
    def hosts_ipv6(self) -> Table:
        return Table(client=self.client, endpoint="tables/addressing/ipv6-hosts")

    @computed_field
    @property
    def phones(self) -> Table:
        return Table(client=self.client, endpoint="tables/inventory/phones")

    @computed_field
    @property
    def fans(self) -> Table:
        return Table(client=self.client, endpoint="tables/inventory/fans")

    @computed_field
    @property
    def modules(self) -> Table:
        return Table(client=self.client, endpoint="tables/inventory/modules")
