from dlthub.common.exceptions import DltPlusException
from dlthub.dbt_generator.types import TableReference


class DbtGeneratorException(DltPlusException):
    pass


class FilesExistException(DbtGeneratorException, FileExistsError):
    def __init__(self, path: str) -> None:
        super().__init__(f"Item(s) at path {path} exist, use the --force flag to allow overwriting")


class InvalidTableReference(DbtGeneratorException):
    def __init__(self, referencing_table: str, reference: TableReference, message: str) -> None:
        message_prefix = (
            f"Invalid reference for table '{referencing_table}' referencing table "
            + f"'{reference['referenced_table']}' with columns {reference['columns']} referencing "
            + f"columns {reference['referenced_columns']}: "
        )
        super().__init__(message_prefix + message)


class InvalidTableReferenceMissingReferencedTable(InvalidTableReference):
    pass


class InvalidTableReferenceMissingReferencingTable(InvalidTableReference):
    pass


class InvalidTableReferenceColumnsMismatch(InvalidTableReference):
    pass


class InvalidTableReferenceNoReferencingColumns(InvalidTableReference):
    pass


class InvalidTableReferenceMissingReferencingTableColumns(InvalidTableReference):
    pass


class InvalidTableReferenceMissingReferencedTableColumns(InvalidTableReference):
    pass


class InvalidTableReferenceIncompleteCompoundKeyReference(InvalidTableReference):
    pass
