import dataclasses
import json
import shutil
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Generic, List, Optional, Type, TypeVar

from abstra_json_sql.eval import eval_sql
from abstra_json_sql.persistence import FileSystemJsonTables
from abstra_json_sql.tables import Column, ColumnType, Table

from abstra_internals.interface.sdk.tables.utils import serialize
from abstra_internals.logger import AbstraLogger
from abstra_internals.settings import Settings
from abstra_internals.utils.file_lock import create_file_lock
from abstra_internals.utils.serializable import Serializable

T = TypeVar("T", bound=Serializable)

MAX_RETRIES = 5
BASE_DELAY = 0.05


class SqlStorage(Generic[T]):
    def __init__(self, directory: str, model: Type[T]):
        self._thread_lock = threading.RLock()
        self.directory = directory
        self.model = model
        self.table_name = "data"
        self._tables_instance: Optional[FileSystemJsonTables] = None
        self.directory_path.mkdir(parents=True, exist_ok=True)
        self._lock_path = str(self.directory_path / ".lock")
        self.health_check()

    @property
    def directory_path(self) -> Path:
        return Settings.root_path / self.directory

    @contextmanager
    def _locked(self):
        """Acquire both thread lock (intra-process) and file lock (cross-process)."""
        with self._thread_lock:
            lock = create_file_lock(self._lock_path)
            lock.acquire()
            try:
                yield
            finally:
                try:
                    lock.release()
                except OSError as release_error:
                    AbstraLogger.capture_exception(release_error)

    @property
    def tables(self) -> FileSystemJsonTables:
        """Get or create a FileSystemJsonTables instance."""
        if self._tables_instance is None:
            self.directory_path.mkdir(parents=True, exist_ok=True)
            self._tables_instance = FileSystemJsonTables(workdir=self.directory_path)
        return self._tables_instance

    def _table_exists(self) -> bool:
        metadata_path = self.directory_path / "__schema__.json"
        if not metadata_path.exists():
            return False
        try:
            metadata = json.loads(metadata_path.read_text())
        except (json.JSONDecodeError, OSError):
            return False
        return any(
            info.get("table_name") == self.table_name for info in metadata.values()
        )

    def _ensure_table_exists(self) -> None:
        """Ensure the table exists in the database."""
        try:
            # Try to get the table to see if it exists
            self.tables.get_table(self.table_name)
        except (FileNotFoundError, Exception):
            # If the table doesn't exist, create it
            # Always start with an id column
            columns = [Column(name="id", schema=ColumnType.string, is_primary_key=True)]

            if dataclasses.is_dataclass(self.model):
                for f in dataclasses.fields(self.model):
                    if f.name != "id":  # Skip if model already has id
                        columns.append(Column(name=f.name, schema=ColumnType.string))

            table = Table(
                name=self.table_name,
                columns=columns,
                data=[],
            )
            try:
                self.tables.add_table(table)
            except ValueError:
                pass

    def _serialize_value(self, value) -> str:
        """Serialize a value to a string for SQL storage."""
        serialized = serialize(value)
        if serialized is None:
            return ""
        if isinstance(serialized, str):
            return serialized
        return json.dumps(serialized)

    def _escape_sql_string(self, value: str) -> str:
        """Escape single quotes in SQL string literals."""
        return value.replace("'", "''")

    def _execute_with_retry(self, sql_code: str) -> list:
        last_exception: Optional[json.JSONDecodeError] = None
        for attempt in range(MAX_RETRIES):
            try:
                result = eval_sql(
                    code=sql_code,
                    tables=self.tables,
                    ctx={},
                )
                return result if result is not None else []
            except json.JSONDecodeError as e:
                last_exception = e
                if attempt < MAX_RETRIES - 1:
                    time.sleep(BASE_DELAY * (2**attempt))
                    self._tables_instance = None
            except Exception as e:
                AbstraLogger.capture_exception(e)
                raise
        if last_exception is not None:
            AbstraLogger.capture_exception(last_exception)
            raise last_exception
        raise RuntimeError("Unexpected state in _execute_with_retry")

    def _find_data_files(self) -> List[Path]:
        return [
            f for f in self.directory_path.glob("*.json") if f.name != "__schema__.json"
        ]

    def _find_salvageable_position(
        self, raw: bytes, error: json.JSONDecodeError
    ) -> Optional[int]:
        """Find a position to truncate corrupted data and salvage valid JSON.

        Handles two corruption patterns:
        - Null bytes: valid JSON followed by \\x00 padding (torn write with gap)
        - Extra data: valid JSON followed by leftover data from a previous write
        """
        # Pattern 1: null bytes in the middle of the file
        null_pos = raw.find(b"\x00")
        if null_pos > 0:
            return null_pos

        # Pattern 2: "Extra data" — parser found valid JSON then trailing garbage
        if error.msg == "Extra data" and error.pos is not None and error.pos > 0:
            return error.pos

        return None

    def _try_recover_corrupted_data(self) -> bool:
        """Attempt to recover corrupted JSON data files.

        Returns True if any file was recovered or reset.
        """
        recovered = False
        for data_file in self._find_data_files():
            try:
                raw = data_file.read_bytes()
            except OSError:
                continue

            try:
                json.loads(raw)
                continue  # file is valid
            except json.JSONDecodeError as e:
                truncate_pos = self._find_salvageable_position(raw, e)

            if truncate_pos is not None:
                try:
                    valid_content = raw[:truncate_pos].decode("utf-8")
                    json.loads(valid_content)  # validate before writing
                    data_file.write_text(valid_content, encoding="utf-8")
                    AbstraLogger.warning(
                        f"Recovered corrupted file {data_file.name}: "
                        f"salvaged {truncate_pos} bytes out of {len(raw)}"
                    )
                    recovered = True
                    continue
                except (json.JSONDecodeError, UnicodeDecodeError, OSError):
                    pass

            # Cannot salvage — reset to empty array
            data_file.write_text("[]", encoding="utf-8")
            AbstraLogger.warning(
                f"Could not recover {data_file.name} — reset to empty. "
                f"Original size: {len(raw)} bytes"
            )
            recovered = True

        if recovered:
            self._tables_instance = None

        return recovered

    def health_check(self) -> None:
        """Validate data files on startup. Locks only if recovery is needed."""
        for data_file in self._find_data_files():
            try:
                raw = data_file.read_bytes()
                json.loads(raw)
            except (json.JSONDecodeError, OSError):
                with self._locked():
                    self._try_recover_corrupted_data()
                return

    def save(self, id: str, data: T) -> None:
        with self._locked():
            self._ensure_table_exists()

            # Convert the model to dict and serialize values
            data_dict = data.dump()

            # Add the id to the data dict if it's not already there
            if "id" not in data_dict:
                data_dict["id"] = id

            # Serialize values
            serialized_dict = {}
            for key, value in data_dict.items():
                serialized_dict[key] = self._serialize_value(value)

            # Check if record exists
            try:
                result = self._execute_with_retry(
                    f'SELECT "id" FROM {self.table_name} WHERE "id" = \'{self._escape_sql_string(id)}\''
                )
            except json.JSONDecodeError:
                self._try_recover_corrupted_data()
                self._ensure_table_exists()
                try:
                    result = self._execute_with_retry(
                        f'SELECT "id" FROM {self.table_name} WHERE "id" = \'{self._escape_sql_string(id)}\''
                    )
                except Exception as e:
                    AbstraLogger.capture_exception(e)
                    result = []
            except Exception as e:
                AbstraLogger.capture_exception(e)
                result = []

            if result and len(result) > 0:
                # Update existing record
                # Use double quotes for column names to handle SQL keywords
                set_parts = []
                for key, value in serialized_dict.items():
                    if key != "id":
                        escaped_value = self._escape_sql_string(value)
                        set_parts.append(f"\"{key}\" = '{escaped_value}'")

                if set_parts:
                    set_clause = ", ".join(set_parts)
                    self._execute_with_retry(
                        f"UPDATE {self.table_name} SET {set_clause} WHERE \"id\" = '{self._escape_sql_string(id)}'"
                    )
            else:
                # Insert new record
                # Use double quotes for column names to handle SQL keywords
                columns = ", ".join([f'"{key}"' for key in serialized_dict.keys()])
                values = ", ".join(
                    [
                        f"'{self._escape_sql_string(value)}'"
                        for value in serialized_dict.values()
                    ]
                )
                sql_command = (
                    f"INSERT INTO {self.table_name} ({columns}) VALUES ({values})"
                )
                self._execute_with_retry(sql_command)

    def _load_all_rows(self) -> List[T]:
        result = self._execute_with_retry(f"SELECT * FROM {self.table_name}")
        data_list = []
        if result is not None:
            for row in result:
                try:
                    deserialized_row = self._deserialize_row(row)
                    data_list.append(self.model.model_validate(deserialized_row))
                except Exception as e:
                    AbstraLogger.capture_exception(e)
                    continue
        return data_list

    def load_all(self) -> List[T]:
        if not self._table_exists():
            return []
        try:
            return self._load_all_rows()
        except json.JSONDecodeError:
            with self._locked():
                if self._try_recover_corrupted_data():
                    try:
                        return self._load_all_rows()
                    except Exception as e:
                        AbstraLogger.capture_exception(e)
                        return []
                return []
        except Exception as e:
            AbstraLogger.capture_exception(e)
            return []

    def load(self, id: str) -> Optional[T]:
        if not self._table_exists():
            return None
        return self._load(id)

    def delete(self, id: str) -> None:
        with self._locked():
            try:
                self._ensure_table_exists()
                self._execute_with_retry(
                    f"DELETE FROM {self.table_name} WHERE \"id\" = '{self._escape_sql_string(id)}'"
                )
            except Exception as e:
                AbstraLogger.capture_exception(e)

    def clear(self) -> None:
        with self._locked():
            try:
                self._ensure_table_exists()
                self._execute_with_retry(f"DELETE FROM {self.table_name}")
            except Exception as e:
                shutil.rmtree(self.directory_path, ignore_errors=True)
                self._tables_instance = None
                AbstraLogger.capture_exception(e)

    def _deserialize_row(self, row: dict) -> dict:
        """Deserialize row data, converting JSON strings back to objects."""
        deserialized = {}
        for key, value in row.items():
            if isinstance(value, str) and value.strip():
                # Try to parse as JSON
                try:
                    deserialized[key] = json.loads(value)
                except (json.JSONDecodeError, ValueError):
                    # If it's not valid JSON, keep as string
                    deserialized[key] = value
            elif value == "":
                # Empty strings might represent None
                deserialized[key] = None
            else:
                deserialized[key] = value
        return deserialized

    def _load(self, id: str) -> Optional[T]:
        try:
            result = self._execute_with_retry(
                f"SELECT * FROM {self.table_name} WHERE \"id\" = '{self._escape_sql_string(id)}'"
            )

            if result and len(result) > 0:
                deserialized_row = self._deserialize_row(result[0])
                return self.model.model_validate(deserialized_row)

            return None
        except Exception as e:
            AbstraLogger.capture_exception(e)
            return None
