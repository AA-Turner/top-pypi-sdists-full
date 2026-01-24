# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations


from contrast_fireball import (
    BotBlocker,
    CmdInjection,
    IpDenyList,
    MethodTampering,
    NosqlInjection,
    PathTraversal,
    ProtectEventOutcome,
    ProtectEventSample,
    SqlInjection,
    UnsafeFileUpload,
    UntrustedDeserialization,
    Xss,
    Xxe,
)

import contrast
from contrast.agent.request import Request
from contrast.api.utils import as_camel_dict
from contrast.utils.timer import now_ms
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


# Certain rules in Protect can only be confirmed as suspicious, meaning they didn't get evaluated against user input
# or they didn't have input tracing applied. We report these rules differently.
SUSPICIOUS_RULES = [
    "reflected-xss",
    "unsafe-file-upload",
    "zip-file-overwrite",
]


EVENT_OUTCOME_TO_REPORTABLE_STR = {
    ProtectEventOutcome.BLOCKED: "blocked",
    ProtectEventOutcome.BLOCKED_AT_PERIMETER: "blocked",
    ProtectEventOutcome.PROBED: "ineffective",
    ProtectEventOutcome.SUSPICIOUS: "suspicious",
    ProtectEventOutcome.EXPLOITED: "exploited",
}

PROTECT_RULE_TO_REPORTABLE_NAME = {
    BotBlocker: "bot-blocker",
    MethodTampering: "method-tampering",
    IpDenyList: "ip-deny-list",
    CmdInjection: "cmd-injection",
    PathTraversal: "path-traversal",
    SqlInjection: "sql-injection",
    NosqlInjection: "nosql-injection",
    UnsafeFileUpload: "unsafe-file-upload",
    UntrustedDeserialization: "untrusted-deserialization",
    Xss: "reflected-xss",
    Xxe: "xxe",
}


class Attack:
    """
    Class storing all data necessary to report a protect attack.
    """

    def __init__(self, samples: list[ProtectEventSample]):
        assert samples

        self.start_time_ms = contrast.REQUEST_CONTEXT.get().request.timestamp_ms
        self.samples: list[ProtectEventSample] = samples
        self.outcome: ProtectEventOutcome
        outcomes = [sample.outcome for sample in self.samples]
        self.outcome = outcomes[0]
        assert all(outcome == self.outcome for outcome in outcomes)

    @property
    def rule_id(self):
        return PROTECT_RULE_TO_REPORTABLE_NAME[self.samples[0].rule.__class__]

    @property
    def blocked(self) -> bool:
        return self.outcome == ProtectEventOutcome.BLOCKED

    def _convert_samples(self, request: Request) -> list[dict]:
        reportable_request = request.reportable_format if request is not None else {}

        return [
            {
                "blocked": self.blocked,
                "input": self._convert_user_input(sample),
                "details": (
                    as_camel_dict(sample.rule.details) if sample.rule.details else {}
                ),
                "request": reportable_request,
                "stack": [
                    {
                        "declaringClass": stack.declaring_class,
                        "methodName": stack.method_name,
                        "fileName": stack.file_name,
                        "lineNumber": stack.line_number,
                    }
                    for stack in sample.stack
                ],
                "timestamp": {
                    "start": sample.timestamp.start,  # in ms
                    "elapsed": (
                        now_ms() - sample.timestamp.start
                    ),  # in ms which is the format TS accepts
                },
            }
            for sample in self.samples
        ]

    def _convert_user_input(self, sample: ProtectEventSample) -> dict:
        user_input = sample.input
        json_sample = {
            "documentType": user_input.document_type.name,
            "filters": user_input.filters,
            "time": sample.timestamp.start,
            "type": user_input.input_type.name,
            "value": user_input.value,
        }
        if user_input.document_path:
            json_sample["documentPath"] = user_input.document_path
        if user_input.name:
            json_sample["name"] = user_input.name

        return json_sample

    def to_json(self, request: Request) -> dict:
        common_fields = {
            "startTime": 0,
            "total": 0,
        }
        json = {
            "startTime": self.start_time_ms,
            "blocked": common_fields,
            "exploited": common_fields,
            "ineffective": common_fields,
            "suspicious": common_fields,
        }

        assert self.outcome is not None
        relevant_mode = EVENT_OUTCOME_TO_REPORTABLE_STR[self.outcome]

        samples = self._convert_samples(request)

        json[relevant_mode] = {
            "total": 1,  # always 1 until batching happens
            "startTime": self.start_time_ms,
            "samples": samples,
        }

        return json
