# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from enum import Enum, auto

import contrast
from contrast.agent.request import Request
from contrast.api.sample import Sample
from contrast.utils.timer import now_ms
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class ProtectResponse(Enum):
    NO_ACTION = auto()
    BLOCKED = auto()
    MONITORED = auto()
    PROBED = auto()
    BLOCKED_AT_PERIMETER = auto()


# Certain rules in Protect can only be confirmed as suspicious, meaning they didn't get evaluated against user input
# or they didn't have input tracing applied. We report these rules differently.
SUSPICIOUS_RULES = [
    "malformed-header",
    "reflected-xss",
    "unsafe-file-upload",
    "zip-file-overwrite",
]


class Attack:
    """
    Class storing all data necessary to report a protect attack.
    """

    def __init__(self, rule_id: str):
        self.rule_id: str = rule_id
        self.samples: list[Sample] = []
        self.response: ProtectResponse | None = None
        self.start_time_ms = contrast.REQUEST_CONTEXT.get().request.timestamp_ms

    @property
    def blocked(self) -> bool:
        return self.response == ProtectResponse.BLOCKED

    @property
    def perimeter_blocked(self) -> bool:
        return self.response == ProtectResponse.BLOCKED_AT_PERIMETER

    def add_sample(self, sample: Sample) -> None:
        self.samples.append(sample)

    def _convert_samples(self, request: Request) -> list[dict]:
        reportable_request = request.reportable_format if request is not None else {}

        return [
            {
                "blocked": self.blocked,
                "input": self._convert_user_input(sample),
                "details": self._mask_details(sample),
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
                    "start": sample.timestamp_ms,  # in ms
                    "elapsed": (
                        now_ms() - sample.timestamp_ms
                    ),  # in ms which is the format TS accepts
                },
            }
            for sample in self.samples
        ]

    def _mask_details(self, sample: Sample) -> dict:
        if not self.masker.mask_rules.mask_attack_vector:
            return sample.details

        return {
            k: self.masker.mask_attack_vector(v) if isinstance(v, str) else v
            for k, v in sample.details.items()
        }

    def _convert_user_input(self, sample: Sample) -> dict:
        masked_user_input = self.masker.mask_attack_input(sample.user_input)
        json_sample = {
            "documentType": masked_user_input.document_type.name,
            "filters": masked_user_input.matcher_ids,
            "time": sample.timestamp_ms,
            "type": masked_user_input.type.name,
            "value": masked_user_input.value,
        }
        if masked_user_input.path:
            json_sample["documentPath"] = masked_user_input.path
        if masked_user_input.name:
            json_sample["name"] = masked_user_input.name

        return json_sample

    def report_result(self) -> str:
        response_map = {
            ProtectResponse.BLOCKED: "blocked",
            ProtectResponse.BLOCKED_AT_PERIMETER: "blocked",
            ProtectResponse.PROBED: "ineffective",
            ProtectResponse.MONITORED: (
                "suspicious" if self.rule_id in SUSPICIOUS_RULES else "exploited"
            ),
        }
        return response_map[self.response]

    def to_json(self, request: Request, request_data_masker) -> dict:
        self.masker = request_data_masker
        request_data_masker.mask_sensitive_data(request, self)

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

        relevant_mode = self.report_result()

        samples = self._convert_samples(request)

        json[relevant_mode] = {
            "total": 1,  # always 1 until batching happens
            "startTime": self.start_time_ms,
            "samples": samples,
        }

        return json
