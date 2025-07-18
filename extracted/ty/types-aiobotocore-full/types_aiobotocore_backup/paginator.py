"""
Type annotations for backup service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_backup.client import BackupClient
    from types_aiobotocore_backup.paginator import (
        ListBackupJobsPaginator,
        ListBackupPlanTemplatesPaginator,
        ListBackupPlanVersionsPaginator,
        ListBackupPlansPaginator,
        ListBackupSelectionsPaginator,
        ListBackupVaultsPaginator,
        ListCopyJobsPaginator,
        ListIndexedRecoveryPointsPaginator,
        ListLegalHoldsPaginator,
        ListProtectedResourcesByBackupVaultPaginator,
        ListProtectedResourcesPaginator,
        ListRecoveryPointsByBackupVaultPaginator,
        ListRecoveryPointsByLegalHoldPaginator,
        ListRecoveryPointsByResourcePaginator,
        ListRestoreAccessBackupVaultsPaginator,
        ListRestoreJobsByProtectedResourcePaginator,
        ListRestoreJobsPaginator,
        ListRestoreTestingPlansPaginator,
        ListRestoreTestingSelectionsPaginator,
    )

    session = get_session()
    with session.create_client("backup") as client:
        client: BackupClient

        list_backup_jobs_paginator: ListBackupJobsPaginator = client.get_paginator("list_backup_jobs")
        list_backup_plan_templates_paginator: ListBackupPlanTemplatesPaginator = client.get_paginator("list_backup_plan_templates")
        list_backup_plan_versions_paginator: ListBackupPlanVersionsPaginator = client.get_paginator("list_backup_plan_versions")
        list_backup_plans_paginator: ListBackupPlansPaginator = client.get_paginator("list_backup_plans")
        list_backup_selections_paginator: ListBackupSelectionsPaginator = client.get_paginator("list_backup_selections")
        list_backup_vaults_paginator: ListBackupVaultsPaginator = client.get_paginator("list_backup_vaults")
        list_copy_jobs_paginator: ListCopyJobsPaginator = client.get_paginator("list_copy_jobs")
        list_indexed_recovery_points_paginator: ListIndexedRecoveryPointsPaginator = client.get_paginator("list_indexed_recovery_points")
        list_legal_holds_paginator: ListLegalHoldsPaginator = client.get_paginator("list_legal_holds")
        list_protected_resources_by_backup_vault_paginator: ListProtectedResourcesByBackupVaultPaginator = client.get_paginator("list_protected_resources_by_backup_vault")
        list_protected_resources_paginator: ListProtectedResourcesPaginator = client.get_paginator("list_protected_resources")
        list_recovery_points_by_backup_vault_paginator: ListRecoveryPointsByBackupVaultPaginator = client.get_paginator("list_recovery_points_by_backup_vault")
        list_recovery_points_by_legal_hold_paginator: ListRecoveryPointsByLegalHoldPaginator = client.get_paginator("list_recovery_points_by_legal_hold")
        list_recovery_points_by_resource_paginator: ListRecoveryPointsByResourcePaginator = client.get_paginator("list_recovery_points_by_resource")
        list_restore_access_backup_vaults_paginator: ListRestoreAccessBackupVaultsPaginator = client.get_paginator("list_restore_access_backup_vaults")
        list_restore_jobs_by_protected_resource_paginator: ListRestoreJobsByProtectedResourcePaginator = client.get_paginator("list_restore_jobs_by_protected_resource")
        list_restore_jobs_paginator: ListRestoreJobsPaginator = client.get_paginator("list_restore_jobs")
        list_restore_testing_plans_paginator: ListRestoreTestingPlansPaginator = client.get_paginator("list_restore_testing_plans")
        list_restore_testing_selections_paginator: ListRestoreTestingSelectionsPaginator = client.get_paginator("list_restore_testing_selections")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListBackupJobsInputPaginateTypeDef,
    ListBackupJobsOutputTypeDef,
    ListBackupPlansInputPaginateTypeDef,
    ListBackupPlansOutputTypeDef,
    ListBackupPlanTemplatesInputPaginateTypeDef,
    ListBackupPlanTemplatesOutputTypeDef,
    ListBackupPlanVersionsInputPaginateTypeDef,
    ListBackupPlanVersionsOutputTypeDef,
    ListBackupSelectionsInputPaginateTypeDef,
    ListBackupSelectionsOutputTypeDef,
    ListBackupVaultsInputPaginateTypeDef,
    ListBackupVaultsOutputTypeDef,
    ListCopyJobsInputPaginateTypeDef,
    ListCopyJobsOutputTypeDef,
    ListIndexedRecoveryPointsInputPaginateTypeDef,
    ListIndexedRecoveryPointsOutputTypeDef,
    ListLegalHoldsInputPaginateTypeDef,
    ListLegalHoldsOutputTypeDef,
    ListProtectedResourcesByBackupVaultInputPaginateTypeDef,
    ListProtectedResourcesByBackupVaultOutputTypeDef,
    ListProtectedResourcesInputPaginateTypeDef,
    ListProtectedResourcesOutputTypeDef,
    ListRecoveryPointsByBackupVaultInputPaginateTypeDef,
    ListRecoveryPointsByBackupVaultOutputTypeDef,
    ListRecoveryPointsByLegalHoldInputPaginateTypeDef,
    ListRecoveryPointsByLegalHoldOutputTypeDef,
    ListRecoveryPointsByResourceInputPaginateTypeDef,
    ListRecoveryPointsByResourceOutputTypeDef,
    ListRestoreAccessBackupVaultsInputPaginateTypeDef,
    ListRestoreAccessBackupVaultsOutputTypeDef,
    ListRestoreJobsByProtectedResourceInputPaginateTypeDef,
    ListRestoreJobsByProtectedResourceOutputTypeDef,
    ListRestoreJobsInputPaginateTypeDef,
    ListRestoreJobsOutputTypeDef,
    ListRestoreTestingPlansInputPaginateTypeDef,
    ListRestoreTestingPlansOutputTypeDef,
    ListRestoreTestingSelectionsInputPaginateTypeDef,
    ListRestoreTestingSelectionsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListBackupJobsPaginator",
    "ListBackupPlanTemplatesPaginator",
    "ListBackupPlanVersionsPaginator",
    "ListBackupPlansPaginator",
    "ListBackupSelectionsPaginator",
    "ListBackupVaultsPaginator",
    "ListCopyJobsPaginator",
    "ListIndexedRecoveryPointsPaginator",
    "ListLegalHoldsPaginator",
    "ListProtectedResourcesByBackupVaultPaginator",
    "ListProtectedResourcesPaginator",
    "ListRecoveryPointsByBackupVaultPaginator",
    "ListRecoveryPointsByLegalHoldPaginator",
    "ListRecoveryPointsByResourcePaginator",
    "ListRestoreAccessBackupVaultsPaginator",
    "ListRestoreJobsByProtectedResourcePaginator",
    "ListRestoreJobsPaginator",
    "ListRestoreTestingPlansPaginator",
    "ListRestoreTestingSelectionsPaginator",
)


if TYPE_CHECKING:
    _ListBackupJobsPaginatorBase = AioPaginator[ListBackupJobsOutputTypeDef]
else:
    _ListBackupJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBackupJobsPaginator(_ListBackupJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupJobs.html#Backup.Paginator.ListBackupJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listbackupjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBackupJobsInputPaginateTypeDef]
    ) -> AioPageIterator[ListBackupJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupJobs.html#Backup.Paginator.ListBackupJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listbackupjobspaginator)
        """


