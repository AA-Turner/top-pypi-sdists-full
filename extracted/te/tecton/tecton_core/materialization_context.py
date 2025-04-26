import typing
from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from typeguard import typechecked

import tecton_core.tecton_pendulum as pendulum
from tecton_core.errors import TectonValidationError


if typing.TYPE_CHECKING:
    import pyspark


class MaterializationContext:
    """
    MaterializationContext is a class that holds the context with relevant metadata, secrets, and resources for a materialization job.
    """

    _start_time: Optional[datetime]
    _end_time: Optional[datetime]
    _batch_schedule: timedelta
    _resources: Optional[Dict[str, Any]] = None
    _secrets: Optional[Dict[str, str]] = None

    def __init__(
        self,
        batch_schedule: Optional[timedelta] = None,
        secrets: Optional[Dict[str, str]] = None,
        resources: Optional[Dict[str, Any]] = None,
        _start_time: Optional[datetime] = None,
        _end_time: Optional[datetime] = None,
    ) -> None:
        """
        Initialize the MaterializationContext object.

        :param _start_time: The start time of the materialization job.
        :param _end_time: The end time of the materialization job.
        :param batch_schedule: The batch schedule of the Feature View.
        :param secrets: A map that maps the secret name to the resolved secret value.
        :param resources: A map that maps the resource name to the resource returned by the resource provider.
        """
        self._start_time = _start_time
        self._end_time = _end_time
        self._batch_schedule = batch_schedule
        self._secrets = secrets
        self._resources = resources

    @property
    def start_time(self) -> Optional[datetime]:
        return self._start_time

    @property
    def end_time(self) -> Optional[datetime]:
        return self._end_time

    @property
    def end_time_inclusive(self) -> Optional[datetime]:
        if self._end_time is None:
            return None

        return self._end_time - timedelta(microseconds=1)

    @property
    def batch_schedule(self) -> timedelta:
        return self._batch_schedule

    @property
    def secrets(self) -> Optional[Dict[str, str]]:
        return self._secrets

    @property
    def resources(self) -> Optional[Dict[str, Any]]:
        return self._resources

    @typechecked
    def time_filter_sql(self, timestamp_expr: str) -> str:
        """
        Returns a SQL string that filters the timestamp_expr based on the context's start_time and end_time.

        :param timestamp_expr: The timestamp expression to filter.
        """
        # Use atom string to include the timezone.
        return f"('{self.start_time.isoformat()}' <= ({timestamp_expr}) AND ({timestamp_expr}) < '{self.end_time.isoformat()}')"

    def time_filter_pyspark(self, timestamp_expr: Union[str, "pyspark.sql.Column"]) -> "pyspark.sql.Column":  # type: ignore
        """
        Returns a PySpark Column that filters the timestamp_expr based on the context's start_time and end_time.

        :param timestamp_expr: The timestamp expression to filter.
        """

        from pyspark.sql.functions import expr
        from pyspark.sql.functions import lit

        if isinstance(timestamp_expr, str):
            timestamp_expr = expr(timestamp_expr)

        # Use atom string to include the timezone.
        return (lit(self.start_time.isoformat()) <= timestamp_expr) & (timestamp_expr < lit(self.end_time.isoformat()))

    def feature_time_filter_pyspark(self, timestamp_expr: Union[str, "pyspark.sql.Column"]) -> "pyspark.sql.Column":  # type: ignore
        """
        Returns a PySpark Column that filters the timestamp_expr based on the context's start_time and end_time.

        :param timestamp_expr: The timestamp expression to filter.
        """
        return self.time_filter_pyspark(timestamp_expr)

    # Everything below is deprecated but kept for backwards compatibility since Snowflake Materialization Runtime
    # is not versioned.
    @property
    def feature_start_time(self) -> datetime:
        return self._start_time

    @property
    def feature_end_time(self) -> datetime:
        return self._end_time

    @property
    def feature_start_time_string(self) -> str:
        return self.feature_start_time.isoformat()

    @property
    def feature_end_time_string(self) -> str:
        return self.feature_end_time.isoformat()

    @typechecked
    def feature_time_filter_sql(self, timestamp_expr: str) -> str:
        """
        Returns a SQL string that filters the timestamp_expr based on the context's start_time and end_time.

        :param timestamp_expr: The timestamp expression to filter.
        """
        return self.time_filter_sql(timestamp_expr)

    @classmethod
    def _create_internal(
        cls,
        start_time: Optional[pendulum.DateTime],
        end_time: Optional[pendulum.DateTime],
        batch_schedule: Optional[pendulum.Duration],
    ) -> "MaterializationContext":
        """
        Deprecated. Should be removed with the removal of Tecton on Snowflake.
        """
        start_dt = datetime.fromtimestamp(start_time.timestamp(), pendulum.tz.UTC)
        end_dt = datetime.fromtimestamp(end_time.timestamp(), pendulum.tz.UTC)

        # should only be used in pipeline_helper
        return MaterializationContext(
            _start_time=start_dt,
            _end_time=end_dt,
            batch_schedule=batch_schedule.as_timedelta(),
        )

    @classmethod
    def _create_from_period(
        cls, feature_time_limits: Optional[pendulum.Period], batch_schedule: pendulum.Duration
    ) -> "MaterializationContext":
        feature_start_time = (
            feature_time_limits.start
            if feature_time_limits is not None
            else pendulum.from_timestamp(0, pendulum.tz.UTC)
        )
        feature_end_time = feature_time_limits.end if feature_time_limits is not None else pendulum.datetime(2100, 1, 1)

        start_dt = datetime.fromtimestamp(feature_start_time.timestamp(), pendulum.tz.UTC)
        end_dt = datetime.fromtimestamp(feature_end_time.timestamp(), pendulum.tz.UTC)

        return MaterializationContext(
            _start_time=start_dt,
            _end_time=end_dt,
            batch_schedule=batch_schedule.as_timedelta(),
        )


