from __future__ import annotations

import time
import uuid
from typing import TYPE_CHECKING

import msgpack

from bec_lib.endpoints import MessageEndpoints
from bec_lib.logger import bec_logger

from .emitter import EmitterBase

logger = bec_logger.logger

if TYPE_CHECKING:
    from .scan_bundler import ScanBundler


class BlueskyEmitter(EmitterBase):
    def __init__(self, scan_bundler: ScanBundler) -> None:
        super().__init__(scan_bundler.connector)
        self.scan_bundler = scan_bundler
        self.bluesky_metadata = {}

    def send_run_start_document(self, scan_id) -> None:
        """Bluesky only: send run start documents."""
        logger.debug(f"sending run start doc for scan_id {scan_id}")
        self.bluesky_metadata[scan_id] = {}
        doc = self._get_run_start_document(scan_id)
        self.bluesky_metadata[scan_id]["start"] = doc
        self.connector.raw_send(MessageEndpoints.bluesky_events(), msgpack.dumps(("start", doc)))
        self.send_descriptor_document(scan_id)

    def _get_run_start_document(self, scan_id) -> dict:
        sb = self.scan_bundler
        doc = {
            "time": time.time(),
            "uid": str(uuid.uuid4()),
            "scan_id": scan_id,
            "queue_id": sb.sync_storage[scan_id]["info"]["queue_id"],
            "scan_id": sb.sync_storage[scan_id]["info"]["scan_number"],
            "motors": tuple(dev.name for dev in sb.scan_motors[scan_id]),
        }
        return doc

    def _get_data_keys(self, scan_id):
        sb = self.scan_bundler
        signals = {}
        for dev in sb.monitored_devices[scan_id]["devices"]:
            # copied from bluesky/callbacks/stream.py:
            signals[dev.name] = sb.device_manager.devices[dev.name]._info.get("describe", {})
        return signals

    def _get_descriptor_document(self, scan_id) -> dict:
        sb = self.scan_bundler
        doc = {
            "run_start": self.bluesky_metadata[scan_id]["start"]["uid"],
            "time": time.time(),
            "data_keys": self._get_data_keys(scan_id),
            "uid": str(uuid.uuid4()),
            "configuration": {},
            "name": "primary",
            "hints": {"samx": {"fields": ["samx"]}, "samy": {"fields": ["samy"]}},
            "object_keys": {
                dev.name: [val for val in dev._info.get("signals", {})]
                for dev in sb.monitored_devices[scan_id]["devices"]
            },
        }
        return doc

    def send_descriptor_document(self, scan_id) -> None:
        """Bluesky only: send descriptor document"""
        doc = self._get_descriptor_document(scan_id)
        self.bluesky_metadata[scan_id]["descriptor"] = doc
        self.connector.raw_send(
            MessageEndpoints.bluesky_events(), msgpack.dumps(("descriptor", doc))
        )

    def cleanup_storage(self, scan_id):
        """remove old scan_ids to free memory"""

        for storage in ["bluesky_metadata"]:
            try:
                getattr(self, storage).pop(scan_id)
            except KeyError:
                logger.warning(f"Failed to remove {scan_id} from {storage}.")

    def send_bluesky_scan_point(self, scan_id, point_id) -> None:
        self.connector.raw_send(
            MessageEndpoints.bluesky_events(),
            msgpack.dumps(("event", self._prepare_bluesky_event_data(scan_id, point_id))),
        )

    def _prepare_bluesky_event_data(self, scan_id, point_id) -> dict:
        # event = {
        #     "descriptor": "5605e810-bb4e-4e40-b...d45279e3a4",
        #     "time": 1648468217.524021,
        #     "data": {
        #         "det": 1.0,
        #         "motor1": -10.0,
        #         "motor1_setpoint": -10.0,
        #         "motor2": -10.0,
        #         "motor2_setpoint": -10.0,
        #     },
        #     "timestamps": {
        #         "det": 1648468209.868633,
        #         "motor1": 1648468209.862141,
        #         "motor1_setpoint": 1648468209.8607192,
        #         "motor2": 1648468209.864479,
        #         "motor2_setpoint": 1648468209.8629901,
        #     },
        #     "seq_num": 1,
        #     "uid": "ea83a56e-6af2-4b94-9...44dcc36d4e",
        #     "filled": {},
        # }
        sb = self.scan_bundler
        metadata = self.bluesky_metadata[scan_id]
        while not metadata.get("descriptor"):
            time.sleep(0.01)

        bls_event = {
            "descriptor": metadata["descriptor"].get("uid"),
            "time": time.time(),
            "seq_num": point_id,
            "uid": str(uuid.uuid4()),
            "filled": {},
            "data": {},
            "timestamps": {},
        }
        for data_point in sb.sync_storage[scan_id][point_id].values():
            for key, val in data_point.items():
                bls_event["data"][key] = val["value"]
                bls_event["timestamps"][key] = val["timestamp"]
        return bls_event

    def on_cleanup(self, scan_id: str):
        self.cleanup_storage(scan_id)

    def on_init(self, scan_id: str):
        self.send_run_start_document(scan_id)
