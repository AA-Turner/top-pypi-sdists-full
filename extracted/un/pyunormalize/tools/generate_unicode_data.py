"""Generate Unicode data modules for pyunormalize.

Input files, cached locally or downloaded on demand from Unicode.org:
    - https://www.unicode.org/Public/18.0.0/ucd/CompositionExclusions.txt
    - https://www.unicode.org/Public/18.0.0/ucd/DerivedNormalizationProps.txt
    - https://www.unicode.org/Public/18.0.0/ucd/UnicodeData.txt

Generated output files, written under `_internal/`:
    - _internal/__init__.py
    - _internal/canonical_composition.py
    - _internal/canonical_decomposition.py
    - _internal/compatibility_decomposition.py
    - _internal/nfc_qc_no_or_maybe.py
    - _internal/nfd_qc_no.py
    - _internal/nfkc_qc_no_or_maybe.py
    - _internal/nfkd_qc_no.py
    - _internal/non_zero_ccc_table.py

The generated files are intended to be moved manually into the package
directory after inspection.
"""

import urllib.error
import urllib.request
from pathlib import Path

UNICODE_VERSION = "18.0.0"

ROOT = Path(__file__).resolve().parent
INTERNAL_DIR = ROOT / "_internal"
SCRIPT_PATH = "/".join(Path(__file__).resolve().parts[-3:])

COMPOSITION_EXCLUSIONS_TXT = "CompositionExclusions.txt"
DERIVED_NORMALIZATION_PROPS_TXT = "DerivedNormalizationProps.txt"
UNICODE_DATA_TXT = "UnicodeData.txt"


### File retrieval ############################################################

def get_file_lines(filename):
    """Retrieve file contents locally or from the remote UCD repository."""
    local_path = ROOT / filename

    if local_path.is_file():
        return local_path.read_text(encoding="utf-8").splitlines()

    url = f"https://www.unicode.org/Public/{UNICODE_VERSION}/ucd/{filename}"
    print(f"\n.. {filename} not found locally. Fetching from {url}...")

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "pyunormalize-builder/1.0"},
        )
        with urllib.request.urlopen(req) as response:
            lines = response.read().decode("utf-8").splitlines()
            print(".. Done.")
            return lines

    except urllib.error.URLError as err:
        raise RuntimeError(f"Failed to fetch {url}: {err}") from err


### Formatting helpers ########################################################

def _hex(cp):
    """Format a Unicode code point as a hexadecimal Python integer literal."""
    return f"0x{cp:05X}"


def _format_tuple(items):
    """Format a tuple containing code points and, optionally, a UCD tag."""
    formatted = []

    for item in items:
        if isinstance(item, int):
            formatted.append(_hex(item))
        elif isinstance(item, str):
            formatted.append(repr(item))
        else:
            raise TypeError(f"Unsupported tuple item: {item!r}")

    if len(formatted) == 1:
        return f"({formatted[0]},)"

    return f"({', '.join(formatted)})"


def _format_mapping_to_tuple(mapping):
    """Format a dictionary mapping code points to tuples."""
    if not mapping:
        return ""

    lines = []

    for key in sorted(mapping):
        lines.append(f"    {_hex(key)}: {_format_tuple(mapping[key])},")

    return "\n".join(lines)


def _format_mapping_to_int(mapping, value_width=3):
    """Format a dictionary mapping code points to integers."""
    if not mapping:
        return ""

    lines = []

    for key in sorted(mapping):
        lines.append(f"    {_hex(key)}: {mapping[key]:>{value_width}},")

    return "\n".join(lines)


def _format_composite_mapping(mapping):
    """Format a canonical composition mapping."""
    if not mapping:
        return ""

    lines = []

    for pair in sorted(mapping):
        lines.append(
            f"    ({_hex(pair[0])}, {_hex(pair[1])}): {_hex(mapping[pair])},"
        )

    return "\n".join(lines)


def _format_qc_source_items(items):
    """Format pre-rendered quick-check set entries."""
    return "\n".join(items)


### Parsing ###################################################################

