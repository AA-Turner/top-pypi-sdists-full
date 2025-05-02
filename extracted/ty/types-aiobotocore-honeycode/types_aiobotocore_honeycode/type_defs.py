"""
Type annotations for honeycode service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_honeycode/type_defs/)

Usage::

    ```python
    from types_aiobotocore_honeycode.type_defs import FailedBatchItemTypeDef

    data: FailedBatchItemTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    ErrorCodeType,
    FormatType,
    ImportDataCharacterEncodingType,
    TableDataImportJobStatusType,
    UpsertActionType,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "FailedBatchItemTypeDef",
    "ResponseMetadataTypeDef",
    "BatchDeleteTableRowsRequestRequestTypeDef",
    "UpsertRowsResultTypeDef",
    "CellInputTypeDef",
    "CellTypeDef",
    "ColumnMetadataTypeDef",
    "DataItemTypeDef",
    "DelimitedTextImportOptionsTypeDef",
    "DescribeTableDataImportJobRequestRequestTypeDef",
    "SourceDataColumnPropertiesTypeDef",
    "FilterTypeDef",
    "VariableValueTypeDef",
    "ImportDataSourceConfigTypeDef",
    "ImportJobSubmitterTypeDef",
    "PaginatorConfigTypeDef",
    "ListTableColumnsRequestRequestTypeDef",
    "TableColumnTypeDef",
    "ListTableRowsRequestRequestTypeDef",
    "ListTablesRequestRequestTypeDef",
    "TableTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "BatchCreateTableRowsResultTypeDef",
    "BatchDeleteTableRowsResultTypeDef",
    "BatchUpdateTableRowsResultTypeDef",
    "InvokeScreenAutomationResultTypeDef",
    "ListTagsForResourceResultTypeDef",
    "StartTableDataImportJobResultTypeDef",
    "BatchUpsertTableRowsResultTypeDef",
    "CreateRowDataTypeDef",
    "UpdateRowDataTypeDef",
    "TableRowTypeDef",
    "ResultRowTypeDef",
    "DestinationOptionsOutputTypeDef",
    "DestinationOptionsTypeDef",
    "QueryTableRowsRequestRequestTypeDef",
    "UpsertRowDataTypeDef",
    "GetScreenDataRequestRequestTypeDef",
    "InvokeScreenAutomationRequestRequestTypeDef",
    "ImportDataSourceTypeDef",
    "ListTableColumnsRequestListTableColumnsPaginateTypeDef",
    "ListTableRowsRequestListTableRowsPaginateTypeDef",
    "ListTablesRequestListTablesPaginateTypeDef",
    "QueryTableRowsRequestQueryTableRowsPaginateTypeDef",
    "ListTableColumnsResultTypeDef",
    "ListTablesResultTypeDef",
    "BatchCreateTableRowsRequestRequestTypeDef",
    "BatchUpdateTableRowsRequestRequestTypeDef",
    "ListTableRowsResultTypeDef",
    "QueryTableRowsResultTypeDef",
    "ResultSetTypeDef",
    "ImportOptionsOutputTypeDef",
    "ImportOptionsTypeDef",
    "BatchUpsertTableRowsRequestRequestTypeDef",
    "GetScreenDataResultTypeDef",
    "TableDataImportJobMetadataTypeDef",
    "ImportOptionsUnionTypeDef",
    "StartTableDataImportJobRequestRequestTypeDef",
    "DescribeTableDataImportJobResultTypeDef",
)

FailedBatchItemTypeDef = TypedDict(
    "FailedBatchItemTypeDef",
    {
        "id": str,
        "errorMessage": str,
    },
)
ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
        "HostId": NotRequired[str],
    },
)
BatchDeleteTableRowsRequestRequestTypeDef = TypedDict(
    "BatchDeleteTableRowsRequestRequestTypeDef",
    {
        "workbookId": str,
        "tableId": str,
        "rowIds": Sequence[str],
        "clientRequestToken": NotRequired[str],
    },
)
UpsertRowsResultTypeDef = TypedDict(
    "UpsertRowsResultTypeDef",
    {
        "rowIds": List[str],
        "upsertAction": UpsertActionType,
    },
)
CellInputTypeDef = TypedDict(
    "CellInputTypeDef",
    {
        "fact": NotRequired[str],
        "facts": NotRequired[Sequence[str]],
    },
)
CellTypeDef = TypedDict(
    "CellTypeDef",
    {
        "formula": NotRequired[str],
        "format": NotRequired[FormatType],
        "rawValue": NotRequired[str],
        "formattedValue": NotRequired[str],
        "formattedValues": NotRequired[List[str]],
    },
)
ColumnMetadataTypeDef = TypedDict(
    "ColumnMetadataTypeDef",
    {
        "name": str,
        "format": FormatType,
    },
)
DataItemTypeDef = TypedDict(
    "DataItemTypeDef",
    {
        "overrideFormat": NotRequired[FormatType],
        "rawValue": NotRequired[str],
        "formattedValue": NotRequired[str],
    },
)
DelimitedTextImportOptionsTypeDef = TypedDict(
    "DelimitedTextImportOptionsTypeDef",
    {
        "delimiter": str,
        "hasHeaderRow": NotRequired[bool],
        "ignoreEmptyRows": NotRequired[bool],
        "dataCharacterEncoding": NotRequired[ImportDataCharacterEncodingType],
    },
)
DescribeTableDataImportJobRequestRequestTypeDef = TypedDict(
    "DescribeTableDataImportJobRequestRequestTypeDef",
    {
        "workbookId": str,
        "tableId": str,
        "jobId": str,
    },
)
SourceDataColumnPropertiesTypeDef = TypedDict(
    "SourceDataColumnPropertiesTypeDef",
    {
        "columnIndex": NotRequired[int],
    },
)
FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "formula": str,
        "contextRowId": NotRequired[str],
    },
)
VariableValueTypeDef = TypedDict(
    "VariableValueTypeDef",
    {
        "rawValue": str,
    },
)
ImportDataSourceConfigTypeDef = TypedDict(
    "ImportDataSourceConfigTypeDef",
    {
        "dataSourceUrl": NotRequired[str],
    },
)
ImportJobSubmitterTypeDef = TypedDict(
    "ImportJobSubmitterTypeDef",
    {
        "email": NotRequired[str],
        "userArn": NotRequired[str],
    },
)
PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)
ListTableColumnsRequestRequestTypeDef = TypedDict(
    "ListTableColumnsRequestRequestTypeDef",
    {
        "workbookId": str,
        "tableId": str,
        "nextToken": NotRequired[str],
    },
)
TableColumnTypeDef = TypedDict(
    "TableColumnTypeDef",
    {
        "tableColumnId": NotRequired[str],
        "tableColumnName": NotRequired[str],
        "format": NotRequired[FormatType],
    },
)
ListTableRowsRequestRequestTypeDef = TypedDict(
    "ListTableRowsRequestRequestTypeDef",
    {
        "workbookId": str,
        "tableId": str,
        "rowIds": NotRequired[Sequence[str]],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListTablesRequestRequestTypeDef = TypedDict(
    "ListTablesRequestRequestTypeDef",
    {
        "workbookId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
TableTypeDef = TypedDict(
    "TableTypeDef",
    {
        "tableId": NotRequired[str],
        "tableName": NotRequired[str],
    },
)
ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)
TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)
UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)
BatchCreateTableRowsResultTypeDef = TypedDict(
    "BatchCreateTableRowsResultTypeDef",
    {
        "workbookCursor": int,
        "createdRows": Dict[str, str],
        "failedBatchItems": List[FailedBatchItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchDeleteTableRowsResultTypeDef = TypedDict(
    "BatchDeleteTableRowsResultTypeDef",
    {
        "workbookCursor": int,
        "failedBatchItems": List[FailedBatchItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchUpdateTableRowsResultTypeDef = TypedDict(
    "BatchUpdateTableRowsResultTypeDef",
    {
        "workbookCursor": int,
        "failedBatchItems": List[FailedBatchItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
InvokeScreenAutomationResultTypeDef = TypedDict(
    "InvokeScreenAutomationResultTypeDef",
    {
        "workbookCursor": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListTagsForResourceResultTypeDef = TypedDict(
    "ListTagsForResourceResultTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartTableDataImportJobResultTypeDef = TypedDict(
    "StartTableDataImportJobResultTypeDef",
    {
        "jobId": str,
        "jobStatus": TableDataImportJobStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchUpsertTableRowsResultTypeDef = TypedDict(
    "BatchUpsertTableRowsResultTypeDef",
    {
        "rows": Dict[str, UpsertRowsResultTypeDef],
        "workbookCursor": int,
        "failedBatchItems": List[FailedBatchItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateRowDataTypeDef = TypedDict(
    "CreateRowDataTypeDef",
    {
        "batchItemId": str,
        "cellsToCreate": Mapping[str, CellInputTypeDef],
    },
)
UpdateRowDataTypeDef = TypedDict(
    "UpdateRowDataTypeDef",
    {
        "rowId": str,
        "cellsToUpdate": Mapping[str, CellInputTypeDef],
    },
)
TableRowTypeDef = TypedDict(
    "TableRowTypeDef",
    {
        "rowId": str,
        "cells": List[CellTypeDef],
    },
)
ResultRowTypeDef = TypedDict(
    "ResultRowTypeDef",
    {
        "dataItems": List[DataItemTypeDef],
        "rowId": NotRequired[str],
    },
)
DestinationOptionsOutputTypeDef = TypedDict(
    "DestinationOptionsOutputTypeDef",
    {
        "columnMap": NotRequired[Dict[str, SourceDataColumnPropertiesTypeDef]],
    },
)
DestinationOptionsTypeDef = TypedDict(
    "DestinationOptionsTypeDef",
    {
        "columnMap": NotRequired[Mapping[str, SourceDataColumnPropertiesTypeDef]],
    },
)
QueryTableRowsRequestRequestTypeDef = TypedDict(
    "QueryTableRowsRequestRequestTypeDef",
    {
        "workbookId": str,
        "tableId": str,
        "filterFormula": FilterTypeDef,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
UpsertRowDataTypeDef = TypedDict(
    "UpsertRowDataTypeDef",
    {
        "batchItemId": str,
        "filter": FilterTypeDef,
        "cellsToUpdate": Mapping[str, CellInputTypeDef],
    },
)
GetScreenDataRequestRequestTypeDef = TypedDict(
    "GetScreenDataRequestRequestTypeDef",
    {
        "workbookId": str,
        "appId": str,
        "screenId": str,
        "variables": NotRequired[Mapping[str, VariableValueTypeDef]],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
InvokeScreenAutomationRequestRequestTypeDef = TypedDict(
    "InvokeScreenAutomationRequestRequestTypeDef",
    {
        "workbookId": str,
        "appId": str,
        "screenId": str,
        "screenAutomationId": str,
        "variables": NotRequired[Mapping[str, VariableValueTypeDef]],
        "rowId": NotRequired[str],
        "clientRequestToken": NotRequired[str],
    },
)
ImportDataSourceTypeDef = TypedDict(
    "ImportDataSourceTypeDef",
    {
        "dataSourceConfig": ImportDataSourceConfigTypeDef,
    },
)
ListTableColumnsRequestListTableColumnsPaginateTypeDef = TypedDict(
    "ListTableColumnsRequestListTableColumnsPaginateTypeDef",
    {
        "workbookId": str,
        "tableId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListTableRowsRequestListTableRowsPaginateTypeDef = TypedDict(
    "ListTableRowsRequestListTableRowsPaginateTypeDef",
    {
        "workbookId": str,
        "tableId": str,
        "rowIds": NotRequired[Sequence[str]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListTablesRequestListTablesPaginateTypeDef = TypedDict(
    "ListTablesRequestListTablesPaginateTypeDef",
    {
        "workbookId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
QueryTableRowsRequestQueryTableRowsPaginateTypeDef = TypedDict(
    "QueryTableRowsRequestQueryTableRowsPaginateTypeDef",
    {
        "workbookId": str,
        "tableId": str,
        "filterFormula": FilterTypeDef,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListTableColumnsResultTypeDef = TypedDict(
    "ListTableColumnsResultTypeDef",
    {
        "tableColumns": List[TableColumnTypeDef],
        "nextToken": str,
        "workbookCursor": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListTablesResultTypeDef = TypedDict(
    "ListTablesResultTypeDef",
    {
        "tables": List[TableTypeDef],
        "nextToken": str,
        "workbookCursor": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchCreateTableRowsRequestRequestTypeDef = TypedDict(
    "BatchCreateTableRowsRequestRequestTypeDef",
    {
        "workbookId": str,
        "tableId": str,
        "rowsToCreate": Sequence[CreateRowDataTypeDef],
        "clientRequestToken": NotRequired[str],
    },
)
BatchUpdateTableRowsRequestRequestTypeDef = TypedDict(
    "BatchUpdateTableRowsRequestRequestTypeDef",
    {
        "workbookId": str,
        "tableId": str,
        "rowsToUpdate": Sequence[UpdateRowDataTypeDef],
        "clientRequestToken": NotRequired[str],
    },
)
ListTableRowsResultTypeDef = TypedDict(
    "ListTableRowsResultTypeDef",
    {
        "columnIds": List[str],
        "rows": List[TableRowTypeDef],
        "rowIdsNotFound": List[str],
        "nextToken": str,
        "workbookCursor": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
QueryTableRowsResultTypeDef = TypedDict(
    "QueryTableRowsResultTypeDef",
    {
        "columnIds": List[str],
        "rows": List[TableRowTypeDef],
        "nextToken": str,
        "workbookCursor": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ResultSetTypeDef = TypedDict(
    "ResultSetTypeDef",
    {
        "headers": List[ColumnMetadataTypeDef],
        "rows": List[ResultRowTypeDef],
    },
)
ImportOptionsOutputTypeDef = TypedDict(
    "ImportOptionsOutputTypeDef",
    {
        "destinationOptions": NotRequired[DestinationOptionsOutputTypeDef],
        "delimitedTextOptions": NotRequired[DelimitedTextImportOptionsTypeDef],
    },
)
ImportOptionsTypeDef = TypedDict(
    "ImportOptionsTypeDef",
    {
        "destinationOptions": NotRequired[DestinationOptionsTypeDef],
        "delimitedTextOptions": NotRequired[DelimitedTextImportOptionsTypeDef],
    },
)
BatchUpsertTableRowsRequestRequestTypeDef = TypedDict(
    "BatchUpsertTableRowsRequestRequestTypeDef",
    {
        "workbookId": str,
        "tableId": str,
        "rowsToUpsert": Sequence[UpsertRowDataTypeDef],
        "clientRequestToken": NotRequired[str],
    },
)
GetScreenDataResultTypeDef = TypedDict(
    "GetScreenDataResultTypeDef",
    {
        "results": Dict[str, ResultSetTypeDef],
        "workbookCursor": int,
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
TableDataImportJobMetadataTypeDef = TypedDict(
    "TableDataImportJobMetadataTypeDef",
    {
        "submitter": ImportJobSubmitterTypeDef,
        "submitTime": datetime,
        "importOptions": ImportOptionsOutputTypeDef,
        "dataSource": ImportDataSourceTypeDef,
    },
)
ImportOptionsUnionTypeDef = Union[ImportOptionsTypeDef, ImportOptionsOutputTypeDef]
StartTableDataImportJobRequestRequestTypeDef = TypedDict(
    "StartTableDataImportJobRequestRequestTypeDef",
    {
        "workbookId": str,
        "dataSource": ImportDataSourceTypeDef,
        "dataFormat": Literal["DELIMITED_TEXT"],
        "destinationTableId": str,
        "importOptions": ImportOptionsTypeDef,
        "clientRequestToken": str,
    },
)
DescribeTableDataImportJobResultTypeDef = TypedDict(
    "DescribeTableDataImportJobResultTypeDef",
    {
        "jobStatus": TableDataImportJobStatusType,
        "message": str,
        "jobMetadata": TableDataImportJobMetadataTypeDef,
        "errorCode": ErrorCodeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
