from typing import Optional

from nexuscli.nexus_http import NexusHttp


# When Python 3.6 is deprecated, switch to data class?
class BaseModel:
    """
    Base class for Nexus 3 server objects.

    Args:
        nexus_http: the NexusHttp client instance that will be used to perform operations against
        the Nexus 3 service. You must provide this at instantiation if you plan on calling any
        methods that require connectivity to Nexus.
    """
    def __init__(self, nexus_http: Optional[NexusHttp] = None, **kwargs):
        self.name: str = kwargs['name']
        self._client: Optional[NexusHttp] = nexus_http
        self._raw: dict = kwargs
        self._validate_params()

    def _validate_params(self) -> None:
        if not isinstance(self._raw.get('name'), str) or not self._raw.get('name'):
            raise KeyError('name must be a non-empty str')

    @property
    def configuration(self) -> dict:
        """
        The model representation as a transformed python dict suitable for converting to JSON and
        passing-through to the Nexus 3 API.
        """
        self._raw.update({'name': self.name})
        return self._raw
