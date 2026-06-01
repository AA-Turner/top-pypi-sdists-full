"""Tests for PR gamma.2 batch 5 mappings (v0.1.90) — WAF family.

Highest-impact batch in the gamma.2 series: 5 CFN types
(`AWS::WAFv2::WebACL`, `AWS::WAFv2::WebACLAssociation`,
`AWS::WAFv2::RuleGroup`, `AWS::WAF::WebACL`, `AWS::Shield::Protection`)
unlock 8 detectors (the whole WAF family + cna_dos_protection's
WAFv2 path).

WAFv2::WebACL is the structural workhorse: CFN's nested
`Rules: [{Action, OverrideAction, Statement: {GeoMatchStatement |
RateBasedStatement | ManagedRuleGroupStatement |
IPSetReferenceStatement | RuleGroupReferenceStatement}}]` translates
to TF's `rule = [{action, override_action, statement = [{<kind> = [{...}]}]}]`
with deep snake_case + list-wrapped-block transformation. Each
detector reads a specific Statement kind, so parity tests below
exercise each kind end-to-end.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.cloudformation import adapt_cfn_resources, apply_mapping, parse_cfn_file
from efterlev.detectors.aws.cna_dos_protection import detector as cna_dos_detector
from efterlev.detectors.aws.waf_action_types import detector as waf_action_detector
from efterlev.detectors.aws.waf_custom_rule_groups import detector as waf_custom_detector
from efterlev.detectors.aws.waf_geo_blocking import detector as waf_geo_detector
from efterlev.detectors.aws.waf_ip_set_blocking import detector as waf_ipset_detector
from efterlev.detectors.aws.waf_managed_rule_groups import detector as waf_managed_detector
from efterlev.detectors.aws.waf_rate_limiting import detector as waf_rate_detector
from efterlev.detectors.aws.waf_rule_count import detector as waf_count_detector

# --- AWS::WAFv2::WebACL — basic shape -------------------------------------


def test_wafv2_web_acl_basic_translation() -> None:
    """Top-level Name/Scope/DefaultAction translate; tf_type override applies."""
    [m] = apply_mapping(
        "AWS::WAFv2::WebACL",
        {
            "Name": "perimeter-waf",
            "Scope": "REGIONAL",
            "Description": "edge boundary",
            "DefaultAction": {"Allow": {}},
            "Rules": [],
        },
    )
    assert m.tf_type == "aws_wafv2_web_acl"
    assert m.body["name"] == "perimeter-waf"
    assert m.body["scope"] == "REGIONAL"
    assert m.body["description"] == "edge boundary"
    assert m.body["default_action"] == [{"allow": [{}]}]
    assert m.body["rule"] == []


def test_wafv2_action_translates_each_kind() -> None:
    """Action.{Block, Allow, Count, Captcha, Challenge} all become list-wrapped blocks."""
    rules = [
        {"Name": f"r-{kind}", "Priority": i, "Action": {kind: {}}}
        for i, kind in enumerate(["Block", "Allow", "Count", "Captcha", "Challenge"])
    ]
    [m] = apply_mapping("AWS::WAFv2::WebACL", {"Name": "w", "Rules": rules})
    expected_kinds = ["block", "allow", "count", "captcha", "challenge"]
    for rule, kind in zip(m.body["rule"], expected_kinds, strict=True):
        assert rule["action"] == [{kind: [{}]}]


def test_wafv2_override_action_translates_none_and_count() -> None:
    """OverrideAction.{None, Count} → override_action[0].{none, count}=[{}]."""
    rules = [
        {"Name": "managed-none", "OverrideAction": {"None": {}}},
        {"Name": "managed-count", "OverrideAction": {"Count": {}}},
    ]
    [m] = apply_mapping("AWS::WAFv2::WebACL", {"Name": "w", "Rules": rules})
    assert m.body["rule"][0]["override_action"] == [{"none": [{}]}]
    assert m.body["rule"][1]["override_action"] == [{"count": [{}]}]


# --- WAFv2::WebACL — Statement deep translation ----------------------------


def test_wafv2_geo_match_statement_translates() -> None:
    """GeoMatchStatement.CountryCodes → geo_match_statement[0].country_codes."""
    [m] = apply_mapping(
        "AWS::WAFv2::WebACL",
        {
            "Name": "geo-block",
            "Rules": [
                {
                    "Name": "block-embargoed",
                    "Priority": 1,
                    "Action": {"Block": {}},
                    "Statement": {"GeoMatchStatement": {"CountryCodes": ["KP", "IR", "CU", "SY"]}},
                }
            ],
        },
    )
    rule = m.body["rule"][0]
    assert rule["statement"] == [
        {"geo_match_statement": [{"country_codes": ["KP", "IR", "CU", "SY"]}]}
    ]


def test_wafv2_rate_based_statement_translates() -> None:
    """RateBasedStatement.{Limit, AggregateKeyType} → rate_based_statement[0] block."""
    [m] = apply_mapping(
        "AWS::WAFv2::WebACL",
        {
            "Name": "rate-limit",
            "Rules": [
                {
                    "Name": "throttle",
                    "Priority": 1,
                    "Action": {"Block": {}},
                    "Statement": {"RateBasedStatement": {"Limit": 2000, "AggregateKeyType": "IP"}},
                }
            ],
        },
    )
    rule = m.body["rule"][0]
    assert rule["statement"] == [
        {"rate_based_statement": [{"limit": 2000, "aggregate_key_type": "IP"}]}
    ]


def test_wafv2_managed_rule_group_statement_translates() -> None:
    """ManagedRuleGroupStatement → managed_rule_group_statement[0] block."""
    [m] = apply_mapping(
        "AWS::WAFv2::WebACL",
        {
            "Name": "owasp-baseline",
            "Rules": [
                {
                    "Name": "aws-common",
                    "Priority": 1,
                    "OverrideAction": {"None": {}},
                    "Statement": {
                        "ManagedRuleGroupStatement": {
                            "VendorName": "AWS",
                            "Name": "AWSManagedRulesCommonRuleSet",
                            "Version": "Version_2.0",
                        }
                    },
                }
            ],
        },
    )
    rule = m.body["rule"][0]
    assert rule["statement"] == [
        {
            "managed_rule_group_statement": [
                {
                    "vendor_name": "AWS",
                    "name": "AWSManagedRulesCommonRuleSet",
                    "version": "Version_2.0",
                }
            ]
        }
    ]


def test_wafv2_ip_set_reference_statement_translates() -> None:
    """IPSetReferenceStatement.Arn → ip_set_reference_statement[0].arn."""
    [m] = apply_mapping(
        "AWS::WAFv2::WebACL",
        {
            "Name": "blocklist",
            "Rules": [
                {
                    "Name": "block-bad",
                    "Priority": 1,
                    "Action": {"Block": {}},
                    "Statement": {
                        "IPSetReferenceStatement": {
                            "Arn": "arn:aws:wafv2:us-east-1:123:regional/ipset/bad-actors/abc"
                        }
                    },
                }
            ],
        },
    )
    rule = m.body["rule"][0]
    assert rule["statement"] == [
        {
            "ip_set_reference_statement": [
                {"arn": "arn:aws:wafv2:us-east-1:123:regional/ipset/bad-actors/abc"}
            ]
        }
    ]


def test_wafv2_rule_group_reference_statement_translates() -> None:
    """RuleGroupReferenceStatement.Arn → rule_group_reference_statement[0].arn."""
    [m] = apply_mapping(
        "AWS::WAFv2::WebACL",
        {
            "Name": "with-custom",
            "Rules": [
                {
                    "Name": "custom",
                    "Priority": 1,
                    "OverrideAction": {"None": {}},
                    "Statement": {
                        "RuleGroupReferenceStatement": {
                            "Arn": "arn:aws:wafv2:us-east-1:123:regional/rulegroup/custom/xyz"
                        }
                    },
                }
            ],
        },
    )
    rule = m.body["rule"][0]
    assert rule["statement"] == [
        {
            "rule_group_reference_statement": [
                {"arn": "arn:aws:wafv2:us-east-1:123:regional/rulegroup/custom/xyz"}
            ]
        }
    ]


# --- WAFv2::WebACL — detector parity end-to-end ----------------------------


def _write_wafv2_fixture(tmp_path: Path) -> Path:
    """Lay down a WAFv2 WebACL CFN template exercising every detector's read path."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  PerimeterWaf:\n"
        "    Type: AWS::WAFv2::WebACL\n"
        "    Properties:\n"
        "      Name: perimeter-waf\n"
        "      Scope: REGIONAL\n"
        "      DefaultAction:\n"
        "        Allow: {}\n"
        "      Rules:\n"
        "        - Name: GeoBlockEmbargoed\n"
        "          Priority: 1\n"
        "          Action:\n"
        "            Block: {}\n"
        "          Statement:\n"
        "            GeoMatchStatement:\n"
        "              CountryCodes: [KP, IR, CU, SY]\n"
        "        - Name: RateThrottle\n"
        "          Priority: 2\n"
        "          Action:\n"
        "            Block: {}\n"
        "          Statement:\n"
        "            RateBasedStatement:\n"
        "              Limit: 2000\n"
        "              AggregateKeyType: IP\n"
        "        - Name: AwsManagedCommon\n"
        "          Priority: 3\n"
        "          OverrideAction:\n"
        "            None: {}\n"
        "          Statement:\n"
        "            ManagedRuleGroupStatement:\n"
        "              VendorName: AWS\n"
        "              Name: AWSManagedRulesCommonRuleSet\n"
        "        - Name: BlockBadIPs\n"
        "          Priority: 4\n"
        "          Action:\n"
        "            Block: {}\n"
        "          Statement:\n"
        "            IPSetReferenceStatement:\n"
        "              Arn: arn:aws:wafv2:us-east-1:123:regional/ipset/bad/abc\n"
        "        - Name: CustomRuleGroup\n"
        "          Priority: 5\n"
        "          OverrideAction:\n"
        "            None: {}\n"
        "          Statement:\n"
        "            RuleGroupReferenceStatement:\n"
        "              Arn: arn:aws:wafv2:us-east-1:123:regional/rulegroup/custom/xyz\n"
    )
    return cfn


