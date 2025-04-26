from abc import ABC

from airflow.models import BaseOperator
from pycarlo.core import Session

from airflow_mcd.hooks.session_hook import SessionHook


class BaseMcdOperator(BaseOperator, ABC):
    def __init__(self, mcd_session_conn_id: str, *args, **kwargs):
        """
        Base Operator for MCD.

        :param mcd_session_conn_id: Connection ID for the MCD session.
        """
        super().__init__(*args, **kwargs)

        self.mcd_session_conn_id = mcd_session_conn_id

    def get_session(self) -> Session:
        """
        Gets session from hook.

        :return: MCD access session.
        """
        return SessionHook(mcd_session_conn_id=self.mcd_session_conn_id).get_conn()
