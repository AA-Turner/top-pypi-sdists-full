import asyncio
import itertools
import os
import time
import datetime
import base64
import getpass
import json
import logging
import math
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  # 36.0.0
import aiohttp       # 3.8.1
import pandas as pd  # 1.4.2
from .hyper_log_log import HyperLogLog
from .average import Average
from .tdigest import TDigest
from .rate import Rate
from .std import Std
from .capture import CaptureMin, CaptureMax, CaptureAnyMin, CaptureAnyMax


def _logtime(ts):
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(ts))

TZINFO = datetime.datetime.now().astimezone().tzinfo
APPLICATION_JSON = 'application/json'
def _get_utc_timestamp(ts):    
    if ts.tz is None:
        ts = ts.tz_localize(tz=TZINFO)
    return ts.timestamp()


def pprint(value, indent=4, depth=0):
    if isinstance(value, dict):
        # empty dict, printed as simple
        if len(value) == 0:
            print('{}', end='')
            return
        # non-empty dict, one item per line
        depth += indent
        print('{\n' + ' ' * depth, end='')
        for i, (k, v) in enumerate(value.items()):
            print(json.dumps(k), end=':')
            pprint(v, indent, depth)
            if i < len(value)-1:  # not last item
                print(',\n' + ' '*depth, end='')
            else:  # last item
                depth -= indent
                print('\n' + ' '*depth, end='')
        print('}', end='')
    elif isinstance(value, list):
        # empty list is printed as simple
        if len(value) == 0:
            print('[]', end='')
            return
        # non-empty list, check if expression
        any_complex = False
        if not isinstance(value[0], str) or not value[0].startswith('$'):
            for e in value:
                if (isinstance(e, dict) and len(e) > 0) or \
                   (isinstance(e, list) and len(e) > 0):
                    any_complex = True
                    break
        if any_complex:
            depth += indent
            print('[\n'+' '*depth, end='')
            for i, e in enumerate(value):
                pprint(e, indent, depth)
                if i < len(value)-1:  # not last item
                    print(',\n' + ' '*depth, end='')
                else:  # last item
                    depth -= indent
                    print('\n' + ' '*depth, end='')
            print(']', end='')
        else:
            print('[', end='')
            for i, e in enumerate(value):
                pprint(e, indent, depth)
                if i < len(value)-1:  # not last item
                    print(',', end='')
            print(']', end='')
    elif isinstance(value, str):  # prevent escaped unicode
        print(f'"{value}"', end='')
    else:  # simple
        print(json.dumps(value), end='')


class UnexpectedStatus(Exception):
    def __init__(self, status, message):
        self.status = status
        self.message = f'{status}: {message}'
        super().__init__(self.message)


