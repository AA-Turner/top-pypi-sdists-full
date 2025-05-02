"""
Type annotations for managedblockchain-query service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain_query/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_managedblockchain_query.client import ManagedBlockchainQueryClient
    from types_aiobotocore_managedblockchain_query.paginator import (
        ListAssetContractsPaginator,
        ListFilteredTransactionEventsPaginator,
        ListTokenBalancesPaginator,
        ListTransactionEventsPaginator,
        ListTransactionsPaginator,
    )

    session = get_session()
    with session.create_client("managedblockchain-query") as client:
        client: ManagedBlockchainQueryClient

        list_asset_contracts_paginator: ListAssetContractsPaginator = client.get_paginator("list_asset_contracts")
        list_filtered_transaction_events_paginator: ListFilteredTransactionEventsPaginator = client.get_paginator("list_filtered_transaction_events")
        list_token_balances_paginator: ListTokenBalancesPaginator = client.get_paginator("list_token_balances")
        list_transaction_events_paginator: ListTransactionEventsPaginator = client.get_paginator("list_transaction_events")
        list_transactions_paginator: ListTransactionsPaginator = client.get_paginator("list_transactions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAssetContractsInputPaginateTypeDef,
    ListAssetContractsOutputTypeDef,
    ListFilteredTransactionEventsInputPaginateTypeDef,
    ListFilteredTransactionEventsOutputTypeDef,
    ListTokenBalancesInputPaginateTypeDef,
    ListTokenBalancesOutputTypeDef,
    ListTransactionEventsInputPaginateTypeDef,
    ListTransactionEventsOutputTypeDef,
    ListTransactionsInputPaginateTypeDef,
    ListTransactionsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAssetContractsPaginator",
    "ListFilteredTransactionEventsPaginator",
    "ListTokenBalancesPaginator",
    "ListTransactionEventsPaginator",
    "ListTransactionsPaginator",
)


if TYPE_CHECKING:
    _ListAssetContractsPaginatorBase = AioPaginator[ListAssetContractsOutputTypeDef]
else:
    _ListAssetContractsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAssetContractsPaginator(_ListAssetContractsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListAssetContracts.html#ManagedBlockchainQuery.Paginator.ListAssetContracts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain_query/paginators/#listassetcontractspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssetContractsInputPaginateTypeDef]
    ) -> AioPageIterator[ListAssetContractsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListAssetContracts.html#ManagedBlockchainQuery.Paginator.ListAssetContracts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain_query/paginators/#listassetcontractspaginator)
        """


if TYPE_CHECKING:
    _ListFilteredTransactionEventsPaginatorBase = AioPaginator[
        ListFilteredTransactionEventsOutputTypeDef
    ]
else:
    _ListFilteredTransactionEventsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFilteredTransactionEventsPaginator(_ListFilteredTransactionEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListFilteredTransactionEvents.html#ManagedBlockchainQuery.Paginator.ListFilteredTransactionEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain_query/paginators/#listfilteredtransactioneventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFilteredTransactionEventsInputPaginateTypeDef]
    ) -> AioPageIterator[ListFilteredTransactionEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListFilteredTransactionEvents.html#ManagedBlockchainQuery.Paginator.ListFilteredTransactionEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain_query/paginators/#listfilteredtransactioneventspaginator)
        """


if TYPE_CHECKING:
    _ListTokenBalancesPaginatorBase = AioPaginator[ListTokenBalancesOutputTypeDef]
else:
    _ListTokenBalancesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTokenBalancesPaginator(_ListTokenBalancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListTokenBalances.html#ManagedBlockchainQuery.Paginator.ListTokenBalances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain_query/paginators/#listtokenbalancespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTokenBalancesInputPaginateTypeDef]
    ) -> AioPageIterator[ListTokenBalancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListTokenBalances.html#ManagedBlockchainQuery.Paginator.ListTokenBalances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain_query/paginators/#listtokenbalancespaginator)
        """


if TYPE_CHECKING:
    _ListTransactionEventsPaginatorBase = AioPaginator[ListTransactionEventsOutputTypeDef]
else:
    _ListTransactionEventsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTransactionEventsPaginator(_ListTransactionEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListTransactionEvents.html#ManagedBlockchainQuery.Paginator.ListTransactionEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain_query/paginators/#listtransactioneventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTransactionEventsInputPaginateTypeDef]
    ) -> AioPageIterator[ListTransactionEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListTransactionEvents.html#ManagedBlockchainQuery.Paginator.ListTransactionEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain_query/paginators/#listtransactioneventspaginator)
        """


if TYPE_CHECKING:
    _ListTransactionsPaginatorBase = AioPaginator[ListTransactionsOutputTypeDef]
else:
    _ListTransactionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTransactionsPaginator(_ListTransactionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListTransactions.html#ManagedBlockchainQuery.Paginator.ListTransactions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain_query/paginators/#listtransactionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTransactionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListTransactionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/paginator/ListTransactions.html#ManagedBlockchainQuery.Paginator.ListTransactions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain_query/paginators/#listtransactionspaginator)
        """
