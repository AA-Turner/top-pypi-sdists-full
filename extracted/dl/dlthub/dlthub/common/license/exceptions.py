from typing import Iterable
from dlthub.common.exceptions import DltPlusException


class DltLicenseException(DltPlusException):
    pass


class DltUnknownScopeException(DltLicenseException):
    def __init__(self, scope: str) -> None:
        super().__init__(f"Unknown scope: {scope}")


class DltLicenseExpiredException(DltLicenseException):
    def __init__(self) -> None:
        super().__init__("Your dlt License has expired.")


class DltLicenseSignatureInvalidException(DltLicenseException):
    def __init__(self) -> None:
        super().__init__("Your dlt License has an invalid signature.")


class DltLicenseScopeInvalidException(DltLicenseException):
    def __init__(self, scope: str, scopes: Iterable[str]) -> None:
        self.scope = scope
        self.scopes = scopes
        super().__init__(
            f"Your dlt License does not have the required scope: {scope}. "
            f"Available scopes: {scopes}\n\n"
            "You can self-issue an anonymous trial license to extend the list of scopes\n\n"
            f"dlt license issue {scope}"
        )


class DltLicenseFeatureScopeFormatInvalid(DltLicenseException):
    def __init__(self, scope: str):
        super().__init__(
            f"Feature scope {scope} has invalid format. Please use `package.feature` format when "
            "requiring license via decorator."
        )


class DltLicenseNotFoundException(DltLicenseException):
    def __init__(self) -> None:
        super().__init__()
        self.required_scope: str = None
        self.feature: str = None

    def set_scope(self, required_scope: str, feature: str) -> None:
        """Adds scope and feature info for nicer error message"""
        self.required_scope = required_scope
        self.feature = feature

    def __str__(self) -> str:
        if self.required_scope:
            for_scope = f" for {self.required_scope} ({self.feature})."
        else:
            for_scope = ""

        return f"""

Could not find a dlt license {for_scope}
Please provide your license in the RUNTIME__LICENSE environment variable
or in your local or global secrets.toml file:

[runtime]
license="1234"

Alternatively you can self-issue an anonymous trial license and use it for development, testing and
ci ops:

dlt license issue {self.required_scope or "<scope>"}
"""


class DltPrivateKeyNotFoundException(DltLicenseException):
    def __init__(self) -> None:
        super().__init__(
            """

Could not find private key for signing. Please provide the private key in
your local or global secrets.toml file:

[runtime]
license_private_key="1234"
"""
        )


class DltLicenseSelfSignedSubInvalid(DltLicenseException):
    def __init__(self, sub: str, host_id: str, anonymous_id: str):
        super().__init__(
            f"Self signed license is bound to the following hostname:anonymous_id `{sub}`."
            f"Actual values are: `{host_id}:{anonymous_id}`. This may happen if you "
            "(1) transferred license to another machine (2) cleaned up dlt global dir (ie. ~/.dlt) "
            "where anonymous id is stored (3) changed the host name. Regenerate the license with "
            "`dlt license issue` command"
        )
