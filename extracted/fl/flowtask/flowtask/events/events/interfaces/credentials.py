from abc import ABC
from typing import TypeVar
from typing_extensions import ParamSpec
from ....interfaces.mask import MaskSupport

P = ParamSpec("P")
T = TypeVar("T")


class CredentialsInterface(MaskSupport, ABC):
    def __init__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        super(CredentialsInterface, self).__init__(*args, **kwargs)
        self.credentials = self.set_credentials(kwargs.pop("credentials", {}))
        if not self.credentials:
            raise ValueError("Missing Credentials on Event Component")

    def set_credentials(self, credentials: dict):
        for key, default in credentials.items():
            try:
                # can process the credentials, extracted from environment or variables:
                val = self.get_env_value(credentials[key], default=default)
                if hasattr(self, "mask_replacement"):
                    val = self.mask_replacement(val)
                credentials[key] = val
            except (TypeError, KeyError) as ex:
                self._logger.error(f"{__name__}: Wrong or missing Credentias")
                raise ValueError(f"{__name__}: Wrong or missing Credentias") from ex
        return credentials
