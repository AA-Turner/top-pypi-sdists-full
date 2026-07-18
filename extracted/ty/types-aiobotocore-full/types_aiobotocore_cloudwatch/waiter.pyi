"""
Type annotations for cloudwatch service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudwatch.client import CloudWatchClient
    from types_aiobotocore_cloudwatch.waiter import (
        AlarmExistsWaiter,
        AlarmMuteRuleExistsWaiter,
        CompositeAlarmExistsWaiter,
        LogAlarmExistsWaiter,
    )

    session = get_session()
    async with session.create_client("cloudwatch") as client:
        client: CloudWatchClient

        alarm_exists_waiter: AlarmExistsWaiter = client.get_waiter("alarm_exists")
        alarm_mute_rule_exists_waiter: AlarmMuteRuleExistsWaiter = client.get_waiter("alarm_mute_rule_exists")
        composite_alarm_exists_waiter: CompositeAlarmExistsWaiter = client.get_waiter("composite_alarm_exists")
        log_alarm_exists_waiter: LogAlarmExistsWaiter = client.get_waiter("log_alarm_exists")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeAlarmsInputWaitExtraExtraTypeDef,
    DescribeAlarmsInputWaitExtraTypeDef,
    DescribeAlarmsInputWaitTypeDef,
    GetAlarmMuteRuleInputWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "AlarmExistsWaiter",
    "AlarmMuteRuleExistsWaiter",
    "CompositeAlarmExistsWaiter",
    "LogAlarmExistsWaiter",
)

class AlarmExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/waiter/AlarmExists.html#CloudWatch.Waiter.AlarmExists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/waiters/#alarmexistswaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAlarmsInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/waiter/AlarmExists.html#CloudWatch.Waiter.AlarmExists.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/waiters/#alarmexistswaiter)
        """

class AlarmMuteRuleExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/waiter/AlarmMuteRuleExists.html#CloudWatch.Waiter.AlarmMuteRuleExists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/waiters/#alarmmuteruleexistswaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetAlarmMuteRuleInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/waiter/AlarmMuteRuleExists.html#CloudWatch.Waiter.AlarmMuteRuleExists.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/waiters/#alarmmuteruleexistswaiter)
        """

class CompositeAlarmExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/waiter/CompositeAlarmExists.html#CloudWatch.Waiter.CompositeAlarmExists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/waiters/#compositealarmexistswaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAlarmsInputWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/waiter/CompositeAlarmExists.html#CloudWatch.Waiter.CompositeAlarmExists.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/waiters/#compositealarmexistswaiter)
        """

class LogAlarmExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/waiter/LogAlarmExists.html#CloudWatch.Waiter.LogAlarmExists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/waiters/#logalarmexistswaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAlarmsInputWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/waiter/LogAlarmExists.html#CloudWatch.Waiter.LogAlarmExists.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/waiters/#logalarmexistswaiter)
        """
