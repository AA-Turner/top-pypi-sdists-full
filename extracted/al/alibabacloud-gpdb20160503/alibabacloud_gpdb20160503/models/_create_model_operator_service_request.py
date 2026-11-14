# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class CreateModelOperatorServiceRequest(DaraModel):
    def __init__(
        self,
        cu: int = None,
        pay_type: str = None,
        period: str = None,
        region_id: str = None,
        used_time: str = None,
    ):
        # The number of compute resource CUs for the model creation operator sub-service. The value must be an integer greater than 0. The available specifications and prices are subject to the actual sales configurations in the target region.
        # 
        # This parameter is required.
        self.cu = cu
        # The billing method. Valid values:
        # - PostPay: pay-as-you-go. This is the default value.
        # - PrePay: subscription. You must also specify UsedTime and Period.
        self.pay_type = pay_type
        # The unit of the subscription duration. This parameter is required when PayType is set to PrePay. Valid values: Month and Year. This parameter is used together with UsedTime and is not required for pay-as-you-go.
        self.period = period
        # The ID of the region to which the service belongs. This parameter is required and must be consistent with the request endpoint and the purchase region.
        # 
        # This parameter is required.
        self.region_id = region_id
        # The subscription duration. This parameter is required when PayType is set to PrePay. The value must be a positive integer string, and the unit is specified by Period. The actual available duration is subject to the sales configurations. This parameter is not required for pay-as-you-go.
        self.used_time = used_time

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.cu is not None:
            result['Cu'] = self.cu

        if self.pay_type is not None:
            result['PayType'] = self.pay_type

        if self.period is not None:
            result['Period'] = self.period

        if self.region_id is not None:
            result['RegionId'] = self.region_id

        if self.used_time is not None:
            result['UsedTime'] = self.used_time

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Cu') is not None:
            self.cu = m.get('Cu')

        if m.get('PayType') is not None:
            self.pay_type = m.get('PayType')

        if m.get('Period') is not None:
            self.period = m.get('Period')

        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')

        if m.get('UsedTime') is not None:
            self.used_time = m.get('UsedTime')

        return self

