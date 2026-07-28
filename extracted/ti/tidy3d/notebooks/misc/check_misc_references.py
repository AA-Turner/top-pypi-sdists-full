#!/usr/bin/env python3
"""Check QMD references to files under misc/ against import_file_mapping.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath

MISC_REF_RE = re.compile(r"(?<![A-Za-z0-9_./-])(?:\./)?misc/([A-Za-z0-9_.()+@=-]+)")
WRITE_METHODS = [
    "save",
    "savetxt",
    "to_file",
    "to_gds_file",
    "to_stl",
    "write_gds",
]
WRITE_VAR_PATTERNS = [
    "gc_file",
    "history_fname",
    "history_file_path",
    "npy_export_path",
    "output_dir",
    "restart_fname",
    "stl_export_path",
]
WRITE_FILE_WHITELIST = [
    "fiber_lens.stl",
    "fiber_lens_params.npy",
    "inv_des_diamond_light_extractor.gds",
    "my_medium.json",
]
GIT_LFS_POINTER_PREFIX = "version https://git-lfs.github.com/spec/v1"
IMPORT_MAPPING_LFS_MESSAGE = (
    "file is a Git LFS pointer, not the actual JSON content. Fetch notebook LFS assets with "
    "`git lfs pull --include 'flex/public/tidy3d/notebooks/misc/import_file_mapping.json'` "
    "from the repository root and rerun the check."
)


def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_import_file_mapping(misc_dir: Path) -> dict[str, object]:
    mapping_file = misc_dir / "import_file_mapping.json"
    content = mapping_file.read_text(encoding="utf-8")
    if content.startswith(GIT_LFS_POINTER_PREFIX):
        raise ValueError(f"{mapping_file}: {IMPORT_MAPPING_LFS_MESSAGE}")
    mapping = json.loads(content)
    if not isinstance(mapping, dict):
        raise ValueError(f"{mapping_file} must contain a JSON object")
    return mapping


def valid_mapped_files(value: object) -> list[str] | None:
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    return None


def normalize_mapped_misc_path(filename: str) -> str | None:
    relative_path = PurePosixPath(filename)
    if (
        not filename
        or relative_path.is_absolute()
        or "." in relative_path.parts
        or ".." in relative_path.parts
    ):
        return None
    return relative_path.as_posix()


def get_misc_files(misc_dir: Path) -> set[str]:
    return {path.relative_to(misc_dir).as_posix() for path in misc_dir.rglob("*") if path.is_file()}


def is_write_context(content: str, match_start: int) -> bool:
    lookback = content[max(0, match_start - 200) : match_start]
    for method in WRITE_METHODS:
        if re.search(rf"\.?{re.escape(method)}\s*\([^)]*$", lookback):
            return True
    for var_pattern in WRITE_VAR_PATTERNS:
        if re.search(rf"{re.escape(var_pattern)}\s*=\s*(?:Path\()?[\"](?:\./)?$", lookback):
            return True
        if re.search(rf"{re.escape(var_pattern)}\s*=\s*(?:Path\()?['](?:\./)?$", lookback):
            return True
    return False


def find_misc_references(qmd_path: Path) -> set[str]:
    content = qmd_path.read_text(encoding="utf-8")
    references: set[str] = set()
    for match in MISC_REF_RE.finditer(content):
        filename = match.group(1).strip()
        if (
            not filename
            or filename.startswith(".")
            or filename.endswith("_")
            or filename in WRITE_FILE_WHITELIST
            or is_write_context(content, match.start())
        ):
            continue
        references.add(filename)
    return references


def check_qmd(
    qmd_path: Path,
    misc_files: set[str],
    import_mapping: dict[str, object],
    errors: list[str],
    missing_mappings: dict[str, list[str]],
) -> None:
    qmd_name = qmd_path.name
    declared_files = set(valid_mapped_files(import_mapping.get(qmd_name)) or [])

    for reference in sorted(find_misc_references(qmd_path)):
        if reference not in misc_files:
            errors.append(
                f"[FILE NOT FOUND] {qmd_name}: references misc/{reference}, "
                "but the file does not exist"
            )
            continue
        if reference not in declared_files:
            errors.append(
                f"[NOT IN MAPPING] {qmd_name}: references misc/{reference}, "
                "but it is not declared in import_file_mapping.json"
            )
            missing_mappings.setdefault(qmd_name, [])
            if reference not in missing_mappings[qmd_name]:
                missing_mappings[qmd_name].append(reference)


def check_mapping_keys(
    import_mapping: dict[str, object],
    qmd_names: set[str],
    misc_files: set[str],
    errors: list[str],
) -> None:
    for qmd_name, files in sorted(import_mapping.items()):
        if not qmd_name.endswith(".qmd"):
            errors.append(f"[INVALID MAPPING KEY] {qmd_name}: mapping keys must end in .qmd")
            continue
        if qmd_name not in qmd_names:
            errors.append(f"[INVALID MAPPING KEY] {qmd_name}: no matching QMD file exists")
        if not isinstance(files, list) or not all(isinstance(item, str) for item in files):
            errors.append(f"[INVALID MAPPING VALUE] {qmd_name}: expected a list of file names")
            continue
        for filename in files:
            normalized_filename = normalize_mapped_misc_path(filename)
            if normalized_filename is None:
                errors.append(f"[INVALID MAPPING VALUE] {qmd_name}: invalid misc path {filename}")
                continue
            if normalized_filename not in misc_files:
                errors.append(f"[FILE NOT FOUND] {qmd_name}: mapped misc/{filename} is missing")


def update_import_file_mapping(
    misc_dir: Path,
    import_mapping: dict[str, object],
    missing_mappings: dict[str, list[str]],
) -> None:
    for qmd_name, files in sorted(missing_mappings.items()):
        mapped_files = valid_mapped_files(import_mapping.get(qmd_name)) or []
        existing = set(mapped_files)
        for filename in files:
            if filename not in existing:
                mapped_files.append(filename)
        import_mapping[qmd_name] = mapped_files

    mapping_file = misc_dir / "import_file_mapping.json"
    with mapping_file.open("w", encoding="utf-8") as file:
        json.dump(dict(sorted(import_mapping.items())), file, indent=4)
        file.write("\n")

    print(f"\nUpdated {mapping_file}")
    print(f"Added mappings for {len(missing_mappings)} QMD file(s)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Add missing existing misc references to import_file_mapping.json.",
    )
    return parser.parse_args()


def run_checks(
    root_dir: Path, misc_dir: Path
) -> tuple[list[str], dict[str, list[str]], dict[str, object]]:
    import_mapping = load_import_file_mapping(misc_dir)
    misc_files = get_misc_files(misc_dir)
    qmd_files = sorted(root_dir.glob("*.qmd"))
    qmd_names = {path.name for path in qmd_files}

    errors: list[str] = []
    missing_mappings: dict[str, list[str]] = {}

    check_mapping_keys(import_mapping, qmd_names, misc_files, errors)
    for qmd_path in qmd_files:
        check_qmd(qmd_path, misc_files, import_mapping, errors, missing_mappings)

    return errors, missing_mappings, import_mapping


def print_errors(errors: list[str]) -> None:
    print(f"\nFound {len(errors)} issue(s):\n")
    for error in errors:
        print(f"  X {error}")


def main() -> None:
    args = parse_args()
    root_dir = get_project_root()
    misc_dir = root_dir / "misc"

    try:
        errors, missing_mappings, import_mapping = run_checks(root_dir, misc_dir)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Project root: {root_dir}")
    print(f"Found {len(list(root_dir.glob('*.qmd')))} QMD files")
    print(f"Found {len(import_mapping)} notebook mappings")
    print("-" * 60)

    if errors:
        print_errors(errors)
        if args.fix and missing_mappings:
            update_import_file_mapping(misc_dir, import_mapping, missing_mappings)

            remaining_errors, _, _ = run_checks(root_dir, misc_dir)
            if not remaining_errors:
                print("\n[OK] Missing mappings have been fixed.")
                return

            print("\nRemaining issues after updating import_file_mapping.json:")
            print_errors(remaining_errors)
        sys.exit(1)

    print("\n[OK] All misc reference checks passed.")


if __name__ == "__main__":
    main()
