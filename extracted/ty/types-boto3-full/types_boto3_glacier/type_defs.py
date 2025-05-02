"""
Type annotations for glacier service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from types_boto3_glacier.type_defs import AbortMultipartUploadInputTypeDef

    data: AbortMultipartUploadInputTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from typing import IO, Any, Union

from botocore.response import StreamingBody

from .literals import (
    ActionCodeType,
    CannedACLType,
    EncryptionTypeType,
    FileHeaderInfoType,
    PermissionType,
    QuoteFieldsType,
    StatusCodeType,
    StorageClassType,
    TypeType,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import list as List
    from collections.abc import Mapping, Sequence
else:
    from typing import Dict, List, Mapping, Sequence
if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AbortMultipartUploadInputTypeDef",
    "AbortVaultLockInputTypeDef",
    "AddTagsToVaultInputTypeDef",
    "ArchiveCreationOutputTypeDef",
    "BlobTypeDef",
    "CSVInputTypeDef",
    "CSVOutputTypeDef",
    "CompleteMultipartUploadInputMultipartUploadCompleteTypeDef",
    "CompleteMultipartUploadInputTypeDef",
    "CompleteVaultLockInputTypeDef",
    "CreateVaultInputAccountCreateVaultTypeDef",
    "CreateVaultInputServiceResourceCreateVaultTypeDef",
    "CreateVaultInputTypeDef",
    "CreateVaultOutputTypeDef",
    "DataRetrievalPolicyOutputTypeDef",
    "DataRetrievalPolicyTypeDef",
    "DataRetrievalPolicyUnionTypeDef",
    "DataRetrievalRuleTypeDef",
    "DeleteArchiveInputTypeDef",
    "DeleteVaultAccessPolicyInputTypeDef",
    "DeleteVaultInputTypeDef",
    "DeleteVaultNotificationsInputTypeDef",
    "DescribeJobInputTypeDef",
    "DescribeVaultInputTypeDef",
    "DescribeVaultInputWaitExtraTypeDef",
    "DescribeVaultInputWaitTypeDef",
    "DescribeVaultOutputTypeDef",
    "DescribeVaultResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncryptionTypeDef",
    "GetDataRetrievalPolicyInputTypeDef",
    "GetDataRetrievalPolicyOutputTypeDef",
    "GetJobOutputInputJobGetOutputTypeDef",
    "GetJobOutputInputTypeDef",
    "GetJobOutputOutputTypeDef",
    "GetVaultAccessPolicyInputTypeDef",
    "GetVaultAccessPolicyOutputTypeDef",
    "GetVaultLockInputTypeDef",
    "GetVaultLockOutputTypeDef",
    "GetVaultNotificationsInputTypeDef",
    "GetVaultNotificationsOutputTypeDef",
    "GlacierJobDescriptionResponseTypeDef",
    "GlacierJobDescriptionTypeDef",
    "GrantTypeDef",
    "GranteeTypeDef",
    "InitiateJobInputTypeDef",
    "InitiateJobOutputTypeDef",
    "InitiateMultipartUploadInputTypeDef",
    "InitiateMultipartUploadInputVaultInitiateMultipartUploadTypeDef",
    "InitiateMultipartUploadOutputTypeDef",
    "InitiateVaultLockInputTypeDef",
    "InitiateVaultLockOutputTypeDef",
    "InputSerializationTypeDef",
    "InventoryRetrievalJobDescriptionTypeDef",
    "InventoryRetrievalJobInputTypeDef",
    "JobParametersTypeDef",
    "ListJobsInputPaginateTypeDef",
    "ListJobsInputTypeDef",
    "ListJobsOutputTypeDef",
    "ListMultipartUploadsInputPaginateTypeDef",
    "ListMultipartUploadsInputTypeDef",
    "ListMultipartUploadsOutputTypeDef",
    "ListPartsInputMultipartUploadPartsTypeDef",
    "ListPartsInputPaginateTypeDef",
    "ListPartsInputTypeDef",
    "ListPartsOutputTypeDef",
    "ListProvisionedCapacityInputTypeDef",
    "ListProvisionedCapacityOutputTypeDef",
    "ListTagsForVaultInputTypeDef",
    "ListTagsForVaultOutputTypeDef",
    "ListVaultsInputPaginateTypeDef",
    "ListVaultsInputTypeDef",
    "ListVaultsOutputTypeDef",
    "OutputLocationOutputTypeDef",
    "OutputLocationTypeDef",
    "OutputLocationUnionTypeDef",
    "OutputSerializationTypeDef",
    "PaginatorConfigTypeDef",
    "PartListElementTypeDef",
    "ProvisionedCapacityDescriptionTypeDef",
    "PurchaseProvisionedCapacityInputTypeDef",
    "PurchaseProvisionedCapacityOutputTypeDef",
    "RemoveTagsFromVaultInputTypeDef",
    "ResponseMetadataTypeDef",
    "S3LocationOutputTypeDef",
    "S3LocationTypeDef",
    "S3LocationUnionTypeDef",
    "SelectParametersTypeDef",
    "SetDataRetrievalPolicyInputTypeDef",
    "SetVaultAccessPolicyInputTypeDef",
    "SetVaultNotificationsInputNotificationSetTypeDef",
    "SetVaultNotificationsInputTypeDef",
    "UploadArchiveInputTypeDef",
    "UploadArchiveInputVaultUploadArchiveTypeDef",
    "UploadListElementTypeDef",
    "UploadMultipartPartInputMultipartUploadUploadPartTypeDef",
    "UploadMultipartPartInputTypeDef",
    "UploadMultipartPartOutputTypeDef",
    "VaultAccessPolicyTypeDef",
    "VaultLockPolicyTypeDef",
    "VaultNotificationConfigOutputTypeDef",
    "VaultNotificationConfigTypeDef",
    "VaultNotificationConfigUnionTypeDef",
    "WaiterConfigTypeDef",
)


class AbortMultipartUploadInputTypeDef(TypedDict):
    vaultName: str
    uploadId: str
    accountId: NotRequired[str]


class AbortVaultLockInputTypeDef(TypedDict):
    vaultName: str
    accountId: NotRequired[str]


class AddTagsToVaultInputTypeDef(TypedDict):
    vaultName: str
    accountId: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class CSVInputTypeDef(TypedDict):
    FileHeaderInfo: NotRequired[FileHeaderInfoType]
    Comments: NotRequired[str]
    QuoteEscapeCharacter: NotRequired[str]
    RecordDelimiter: NotRequired[str]
    FieldDelimiter: NotRequired[str]
    QuoteCharacter: NotRequired[str]


class CSVOutputTypeDef(TypedDict):
    QuoteFields: NotRequired[QuoteFieldsType]
    QuoteEscapeCharacter: NotRequired[str]
    RecordDelimiter: NotRequired[str]
    FieldDelimiter: NotRequired[str]
    QuoteCharacter: NotRequired[str]


class CompleteMultipartUploadInputMultipartUploadCompleteTypeDef(TypedDict):
    archiveSize: NotRequired[str]
    checksum: NotRequired[str]


class CompleteMultipartUploadInputTypeDef(TypedDict):
    vaultName: str
    uploadId: str
    accountId: NotRequired[str]
    archiveSize: NotRequired[str]
    checksum: NotRequired[str]


class CompleteVaultLockInputTypeDef(TypedDict):
    vaultName: str
    lockId: str
    accountId: NotRequired[str]


class CreateVaultInputAccountCreateVaultTypeDef(TypedDict):
    vaultName: str


class CreateVaultInputServiceResourceCreateVaultTypeDef(TypedDict):
    vaultName: str
    accountId: NotRequired[str]


class CreateVaultInputTypeDef(TypedDict):
    vaultName: str
    accountId: NotRequired[str]


class DataRetrievalRuleTypeDef(TypedDict):
    Strategy: NotRequired[str]
    BytesPerHour: NotRequired[int]


class DeleteArchiveInputTypeDef(TypedDict):
    vaultName: str
    archiveId: str
    accountId: NotRequired[str]


class DeleteVaultAccessPolicyInputTypeDef(TypedDict):
    vaultName: str
    accountId: NotRequired[str]


class DeleteVaultInputTypeDef(TypedDict):
    vaultName: str
    accountId: NotRequired[str]


class DeleteVaultNotificationsInputTypeDef(TypedDict):
    vaultName: str
    accountId: NotRequired[str]


class DescribeJobInputTypeDef(TypedDict):
    vaultName: str
    jobId: str
    accountId: NotRequired[str]


class DescribeVaultInputTypeDef(TypedDict):
    vaultName: str
    accountId: NotRequired[str]


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class DescribeVaultOutputTypeDef(TypedDict):
    VaultARN: NotRequired[str]
    VaultName: NotRequired[str]
    CreationDate: NotRequired[str]
    LastInventoryDate: NotRequired[str]
    NumberOfArchives: NotRequired[int]
    SizeInBytes: NotRequired[int]


class EncryptionTypeDef(TypedDict):
    EncryptionType: NotRequired[EncryptionTypeType]
    KMSKeyId: NotRequired[str]
    KMSContext: NotRequired[str]


class GetDataRetrievalPolicyInputTypeDef(TypedDict):
    accountId: NotRequired[str]


GetJobOutputInputJobGetOutputTypeDef = TypedDict(
    "GetJobOutputInputJobGetOutputTypeDef",
    {
        "range": NotRequired[str],
    },
)
GetJobOutputInputTypeDef = TypedDict(
    "GetJobOutputInputTypeDef",
    {
        "vaultName": str,
        "jobId": str,
        "accountId": NotRequired[str],
        "range": NotRequired[str],
    },
)


class GetVaultAccessPolicyInputTypeDef(TypedDict):
    vaultName: str
    accountId: NotRequired[str]


class VaultAccessPolicyTypeDef(TypedDict):
    Policy: NotRequired[str]


class GetVaultLockInputTypeDef(TypedDict):
    vaultName: str
    accountId: NotRequired[str]


class GetVaultNotificationsInputTypeDef(TypedDict):
    vaultName: str
    accountId: NotRequired[str]


class VaultNotificationConfigOutputTypeDef(TypedDict):
    SNSTopic: NotRequired[str]
    Events: NotRequired[List[str]]


class InventoryRetrievalJobDescriptionTypeDef(TypedDict):
    Format: NotRequired[str]
    StartDate: NotRequired[str]
    EndDate: NotRequired[str]
    Limit: NotRequired[str]
    Marker: NotRequired[str]


GranteeTypeDef = TypedDict(
    "GranteeTypeDef",
    {
        "Type": TypeType,
        "DisplayName": NotRequired[str],
        "URI": NotRequired[str],
        "ID": NotRequired[str],
        "EmailAddress": NotRequired[str],
    },
)


class InitiateMultipartUploadInputTypeDef(TypedDict):
    vaultName: str
    accountId: NotRequired[str]
    archiveDescription: NotRequired[str]
    partSize: NotRequired[str]


class InitiateMultipartUploadInputVaultInitiateMultipartUploadTypeDef(TypedDict):
    archiveDescription: NotRequired[str]
    partSize: NotRequired[str]


class VaultLockPolicyTypeDef(TypedDict):
    Policy: NotRequired[str]


class InventoryRetrievalJobInputTypeDef(TypedDict):
    StartDate: NotRequired[str]
    EndDate: NotRequired[str]
    Limit: NotRequired[str]
    Marker: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListJobsInputTypeDef(TypedDict):
    vaultName: str
    accountId: NotRequired[str]
    limit: NotRequired[str]
    marker: NotRequired[str]
    statuscode: NotRequired[str]
    completed: NotRequired[str]


class ListMultipartUploadsInputTypeDef(TypedDict):
    vaultName: str
    accountId: NotRequired[str]
    marker: NotRequired[str]
    limit: NotRequired[str]


class UploadListElementTypeDef(TypedDict):
    MultipartUploadId: NotRequired[str]
    VaultARN: NotRequired[str]
    ArchiveDescription: NotRequired[str]
    PartSizeInBytes: NotRequired[int]
    CreationDate: NotRequired[str]


class ListPartsInputMultipartUploadPartsTypeDef(TypedDict):
    marker: NotRequired[str]
    limit: NotRequired[str]


class ListPartsInputTypeDef(TypedDict):
    vaultName: str
    uploadId: str
    accountId: NotRequired[str]
    marker: NotRequired[str]
    limit: NotRequired[str]


class PartListElementTypeDef(TypedDict):
    RangeInBytes: NotRequired[str]
    SHA256TreeHash: NotRequired[str]


class ListProvisionedCapacityInputTypeDef(TypedDict):
    accountId: NotRequired[str]


class ProvisionedCapacityDescriptionTypeDef(TypedDict):
    CapacityId: NotRequired[str]
    StartDate: NotRequired[str]
    ExpirationDate: NotRequired[str]


class ListTagsForVaultInputTypeDef(TypedDict):
    vaultName: str
    accountId: NotRequired[str]


class ListVaultsInputTypeDef(TypedDict):
    accountId: NotRequired[str]
    marker: NotRequired[str]
    limit: NotRequired[str]


class PurchaseProvisionedCapacityInputTypeDef(TypedDict):
    accountId: NotRequired[str]


class RemoveTagsFromVaultInputTypeDef(TypedDict):
    vaultName: str
    accountId: NotRequired[str]
    TagKeys: NotRequired[Sequence[str]]


class VaultNotificationConfigTypeDef(TypedDict):
    SNSTopic: NotRequired[str]
    Events: NotRequired[Sequence[str]]


class ArchiveCreationOutputTypeDef(TypedDict):
    location: str
    checksum: str
    archiveId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateVaultOutputTypeDef(TypedDict):
    location: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVaultResponseTypeDef(TypedDict):
    VaultARN: str
    VaultName: str
    CreationDate: str
    LastInventoryDate: str
    NumberOfArchives: int
    SizeInBytes: int
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetJobOutputOutputTypeDef(TypedDict):
    body: StreamingBody
    checksum: str
    status: int
    contentRange: str
    acceptRanges: str
    contentType: str
    archiveDescription: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetVaultLockOutputTypeDef(TypedDict):
    Policy: str
    State: str
    ExpirationDate: str
    CreationDate: str
    ResponseMetadata: ResponseMetadataTypeDef


class InitiateJobOutputTypeDef(TypedDict):
    location: str
    jobId: str
    jobOutputPath: str
    ResponseMetadata: ResponseMetadataTypeDef


class InitiateMultipartUploadOutputTypeDef(TypedDict):
    location: str
    uploadId: str
    ResponseMetadata: ResponseMetadataTypeDef


class InitiateVaultLockOutputTypeDef(TypedDict):
    lockId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForVaultOutputTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class PurchaseProvisionedCapacityOutputTypeDef(TypedDict):
    capacityId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UploadMultipartPartOutputTypeDef(TypedDict):
    checksum: str
    ResponseMetadata: ResponseMetadataTypeDef


class UploadArchiveInputTypeDef(TypedDict):
    vaultName: str
    accountId: NotRequired[str]
    archiveDescription: NotRequired[str]
    checksum: NotRequired[str]
    body: NotRequired[BlobTypeDef]


class UploadArchiveInputVaultUploadArchiveTypeDef(TypedDict):
    archiveDescription: NotRequired[str]
    checksum: NotRequired[str]
    body: NotRequired[BlobTypeDef]


UploadMultipartPartInputMultipartUploadUploadPartTypeDef = TypedDict(
    "UploadMultipartPartInputMultipartUploadUploadPartTypeDef",
    {
        "checksum": NotRequired[str],
        "range": NotRequired[str],
        "body": NotRequired[BlobTypeDef],
    },
)
UploadMultipartPartInputTypeDef = TypedDict(
    "UploadMultipartPartInputTypeDef",
    {
        "vaultName": str,
        "uploadId": str,
        "accountId": NotRequired[str],
        "checksum": NotRequired[str],
        "range": NotRequired[str],
        "body": NotRequired[BlobTypeDef],
    },
)


class InputSerializationTypeDef(TypedDict):
    csv: NotRequired[CSVInputTypeDef]


class OutputSerializationTypeDef(TypedDict):
    csv: NotRequired[CSVOutputTypeDef]


class DataRetrievalPolicyOutputTypeDef(TypedDict):
    Rules: NotRequired[List[DataRetrievalRuleTypeDef]]


class DataRetrievalPolicyTypeDef(TypedDict):
    Rules: NotRequired[Sequence[DataRetrievalRuleTypeDef]]


class DescribeVaultInputWaitExtraTypeDef(TypedDict):
    accountId: str
    vaultName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeVaultInputWaitTypeDef(TypedDict):
    accountId: str
    vaultName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class ListVaultsOutputTypeDef(TypedDict):
    VaultList: List[DescribeVaultOutputTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetVaultAccessPolicyOutputTypeDef(TypedDict):
    policy: VaultAccessPolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SetVaultAccessPolicyInputTypeDef(TypedDict):
    vaultName: str
    accountId: NotRequired[str]
    policy: NotRequired[VaultAccessPolicyTypeDef]


class GetVaultNotificationsOutputTypeDef(TypedDict):
    vaultNotificationConfig: VaultNotificationConfigOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GrantTypeDef(TypedDict):
    Grantee: NotRequired[GranteeTypeDef]
    Permission: NotRequired[PermissionType]


class InitiateVaultLockInputTypeDef(TypedDict):
    vaultName: str
    accountId: NotRequired[str]
    policy: NotRequired[VaultLockPolicyTypeDef]


class ListJobsInputPaginateTypeDef(TypedDict):
    accountId: str
    vaultName: str
    statuscode: NotRequired[str]
    completed: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMultipartUploadsInputPaginateTypeDef(TypedDict):
    accountId: str
    vaultName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPartsInputPaginateTypeDef(TypedDict):
    accountId: str
    vaultName: str
    uploadId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListVaultsInputPaginateTypeDef(TypedDict):
    accountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMultipartUploadsOutputTypeDef(TypedDict):
    UploadsList: List[UploadListElementTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListPartsOutputTypeDef(TypedDict):
    MultipartUploadId: str
    VaultARN: str
    ArchiveDescription: str
    PartSizeInBytes: int
    CreationDate: str
    Parts: List[PartListElementTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListProvisionedCapacityOutputTypeDef(TypedDict):
    ProvisionedCapacityList: List[ProvisionedCapacityDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


VaultNotificationConfigUnionTypeDef = Union[
    VaultNotificationConfigTypeDef, VaultNotificationConfigOutputTypeDef
]


class SelectParametersTypeDef(TypedDict):
    InputSerialization: NotRequired[InputSerializationTypeDef]
    ExpressionType: NotRequired[Literal["SQL"]]
    Expression: NotRequired[str]
    OutputSerialization: NotRequired[OutputSerializationTypeDef]


class GetDataRetrievalPolicyOutputTypeDef(TypedDict):
    Policy: DataRetrievalPolicyOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


DataRetrievalPolicyUnionTypeDef = Union[
    DataRetrievalPolicyTypeDef, DataRetrievalPolicyOutputTypeDef
]


class S3LocationOutputTypeDef(TypedDict):
    BucketName: NotRequired[str]
    Prefix: NotRequired[str]
    Encryption: NotRequired[EncryptionTypeDef]
    CannedACL: NotRequired[CannedACLType]
    AccessControlList: NotRequired[List[GrantTypeDef]]
    Tagging: NotRequired[Dict[str, str]]
    UserMetadata: NotRequired[Dict[str, str]]
    StorageClass: NotRequired[StorageClassType]


class S3LocationTypeDef(TypedDict):
    BucketName: NotRequired[str]
    Prefix: NotRequired[str]
    Encryption: NotRequired[EncryptionTypeDef]
    CannedACL: NotRequired[CannedACLType]
    AccessControlList: NotRequired[Sequence[GrantTypeDef]]
    Tagging: NotRequired[Mapping[str, str]]
    UserMetadata: NotRequired[Mapping[str, str]]
    StorageClass: NotRequired[StorageClassType]


class SetVaultNotificationsInputNotificationSetTypeDef(TypedDict):
    vaultNotificationConfig: NotRequired[VaultNotificationConfigUnionTypeDef]


class SetVaultNotificationsInputTypeDef(TypedDict):
    vaultName: str
    accountId: NotRequired[str]
    vaultNotificationConfig: NotRequired[VaultNotificationConfigUnionTypeDef]


class SetDataRetrievalPolicyInputTypeDef(TypedDict):
    accountId: NotRequired[str]
    Policy: NotRequired[DataRetrievalPolicyUnionTypeDef]


class OutputLocationOutputTypeDef(TypedDict):
    S3: NotRequired[S3LocationOutputTypeDef]


S3LocationUnionTypeDef = Union[S3LocationTypeDef, S3LocationOutputTypeDef]


class GlacierJobDescriptionResponseTypeDef(TypedDict):
    JobId: str
    JobDescription: str
    Action: ActionCodeType
    ArchiveId: str
    VaultARN: str
    CreationDate: str
    Completed: bool
    StatusCode: StatusCodeType
    StatusMessage: str
    ArchiveSizeInBytes: int
    InventorySizeInBytes: int
    SNSTopic: str
    CompletionDate: str
    SHA256TreeHash: str
    ArchiveSHA256TreeHash: str
    RetrievalByteRange: str
    Tier: str
    InventoryRetrievalParameters: InventoryRetrievalJobDescriptionTypeDef
    JobOutputPath: str
    SelectParameters: SelectParametersTypeDef
    OutputLocation: OutputLocationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GlacierJobDescriptionTypeDef(TypedDict):
    JobId: NotRequired[str]
    JobDescription: NotRequired[str]
    Action: NotRequired[ActionCodeType]
    ArchiveId: NotRequired[str]
    VaultARN: NotRequired[str]
    CreationDate: NotRequired[str]
    Completed: NotRequired[bool]
    StatusCode: NotRequired[StatusCodeType]
    StatusMessage: NotRequired[str]
    ArchiveSizeInBytes: NotRequired[int]
    InventorySizeInBytes: NotRequired[int]
    SNSTopic: NotRequired[str]
    CompletionDate: NotRequired[str]
    SHA256TreeHash: NotRequired[str]
    ArchiveSHA256TreeHash: NotRequired[str]
    RetrievalByteRange: NotRequired[str]
    Tier: NotRequired[str]
    InventoryRetrievalParameters: NotRequired[InventoryRetrievalJobDescriptionTypeDef]
    JobOutputPath: NotRequired[str]
    SelectParameters: NotRequired[SelectParametersTypeDef]
    OutputLocation: NotRequired[OutputLocationOutputTypeDef]


class OutputLocationTypeDef(TypedDict):
    S3: NotRequired[S3LocationUnionTypeDef]


class ListJobsOutputTypeDef(TypedDict):
    JobList: List[GlacierJobDescriptionTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


OutputLocationUnionTypeDef = Union[OutputLocationTypeDef, OutputLocationOutputTypeDef]
JobParametersTypeDef = TypedDict(
    "JobParametersTypeDef",
    {
        "Format": NotRequired[str],
        "Type": NotRequired[str],
        "ArchiveId": NotRequired[str],
        "Description": NotRequired[str],
        "SNSTopic": NotRequired[str],
        "RetrievalByteRange": NotRequired[str],
        "Tier": NotRequired[str],
        "InventoryRetrievalParameters": NotRequired[InventoryRetrievalJobInputTypeDef],
        "SelectParameters": NotRequired[SelectParametersTypeDef],
        "OutputLocation": NotRequired[OutputLocationUnionTypeDef],
    },
)


class InitiateJobInputTypeDef(TypedDict):
    vaultName: str
    accountId: NotRequired[str]
    jobParameters: NotRequired[JobParametersTypeDef]
