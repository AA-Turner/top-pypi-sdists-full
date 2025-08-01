# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from collections.abc import Mapping
import re


from enum import Enum, auto

from contrast.utils.decorators import fail_loudly


from contrast_fireball import AssessEventAction, AssessFinding
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class InputExclusionSourceType(Enum):
    COOKIE = auto()
    PARAMETER = auto()
    HEADER = auto()
    BODY = auto()
    QUERYSTRING = auto()
    UNKNOWN = auto()


@fail_loudly("Unable to compile regex", log_level="warning")
def safe_re_compile(pattern, flags=0):
    return re.compile(pattern, flags=flags)


def strs_to_regexes(patterns: list[str], ignorecase=0):
    """
    Safely compiles a list of pattern strings into regex patterns.
    If a string cannot be compiled, it is skipped.
    """
    return [
        compiled_regex
        for pattern in patterns
        if (compiled_regex := safe_re_compile(pattern, flags=ignorecase))
    ]


class Exclusions:
    """
    Container for all exclusions
    """

    @staticmethod
    def init_input_exclusions_container():
        input_exclusions = dict(
            HEADER=[], HEADER_KEY=[], PARAMETER=[], COOKIE=[], BODY=[], QUERYSTRING=[]
        )

        # Aliases for the same source type
        input_exclusions["HEADER"] = input_exclusions["HEADER_KEY"]
        input_exclusions["MULTIPART_FORM_DATA"] = input_exclusions["BODY"]
        input_exclusions["MULTIPART_CONTENT_DATA"] = input_exclusions["BODY"]

        return input_exclusions

    def __init__(self, config: Mapping):
        active_modes = set()
        if config["assess.enable"]:
            active_modes.add("assess")
        if config["protect.enable"]:
            active_modes.add("defend")

        def active(exclusions):
            return (
                excl
                for excl in exclusions
                if set(excl.get("modes", {})).intersection(active_modes)
            )

        self.url_exclusions = [
            UrlExclusion(excl)
            for excl in active(config.get("application.url_exclusions", []))
        ]

        has_named_exclusion = False
        input_exclusions = self.init_input_exclusions_container()
        for exc in active(config.get("application.input_exclusions", [])):
            input_exclusions[exc.get("input_type")].append(InputExclusion(exc))
            has_named_exclusion = True
        self.input_exclusions = input_exclusions if has_named_exclusion else None

    def evaluate_assess_trigger_time_exclusions(self, context, finding):
        # returns True if we do not report finding
        return any(
            exc.match_in_finding(finding)
            for exc in context.input_exclusions_trigger_time
        )

    def evaluate_input_exclusions(
        self, context, source_type: str, source_name: str, mode=None
    ):
        # Evaluate all exclusions against the current source
        if context.input_exclusions is None:
            return False

        exclusions = context.input_exclusions.get(source_type, None)
        if exclusions is None:
            return False

        for exc in exclusions:
            if mode and mode not in exc.modes:
                continue

            if exc.match(
                context,
                source_type=source_type,
                source_name=source_name,
            ):
                logger.debug(
                    "The input exclusion rule named '%s' matched on the input name '%s' for the input type of '%s'",
                    exc.exclusion_name,
                    source_name,
                    exc.input_type,
                )
                return True

        return False

    def evaluate_input_exclusions_url(
        self, context, source_type: str, path: str, mode=None
    ):
        # Evaluate all exclusions against the current source
        if context.input_exclusions is None:
            return False

        exclusions = context.input_exclusions.get(source_type, None)
        if exclusions is None:
            return False

        for exc in exclusions:
            if mode and mode not in exc.modes:
                continue

            if exc.match_type == "ALL":
                logger.debug(
                    "The input url exclusion rule named '%s' matched on the path '%s' for the input type of '%s'",
                    exc.exclusion_name,
                    path,
                    exc.input_type,
                )
                return True

            for url_regex in exc.url_regexes:
                if url_regex.search(path):
                    logger.debug(
                        "The input url exclusion rule named '%s' matched on the path '%s' for the input type of '%s'",
                        exc.exclusion_name,
                        path,
                        exc.input_type,
                    )
                    return True

        return False

    def evaluate_url_exclusions(self, context, path: str) -> None:
        """
        This function evaluates all exclusions depending on the request URL and updates the request context to contain
        the list of disabled assess and protect rules to be evaluated at trigger time for url exclusions
        """
        for exc in self.url_exclusions:
            exc.evaluate(context, path)

    def set_input_exclusions_by_url(self, context, path: str):
        """
        Evaluates the set of input exclusions that apply to this path. Update request
        context with input exclusions to apply.
        """
        if self.input_exclusions is None:
            return

        context.input_exclusions = self.init_input_exclusions_container()
        context.input_exclusions_trigger_time = []

        has_match = False

        for input_type, exclusions in self.input_exclusions.items():
            for exc in exclusions:
                if exc.url_regexes and not any(
                    pattern.fullmatch(path) for pattern in exc.url_regexes
                ):
                    continue

                if exc.protect_rules or exc.assess_rules:
                    context.input_exclusions_trigger_time.append(exc)
                else:
                    context.input_exclusions[input_type].append(exc)

                has_match = True

        if not has_match:
            # No exclusions for this request
            context.input_exclusions = None


