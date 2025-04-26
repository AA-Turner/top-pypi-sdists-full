from typing import Mapping
from typing import Optional


class ResourceProviderContext:
    """
    ResourceProviderContext is a class that is used to pass context metadata
    to the `context` parameter of a Resource Provider
    """

    _secrets: Optional[Mapping[str, str]] = None

    def __init__(
        self,
        secrets: Optional[Mapping[str, str]] = None,
    ) -> None:
        """
        Initialize the ResourceProviderContext object.

        :param secrets: A map that maps the secret name to the resolved secret value.
        """
        self._secrets = secrets

    @property
    def secrets(self) -> Optional[Mapping[str, str]]:
        return self._secrets
