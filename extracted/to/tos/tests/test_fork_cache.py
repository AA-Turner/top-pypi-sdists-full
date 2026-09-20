import multiprocessing
import os
import threading
import time
import traceback
import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest import mock

import tos
from tests.common import MockResponse
from tos.safe_map import SafeMapFIFO
from tos.utils import DnsCacheService


def _bucket_lookup_in_child(conn, client):
    try:
        old_cache = client.bucket_type_cache
        old_lock = old_cache.lock
        response = MockResponse(headers={'content-length': '0', 'x-tos-bucket-type': 'hns'})
        with mock.patch('requests.Session.request', return_value=response):
            with ThreadPoolExecutor(max_workers=8) as pool:
                results = list(pool.map(lambda _: client.get_bucket_type('bucket123'), range(16)))
        conn.send({
            'ok': True,
            'types': [result.bucket_type for result in results],
            'new_lock': client.bucket_type_cache.lock is not old_lock,
            'parent_entry_cleared': client.bucket_type_cache.get('parent-only') is None,
            'settings': (client.bucket_type_cache.max_length, client.bucket_type_cache.default_expiration_sec),
        })
        client.close()
    except Exception:
        conn.send({'ok': False, 'traceback': traceback.format_exc()})
    finally:
        conn.close()


def _close_client_in_child(conn, client):
    try:
        old_session = client.session
        client.close()
        conn.send({'ok': True, 'new_session': client.session is not old_session,
                   'child_pid': client._session_pid == os.getpid()})
    except Exception:
        conn.send({'ok': False, 'traceback': traceback.format_exc()})
    finally:
        conn.close()


def _map_operation_in_child(conn, cache, operation):
    try:
        old_lock = cache.lock
        args = {'put': ('child-only', 'child-value'), 'get': ('parent-only',),
                'delete': ('parent-only',), 'has_key': ('parent-only',),
                'items': (), '_clean_expired_keys': ()}
        # This must be the first cache operation in the child.
        value = getattr(cache, operation)(*args[operation])
        conn.send({'ok': True, 'value': value, 'new_lock': cache.lock is not old_lock,
                   'child_pid': cache._pid == os.getpid(), 'items': cache.items(),
                   'settings': (cache.max_length, cache.default_expiration_sec)})
    except Exception:
        conn.send({'ok': False, 'traceback': traceback.format_exc()})
    finally:
        conn.close()


def _inactive_dns_in_child(conn, cache, operation):
    try:
        old_lock = cache.async_lock
        config = cache._refresh_config
        with mock.patch.object(threading.Thread, 'start') as start:
            if operation == 'add':
                entry = cache.add('child.example', 443, ['child-ip'], int(time.time()) + 60)
                assert entry.ip_list == ['child-ip']
            else:
                assert cache.get_ip_list('parent.example', 443) is None
            conn.send({'ok': True, 'new_lock': cache.async_lock is not old_lock,
                       'child_pid': cache._pid == os.getpid(),
                       'parent_entry_cleared': cache.get_ip_list('parent.example', 443) is None,
                       'child_entry': cache.get_ip_list('child.example', 443) is not None,
                       'inactive': cache.is_shutdown and not cache.async_started,
                       'thread_starts': start.call_count,
                       'config_preserved': cache._refresh_config == config})
    except Exception:
        conn.send({'ok': False, 'traceback': traceback.format_exc()})
    finally:
        conn.close()


