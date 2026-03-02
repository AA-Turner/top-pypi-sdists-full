
from pydantic import BaseModel, EmailStr
from .device import Device


class AuthenticationFactor(BaseModel):
    """
    An Authentication Factor object describes a category of methods used for
    identity verification in an authentication attempt.
    """

    factor_type_id: int

    # Recommended:
    factor_type: str | None = None
    device: Device | None = None # Device used to complete an authentication request.
    provider: str | None = None # The name of provider for an authentication factor.
    is_totp: bool | None = None
    is_hotp: bool | None = None

    # Optional:
    security_questions: list[str] | None = None
    phone_number: str | None = None # The phone number used for a telephony-based authentication
                                    # request.
    email_addr: EmailStr | None = None # The email address used in an email-based authentication
                                       # factor.
