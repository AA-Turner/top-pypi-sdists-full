from datetime import datetime
from typing import Mapping
from typing import Optional


class SinkContext:
    """
    SinkContext is a class that is used to pass context metadata
    to the `context` parameter of a SinkConfig
    """

    _secrets: Optional[Mapping[str, str]] = None
    feature_view_name: str
    feature_view_id: str
    workspace: str
    _start_time: datetime
    _end_time: datetime

    def __init__(
        self,
        feature_view_name: str,
        feature_view_id: str,
        workspace: str,
        start_time: datetime,
        end_time: datetime,
        secrets: Optional[Mapping[str, str]] = None,
    ) -> None:
        """
        Initialize the SinkContext object.

        :param secrets: A map that maps the secret name to the resolved secret value.
        """
        self.feature_view_name = feature_view_name
        self.feature_view_id = feature_view_id
        self.workspace = workspace
        self._secrets = secrets
        self._start_time = start_time
        self._end_time = end_time

    @property
    def secrets(self) -> Optional[Mapping[str, str]]:
        return self._secrets

    @property
    def start_time(self) -> datetime:
        return self._start_time

    @property
    def end_time(self) -> datetime:
        return self._end_time
