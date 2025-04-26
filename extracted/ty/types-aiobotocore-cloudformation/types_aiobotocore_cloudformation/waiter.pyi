"""
Type annotations for cloudformation service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudformation.client import CloudFormationClient
    from types_aiobotocore_cloudformation.waiter import (
        ChangeSetCreateCompleteWaiter,
        StackCreateCompleteWaiter,
        StackDeleteCompleteWaiter,
        StackExistsWaiter,
        StackImportCompleteWaiter,
        StackRefactorCreateCompleteWaiter,
        StackRefactorExecuteCompleteWaiter,
        StackRollbackCompleteWaiter,
        StackUpdateCompleteWaiter,
        TypeRegistrationCompleteWaiter,
    )

    session = get_session()
    async with session.create_client("cloudformation") as client:
        client: CloudFormationClient

        change_set_create_complete_waiter: ChangeSetCreateCompleteWaiter = client.get_waiter("change_set_create_complete")
        stack_create_complete_waiter: StackCreateCompleteWaiter = client.get_waiter("stack_create_complete")
        stack_delete_complete_waiter: StackDeleteCompleteWaiter = client.get_waiter("stack_delete_complete")
        stack_exists_waiter: StackExistsWaiter = client.get_waiter("stack_exists")
        stack_import_complete_waiter: StackImportCompleteWaiter = client.get_waiter("stack_import_complete")
        stack_refactor_create_complete_waiter: StackRefactorCreateCompleteWaiter = client.get_waiter("stack_refactor_create_complete")
        stack_refactor_execute_complete_waiter: StackRefactorExecuteCompleteWaiter = client.get_waiter("stack_refactor_execute_complete")
        stack_rollback_complete_waiter: StackRollbackCompleteWaiter = client.get_waiter("stack_rollback_complete")
        stack_update_complete_waiter: StackUpdateCompleteWaiter = client.get_waiter("stack_update_complete")
        type_registration_complete_waiter: TypeRegistrationCompleteWaiter = client.get_waiter("type_registration_complete")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeChangeSetInputWaitTypeDef,
    DescribeStackRefactorInputWaitExtraTypeDef,
    DescribeStackRefactorInputWaitTypeDef,
    DescribeStacksInputWaitExtraExtraExtraExtraExtraTypeDef,
    DescribeStacksInputWaitExtraExtraExtraExtraTypeDef,
    DescribeStacksInputWaitExtraExtraExtraTypeDef,
    DescribeStacksInputWaitExtraExtraTypeDef,
    DescribeStacksInputWaitExtraTypeDef,
    DescribeStacksInputWaitTypeDef,
    DescribeTypeRegistrationInputWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ChangeSetCreateCompleteWaiter",
    "StackCreateCompleteWaiter",
    "StackDeleteCompleteWaiter",
    "StackExistsWaiter",
    "StackImportCompleteWaiter",
    "StackRefactorCreateCompleteWaiter",
    "StackRefactorExecuteCompleteWaiter",
    "StackRollbackCompleteWaiter",
    "StackUpdateCompleteWaiter",
    "TypeRegistrationCompleteWaiter",
)

class ChangeSetCreateCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/ChangeSetCreateComplete.html#CloudFormation.Waiter.ChangeSetCreateComplete)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#changesetcreatecompletewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeChangeSetInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/ChangeSetCreateComplete.html#CloudFormation.Waiter.ChangeSetCreateComplete.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#changesetcreatecompletewaiter)
        """

class StackCreateCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackCreateComplete.html#CloudFormation.Waiter.StackCreateComplete)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackcreatecompletewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeStacksInputWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackCreateComplete.html#CloudFormation.Waiter.StackCreateComplete.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackcreatecompletewaiter)
        """

class StackDeleteCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackDeleteComplete.html#CloudFormation.Waiter.StackDeleteComplete)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackdeletecompletewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeStacksInputWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackDeleteComplete.html#CloudFormation.Waiter.StackDeleteComplete.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackdeletecompletewaiter)
        """

class StackExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackExists.html#CloudFormation.Waiter.StackExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackexistswaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeStacksInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackExists.html#CloudFormation.Waiter.StackExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackexistswaiter)
        """

class StackImportCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackImportComplete.html#CloudFormation.Waiter.StackImportComplete)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackimportcompletewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeStacksInputWaitExtraExtraExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackImportComplete.html#CloudFormation.Waiter.StackImportComplete.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackimportcompletewaiter)
        """

class StackRefactorCreateCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackRefactorCreateComplete.html#CloudFormation.Waiter.StackRefactorCreateComplete)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackrefactorcreatecompletewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeStackRefactorInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackRefactorCreateComplete.html#CloudFormation.Waiter.StackRefactorCreateComplete.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackrefactorcreatecompletewaiter)
        """

class StackRefactorExecuteCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackRefactorExecuteComplete.html#CloudFormation.Waiter.StackRefactorExecuteComplete)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackrefactorexecutecompletewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeStackRefactorInputWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackRefactorExecuteComplete.html#CloudFormation.Waiter.StackRefactorExecuteComplete.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackrefactorexecutecompletewaiter)
        """

class StackRollbackCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackRollbackComplete.html#CloudFormation.Waiter.StackRollbackComplete)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackrollbackcompletewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeStacksInputWaitExtraExtraExtraExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackRollbackComplete.html#CloudFormation.Waiter.StackRollbackComplete.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackrollbackcompletewaiter)
        """

class StackUpdateCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackUpdateComplete.html#CloudFormation.Waiter.StackUpdateComplete)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackupdatecompletewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeStacksInputWaitExtraExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackUpdateComplete.html#CloudFormation.Waiter.StackUpdateComplete.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackupdatecompletewaiter)
        """

class TypeRegistrationCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/TypeRegistrationComplete.html#CloudFormation.Waiter.TypeRegistrationComplete)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#typeregistrationcompletewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTypeRegistrationInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/TypeRegistrationComplete.html#CloudFormation.Waiter.TypeRegistrationComplete.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#typeregistrationcompletewaiter)
        """
