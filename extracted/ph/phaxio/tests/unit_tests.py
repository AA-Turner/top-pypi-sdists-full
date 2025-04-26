import unittest
import re
import logging
import urllib
import six
from six import PY3

from urllib3_mock import Responses
from datetime import datetime

from phaxio import PhaxioApi

# need to set up mocks for both urllib3-based requests (used for most everything) and requests-based ones (used for some posts)
responses_requests = Responses('requests.packages.urllib3')
responses_urllib = Responses()


test_phone_number = '2065551234'
test_phone_number2 = '2065551235'
test_fax_id = 12345



class PhaxioApiUnitTests(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG

    handler = logging.FileHandler('test.log')
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(handler)

    def setUp(self):
        self.client = PhaxioApi('TEST_API_KEY', 'TEST_API_SECRET')
        self.request = None

        # this will cause all API requests to get routed to request_callback, which just returns empty reponses
        # and saves the request in self.request so it can be validated
        url_re = re.compile(r'/v2/.*', flags=re.UNICODE)
        responses_urllib.add_callback('GET', url_re, callback=self.request_callback)
        responses_urllib.add_callback('POST', url_re, callback=self.request_callback)
        responses_urllib.add_callback('DELETE', url_re, callback=self.request_callback)

        responses_requests.add_callback('POST', url_re, callback=self.request_callback)
        responses_requests.add_callback('GET', url_re, callback=self.request_callback)
        responses_requests.add_callback('DELETE', url_re, callback=self.request_callback)

    def request_callback(self, r):
        self.request = r
        self.logger.debug('request={}'.format(r))
        return 200, {}, ''

    def assert_request_is_correct(self, method, url, headers_dict=None, body=None):
        self.assertEqual(self.request.method, method)

        parsed_url = url.split('?')
        parsed_request_url = self.request.url.split('?')

        self.assertEqual(parsed_request_url[0], parsed_url[0])
        self.assertEqual(len(parsed_request_url), len(parsed_url))
        if len(parsed_request_url) > 1:
            six.assertCountEqual(self, parsed_request_url[1].split('&'), parsed_url[1].split('&'))

        if headers_dict:
            self.assertTrue(set(headers_dict.items()).issubset(set(self.request.headers.items())))
        if body:
            self.assertEqual(body, self.request.body)

    def create_test_files(self):
        with open('./_test_fax_file1.pdf', mode='w+') as file:
            file.write('test file 1 contents')

        with open('./_test_fax_file2.doc', mode='w+') as file:
            file.write('test file 2 contents')

    @responses_urllib.activate
    @responses_requests.activate
    def test_phone_numbers_api(self):
        self.client.PhoneNumber.get_phone_number_info(test_phone_number)
        self.assert_request_is_correct('GET', '/v2/phone_numbers/{}'.format(test_phone_number))

        self.client.PhoneNumber.get_area_codes(page=3, per_page=49)
        self.assert_request_is_correct('GET', '/v2/public/area_codes?page=3&per_page=49')
        # auth not required for this api
        self.assertNotIn('Authorization', self.request.headers)

        # some apis don't like the empty return, so catch the exception
        try:
            self.client.PhoneNumber.provision_phone_number('1', '206', 'http://fake/callback')
        except Exception as e:
            pass

        self.assert_request_is_correct('POST', '/v2/phone_numbers', {'Content-Type': 'application/x-www-form-urlencoded'},
                                       body='country_code=1&area_code=206&callback_url=http%3A%2F%2Ffake%2Fcallback')

        self.client.PhoneNumber.query_phone_numbers(country_code=1, area_code=206, page=4, per_page=12)
        self.assert_request_is_correct('GET', '/v2/phone_numbers?country_code=1&per_page=12&area_code=206&page=4')

        self.client.PhoneNumber.release_phone_number(test_phone_number)
        self.assert_request_is_correct('DELETE', '/v2/phone_numbers/{}'.format(test_phone_number))

    @responses_urllib.activate
    @responses_requests.activate
    def test_account_info_api(self):
        self.client.Account.get_status()
        self.assert_request_is_correct('GET', '/v2/account/status')

    @responses_urllib.activate
    @responses_requests.activate
    def test_phax_code_api(self):
        try:
            self.client.PhaxCode.create_phax_code_json_response('{"test_key": "test_val"}')
        except Exception as e:
            pass

        self.assert_request_is_correct('POST', '/v2/phax_codes',
                                       headers_dict={'Content-Type': 'application/x-www-form-urlencoded'},
                                       body='metadata=%7B%22test_key%22%3A+%22test_val%22%7D')
        self.client.PhaxCode.get_phax_code_json_response('phax_code_id')
        self.assert_request_is_correct('GET', '/v2/phax_codes/phax_code_id')

    @responses_urllib.activate
    @responses_requests.activate
    def test_countries_api(self):
        self.client.Countries.get_countries()
        self.assert_request_is_correct('GET', '/v2/public/countries')
        self.client.Countries.get_countries(page=4)
        self.assert_request_is_correct('GET', '/v2/public/countries?page=4')

    @responses_urllib.activate
    @responses_requests.activate
    def test_fax_api(self):
        self.client.Fax.cancel(test_fax_id)
        self.assert_request_is_correct('POST', '/v2/faxes/{}/cancel'.format(test_fax_id))

        self.client.Fax.resend(test_fax_id)
        self.assert_request_is_correct('POST', '/v2/faxes/{}/resend'.format(test_fax_id))

        self.client.Fax.delete(test_fax_id)
        self.assert_request_is_correct('DELETE', '/v2/faxes/{}'.format(test_fax_id))

        self.client.Fax.delete_file(test_fax_id)
        self.assert_request_is_correct('DELETE', '/v2/faxes/{}/file'.format(test_fax_id))

        self.client.Fax.status(test_fax_id)
        self.assert_request_is_correct('GET', '/v2/faxes/{}'.format(test_fax_id))

        self.client.Fax.get_file(test_fax_id)
        self.assert_request_is_correct('GET', '/v2/faxes/{}/file'.format(test_fax_id),
                                       headers_dict={'Accept': 'application/octet-stream'})

        self.client.Fax.get_file(test_fax_id, thumbnail='l')
        self.assert_request_is_correct('GET', '/v2/faxes/{}/file?thumbnail=l'.format(test_fax_id),
                                       headers_dict={'Accept': 'application/octet-stream'})
        timestamp = datetime.now().replace(microsecond=0)
        ts_str = timestamp.isoformat('T')
        if PY3:
            ts_str_encoded = urllib.parse.quote_plus(ts_str)
        else:
            ts_str_encoded = urllib.quote_plus(ts_str)

        # send timestamp as datetime object
        self.client.Fax.query_faxes(created_before=timestamp, created_after=timestamp, direction='send',
                                    status='success', phone_number=test_phone_number,
                                    tags_dict={'foo': 'bar'}, per_page=2, page=1)
        self.assert_request_is_correct('GET', '/v2/faxes?status=success&phone_number=2065551234&direction=send&tag%5Bfoo%5D=bar&'
                                       'created_after={}&per_page=2&created_before={}&page=1'.format(ts_str_encoded, ts_str_encoded))
        # send timestamp as string
        self.client.Fax.query_faxes(created_before=ts_str, created_after=ts_str)
        self.assert_request_is_correct('GET',
                                       '/v2/faxes?created_before={}&created_after={}'.format(ts_str_encoded, ts_str_encoded))

    @responses_urllib.activate
    @responses_requests.activate
    def test_send_fax(self):
        test_tags = {'foo': 'bar', 'abc': 'xyz'}

        try:
            self.client.Fax.send(to=[test_phone_number, test_phone_number2],
                                 content_urls=['http://www.google.com', 'http://www.bing.com'],
                                 header_text='foo header text', batch_delay=10, batch_collision_avoidance=True,
                                 callback_url='http://a.callback.url.com', cancel_timeout='30',
                                 caller_id=test_phone_number, test_fail=False, tags_dict=test_tags)
        except Exception as e:
            pass

        self.assert_request_is_correct('POST', '/v2/faxes', {'Content-Type': 'application/x-www-form-urlencoded'})

        if PY3:
            body = urllib.parse.unquote_plus(self.request.body)
        else:
            body = urllib.unquote_plus(self.request.body)
        actual_vals = body.split('&')
        correct_vals = ['to[]={}'.format(test_phone_number), 'to[]={}'.format(test_phone_number2),
                        'caller_id={}'.format(test_phone_number),
                        'content_url[]=http://www.google.com', 'content_url[]=http://www.bing.com',
                        'header_text=foo header text', 'batch_delay=10', 'batch_collision_avoidance=true',
                        'callback_url=http://a.callback.url.com', 'cancel_timeout=30', 'test_fail=false',
                        'tag[foo]=bar', 'tag[abc]=xyz'
        ]
        actual_vals.sort()
        correct_vals.sort()
        self.assertListEqual(actual_vals, correct_vals)

        self.create_test_files()
        try:
            self.client.Fax.send(test_phone_number, files=['./_test_fax_file1.pdf', './_test_fax_file2.doc'],
                                 content_urls=['http://www.google.com', 'http://www.bing.com'], tags_dict=test_tags)
        except Exception as e:
            pass
        self.assert_request_is_correct('POST', '/v2/faxes')
        # find the delimiter in the header, split up the body by the delimiter, then verify that each value is correct
        self.assertTrue(self.request.headers['Content-Type'].startswith('multipart/form-data'))
        delim = '--' + self.request.headers['Content-Type'].split('=')[-1]
        self.logger.debug('delim={}'.format(delim))
        if PY3:
            body = self.request.body.decode('UTF-8')
        else:
            body = self.request.body
        body_lst = re.split('\s*{}-*\s*'.format(delim), body)
        body_lst = [x for x in body_lst if x]  # remove empty strings from list
        self.logger.debug('body_lst={}'.format(body_lst))
        correct_vals = ['Content-Disposition: form-data; name="to[]"\r\n\r\n2065551234',
                        'Content-Disposition: form-data; name="tag[foo]"\r\n\r\nbar',
                        'Content-Disposition: form-data; name="tag[abc]"\r\n\r\nxyz',
                        'Content-Disposition: form-data; name="content_url[]"\r\n\r\nhttp://www.google.com',
                        'Content-Disposition: form-data; name="content_url[]"\r\n\r\nhttp://www.bing.com',
                        'Content-Disposition: form-data; name="file[]"; filename="_test_fax_file1.pdf"\r\nContent-Type: application/pdf\r\n\r\ntest file 1 contents',
                        'Content-Disposition: form-data; name="file[]"; filename="_test_fax_file2.doc"\r\nContent-Type: application/msword\r\n\r\ntest file 2 contents',
                        ]
        correct_vals.sort()
        body_lst.sort()
        self.assertListEqual(body_lst, correct_vals)
