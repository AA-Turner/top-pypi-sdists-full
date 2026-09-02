#!/usr/bin/env bash
#
# resolve-cascade-target.sh — resolve hierarchy.yml path and cascade mode for a given issue
#
# Usage:
#   resolve-cascade-target.sh --issue <number> --spec-base-path <path> [--level <epic|feature|task>]
#
# Standard output (eval-safe shell variable assignments):
#   HIERARCHY_YML=<path>
#   MODE=<first-child|next-sibling>
#
# Standard error:
#   Diagnostic/progress messages and GitHub Actions error annotations.
#
# Exit codes:
#   0  — resolved successfully; HIERARCHY_YML and MODE are set
#   2  — no hierarchy.yml found (standalone issue) or no parent found (task without parent);
#        caller should skip the cascade step gracefully
#   1  — configuration error (unknown level, missing required arguments)

set -euo pipefail

ISSUE_NUMBER=""
SPEC_BASE_PATH=""
HIERARCHY_LEVEL=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --issue)           ISSUE_NUMBER="$2";    shift 2 ;;
    --spec-base-path)  SPEC_BASE_PATH="$2";  shift 2 ;;
    --level)           HIERARCHY_LEVEL="$2"; shift 2 ;;
    *) echo "::error::Unknown argument: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$ISSUE_NUMBER" ]]; then
  echo "::error::--issue is required" >&2
  exit 1
fi
if [[ -z "$SPEC_BASE_PATH" ]]; then
  echo "::error::--spec-base-path is required" >&2
  exit 1
fi

if [[ ! -d "$SPEC_BASE_PATH" ]]; then
  echo "::error::SPEC_BASE_PATH '${SPEC_BASE_PATH}' does not exist or is not a directory" >&2
  exit 1
fi

# --------------------------------------------------------------------------
# Locate hierarchy.yml for the issue
# --------------------------------------------------------------------------
HIERARCHY_YML=""

HIERARCHY_CANDIDATES=()
while IFS= read -r -d '' yml; do
  dir_name="$(basename "$(dirname "$yml")")"
  if [[ "$dir_name" == "$ISSUE_NUMBER" || "$dir_name" == "$ISSUE_NUMBER-"* ]]; then
    HIERARCHY_CANDIDATES+=("$yml")
  fi
done < <(find "$SPEC_BASE_PATH" -name "hierarchy.yml" -type f -print0 2>/dev/null)

