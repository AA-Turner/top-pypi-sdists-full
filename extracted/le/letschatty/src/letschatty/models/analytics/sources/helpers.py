from ...utils.types.source_types import SourceType, SourceCheckerType, get_label, get_description
from typing import Type, List

SOURCE_CHECKER_MAPPING = {
    SourceType.OTHER_SOURCE: [SourceCheckerType.SIMILARITY, SourceCheckerType.LITERAL, SourceCheckerType.SMART_MESSAGES],
    SourceType.PURE_AD: [SourceCheckerType.REFERRAL],
    SourceType.WHATSAPP_DEFAULT_SOURCE: [SourceCheckerType.FIRST_CONTACT],
    SourceType.TOPIC_DEFAULT_SOURCE: [SourceCheckerType.SMART_MESSAGES],
    SourceType.UTM_SOURCE: [SourceCheckerType.CHATTY_PIXEL],
    SourceType.PURE_AD_UTM_SOURCE: [SourceCheckerType.AD_ID_IN_UTM_PARAMS],
    SourceType.GOOGLE_AD_UTM_SOURCE: [SourceCheckerType.AD_ID_IN_UTM_PARAMS],
    SourceType.TEMPLATE_SOURCE: [SourceCheckerType.TEMPLATE]
}

class SourceHelpers:
    @staticmethod
    def is_valid_source_checker(source_type: SourceType, source_checker: SourceCheckerType) -> bool:
        return source_checker in SOURCE_CHECKER_MAPPING[source_type]

    @staticmethod
    def get_source_checkers(source_type: SourceType) -> List[dict]:
        source_checkers : List[SourceCheckerType] = SOURCE_CHECKER_MAPPING[source_type]
        return [{"type": source_checker.value, "label": get_label(source_checker), "description": get_description(source_checker)} for source_checker in source_checkers]
