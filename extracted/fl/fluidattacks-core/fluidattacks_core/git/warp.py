import asyncio
import logging
import re
import socket

import aiohttp

LOGGER = logging.getLogger(__name__)

CONFIG_DELAY: int = 5  # For WARP to apply network configurations, in seconds
DOMAIN_TO_TEST_DNS: str = "notify.bugsnag.com"  # Using a domain that used to fail


class WarpError(Exception):
    pass


async def test_public_ip(expected_ip: str) -> bool:
    ip_service_url = "https://api.ipify.org?format=text"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(ip_service_url) as response:
                if response.status == 200:
                    public_ip = await response.text()
                    LOGGER.info("Current public IP: %s", public_ip)
                    return public_ip.strip() == expected_ip

                LOGGER.error("Failed to fetch public IP. Status code: %s", response.status)
                return False

    except aiohttp.ClientError as ex:
        LOGGER.exception(ex)
        return False


async def public_ip_ready(expected_ip: str, *, attempts: int, seconds_per_attempt: int) -> bool:
    for attempt_number in range(1, attempts + 1):
        LOGGER.info("Checking public IP... Attempt %s/%s", attempt_number, attempts)
        if await test_public_ip(expected_ip):
            LOGGER.info("Public IP test successful after %s attempts", attempt_number)
            return True

        LOGGER.info("Public IP test failed. Retrying in %s seconds", seconds_per_attempt)
        await asyncio.sleep(seconds_per_attempt)

    LOGGER.error("Public IP test failed after %s attempts", attempts)
    return False


async def _dns_test(host: str) -> bool:
    try:
        socket.gethostbyname(host)
    except socket.gaierror:
        return False
    else:
        return True


async def is_dns_ready(
    *,
    host_to_test_dns: str,
    attempts: int = 40,
    seconds_per_attempt: int = 5,
) -> bool:
    for attempt_number in range(1, attempts + 1):
        LOGGER.info("Waiting for DNS resolution... Attempt %s/%s", attempt_number, attempts)
        if await _dns_test(host_to_test_dns):
            LOGGER.info("DNS resolution successful after %s attempts", attempt_number)
            return True
        LOGGER.error("DNS resolution failed. Retrying in %s seconds...", seconds_per_attempt)
        await asyncio.sleep(seconds_per_attempt)

    LOGGER.error("DNS resolution failed after %s attempts on %s", attempts, host_to_test_dns)
    return False


async def warp_cli(*args: str) -> str:
    proc = await asyncio.create_subprocess_exec(
        "warp-cli",
        "--accept-tos",
        *args,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.DEVNULL,
    )
    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), 30)
    except (asyncio.exceptions.TimeoutError, OSError) as ex:
        raise WarpError("Failed to run command") from ex

    if proc.returncode != 0:
        raise WarpError(stderr.decode().strip())

    return stdout.decode().strip()


async def warp_cli_status() -> str:
    return await warp_cli("status")


async def warp_cli_connect() -> None:
    response = await warp_cli("connect")
    LOGGER.info("Connect: %s", response)
    await asyncio.sleep(CONFIG_DELAY)
    if not await is_dns_ready(host_to_test_dns=DOMAIN_TO_TEST_DNS):
        raise WarpError("Failed to resolve DNS")

    LOGGER.info("Connected. Status: %s", await warp_cli_status())


async def warp_cli_disconnect() -> None:
    response = await warp_cli("disconnect")
    LOGGER.info("Disconnect: %s", response)
    await asyncio.sleep(CONFIG_DELAY)
    LOGGER.info("Disconnected. Status: %s", await warp_cli_status())


async def warp_cli_get_virtual_network_id(vnet_name: str) -> str:
    vnet_id_match = re.search(
        f"ID: (.*)\n  Name: {vnet_name}\n",
        await warp_cli("vnet"),
    )
    if not vnet_id_match:
        raise WarpError(f"Failed to find virtual network {vnet_name}")

    return vnet_id_match.groups()[0]


async def warp_cli_set_virtual_network(vnet_name: str) -> None:
    vnet_id = await warp_cli_get_virtual_network_id(vnet_name)
    await warp_cli("vnet", vnet_id)
    await asyncio.sleep(CONFIG_DELAY)
    LOGGER.info(
        "Setup virtual network. Name: %s, Network ID: %s, Status: %s",
        vnet_name,
        vnet_id,
        await warp_cli_status(),
    )


def _resolve_host(host: str) -> str:
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return host


async def _ip_route_get(host: str) -> tuple[bytes, bytes]:
    target = _resolve_host(host)
    proc = await asyncio.create_subprocess_exec(
        "ip",
        "route",
        "get",
        target,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.DEVNULL,
    )
    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), 5)
    except asyncio.exceptions.TimeoutError as ex:
        raise WarpError("Timeout - Failed to retrieve route") from ex

    if proc.returncode != 0:
        raise WarpError(stderr.decode())

    return stdout, stderr


async def is_using_split_tunnel(host: str) -> bool:
    try:
        stdout, _ = await _ip_route_get(host)
        LOGGER.info("Route command for '%s': %s", host, stdout.decode().replace("\n", " "))
    except WarpError as ex:
        LOGGER.exception(ex)
        return False
    else:
        return b"CloudflareWARP" in stdout