class Client:
    ACCESS_TOKEN_TIMEOUT = 86400 / 2
    SUPPORT_STRATEGIES = ['custom', 'local', 'remote', 'controller']

    def __init__(self, url, user, tenant, password, ssl=True, burst=1, retry=0, conn_timeout=30, read_timeout=300, strategy="custom", controller=None):
        self.strategy = strategy
        self.controller = controller
        self.url = url        # base url
        self.user = user      # user name
        self.tenant = tenant  # tenant name
        self.password = base64.b64encode(password.encode('utf-8')).decode()  # base64 encoded password
        self.ssl = ssl  # False to disable certificate verification
        self.retry = retry
        self.burst = burst
        self._sem = asyncio.Semaphore(burst)  # semaphone to throttle concurrent burst
        self._headers = {
            'Content-Type': APPLICATION_JSON
        }
        if self.strategy not in Client.SUPPORT_STRATEGIES:
            raise ValueError(f"unsupported strategy {self.strategy}, supported strategies are {Client.SUPPORT_STRATEGIES}")
        if self.strategy == 'controller' and self.controller is None:
            raise TypeError('controller strategy requires "controller" argument')

        self._last_auth = 0  # timestamp of last authenticate in seconds since Eopch
        self._session = aiohttp.ClientSession(trust_env=True)
        self.timeout = aiohttp.ClientTimeout(total=None, connect=None, sock_connect=conn_timeout, sock_read=read_timeout)

    async def _authenticate(self):
        auth_data = {
            'strategy': 'custom',
            'account': f'{self.user}@{self.tenant}',  # user account '<user>@<tenant>'
            'password': self.password                 # user password
        }
        # bringup
        logging.info('bringup')
        url = self.url + f'/bringup?name={self.tenant}'
        async with self._session.get(url, headers=self._headers, ssl=self.ssl) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise UnexpectedStatus(resp.status, text)
            bringup = await resp.json()
        # do captcha when enabled
        if bringup.get('tenantID') is not None:
            self.tenant_id = bringup['tenantID']
        if bringup['captchaEnabled']:
            logging.info('captcha')
            key = os.urandom(24)
            iv = os.urandom(16)
            data = {
                'key': key.hex(),
                'iv': iv.hex()
            }
            async with self._session.post(self.url+'/captcha', json=data, headers=self._headers, ssl=self.ssl) as resp:
                if resp.status != 201:
                    text = await resp.text()
                    raise UnexpectedStatus(resp.status, text)
                # decrypt answer
                captcha = await resp.json()
                ct = base64.b64decode(captcha['answer'])
                decryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
                answer_b = decryptor.update(ct) + decryptor.finalize()
                answer_s = answer_b.decode('utf8')
                auth_data['captcha'] = {
                    '_id': captcha['_id'],
                    'answer': answer_s
                }
        # do authenticate
        if 'allowLogin' in bringup:
            if (self.strategy == 'custom' or self.strategy == 'local') and bringup['allowLogin']['local'] is False:
                raise ValueError('local login is not allowed')
            elif self.strategy == 'remote' and bringup['allowLogin']['remote'] is False:
                raise ValueError('remote login is not allowed')
            elif self.strategy == 'controller':
                if bringup['allowLogin']['controller'] is False:
                    raise ValueError('controller login is not allowed')
                elif len([x for x in bringup['allowLogin']['controller'] if x['_id'] == self.controller]) == 0:
                    raise ValueError(f'controller is not found, available controllers are:{bringup["allowLogin"]["controller"]}')
                auth_data['controller'] = self.controller
            auth_data['strategy'] = self.strategy

        url = self.url+'/authentication'
        async with self._session.post(url, json=auth_data, headers=self._headers, ssl=self.ssl) as resp:
            if resp.status != 201:
                text = await resp.text()
                raise UnexpectedStatus(resp.status, text)
            body = await resp.json()
            self._headers = {
                'Content-Type': APPLICATION_JSON,
                'Authorization': body['accessToken']
            }
            self._last_auth = time.time()
            logging.info('authenticate done')

    async def _request(self, method, path, code, data=None, test_fn=None):
        # authenticate if required
        if time.time() - self._last_auth >= Client.ACCESS_TOKEN_TIMEOUT:
            retry_count = 0
            while True:
                try:
                    await self._authenticate()
                    break
                except aiohttp.ClientError as e:
                    if retry_count < self.retry:  # user asks for retry
                        retry_count += 1
                        logging.warning(f'retry {retry_count}-th time')
                    else:
                        logging.error(f'authentication fail {e}')
                        raise e
        # send the request
        retry_count = 0
        meta = {}
        async with self._sem:
            # test_fn is a function to check if the request should be sent
            if test_fn is not None and test_fn() is False:
                return 0, None, meta
            ts_send = datetime.datetime.now()
            while True:
                try:
                    # logging.debug(f'{method} {path}')
                    async with self._session.request(method, self.url+path, json=data, headers=self._headers, ssl=self.ssl, timeout=self.timeout) as resp:
                        if resp.status in code:  # expected status code
                            rlt = None
                            ts_head = datetime.datetime.now()
                            if resp.content_type == APPLICATION_JSON:
                                data = await resp.json()
                                if 'rlt' in data:
                                    rlt = data['rlt']
                                if 'status' in data:
                                    meta = data['status']
                            ts_done = datetime.datetime.now()
                            logging.debug(f'transfer req={ts_send.strftime("%Y/%m/%d %H:%M:%S")} head={ts_head.strftime("%Y/%m/%d %H:%M:%S")} data={ts_done.strftime("%Y/%m/%d %H:%M:%S")}')
                            wrk_total = 0
                            if "wrk_wait" in meta:
                                wrk_total += meta["wrk_wait"]
                            if "wrk_exec" in meta:
                                wrk_total += meta["wrk_exec"]
                            if "wrk_resp" in meta:
                                wrk_total += meta["wrk_resp"]
                            meta["srv_wait"] = (ts_head - ts_send).total_seconds()*1000 - wrk_total
                            meta["srv_resp"] = (ts_done - ts_head).total_seconds()*1000
                            return resp.status, rlt, meta
                        elif resp.status == 202:  # API server asks for retry
                            text = await resp.text()
                            logging.debug(f'status={resp.status} message={text} path={path}')
                            continue
                        elif resp.status == 500:  # General error contain retry information
                            text = await resp.text()
                            if 'Warning' in text or 'Please try again' in text:
                                logging.debug(f'status={resp.status} message={text} path={path}')
                                continue
                            else:
                                logging.error(f'unexpected status={resp.status} message={text} path={path}')
                                raise UnexpectedStatus(resp.status, text)
                        else:
                            text = await resp.text()
                            logging.error(f'unexpected status={resp.status} message={text} path={path}')
                            raise UnexpectedStatus(resp.status, text)
                except aiohttp.ClientError as e:
                    if retry_count < self.retry:  # user asks for retry
                        retry_count += 1
                        logging.error(f'{method} {path} - {e}, retry {retry_count}')
                    else:
                        logging.error(f'{method} {path} - {e}, fail')
                        raise e
                except Exception as e:
                    logging.error(f'{method} {path} - {e}, fail')
                    raise e


