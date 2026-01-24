"""
Type annotations for codecommit service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_codecommit.type_defs import ApprovalRuleEventMetadataTypeDef

    data: ApprovalRuleEventMetadataTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import IO, Any, Union

from botocore.response import StreamingBody

from .literals import (
    ApprovalStateType,
    BatchGetRepositoriesErrorCodeEnumType,
    ChangeTypeEnumType,
    ConflictDetailLevelTypeEnumType,
    ConflictResolutionStrategyTypeEnumType,
    FileModeTypeEnumType,
    MergeOptionTypeEnumType,
    ObjectTypeEnumType,
    OrderEnumType,
    OverrideStatusType,
    PullRequestEventTypeType,
    PullRequestStatusEnumType,
    RelativeFileVersionEnumType,
    ReplacementTypeEnumType,
    RepositoryTriggerEventEnumType,
    SortByEnumType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ApprovalRuleEventMetadataTypeDef",
    "ApprovalRuleOverriddenEventMetadataTypeDef",
    "ApprovalRuleTemplateTypeDef",
    "ApprovalRuleTypeDef",
    "ApprovalStateChangedEventMetadataTypeDef",
    "ApprovalTypeDef",
    "AssociateApprovalRuleTemplateWithRepositoryInputTypeDef",
    "BatchAssociateApprovalRuleTemplateWithRepositoriesErrorTypeDef",
    "BatchAssociateApprovalRuleTemplateWithRepositoriesInputTypeDef",
    "BatchAssociateApprovalRuleTemplateWithRepositoriesOutputTypeDef",
    "BatchDescribeMergeConflictsErrorTypeDef",
    "BatchDescribeMergeConflictsInputTypeDef",
    "BatchDescribeMergeConflictsOutputTypeDef",
    "BatchDisassociateApprovalRuleTemplateFromRepositoriesErrorTypeDef",
    "BatchDisassociateApprovalRuleTemplateFromRepositoriesInputTypeDef",
    "BatchDisassociateApprovalRuleTemplateFromRepositoriesOutputTypeDef",
    "BatchGetCommitsErrorTypeDef",
    "BatchGetCommitsInputTypeDef",
    "BatchGetCommitsOutputTypeDef",
    "BatchGetRepositoriesErrorTypeDef",
    "BatchGetRepositoriesInputTypeDef",
    "BatchGetRepositoriesOutputTypeDef",
    "BlobMetadataTypeDef",
    "BlobTypeDef",
    "BranchInfoTypeDef",
    "CommentTypeDef",
    "CommentsForComparedCommitTypeDef",
    "CommentsForPullRequestTypeDef",
    "CommitTypeDef",
    "ConflictMetadataTypeDef",
    "ConflictResolutionTypeDef",
    "ConflictTypeDef",
    "CreateApprovalRuleTemplateInputTypeDef",
    "CreateApprovalRuleTemplateOutputTypeDef",
    "CreateBranchInputTypeDef",
    "CreateCommitInputTypeDef",
    "CreateCommitOutputTypeDef",
    "CreatePullRequestApprovalRuleInputTypeDef",
    "CreatePullRequestApprovalRuleOutputTypeDef",
    "CreatePullRequestInputTypeDef",
    "CreatePullRequestOutputTypeDef",
    "CreateRepositoryInputTypeDef",
    "CreateRepositoryOutputTypeDef",
    "CreateUnreferencedMergeCommitInputTypeDef",
    "CreateUnreferencedMergeCommitOutputTypeDef",
    "DeleteApprovalRuleTemplateInputTypeDef",
    "DeleteApprovalRuleTemplateOutputTypeDef",
    "DeleteBranchInputTypeDef",
    "DeleteBranchOutputTypeDef",
    "DeleteCommentContentInputTypeDef",
    "DeleteCommentContentOutputTypeDef",
    "DeleteFileEntryTypeDef",
    "DeleteFileInputTypeDef",
    "DeleteFileOutputTypeDef",
    "DeletePullRequestApprovalRuleInputTypeDef",
    "DeletePullRequestApprovalRuleOutputTypeDef",
    "DeleteRepositoryInputTypeDef",
    "DeleteRepositoryOutputTypeDef",
    "DescribeMergeConflictsInputTypeDef",
    "DescribeMergeConflictsOutputTypeDef",
    "DescribePullRequestEventsInputPaginateTypeDef",
    "DescribePullRequestEventsInputTypeDef",
    "DescribePullRequestEventsOutputTypeDef",
    "DifferenceTypeDef",
    "DisassociateApprovalRuleTemplateFromRepositoryInputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EvaluatePullRequestApprovalRulesInputTypeDef",
    "EvaluatePullRequestApprovalRulesOutputTypeDef",
    "EvaluationTypeDef",
    "FileMetadataTypeDef",
    "FileModesTypeDef",
    "FileSizesTypeDef",
    "FileTypeDef",
    "FileVersionTypeDef",
    "FolderTypeDef",
    "GetApprovalRuleTemplateInputTypeDef",
    "GetApprovalRuleTemplateOutputTypeDef",
    "GetBlobInputTypeDef",
    "GetBlobOutputTypeDef",
    "GetBranchInputTypeDef",
    "GetBranchOutputTypeDef",
    "GetCommentInputTypeDef",
    "GetCommentOutputTypeDef",
    "GetCommentReactionsInputTypeDef",
    "GetCommentReactionsOutputTypeDef",
    "GetCommentsForComparedCommitInputPaginateTypeDef",
    "GetCommentsForComparedCommitInputTypeDef",
    "GetCommentsForComparedCommitOutputTypeDef",
    "GetCommentsForPullRequestInputPaginateTypeDef",
    "GetCommentsForPullRequestInputTypeDef",
    "GetCommentsForPullRequestOutputTypeDef",
    "GetCommitInputTypeDef",
    "GetCommitOutputTypeDef",
    "GetDifferencesInputPaginateTypeDef",
    "GetDifferencesInputTypeDef",
    "GetDifferencesOutputTypeDef",
    "GetFileInputTypeDef",
    "GetFileOutputTypeDef",
    "GetFolderInputTypeDef",
    "GetFolderOutputTypeDef",
    "GetMergeCommitInputTypeDef",
    "GetMergeCommitOutputTypeDef",
    "GetMergeConflictsInputTypeDef",
    "GetMergeConflictsOutputTypeDef",
    "GetMergeOptionsInputTypeDef",
    "GetMergeOptionsOutputTypeDef",
    "GetPullRequestApprovalStatesInputTypeDef",
    "GetPullRequestApprovalStatesOutputTypeDef",
    "GetPullRequestInputTypeDef",
    "GetPullRequestOutputTypeDef",
    "GetPullRequestOverrideStateInputTypeDef",
    "GetPullRequestOverrideStateOutputTypeDef",
    "GetRepositoryInputTypeDef",
    "GetRepositoryOutputTypeDef",
    "GetRepositoryTriggersInputTypeDef",
    "GetRepositoryTriggersOutputTypeDef",
    "IsBinaryFileTypeDef",
    "ListApprovalRuleTemplatesInputTypeDef",
    "ListApprovalRuleTemplatesOutputTypeDef",
    "ListAssociatedApprovalRuleTemplatesForRepositoryInputTypeDef",
    "ListAssociatedApprovalRuleTemplatesForRepositoryOutputTypeDef",
    "ListBranchesInputPaginateTypeDef",
    "ListBranchesInputTypeDef",
    "ListBranchesOutputTypeDef",
    "ListFileCommitHistoryRequestTypeDef",
    "ListFileCommitHistoryResponseTypeDef",
    "ListPullRequestsInputPaginateTypeDef",
    "ListPullRequestsInputTypeDef",
    "ListPullRequestsOutputTypeDef",
    "ListRepositoriesForApprovalRuleTemplateInputTypeDef",
    "ListRepositoriesForApprovalRuleTemplateOutputTypeDef",
    "ListRepositoriesInputPaginateTypeDef",
    "ListRepositoriesInputTypeDef",
    "ListRepositoriesOutputTypeDef",
    "ListTagsForResourceInputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "LocationTypeDef",
    "MergeBranchesByFastForwardInputTypeDef",
    "MergeBranchesByFastForwardOutputTypeDef",
    "MergeBranchesBySquashInputTypeDef",
    "MergeBranchesBySquashOutputTypeDef",
    "MergeBranchesByThreeWayInputTypeDef",
    "MergeBranchesByThreeWayOutputTypeDef",
    "MergeHunkDetailTypeDef",
    "MergeHunkTypeDef",
    "MergeMetadataTypeDef",
    "MergeOperationsTypeDef",
    "MergePullRequestByFastForwardInputTypeDef",
    "MergePullRequestByFastForwardOutputTypeDef",
    "MergePullRequestBySquashInputTypeDef",
    "MergePullRequestBySquashOutputTypeDef",
    "MergePullRequestByThreeWayInputTypeDef",
    "MergePullRequestByThreeWayOutputTypeDef",
    "ObjectTypesTypeDef",
    "OriginApprovalRuleTemplateTypeDef",
    "OverridePullRequestApprovalRulesInputTypeDef",
    "PaginatorConfigTypeDef",
    "PostCommentForComparedCommitInputTypeDef",
    "PostCommentForComparedCommitOutputTypeDef",
    "PostCommentForPullRequestInputTypeDef",
    "PostCommentForPullRequestOutputTypeDef",
    "PostCommentReplyInputTypeDef",
    "PostCommentReplyOutputTypeDef",
    "PullRequestCreatedEventMetadataTypeDef",
    "PullRequestEventTypeDef",
    "PullRequestMergedStateChangedEventMetadataTypeDef",
    "PullRequestSourceReferenceUpdatedEventMetadataTypeDef",
    "PullRequestStatusChangedEventMetadataTypeDef",
    "PullRequestTargetTypeDef",
    "PullRequestTypeDef",
    "PutCommentReactionInputTypeDef",
    "PutFileEntryTypeDef",
    "PutFileInputTypeDef",
    "PutFileOutputTypeDef",
    "PutRepositoryTriggersInputTypeDef",
    "PutRepositoryTriggersOutputTypeDef",
    "ReactionForCommentTypeDef",
    "ReactionValueFormatsTypeDef",
    "ReplaceContentEntryTypeDef",
    "RepositoryMetadataTypeDef",
    "RepositoryNameIdPairTypeDef",
    "RepositoryTriggerExecutionFailureTypeDef",
    "RepositoryTriggerOutputTypeDef",
    "RepositoryTriggerTypeDef",
    "RepositoryTriggerUnionTypeDef",
    "ResponseMetadataTypeDef",
    "SetFileModeEntryTypeDef",
    "SourceFileSpecifierTypeDef",
    "SubModuleTypeDef",
    "SymbolicLinkTypeDef",
    "TagResourceInputTypeDef",
    "TargetTypeDef",
    "TestRepositoryTriggersInputTypeDef",
    "TestRepositoryTriggersOutputTypeDef",
    "UntagResourceInputTypeDef",
    "UpdateApprovalRuleTemplateContentInputTypeDef",
    "UpdateApprovalRuleTemplateContentOutputTypeDef",
    "UpdateApprovalRuleTemplateDescriptionInputTypeDef",
    "UpdateApprovalRuleTemplateDescriptionOutputTypeDef",
    "UpdateApprovalRuleTemplateNameInputTypeDef",
    "UpdateApprovalRuleTemplateNameOutputTypeDef",
    "UpdateCommentInputTypeDef",
    "UpdateCommentOutputTypeDef",
    "UpdateDefaultBranchInputTypeDef",
    "UpdatePullRequestApprovalRuleContentInputTypeDef",
    "UpdatePullRequestApprovalRuleContentOutputTypeDef",
    "UpdatePullRequestApprovalStateInputTypeDef",
    "UpdatePullRequestDescriptionInputTypeDef",
    "UpdatePullRequestDescriptionOutputTypeDef",
    "UpdatePullRequestStatusInputTypeDef",
    "UpdatePullRequestStatusOutputTypeDef",
    "UpdatePullRequestTitleInputTypeDef",
    "UpdatePullRequestTitleOutputTypeDef",
    "UpdateRepositoryDescriptionInputTypeDef",
    "UpdateRepositoryEncryptionKeyInputTypeDef",
    "UpdateRepositoryEncryptionKeyOutputTypeDef",
    "UpdateRepositoryNameInputTypeDef",
    "UserInfoTypeDef",
)

class ApprovalRuleEventMetadataTypeDef(TypedDict):
    approvalRuleName: NotRequired[str]
    approvalRuleId: NotRequired[str]
    approvalRuleContent: NotRequired[str]

class ApprovalRuleOverriddenEventMetadataTypeDef(TypedDict):
    revisionId: NotRequired[str]
    overrideStatus: NotRequired[OverrideStatusType]

class ApprovalRuleTemplateTypeDef(TypedDict):
    approvalRuleTemplateId: NotRequired[str]
    approvalRuleTemplateName: NotRequired[str]
    approvalRuleTemplateDescription: NotRequired[str]
    approvalRuleTemplateContent: NotRequired[str]
    ruleContentSha256: NotRequired[str]
    lastModifiedDate: NotRequired[datetime]
    creationDate: NotRequired[datetime]
    lastModifiedUser: NotRequired[str]

class OriginApprovalRuleTemplateTypeDef(TypedDict):
    approvalRuleTemplateId: NotRequired[str]
    approvalRuleTemplateName: NotRequired[str]

class ApprovalStateChangedEventMetadataTypeDef(TypedDict):
    revisionId: NotRequired[str]
    approvalStatus: NotRequired[ApprovalStateType]

class ApprovalTypeDef(TypedDict):
    userArn: NotRequired[str]
    approvalState: NotRequired[ApprovalStateType]

class AssociateApprovalRuleTemplateWithRepositoryInputTypeDef(TypedDict):
    approvalRuleTemplateName: str
    repositoryName: str

class BatchAssociateApprovalRuleTemplateWithRepositoriesErrorTypeDef(TypedDict):
    repositoryName: NotRequired[str]
    errorCode: NotRequired[str]
    errorMessage: NotRequired[str]

class BatchAssociateApprovalRuleTemplateWithRepositoriesInputTypeDef(TypedDict):
    approvalRuleTemplateName: str
    repositoryNames: Sequence[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BatchDescribeMergeConflictsErrorTypeDef(TypedDict):
    filePath: str
    exceptionName: str
    message: str

class BatchDescribeMergeConflictsInputTypeDef(TypedDict):
    repositoryName: str
    destinationCommitSpecifier: str
    sourceCommitSpecifier: str
    mergeOption: MergeOptionTypeEnumType
    maxMergeHunks: NotRequired[int]
    maxConflictFiles: NotRequired[int]
    filePaths: NotRequired[Sequence[str]]
    conflictDetailLevel: NotRequired[ConflictDetailLevelTypeEnumType]
    conflictResolutionStrategy: NotRequired[ConflictResolutionStrategyTypeEnumType]
    nextToken: NotRequired[str]

class BatchDisassociateApprovalRuleTemplateFromRepositoriesErrorTypeDef(TypedDict):
    repositoryName: NotRequired[str]
    errorCode: NotRequired[str]
    errorMessage: NotRequired[str]

class BatchDisassociateApprovalRuleTemplateFromRepositoriesInputTypeDef(TypedDict):
    approvalRuleTemplateName: str
    repositoryNames: Sequence[str]

class BatchGetCommitsErrorTypeDef(TypedDict):
    commitId: NotRequired[str]
    errorCode: NotRequired[str]
    errorMessage: NotRequired[str]

class BatchGetCommitsInputTypeDef(TypedDict):
    commitIds: Sequence[str]
    repositoryName: str

class BatchGetRepositoriesErrorTypeDef(TypedDict):
    repositoryId: NotRequired[str]
    repositoryName: NotRequired[str]
    errorCode: NotRequired[BatchGetRepositoriesErrorCodeEnumType]
    errorMessage: NotRequired[str]

class BatchGetRepositoriesInputTypeDef(TypedDict):
    repositoryNames: Sequence[str]

class RepositoryMetadataTypeDef(TypedDict):
    accountId: NotRequired[str]
    repositoryId: NotRequired[str]
    repositoryName: NotRequired[str]
    repositoryDescription: NotRequired[str]
    defaultBranch: NotRequired[str]
    lastModifiedDate: NotRequired[datetime]
    creationDate: NotRequired[datetime]
    cloneUrlHttp: NotRequired[str]
    cloneUrlSsh: NotRequired[str]
    Arn: NotRequired[str]
    kmsKeyId: NotRequired[str]

class BlobMetadataTypeDef(TypedDict):
    blobId: NotRequired[str]
    path: NotRequired[str]
    mode: NotRequired[str]

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class BranchInfoTypeDef(TypedDict):
    branchName: NotRequired[str]
    commitId: NotRequired[str]

class CommentTypeDef(TypedDict):
    commentId: NotRequired[str]
    content: NotRequired[str]
    inReplyTo: NotRequired[str]
    creationDate: NotRequired[datetime]
    lastModifiedDate: NotRequired[datetime]
    authorArn: NotRequired[str]
    deleted: NotRequired[bool]
    clientRequestToken: NotRequired[str]
    callerReactions: NotRequired[list[str]]
    reactionCounts: NotRequired[dict[str, int]]

class LocationTypeDef(TypedDict):
    filePath: NotRequired[str]
    filePosition: NotRequired[int]
    relativeFileVersion: NotRequired[RelativeFileVersionEnumType]

class UserInfoTypeDef(TypedDict):
    name: NotRequired[str]
    email: NotRequired[str]
    date: NotRequired[str]

class FileModesTypeDef(TypedDict):
    source: NotRequired[FileModeTypeEnumType]
    destination: NotRequired[FileModeTypeEnumType]
    base: NotRequired[FileModeTypeEnumType]

class FileSizesTypeDef(TypedDict):
    source: NotRequired[int]
    destination: NotRequired[int]
    base: NotRequired[int]

class IsBinaryFileTypeDef(TypedDict):
    source: NotRequired[bool]
    destination: NotRequired[bool]
    base: NotRequired[bool]

class MergeOperationsTypeDef(TypedDict):
    source: NotRequired[ChangeTypeEnumType]
    destination: NotRequired[ChangeTypeEnumType]

class ObjectTypesTypeDef(TypedDict):
    source: NotRequired[ObjectTypeEnumType]
    destination: NotRequired[ObjectTypeEnumType]
    base: NotRequired[ObjectTypeEnumType]

class DeleteFileEntryTypeDef(TypedDict):
    filePath: str

class SetFileModeEntryTypeDef(TypedDict):
    filePath: str
    fileMode: FileModeTypeEnumType

class CreateApprovalRuleTemplateInputTypeDef(TypedDict):
    approvalRuleTemplateName: str
    approvalRuleTemplateContent: str
    approvalRuleTemplateDescription: NotRequired[str]

class CreateBranchInputTypeDef(TypedDict):
    repositoryName: str
    branchName: str
    commitId: str

class FileMetadataTypeDef(TypedDict):
    absolutePath: NotRequired[str]
    blobId: NotRequired[str]
    fileMode: NotRequired[FileModeTypeEnumType]

class CreatePullRequestApprovalRuleInputTypeDef(TypedDict):
    pullRequestId: str
    approvalRuleName: str
    approvalRuleContent: str

class TargetTypeDef(TypedDict):
    repositoryName: str
    sourceReference: str
    destinationReference: NotRequired[str]

class CreateRepositoryInputTypeDef(TypedDict):
    repositoryName: str
    repositoryDescription: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    kmsKeyId: NotRequired[str]

class DeleteApprovalRuleTemplateInputTypeDef(TypedDict):
    approvalRuleTemplateName: str

class DeleteBranchInputTypeDef(TypedDict):
    repositoryName: str
    branchName: str

class DeleteCommentContentInputTypeDef(TypedDict):
    commentId: str

class DeleteFileInputTypeDef(TypedDict):
    repositoryName: str
    branchName: str
    filePath: str
    parentCommitId: str
    keepEmptyFolders: NotRequired[bool]
    commitMessage: NotRequired[str]
    name: NotRequired[str]
    email: NotRequired[str]

class DeletePullRequestApprovalRuleInputTypeDef(TypedDict):
    pullRequestId: str
    approvalRuleName: str

class DeleteRepositoryInputTypeDef(TypedDict):
    repositoryName: str

class DescribeMergeConflictsInputTypeDef(TypedDict):
    repositoryName: str
    destinationCommitSpecifier: str
    sourceCommitSpecifier: str
    mergeOption: MergeOptionTypeEnumType
    filePath: str
    maxMergeHunks: NotRequired[int]
    conflictDetailLevel: NotRequired[ConflictDetailLevelTypeEnumType]
    conflictResolutionStrategy: NotRequired[ConflictResolutionStrategyTypeEnumType]
    nextToken: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class DescribePullRequestEventsInputTypeDef(TypedDict):
    pullRequestId: str
    pullRequestEventType: NotRequired[PullRequestEventTypeType]
    actorArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class DisassociateApprovalRuleTemplateFromRepositoryInputTypeDef(TypedDict):
    approvalRuleTemplateName: str
    repositoryName: str

class EvaluatePullRequestApprovalRulesInputTypeDef(TypedDict):
    pullRequestId: str
    revisionId: str

class EvaluationTypeDef(TypedDict):
    approved: NotRequired[bool]
    overridden: NotRequired[bool]
    approvalRulesSatisfied: NotRequired[list[str]]
    approvalRulesNotSatisfied: NotRequired[list[str]]

class FileTypeDef(TypedDict):
    blobId: NotRequired[str]
    absolutePath: NotRequired[str]
    relativePath: NotRequired[str]
    fileMode: NotRequired[FileModeTypeEnumType]

class FolderTypeDef(TypedDict):
    treeId: NotRequired[str]
    absolutePath: NotRequired[str]
    relativePath: NotRequired[str]

class GetApprovalRuleTemplateInputTypeDef(TypedDict):
    approvalRuleTemplateName: str

class GetBlobInputTypeDef(TypedDict):
    repositoryName: str
    blobId: str

class GetBranchInputTypeDef(TypedDict):
    repositoryName: NotRequired[str]
    branchName: NotRequired[str]

class GetCommentInputTypeDef(TypedDict):
    commentId: str

class GetCommentReactionsInputTypeDef(TypedDict):
    commentId: str
    reactionUserArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class GetCommentsForComparedCommitInputTypeDef(TypedDict):
    repositoryName: str
    afterCommitId: str
    beforeCommitId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class GetCommentsForPullRequestInputTypeDef(TypedDict):
    pullRequestId: str
    repositoryName: NotRequired[str]
    beforeCommitId: NotRequired[str]
    afterCommitId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class GetCommitInputTypeDef(TypedDict):
    repositoryName: str
    commitId: str

class GetDifferencesInputTypeDef(TypedDict):
    repositoryName: str
    afterCommitSpecifier: str
    beforeCommitSpecifier: NotRequired[str]
    beforePath: NotRequired[str]
    afterPath: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class GetFileInputTypeDef(TypedDict):
    repositoryName: str
    filePath: str
    commitSpecifier: NotRequired[str]

class GetFolderInputTypeDef(TypedDict):
    repositoryName: str
    folderPath: str
    commitSpecifier: NotRequired[str]

class SubModuleTypeDef(TypedDict):
    commitId: NotRequired[str]
    absolutePath: NotRequired[str]
    relativePath: NotRequired[str]

class SymbolicLinkTypeDef(TypedDict):
    blobId: NotRequired[str]
    absolutePath: NotRequired[str]
    relativePath: NotRequired[str]
    fileMode: NotRequired[FileModeTypeEnumType]

class GetMergeCommitInputTypeDef(TypedDict):
    repositoryName: str
    sourceCommitSpecifier: str
    destinationCommitSpecifier: str
    conflictDetailLevel: NotRequired[ConflictDetailLevelTypeEnumType]
    conflictResolutionStrategy: NotRequired[ConflictResolutionStrategyTypeEnumType]

class GetMergeConflictsInputTypeDef(TypedDict):
    repositoryName: str
    destinationCommitSpecifier: str
    sourceCommitSpecifier: str
    mergeOption: MergeOptionTypeEnumType
    conflictDetailLevel: NotRequired[ConflictDetailLevelTypeEnumType]
    maxConflictFiles: NotRequired[int]
    conflictResolutionStrategy: NotRequired[ConflictResolutionStrategyTypeEnumType]
    nextToken: NotRequired[str]

class GetMergeOptionsInputTypeDef(TypedDict):
    repositoryName: str
    sourceCommitSpecifier: str
    destinationCommitSpecifier: str
    conflictDetailLevel: NotRequired[ConflictDetailLevelTypeEnumType]
    conflictResolutionStrategy: NotRequired[ConflictResolutionStrategyTypeEnumType]

class GetPullRequestApprovalStatesInputTypeDef(TypedDict):
    pullRequestId: str
    revisionId: str

class GetPullRequestInputTypeDef(TypedDict):
    pullRequestId: str

class GetPullRequestOverrideStateInputTypeDef(TypedDict):
    pullRequestId: str
    revisionId: str

class GetRepositoryInputTypeDef(TypedDict):
    repositoryName: str

class GetRepositoryTriggersInputTypeDef(TypedDict):
    repositoryName: str

class RepositoryTriggerOutputTypeDef(TypedDict):
    name: str
    destinationArn: str
    events: list[RepositoryTriggerEventEnumType]
    customData: NotRequired[str]
    branches: NotRequired[list[str]]

class ListApprovalRuleTemplatesInputTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListAssociatedApprovalRuleTemplatesForRepositoryInputTypeDef(TypedDict):
    repositoryName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListBranchesInputTypeDef(TypedDict):
    repositoryName: str
    nextToken: NotRequired[str]

class ListFileCommitHistoryRequestTypeDef(TypedDict):
    repositoryName: str
    filePath: str
    commitSpecifier: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListPullRequestsInputTypeDef(TypedDict):
    repositoryName: str
    authorArn: NotRequired[str]
    pullRequestStatus: NotRequired[PullRequestStatusEnumType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListRepositoriesForApprovalRuleTemplateInputTypeDef(TypedDict):
    approvalRuleTemplateName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListRepositoriesInputTypeDef(TypedDict):
    nextToken: NotRequired[str]
    sortBy: NotRequired[SortByEnumType]
    order: NotRequired[OrderEnumType]

class RepositoryNameIdPairTypeDef(TypedDict):
    repositoryName: NotRequired[str]
    repositoryId: NotRequired[str]

class ListTagsForResourceInputTypeDef(TypedDict):
    resourceArn: str
    nextToken: NotRequired[str]

class MergeBranchesByFastForwardInputTypeDef(TypedDict):
    repositoryName: str
    sourceCommitSpecifier: str
    destinationCommitSpecifier: str
    targetBranch: NotRequired[str]

class MergeHunkDetailTypeDef(TypedDict):
    startLine: NotRequired[int]
    endLine: NotRequired[int]
    hunkContent: NotRequired[str]

class MergeMetadataTypeDef(TypedDict):
    isMerged: NotRequired[bool]
    mergedBy: NotRequired[str]
    mergeCommitId: NotRequired[str]
    mergeOption: NotRequired[MergeOptionTypeEnumType]

class MergePullRequestByFastForwardInputTypeDef(TypedDict):
    pullRequestId: str
    repositoryName: str
    sourceCommitId: NotRequired[str]

class OverridePullRequestApprovalRulesInputTypeDef(TypedDict):
    pullRequestId: str
    revisionId: str
    overrideStatus: OverrideStatusType

class PostCommentReplyInputTypeDef(TypedDict):
    inReplyTo: str
    content: str
    clientRequestToken: NotRequired[str]

class PullRequestCreatedEventMetadataTypeDef(TypedDict):
    repositoryName: NotRequired[str]
    sourceCommitId: NotRequired[str]
    destinationCommitId: NotRequired[str]
    mergeBase: NotRequired[str]

class PullRequestSourceReferenceUpdatedEventMetadataTypeDef(TypedDict):
    repositoryName: NotRequired[str]
    beforeCommitId: NotRequired[str]
    afterCommitId: NotRequired[str]
    mergeBase: NotRequired[str]

class PullRequestStatusChangedEventMetadataTypeDef(TypedDict):
    pullRequestStatus: NotRequired[PullRequestStatusEnumType]

class PutCommentReactionInputTypeDef(TypedDict):
    commentId: str
    reactionValue: str

class SourceFileSpecifierTypeDef(TypedDict):
    filePath: str
    isMove: NotRequired[bool]

class ReactionValueFormatsTypeDef(TypedDict):
    emoji: NotRequired[str]
    shortCode: NotRequired[str]
    unicode: NotRequired[str]

class RepositoryTriggerExecutionFailureTypeDef(TypedDict):
    trigger: NotRequired[str]
    failureMessage: NotRequired[str]

class RepositoryTriggerTypeDef(TypedDict):
    name: str
    destinationArn: str
    events: Sequence[RepositoryTriggerEventEnumType]
    customData: NotRequired[str]
    branches: NotRequired[Sequence[str]]

class TagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateApprovalRuleTemplateContentInputTypeDef(TypedDict):
    approvalRuleTemplateName: str
    newRuleContent: str
    existingRuleContentSha256: NotRequired[str]

class UpdateApprovalRuleTemplateDescriptionInputTypeDef(TypedDict):
    approvalRuleTemplateName: str
    approvalRuleTemplateDescription: str

class UpdateApprovalRuleTemplateNameInputTypeDef(TypedDict):
    oldApprovalRuleTemplateName: str
    newApprovalRuleTemplateName: str

class UpdateCommentInputTypeDef(TypedDict):
    commentId: str
    content: str

class UpdateDefaultBranchInputTypeDef(TypedDict):
    repositoryName: str
    defaultBranchName: str

class UpdatePullRequestApprovalRuleContentInputTypeDef(TypedDict):
    pullRequestId: str
    approvalRuleName: str
    newRuleContent: str
    existingRuleContentSha256: NotRequired[str]

class UpdatePullRequestApprovalStateInputTypeDef(TypedDict):
    pullRequestId: str
    revisionId: str
    approvalState: ApprovalStateType

class UpdatePullRequestDescriptionInputTypeDef(TypedDict):
    pullRequestId: str
    description: str

class UpdatePullRequestStatusInputTypeDef(TypedDict):
    pullRequestId: str
    pullRequestStatus: PullRequestStatusEnumType

class UpdatePullRequestTitleInputTypeDef(TypedDict):
    pullRequestId: str
    title: str

class UpdateRepositoryDescriptionInputTypeDef(TypedDict):
    repositoryName: str
    repositoryDescription: NotRequired[str]

class UpdateRepositoryEncryptionKeyInputTypeDef(TypedDict):
    repositoryName: str
    kmsKeyId: str

class UpdateRepositoryNameInputTypeDef(TypedDict):
    oldName: str
    newName: str

class ApprovalRuleTypeDef(TypedDict):
    approvalRuleId: NotRequired[str]
    approvalRuleName: NotRequired[str]
    approvalRuleContent: NotRequired[str]
    ruleContentSha256: NotRequired[str]
    lastModifiedDate: NotRequired[datetime]
    creationDate: NotRequired[datetime]
    lastModifiedUser: NotRequired[str]
    originApprovalRuleTemplate: NotRequired[OriginApprovalRuleTemplateTypeDef]

class BatchAssociateApprovalRuleTemplateWithRepositoriesOutputTypeDef(TypedDict):
    associatedRepositoryNames: list[str]
    errors: list[BatchAssociateApprovalRuleTemplateWithRepositoriesErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateApprovalRuleTemplateOutputTypeDef(TypedDict):
    approvalRuleTemplate: ApprovalRuleTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateUnreferencedMergeCommitOutputTypeDef(TypedDict):
    commitId: str
    treeId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteApprovalRuleTemplateOutputTypeDef(TypedDict):
    approvalRuleTemplateId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteFileOutputTypeDef(TypedDict):
    commitId: str
    blobId: str
    treeId: str
    filePath: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeletePullRequestApprovalRuleOutputTypeDef(TypedDict):
    approvalRuleId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteRepositoryOutputTypeDef(TypedDict):
    repositoryId: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetApprovalRuleTemplateOutputTypeDef(TypedDict):
    approvalRuleTemplate: ApprovalRuleTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetBlobOutputTypeDef(TypedDict):
    content: bytes
    ResponseMetadata: ResponseMetadataTypeDef

class GetFileOutputTypeDef(TypedDict):
    commitId: str
    blobId: str
    filePath: str
    fileMode: FileModeTypeEnumType
    fileSize: int
    fileContent: bytes
    ResponseMetadata: ResponseMetadataTypeDef

class GetMergeCommitOutputTypeDef(TypedDict):
    sourceCommitId: str
    destinationCommitId: str
    baseCommitId: str
    mergedCommitId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetMergeOptionsOutputTypeDef(TypedDict):
    mergeOptions: list[MergeOptionTypeEnumType]
    sourceCommitId: str
    destinationCommitId: str
    baseCommitId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetPullRequestApprovalStatesOutputTypeDef(TypedDict):
    approvals: list[ApprovalTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetPullRequestOverrideStateOutputTypeDef(TypedDict):
    overridden: bool
    overrider: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListApprovalRuleTemplatesOutputTypeDef(TypedDict):
    approvalRuleTemplateNames: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAssociatedApprovalRuleTemplatesForRepositoryOutputTypeDef(TypedDict):
    approvalRuleTemplateNames: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListBranchesOutputTypeDef(TypedDict):
    branches: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListPullRequestsOutputTypeDef(TypedDict):
    pullRequestIds: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListRepositoriesForApprovalRuleTemplateOutputTypeDef(TypedDict):
    repositoryNames: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class MergeBranchesByFastForwardOutputTypeDef(TypedDict):
    commitId: str
    treeId: str
    ResponseMetadata: ResponseMetadataTypeDef

class MergeBranchesBySquashOutputTypeDef(TypedDict):
    commitId: str
    treeId: str
    ResponseMetadata: ResponseMetadataTypeDef

class MergeBranchesByThreeWayOutputTypeDef(TypedDict):
    commitId: str
    treeId: str
    ResponseMetadata: ResponseMetadataTypeDef

class PutFileOutputTypeDef(TypedDict):
    commitId: str
    blobId: str
    treeId: str
    ResponseMetadata: ResponseMetadataTypeDef

class PutRepositoryTriggersOutputTypeDef(TypedDict):
    configurationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateApprovalRuleTemplateContentOutputTypeDef(TypedDict):
    approvalRuleTemplate: ApprovalRuleTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateApprovalRuleTemplateDescriptionOutputTypeDef(TypedDict):
    approvalRuleTemplate: ApprovalRuleTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateApprovalRuleTemplateNameOutputTypeDef(TypedDict):
    approvalRuleTemplate: ApprovalRuleTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRepositoryEncryptionKeyOutputTypeDef(TypedDict):
    repositoryId: str
    kmsKeyId: str
    originalKmsKeyId: str
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDisassociateApprovalRuleTemplateFromRepositoriesOutputTypeDef(TypedDict):
    disassociatedRepositoryNames: list[str]
    errors: list[BatchDisassociateApprovalRuleTemplateFromRepositoriesErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetRepositoriesOutputTypeDef(TypedDict):
    repositories: list[RepositoryMetadataTypeDef]
    repositoriesNotFound: list[str]
    errors: list[BatchGetRepositoriesErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRepositoryOutputTypeDef(TypedDict):
    repositoryMetadata: RepositoryMetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetRepositoryOutputTypeDef(TypedDict):
    repositoryMetadata: RepositoryMetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DifferenceTypeDef(TypedDict):
    beforeBlob: NotRequired[BlobMetadataTypeDef]
    afterBlob: NotRequired[BlobMetadataTypeDef]
    changeType: NotRequired[ChangeTypeEnumType]

class PutFileInputTypeDef(TypedDict):
    repositoryName: str
    branchName: str
    fileContent: BlobTypeDef
    filePath: str
    fileMode: NotRequired[FileModeTypeEnumType]
    parentCommitId: NotRequired[str]
    commitMessage: NotRequired[str]
    name: NotRequired[str]
    email: NotRequired[str]

class ReplaceContentEntryTypeDef(TypedDict):
    filePath: str
    replacementType: ReplacementTypeEnumType
    content: NotRequired[BlobTypeDef]
    fileMode: NotRequired[FileModeTypeEnumType]

class DeleteBranchOutputTypeDef(TypedDict):
    deletedBranch: BranchInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetBranchOutputTypeDef(TypedDict):
    branch: BranchInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteCommentContentOutputTypeDef(TypedDict):
    comment: CommentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetCommentOutputTypeDef(TypedDict):
    comment: CommentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PostCommentReplyOutputTypeDef(TypedDict):
    comment: CommentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateCommentOutputTypeDef(TypedDict):
    comment: CommentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CommentsForComparedCommitTypeDef(TypedDict):
    repositoryName: NotRequired[str]
    beforeCommitId: NotRequired[str]
    afterCommitId: NotRequired[str]
    beforeBlobId: NotRequired[str]
    afterBlobId: NotRequired[str]
    location: NotRequired[LocationTypeDef]
    comments: NotRequired[list[CommentTypeDef]]

class CommentsForPullRequestTypeDef(TypedDict):
    pullRequestId: NotRequired[str]
    repositoryName: NotRequired[str]
    beforeCommitId: NotRequired[str]
    afterCommitId: NotRequired[str]
    beforeBlobId: NotRequired[str]
    afterBlobId: NotRequired[str]
    location: NotRequired[LocationTypeDef]
    comments: NotRequired[list[CommentTypeDef]]

class PostCommentForComparedCommitInputTypeDef(TypedDict):
    repositoryName: str
    afterCommitId: str
    content: str
    beforeCommitId: NotRequired[str]
    location: NotRequired[LocationTypeDef]
    clientRequestToken: NotRequired[str]

class PostCommentForComparedCommitOutputTypeDef(TypedDict):
    repositoryName: str
    beforeCommitId: str
    afterCommitId: str
    beforeBlobId: str
    afterBlobId: str
    location: LocationTypeDef
    comment: CommentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PostCommentForPullRequestInputTypeDef(TypedDict):
    pullRequestId: str
    repositoryName: str
    beforeCommitId: str
    afterCommitId: str
    content: str
    location: NotRequired[LocationTypeDef]
    clientRequestToken: NotRequired[str]

class PostCommentForPullRequestOutputTypeDef(TypedDict):
    repositoryName: str
    pullRequestId: str
    beforeCommitId: str
    afterCommitId: str
    beforeBlobId: str
    afterBlobId: str
    location: LocationTypeDef
    comment: CommentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CommitTypeDef(TypedDict):
    commitId: NotRequired[str]
    treeId: NotRequired[str]
    parents: NotRequired[list[str]]
    message: NotRequired[str]
    author: NotRequired[UserInfoTypeDef]
    committer: NotRequired[UserInfoTypeDef]
    additionalData: NotRequired[str]

class ConflictMetadataTypeDef(TypedDict):
    filePath: NotRequired[str]
    fileSizes: NotRequired[FileSizesTypeDef]
    fileModes: NotRequired[FileModesTypeDef]
    objectTypes: NotRequired[ObjectTypesTypeDef]
    numberOfConflicts: NotRequired[int]
    isBinaryFile: NotRequired[IsBinaryFileTypeDef]
    contentConflict: NotRequired[bool]
    fileModeConflict: NotRequired[bool]
    objectTypeConflict: NotRequired[bool]
    mergeOperations: NotRequired[MergeOperationsTypeDef]

class CreateCommitOutputTypeDef(TypedDict):
    commitId: str
    treeId: str
    filesAdded: list[FileMetadataTypeDef]
    filesUpdated: list[FileMetadataTypeDef]
    filesDeleted: list[FileMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreatePullRequestInputTypeDef(TypedDict):
    title: str
    targets: Sequence[TargetTypeDef]
    description: NotRequired[str]
    clientRequestToken: NotRequired[str]

class DescribePullRequestEventsInputPaginateTypeDef(TypedDict):
    pullRequestId: str
    pullRequestEventType: NotRequired[PullRequestEventTypeType]
    actorArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetCommentsForComparedCommitInputPaginateTypeDef(TypedDict):
    repositoryName: str
    afterCommitId: str
    beforeCommitId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetCommentsForPullRequestInputPaginateTypeDef(TypedDict):
    pullRequestId: str
    repositoryName: NotRequired[str]
    beforeCommitId: NotRequired[str]
    afterCommitId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetDifferencesInputPaginateTypeDef(TypedDict):
    repositoryName: str
    afterCommitSpecifier: str
    beforeCommitSpecifier: NotRequired[str]
    beforePath: NotRequired[str]
    afterPath: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListBranchesInputPaginateTypeDef(TypedDict):
    repositoryName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPullRequestsInputPaginateTypeDef(TypedDict):
    repositoryName: str
    authorArn: NotRequired[str]
    pullRequestStatus: NotRequired[PullRequestStatusEnumType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRepositoriesInputPaginateTypeDef(TypedDict):
    sortBy: NotRequired[SortByEnumType]
    order: NotRequired[OrderEnumType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class EvaluatePullRequestApprovalRulesOutputTypeDef(TypedDict):
    evaluation: EvaluationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetFolderOutputTypeDef(TypedDict):
    commitId: str
    folderPath: str
    treeId: str
    subFolders: list[FolderTypeDef]
    files: list[FileTypeDef]
    symbolicLinks: list[SymbolicLinkTypeDef]
    subModules: list[SubModuleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetRepositoryTriggersOutputTypeDef(TypedDict):
    configurationId: str
    triggers: list[RepositoryTriggerOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListRepositoriesOutputTypeDef(TypedDict):
    repositories: list[RepositoryNameIdPairTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class MergeHunkTypeDef(TypedDict):
    isConflict: NotRequired[bool]
    source: NotRequired[MergeHunkDetailTypeDef]
    destination: NotRequired[MergeHunkDetailTypeDef]
    base: NotRequired[MergeHunkDetailTypeDef]

class PullRequestMergedStateChangedEventMetadataTypeDef(TypedDict):
    repositoryName: NotRequired[str]
    destinationReference: NotRequired[str]
    mergeMetadata: NotRequired[MergeMetadataTypeDef]

class PullRequestTargetTypeDef(TypedDict):
    repositoryName: NotRequired[str]
    sourceReference: NotRequired[str]
    destinationReference: NotRequired[str]
    destinationCommit: NotRequired[str]
    sourceCommit: NotRequired[str]
    mergeBase: NotRequired[str]
    mergeMetadata: NotRequired[MergeMetadataTypeDef]

class PutFileEntryTypeDef(TypedDict):
    filePath: str
    fileMode: NotRequired[FileModeTypeEnumType]
    fileContent: NotRequired[BlobTypeDef]
    sourceFile: NotRequired[SourceFileSpecifierTypeDef]

class ReactionForCommentTypeDef(TypedDict):
    reaction: NotRequired[ReactionValueFormatsTypeDef]
    reactionUsers: NotRequired[list[str]]
    reactionsFromDeletedUsersCount: NotRequired[int]

class TestRepositoryTriggersOutputTypeDef(TypedDict):
    successfulExecutions: list[str]
    failedExecutions: list[RepositoryTriggerExecutionFailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

RepositoryTriggerUnionTypeDef = Union[RepositoryTriggerTypeDef, RepositoryTriggerOutputTypeDef]

class CreatePullRequestApprovalRuleOutputTypeDef(TypedDict):
    approvalRule: ApprovalRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePullRequestApprovalRuleContentOutputTypeDef(TypedDict):
    approvalRule: ApprovalRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetDifferencesOutputTypeDef(TypedDict):
    differences: list[DifferenceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ConflictResolutionTypeDef(TypedDict):
    replaceContents: NotRequired[Sequence[ReplaceContentEntryTypeDef]]
    deleteFiles: NotRequired[Sequence[DeleteFileEntryTypeDef]]
    setFileModes: NotRequired[Sequence[SetFileModeEntryTypeDef]]

class GetCommentsForComparedCommitOutputTypeDef(TypedDict):
    commentsForComparedCommitData: list[CommentsForComparedCommitTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetCommentsForPullRequestOutputTypeDef(TypedDict):
    commentsForPullRequestData: list[CommentsForPullRequestTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class BatchGetCommitsOutputTypeDef(TypedDict):
    commits: list[CommitTypeDef]
    errors: list[BatchGetCommitsErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class FileVersionTypeDef(TypedDict):
    commit: NotRequired[CommitTypeDef]
    blobId: NotRequired[str]
    path: NotRequired[str]
    revisionChildren: NotRequired[list[str]]

class GetCommitOutputTypeDef(TypedDict):
    commit: CommitTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetMergeConflictsOutputTypeDef(TypedDict):
    mergeable: bool
    destinationCommitId: str
    sourceCommitId: str
    baseCommitId: str
    conflictMetadataList: list[ConflictMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ConflictTypeDef(TypedDict):
    conflictMetadata: NotRequired[ConflictMetadataTypeDef]
    mergeHunks: NotRequired[list[MergeHunkTypeDef]]

class DescribeMergeConflictsOutputTypeDef(TypedDict):
    conflictMetadata: ConflictMetadataTypeDef
    mergeHunks: list[MergeHunkTypeDef]
    destinationCommitId: str
    sourceCommitId: str
    baseCommitId: str
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PullRequestEventTypeDef(TypedDict):
    pullRequestId: NotRequired[str]
    eventDate: NotRequired[datetime]
    pullRequestEventType: NotRequired[PullRequestEventTypeType]
    actorArn: NotRequired[str]
    pullRequestCreatedEventMetadata: NotRequired[PullRequestCreatedEventMetadataTypeDef]
    pullRequestStatusChangedEventMetadata: NotRequired[PullRequestStatusChangedEventMetadataTypeDef]
    pullRequestSourceReferenceUpdatedEventMetadata: NotRequired[
        PullRequestSourceReferenceUpdatedEventMetadataTypeDef
    ]
    pullRequestMergedStateChangedEventMetadata: NotRequired[
        PullRequestMergedStateChangedEventMetadataTypeDef
    ]
    approvalRuleEventMetadata: NotRequired[ApprovalRuleEventMetadataTypeDef]
    approvalStateChangedEventMetadata: NotRequired[ApprovalStateChangedEventMetadataTypeDef]
    approvalRuleOverriddenEventMetadata: NotRequired[ApprovalRuleOverriddenEventMetadataTypeDef]

class PullRequestTypeDef(TypedDict):
    pullRequestId: NotRequired[str]
    title: NotRequired[str]
    description: NotRequired[str]
    lastActivityDate: NotRequired[datetime]
    creationDate: NotRequired[datetime]
    pullRequestStatus: NotRequired[PullRequestStatusEnumType]
    authorArn: NotRequired[str]
    pullRequestTargets: NotRequired[list[PullRequestTargetTypeDef]]
    clientRequestToken: NotRequired[str]
    revisionId: NotRequired[str]
    approvalRules: NotRequired[list[ApprovalRuleTypeDef]]

class CreateCommitInputTypeDef(TypedDict):
    repositoryName: str
    branchName: str
    parentCommitId: NotRequired[str]
    authorName: NotRequired[str]
    email: NotRequired[str]
    commitMessage: NotRequired[str]
    keepEmptyFolders: NotRequired[bool]
    putFiles: NotRequired[Sequence[PutFileEntryTypeDef]]
    deleteFiles: NotRequired[Sequence[DeleteFileEntryTypeDef]]
    setFileModes: NotRequired[Sequence[SetFileModeEntryTypeDef]]

class GetCommentReactionsOutputTypeDef(TypedDict):
    reactionsForComment: list[ReactionForCommentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PutRepositoryTriggersInputTypeDef(TypedDict):
    repositoryName: str
    triggers: Sequence[RepositoryTriggerUnionTypeDef]

class TestRepositoryTriggersInputTypeDef(TypedDict):
    repositoryName: str
    triggers: Sequence[RepositoryTriggerUnionTypeDef]

class CreateUnreferencedMergeCommitInputTypeDef(TypedDict):
    repositoryName: str
    sourceCommitSpecifier: str
    destinationCommitSpecifier: str
    mergeOption: MergeOptionTypeEnumType
    conflictDetailLevel: NotRequired[ConflictDetailLevelTypeEnumType]
    conflictResolutionStrategy: NotRequired[ConflictResolutionStrategyTypeEnumType]
    authorName: NotRequired[str]
    email: NotRequired[str]
    commitMessage: NotRequired[str]
    keepEmptyFolders: NotRequired[bool]
    conflictResolution: NotRequired[ConflictResolutionTypeDef]

class MergeBranchesBySquashInputTypeDef(TypedDict):
    repositoryName: str
    sourceCommitSpecifier: str
    destinationCommitSpecifier: str
    targetBranch: NotRequired[str]
    conflictDetailLevel: NotRequired[ConflictDetailLevelTypeEnumType]
    conflictResolutionStrategy: NotRequired[ConflictResolutionStrategyTypeEnumType]
    authorName: NotRequired[str]
    email: NotRequired[str]
    commitMessage: NotRequired[str]
    keepEmptyFolders: NotRequired[bool]
    conflictResolution: NotRequired[ConflictResolutionTypeDef]

class MergeBranchesByThreeWayInputTypeDef(TypedDict):
    repositoryName: str
    sourceCommitSpecifier: str
    destinationCommitSpecifier: str
    targetBranch: NotRequired[str]
    conflictDetailLevel: NotRequired[ConflictDetailLevelTypeEnumType]
    conflictResolutionStrategy: NotRequired[ConflictResolutionStrategyTypeEnumType]
    authorName: NotRequired[str]
    email: NotRequired[str]
    commitMessage: NotRequired[str]
    keepEmptyFolders: NotRequired[bool]
    conflictResolution: NotRequired[ConflictResolutionTypeDef]

class MergePullRequestBySquashInputTypeDef(TypedDict):
    pullRequestId: str
    repositoryName: str
    sourceCommitId: NotRequired[str]
    conflictDetailLevel: NotRequired[ConflictDetailLevelTypeEnumType]
    conflictResolutionStrategy: NotRequired[ConflictResolutionStrategyTypeEnumType]
    commitMessage: NotRequired[str]
    authorName: NotRequired[str]
    email: NotRequired[str]
    keepEmptyFolders: NotRequired[bool]
    conflictResolution: NotRequired[ConflictResolutionTypeDef]

class MergePullRequestByThreeWayInputTypeDef(TypedDict):
    pullRequestId: str
    repositoryName: str
    sourceCommitId: NotRequired[str]
    conflictDetailLevel: NotRequired[ConflictDetailLevelTypeEnumType]
    conflictResolutionStrategy: NotRequired[ConflictResolutionStrategyTypeEnumType]
    commitMessage: NotRequired[str]
    authorName: NotRequired[str]
    email: NotRequired[str]
    keepEmptyFolders: NotRequired[bool]
    conflictResolution: NotRequired[ConflictResolutionTypeDef]

class ListFileCommitHistoryResponseTypeDef(TypedDict):
    revisionDag: list[FileVersionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class BatchDescribeMergeConflictsOutputTypeDef(TypedDict):
    conflicts: list[ConflictTypeDef]
    errors: list[BatchDescribeMergeConflictsErrorTypeDef]
    destinationCommitId: str
    sourceCommitId: str
    baseCommitId: str
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DescribePullRequestEventsOutputTypeDef(TypedDict):
    pullRequestEvents: list[PullRequestEventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreatePullRequestOutputTypeDef(TypedDict):
    pullRequest: PullRequestTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetPullRequestOutputTypeDef(TypedDict):
    pullRequest: PullRequestTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class MergePullRequestByFastForwardOutputTypeDef(TypedDict):
    pullRequest: PullRequestTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class MergePullRequestBySquashOutputTypeDef(TypedDict):
    pullRequest: PullRequestTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class MergePullRequestByThreeWayOutputTypeDef(TypedDict):
    pullRequest: PullRequestTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePullRequestDescriptionOutputTypeDef(TypedDict):
    pullRequest: PullRequestTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePullRequestStatusOutputTypeDef(TypedDict):
    pullRequest: PullRequestTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePullRequestTitleOutputTypeDef(TypedDict):
    pullRequest: PullRequestTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