def _dns_in_child(conn, cache, mode):
    try:
        old_lock = cache.async_lock
        refreshed = threading.Event()
        refresh_threads = set()
        started = []
        original_start = threading.Thread.start

        def record_start(thread):
            if getattr(thread._target, '__name__', '') == '_refresh_cache':
                started.append(thread)
            return original_start(thread)

        def resolve(host, port):
            refresh_threads.add(threading.get_ident())
            refreshed.set()
            return ['refreshed-ip']

        refresh_start = time.time()
        with mock.patch('tos.utils.resolve_ip_list', side_effect=resolve), \
                mock.patch.object(threading.Thread, 'start', record_start), \
                mock.patch('tos.clientv2._dns_cache', cache), \
                mock.patch('tos.clientv2.connection.create_connection'):
            client = None
            if mode == 'shutdown':
                cache.shutdown()
                restart_owner = False
            elif mode == 'new-client':
                # Exercise _open_dns_cache when constructing a client after fork.
                original_refresh = cache.async_refresh_cache
                with mock.patch.object(cache, 'async_refresh_cache',
                                       side_effect=lambda ttl: original_refresh(ttl, interval=0.01)):
                    client = tos.TosClientV2(endpoint='https://example.com', region='cn-beijing',
                                             dns_cache_time=1)
                restart_owner = client._start_async_refresh_cache
            elif mode == 'add':
                cache.add('child.example', 443, ['initial-ip'], int(time.time()) + 1)
                restart_owner = False
            else:
                # The inherited connection hook accesses this shared service directly.
                with ThreadPoolExecutor(max_workers=8) as pool:
                    list(pool.map(lambda _: cache.get_ip_list('parent.example', 443), range(16)))
                restart_owner = False

            cleared = cache.get_ip_list('parent.example', 443) is None
            if mode != 'shutdown':
                cache.add('child.example', 443, ['initial-ip'], int(time.time()) + 1)
                if not refreshed.wait(2):
                    raise AssertionError('DNS refresh thread did not run in child')
            if client is not None:
                client.close()
            else:
                cache.shutdown()
            for thread in started:
                thread.join(2)
            # The resolver event fires before the worker writes its result.
            # Joining the worker makes this assertion cover the completed write.
            entry = cache.get_ip_list('child.example', 443)
            if mode != 'shutdown':
                assert entry is not None and entry.ip_list == ['refreshed-ip']
                assert refresh_start + 60 <= entry.expire <= time.time() + 60
                assert not entry.immortal
            conn.send({
                'ok': True,
                'new_lock': cache.async_lock is not old_lock,
                'parent_entry_cleared': cleared,
                'refresh_thread_count': len(started),
                'refresh_ran_in_background': bool(refresh_threads) and
                    threading.get_ident() not in refresh_threads,
                'threads_stopped': all(not thread.is_alive() for thread in started),
                'restart_owner': restart_owner,
                'shutdown': cache.is_shutdown and not cache.async_started,
            })
    except Exception:
        conn.send({'ok': False, 'traceback': traceback.format_exc()})
    finally:
        conn.close()