class System(Client):
    def __init__(self, url, user=None, password=None, ssl=True, retry=0, conn_timeout=30, read_timeout=300, strategy="custom", controller=None):
        """Construct object to send system requests.

        Args:
            url: The base url of API server.
            user: The username.
            password: The password.
            ssl: `False` to relax certificate verification.
            retry: Number of retry at network failure.
        """
        if user is None:
            user = input('User:')
        if password is None:
            password = getpass.getpass('Password:')
        super().__init__(url, user, 'system', password, ssl=ssl, retry=retry, conn_timeout=conn_timeout, read_timeout=read_timeout, strategy=strategy, controller=controller)

    async def close(self):
        """Close the underlying connections gracefully. If the event loop is stopped before
        the system object is closed, a warning is emitted.
        """
        await self._session.close()
        await asyncio.sleep(0.250)

    async def get_system(self):
        """Get system config and status

        Returns:
            System descriptor. For example::

            {
                "config":{
                    "burst":1,
                    "retry":1,
                    "maxTasks":65536
                },
                "status":{
                    "created":"2022-02-17T10:18:06.714Z",
                    "modified":"2022-03-14T17:44:46.717Z",
                    "size":38,
                    "maxId":36
                }
            }
        """
        # 200 - ok, return read system descriptor
        status, rlt, _ = await self._request('GET', '/cq/config', [200])
        logging.info(f'status={status}')
        return rlt

    async def set_system(self, config):
        """Set system config

        Args:
            config: The config part of system descriptor. See `System.get_system()`

        Returns:
            The modified system descriptor.
        """
        # 200 - ok, return modified system descriptor
        status, rlt, _ = await self._request('PATCH', '/cq/config', [200], config)
        logging.info(f'status={status}')
        return rlt

    async def get_all_tenants(self):
        """Gets config and status of all tenants.

        Returns:
            Dictionary of tenant descriptors indexed by tenant id.
        """
        # 200 - ok, return array of tenant descriptor
        status, rlt, _ = await self._request('GET', '/cq/config/tenant', [200])
        logging.info(f'status={status}')
        return rlt

    async def get_tenant(self, tid):
        """Get tenant config and status.

        Args:
            tid: The target tenant id

        Returns:
            Descriptor of the target tenant. For example::

            {
                "_id":0,
                "config":{
                    "limit":10000000000
                },
                "status":{
                    "created":"2022-03-14T17:46:28.860Z",
                    "modified":"2022-03-14T18:31:51.716Z",
                    "size":0
                }
            }
        """
        # 200 - ok, return read tenant descriptor
        status, rlt, _ = await self._request('GET', f'/cq/config/tenant/{tid}', [200])
        logging.info(f'status={status}')
        return rlt if status == 200 else None

    async def create_tenant(self, tid, config):
        """Creates a new tenant

        Args:
            tid: The target tenant id
            config: The config part of tenant descriptor. See `System.get_tenant()`

        Returns:
            Descriptor of the created tenant
        """
        # 200 - ok, return created tenant descriptor
        status, rlt, _ = await self._request('POST', f'/cq/config/tenant/{tid}', [200], config)
        logging.info(f'status={status} tid={tid}')
        return rlt

    async def update_tenant(self, tid, config):
        """Updates tenant config

        Args:
            tid: The target tenant id
            config: The config part of tenant descriptor. See `System.get_tenant()`

        Returns:
            Descriptor of the target tenant
        """
        # 200 - ok, return modified tenant descriptor
        status, rlt, _ = await self._request('PATCH', f'/cq/config/tenant/{tid}', [200], config)
        logging.info(f'status={status} tid={tid}')
        return rlt

    async def delete_tenant(self, tid):
        """Deletes tenant and its associated data.

        Args:
            tid: The target tenant id
        """
        # 204 - ok, return None
        status, *_ = await self._request('DELETE', f'/cq/config/tenant/{tid}', [204])
        logging.info(f'status={status} tid={tid}')


def desc_dataframe(desc_list):
    desc_dict = {}
    for dset in desc_list:
        item = dset['config'].copy()
        item.update(dset['status'])
        item.pop('pipeline', None)
        desc_dict[dset['_id']] = item
    return pd.DataFrame.from_dict(desc_dict, orient='index')


class Reader:
    def __init__(self, client, pipeline):
        self._client = client
        self.pipeline = pipeline
        self.count = 0
        self.size = 0
        self.sub_size = 0
        self.meta = None

    def test_fn(self):
        return self.count < self.size

    async def _exec(self, start, end):
        start = _get_utc_timestamp(start)
        end = _get_utc_timestamp(end)
        pipeline = self.pipeline.copy()
        if 'config' not in pipeline:
            pipeline['config'] = {}
        pipeline['config']['start'] = start
        pipeline['config']['end'] = end
        pipeline['config']['size'] = self.sub_size
        pipeline['config']['series'] = self.series
        if self.fields is not None:
            pipeline['config']['fields'] = self.fields
        status, rlt, meta = await self._client._request('POST', '/record', [200], pipeline, self.test_fn)
        meta["start"] = start
        if status != 0:
            logging.info(f'/record status={status} start={_logtime(start)} end={_logtime(end)} series={self.series} meta={meta}')
        if rlt is not None and len(rlt) > 0:
            self.count += len(rlt) - 1  # skip first row, which is header
            return pd.DataFrame(rlt[1:], columns=rlt[0]), meta
        return pd.DataFrame(), meta  # empty dataframe is returned if no data

    def read_perf(self):
        if self.meta is None:
            return pd.DataFrame()
        return pd.DataFrame.from_dict(self.meta)
    
    async def read_data(self, dts, series='full', size=100, fields=None, sub_size=None):
        """Execute adhoc request and read its data
        Args:
            dts: pd.DatetimeIndex, using pd.date_range to generate.
            series: 'full', 'hour', 'day' or 'log
            size: number of rows to read
            fields: list of field names
            sub_size: size of each dts query, default is size
        Returns:
            The record of dataframe.
        """
        if sub_size is None:
            sub_size = size
        self.sub_size = sub_size
        self.size = size
        self.count = 0
        self.series = f"%{series}"  # present in literal
        self.fields = fields
        tasks = []
        for i in range(0, len(dts)):
            start_time = dts[i]
            end_time = dts[i] + pd.Timedelta(dts.freq)
            tasks.append(asyncio.create_task(self._exec(start_time, end_time)))
        try:
            results = await asyncio.gather(*tasks)
            rlts, metas = zip(*results)
            df = pd.DataFrame()
            self.meta = list(metas)
            for rlt in rlts:
                df = pd.concat([df, rlt], ignore_index=True, copy=False)
                if len(df) >= self.size:
                    break
            if self.fields is not None and len(df) != 0:
                return df.head(self.size)[self.fields]
            return df.head(self.size)
        except Exception as e:
            logging.error(f'execute record fail {e}')
            for task in tasks:
                task.cancel()
            raise e


