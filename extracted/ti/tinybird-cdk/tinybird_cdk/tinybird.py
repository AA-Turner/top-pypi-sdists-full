import time
import urllib.parse

import httpx
import humanize
import json
import random

from . import config, errors, formats, logger
from typing import Optional


class Client:
    '''Tinybird client. All connectors have an instance of this class.'''

    DS_PATH      = '/v0/datasources'
    SQL_PATH     = '/v0/sql'
    EVENTS_PATH  = '/v0/events'
    LINKERS_PATH = '/v0/linkers'

    JOB_POLL_PERIOD_S     = 1.0
    MAX_RETRIES           = 5
    MAX_RATE_LIMIT_WAIT_S = 60*60
    MIN_WAIT_S = 60

    # By default, HTTPX uses a timeout of 5s. David said in
    #
    #     https://3.basecamp.com/4360466/buckets/25800185/messages/4818119130#__recording_4827620424
    #
    # that this does not suffice for reading, because Tinybird starts responding
    # when the work has been completed and large payloads may need time. By now,
    # we simply disable it. The rest of timeouts are kept at 5s.
    #
    # See https://www.python-httpx.org/advanced/#timeout-configuration.
    TIMEOUT = httpx.Timeout(5.0, read=None)

    def __init__(self, token: Optional[str]=None, cdk_tag: Optional[str]=None, tb_endpoint: Optional[str]=None):
        self.tb_cdk_token = token or config.get('TB_CDK_TOKEN')
        self.tb_cdk_tag = cdk_tag or config.get('TB_CDK_TAG')
        self.tb_cdk_endpoint = tb_endpoint or config.get('TB_CDK_ENDPOINT', default='https://api.tinybird.co').rstrip('/')
        headers = {
            'Accept-Encoding': 'gzip',
            'Authorization': f"Bearer {self.tb_cdk_token}",
            'X-TB-CDK-TAG': self.tb_cdk_tag
        }
        self.client = httpx.Client(headers=headers, timeout=self.TIMEOUT, follow_redirects=True)

    # --- Append ----------------------------------------------------------------------------------

    def append_data(self, data, data_source, fmt):
        params = {'mode': 'append', 'name': data_source, 'format': fmt, **self._fmt_params(fmt)}
        headers = {'Content-Type': formats.mime_type_for(fmt)}
        hsize = humanize.naturalsize(len(data))
        logger.info(f'Appending {hsize} of data to {data_source}, format = {fmt}')
        return self._post(self.DS_PATH, params=params, headers=headers, content=data)

    def append_file(self, filename, data_source, fmt):
        params = {'mode': 'append', 'name': data_source, 'format': fmt, **self._fmt_params(fmt)}
        logger.info(f'Appending {filename} to {data_source}, format = {fmt}')
        return self._upload_file(filename, fmt, params)

    def append_url(self, url, data_source, fmt):
        params = {'mode': 'append', 'name': data_source, 'format': fmt, 'url': url, **self._fmt_params(fmt)}
        logger.info(f'Appending {url} to {data_source}, format = {fmt}')
        job = self._post(self.DS_PATH, params=params).json()
        return self.wait_for_job(job)

    # --- Replace ---------------------------------------------------------------------------------

    def replace_data(self, data, data_source, fmt, replace_condition=None):
        params = {'mode': 'replace', 'name': data_source, 'format': fmt, **self._fmt_params(fmt)}
        headers = {'Content-Type': formats.mime_type_for(fmt)}
        hsize = humanize.naturalsize(len(data))
        msg = [f'Replacing {data_source} with {hsize} of data', f'format = {fmt}']

        if replace_condition:
            params['replace_condition'] = replace_condition
            msg.append(f'replace condition = "{replace_condition}"')

        logger.info(', '.join(msg))
        return self._post(self.DS_PATH, params=params, headers=headers, content=data)

    def replace_file(self, filename, data_source, fmt, replace_condition=None):
        params = {'mode': 'replace', 'name': data_source, 'format': fmt, **self._fmt_params(fmt)}
        msg = [f'Replacing {data_source} with {filename}', f'format = {fmt}']

        if replace_condition:
            params['replace_condition'] = replace_condition
            msg.append(f'replace condition = "{replace_condition}"')

        logger.info(', '.join(msg))
        return self._upload_file(filename, fmt, params)

    def replace_url(self, url, data_source, fmt, replace_condition=None):
        params = {'mode': 'replace', 'name': data_source, 'format': fmt, 'url': url, **self._fmt_params(fmt)}
        msg = [f'Replacing {data_source} with {url}', f'format = {fmt}']
        data={}

        if replace_condition:
            data['replace_condition'] = replace_condition
            msg.append(f'replace condition = "{replace_condition}"')

        logger.info(', '.join(msg))
        job = self._post(self.DS_PATH, params=params, data=data).json()
        return self.wait_for_job(job)

    # --- Truncate --------------------------------------------------------------------------------

    def truncate(self, data_source):
        logger.info(f'Truncating {data_source}')
        return self._post(f'{self.DS_PATH}/{urllib.parse.quote(data_source)}/truncate')

    # --- Alter -----------------------------------------------------------------------------------

    def alter(self, data_source: str, schema: str):
        logger.info(f'Altering {data_source} with schema {schema}')
        params = {'name': data_source, 'schema': schema}
        return self._post(f'{self.DS_PATH}/{urllib.parse.quote(data_source)}/alter', params=params)

    # --- Linker -----------------------------------------------------------------------------------

    def alter_linker(self, data_source: str, kind: str, schema: str):
        logger.info(f'Altering linker for {data_source} with schema {schema}')
        params = {'name': data_source, 'service': kind, 'query': schema}
        return self._put(f'{self.LINKERS_PATH}/{urllib.parse.quote(data_source)}', params=params)

    def linker(self, data_source: str, kind: str):
        logger.info(f'Getting linker for data source {data_source}')
        params = {'service': kind}
        headers = {
            'Authorization': f"Bearer {self.tb_cdk_token}",
            'X-TB-CDK-TAG': self.tb_cdk_tag
        }
        response = self._get(f'{self.LINKERS_PATH}/{urllib.parse.quote(data_source)}', params=params, headers=headers)
        return response.json()

    # --- Data Source -----------------------------------------------------------------------------------

    def data_source(self, data_source: str):
        logger.info(f'Getting info for data source {data_source}')
        response = self._get(f'{self.DS_PATH}/{urllib.parse.quote(data_source)}')
        return response.json()

    # --- Events ----------------------------------------------------------------------------------

    def append_event(self, event, data_source):
        params = {'name': data_source}
        return self._post(self.EVENTS_PATH, params=params, content=event)

    def append_events(self, events, data_source):
        params = {'name': data_source}
        return self._post(self.EVENTS_PATH, params=params, content='\n'.join(events))

    # --- Query -----------------------------------------------------------------------------------

    def query(self, sql, pipe=None, scalar=False):
        logger.info(f'Executing query "{sql}", pipe = {pipe}')

        # HTTPX automatically URL-encodes parameter values, the query will be
        # %-encoded.
        params = {'q': sql + ' FORMAT JSON'}

        if pipe:
            params['pipeline'] = pipe

        response = self._get(self.SQL_PATH, params=params)
        data = response.json()['data']

        if scalar:
            return list(data[0].values())[0] if data else None

        return data

    # --- Utilities -------------------------------------------------------------------------------

    def wait_for_job(self, job):
        job_id = job['job_id']
        job_url = job['job_url']
        attempts = 0

        while True:
            attempts += 1

            time.sleep(self.JOB_POLL_PERIOD_S)
            response = self._get(job_url)
            job_status = response.json()['status']

            if job_status == 'done':
                logger.info(f'Job {job_id} completed successfully')
                return response

            if job_status == 'error':
                logger.error(f'Job {job_id} failed')
                raise errors.JobError(self._error_message_from_response(response), job_id)

            # We poll frequently, but only log from time to time, because in
            # large ingestions the log had too much noise/signal for my taste.
            if attempts % 5 == 1:
                logger.debug(f'Waiting for job {job_id}, current status is "{job_status}"')

    def _upload_file(self, filename, fmt, params):
        with open(filename, 'rb') as file_object:
            files = {fmt: (filename, file_object, formats.mime_type_for(fmt))}
            return self._post(self.DS_PATH, params=params, files=files)

    def _post(self, path, headers=None, **kwargs):
        if headers is None:
            headers = {}
        return self._request('POST', path, headers=headers, **kwargs)

    def _put(self, path, headers=None, **kwargs):
        if headers is None:
            headers = {}
        return self._request('PUT', path, headers=headers, **kwargs)

    def _get(self, path, headers=None, **kwargs):
        if headers is None:
            headers = {}
        return self._request('GET', path, headers=headers, **kwargs)

    def _request(self, method, url_or_path, headers, **kwargs):
        if url_or_path.startswith('/'):
            url = f'{self.tb_cdk_endpoint}{url_or_path}'
        else:
            url = url_or_path

        retries = 0
        start = time.monotonic()

        while True:
            response = self.client.request(method, url, headers=headers, **kwargs)
            if response.is_success:
                return response

            status_code = response.status_code
            if retry_after_s := self._should_retry(method, status_code, response.headers, retries):
                elapsed = time.monotonic() - start
                if elapsed + retry_after_s <= self.MAX_RATE_LIMIT_WAIT_S:
                    logger.warning(f'{status_code} code for {method} {url}, retrying in {retry_after_s} seconds')
                    time.sleep(retry_after_s)
                    retries += 1
                    continue
                raise errors.RateLimitedForTooLongError(self.MAX_RATE_LIMIT_WAIT_S)
            raise errors.HTTPError(method, response, self._error_message_from_response(response), self.get_job_from_response(response))

    def _error_message_from_response(self, response):
        if ('Content-Type' not in response.headers or not response.headers["Content-Type"].startswith("application/json")):
            return response.text # HFI returns text/plain with the message in the body

        error_messages = []

        try:
            response_message = response.json()
        except json.JSONDecodeError:
            return response.text

        if 'error' in response_message:
            error_messages.append(response_message['error'])
        if 'errors' in response_message:
            error_messages += response_message['errors']
        return ', '.join(error_messages)

    def get_job_from_response(self, response) -> dict:
        try:
            if ('Content-Type' not in response.headers or not response.headers["Content-Type"].startswith("application/json")):
                return {}
        except Exception:
            return {}

        try:
            response_message = response.json()
        except json.JSONDecodeError:
            return {}

        if 'job_id' in response_message:
            job_id = response_message['job_id']
            return {
                'job_id': job_id,
            }
        return {}

    # Status codes are documented in
    #
    #     https://www.tinybird.co/docs/api-reference/api-reference.html#errors
    #
    # Rate limiting is documented in
    #
    #     https://www.tinybird.co/docs/api-reference/api-reference.html#limits-title.
    #
    # We discussed error handling in
    #
    #     https://3.basecamp.com/4360466/buckets/25800185/messages/4818119130
    #
    # In particular, retries on 500s were discarded except for 502s for GET.
    def _should_retry(self, method, status_code, headers, retries):
        # Rate limiting.
        if status_code == 429 and retries < self.MAX_RETRIES:
            # Exponential backoff with some random jitter to avoid deadlocks
            return max(
                int(headers['Retry-After']) * 2 ** retries + random.randint(0, 9),
                self.MIN_WAIT_S
            )

        # Timeout: Retry safety considerations in the discussion linked above.
        if status_code == 408 and retries < self.MAX_RETRIES:
            return 2**(retries + 1)

        # Bad Gateway: Communication hiccup between NGINX and Analytics.
        if status_code == 502 and method in ('GET', 'HEAD'):
            return 2**(retries + 1)

        return None

    # This is a compromise.
    #
    # If format options were generic, we should model them. Connectors would
    # pass them together with export objects, and the private export methods
    # would forward them to this Tinybird HTTP client to translate them into
    # query params.
    #
    # That is doable, and I implemented it, but the overhead once written seemed
    # disproportionate because the actual situation is very asymmetrical.
    #
    # Instead, we can *require* connectors to generate CSV using these settings.
    # Only CSV has a need for format options. From a pragmatic point of view,
    # hard-coding this down here seems a good a trade-off to me.
    #
    # If time proves connectors need flexibility for format options, then I
    # believe the refactor sketched above could be the way to go.
    def _fmt_params(self, fmt):
        if fmt == formats.CSV:
            # We set these parameters to prevent the server from guessing. We
            # control the exports, guessing would be an unnecessary risk and
            # overhead.
            #
            # HTTPX automatically URL-encodes parameter values, the newline will
            # be %-encoded.
            return {'dialect_delimiter': ',', 'dialect_new_line': '\n'}
        return {}
