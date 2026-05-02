"""
http工具类
"""

import random
import socket
import ssl
from collections import defaultdict
from functools import wraps
from pathlib import Path
from urllib.parse import urlparse

import requests
from joblib import Parallel, delayed
from loguru import logger
from requests.adapters import HTTPAdapter, PoolManager
from urllib3.util.ssl_ import create_urllib3_context

from .lib import log_error, mkdir, tqdm_loguru


def handle_exception(func):
    """异常处理包装类"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            logger.error(f"请求失败，状态码: {e.response.status_code}")
            return None
        except requests.exceptions.Timeout as e:
            logger.error(f"请求超时: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"发生错误: {e}")
            return None
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error(f"发生错误: {e}")
            return None

    return wrapper


def __get_headers(token: str) -> dict[str, str]:
    return {
        "Access-Token": token,
    }


@handle_exception
def get_json(url: str, session: requests.Session | None = None, proxies=None):
    """获取json"""
    response = (session or requests).get(url, proxies=proxies)
    response.raise_for_status()
    if response.status_code != 200:
        return None
    return response.json()


@handle_exception
def get_content(
    url: str,
    session: requests.Session | None = None,
    proxies: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
) -> bytes:
    """获取内容"""
    response = (session or requests).get(url, proxies=proxies, headers=headers)
    response.raise_for_status()
    return response.content


def write_content(
    url: str,
    path: Path,
    session: requests.Session | None = None,
    proxies: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
):
    """写入内容"""
    from loguru import logger

    if path.exists():
        logger.debug(f"文件已存在: {path}")
        return
    mkdir(path.parent).lash(lambda err: log_error("文件夹创建失败", err))
    while (
        content := get_content(
            url=url, session=session, proxies=proxies, headers=headers
        )
    ) is None:
        continue
    with path.open("wb") as f:
        f.write(content)


def batch_download(
    path_url: dict[Path, str],
    proxies: dict[str, str] | None = None,
    n_jobs: int = 16,
):
    """批量下载"""
    session = requests.Session()
    Parallel(n_jobs=n_jobs)(
        delayed(write_content)(
            url,
            write_path,
            session,
            proxies,
        )
        for write_path, url in tqdm_loguru(
            path_url.items(),
            desc="batch downloading...",
        )
    )


@handle_exception
def get_task_info(
    task_id: str,
    token: str,
    domain: str,
    session: requests.Session | None = None,
    headers: dict[str, str] | None = None,
):
    """请求task_info信息"""
    url = f"{domain}/api/v2/task/get/task-info"
    if not headers:
        headers = {}
    headers.update(__get_headers(token))
    params = {"taskId": task_id}
    response = (session or requests).post(url, headers=headers, json=params)
    response.raise_for_status()
    if response.status_code != 200:
        return None
    return response.json()


@handle_exception
def get_item_info(
    item_id: str,
    token: str,
    domain: str,
    session: requests.Session | None = None,
    host: str | None = None,
):
    """item 请求信息"""
    url = f"{domain}/api/v2/item/get-item-info"
    headers = __get_headers(token)
    if host:
        headers["Host"] = host
    params = {"itemId": item_id}
    response = (session or requests).post(url, headers=headers, json=params)
    response.raise_for_status()
    if response.status_code != 200:
        return None
    return response.json()


@handle_exception
def find_labels(
    task_id: str,
    item_id: str,
    token: str,
    domain: str,
    session: requests.Session | None = None,
    host: str | None = None,
):
    """请求标签信息"""
    url = f"{domain}/api/v2/label/find-labels"
    headers = __get_headers(token)
    if host:
        headers["Host"] = host
    params = {"taskId": task_id, "itemId": item_id}
    response = (session or requests).post(url, headers=headers, json=params)
    response.raise_for_status()
    if response.status_code != 200:
        return None
    return response.json()