@dataclass
class UnboundMaterializationContext(MaterializationContext):
    """
    Deprecated. Should be removed with the removal of `context=materialization_context()`

    This is only meant for instantiation in transformation default args. Using it directly will fail.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def batch_schedule(self):
        msg = "tecton.materialization_context() must be passed in via a kwarg default only. Instantiation in function body is not allowed."
        raise TectonValidationError(msg)

    @property
    def start_time(self):
        msg = "tecton.materialization_context() must be passed in via a kwarg default only. Instantiation in function body is not allowed."
        raise TectonValidationError(msg)

    @property
    def end_time(self):
        msg = "tecton.materialization_context() must be passed in via a kwarg default only. Instantiation in function body is not allowed."
        raise TectonValidationError(msg)

    @property
    def feature_start_time(self):
        msg = "tecton.materialization_context() must be passed in via a kwarg default only. Instantiation in function body is not allowed."
        raise TectonValidationError(msg)

    @property
    def feature_end_time(self):
        msg = "tecton.materialization_context() must be passed in via a kwarg default only. Instantiation in function body is not allowed."
        raise TectonValidationError(msg)


def materialization_context():
    """
    Deprecated. Should be removed after Tecton 1.1.

    Used as a default value for a Feature View or Transformation with a materialization context parameter.

    ``context.start_time`` and ``context.end_time`` return a `datetime.datetime` object equal to the beginning and end of the period being materialized respectively. For example for a batch feature view materializing data from May 1st, 2022, ``context.start_time = datetime(2022, 5, 1)`` and ``context.end_time = datetime(2022, 5, 2)``.

    The datetimes can be used in SQL query strings directly (the datetime object will be cast to an atom-formatted timestamp string and inlined as a constant in the SQL query).

    Example usage:

    .. code-block:: python

        from tecton import batch_feature_view, materialization_context
        from datetime import datetime, timedelta

        @batch_feature_view(
            sources=[transactions],
            entities=[user],
            mode='spark_sql',
            features=[Attribute("AMOUNT", Float64)],
            batch_schedule=timedelta(days=1),
            feature_start_time=datetime(2020, 10, 10),
        )
        def user_last_transaction_amount(transactions, context=materialization_context()):
            return f'''
                SELECT
                    USER_ID,
                    AMOUNT,
                    TIMESTAMP
                FROM
                    {transactions}
                WHERE TIMESTAMP >= TO_TIMESTAMP("{context.start_time}") -- e.g. TO_TIMESTAMP("2022-05-01T00:00:00+00:00")
                    AND TIMESTAMP < TO_TIMESTAMP("{context.end_time}") -- e.g. TO_TIMESTAMP("2022-05-02T00:00:00+00:00")
                '''
    """
    dummy_time = pendulum.datetime(1970, 1, 1)
    dummy_period = timedelta()
    return UnboundMaterializationContext(
        _start_time=dummy_time,
        _end_time=dummy_time,
        batch_schedule=dummy_period,
    )
