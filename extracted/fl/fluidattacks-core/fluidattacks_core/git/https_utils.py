import asyncio
import base64
import logging
from contextlib import suppress

import aiohttp
from urllib3.exceptions import LocationParseError
from urllib3.util import Url, parse_url

from fluidattacks_core.http.client import request
from fluidattacks_core.http.validations import HTTPValidationError

from .classes import InvalidParameter
from .utils import format_url

LOGGER = logging.getLogger(__name__)


def format_redirected_url(
    original_url: Url,
    redirect_url: Url,
) -> str:
    return (
        redirect_url._replace(
            query=None,
            path=(redirect_url.path or "").removesuffix("info/refs"),
        ).url
        if original_url.host == redirect_url.host
        else original_url.url
    )


async def get_redirected_url(
    *,
    url: str,
    user: str | None,
    password: str | None,
    token: str | None,
    is_pat: bool,
) -> str:
    try:
        uri = parse_url(url)._replace(auth=None).url
    except LocationParseError:
        uri = url
    if user is not None and password is not None:
        return await _get_redirected_url(
            uri,
            authorization="Basic " + base64.b64encode(f"{user}:{password}".encode()).decode(),
        )
    if token is not None and is_pat:
        return await _get_redirected_url(
            uri,
            authorization=("Basic " + base64.b64encode(f":{token}".encode()).decode()),
        )
    if token is not None and not is_pat:
        return await _get_redirected_url(uri, authorization=f"Bearer {token}")
    if url.startswith("http"):
        return await _get_redirected_url(url)
    raise InvalidParameter


async def _get_redirected_url(
    url: str,
    authorization: str | None = None,
) -> str:
    try:
        return await _get_url(url, authorization=authorization)
    except (aiohttp.ClientError, TimeoutError) as exc:
        LOGGER.warning(
            "Failed to get redirected-url",
            extra={"extra": {"url": url, "exc": exc}},
        )
        raise
    except (ValueError, HTTPValidationError) as exc:
        LOGGER.warning(
            "Failed validation to get redirected-url",
            extra={"extra": {"url": url, "exc": exc}},
        )
        raise


async def _get_url(
    original_url: str,
    *,
    redirect_url: str = "",
    max_retries: int = 5,
    authorization: str | None = None,
) -> str:
    try:
        original = parse_url(original_url.removesuffix("/"))
        url = parse_url(redirect_url.removesuffix("/")) if redirect_url else original
    except LocationParseError as exc:
        raise HTTPValidationError(f"Invalid URL {redirect_url}") from exc

    if max_retries < 1:
        return format_redirected_url(original, url)

    # https://git-scm.com/book/en/v2/Git-Internals-Transfer-Protocols
    url = (
        url._replace(path=(url.path or "") + "/info/refs")
        if not (url.path or "").endswith("info/refs")
        else url
    )
    url = url._replace(query="service=git-upload-pack")

    result = await request(
        url.url,
        method="GET",
        headers={
            "Host": url.host or "",
            "Accept": "*/*",
            "Accept-Encoding": "deflate, gzip",
            "Pragma": "no-cache",
            "Accept-Language": "*",
            "User-Agent": "FluidAttacksAPIClient/1.0",
            **({"Authorization": authorization} if authorization else {}),
        },
        timeout=20,
    )
    if result.status == 200:
        return format_redirected_url(original, url)
    if result.status > 300 and result.status < 400 and "Location" in result.headers:
        with suppress(LocationParseError):
            _url = parse_url(result.headers["Location"])
            return await _get_url(
                original_url,
                redirect_url=result.headers["Location"],
                max_retries=max_retries - 1,
                authorization=authorization if _url.host == url.host else None,
            )

        return await _get_url(
            original_url,
            redirect_url=result.headers["Location"],
            max_retries=max_retries - 1,
        )

    return format_redirected_url(original, url)


async def _execute_git_command(
    *,
    url: str,
    branch: str,
    is_pat: bool,
    token: str | None = None,
    follow_redirects: bool = False,
) -> tuple[bytes, bytes, int | None]:
    proc = await asyncio.create_subprocess_exec(
        "git",
        "-c",
        "http.sslVerify=false",
        "-c",
        f"http.followRedirects={follow_redirects}",
        *(
            [
                "-c",
                "http.extraHeader=Authorization: Basic "
                + base64.b64encode(f":{token}".encode()).decode(),
            ]
            if is_pat
            else []
        ),
        "ls-remote",
        "--",
        url,
        branch,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.DEVNULL,
    )
    stdout, _stderr = await asyncio.wait_for(proc.communicate(), 20)

    return stdout, _stderr, proc.returncode


async def https_ls_remote(
    *,
    repo_url: str,
    branch: str,
    user: str | None = None,
    password: str | None = None,
    token: str | None = None,
    provider: str | None = None,
    is_pat: bool = False,
    follow_redirects: bool = False,
) -> tuple[str | None, str | None]:
    url = format_url(
        repo_url=repo_url,
        user=user,
        password=password,
        token=token,
        provider=provider,
        is_pat=is_pat,
    )
    try:
        stdout, stderr, return_code = await _execute_git_command(
            url=url,
            branch=branch,
            is_pat=is_pat,
            token=token,
            follow_redirects=follow_redirects,
        )
    except asyncio.exceptions.TimeoutError:
        return None, "git ls-remote time out"

    if return_code == 0:
        return stdout.decode().split("\t")[0], None

    return None, stderr.decode("utf-8")


async def call_https_ls_remote(
    *,
    repo_url: str,
    user: str | None,
    password: str | None,
    token: str | None,
    branch: str,
    provider: str | None,
    is_pat: bool,
    follow_redirects: bool = False,
) -> tuple[str | None, str | None]:
    if user is not None and password is not None:
        return await https_ls_remote(
            repo_url=repo_url,
            user=user,
            password=password,
            branch=branch,
            follow_redirects=follow_redirects,
        )

    if token is not None:
        return await https_ls_remote(
            repo_url=repo_url,
            token=token,
            branch=branch,
            provider=provider or "",
            is_pat=is_pat,
            follow_redirects=follow_redirects,
        )

    if repo_url.startswith("http"):
        return await https_ls_remote(
            repo_url=repo_url,
            branch=branch,
            follow_redirects=follow_redirects,
        )

    raise InvalidParameter
