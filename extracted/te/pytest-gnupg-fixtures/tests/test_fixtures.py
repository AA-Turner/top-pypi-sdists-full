#!/usr/bin/env python

# pylint: disable=redefined-outer-name

"""pytest fixture tests."""

import logging

from pathlib import Path

from pytest_gnupg_fixtures import (
    GnuPGKeypair,
    GnuPGTrustStore,
)

LOGGER = logging.getLogger(__name__)


def test_gnupg_email(gnupg_email: str):
    """Test that a passphrase can be provided."""
    assert gnupg_email


def test_gnupg_gen_key_conf(gnupg_gen_key_conf: Path):
    """Test that a GnuPG script to generate a keypair can be provided."""
    assert gnupg_gen_key_conf.exists()
    content = gnupg_gen_key_conf.read_text("utf-8")
    assert "commit" in content


def test_gnupg_keypair(gnupg_keypair: GnuPGKeypair):
    """Test that a GnuPG keypair can be initialized."""
    assert gnupg_keypair.email
    assert gnupg_keypair.fingerprints
    assert gnupg_keypair.gnupg_home.exists()
    assert gnupg_keypair.keyid
    assert gnupg_keypair.passphrase
    assert gnupg_keypair.script.exists()
    assert gnupg_keypair.uids


def test_gnupg_passphrase(gnupg_passphrase: str):
    """Test that a passphrase can be provided."""
    assert gnupg_passphrase


def test_gnupg_trust_store(gnupg_trust_store: GnuPGTrustStore):
    """Test that an temporary GnuPG trust store can be initialized."""
    assert gnupg_trust_store.gnupg_home.exists()
    assert gnupg_trust_store.gnupg_home.is_dir()

    path = Path(gnupg_trust_store.gnupg_home, "gpg-agent.conf")
    assert path.exists()
    content = path.read_text("utf-8")
    assert "allow-loopback-pinentry" in content
