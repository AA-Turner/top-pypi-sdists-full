"""AP control-plane protocol. This module never downloads artifact bytes."""
from __future__ import annotations

import http.client
import json
import math
from copy import deepcopy
import re
import urllib.error
import urllib.parse
import urllib.request

from .errors import (AccessDenied, ArtifactNotFound, ConfigurationError,
                     ArtifactError, DownloadError, ProtocolError)
from .models import DownloadTarget
from .diagnostics import Diagnostics
from .manifest_wait import ManifestBudget, budget_handlers, retry_delay, http_retry_delay


def validate_id(value: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,127}', value):
        raise ConfigurationError('invalid job or group ID')
    return value


def validate_url(value: str) -> str:
    try:
        parsed = urllib.parse.urlsplit(value)
        valid = (isinstance(value, str) and parsed.scheme in ('http', 'https')
                 and parsed.hostname and not parsed.username and not parsed.password
                 and not parsed.fragment and not any(c.isspace() for c in value))
        parsed.port
    except (ValueError, TypeError, AttributeError):
        valid = False
    if not valid:
        raise ProtocolError('invalid HTTP URL')
    return value


# Only standard regional endpoints: neither custom domains nor acceleration.
_OSS_HOST = re.compile(
    r'(?P<bucket>[a-z0-9][a-z0-9-]*\.)?oss-'
    r'(?P<region>(?:cn|us|ap|eu|me|na|sa|af)-[a-z0-9]+(?:-[a-z0-9]+)*?)'
    r'(?P<internal>-internal)?\.aliyuncs\.com', re.IGNORECASE)


def is_standard_oss_url(url: str) -> bool:
    return _OSS_HOST.fullmatch(urllib.parse.urlsplit(url).hostname.rstrip('.')) is not None


def internal_download_url(url: str) -> str:
    validate_url(url)
    parsed = urllib.parse.urlsplit(url)
    match = _OSS_HOST.fullmatch(parsed.hostname.rstrip('.'))
    if match is None or match['internal']:
        return url
    host = (match['bucket'] or '') + 'oss-' + match['region'] + '-internal.aliyuncs.com'
    if parsed.hostname.endswith('.'):
        host += '.'
    authority = host + parsed.netloc[len(parsed.hostname):]
    # Preserve the signed path/query byte-for-byte, including escaping and order.
    start = url.index('//') + 2
    return url[:start] + authority + url[start + len(parsed.netloc):]


def target(data: dict, expires_in=None) -> DownloadTarget:
    if not isinstance(data, dict):
        raise ProtocolError('invalid download target')
    url = validate_url(data.get('url'))
    expiry = data.get('expires_in', expires_in)
    if expiry is not None and (isinstance(expiry, bool) or not isinstance(expiry, (int, float))
                               or not math.isfinite(expiry) or expiry <= 0):
        raise ProtocolError('invalid download expiry')
    return DownloadTarget(url, expiry)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class _APStatus(ProtocolError):
    def __init__(self, status, response=None, headers=None):
        self.status = status
        self.response = response
        self.headers = headers or {}
        super().__init__(f'AP returned HTTP {status}')


