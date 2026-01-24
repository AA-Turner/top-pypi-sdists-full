# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import json
import re

from contrast.agent.assess.rules.response.base_header_only_rule import (
    BaseResponseRule,
)
from contrast.agent.assess.rules import build_finding, send_finding
from contrast.utils.decorators import fail_quietly

UNSAFE_RE = re.compile(r"unsafe-(inline|eval)")

DEFAULT_SRC = "default-src"
CHILD_SRC = "child-src"
CONNECT_SRC = "connect-src"
FRAME_SRC = "frame-src"
MEDIA_SRC = "media-src"
OBJECT_SRC = "object-src"
SCRIPT_SRC = "script-src"
STYLE_SRC = "style-src"
BASE_URI = "base-uri"
FORM_ACTION = "form-action"
FRAME_ANCESTORS = "frame-ancestors"


class CspHeaderInsecureRule(BaseResponseRule):
    """
    Rule is violated if any the following headers:

    - Content-Security-Policy
    - X-Content-Security-Policy
    - X-Webkit-CSP

    are set with insecure parameters.

    Note that CSP-header-missing is a separate rule.
    """

    @property
    def name(self):
        return "csp-header-insecure"

    @property
    def header_keys(self):
        return ("Content-Security-Policy", "X-Content-Security-Policy", "X-Webkit-CSP")

    def is_violated(self, headers, _, form_tags, meta_tags):
        header_violated, header_properties = self.is_header_violated(headers)
        if not header_violated:
            # If header is correctly configured for this rule, no need to check body.
            return False, {}

        body_violated, body_properties = self.is_body_violated(meta_tags)
        if not body_violated:
            # Even though header may have violated the rule, if the body was configured
            # correctly for this rule, the rule is not violated.
            return False, {}

        return True, header_properties or body_properties

    def is_header_violated(self, headers):
        for key in self.header_keys:
            value = headers.get(key)
            if not value:
                continue

            csp_instructions = _detect_csp_settings(value)

            if csp_instructions is None or csp_instructions.is_safe():
                continue

            return True, csp_instructions.to_properties()

        return False, None

    def is_body_violated(self, meta_tags):
        """
        Rule is violated if:
        1. none of the attrs of the list of form tags have an "http-equiv" attr
        2. at least one attr is "http-equiv" and the next one in the current meta tag is not "content"
        :param form_tags: list of Tag namedtuple
        :return: violated bool, properties dict
        """
        if not meta_tags:
            return True, {}

        for tag in meta_tags:
            attrs_dict = {k.lower(): v.lower() for k, v in tag.attrs}
            if (
                attrs_dict.get("http-equiv") == "content-security-policy"
                and "content" in attrs_dict
            ):
                csp_instructions = _detect_csp_settings(attrs_dict.get("content"))
                if not csp_instructions.is_safe():
                    return True, csp_instructions.to_properties()

        return False, None

    def create_finding(self, properties):
        return build_finding(self, {"data": json.dumps(properties)})

    def build_and_append_finding(self, properties, context):
        finding = self.create_finding(properties)
        send_finding(finding, context)


@fail_quietly("Failed to detect CSP settings")
def _detect_csp_settings(csp_header_value):
    """
    Parse and detect safety of the entire CSP header. The format of CSP is a series of
    semi-colon separated directives, where each directive consists of a key followed by
    several values, all separated by whitespace. For example:

    "default-src 'self' cdn.example.com; script-src 'self'; connect-src 'self'"

    parses to:

    {
        "default-src": ["'self'", "cdn.example.com"],
        "script-src": ["'self'"],
        "connect-src": ["'self'"],
    }
    """
    split_values = [d.split(sep=None, maxsplit=1) for d in csp_header_value.split(";")]
    parsed_values = {v[0].lower(): v[1].lower() for v in split_values if len(v) > 1}
    return _CSPInstructions(parsed_values)


def _is_content_secure(value):
    return not (value is None or "*" in value)


def _is_content_safe(value):
    return not UNSAFE_RE.match(value)


class _CSPInstructions:
    def __init__(self, parsed_values):
        self.default_src = parsed_values.get(DEFAULT_SRC)
        self.child_src = parsed_values.get(CHILD_SRC)
        self.connect_src = parsed_values.get(CONNECT_SRC)
        self.frame_src = parsed_values.get(FRAME_SRC)
        self.media_src = parsed_values.get(MEDIA_SRC)
        self.object_src = parsed_values.get(OBJECT_SRC)
        self.script_src = parsed_values.get(SCRIPT_SRC)
        self.style_src = parsed_values.get(STYLE_SRC)
        self.base_uri = parsed_values.get(BASE_URI)
        self.form_action = parsed_values.get(FORM_ACTION)
        self.frame_ancestors = parsed_values.get(FRAME_ANCESTORS)

        self.default_src_secure = _is_content_secure(self.default_src)
        self.child_src_secure = _is_content_secure(self.child_src)
        self.connect_src_secure = _is_content_secure(self.connect_src)
        self.frame_src_secure = _is_content_secure(self.frame_src)
        self.media_src_secure = _is_content_secure(self.media_src)
        self.object_src_secure = _is_content_secure(self.object_src)
        self.script_src_secure = _is_content_secure(
            self.script_src
        ) and _is_content_safe(self.script_src)
        self.style_src_secure = _is_content_secure(self.style_src) and _is_content_safe(
            self.style_src
        )
        self.base_uri_secure = _is_content_secure(self.base_uri)
        self.form_action_secure = _is_content_secure(self.form_action)
        self.frame_ancestors_secure = _is_content_secure(self.frame_ancestors)

    def is_safe(self):
        return (
            self.form_action_secure
            and self.frame_ancestors_secure
            and self.base_uri_secure
            and self.are_sources_secure()
        )

    def are_sources_secure(self):
        extra_sources = [
            "child_src",
            "frame_src",
            "connect_src",
            "media_src",
            "object_src",
            "script_src",
            "style_src",
        ]
        if self.default_src_secure:
            for src in extra_sources:
                if getattr(self, src) is not None and not getattr(
                    self, f"{src}_secure"
                ):
                    return False
            return True

        return all([getattr(self, f"{src}_secure") for src in extra_sources])

    def to_properties(self):
        return {
            "defaultSrcValue": self.default_src or "",
            "childSrcValue": self.child_src or "",
            "connectSrcValue": self.connect_src or "",
            "frameSrcValue": self.frame_src or "",
            "mediaSrcValue": self.media_src or "",
            "objectSrcValue": self.object_src or "",
            "scriptSrcValue": self.script_src or "",
            "styleSrcValue": self.style_src or "",
            "baseUriValue": self.base_uri or "",
            "formActionValue": self.form_action or "",
            "frameAncestorsValue": self.frame_ancestors or "",
            "defaultSrcSecure": self.default_src_secure,
            "childSrcSecure": self.child_src_secure,
            "connectSrcSecure": self.connect_src_secure,
            "frameSrcSecure": self.frame_src_secure,
            "mediaSrcSecure": self.media_src_secure,
            "objectSrcSecure": self.object_src_secure,
            "scriptSrcSecure": self.script_src_secure,
            "styleSrcSecure": self.style_src_secure,
            "baseUriSecure": self.base_uri_secure,
            "formActionSecure": self.form_action_secure,
            "frameAncestorsSecure": self.frame_ancestors_secure,
        }
