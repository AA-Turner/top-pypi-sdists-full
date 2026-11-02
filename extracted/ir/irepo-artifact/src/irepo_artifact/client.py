"""Standalone artifact orchestration shared by SDK consumers."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from copy import deepcopy
import time

from .api import APAPI, _APStatus, validate_id
from .download import download_archive, download_with_refresh
from .errors import (ArtifactError, ArtifactNotFound, ConfigurationError,
                     DownloadError, HTTPStatusError, NoMatchingFiles)
from .layout import JobOutput, select_files, selectors
from .models import DownloadResult
from .probe import DownloadProbe


def _options(include_files, exclude_files, extract, overwrite):
    includes, excludes = selectors(include_files), selectors(exclude_files)
    if not isinstance(extract, bool) or not isinstance(overwrite, bool):
        raise ConfigurationError('extract and overwrite must be bool')
    if extract and (includes or excludes):
        raise ConfigurationError('file filtering cannot be combined with extract=True')
    return includes, excludes


def _workers(value):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ConfigurationError('max_concurrent must be a positive integer')


def _deadline(targets):
    expiries = [t.expires_in for t in targets.values() if t.expires_in is not None]
    if not expiries:
        return float('inf')
    expiry = min(expiries)
    return time.monotonic() + max(0, expiry - min(30, max(1, expiry * 0.1)))


def _archive_targets(api, job_ids, mode, metadata, *, tolerate_errors=False):
    try:
        targets = api.get_archive_targets(
            job_ids, mode=mode, metadata=metadata, tolerate_errors=tolerate_errors)
        return targets, mode
    except _APStatus as exc:
        if mode != 'oss' or exc.status not in (502, 503) or len(job_ids) > 1:
            raise
    targets = api.get_archive_targets(
        job_ids, mode='proxy', metadata=metadata, tolerate_errors=tolerate_errors)
    return targets, 'proxy'


class ArtifactClient:
    """Download AP artifacts without a parent SDK or storage client.

    Single-job output_dir is the Job directory. Batch/Group add jobs/<job_id>.
    Authorization is performed by the AP artifact endpoints.
    timeout limits socket operations; manifest_wait_timeout separately bounds
    each Job's manifest requests, polling and retries (not file transfers).
    """
    def __init__(self, *, ap_endpoint: str, api_key: str | None = None,
                 cluster: str = '', timeout: float = 30, headers: dict[str, str] | None = None,
                 api_prefix: str = '/api', layout: str = 'sdk', verbose: bool = False,
                 manifest_wait_timeout: float = 1800):
        if not isinstance(verbose, bool):
            raise ConfigurationError('verbose must be bool')
        if layout not in ('sdk', 'ap_export'):
            raise ConfigurationError('layout must be sdk or ap_export')
        self._layout = layout
        self._api = APAPI(ap_endpoint, api_key, cluster, timeout, headers=headers, api_prefix=api_prefix,
                          verbose=verbose, manifest_wait_timeout=manifest_wait_timeout)
        self._timeout = timeout

    def download(self, job_id: str, output_dir: str = '.', *,
                 include_files: list[str] | None = None,
                 exclude_files: list[str] | None = None,
                 extract: bool = False, overwrite: bool = False) -> DownloadResult:
        validate_id(job_id)
        includes, excludes = _options(include_files, exclude_files, extract, overwrite)
        return self._download(job_id, Path(output_dir), includes, excludes, extract, overwrite,
                              probe=DownloadProbe(self._timeout))

    @staticmethod
    def _attach(error, metadata):
        error.artifacts_response = deepcopy(metadata.get('artifacts_response'))
        error.manifest_response = deepcopy(metadata.get('manifest_response'))
        return error

    def _download(self, job_id, job_dir, includes, excludes, extract, overwrite,
                  targets=None, artifact_response=None, probe=None, link_mode='oss'):
        metadata = {'artifacts_response': deepcopy(artifact_response), 'manifest_response': None}
        output = None
        try:
            if isinstance(targets, ArtifactError):
                raise targets
            selected = None
            if includes or excludes:
                manifest = self._api.get_manifest(job_id, metadata=metadata)
                selected = select_files(manifest, includes, excludes, ap_export=self._layout == 'ap_export')
                if not selected and self._layout != 'ap_export':
                    raise NoMatchingFiles('no matching artifact files')
            elif targets is None:
                raw = {}
                try:
                    signed, link_mode = _archive_targets(self._api, [job_id], link_mode, raw)
                    targets = signed[job_id]
                finally:
                    metadata['artifacts_response'] = raw.get(job_id)
            output = JobOutput(job_dir, overwrite,
                               private_selected=selected is not None and self._layout == 'ap_export')
            if selected is not None:
                self._selected(job_id, selected, output.files_temp)
                relative_files = tuple(sorted(Path(logical) for _, logical in selected))
                mode, channel = 'selected', 'proxy'
            else:
                if 'proxy' in targets and 'oss' not in targets:
                    link_mode = 'proxy'
                refreshed_metadata = {}
                def refresh(channel):
                    raw = {}
                    try:
                        mode = channel if channel in ('oss', 'proxy') else link_mode
                        renewed = self._api.get_archive_targets([job_id], mode=mode, metadata=raw)[job_id]
                    except ArtifactError as exc:
                        # A failed refresh must not replace the last usable response.
                        raise self._attach(exc, metadata) from None
                    refreshed_metadata['artifacts_response'] = raw[job_id]
                    return renewed
                def proxy_targets():
                    nonlocal link_mode
                    raw = {}
                    renewed = self._api.get_archive_targets([job_id], mode='proxy', metadata=raw)[job_id]
                    link_mode = 'proxy'
                    metadata['artifacts_response'] = raw[job_id]
                    return renewed
                channel = download_archive(
                    targets, output.archive_temp, refresh, self._timeout,
                    on_refreshed=lambda: metadata.update(refreshed_metadata),
                    probe=probe.reachable if probe is not None else None,
                    get_proxy_targets=(proxy_targets if 'oss' in targets and
                                       isinstance(metadata['artifacts_response'], dict) and
                                       metadata['artifacts_response'].get('downloads') else None))
                mode = 'expanded' if extract else 'archive'
                relative_files = output.extract_archive() if extract else ()
            output.commit(mode)
            archive_path = output.job_dir / 'result.tgz' if mode != 'selected' else None
            files_dir = output.job_dir / 'artifacts/output' if mode != 'archive' else None
            files = tuple(files_dir / path for path in relative_files) if files_dir else ()
            return DownloadResult(job_id, output.job_dir, archive_path, files_dir, files, channel,
                                  'success', **metadata)
        except HTTPStatusError as exc:
            if exc.status == 404:
                raise self._attach(ArtifactNotFound('artifact content not found'), metadata) from None
            raise self._attach(exc, metadata) from None
        except ArtifactError as exc:
            raise self._attach(exc, metadata) from None
        except OSError:
            raise self._attach(DownloadError('cannot write artifact files'), metadata) from None
        finally:
            if output is not None:
                output.cleanup()

    def _selected(self, job_id, selected, directory):
        for start in range(0, len(selected), 500):
            batch = selected[start:start + 500]
            paths = [path for path, _ in batch]
            targets = self._api.get_file_targets(job_id, paths)
            refresh_at = _deadline(targets)
            issued_at_index = 0
            for index, (path, logical) in enumerate(batch):
                # Never immediately re-sign before the first file of a fresh batch.
                if index > issued_at_index and time.monotonic() >= refresh_at:
                    targets = self._api.get_file_targets(job_id, paths[index:])
                    refresh_at = _deadline(targets)
                    issued_at_index = index
                dest = directory / logical
                dest.parent.mkdir(parents=True, exist_ok=True)
                def refresh():
                    nonlocal targets, refresh_at, issued_at_index
                    targets = self._api.get_file_targets(job_id, paths[index:])
                    refresh_at = _deadline(targets)
                    issued_at_index = index
                    return targets[path]
                download_with_refresh(targets[path], dest, refresh, self._timeout)

    @staticmethod
    def _failure(job_id, directory, error):
        status = ('missing' if isinstance(error, ArtifactNotFound) else
                  'no_match' if isinstance(error, NoMatchingFiles) else 'failed')
        return DownloadResult(job_id, directory.absolute(), None, None, (), None, status, error,
                              deepcopy(error.artifacts_response), deepcopy(error.manifest_response))

    def download_many(self, job_ids: list[str], output_dir: str = '.', *,
                      max_concurrent: int = 8, include_files: list[str] | None = None,
                      exclude_files: list[str] | None = None, extract: bool = False,
                      overwrite: bool = False) -> dict[str, DownloadResult]:
        _workers(max_concurrent)
        includes, excludes = _options(include_files, exclude_files, extract, overwrite)
        if not isinstance(job_ids, (list, tuple)):
            raise ConfigurationError('job_ids must be a list')
        ids = list(dict.fromkeys(validate_id(j) for j in job_ids))
        results = {}
        root = Path(output_dir) / 'jobs'
        width = min(max_concurrent, 5000)
        probe = DownloadProbe(self._timeout)
        prefetched, prefetched_raw = {}, {}
        link_mode = 'oss'
        if ids and not (includes or excludes):
            jid = ids[0]
            raw = {}
            try:
                signed_targets, _ = _archive_targets(
                    self._api, [jid], 'oss', raw, tolerate_errors=True)
                signed = signed_targets[jid]
            except ArtifactError as exc:
                signed = exc.clone()
                signed.artifacts_response = deepcopy(raw.get(jid))
            prefetched[jid] = signed
            prefetched_raw[jid] = raw.get(jid)
            if (isinstance(signed, dict) and 'oss' in signed and
                    isinstance(raw.get(jid), dict) and raw[jid].get('downloads')):
                link_mode = 'oss' if probe.reachable(signed['oss'].url) else 'proxy'
                if link_mode == 'proxy':
                    del prefetched[jid]  # Reissue with the chosen channel.
                    del prefetched_raw[jid]
        with ThreadPoolExecutor(max_workers=min(width, len(ids) or 1)) as pool:
            for start in range(0, len(ids), width):
                ready = ids[start:start + width]
                targets = {jid: prefetched[jid] for jid in ready if jid in prefetched}
                raw = {jid: prefetched_raw[jid] for jid in ready if jid in prefetched_raw}
                if not (includes or excludes):
                    to_sign = [jid for jid in ready if jid not in prefetched]
                    try:
                        signed_targets, _ = _archive_targets(
                            self._api, to_sign, link_mode, raw, tolerate_errors=True)
                        targets.update(signed_targets)
                    except ArtifactError as exc:
                        if len(to_sign) > 1 and (
                                getattr(exc, '_request_status', None) in (403, 404) or
                                isinstance(exc, _APStatus) and link_mode == 'oss' and
                                exc.status in (502, 503)):
                            # No links were issued. Let the existing workers
                            # sign each Job independently before downloading.
                            pass
                        else:
                            for jid in to_sign:
                                error = exc.clone()
                                error.artifacts_response = deepcopy(raw.get(jid))
                                results[jid] = self._failure(jid, root / jid, error)
                    if probe.result is None:
                        sample = next((value['oss'].url for jid, value in targets.items()
                                       if isinstance(value, dict) and 'oss' in value and
                                       isinstance(raw.get(jid), dict) and raw[jid].get('downloads')), None)
                        if sample is not None:
                            link_mode = 'oss' if probe.reachable(sample) else 'proxy'
                            if link_mode == 'proxy':
                                reissue = [jid for jid in ready if isinstance(targets.get(jid), dict)
                                           and 'oss' in targets[jid]]
                                try:
                                    targets.update(self._api.get_archive_targets(
                                        reissue, mode='proxy', metadata=raw, tolerate_errors=True))
                                except ArtifactError as exc:
                                    for jid in reissue:
                                        error = exc.clone()
                                        error.artifacts_response = deepcopy(raw.get(jid))
                                        results[jid] = self._failure(jid, root / jid, error)
                    ready = [jid for jid in ready if jid not in results]
                futures = {jid: pool.submit(self._download, jid, root / jid, includes, excludes,
                                             extract, overwrite, targets.get(jid), raw.get(jid), probe,
                                             link_mode) for jid in ready}
                for jid, future in futures.items():
                    try:
                        results[jid] = future.result()
                    except ArtifactError as exc:
                        results[jid] = self._failure(jid, root / jid, exc)
        return {jid: results[jid] for jid in ids}

    def download_group(self, group_id: str, output_dir: str = '.', *,
                       max_concurrent: int = 8, include_files: list[str] | None = None,
                       exclude_files: list[str] | None = None, extract: bool = False,
                       overwrite: bool = False) -> dict[str, DownloadResult]:
        validate_id(group_id)
        _workers(max_concurrent)
        _options(include_files, exclude_files, extract, overwrite)
        return self.download_many(
            self._api.list_group_job_ids(group_id), output_dir, max_concurrent=max_concurrent,
            include_files=include_files, exclude_files=exclude_files, extract=extract, overwrite=overwrite)
