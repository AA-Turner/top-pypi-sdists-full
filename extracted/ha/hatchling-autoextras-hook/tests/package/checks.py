from __future__ import annotations

import logging

import hatchling_autoextras_hook
from hatchling_autoextras_hook import AutoExtrasMetadataHook

logger = logging.getLogger(__name__)


def check_auto_extras_metadata_hook() -> None:
    logger.info("Checking AutoExtrasMetadataHook...")
    metadata = {}
    AutoExtrasMetadataHook("test", {}).update(metadata)
    assert metadata == {"optional-dependencies": {"all": []}}


def check_version() -> None:
    logger.info("Checking __version__...")
    assert hatchling_autoextras_hook.__version__ != "0.0.0"


def main() -> None:
    check_auto_extras_metadata_hook()
    check_version()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