class Tenant(Client):
    def __init__(self, url, user=None, tenant=None, password=None, ssl=True, burst=1, retry=0, conn_timeout=30, read_timeout=300, strategy="custom", controller=None):
        if user is None:
            user = input('User:')
        if tenant is None:
            tenant = input('Tenant:')
        if password is None:
            password = getpass.getpass('Password:')
        super().__init__(url, user, tenant, password, ssl=ssl, burst=burst, retry=retry, conn_timeout=conn_timeout, read_timeout=read_timeout, strategy=strategy, controller=controller)

    async def close(self):
        """Close the underlying connections gracefully. If the event loop is stopped before
        the tenant object is closed, a warning is emitted.
        """
        await self._session.close()
        await asyncio.sleep(0.250)

    async def create_adhoc(self, pipeline):
        # 201 - ok, return adhoc id
        status, rlt, _ = await self._request('POST', '/pipeline', [201], pipeline)
        logging.info(f'status={status} rlt={rlt}')
        return rlt

    async def execute_adhoc(self, pid, start, end, series):
        # 200 - ok, return tabular data
        # 202 - accepted, try again to get data
        status, rlt, meta = await self._request('GET', f'/pipeline/{pid}?start={start}&end={end}&series={series}', [200])
        logging.info(f'status={status} pid={pid} start={_logtime(start)} end={_logtime(end)} series={series}, meta={meta}')
        rlt = rlt if isinstance(rlt, list) else []
        return rlt, meta

    async def create_reader(self, pipeline):
        return Reader(self, pipeline)

    async def get_all_datasets(self):
        # 200 - ok, return array of dataset descriptor
        status, rlt, _ = await self._request('GET', '/cq/dataset', [200])
        logging.info(f'status={status} rlt={rlt}')
        return rlt

    async def get_mgr_config(self, req):
        # 200 - ok, return mgr configuration
        status, rlt, _ = await self._request('GET', f"/mgr/{req}", [200])
        logging.info(f'status={status}')
        return rlt

    async def list_all_datasets(self):
        dset_list = await self.get_all_datasets()
        return desc_dataframe(dset_list)

    async def delete_all_datasets(self):
        # 204 - ok, return None
        status, rlt, _ = await self._request('DELETE', '/cq/dataset', [204])
        logging.info(f'status={status} rlt={rlt}')
        return rlt

    async def create_dataset(self, dsid, config):
        # 200 - ok, return created dataset descriptor
        status, rlt, _ = await self._request('POST', f'/cq/dataset/{dsid}', [200], config)
        logging.info(f'status={status} dsid={dsid}')
        return rlt

    async def get_dataset(self, dsid, missing_ok=False):
        # 200 - ok, return read dataset descriptor
        # 404 - error, dataset not found
        code = [200, 404] if missing_ok else [200]
        status, rlt, _ = await self._request('GET', f'/cq/dataset/{dsid}', code)
        if status != 404 or not missing_ok:
            logging.info(f'status={status} dsid={dsid}')
            return rlt
        else:
            return None

    async def update_dataset(self, dsid, config, missing_ok=False):
        # 200 - ok, return modified dataset descriptor
        # 404 - error, dataset not found
        code = [200, 404] if missing_ok else [200]
        status, rlt, _ = await self._request('PATCH', f'/cq/dataset/{dsid}', code, config)
        if status != 404 or not missing_ok:
            logging.info(f'status={status} dsid={dsid}')
            return rlt
        else:
            return None

    async def delete_dataset(self, dsid, missing_ok=False):
        # 204 - ok, return None
        # 404 - error, dataset not found
        code = [204, 404] if missing_ok else [204]
        status, rlt, _ = await self._request('DELETE', f'/cq/dataset/{dsid}', code)
        if status != 404 or not missing_ok:
            logging.info(f'status={status} dsid={dsid}')
        return rlt

    async def get_all_pipelines(self, dsid):
        # 200 - ok, return array of pipeline descriptors
        status, rlt, _ = await self._request('GET', f'/cq/dataset/{dsid}/pipeline', [200])
        logging.info(f'status={status} dsid={dsid}')
        return rlt

    async def list_all_pipelines(self, dsid):
        pipe_list = await self.get_all_pipelines(dsid)
        return desc_dataframe(pipe_list)

    async def delete_all_pipelines(self, dsid):
        # 204 - ok, return None
        status, rlt = await self._request('DELETE', f'/cq/dataset/{dsid}/pipeline', [204])
        logging.info(f'status={status} dsid={dsid}')
        return rlt

    async def create_pipeline(self, dsid, plid, config):
        # 200 - ok, return created pipeline descriptor
        status, rlt, _ = await self._request('POST', f'/cq/dataset/{dsid}/pipeline/{plid}', [200], config)
        logging.info(f'status={status} dsid={dsid} plid={plid}')
        return rlt

    async def get_pipeline(self, dsid, plid, missing_ok=False):
        # 200 - ok, return read pipeline descriptor
        # 404 - error, pipeline not found
        code = [200, 404] if missing_ok else [200]
        status, rlt, _ = await self._request('GET', f'/cq/dataset/{dsid}/pipeline/{plid}', code)
        if status != 404 or not missing_ok:
            logging.info(f'status={status} dsid={dsid} plid={plid}')
            return rlt
        else:
            return None

    async def update_pipeline(self, dsid, plid, config, missing_ok=False):
        # 200 - ok, return modified pipeline descriptor
        # 404 - error, dataset not found
        code = [200, 404] if missing_ok else [200]
        status, rlt = await self._request('PATCH', f'/cq/dataset/{dsid}/pipeline/{plid}', code, config)
        if status != 404 or not missing_ok:
            logging.info(f'status={status} dsid={dsid} plid={plid}')
            return rlt
        else:
            return None

    async def delete_pipeline(self, dsid, plid, missing_ok=False):
        # 204 - ok, return None
        # 404 - error, pipeline not found
        code = [204, 404] if missing_ok else [204]
        status, rlt, _ = await self._request('DELETE', f'/cq/dataset/{dsid}/pipeline/{plid}', code)
        if status != 404 or not missing_ok:
            logging.info(f'status={status} dsid={dsid} plid={plid}')
        return rlt

    async def patch_dataset_data(self, dsid, ts, overwrite=False):
        # 200 - ok, return dict of patch result (1:data, 0:no data)
        # 202 - accepted, try again to get data
        # 204 - future, return None
        # 400 - purged, return ??
        status, rlt, _  = await self._request('POST', f'/cq/dataset/{dsid}/task', [200, 204], {
            'ts': ts,
            'overwrite': overwrite
        })
        logging.info(f'status={status} dsid={dsid} ts={_logtime(ts)}')
        return None if status != 200 else rlt

    async def poll_dataset_data(self, dsid, ts):
        # 200 - ok, return [<row>,...]
        # 202 - scheduled task
        # 204 - future, return None
        status, rlt, _  = await self._request('POST', f'/cq/dataset/{dsid}/poll', [200, 204], {
            'ts': ts
        })
        logging.info(f'status={status} dsid={dsid} ts={_logtime(ts)}')
        return None if status != 200 else rlt

    async def query_dataset_data(self, dsid, ts):
        # 200 - ok, return dictionary of [<row>,...], key is str(plid)
        _, rlt, _  = await self._request('GET', f'/cq/dataset/{dsid}/data?ts={ts}', [200])
        return rlt if isinstance(rlt, dict) else {}

    async def query_pipeline_data(self, dsid, plid, ts):
        # 200 - ok, return [<row>,...]
        status, rlt, _  = await self._request('GET', f'/cq/dataset/{dsid}/pipeline/{plid}/data?ts={ts}', [200])
        logging.info(f'status={status} dsid={dsid} plid={plid} ts={_logtime(ts)}')
        return rlt if isinstance(rlt, list) else []


