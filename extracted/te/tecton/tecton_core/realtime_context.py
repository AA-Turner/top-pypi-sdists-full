from datetime import datetime
from typing import Any
from typing import Mapping
from typing import Optional

import pandas

from tecton_proto.args.transformation__client_pb2 import TransformationMode


REQUEST_TIMESTAMP_FIELD_NAME = "request_timestamp"

VALID_TRANSFORMATION_MODES = {
    TransformationMode.TRANSFORMATION_MODE_PYTHON,
    TransformationMode.TRANSFORMATION_MODE_PANDAS,
    TransformationMode.TRANSFORMATION_MODE_NO_TRANSFORMATION,
}


class RealtimeContext:
    """
    RealtimeContext is a class that is used to pass context metadata such as the request_timestamp
    to the `context` parameter of a Realtime Feature Views.
    """

    _mode: Optional[TransformationMode.ValueType] = None
    _request_timestamp: Optional[datetime] = None
    _row_level_data: Optional[pandas.DataFrame] = None
    _secrets: Optional[Mapping[str, str]] = None
    _resources: Optional[Mapping[str, Any]] = None

    def __init__(
        self,
        secrets: Optional[Mapping[str, str]] = None,
        resources: Optional[Mapping[str, Any]] = None,
        request_timestamp: Optional[datetime] = None,
        _row_level_data: Optional[pandas.DataFrame] = None,
        _mode: Optional[TransformationMode.ValueType] = None,
    ) -> None:
        """
        Initialize the RealtimeContext object.

        :param secrets: A map that maps the secret name to the resolved secret value.
        :param resources: A map that maps the resource name to the resource returned by the resource provider.
        :param request_timestamp: The timestamp of the request made to the Tecton Feature Server. Used for Python mode offline and for both modes online.
        :param _mode: Realtime Feature View mode. Valid modes: Python, Pandas, No Transformation.
        :param _row_level_data: The row-level context data for the Realtime Feature View for each row in the events data frame. Only populated in Pandas mode during Offline Retrieval.
        """
        self._mode = _mode
        self._request_timestamp = request_timestamp
        self._row_level_data = _row_level_data
        self._secrets = secrets
        self._resources = resources
        self._current_row_index = -1

    def __str__(self) -> str:
        return (
            f"RealtimeContext(mode={self._mode}, "
            f"request_timestamp={self._request_timestamp}, "
            f"has_row_level_data={self._row_level_data is not None}, "
            f"secrets={self._secrets}, "
            f"resources={self._resources})"
        )

    def set_mode(self, mode: TransformationMode.ValueType) -> None:
        """
        Set the mode of the Realtime Feature View.

        :param mode: Mode of the Realtime Feature View.
        """
        assert mode in VALID_TRANSFORMATION_MODES, f"Mode {mode} is not a valid transformation mode."
        self._mode = mode

    def set_request_timestamp(self, request_timestamp: datetime) -> None:
        """
        Set the request_timestamp for the Realtime Feature View.

        :param request_timestamp: The timestamp of the request made to the Tecton Feature Server.
        """
        self._request_timestamp = request_timestamp

    @property
    def request_timestamp(self) -> Optional[datetime]:
        """
        The request_timestamp is the timestamp of the request made to the Tecton Feature Server.
        """
        if self._mode not in [
            TransformationMode.TRANSFORMATION_MODE_PYTHON,
            TransformationMode.TRANSFORMATION_MODE_NO_TRANSFORMATION,
        ]:
            str = "The field `request_timestamp` is not available in Realtime Feature Views with Pandas mode. Please use `context.request_timestamp_series` when using Pandas mode."
            raise ValueError(str)

        if self._row_level_data is not None and self._current_row_index is not None:
            return self._row_level_data[REQUEST_TIMESTAMP_FIELD_NAME][self._current_row_index]

        return self._request_timestamp

    @property
    def request_timestamp_series(self) -> Optional[pandas.Series]:
        """
        The request_timestamp_series is a pandas Series with the request_timestamp as the only element. Each element in the
        Series is the request_timestamp for the corresponding row in the input data.
        """
        if self._mode != TransformationMode.TRANSFORMATION_MODE_PANDAS:
            str = "The field `request_timestamp_series` is only available in Realtime Feature Views with Pandas mode. Please use `context.request_timestamp` when using Python mode or when no transformations are present."
            raise ValueError(str)

        # For online retrieval, we build a Series with the request_timestamp as the only element
        if self._request_timestamp is not None:
            return pandas.Series([self._request_timestamp], name=REQUEST_TIMESTAMP_FIELD_NAME)

        if self._row_level_data is None:
            return None

        return self._row_level_data[REQUEST_TIMESTAMP_FIELD_NAME]

    @property
    def secrets(self) -> Optional[Mapping[str, str]]:
        return self._secrets

    @property
    def resources(self) -> Optional[Mapping[str, Any]]:
        return self._resources

    def __iter__(self) -> "RealtimeContext":
        # Making RealtimeContext an iterator allows us to iterate over the rows in the row_level_data dataframe
        # in Python mode.
        self._current_row_index = -1
        return self

    def __next__(self) -> "RealtimeContext":
        self._current_row_index += 1

        if self._row_level_data is not None and self._current_row_index >= len(self._row_level_data):
            raise StopIteration

        return self
