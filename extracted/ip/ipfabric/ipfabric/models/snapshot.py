from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ipfabric import IPFClient

import logging
from datetime import datetime, timezone
from time import sleep
from typing import Optional, Union, Literal, Any
from pathlib import Path
from ipfabric.models import Device, Job
from ipfabric.tools.shared import validate_ip_network_str, VALID_IP, raise_for_status
from ipfabric.settings.attributes import Attributes
from ipfabric.models.discovery import Networks, Community, SeedList, ManualLink
from ipfabric.models.authentication import CredentialList, PrivilegeList
from ipfabric.settings.discovery import Discovery
from ipfabric.settings.vendor_api import VendorAPI
from ipfabric.settings.authentication import Authentication

from pydantic import BaseModel, Field

logger = logging.getLogger("ipfabric")

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"
VALID_SNAPSHOT_SETTINGS = {
    "allowTelnet",
    "bgps",
    "cliRetryLimit",
    "cliSessionsLimit",
    "credentials",
    "disabledPostDiscoveryActions",
    # "discoveryHistorySeeds",  # TODO:
    "discoveryTasks",
    "fullBgpIpv6Limit",
    "fullBgpLimit",
    "limitDiscoveryTasks",
    "manualLinks",
    "networks",
    "ports",
    "privileges",
    "resolveNames",
    "scanner",
    "seedList",
    "siteSeparation",
    "snapshotName",
    "snapshotNote",
    "timeouts",
    "traceroute",
    "vendorApi",
}
DISABLED_ASSURANCE = {"graphCache", "historicalData", "intentVerification"}
SNAPSHOT_TABLE = "tables/management/snapshots"


def loaded_status(func):
    def _decorator(self, *args, **kwargs):
        if self.running:
            logger.warning(f"Snapshot {self.snapshot_id} is running; some methods may not be available.")
        elif not self.loaded:
            logger.error(f"Snapshot {self.snapshot_id} is not loaded.")
        else:
            return func(self, *args, **kwargs)
        return False

    return _decorator


def snapshot_upload(ipf: IPFClient, filename: str):
    data = {"file": (Path(filename).name, open(filename, "rb"), "application/x-tar")}
    resp = ipf.post("snapshots/upload", files=data)
    if resp.status_code == 400:
        if resp.json()["code"] == "API_SNAPSHOT_CONFLICT":
            logger.warning(f"SNAPSHOT ID {resp.json()['data']['snapshot']} already uploaded")
            return
    raise_for_status(resp)
    return resp.json()


class ScheduledSnapshot(BaseModel):
    error: bool = False
    message: Optional[str] = None
    success: bool = False
    snapshot_running: bool = False
    job: Optional[Job] = None
    params: Optional[dict] = Field(default_factory=dict)

    def add_error(self, message: str):
        self.error = True
        self.message = message

    def add_params(self, params: dict):  # noqa: C901, S3776
        for k, v in params.items():
            if k not in VALID_SNAPSHOT_SETTINGS:
                raise SyntaxError(f"Invalid Snapshot creation setting parameter '{k}'.")
            elif k == "disabledPostDiscoveryActions" and v and not DISABLED_ASSURANCE.issuperset(set(v)):
                raise SyntaxError(f"Invalid Disabled Assurance Job Setting parameter '{set(v) - DISABLED_ASSURANCE}'.")
            elif k == "credentials" and v is not None and not v:
                raise SyntaxError("Credentials cannot be empty.")
            elif v is None:
                continue
            elif k == "credentials":
                self.params[k] = (
                    v.model_dump() if isinstance(v, CredentialList) else CredentialList(root=v).model_dump()
                )
            elif k == "privileges":
                self.params[k] = v.model_dump() if isinstance(v, PrivilegeList) else PrivilegeList(root=v).model_dump()
            elif k == "networks":
                self.params[k] = v.model_dump() if isinstance(v, Networks) else Networks(**v).model_dump()
            elif k == "seedList":
                self.params[k] = v.model_dump() if isinstance(v, SeedList) else SeedList(seeds=v).model_dump()
            elif k == "bgps":
                self.params[k] = [
                    _.model_dump() if isinstance(_, Community) else Community(**_).model_dump() for _ in v
                ]
            elif k == "manualLinks":
                self.params[k] = [
                    _.model_dump() if isinstance(_, ManualLink) else ManualLink(**_).model_dump() for _ in v
                ]
            else:
                self.params[k] = v

    @property
    def snapshot_id(self):
        return self.job.snapshot if self.job else None

    @property
    def job_id(self):
        return self.job.id if self.job else None

    @property
    def job_scheduled_at(self):
        return self.job.scheduledAt if self.job else None


