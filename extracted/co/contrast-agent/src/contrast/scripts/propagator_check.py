# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import argparse
import logging
from sys import version
from sysconfig import get_platform

import contrast
from contrast.agent.assess.utils import get_properties, track_and_tag
from contrast.agent.patch_controller import enable_assess_patches
from contrast.agent.settings import Settings
from contrast.utils.loggers.logger import setup_basic_agent_logger


class ContextDuck:
    @property
    def stop_propagation(self):
        return False

    def propagated(self):
        """No action required, just a dummy method to satisfy the expected API"""


class MyString(str):
    pass


def test_concat():
    x = "foo"
    y = "bar"
    track_and_tag(x)
    return x + y


def test_join():
    x = "sep"
    track_and_tag(x)
    return x.join(["foo", "bar"])


def test_cformat():
    x = "whatever"
    y = "%s in here"
    track_and_tag(x)
    return y % x  # pylint: disable=string-format-interpolation


def test_repr():
    x = b"whatever"
    track_and_tag(x)
    return repr(x)


def test_string_subclass():
    x = "whatever"
    track_and_tag(x)
    return MyString(x)


def test_string_subclass_defined_later():
    x = "whatever"
    track_and_tag(x)

    class MyString(str):
        pass

    return MyString(x)


def test_django_safestring():
    from django.utils.safestring import SafeString

    x = "whatever"
    track_and_tag(x)
    return str(SafeString(x))


PROPAGATOR_TESTS = {
    "cformat": test_cformat,
    "concat": test_concat,
    "join": test_join,
    "repr": test_repr,
    "string subclass": test_string_subclass,
    "string subclass (defined after hook)": test_string_subclass_defined_later,
    "safestring": test_django_safestring,
}


def propagator_check():
    parser = argparse.ArgumentParser(
        description="Checks Contrast agent string propagation"
    )
    parser.parse_args()
    # We don't necessarily need logs from this utility
    setup_basic_agent_logger(level=logging.ERROR)

    settings = Settings()
    settings.config.get_option("assess.enable").env_value = True

    enable_assess_patches()

    # NOTE: here's where we might eventually apply the rewriter

    print("Contrast Agent Propagator Diagnostic Tool")
    print(f"Platform: {get_platform()}, Python: {version}\n")

    num_fails = 0
    with contrast.lifespan(ContextDuck()):
        for name, tester in PROPAGATOR_TESTS.items():
            is_ok = get_properties(tester()) is not None
            # NOTE: maybe add command-line option for no unicode/emoji output
            print("✅" if is_ok else "❌", name)
            if not is_ok:
                num_fails += 1
            contrast.STRING_TRACKER.clear()

    total = len(PROPAGATOR_TESTS)
    num_passes = total - num_fails
    print(f"{num_passes} passed, {num_fails} failed of {total} total")

    return int(bool(num_fails))
