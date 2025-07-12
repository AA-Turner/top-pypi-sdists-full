from typing import Any
from typing import Mapping
from typing import Optional


class MockContext:
    """
    MockContext is a class that is used to pass mock context metadata such as secrets and resources for
    testing.
    """

    _secrets: Optional[Mapping[str, str]] = None
    _resources: Optional[Mapping[str, Any]] = None

    def __init__(
        self,
        secrets: Optional[Mapping[str, str]] = None,
        resources: Optional[Mapping[str, Any]] = None,
    ) -> None:
        """
        Initialize the MockContext object.

        Example:
        ```python
        MockContext(
            secrets={"my_api_key": "1234567890"},
            resources={"my_resource": {"client_version": "1.0.0"}}
        )
        ```

        :param secrets: A map that maps the secret name to the resolved secret value.
        :param resources: A map that maps the resource name to the resource returned by the resource provider.
        """
        self._secrets = secrets
        self._resources = resources

    def __str__(self) -> str:
        return f"MockContext(secrets={self._secrets}, resources={self._resources})"

    @property
    def secrets(self) -> Optional[Mapping[str, str]]:
        return self._secrets

    @property
    def resources(self) -> Optional[Mapping[str, Any]]:
        return self._resources
