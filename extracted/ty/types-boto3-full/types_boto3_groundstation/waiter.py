"""
Type annotations for groundstation service client waiters.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_groundstation/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_groundstation.client import GroundStationClient
    from types_boto3_groundstation.waiter import (
        ContactScheduledWaiter,
        ContactUpdatedWaiter,
    )

    session = Session()
    client: GroundStationClient = session.client("groundstation")

    contact_scheduled_waiter: ContactScheduledWaiter = client.get_waiter("contact_scheduled")
    contact_updated_waiter: ContactUpdatedWaiter = client.get_waiter("contact_updated")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import DescribeContactRequestWaitTypeDef, DescribeContactVersionRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ContactScheduledWaiter", "ContactUpdatedWaiter")


class ContactScheduledWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/waiter/ContactScheduled.html#GroundStation.Waiter.ContactScheduled)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_groundstation/waiters/#contactscheduledwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeContactRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/waiter/ContactScheduled.html#GroundStation.Waiter.ContactScheduled.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_groundstation/waiters/#contactscheduledwaiter)
        """


class ContactUpdatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/waiter/ContactUpdated.html#GroundStation.Waiter.ContactUpdated)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_groundstation/waiters/#contactupdatedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeContactVersionRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/waiter/ContactUpdated.html#GroundStation.Waiter.ContactUpdated.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_groundstation/waiters/#contactupdatedwaiter)
        """
