import os
import time
import json
from datetime import datetime
from dateutil.tz import tzlocal

from phaxio.api import PhaxioApi
from phaxio import ApiException

import unittest
import logging

test_filename1 = './_test_fax_file1.txt'
test_filename2 = './_test_fax_file2.txt'


class TestV2Api(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG

    handler = logging.FileHandler('test.log')
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(handler)

    test_number = '4145556984'

    def _pause(self):
        # wait between API calls to avoid being rate-limited
        time.sleep(1)

    def create_test_files(self):
        with open(test_filename1, mode='w+') as file:
            file.write('test file 1 contents')

        with open(test_filename2, mode='w+') as file:
            file.write('test file 2 contents')

    def setUp(self):

        api_key = os.getenv('API_KEY')
        api_secret = os.getenv('API_SECRET')

        if not api_key or not api_secret:
            self.skipTest("API_KEY or API_SECRET environment variables not defined. Skipping.")

        file_download_path = './'
        self.client = PhaxioApi(api_key, api_secret, file_download_path=file_download_path)

    def tearDown(self):
        self._pause()

    def test_send_fax(self):
        self.create_test_files()

        response = self.client.Fax.send(self.test_number, files=[test_filename1, test_filename2],
                        content_urls=['http://www.google.com', 'http://www.bing.com'], tags_dict={'foo': 'bar'})
        self.logger.info('response={}'.format(response))
        self.assertTrue(response.success)

        self._pause()
        # test multiple recipients
        response = self.client.Fax.send([self.test_number, '2065551234'],
                                        files=test_filename1,
                                        content_urls=['http://www.google.com', 'http://www.bing.com'],
                                        tags_dict={'foo': 'bar'})
        self.logger.info('response={}'.format(response))
        self.assertTrue(response.success)


    def test_send_fax_with_test_failure(self):
        test_dict = {'test_tag_key': 'test_tag_val'}
        # send fax with test_fail set, get its status, delete the file then delete the fax, verify each
        response = self.client.Fax.send(self.test_number, content_urls='http://www.google.com', test_fail='lineError',
                                        tags_dict=test_dict)
        self.logger.debug('response_type={}, response={}'.format(type(response), response))
        self.assertTrue(response.success)
        fax_id = response.data.id

        # get fax metadata
        time.sleep(7)
        status_response = self.client.Fax.status(fax_id)
        self.logger.debug('status={}'.format(status_response))
        self.assertEqual(status_response.data.recipients[0].error_type, 'lineError')
        self.assertDictEqual(status_response.data.tags, test_dict)

        self.logger.debug('created_at type={}, val={}'.format(type(status_response.data.created_at), status_response.data.created_at))

        # try downloading the file
        self._pause()
        response = self.client.Fax.get_file(fax_id, thumbnail='l')
        self.logger.debug('file download response={}'.format(response))

        # resend the fax
        self._pause()
        resend_response = self.client.Fax.resend(fax_id)
        self.logger.debug('resend_response={}'.format(resend_response))
        self.assertTrue(resend_response.success)

        self._pause()
        # now verify delete, file first
        delete_response = self.client.Fax.delete_file(fax_id)
        self.assertTrue(delete_response.success)
        self.logger.debug('delete_file_response={}'.format(delete_response))

        # now delete the fax itself
        self._pause()
        delete_response = self.client.Fax.delete(fax_id)
        self.assertTrue(delete_response.success)
        self.logger.debug('delete_response={}'.format(delete_response))

    def _assert_paging_params(self, result, page, per_page):
        self.assertEqual(result.paging.page, page)
        self.assertEqual(result.paging.per_page, per_page)
        self.assertLessEqual(len(result.data), per_page)

    def test_get_countries(self):
        result = self.client.Countries.get_countries(page=1, per_page=10)
        self.logger.debug("countries result={}".format(result))

        self.assertTrue(result.success)
        self._assert_paging_params(result, 1, 10)

    def test_query_fax(self):
        result = self.client.Fax.query_faxes(direction='sent', status='success', per_page=20, page=1,
                                             tags_dict={'foo': 'bar'})
        self.logger.debug('query_result={}'.format(result))
        self.assertTrue(result.success)
        self.assertTrue(result.paging.total > 0)
        self._assert_paging_params(result, 1, 20)

        self._pause()
        localtimezone = tzlocal()
        result = self.client.Fax.query_faxes(created_after=datetime.now(localtimezone))
        self.logger.debug('query_result={}'.format(result))
        self.assertTrue(result.success)
        self.assertTrue(len(result.data) == 0)
        self.assertTrue(result.paging.total == 0)

        self._pause()
        result = self.client.Fax.query_faxes(created_before=datetime.now())
        self.logger.debug('query_result={}'.format(result))
        self.assertTrue(result.success)
        self.assertTrue(len(result.data) > 0)
        self.assertTrue(result.paging.total > 0)

    def test_area_codes(self):
        result = self.client.PhoneNumber.get_area_codes(page=3, per_page=10)
        self.logger.debug('area_codes_results={}'.format(result))
        self._assert_paging_params(result, 3, 10)

    def test_phax_codes_json(self):
        test_metadata = {'testkey': 'testval'}
        result = self.client.PhaxCode.create_phax_code_json_response(json.dumps(test_metadata))
        self.logger.debug('create_phax_code_result={}'.format(result))
        self.assertTrue(result.success)
        phax_id = result.data.identifier

        self._pause()
        result = self.client.PhaxCode.get_phax_code_json_response(phax_code_id=phax_id)
        self.logger.debug('get_phax_code_result={}'.format(result))
        self.assertTrue(result.success)

        metadata_dict = json.loads(result.data.metadata)
        self.assertDictEqual(metadata_dict, test_metadata)

    def test_phax_codes_png(self):
        test_metadata = "{'testkey': 'testval'}"
        result = self.client.PhaxCode.get_phax_code_png_response('Y3jOfA')
        self.logger.debug('create_phax_code_result={}'.format(result))

        self._pause()
        result = self.client.PhaxCode.get_phax_code_png_response()
        self.logger.debug('create_phax_code_result={}'.format(result))

        self._pause()
        result = self.client.PhaxCode.create_phax_code_png_response(metadata=test_metadata)
        self.logger.debug('create_phax_code_result={}'.format(result))

    def test_exceptions(self):
        self.assertRaises(ApiException, self.client.Fax.get_file, 36965299, thumbnail='x')

