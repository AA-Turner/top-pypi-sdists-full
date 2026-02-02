import logging
from typing import Optional, List

import pydantic

from datafold_sdk.sdk.exceptions import DatafoldSDKException
from datafold_sdk.sdk.utils import (
    check_commit_sha,
    prepare_api_url,
    prepare_headers,
    get_data,
    post_data
)

from datafold_sdk import sdk_log

logger = logging.getLogger(__file__)
logger.addHandler(sdk_log.SDKLogHandler())


class CiRunListOptions(pydantic.BaseModel):
    limit: int = 100
    offset: int = 0
    pr_sha: Optional[str]
    pr_num: Optional[str]


class CiRun(pydantic.BaseModel):
    id: int
    base_branch: str
    base_sha: str
    pr_branch: str
    pr_sha: str
    pr_num: str
    status: str


def list_runs(
        host: str,
        api_key: str,
        ci_config_id: int,
        pr_sha: Optional[str] = None,
        pr_num: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None) -> List[CiRun]:
    """
    List runs for specified CI config.

    Args:
        host          (str): The location of the datafold app server.
        api_key       (str): The API_KEY to use for authentication
        ci_config_id  (int): The ID of the CI config for which you submit these artifacts
                             (See the CI config ID in the CI settings screen).
        pr_sha        (str): Optionally filter by PR sha.
        pr_num        (int): Optionally filter by PR number.
        limit         (int): Optionally limit number of results (1..1000).
        offset        (int): Optionally list results starting from this index.
    Returns:
        None
    """

    api_segment = f"api/v1/ci/{ci_config_id}/runs"
    url = prepare_api_url(host, api_segment)
    headers = prepare_headers(api_key)
    params = {
        'limit': limit,
        'offset': offset,
        'pr_sha': pr_sha,
        'pr_num': pr_num,
    }
    params = {k: str(v) for k, v in params.items() if v is not None}

    results = get_data(url, params=params, headers=headers).json()
    return [CiRun(**record) for record in results]


class CiDiff(pydantic.BaseModel):
    prod: str
    pr: str
    pk: Optional[List[str]]
    include_columns: List[str] = []
    exclude_columns: List[str] = []


class CiTrigger(pydantic.BaseModel):
    pr_number: int
    base_branch: str
    base_sha: str
    pr_sha: str
    pr_branch: str


def run_diff(
        host: str,
        api_key: str,
        ci_config_id: int,
        pr_num: int,
        diffs: List[CiDiff]) -> Optional[int]:
    """
    Triggers a run from a Pull Request

    Args:
        host          (str): The location of the Datafold app server.
        api_key       (str): The API_KEY to use for authentication
        ci_config_id  (int): The ID of the CI config for which you submit these artifacts
                             (See the CI config ID in the CI settings screen).
        pr_num        (int): Optionally filter by PR number.
        diffs         (CiDiff): The tables that you want to have diffed
    Returns:
        None
    """
    api_segment = f"api/v1/ci/{ci_config_id}/{pr_num}"
    url = prepare_api_url(host, api_segment)
    headers = prepare_headers(api_key)
    payload = [d.model_dump() for d in diffs]
    response = post_data(url, json_data=payload, headers=headers).json()
    return response['run_id']


def trigger_ci_run(host: str,
                   api_key: str,
                   ci_config_id: int,
                   pr_num: int,
                   pr_sha: Optional[str] = None,
                   pr_branch: Optional[str] = None,
                   base_sha: Optional[str] = None,
                   base_branch: Optional[str] = None) -> int:
    """
    Attempts to trigger a CI run on the datafold server

    Args:
        host          (str): The location of the datafold app server.
        api_key       (str): The API_KEY to use for authentication
        ci_config_id  (int): The ID of the CI config for which you submit these artifacts
                             (See the CI config ID in the CI settings screen).
        pr_num        (int): The PR number of the pull or merge request.
        pr_sha        (str): Optional. If not provided, the SDK will resolve this through a git command
                             otherwise used as is.
        pr_branch     (str): Optional. If not provided, the SDK will resolve this through a git command
                             otherwise used as is.
        base_sha      (str): Optional. If not provided, the SDK will resolve this through a git command
                             otherwise used as is.
        base_branch   (str): Optional. If not provided, the SDK will resolve this through a git command
                             otherwise used as is.
    Returns:
        ci_run_id     (int): The ID of the CI run that was created.
    """

    api_segment = f"api/v1/ci/{ci_config_id}/trigger"
    url = prepare_api_url(host, api_segment)
    headers = prepare_headers(api_key)

    if not pr_sha:
        pr_sha = check_commit_sha(cwd="./")

    if not pr_sha:
        logger.error("No pr sha resolved. Override the pr_sha with the --pr-sha param")
        raise DatafoldSDKException("No pr sha resolved")

    trigger_info = CiTrigger(
        ci_config_id=ci_config_id,
        pr_number=pr_num,
        base_sha=base_sha,
        base_branch=base_branch,
        pr_branch=pr_branch,
        pr_sha=pr_sha,
    )
    res = post_data(url, json_data=trigger_info.model_dump(), headers=headers)
    rv = res.json()
    ci_run_id = rv['ci_run_id']
    logger.info(f"Successfully triggered the CI run: {ci_run_id}")
    return ci_run_id
