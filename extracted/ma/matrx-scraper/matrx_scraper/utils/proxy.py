"""Translate the configured proxy URL into Playwright's proxy contract."""
from urllib.parse import unquote, urlsplit


def playwright_proxy(proxy: str) -> dict[str, str]:
    # Playwright strips URL userinfo from server without transferring it to
    # username/password. Preserve authentication explicitly at this boundary.
    parsed = urlsplit(proxy if "://" in proxy else f"http://{proxy}")
    options = {"server": f"{parsed.scheme}://{parsed.netloc.rsplit('@', 1)[-1]}"}
    if parsed.username is not None:
        options["username"] = unquote(parsed.username)
    if parsed.password is not None:
        options["password"] = unquote(parsed.password)
    return options
