# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.response.base_response_rule import BaseResponseRule


class BaseBodyOnlyRule(BaseResponseRule):
    @property
    def name(self):
        raise NotImplementedError

    def is_body_violated(self, body, form_tags):
        raise NotImplementedError

    def is_violated(self, _, body, form_tags, meta_tags):
        body_violated, body_properties = self.is_body_violated(body, form_tags)
        return body_violated, body_properties

    def build_properties(self, full_tag, body):
        original_start = body.index(full_tag)
        original_end = original_start + len(full_tag)

        # 50chars before + full tag + 50 chars after
        html = body[max(0, original_start - 50) : min(len(body), original_end + 50)]

        redacted_start = html.index(full_tag)
        redacted_end = redacted_start + len(full_tag)

        return dict(
            html=html,
            start=str(redacted_start),
            end=str(redacted_end),
        )
