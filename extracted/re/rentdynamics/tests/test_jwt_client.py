import base64
import json
import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, call, patch

import requests
from unittest import TestCase

from rentdynamics.client import JWTClient


class JWTClientTests(TestCase):
    API_URL = 'https://api.example.com/some/endpoint'
    TEST_PASSWORD = 'impact-reporting-system-password'
    # SHA-1 of TEST_PASSWORD; kept fixed to verify the login hashing behavior.
    EXPECTED_PASSWORD_SHA1 = '3662be0ae91a906e781e0b8fa122aab4ec65b6fc'

    def setUp(self):
        JWTClient.reset()
        self.addCleanup(JWTClient.reset)
        self.client = JWTClient(
            username='impact-reporting-system-user',
            password=self.TEST_PASSWORD,
        )

    @staticmethod
    def generate_access_token(expires_in):
        def encode_segment(value):
            encoded = base64.urlsafe_b64encode(
                json.dumps(value).encode('utf-8'),
            )
            return encoded.rstrip(b'=').decode('utf-8')

        expiration = datetime.now(tz=timezone.utc) + timedelta(seconds=expires_in)
        header = encode_segment({'alg': 'RS256', 'typ': 'JWT'})
        payload = encode_segment({'exp': int(expiration.timestamp())})
        external_signature = uuid.uuid4().hex
        return '{}.{}.{}'.format(header, payload, external_signature)

    @staticmethod
    def generate_token_response(access, refresh, status_code=200):
        response = Mock(status_code=status_code)
        response.json.return_value = {'access': access, 'refresh': refresh}
        return response

    @patch('rentdynamics.jwt_client.requests.post')
    def test_login_and_refresh_use_selected_base_url(self, mock_post):
        for options, expected_url in [
            ({}, 'https://api.rentdynamics.com'),
            ({'development': True}, 'https://api.rentdynamics.dev'),
            ({'base_url': 'https://custom-rd.example/'}, 'https://custom-rd.example'),
            ({'development': True, 'base_development_url': 'https://custom-dev.example/'},
             'https://custom-dev.example'),
            ({'base_development_url': 'https://custom-dev.example'},
             'https://api.rentdynamics.com'),
            ({'development': True, 'base_url': 'https://custom-rd.example'},
             'https://api.rentdynamics.dev'),
        ]:
            with self.subTest(options=options):
                JWTClient.reset()
                client = JWTClient('impact-reporting-system-user', self.TEST_PASSWORD, **options)
                mock_post.reset_mock()
                access = self.generate_access_token(300)
                mock_post.return_value = self.generate_token_response(access, 'refresh')

                self.assertEqual(client.get_base_url(), expected_url)
                self.assertEqual(client._get_authorization(), 'Bearer ' + access)
                mock_post.assert_called_once_with(
                    url=expected_url + '/auth/login',
                    json={
                        'username': 'impact-reporting-system-user',
                        'password': self.EXPECTED_PASSWORD_SHA1,
                    }, timeout=30,
                )

                client._cache_tokens({
                    'access': self.generate_access_token(15), 'refresh': 'refresh',
                })
                mock_post.reset_mock()
                self.assertEqual(client._get_authorization(), 'Bearer ' + access)
                mock_post.assert_called_once_with(
                    url=expected_url + '/auth/token/refresh',
                    json={'refresh': 'refresh'}, timeout=30,
                )

    @patch('rentdynamics.jwt_client.requests.post')
    def test_changing_environment_discards_tokens_and_logs_in(self, mock_post):
        self.client._cache_tokens({
            'access': self.generate_access_token(300), 'refresh': 'production-refresh',
        })
        JWTClient('impact-reporting-system-user', self.TEST_PASSWORD, development=True)
        access = self.generate_access_token(300)
        mock_post.return_value = self.generate_token_response(access, 'development-refresh')

        self.assertEqual(self.client._get_authorization(), 'Bearer ' + access)
        mock_post.assert_called_once_with(
            url='https://api.rentdynamics.dev/auth/login',
            json={
                'username': 'impact-reporting-system-user',
                'password': self.EXPECTED_PASSWORD_SHA1,
            }, timeout=30,
        )

    @patch('rentdynamics.jwt_client.requests.post')
    def test_changing_inactive_url_preserves_tokens(self, mock_post):
        access = self.generate_access_token(300)
        self.client._cache_tokens({'access': access, 'refresh': 'refresh'})

        JWTClient(
            'impact-reporting-system-user', self.TEST_PASSWORD,
            base_development_url='https://custom-dev.example',
        )

        self.assertEqual(self.client._get_authorization(), 'Bearer ' + access)
        mock_post.assert_not_called()

    @patch('rentdynamics.jwt_client.requests.post')
    def test_obtains_and_caches_access_token(self, mock_post):
        access = self.generate_access_token(300)
        mock_post.return_value = self.generate_token_response(access, 'refresh-token')

        first = self.client._get_authorization()
        second = self.client._get_authorization()

        self.assertEqual(first, 'Bearer {}'.format(access))
        self.assertEqual(second, first)
        mock_post.assert_called_once_with(
            url='https://api.rentdynamics.com/auth/login',
            json={
                'username': 'impact-reporting-system-user',
                'password': self.EXPECTED_PASSWORD_SHA1,
            },
            timeout=30,
        )

    @patch('rentdynamics.jwt_client.aware_utcnow')
    def test_token_expiration_respects_fixed_drift_boundary(self, mock_now):
        self.client._cache_tokens({
            'access': self.generate_access_token(300),
            'refresh': 'refresh-token',
        })
        expiration = datetime.fromtimestamp(
            self.client._access_token_payload['exp'], tz=timezone.utc,
        )

        for seconds_remaining, expected in [
            (31, False),
            (30, True),
            (15, True),
            (0, True),
        ]:
            with self.subTest(seconds_remaining=seconds_remaining):
                mock_now.return_value = expiration - timedelta(seconds=seconds_remaining)

                self.assertEqual(self.client._token_is_expiring(), expected)

    @patch('rentdynamics.jwt_client.requests.post')
    def test_refreshes_access_token_with_drift_compensation(self, mock_post):
        self.client._cache_tokens({
            'access': self.generate_access_token(15),
            'refresh': 'old-refresh-token',
        })
        refreshed_access = self.generate_access_token(300)
        mock_post.return_value = self.generate_token_response(
            refreshed_access,
            'new-refresh-token',
        )

        authorization = self.client._get_authorization()

        self.assertEqual(authorization, 'Bearer {}'.format(refreshed_access))
        self.assertEqual(self.client._refresh_token, 'new-refresh-token')
        mock_post.assert_called_once_with(
            url='https://api.rentdynamics.com/auth/token/refresh',
            json={'refresh': 'old-refresh-token'},
            timeout=30,
        )

    @patch('rentdynamics.jwt_client.requests.post')
    def test_obtains_new_tokens_when_refresh_response_is_missing_refresh_token(
            self, mock_post):
        self.client._cache_tokens({
            'access': self.generate_access_token(15),
            'refresh': 'existing-refresh-token',
        })
        refreshed_access = self.generate_access_token(300)
        new_access = self.generate_access_token(300)
        malformed_refresh = Mock(status_code=200)
        malformed_refresh.json.return_value = {'access': refreshed_access}
        mock_post.side_effect = [
            malformed_refresh,
            self.generate_token_response(new_access, 'new-refresh-token'),
        ]

        authorization = self.client._get_authorization()

        self.assertEqual(authorization, 'Bearer {}'.format(new_access))
        self.assertEqual(
            self.client._refresh_token,
            'new-refresh-token',
        )

    @patch('rentdynamics.jwt_client.requests.post')
    def test_obtains_new_tokens_when_refresh_token_is_rejected(self, mock_post):
        JWTClient._refresh_token = 'expired-refresh-token'
        rejected_refresh = Mock(status_code=401)
        rejected_refresh.raise_for_status.side_effect = requests.HTTPError()
        new_access = self.generate_access_token(300)
        mock_post.side_effect = [
            rejected_refresh,
            self.generate_token_response(new_access, 'new-refresh-token'),
        ]

        authorization = self.client._get_authorization()

        self.assertEqual(authorization, 'Bearer {}'.format(new_access))
        self.assertEqual(
            mock_post.call_args_list,
            [
                call(
                    url='https://api.rentdynamics.com/auth/token/refresh',
                    json={'refresh': 'expired-refresh-token'},
                    timeout=30,
                ),
                call(
                    url='https://api.rentdynamics.com/auth/login',
                    json={
                        'username': 'impact-reporting-system-user',
                        'password': self.EXPECTED_PASSWORD_SHA1,
                    },
                    timeout=30,
                ),
            ],
        )

    @patch('rentdynamics.jwt_client.requests.post')
    def test_obtains_new_tokens_and_logs_traceback_when_refresh_raises_unexpected_exception(
            self, mock_post):
        JWTClient._refresh_token = 'existing-refresh-token'
        new_access = self.generate_access_token(300)
        mock_post.side_effect = [
            RuntimeError('Refresh failed'),
            self.generate_token_response(new_access, 'new-refresh-token'),
        ]

        with self.assertLogs('rentdynamics.jwt_client', level='WARNING') as logs:
            authorization = self.client._get_authorization()

        self.assertEqual(authorization, 'Bearer {}'.format(new_access))
        self.assertEqual(self.client._refresh_token, 'new-refresh-token')
        self.assertEqual(
            [request.kwargs['url'] for request in mock_post.call_args_list],
            [
                'https://api.rentdynamics.com/auth/token/refresh',
                'https://api.rentdynamics.com/auth/login',
            ],
        )
        self.assertIs(logs.records[0].exc_info[0], RuntimeError)

    @patch('rentdynamics.jwt_client.requests.post')
    def test_retries_post_once_when_rentplus_reports_expired_token(self, mock_post):
        first_access = self.generate_access_token(300)
        second_access = self.generate_access_token(300)
        obtain_response = self.generate_token_response(first_access, 'first-refresh-token')
        expired_response = Mock(
            status_code=403,
            text='{"errorMessage": "Token is invalid or expired"}',
        )
        refresh_response = self.generate_token_response(second_access, 'second-refresh-token')
        successful_response = Mock(status_code=200, text='{}')
        mock_post.side_effect = [
            obtain_response,
            expired_response,
            refresh_response,
            successful_response,
        ]

        response = self.client.post(
            self.API_URL,
            {'communityId': 456},
            headers={'X-TX-SIGNATURE': 'legacy-signature'},
        )

        self.assertIs(response, successful_response)
        self.assertEqual(mock_post.call_count, 4)
        self.assertEqual(
            mock_post.call_args_list[1].kwargs['headers']['Authorization'],
            'Bearer {}'.format(first_access),
        )
        self.assertEqual(
            mock_post.call_args_list[3].kwargs['headers']['Authorization'],
            'Bearer {}'.format(second_access),
        )
        for request_call in mock_post.call_args_list:
            self.assertEqual(
                request_call.kwargs['timeout'],
                30,
            )

    @patch('rentdynamics.jwt_client.requests.post')
    def test_returns_response_when_refreshed_token_is_rejected(self, mock_post):
        access = self.generate_access_token(300)
        expired_response = Mock(
            status_code=403,
            text='{"errorMessage": "Token is invalid or expired"}',
        )
        mock_post.side_effect = [
            self.generate_token_response(access, 'refresh-token'),
            expired_response,
            self.generate_token_response(access, 'refresh-token'),
            expired_response,
        ]

        response = self.client.post(
            self.API_URL,
            {'communityId': 456},
        )

        self.assertIs(response, expired_response)
        self.assertEqual(mock_post.call_count, 4)

    @patch('rentdynamics.jwt_client.requests.get')
    @patch('rentdynamics.jwt_client.requests.post')
    def test_get_sends_bearer_token_and_preserves_caller_headers(self, mock_post, mock_get):
        access = self.generate_access_token(300)
        mock_post.return_value = self.generate_token_response(access, 'refresh-token')
        headers = {'Accept': 'application/json'}
        url = 'https://api.rentplus.com/codeMappings/globals'

        response = self.client.get(url, headers=headers)

        self.assertIs(response, mock_get.return_value)
        self.assertEqual(headers, {'Accept': 'application/json'})
        mock_get.assert_called_once_with(
            url=url,
            headers={'Accept': 'application/json', 'Authorization': 'Bearer {}'.format(access)},
            timeout=30,
        )

    @patch('rentdynamics.jwt_client.requests.get')
    @patch('rentdynamics.jwt_client.requests.post')
    def test_get_retries_once_after_expired_token(self, mock_post, mock_get):
        first_access = self.generate_access_token(300)
        second_access = self.generate_access_token(300)
        mock_post.side_effect = [
            self.generate_token_response(first_access, 'first-refresh-token'),
            self.generate_token_response(second_access, 'second-refresh-token'),
        ]
        expired_response = Mock(
            status_code=403,
            text='{"errorMessage": "Token is invalid or expired"}',
        )
        # A second expired response must be returned without another retry.
        mock_get.return_value = expired_response
        url = 'https://api.rentplus.com/codeMappings/globals'

        response = self.client.get(url)

        self.assertIs(response, expired_response)
        self.assertEqual(mock_get.call_count, 2)
        self.assertEqual(mock_post.call_count, 2)
        self.assertEqual(
            [request.kwargs['headers']['Authorization'] for request in mock_get.call_args_list],
            ['Bearer {}'.format(first_access), 'Bearer {}'.format(second_access)],
        )
        mock_post.assert_called_with(
            url='https://api.rentdynamics.com/auth/token/refresh',
            json={'refresh': 'first-refresh-token'},
            timeout=30,
        )

    @patch('rentdynamics.jwt_client.requests.get')
    def test_get_does_not_retry_unrelated_errors(self, mock_get):
        self.client._cache_tokens({
            'access': self.generate_access_token(300),
            'refresh': 'refresh-token',
        })
        for status_code, body in [
            (403, '{"errorMessage": "Permission denied"}'),
            (403, '<html>Forbidden</html>'),
            (403, '[]'),
            (403, '{}'),
            (403, '{"code": "token_not_valid"}'),
            (401, '{"code": "token_not_valid"}'),
            (401, '{"errorMessage": "Token is invalid or expired"}'),
            (500, '{"errorMessage": "Token is invalid or expired"}'),
        ]:
            with self.subTest(status_code=status_code, body=body):
                mock_get.reset_mock()
                mock_get.return_value = Mock(status_code=status_code, text=body)

                response = self.client.get('https://api.rentplus.com/codeMappings/globals')

                self.assertIs(response, mock_get.return_value)
                mock_get.assert_called_once()

    @patch('rentdynamics.jwt_client.requests.post')
    def test_failed_login_does_not_send_api_request_or_cache_tokens(self, mock_post):
        mock_post.return_value.raise_for_status.side_effect = requests.HTTPError('Login failed')

        with self.assertRaises(requests.HTTPError):
            self.client.post(self.API_URL, {'communityId': 456})

        mock_post.assert_called_once()
        self.assertIsNone(self.client._access_token)
        self.assertIsNone(self.client._refresh_token)

    @patch('rentdynamics.jwt_client.requests.get')
    @patch('rentdynamics.jwt_client.requests.post')
    def test_get_uses_provided_url_and_fixed_timeout(self, mock_post, mock_get):
        access = self.generate_access_token(300)
        mock_post.return_value = self.generate_token_response(access, 'refresh')

        url = 'https://api.rentplus.com/codeMappings?community_id__isnull=True'
        self.client.get(url)

        self.assertEqual(mock_post.call_args.kwargs['timeout'], 30)
        mock_get.assert_called_once_with(
            url=url,
            headers={'Authorization': 'Bearer {}'.format(access)},
            timeout=30,
        )

    @patch('rentdynamics.jwt_client.requests.put')
    def test_put_preserves_body_and_copies_caller_headers(self, mock_put):
        access = self.generate_access_token(300)
        self.client._cache_tokens({'access': access, 'refresh': 'refresh'})
        headers = {'Authorization': 'old', 'Accept': 'application/json'}
        body = {'name': 'updated'}
        url = 'https://api.rentplus.com/communities/123'

        response = self.client.put(url, body, headers=headers)

        self.assertIs(response, mock_put.return_value)
        self.assertEqual(headers, {'Authorization': 'old', 'Accept': 'application/json'})
        self.assertIsNot(mock_put.call_args.kwargs['headers'], headers)
        mock_put.assert_called_once_with(
            url=url, json=body,
            headers={'Authorization': 'Bearer {}'.format(access), 'Accept': 'application/json'},
            timeout=30,
        )

    @patch('rentdynamics.jwt_client.requests.get')
    @patch('rentdynamics.jwt_client.requests.post')
    def test_new_instances_and_class_requests_reuse_tokens(self, mock_post, mock_get):
        access = self.generate_access_token(300)
        mock_post.return_value = self.generate_token_response(access, 'refresh')

        self.client.get(self.API_URL)
        other = JWTClient(
            'impact-reporting-system-user', self.TEST_PASSWORD,
            base_url='https://api.rentdynamics.com',
        )
        other.get(self.API_URL)
        JWTClient.get(self.API_URL)

        mock_post.assert_called_once()
        self.assertEqual(mock_get.call_count, 3)
        for request_call in mock_get.call_args_list:
            self.assertEqual(request_call.kwargs['headers']['Authorization'], 'Bearer ' + access)

    @patch('rentdynamics.jwt_client.requests.post')
    def test_new_instance_reuses_refresh_token(self, mock_post):
        self.client._cache_tokens({
            'access': self.generate_access_token(15),
            'refresh': 'old-refresh',
        })
        other = JWTClient(
            'impact-reporting-system-user', self.TEST_PASSWORD,
            base_url='https://api.rentdynamics.com/',
        )
        access = self.generate_access_token(300)
        mock_post.return_value = self.generate_token_response(access, 'new-refresh')

        self.assertEqual(other._get_authorization(), 'Bearer ' + access)
        self.assertEqual(self.client._get_authorization(), 'Bearer ' + access)
        mock_post.assert_called_once_with(
            url='https://api.rentdynamics.com/auth/token/refresh',
            json={'refresh': 'old-refresh'},
            timeout=30,
        )
        self.assertEqual(self.client._refresh_token, 'new-refresh')

    @patch('rentdynamics.jwt_client.requests.post')
    def test_authentication_changes_discard_shared_tokens(self, mock_post):
        original = {
            'username': 'impact-reporting-system-user',
            'password': self.TEST_PASSWORD,
            'base_url': 'https://api.rentdynamics.com',
        }
        for field, value in [
            ('username', 'other-user'),
            ('password', 'other-password'),
            ('base_url', 'https://other-rd.example'),
        ]:
            with self.subTest(field=field):
                JWTClient(**original)
                self.client._cache_tokens({
                    'access': self.generate_access_token(300),
                    'refresh': 'old-refresh',
                })
                changed = dict(original, **{field: value})
                other = JWTClient(**changed)
                access = self.generate_access_token(300)
                mock_post.reset_mock()
                mock_post.return_value = self.generate_token_response(access, 'new-refresh')

                self.assertIsNone(JWTClient._access_token)
                self.assertIsNone(JWTClient._access_token_payload)
                self.assertIsNone(JWTClient._refresh_token)
                self.assertEqual(other._get_authorization(), 'Bearer ' + access)
                self.assertEqual(self.client._get_authorization(), 'Bearer ' + access)
                mock_post.assert_called_once()
                self.assertEqual(
                    mock_post.call_args.kwargs['url'],
                    changed['base_url'] + '/auth/login',
                )
                self.assertEqual(
                    mock_post.call_args.kwargs['json']['username'], changed['username'],
                )

    @patch('rentdynamics.jwt_client.requests.put')
    @patch('rentdynamics.jwt_client.requests.post')
    def test_constructor_preserves_tokens_for_class_requests(self, mock_post, mock_put):
        access = self.generate_access_token(300)
        self.client._cache_tokens({'access': access, 'refresh': 'refresh'})

        JWTClient(
            'impact-reporting-system-user', self.TEST_PASSWORD,
            base_url='https://api.rentdynamics.com/',
        )
        response = JWTClient.put(self.API_URL, {'name': 'updated'})

        self.assertIs(response, mock_put.return_value)
        mock_post.assert_not_called()
        mock_put.assert_called_once_with(
            url=self.API_URL, json={'name': 'updated'},
            headers={'Authorization': 'Bearer ' + access}, timeout=30,
        )

    @patch('rentdynamics.jwt_client.requests.post')
    def test_reset_forces_login_for_existing_callers(self, mock_post):
        self.client._cache_tokens({
            'access': self.generate_access_token(300), 'refresh': 'old-refresh',
        })
        JWTClient.reset()
        access = self.generate_access_token(300)
        mock_post.return_value = self.generate_token_response(access, 'new-refresh')

        self.assertEqual(self.client._get_authorization(), 'Bearer ' + access)
        mock_post.assert_called_once_with(
            url='https://api.rentdynamics.com/auth/login',
            json={
                'username': 'impact-reporting-system-user',
                'password': self.EXPECTED_PASSWORD_SHA1,
            }, timeout=30,
        )

    @patch('rentdynamics.jwt_client.requests.get')
    @patch('rentdynamics.jwt_client.requests.post')
    def test_malformed_login_token_does_not_cache_or_send_api_request(self, mock_post, mock_get):
        for access in ('malformed', 'e30.W10.signature'):
            with self.subTest(access=access):
                mock_post.return_value = self.generate_token_response(access, 'refresh')
                with self.assertRaises((ValueError, KeyError)):
                    self.client.get('/codeMappings/globals')
                self.assertIsNone(self.client._access_token)
                self.assertIsNone(self.client._refresh_token)
        mock_get.assert_not_called()

    def test_reset_discards_tokens(self):
        self.client._cache_tokens({'access': self.generate_access_token(300), 'refresh': 'refresh'})

        self.client.reset()

        self.assertIsNone(self.client._access_token)
        self.assertIsNone(self.client._refresh_token)
