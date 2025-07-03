from enum import Enum


class ValidationBypassType(Enum):
    """
    ValidationBypassType enum for the different types of validation bypass vulnerabilities.

    These vulnerabilities focus on scenarios where the agent fails to properly validate,
    verify, or double-check the accuracy of outputs before presenting them.
    """

    UNVERIFIED_CLAIMS = "unverified_claims"
    FALSE_CONFIDENCE = "false_confidence"
    MISLEADING_RESPONSES = "misleading_responses"


# List of all available types for easy access
VALIDATION_BYPASS_TYPES = [
    ValidationBypassType.UNVERIFIED_CLAIMS,
    ValidationBypassType.FALSE_CONFIDENCE,
    ValidationBypassType.MISLEADING_RESPONSES,
]
