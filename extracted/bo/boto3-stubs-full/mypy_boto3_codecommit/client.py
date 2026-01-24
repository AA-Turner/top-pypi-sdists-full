"""
Type annotations for codecommit service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_codecommit.client import CodeCommitClient

    session = Session()
    client: CodeCommitClient = session.client("codecommit")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    DescribePullRequestEventsPaginator,
    GetCommentsForComparedCommitPaginator,
    GetCommentsForPullRequestPaginator,
    GetDifferencesPaginator,
    ListBranchesPaginator,
    ListPullRequestsPaginator,
    ListRepositoriesPaginator,
)
from .type_defs import (
    AssociateApprovalRuleTemplateWithRepositoryInputTypeDef,
    BatchAssociateApprovalRuleTemplateWithRepositoriesInputTypeDef,
    BatchAssociateApprovalRuleTemplateWithRepositoriesOutputTypeDef,
    BatchDescribeMergeConflictsInputTypeDef,
    BatchDescribeMergeConflictsOutputTypeDef,
    BatchDisassociateApprovalRuleTemplateFromRepositoriesInputTypeDef,
    BatchDisassociateApprovalRuleTemplateFromRepositoriesOutputTypeDef,
    BatchGetCommitsInputTypeDef,
    BatchGetCommitsOutputTypeDef,
    BatchGetRepositoriesInputTypeDef,
    BatchGetRepositoriesOutputTypeDef,
    CreateApprovalRuleTemplateInputTypeDef,
    CreateApprovalRuleTemplateOutputTypeDef,
    CreateBranchInputTypeDef,
    CreateCommitInputTypeDef,
    CreateCommitOutputTypeDef,
    CreatePullRequestApprovalRuleInputTypeDef,
    CreatePullRequestApprovalRuleOutputTypeDef,
    CreatePullRequestInputTypeDef,
    CreatePullRequestOutputTypeDef,
    CreateRepositoryInputTypeDef,
    CreateRepositoryOutputTypeDef,
    CreateUnreferencedMergeCommitInputTypeDef,
    CreateUnreferencedMergeCommitOutputTypeDef,
    DeleteApprovalRuleTemplateInputTypeDef,
    DeleteApprovalRuleTemplateOutputTypeDef,
    DeleteBranchInputTypeDef,
    DeleteBranchOutputTypeDef,
    DeleteCommentContentInputTypeDef,
    DeleteCommentContentOutputTypeDef,
    DeleteFileInputTypeDef,
    DeleteFileOutputTypeDef,
    DeletePullRequestApprovalRuleInputTypeDef,
    DeletePullRequestApprovalRuleOutputTypeDef,
    DeleteRepositoryInputTypeDef,
    DeleteRepositoryOutputTypeDef,
    DescribeMergeConflictsInputTypeDef,
    DescribeMergeConflictsOutputTypeDef,
    DescribePullRequestEventsInputTypeDef,
    DescribePullRequestEventsOutputTypeDef,
    DisassociateApprovalRuleTemplateFromRepositoryInputTypeDef,
    EmptyResponseMetadataTypeDef,
    EvaluatePullRequestApprovalRulesInputTypeDef,
    EvaluatePullRequestApprovalRulesOutputTypeDef,
    GetApprovalRuleTemplateInputTypeDef,
    GetApprovalRuleTemplateOutputTypeDef,
    GetBlobInputTypeDef,
    GetBlobOutputTypeDef,
    GetBranchInputTypeDef,
    GetBranchOutputTypeDef,
    GetCommentInputTypeDef,
    GetCommentOutputTypeDef,
    GetCommentReactionsInputTypeDef,
    GetCommentReactionsOutputTypeDef,
    GetCommentsForComparedCommitInputTypeDef,
    GetCommentsForComparedCommitOutputTypeDef,
    GetCommentsForPullRequestInputTypeDef,
    GetCommentsForPullRequestOutputTypeDef,
    GetCommitInputTypeDef,
    GetCommitOutputTypeDef,
    GetDifferencesInputTypeDef,
    GetDifferencesOutputTypeDef,
    GetFileInputTypeDef,
    GetFileOutputTypeDef,
    GetFolderInputTypeDef,
    GetFolderOutputTypeDef,
    GetMergeCommitInputTypeDef,
    GetMergeCommitOutputTypeDef,
    GetMergeConflictsInputTypeDef,
    GetMergeConflictsOutputTypeDef,
    GetMergeOptionsInputTypeDef,
    GetMergeOptionsOutputTypeDef,
    GetPullRequestApprovalStatesInputTypeDef,
    GetPullRequestApprovalStatesOutputTypeDef,
    GetPullRequestInputTypeDef,
    GetPullRequestOutputTypeDef,
    GetPullRequestOverrideStateInputTypeDef,
    GetPullRequestOverrideStateOutputTypeDef,
    GetRepositoryInputTypeDef,
    GetRepositoryOutputTypeDef,
    GetRepositoryTriggersInputTypeDef,
    GetRepositoryTriggersOutputTypeDef,
    ListApprovalRuleTemplatesInputTypeDef,
    ListApprovalRuleTemplatesOutputTypeDef,
    ListAssociatedApprovalRuleTemplatesForRepositoryInputTypeDef,
    ListAssociatedApprovalRuleTemplatesForRepositoryOutputTypeDef,
    ListBranchesInputTypeDef,
    ListBranchesOutputTypeDef,
    ListFileCommitHistoryRequestTypeDef,
    ListFileCommitHistoryResponseTypeDef,
    ListPullRequestsInputTypeDef,
    ListPullRequestsOutputTypeDef,
    ListRepositoriesForApprovalRuleTemplateInputTypeDef,
    ListRepositoriesForApprovalRuleTemplateOutputTypeDef,
    ListRepositoriesInputTypeDef,
    ListRepositoriesOutputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    MergeBranchesByFastForwardInputTypeDef,
    MergeBranchesByFastForwardOutputTypeDef,
    MergeBranchesBySquashInputTypeDef,
    MergeBranchesBySquashOutputTypeDef,
    MergeBranchesByThreeWayInputTypeDef,
    MergeBranchesByThreeWayOutputTypeDef,
    MergePullRequestByFastForwardInputTypeDef,
    MergePullRequestByFastForwardOutputTypeDef,
    MergePullRequestBySquashInputTypeDef,
    MergePullRequestBySquashOutputTypeDef,
    MergePullRequestByThreeWayInputTypeDef,
    MergePullRequestByThreeWayOutputTypeDef,
    OverridePullRequestApprovalRulesInputTypeDef,
    PostCommentForComparedCommitInputTypeDef,
    PostCommentForComparedCommitOutputTypeDef,
    PostCommentForPullRequestInputTypeDef,
    PostCommentForPullRequestOutputTypeDef,
    PostCommentReplyInputTypeDef,
    PostCommentReplyOutputTypeDef,
    PutCommentReactionInputTypeDef,
    PutFileInputTypeDef,
    PutFileOutputTypeDef,
    PutRepositoryTriggersInputTypeDef,
    PutRepositoryTriggersOutputTypeDef,
    TagResourceInputTypeDef,
    TestRepositoryTriggersInputTypeDef,
    TestRepositoryTriggersOutputTypeDef,
    UntagResourceInputTypeDef,
    UpdateApprovalRuleTemplateContentInputTypeDef,
    UpdateApprovalRuleTemplateContentOutputTypeDef,
    UpdateApprovalRuleTemplateDescriptionInputTypeDef,
    UpdateApprovalRuleTemplateDescriptionOutputTypeDef,
    UpdateApprovalRuleTemplateNameInputTypeDef,
    UpdateApprovalRuleTemplateNameOutputTypeDef,
    UpdateCommentInputTypeDef,
    UpdateCommentOutputTypeDef,
    UpdateDefaultBranchInputTypeDef,
    UpdatePullRequestApprovalRuleContentInputTypeDef,
    UpdatePullRequestApprovalRuleContentOutputTypeDef,
    UpdatePullRequestApprovalStateInputTypeDef,
    UpdatePullRequestDescriptionInputTypeDef,
    UpdatePullRequestDescriptionOutputTypeDef,
    UpdatePullRequestStatusInputTypeDef,
    UpdatePullRequestStatusOutputTypeDef,
    UpdatePullRequestTitleInputTypeDef,
    UpdatePullRequestTitleOutputTypeDef,
    UpdateRepositoryDescriptionInputTypeDef,
    UpdateRepositoryEncryptionKeyInputTypeDef,
    UpdateRepositoryEncryptionKeyOutputTypeDef,
    UpdateRepositoryNameInputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("CodeCommitClient",)


class Exceptions(BaseClientExceptions):
    ActorDoesNotExistException: type[BotocoreClientError]
    ApprovalRuleContentRequiredException: type[BotocoreClientError]
    ApprovalRuleDoesNotExistException: type[BotocoreClientError]
    ApprovalRuleNameAlreadyExistsException: type[BotocoreClientError]
    ApprovalRuleNameRequiredException: type[BotocoreClientError]
    ApprovalRuleTemplateContentRequiredException: type[BotocoreClientError]
    ApprovalRuleTemplateDoesNotExistException: type[BotocoreClientError]
    ApprovalRuleTemplateInUseException: type[BotocoreClientError]
    ApprovalRuleTemplateNameAlreadyExistsException: type[BotocoreClientError]
    ApprovalRuleTemplateNameRequiredException: type[BotocoreClientError]
    ApprovalStateRequiredException: type[BotocoreClientError]
    AuthorDoesNotExistException: type[BotocoreClientError]
    BeforeCommitIdAndAfterCommitIdAreSameException: type[BotocoreClientError]
    BlobIdDoesNotExistException: type[BotocoreClientError]
    BlobIdRequiredException: type[BotocoreClientError]
    BranchDoesNotExistException: type[BotocoreClientError]
    BranchNameExistsException: type[BotocoreClientError]
    BranchNameIsTagNameException: type[BotocoreClientError]
    BranchNameRequiredException: type[BotocoreClientError]
    CannotDeleteApprovalRuleFromTemplateException: type[BotocoreClientError]
    CannotModifyApprovalRuleFromTemplateException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ClientRequestTokenRequiredException: type[BotocoreClientError]
    CommentContentRequiredException: type[BotocoreClientError]
    CommentContentSizeLimitExceededException: type[BotocoreClientError]
    CommentDeletedException: type[BotocoreClientError]
    CommentDoesNotExistException: type[BotocoreClientError]
    CommentIdRequiredException: type[BotocoreClientError]
    CommentNotCreatedByCallerException: type[BotocoreClientError]
    CommitDoesNotExistException: type[BotocoreClientError]
    CommitIdDoesNotExistException: type[BotocoreClientError]
    CommitIdRequiredException: type[BotocoreClientError]
    CommitIdsLimitExceededException: type[BotocoreClientError]
    CommitIdsListRequiredException: type[BotocoreClientError]
    CommitMessageLengthExceededException: type[BotocoreClientError]
    CommitRequiredException: type[BotocoreClientError]
    ConcurrentReferenceUpdateException: type[BotocoreClientError]
    DefaultBranchCannotBeDeletedException: type[BotocoreClientError]
    DirectoryNameConflictsWithFileNameException: type[BotocoreClientError]
    EncryptionIntegrityChecksFailedException: type[BotocoreClientError]
    EncryptionKeyAccessDeniedException: type[BotocoreClientError]
    EncryptionKeyDisabledException: type[BotocoreClientError]
    EncryptionKeyInvalidIdException: type[BotocoreClientError]
    EncryptionKeyInvalidUsageException: type[BotocoreClientError]
    EncryptionKeyNotFoundException: type[BotocoreClientError]
    EncryptionKeyRequiredException: type[BotocoreClientError]
    EncryptionKeyUnavailableException: type[BotocoreClientError]
    FileContentAndSourceFileSpecifiedException: type[BotocoreClientError]
    FileContentRequiredException: type[BotocoreClientError]
    FileContentSizeLimitExceededException: type[BotocoreClientError]
    FileDoesNotExistException: type[BotocoreClientError]
    FileEntryRequiredException: type[BotocoreClientError]
    FileModeRequiredException: type[BotocoreClientError]
    FileNameConflictsWithDirectoryNameException: type[BotocoreClientError]
    FilePathConflictsWithSubmodulePathException: type[BotocoreClientError]
    FileTooLargeException: type[BotocoreClientError]
    FolderContentSizeLimitExceededException: type[BotocoreClientError]
    FolderDoesNotExistException: type[BotocoreClientError]
    IdempotencyParameterMismatchException: type[BotocoreClientError]
    InvalidActorArnException: type[BotocoreClientError]
    InvalidApprovalRuleContentException: type[BotocoreClientError]
    InvalidApprovalRuleNameException: type[BotocoreClientError]
    InvalidApprovalRuleTemplateContentException: type[BotocoreClientError]
    InvalidApprovalRuleTemplateDescriptionException: type[BotocoreClientError]
    InvalidApprovalRuleTemplateNameException: type[BotocoreClientError]
    InvalidApprovalStateException: type[BotocoreClientError]
    InvalidAuthorArnException: type[BotocoreClientError]
    InvalidBlobIdException: type[BotocoreClientError]
    InvalidBranchNameException: type[BotocoreClientError]
    InvalidClientRequestTokenException: type[BotocoreClientError]
    InvalidCommentIdException: type[BotocoreClientError]
    InvalidCommitException: type[BotocoreClientError]
    InvalidCommitIdException: type[BotocoreClientError]
    InvalidConflictDetailLevelException: type[BotocoreClientError]
    InvalidConflictResolutionException: type[BotocoreClientError]
    InvalidConflictResolutionStrategyException: type[BotocoreClientError]
    InvalidContinuationTokenException: type[BotocoreClientError]
    InvalidDeletionParameterException: type[BotocoreClientError]
    InvalidDescriptionException: type[BotocoreClientError]
    InvalidDestinationCommitSpecifierException: type[BotocoreClientError]
    InvalidEmailException: type[BotocoreClientError]
    InvalidFileLocationException: type[BotocoreClientError]
    InvalidFileModeException: type[BotocoreClientError]
    InvalidFilePositionException: type[BotocoreClientError]
    InvalidMaxConflictFilesException: type[BotocoreClientError]
    InvalidMaxMergeHunksException: type[BotocoreClientError]
    InvalidMaxResultsException: type[BotocoreClientError]
    InvalidMergeOptionException: type[BotocoreClientError]
    InvalidOrderException: type[BotocoreClientError]
    InvalidOverrideStatusException: type[BotocoreClientError]
    InvalidParentCommitIdException: type[BotocoreClientError]
    InvalidPathException: type[BotocoreClientError]
    InvalidPullRequestEventTypeException: type[BotocoreClientError]
    InvalidPullRequestIdException: type[BotocoreClientError]
    InvalidPullRequestStatusException: type[BotocoreClientError]
    InvalidPullRequestStatusUpdateException: type[BotocoreClientError]
    InvalidReactionUserArnException: type[BotocoreClientError]
    InvalidReactionValueException: type[BotocoreClientError]
    InvalidReferenceNameException: type[BotocoreClientError]
    InvalidRelativeFileVersionEnumException: type[BotocoreClientError]
    InvalidReplacementContentException: type[BotocoreClientError]
    InvalidReplacementTypeException: type[BotocoreClientError]
    InvalidRepositoryDescriptionException: type[BotocoreClientError]
    InvalidRepositoryNameException: type[BotocoreClientError]
    InvalidRepositoryTriggerBranchNameException: type[BotocoreClientError]
    InvalidRepositoryTriggerCustomDataException: type[BotocoreClientError]
    InvalidRepositoryTriggerDestinationArnException: type[BotocoreClientError]
    InvalidRepositoryTriggerEventsException: type[BotocoreClientError]
    InvalidRepositoryTriggerNameException: type[BotocoreClientError]
    InvalidRepositoryTriggerRegionException: type[BotocoreClientError]
    InvalidResourceArnException: type[BotocoreClientError]
    InvalidRevisionIdException: type[BotocoreClientError]
    InvalidRuleContentSha256Exception: type[BotocoreClientError]
    InvalidSortByException: type[BotocoreClientError]
    InvalidSourceCommitSpecifierException: type[BotocoreClientError]
    InvalidSystemTagUsageException: type[BotocoreClientError]
    InvalidTagKeysListException: type[BotocoreClientError]
    InvalidTagsMapException: type[BotocoreClientError]
    InvalidTargetBranchException: type[BotocoreClientError]
    InvalidTargetException: type[BotocoreClientError]
    InvalidTargetsException: type[BotocoreClientError]
    InvalidTitleException: type[BotocoreClientError]
    ManualMergeRequiredException: type[BotocoreClientError]
    MaximumBranchesExceededException: type[BotocoreClientError]
    MaximumConflictResolutionEntriesExceededException: type[BotocoreClientError]
    MaximumFileContentToLoadExceededException: type[BotocoreClientError]
    MaximumFileEntriesExceededException: type[BotocoreClientError]
    MaximumItemsToCompareExceededException: type[BotocoreClientError]
    MaximumNumberOfApprovalsExceededException: type[BotocoreClientError]
    MaximumOpenPullRequestsExceededException: type[BotocoreClientError]
    MaximumRepositoryNamesExceededException: type[BotocoreClientError]
    MaximumRepositoryTriggersExceededException: type[BotocoreClientError]
    MaximumRuleTemplatesAssociatedWithRepositoryException: type[BotocoreClientError]
    MergeOptionRequiredException: type[BotocoreClientError]
    MultipleConflictResolutionEntriesException: type[BotocoreClientError]
    MultipleRepositoriesInPullRequestException: type[BotocoreClientError]
    NameLengthExceededException: type[BotocoreClientError]
    NoChangeException: type[BotocoreClientError]
    NumberOfRuleTemplatesExceededException: type[BotocoreClientError]
    NumberOfRulesExceededException: type[BotocoreClientError]
    OperationNotAllowedException: type[BotocoreClientError]
    OverrideAlreadySetException: type[BotocoreClientError]
    OverrideStatusRequiredException: type[BotocoreClientError]
    ParentCommitDoesNotExistException: type[BotocoreClientError]
    ParentCommitIdOutdatedException: type[BotocoreClientError]
    ParentCommitIdRequiredException: type[BotocoreClientError]
    PathDoesNotExistException: type[BotocoreClientError]
    PathRequiredException: type[BotocoreClientError]
    PullRequestAlreadyClosedException: type[BotocoreClientError]
    PullRequestApprovalRulesNotSatisfiedException: type[BotocoreClientError]
    PullRequestCannotBeApprovedByAuthorException: type[BotocoreClientError]
    PullRequestDoesNotExistException: type[BotocoreClientError]
    PullRequestIdRequiredException: type[BotocoreClientError]
    PullRequestStatusRequiredException: type[BotocoreClientError]
    PutFileEntryConflictException: type[BotocoreClientError]
    ReactionLimitExceededException: type[BotocoreClientError]
    ReactionValueRequiredException: type[BotocoreClientError]
    ReferenceDoesNotExistException: type[BotocoreClientError]
    ReferenceNameRequiredException: type[BotocoreClientError]
    ReferenceTypeNotSupportedException: type[BotocoreClientError]
    ReplacementContentRequiredException: type[BotocoreClientError]
    ReplacementTypeRequiredException: type[BotocoreClientError]
    RepositoryDoesNotExistException: type[BotocoreClientError]
    RepositoryLimitExceededException: type[BotocoreClientError]
    RepositoryNameExistsException: type[BotocoreClientError]
    RepositoryNameRequiredException: type[BotocoreClientError]
    RepositoryNamesRequiredException: type[BotocoreClientError]
    RepositoryNotAssociatedWithPullRequestException: type[BotocoreClientError]
    RepositoryTriggerBranchNameListRequiredException: type[BotocoreClientError]
    RepositoryTriggerDestinationArnRequiredException: type[BotocoreClientError]
    RepositoryTriggerEventsListRequiredException: type[BotocoreClientError]
    RepositoryTriggerNameRequiredException: type[BotocoreClientError]
    RepositoryTriggersListRequiredException: type[BotocoreClientError]
    ResourceArnRequiredException: type[BotocoreClientError]
    RestrictedSourceFileException: type[BotocoreClientError]
    RevisionIdRequiredException: type[BotocoreClientError]
    RevisionNotCurrentException: type[BotocoreClientError]
    SameFileContentException: type[BotocoreClientError]
    SamePathRequestException: type[BotocoreClientError]
    SourceAndDestinationAreSameException: type[BotocoreClientError]
    SourceFileOrContentRequiredException: type[BotocoreClientError]
    TagKeysListRequiredException: type[BotocoreClientError]
    TagPolicyException: type[BotocoreClientError]
    TagsMapRequiredException: type[BotocoreClientError]
    TargetRequiredException: type[BotocoreClientError]
    TargetsRequiredException: type[BotocoreClientError]
    TipOfSourceReferenceIsDifferentException: type[BotocoreClientError]
    TipsDivergenceExceededException: type[BotocoreClientError]
    TitleRequiredException: type[BotocoreClientError]
    TooManyTagsException: type[BotocoreClientError]


class CodeCommitClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CodeCommitClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#generate_presigned_url)
        """

    def associate_approval_rule_template_with_repository(
        self, **kwargs: Unpack[AssociateApprovalRuleTemplateWithRepositoryInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates an association between an approval rule template and a specified
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/associate_approval_rule_template_with_repository.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#associate_approval_rule_template_with_repository)
        """

    def batch_associate_approval_rule_template_with_repositories(
        self, **kwargs: Unpack[BatchAssociateApprovalRuleTemplateWithRepositoriesInputTypeDef]
    ) -> BatchAssociateApprovalRuleTemplateWithRepositoriesOutputTypeDef:
        """
        Creates an association between an approval rule template and one or more
        specified repositories.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/batch_associate_approval_rule_template_with_repositories.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#batch_associate_approval_rule_template_with_repositories)
        """

    def batch_describe_merge_conflicts(
        self, **kwargs: Unpack[BatchDescribeMergeConflictsInputTypeDef]
    ) -> BatchDescribeMergeConflictsOutputTypeDef:
        """
        Returns information about one or more merge conflicts in the attempted merge of
        two commit specifiers using the squash or three-way merge strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/batch_describe_merge_conflicts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#batch_describe_merge_conflicts)
        """

    def batch_disassociate_approval_rule_template_from_repositories(
        self, **kwargs: Unpack[BatchDisassociateApprovalRuleTemplateFromRepositoriesInputTypeDef]
    ) -> BatchDisassociateApprovalRuleTemplateFromRepositoriesOutputTypeDef:
        """
        Removes the association between an approval rule template and one or more
        specified repositories.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/batch_disassociate_approval_rule_template_from_repositories.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#batch_disassociate_approval_rule_template_from_repositories)
        """

    def batch_get_commits(
        self, **kwargs: Unpack[BatchGetCommitsInputTypeDef]
    ) -> BatchGetCommitsOutputTypeDef:
        """
        Returns information about the contents of one or more commits in a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/batch_get_commits.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#batch_get_commits)
        """

    def batch_get_repositories(
        self, **kwargs: Unpack[BatchGetRepositoriesInputTypeDef]
    ) -> BatchGetRepositoriesOutputTypeDef:
        """
        Returns information about one or more repositories.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/batch_get_repositories.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#batch_get_repositories)
        """

    def create_approval_rule_template(
        self, **kwargs: Unpack[CreateApprovalRuleTemplateInputTypeDef]
    ) -> CreateApprovalRuleTemplateOutputTypeDef:
        """
        Creates a template for approval rules that can then be associated with one or
        more repositories in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/create_approval_rule_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#create_approval_rule_template)
        """

    def create_branch(
        self, **kwargs: Unpack[CreateBranchInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a branch in a repository and points the branch to a commit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/create_branch.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#create_branch)
        """

    def create_commit(
        self, **kwargs: Unpack[CreateCommitInputTypeDef]
    ) -> CreateCommitOutputTypeDef:
        """
        Creates a commit for a repository on the tip of a specified branch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/create_commit.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#create_commit)
        """

    def create_pull_request(
        self, **kwargs: Unpack[CreatePullRequestInputTypeDef]
    ) -> CreatePullRequestOutputTypeDef:
        """
        Creates a pull request in the specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/create_pull_request.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#create_pull_request)
        """

    def create_pull_request_approval_rule(
        self, **kwargs: Unpack[CreatePullRequestApprovalRuleInputTypeDef]
    ) -> CreatePullRequestApprovalRuleOutputTypeDef:
        """
        Creates an approval rule for a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/create_pull_request_approval_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#create_pull_request_approval_rule)
        """

    def create_repository(
        self, **kwargs: Unpack[CreateRepositoryInputTypeDef]
    ) -> CreateRepositoryOutputTypeDef:
        """
        Creates a new, empty repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/create_repository.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#create_repository)
        """

    def create_unreferenced_merge_commit(
        self, **kwargs: Unpack[CreateUnreferencedMergeCommitInputTypeDef]
    ) -> CreateUnreferencedMergeCommitOutputTypeDef:
        """
        Creates an unreferenced commit that represents the result of merging two
        branches using a specified merge strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/create_unreferenced_merge_commit.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#create_unreferenced_merge_commit)
        """

    def delete_approval_rule_template(
        self, **kwargs: Unpack[DeleteApprovalRuleTemplateInputTypeDef]
    ) -> DeleteApprovalRuleTemplateOutputTypeDef:
        """
        Deletes a specified approval rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/delete_approval_rule_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#delete_approval_rule_template)
        """

    def delete_branch(
        self, **kwargs: Unpack[DeleteBranchInputTypeDef]
    ) -> DeleteBranchOutputTypeDef:
        """
        Deletes a branch from a repository, unless that branch is the default branch
        for the repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/delete_branch.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#delete_branch)
        """

    def delete_comment_content(
        self, **kwargs: Unpack[DeleteCommentContentInputTypeDef]
    ) -> DeleteCommentContentOutputTypeDef:
        """
        Deletes the content of a comment made on a change, file, or commit in a
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/delete_comment_content.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#delete_comment_content)
        """

    def delete_file(self, **kwargs: Unpack[DeleteFileInputTypeDef]) -> DeleteFileOutputTypeDef:
        """
        Deletes a specified file from a specified branch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/delete_file.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#delete_file)
        """

    def delete_pull_request_approval_rule(
        self, **kwargs: Unpack[DeletePullRequestApprovalRuleInputTypeDef]
    ) -> DeletePullRequestApprovalRuleOutputTypeDef:
        """
        Deletes an approval rule from a specified pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/delete_pull_request_approval_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#delete_pull_request_approval_rule)
        """

    def delete_repository(
        self, **kwargs: Unpack[DeleteRepositoryInputTypeDef]
    ) -> DeleteRepositoryOutputTypeDef:
        """
        Deletes a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/delete_repository.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#delete_repository)
        """

    def describe_merge_conflicts(
        self, **kwargs: Unpack[DescribeMergeConflictsInputTypeDef]
    ) -> DescribeMergeConflictsOutputTypeDef:
        """
        Returns information about one or more merge conflicts in the attempted merge of
        two commit specifiers using the squash or three-way merge strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/describe_merge_conflicts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#describe_merge_conflicts)
        """

    def describe_pull_request_events(
        self, **kwargs: Unpack[DescribePullRequestEventsInputTypeDef]
    ) -> DescribePullRequestEventsOutputTypeDef:
        """
        Returns information about one or more pull request events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/describe_pull_request_events.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#describe_pull_request_events)
        """

    def disassociate_approval_rule_template_from_repository(
        self, **kwargs: Unpack[DisassociateApprovalRuleTemplateFromRepositoryInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the association between a template and a repository so that approval
        rules based on the template are not automatically created when pull requests
        are created in the specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/disassociate_approval_rule_template_from_repository.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#disassociate_approval_rule_template_from_repository)
        """

    def evaluate_pull_request_approval_rules(
        self, **kwargs: Unpack[EvaluatePullRequestApprovalRulesInputTypeDef]
    ) -> EvaluatePullRequestApprovalRulesOutputTypeDef:
        """
        Evaluates whether a pull request has met all the conditions specified in its
        associated approval rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/evaluate_pull_request_approval_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#evaluate_pull_request_approval_rules)
        """

    def get_approval_rule_template(
        self, **kwargs: Unpack[GetApprovalRuleTemplateInputTypeDef]
    ) -> GetApprovalRuleTemplateOutputTypeDef:
        """
        Returns information about a specified approval rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_approval_rule_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_approval_rule_template)
        """

    def get_blob(self, **kwargs: Unpack[GetBlobInputTypeDef]) -> GetBlobOutputTypeDef:
        """
        Returns the base-64 encoded content of an individual blob in a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_blob.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_blob)
        """

    def get_branch(self, **kwargs: Unpack[GetBranchInputTypeDef]) -> GetBranchOutputTypeDef:
        """
        Returns information about a repository branch, including its name and the last
        commit ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_branch.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_branch)
        """

    def get_comment(self, **kwargs: Unpack[GetCommentInputTypeDef]) -> GetCommentOutputTypeDef:
        """
        Returns the content of a comment made on a change, file, or commit in a
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_comment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_comment)
        """

    def get_comment_reactions(
        self, **kwargs: Unpack[GetCommentReactionsInputTypeDef]
    ) -> GetCommentReactionsOutputTypeDef:
        """
        Returns information about reactions to a specified comment ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_comment_reactions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_comment_reactions)
        """

    def get_comments_for_compared_commit(
        self, **kwargs: Unpack[GetCommentsForComparedCommitInputTypeDef]
    ) -> GetCommentsForComparedCommitOutputTypeDef:
        """
        Returns information about comments made on the comparison between two commits.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_comments_for_compared_commit.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_comments_for_compared_commit)
        """

    def get_comments_for_pull_request(
        self, **kwargs: Unpack[GetCommentsForPullRequestInputTypeDef]
    ) -> GetCommentsForPullRequestOutputTypeDef:
        """
        Returns comments made on a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_comments_for_pull_request.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_comments_for_pull_request)
        """

    def get_commit(self, **kwargs: Unpack[GetCommitInputTypeDef]) -> GetCommitOutputTypeDef:
        """
        Returns information about a commit, including commit message and committer
        information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_commit.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_commit)
        """

    def get_differences(
        self, **kwargs: Unpack[GetDifferencesInputTypeDef]
    ) -> GetDifferencesOutputTypeDef:
        """
        Returns information about the differences in a valid commit specifier (such as
        a branch, tag, HEAD, commit ID, or other fully qualified reference).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_differences.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_differences)
        """

    def get_file(self, **kwargs: Unpack[GetFileInputTypeDef]) -> GetFileOutputTypeDef:
        """
        Returns the base-64 encoded contents of a specified file and its metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_file.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_file)
        """

    def get_folder(self, **kwargs: Unpack[GetFolderInputTypeDef]) -> GetFolderOutputTypeDef:
        """
        Returns the contents of a specified folder in a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_folder.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_folder)
        """

    def get_merge_commit(
        self, **kwargs: Unpack[GetMergeCommitInputTypeDef]
    ) -> GetMergeCommitOutputTypeDef:
        """
        Returns information about a specified merge commit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_merge_commit.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_merge_commit)
        """

    def get_merge_conflicts(
        self, **kwargs: Unpack[GetMergeConflictsInputTypeDef]
    ) -> GetMergeConflictsOutputTypeDef:
        """
        Returns information about merge conflicts between the before and after commit
        IDs for a pull request in a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_merge_conflicts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_merge_conflicts)
        """

    def get_merge_options(
        self, **kwargs: Unpack[GetMergeOptionsInputTypeDef]
    ) -> GetMergeOptionsOutputTypeDef:
        """
        Returns information about the merge options available for merging two specified
        branches.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_merge_options.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_merge_options)
        """

    def get_pull_request(
        self, **kwargs: Unpack[GetPullRequestInputTypeDef]
    ) -> GetPullRequestOutputTypeDef:
        """
        Gets information about a pull request in a specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_pull_request.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_pull_request)
        """

    def get_pull_request_approval_states(
        self, **kwargs: Unpack[GetPullRequestApprovalStatesInputTypeDef]
    ) -> GetPullRequestApprovalStatesOutputTypeDef:
        """
        Gets information about the approval states for a specified pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_pull_request_approval_states.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_pull_request_approval_states)
        """

    def get_pull_request_override_state(
        self, **kwargs: Unpack[GetPullRequestOverrideStateInputTypeDef]
    ) -> GetPullRequestOverrideStateOutputTypeDef:
        """
        Returns information about whether approval rules have been set aside
        (overridden) for a pull request, and if so, the Amazon Resource Name (ARN) of
        the user or identity that overrode the rules and their requirements for the
        pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_pull_request_override_state.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_pull_request_override_state)
        """

    def get_repository(
        self, **kwargs: Unpack[GetRepositoryInputTypeDef]
    ) -> GetRepositoryOutputTypeDef:
        """
        Returns information about a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_repository.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_repository)
        """

    def get_repository_triggers(
        self, **kwargs: Unpack[GetRepositoryTriggersInputTypeDef]
    ) -> GetRepositoryTriggersOutputTypeDef:
        """
        Gets information about triggers configured for a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_repository_triggers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_repository_triggers)
        """

    def list_approval_rule_templates(
        self, **kwargs: Unpack[ListApprovalRuleTemplatesInputTypeDef]
    ) -> ListApprovalRuleTemplatesOutputTypeDef:
        """
        Lists all approval rule templates in the specified Amazon Web Services Region
        in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/list_approval_rule_templates.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#list_approval_rule_templates)
        """

    def list_associated_approval_rule_templates_for_repository(
        self, **kwargs: Unpack[ListAssociatedApprovalRuleTemplatesForRepositoryInputTypeDef]
    ) -> ListAssociatedApprovalRuleTemplatesForRepositoryOutputTypeDef:
        """
        Lists all approval rule templates that are associated with a specified
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/list_associated_approval_rule_templates_for_repository.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#list_associated_approval_rule_templates_for_repository)
        """

    def list_branches(
        self, **kwargs: Unpack[ListBranchesInputTypeDef]
    ) -> ListBranchesOutputTypeDef:
        """
        Gets information about one or more branches in a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/list_branches.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#list_branches)
        """

    def list_file_commit_history(
        self, **kwargs: Unpack[ListFileCommitHistoryRequestTypeDef]
    ) -> ListFileCommitHistoryResponseTypeDef:
        """
        Retrieves a list of commits and changes to a specified file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/list_file_commit_history.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#list_file_commit_history)
        """

    def list_pull_requests(
        self, **kwargs: Unpack[ListPullRequestsInputTypeDef]
    ) -> ListPullRequestsOutputTypeDef:
        """
        Returns a list of pull requests for a specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/list_pull_requests.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#list_pull_requests)
        """

    def list_repositories(
        self, **kwargs: Unpack[ListRepositoriesInputTypeDef]
    ) -> ListRepositoriesOutputTypeDef:
        """
        Gets information about one or more repositories.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/list_repositories.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#list_repositories)
        """

    def list_repositories_for_approval_rule_template(
        self, **kwargs: Unpack[ListRepositoriesForApprovalRuleTemplateInputTypeDef]
    ) -> ListRepositoriesForApprovalRuleTemplateOutputTypeDef:
        """
        Lists all repositories associated with the specified approval rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/list_repositories_for_approval_rule_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#list_repositories_for_approval_rule_template)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Gets information about Amazon Web Servicestags for a specified Amazon Resource
        Name (ARN) in CodeCommit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#list_tags_for_resource)
        """

    def merge_branches_by_fast_forward(
        self, **kwargs: Unpack[MergeBranchesByFastForwardInputTypeDef]
    ) -> MergeBranchesByFastForwardOutputTypeDef:
        """
        Merges two branches using the fast-forward merge strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/merge_branches_by_fast_forward.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#merge_branches_by_fast_forward)
        """

    def merge_branches_by_squash(
        self, **kwargs: Unpack[MergeBranchesBySquashInputTypeDef]
    ) -> MergeBranchesBySquashOutputTypeDef:
        """
        Merges two branches using the squash merge strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/merge_branches_by_squash.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#merge_branches_by_squash)
        """

    def merge_branches_by_three_way(
        self, **kwargs: Unpack[MergeBranchesByThreeWayInputTypeDef]
    ) -> MergeBranchesByThreeWayOutputTypeDef:
        """
        Merges two specified branches using the three-way merge strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/merge_branches_by_three_way.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#merge_branches_by_three_way)
        """

    def merge_pull_request_by_fast_forward(
        self, **kwargs: Unpack[MergePullRequestByFastForwardInputTypeDef]
    ) -> MergePullRequestByFastForwardOutputTypeDef:
        """
        Attempts to merge the source commit of a pull request into the specified
        destination branch for that pull request at the specified commit using the
        fast-forward merge strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/merge_pull_request_by_fast_forward.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#merge_pull_request_by_fast_forward)
        """

    def merge_pull_request_by_squash(
        self, **kwargs: Unpack[MergePullRequestBySquashInputTypeDef]
    ) -> MergePullRequestBySquashOutputTypeDef:
        """
        Attempts to merge the source commit of a pull request into the specified
        destination branch for that pull request at the specified commit using the
        squash merge strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/merge_pull_request_by_squash.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#merge_pull_request_by_squash)
        """

    def merge_pull_request_by_three_way(
        self, **kwargs: Unpack[MergePullRequestByThreeWayInputTypeDef]
    ) -> MergePullRequestByThreeWayOutputTypeDef:
        """
        Attempts to merge the source commit of a pull request into the specified
        destination branch for that pull request at the specified commit using the
        three-way merge strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/merge_pull_request_by_three_way.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#merge_pull_request_by_three_way)
        """

    def override_pull_request_approval_rules(
        self, **kwargs: Unpack[OverridePullRequestApprovalRulesInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets aside (overrides) all approval rule requirements for a specified pull
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/override_pull_request_approval_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#override_pull_request_approval_rules)
        """

    def post_comment_for_compared_commit(
        self, **kwargs: Unpack[PostCommentForComparedCommitInputTypeDef]
    ) -> PostCommentForComparedCommitOutputTypeDef:
        """
        Posts a comment on the comparison between two commits.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/post_comment_for_compared_commit.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#post_comment_for_compared_commit)
        """

    def post_comment_for_pull_request(
        self, **kwargs: Unpack[PostCommentForPullRequestInputTypeDef]
    ) -> PostCommentForPullRequestOutputTypeDef:
        """
        Posts a comment on a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/post_comment_for_pull_request.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#post_comment_for_pull_request)
        """

    def post_comment_reply(
        self, **kwargs: Unpack[PostCommentReplyInputTypeDef]
    ) -> PostCommentReplyOutputTypeDef:
        """
        Posts a comment in reply to an existing comment on a comparison between commits
        or a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/post_comment_reply.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#post_comment_reply)
        """

    def put_comment_reaction(
        self, **kwargs: Unpack[PutCommentReactionInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or updates a reaction to a specified comment for the user whose identity
        is used to make the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/put_comment_reaction.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#put_comment_reaction)
        """

    def put_file(self, **kwargs: Unpack[PutFileInputTypeDef]) -> PutFileOutputTypeDef:
        """
        Adds or updates a file in a branch in an CodeCommit repository, and generates a
        commit for the addition in the specified branch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/put_file.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#put_file)
        """

    def put_repository_triggers(
        self, **kwargs: Unpack[PutRepositoryTriggersInputTypeDef]
    ) -> PutRepositoryTriggersOutputTypeDef:
        """
        Replaces all triggers for a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/put_repository_triggers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#put_repository_triggers)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or updates tags for a resource in CodeCommit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#tag_resource)
        """

    def test_repository_triggers(
        self, **kwargs: Unpack[TestRepositoryTriggersInputTypeDef]
    ) -> TestRepositoryTriggersOutputTypeDef:
        """
        Tests the functionality of repository triggers by sending information to the
        trigger target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/test_repository_triggers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#test_repository_triggers)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes tags for a resource in CodeCommit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#untag_resource)
        """

    def update_approval_rule_template_content(
        self, **kwargs: Unpack[UpdateApprovalRuleTemplateContentInputTypeDef]
    ) -> UpdateApprovalRuleTemplateContentOutputTypeDef:
        """
        Updates the content of an approval rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_approval_rule_template_content.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_approval_rule_template_content)
        """

    def update_approval_rule_template_description(
        self, **kwargs: Unpack[UpdateApprovalRuleTemplateDescriptionInputTypeDef]
    ) -> UpdateApprovalRuleTemplateDescriptionOutputTypeDef:
        """
        Updates the description for a specified approval rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_approval_rule_template_description.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_approval_rule_template_description)
        """

    def update_approval_rule_template_name(
        self, **kwargs: Unpack[UpdateApprovalRuleTemplateNameInputTypeDef]
    ) -> UpdateApprovalRuleTemplateNameOutputTypeDef:
        """
        Updates the name of a specified approval rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_approval_rule_template_name.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_approval_rule_template_name)
        """

    def update_comment(
        self, **kwargs: Unpack[UpdateCommentInputTypeDef]
    ) -> UpdateCommentOutputTypeDef:
        """
        Replaces the contents of a comment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_comment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_comment)
        """

    def update_default_branch(
        self, **kwargs: Unpack[UpdateDefaultBranchInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets or changes the default branch name for the specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_default_branch.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_default_branch)
        """

    def update_pull_request_approval_rule_content(
        self, **kwargs: Unpack[UpdatePullRequestApprovalRuleContentInputTypeDef]
    ) -> UpdatePullRequestApprovalRuleContentOutputTypeDef:
        """
        Updates the structure of an approval rule created specifically for a pull
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_pull_request_approval_rule_content.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_pull_request_approval_rule_content)
        """

    def update_pull_request_approval_state(
        self, **kwargs: Unpack[UpdatePullRequestApprovalStateInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the state of a user's approval on a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_pull_request_approval_state.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_pull_request_approval_state)
        """

    def update_pull_request_description(
        self, **kwargs: Unpack[UpdatePullRequestDescriptionInputTypeDef]
    ) -> UpdatePullRequestDescriptionOutputTypeDef:
        """
        Replaces the contents of the description of a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_pull_request_description.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_pull_request_description)
        """

    def update_pull_request_status(
        self, **kwargs: Unpack[UpdatePullRequestStatusInputTypeDef]
    ) -> UpdatePullRequestStatusOutputTypeDef:
        """
        Updates the status of a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_pull_request_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_pull_request_status)
        """

    def update_pull_request_title(
        self, **kwargs: Unpack[UpdatePullRequestTitleInputTypeDef]
    ) -> UpdatePullRequestTitleOutputTypeDef:
        """
        Replaces the title of a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_pull_request_title.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_pull_request_title)
        """

    def update_repository_description(
        self, **kwargs: Unpack[UpdateRepositoryDescriptionInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets or changes the comment or description for a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_repository_description.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_repository_description)
        """

    def update_repository_encryption_key(
        self, **kwargs: Unpack[UpdateRepositoryEncryptionKeyInputTypeDef]
    ) -> UpdateRepositoryEncryptionKeyOutputTypeDef:
        """
        Updates the Key Management Service encryption key used to encrypt and decrypt a
        CodeCommit repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_repository_encryption_key.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_repository_encryption_key)
        """

    def update_repository_name(
        self, **kwargs: Unpack[UpdateRepositoryNameInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Renames a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_repository_name.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_repository_name)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_pull_request_events"]
    ) -> DescribePullRequestEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_comments_for_compared_commit"]
    ) -> GetCommentsForComparedCommitPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_comments_for_pull_request"]
    ) -> GetCommentsForPullRequestPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_differences"]
    ) -> GetDifferencesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_branches"]
    ) -> ListBranchesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_pull_requests"]
    ) -> ListPullRequestsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_repositories"]
    ) -> ListRepositoriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_paginator)
        """
