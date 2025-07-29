"""HotglueTarget target class."""

import click
import copy
import time
import os
import pydantic
from abc import abstractmethod
from io import FileIO
from pathlib import Path, PurePath
from typing import Callable, Dict, List, Optional, Tuple, Type, Union
from singer_sdk.sinks import Sink
# from singer_sdk.target_base import Target
from singer_sdk.mapper import PluginMapper
from singer_sdk.cli import common_options
from singer_sdk.helpers._classproperty import classproperty
from singer_sdk.helpers._secrets import SecretString
from singer_sdk.helpers._util import read_json_file

from target_hotglue.target_base import Target
from target_hotglue.sinks import ModelSink
import pandas as pd
import os

job_id = os.environ.get('JOB_ID')
flow_id = os.environ.get('FLOW')
SNAPSHOT_DIR = os.environ.get('SNAPSHOT_DIR') or f"/home/hotglue/{job_id}/snapshots"

class TargetHotglue(Target):
    """Sample target for Hotglue."""

    MAX_PARALLELISM = 8
    EXTERNAL_ID_KEY = "externalId"
    GLOBAL_PRIMARY_KEY = "id"

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def SINK_TYPES(self) -> List[ModelSink]:
        raise NotImplementedError

    def __init__(
        self,
        config: Optional[Union[dict, PurePath, str, List[Union[PurePath, str]]]] = None,
        parse_env_config: bool = False,
        validate_config: bool = True,
        state: str = None
    ) -> None:
        """Initialize the target.

        Args:
            config: Target configuration. Can be a dictionary, a single path to a
                configuration file, or a list of paths to multiple configuration
                files.
            parse_env_config: Whether to look for configuration values in environment
                variables.
            validate_config: True to require validation of config settings.
        """
        config_file_path = None
        if not state:
            state_dict = {}
        elif isinstance(state, str) or isinstance(state, PurePath):
            state_dict = read_json_file(state)
        if not config:
            config_dict = {}
        elif isinstance(config, str) or isinstance(config, PurePath):
            config_dict = read_json_file(config)
            config_file_path = str(config)
        elif isinstance(config, list):
            config_dict = {}
            config_file_path = str(config[0])
            for config_path in config:
                # Read each config file sequentially. Settings from files later in the
                # list will override those of earlier ones.
                config_dict.update(read_json_file(config_path))
        elif isinstance(config, dict):
            config_dict = config
        else:
            raise ValueError(f"Error parsing config of type '{type(config).__name__}'.")
        if parse_env_config:
            self.logger.info("Parsing env var for settings config...")
            config_dict.update(self._env_var_config)
        else:
            self.logger.info("Skipping parse of env var settings...")
        for k, v in config_dict.items():
            if self._is_secret_config(k):
                config_dict[k] = SecretString(v)
        self._config = config_dict
        self._state = state_dict
        self._config_file_path = config_file_path
        self._validate_config(raise_errors=validate_config)
        self.mapper: PluginMapper
        self.streaming_job = os.environ.get('STREAMING_JOB') == 'True'
        if self.streaming_job:
            self._latest_state: Dict[str, dict] = { "tap": {}, "target": {} }
        else:
            self._latest_state: Dict[str, dict] = {}
        self._drained_state: Dict[str, dict] = {}
        self._sinks_active: Dict[str, Sink] = {}
        self._sinks_to_clear: List[Sink] = []
        self._max_parallelism: Optional[int] = self.MAX_PARALLELISM

        # Approximated for max record age enforcement
        self._last_full_drain_at: float = time.time()

        # Initialize mapper
        self.mapper: PluginMapper
        self.mapper = PluginMapper(
            plugin_config=dict(self.config),
            logger=self.logger,
        )

    def get_sink_class(self, stream_name: str) -> Type[Sink]:
        """Get sink for a stream."""
        return next(
            (
                sink_class
                for sink_class in self.SINK_TYPES
                if sink_class.name.lower() == stream_name.lower()
            ),
            None,
        )
    
    def get_record_id(self, sink_name, record, relation_fields=None):
        external_id = record.get(self.EXTERNAL_ID_KEY)
        if external_id and not record.get(self.GLOBAL_PRIMARY_KEY):
            sink_snapshot = None
            snapshot_path_csv = f"{SNAPSHOT_DIR}/{sink_name}_{flow_id}.snapshot.csv"
            snapshot_path_parquet = f"{SNAPSHOT_DIR}/{sink_name}_{flow_id}.snapshot.parquet"
            if os.path.exists(snapshot_path_csv):
                sink_snapshot = pd.read_csv(snapshot_path_csv)
            elif os.path.exists(snapshot_path_parquet):
                sink_snapshot = pd.read_parquet(snapshot_path_parquet)
            
            if sink_snapshot is not None:
                sink_snapshot["InputId"] = sink_snapshot["InputId"].astype(str)
                external_id = sink_snapshot[sink_snapshot["InputId"] == str(external_id)]
                if len(external_id):
                    record[self.GLOBAL_PRIMARY_KEY] = external_id["RemoteId"].iloc[0]

        if isinstance(relation_fields, list):
            for relation in relation_fields:

                if not isinstance(relation, dict):
                    continue

                field = relation.get("field")
                object_name = relation.get("objectName")

                if (
                    not field or
                    not object_name or
                    not record.get(field)
                ):
                    continue

                relation_snapshot = None

                relation_path_csv = f"{SNAPSHOT_DIR}/{object_name}_{flow_id}.snapshot.csv"
                relation_path_parquet = f"{SNAPSHOT_DIR}/{object_name}_{flow_id}.snapshot.parquet"

                if os.path.exists(relation_path_csv):
                    relation_snapshot = pd.read_csv(relation_path_csv)
                elif os.path.exists(relation_path_parquet):
                    relation_snapshot = pd.read_parquet(relation_path_parquet)

                if relation_snapshot is None:
                    continue

                row = relation_snapshot[relation_snapshot["InputId"] == record.get(field)]

                if len(row) > 0:
                    record[field] = row.iloc[0]["RemoteId"]

        return record

    def _process_state_message(self, message_dict: dict) -> None:
        """Process a state message. drain sinks if needed."""
        # Determine where to store state based on streaming_job
        if self.streaming_job:
            self._assert_line_requires(message_dict, requires={"value"})
            state = message_dict["value"]
            current_state = self._latest_state["tap"]
            if current_state == state:
                return
            self._latest_state["tap"] = state
        else:
            if not self._latest_state:
                self._assert_line_requires(message_dict, requires={"value"})
                state = message_dict["value"]
                if self._latest_state == state:
                    return
                self._latest_state = state
        if self._max_record_age_in_minutes > self._MAX_RECORD_AGE_IN_MINUTES:
            self.logger.info(
                "One or more records have exceeded the max age of "
                f"{self._MAX_RECORD_AGE_IN_MINUTES} minutes. Draining all sinks."
            )
            self.drain_all()

    def _validate_unified_schema(self, sink: Sink, transformed_record: dict) -> dict:
        """Validate the unified schema for a sink."""

        def flatten_dict_keys(dictionary: dict, parent_key=''):
            keys = set()
            for key, value in dictionary.items():
                new_key = f"{parent_key}.{key}" if parent_key else key
                if isinstance(value, dict):
                    keys.update(flatten_dict_keys(value, new_key))
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            keys.update(flatten_dict_keys(item, new_key))
                else:
                    keys.add(new_key)
            return keys

        success = True
        if hasattr(sink, 'auto_validate_unified_schema') and sink.auto_validate_unified_schema \
            and hasattr(sink, 'unified_schema') and sink.unified_schema and issubclass(sink.unified_schema, pydantic.BaseModel):
            try:
                unified_record = sink.unified_schema.model_validate(transformed_record, strict=True)
                unified_transformed = unified_record.model_dump(exclude_none=True, exclude_unset=True)
                extra_fields = flatten_dict_keys(transformed_record) - flatten_dict_keys(unified_transformed)
                if extra_fields:
                    self.logger.warning(f"Extra fields found in {sink.name} will be ignored: {', '.join(extra_fields)}")
                transformed_record = unified_transformed
            except pydantic.ValidationError as e:
                error_msg_fields = "; ".join([f"'{'.'.join(map(str, err.get('loc', tuple())))}' -> {err.get('msg')} (got value {err.get('input')} of type {type(err.get('input')).__name__})" for err in e.errors()])
                error_msg = f"Failed Structure/Datatype validation for {sink.name}: {error_msg_fields}"
                self.logger.error(error_msg)
                
                if not sink.latest_state:
                    sink.init_state()

                state = {"success": False, "error": error_msg}
                id = transformed_record.get("id")
                if id:
                    state["id"] = str(id)
                external_id = transformed_record.get("externalId")
                if external_id:
                    state["externalId"] = external_id
                sink.update_state(state)
                success = False

        return success, transformed_record

    def _process_record_message(self, message_dict: dict) -> None:
        """Process a RECORD message."""
        self._assert_line_requires(message_dict, requires={"stream", "record"})

        stream_name = message_dict["stream"]
        for stream_map in self.mapper.stream_maps[stream_name]:
            # new_schema = helpers._float_to_decimal(new_schema)
            raw_record = copy.copy(message_dict["record"])

            lower_raw_record = {k.lower(): v for k, v in raw_record.items()}

            external_id = lower_raw_record.get(self.EXTERNAL_ID_KEY.lower())

            transformed_record = stream_map.transform(raw_record)
            if transformed_record is None:
                # Record was filtered out by the map transform
                continue

            sink = self.get_sink(stream_map.stream_alias, record=transformed_record)

            if not sink:
                continue

            context = sink._get_context(transformed_record)
            if sink.include_sdc_metadata_properties:
                sink._add_sdc_metadata_to_record(
                    transformed_record, message_dict, context
                )
            else:
                sink._remove_sdc_metadata_from_record(transformed_record)

            sink._validate_and_parse(transformed_record)

            sink.tally_record_read()

            validation_success, transformed_record = self._validate_unified_schema(sink, transformed_record)
            if not validation_success:
                continue

            transformed_record = self.get_record_id(sink.name, transformed_record, sink.relation_fields if hasattr(sink, 'relation_fields') else None)

            if not self.name in sink.allows_externalid:
                external_id = transformed_record.pop(self.EXTERNAL_ID_KEY, None)

            transformed_record = sink.preprocess_record(transformed_record, context)

            if transformed_record and external_id:
                transformed_record[self.EXTERNAL_ID_KEY] = external_id

            sink.process_record(transformed_record, context)
            sink._after_process_record(context)

            if sink.is_full:
                self.logger.info(
                    f"Target sink for '{sink.stream_name}' is full. Draining..."
                )
                self.drain_one(sink)


            sink_latest_state = sink.latest_state or {}
            if self.streaming_job:
                if not self._latest_state:
                    # If "self._latest_state" is empty, save the value of "sink.latest_state"
                    self._latest_state["target"] = sink_latest_state
                else:
                    # If "self._latest_state" is not empty, update all its fields with the
                    # fields from "sink.latest_state" (if they exist)
                    for key in self._latest_state["target"].keys():
                        if isinstance(self._latest_state[key], dict):
                            self._latest_state[key].update(sink_latest_state.get(key) or dict())
            else:
                if not self._latest_state:
                    # If "self._latest_state" is empty, save the value of "sink.latest_state"
                    self._latest_state = sink_latest_state
                else:
                    # If "self._latest_state" is not empty, update all its fields with the
                    # fields from "sink.latest_state" (if they exist)
                    for key in self._latest_state.keys():
                        if isinstance(self._latest_state[key], dict):
                            self._latest_state[key].update(sink_latest_state.get(key) or dict())

    @classproperty
    def cli(cls) -> Callable:
        """Execute standard CLI handler for taps.

        Returns:
            A callable CLI object.
        """

        @common_options.PLUGIN_VERSION
        @common_options.PLUGIN_ABOUT
        @common_options.PLUGIN_ABOUT_FORMAT
        @common_options.PLUGIN_CONFIG
        @common_options.PLUGIN_FILE_INPUT
        @click.option(
            "--state",
            multiple=False,
            help="State file location.",
            type=click.STRING,
            default=(),
        )
        @click.command(
            help="Execute the Singer target.",
            context_settings={"help_option_names": ["--help"]},
        )
        def cli(
            version: bool = False,
            about: bool = False,
            config: Tuple[str, ...] = (),
            state: str = None,
            format: str = None,
            file_input: FileIO = None,
        ) -> None:
            """Handle command line execution.

            Args:
                version: Display the package version.
                about: Display package metadata and settings.
                format: Specify output style for `--about`.
                config: Configuration file location or 'ENV' to use environment
                    variables. Accepts multiple inputs as a tuple.
                file_input: Specify a path to an input file to read messages from.
                    Defaults to standard in if unspecified.

            Raises:
                FileNotFoundError: If the config file does not exist.
            """
            if version:
                cls.print_version()
                return

            if not about:
                cls.print_version(print_fn=cls.logger.info)
            else:
                cls.print_about(format=format)
                return

            validate_config: bool = True

            cls.print_version(print_fn=cls.logger.info)

            parse_env_config = False
            config_files: List[PurePath] = []
            for config_path in config:
                if config_path == "ENV":
                    # Allow parse from env vars:
                    parse_env_config = True
                    continue

                # Validate config file paths before adding to list
                if not Path(config_path).is_file():
                    raise FileNotFoundError(
                        f"Could not locate config file at '{config_path}'."
                        "Please check that the file exists."
                    )

                config_files.append(Path(config_path))
            state = None if state == "()" else state
            target = cls(  # type: ignore  # Ignore 'type not callable'
                config=config_files or None,
                parse_env_config=parse_env_config,
                validate_config=validate_config,
                state=state,
            )

            target.listen(file_input)

        return cli

