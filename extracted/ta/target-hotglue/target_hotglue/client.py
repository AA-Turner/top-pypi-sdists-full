"""WoocommerceSink target sink class, which handles writing streams."""

import hashlib
import json
import os
from abc import abstractmethod
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from target_hotglue.rest import Rest
from target_hotglue.auth import Authenticator
from target_hotglue.common import HGJSONEncoder
from singer_sdk.plugin_base import PluginBase
from singer_sdk.sinks import RecordSink, BatchSink

class HotglueBaseSink(Rest):
    summary_init = False
    # include any stream names if externalId needs to be passed in the payload
    allows_externalid = []

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def endpoint(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def base_url(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def unified_schema(self) -> BaseModel:
        raise NotImplementedError()

    def __init__(
        self,
        target: PluginBase,
        stream_name: str,
        schema: Dict,
        key_properties: Optional[List[str]],
    ) -> None:
        self._state = dict(target._state)
        self._target = target
        super().__init__(target, stream_name, schema, key_properties)

    def url(self, endpoint=None):
        if not endpoint:
            endpoint = self.endpoint
        return f"{self.base_url}{endpoint}"

    def validate_input(self, record: dict):
        raise NotImplementedError()

    def validate_output(self, mapping):
        return mapping

    def init_state(self):
        # get the full target state
        target_state = self._target._latest_state

        # If there is data for the stream name in target_state use that to initialize the state
        if target_state:
            if not self._state and target_state.get("bookmarks", {}).get(self.name) and target_state.get("summary", {}).get(self.name):
                self.latest_state = target_state
        # If not init sink state latest_state
        if not self.latest_state:
            self.latest_state = self._state or {"bookmarks": {}, "summary": {}}

        if self.name not in self.latest_state["bookmarks"]:
            if not self.latest_state["bookmarks"].get(self.name):
                self.latest_state["bookmarks"][self.name] = []

        if not self.summary_init:
            if not self.latest_state.get("summary"):
                self.latest_state["summary"] = {}
            if not self.latest_state["summary"].get(self.name):
                self.latest_state["summary"][self.name] = {"success": 0, "fail": 0, "existing": 0, "updated": 0}

            self.summary_init = True
    
    def error_to_string(self, error: Any):
        return str(error)
    
    def process_error_state(self, state: dict):
        # log full error
        self.logger.error(f"Error processing record of type {self.name}: {state.get('error')}")
        # clean error for state
        state["error"] = self.error_to_string(state.get("error"))
        return state

    def update_state(self, state: dict, is_duplicate=False, record=None):
        if is_duplicate:
            self.logger.info(f"Record of type {self.name} already exists with id: {state.get('id')}")
            self.latest_state["summary"][self.name]["existing"] += 1

        elif not state.get("success", False):
            self.latest_state["summary"][self.name]["fail"] += 1
            self.process_error_state(state)
        elif state.get("is_updated", False):
            self.latest_state["summary"][self.name]["updated"] += 1
            state.pop("is_updated", None)
        else:
            self.latest_state["summary"][self.name]["success"] += 1
        
        # add the mapped record to the state if it exists and env var OUTPUT_MAPPED_RECORD is set to true
        if record and os.getenv("OUTPUT_MAPPED_RECORD", "false").lower() == "true":
            state["mapped_record"] = record

        self.latest_state["bookmarks"][self.name].append(state)

        # If "authenticator" exists and if it's an instance of "Authenticator" class,
        # update "self.latest_state" with the the "authenticator" state
        if self.authenticator and isinstance(self.authenticator, Authenticator):
            self.latest_state.update(self.authenticator.state)


class HotglueSink(HotglueBaseSink, RecordSink):
    """Hotglue target sink class."""
    def upsert_record(self, record: dict, context: dict):
        response = self.request_api("POST", request_data=record)
        id = response.json().get("id")
        return id, response.ok, dict()

    def build_record_hash(self, record: dict):
        return hashlib.sha256(json.dumps(record, cls=HGJSONEncoder).encode()).hexdigest()

    def get_existing_state(self, hash: str):
        states = self.latest_state["bookmarks"][self.name]

        existing_state = next((s for s in states if hash==s.get("hash") and s.get("success")), None)

        if existing_state:
            self.latest_state["summary"][self.name]["existing"] += 1

        return existing_state

    @abstractmethod
    def preprocess_record(self, record: dict, context: dict) -> dict:
        raise NotImplementedError()

    def process_record(self, record: dict, context: dict) -> None:
        """Process the record."""
        if not self.latest_state:
            self.init_state()

        hash = self.build_record_hash(record)

        existing_state =  self.get_existing_state(hash)

        if self.name in self.allows_externalid:
            external_id = record.get("externalId")
        else:
            external_id = record.pop("externalId", None)

        if existing_state:
            return self.update_state(existing_state, is_duplicate=True, record=record)

        state = {"hash": hash}

        id = None
        success = False
        state_updates = dict()

        try:
            id, success, state_updates = self.upsert_record(record, context)
        except Exception as e:
            self.logger.exception(f"Upsert record error {str(e)}")
            state_updates['error'] = str(e)

        if success:
            self.logger.info(f"{self.name} processed id: {id}")

        state["success"] = success

        if id:
            state["id"] = id

        if external_id:
            state["externalId"] = external_id

        # if is_duplicate is in state_updates, set is_duplicate to True
        is_duplicate = False
        if state_updates.pop("existing", False):
            is_duplicate = True

        if state_updates and isinstance(state_updates, dict):
            state = dict(state, **state_updates)

        self.update_state(state, is_duplicate=is_duplicate, record=record)


class HotglueBatchSink(HotglueBaseSink, BatchSink):
    """Hotglue target sink class."""

    def process_batch_record(self, record: dict, index: int) -> dict:
        return record

    @abstractmethod
    def make_batch_request(self, records: List[dict]):
        raise NotImplementedError()

    def handle_batch_response(self, response) -> dict:
        """
        This method should return a dict.
        It's recommended that you return a key named "state_updates".
        This key should be an array of all state updates
        """
        return dict()

    def process_batch(self, context: dict) -> None:
        if not self.latest_state:
            self.init_state()

        raw_records = context["records"]

        records = list(map(lambda e: self.process_batch_record(e[1], e[0]), enumerate(raw_records)))

        response = self.make_batch_request(records)

        result = self.handle_batch_response(response)

        for state in result.get("state_updates", list()):
            self.update_state(state)
