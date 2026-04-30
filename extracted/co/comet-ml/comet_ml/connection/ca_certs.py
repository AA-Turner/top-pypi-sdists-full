# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2025 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************

import hashlib
import logging
import os
import stat
import tempfile
from typing import List, Optional

import certifi

LOGGER = logging.getLogger(__name__)

# Global custom CA certs placeholder
merged_ca_certs_bundle: Optional[str] = None


def _create_merged_ca_bundle(cert_paths: List[str]) -> str:
    combined = tempfile.NamedTemporaryFile(
        suffix=".pem", delete=False, mode="wb", prefix="comet-ca-"
    )
    for path in [certifi.where()] + cert_paths:
        with open(path, "rb") as f:
            content = f.read()
        combined.write(content)
        if not content.endswith(b"\n"):
            combined.write(b"\n")
    combined.flush()
    combined.close()
    return combined.name


def _persist_merged_ca_bundle(path: str) -> None:
    global merged_ca_certs_bundle
    os.environ["REQUESTS_CA_BUNDLE"] = path
    os.environ["SSL_CERT_FILE"] = path
    merged_ca_certs_bundle = path
    LOGGER.info("Merged CA bundle written to: %s", path)


def setup_ca_certs_from_dir(dir_path: str) -> Optional[str]:
    if merged_ca_certs_bundle is not None:
        return merged_ca_certs_bundle

    LOGGER.info("Setting up custom CA certificates from directory: %s", dir_path)

    cert_paths = []

    for entry in os.scandir(dir_path):
        s = entry.stat()
        perms = stat.filemode(s.st_mode)

        if entry.is_dir():
            continue
        elif entry.is_symlink():
            target = os.path.realpath(entry.path)
            if os.path.isfile(target):
                try:
                    with open(target, "rb") as f:
                        data = f.read()
                    h = hashlib.md5()
                    h.update(data)
                    checksum = f"md5:{h.hexdigest()}"
                    ftype = "symlink->file"
                    cert_paths.append(target)
                except OSError as e:
                    ftype, checksum = "symlink->file(err)", "-"
                    LOGGER.warning("Could not read symlink target %s: %s", target, e)
            elif os.path.isdir(target):
                ftype, checksum = "symlink->dir", "-"
            else:
                ftype, checksum = "symlink->?", "-"
        elif entry.is_file():
            with open(entry.path, "rb") as f:
                data = f.read()
            h = hashlib.md5()
            h.update(data)
            checksum = f"md5:{h.hexdigest()}"
            ftype = "file"
            cert_paths.append(entry.path)
        else:
            ftype, checksum = "other", "-"

        LOGGER.info("%s   %-14s   %-38s   %s", perms, ftype, checksum, entry.name)

    if not cert_paths:
        raise FileNotFoundError(f"No certificate files found in directory: {dir_path}")

    try:
        _persist_merged_ca_bundle(_create_merged_ca_bundle(cert_paths))
    except Exception as e:
        LOGGER.error(
            "Could not set up custom CA certificates from directory: %s, reason: %r",
            dir_path,
            e,
        )

    return merged_ca_certs_bundle


def setup_ca_certs(custom_ca_certs: str) -> Optional[str]:
    if os.path.isdir(custom_ca_certs):
        return setup_ca_certs_from_dir(custom_ca_certs)

    if merged_ca_certs_bundle is not None:
        return merged_ca_certs_bundle

    if not os.path.exists(custom_ca_certs):
        raise FileNotFoundError(
            f"Could not find a suitable TLS CA certificate bundle, invalid path: {custom_ca_certs}"
        )

    LOGGER.info("Setting up custom CA certificates from: %s", custom_ca_certs)

    try:
        _persist_merged_ca_bundle(_create_merged_ca_bundle([custom_ca_certs]))
    except Exception as e:
        LOGGER.error(
            "Could not set up custom CA certificates from: %s, reason: %r",
            custom_ca_certs,
            e,
        )

    return merged_ca_certs_bundle
