# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from darabonba.model import DaraModel

class CreateNatRateLimitRuleRequest(DaraModel):
    def __init__(
        self,
        bandwidth_limit: str = None,
        client_token: str = None,
        dry_run: str = None,
        match_type: str = None,
        nat_gateway_id: str = None,
        region_id: str = None,
        rule_description: str = None,
        rule_name: str = None,
        source_cidrs: List[str] = None,
        tunnel_index: str = None,
    ):
        # The bandwidth limit. Unit: Mbit/s.
        self.bandwidth_limit = bandwidth_limit
        # The client token that is used to ensure the idempotence of the request.
        # 
        # You can use the client to generate the value, but you must ensure that it is unique among different requests. The client token can contain only ASCII characters.
        # 
        # > If you do not specify this parameter, the system automatically uses the **RequestId** of the API request as the **ClientToken**. The **RequestId** of each API request is unique.
        self.client_token = client_token
        # Specifies whether to only precheck the request. Valid values:
        # 
        # - **true**: The system prechecks the request without creating the rate limiting rule. The system checks whether the required parameters are specified, and validates the request format and limits. If the request fails the precheck, the corresponding error is returned. If the request passes the precheck, the `DryRunOperation` error code is returned.
        # 
        # 
        # - **false** (default): The system sends a normal request. If the request passes the precheck, the rate limiting rule is created.
        self.dry_run = dry_run
        # The source match type for rate limiting. Valid values:
        # 
        # CIDR: CIDR block match. This is the default value.
        # TUNNEL: tunnel match. If you set the value to TUNNEL, a corresponding SNAT rule of the TUNNEL type must exist.
        self.match_type = match_type
        # The ID of the NAT gateway to which the rate limiting rule belongs.
        self.nat_gateway_id = nat_gateway_id
        # The region ID of the NAT gateway.
        # 
        # You can call the DescribeRegions operation to query region IDs.
        self.region_id = region_id
        # The description of the rate limiting rule.
        self.rule_description = rule_description
        # The name of the rate limiting rule.
        self.rule_name = rule_name
        # The list of source CIDR blocks to which the rate limiting rule applies.
        self.source_cidrs = source_cidrs
        # The tunnel index. If MatchType is set to TUNNEL, a corresponding SNAT rule must exist.
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

        if self.client_token is not None:
            result['ClientToken'] = self.client_token

        if self.dry_run is not None:
            result['DryRun'] = self.dry_run

        if self.match_type is not None:
            result['MatchType'] = self.match_type

        if self.nat_gateway_id is not None:
            result['NatGatewayId'] = self.nat_gateway_id

        if self.region_id is not None:
            result['RegionId'] = self.region_id

        if self.rule_description is not None:
            result['RuleDescription'] = self.rule_description

        if self.rule_name is not None:
            result['RuleName'] = self.rule_name

        if self.source_cidrs is not None:
            result['SourceCIDRs'] = self.source_cidrs

        if self.tunnel_index is not None:
            result['TunnelIndex'] = self.tunnel_index

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BandwidthLimit') is not None:
            self.bandwidth_limit = m.get('BandwidthLimit')

        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')

        if m.get('DryRun') is not None:
            self.dry_run = m.get('DryRun')

        if m.get('MatchType') is not None:
            self.match_type = m.get('MatchType')

        if m.get('NatGatewayId') is not None:
            self.nat_gateway_id = m.get('NatGatewayId')

        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')

        if m.get('RuleDescription') is not None:
            self.rule_description = m.get('RuleDescription')

        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')

        if m.get('SourceCIDRs') is not None:
            self.source_cidrs = m.get('SourceCIDRs')

        if m.get('TunnelIndex') is not None:
            self.tunnel_index = m.get('TunnelIndex')

        return self

