from datetime import date


class BadCredentialsException(Exception):
    def __init__(self) -> None:
        super(Exception, self).__init__("Could not log in, check the credentials")


class MissingCsrfTokenException(Exception):
    def __init__(self, found_cookies: dict) -> None:
        super(Exception, self).__init__(
            f"Login unsuccessful, no multipart cookie found, only found {found_cookies}, make sure credentials are correct")


class MissingConfigurationException(Exception):
    def __init__(self, missing_keys: list) -> None:
        super(Exception, self).__init__(
            f'Missing keys in configuration file, please verify that all of the following exist and are correct: {missing_keys}')


class IncorrectDesignAccessException(Exception):
    def __init__(self, object_type: str, correct_access_method: str) -> None:
        super().__init__(
            f"Selected Design Object was of type {object_type}, use {correct_access_method} method instead")


class MissingUrlProviderException(Exception):
    def __init__(self) -> None:
        super().__init__("Url Provider not initialized in Interactor")


class InvalidDateRangeException(Exception):
    def __init__(self, start_date: date, end_date: date) -> None:
        super().__init__(
            f"Start Date of {start_date.isoformat()} occurs after End Date of {end_date.isoformat()}")
        
class DisabledComponentException(Exception):
    def __init__(self, label: str) -> None:
        super().__init__(f"Cannot interact with disabled component with label '{label}'")

class IgnoredValidationException(Exception):
    def __init__(self, breadcrumb: str) -> None:
        super().__init__(f"At least one validation was found in the form {breadcrumb}")

class ComponentNotFoundException(Exception):
    pass


class InvalidComponentException(Exception):
    pass


class ChoiceNotFoundException(Exception):
    pass


class SiteNotFoundException(Exception):
    pass


class PageNotFoundException(Exception):
    pass


class InvalidSiteException(Exception):
    pass
