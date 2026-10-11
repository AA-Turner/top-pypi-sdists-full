"""Shared init_bootstrap matrix for unit and integration tests (OpenAPI enums)."""

from itertools import product

# PublicationEntityType indices in swagger (0-21).
ALL_PUBLICATION_ENTITY_TYPES = list(range(22))
# PublicationEntityFormatType: 0 = Cells Structure, 1 = Rows Structure.
ALL_PUBLICATION_ENTITY_FORMATS = [0, 1]

INIT_BOOTSTRAP_PARAM_CASES = list(
    product(ALL_PUBLICATION_ENTITY_TYPES, ALL_PUBLICATION_ENTITY_FORMATS)
)


def init_bootstrap_param_ids() -> list[str]:
    return [f"entity_{et}_format_{ef}" for et, ef in INIT_BOOTSTRAP_PARAM_CASES]


# Entity types accepted by POST /initbootstrap on a live site (integration matrix).
# Types 12 (EntryGroups) and 13 (EntryToEntryGroups) are not standalone bootstrap targets—
# the API returns 400; they are covered when bootstrapping Data (1).
ALLOWED_INIT_BOOTSTRAP_ENTITY_TYPES = [1, 3, 4, 5, 6, 18]

INIT_BOOTSTRAP_ALLOWED_PARAM_CASES = list(
    product(ALLOWED_INIT_BOOTSTRAP_ENTITY_TYPES, ALL_PUBLICATION_ENTITY_FORMATS)
)


def init_bootstrap_allowed_param_ids() -> list[str]:
    return [f"entity_{et}_format_{ef}" for et, ef in INIT_BOOTSTRAP_ALLOWED_PARAM_CASES]
