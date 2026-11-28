# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from darabonba.model import DaraModel

class ListNatRateLimitRulesRequest(DaraModel):
    def __init__(
        self,
        client_token: str = None,
        max_results: int = None,
        nat_gateway_id: str = None,
        next_token: str = None,
        owner_id: int = None,
        region_id: str = None,
        rule_ids: List[str] = None,
        rule_name: str = None,
        source_cidr: str = None,
    ):
        # The client token that is used to ensure the idempotence of the request.
        # 
        # You can use the client to generate the value, and you must ensure that the value is unique among different requests. The client token can contain only ASCII characters.
        # 
        # > If you do not specify this parameter, the system automatically uses the **RequestId** of the API request as the **ClientToken**. The **RequestId** of each API request may be different.
        self.client_token = client_token
        # The number of entries to return on each page. Valid values: **1** to **100**. Default value: **20**.
        self.max_results = max_results
        # The ID of the NAT gateway.
        self.nat_gateway_id = nat_gateway_id
        # The token that is used for the next query. Valid values:
        # 
        # - If this is your first query or no next query is to be sent, ignore this parameter.
        # 
        # - If a next query is to be sent, set the value to the **NextToken** value returned from the last call.
        self.next_token = next_token
        self.owner_id = owner_id
        # The region ID of the NAT gateway.
        # 
        # You can call the [DescribeRegions](https://help.aliyun.com/document_detail/36063.html) operation to obtain the region ID.
        self.region_id = region_id
        # The IDs of the rate limiting rules.
        self.rule_ids = rule_ids
        # The name of the rate limiting rule.
        self.rule_name = rule_name
        # The source IP address CIDR block of the rate limiting rule.
        self.source_cidr = source_cidr

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.client_token is not None:
            result['ClientToken'] = self.client_token

        if self.max_results is not None:
            result['MaxResults'] = self.max_results

        if self.nat_gateway_id is not None:
            result['NatGatewayId'] = self.nat_gateway_id

        if self.next_token is not None:
            result['NextToken'] = self.next_token

        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id

        if self.region_id is not None:
            result['RegionId'] = self.region_id

        if self.rule_ids is not None:
            result['RuleIds'] = self.rule_ids

        if self.rule_name is not None:
            result['RuleName'] = self.rule_name

        if self.source_cidr is not None:
            result['SourceCIDR'] = self.source_cidr

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')

        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')

        if m.get('NatGatewayId') is not None:
            self.nat_gateway_id = m.get('NatGatewayId')

        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')

        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')

        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')

        if m.get('RuleIds') is not None:
            self.rule_ids = m.get('RuleIds')

        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')

        if m.get('SourceCIDR') is not None:
            self.source_cidr = m.get('SourceCIDR')

        return self

