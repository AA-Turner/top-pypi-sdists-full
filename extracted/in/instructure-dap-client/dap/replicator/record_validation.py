"""
Validation of record values that cannot be stored by the target database.

The DAP schema declares floating-point columns as ``float64``/``float32``, which map
to a Python ``float`` and to a native floating-point column in the target database.
IEEE-754 permits the non-finite values ``inf``, ``-inf`` and ``nan``, but SQL Server
and MySQL cannot store them in such a column: the driver rejects the whole parameter
batch, aborting the table load. PostgreSQL accepts them.

Rows are streamed to the driver in batches of ``pysqlsync.base.BATCH_SIZE``, so by the
time a batch is rejected the offending record can no longer be identified: it has been
consumed along with the rest of the batch. The error surfaced to the user is the raw
driver message, which names only the ordinal position of the parameter in the prepared
statement. Checking the values as they stream past lets the CLI report the table,
column, primary key and value instead.

Batching also means that beyond the first batch, the records preceding the failure have
already been written. Whether those rows obstruct a retry depends on how they were
written, which the ``uses_upsert`` flag below conveys.
"""

import math
from dataclasses import dataclass
from typing import Any, AsyncIterator, Optional, Sequence

from ..integration.database_errors import NonFiniteNumericValueError

# Dialects whose floating-point type cannot represent `inf`, `-inf` or `nan`. PostgreSQL
# stores them as `Infinity`/`NaN`, so records are passed through unvalidated there; a
# database that accepts the value must keep accepting it.
DIALECTS_REJECTING_NON_FINITE: frozenset[str] = frozenset({"mssql", "mysql"})


def rejects_non_finite(dialect: str) -> bool:
    """
    Returns whether the target database rejects non-finite floating-point values.

    :param dialect: The database dialect, e.g. ``postgresql``, ``mysql`` or ``mssql``.
    """

    return dialect in DIALECTS_REJECTING_NON_FINITE


def find_float_field_indices(field_types: Sequence[type]) -> tuple[int, ...]:
    """
    Determines which fields of a record hold a floating-point value.

    Only ``float`` is considered: ``decimal.Decimal`` columns are backed by a
    fixed-precision numeric type, which every supported database accepts.

    :param field_types: The TSV storage types of the fields of a record, in record order.
    :returns: The indices of the floating-point fields, in ascending order.
    """

    return tuple(
        index for index, field_type in enumerate(field_types) if field_type is float
    )


def find_non_finite_field(
    record: Sequence[Any], float_field_indices: Sequence[int]
) -> Optional[int]:
    """
    Looks for a non-finite floating-point value in a record.

    :param record: The field values of a single record.
    :param float_field_indices: The indices of the floating-point fields, as returned
        by :func:`find_float_field_indices`.
    :returns: The index of the first field holding a non-finite value, or ``None`` if
        all floating-point fields are finite (or absent).
    """

    for index in float_field_indices:
        value = record[index]
        # `math.isfinite` would reject `None`, which is how a NULL field is represented.
        if value is not None and not math.isfinite(value):
            return index
    return None


@dataclass(frozen=True)
class _RecordChecker:
    """
    The per-record check, with everything derivable from the table set up once.

    Both entry points below iterate differently -- one over a list, one over an
    asynchronous stream -- but do the same work per record, which lives here.
    """

    float_field_indices: tuple[int, ...]
    primary_key_index: Optional[int]
    field_names: Sequence[str]
    namespace: str
    table_name: str
    primary_key_name: Optional[str]
    dialect: str
    uses_upsert: bool

    @property
    def is_noop(self) -> bool:
        "Whether no record can fail the check, so iteration need not inspect any."

        return not self.float_field_indices

    def check(self, record: Sequence[Any]) -> None:
        """
        :param record: The field values of a single record.
        :raises NonFiniteNumericValueError: If a floating-point field holds ``inf``,
            ``-inf`` or ``nan``.
        """

        offending_index = find_non_finite_field(record, self.float_field_indices)
        if offending_index is None:
            return

        primary_key_value = (
            record[self.primary_key_index]
            if self.primary_key_index is not None
            else None
        )
        raise NonFiniteNumericValueError(
            namespace=self.namespace,
            table_name=self.table_name,
            column_name=self.field_names[offending_index],
            value=record[offending_index],
            dialect=self.dialect,
            primary_key_name=self.primary_key_name,
            primary_key_value=primary_key_value,
            retry_needs_empty_table=not self.uses_upsert,
        )


