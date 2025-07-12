import json
import logging
import uuid
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union
from urllib.parse import urlparse

import boto3
import pyarrow
from botocore.exceptions import ClientError
from pyiceberg.catalog import MetastoreCatalog
from pyiceberg.catalog import PropertiesUpdateSummary
from pyiceberg.exceptions import CommitFailedException
from pyiceberg.exceptions import NoSuchTableError
from pyiceberg.io import FileIO
from pyiceberg.partitioning import UNPARTITIONED_PARTITION_SPEC
from pyiceberg.partitioning import PartitionSpec
from pyiceberg.schema import Schema
from pyiceberg.serializers import FromInputFile
from pyiceberg.table import CommitTableRequest
from pyiceberg.table import CommitTableResponse
from pyiceberg.table import CreateTableTransaction
from pyiceberg.table import StagedTable
from pyiceberg.table import Table
from pyiceberg.table import TableRequirement
from pyiceberg.table import TableUpdate
from pyiceberg.table.metadata import new_table_metadata
from pyiceberg.table.sorting import UNSORTED_SORT_ORDER
from pyiceberg.table.sorting import SortOrder
from pyiceberg.typedef import EMPTY_DICT
from pyiceberg.typedef import Identifier
from pyiceberg.typedef import Properties


logger = logging.getLogger(__name__)


def _read_json(io: FileIO, path: str) -> Dict:
    with io.new_input(path).open() as f:
        return json.load(f)


def _write_json(io: FileIO, path: str, content: Dict) -> None:
    with io.new_output(path).create(overwrite=True) as f:
        f.write(json.dumps(content, indent=2).encode("utf-8"))


def _safe_update_metadata_pointer(io: FileIO, path: str, metadata_pointer_content: Dict, is_first_commit: bool) -> None:
    """
    This function performs a conditional write using the ETag of the original file,
    ensuring that the file hasn't been modified by another process between read and write.

    Args:
        metadata_pointer_content: The new metadata content to write
        path: The path for the metadata file
        is_first_commit: Whether this is the first commit
    Returns:
        The updated JSON content that was written

    Raises:
        CommitFailedException: If the file was modified concurrently
    """
    parts = urlparse(path)
    bucket = parts.netloc
    key = parts.path.lstrip("/")

    if parts.scheme != "s3":
        # Conditional writes only supported for S3 in this setup.
        # TODO: support conditional writes for GCS.
        return _write_json(io, path, metadata_pointer_content)

    s3_client = boto3.client("s3")

    params = {}
    if is_first_commit:
        params["IfNoneMatch"] = "*"  # Ensure that the file doesn't exist
    else:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        etag = response.get("ETag", "").strip('"')
        params["IfMatch"] = etag
        prev_metadata_content = json.loads(response["Body"].read().decode("utf-8"))
        prev_version = int(prev_metadata_content["version"])
        new_version = int(metadata_pointer_content["version"])
        if prev_version != new_version - 1:
            # Another concurrent commit already happened.
            msg = f"Commit version mismatch. Attempted new commit version {new_version} is not an increment on the current metadata version {prev_version}."
            raise CommitFailedException(msg)

    metadata_json_content = json.dumps(metadata_pointer_content, indent=2)
    try:
        logger.info(
            f"Writing a new Iceberg metadata pointer version={int(metadata_pointer_content['version'])} and metadata file={metadata_pointer_content['current_metadata_location']} to {path}"
        )
        s3_client.put_object(
            Bucket=bucket, Key=key, Body=metadata_json_content.encode("utf-8"), ContentType="application/json", **params
        )
    except ClientError as e:
        msg = f"Iceberg commit version={metadata_pointer_content['version']} failed."
        raise CommitFailedException(msg) from e


def _new_metadata_file_location(location: str, new_version: int = 0) -> str:
    """Return a fully-qualified metadata file location for a new table version.

    Args:
        new_version (int): Version number of the metadata file.

    Returns:
        str: fully-qualified URI for the new table metadata file.

    Raises:
        ValueError: If the version is negative.
    """
    if new_version < 0:
        msg = f"Table metadata version: `{new_version}` must be a non-negative integer."
        raise ValueError(msg)

    version_str = f"{new_version:05d}"
    return f"{location}/metadata/{version_str}-{uuid.uuid4()}.metadata.json"


