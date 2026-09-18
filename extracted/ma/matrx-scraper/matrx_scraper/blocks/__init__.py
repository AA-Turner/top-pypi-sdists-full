"""The Block Ledger's host-neutral half: what a block IS, and how one becomes a row.

A BLOCK IS A FINDING (`common-docs/projects/acquisition-frontier/IDEAS-WIDE.md` §C1 rule 2):
the moment an ingest path fails — a paywall, a login, a rate limit, a format, a CAPTCHA, a
missing API — that failure is the deliverable, not an inconvenience.

The rules of the ledger live here, beside `matrx_scraper.ladder`, which already owns the rung
contract this module's `RUNGS` come from. What stays with each host is only the table access
(`store`) and, in aidream, its generated manager. Read `sink.py` first: it carries the whole
reason this is a package and not a service.
"""

from matrx_scraper.blocks.record import record_block
from matrx_scraper.blocks.selftest import BlockSinkSelfTestFailed, self_test_block_ledger
from matrx_scraper.blocks.sink import (
    BlockSinkNotConfigured,
    assert_block_sink_ready,
    carried_organization_id,
    configure_block_ledger,
    make_block_sink,
)
from matrx_scraper.blocks.store import BlockStore, OrmBlockStore
from matrx_scraper.blocks.unblock import Unblock, unblock_for
from matrx_scraper.blocks.vocabulary import (
    ENGINES,
    RUNGS,
    SOURCE_TYPES,
    STATUSES,
    engine_label,
    source_type_label,
)

__all__ = [
    "ENGINES",
    "RUNGS",
    "SOURCE_TYPES",
    "STATUSES",
    "BlockSinkNotConfigured",
    "BlockSinkSelfTestFailed",
    "BlockStore",
    "OrmBlockStore",
    "Unblock",
    "assert_block_sink_ready",
    "carried_organization_id",
    "configure_block_ledger",
    "engine_label",
    "make_block_sink",
    "record_block",
    "self_test_block_ledger",
    "source_type_label",
    "unblock_for",
]
