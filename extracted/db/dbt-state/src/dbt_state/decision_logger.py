from __future__ import annotations

import dacite
import dataclasses
import datetime
import json
import glob
import os
import threading
import typing as t

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from dbt.config.runtime import RuntimeConfig
from dbt.contracts.graph.nodes import (
    CompiledNode,
    ManifestNode,
    SeedNode,
)

from dbt_state.config import RunCacheConfig, CloneIncrementalInDev
import dbt_state.utils as utils


class DataclassEncoder(json.JSONEncoder):
    def default(self, o: t.Any) -> t.Any:
        if dataclasses.is_dataclass(o) and not isinstance(o, type):
            return dataclasses.asdict(o)
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return super().default(o)


DACITE_CONFIG = dacite.Config(
    type_hooks={
        datetime.datetime: datetime.datetime.fromisoformat,
        CloneIncrementalInDev: CloneIncrementalInDev,
    },
)


@dataclass
class RunConfigEntry:
    # subset of RunCacheConfig safe to write to the log file
    defer_to_target: str
    freshness_tolerance_seconds: int
    tolerate_nondeterminism: bool
    clone_incremental_in_dev: CloneIncrementalInDev
    metadata_cache_ttl_seconds: int
    org_id: t.Optional[str]
    snowflake_get_view_ddl_override: t.Optional[str]

    # relevant dbt config
    profile_name: str
    target_name: str
    select: t.List[str]
    exclude: t.List[str]


@dataclass
class RunStartEntry:
    start_timestamp_utc: datetime.datetime
    run_config: RunConfigEntry
    entry_type: t.Literal["run_start"] = "run_start"

    @classmethod
    def from_config(
        cls, run_cache_config: RunCacheConfig, dbt_config: RuntimeConfig
    ) -> RunStartEntry:
        return cls(
            start_timestamp_utc=datetime.datetime.now(datetime.timezone.utc),
            run_config=RunConfigEntry(
                # run cache
                org_id=run_cache_config.org_id,
                defer_to_target=run_cache_config.defer_to,
                freshness_tolerance_seconds=run_cache_config.freshness_tolerance,
                tolerate_nondeterminism=run_cache_config.tolerate_nondeterminism,
                clone_incremental_in_dev=run_cache_config.clone_incremental_in_dev,
                metadata_cache_ttl_seconds=run_cache_config.metadata_cache_ttl,
                snowflake_get_view_ddl_override=run_cache_config.snowflake_get_view_ddl_override,
                # dbt
                profile_name=dbt_config.profile_name,
                target_name=dbt_config.target_name,
                select=list(dbt_config.args.select),
                exclude=list(dbt_config.args.exclude),
            ),
        )

    @classmethod
    def from_dict(cls, data: t.Dict) -> RunStartEntry:
        return dacite.from_dict(cls, data, config=DACITE_CONFIG)

    def to_json(self) -> str:
        return json.dumps(self, cls=DataclassEncoder)


@dataclass
class DevCloneInfo:
    source_table_fqn: str
    target_table_fqn: str


@dataclass
class NodeInfo:
    fqn: str
    node_resource_type: str
    dev_clone: t.Optional[DevCloneInfo] = None
    deferrals: t.Dict[str, str] = field(
        default_factory=dict
    )  # key = original relation name, value = fqn of table it got deferred to
    is_full_refresh: bool = False
    is_incremental_or_snapshot: bool = False
    is_view: bool = False
    is_table: bool = True


@dataclass
class NodeLogEntry:
    node_name: str
    node_info: NodeInfo
    execution_decision_id: t.Optional[str] = None
    entry_type: t.Literal["node"] = "node"

    def to_json(self) -> str:
        return json.dumps(self, cls=DataclassEncoder)

    @classmethod
    def from_dict(cls, data: t.Dict) -> NodeLogEntry:
        return dacite.from_dict(cls, data, config=DACITE_CONFIG)


def create_decision_logger(
    project_root: Path | str, log_path: str, config: RunCacheConfig
) -> BaseDecisionLogger:
    if config.enable_response_logging:
        logger = DecisionLogger(project_root=project_root, log_path=log_path, config=config)
        logger.remove_extra_logs()
        return logger
    return NoOpLogger()


class BaseDecisionLogger(ABC):
    """Abstract base class for decision loggers."""

    @abstractmethod
    def log_run_start(self, dbt_config: RuntimeConfig) -> None:
        """Log the start of a dbt run.

        Must be called before any log_node_start calls since dbt config is required to evaluate per-node properties
        """
        ...

    @abstractmethod
    def log_node_start(self, node: ManifestNode) -> None:
        """Start collecting logging information about a node

        Must be paired with a corresponding log_node_end call.
        """
        ...

    @abstractmethod
    def log_deferral(self, node_name: str, relation_name: str, deferred_to_fqn: str) -> None:
        """Log when a deferral to a table from another environment has occured"""
        ...

    @abstractmethod
    def log_dev_clone(self, node_name: str, source_fqn: str, target_fqn: str) -> None:
        """Log when a local dev clone occurred"""
        ...

    @abstractmethod
    def log_execution_decision_id(self, node_name: str, execution_decision_id: str) -> None:
        """Log ID of the server-side decision response."""
        ...

    @abstractmethod
    def log_node_end(self, node_name: str) -> None:
        """Log and flush a node entry to the log file."""
        ...