MOPER_MAP = {
    "$distinct": HyperLogLog,
    "$count": float,
    "$sum": float,
    "$capMin": CaptureMin,
    "$capMax": CaptureMax,
    "$capAnyMin": CaptureAnyMin,
    "$capAnyMax": CaptureAnyMax,
    "$std": Std,
    "$avg": Average,
    "$tDigest": TDigest,
    "$rate": Rate,
}


def _compute_kcol_mcol(pipeline):
    kcol = 0  # key columns
    mcol = 0  # mtr columns
    moper = []
    if 'bucket' in pipeline:
        for bkt in pipeline['bucket']:
            if bkt[0] in ['$distinctTuple', '$enumTuple', '$distinctTree']:
                # each field introduce one key column
                kcol += len(bkt[1]['fields'])
            else:
                # each tier introduce one key column
                kcol += 1
    if 'metric' in pipeline:
        # each metric introduce two columns
        mcol += len(pipeline['metric']) * 2
        for m in pipeline['metric']:
            if m[0] in MOPER_MAP:
                moper.append(m[0])
            elif m[0] in ['$capNum', '$capDate']:
                if 'method' not in m[1] or m[1]['method'] == '%max':
                    moper.append('$capMax')
                else:
                    moper.append('$capMin')
            elif m[0] == '$capAny':
                if 'method' not in m[1] or m[1]['method'] == '%max':
                    moper.append('$capAnyMax')
                else:
                    moper.append('$capAnyMin')
            else:
                raise ValueError(f"unknown metric operation {m[0]}")
    return kcol, mcol, moper


class _translate_table:
    def __init__(self, table, ts, kcol, mcol, moper):
        if isinstance(table, list) and len(table) > 0:
            self.table = table
        else:
            key_cols = list(itertools.repeat('!all', kcol))
            mtr_cols = list(itertools.repeat(math.nan, mcol))
            self.table = [key_cols+mtr_cols]
        self.ts = ts
        self.kcol = kcol
        self.moper = moper

    def __iter__(self):
        for input_row in self.table:
            output_row = [] if self.ts is None else [self.ts]
            for idx, elem in enumerate(input_row):
                if idx < self.kcol:
                    if isinstance(elem, list):
                        output_row.append(tuple(elem))
                    else:
                        output_row.append(elem)
                else:  # metric
                    moper_idx = int((idx-self.kcol)/2)
                    moper = self.moper[moper_idx]
                    output_row.append(MOPER_MAP[moper](elem))
            yield output_row


class _translate_rlts:
    def __init__(self, tsidx, rlts, kcol, mcol, moper):
        self.tsidx = tsidx
        self.rlts = rlts
        self.kcol = kcol
        self.mcol = mcol
        self.moper = moper

    def __iter__(self):
        for ts, rlt in zip(self.tsidx, self.rlts):
            yield _translate_table(rlt, ts, self.kcol, self.mcol, self.moper)