def parse_unicode_data(lines):
    """Parse `UnicodeData.txt`.

    Returns:
        - non-zero canonical combining class table
        - raw decomposition mapping, including compatibility tags
    """
    ccc_table = {}
    decomp_by_character = {}

    for line in lines:
        if not line or line.startswith("#"):
            continue

        code, _, _, ccc, _, decomposition, *_ = line.split(";", 6)
        cp = int(code, 16)

        if ccc != "0":
            ccc_table[cp] = int(ccc)

        if decomposition:
            parsed_decomposition = []

            for token in decomposition.split():
                if token.startswith("<"):
                    parsed_decomposition.append(token)
                else:
                    parsed_decomposition.append(int(token, 16))

            decomp_by_character[cp] = tuple(parsed_decomposition)

    return ccc_table, decomp_by_character


def parse_composition_exclusions(lines):
    """Parse `CompositionExclusions.txt`."""
    assert UNICODE_VERSION in lines[0], (
        f"Unicode version mismatch in {COMPOSITION_EXCLUSIONS_TXT}"
    )

    exclusions = set()

    for line in lines:
        stripped = line.split("#", 1)[0].strip()

        if stripped:
            exclusions.add(int(stripped, 16))

    return exclusions


def _target_list(prop, prop_value, mapping):
    """Resolve the output list for a given normalization property and value."""
    target = mapping.get(prop)

    if isinstance(target, tuple):
        return target[0] if prop_value == "N" else target[1]

    if target is not None:
        return target

    raise ValueError(
        f"Unknown normalization property/value combination: "
        f"{prop}={prop_value}"
    )


def _render_qc_code_item(code):
    """Render a code point or code point range as a set entry."""
    if ".." in code:
        start, end = code.split("..")
        return f"    *range({_hex(int(start, 16))}, {_hex(int(end, 16))} + 1),"

    return f"           {_hex(int(code, 16))},"


def parse_derived_normalization_props(lines):
    """Parse `DerivedNormalizationProps.txt` quick-check data.

    The returned dictionary contains source-code-ready list entries for:
        - NFD_QC_NO
        - NFKD_QC_NO
        - NFC_QC_NO
        - NFC_QC_MAYBE
        - NFKC_QC_NO
        - NFKC_QC_MAYBE
    """
    assert UNICODE_VERSION in lines[0], (
        f"Unicode version mismatch in {DERIVED_NORMALIZATION_PROPS_TXT}"
    )

    nfd_qc_no = []
    nfkd_qc_no = []
    nfc_qc_no = []
    nfc_qc_maybe = []
    nfkc_qc_no = []
    nfkc_qc_maybe = []

    prop_mapping = {
        "NFD_QC": nfd_qc_no,
        "NFKD_QC": nfkd_qc_no,
        "NFC_QC": (nfc_qc_no, nfc_qc_maybe),
        "NFKC_QC": (nfkc_qc_no, nfkc_qc_maybe),
    }

    for line in lines:
        stripped = line.split("#", 1)[0].strip()

        if not stripped:
            continue

        parts = [part.strip() for part in stripped.split(";")]

        if len(parts) < 2:
            continue

        code = parts[0]
        prop = parts[1]
        prop_value = parts[2] if len(parts) > 2 else "N"

        if prop not in prop_mapping:
            continue

        target = _target_list(prop, prop_value, prop_mapping)
        target.append(_render_qc_code_item(code))

    return {
        "NFD_QC_NO": nfd_qc_no,
        "NFKD_QC_NO": nfkd_qc_no,
        "NFC_QC_NO": nfc_qc_no,
        "NFC_QC_MAYBE": nfc_qc_maybe,
        "NFKC_QC_NO": nfkc_qc_no,
        "NFKC_QC_MAYBE": nfkc_qc_maybe,
    }


### Runtime table construction ################################################

def compute_full_decompositions(mapping):
    """Recursively expand decomposition mappings.

    The input mapping must contain integer-only decomposition sequences.
    """
    cache = {}

    def expand(cp, stack):
        if cp in cache:
            return cache[cp]

        if cp not in mapping:
            return (cp,)

        if cp in stack:
            chain = " -> ".join(_hex(item) for item in (*stack, cp))
            raise RuntimeError(f"Cyclic decomposition detected: {chain}")

        expanded = []

        for child in mapping[cp]:
            expanded.extend(expand(child, (*stack, cp)))

        result = tuple(expanded)
        cache[cp] = result
        return result

    full_mapping = {}

    for cp in sorted(mapping):
        full_mapping[cp] = expand(cp, ())

    return full_mapping


