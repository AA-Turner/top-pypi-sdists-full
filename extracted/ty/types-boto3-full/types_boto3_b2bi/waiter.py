"""
Type annotations for b2bi service client waiters.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_b2bi.client import B2BIClient
    from types_boto3_b2bi.waiter import (
        TransformerJobSucceededWaiter,
    )

    session = Session()
    client: B2BIClient = session.client("b2bi")

    transformer_job_succeeded_waiter: TransformerJobSucceededWaiter = client.get_waiter("transformer_job_succeeded")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import GetTransformerJobRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("TransformerJobSucceededWaiter",)


class TransformerJobSucceededWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/waiter/TransformerJobSucceeded.html#B2BI.Waiter.TransformerJobSucceeded)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/waiters/#transformerjobsucceededwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetTransformerJobRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/waiter/TransformerJobSucceeded.html#B2BI.Waiter.TransformerJobSucceeded.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/waiters/#transformerjobsucceededwaiter)
        """
