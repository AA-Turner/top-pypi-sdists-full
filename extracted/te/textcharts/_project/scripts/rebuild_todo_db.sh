#!/usr/bin/env bash
# Deterministically (re)build the project-isolated todo-db tracker database from
# the retained legacy YAML corpus, LOSSLESSLY.
#
# The tracker database (.todo-db/standalone.sqlite) is git-ignored (databases are
# never committed). The committed sources of truth for a rebuild are:
#   1. the retained legacy YAML under _project/{TODO,DONE}  (rollback snapshot)
#   2. _project/scripts/todo_migrate_transform.py           (zero-loss transform)
#
# The transform folds every legacy field the todo-db schema does not model
# (tags, estimated_effort, owners, impact, files_affected, success_metrics,
# context_sections, open_questions, sections, last_updated, moved_from) verbatim
# into each item's description, so nothing is lost. Modeled fields import via the
# tool's supported import-yaml path.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

TODO_DB_HOME="${TODO_DB_HOME:-/Users/joe/Developer/todo-db}"
DB="${TODO_DB_PATH:-$PROJECT_DIR/.todo-db/standalone.sqlite}"
PROJECT_ID="${TODO_DB_PROJECT_ID:-textcharts}"
REPOSITORY="${TODO_DB_REPOSITORY:-https://github.com/joeharris76/textcharts.git}"
# Export identity so every todo-db invocation (which opens the DB with the
# TODO_DB_PROJECT_ID/TODO_DB_REPOSITORY identity) is pinned to this project.
export TODO_DB_PROJECT_ID="$PROJECT_ID"
export TODO_DB_REPOSITORY="$REPOSITORY"

TDB() { uv run --project "$TODO_DB_HOME" --extra legacy --extra audit todo-db "$@"; }

if [[ -f "$DB" ]]; then
  echo "rebuild: $DB already exists; refusing to overwrite. Remove it first to rebuild." >&2
  exit 2
fi

WORK="$(mktemp -d "${TMPDIR:-/tmp}/textcharts-todo-db.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

echo "rebuild: transforming retained YAML (zero-loss) -> $WORK"
uv run --project "$TODO_DB_HOME" python "$SCRIPT_DIR/todo_migrate_transform.py" \
  "$PROJECT_DIR/_project/TODO" "$PROJECT_DIR/_project/DONE" "$WORK"

echo "rebuild: initializing $DB with identity $PROJECT_ID"
mkdir -p "$(dirname "$DB")"
TDB --db "$DB" init --project-id "$PROJECT_ID" --repository "$REPOSITORY"

echo "rebuild: importing transformed corpus"
TDB --db "$DB" import-yaml --todo-dir "$WORK/TODO" --done-dir "$WORK/DONE" \
  --project-id "$PROJECT_ID" --repository "$REPOSITORY"

echo "rebuild: verifying zero-loss retention + audit chain"
TDB --db "$DB" export --output "$WORK/export.json"
uv run --project "$TODO_DB_HOME" python "$SCRIPT_DIR/todo_zero_loss_check.py" \
  "$WORK/export.json" "$WORK/residuals.json" \
  "$PROJECT_DIR/_project/TODO" "$PROJECT_DIR/_project/DONE"
uv run --project "$TODO_DB_HOME" python "$SCRIPT_DIR/todo_parity_check.py" \
  "$WORK/export.json" "$PROJECT_DIR/_project/TODO" "$PROJECT_DIR/_project/DONE" >/dev/null
TDB --db "$DB" audit verify
echo "rebuild: done -> $DB"
