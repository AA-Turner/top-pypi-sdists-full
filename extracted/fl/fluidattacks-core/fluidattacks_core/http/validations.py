import html
import ipaddress

from urllib3.exceptions import LocationParseError
from urllib3.util import Url, parse_url


class HTTPValidationError(Exception):
    pass


def validate_scheme(scheme: str | None, schemes: list[str]) -> None:
    if scheme and scheme not in schemes:
        raise HTTPValidationError(f"Only allowed schemes are {', '.join(schemes)}")


def validate_port(port: int | None, ports: list[int]) -> None:
    if port and port < 1024 and port not in ports:
        raise HTTPValidationError(
            f"Only allowed ports are {', '.join(map(str, ports))}, and any over 1024",
        )


def validate_host(host: str | None) -> None:
    if not host:
        return
    try:
        ipaddress.ip_address(host)
    except ValueError:
        if host[0].isalnum():
            return
    else:
        return
    raise HTTPValidationError("Hostname or IP address invalid")


def validate_unicode_restriction(uri: Url) -> None:
    uri_str = str(uri)
    if not uri_str.isascii():
        raise HTTPValidationError(f"URI must be ascii only {uri_str}")


def validate_html_tags(uri: Url) -> None:
    uri_str = str(uri)
    sanitized_uri = html.escape(uri_str)
    if sanitized_uri != uri_str:
        raise HTTPValidationError("HTML/CSS/JS tags are not allowed")


def validate_url(
    url: str,
    *,
    ascii_only: bool,
    enforce_sanitization: bool,
    ports: list[int],
    schemes: list[str],
) -> None:
    try:
        uri = parse_url(url)
    except LocationParseError as exc:
        raise HTTPValidationError(f"Invalid URL {url}") from exc
    validate_host(uri.host)

    if ascii_only:
        validate_unicode_restriction(uri)
    if enforce_sanitization:
        validate_html_tags(uri)
    if ports:
        validate_port(uri.port, ports)
    if schemes:
        validate_scheme(uri.scheme, schemes)


def validate_loopback(
    ips: list[ipaddress.IPv4Address | ipaddress.IPv6Address],
) -> None:
    if any(ip.is_loopback for ip in ips):
        raise HTTPValidationError("Requests to loopback addresses are not allowed")


def validate_local_network(
    ips: list[ipaddress.IPv4Address | ipaddress.IPv6Address],
) -> None:
    if any(ip.is_private for ip in ips):
        raise HTTPValidationError("Requests to the local network are not allowed")


def validate_link_local(
    ips: list[ipaddress.IPv4Address | ipaddress.IPv6Address],
) -> None:
    if any(ip.is_link_local for ip in ips):
        raise HTTPValidationError("Requests to the link local network are not allowed")


def validate_shared_address(
    ips: list[ipaddress.IPv4Address | ipaddress.IPv6Address],
) -> None:
    shared_address_space = ipaddress.ip_network("100.64.0.0/10")
    if any(ip in shared_address_space for ip in ips):
        raise HTTPValidationError("Requests to the shared address space are not allowed")


def validate_limited_broadcast_address(
    ips: list[ipaddress.IPv4Address | ipaddress.IPv6Address],
) -> None:
    limited_broadcast_address = ipaddress.ip_address("255.255.255.255")
    if any(ip == limited_broadcast_address for ip in ips):
        raise HTTPValidationError("Requests to the limited broadcast address are not allowed")


def validate_local_request(
    ips: list[ipaddress.IPv4Address | ipaddress.IPv6Address],
    *,
    allow_local_network: bool,
    allow_localhost: bool,
) -> None:
    if not allow_localhost:
        validate_loopback(ips)

    if not allow_local_network:
        validate_local_network(ips)
        validate_link_local(ips)
        validate_shared_address(ips)
        validate_limited_broadcast_address(ips)