class MetadataCatalog(MetastoreCatalog):
    POINTER_FILE = "_current_metadata.json"

    def __init__(self, name: str, properties: Dict) -> None:
        super().__init__(name, **properties)

    def _base_location(self, location: str) -> str:
        if not location.endswith("/"):
            location += "/"
        return location

    def create_table(
        self,
        identifier: Union[str, Identifier],
        schema: Union[Schema, "pyarrow.Schema"],
        location: Optional[str] = None,
        partition_spec: PartitionSpec = UNPARTITIONED_PARTITION_SPEC,
        sort_order: SortOrder = UNSORTED_SORT_ORDER,
        properties: Properties = EMPTY_DICT,
    ) -> Table:
        schema: Schema = self._convert_schema_if_needed(schema)  # type: ignore

        metadata_location = _new_metadata_file_location(location=location)
        metadata = new_table_metadata(
            location=location,
            schema=schema,
            partition_spec=partition_spec,
            sort_order=sort_order,
            properties=properties,
        )
        io = self._load_file_io(properties=properties, location=metadata_location)
        staged_table = StagedTable(
            identifier=identifier,
            metadata=metadata,
            metadata_location=metadata_location,
            io=io,
            catalog=self,
        )

        self._write_metadata(staged_table.metadata, staged_table.io, staged_table.metadata_location)
        metadata_version = self._parse_metadata_version(staged_table.metadata_location)

        # Write metadata pointer file
        metadata_pointer_content = {
            "current_metadata_location": staged_table.metadata_location,
            "version": metadata_version,
        }
        metadata_pointer_path = self._base_location(location) + self.POINTER_FILE
        _safe_update_metadata_pointer(
            staged_table.io, metadata_pointer_path, metadata_pointer_content, is_first_commit=True
        )

        return self.load_table(location=location)

    def create_table_transaction(
        self,
        identifier: Union[str, Identifier],
        schema: Union[Schema, "pyarrow.Schema"],
        location: Optional[str] = None,
        partition_spec: PartitionSpec = UNPARTITIONED_PARTITION_SPEC,
        sort_order: SortOrder = UNSORTED_SORT_ORDER,
        properties: Properties = EMPTY_DICT,
    ) -> CreateTableTransaction:
        raise NotImplementedError

    def load_table(self, location: str) -> Table:
        base = self._base_location(location)
        metadata_pointer_path = base + self.POINTER_FILE
        io = self._load_file_io(location=base)

        try:
            metadata_pointer = _read_json(io, metadata_pointer_path)
        except Exception as _:
            msg = f"Table not found at {metadata_pointer_path}"
            raise NoSuchTableError(msg)

        metadata_location = metadata_pointer["current_metadata_location"]
        file = io.new_input(metadata_location)
        metadata = FromInputFile.table_metadata(file)
        return Table((location,), metadata, metadata_location, io, self)

    def table_exists(self, identifier: Union[str, Identifier]) -> bool:
        base = self._base_location(identifier)
        pointer_path = base + self.POINTER_FILE
        io = self._load_file_io(location=base)
        try:
            _ = _read_json(io, pointer_path)
            return True
        except FileNotFoundError as _:
            return False

    def register_table(self, identifier: Union[str, Identifier], metadata_location: str) -> Table:
        """Register a new table using existing metadata.

        Args:
            identifier Union[str, Identifier]: Table identifier for the table
            metadata_location str: The location to the metadata

        Returns:
            Table: The newly registered table

        Raises:
            TableAlreadyExistsError: If the table already exists
        """
        raise NotImplementedError

    def drop_table(self, identifier: Union[str, Identifier]) -> None:
        raise NotImplementedError

    def purge_table(self, identifier: Union[str, Identifier]) -> None:
        raise NotImplementedError

    def rename_table(self, from_identifier: Union[str, Identifier], to_identifier: Union[str, Identifier]) -> Table:
        raise NotImplementedError

    def commit_table(
        self, table: Table, requirements: Tuple[TableRequirement, ...], updates: Tuple[TableUpdate, ...]
    ) -> CommitTableResponse:
        """Commit updates to a table.

        Args:
            table (Table): The table to be updated.
            requirements: (Tuple[TableRequirement, ...]): Table requirements.
            updates: (Tuple[TableUpdate, ...]): Table updates.

        Returns:
            CommitTableResponse: The updated metadata.

        Raises:
            NoSuchTableError: If a table with the given identifier does not exist.
            CommitFailedException: Requirement not met, or a conflict with a concurrent commit.
        """
        if not table:
            raise NoSuchTableError()

        table_identifier = table.name()
        updated_staged_table = self._update_and_stage_table(table, table_identifier, requirements, updates)
        if updated_staged_table.metadata == table.metadata:
            # no changes, do nothing
            return CommitTableResponse(metadata=table.metadata, metadata_location=table.metadata_location)
        return self.__commit_table(updated_staged_table)

    # Note: `_commit_table` maintains abstract class compatibility with pyiceberg 0.7
    def _commit_table(self, table_request: CommitTableRequest) -> CommitTableResponse:
        table = self.load_table(table_request.identifier.name)
        if not table:
            raise NoSuchTableError()

        updated_staged_table = self.__update_and_stage_table(table, table_request)
        if updated_staged_table.metadata == table.metadata:
            # no changes, do nothing
            return CommitTableResponse(metadata=table.metadata, metadata_location=table.metadata_location)
        return self.__commit_table(updated_staged_table)

    def __commit_table(self, updated_staged_table: StagedTable) -> CommitTableResponse:
        table_identifier = updated_staged_table.name()
        new_metadata_version = self._parse_metadata_version(updated_staged_table.metadata_location)

        metadata_pointer_path = self._base_location(table_identifier[-1]) + self.POINTER_FILE
        metadata_content = _read_json(updated_staged_table.io, metadata_pointer_path)
        prev_metadata_version = int(metadata_content["version"])
        if prev_metadata_version != new_metadata_version - 1:
            # Another concurrent commit already happened.
            msg = f"Commit version mismatch. Attempted new commit version {new_metadata_version} is not an increment on the current metadata version {prev_metadata_version}."
            raise CommitFailedException(msg)

        self._write_metadata(
            metadata=updated_staged_table.metadata,
            io=updated_staged_table.io,
            metadata_path=updated_staged_table.metadata_location,
        )

        # Update the metadata pointer file
        metadata_content["current_metadata_location"] = updated_staged_table.metadata_location
        metadata_content["version"] = new_metadata_version
        _safe_update_metadata_pointer(
            updated_staged_table.io, metadata_pointer_path, metadata_content, is_first_commit=False
        )

        return CommitTableResponse(
            metadata=updated_staged_table.metadata, metadata_location=updated_staged_table.metadata_location
        )

    def __update_and_stage_table(
        self, current_table: Optional[Table], table_request: CommitTableRequest
    ) -> StagedTable:
        return self._update_and_stage_table(current_table, table_request)

    def create_namespace(self, namespace: Union[str, Identifier], properties: Properties = EMPTY_DICT) -> None:
        raise NotImplementedError

    def drop_namespace(self, namespace: Union[str, Identifier]) -> None:
        raise NotImplementedError

    def list_tables(self, namespace: Union[str, Identifier]) -> List[Identifier]:
        raise NotImplementedError

    def list_namespaces(self, namespace: Union[str, Identifier] = ()) -> List[Identifier]:
        raise NotImplementedError

    def load_namespace_properties(self, namespace: Union[str, Identifier]) -> Properties:
        raise NotImplementedError

    def update_namespace_properties(
        self, namespace: Union[str, Identifier], removals: Optional[Set[str]] = None, updates: Properties = EMPTY_DICT
    ) -> PropertiesUpdateSummary:
        raise NotImplementedError

    def list_views(self, namespace: Union[str, Identifier]) -> List[Identifier]:
        raise NotImplementedError

    def drop_view(self, identifier: Union[str, Identifier]) -> None:
        raise NotImplementedError

    def view_exists(self, identifier: Union[str, Identifier]) -> bool:
        raise NotImplementedError