class Adhoc:
    @staticmethod
    async def _create(tenant, freq, pipeline):
        """Create Adhoc object to send adhoc request

        Args:
            tenant: tenant object to access API server
            freq: frequency in seconds
            pipeline: pipeline object

        Returns:
            The created Adhoc object.
        """
        self = Adhoc()
        self._tenant = tenant
        self.freq = freq
        self.pipeline = pipeline  # pipeline object
        self.pid = await self._tenant.create_adhoc(self.pipeline)
        self.meta = None
        return self

    async def _read_point(self, ts, series, columns=None, refresh=True):
        if refresh:
            await self._tenant.create_adhoc(self.pipeline)
        freq_str = f"{self.freq}s"
        delta = pd.Timedelta(freq_str)
        start = pd.Timestamp(ts).floor(freq_str)
        end = start + delta
        table, meta = await self._tenant.execute_adhoc(self.pid, _get_utc_timestamp(start), _get_utc_timestamp(end), series)
        kcol, mcol, moper = _compute_kcol_mcol(self.pipeline)
        return pd.DataFrame(_translate_table(table, None, kcol, mcol, moper), columns=columns), [meta]

    async def _read_range(self, dts, series, columns=None, refresh=True):
        if refresh:
            await self._tenant.create_adhoc(self.pipeline)
        tasks = []
        tsidx = []
        freq_str = f"{self.freq}s"
        rlts = None
        delta = pd.Timedelta(freq_str)
        for ts in dts:
            start = ts.floor(freq_str)
            end = start + delta
            coro = self._tenant.execute_adhoc(self.pid, _get_utc_timestamp(start), _get_utc_timestamp(end), series)
            tasks.append(asyncio.create_task(coro))
            tsidx.append(start)
        try:
            results = await asyncio.gather(*tasks)
            rlts, metas = zip(*results)
            metas = list(metas)
            for idx, ts in enumerate(tsidx):
                metas[idx]['start'] = ts
            
        except Exception as e:
            logging.error(f'read range fail {e}')
            for task in tasks:
                task.cancel()
            raise e
        kcol, mcol, moper = _compute_kcol_mcol(self.pipeline)
        iters = itertools.chain.from_iterable(_translate_rlts(tsidx, rlts, kcol, mcol, moper))
        return pd.DataFrame(iters, columns=columns), metas

    async def read_data(self, dts, *args, **kwargs):
        """Execute adhoc request and read its data

        Args:
            dts: str, pandas.Timestamp or array-like.
            series: 'full', 'hour' or 'day'.
            columns: column labels of frame. Defaults to None.
            refresh: refresh adhoc on API server. Defaults to True.

        Returns:
            The adhoc data frame.
        """
        try:
            ts = pd.Timestamp(dts)
        except Exception:
            ts = None
        if ts is None:
            rlt, meta = await self._read_range(dts, *args, **kwargs)
        else:
            rlt, meta = await self._read_point(ts, *args, **kwargs)
        self.meta = meta
        return rlt
    
    def read_perf(self):
        if self.meta is None:
            return pd.DataFrame()
        return pd.DataFrame.from_dict(self.meta)



class Pipeline:
    def __init__(self, tenant, dset, plid, conf):
        """Construct pipeline object to send pipeline requests.

        Args:
            tenant: tenant object to access API server
            dset: parent dataset object.
            plid: pipeline ID
            conf: pipeline config
        """
        self._tenant = tenant
        self._dset = dset
        self.plid = plid
        self.conf = conf

    async def _read_point(self, ts, columns=None):
        freq_str = f"{self._dset.conf['freq']}s"
        start = ts.floor(freq_str)
        table = await self._tenant.query_pipeline_data(self._dset.dsid, self.plid, _get_utc_timestamp(start))
        kcol, mcol, moper = _compute_kcol_mcol(self.conf['pipeline'])
        return pd.DataFrame(_translate_table(table, None, kcol, mcol, moper), columns=columns)

    async def _read_range(self, dts, columns=None):
        tasks = []
        tsidx = []
        freq_str = f"{self._dset.conf['freq']}s"
        rlts = None
        for ts in dts:
            start = ts.floor(freq_str)
            coro = self._tenant.query_pipeline_data(self._dset.dsid, self.plid, _get_utc_timestamp(start))
            tasks.append(asyncio.create_task(coro))
            tsidx.append(start)
        try:
            rlts = await asyncio.gather(*tasks)
        except Exception as e:
            logging.error(f'read range fail {e}')
            for task in tasks:
                task.cancel()
            raise e
        kcol, mcol, moper = _compute_kcol_mcol(self.conf['pipeline'])
        iters = itertools.chain.from_iterable(_translate_rlts(tsidx, rlts, kcol, mcol, moper))
        return pd.DataFrame(iters, columns=columns)

    async def read_data(self, dts, *args, **kwargs):
        """Read pipeline data on API server.

        Args:
            dts: pandas.Timestamp or array-like.
            columns: Column labels of frame. Defaults to None.

        Returns:
            The pipeline data frame.
        """
        try:
            ts = pd.Timestamp(dts)
        except Exception:
            ts = None
        if ts is None:
            return await self._read_range(dts, *args, **kwargs)
        else:
            return await self._read_point(ts, *args, **kwargs)


