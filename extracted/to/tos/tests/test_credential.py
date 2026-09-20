# -*- coding: utf-8 -*-
import datetime
import multiprocessing
import os
import subprocess
import sys
import tempfile
import textwrap
import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest import mock

import requests

import tos
from tos.auth import CredentialProviderAuth
from tos.credential import OIDCCredentialsProvider
from tos.exceptions import TosClientError
from tos.http import Request


def _sign_with_inherited_oidc_provider(conn, provider, response):
    try:
        auth = CredentialProviderAuth(provider, 'cn-beijing')

        def sign(unused):
            request = Request('GET', 'https://bucket.example.com/key', '/key',
                              'bucket.example.com')
            auth.sign_request(request)
            return request.headers['x-tos-security-token']

        with mock.patch('tos.credential.requests.post', return_value=response) as post:
            with ThreadPoolExecutor(max_workers=8) as executor:
                tokens = list(executor.map(sign, range(16)))
            conn.send({'tokens': tokens, 'refreshes': post.call_count,
                       'oidc_token': post.call_args[1]['data']['OIDCToken']})
    except Exception as error:
        conn.send({'error': repr(error)})
    finally:
        conn.close()


class OIDCCredentialsProviderTestCase(unittest.TestCase):
    def setUp(self):
        token_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        token_file.write(self._fixture_value('oidc-token') + '\n')
        token_file.close()
        self.token_file = token_file.name
        self.addCleanup(self._remove_token_file)

    @staticmethod
    def _fixture_value(prefix, suffix='1'):
        # Build synthetic credential values at runtime so secret scanners do
        # not mistake deterministic test fixtures for embedded credentials.
        return '{0}-{1}'.format(prefix, suffix)

    def _remove_token_file(self):
        if os.path.exists(self.token_file):
            os.remove(self.token_file)

    @staticmethod
    def _expiration(seconds=3600):
        value = datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds)
        return value.strftime('%Y-%m-%dT%H:%M:%SZ')

    def _success_response(self, expiration=None, token_suffix='1'):
        response = mock.Mock()
        response.status_code = 200
        response.json.return_value = {
            'ResponseMetadata': {'RequestId': 'request-id'},
            'Result': {
                'Credentials': {
                    'AccessKeyId': self._fixture_value('ak', token_suffix),
                    'SecretAccessKey': self._fixture_value('sk', token_suffix),
                    'SessionToken': self._fixture_value('sts', token_suffix),
                    'Expiration': expiration or self._expiration(),
                }
            }
        }
        return response

    @mock.patch('tos.credential.requests.post')
    def test_get_credentials_from_environment(self, mock_post):
        mock_post.return_value = self._success_response()
        environment = {
            'VOLCENGINE_OIDC_ROLE_TRN': 'trn:iam::123456789:role/tos-reader',
            'VOLCENGINE_OIDC_TOKEN_FILE': self.token_file,
            'VOLCENGINE_OIDC_ROLE_SESSION_NAME': 'test-session',
            'VOLCENGINE_OIDC_ROLE_POLICY': '{"Statement":[]}',
            'VOLCENGINE_OIDC_STS_ENDPOINT': 'sts.example.com',
        }
        with mock.patch.dict(os.environ, environment, clear=True):
            provider = OIDCCredentialsProvider(timeout=5)
            credentials = provider.get_credentials()

        self.assertEqual(credentials.get_ak(), self._fixture_value('ak'))
        self.assertEqual(credentials.get_sk(), self._fixture_value('sk'))
        self.assertEqual(credentials.get_security_token(), self._fixture_value('sts'))
        mock_post.assert_called_once_with(
            'https://sts.example.com/?Action=AssumeRoleWithOIDC&Version=2018-01-01',
            data={
                'RoleTrn': 'trn:iam::123456789:role/tos-reader',
                'OIDCToken': self._fixture_value('oidc-token'),
                'RoleSessionName': 'test-session',
                'DurationSeconds': '3600',
                'Policy': '{"Statement":[]}',
            },
            timeout=5,
            allow_redirects=False,
        )

    @mock.patch('tos.credential.requests.post')
    def test_explicit_arguments_override_environment(self, mock_post):
        mock_post.return_value = self._success_response()
        environment = {
            'VOLCENGINE_OIDC_ROLE_TRN': 'environment-role',
            'VOLCENGINE_OIDC_TOKEN_FILE': '/environment/token',
        }
        with mock.patch.dict(os.environ, environment, clear=True):
            provider = OIDCCredentialsProvider(
                role_trn='explicit-role',
                oidc_token_file=self.token_file,
                role_session_name='explicit-session',
                duration_seconds=900,
                sts_endpoint='https://sts.example.com/',
            )
            provider.get_credentials()

        args, kwargs = mock_post.call_args
        self.assertEqual(args[0],
                         'https://sts.example.com/?Action=AssumeRoleWithOIDC&Version=2018-01-01')
        self.assertEqual(kwargs['data']['RoleTrn'], 'explicit-role')
        self.assertEqual(kwargs['data']['RoleSessionName'], 'explicit-session')
        self.assertEqual(kwargs['data']['DurationSeconds'], '900')

    @mock.patch('tos.credential.requests.post')
    def test_valid_credentials_are_cached(self, mock_post):
        mock_post.return_value = self._success_response()
        provider = self._provider()

        first = provider.get_credentials()
        second = provider.get_credentials()

        self.assertIs(first, second)
        self.assertEqual(mock_post.call_count, 1)

    @mock.patch('tos.credential.requests.post')
    def test_refresh_reads_rotated_token_file(self, mock_post):
        responses = [
            self._success_response(expiration=self._expiration(120), token_suffix='1'),
        ]
        rotated_suffix = str(len(responses) + 1)
        responses.append(self._success_response(token_suffix=rotated_suffix))
        mock_post.side_effect = responses
        provider = self._provider(pre_fetch_sec=300)

        first = provider.get_credentials()
        with open(self.token_file, 'w', encoding='utf-8') as token_file:
            token_file.write(self._fixture_value('oidc-token', rotated_suffix))
        second = provider.get_credentials()

        self.assertEqual(first.get_ak(), self._fixture_value('ak'))
        self.assertEqual(second.get_ak(), self._fixture_value('ak', rotated_suffix))
        self.assertEqual(mock_post.call_args_list[0][1]['data']['OIDCToken'],
                         self._fixture_value('oidc-token'))
        self.assertEqual(mock_post.call_args_list[1][1]['data']['OIDCToken'],
                         self._fixture_value('oidc-token', rotated_suffix))

    @mock.patch('tos.credential.requests.post')
    def test_refresh_failure_reuses_unexpired_credentials(self, mock_post):
        mock_post.side_effect = [
            self._success_response(expiration=self._expiration(120)),
            requests.ConnectionError('unavailable'),
        ]
        provider = self._provider(pre_fetch_sec=300)

        first = provider.get_credentials()
        second = provider.get_credentials()
        third = provider.get_credentials()

        self.assertIs(first, second)
        self.assertIs(first, third)
        self.assertEqual(mock_post.call_count, 2)

    @mock.patch('tos.credential.requests.post')
    def test_refresh_failure_retries_after_backoff(self, mock_post):
        mock_post.side_effect = [
            self._success_response(token_suffix='1'),
            requests.ConnectionError('unavailable'),
            self._success_response(token_suffix='2'),
        ]
        provider = self._provider(pre_fetch_sec=300)
        first = provider.get_credentials()
        provider._expiration_timestamp = 1200

        with mock.patch('tos.credential.random.uniform', return_value=5) as mock_uniform:
            with mock.patch('tos.credential.time.time', return_value=1000):
                fallback = provider.get_credentials()
            with mock.patch('tos.credential.time.time', return_value=1014):
                during_backoff = provider.get_credentials()
            with mock.patch('tos.credential.time.time', return_value=1016):
                refreshed = provider.get_credentials()

        self.assertIs(first, fallback)
        self.assertIs(first, during_backoff)
        self.assertIsNot(first, refreshed)
        self.assertEqual(mock_post.call_count, 3)
        mock_uniform.assert_called_once_with(0, 5)

    @mock.patch('tos.credential.requests.post')
    def test_concurrent_refresh_failure_shares_backoff(self, mock_post):
        mock_post.side_effect = requests.ConnectionError('unavailable')
        provider = self._provider(pre_fetch_sec=300)
        credentials = tos.StaticCredentialsProvider(
            self._fixture_value('old-ak'), self._fixture_value('old-sk'),
            self._fixture_value('old-token')).get_credentials()
        provider.credentials = credentials
        provider._expiration_timestamp = time.time() + 120

        with mock.patch('tos.credential.random.uniform', return_value=0):
            with ThreadPoolExecutor(max_workers=8) as executor:
                results = list(executor.map(lambda unused: provider.get_credentials(), range(16)))

        self.assertEqual(mock_post.call_count, 1)
        self.assertTrue(all(value is credentials for value in results))

    @mock.patch('tos.credential.requests.post')
    def test_hard_expiry_window_fails_closed_and_obeys_backoff(self, mock_post):
        mock_post.side_effect = requests.ConnectionError('unavailable')
        provider = self._provider(pre_fetch_sec=0)
        provider.credentials = tos.StaticCredentialsProvider(
            self._fixture_value('old-ak'), self._fixture_value('old-sk'),
            self._fixture_value('old-token')).get_credentials()
        provider._expiration_timestamp = 1060

        with mock.patch('tos.credential.random.uniform', return_value=0):
            with mock.patch('tos.credential.time.time', return_value=1000):
                with self.assertRaises(TosClientError):
                    provider.get_credentials()
                with self.assertRaises(TosClientError):
                    provider.get_credentials()

        self.assertEqual(mock_post.call_count, 1)

    @mock.patch('tos.credential.requests.post')
    def test_refresh_backoff_does_not_cross_hard_expiry_window(self, mock_post):
        mock_post.side_effect = requests.ConnectionError('unavailable')
        provider = self._provider(pre_fetch_sec=300)
        credentials = tos.StaticCredentialsProvider(
            self._fixture_value('old-ak'), self._fixture_value('old-sk'),
            self._fixture_value('old-token')).get_credentials()
        provider.credentials = credentials
        provider._expiration_timestamp = 1070

        with mock.patch('tos.credential.random.uniform', return_value=5):
            with mock.patch('tos.credential.time.time', return_value=1000):
                self.assertIs(provider.get_credentials(), credentials)
            self.assertEqual(provider._next_refresh_timestamp, 1010)

            with mock.patch('tos.credential.time.time', return_value=1009):
                self.assertIs(provider.get_credentials(), credentials)
            with mock.patch('tos.credential.time.time', return_value=1010):
                with self.assertRaises(TosClientError):
                    provider.get_credentials()
            with mock.patch('tos.credential.time.time', return_value=1011):
                with self.assertRaises(TosClientError):
                    provider.get_credentials()

        self.assertEqual(mock_post.call_count, 2)

    @mock.patch('tos.credential.requests.post')
    def test_expired_credentials_fail_closed(self, mock_post):
        mock_post.side_effect = requests.ConnectionError('unavailable')
        provider = self._provider()
        provider.credentials = tos.StaticCredentialsProvider(
            self._fixture_value('old-ak'), self._fixture_value('old-sk'),
            self._fixture_value('old-token')).get_credentials()
        provider._expiration_timestamp = time.time() - 1

        with self.assertRaises(TosClientError) as error:
            provider.get_credentials()

        self.assertIn('failed to request STS AssumeRoleWithOIDC', str(error.exception))

    def test_missing_configuration_is_rejected(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(TosClientError) as role_error:
                OIDCCredentialsProvider()
            self.assertIn('OIDC role TRN is empty', str(role_error.exception))

            with self.assertRaises(TosClientError) as token_error:
                OIDCCredentialsProvider(role_trn='role')
            self.assertIn('OIDC token file is empty', str(token_error.exception))

    def test_invalid_options_are_rejected(self):
        with self.assertRaises(TosClientError):
            self._provider(duration_seconds=899)
        with self.assertRaises(TosClientError):
            self._provider(duration_seconds=43201)
        with self.assertRaises(TosClientError):
            self._provider(timeout=0)
        with self.assertRaises(TosClientError):
            self._provider(pre_fetch_sec=-1)
        with self.assertRaises(TosClientError):
            self._provider(duration_seconds=900, pre_fetch_sec=900)
        with self.assertRaises(TosClientError) as insecure_endpoint_error:
            self._provider(sts_endpoint='http://sts.example.com')
        self.assertIn('must use https', str(insecure_endpoint_error.exception))
        with self.assertRaises(TosClientError):
            self._provider(sts_endpoint='ftp://sts.example.com')
        with self.assertRaises(TosClientError):
            self._provider(role_session_name=123)
        with self.assertRaises(TosClientError):
            self._provider(policy={})

    @mock.patch('tos.credential.requests.post')
    def test_missing_and_empty_token_file_are_rejected(self, mock_post):
        provider = self._provider(oidc_token_file=self.token_file + '.missing')
        with self.assertRaises(TosClientError) as missing_error:
            provider.get_credentials()
        self.assertIn('failed to read OIDC token file', str(missing_error.exception))

        with open(self.token_file, 'w', encoding='utf-8') as token_file:
            token_file.write(' \n')
        provider = self._provider()
        with self.assertRaises(TosClientError) as empty_error:
            provider.get_credentials()
        self.assertIn('OIDC token file is empty', str(empty_error.exception))
        self.assertFalse(mock_post.called)

    @mock.patch('tos.credential.requests.post')
    def test_sts_http_and_service_errors_are_rejected(self, mock_post):
        http_error = mock.Mock()
        http_error.status_code = 403
        http_error.json.return_value = {
            'ResponseMetadata': {
                'RequestId': 'request-http',
                'Error': {'Code': 'AccessDenied', 'Message': 'denied'},
            }
        }
        mock_post.return_value = http_error
        with self.assertRaises(TosClientError) as error:
            self._provider().get_credentials()
        self.assertIn('HTTP 403', str(error.exception))
        self.assertIn('code=AccessDenied', str(error.exception))
        self.assertIn('request_id=request-http', str(error.exception))

        service_error = mock.Mock()
        service_error.status_code = 200
        service_error.json.return_value = {
            'ResponseMetadata': {
                'RequestId': 'request-service',
                'Error': {
                    'Code': 'InvalidIdentityToken',
                    'Message': self._fixture_value('invalid-token'),
                },
            }
        }
        mock_post.return_value = service_error
        with self.assertRaises(TosClientError) as error:
            self._provider().get_credentials()
        self.assertIn('InvalidIdentityToken', str(error.exception))

        non_json_error = mock.Mock()
        non_json_error.status_code = 503
        non_json_error.json.side_effect = ValueError('not json')
        mock_post.return_value = non_json_error
        with self.assertRaises(TosClientError) as error:
            self._provider().get_credentials()
        self.assertIn('HTTP 503', str(error.exception))

    @mock.patch('tos.credential.requests.post')
    def test_sts_redirect_is_rejected_without_parsing_response(self, mock_post):
        redirect = mock.Mock()
        redirect.status_code = 307
        redirect.json.side_effect = AssertionError('redirect response must not be parsed')
        mock_post.return_value = redirect

        with self.assertRaises(TosClientError) as error:
            self._provider().get_credentials()

        self.assertIn('redirect HTTP 307 is not allowed', str(error.exception))
        self.assertFalse(redirect.json.called)
        self.assertFalse(mock_post.call_args[1]['allow_redirects'])

    @mock.patch('tos.credential.requests.post')
    def test_invalid_sts_responses_are_rejected(self, mock_post):
        invalid_json = mock.Mock()
        invalid_json.status_code = 200
        invalid_json.json.side_effect = ValueError('bad json')
        mock_post.return_value = invalid_json
        with self.assertRaises(TosClientError) as error:
            self._provider().get_credentials()
        self.assertIn('invalid JSON response', str(error.exception))

        missing_credentials = mock.Mock()
        missing_credentials.status_code = 200
        missing_credentials.json.return_value = {'ResponseMetadata': {}, 'Result': {}}
        mock_post.return_value = missing_credentials
        with self.assertRaises(TosClientError) as error:
            self._provider().get_credentials()
        self.assertIn('missing credentials or expiration', str(error.exception))

        mock_post.return_value = self._success_response(expiration='not-a-date')
        with self.assertRaises(TosClientError) as error:
            self._provider().get_credentials()
        self.assertIn('invalid expiration', str(error.exception))

        mock_post.return_value = self._success_response(expiration=self._expiration(30))
        with self.assertRaises(TosClientError) as error:
            self._provider().get_credentials()
        self.assertIn('too close to expiration', str(error.exception))

        invalid_shape = mock.Mock()
        invalid_shape.status_code = 200
        invalid_shape.json.return_value = []
        mock_post.return_value = invalid_shape
        with self.assertRaises(TosClientError) as error:
            self._provider().get_credentials()
        self.assertIn('invalid JSON response', str(error.exception))

    @mock.patch('tos.credential.requests.post')
    def test_expired_time_response_field_is_supported(self, mock_post):
        response = self._success_response()
        credentials = response.json.return_value['Result']['Credentials']
        credentials['ExpiredTime'] = credentials.pop('Expiration')
        mock_post.return_value = response

        result = self._provider().get_credentials()

        self.assertEqual(result.get_ak(), self._fixture_value('ak'))

    def test_provider_is_exported(self):
        self.assertIs(tos.OIDCCredentialsProvider, OIDCCredentialsProvider)

    @mock.patch('tos.credential.requests.post')
    def test_credentials_sign_tos_request_with_session_token(self, mock_post):
        mock_post.return_value = self._success_response()
        auth = CredentialProviderAuth(self._provider(), 'cn-beijing')
        request = Request('GET', 'https://bucket.example.com/key', '/key',
                          'bucket.example.com')

        auth.sign_request(request)

        self.assertEqual(request.headers['x-tos-security-token'], self._fixture_value('sts'))
        self.assertTrue(request.headers['Authorization'].startswith(
            'TOS4-HMAC-SHA256 Credential={0}/'.format(self._fixture_value('ak'))))

    @mock.patch('tos.credential.requests.post')
    def test_concurrent_callers_share_one_refresh(self, mock_post):
        mock_post.return_value = self._success_response()
        provider = self._provider()

        with ThreadPoolExecutor(max_workers=8) as executor:
            credentials = list(executor.map(lambda unused: provider.get_credentials(), range(16)))

        self.assertEqual(mock_post.call_count, 1)
        self.assertTrue(all(value is credentials[0] for value in credentials))

    @mock.patch('tos.credential.requests.post')
    def test_pid_change_discards_inherited_credentials_and_backoff(self, mock_post):
        mock_post.side_effect = [
            self._success_response(expiration=self._expiration(120)),
            requests.ConnectionError('unavailable'),
            self._success_response(token_suffix='child'),
        ]
        provider = self._provider()
        inherited = provider.get_credentials()
        self.assertIs(provider.get_credentials(), inherited)
        self.assertIsNotNone(provider._next_refresh_timestamp)

        with mock.patch('tos.credential.os.getpid', return_value=os.getpid() + 1):
            refreshed = provider.get_credentials()
            self.assertIs(provider.get_credentials(), refreshed)

        self.assertIsNot(refreshed, inherited)
        self.assertEqual(refreshed.get_security_token(), self._fixture_value('sts', 'child'))
        self.assertIsNone(provider._next_refresh_timestamp)
        self.assertIsNone(provider._last_refresh_error)
        self.assertEqual(mock_post.call_count, 3)

    def test_fork_during_refresh_allows_concurrent_child_signing(self):
        if 'fork' not in multiprocessing.get_all_start_methods():
            self.skipTest('fork start method is not available')

        provider = self._provider()
        entered_refresh = threading.Event()
        finish_refresh = threading.Event()
        parent_results = []
        parent_errors = []

        def blocked_post(*args, **kwargs):
            entered_refresh.set()
            if not finish_refresh.wait(15):
                raise AssertionError('parent refresh was not released')
            return self._success_response(token_suffix='parent')

        def refresh_parent():
            try:
                parent_results.append(provider.get_credentials())
            except Exception as error:
                parent_errors.append(error)

        ctx = multiprocessing.get_context('fork')
        parent_conn, child_conn = ctx.Pipe(duplex=False)
        proc = None
        with mock.patch('tos.credential.requests.post', side_effect=blocked_post) as post:
            thread = threading.Thread(target=refresh_parent, daemon=True)
            thread.start()
            try:
                self.assertTrue(entered_refresh.wait(5))
                # The parent has already read the old token and holds the refresh
                # lock. The child must independently read the rotated token.
                with open(self.token_file, 'w') as token_file:
                    token_file.write(self._fixture_value('oidc-token', suffix='rotated'))
                proc = ctx.Process(target=_sign_with_inherited_oidc_provider,
                                   args=(child_conn, provider,
                                         self._success_response(token_suffix='child')))
                proc.start()
                child_conn.close()
                self.assertTrue(parent_conn.poll(5), 'child hung on inherited OIDC refresh lock')
                result = parent_conn.recv()
                proc.join(5)
                self.assertEqual(proc.exitcode, 0)
                self.assertNotIn('error', result)
                self.assertEqual(result['refreshes'], 1)
                self.assertEqual(result['tokens'], [self._fixture_value('sts', 'child')] * 16)
                self.assertEqual(result['oidc_token'], self._fixture_value('oidc-token', suffix='rotated'))
            finally:
                if proc is not None and proc.is_alive():
                    proc.terminate()
                    proc.join(5)
                finish_refresh.set()
                thread.join(5)
                parent_conn.close()
                child_conn.close()

            self.assertFalse(thread.is_alive())
            self.assertEqual(parent_errors, [])
            self.assertEqual(post.call_count, 1)
            self.assertEqual(parent_results[0].get_security_token(), self._fixture_value('sts', 'parent'))
            self.assertIs(provider.get_credentials(), parent_results[0])

    @unittest.skipUnless('fork' in multiprocessing.get_all_start_methods(), 'fork is unavailable')
    def test_fork_test_exits_if_parent_refresh_never_reaches_sts(self):
        # Run the actual fork test in a separate interpreter. A non-daemon
        # refresh thread would keep that interpreter alive after test failure.
        script = textwrap.dedent('''
            import threading
            import unittest
            from unittest import mock
            from tests.test_credential import OIDCCredentialsProviderTestCase
            from tos.credential import OIDCCredentialsProvider

            wait = threading.Event.wait
            join = threading.Thread.join
            blocked = threading.Event()
            entered = threading.Event()

            def block_before_sts(self):
                entered.set()
                wait(blocked)

            def bounded_wait(event, timeout=None):
                if threading.current_thread() is threading.main_thread() and timeout is not None:
                    # Ensure this is an injected deadlock, not a slow thread start.
                    assert wait(entered, 2), 'refresh thread did not enter injected block'
                    timeout = min(timeout, 0.05)
                return wait(event, timeout)

            case = OIDCCredentialsProviderTestCase(
                'test_fork_during_refresh_allows_concurrent_child_signing')
            result = unittest.TestResult()
            with mock.patch.object(OIDCCredentialsProvider, 'get_credentials', block_before_sts), \\
                    mock.patch.object(threading.Event, 'wait', bounded_wait), \\
                    mock.patch.object(threading.Thread, 'join',
                                      lambda thread, timeout=None: join(thread, 0.05)):
                case.run(result)
            assert entered.is_set()
            assert result.testsRun == 1 and len(result.failures) == 1 and not result.errors, result
            print('injected refresh deadlock reported as test failure', flush=True)
        ''')
        result = subprocess.run([sys.executable, '-c', script],
                                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('injected refresh deadlock reported as test failure', result.stdout)

    def test_default_session_name_and_expiration_formats(self):
        provider = self._provider()
        self.assertTrue(provider.role_session_name.startswith('tos-python-sdk-'))
        self.assertLessEqual(len(provider.role_session_name), 64)

        expiration = OIDCCredentialsProvider._parse_expiration('2099-01-01T08:00:00.123456+08:00')
        expected = OIDCCredentialsProvider._parse_expiration('2099-01-01T00:00:00Z')
        self.assertEqual(expiration, expected + 0.123456)

    def _provider(self, **kwargs):
        options = {
            'role_trn': 'trn:iam::123456789:role/tos-reader',
            'oidc_token_file': self.token_file,
        }
        options.update(kwargs)
        return OIDCCredentialsProvider(**options)


if __name__ == '__main__':
    unittest.main()