def _record_checker(
    field_names: Sequence[str],
    field_types: Sequence[type],
    namespace: str,
    table_name: str,
    primary_key_name: Optional[str],
    dialect: str,
    uses_upsert: bool,
) -> _RecordChecker:
    "Prepares the per-record check for one table and target database."

    # a database that stores non-finite values has nothing to check
    float_field_indices = (
        find_float_field_indices(field_types) if rejects_non_finite(dialect) else ()
    )
    primary_key_index = (
        field_names.index(primary_key_name)
        if primary_key_name is not None and primary_key_name in field_names
        else None
    )
    return _RecordChecker(
        float_field_indices=float_field_indices,
        primary_key_index=primary_key_index,
        field_names=field_names,
        namespace=namespace,
        table_name=table_name,
        primary_key_name=primary_key_name,
        dialect=dialect,
        uses_upsert=uses_upsert,
    )


def validate_records(
    records: Sequence[Sequence[Any]],
    *,
    field_names: Sequence[str],
    field_types: Sequence[type],
    namespace: str,
    table_name: str,
    primary_key_name: Optional[str],
    dialect: str,
    uses_upsert: bool = False,
) -> None:
    """
    Checks a batch of records for values the database cannot store.

    Counterpart of :func:`validated_records` for call sites that have already
    materialized the records into a list.

    :param records: The records to check.
    :param field_names: The field names of a record, in record order.
    :param field_types: The TSV storage types of a record, in record order.
    :param namespace: The namespace of the table being loaded, e.g. ``canvas``.
    :param table_name: The name of the table being loaded.
    :param primary_key_name: The primary key field, used to identify the offending
        record to the user. ``None`` if the key is not among the fields.
    :param dialect: The target database dialect. Validation is skipped for dialects
        that can store non-finite values.
    :param uses_upsert: Whether the operation upserts rather than inserts. Records
        preceding the offending one may already have been written; an insert would
        collide with them on a retry, so the error tells the user to empty the table
        first, whereas an upsert is idempotent and can simply be re-run.
    :raises NonFiniteNumericValueError: If a floating-point field holds ``inf``,
        ``-inf`` or ``nan``.
    """

    checker = _record_checker(
        field_names,
        field_types,
        namespace,
        table_name,
        primary_key_name,
        dialect,
        uses_upsert,
    )
    if checker.is_noop:
        return

    for record in records:
        checker.check(record)


def validated_records(
    records: AsyncIterator[tuple[Any, ...]],
    *,
    field_names: Sequence[str],
    field_types: Sequence[type],
    namespace: str,
    table_name: str,
    primary_key_name: Optional[str],
    dialect: str,
    uses_upsert: bool = False,
) -> AsyncIterator[tuple[Any, ...]]:
    """
    Wraps a record stream so that a value the database cannot store is reported.

    Checking in the streaming path keeps the offending record available to be named in
    the error message. When no record could fail the check -- the target database
    stores non-finite values, or the table has no floating-point column -- the original
    iterator is returned unwrapped, leaving the row-level path untouched.

    :param records: The records read from the downloaded data files.
    :param field_names: The field names of a record, in record order.
    :param field_types: The TSV storage types of a record, in record order.
    :param namespace: The namespace of the table being loaded, e.g. ``canvas``.
    :param table_name: The name of the table being loaded.
    :param primary_key_name: The primary key field, used to identify the offending
        record to the user. ``None`` if the key is not among the fields.
    :param dialect: The target database dialect. Validation is skipped for dialects
        that can store non-finite values.
    :param uses_upsert: Whether the operation upserts rather than inserts. Records
        preceding the offending one may already have been written; an insert would
        collide with them on a retry, so the error tells the user to empty the table
        first, whereas an upsert is idempotent and can simply be re-run.
    :returns: The records, checked as they are consumed.
    """

    checker = _record_checker(
        field_names,
        field_types,
        namespace,
        table_name,
        primary_key_name,
        dialect,
        uses_upsert,
    )
    if checker.is_noop:
        return records
    return _checked_records(records, checker)


async def _checked_records(
    records: AsyncIterator[tuple[Any, ...]], checker: _RecordChecker
) -> AsyncIterator[tuple[Any, ...]]:
    """
    :raises NonFiniteNumericValueError: If a floating-point field holds ``inf``,
        ``-inf`` or ``nan``.
    """

    async for record in records:
        checker.check(record)
        yield record
