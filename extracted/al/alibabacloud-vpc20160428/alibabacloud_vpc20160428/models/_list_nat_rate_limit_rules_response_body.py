# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from alibabacloud_vpc20160428 import models as main_models
from darabonba.model import DaraModel

class ListNatRateLimitRulesResponseBody(DaraModel):
    def __init__(
        self,
        max_results: int = None,
        nat_gateway_id: str = None,
        next_token: str = None,
        request_id: str = None,
        rule_infos: List[main_models.ListNatRateLimitRulesResponseBodyRuleInfos] = None,
        total_count: int = None,
    ):
        # The maximum number of entries returned.
        self.max_results = max_results
        # The NAT gateway instance ID.
        self.nat_gateway_id = nat_gateway_id
        # The token that is used for the next query. Valid values:
        # - If **NextToken** is empty, no next query is to be sent.
        # - If **NextToken** is returned, the value indicates the token that is used for the next query.
        self.next_token = next_token
        # The request ID.
        self.request_id = request_id
        # The list of rate limiting rules.
        self.rule_infos = rule_infos
        # The total number of rate limiting rules returned.
        self.total_count = total_count

    def validate(self):
        if self.rule_infos:
            for v1 in self.rule_infos:
                 if v1:
                    v1.validate()

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.max_results is not None:
            result['MaxResults'] = self.max_results

        if self.nat_gateway_id is not None:
            result['NatGatewayId'] = self.nat_gateway_id

        if self.next_token is not None:
            result['NextToken'] = self.next_token

        if self.request_id is not None:
            result['RequestId'] = self.request_id

        result['RuleInfos'] = []
        if self.rule_infos is not None:
            for k1 in self.rule_infos:
                result['RuleInfos'].append(k1.to_map() if k1 else None)

        if self.total_count is not None:
            result['TotalCount'] = self.total_count

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')

        if m.get('NatGatewayId') is not None:
            self.nat_gateway_id = m.get('NatGatewayId')

        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')

        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')

        self.rule_infos = []
        if m.get('RuleInfos') is not None:
            for k1 in m.get('RuleInfos'):
                temp_model = main_models.ListNatRateLimitRulesResponseBodyRuleInfos()
                self.rule_infos.append(temp_model.from_map(k1))

        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')

        return self

class ListNatRateLimitRulesResponseBodyRuleInfos(DaraModel):
    def __init__(
        self,
        bandwidth_limit: str = None,
        match_type: str = None,
        rule_description: str = None,
        rule_id: str = None,
        rule_name: str = None,
        source_cidrs: List[str] = None,
        status: str = None,
        tunnel_index: str = None,
    ):
        # The bandwidth limit. Unit: Mbit/s.
        self.bandwidth_limit = bandwidth_limit
        # The source match type of the rate limiting rule. Valid values:
        # 
        # - **CIDR**: CIDR block match. This is the default value.
        # - **TUNNEL**: tunnel match. If this value is specified, a corresponding SNAT rule of the TUNNEL type must exist.
        self.match_type = match_type
        # The description of the rate limiting rule.
        self.rule_description = rule_description
        # The ID of the rate limiting rule.
        self.rule_id = rule_id
        # The name of the rate limiting rule.
        self.rule_name = rule_name
        # The source CIDR blocks of the rate limiting rule.
        self.source_cidrs = source_cidrs
        # The status of the rate limiting rule. Valid values:
        # - **Created**: The rule is available.
        # - **Deleting**: The rule is being deleted.
        # - **Modifying**: The rule is being modified.
        self.status = status
        # The tunnel index. If the MatchType parameter is set to TUNNEL, a corresponding SNAT rule must exist.
        self.tunnel_index = tunnel_index

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.bandwidth_limit is not None:
            result['BandwidthLimit'] = self.bandwidth_limit

        if self.match_type is not None:
            result['MatchType'] = self.match_type

        if self.rule_description is not None:
            result['RuleDescription'] = self.rule_description

        if self.rule_id is not None:
            result['RuleId'] = self.rule_id

        if self.rule_name is not None:
            result['RuleName'] = self.rule_name

        if self.source_cidrs is not None:
            result['SourceCIDRs'] = self.source_cidrs

        if self.status is not None:
            result['Status'] = self.status

        if self.tunnel_index is not None:
            result['TunnelIndex'] = self.tunnel_index

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BandwidthLimit') is not None:
            self.bandwidth_limit = m.get('BandwidthLimit')

        if m.get('MatchType') is not None:
            self.match_type = m.get('MatchType')

        if m.get('RuleDescription') is not None:
            self.rule_description = m.get('RuleDescription')

        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')

        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')

        if m.get('SourceCIDRs') is not None:
            self.source_cidrs = m.get('SourceCIDRs')

        if m.get('Status') is not None:
            self.status = m.get('Status')

        if m.get('TunnelIndex') is not None:
            self.tunnel_index = m.get('TunnelIndex')

        return self

