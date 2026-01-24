# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import re

import contrast_fireball
from contrast_fireball import (
    AttackInputType,
    DocumentType,
    ProtectEventInput,
    ProtectEventSample,
)

from contrast.agent.agent_lib.input_tracing import InputAnalysisResult
from contrast.agent.policy.patch_location_policy import PatchLocationPolicy
from contrast.agent.protect.rule.base_rule import BaseRule
from contrast.agent.protect.rule.xxe.entity_wrapper import EntityWrapper
from contrast.utils.patch_utils import get_arg


class Xxe(BaseRule):
    """
    XXE Protection rule
    """

    RULE_NAME = "xxe"
    FIREBALL_RULE = contrast_fireball.Xxe
    INPUT_NAME = "XML Prolog"

    EXTERNAL_ENTITY_PATTERN = re.compile(
        r"<!ENTITY\s+[a-zA-Z0-f]+\s+(?:SYSTEM|PUBLIC)\s+(.*?)>"
    )

    def __init__(self):
        super().__init__()

        self.prolog_xml = None

    def is_prefilter(self):
        return False

    def is_postfilter(self):
        return False

    def skip_protect_analysis(
        self, user_input: object, args: tuple, kwargs: dict[str, object]
    ) -> bool:
        return bool(
            (parser := get_arg(args, kwargs, 1, "parser", None))
            and getattr(parser, "resolve_entities", None) is False
        )

    def find_sink_attack(
        self,
        candidate_string: str | None = None,
        **kwargs,
    ) -> list[ProtectEventSample]:
        assert candidate_string is not None
        last_idx = 0
        declared_entities = []
        entities_resolved = []

        for match in self.EXTERNAL_ENTITY_PATTERN.finditer(candidate_string):
            last_idx = match.end(0)

            entity_wrapper = EntityWrapper(match.group())
            if not entity_wrapper.is_external_entity():
                continue

            declared_entities.append(
                contrast_fireball.XxeDeclaredEntity(
                    start=match.start(),
                    end=match.end(),
                )
            )
            entities_resolved.append(
                contrast_fireball.XxeExternalEntity(
                    system_id=entity_wrapper.system_id,
                    public_id=entity_wrapper.public_id,
                )
            )

        self.prolog_xml = candidate_string[:last_idx]
        if not self.prolog_xml:
            return []

        attack_sample = self.build_sample(
            None,
            candidate_string=None,
            outcome=self.outcome_from_mode,
            declared_entities=declared_entities,
            entities_resolved=entities_resolved,
        )
        return [attack_sample]

    def build_sample(
        self,
        evaluation: InputAnalysisResult | None,
        candidate_string: str | None,
        outcome: contrast_fireball.ProtectEventOutcome,
        **kwargs,
    ) -> ProtectEventSample:
        rule = self.FIREBALL_RULE(
            details=contrast_fireball.XxeDetails(
                xml=self.prolog_xml,
                declared_entities=kwargs["declared_entities"],
                entities_resolved=kwargs["entities_resolved"],
            )
        )
        sample = self.build_base_sample(
            evaluation,
            outcome=outcome or self.outcome_from_mode,
            rule=rule,
        )

        return sample

    def build_user_input(self, evaluation: InputAnalysisResult) -> ProtectEventInput:
        assert self.prolog_xml is not None
        return ProtectEventInput(
            filters=[],
            input_type=AttackInputType.UNKNOWN,
            time=None,
            value=self.prolog_xml,
            name=self.INPUT_NAME,
            document_type=DocumentType.NORMAL,
        )

    def infilter_kwargs(self, user_input: str, patch_policy: PatchLocationPolicy):
        return dict(framework=patch_policy.method_name)