class DecisionLogger(BaseDecisionLogger):
    """Decision logger that writes responses to log files."""

    def __init__(self, project_root: Path | str, log_path: str, config: RunCacheConfig) -> None:
        self._project_root = Path(project_root)
        self._log_path = log_path
        self._log_filepath: Path | None = None
        self._config = config
        self._lock = threading.Lock()
        self._inflight: t.Dict[str, NodeLogEntry] = {}
        self.log_limit = config.log_file_limit

    @cached_property
    def log_prefix(self) -> Path:
        """Prefix path for log files."""
        return self.log_dir / self._config.log_prefix

    def logs_filepaths(self, desc: bool = True) -> t.List[Path]:
        """Returns list of existing log files."""
        return [Path(x) for x in sorted(glob.glob(f"{self.log_prefix}*.jsonl"), reverse=desc)]

    @property
    def log_dir(self) -> Path:
        """Directory where log files are stored. Can be overridden via config."""
        if self._config.log_dir_override:
            return Path(self._config.log_dir_override).expanduser()
        if self._project_root is None:
            raise RuntimeError("DecisionLogger not configured with project_root")
        if self._log_path is None:
            raise RuntimeError("DecisionLogger not configured with log_path")
        log_dir = self._project_root / self._log_path / "state"
        return Path(log_dir).expanduser()

    @property
    def log_filepath(self) -> Path:
        """Current log file path for writing. Creates directory if needed."""
        if not self._log_filepath:
            # note: milliseconds are for integration tests that can produce multiple dbt runs in the same second
            ts = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")[:-3]
            self._log_filepath = Path(f"{self.log_prefix}{ts}.jsonl")
            self._log_filepath.parent.mkdir(parents=True, exist_ok=True)
        return self._log_filepath

    def remove_extra_logs(self) -> None:
        """Remove old log files beyond the configured limit."""
        if self.log_limit < 0:
            return

        for path in self.logs_filepaths()[self.log_limit :]:
            os.remove(path)

    def log_run_start(self, dbt_config: RuntimeConfig) -> None:
        self._dbt_config = dbt_config
        self._write_record(RunStartEntry.from_config(self._config, dbt_config))

    def log_node_start(self, node: ManifestNode) -> None:
        if not getattr(self, "_dbt_config", None):
            raise ValueError(
                "log_run_start() must be called before individual model log_node_start()"
            )
        if not isinstance(node, (CompiledNode, SeedNode)):
            return

        self._inflight[node.name] = NodeLogEntry(
            node_name=node.name,
            node_info=NodeInfo(
                fqn=node.relation_name or "",
                node_resource_type=node.resource_type,
                is_full_refresh=utils.is_full_refresh(self._dbt_config, node),
                is_incremental_or_snapshot=utils.is_incremental_or_snapshot(node),
                is_view=utils.is_view(node),
                is_table=utils.is_table(node),
            ),
        )

    def log_dev_clone(self, node_name: str, source_fqn: str, target_fqn: str) -> None:
        if inflight := self._inflight.get(node_name):
            inflight.node_info.dev_clone = DevCloneInfo(
                source_table_fqn=source_fqn, target_table_fqn=target_fqn
            )

    def log_deferral(self, node_name: str, relation_name: str, deferred_to_fqn: str) -> None:
        if inflight := self._inflight.get(node_name):
            inflight.node_info.deferrals[relation_name] = deferred_to_fqn

    def log_execution_decision_id(self, node_name: str, execution_decision_id: str) -> None:
        """Log a decision response to the log file."""
        if inflight := self._inflight.get(node_name):
            inflight.execution_decision_id = execution_decision_id

    def log_node_end(self, node_name: str) -> None:
        if inflight := self._inflight.pop(node_name, None):
            self._write_record(inflight)

    def _write_record(self, record: t.Any) -> None:
        if not hasattr(record, "to_json"):
            raise ValueError("Record must have a to_json() method")

        with self._lock:
            with open(self.log_filepath, "a") as f:
                f.write(f"{record.to_json()}\n")


class NoOpLogger(BaseDecisionLogger):
    """No-op logger that can read existing logs but does not write new ones."""

    def log_run_start(self, dbt_config: RuntimeConfig) -> None:
        """No-op: NoOpLogger does not write logs."""
        ...

    def log_node_start(self, node: ManifestNode) -> None:
        """No-op: NoOpLogger does not write logs."""
        pass

    def log_deferral(self, node_name: str, relation_name: str, deferred_to_fqn: str) -> None:
        """No-op: NoOpLogger does not write logs."""
        pass

    def log_dev_clone(self, node_name: str, source_fqn: str, target_fqn: str) -> None:
        """No-op: NoOpLogger does not write logs."""
        pass

    def log_execution_decision_id(self, node_name: str, execution_decision_id: str) -> None:
        """No-op: NoOpLogger does not write logs."""
        pass

    def log_node_end(self, node_name: str) -> None:
        """No-op: NoOpLogger does not write logs."""
        pass
