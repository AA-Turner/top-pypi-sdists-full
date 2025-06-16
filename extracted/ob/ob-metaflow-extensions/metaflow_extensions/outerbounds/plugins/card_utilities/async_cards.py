from metaflow.metaflow_current import current
import sqlite3
from threading import Thread, Event
import time


class InfoCollectorThread(Thread):
    def __init__(
        self,
        interval=1,
        file_name=None,
        sqlite_fetch_func=None,  # Callable
    ):
        super().__init__()
        self._exit_event = Event()
        self._interval = interval
        assert file_name is not None, "file_name must be provided"
        self._file_name = file_name
        self.daemon = True
        self._data = {}
        self._has_errored = False
        self._current_error = None
        self.sqlite_fetch_func = sqlite_fetch_func

    def read(self):
        return self._data

    def has_errored(self):
        return self._has_errored

    def get_error(self):
        return self._current_error

    def _safely_load(self):
        try:
            conn = sqlite3.connect(self._file_name)
            data = self.sqlite_fetch_func(conn)
            return {"metrics": data}, None
        except FileNotFoundError as e:
            return {}, e
        except sqlite3.Error as e:
            return {}, e
        finally:
            conn.close()

    def run(self):
        while self._exit_event.is_set() is False:
            data, self._current_error = self._safely_load()
            if not self._current_error:
                self._data = data
            self._has_errored = True if self._current_error else False
            time.sleep(self._interval)

    def stop(self):
        self._exit_event.set()
        self.join()


class CardRefresher:

    CARD_ID = None

    def on_startup(self, current_card):
        raise NotImplementedError("make_card method must be implemented")

    def on_error(self, current_card, error_message):
        raise NotImplementedError("error_card method must be implemented")

    def on_update(self, current_card, data_object):
        raise NotImplementedError("update_card method must be implemented")

    def sqlite_fetch_func(self, conn):
        raise NotImplementedError("sqlite_fetch_func must be implemented")


class CardUpdaterThread(Thread):
    def __init__(
        self,
        card_refresher: CardRefresher,
        interval=1,
        file_name=None,
        collector_thread: InfoCollectorThread = None,
    ):
        super().__init__()
        self._exit_event = Event()
        self._interval = interval
        self._refresher = card_refresher
        self._file_name = file_name
        self._collector_thread = collector_thread
        self.daemon = True

    def run(self):
        if self._refresher.CARD_ID is None:
            raise ValueError("CARD_ID must be defined")
        current_card = current.card[self._refresher.CARD_ID]
        self._refresher.on_startup(current_card)
        while self._exit_event.is_set() is False:
            data = self._collector_thread.read()
            if self._collector_thread.has_errored():
                self._refresher.on_error(
                    current_card, self._collector_thread.get_error()
                )
            self._refresher.on_update(current_card, data)
            time.sleep(self._interval)

    def stop(self):
        self._exit_event.set()
        self._collector_thread.stop()
        self.join()


class AsyncPeriodicRefresher:
    def __init__(
        self,
        card_referesher: CardRefresher,
        updater_interval=1,
        collector_interval=1,
        file_name=None,
    ):
        assert card_referesher.CARD_ID is not None, "CARD_ID must be defined"
        self._collector_thread = InfoCollectorThread(
            interval=collector_interval,
            file_name=file_name,
            sqlite_fetch_func=card_referesher.sqlite_fetch_func,
        )
        self._collector_thread.start()
        self._updater_thread = CardUpdaterThread(
            card_refresher=card_referesher,
            interval=updater_interval,
            file_name=file_name,
            collector_thread=self._collector_thread,
        )

    def start(self):
        self._updater_thread.start()

    def stop(self):
        data = self._collector_thread.read()
        current_card = current.card[self._updater_thread._refresher.CARD_ID]
        self._updater_thread._refresher.on_update(current_card, data)
        self._updater_thread.stop()
        self._collector_thread.stop()