def build_runtime_tables(
    decomp_by_character,
    ccc_table,
    composition_exclusions,
):
    """Build runtime composition and full decomposition tables."""
    composite_by_cdecomp = {}
    raw_canonical_decomp = {}
    raw_compatibility_decomp = {}

    for cp in sorted(decomp_by_character):
        decomposition = decomp_by_character[cp]

        if not decomposition:
            raise ValueError(f"Empty decomposition for {_hex(cp)}")

        first = decomposition[0]

        if isinstance(first, int):
            if not all(isinstance(item, int) for item in decomposition):
                raise TypeError(
                    f"Mixed canonical decomposition for {_hex(cp)}: "
                    f"{decomposition!r}"
                )

            sequence = tuple(decomposition)

            raw_canonical_decomp[cp] = sequence
            raw_compatibility_decomp[cp] = sequence

            # Ordinary canonical composition pairs.
            #
            # Hangul syllables are excluded from the data and handled
            # algorithmically in `normalization.py`.
            #
            # Composition exclusions are filtered here so the runtime
            # composition table contains only allowed composites.
            if (
                len(sequence) == 2
                and sequence[0] not in ccc_table
                and cp not in composition_exclusions
            ):
                composite_by_cdecomp[(sequence[0], sequence[1])] = cp

        elif isinstance(first, str):
            sequence = decomposition[1:]

            if not sequence:
                raise ValueError(
                    f"Compatibility tag without decomposition for {_hex(cp)}"
                )

            if not all(isinstance(item, int) for item in sequence):
                raise TypeError(
                    f"Mixed compatibility decomposition for {_hex(cp)}: "
                    f"{decomposition!r}"
                )

            raw_compatibility_decomp[cp] = tuple(sequence)

        else:
            raise TypeError(
                f"Unsupported decomposition entry for {_hex(cp)}: "
                f"{decomposition!r}"
            )

    full_canonical_decomp = compute_full_decompositions(raw_canonical_decomp)
    full_compatibility_decomp = compute_full_decompositions(
        raw_compatibility_decomp
    )

    return (
        composite_by_cdecomp,
        full_canonical_decomp,
        full_compatibility_decomp,
    )


### Writers ###################################################################

def write_internal_init():
    """Write `_internal/__init__.py`."""
    output_path = INTERNAL_DIR / "__init__.py"

    content = f'''\
"""Internal Unicode data package.

Auto-generated via `{SCRIPT_PATH}`.

Do not edit this file manually.
"""

UNICODE_VERSION = "{UNICODE_VERSION}"
'''

    output_path.write_text(content, encoding="utf-8", newline="\n")
    return output_path


def write_non_zero_ccc_table(ccc_table):
    """Write `_internal/non_zero_ccc_table.py`."""
    output_path = INTERNAL_DIR / "non_zero_ccc_table.py"

    content = f'''\
"""Runtime Non-Zero Canonical Combining Class table.

Auto-generated via `{SCRIPT_PATH}`.

Do not edit this file manually.
"""

UNICODE_VERSION = "{UNICODE_VERSION}"

# Dictionary mapping code points with ccc != 0
# to their canonical combining class value
NON_ZERO_CCC_TABLE = {{
{_format_mapping_to_int(ccc_table)}
}}
'''

    output_path.write_text(content, encoding="utf-8", newline="\n")
    return output_path


def write_nfd_qc_no(quick_check):
    """Write `_internal/nfd_qc_no.py`."""
    output_path = INTERNAL_DIR / "nfd_qc_no.py"

    content = f'''\
"""Runtime NFD Quick-Check table.

Auto-generated via `{SCRIPT_PATH}`.

Do not edit this file manually.
"""

UNICODE_VERSION = "{UNICODE_VERSION}"

# Set of code points where NFD_Quick_Check=No,
# i.e., characters that cannot ever occur in normalization form D
NFD_QC_NO = {{
{_format_qc_source_items(quick_check["NFD_QC_NO"])}
}}
'''

    output_path.write_text(content, encoding="utf-8", newline="\n")
    return output_path