def _parse_snapshot_creation(ipf, resp: dict, snapshot: ScheduledSnapshot) -> ScheduledSnapshot:
    if not resp["success"]:
        snapshot.add_error("Unknown error creating snapshot.")
        return snapshot
    snapshot.success = True
    sleep(2)

    snapshot.job = ipf.jobs.get_job_by_id(resp["jobId"])
    if snapshot.snapshot_id:
        ipf.update()
    else:
        snapshot.message = "Please wait till current running snapshot finishes to get the new snapshot ID."
    return snapshot


def create_snapshot(
    ipf: IPFClient,
    snapshot_name: str = "",
    snapshot_note: str = "",
    networks: Optional[Union[Networks, dict[str, list[Union[str, VALID_IP]]]]] = None,
    seeds: Optional[Union[SeedList, list[Union[str, VALID_IP]]]] = None,
    credentials: Optional[Union[CredentialList, list[dict]]] = None,
    privileges: Optional[Union[PrivilegeList, list[dict]]] = None,
    disabled_assurance_jobs: Optional[list[Literal["graphCache", "historicalData", "intentVerification"]]] = None,
    fail_if_running_snapshot: bool = True,
    **kwargs,
) -> ScheduledSnapshot:
    snapshot = ScheduledSnapshot()
    snapshot.add_params(
        dict(
            snapshotName=snapshot_name,
            snapshotNote=snapshot_note,
            networks=networks,
            seedList=seeds,
            credentials=credentials,
            privileges=privileges,
            disabledPostDiscoveryActions=disabled_assurance_jobs,
            **kwargs,
        )
    )
    if not ipf._last_snapshot_update:
        ipf.update()
    elif (datetime.now(timezone.utc) - ipf._last_snapshot_update).total_seconds() > 60:
        logger.warning("Snapshot list is stale, updating.")
        ipf.update()

    snapshot.snapshot_running = True if ipf.running_snapshot else False

    if fail_if_running_snapshot and ipf.running_snapshot:
        logger.error("A snapshot is already running and 'fail_if_running_snapshot' is set to True.")
        snapshot.add_error("A snapshot is already running.")
        return snapshot

    resp = raise_for_status(ipf.post("snapshots", json=snapshot.params))
    return _parse_snapshot_creation(ipf, resp.json(), snapshot)


class Error(BaseModel):
    error_type: str = Field(None, alias="errorType")
    count: int


