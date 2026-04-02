from typing import Literal, cast

IncidentFeedbackRating = Literal[0, 1, 2, 3, 4]

INCIDENT_FEEDBACK_RATING_VALUES: set[IncidentFeedbackRating] = {
    0,
    1,
    2,
    3,
    4,
}


def check_incident_feedback_rating(value: int) -> IncidentFeedbackRating:
    if value in INCIDENT_FEEDBACK_RATING_VALUES:
        return cast(IncidentFeedbackRating, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {INCIDENT_FEEDBACK_RATING_VALUES!r}")