class Dataset:
    def __init__(self, tenant, dsid, conf):
        """Construct dataset object to send dataset requests. Don't call directly.

        Args:
            tenant: tenant object to access API server
            dsid: dataset id
            conf: dataset config
        """
        self._tenant = tenant
        self.dsid = dsid
        self.conf = conf

    async def list(self):
        """List all pipelines

        Returns:
            pandas.DataFrame: Pipeline configurations indexed by id.
        """
        pipe_list = await self._tenant.get_all_pipelines(self.dsid)
        return desc_dataframe(pipe_list)

    async def pipeline(self, plid):
        """Get pipeline

        Returns:
            dset: Pipeline object with the specified id.
        """
        desc = await self._tenant.get_pipeline(self.dsid, plid)
        return Pipeline(self._tenant, self, plid, desc['config'])

    async def patch(self, dts, overwrite=False):
        """Patch dataset data

        Args:
            dts: pandas.DatetimeIndex or array-like.
            overwrite: True to force overwrite data on API server. Defaults to False.

        Returns:
            Patch result in frame.
        """
        freq_str = f"{self.conf['freq']}s"
        tasks = []
        tsidx = []
        rlts = None
        for ts in dts:
            start = ts.floor(freq_str)
            coro = self._tenant.patch_dataset_data(self.dsid, _get_utc_timestamp(start), overwrite)
            tasks.append(asyncio.create_task(coro))
            tsidx.append(start)
        try:
            rlts = await asyncio.gather(*tasks)
        except Exception as e:
            logging.error(f'patch fail {e}')
            for task in tasks:
                task.cancel()
            raise e
        rlts = [elem if isinstance(elem, dict) else {} for elem in rlts]
        return pd.DataFrame(rlts, index=pd.Index(dts, name='timestamp'))

    async def poll(self, dts):
        """Check dataset data availability.

        Args:
            dts: pandas.DatetimeIndex or array-like.

        Returns:
            Patch result in frame.
        """
        freq_str = f"{self.conf['freq']}s"
        tasks = []
        tsidx = []
        rlts = None
        for ts in dts:
            start = ts.floor(freq_str)
            coro = self._tenant.poll_dataset_data(self.dsid, _get_utc_timestamp(start))
            tasks.append(asyncio.create_task(coro))
            tsidx.append(start)
        try:
            rlts = await asyncio.gather(*tasks)
        except Exception as e:
            logging.error(f'poll fail {e}')
            for task in tasks:
                task.cancel()
            raise e
        rlts = [elem if isinstance(elem, dict) else {} for elem in rlts]
        return pd.DataFrame(rlts, index=pd.Index(tsidx, name='timestamp'))

    def monitor(self, ts, coro, *args):
        """Create a task to monitor dataset data.

        Args:
            ts: start time in pandas.Timestamp
            coro: coroutine to handle new data

        Returns:
            The created task
        """
        freq_str = f"{self.conf['freq']}s"
        next_ts = pd.Timestamp(ts).floor(freq_str)
        delta = pd.Timedelta(freq_str)
        return asyncio.create_task(self._monitor_loop(next_ts, delta, coro, *args))

    async def _monitor_loop(self, next_ts, delta, coro, *args):
        add_delta = True
        while True:
            try:
                rlt = await self._tenant.poll_dataset_data(self.dsid, _get_utc_timestamp(next_ts))
                if rlt is None:  # 204
                    logging.debug(f'204 for {next_ts}, retried')
                    await asyncio.sleep(3)
                    add_delta = False
                    continue
                await coro(next_ts, *args)
                add_delta = True
            except Exception as e:
                logging.exception(e)
            finally:
                if add_delta:
                    next_ts += delta


class Controller:
    def __init__(self, cid, tenant):
        self.cid = cid
        self._tenant = tenant

    def desc_resource(self, rlt):
        tmp_dict = {}
        for i in rlt:
            item = i.copy()
            item.pop('tenant', None)
            item.pop('rawConfig', None)
            item.pop('devices', None)
            tmp_dict[item["_id"]] = item
            # item.pop('_id', group.None)
        return pd.DataFrame.from_dict(tmp_dict, orient='index')

    def desc_resource_group(self, rlt):
        lst = []
        for i in rlt:
            for m in i["member"]:
                lst.append([i["_id"], i["name"], m])
            # item.pop('_id', None)
        return pd.DataFrame(lst, columns=['_id', 'name', 'resource'])

    async def list_interface(self):
        """List all interface of controller

        Returns:
            pandas.DataFrane: interface indexed by tag
        """
        req = f'tenant.{self._tenant.tenant_id}.intern.atmC.{self.cid}.sync.interface'
        rlt = await self._tenant.get_mgr_config(req)
        return self.desc_resource(rlt)

    async def list_home(self):
        """List all home of controller

        Returns:
            pandas.DataFrane: home indexed by tag
        """
        req = f'tenant.{self._tenant.tenant_id}.intern.atmC.{self.cid}.sync.home'
        rlt = await self._tenant.get_mgr_config(req)
        return self.desc_resource(rlt)

    async def list_router(self):
        """List all router of controller

        Returns:
            pandas.DataFrane: router indexed by tag
        """
        req = f'tenant.{self._tenant.tenant_id}.intern.atmC.{self.cid}.sync.router'
        rlt = await self._tenant.get_mgr_config(req)
        return self.desc_resource(rlt)

    async def list_boundary(self):
        """List all boundary of controller

        Returns:
            pandas.DataFrane: boundary indexed by tag
        """
        req = f'tenant.{self._tenant.tenant_id}.intern.atmC.{self.cid}.sync.boundary'
        rlt = await self._tenant.get_mgr_config(req)
        return self.desc_resource(rlt)

    async def list_neighbor(self):
        """List all neighbor of controller

        Returns:
            pandas.DataFrane: neighbor indexed by tag
        """
        req = f'tenant.{self._tenant.tenant_id}.intern.atmC.{self.cid}.sync.neighbor'
        rlt = await self._tenant.get_mgr_config(req)
        return self.desc_resource(rlt)

    async def list_subnetwork(self):
        """List all subnetwork of controller

        Returns:
            pandas.DataFrane: subnetwork indexed by tag
        """
        req = f'tenant.{self._tenant.tenant_id}.intern.atmC.{self.cid}.sync.subnetwork'
        rlt = await self._tenant.get_mgr_config(req)
        return self.desc_resource(rlt)

    async def list_serverfarm(self):
        """List all serverfarm of controller

        Returns:
            pandas.DataFrane: serverfarm indexed by tag
        """
        req = f'tenant.{self._tenant.tenant_id}.intern.atmC.{self.cid}.sync.serverfarm'
        rlt = await self._tenant.get_mgr_config(req)
        return self.desc_resource(rlt)

    async def list_vpn(self):
        """List all vpn of controller

        Returns:
            pandas.DataFrane: vpn indexed by tag
        """
        req = f'tenant.{self._tenant.tenant_id}.intern.atmC.{self.cid}.sync.vpnCustomer'
        rlt = await self._tenant.get_mgr_config(req)
        return self.desc_resource(rlt)

    async def list_pop(self):
        """List all pop of controller

        Returns:
            pandas.DataFrane: pop indexed by tag
        """
        req = f'tenant.{self._tenant.tenant_id}.intern.atmC.{self.cid}.sync.pop'
        rlt = await self._tenant.get_mgr_config(req)
        return self.desc_resource(rlt)

    async def list_interface_group(self):
        """List all interface_group of controller

        Returns:
            pandas.DataFrane: interface groups indexed by group ID
        """
        req = f'tenant.{self._tenant.tenant_id}.intern.atmC.{self.cid}.sync.group.interface'
        rlt = await self._tenant.get_mgr_config(req)
        return self.desc_resource_group(rlt)

    async def list_router_group(self):
        """List all router_group of controller

        Returns:
            pandas.DataFrane: router groups indexed by group ID
        """
        req = f'tenant.{self._tenant.tenant_id}.intern.atmC.{self.cid}.sync.group.router'
        rlt = await self._tenant.get_mgr_config(req)
        return self.desc_resource_group(rlt)

    async def list_boundary_group(self):
        """List all boundary_group of controller

        Returns:
            pandas.DataFrane: boundary groups indexed by group ID
        """
        req = f'tenant.{self._tenant.tenant_id}.intern.atmC.{self.cid}.sync.group.boundary'
        rlt = await self._tenant.get_mgr_config(req)
        return self.desc_resource_group(rlt)

    async def list_neighbor_group(self):
        """List all neighbor_group of controller

        Returns:
            pandas.DataFrane: neighbor groups indexed by group ID
        """
        req = f'tenant.{self._tenant.tenant_id}.intern.atmC.{self.cid}.sync.group.neighbor'
        rlt = await self._tenant.get_mgr_config(req)
        return self.desc_resource_group(rlt)

    async def list_subnetwork_group(self):
        """List all subnetwork_group of controller

        Returns:
            pandas.DataFrane: subnetwork groups indexed by group ID
        """
        req = f'tenant.{self._tenant.tenant_id}.intern.atmC.{self.cid}.sync.group.subnetwork'
        rlt = await self._tenant.get_mgr_config(req)
        return self.desc_resource_group(rlt)

    async def list_serverfarm_group(self):
        """List all serverfarm_group of controller

        Returns:
            pandas.DataFrane: serverfarm groups indexed by group ID
        """
        req = f'tenant.{self._tenant.tenant_id}.intern.atmC.{self.cid}.sync.group.serverfarm'
        rlt = await self._tenant.get_mgr_config(req)
        return self.desc_resource_group(rlt)

    async def list_vpn_group(self):
        """List all vpn_group of controller

        Returns:
            pandas.DataFrane: vpn groups indexed by group ID
        """
        req = f'tenant.{self._tenant.tenant_id}.intern.atmC.{self.cid}.sync.group.vpnCustomer'
        rlt = await self._tenant.get_mgr_config(req)
        return self.desc_resource_group(rlt)

    async def list_pop_group(self):
        """List all pop_group of controller

        Returns:
            pandas.DataFrane: pop groups indexed by group ID
        """
        req = f'tenant.{self._tenant.tenant_id}.intern.atmC.{self.cid}.sync.group.pop'
        rlt = await self._tenant.get_mgr_config(req)
        return self.desc_resource_group(rlt)


