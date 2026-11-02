#!/usr/bin/env bash

find_issue_spec_directories() {
    local specs_dir="$1"
    local issue_number="$2"
    find "$specs_dir" -type d \
        \( -name "${issue_number}-*" -o -name "${issue_number}" \) -print | sort
}

is_verified_inherited_task_directory() {
    local existing_dir="$1"
    local repo_root="$2"
    local issue_number="$3"
    local hierarchy_level="$4"
    local spec_context="$5"

    [[ "$hierarchy_level" == "task" ]] || return 1
    [[ "$existing_dir" == "$repo_root/"* ]] || return 1
    [[ "$(basename "$existing_dir")" == "${issue_number}-"* ]] || return 1
    [[ "$spec_context" == specs/*/spec.md ]] || return 1
    [[ "/$spec_context/" != *"/../"* && "/$spec_context/" != *"/./"* && "/$spec_context/" != *"//"* ]] || return 1

    local parent_dir="$repo_root/${spec_context%/spec.md}"
    [[ -f "$parent_dir/spec.md" ]] || return 1
    [[ "$(dirname "$existing_dir")" == "$parent_dir" ]]
}

reconcile_task_parent_metadata() {
    local hierarchy_file="$1"
    local parent_number="$2"
    [[ "$parent_number" =~ ^[0-9]+$ ]] || return 1
    if [[ ! -f "$hierarchy_file" || -L "$hierarchy_file" ]]; then
        echo "Error: Hierarchy metadata must be a regular, non-symlinked file: $hierarchy_file" >&2
        return 1
    fi
    python3 - "$hierarchy_file" "$parent_number" <<'PY'
import re
import sys
from pathlib import Path

hierarchy_file = Path(sys.argv[1])
parent_number = sys.argv[2]
parent_value = f'"{parent_number}"' if len(parent_number) > 1 and parent_number.startswith("0") else parent_number
lines = hierarchy_file.read_text(encoding="utf-8").splitlines()
parent_indexes = [index for index, line in enumerate(lines) if re.match(r"^[ \t]*parent[ \t]*:", line)]
if len(parent_indexes) > 1:
    raise SystemExit(f"Error: Multiple parent declarations in {hierarchy_file}")
if parent_indexes:
    index = parent_indexes[0]
    indentation = re.match(r"^([ \t]*)", lines[index]).group(1)
    lines[index] = f"{indentation}parent: {parent_value}"
else:
    lines.append(f"parent: {parent_value}")
hierarchy_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY
}