def test_waf_geo_blocking_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.waf_geo_blocking` reads geo_match_statement.country_codes from CFN-translated body."""
    tf_resources = adapt_cfn_resources(
        parse_cfn_file(_write_wafv2_fixture(tmp_path)), scan_root=tmp_path
    )
    evidence = waf_geo_detector.detect(tf_resources)
    assert len(evidence) == 1
    e = evidence[0]
    assert e.content["resource_type"] == "aws_wafv2_web_acl"
    assert "KP" in e.content["country_codes"]
    assert "IR" in e.content["country_codes"]


def test_waf_rate_limiting_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.waf_rate_limiting` reads rate_based_statement.limit from CFN-translated body."""
    tf_resources = adapt_cfn_resources(
        parse_cfn_file(_write_wafv2_fixture(tmp_path)), scan_root=tmp_path
    )
    evidence = waf_rate_detector.detect(tf_resources)
    assert len(evidence) == 1
    assert evidence[0].content["resource_type"] == "aws_wafv2_web_acl"


def test_waf_managed_rule_groups_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.waf_managed_rule_groups` reads managed_rule_group_statement.{vendor_name, name}."""
    tf_resources = adapt_cfn_resources(
        parse_cfn_file(_write_wafv2_fixture(tmp_path)), scan_root=tmp_path
    )
    evidence = waf_managed_detector.detect(tf_resources)
    assert len(evidence) == 1
    assert evidence[0].content["resource_type"] == "aws_wafv2_web_acl"