def write_nfkd_qc_no(quick_check):
    """Write `_internal/nfkd_qc_no.py`."""
    output_path = INTERNAL_DIR / "nfkd_qc_no.py"

    content = f'''\
"""Runtime NFKD Quick-Check table.

Auto-generated via `{SCRIPT_PATH}`.

Do not edit this file manually.
"""

UNICODE_VERSION = "{UNICODE_VERSION}"

# Set of code points where NFKD_Quick_Check=No,
# i.e., characters that cannot ever occur in normalization form KD
NFKD_QC_NO = {{
{_format_qc_source_items(quick_check["NFKD_QC_NO"])}
}}
'''

    output_path.write_text(content, encoding="utf-8", newline="\n")
    return output_path


def write_nfc_qc_no_or_maybe(quick_check):
    """Write `_internal/nfc_qc_no_or_maybe.py`."""
    output_path = INTERNAL_DIR / "nfc_qc_no_or_maybe.py"

    content = f'''\
"""Runtime NFC Quick-Check table.

Auto-generated via `{SCRIPT_PATH}`.

Do not edit this file manually.
"""

UNICODE_VERSION = "{UNICODE_VERSION}"

# Set of code points where NFC_Quick_Check=No,
# i.e., characters that cannot ever occur in normalization form C
NFC_QC_NO = {{
{_format_qc_source_items(quick_check["NFC_QC_NO"])}
}}

# Set of code points where NFC_Quick_Check=Maybe,
# i.e., characters that may or may not occur in normalization form C,
# depending on context
NFC_QC_MAYBE = {{
{_format_qc_source_items(quick_check["NFC_QC_MAYBE"])}
}}

# Set of code points listed for NFC_Quick_Check=No or NFC_Quick_Check=Maybe
NFC_QC_NO_OR_MAYBE = NFC_QC_NO | NFC_QC_MAYBE

# Cleanup intermediate quick-check sets
del NFC_QC_NO, NFC_QC_MAYBE
'''

    output_path.write_text(content, encoding="utf-8", newline="\n")
    return output_path


def write_nfkc_qc_no_or_maybe(quick_check):
    """Write `_internal/nfkc_qc_no_or_maybe.py`."""
    output_path = INTERNAL_DIR / "nfkc_qc_no_or_maybe.py"

    content = f'''\
"""Runtime NFKC Quick-Check table.

Auto-generated via `{SCRIPT_PATH}`.

Do not edit this file manually.
"""

UNICODE_VERSION = "{UNICODE_VERSION}"

# Set of code points where NFKC_Quick_Check=No,
# i.e., characters that cannot ever occur in normalization form KC
NFKC_QC_NO = {{
{_format_qc_source_items(quick_check["NFKC_QC_NO"])}
}}

# Set of code points where NFKC_Quick_Check=Maybe,
# i.e., characters that may or may not occur in normalization form KC,
# depending on context
NFKC_QC_MAYBE = {{
{_format_qc_source_items(quick_check["NFKC_QC_MAYBE"])}
}}

# Set of code points listed for NFKC_Quick_Check=No or NFKC_Quick_Check=Maybe
NFKC_QC_NO_OR_MAYBE = NFKC_QC_NO | NFKC_QC_MAYBE

# Cleanup intermediate quick-check sets
del NFKC_QC_NO, NFKC_QC_MAYBE
'''

    output_path.write_text(content, encoding="utf-8", newline="\n")
    return output_path


def write_table_c(full_canonical_decomp):
    """Write `_internal/canonical_decomposition.py`."""
    output_path = INTERNAL_DIR / "canonical_decomposition.py"

    content = f'''\
"""Runtime full canonical decomposition table for Unicode normalization.

Auto-generated via `{SCRIPT_PATH}`.

Do not edit this file manually.
"""

UNICODE_VERSION = "{UNICODE_VERSION}"

# Mapping from listed code points to their full canonical decomposition
# sequence, excluding Hangul syllables, which are handled algorithmically
FULL_CDECOMP_BY_CHAR = {{
{_format_mapping_to_tuple(full_canonical_decomp)}
}}
'''

    output_path.write_text(content, encoding="utf-8", newline="\n")
    return output_path


