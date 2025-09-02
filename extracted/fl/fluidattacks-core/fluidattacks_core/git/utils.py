from urllib.parse import (
    ParseResult,
    quote,
    unquote,
    urlparse,
)


def _replace_netloc_in_url(parsed_url: ParseResult, netloc: str) -> str:
    return parsed_url._replace(netloc=netloc).geturl()


def _format_token_for_provider(provider: str | None, token: str, host: str) -> str:
    if provider == "BITBUCKET":
        return f"x-token-auth:{token}@{host}"
    if provider:
        return f"oauth2:{token}@{host}"
    return f"{token}@{host}"


def _format_token(
    parsed_url: ParseResult,
    token: str,
    host: str,
    provider: str | None,
) -> str:
    formatted_token = _format_token_for_provider(provider, token, host)
    url = _replace_netloc_in_url(parsed_url, formatted_token)

    return url


def _quote_if_not_none(value: str | None) -> str | None:
    return quote(value, safe="") if value is not None else value


def _quote_path_in_url(url: str) -> ParseResult:
    parsed_url = urlparse(url)
    parsed_url = parsed_url._replace(path=quote(unquote(parsed_url.path)))
    return parsed_url


def _get_host_from_url(parsed_url: ParseResult) -> str:
    host = parsed_url.netloc
    if "@" in host:
        host = host.split("@")[-1]
    return host


def _get_url_based_on_credentials(
    *,
    parsed_url: ParseResult,
    token: str | None,
    host: str,
    provider: str | None,
    user: str | None,
    password: str | None,
) -> str:
    if token is not None:
        return _format_token(parsed_url, token, host, provider)
    if user is not None and password is not None:
        return _replace_netloc_in_url(parsed_url, f"{user}:{password}@{host}")
    return parsed_url.geturl()


def format_url(
    *,
    repo_url: str,
    user: str | None = None,
    password: str | None = None,
    token: str | None = None,
    provider: str | None = None,
    is_pat: bool = False,
) -> str:
    parsed_url = _quote_path_in_url(repo_url)
    if is_pat:
        return parsed_url.geturl()

    host = _get_host_from_url(parsed_url)
    user = _quote_if_not_none(user)
    password = _quote_if_not_none(password)
    url = _get_url_based_on_credentials(
        parsed_url=parsed_url,
        token=token,
        host=host,
        provider=provider,
        user=user,
        password=password,
    )

    return url