class BaseExclusion:
    def __init__(self, exclusion: Mapping):
        self.exclusion_name = exclusion.get("name")
        self.url_regexes = strs_to_regexes(exclusion.get("urls", []))

        self.protect_rules = exclusion.get("protect_rules", [])
        self.assess_rules = exclusion.get("assess_rules", [])

        self.match_type = exclusion.get("match_strategy")
        self.modes = exclusion.get("modes", [])


class InputExclusion(BaseExclusion):
    def __init__(self, exclusion: Mapping):
        super().__init__(exclusion)

        self.input_name_regex = None

        self.input_type: InputExclusionSourceType = getattr(
            InputExclusionSourceType,
            exclusion.get("input_type", ""),
            InputExclusionSourceType.UNKNOWN,
        )

        if self.input_type == InputExclusionSourceType.UNKNOWN:
            logger.error(
                "Invalid input exclusion type for the exclusion", exclusion=exclusion
            )

        if input_name := exclusion.get("input_name"):
            # Adding a check for type cookie to ignore case as per requirements
            # https://github.com/Contrast-Security-Inc/platform-specifications/blob/main/exclusions/EXCLUSIONS_INPUT.md
            flags = (
                re.IGNORECASE
                if self.input_type == InputExclusionSourceType.COOKIE
                else 0
            )
            self.input_name_regex = safe_re_compile(input_name, flags)

    def is_body_input_type(self, source_type: str):
        return self.input_type == InputExclusionSourceType.BODY or source_type in [
            "BODY",
            "MULTIPART_FORM_DATA",
            "MULTIPART_CONTENT_DATA",
        ]

    def is_querystring_input_type(self, source_type: str):
        return (
            self.input_type == InputExclusionSourceType.QUERYSTRING
            or source_type == "QUERYSTRING"
        )

    def match_in_finding(self, finding: AssessFinding):
        # pylint: disable=too-many-nested-blocks
        if finding.rule_id in self.assess_rules:
            for event in finding.events:
                if event.action == AssessEventAction.CREATION:
                    for trace_event in event.event_sources:
                        event_type = trace_event.source_type.name
                        event_src_name = trace_event.source_name

                        if event_type == self.input_type.name:
                            exclude = False

                            if (
                                self.input_name_regex is not None
                                and self.input_name_regex.fullmatch(event_src_name)
                            ):
                                exclude = True

                            if self.input_type in [
                                InputExclusionSourceType.QUERYSTRING,
                                InputExclusionSourceType.BODY,
                            ]:
                                exclude = True

                            if exclude:
                                logger.debug(
                                    "The input exclusion rule named '%s' matched on the input name '%s' for the input type of '%s' for the rule '%s'",
                                    self.exclusion_name,
                                    event_src_name,
                                    event_type,
                                    finding.rule_id,
                                )
                                return exclude

        return False

    def match(
        self,
        context,
        source_type: str | None = None,
        source_name: str | None = None,
    ):
        if source_name is None and self.input_type not in [
            InputExclusionSourceType.QUERYSTRING,
            InputExclusionSourceType.BODY,
        ]:
            return False

        if self.is_body_input_type(source_type) or self.is_querystring_input_type(
            source_type
        ):
            return True

        return self.input_name_regex.fullmatch(source_name) is not None


class UrlExclusion(BaseExclusion):
    @fail_loudly("Unable to ignore request", return_value=False)
    def evaluate(self, context, path: str):
        """
        Determine if the given path exactly matches any of the
        configured urls for this exclusion rule. This function modifies the
        request context to notify rules if they should be disabled for this url.

        @param context: request context
        @param path: path for current request
        @return This function returns True if a match was found
        @rtype: bool
        """
        for pattern in self.url_regexes:
            if pattern.fullmatch(path):
                logger.debug("Path %s matched on pattern %s", path, pattern)
                self.update_disabled_rules(context)
                return True

        return False

    def update_disabled_rules(self, context):
        if "assess" in self.modes:
            if self.assess_rules:
                context.excluded_assess_rules.extend(self.assess_rules)
            else:
                context.assess_enabled = False

        if "defend" in self.modes:
            if self.protect_rules:
                context.excluded_protect_rules.extend(self.protect_rules)
            else:
                context.protect_enabled = False