def write_table_k(full_compatibility_decomp):
    """Write `_internal/compatibility_decomposition.py`."""
    output_path = INTERNAL_DIR / "compatibility_decomposition.py"

    content = f'''\
"""Runtime full compatibility decomposition table for Unicode normalization.

Auto-generated via `{SCRIPT_PATH}`.

Do not edit this file manually.
"""

UNICODE_VERSION = "{UNICODE_VERSION}"

# Mapping from listed code points to their full compatibility decomposition
# sequence, excluding Hangul syllables, which are handled algorithmically
FULL_KDECOMP_BY_CHAR = {{
{_format_mapping_to_tuple(full_compatibility_decomp)}
}}
'''

    output_path.write_text(content, encoding="utf-8", newline="\n")
    return output_path


def write_table_comp(composite_by_cdecomp):
    """Write `_internal/canonical_composition.py`."""
    output_path = INTERNAL_DIR / "canonical_composition.py"

    content = f'''\
"""Runtime canonical composition table for Unicode normalization.

Auto-generated via `{SCRIPT_PATH}`.

Do not edit this file manually.
"""

UNICODE_VERSION = "{UNICODE_VERSION}"

# Mapping from canonical decomposition pairs to their allowed composite,
# with composition exclusions already filtered out and Hangul composition
# handled algorithmically
COMPOSITE_BY_CDECOMP = {{
{_format_composite_mapping(composite_by_cdecomp)}
}}
'''

    output_path.write_text(content, encoding="utf-8", newline="\n")
    return output_path


### Main ######################################################################

def main():
    INTERNAL_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Parse UnicodeData.txt
    unicode_data_lines = get_file_lines(UNICODE_DATA_TXT)
    ccc_table, decomp_by_character = parse_unicode_data(unicode_data_lines)

    # 2. Parse CompositionExclusions.txt
    composition_exclusions_lines = get_file_lines(COMPOSITION_EXCLUSIONS_TXT)
    composition_exclusions = parse_composition_exclusions(
        composition_exclusions_lines
    )

    # 3. Parse DerivedNormalizationProps.txt
    derived_normalization_props_lines = get_file_lines(
        DERIVED_NORMALIZATION_PROPS_TXT
    )
    quick_check = parse_derived_normalization_props(
        derived_normalization_props_lines
    )

    # 4. Build precomputed runtime tables
    (
        composite_by_cdecomp,
        full_canonical_decomp,
        full_compatibility_decomp,
    ) = build_runtime_tables(
        decomp_by_character,
        ccc_table,
        composition_exclusions,
    )

    # 5. Write generated modules
    generated_paths = [
        write_internal_init(),
        write_non_zero_ccc_table(ccc_table),
        write_nfd_qc_no(quick_check),
        write_nfkd_qc_no(quick_check),
        write_nfc_qc_no_or_maybe(quick_check),
        write_nfkc_qc_no_or_maybe(quick_check),
        write_table_c(full_canonical_decomp),
        write_table_k(full_compatibility_decomp),
        write_table_comp(composite_by_cdecomp),
    ]

    print("\nSuccessfully generated Unicode data modules:")
    for path in generated_paths:
        print(f"  - {path}")

    print("\nSummary:")
    print(f"  Unicode version: {UNICODE_VERSION}")
    print(f"  CCC entries: {len(ccc_table):,}")
    print(f"  Raw decomposition entries: {len(decomp_by_character):,}")
    print(f"  Composition exclusions: {len(composition_exclusions):,}")
    print(f"  Canonical composition pairs: {len(composite_by_cdecomp):,}")
    print(f"  Full canonical decompositions: {len(full_canonical_decomp):,}")
    print(
        f"  Full compatibility decompositions: "
        f"{len(full_compatibility_decomp):,}"
    )


if __name__ == "__main__":
    main()
