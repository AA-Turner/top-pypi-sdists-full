# -*- coding: utf-8 -*-
import multiprocessing as multiprocessing
import os
import threading
import time
import traceback
import unittest
from unittest import mock

import tos
from tests.common import MockResponse


def _hold_lock(lock, ready, stop):
    lock.acquire()
    ready.set()
    try:
        stop.wait()
    finally:
        lock.release()


def _request_with_inherited_client(conn, client, old_session_id, old_pool_lock_id):
    try:
        request_error = None
        try:
            client.get_object('bucket123', 'key', range_start=0, range_end=0)
        except Exception as e:
            request_error = type(e).__name__

        new_lock = client.session.get_adapter('http://').poolmanager.pools.lock
        lock_acquired = new_lock.acquire(False)
        if lock_acquired:
            new_lock.release()

        conn.send({
            'ok': True,
            'request_error': request_error,
            'old_session_id': old_session_id,
            'new_session_id': id(client.session),
            'old_pool_lock_id': old_pool_lock_id,
            'new_pool_lock_id': id(new_lock),
            'new_lock_acquirable': lock_acquired,
        })
    except Exception:
        conn.send({
            'ok': False,
            'traceback': traceback.format_exc(),
        })
    finally:
        conn.close()


class TestForkSessionRebuild(unittest.TestCase):
    def _new_client(self):
        return tos.TosClientV2(
            'ak',
            'sk',
            'tos-cn-beijing.volces.com',
            'cn-beijing',
            max_connections=4,
            dns_cache_time=0,
            follow_redirect_times=7,
        )

    def test_rebuild_session_when_pid_changes(self):
        client = self._new_client()
        old_session = client.session
        marker_hook = lambda r, *args, **kwargs: None
        old_session.trust_env = False
        old_session.cookies.set('session-id', 'cookie-value')
        old_session.hooks['response'].append(marker_hook)
        old_lock_id = id(old_session.get_adapter('http://').poolmanager.pools.lock)

        client._session_pid = os.getpid() - 1
        client._ensure_session_fork_safe()

        self.assertIsNot(client.session, old_session)
        self.assertEqual(client._session_pid, os.getpid())
        self.assertFalse(client.session.trust_env)
        self.assertEqual(client.session.max_redirects, 7)
        self.assertEqual(client.session.cookies.get('session-id'), 'cookie-value')
        self.assertIn(marker_hook, client.session.hooks['response'])
        self.assertNotEqual(id(client.session.get_adapter('http://').poolmanager.pools.lock), old_lock_id)

        new_lock = client.session.get_adapter('http://').poolmanager.pools.lock
        self.assertTrue(new_lock.acquire(False))
        new_lock.release()

    def test_missing_session_pid_rebuilds_session(self):
        client = self._new_client()
        old_session = client.session

        del client._session_pid
        client._ensure_session_fork_safe()

        self.assertIsNot(client.session, old_session)
        self.assertEqual(client._session_pid, os.getpid())

    def test_concurrent_rebuild_session_when_pid_changes_once(self):
        client = self._new_client()
        client._session_pid = os.getpid() - 1
        original_rebuild = client._rebuild_session_after_fork
        calls = []
        errors = []
        start = threading.Event()

        def rebuild(old_session):
            calls.append(id(old_session))
            time.sleep(0.05)
            return original_rebuild(old_session)

        def worker():
            start.wait()
            try:
                client._ensure_session_fork_safe()
            except Exception as e:
                errors.append(e)

        client._rebuild_session_after_fork = rebuild
        threads = [threading.Thread(target=worker) for _ in range(8)]
        for thread in threads:
            thread.start()
        start.set()
        for thread in threads:
            thread.join(5)

        self.assertEqual(errors, [])
        self.assertEqual(len(calls), 1)
        self.assertEqual(client._session_pid, os.getpid())

    @mock.patch('requests.Session.request')
    def test_v2_request_rebuilds_session_before_request(self, mock_request):
        client = self._new_client()
        old_session = client.session
        old_lock_id = id(old_session.get_adapter('http://').poolmanager.pools.lock)
        mock_request.return_value = MockResponse(headers={'content-length': '0'})

        client._session_pid = os.getpid() - 1
        client.get_object('bucket123', 'key')

        self.assertIsNot(client.session, old_session)
        self.assertNotEqual(id(client.session.get_adapter('http://').poolmanager.pools.lock), old_lock_id)
        mock_request.assert_called_once()

    def test_forked_child_can_exit_after_sending_result(self):
        request_in_child = _request_with_inherited_client

        def delayed_exit(*args):
            request_in_child(*args)
            # Sending the result does not mean the process has finished exiting.
            time.sleep(0.1)

        with mock.patch(__name__ + '._request_with_inherited_client', side_effect=delayed_exit):
            self.test_forked_child_rebuilds_inherited_parent_session()

    def test_forked_child_rebuilds_inherited_parent_session(self):
        if 'fork' not in multiprocessing.get_all_start_methods():
            self.skipTest('fork start method is not available')

        client = tos.TosClientV2(
            'ak',
            'sk',
            'http://127.0.0.1:9',
            'cn-beijing',
            max_retry_count=0,
            connection_time=1,
            socket_timeout=1,
            dns_cache_time=0,
            is_custom_domain=True,
        )
        client.session.trust_env = False
        old_session = client.session
        old_lock = old_session.get_adapter('http://').poolmanager.pools.lock

        ready = threading.Event()
        stop = threading.Event()
        holder = threading.Thread(target=_hold_lock, args=(old_lock, ready, stop))
        holder.daemon = True
        holder.start()
        self.assertTrue(ready.wait(5))

        ctx = multiprocessing.get_context('fork')
        parent_conn, child_conn = ctx.Pipe(duplex=False)
        proc = ctx.Process(
            target=_request_with_inherited_client,
            args=(child_conn, client, id(old_session), id(old_lock)),
        )
        proc.start()
        child_conn.close()

        try:
            self.assertTrue(
                parent_conn.poll(8),
                'forked child hung while reusing inherited parent client session',
            )
            result = parent_conn.recv()
            # The pipe can be readable before the child finishes exiting.
            proc.join(5)
            self.assertEqual(proc.exitcode, 0, 'child did not exit cleanly after sending its result')
        finally:
            if proc.is_alive():
                proc.terminate()
            proc.join(5)
            stop.set()
            holder.join(5)
            client.close()
            parent_conn.close()
            child_conn.close()

        self.assertTrue(result['ok'], result.get('traceback'))
        self.assertNotEqual(result['new_session_id'], result['old_session_id'])
        self.assertNotEqual(result['new_pool_lock_id'], result['old_pool_lock_id'])
        self.assertTrue(result['new_lock_acquirable'])


if __name__ == '__main__':
    unittest.main()