class APAPI:
    def __init__(self, ap_endpoint: str, api_key: str | None, cluster: str, timeout: float = 30, *, headers=None, api_prefix="/api", verbose=False, manifest_wait_timeout=1800):
        try:
            validate_url(ap_endpoint)
        except ProtocolError:
            raise ConfigurationError('AP endpoint must be an HTTP root URL') from None
        if urllib.parse.urlsplit(ap_endpoint).query:
            raise ConfigurationError('AP endpoint must not contain a query')
        if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or timeout <= 0:
            raise ConfigurationError('timeout must be positive')
        self._diagnostics = Diagnostics(verbose)
        self.endpoint = ap_endpoint.rstrip('/')
        self.timeout = timeout
        if (isinstance(manifest_wait_timeout, bool) or not isinstance(manifest_wait_timeout, (int, float))
                or not math.isfinite(manifest_wait_timeout) or manifest_wait_timeout <= 0):
            raise ConfigurationError('manifest_wait_timeout must be a finite positive number')
        self.manifest_wait_timeout = manifest_wait_timeout
        if api_prefix not in ('', '/api'):
            raise ConfigurationError('api_prefix must be /api or empty for direct routes')
        self.api_prefix = api_prefix
        if headers is not None and not isinstance(headers, dict):
            raise ConfigurationError('headers must be a mapping of strings')
        self.headers = {'accept': 'application/json'}
        for key, value in (headers or {}).items():
            if (not isinstance(key, str) or not re.fullmatch(r"[!#$%&'*+.^_`|~0-9A-Za-z-]+", key)
                    or not isinstance(value, str) or '\r' in value or '\n' in value):
                raise ConfigurationError('invalid AP request header')
            self.headers[key.lower()] = value
        for key, value in (('x-api-key', api_key), ('x-cluster', cluster)):
            if value:
                if not isinstance(value, str) or '\r' in value or '\n' in value:
                    raise ConfigurationError('invalid AP request header')
                self.headers[key] = value

    def _request(self, path, body=None, *, with_response=False, budget=None):
        headers = dict(self.headers)
        data = None
        if body is not None:
            data = json.dumps(body).encode()
            headers['content-type'] = 'application/json'
        request = urllib.request.Request(self.endpoint + self.api_prefix + path, data=data, headers=headers)
        self._diagnostics.request(path, request.full_url, body)
        timeout = self.timeout if budget is None else min(self.timeout, budget.remaining())
        handlers = () if budget is None else budget_handlers(budget, self.timeout)
        try:
            # Never forward control-plane credentials through a redirect.
            with urllib.request.build_opener(_NoRedirect(), *handlers).open(request, timeout=timeout) as response:
                payload = response.read(8 * 1024 * 1024 + 1)
                if len(payload) > 8 * 1024 * 1024:
                    raise ProtocolError('AP control response exceeds size limit')
                status, response_headers = response.status, response.headers
        except urllib.error.HTTPError as exc:
            code = exc.code
            self._diagnostics.request(path, request.full_url, body, status=code)
            error_response = None
            try:
                if with_response:
                    error_response = json.loads(exc.read(65536))
            except (ValueError, OSError, http.client.HTTPException):
                pass
            finally:
                exc.close()
            if budget is not None:
                budget.remaining()
            retry_headers = {'Retry-After': exc.headers.get('Retry-After')} if exc.headers else {}
            raise _APStatus(code, error_response, retry_headers) from None
        except (urllib.error.URLError, OSError, ValueError, http.client.HTTPException) as exc:
            self._diagnostics.request(path, request.full_url, body, error=type(exc).__name__)
            if budget is not None:
                budget.remaining()
            raise DownloadError('unable to reach AP') from None
        if budget is not None:
            budget.remaining()
        try:
            decoded = json.loads(payload)
            return (status, response_headers, decoded) if with_response else decoded
        except (ValueError, UnicodeError):
            self._diagnostics.request(path, request.full_url, body, error='ProtocolError')
            raise ProtocolError('AP returned invalid JSON') from None

    def _call(self, path, body=None):
        try:
            return self._request(path, body)
        except _APStatus as exc:
            if exc.status in (401, 403):
                error = AccessDenied(f'AP returned HTTP {exc.status}')
            elif exc.status == 404:
                error = ArtifactNotFound('AP resource not found')
            else:
                raise
            # Keep request status internally: a batch 403/404 can concern only
            # one Job, whereas a 401 must not trigger per-Job signing retries.
            error._request_status = exc.status
            raise error from None

    def list_group_job_ids(self, group_id):
        validate_id(group_id)
        result, seen = [], set()
        skip = 0
        for _ in range(1000):
            data = self._call(f'/groups/{group_id}/jobs?skip={skip}&limit=500&include_post_process=false')
            if not isinstance(data, dict) or not isinstance(data.get('jobs'), list):
                raise ProtocolError('invalid Group jobs response')
            jobs = data['jobs']
            if len(jobs) > 500:
                raise ProtocolError('Group jobs page exceeds requested limit')
            added = 0
            for job in jobs:
                if not isinstance(job, dict) or not isinstance(job.get('job_id'), str):
                    raise ProtocolError('invalid Group job')
                jid = validate_id(job['job_id'])
                if jid not in seen:
                    seen.add(jid)
                    result.append(jid)
                    added += 1
            if len(jobs) < 500:
                return result
            if added == 0:
                raise ProtocolError('Group jobs pagination made no progress')
            skip += len(jobs)
        raise ProtocolError('Group jobs pagination budget exhausted')

    def get_archive_targets(self, job_ids, *, mode='both', metadata=None, tolerate_errors=False):
        if not job_ids:
            return {}
        if len(job_ids) > 5000:
            raise ConfigurationError('at most 5000 jobs per link request')
        for jid in job_ids:
            validate_id(jid)
        requested_ids = set(job_ids)
        if mode not in ('oss', 'proxy', 'both'):
            raise ConfigurationError('invalid archive download mode')
        rows = self._call('/jobs/artifacts', {'job_ids': job_ids, 'download_mode': mode})
        if not isinstance(rows, list):
            raise ProtocolError('invalid archive links response')
        result = {}
        # Correlate before parsing so one missing Job cannot discard other rows.
        by_id = {}
        malformed = False
        for row in rows:
            if (not isinstance(row, dict) or not isinstance(row.get('job_id'), str)
                    or row['job_id'] not in requested_ids or row['job_id'] in by_id):
                malformed = True
                continue
            by_id[row['job_id']] = row
            if metadata is not None:
                metadata[row['job_id']] = deepcopy(row)
        if malformed:
            raise ProtocolError('unexpected or duplicate archive Job')
        for jid in job_ids:
            row = by_id.get(jid)
            try:
                if row is None:
                    raise ProtocolError('archive links response is missing Jobs')
                downloads = row.get('downloads')
                if row.get('url', False) is None and not downloads:
                    raise ArtifactNotFound('artifact links not found')
                if downloads is None or downloads == {}:
                    legacy = target(row)
                    kind = 'oss' if is_standard_oss_url(legacy.url) else 'legacy'
                    result[jid] = {kind: legacy}
                    self._diagnostics.links(jid, result[jid], internal_download_url)
                    continue
                if not isinstance(downloads, dict):
                    raise ProtocolError('invalid download links')
                parsed = {}
                for kind, value in downloads.items():
                    if kind not in ('oss', 'proxy'):
                        continue  # Preserve unknown providers in raw metadata.
                    parsed[kind] = target(value)
                if not parsed:
                    raise ProtocolError('no supported download channel')
                result[jid] = parsed
                self._diagnostics.links(jid, parsed, internal_download_url)
            except ArtifactError as exc:
                exc.artifacts_response = deepcopy(row)
                if not tolerate_errors:
                    raise
                result[jid] = exc
        return result

    def get_manifest(self, job_id, *, metadata=None):
        validate_id(job_id)
        # State belongs to this Job, never to the client/cluster: mixed server
        # deployments and concurrent Jobs must not poison one another's routing.
        budget = ManifestBudget(self.manifest_wait_timeout)
        metadata = metadata if metadata is not None else {}
        path = f'/jobs/{job_id}/artifacts/manifest'
        fallback_status = None
        first_request = True
        failures = 0
        try:
            while True:
                try:
                    status, headers, data = self._request(path, with_response=True, budget=budget)
                except _APStatus as exc:
                    if isinstance(exc.response, dict):
                        metadata['manifest_response'] = deepcopy(exc.response)
                    if first_request and exc.status in (404, 405):
                        fallback_status = exc.status
                        path = f'/jobs/{job_id}/artifacts-manifest?require_file_download=true'
                        first_request = False
                        continue
                    first_request = False
                    if exc.status in (401, 403):
                        raise AccessDenied(f'AP returned HTTP {exc.status}') from None
                    if exc.status in (408, 429, 500, 502, 503, 504) and failures < 2:
                        budget.sleep(http_retry_delay(exc.headers, failures))
                        failures += 1
                        continue
                    raise
                except DownloadError:
                    first_request = False
                    if failures >= 2:
                        raise
                    budget.sleep(http_retry_delay({}, failures))
                    failures += 1
                    continue
                first_request = False
                failures = 0
                if isinstance(data, dict):
                    metadata['manifest_response'] = deepcopy(data)
                if (not isinstance(data, dict)
                        or data.get('job_id', job_id if fallback_status is not None else None) != job_id):
                    raise ProtocolError('invalid manifest response')
                if status == 202 and fallback_status is None:
                    if data.get('status') != 'preparing':
                        raise ProtocolError('invalid manifest preparation response')
                    budget.sleep(retry_delay(headers, 2))
                    continue
                if status != 200 or 'manifest' not in data or data.get('truncated'):
                    raise ProtocolError('invalid or truncated manifest')
                if data['manifest'] is None:
                    raise ArtifactNotFound('artifact manifest not found')
                if not isinstance(data['manifest'], list):
                    raise ProtocolError('invalid manifest')
                return data['manifest']
        except ArtifactError as exc:
            exc.manifest_response = deepcopy(metadata.get('manifest_response'))
            if fallback_status is not None and not isinstance(exc, ArtifactNotFound):
                exc.args = (f'manifest compatibility request failed (new HTTP {fallback_status}; '
                            f'legacy): {exc}',)
            raise

    def get_file_targets(self, job_id, paths):
        validate_id(job_id)
        if not paths or len(paths) > 500:
            raise ConfigurationError('file link request requires 1 to 500 paths')
        endpoint = f'/jobs/{job_id}/artifacts/files/download'
        try:
            data = self._request(endpoint, {'paths': paths})
        except _APStatus as exc:
            if exc.status in (401, 403):
                raise AccessDenied(f'AP returned HTTP {exc.status}') from None
            raise
        if not isinstance(data, dict) or not isinstance(data.get('files'), list):
            raise ProtocolError('invalid file links response')
        result = {}
        for row in data['files']:
            if not isinstance(row, dict) or row.get('path') not in paths or row['path'] in result:
                raise ProtocolError('unexpected or duplicate file path')
            result[row['path']] = target(row, data.get('expires_in'))
        if set(result) != set(paths):
            raise ProtocolError('file links response is incomplete')
        for path, link in result.items():
            self._diagnostics.links(job_id, {'proxy': link}, internal_download_url, file=path)
        return result
