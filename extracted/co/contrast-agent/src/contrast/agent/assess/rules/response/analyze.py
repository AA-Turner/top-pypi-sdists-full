# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from collections import namedtuple
from html.parser import HTMLParser

from contrast.agent.settings import Settings
from contrast_vendor import structlog as logging
from contrast.utils.string_utils import ensure_string

logger = logging.getLogger("contrast")

Tag = namedtuple("Tag", ["type", "tag", "attrs"])


def analyze_response_rules(context):
    settings = Settings()

    response_rules = settings.enabled_response_rules()
    response = context.response
    if (
        not response_rules
        or not response
        or not response.body
        or not (body := ensure_string(response.body))
    ):
        return

    content_type = response.headers.get("content-type", "")

    status_code = response.status_code
    valid_response_rules = [
        rule for rule in response_rules if rule.is_valid(status_code, content_type)
    ]

    if not valid_response_rules:
        return

    form_tags, meta_tags = get_tags(body, content_type)

    logger.debug("Analyzing response rules", response_rules=valid_response_rules)

    for rule in valid_response_rules:
        violated, properties = rule.is_violated(
            response.headers, body, form_tags, meta_tags
        )
        if violated:
            rule.build_and_append_finding(properties, context)


class BodyParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.form_tags = []
        self.meta_tags = []

    def handle_starttag(self, tag, attrs):
        if tag == "form":
            self.form_tags.append(
                Tag(type="form", tag=self.get_starttag_text(), attrs=attrs)
            )
        if tag == "meta":
            self.meta_tags.append(
                Tag(type="meta", tag=self.get_starttag_text(), attrs=attrs)
            )

    def error(self, message: str):
        """
        error is a method that should be overridden by a subclass to handle
        HTMLParser errors. In py3.10, it is no longer used and the parser
        will raise AssertionErrors instead. This method unifies the behavior
        across versions.
        """
        raise AssertionError(message)


def get_tags(body, content_type: str):
    parser = BodyParser()
    try:
        parser.feed(body)
        parser.close()
    except AssertionError as exc:
        # Invalid HTML throws assertion errors. HTMLParser doesn't expose an API
        # to disable these assertions.
        # We don't validate that the body is HTML, and the error can be ignored
        # if the body isn't HTML. If the body is HTML or we partially parsed
        # tags, throw the exception so that we can investigate the issue.
        if "html" in content_type:
            raise RuntimeError(
                f"Failed to parse response body {content_type=}"
            ) from exc
        if parser.form_tags or parser.meta_tags:
            raise RuntimeError(
                f"Partially parsed response body {parser.form_tags=} {parser.meta_tags=}"
            ) from exc

    return parser.form_tags, parser.meta_tags
