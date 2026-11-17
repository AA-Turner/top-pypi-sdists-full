"""
Type annotations for wellarchitected service client waiters.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_wellarchitected/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_wellarchitected.client import WellArchitectedClient
    from types_boto3_wellarchitected.waiter import (
        AgentOrganizationalReportCompletedWaiter,
    )

    session = Session()
    client: WellArchitectedClient = session.client("wellarchitected")

    agent_organizational_report_completed_waiter: AgentOrganizationalReportCompletedWaiter = client.get_waiter("agent_organizational_report_completed")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import GetAgentOrganizationalReportRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("AgentOrganizationalReportCompletedWaiter",)

class AgentOrganizationalReportCompletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/waiter/AgentOrganizationalReportCompleted.html#WellArchitected.Waiter.AgentOrganizationalReportCompleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_wellarchitected/waiters/#agentorganizationalreportcompletedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetAgentOrganizationalReportRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/waiter/AgentOrganizationalReportCompleted.html#WellArchitected.Waiter.AgentOrganizationalReportCompleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_wellarchitected/waiters/#agentorganizationalreportcompletedwaiter)
        """
