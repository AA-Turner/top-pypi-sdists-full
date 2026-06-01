from typing import Literal, cast

EmailResourceType = Literal["email"]

EMAIL_RESOURCE_TYPE_VALUES: set[EmailResourceType] = {
    "email",
}


def check_email_resource_type(value: str) -> EmailResourceType:
    if value in EMAIL_RESOURCE_TYPE_VALUES:
        return cast(EmailResourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {EMAIL_RESOURCE_TYPE_VALUES!r}")
