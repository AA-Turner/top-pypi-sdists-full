#!/usr/bin/env bash
# E2E test runner for airflow-mcd / YET-792
#
# Spins up Airflow 2 + Airflow 3 in Docker, triggers a test DAG on each,
# waits for the Monte Carlo callbacks to arrive at the mock server, then
# verifies that:
#   - Airflow 2 sends a version string that _is_airflow_3() evaluates to False
#     → expected DAG run URL uses the old /dags/{dag_id}/graph?run_id= format
#   - Airflow 3 sends a version string that _is_airflow_3() evaluates to True
#     → expected DAG run URL uses the new /dags/{dag_id}/runs/{run_id} format
#
# Prerequisites: docker, docker compose (v2), curl, python3
#
# Usage:
#   cd scripts/e2e
#   ./run_e2e.sh
#
# Options:
#   --no-build   Skip image rebuild (useful when images already exist)
#   --keep-up    Leave containers running after the test (for debugging)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ---- colours ----------------------------------------------------------------
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BOLD='\033[1m'; NC='\033[0m'
info()  { echo -e "${YELLOW}[e2e]${NC} $*"; }
pass()  { echo -e "${GREEN}[PASS]${NC} $*"; }
fail()  { echo -e "${RED}[FAIL]${NC} $*"; exit 1; }
header(){ echo -e "\n${BOLD}$*${NC}"; }

# ---- options ----------------------------------------------------------------
BUILD_FLAG="--build"
KEEP_UP=false
for arg in "$@"; do
  case "$arg" in
    --no-build) BUILD_FLAG="" ;;
    --keep-up)  KEEP_UP=true ;;
  esac
done

# ---- cleanup on exit --------------------------------------------------------
cleanup() {
  if [ "$KEEP_UP" = false ]; then
    info "Stopping containers..."
    docker compose down -v --remove-orphans 2>/dev/null || true
  else
    info "--keep-up: leaving containers running."
  fi
}
trap cleanup EXIT

# ---- helpers ----------------------------------------------------------------

wait_for_url() {
  local url="$1" label="$2" max="${3:-60}" interval="${4:-5}"
  info "Waiting for $label ($url)..."
  local n=0
  while ! curl -sf "$url" >/dev/null 2>&1; do
    n=$((n + interval))
    if [ $n -ge $((max * interval)) ]; then
      fail "$label did not become reachable within $((max * interval))s"
    fi
    sleep "$interval"
  done
  info "$label is up."
}

wait_for_scheduler() {
  local service="$1" max_attempts="${2:-40}"
  info "Waiting for $service scheduler to be healthy..."
  local n=0
  while [ $n -lt "$max_attempts" ]; do
    if docker compose exec -T "$service" \
        airflow jobs check --job-type SchedulerJob 2>/dev/null; then
      info "$service scheduler is healthy."
      return 0
    fi
    n=$((n + 1))
    sleep 10
  done
  fail "$service scheduler did not become healthy after $((max_attempts * 10))s"
}

wait_for_dag() {
  local service="$1" dag_id="$2" max_attempts="${3:-24}"
  info "Waiting for $dag_id to be loaded on $service..."
  local n=0
  while [ $n -lt "$max_attempts" ]; do
    if docker compose exec -T "$service" airflow dags show "$dag_id" >/dev/null 2>&1; then
      info "$dag_id is loaded on $service."
      return 0
    fi
    n=$((n + 1))
    sleep 5
  done
  fail "$dag_id not found on $service after $((max_attempts * 5))s — check scheduler logs."
}

trigger_dag() {
  local service="$1" dag_id="$2"
  wait_for_dag "$service" "$dag_id"
  info "Unpausing and triggering $dag_id on $service..."
  docker compose exec -T "$service" airflow dags unpause "$dag_id" 2>/dev/null || true
  docker compose exec -T "$service" airflow dags trigger "$dag_id" 2>/dev/null
}

wait_for_callbacks() {
  local expected_count="$1" max_wait="${2:-120}"
  info "Waiting up to ${max_wait}s for callbacks from $expected_count distinct Airflow version(s)..."
  local elapsed=0
  while [ "$elapsed" -lt "$max_wait" ]; do
    local count
    # Count distinct Airflow major versions that have sent any dag-result or task-result callback.
    # Airflow 3.0 has an upstream bug where dag-level callbacks receive an empty context and
    # never fire; task-result callbacks carry the same env/version payload and are sufficient.
    count=$(curl -sf http://localhost:8080/callbacks \
      | python3 -c "
import json,sys
cbs = json.load(sys.stdin)
versions = set()
for c in cbs:
    if c.get('operation') in ('upload_airflow_dag_result', 'upload_airflow_task_result'):
        v = (c.get('env') or {}).get('version')
        if v:
            versions.add(v.split('.')[0])
print(len(versions))
" 2>/dev/null || echo 0)
    if [ "$count" -ge "$expected_count" ]; then
      info "Got callbacks from $count distinct Airflow version(s) — proceeding to verification."
      return 0
    fi
    sleep 5
    elapsed=$((elapsed + 5))
  done
  info "Timed out — proceeding with whatever was captured (may fail verification)."
}

# ---- main -------------------------------------------------------------------

header "=== airflow-mcd e2e: DAG run URL verification ==="

# 1. Start the stack
info "Starting Docker Compose stack..."
docker compose up $BUILD_FLAG -d

# 2. Wait for the mock server
wait_for_url "http://localhost:8080/health" "mock-server" 20 3

# 3. Wait for both schedulers
wait_for_scheduler airflow2
wait_for_scheduler airflow3

# 4. Reset callback state (safety net for --keep-up re-runs)
info "Resetting mock-server callback state..."
curl -sf -X DELETE http://localhost:8080/callbacks >/dev/null

# 5. Trigger DAG runs
trigger_dag airflow2 e2e_test_dag
trigger_dag airflow3 e2e_test_dag

# 6. Poll for callbacks (2 DAG-result callbacks: one per Airflow version)
wait_for_callbacks 2 120

# 7. Show raw captured callbacks
header "--- Captured callbacks ---"
curl -sf http://localhost:8080/callbacks | python3 -m json.tool

# 8. Run verification
header "--- Verification ---"
VERIFY_JSON=$(curl -sf http://localhost:8080/verify)
echo "$VERIFY_JSON" | python3 -m json.tool

PASSED=$(echo "$VERIFY_JSON" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print('true' if d.get('passed') else 'false')
")

header "--- Result ---"
if [ "$PASSED" = "true" ]; then
  pass "All e2e checks passed!"
  echo
  echo "$VERIFY_JSON" | python3 -c "
import json, sys
d = json.load(sys.stdin)
for r in d.get('results', []):
    print(f\"  version={r['version_received']:12s}  is_airflow_3={str(r['is_airflow_3']):5s}  url_path={r['expected_dag_run_url_path']}\")
"
else
  fail "e2e verification FAILED — see output above for details."
fi
