#!/usr/bin/env bash

set -e

JSON_MODE=false
SHORT_NAME=""
ISSUE_NUMBER=""
EXPLICIT_ISSUE=""
FLAT_MODE=false
PARENT_NUMBER=""
ARGS=()
i=1
while [ $i -le $# ]; do
    arg="${!i}"
    case "$arg" in
        --json) 
            JSON_MODE=true 
            ;;
        --flat)
            FLAT_MODE=true
            ;;
        --parent)
            if [ $((i + 1)) -gt $# ]; then
                echo "[specify] Error: --parent requires a value" >&2
                exit 1
            fi
            i=$((i + 1))
            next_arg="${!i}"
            if [[ "$next_arg" == --* ]]; then
                echo "[specify] Error: --parent requires a value" >&2
                exit 1
            fi
            PARENT_NUMBER="$next_arg"
            ;;
        --short-name)
            if [ $((i + 1)) -gt $# ]; then
                echo 'Error: --short-name requires a value' >&2
                exit 1
            fi
            i=$((i + 1))
            next_arg="${!i}"
            # Check if the next argument is another option (starts with --)
            if [[ "$next_arg" == --* ]]; then
                echo 'Error: --short-name requires a value' >&2
                exit 1
            fi
            SHORT_NAME="$next_arg"
            ;;
        --issue|--number)
            if [ $((i + 1)) -gt $# ]; then
                echo "Error: $arg requires a value" >&2
                exit 1
            fi
            i=$((i + 1))
            next_arg="${!i}"
            if [[ "$next_arg" == --* ]]; then
                echo "Error: $arg requires a value" >&2
                exit 1
            fi
            if [[ ! "$next_arg" =~ ^[1-9][0-9]*$ ]]; then
                echo "Error: $arg requires a positive integer (got '$next_arg')" >&2
                exit 1
            fi
            ISSUE_NUMBER="$next_arg"
            EXPLICIT_ISSUE=true
            ;;
        --help|-h) 
            echo "Usage: $0 [--json] [--short-name <name>] [--issue N] [--parent P] [--flat] <feature_description>"
            echo ""
            echo "Options:"
            echo "  --json              Output in JSON format"
            echo "  --short-name <name> Provide a custom short name (2-4 words) for the branch"
            echo "  --issue N           GitHub issue number to use as directory/branch prefix"
            echo "  --number N          Deprecated alias for --issue"
            echo "  --parent P          Explicit parent issue number (overrides hierarchy detection)"
            echo "  --flat              Force flat directory creation (ignore hierarchy)"
            echo "  --help, -h          Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 --issue 1175 'Plan phase fails for large specs' --short-name 'plan-phase-fails-large'"
            echo "  $0 --issue 42 'Add user authentication system'"
            echo "  $0 --issue 200 --parent 100 'Child feature'"
            echo "  $0 --issue 200 --flat 'Force flat layout'"
            exit 0
            ;;
        *) 
            ARGS+=("$arg") 
            ;;
    esac
    i=$((i + 1))
done

# Validate --parent when --flat is not set
if [ -n "$PARENT_NUMBER" ] && [ "$FLAT_MODE" = false ]; then
    if [[ ! "$PARENT_NUMBER" =~ ^[1-9][0-9]*$ ]]; then
        echo "[specify] Error: --parent requires a positive integer (got '$PARENT_NUMBER')" >&2
        exit 1
    fi
fi

# Validate: --parent requires --issue when --flat is not set
if [ -n "$PARENT_NUMBER" ] && [ -z "$EXPLICIT_ISSUE" ] && [ "$FLAT_MODE" = false ]; then
    echo "[specify] Error: --parent requires --issue to be specified (hierarchy nesting requires an explicit issue number)" >&2
    exit 1
fi

# Fail fast when explicit nested creation is requested but python3 is unavailable.
# The hierarchy YAML update later depends on python3; checking early avoids creating
# partial directories before hitting a confusing "command not found" error.
if [ -n "$PARENT_NUMBER" ] && [ "$FLAT_MODE" = false ]; then
    if ! command -v python3 >/dev/null 2>&1; then
        echo "[specify] Error: python3 is required for nested hierarchy creation but was not found on PATH" >&2
        exit 1
    fi
fi

FEATURE_DESCRIPTION="${ARGS[*]}"
if [ -z "$FEATURE_DESCRIPTION" ]; then
    echo "Usage: $0 [--json] [--short-name <name>] [--issue N] <feature_description>" >&2
    exit 1
fi

# Function to find the repository root by searching for existing project markers
find_repo_root() {
    local dir="$1"
    while [ "$dir" != "/" ]; do
        if [ -d "$dir/.git" ] || [ -d "$dir/.specify" ]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}

