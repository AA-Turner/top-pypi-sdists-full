"""Democritus functions to interact with Hypothesis."""

import ipaddress
from functools import partial

from hypothesis.strategies._internal.ipaddress import ip_addresses

from d8s_hypothesis import hypothesis_get_strategy_results


def is_ip_address(text: str) -> bool:
    """Determine whether or not the given text is an ip address."""
    try:
        ipaddress.ip_address(text)
    except ValueError:
        return False
    else:
        return True


def test_hypothesis_get_strategy_results_dates():
    ipv4_addresses_func = partial(ip_addresses, v=4)
    results = hypothesis_get_strategy_results(ipv4_addresses_func)
    assert len(results) == 10
    for result in results:
        assert is_ip_address(result)

    # try specifying a specific number
    ipv4_addresses_func = partial(ip_addresses, v=4)
    results = hypothesis_get_strategy_results(ipv4_addresses_func, n=12)
    assert len(results) == 12
    for result in results:
        assert is_ip_address(result)
