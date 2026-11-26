# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class CreateDBInstancePlanRequest(DaraModel):
    def __init__(
        self,
        dbinstance_id: str = None,
        owner_id: int = None,
        plan_config: str = None,
        plan_desc: str = None,
        plan_end_date: str = None,
        plan_name: str = None,
        plan_schedule_type: str = None,
        plan_start_date: str = None,
        plan_type: str = None,
    ):
        # The instance ID.
        # 
        # > You can call the [DescribeDBInstances](https://help.aliyun.com/document_detail/86911.html) operation to query the IDs of all AnalyticDB for PostgreSQL instances in a specific region.
        # 
        # This parameter is required.
        self.dbinstance_id = dbinstance_id
        self.owner_id = owner_id
        # The detailed information about the execution plan. The value must be in JSON format. The content must be adjusted based on the values of the **PlanType** and **PlanScheduleType** parameters. For more information, see the following supplementary instructions.
        # 
        # This parameter is required.
        self.plan_config = plan_config
        # The description of the plan.
        self.plan_desc = plan_desc
        # The end time of the plan. The end time must be later than the start time. Specify the time in the <i>yyyy-MM-dd</i>T<i>HH:mm:ss</i>Z format. The time must be in UTC.
        # 
        # > - This parameter is required only when **PlanScheduleType** is set to **Regular**.
        # > - This parameter is optional. If you do not specify an end time, the plan stops when the cycle ends.
        self.plan_end_date = plan_end_date
        # The name of the plan.
        # 
        # This parameter is required.
        self.plan_name = plan_name
        # The execution mode of the plan. Valid values:
        # 
        # - **Postpone**: execute later.
        # - **Regular**: periodic execution.
        # 
        # This parameter is required.
        self.plan_schedule_type = plan_schedule_type
        # The start time of the plan. Specify the time in the <i>yyyy-MM-dd</i>T<i>HH:mm:ss</i>Z format. The time must be in UTC.
        # 
        # > - This parameter is required only when **PlanScheduleType** is set to **Regular**.
        # > - If you do not specify this parameter, the current time is used by default.
        self.plan_start_date = plan_start_date
        # The type of the plan. Valid values:
        # 
        # - **PauseResume**: automatic start and stop.
        # - **Resize**: instance upgrade/downgrade, which increases or decreases the number of compute nodes.
        # - **ModifySpec**: specification change, which changes the node specifications.
        # - **InPlaceModifySpec**: in-place elastic scaling, which scales the compute resources on the local node without changing the base specifications.
        # 
        # > - Instance upgrade/downgrade is supported only for instances in Serverless mode.
        # > - Specification changes are supported only for instances in elastic storage mode.
        # > - In-place elastic scaling is supported only for high availability (HA) instances in elastic storage mode.
        # 
        # This parameter is required.
        self.plan_type = plan_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.dbinstance_id is not None:
            result['DBInstanceId'] = self.dbinstance_id

        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id

        if self.plan_config is not None:
            result['PlanConfig'] = self.plan_config

        if self.plan_desc is not None:
            result['PlanDesc'] = self.plan_desc

        if self.plan_end_date is not None:
            result['PlanEndDate'] = self.plan_end_date

        if self.plan_name is not None:
            result['PlanName'] = self.plan_name

        if self.plan_schedule_type is not None:
            result['PlanScheduleType'] = self.plan_schedule_type

        if self.plan_start_date is not None:
            result['PlanStartDate'] = self.plan_start_date

        if self.plan_type is not None:
            result['PlanType'] = self.plan_type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')

        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')

        if m.get('PlanConfig') is not None:
            self.plan_config = m.get('PlanConfig')

        if m.get('PlanDesc') is not None:
            self.plan_desc = m.get('PlanDesc')

        if m.get('PlanEndDate') is not None:
            self.plan_end_date = m.get('PlanEndDate')

        if m.get('PlanName') is not None:
            self.plan_name = m.get('PlanName')

        if m.get('PlanScheduleType') is not None:
            self.plan_schedule_type = m.get('PlanScheduleType')

        if m.get('PlanStartDate') is not None:
            self.plan_start_date = m.get('PlanStartDate')

        if m.get('PlanType') is not None:
            self.plan_type = m.get('PlanType')

        return self