# Function to get highest number from specs directory (legacy 3-digit prefixes only)
get_highest_from_specs() {
    local specs_dir="$1"
    local highest=0
    
    if [ -d "$specs_dir" ]; then
        for dir in "$specs_dir"/*; do
            [ -d "$dir" ] || continue
            dirname=$(basename "$dir")
            # Only match legacy 3-digit prefixed directories (e.g., 001-feature)
            # to avoid picking up issue-number dirs (e.g., 1175-feature)
            if echo "$dirname" | grep -q '^[0-9]\{3\}-'; then
                number=$(echo "$dirname" | grep -o '^[0-9]\{3\}')
                number=$((10#$number))
                if [ "$number" -gt "$highest" ]; then
                    highest=$number
                fi
            fi
        done
    fi
    
    echo "$highest"
}

# Function to get highest number from git branches
get_highest_from_branches() {
    local highest=0
    
    # Get all branches (local and remote)
    branches=$(git branch -a 2>/dev/null || echo "")
    
    if [ -n "$branches" ]; then
        while IFS= read -r branch; do
            # Clean branch name: remove leading markers and remote prefixes
            clean_branch=$(echo "$branch" | sed 's/^[* ]*//; s|^remotes/[^/]*/||')
            
            # Extract feature number if branch matches pattern ###-*
            if echo "$clean_branch" | grep -q '^[0-9]\{3\}-'; then
                number=$(echo "$clean_branch" | grep -o '^[0-9]\{3\}' || echo "0")
                number=$((10#$number))
                if [ "$number" -gt "$highest" ]; then
                    highest=$number
                fi
            fi
        done <<< "$branches"
    fi
    
    echo "$highest"
}

# Function to check existing branches (local and remote) and return next available number
check_existing_branches() {
    local specs_dir="$1"

    # Fetch all remotes to get latest branch info (suppress errors if no remotes)
    git fetch --all --prune 2>/dev/null || true

    # Get highest number from ALL branches (not just matching short name)
    local highest_branch=$(get_highest_from_branches)

    # Get highest number from ALL specs (not just matching short name)
    local highest_spec=$(get_highest_from_specs "$specs_dir")

    # Take the maximum of both
    local max_num=$highest_branch
    if [ "$highest_spec" -gt "$max_num" ]; then
        max_num=$highest_spec
    fi

    # Return next number
    echo $((max_num + 1))
}

# Function to clean and format a branch name
clean_branch_name() {
    local name="$1"
    echo "$name" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$//'
}

# Resolve repository root. Prefer git information when available, but fall back
# to searching for repository markers so the workflow still functions in repositories that
# were initialised with --no-git.
SCRIPT_DIR="$(CDPATH="" cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if git rev-parse --show-toplevel >/dev/null 2>&1; then
    REPO_ROOT=$(git rev-parse --show-toplevel)
    HAS_GIT=true
else
    REPO_ROOT="$(find_repo_root "$SCRIPT_DIR")"
    if [ -z "$REPO_ROOT" ]; then
        echo "Error: Could not determine repository root. Please run this script from within the repository." >&2
        exit 1
    fi
    HAS_GIT=false
fi

cd "$REPO_ROOT"

SPECS_DIR="$REPO_ROOT/specs"
mkdir -p "$SPECS_DIR"

# Function to generate branch name with stop word filtering and length filtering
generate_branch_name() {
    local description="$1"
    
    # Common stop words to filter out
    local stop_words="^(i|a|an|the|to|for|of|in|on|at|by|with|from|is|are|was|were|be|been|being|have|has|had|do|does|did|will|would|should|could|can|may|might|must|shall|this|that|these|those|my|your|our|their|want|need|add|get|set)$"
    
    # Convert to lowercase and split into words
    local clean_name=$(echo "$description" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/ /g')
    
    # Filter words: remove stop words and words shorter than 3 chars (unless they're uppercase acronyms in original)
    local meaningful_words=()
    for word in $clean_name; do
        # Skip empty words
        [ -z "$word" ] && continue
        
        # Keep words that are NOT stop words AND (length >= 3 OR are potential acronyms)
        if ! echo "$word" | grep -qiE "$stop_words"; then
            if [ ${#word} -ge 3 ]; then
                meaningful_words+=("$word")
            elif echo "$description" | grep -q "\b${word^^}\b"; then
                # Keep short words if they appear as uppercase in original (likely acronyms)
                meaningful_words+=("$word")
            fi
        fi
    done
    
    # If we have meaningful words, use first 3-4 of them
    if [ ${#meaningful_words[@]} -gt 0 ]; then
        local max_words=3
        if [ ${#meaningful_words[@]} -eq 4 ]; then max_words=4; fi
        
        local result=""
        local count=0
        for word in "${meaningful_words[@]}"; do
            if [ $count -ge $max_words ]; then break; fi
            if [ -n "$result" ]; then result="$result-"; fi
            result="$result$word"
            count=$((count + 1))
        done
        echo "$result"
    else
        # Fallback to original logic if no meaningful words found
        local cleaned=$(clean_branch_name "$description")
        echo "$cleaned" | tr '-' '\n' | grep -v '^$' | head -3 | tr '\n' '-' | sed 's/-$//'
    fi
}

# Generate branch name
if [ -n "$SHORT_NAME" ]; then
    # Use provided short name, just clean it up
    BRANCH_SUFFIX=$(clean_branch_name "$SHORT_NAME")
else
    # Generate from description with smart filtering
    BRANCH_SUFFIX=$(generate_branch_name "$FEATURE_DESCRIPTION")
fi

# Determine feature number (issue number or auto-detected sequential number)
if [ -z "$ISSUE_NUMBER" ]; then
    if [ "$HAS_GIT" = true ]; then
        # Legacy fallback: auto-detect next sequential number
        ISSUE_NUMBER=$(check_existing_branches "$SPECS_DIR")
    else
        # Fall back to local directory check
        HIGHEST=$(get_highest_from_specs "$SPECS_DIR")
        ISSUE_NUMBER=$((HIGHEST + 1))
    fi
fi

# When --issue was explicitly provided, use the number as-is (no zero-padding).
# When the number was auto-detected from legacy 3-digit dirs/branches, preserve
# the 3-digit zero-padded format so the new branch/dir will be picked up by
# subsequent legacy detection runs.
if [ -n "$EXPLICIT_ISSUE" ]; then
    FEATURE_NUM="$((10#$ISSUE_NUMBER))"
else
    FEATURE_NUM=$(printf "%03d" "$((10#$ISSUE_NUMBER))")
fi
BRANCH_NAME="${FEATURE_NUM}-${BRANCH_SUFFIX}"

# GitHub enforces a 244-byte limit on branch names
# Validate and truncate if necessary
MAX_BRANCH_LENGTH=244
if [ ${#BRANCH_NAME} -gt $MAX_BRANCH_LENGTH ]; then
    # Calculate how much we need to trim from suffix
    # Account for: feature number (variable length) + hyphen (1)
    PREFIX_LENGTH=$(( ${#FEATURE_NUM} + 1 ))
    MAX_SUFFIX_LENGTH=$((MAX_BRANCH_LENGTH - PREFIX_LENGTH))
    
    # Truncate suffix at word boundary if possible
    TRUNCATED_SUFFIX=$(echo "$BRANCH_SUFFIX" | cut -c1-$MAX_SUFFIX_LENGTH)
    # Remove trailing hyphen if truncation created one
    TRUNCATED_SUFFIX=$(echo "$TRUNCATED_SUFFIX" | sed 's/-$//')
    
    ORIGINAL_BRANCH_NAME="$BRANCH_NAME"
    BRANCH_NAME="${FEATURE_NUM}-${TRUNCATED_SUFFIX}"
    
    >&2 echo "[specify] Warning: Branch name exceeded GitHub's 244-byte limit"
    >&2 echo "[specify] Original: $ORIGINAL_BRANCH_NAME (${#ORIGINAL_BRANCH_NAME} bytes)"
    >&2 echo "[specify] Truncated to: $BRANCH_NAME (${#BRANCH_NAME} bytes)"
fi

if [ "$HAS_GIT" = true ]; then
    git checkout -b "$BRANCH_NAME"
else
    >&2 echo "[specify] Warning: Git repository not detected; skipped branch creation for $BRANCH_NAME"
fi

# ============================================================================
# Hierarchy-aware directory creation
# ============================================================================

# Resolve repository owner/repo for hierarchy detection
resolve_repo_slug() {
    # Try gh CLI first
    if command -v gh >/dev/null 2>&1; then
        local slug
        slug=$(gh repo view --json nameWithOwner -q '.nameWithOwner' 2>/dev/null) || true
        if [ -n "$slug" ] && [[ "$slug" == */* ]]; then
            echo "$slug"
            return 0
        fi
    fi
    # Fall back to parsing git remote
    if [ "$HAS_GIT" = true ]; then
        local remote_url
        remote_url=$(git remote get-url origin 2>/dev/null) || true
        if [ -n "$remote_url" ]; then
            # Handle SSH format: git@github.com:owner/repo.git
            local slug
            slug=$(echo "$remote_url" | sed -E 's|.*[:/]([^/]+/[^/]+?)(\.git)?$|\1|')
            if [[ "$slug" == */* ]]; then
                echo "$slug"
                return 0
            fi
        fi
    fi
    return 1
}

# Invoke hierarchy detector with timeout
# Sets: DETECTED_PARENT, DETECTED_LEVEL, DETECTED_TITLE, DETECTOR_STATUS
invoke_hierarchy_detector() {
    local issue_num="$1"
    local repo_slug="$2"

    DETECTED_PARENT=""
    DETECTED_LEVEL=""
    DETECTED_TITLE=""
    DETECTOR_STATUS="error"

    if [ -z "$repo_slug" ]; then
        return 1
    fi

    local output detector_stderr
    detector_stderr=$(mktemp)
    if ! output=$(python3 -m agentic_devtools.cli.speckit.detect_parent_cli \
        --issue "$issue_num" --repo "$repo_slug" --timeout 10 2>"$detector_stderr"); then
        # Show stderr on failure for diagnostics
        if [ -s "$detector_stderr" ]; then
            echo "[specify] Hierarchy detector: $(cat "$detector_stderr")" >&2
        fi
        rm -f "$detector_stderr"
        return 1
    fi
    rm -f "$detector_stderr"

    # Parse line-oriented output
    local status parent level title
    while IFS= read -r line; do
        case "$line" in
            status=*) status="${line#status=}" ;;
            parent=*) parent="${line#parent=}" ;;
            level=*) level="${line#level=}" ;;
            title=*) title="${line#title=}" ;;
        esac
    done <<< "$output"

    if [ "$status" = "ok" ]; then
        DETECTOR_STATUS="ok"
        [ "$parent" != "null" ] && DETECTED_PARENT="$parent"
        [ "$level" != "null" ] && DETECTED_LEVEL="$level"
        [ "$title" != "null" ] && DETECTED_TITLE="$title"
        return 0
    fi
    return 1
}

# Find parent spec directory by scanning specs/ recursively (no symlinks)
# Returns the path to the parent spec directory
find_parent_dir() {
    local specs_dir="$1"
    local parent_key="$2"
    local matches=()

    # Use find to scan recursively, no symlinks
    while IFS= read -r -d '' dir; do
        local base
        base=$(basename "$dir")
        # Match exact key or key-followed-by-hyphen
        if [ "$base" = "$parent_key" ] || [[ "$base" == "${parent_key}-"* ]]; then
            matches+=("$dir")
        fi
    done < <(find "$specs_dir" -not -type l -type d -print0 2>/dev/null)

    if [ ${#matches[@]} -eq 0 ]; then
        echo ""
        return 1
    elif [ ${#matches[@]} -eq 1 ]; then
        echo "${matches[0]}"
        return 0
    else
        echo "[specify] Error: Multiple spec directories found matching parent '$parent_key':" >&2
        for m in "${matches[@]}"; do
            echo "  $m" >&2
        done
        return 2
    fi
}

# Compute nesting depth from specs/ root
# specs/ = root (0), specs/100-epic/ = depth 1, specs/100-epic/200/ = depth 2
compute_nesting_depth() {
    local specs_dir="$1"
    local target_dir="$2"

    # Get relative path from specs_dir to target_dir
    local rel_path="${target_dir#$specs_dir/}"
    # Count path separators
    local depth
    depth=$(echo "$rel_path" | tr -cd '/' | wc -c)
    echo "$((depth + 1))"
}

# Create hierarchy.yml for a directory
create_hierarchy_yml() {
    local dir="$1"
    local title="$2"
    local level="$3"
    local parent_key="$4"

    local hierarchy_file="$dir/hierarchy.yml"
    local parent_field="null"
    if [ -n "$parent_key" ]; then
        parent_field="'$parent_key'"
    fi

    # Escape single quotes for YAML single-quoted scalars (' → '').
    # Use double-quoted literal forms to avoid ambiguity with backslash
    # handling inside ${...//} expansions across bash versions.
    local escaped_title="${title//"'"/"''"}"

    cat > "$hierarchy_file" <<EOF
title: '$escaped_title'
level: $level
parent: $parent_field
children: []
processed_at: null
EOF
}

_update_parent_hierarchy_with_advisory_lock() {
    local lock_file="$1"
    local hierarchy_file="$2"
    local child_key="$3"
    local child_title="$4"
    local parent_title="$5"
    local parent_level="$6"

    _LOCK_FILE="$lock_file" _HIER_FILE="$hierarchy_file" _CHILD_KEY="$child_key" _CHILD_TITLE="$child_title" \
    _PARENT_TITLE="$parent_title" _PARENT_LEVEL="$parent_level" \
    python3 -c "
import json
import os
import sys
import tempfile
import time
from pathlib import Path

import yaml

def _acquire_lock_nb(fd: int) -> bool:
    '''Attempt a non-blocking exclusive lock; return True on success.'''
    if sys.platform == 'win32':
        import msvcrt
        try:
            os.lseek(fd, 0, os.SEEK_SET)
            msvcrt.locking(fd, msvcrt.LK_NBLCK, 1 << 30)
            return True
        except OSError:
            return False
    else:
        import fcntl
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except BlockingIOError:
            return False

lock_file = Path(os.environ['_LOCK_FILE'])
hierarchy_file = Path(os.environ['_HIER_FILE'])
child_key = os.environ['_CHILD_KEY']
child_title = os.environ['_CHILD_TITLE']
parent_title = os.environ['_PARENT_TITLE']
parent_level = os.environ['_PARENT_LEVEL']
child_order = int(child_key) if child_key.isdigit() else 0

o_nofollow = getattr(os, 'O_NOFOLLOW', 0)
fd = os.open(lock_file, os.O_CREAT | os.O_RDWR | o_nofollow)
try:
    if sys.platform != 'win32':
        st_lock = os.fstat(fd)
        try:
            st_path = os.lstat(str(lock_file))
        except OSError:
            raise SystemExit(f'[specify] Error: Lock path disappeared after open: {lock_file}')
        if st_lock.st_ino != st_path.st_ino or st_lock.st_dev != st_path.st_dev:
            raise SystemExit(f'[specify] Error: Lock path was replaced after open: {lock_file}')

    deadline = time.monotonic() + 5.0
    while True:
        if _acquire_lock_nb(fd):
            break
        if time.monotonic() >= deadline:
            raise SystemExit(
                f'[specify] Error: Could not acquire lock on {lock_file} (timeout after 5s)'
            )
        time.sleep(0.1)

    metadata = json.dumps({'pid': os.getpid(), 'created_at': time.time()}).encode('utf-8')
    os.ftruncate(fd, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    os.write(fd, metadata)

    if hierarchy_file.exists():
        data = yaml.safe_load(hierarchy_file.read_text(encoding='utf-8'))
        if data is None:
            data = {}
        if not isinstance(data, dict):
            raise SystemExit(
                f'[specify] Error: Existing hierarchy file has malformed YAML root: {hierarchy_file}'
            )
    else:
        data = {}

    data.setdefault('title', parent_title)
    data.setdefault('level', parent_level)
    data.setdefault('parent', None)
    data.setdefault('processed_at', None)
    children = data.get('children')
    if children is None:
        children = []
    elif not isinstance(children, list):
        raise SystemExit(
            f'[specify] Error: Existing hierarchy file has malformed children list: {hierarchy_file}'
        )

    for child in children:
        if isinstance(child, dict) and str(child.get('key', '')) == child_key:
            break
    else:
        children.append({'key': child_key, 'title': child_title, 'order': child_order})

    data['children'] = children

    tmp_fd, tmp_path = tempfile.mkstemp(dir=str(hierarchy_file.parent), suffix='.yml.tmp')
    try:
        try:
            f = os.fdopen(tmp_fd, 'w', encoding='utf-8')
        except Exception:
            os.close(tmp_fd)
            raise
        with f:
            yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        os.replace(tmp_path, str(hierarchy_file))
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
finally:
    os.close(fd)
" || return 1
}

# Update parent's hierarchy.yml to include a new child entry (with locking)
# Args:
#   $1 parent_dir    - Path to the parent spec directory
#   $2 child_key     - Issue key for the child (e.g., "200")
#   $3 child_title   - Title of the child issue
#   $4 parent_title  - (optional) Title for the parent when creating a missing hierarchy.yml
#   $5 parent_level  - (optional) Level for the parent when creating a missing hierarchy.yml (default: epic)
update_parent_hierarchy_yml() {
    local parent_dir="$1"
    local child_key="$2"
    local child_title="$3"
    local parent_title="${4:-}"   # Title to use when creating a missing parent hierarchy.yml
    local parent_level="${5:-epic}"  # Level to use when creating a missing parent hierarchy.yml

    local hierarchy_file="$parent_dir/hierarchy.yml"
    local lock_file="$parent_dir/.hierarchy.yml.lock"

    # Acquire lock (try flock first, then mkdir fallback)
    local lock_acquired=false
    local flock_available=false
    # Fixed file descriptor for flock (avoids 'exec {var}>>' which requires Bash 4.1+)
    local lock_fd=""
    local lock_owner_file="$lock_file/.owner"

    if command -v flock >/dev/null 2>&1; then
        flock_available=true
        # Check if lock path is a directory (left by mkdir fallback)
        if [ -d "$lock_file" ]; then
            # Wait for directory lock to be released (up to 5 seconds)
            local wait_start=$SECONDS
            while [ -d "$lock_file" ] && [ $((SECONDS - wait_start)) -lt 5 ]; do
                sleep 0.1
            done
            if [ -d "$lock_file" ]; then
                echo "[specify] Error: Could not acquire lock on $lock_file (directory lock held by another process, timeout after 5s)" >&2
                return 1
            fi
        fi
        # Use flock with 5-second timeout; FD 9 is a fixed descriptor (compatible with Bash 3.2+)
        exec 9>>"$lock_file"
        if flock -w 5 9 2>/dev/null; then
            lock_acquired=true
            lock_fd=9
        else
            exec 9>&- 2>/dev/null || true
            lock_fd=""
            echo "[specify] Error: Could not acquire flock on $lock_file (timeout after 5s)" >&2
            return 1
        fi
    fi

    if [ "$lock_acquired" = false ] && [ "$flock_available" = false ]; then
        if [ -e "$lock_file" ] && [ ! -d "$lock_file" ]; then
            if [ -L "$lock_file" ]; then
                echo "[specify] Error: Refusing to use symlinked lock path $lock_file" >&2
                return 1
            fi
            if [ ! -f "$lock_file" ]; then
                echo "[specify] Error: Unsupported lock path type at $lock_file" >&2
                return 1
            fi

            local dir_basename
            dir_basename="$(basename "$parent_dir")"
            local extracted_parent_key="${dir_basename%%-*}"
            local inferred_parent_title="${parent_title:-Issue ${extracted_parent_key}}"

            _update_parent_hierarchy_with_advisory_lock \
                "$lock_file" \
                "$hierarchy_file" \
                "$child_key" \
                "$child_title" \
                "$inferred_parent_title" \
                "${parent_level:-epic}" || return 1
            return 0
        fi

        # mkdir fallback
        local wait_start=$SECONDS
        while ! mkdir "$lock_file" 2>/dev/null; do
            if [ $((SECONDS - wait_start)) -ge 5 ]; then
                echo "[specify] Error: Could not acquire lock on $lock_file (timeout after 5s)" >&2
                return 1
            fi
            # If a native process has since created a persistent file lock, delegate to the
            # advisory-lock path rather than continuing to retry mkdir against a regular file.
            if [ -f "$lock_file" ] && [ ! -L "$lock_file" ]; then
                local _fallback_dir_basename
                _fallback_dir_basename="$(basename "$parent_dir")"
                local _fallback_parent_key="${_fallback_dir_basename%%-*}"
                _update_parent_hierarchy_with_advisory_lock \
                    "$lock_file" \
                    "$hierarchy_file" \
                    "$child_key" \
                    "$child_title" \
                    "${parent_title:-Issue ${_fallback_parent_key}}" \
                    "${parent_level:-epic}" || return 1
                return 0
            fi
            sleep 0.1
        done
        lock_acquired=true
        if ! printf '{"pid":%s,"created_at":%s}\n' "$$" "$(date +%s)" > "$lock_owner_file"; then
            rm -f "$lock_owner_file" 2>/dev/null || true
            rmdir "$lock_file" 2>/dev/null || true
            echo "[specify] Error: Could not record lock ownership in $lock_file" >&2
            return 1
        fi
        # Set up cleanup trap for mkdir-based lock
        trap "rm -f '$lock_owner_file' 2>/dev/null || true; rmdir '$lock_file' 2>/dev/null || true" EXIT INT TERM
    fi

    # Under lock: create or update hierarchy.yml
    if [ ! -f "$hierarchy_file" ]; then
        # Create a default parent hierarchy.yml using the provided title or fallback.
        # Extract parent key from directory basename (e.g., "100-epic-name" -> "100")
        local dir_basename
        dir_basename="$(basename "$parent_dir")"
        local extracted_parent_key="${dir_basename%%-*}"
        local inferred_parent_title="${parent_title:-Issue ${extracted_parent_key}}"
        create_hierarchy_yml "$parent_dir" "$inferred_parent_title" "${parent_level:-epic}" ""
    fi

    # Check if child already present (idempotency)
    if grep -q "key: '$child_key'" "$hierarchy_file" 2>/dev/null || \
       grep -q "key: \"$child_key\"" "$hierarchy_file" 2>/dev/null; then
        # Child already present, release lock and return
        if [ -n "$lock_fd" ]; then
            flock -u 9 2>/dev/null || true
            exec 9>&- 2>/dev/null || true
        else
            rm -f "$lock_owner_file" 2>/dev/null || true
            rmdir "$lock_file" 2>/dev/null || true
            trap - EXIT INT TERM
        fi
        return 0
    fi

    # Use Python to safely update YAML (avoiding yq dependency)
    # Pass values via environment variables to avoid shell injection
    local _yaml_update_ok=true
    _HIER_FILE="$hierarchy_file" _CHILD_KEY="$child_key" _CHILD_TITLE="$child_title" \
    python3 -c "
import os, sys, yaml
from pathlib import Path

hierarchy_file = Path(os.environ['_HIER_FILE'])
child_key = os.environ['_CHILD_KEY']
child_title = os.environ['_CHILD_TITLE']
child_order = int(child_key) if child_key.isdigit() else 0

data = yaml.safe_load(hierarchy_file.read_text(encoding='utf-8'))
if data is None:
    data = {}

if 'children' not in data or data['children'] is None:
    data['children'] = []

# Check idempotency again under lock
for child in data['children']:
    if isinstance(child, dict) and str(child.get('key', '')) == child_key:
        sys.exit(0)

data['children'].append({'key': child_key, 'title': child_title, 'order': child_order})

# Write atomically
import tempfile
tmp_fd, tmp_path = tempfile.mkstemp(dir=str(hierarchy_file.parent), suffix='.yml.tmp')
try:
    with os.fdopen(tmp_fd, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    os.replace(tmp_path, str(hierarchy_file))
except:
    os.unlink(tmp_path)
    raise
" || _yaml_update_ok=false

    if [ "$_yaml_update_ok" = false ]; then
        echo "[specify] Error: Failed to update $hierarchy_file" >&2
        # Release lock before returning
        if [ -n "$lock_fd" ]; then
            flock -u 9 2>/dev/null || true
            exec 9>&- 2>/dev/null || true
        else
            rm -f "$lock_owner_file" 2>/dev/null || true
            rmdir "$lock_file" 2>/dev/null || true
            trap - EXIT INT TERM
        fi
        return 1
    fi

    # Release lock
    if [ -n "$lock_fd" ]; then
        flock -u 9 2>/dev/null || true
        exec 9>&- 2>/dev/null || true
    else
        rm -f "$lock_owner_file" 2>/dev/null || true
        rmdir "$lock_file" 2>/dev/null || true
        trap - EXIT INT TERM
    fi
}

# Initialize hierarchy output variables
PARENT_SPEC_DIR="null"
HIERARCHY_LEVEL="null"

# Determine if we should attempt nested creation
NESTED_CREATION=false
RESOLVED_PARENT=""

if [ -n "$EXPLICIT_ISSUE" ] && [ "$FLAT_MODE" = false ]; then
    # Try to resolve repository for hierarchy detection
    REPO_SLUG=""
    REPO_SLUG=$(resolve_repo_slug) || true

    # Determine parent (explicit --parent or auto-detected)
    if [ -n "$PARENT_NUMBER" ]; then
        RESOLVED_PARENT="$PARENT_NUMBER"
        # Still invoke detector for level/title (but ignore parent result)
        invoke_hierarchy_detector "$ISSUE_NUMBER" "$REPO_SLUG" 2>/dev/null || true
        NESTED_CREATION=true
    else
        # Try hierarchy detection
        if invoke_hierarchy_detector "$ISSUE_NUMBER" "$REPO_SLUG" 2>/dev/null; then
            if [ -n "$DETECTED_PARENT" ]; then
                RESOLVED_PARENT="$DETECTED_PARENT"
                NESTED_CREATION=true
            fi
        else
            echo "[specify] Warning: Hierarchy detection failed; falling back to flat directory creation" >&2
        fi
    fi

    # Update HIERARCHY_LEVEL from detector results
    if [ -n "$DETECTED_LEVEL" ]; then
        HIERARCHY_LEVEL="$DETECTED_LEVEL"
    fi
fi

TEMPLATE="$REPO_ROOT/.specify/presets/agdt-templates/templates/spec-template.md"

if [ "$NESTED_CREATION" = true ] && [ -n "$RESOLVED_PARENT" ]; then
    # --- Nested directory creation ---

    # Detect the *parent* issue's own title and level for directory naming and
    # hierarchy.yml creation.  DETECTED_TITLE currently holds the child issue's
    # title from the earlier detection call, so we re-invoke the detector for the
    # parent issue number, save the results, then restore the child values.
    PARENT_DETECTED_TITLE=""
    PARENT_DETECTED_LEVEL="epic"
    if [ -n "$REPO_SLUG" ]; then
        _saved_child_title="$DETECTED_TITLE"
        _saved_child_level="$DETECTED_LEVEL"
        if ! invoke_hierarchy_detector "$RESOLVED_PARENT" "$REPO_SLUG" 2>/dev/null; then
            echo "[specify] Warning: Could not detect title for parent issue $RESOLVED_PARENT; using numeric key as directory name" >&2
        fi
        PARENT_DETECTED_TITLE="${DETECTED_TITLE:-}"
        PARENT_DETECTED_LEVEL="${DETECTED_LEVEL:-epic}"
        DETECTED_TITLE="$_saved_child_title"
        DETECTED_LEVEL="$_saved_child_level"
    fi

    # Find parent directory
    PARENT_DIR=""
    find_result=0
    PARENT_DIR=$(find_parent_dir "$SPECS_DIR" "$RESOLVED_PARENT") || find_result=$?

    if [ $find_result -eq 2 ]; then
        # Ambiguous match - exit
        exit 1
    fi

    if [ -z "$PARENT_DIR" ] || [ ! -d "$PARENT_DIR" ]; then
        # Parent dir doesn't exist - create it at top level with {key}-{slug}/ naming
        if [ -n "$PARENT_DETECTED_TITLE" ]; then
            parent_slug=$(clean_branch_name "$PARENT_DETECTED_TITLE")
            PARENT_DIR="$SPECS_DIR/${RESOLVED_PARENT}-${parent_slug}"
        else
            PARENT_DIR="$SPECS_DIR/${RESOLVED_PARENT}"
        fi
        mkdir -p "$PARENT_DIR"
        # Create parent spec.md
        if [ -f "$TEMPLATE" ]; then
            cp "$TEMPLATE" "$PARENT_DIR/spec.md"
        else
            touch "$PARENT_DIR/spec.md"
        fi
    fi

    # Check depth enforcement (max 3 levels)
    DEPTH=$(compute_nesting_depth "$SPECS_DIR" "$PARENT_DIR")
    if [ "$DEPTH" -ge 3 ]; then
        echo "[specify] Warning: Maximum nesting depth (3) would be exceeded; falling back to flat directory creation" >&2
        NESTED_CREATION=false
    fi
fi

if [ "$NESTED_CREATION" = true ] && [ -n "$RESOLVED_PARENT" ]; then
    # Create child directory with issue-key-only naming
    FEATURE_DIR="$PARENT_DIR/$FEATURE_NUM"
    mkdir -p "$FEATURE_DIR"

    # Create spec.md
    SPEC_FILE="$FEATURE_DIR/spec.md"
    if [ -f "$TEMPLATE" ]; then cp "$TEMPLATE" "$SPEC_FILE"; else touch "$SPEC_FILE"; fi

    # Create child hierarchy.yml
    CHILD_TITLE="${DETECTED_TITLE:-$FEATURE_DESCRIPTION}"
    CHILD_LEVEL="${DETECTED_LEVEL:-task}"
    create_hierarchy_yml "$FEATURE_DIR" "$CHILD_TITLE" "$CHILD_LEVEL" "$RESOLVED_PARENT"

    # Update parent hierarchy.yml
    update_parent_hierarchy_yml "$PARENT_DIR" "$FEATURE_NUM" "$CHILD_TITLE" "$PARENT_DETECTED_TITLE" "$PARENT_DETECTED_LEVEL"

    PARENT_SPEC_DIR="$PARENT_DIR"
else
    # --- Flat directory creation (original behavior) ---
    FEATURE_DIR="$SPECS_DIR/$BRANCH_NAME"
    mkdir -p "$FEATURE_DIR"

    SPEC_FILE="$FEATURE_DIR/spec.md"
    if [ -f "$TEMPLATE" ]; then cp "$TEMPLATE" "$SPEC_FILE"; else touch "$SPEC_FILE"; fi
fi

# Set the SPECIFY_FEATURE environment variable for the current session
export SPECIFY_FEATURE="$BRANCH_NAME"

if $JSON_MODE; then
    printf '{"BRANCH_NAME":"%s","SPEC_FILE":"%s","FEATURE_NUM":"%s","PARENT_SPEC_DIR":%s,"HIERARCHY_LEVEL":%s}\n' \
        "$BRANCH_NAME" "$SPEC_FILE" "$FEATURE_NUM" \
        "$(if [ "$PARENT_SPEC_DIR" = "null" ]; then echo 'null'; else printf '"%s"' "$PARENT_SPEC_DIR"; fi)" \
        "$(if [ "$HIERARCHY_LEVEL" = "null" ]; then echo 'null'; else printf '"%s"' "$HIERARCHY_LEVEL"; fi)"
else
    echo "BRANCH_NAME: $BRANCH_NAME"
    echo "SPEC_FILE: $SPEC_FILE"
    echo "FEATURE_NUM: $FEATURE_NUM"
    echo "PARENT_SPEC_DIR: $PARENT_SPEC_DIR"
    echo "HIERARCHY_LEVEL: $HIERARCHY_LEVEL"
    echo "SPECIFY_FEATURE environment variable set to: $BRANCH_NAME"
fi