if [[ ${#HIERARCHY_CANDIDATES[@]} -gt 1 ]]; then
  echo "::error::Multiple hierarchy.yml candidates found for issue #${ISSUE_NUMBER}; refusing arbitrary selection." >&2
  printf ' - %s\n' "${HIERARCHY_CANDIDATES[@]}" >&2
  exit 1
fi
if [[ ${#HIERARCHY_CANDIDATES[@]} -eq 1 ]]; then
  HIERARCHY_YML="${HIERARCHY_CANDIDATES[0]}"
fi

if [[ -z "$HIERARCHY_YML" ]]; then
  echo "No hierarchy.yml found for issue #${ISSUE_NUMBER} — skipping cascade (standalone issue)" >&2
  exit 2
fi

HIERARCHY_LEVEL="${HIERARCHY_LEVEL,,}"
# Always parse the canonical level from hierarchy.yml regardless of whether --level was supplied.
# A stale or incorrect caller-supplied --level must be caught here before the cascade mode is set.
mapfile -t level_lines < <(grep -E '^level:' "$HIERARCHY_YML" || true)
if [[ ${#level_lines[@]} -ne 1 ]]; then
  echo "::error::Hierarchy file '$HIERARCHY_YML' must contain exactly one 'level:' field for issue #${ISSUE_NUMBER}." >&2
  exit 1
fi
CANONICAL_LEVEL="$(printf '%s' "${level_lines[0]}" \
  | sed -nE \
      -e 's/^level:[[:space:]]*"([^"]*)"([[:space:]]+(#.*)?)?[[:space:]]*$/\1/p' \
      -e "s/^level:[[:space:]]*'([^']*)'([[:space:]]+(#.*)?)?[[:space:]]*$/\1/p" \
      -e 's/^level:[[:space:]]*([^#"'"'"'\t ]+)([[:space:]]+(#.*)?)?[[:space:]]*$/\1/p' \
  | xargs)"
if [[ -z "$CANONICAL_LEVEL" ]]; then
  echo "::error::Empty hierarchy level in '$HIERARCHY_YML' for issue #${ISSUE_NUMBER}." >&2
  exit 1
fi
CANONICAL_LEVEL="${CANONICAL_LEVEL,,}"
if [[ -n "$HIERARCHY_LEVEL" && "$HIERARCHY_LEVEL" != "$CANONICAL_LEVEL" ]]; then
  echo "::error::Supplied --level '${HIERARCHY_LEVEL}' conflicts with canonical level '${CANONICAL_LEVEL}' in '$HIERARCHY_YML' for issue #${ISSUE_NUMBER}; failing closed." >&2
  exit 1
fi
HIERARCHY_LEVEL="$CANONICAL_LEVEL"
case "$HIERARCHY_LEVEL" in
  epic|feature|task) ;;
  *)
    echo "::error::Unknown hierarchy level '${HIERARCHY_LEVEL}' for issue #${ISSUE_NUMBER}; failing closed." >&2
    exit 1
    ;;
esac

echo "Found hierarchy.yml at: $HIERARCHY_YML (level: $HIERARCHY_LEVEL)" >&2

# --------------------------------------------------------------------------
# Determine cascade mode from hierarchy level
# --------------------------------------------------------------------------
case "$HIERARCHY_LEVEL" in
  epic|feature)
    MODE="first-child"
    ;;
  task)
    # For tasks, cascade to the next sibling — requires the parent's hierarchy.yml.
    # First try the nested path: specs/{epic}/{feature}/{task}/hierarchy.yml →
    # two dirname() levels up lands at specs/{epic}/{feature}/hierarchy.yml.
    mapfile -t parent_lines < <(grep -E '^[[:space:]]*parent:' "$HIERARCHY_YML" || true)
    DECLARED_PARENT_NUMBER=""
    if [[ ${#parent_lines[@]} -gt 1 ]]; then
      echo "::error::Multiple 'parent:' declarations found in '$HIERARCHY_YML' for task #${ISSUE_NUMBER}; refusing arbitrary selection." >&2
      exit 1
    fi
    if [[ ${#parent_lines[@]} -eq 1 ]]; then
      parent_line="${parent_lines[0]}"
      DECLARED_PARENT_NUMBER="$(printf '%s' "$parent_line" \
        | sed -nE \
            -e 's/^[[:space:]]*parent:[[:space:]]*"#?([0-9]+)"([[:space:]]+(#.*)?)?[[:space:]]*$/\1/p' \
            -e "s/^[[:space:]]*parent:[[:space:]]*'#?([0-9]+)'([[:space:]]+(#.*)?)?[[:space:]]*$/\\1/p" \
            -e 's/^[[:space:]]*parent:[[:space:]]*#?([0-9]+)([[:space:]]+(#.*)?)?[[:space:]]*$/\1/p' \
        | xargs)"
      if [[ -z "$DECLARED_PARENT_NUMBER" ]]; then
        echo "::error::Malformed or unsupported 'parent:' declaration in '$HIERARCHY_YML' for task #${ISSUE_NUMBER}; expected exactly one bare numeric issue number (for example: parent: 42)." >&2
        exit 1
      fi
      if [[ "$DECLARED_PARENT_NUMBER" == "$ISSUE_NUMBER" ]]; then
        echo "::error::Task #${ISSUE_NUMBER} declares itself as parent in '$HIERARCHY_YML'; refusing invalid self-parent hierarchy." >&2
        exit 1
      fi
    fi
    PARENT_DIR="$(dirname "$(dirname "$HIERARCHY_YML")")"
    PARENT_YML="$PARENT_DIR/hierarchy.yml"
    PARENT_CANDIDATES=()
    if [[ -n "$DECLARED_PARENT_NUMBER" ]]; then
      if [[ -f "$PARENT_YML" ]]; then
        PARENT_DIR_NAME="$(basename "$PARENT_DIR")"
        if [[ "$PARENT_DIR_NAME" != "$DECLARED_PARENT_NUMBER" && "$PARENT_DIR_NAME" != "$DECLARED_PARENT_NUMBER-"* ]]; then
          echo "::error::Task #${ISSUE_NUMBER} declares parent #${DECLARED_PARENT_NUMBER}, but nested hierarchy infers a different parent directory." >&2
          printf ' - inferred directory: %s\n - declared parent: #%s\n' "$PARENT_DIR_NAME" "$DECLARED_PARENT_NUMBER" >&2
          exit 1
        fi
      fi
      while IFS= read -r -d '' yml; do
        DIR_NAME="$(basename "$(dirname "$yml")")"
        if [[ "$DIR_NAME" == "$DECLARED_PARENT_NUMBER" || "$DIR_NAME" == "$DECLARED_PARENT_NUMBER-"* ]]; then
          PARENT_CANDIDATES+=("$yml")
        fi
      done < <(find "$SPEC_BASE_PATH" -name "hierarchy.yml" -type f -print0 2>/dev/null)
      if [[ ${#PARENT_CANDIDATES[@]} -gt 1 ]]; then
        echo "::error::Multiple parent hierarchy.yml candidates found for task #${ISSUE_NUMBER}; refusing arbitrary selection." >&2
        printf ' - %s\n' "${PARENT_CANDIDATES[@]}" >&2
        exit 1
      fi
      if [[ ${#PARENT_CANDIDATES[@]} -eq 1 ]]; then
        DECLARED_PARENT_YML="${PARENT_CANDIDATES[0]}"
        if [[ -f "$PARENT_YML" && "$DECLARED_PARENT_YML" != "$PARENT_YML" ]]; then
          echo "::error::Task #${ISSUE_NUMBER} declares parent #${DECLARED_PARENT_NUMBER}, but nested hierarchy infers a different parent hierarchy.yml." >&2
          printf ' - inferred: %s\n - declared: %s\n' "$PARENT_YML" "$DECLARED_PARENT_YML" >&2
          exit 1
        fi
        PARENT_YML="$DECLARED_PARENT_YML"
      fi
    elif [[ ! -f "$PARENT_YML" ]]; then
      echo "No 'parent:' field found in '$HIERARCHY_YML' for task #${ISSUE_NUMBER}; skipping cascade" >&2
      exit 2
    fi
    if [[ ! -f "$PARENT_YML" ]]; then
      # Nested path did not yield a parent yml (e.g. legacy flat layout), and no
      # declared parent candidate resolved to a concrete hierarchy file.
      echo "No parent hierarchy.yml found for task #${ISSUE_NUMBER} — skipping cascade" >&2
      exit 2
    fi
    HIERARCHY_YML="$PARENT_YML"
    MODE="next-sibling"
    ;;
  *)
    echo "::error::Unknown hierarchy level '${HIERARCHY_LEVEL}' for issue #${ISSUE_NUMBER}; cannot determine cascade mode." >&2
    exit 1
    ;;
esac

echo "Cascade mode: $MODE, hierarchy.yml: $HIERARCHY_YML" >&2

# Output shell variable assignments for the caller to eval
printf 'HIERARCHY_YML=%q\nMODE=%q\n' "$HIERARCHY_YML" "$MODE"