def test_waf_ip_set_blocking_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.waf_ip_set_blocking` reads ip_set_reference_statement.arn."""
    tf_resources = adapt_cfn_resources(
        parse_cfn_file(_write_wafv2_fixture(tmp_path)), scan_root=tmp_path
    )
    evidence = waf_ipset_detector.detect(tf_resources)
    assert len(evidence) == 1
    assert evidence[0].content["resource_type"] == "aws_wafv2_web_acl"


def test_waf_custom_rule_groups_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.waf_custom_rule_groups` reads rule_group_reference_statement.arn."""
    tf_resources = adapt_cfn_resources(
        parse_cfn_file(_write_wafv2_fixture(tmp_path)), scan_root=tmp_path
    )
    evidence = waf_custom_detector.detect(tf_resources)
    assert len(evidence) == 1
    assert evidence[0].content["resource_type"] == "aws_wafv2_web_acl"


def test_waf_rule_count_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.waf_rule_count` counts rule blocks; should see all 5 from the fixture."""
    tf_resources = adapt_cfn_resources(
        parse_cfn_file(_write_wafv2_fixture(tmp_path)), scan_root=tmp_path
    )
    evidence = waf_count_detector.detect(tf_resources)
    assert len(evidence) == 1


def test_waf_action_types_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.waf_action_types` reads each rule's action / override_action enforcement state."""
    tf_resources = adapt_cfn_resources(
        parse_cfn_file(_write_wafv2_fixture(tmp_path)), scan_root=tmp_path
    )
    evidence = waf_action_detector.detect(tf_resources)
    assert len(evidence) == 1


# --- AWS::WAFv2::WebACLAssociation -----------------------------------------


def test_wafv2_web_acl_association_basic_translation() -> None:
    """ResourceArn + WebACLArn → resource_arn + web_acl_arn; tf_type override applies."""
    [m] = apply_mapping(
        "AWS::WAFv2::WebACLAssociation",
        {
            "ResourceArn": "arn:aws:apigateway:us-east-1::/restapis/abc/stages/prod",
            "WebACLArn": "arn:aws:wafv2:us-east-1:123:regional/webacl/perimeter/xyz",
        },
    )
    assert m.tf_type == "aws_wafv2_web_acl_association"
    assert m.body["resource_arn"] == "arn:aws:apigateway:us-east-1::/restapis/abc/stages/prod"
    assert m.body["web_acl_arn"] == "arn:aws:wafv2:us-east-1:123:regional/webacl/perimeter/xyz"


# --- AWS::WAFv2::RuleGroup -------------------------------------------------


def test_wafv2_rule_group_basic_translation() -> None:
    """Top-level fields + Rules deep-translation, tf_type override applies."""
    [m] = apply_mapping(
        "AWS::WAFv2::RuleGroup",
        {
            "Name": "custom-blocklist",
            "Scope": "REGIONAL",
            "Capacity": 50,
            "Rules": [
                {
                    "Name": "block-bad-ips",
                    "Priority": 1,
                    "Action": {"Block": {}},
                    "Statement": {
                        "IPSetReferenceStatement": {
                            "Arn": "arn:aws:wafv2:us-east-1:123:regional/ipset/bad/abc"
                        }
                    },
                }
            ],
        },
    )
    assert m.tf_type == "aws_wafv2_rule_group"
    assert m.body["name"] == "custom-blocklist"
    assert m.body["scope"] == "REGIONAL"
    assert m.body["capacity"] == 50
    assert len(m.body["rule"]) == 1


# --- AWS::WAF::WebACL (legacy v1) ------------------------------------------


def test_waf_web_acl_legacy_basic_translation() -> None:
    """WAF Classic: Name + MetricName + DefaultAction.Type. Minimal mapping by design."""
    [m] = apply_mapping(
        "AWS::WAF::WebACL",
        {
            "Name": "legacy-waf",
            "MetricName": "legacyWaf",
            "DefaultAction": {"Type": "ALLOW"},
        },
    )
    assert m.tf_type == "aws_waf_web_acl"
    assert m.body["name"] == "legacy-waf"
    assert m.body["metric_name"] == "legacyWaf"
    assert m.body["default_action"] == [{"type": "ALLOW"}]


# --- AWS::Shield::Protection -----------------------------------------------


def test_shield_protection_basic_translation() -> None:
    """Name + ResourceArn rename; default tf_type already correct (aws_shield_protection)."""
    [m] = apply_mapping(
        "AWS::Shield::Protection",
        {
            "Name": "alb-protection",
            "ResourceArn": "arn:aws:elasticloadbalancing:us-east-1:123:loadbalancer/app/main/abc",
        },
    )
    # tf_type=None → adapter falls back to cfn_type_to_tf_type which yields aws_shield_protection
    assert m.tf_type is None
    assert m.body["name"] == "alb-protection"
    assert (
        m.body["resource_arn"]
        == "arn:aws:elasticloadbalancing:us-east-1:123:loadbalancer/app/main/abc"
    )


def test_shield_protection_routes_through_adapter_to_aws_shield_protection(
    tmp_path: Path,
) -> None:
    """Adapter combines the default tf_type with the mapped body to yield aws_shield_protection."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  AlbShield:\n"
        "    Type: AWS::Shield::Protection\n"
        "    Properties:\n"
        "      Name: alb\n"
        "      ResourceArn: arn:aws:elasticloadbalancing:us-east-1:123:loadbalancer/app/main/abc\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    assert len(tf_resources) == 1
    assert tf_resources[0].type == "aws_shield_protection"
    assert tf_resources[0].body["resource_arn"].startswith("arn:aws:elasticloadbalancing")


# --- cna_dos_protection: WAFv2-aware path ----------------------------------


def test_cna_dos_protection_fires_on_cfn_wafv2_with_rate_rule(tmp_path: Path) -> None:
    """`aws.cna_dos_protection` counts rate_based_statement blocks via CFN-translated WAFv2."""
    tf_resources = adapt_cfn_resources(
        parse_cfn_file(_write_wafv2_fixture(tmp_path)), scan_root=tmp_path
    )
    evidence = cna_dos_detector.detect(tf_resources)
    # The fixture has WAFv2 with a rate-based rule + ip-set + managed group.
    # cna_dos_protection emits one Evidence per WAF/Shield/relevant resource;
    # the WAFv2 WebACL should be among them.
    assert any(e.content.get("resource_type") == "aws_wafv2_web_acl" for e in evidence)
