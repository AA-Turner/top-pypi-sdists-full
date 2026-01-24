try:
    from airflow.models import BaseOperator
except ImportError: # airflow 3.0
    from airflow.providers.standard.operators.base import BaseOperator

try:
    from airflow.utils.decorators import apply_defaults
except ImportError: # airflow 3.0
    apply_defaults = lambda f: f

from typing import Any

from airflow_provider_census.hooks.census import CensusHook


class CensusOperator(BaseOperator):
    """Triggers sync with Census API.

    :param sync_id: Census sync ID
    :type sync_id: int
    :param census_conn_id: `Conn ID` of the Connection to be used to configure this hook.
    :type census_conn_id: str
    """

    @apply_defaults
    def __init__(self, sync_id: int, census_conn_id: str = 'census_default', **kwargs):
        super().__init__(**kwargs)
        self.sync_id = sync_id
        self.census_conn_id = census_conn_id

    def _get_hook(self) -> CensusHook:
        return CensusHook(census_conn_id=self.census_conn_id)

    def execute(self, context) -> Any:
        hook = self._get_hook()

        return hook.trigger_sync(self.sync_id)
