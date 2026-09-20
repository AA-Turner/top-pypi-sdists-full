import os
import threading
import time


class SafeMapFIFO:
    def __init__(self, max_length: int = 100, default_expiration_sec: int = 60):
        self.map = {}
        self.lock = threading.Lock()
        self._pid = os.getpid()
        self._fork_locks = {self._pid: self.lock}
        self.max_length = max_length
        self.default_expiration_sec = default_expiration_sec

    def _ensure_fork_safe(self):
        current_pid = os.getpid()
        if self._pid == current_pid:
            return
        lock = self._fork_locks.setdefault(current_pid, threading.Lock())
        with lock:
            if self._pid == current_pid:
                return
            # The inherited lock may be held by a vanished parent thread, and
            # a cache update may have been interrupted. Rebuild both in the child.
            self.map = {}
            self.lock = lock
            self._pid = current_pid

    def _clean_expired_keys(self):
        self._ensure_fork_safe()
        current_time = time.time()
        with self.lock:
            keys_to_delete = [key for key, value in self.map.items() if
                              current_time - value['insert_time'] > value['expiration']]
            for key in keys_to_delete:
                del self.map[key]

    def put(self, key, value, expiration_time=None):
        self._ensure_fork_safe()
        with self.lock:
            if len(self.map) >= self.max_length:
                # 达到最大长度，删除最早插入的元素
                oldest_key = min(self.map.keys(), key=lambda k: self.map[k]['insert_time'])
                del self.map[oldest_key]
            now = time.time()
            expiration = expiration_time if expiration_time else self.default_expiration_sec
            self.map[key] = {'value': value, 'insert_time': now, 'expiration': expiration}

    def get(self, key):
        self._ensure_fork_safe()
        with self.lock:
            if key in self.map:
                item = self.map[key]
                if time.time() - item['insert_time'] <= item['expiration']:
                    return item['value']
                else:
                    del self.map[key]  # 过期删除
            return None

    def delete(self, key):
        self._ensure_fork_safe()
        with self.lock:
            if key in self.map:
                del self.map[key]

    def has_key(self, key):
        self._ensure_fork_safe()
        with self.lock:
            return key in self.map

    def items(self):
        self._ensure_fork_safe()
        with self.lock:
            current_time = time.time()
            return [(k, v['value']) for k, v in self.map.items() if current_time - v['insert_time'] <= v['expiration']]
