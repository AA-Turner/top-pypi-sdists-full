from enum import Enum


class ReviewerProfileOEnum(str, Enum):
    CREATED = "created"
    USER_EMAIL = "user_email"
    USER_NAME = "user_name"
    VALUE_0 = "-created"
    VALUE_1 = "-user_email"
    VALUE_2 = "-user_name"

    def __str__(self) -> str:
        return str(self.value)
