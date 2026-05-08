#!/usr/bin/env bash
# Minimal Airflow startup for e2e testing.
# Runs inside the Airflow container; postgres is already healthy when this starts
# (docker-compose depends_on: condition: service_healthy).
set -e

log() { echo "[airflow-entrypoint] $*" >&2; }

log "Initialising database..."
# db migrate works in Airflow 2.7+ and 3.x; fall back to db init for older 2.x
airflow db migrate 2>/dev/null || airflow db init

log "Creating Monte Carlo callback connection (GQL path via mock server)..."
# Use conn-type 'http' — not 'mcd-gateway' — so pycarlo takes the GraphQL path
# (session_scope is None → _upload_result_gql).  The mock server handles the POST.
airflow connections delete mcd_gateway_default_session 2>/dev/null || true
airflow connections add mcd_gateway_default_session \
    --conn-type http \
    --conn-login  "fake-mcd-id" \
    --conn-password "fake-mcd-token" \
    --conn-host   "http://mock-server:8080"

# Airflow 3 uses DAG bundles; pre-seed the bundle so the scheduler picks up
# DAGs immediately rather than waiting for the first bundle sync cycle.
log "Seeding DAG bundle (noop on Airflow 2)..."
airflow dags reserialize 2>/dev/null || true

log "Starting scheduler in background..."
airflow scheduler &

# Airflow 3 moved DAG callback execution out of the scheduler and into the
# dag-processor.  Without it, on_success_callback / on_failure_callback on
# DAGs are written to the DB but never consumed.  Airflow 2 has no such command.
if airflow dag-processor --help >/dev/null 2>&1; then
    log "Starting dag-processor in background (Airflow 3)..."
    airflow dag-processor &
fi

# Give scheduler (and dag-processor) a moment to register before the webserver.
sleep 3

log "Starting webserver on :8080..."
# Airflow 3 renamed `airflow webserver` to `airflow api-server`.
# exec replaces this shell so signals propagate correctly.
if airflow api-server --help >/dev/null 2>&1; then
    exec airflow api-server --port 8080
else
    exec airflow webserver --port 8080
fi