class Snapshot(BaseModel):
    client: Any = Field(exclude=True)
    snapshot_id: str = Field(None, alias="id")
    name: Optional[str] = None
    note: Optional[str] = None
    creator_username: Optional[str] = Field(None, alias="creatorUsername")
    total_dev_count: int = Field(None, alias="totalDevCount")
    licensed_dev_count: Optional[int] = Field(None, alias="licensedDevCount")
    user_count: int = Field(0, alias="userCount")
    interface_active_count: int = Field(0, alias="interfaceActiveCount")
    interface_count: int = Field(0, alias="interfaceCount")
    interface_edge_count: int = Field(0, alias="interfaceEdgeCount")
    device_added_count: int = Field(0, alias="deviceAddedCount")
    device_removed_count: int = Field(0, alias="deviceRemovedCount")
    status: str
    finish_status: str = Field(alias="finishStatus")
    loading: bool
    locked: bool
    from_archive: bool = Field(None, alias="fromArchive")
    start: datetime = Field(None, alias="tsStart")
    end: Optional[datetime] = Field(None, alias="tsEnd")
    change: Optional[datetime] = Field(None, alias="tsChange")
    version: Optional[str] = None  # TODO: NIM-20526
    initial_version: Optional[str] = Field(None, alias="initialVersion")
    sites: list[str] = Field(default_factory=list)
    errors: Optional[list[Error]] = None
    loaded_size: int = Field(None, alias="loadedSize")
    unloaded_size: int = Field(None, alias="unloadedSize")
    disabled_graph_cache: Optional[bool] = None
    disabled_historical_data: Optional[bool] = None
    disabled_intent_verification: Optional[bool] = None
    _local_attributes: Optional[Union[Attributes, bool]] = None
    _connectivity_report: Optional[list[dict]] = None

    def update(self) -> Optional[Snapshot]:
        result = self.client.fetch(SNAPSHOT_TABLE, filters={"id": ["eq", self.snapshot_id]}, snapshot=False, limit=1)
        if not result:
            logger.error(f"Snapshot {self.snapshot_id} not found.")
            return None
        get_result = self.client.get(f"snapshots/{self.snapshot_id}").json()
        snap_update = {
            "licensedDevCount": get_result.get("licensedDevCount", None),
            "errors": get_result.get("errors", None),
            "version": get_result.get("version", None),
            "initialVersion": get_result.get("initialVersion", None),
            **result[0],
        }
        update = self.model_copy(update=snap_update)
        for attr in self.model_fields_set:
            if getattr(update, attr) != getattr(self, attr):
                setattr(self, attr, getattr(update, attr))
        return self

    def snapshot_settings(self) -> Discovery:
        """Returns the snapshot settings for the current snapshot."""
        settings = raise_for_status(self.client.get(f"snapshots/{self.snapshot_id}/settings")).json()
        return Discovery(
            client=self.client,
            snapshot_id=self.snapshot_id,
            vendorApi=VendorAPI(client=self.client, snapshot_id=self.snapshot_id, vendor_api=settings.pop("vendorApi")),
            authentication=Authentication(
                client=self.client,
                settings={"credentials": settings.pop("credentials"), "privileges": settings.pop("privileges")},
                snapshot_id=self.snapshot_id,
            ),
            **settings,
        )

    def discovery_errors(self, filters: dict = None, columns: list[str] = None, sort: dict = None) -> list[dict]:
        return self.client.fetch_all(
            "tables/reports/discovery-errors", snapshot_id=self.snapshot_id, filters=filters, columns=columns, sort=sort
        )

    def discovery_tasks(self, filters: dict = None, columns: list[str] = None, sort: dict = None) -> list[dict]:
        return self.client.fetch_all(
            "tables/reports/discovery-tasks", snapshot_id=self.snapshot_id, filters=filters, columns=columns, sort=sort
        )

    def connectivity_report(
        self,
        export: Literal["json", "csv", "df"] = "json",
        columns: Optional[list[str]] = None,
        filters: Optional[Union[dict, str]] = None,
        sort: Optional[dict] = None,
        csv_tz: Optional[str] = None,
    ) -> list[dict]:
        if not self._connectivity_report:
            self._connectivity_report = self.client.fetch_all(
                "tables/reports/discovery-tasks",
                export=export,
                snapshot_id=self.snapshot_id,
                columns=columns
                or [
                    "ip",
                    "dnsName",
                    "context",
                    "source",
                    "status",
                    "vendor",
                    "mac",
                    "errorType",
                    "errorMessage",
                    "slug",
                    "attemptCount",
                    "errorReasons",
                    "hasLogFile",
                    "id",
                ],
                filters=filters,
                sort=sort,
                csv_tz=csv_tz,
            )
        return self._connectivity_report

    @property
    @loaded_status
    def errors_dict(self):
        return {_.error_type: _.count for _ in self.errors}

    @loaded_status
    def lock(self) -> bool:
        if not self.locked:
            raise_for_status(self.client.post(f"snapshots/{self.snapshot_id}/lock"))
            self.locked = True
        else:
            logger.warning(f"Snapshot {self.snapshot_id} is already locked.")
        return True

    def unlock(self) -> bool:
        if self.locked and self.loaded:
            raise_for_status(self.client.post(f"snapshots/{self.snapshot_id}/unlock"))
            self.locked = False
        else:
            logger.warning(f"Snapshot {self.snapshot_id} is already unlocked.")
        return True

    @property
    def loaded(self):
        return self.status == "done" and self.finish_status == "done" and self.loading is False

    @property
    def running(self):
        return not self.loading and self.status in ["run", "ready", "finishing"]

    def unload(self, wait_for_unload: bool = False, timeout: int = 60, retry: int = 5) -> bool:
        if not self.loaded and not self.running:
            logger.warning(f"Snapshot {self.snapshot_id} is already unloaded.")
            return True
        elif not self.loaded and self.running:
            logger.warning(f"Snapshot {self.snapshot_id} is running, cannot unload.")
            return False
        resp = raise_for_status(
            self.client.post("snapshots/unload", json=[{"jobDetail": self.name, "id": self.snapshot_id}])
        )
        job_id = next(iter([_["jobId"] for _ in resp.json() if _["snapshotId"] == self.snapshot_id]))
        if not job_id:
            logger.error("Could not find unload job for snapshot.")
            return False
        if wait_for_unload and not self.client.jobs.return_job_when_done(job_id, retry, timeout):
            logger.error("Snapshot Unload did not finish.")
            return False
        self.update()
        return True

    def delete(self):
        resp = raise_for_status(
            self.client.delete("snapshots", json=[{"id": self.snapshot_id, "jobDetail": self.name}])
        )
        return resp.ok

    def load(
        self,
        wait_for_load: bool = True,
        wait_for_assurance: bool = True,
        timeout: int = 60,
        retry: int = 5,
    ) -> bool:
        if self.loaded:
            logger.warning(f"Snapshot {self.snapshot_id} is already loaded.")
            return True
        resp = raise_for_status(
            self.client.post("snapshots/load", json=[{"jobDetail": self.name, "id": self.snapshot_id}])
        )
        job_id = next(iter([_["jobId"] for _ in resp.json() if _["snapshotId"] == self.snapshot_id]))
        if not job_id:
            logger.error("Could not find load job for snapshot.")
            return False
        if (wait_for_load or wait_for_assurance) and not self._check_load_status_by_id(
            job_id, wait_for_assurance, timeout, retry
        ):
            logger.error("Snapshot Load did not finish.")
            return False
        self.update()
        return True

    def _check_load_status_by_id(
        self,
        job_id: str,
        wait_for_assurance: bool = True,
        timeout: int = 60,
        retry: int = 5,
    ):
        if not self.client.jobs.return_job_when_done(job_id, timeout=timeout, retry=retry):
            logger.error("Snapshot Load did not complete.")
            return False
        if wait_for_assurance:
            return self._check_assurance_status(job_id, timeout, retry)
        return True

    def _check_load_status(
        self,
        ts: int,
        wait_for_assurance: bool = True,
        timeout: int = 60,
        retry: int = 5,
        action: str = "load",
    ):
        load_job = self.client.jobs.check_snapshot_job(
            self.snapshot_id, started=ts, action=action, timeout=timeout, retry=retry
        )
        if not load_job:
            logger.error("Could not find load job for snapshot.")
            return False
        return self._check_load_status_by_id(load_job.id, wait_for_assurance, timeout, retry)

    def _check_assurance_status(
        self,
        ts: int,
        timeout: int = 60,
        retry: int = 5,
    ):
        ae_settings = self.get_assurance_engine_settings()
        ae_status = False
        if ae_settings:
            ae_status = self.client.jobs.check_snapshot_assurance_jobs(
                self.snapshot_id, ae_settings, started=ts, timeout=timeout, retry=retry
            )
            if not ae_status:
                logger.error("Assurance Engine tasks did not complete")
        elif not ae_settings:
            logger.error("Could not get Assurance Engine tasks please check permissions.")
        if not ae_settings or not ae_status:
            self.client.update()
            return False
        self.update()
        return True

    @loaded_status
    def attributes(self):
        return self.local_attributes.all()

    @property
    @loaded_status
    def local_attributes(self):
        if self._local_attributes is None:
            self._local_attributes = Attributes(client=self.client, snapshot_id=self.snapshot_id)
        return self._local_attributes

    def download(self, path: str = None, timeout: int = 60, retry: int = 5):  # TODO
        job_id = raise_for_status(self.client.get(f"/snapshots/{self.snapshot_id}/download")).json()["jobId"]

        if not self.client.jobs.return_job_when_done(job_id, retry, timeout):
            logger.error(f"Download job did not finish within {retry * timeout} seconds, could not get file.")
            return None
        file = self.client.get(f"jobs/{job_id}/download")
        try:
            filename = file.headers["Content-Disposition"].split("filename=")[-1].strip('"').replace(":", "_")
        except:  # noqa: E722
            filename = f"{self.snapshot_id}.tar"
        path = Path(path or filename).resolve().with_suffix(".tar").absolute()
        with open(path, "wb") as fp:
            fp.write(file.content)
        return path

    @loaded_status
    def get_snapshot_settings(self) -> Union[dict, None]:
        settings = None
        msg = "API_INSUFFICIENT_RIGHTS to `snapshots/:key/settings` " + self.client.user.error_msg

        if self.client.user.snapshots_settings is False:
            logger.debug(f"Could not get Snapshot {self.snapshot_id} Settings:" + msg)
            return settings

        res = self.client.get(f"/snapshots/{self.snapshot_id}/settings")
        if res.status_code == 200:
            settings = res.json()
            if self.client.user.snapshots_settings is None:
                self.client.user.snapshots_settings = True

        else:
            logger.debug(f"Could not get Snapshot {self.snapshot_id} Settings:" + msg)
            logger.warning(msg)
            self.client.user.snapshots_settings = False
        return settings

    @loaded_status
    def get_assurance_engine_settings(self) -> Union[dict, bool]:
        settings = self.get_snapshot_settings()
        if settings is None:
            logger.debug(f"Could not get Snapshot {self.snapshot_id} Settings to verify Assurance Engine tasks.")
            return False
        disabled = settings.get("disabledPostDiscoveryActions", [])
        self.disabled_graph_cache = True if "graphCache" in disabled else False
        self.disabled_historical_data = True if "historicalData" in disabled else False
        self.disabled_intent_verification = True if "intentVerification" in disabled else False
        return {
            "disabled_graph_cache": self.disabled_graph_cache,
            "disabled_historical_data": self.disabled_historical_data,
            "disabled_intent_verification": self.disabled_intent_verification,
        }

    @loaded_status
    def update_assurance_engine_settings(
        self,
        disabled_graph_cache: bool = False,
        disabled_historical_data: bool = False,
        disabled_intent_verification: bool = False,
        wait_for_assurance: bool = True,
        timeout: int = 60,
        retry: int = 5,
    ) -> bool:
        settings = self.get_snapshot_settings(self.client)
        if settings is None:
            logger.error(
                f"Could not get Snapshot {self.snapshot_id} Settings and cannot update Assurance Engine tasks."
            )
            return False
        current = set(settings.get("disabledPostDiscoveryActions", []))
        disabled, ae_settings = self._calculate_new_ae_settings(
            current, disabled_graph_cache, disabled_historical_data, disabled_intent_verification
        )
        if disabled == current:
            logger.info("No changes to Assurance Engine Settings required.")
            return True
        ts = int(datetime.now().timestamp() * 1000)
        raise_for_status(
            self.client.patch(
                f"/snapshots/{self.snapshot_id}/settings", json={"disabledPostDiscoveryActions": list(disabled)}
            )
        )
        if wait_for_assurance and current - disabled:
            ae_status = self.client.jobs.check_snapshot_assurance_jobs(
                self.snapshot_id, ae_settings, started=ts, timeout=timeout, retry=retry
            )
            if not ae_status:
                logger.error("Assurance Engine tasks did not complete")
                return False
        return True

    @staticmethod
    def _calculate_new_ae_settings(
        current: set,
        disabled_graph_cache: bool = False,
        disabled_historical_data: bool = False,
        disabled_intent_verification: bool = False,
    ):
        disabled = set()
        if disabled_graph_cache:
            disabled.add("graphCache")
        if disabled_historical_data:
            disabled.add("historicalData")
        if disabled_intent_verification:
            disabled.add("intentVerification")
        enabled = current - disabled

        ae_settings = {
            "disabled_graph_cache": False if "graphCache" in enabled else True,
            "disabled_historical_data": False if "historicalData" in enabled else True,
            "disabled_intent_verification": False if "intentVerification" in enabled else True,
        }

        return disabled, ae_settings

    @staticmethod
    def _dev_to_sn(devices: Union[list[str], list[Device], set[str], str, Device]) -> set[str]:
        sns = set()
        if not isinstance(devices, (list, set)):
            devices = {devices}
        for device in devices:
            if isinstance(device, str):
                sns.add(device)
            elif isinstance(device, Device):
                sns.add(device.sn)
        return sns

    @loaded_status
    def verify_snapshot_devices(
        self, devices: Union[list[str], list[Device], set[str], str, Device]
    ) -> dict[str, set[str]]:
        """Checks to ensure that the Vendor is enabled for the devices.

        Args:
            devices: IP Fabric Device Serial Number, Device object, or list of either

        Returns: bool
        """
        sn = self._dev_to_sn(devices)
        snap_devs = self.client.fetch_all(
            "tables/snapshot-devices",
            columns=["id", "isApiTask", "sn", "settingsStates", "vendor"],
            filters={"isSelected": ["eq", True]},
            bind_variables={"selected": list(sn), "isDelete": False},
            snapshot_id=self.snapshot_id,
        )
        disabled = {dev["sn"] for dev in snap_devs if "noApiSettings" in dev["settingsStates"] and dev["isApiTask"]}
        valid = {dev["sn"] for dev in snap_devs if "ok" in dev["settingsStates"]}
        invalid = sn - valid - disabled
        if disabled:
            logger.warning(f"Vendor API(s) disabled for devices: {list(disabled)}.")
        if invalid:
            logger.warning(f"Invalid snapshot devices: {list(invalid)}.")
        return {"disabled": disabled, "invalid": invalid, "valid": valid}

    @loaded_status
    def delete_devices(
        self,
        devices: Union[list[str], list[Device], set[str], str, Device],
        wait_for_discovery: bool = True,
        wait_for_assurance: bool = True,
        timeout: int = 60,
        retry: int = 5,
        skip_invalid_devices: bool = True,
    ) -> bool:
        """Rediscover device(s) based on a serial number or Device object.

        Args:
            devices: IP Fabric Device Serial Number, Device object, or list of either
            wait_for_discovery: Default True to wait before returning
            wait_for_assurance:  Default True to wait before returning
            timeout: How long to wait, larger snapshots will take longer times
            retry: Number of retries to wait ( (timeout X retry = total length) X 2) Will check for Discovery
                   and then use same times for Assurance.
            skip_invalid_devices: If a Vendor API device is included and the vendor is disabled it will be skipped
                                  instead of not refreshing devices.

        Returns: bool
        """
        return self._rediscover_delete_devices(
            "delete", devices, wait_for_discovery, wait_for_assurance, timeout, retry, skip_invalid_devices
        )

    @loaded_status
    def rediscover_devices(
        self,
        devices: Union[list[str], list[Device], set[str], str, Device],
        wait_for_discovery: bool = True,
        wait_for_assurance: bool = True,
        timeout: int = 60,
        retry: int = 5,
        skip_invalid_devices: bool = True,
    ) -> bool:
        """Rediscover device(s) based on a serial number or Device object.

        Args:
            devices: IP Fabric Device Serial Number, Device object, or list of either
            wait_for_discovery: Default True to wait before returning
            wait_for_assurance:  Default True to wait before returning
            timeout: How long to wait, larger snapshots will take longer times
            retry: Number of retries to wait ( (timeout X retry = total length) X 2) Will check for Discovery
                   and then use same times for Assurance.
            skip_invalid_devices: If a Vendor API device is included and the vendor is disabled it will be skipped
                                  instead of not refreshing devices.

        Returns: bool
        """
        return self._rediscover_delete_devices(
            "refresh", devices, wait_for_discovery, wait_for_assurance, timeout, retry, skip_invalid_devices
        )

    @loaded_status
    def _rediscover_delete_devices(
        self,
        action: Literal["refresh", "delete"],
        devices: Union[list[str], list[Device], set[str], str, Device],
        wait_for_discovery: bool = True,
        wait_for_assurance: bool = True,
        timeout: int = 60,
        retry: int = 5,
        skip_invalid_devices: bool = True,
    ) -> bool:
        """Rediscover device(s) based on a serial number or Device object.

        Args:
            devices: IP Fabric Device Serial Number, Device object, or list of either
            wait_for_discovery: Default True to wait before returning
            wait_for_assurance:  Default True to wait before returning
            timeout: How long to wait, larger snapshots will take longer times
            retry: Number of retries to wait ( (timeout X retry = total length) X 2) Will check for Discovery
                   and then use same times for Assurance.
            skip_invalid_devices: If a Vendor API device is included and the vendor is disabled it will be skipped
                                  instead of not refreshing devices.

        Returns: bool
        """
        sn = self._dev_to_sn(devices)
        devices = self.verify_snapshot_devices(sn)
        if not skip_invalid_devices and (devices["disabled"] or devices["invalid"]):
            return False
        sn = list(devices["valid"])
        if not sn:
            return False

        if action == "delete":
            resp = self.client.request("DELETE", f"snapshots/{self.snapshot_id}/devices", json=sn)
        else:
            resp = self.client.post(
                f"snapshots/{self.snapshot_id}/devices", json={"snList": sn, "vendorSettingsMap": {}}
            )
        raise_for_status(resp)
        resp = resp.json()
        if not wait_for_discovery:
            self.client.update()
            return True

        return self._check_modification_status(wait_for_assurance, resp["jobId"], timeout, retry)

    def _vendor_apis(self):
        vendors = []
        for vendor in self.client.get(f"snapshots/{self.snapshot_id}/available-vendor-settings").json():
            vendor.pop("details", None)
            if vendor["type"] not in ["juniper-mist", "ruckus-vsz"]:
                vendor.pop("apiVersion", None)
            if vendor["type"] == "aws-ec2":
                vendor.pop("baseUrl", None)
            vendors.append(vendor)
        return vendors

    @loaded_status
    def add_devices(
        self,
        ip: Union[list[str], list[VALID_IP], str, VALID_IP] = None,
        refresh_vendor_api: bool = True,
        retry_timed_out: bool = True,
        wait_for_discovery: bool = True,
        wait_for_assurance: bool = True,
        timeout: int = 60,
        retry: int = 5,
    ) -> bool:
        """Add device(s) based on a IP address or subnet.

        Args:
            ip: Single IP or list of IPs
            refresh_vendor_api: Default True to refresh Vendor API devices that are enabled in snapshot settings.
            retry_timed_out: IP Default True to retry devices that timed out.
            wait_for_discovery: Default True to wait before returning
            wait_for_assurance:  Default True to wait before returning
            timeout: How long to wait, larger snapshots will take longer times
            retry: Number of retries to wait ( (timeout X retry = total length) X 2) Will check for Discovery
                   and then use same times for Assurance.

        Returns: bool
        """
        if not ip and not refresh_vendor_api and not retry_timed_out:
            raise SyntaxError("No snapshot modification selected.")
        elif not ip and not refresh_vendor_api and not self.errors_dict.get("ABCommandTimeout", 0):
            logger.warning(f"No Command Timeout Errors found in {self.snapshot_id}, not refreshing snapshot.")
            return True
        vendors = self._vendor_apis() if refresh_vendor_api else []
        ips = []
        if isinstance(ip, str):
            ip = [ip]
        elif ip is None:
            ip = []
        for i in ip:
            i = validate_ip_network_str(i, ipv6=True)
            ips.append(i)

        payload = {"ipList": ips, "retryTimedOut": retry_timed_out, "vendorApi": vendors}
        resp = raise_for_status(self.client.post(f"snapshots/{self.snapshot_id}/devices", json=payload)).json()

        if not wait_for_discovery:
            self.client.update()
            return resp["success"]
        return self._check_modification_status(wait_for_assurance, resp["jobId"], timeout, retry)

    def _check_modification_status(self, wait_for_assurance, job_id, timeout, retry):
        job = self.client.jobs.return_job_when_done(job_id, timeout=timeout, retry=retry)
        if job and wait_for_assurance:
            return self._check_assurance_status(job.startedAt, timeout, retry)
        elif not job:
            logger.error("Snapshot Modification Discovery did not complete.")
        self.client.update()
        return True if job else False

    @loaded_status
    def add_ip_devices(
        self,
        ip: Union[list[str], list[VALID_IP], str, VALID_IP],
        wait_for_discovery: bool = True,
        wait_for_assurance: bool = True,
        timeout: int = 60,
        retry: int = 5,
    ) -> bool:
        """Refreshes Vendor API devices.

        Args:
            ip: Single IP or list of IPs
            wait_for_discovery: Default True to wait before returning
            wait_for_assurance:  Default True to wait before returning
            timeout: How long to wait, larger snapshots will take longer times
            retry: Number of retries to wait ( (timeout X retry = total length) X 2) Will check for Discovery
                   and then use same times for Assurance.

        Returns: bool
        """
        return self.add_devices(ip, False, False, wait_for_discovery, wait_for_assurance, timeout, retry)

    @loaded_status
    def refresh_vendor_api(
        self,
        wait_for_discovery: bool = True,
        wait_for_assurance: bool = True,
        timeout: int = 60,
        retry: int = 5,
    ) -> bool:
        """Refreshes Vendor API devices.

        Args:
            wait_for_discovery: Default True to wait before returning
            wait_for_assurance:  Default True to wait before returning
            timeout: How long to wait, larger snapshots will take longer times
            retry: Number of retries to wait ( (timeout X retry = total length) X 2) Will check for Discovery
                   and then use same times for Assurance.

        Returns: bool
        """
        return self.add_devices(None, True, False, wait_for_discovery, wait_for_assurance, timeout, retry)

    @loaded_status
    def retry_timed_out_devices(
        self,
        wait_for_discovery: bool = True,
        wait_for_assurance: bool = True,
        timeout: int = 60,
        retry: int = 5,
    ) -> bool:
        """Retries devices that timed out in Snapshot.

        Args:
            wait_for_discovery: Default True to wait before returning
            wait_for_assurance:  Default True to wait before returning
            timeout: How long to wait, larger snapshots will take longer times
            retry: Number of retries to wait ( (timeout X retry = total length) X 2) Will check for Discovery
                   and then use same times for Assurance.

        Returns: bool
        """
        return self.add_devices(None, False, True, wait_for_discovery, wait_for_assurance, timeout, retry)
