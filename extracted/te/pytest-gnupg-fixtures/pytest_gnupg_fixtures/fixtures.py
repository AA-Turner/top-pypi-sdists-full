#!/usr/bin/env python

# pylint: disable=redefined-outer-name

"""The actual fixtures, you found them ;)."""

import logging
import re
import shutil
import subprocess

from pathlib import Path
from string import Template
from time import time
from typing import Generator, List, NamedTuple

import pytest

from _pytest.tmpdir import TempPathFactory

from .utils import get_embedded_file, get_user_defined_file

LOGGER = logging.getLogger(__name__)


class GnuPGKeypair(NamedTuple):
    # pylint: disable=missing-class-docstring
    email: str
    fingerprints: List[str]
    gnupg_home: Path
    keyid: str
    passphrase: str
    script: Path
    uids: List[str]


class GnuPGTrustStore(NamedTuple):
    # pylint: disable=missing-class-docstring
    gnupg_home: Path


@pytest.fixture
def gnupg_email() -> str:
    """Provides the email to use for the temporary GnuPG keypair."""
    return f"{time()}@pytest-gnupg-fixtures.com"


@pytest.fixture
def gnupg_gen_key_conf(
    pytestconfig: "_pytest.config.Config", tmp_path_factory: TempPathFactory
) -> Generator[Path, None, None]:
    """Provides the location of the templated GnuPG script to generate a temporary keypair."""
    name = "gnupg-gen-key.conf"
    yield from get_user_defined_file(pytestconfig, name)
    yield from get_embedded_file(tmp_path_factory, name=name)


@pytest.fixture
def gnupg_keypair(
    gnupg_email: str,
    gnupg_gen_key_conf: Path,
    gnupg_passphrase: str,
    gnupg_trust_store: GnuPGTrustStore,
    tmp_path: Path,
) -> GnuPGKeypair:
    """Provides a keypair within a temporary GnuPG trust store."""

    LOGGER.debug("Initializing GPG keypair ...")

    # Create a GnuPG script from the template ...
    path_script = tmp_path.joinpath(__name__)
    template = Template(gnupg_gen_key_conf.read_text("utf-8"))
    path_script.write_text(
        template.substitute(
            {"GNUPG_EMAIL": gnupg_email, "GNUPG_PASSPHRASE": gnupg_passphrase}
        ),
        "utf-8",
    )

    environment = {"HOME": "/dev/null"}
    result = subprocess.run(
        [
            "gpg",
            "--batch",
            "--homedir",
            str(gnupg_trust_store.gnupg_home),
            "--gen-key",
            "--keyid-format",
            "long",
            str(path_script),
        ],
        capture_output=True,
        check=True,
        env=environment,
    )
    keyid = re.findall(
        r"gpg: key (\w+) marked as ultimately trusted", result.stderr.decode("utf-8")
    )[0]

    result = subprocess.run(
        [
            "gpg",
            "--fingerprint",
            "--fingerprint",  # Double --fingerprint needed for subkeys
            "--homedir",
            str(gnupg_trust_store.gnupg_home),
            "--with-colons",
            str(keyid),
        ],
        capture_output=True,
        check=True,
        env=environment,
    )
    # Fingerprint order: pubkey [, subkey ]...
    fingerprints = re.findall(r"fpr:{9}(\w+):", result.stdout.decode("utf-8"))

    # Parse UIDs
    uids = re.findall(r"uid(?::(?:\w+)?){8}:([^:]+):", result.stdout.decode("utf-8"))

    LOGGER.debug("  email        : %s", gnupg_email)
    LOGGER.debug("  fingerprints :")
    for fingerprint in fingerprints:
        LOGGER.debug("    %s", fingerprint)
    # LOGGER.debug("  keyid        : %s", keyid)
    LOGGER.debug("  passphrase   : %s", gnupg_passphrase)
    LOGGER.debug("  username     : %s", uids)

    yield GnuPGKeypair(
        email=gnupg_email,
        fingerprints=fingerprints,
        gnupg_home=gnupg_trust_store.gnupg_home,
        keyid=keyid,
        passphrase=gnupg_passphrase,
        script=path_script,
        uids=uids,
    )


@pytest.fixture
def gnupg_passphrase() -> str:
    """Provides the passphrase to use for the temporary GnuPG keypair."""
    return f"pytest.passphrase.{time()}"


@pytest.fixture
def gnupg_trust_store(request, tmp_path_factory: TempPathFactory) -> GnuPGTrustStore:
    """Provides a temporary, initialized, GnuPG trust store."""

    # https://github.com/isislovecruft/python-gnupg/issues/137#issuecomment-459043779
    tmp_path = tmp_path_factory.mktemp(__name__)
    LOGGER.debug("Initializing GPG home: %s ...", tmp_path)
    tmp_path.chmod(0o0700)

    # Note: dirmngr cannot be stopped unless this files exists!?!
    path = tmp_path.joinpath("dirmngr_ldapservers.conf")
    with path.open("w") as file:
        file.write("# GnuPG sucks sometimes!")
    path.chmod(0o600)

    path = tmp_path.joinpath("gpg-agent.conf")
    with path.open("w") as file:
        file.write(
            """
            allow-loopback-pinentry
            max-cache-ttl 60
        """
        )
    path.chmod(0o600)

    # https://betakuang.me/post/2020-05-08-git-gpg-command-line-passphrase.html
    path = tmp_path.joinpath("gpg-wrapper")
    with path.open("w") as file:
        file.write(
            """
            #!/bin/sh
            gpg --passphrase "${GNUPG_PASSPHRASE}" --pinentry-mode loopback $@
            """
        )
    path.chmod(0o755)

    def _stop_dirmngr():
        LOGGER.debug("Stopping dirmngr ...")
        subprocess.run(
            [
                "/usr/bin/gpgconf",
                "--kill",
                "dirmngr",
            ],
            check=False,
            env={"GNUPGHOME": str(tmp_path)},
        )

    def _stop_gpg_agent():
        LOGGER.debug("Stopping gpg-agent ...")
        subprocess.run(
            [
                "/usr/bin/gpg-connect-agent",
                "--homedir",
                str(tmp_path),
                "--no-autostart",
                "killagent",
                "/bye",
            ],
            check=False,
        )

    request.addfinalizer(_stop_dirmngr)
    request.addfinalizer(_stop_gpg_agent)

    yield GnuPGTrustStore(gnupg_home=tmp_path)
    shutil.rmtree(tmp_path, ignore_errors=True)
