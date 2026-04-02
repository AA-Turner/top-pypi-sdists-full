from nsj_queue_lib.client.socket_client import SocketClient

from nsj_sql_utils_lib.dbadapter3 import DBAdapter3


class LockClient:
    LOCK_ID_RETRY = 1
    LOCK_ID_PURGE = 2
    LOCK_ID_NOTIFY = 3

    SQL_LOCK = """
    SELECT pg_try_advisory_lock(%(value)s) as lock
    """

    SQL_UNLOCK = """
    SELECT pg_advisory_unlock(%(value)s)
    """

    def __init__(self, db: DBAdapter3, socket_client: SocketClient):
        self._db = db
        self._socket_client = socket_client

    def try_lock_retry(self) -> bool:
        return self.try_lock(LockClient.LOCK_ID_RETRY)

    def unlock_retry(self):
        self.unlock(LockClient.LOCK_ID_RETRY)

    def try_lock_purge(self) -> bool:
        return self.try_lock(LockClient.LOCK_ID_PURGE)

    def unlock_purge(self):
        self.unlock(LockClient.LOCK_ID_PURGE)

    def try_lock_notify(self) -> bool:
        return self.try_lock(LockClient.LOCK_ID_NOTIFY)

    def unlock_notify(self):
        self.unlock(LockClient.LOCK_ID_NOTIFY)

    def try_lock(self, value: int) -> bool:
        if self._socket_client is None:
            _, result = self._db.execute(LockClient.SQL_LOCK, value=value)
            return result[0]["lock"] or False
        else:
            return self._socket_client.try_lock(value)

    def unlock(self, value: int):
        if self._socket_client is None:
            self._db.execute(LockClient.SQL_UNLOCK, value=value)
        else:
            return self._socket_client.release_lock(value)
