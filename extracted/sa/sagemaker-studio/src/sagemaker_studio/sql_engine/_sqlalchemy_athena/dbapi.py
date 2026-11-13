"""PEP 249 adapter backed by the SDK's native Athena executor."""

from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from botocore.session import get_session

from sagemaker_studio.utils.athena_v4 import (
    AthenaQueryError,
    AthenaV4Executor,
    WorkgroupInfo,
    _refreshable_credentials,
    workgroup_info,
)

apilevel = "2.0"
threadsafety = 1
paramstyle = "named"


class Warning(Exception):
    pass


class Error(Exception):
    pass


class InterfaceError(Error):
    pass


class DatabaseError(Error):
    pass


class DataError(DatabaseError):
    pass


class OperationalError(DatabaseError):
    pass


class IntegrityError(DatabaseError):
    pass


class InternalError(DatabaseError):
    pass


class ProgrammingError(DatabaseError):
    pass


class NotSupportedError(DatabaseError):
    pass


def _executor_from_config(config: Dict[str, Any]) -> AthenaV4Executor:
    work_group = config.get("work_group")
    region = config.get("region")
    if not work_group or not region:
        raise InterfaceError("Athena requires work_group and region")

    session = get_session()
    model_path = str(Path(__file__).resolve().parents[2] / "boto3_models")
    loader = session.get_component("data_loader")
    if model_path not in loader.search_paths:
        loader.search_paths.insert(0, model_path)

    provider = config.get("credential_provider")
    if provider is not None:
        session._credentials = _refreshable_credentials(provider)
    elif config.get("aws_access_key_id"):
        session.set_credentials(
            config["aws_access_key_id"],
            config.get("aws_secret_access_key"),
            config.get("aws_session_token"),
        )

    client = session.create_client(
        "athena", region_name=region, endpoint_url=config.get("endpoint_url")
    )
    try:
        info = workgroup_info(client, work_group)
    except Exception:
        info = WorkgroupInfo(engine_version=None, managed_storage=False)

    return AthenaV4Executor(
        client,
        work_group,
        catalog=config.get("catalog_name"),
        schema=config.get("schema_name"),
        managed_storage=info.managed_storage,
        workgroup_engine_version=info.engine_version,
        selected_engine_version=config.get("selected_engine_version")
        or config.get("engine_version"),
    )


class Connection:
    def __init__(self, **config: Any):
        self.executor = _executor_from_config(config)
        self.catalog_name = self.executor.catalog or "AwsDataCatalog"
        self.schema_name = self.executor.schema or "default"
        self._closed = False

    def cursor(self) -> "Cursor":
        if self._closed:
            raise InterfaceError("Connection is closed")
        return Cursor(self)

    def close(self) -> None:
        self._closed = True

    def commit(self) -> None:
        if self._closed:
            raise InterfaceError("Connection is closed")

    def rollback(self) -> None:
        if self._closed:
            raise InterfaceError("Connection is closed")


class Cursor:
    arraysize = 1000

    def __init__(self, connection: Connection):
        self.connection = connection
        self.description = None
        self.rowcount = -1
        self.query_id: Optional[str] = None
        self._rows = []
        self._position = 0
        self._closed = False
        self._metadata: Dict[str, Any] = {}

    def __enter__(self) -> "Cursor":
        return self

    def __exit__(self, *_args: Any) -> None:
        self.close()

    def __iter__(self) -> "Cursor":
        return self

    def __next__(self):
        row = self.fetchone()
        if row is None:
            raise StopIteration
        return row

    def close(self) -> None:
        self._closed = True
        self._rows = []

    def execute(self, operation: str, parameters: Any = None) -> "Cursor":
        if self._closed:
            raise InterfaceError("Cursor is closed")
        self.description = None
        self.rowcount = -1
        self.query_id = None
        self._rows = []
        self._position = 0
        self._metadata = {}
        executor = self.connection.executor
        previous = executor.execution_parameters
        executor.execution_parameters = parameters
        try:
            result = executor.execute(operation)
        except (ValueError, TypeError) as error:
            raise ProgrammingError(str(error)) from error
        except AthenaQueryError as error:
            raise OperationalError(str(error)) from error
        except Exception as error:
            raise DatabaseError(str(error)) from error
        finally:
            executor.execution_parameters = previous

        self._metadata = result.execution_metadata or {}
        self.query_id = self._metadata.get("query_execution_id")
        value = result.result
        if hasattr(value, "columns") and hasattr(value, "itertuples"):
            self._rows = list(value.itertuples(index=False, name=None))
            self.description = [
                (str(name), None, None, None, None, None, True) for name in value.columns
            ]
            self.rowcount = len(self._rows)
        else:
            self._rows = []
            self.description = None
            self.rowcount = value if isinstance(value, int) else -1
        self._position = 0
        return self

    def executemany(self, operation: str, seq_of_parameters: Iterable[Any]) -> None:
        for parameters in seq_of_parameters:
            self.execute(operation, parameters)
            if self.description is not None:
                raise NotSupportedError("executemany does not support result-returning statements")

    def fetchone(self):
        self._require_result()
        if self._position >= len(self._rows):
            return None
        row = self._rows[self._position]
        self._position += 1
        return row

    def fetchmany(self, size: Optional[int] = None):
        self._require_result()
        size = self.arraysize if size is None else size
        start = self._position
        self._position = min(start + size, len(self._rows))
        return self._rows[start : self._position]

    def fetchall(self):
        self._require_result()
        rows = self._rows[self._position :]
        self._position = len(self._rows)
        return rows

    def setinputsizes(self, *_args: Any) -> None:
        pass

    def setoutputsize(self, *_args: Any) -> None:
        pass

    def get_execution_metadata(self) -> Dict[str, Any]:
        return dict(self._metadata)

    def _require_result(self) -> None:
        if self._closed:
            raise InterfaceError("Cursor is closed")
        if self.description is None:
            raise ProgrammingError("The last operation did not return rows")


def connect(**kwargs: Any) -> Connection:
    return Connection(**kwargs)
