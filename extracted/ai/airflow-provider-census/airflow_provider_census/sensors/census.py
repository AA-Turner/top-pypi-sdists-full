from airflow.sensors.base import BaseSensorOperator
from airflow.exceptions import AirflowException
from airflow_provider_census.hooks.census import CensusHook
try:
    from airflow.utils.decorators import apply_defaults
except ImportError: # airflow 3.0
    apply_defaults = lambda f: f

from airflow_provider_census.hooks.census import CensusHook


class CensusSensor(BaseSensorOperator):
    """Waits for sync to complete.


    :param sync_run_id: Census sync run ID
    :type sync_run_id: str
    :param census_conn_id: `Conn ID` of the Connection to be used to configure this hook.
    :type census_conn_id: str
    """

    template_fields = ['sync_run_id']

    @apply_defaults
    def __init__(self, sync_run_id, census_conn_id='census_default', **kwargs):
        super().__init__(**kwargs)
        self.sync_run_id = sync_run_id
        self.census_conn_id = census_conn_id
        self.hook = None

    def _get_hook(self) -> CensusHook:
        if self.hook is None:
            self.hook = CensusHook(census_conn_id=self.census_conn_id)
        return self.hook

    def poke(self, context):
        hook = self._get_hook()
        info = hook.get_sync_run_info(self.sync_run_id)
        status = info['status']

        if status == 'failed':
            raise AirflowException(
                'Census sync run {sync_run_id} failed with error: {error_message}'.format(
                    sync_run_id=self.sync_run_id,
                    error_message=info['error_message']
                )
            )
        else:
            return status == 'completed'