if TYPE_CHECKING:
    _ListBackupPlanTemplatesPaginatorBase = AioPaginator[ListBackupPlanTemplatesOutputTypeDef]
else:
    _ListBackupPlanTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBackupPlanTemplatesPaginator(_ListBackupPlanTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupPlanTemplates.html#Backup.Paginator.ListBackupPlanTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listbackupplantemplatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBackupPlanTemplatesInputPaginateTypeDef]
    ) -> AioPageIterator[ListBackupPlanTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupPlanTemplates.html#Backup.Paginator.ListBackupPlanTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listbackupplantemplatespaginator)
        """


if TYPE_CHECKING:
    _ListBackupPlanVersionsPaginatorBase = AioPaginator[ListBackupPlanVersionsOutputTypeDef]
else:
    _ListBackupPlanVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBackupPlanVersionsPaginator(_ListBackupPlanVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupPlanVersions.html#Backup.Paginator.ListBackupPlanVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listbackupplanversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBackupPlanVersionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListBackupPlanVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupPlanVersions.html#Backup.Paginator.ListBackupPlanVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listbackupplanversionspaginator)
        """


if TYPE_CHECKING:
    _ListBackupPlansPaginatorBase = AioPaginator[ListBackupPlansOutputTypeDef]
else:
    _ListBackupPlansPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBackupPlansPaginator(_ListBackupPlansPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupPlans.html#Backup.Paginator.ListBackupPlans)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listbackupplanspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBackupPlansInputPaginateTypeDef]
    ) -> AioPageIterator[ListBackupPlansOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupPlans.html#Backup.Paginator.ListBackupPlans.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listbackupplanspaginator)
        """


if TYPE_CHECKING:
    _ListBackupSelectionsPaginatorBase = AioPaginator[ListBackupSelectionsOutputTypeDef]
else:
    _ListBackupSelectionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBackupSelectionsPaginator(_ListBackupSelectionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupSelections.html#Backup.Paginator.ListBackupSelections)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listbackupselectionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBackupSelectionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListBackupSelectionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupSelections.html#Backup.Paginator.ListBackupSelections.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listbackupselectionspaginator)
        """


if TYPE_CHECKING:
    _ListBackupVaultsPaginatorBase = AioPaginator[ListBackupVaultsOutputTypeDef]
else:
    _ListBackupVaultsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBackupVaultsPaginator(_ListBackupVaultsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupVaults.html#Backup.Paginator.ListBackupVaults)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listbackupvaultspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBackupVaultsInputPaginateTypeDef]
    ) -> AioPageIterator[ListBackupVaultsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListBackupVaults.html#Backup.Paginator.ListBackupVaults.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listbackupvaultspaginator)
        """


if TYPE_CHECKING:
    _ListCopyJobsPaginatorBase = AioPaginator[ListCopyJobsOutputTypeDef]
else:
    _ListCopyJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCopyJobsPaginator(_ListCopyJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListCopyJobs.html#Backup.Paginator.ListCopyJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listcopyjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCopyJobsInputPaginateTypeDef]
    ) -> AioPageIterator[ListCopyJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListCopyJobs.html#Backup.Paginator.ListCopyJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listcopyjobspaginator)
        """


if TYPE_CHECKING:
    _ListIndexedRecoveryPointsPaginatorBase = AioPaginator[ListIndexedRecoveryPointsOutputTypeDef]
else:
    _ListIndexedRecoveryPointsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListIndexedRecoveryPointsPaginator(_ListIndexedRecoveryPointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListIndexedRecoveryPoints.html#Backup.Paginator.ListIndexedRecoveryPoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listindexedrecoverypointspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIndexedRecoveryPointsInputPaginateTypeDef]
    ) -> AioPageIterator[ListIndexedRecoveryPointsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListIndexedRecoveryPoints.html#Backup.Paginator.ListIndexedRecoveryPoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listindexedrecoverypointspaginator)
        """


if TYPE_CHECKING:
    _ListLegalHoldsPaginatorBase = AioPaginator[ListLegalHoldsOutputTypeDef]
else:
    _ListLegalHoldsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListLegalHoldsPaginator(_ListLegalHoldsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListLegalHolds.html#Backup.Paginator.ListLegalHolds)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listlegalholdspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLegalHoldsInputPaginateTypeDef]
    ) -> AioPageIterator[ListLegalHoldsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListLegalHolds.html#Backup.Paginator.ListLegalHolds.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listlegalholdspaginator)
        """


if TYPE_CHECKING:
    _ListProtectedResourcesByBackupVaultPaginatorBase = AioPaginator[
        ListProtectedResourcesByBackupVaultOutputTypeDef
    ]
else:
    _ListProtectedResourcesByBackupVaultPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListProtectedResourcesByBackupVaultPaginator(
    _ListProtectedResourcesByBackupVaultPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListProtectedResourcesByBackupVault.html#Backup.Paginator.ListProtectedResourcesByBackupVault)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listprotectedresourcesbybackupvaultpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProtectedResourcesByBackupVaultInputPaginateTypeDef]
    ) -> AioPageIterator[ListProtectedResourcesByBackupVaultOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListProtectedResourcesByBackupVault.html#Backup.Paginator.ListProtectedResourcesByBackupVault.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listprotectedresourcesbybackupvaultpaginator)
        """


if TYPE_CHECKING:
    _ListProtectedResourcesPaginatorBase = AioPaginator[ListProtectedResourcesOutputTypeDef]
else:
    _ListProtectedResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListProtectedResourcesPaginator(_ListProtectedResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListProtectedResources.html#Backup.Paginator.ListProtectedResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listprotectedresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProtectedResourcesInputPaginateTypeDef]
    ) -> AioPageIterator[ListProtectedResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListProtectedResources.html#Backup.Paginator.ListProtectedResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listprotectedresourcespaginator)
        """


if TYPE_CHECKING:
    _ListRecoveryPointsByBackupVaultPaginatorBase = AioPaginator[
        ListRecoveryPointsByBackupVaultOutputTypeDef
    ]
else:
    _ListRecoveryPointsByBackupVaultPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRecoveryPointsByBackupVaultPaginator(_ListRecoveryPointsByBackupVaultPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRecoveryPointsByBackupVault.html#Backup.Paginator.ListRecoveryPointsByBackupVault)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listrecoverypointsbybackupvaultpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRecoveryPointsByBackupVaultInputPaginateTypeDef]
    ) -> AioPageIterator[ListRecoveryPointsByBackupVaultOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRecoveryPointsByBackupVault.html#Backup.Paginator.ListRecoveryPointsByBackupVault.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listrecoverypointsbybackupvaultpaginator)
        """


if TYPE_CHECKING:
    _ListRecoveryPointsByLegalHoldPaginatorBase = AioPaginator[
        ListRecoveryPointsByLegalHoldOutputTypeDef
    ]
else:
    _ListRecoveryPointsByLegalHoldPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRecoveryPointsByLegalHoldPaginator(_ListRecoveryPointsByLegalHoldPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRecoveryPointsByLegalHold.html#Backup.Paginator.ListRecoveryPointsByLegalHold)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listrecoverypointsbylegalholdpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRecoveryPointsByLegalHoldInputPaginateTypeDef]
    ) -> AioPageIterator[ListRecoveryPointsByLegalHoldOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRecoveryPointsByLegalHold.html#Backup.Paginator.ListRecoveryPointsByLegalHold.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listrecoverypointsbylegalholdpaginator)
        """


if TYPE_CHECKING:
    _ListRecoveryPointsByResourcePaginatorBase = AioPaginator[
        ListRecoveryPointsByResourceOutputTypeDef
    ]
else:
    _ListRecoveryPointsByResourcePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRecoveryPointsByResourcePaginator(_ListRecoveryPointsByResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRecoveryPointsByResource.html#Backup.Paginator.ListRecoveryPointsByResource)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listrecoverypointsbyresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRecoveryPointsByResourceInputPaginateTypeDef]
    ) -> AioPageIterator[ListRecoveryPointsByResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRecoveryPointsByResource.html#Backup.Paginator.ListRecoveryPointsByResource.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listrecoverypointsbyresourcepaginator)
        """


if TYPE_CHECKING:
    _ListRestoreAccessBackupVaultsPaginatorBase = AioPaginator[
        ListRestoreAccessBackupVaultsOutputTypeDef
    ]
else:
    _ListRestoreAccessBackupVaultsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRestoreAccessBackupVaultsPaginator(_ListRestoreAccessBackupVaultsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRestoreAccessBackupVaults.html#Backup.Paginator.ListRestoreAccessBackupVaults)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listrestoreaccessbackupvaultspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRestoreAccessBackupVaultsInputPaginateTypeDef]
    ) -> AioPageIterator[ListRestoreAccessBackupVaultsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRestoreAccessBackupVaults.html#Backup.Paginator.ListRestoreAccessBackupVaults.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listrestoreaccessbackupvaultspaginator)
        """


if TYPE_CHECKING:
    _ListRestoreJobsByProtectedResourcePaginatorBase = AioPaginator[
        ListRestoreJobsByProtectedResourceOutputTypeDef
    ]
else:
    _ListRestoreJobsByProtectedResourcePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRestoreJobsByProtectedResourcePaginator(_ListRestoreJobsByProtectedResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRestoreJobsByProtectedResource.html#Backup.Paginator.ListRestoreJobsByProtectedResource)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listrestorejobsbyprotectedresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRestoreJobsByProtectedResourceInputPaginateTypeDef]
    ) -> AioPageIterator[ListRestoreJobsByProtectedResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRestoreJobsByProtectedResource.html#Backup.Paginator.ListRestoreJobsByProtectedResource.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listrestorejobsbyprotectedresourcepaginator)
        """


if TYPE_CHECKING:
    _ListRestoreJobsPaginatorBase = AioPaginator[ListRestoreJobsOutputTypeDef]
else:
    _ListRestoreJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRestoreJobsPaginator(_ListRestoreJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRestoreJobs.html#Backup.Paginator.ListRestoreJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listrestorejobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRestoreJobsInputPaginateTypeDef]
    ) -> AioPageIterator[ListRestoreJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRestoreJobs.html#Backup.Paginator.ListRestoreJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listrestorejobspaginator)
        """


if TYPE_CHECKING:
    _ListRestoreTestingPlansPaginatorBase = AioPaginator[ListRestoreTestingPlansOutputTypeDef]
else:
    _ListRestoreTestingPlansPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRestoreTestingPlansPaginator(_ListRestoreTestingPlansPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRestoreTestingPlans.html#Backup.Paginator.ListRestoreTestingPlans)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listrestoretestingplanspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRestoreTestingPlansInputPaginateTypeDef]
    ) -> AioPageIterator[ListRestoreTestingPlansOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRestoreTestingPlans.html#Backup.Paginator.ListRestoreTestingPlans.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listrestoretestingplanspaginator)
        """


if TYPE_CHECKING:
    _ListRestoreTestingSelectionsPaginatorBase = AioPaginator[
        ListRestoreTestingSelectionsOutputTypeDef
    ]
else:
    _ListRestoreTestingSelectionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRestoreTestingSelectionsPaginator(_ListRestoreTestingSelectionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRestoreTestingSelections.html#Backup.Paginator.ListRestoreTestingSelections)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listrestoretestingselectionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRestoreTestingSelectionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListRestoreTestingSelectionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/paginator/ListRestoreTestingSelections.html#Backup.Paginator.ListRestoreTestingSelections.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/paginators/#listrestoretestingselectionspaginator)
        """
