from pydantic import ValidationError
from pydantic_settings import BaseSettings

from ._base import Check, CheckResult


class SettingsCheck(Check):
    _name: str
    _settings_class: type[BaseSettings]

    def __init__(self, name: str, settings_class: type[BaseSettings]):
        self._name = name
        self._settings_class = settings_class

    async def __call__(self) -> CheckResult:
        try:
            self._settings_class()
            return CheckResult(name=self._name, passed=True)
        except ValidationError as error:
            return CheckResult(name=self._name, passed=False, details=error.json())
        except Exception as exception:
            return CheckResult(name=self._name, passed=False, details=str(exception))
