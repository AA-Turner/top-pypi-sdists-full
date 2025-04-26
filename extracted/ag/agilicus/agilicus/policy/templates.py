import regex

from abc import abstractmethod
from typing import Optional

from agilicus import (
    RuleAction,
    RuleCondition,
    RuleConfig,
    MaxMFAProofRuleCondition,
    StandaloneObjectConditions,
    StandaloneRule,
    StandaloneRuleName,
    StandaloneRuleScope,
    StandaloneRuleSpec,
    StandaloneRuleTree,
    StandaloneRuleTreeSpec,
    StandaloneRuleTreeRef,
    StandaloneRuleTreeRuleRef,
    StandaloneRuleTreeNode,
    StandaloneRuleset,
    StandaloneRulesetLabelName,
    StandaloneRulesetLabelSpec,
    StandaloneRulesetLabel,
    StandaloneRulesetSpec,
)


class PolicyTemplate:
    @abstractmethod
    def get_rules(self) -> list[StandaloneRule]:
        pass

    @abstractmethod
    def get_trees(self) -> list[StandaloneRuleTree]:
        pass

    @abstractmethod
    def get_sets(self) -> list[StandaloneRuleset]:
        pass

    @abstractmethod
    def get_labels(self) -> list[StandaloneRulesetLabel]:
        pass


def mfa_cond(max_seconds):
    return MaxMFAProofRuleCondition(
        condition_type="mfa_rule_condition", max_seconds=max_seconds
    )


MFA_LABEL = "global-multifactor"
LABEL_REGEX = regex.compile(r"urn:agilicus:label:(?P<label>[a-zA-Z0-9\-\._:]+)")


def parse_label(scope):
    match = LABEL_REGEX.match(str(scope))
    if not match:
        return None
    return match.group("label")


def parse_labels(scopes):
    result = []
    for scope in scopes:
        label = parse_label(scope)
        if not label:
            continue
        result.append(label)
    return result


class MultifactorTemplate(PolicyTemplate):
    name_regex = regex.compile(r"agilicus-mfa-tmpl-(?P<name>[a-zA-Z0-9\-\._]+)")

    def __init__(self, name, duration, org_id, labels: Optional[list[str]] = None):
        self.name = name
        self.duration = duration
        self.labels = labels or []
        self.org_id = org_id

    def to_dict(self):
        return {
            "name": self.name,
            "duration": self.duration,
            "labels": self.labels,
            "org_id": self.org_id,
        }

    @classmethod
    def build_name(cls, name):
        return f"agilicus-mfa-tmpl-{name}"

    def get_name(self):
        return self.build_name(self.name)

    @classmethod
    def parse_name(cls, name):
        match = cls.name_regex.match(name)
        if not match:
            return None
        return match.group("name")

    def get_rules(self) -> list[StandaloneRule]:
        cond = mfa_cond(self.duration)
        action = RuleAction(action="mfa")
        extended_condition = RuleCondition(negated=True, condition=cond)
        spec = StandaloneRuleSpec(
            rule=RuleConfig(
                name=self.get_name(),
                extended_condition=extended_condition,
                actions=[action],
            ),
            org_id=self.org_id,
        )

        rule = StandaloneRule(spec=spec)
        return [rule]

    def get_trees(self) -> list[StandaloneRuleTree]:
        spec = StandaloneRuleTreeSpec(
            tree=StandaloneRuleTreeNode(
                rules=[
                    StandaloneRuleTreeRuleRef(
                        rule_name=StandaloneRuleName(self.get_name()),
                    )
                ],
                children=[],
            ),
            name=StandaloneRuleName(self.get_name()),
            org_id=self.org_id,
            object_conditions=StandaloneObjectConditions(),
            # object_conditions=StandaloneObjectConditions(
            #     scopes=[StandaloneRuleScope("urn:agilicus:scope:any_resource_user")]
            # )
        )

        return [StandaloneRuleTree(spec=spec)]

    def get_sets(self) -> list[StandaloneRuleset]:
        spec = StandaloneRulesetSpec(
            rule_trees=[
                StandaloneRuleTreeRef(
                    rule_tree_name=StandaloneRuleName(self.get_name()),
                    priority=0,
                )
            ],
            labels=[StandaloneRulesetLabelName(MFA_LABEL)],
            name=StandaloneRuleName(self.get_name()),
            org_id=self.org_id,
        )
        scopes = [
            StandaloneRuleScope(f"urn:agilicus:label:{label}") for label in self.labels
        ]
        if scopes:
            object_conditions = StandaloneObjectConditions(scopes=scopes)
            spec.object_conditions = object_conditions

        return [StandaloneRuleset(spec=spec)]

    def get_labels(self) -> list[StandaloneRulesetLabel]:
        spec = StandaloneRulesetLabelSpec(
            name=StandaloneRulesetLabelName(MFA_LABEL),
            org_id=self.org_id,
        )

        return [
            StandaloneRulesetLabel(spec=spec),
        ]

    @classmethod
    def from_api(cls, name, rules, org_id, trees, sets):
        found_sets = list(filter(lambda s: str(s.spec.name) == name, sets))
        found_trees = list(filter(lambda s: str(s.spec.name) == name, trees))
        found_rules = list(filter(lambda s: str(s.spec.rule.name) == name, rules))

        if len(found_sets) == 0 or len(found_rules) == 0 or len(found_trees) == 0:
            return None

        # There should be only one, given that names are unique.
        ruleset = found_sets[0]
        labels = []
        if ruleset.spec.object_conditions:
            labels = parse_labels(ruleset.spec.object_conditions.scopes)
        rule = found_rules[0]
        try:
            duration = rule.spec.rule.extended_condition.condition.max_seconds
        except Exception:
            return None

        return MultifactorTemplate(
            name=cls.parse_name(name), duration=duration, labels=labels, org_id=org_id
        )
