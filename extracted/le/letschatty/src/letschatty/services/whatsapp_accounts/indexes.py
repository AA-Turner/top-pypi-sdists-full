"""Indexes of the multi-account model. Single source of truth: api-chatty's index migration
creates exactly these, and the integration tests create them on a throwaway database.

The unique indexes ARE the correctness guarantees of the design (one company per number, one
default account per company, one person per BSUID); Redis locks only save work.
"""
from typing import Dict, List, Tuple

from pymongo import ASCENDING, IndexModel

from .mongo_repositories import ACCOUNTS, NUMBERS, PORTFOLIOS, WABAS

CLIENTS = "clients"
CHATS = "chats"

#: One live chat per (company, account, person) from now on. Chats are never merged (decision of
#: 2026-09-29): the duplicates that already existed get `legacy_duplicate_key` (their own id) and
#: stay usable. Created by its own migration step AFTER marking them, never with the others.
UNIQUE_LIVE_CHAT_INDEX = IndexModel(
    [("company_id", ASCENDING), ("account_id", ASCENDING), ("client_id", ASCENDING), ("legacy_duplicate_key", ASCENDING)],
    name="uniq_live_chat_per_account",
    unique=True,
    partialFilterExpression={"deleted_at": None, "client_id": {"$type": "string"}},
)

SOURCES = "sources"

# Not part of WHATSAPP_ACCOUNT_INDEXES on purpose: they replace two live indexes (LEGACY_SOURCE_INDEX_NAMES),
# so api-chatty creates them and drops the old ones in one dedicated step (`sources-indexes`).
#: Source types that exist exactly once per (company, account). Values of `SourceType`.
SINGLETON_SOURCE_TYPES: Tuple[str, ...] = (
    "whatsapp_default_source",  # the organic
    "contact_import",
    "coexistence_echo",
    "meta_ad_inferred",
)


def singleton_source_index_name(source_type: str) -> str:
    return f"uniq_{source_type}_per_account"


#: One singleton source per (company, account, type) among the live ones. `account_id` is part of
#: the key, so documents that still have none collide with each other exactly as the old
#: per-company indexes did, until the migration stamps them.
SOURCE_SINGLETON_INDEXES: List[IndexModel] = [
    IndexModel(
        [("company_id", ASCENDING), ("account_id", ASCENDING)],
        name=singleton_source_index_name(source_type),
        unique=True,
        partialFilterExpression={"type": source_type, "deleted_at": None},
    )
    for source_type in SINGLETON_SOURCE_TYPES
]

#: Replaced by SOURCE_SINGLETON_INDEXES (they were per company, so a second account could never
#: have its own import/inferred source). Dropped in the same run that creates the new ones.
LEGACY_SOURCE_INDEX_NAMES: Tuple[str, ...] = (
    "company_id_contact_import_unique",
    "company_id_meta_ad_inferred_unique",
)

WHATSAPP_ACCOUNT_INDEXES: Dict[str, List[IndexModel]] = {
    ACCOUNTS: [
        IndexModel([("company_id", ASCENDING)], name="idx_company"),
        IndexModel([("waba_id", ASCENDING)], name="idx_waba"),
        IndexModel(
            [("company_id", ASCENDING)],
            name="uniq_default_per_company",
            unique=True,
            partialFilterExpression={"is_default": True},
        ),
    ],
    NUMBERS: [
        IndexModel([("account_id", ASCENDING)], name="idx_account"),
        # «Is this number already in Chatty?» by its visible digits (a new WABA = a new id).
        IndexModel([("digits", ASCENDING)], name="idx_digits"),
    ],
    WABAS: [
        IndexModel([("company_id", ASCENDING), ("waba_id", ASCENDING)], name="uniq_company_waba", unique=True),
        IndexModel([("waba_id", ASCENDING)], name="idx_waba"),
    ],
    PORTFOLIOS: [
        IndexModel([("company_id", ASCENDING), ("portfolio_id", ASCENDING)], name="uniq_company_portfolio", unique=True),
    ],
    CLIENTS: [
        # Separate indexes: a compound index allows a single array field.
        IndexModel(
            [("company_id", ASCENDING), ("bsuids.bsuid", ASCENDING)],
            name="uniq_company_bsuids",
            unique=True,
            partialFilterExpression={"bsuids.bsuid": {"$exists": True}},
        ),
        IndexModel(
            [("company_id", ASCENDING), ("parent_bsuids", ASCENDING)],
            name="uniq_company_parent_bsuids",
            unique=True,
            partialFilterExpression={"parent_bsuids": {"$exists": True}},
        ),
    ],
    CHATS: [
        # Not unique: the guarantee is UNIQUE_LIVE_CHAT_INDEX (with the legacy duplicates out).
        IndexModel(
            [("company_id", ASCENDING), ("account_id", ASCENDING), ("client_id", ASCENDING)],
            name="idx_company_account_client",
        ),
        IndexModel([("company_id", ASCENDING), ("bsuid", ASCENDING)], name="idx_company_bsuid", sparse=True),
    ],
}