class Repository:
    def __init__(self, url, user=None, tenant=None, password=None, ssl=True, burst=1,
            retry=0, conn_timeout=30, read_timeout=300, strategy='custom', controller=None):
        """Construct repository object to send tenant requests to API server

        Args:
            url: The base URL of API server.
            user: The user name.
            tenant: The tenant name.
            password: The user password.
            ssl: Set False to relax certification checks for self signed API server. Defaults to True.
            burst: Maximum concurrent requests to the API server.
            retry: Number of retry at fail of sending request.
        """
        self._tenant = Tenant(url, user, tenant, password, ssl=ssl, burst=burst, retry=retry,
            conn_timeout=conn_timeout, read_timeout=read_timeout, strategy=strategy, controller=controller)

    async def close(self):
        """Close the underlying connections gracefully. If the event loop is stopped before
        the repository is closed, a warning is emitted.
        """
        await self._tenant.close()
        await asyncio.sleep(0.250)

    async def list_controller(self):
        """List all controllers

        Returns:
            pandas.DataFrame: Dataset configurations indexed by id.
        """
        now = datetime.datetime.now().timestamp()
        req_path = f'tenant.{self._tenant.tenant_id}.intern.atmC?ts={now}'
        controller_list = await self._tenant.get_mgr_config(req_path)
        controller_dict = {}
        for controller in controller_list:
            item = controller.copy()
            item.pop('sync', None)
            item['version'] = item['setting']['version']
            item['host'] = item['setting']['rest']['host']
            item.pop('setting', None)
            item.pop('keepUnsync', None)
            controller_dict[item['_id']] = item
            item.pop('_id', None)
        return pd.DataFrame.from_dict(controller_dict, orient='index')

    async def controller(self, cid):
        """List all controllers
        Args:
            cid: the controller ID

        Returns:
            Controller object with the specified id.
        """
        return await Controller(cid, self._tenant)

    async def list(self):
        """List all datasets

        Returns:
            pandas.DataFrame: Dataset configurations indexed by id.
        """
        dset_list = await self._tenant.get_all_datasets()
        return desc_dataframe(dset_list)

    async def dataset(self, dsid):
        """Get dataset

        Returns:
            dset: Dataset object with the specified id.
        """
        desc = await self._tenant.get_dataset(dsid)
        return Dataset(self._tenant, dsid, desc['config'])

    async def adhoc(self, freq, pipeline):
        """Create an Adhoc Object.

        Args:
            freq: the aggregate frequency in seconds between 60 to 3600.
            pipeline: the pipeline

        Returns:
            Adhoc: The Adhoc object
        """
        return await Adhoc._create(self._tenant, freq, pipeline)

    async def reader(self, pipeline):
        """Execute an Record operation.

        Args:
            pipeline: the pipeline descriptor
        Returns:
            The record data frame.
        """
        return Reader(self._tenant, pipeline)

    async def authenticate(self):
        """Execute authentication.

        """
        await self._tenant._authenticate()
