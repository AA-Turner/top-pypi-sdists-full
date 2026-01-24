import logging
from collections import OrderedDict
from datetime import datetime, timezone
from typing import Any, Union
from typing import OrderedDict as OrderedDictType
from uuid import UUID

from pydantic import BaseModel, PrivateAttr, Field

from ipfabric.models import Snapshot
from ipfabric.tools.shared import VALID_REFS, raise_for_status

logger = logging.getLogger("ipfabric")

LAST_ID, PREV_ID, LASTLOCKED_ID = VALID_REFS
SNAPSHOT_TABLE = "tables/management/snapshots"


class Snapshots(BaseModel):
    client: Any = Field(exclude=True)
    _snapshots: OrderedDictType[str, Snapshot] = PrivateAttr(default_factory=OrderedDict)

    def model_post_init(self, __context) -> None:
        self.snapshots = self.get_snapshots()
        self.client._last_snapshot_update = datetime.now(timezone.utc)

    def update(self):
        """get all snapshots and assigns them to an attribute"""
        self.snapshots = self.get_snapshots()
        self.client._last_snapshot_update = datetime.now(timezone.utc)
        self.client._no_loaded_snapshots = self.loaded_snapshots == {}

    @property
    def snapshots(self) -> OrderedDictType[str, Snapshot]:
        return self._snapshots

    @snapshots.setter
    def snapshots(self, _):
        self._snapshots = _

    @property
    def loaded_snapshots(self) -> OrderedDictType[str, Snapshot]:
        """get only loaded snapshots"""
        return OrderedDict([(k, v) for k, v in self.snapshots.items() if v.loaded])

    @property
    def loading_snapshot(self) -> Union[Snapshot, None]:
        """Return Loading Snapshot or None"""
        return next(iter([v for v in self.snapshots.values() if v.loading]), None)

    @property
    def running_snapshot(self) -> Union[Snapshot, None]:
        """Return Running Snapshot"""
        return next(iter([v for v in self.snapshots.values() if v.running]), None)

    @property
    def unloaded_snapshots(self) -> OrderedDictType[str, Snapshot]:
        if not self.client.unloaded:
            logger.warning("Unloaded snapshots not initialized. Retrieving unloaded snapshots.")
            self.client.unloaded = True
            self.update()
        return OrderedDict([(k, v) for k, v in self.snapshots.items() if not v.loaded])

    def get_snapshot(self, snapshot_id: str) -> Snapshot:
        if snapshot_id in self.snapshots:
            return self.snapshots[snapshot_id]
        else:
            results = self.client.fetch(SNAPSHOT_TABLE, filters={"id": ["eq", snapshot_id]}, limit=1)
            if not results:
                logger.error(f"Snapshot {snapshot_id} not found.")
                return None
            get_result = self.client.get(f"/snapshots/{snapshot_id}")
            snapshot = self._create_snapshot_model(results[0], get_result)
            return snapshot

    def _create_snapshot_model(self, s: dict, get_result: dict) -> Snapshot:
        return Snapshot(
            client=self.client,
            **s,
            snapshot_id=get_result["id"],
            licensedDevCount=get_result.get("licensedDevCount", None),
            errors=get_result.get("errors", None),
            version=get_result.get("version", None),
            initialVersion=get_result.get("initialVersion", None),
        )

    def get_snapshot_id(self, snapshot: Union[Snapshot, str]) -> str:
        """
        Returns a Snapshot ID for a given input.

        Args:
            snapshot: Snapshot model, name, or ID

        Returns:
            Snapshot ID
        """
        if isinstance(snapshot, Snapshot):
            return snapshot.snapshot_id
        elif snapshot in VALID_REFS:
            return self.snapshots[snapshot].snapshot_id
        try:
            UUID(snapshot, version=4)
            return self.snapshots[snapshot].snapshot_id
        except ValueError:
            for snap in self.snapshots.values():
                if snapshot == snap.name:
                    return snap.snapshot_id
        raise ValueError(f"Could not locate Snapshot ID for {snapshot}.")

    def _get_snapshots(self):
        """
        Need to do a GET and POST to get all Snapshot data. See NIM-7223
        POST Missing:
        licensedDevCount
        errors
        version
        initialVersion
        """
        res = raise_for_status(self.client.get("/snapshots"))
        return {s["id"]: s for s in res.json()}

    def get_snapshots(self) -> OrderedDictType[str, Snapshot]:
        """Gets all snapshots from IP Fabric and returns a dictionary of {ID: Snapshot_info}

        Returns:
            Dictionary with ID as key and dictionary with info as the value
        """
        results = self.client.fetch_all(
            SNAPSHOT_TABLE,
            sort={"order": "desc", "column": "tsEnd"},
            filters={"status": ["nreg", "unloaded|error"]} if not self.client.unloaded else None,
        )
        get_results = self._get_snapshots()

        snap_dict = OrderedDict()
        for s in results:
            snap = self._create_snapshot_model(s, get_results[s["id"]])
            snap_dict[snap.snapshot_id] = snap
            if snap.loaded:
                # snap.get_assurance_engine_settings()  # REMOVED TOO MANY API CALLS
                if LASTLOCKED_ID not in snap_dict and snap.locked:
                    snap_dict[LASTLOCKED_ID] = snap
                if LAST_ID not in snap_dict:
                    snap_dict[LAST_ID] = snap
                    continue
                if PREV_ID not in snap_dict:
                    snap_dict[PREV_ID] = snap
        return snap_dict
