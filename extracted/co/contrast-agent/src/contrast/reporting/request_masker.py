# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from dataclasses import dataclass, replace
from typing import TypedDict
from urllib.parse import parse_qs, unquote, urlencode
from collections.abc import Mapping

from contrast.api.attack import ProtectResponse
from contrast.api.user_input import UserInput
from contrast_vendor import structlog as logging
from contrast_vendor.webob.multidict import MultiDict

logger = logging.getLogger("contrast")

MASK = "contrast-redacted-{}"
VECTOR_MASK = MASK.format("vector")
BODY_MASK = "contrast-redacted-body"
SEMICOLON_URL_ENCODE_VAL = "%25"


class SensitiveDataRule(TypedDict):
    id: str
    keywords: list[str]


@dataclass(frozen=True)
class SensitiveDataPolicy:
    mask_attack_vector: bool
    mask_http_body: bool
    rules: list[SensitiveDataRule]


class RequestMasker:
    def __init__(self, config: Mapping):
        self.mask_rules = SensitiveDataPolicy(
            mask_attack_vector=config[
                "application.sensitive_data_masking_policy.mask_attack_vector"
            ],
            mask_http_body=config[
                "application.sensitive_data_masking_policy.mask_http_body"
            ],
            rules=config["application.sensitive_data_masking_policy.rules"],
        )

    @classmethod
    def new_request_masker(cls, config: SensitiveDataPolicy):
        return cls(
            {
                "application.sensitive_data_masking_policy.mask_attack_vector": config.mask_attack_vector,
                "application.sensitive_data_masking_policy.mask_http_body": config.mask_http_body,
                "application.sensitive_data_masking_policy.rules": config.rules,
            }
        )

    def mask_attack_input(self, input: UserInput):
        """
        Mask the attack input based on the masking rules.
        """
        masked_name = (
            self.mask_attack_vector(input.name)
            if input.is_name_based and input.name
            else input.name
        )

        return replace(
            input,
            value=self.mask_attack_vector(input.value),
            name=masked_name,
        )

    def mask_attack_vector(self, vector: str):
        """
        Mask the provided vector if "mask_attack_vector" is set to True in the mask rules.
        """
        return vector if not self.mask_rules.mask_attack_vector else VECTOR_MASK

    def mask_sensitive_data(self, request, attack=None):
        if not request or not self.mask_rules:
            return

        self.request = request
        self.attack = attack

        logger.debug("Masker: masking sensitive data")

        self._mask_body()
        self._mask_query_string()
        self._mask_request_params()
        self._mask_request_cookies()
        self._mask_request_headers()

        request._masked = True

    def _mask_body(self):
        if not self.request.body:
            return

        if self.mask_rules.mask_http_body:
            self.request._masked_body = BODY_MASK
            return
        if (
            self.mask_rules.mask_attack_vector
            and self.attack
            and any(
                sample.user_input.type.is_body_based for sample in self.attack.samples
            )
        ):
            # NOTE: is_body_based is loose when it comes to querystring parameters.
            # This could cause extra redaction, but that's an acceptable trade-off
            # in the short term.
            self.request._masked_body = VECTOR_MASK

    def _mask_query_string(self):
        if self.request.query_string:
            self.request._masked_query_string = self._mask_raw_query(
                self.request.query_string
            )

    def _mask_raw_query(self, query_string):
        qs_dict = parse_qs(query_string)
        masked_qs_dict = self._mask_dictionary(qs_dict)
        return urlencode(masked_qs_dict, doseq=True)

    def _mask_request_params(self):
        params = self.request.params
        if not params:
            return

        self.request._masked_params = self._mask_dictionary(params)

    def _mask_request_cookies(self):
        cookies = self.request.cookies
        if not cookies:
            return

        self.request._masked_cookies = self._mask_dictionary(cookies)

    def _mask_request_headers(self):
        headers = self.request.headers
        if not headers:
            return

        self.request._masked_headers = self._mask_dictionary(headers)

    def _mask_dictionary(self, d):
        if not d:
            return d

        if isinstance(d, MultiDict):
            d = d.mixed()

        return {
            self._mask_key_vector(k, self.attack): self._mask_value(k, v, self.attack)
            for k, v in d.items()
        }

    def _mask_key_vector(self, k, attack):
        return (
            VECTOR_MASK
            if self.mask_rules.mask_attack_vector and self._is_value_vector(attack, k)
            else k
        )

    def _mask_value(self, k, v, attack):
        if isinstance(v, list):
            return [self._mask_value(k, item, attack) for item in v]

        if not self._is_value_vector(attack, v):
            if k is not None and self._find_value_index_in_rules(k.lower()) != -1:
                return MASK.format(k.lower())
        elif self.mask_rules.mask_attack_vector:
            return VECTOR_MASK
        return v

    def _is_value_vector(self, attack, value):
        if not attack or attack.response == ProtectResponse.NO_ACTION or not value:
            return False

        return self._is_value_in_sample(attack.samples, value)

    def _is_value_in_sample(self, samples, value):
        if not samples:
            return False

        # Setting this to remove url encoding of header and cookie values
        value = unquote(value)

        return any(sample.user_input.value == value for sample in samples)

    def _find_value_index_in_rules(self, s):
        index = -1
        # When looking for header it replaces '_' with '-' and I don't want to risk not
        # properly matching to the rules
        s = s.replace("-", "_")
        for rule in self.mask_rules.rules:
            try:
                index = rule.get("keywords").index(s)
                break
            except ValueError:
                index = -1

        return index
