"""Shared residue-name constants used across workflows."""

WATER_RESIDUES: frozenset[str] = frozenset({"HOH", "WAT", "H2O", "DOD", "TIP3"})

ION_RESIDUES: frozenset[str] = frozenset(
    {
        "AL",
        "BA",
        "BR",
        "CA",
        "CD",
        "CL",
        "CO",
        "CR",
        "CS",
        "CU",
        "F",
        "FE",
        "FE2",
        "HG",
        "IOD",
        "K",
        "LI",
        "MG",
        "MN",
        "NA",
        "NI",
        "PB",
        "RB",
        "SR",
        "ZN",
    }
)