@unittest.skipUnless('fork' in multiprocessing.get_all_start_methods(), 'fork is unavailable')
class TestForkCache(unittest.TestCase):
    def _run_child_while_locked(self, lock, target, *args):
        ready = threading.Event()
        release = threading.Event()

        def hold():
            with lock:
                ready.set()
                release.wait()

        holder = threading.Thread(target=hold, daemon=True)
        holder.start()
        ctx = multiprocessing.get_context('fork')
        parent_conn, child_conn = ctx.Pipe(duplex=False)
        proc = ctx.Process(target=target, args=(child_conn,) + args)
        try:
            self.assertTrue(ready.wait(2))
            proc.start()
            child_conn.close()
            self.assertTrue(parent_conn.poll(5), 'child hung with an inherited cache lock')
            result = parent_conn.recv()
            self.assertTrue(result['ok'], result.get('traceback'))
            proc.join(2)
            self.assertEqual(proc.exitcode, 0)
            return result
        finally:
            if proc.pid is not None:
                if proc.is_alive():
                    proc.terminate()
                proc.join(2)
            release.set()
            holder.join(2)
            parent_conn.close()
            child_conn.close()

    def test_each_map_entry_point_after_fork_with_parent_lock_held(self):
        for operation in ('put', 'get', 'delete', 'has_key', 'items', '_clean_expired_keys'):
            with self.subTest(operation=operation):
                cache = SafeMapFIFO(max_length=17, default_expiration_sec=123)
                cache.put('parent-only', 'parent-value')
                result = self._run_child_while_locked(cache.lock, _map_operation_in_child,
                                                     cache, operation)
                self.assertTrue(result['new_lock'])
                self.assertTrue(result['child_pid'])
                self.assertEqual(result['settings'], (17, 123))
                self.assertEqual(result['value'], {'has_key': False, 'items': []}.get(operation))
                self.assertEqual(result['items'], [('child-only', 'child-value')]
                                 if operation == 'put' else [])
                self.assertEqual(cache.items(), [('parent-only', 'parent-value')])

    def test_inactive_dns_is_not_restarted_after_fork(self):
        for state in ('never-started', 'stopped'):
            for operation in ('lookup', 'add'):
                with self.subTest(state=state, operation=operation):
                    cache = DnsCacheService()
                    if state == 'stopped':
                        threads = []
                        original_start = threading.Thread.start

                        def record_start(thread):
                            threads.append(thread)
                            return original_start(thread)

                        with mock.patch.object(threading.Thread, 'start', record_start):
                            cache.async_refresh_cache(60, interval=0.01)
                        cache.shutdown()
                        for thread in threads:
                            thread.join(2)
                            self.assertFalse(thread.is_alive())
                    cache.add('parent.example', 443, ['parent-ip'], int(time.time()) + 60)
                    result = self._run_child_while_locked(cache.async_lock, _inactive_dns_in_child,
                                                         cache, operation)
                    for key in ('new_lock', 'child_pid', 'parent_entry_cleared',
                                'inactive', 'config_preserved'):
                        self.assertTrue(result[key], key)
                    self.assertEqual(result['thread_starts'], 0)
                    self.assertEqual(result['child_entry'], operation == 'add')
                    self.assertEqual(cache.get_ip_list('parent.example', 443).ip_list, ['parent-ip'])
                    self.assertIsNone(cache.get_ip_list('child.example', 443))
                    self.assertFalse(cache.async_started)
                    self.assertTrue(cache.is_shutdown)

    def test_bucket_lookup_after_fork_with_parent_cache_locked(self):
        client = tos.TosClientV2(endpoint='https://example.com',
                                 region='cn-beijing', dns_cache_time=0)
        self.addCleanup(client.close)
        cache = client.bucket_type_cache
        cache.max_length = 17
        cache.default_expiration_sec = 123
        cache.put('parent-only', 'parent-value')
        result = self._run_child_while_locked(cache.lock, _bucket_lookup_in_child, client)
        self.assertTrue(result['new_lock'])
        self.assertTrue(result['parent_entry_cleared'])
        self.assertEqual(result['types'], ['hns'] * 16)
        self.assertEqual(result['settings'], (17, 123))
        self.assertEqual(cache.get('parent-only'), 'parent-value')
        self.assertIsNone(cache.get('bucket123'))

    def test_dns_lifecycle_after_fork_with_parent_lock_held(self):
        for mode in ('lookup', 'add', 'new-client', 'shutdown'):
            with self.subTest(mode=mode):
                cache = DnsCacheService()
                threads = []
                original_start = threading.Thread.start

                def record_start(thread):
                    threads.append(thread)
                    return original_start(thread)

                # Keep the parent refresher real, but all DNS resolution local.
                with mock.patch('tos.utils.resolve_ip_list', return_value=['parent-ip']):
                    with mock.patch.object(threading.Thread, 'start', record_start):
                        cache.async_refresh_cache(60, interval=0.01)
                    cache.add('parent.example', 443, ['parent-ip'], int(time.time()) + 60)
                    try:
                        result = self._run_child_while_locked(cache.async_lock, _dns_in_child, cache, mode)
                        self.assertTrue(result['new_lock'])
                        self.assertTrue(result['parent_entry_cleared'])
                        self.assertTrue(result['shutdown'])
                        self.assertTrue(result['threads_stopped'])
                        self.assertEqual(result['refresh_thread_count'], 0 if mode == 'shutdown' else 1)
                        if mode != 'shutdown':
                            self.assertTrue(result['refresh_ran_in_background'])
                        if mode == 'new-client':
                            self.assertTrue(result['restart_owner'])
                        self.assertTrue(cache.async_started)
                        self.assertFalse(cache.is_shutdown)
                        self.assertIsNotNone(cache.get_ip_list('parent.example', 443))
                    finally:
                        cache.shutdown()
                        for thread in threads:
                            thread.join(2)

    def test_close_after_fork_with_parent_pool_locked(self):
        client = tos.TosClientV2(endpoint='https://example.com',
                                 region='cn-beijing', dns_cache_time=0)
        self.addCleanup(client.close)
        old_session = client.session
        lock = old_session.get_adapter('https://').poolmanager.pools.lock
        result = self._run_child_while_locked(lock, _close_client_in_child, client)
        self.assertTrue(result['new_session'])
        self.assertTrue(result['child_pid'])
        self.assertIs(client.session, old_session)


class TestSafeMapForkState(unittest.TestCase):
    def test_same_process_retains_cache_and_eviction(self):
        cache = SafeMapFIFO(max_length=2, default_expiration_sec=10)
        lock = cache.lock
        with mock.patch('tos.safe_map.time.time', return_value=100):
            cache.put('first', 1)
        with mock.patch('tos.safe_map.time.time', return_value=101):
            cache.put('second', 2)
            cache.put('third', 3)
            self.assertIsNone(cache.get('first'))
            self.assertEqual(cache.get('second'), 2)
        with mock.patch('tos.safe_map.time.time', return_value=112):
            self.assertIsNone(cache.get('second'))
        self.assertIs(cache.lock, lock)


if __name__ == '__main__':
    unittest.main()
