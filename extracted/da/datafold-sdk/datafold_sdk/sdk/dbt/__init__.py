import logging
import sys
from os import path, walk
import tempfile
import zipfile
import time
from typing import List, Optional, Tuple

import pydantic

from datafold_sdk.sdk.ci import list_runs
from datafold_sdk.sdk.exceptions import DatafoldSDKException
from datafold_sdk.sdk.utils import check_commit_sha, prepare_api_url, prepare_headers, post_data

from datafold_sdk import sdk_log

logger = logging.getLogger(__file__)
logger.addHandler(sdk_log.SDKLogHandler())


def submit_artifacts(
    host: str,
    api_key: str,
    ci_config_id: int,
    run_type: str,
    target_folder: str,
    commit_sha: Optional[str] = None,
    run_id: Optional[str] = None,
) -> str:
    """
    Submits dbt artifacts to the datafold app server.

    Args:
        host          (str): The location of the datafold app server.
        api_key       (str): The API_KEY to use for authentication
        ci_config_id  (int): The ID of the CI config for which you submit these artifacts
                             (See the CI config ID in the CI settings screen).
        run_type      (str): The run_type to apply. Can be either "pull_request" or "production"
        target_folder (str): The location of the `target` folder after the `dbt run`, which includes
                             files this utility will zip and include in the upload
        commit_sha    (str): Optional. If not provided, the SDK will resolve this through a git command
                             otherwise used as is.
        run_id        (str): Not used for normal mode, required for low-drift mode. This is
                             a unique string identifier that links PR manifest and base manifest.
                             For each PR build you'll need to build a branch of production.
    Returns:
        commit_sha    (str): The commit sha that just has been submitted
    """

    api_segment = f"api/v1/dbt/submit_artifacts/{ci_config_id}"
    url = prepare_api_url(host, api_segment)
    headers = prepare_headers(api_key)

    if not commit_sha:
        commit_sha = check_commit_sha(target_folder)

    if not commit_sha:
        logger.error("No commit sha resolved. Override the commit_sha with the --commit-sha parameter")
        raise DatafoldSDKException("No commit sha resolved")

    target_folder = path.abspath(target_folder)
    with tempfile.NamedTemporaryFile(suffix=".zip", mode='w+b', delete=True) as tmp_file:
        with zipfile.ZipFile(
            tmp_file.name,
            mode='w',
            compression=zipfile.ZIP_DEFLATED,
        ) as zip_file:
            seen_manifest = False
            for folder_name, _, file_names in walk(target_folder):
                rel_path = path.relpath(folder_name, target_folder)
                for file_name in file_names:
                    if file_name == "manifest.json":
                        seen_manifest = True

                    file_path = path.join(folder_name, file_name)
                    zip_path = path.join(rel_path, path.basename(file_path))
                    zip_file.write(file_path, zip_path)

        if not seen_manifest:
            logger.error("The manifest.json is missing in the target directory.")
            raise DatafoldSDKException("The manifest.json is missing in the target directory.")

        with open(tmp_file.name, 'rb') as f:
            files = {'artifacts': f}
            data = {'commit_sha': commit_sha, 'run_type': run_type, 'run_id': run_id}
            post_data(url, files=files, data=data, headers=headers)

    logger.info("Successfully uploaded the manifest")
    return commit_sha


def check_artifacts(
    host: str,
    api_key: str,
    ci_config_id: int,
    run_type: str,
    branch: str,
    commit_sha: str
):
    """This function check if dbt artifacts were successfully uploaded."""

    api_segment = f'api/v1/dbt/post_upload_check_artifacts/{ci_config_id}'
    url = prepare_api_url(host, api_segment)
    headers = prepare_headers(api_key)

    data = {
        'commit_sha': commit_sha,
        'run_type': run_type,
        'branch': branch,
    }
    logger.info(f'Checking dbt artifacts for ci config={ci_config_id}, branch={branch}, commit sha={commit_sha}, '
                f'run type={run_type}')
    res = post_data(url, data=data, headers=headers)
    data = res.json()
    if data['status'] == 'ok':
        logger.info('Dbt artifacts exist')
    else:
        logger.error('Cannot find dbt artifacts')


def wait_for_completion(
        host: str,
        api_key: str,
        ci_config_id: int,
        commit_sha: str,
        wait_in_minutes: int = 60):
    """
    Blocks until Datafold is done running the diff
    """

    start = time.monotonic()
    while 1:
        runs = list_runs(
            host,
            api_key,
            ci_config_id,
            pr_sha=commit_sha,
            limit=1,
        )
        seconds_elapsed = time.monotonic() - start
        if runs:
            run = runs[0]
            logger.info(f'Run #{run.id}, PR {run.pr_num}: {run.status}, {seconds_elapsed:.0f}s')

            if run.status == 'done':
                break

            if run.status == 'cancelled':
                logger.warning("The CI job has been cancelled, probably an old commit hash")
                sys.exit(1)

            if run.status == 'failed':
                logger.error("The CI job failed")
                sys.exit(1)
        else:
            logger.info(f'Waiting for CI run to start, {seconds_elapsed:.0f}s')

        if not runs and seconds_elapsed > 60:
            raise TimeoutError("Timed out waiting for the Data Diff to start")

        if seconds_elapsed > 60 * wait_in_minutes:
            raise TimeoutError("Timed out waiting for the Data Diff to complete")

        time.sleep(5)


class DbtPkInfo(pydantic.BaseModel):
    source: str
    sql_table: Tuple[str, ...]
    sql_pks: List[str]
    dbt_fqn: Tuple[str, ...]
    dbt_pks: List[str]
    dbt_original_file_path: str
    dbt_patch_path: Optional[str]
    warnings: List[str]


def check_pks_in_manifest(
        host: str, api_key: str, ci_config_id: int, manifest: bytes
) -> List[DbtPkInfo]:
    api_segment = f"api/internal/ci/{ci_config_id}/check_pks_in_dbt_manifest"
    url = prepare_api_url(host, api_segment)
    headers = prepare_headers(api_key)
    result = post_data(url, data=manifest, headers=headers).json()
    return [DbtPkInfo(**x) for x in result]
