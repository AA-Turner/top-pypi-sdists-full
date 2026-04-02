from typing import Literal, cast

UpdateIncidentFeedbackDataAttributesRating = Literal[0, 1, 2, 3, 4]

UPDATE_INCIDENT_FEEDBACK_DATA_ATTRIBUTES_RATING_VALUES: set[UpdateIncidentFeedbackDataAttributesRating] = {
    0,
    1,
    2,
    3,
    4,
}


def check_update_incident_feedback_data_attributes_rating(value: int) -> UpdateIncidentFeedbackDataAttributesRating:
    if value in UPDATE_INCIDENT_FEEDBACK_DATA_ATTRIBUTES_RATING_VALUES:
        return cast(UpdateIncidentFeedbackDataAttributesRating, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {UPDATE_INCIDENT_FEEDBACK_DATA_ATTRIBUTES_RATING_VALUES!r}"
    )
