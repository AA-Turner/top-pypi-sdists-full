#!/usr/bin/env bash
# bootstrap_test_db.sh — build the workflow.* schema on a scratch Postgres
# so packages/matrx-graph/tests/test_postgres_checkpointer.py and
# test_node_data_slot_store.py can run.
#
# Usage:
#   WF_TEST_DB_URL=postgresql://postgres:postgres@127.0.0.1:55432/wf_test \
#       packages/matrx-graph/tests/ci/bootstrap_test_db.sh
#
# This exercises the FRESH-INSTALL path exactly as documented in
# matrx_graph/db/migrations/README.md:
#   1. 00_supabase_shim.sql          — roles / auth schema / platform.visibility
#                                      (what Supabase provides out of the box)
#   2. 0100_baseline_post_reorg.sql  — the complete post-reorg schema, one file
#   3. upgrade convergence probe     — remove current columns / restore the old
#                                      enum label, then prove 0102 repairs both
#   4. idempotency drift guard       — replay standalone incrementals on the baseline;
#                                      they are folded into 0100 and MUST no-op
#                                      cleanly (a failure here means 0100 and
#                                      the incrementals have drifted apart)
#   5. sanity check                  — scream if anything is missing
#
# (The old flow — legacy 0001-0019 + 10_canonical_reorg_shim.sql — is retired;
# the shim file is kept, deprecated, as documentation of the 2026 reorg.)
set -euo pipefail

: "${WF_TEST_DB_URL:?Set WF_TEST_DB_URL to the scratch Postgres URL (never production!)}"

case "$WF_TEST_DB_URL" in
    *brsgrqvjdzwihsvnfqkf*|*txzxabzwovsujtloxrus*|*supabase.co*|*supabase.com*)
        echo "::error::WF_TEST_DB_URL looks like a Supabase/production URL — refusing to bootstrap." >&2
        exit 1
        ;;
esac

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MIGRATIONS="$HERE/../../matrx_graph/db/migrations"

run_sql() {
    echo "--> $(basename "$1")"
    psql "$WF_TEST_DB_URL" -v ON_ERROR_STOP=1 -q -f "$1"
}

echo "==> [1/5] Supabase shim"
run_sql "$HERE/00_supabase_shim.sql"

echo "==> [2/5] post-reorg baseline (the fresh-install path: 0100, nothing else)"
run_sql "$MIGRATIONS/0100_baseline_post_reorg.sql"

# The incrementals are folded into 0100 but stay in the directory (already recorded
# in the shared migration ledger for Matrx Main). Replaying them here proves
# they no-op cleanly on the baseline — the drift guard that fires if a future
# edit to 0100 or to an incremental breaks the fold-plus-replay equivalence.
# Append every new workflow.*-targeting migration here AND fold it into 0100.
POST_REORG_MIGRATIONS=(
    "0020_wf_run_announce.sql"
    "0021_join_semantics.sql"
    "0022_node_data_slot.sql"
    "0023_fanout_identity.sql"
    "0024_definition_variables.sql"
    "0101_run_request_attribution.sql"
    "0102_visibility_and_kind_verdicts.sql"
    "0103_work_item.sql"
    "0105_plan.sql"
    "0106_definition_visibility_internal_default.sql"
    "0107_plan_anchor_integrity.sql"
    "0108_plan_persistence_invariants.sql"
    "0109_node_data_slot_created_by.sql"
    "0113_definition_published_to_web_and_shown_to.sql"
    "0116_standalone_checkpoint_organization_and_values.sql"
    "0119_step_result.sql"
)

echo "==> [3/5] existing-install convergence probe (0102)"
psql "$WF_TEST_DB_URL" -v ON_ERROR_STOP=1 -q <<'SQL'
ALTER TABLE workflow.node_outcome
    DROP COLUMN output_kind_ok,
    DROP COLUMN output_kind_errors,
    DROP COLUMN output_kind_version,
    DROP COLUMN output_kind_degraded;
ALTER TYPE platform.visibility RENAME VALUE 'personal' TO 'private';
SQL
run_sql "$MIGRATIONS/0102_visibility_and_kind_verdicts.sql"

echo "==> [4/5] idempotency drift guard (all incrementals must no-op on the baseline)"
for base in "${POST_REORG_MIGRATIONS[@]}"; do
    run_sql "$MIGRATIONS/$base"
done

echo "==> [4a/5] node_data_slot legacy-owner convergence probe"
psql "$WF_TEST_DB_URL" -v ON_ERROR_STOP=1 -q <<'SQL'
DROP POLICY wf_node_data_slot_owner_select ON workflow.node_data_slot;
DROP POLICY wf_node_data_slot_owner_insert ON workflow.node_data_slot;
DROP POLICY wf_node_data_slot_owner_update ON workflow.node_data_slot;
DROP POLICY wf_node_data_slot_owner_delete ON workflow.node_data_slot;
ALTER TABLE workflow.node_data_slot RENAME COLUMN created_by TO user_id;

INSERT INTO auth.users (id)
VALUES ('87a6e699-3622-4869-8843-d0867456c0dd')
ON CONFLICT (id) DO NOTHING;
INSERT INTO workflow.definition (id, name, created_by)
VALUES (
    '20000000-0000-0000-0000-000000000009',
    'node data slot owner migration probe',
    '87a6e699-3622-4869-8843-d0867456c0dd'
);
INSERT INTO workflow.node_data_slot (
    definition_id, node_id, slot, value, source, captured_at, user_id
) VALUES (
    '20000000-0000-0000-0000-000000000009', 'probe', 'declared_sample',
    '{"owner":"legacy"}'::jsonb, 'declared', now(),
    '87a6e699-3622-4869-8843-d0867456c0dd'
);
SQL
run_sql "$MIGRATIONS/0109_node_data_slot_created_by.sql"
psql "$WF_TEST_DB_URL" -v ON_ERROR_STOP=1 -q <<'SQL'
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM workflow.node_data_slot
        WHERE definition_id = '20000000-0000-0000-0000-000000000009'
          AND created_by = '87a6e699-3622-4869-8843-d0867456c0dd'
    ) THEN
        RAISE EXCEPTION '0109 failed to preserve legacy node_data_slot ownership';
    END IF;
END
$$;
DELETE FROM workflow.definition
WHERE id = '20000000-0000-0000-0000-000000000009';
SQL

echo "==> [4b/5] plan persistence behavior probe"
psql "$WF_TEST_DB_URL" -v ON_ERROR_STOP=1 -q <<'SQL'
BEGIN;

INSERT INTO workflow.definition (id, name, created_by)
VALUES (
    '20000000-0000-0000-0000-000000000001',
    'plan persistence invariant probe',
    '87a6e699-3622-4869-8843-d0867456c0dd'
);
INSERT INTO workflow.plan (
    id, user_id, organization_id, definition_id, node_id, name
) VALUES (
    '20000000-0000-0000-0000-000000000002',
    '87a6e699-3622-4869-8843-d0867456c0dd',
    '20000000-0000-0000-0000-000000000003',
    '20000000-0000-0000-0000-000000000001',
    'probe-node',
    'before'
);

UPDATE workflow.plan
SET name = 'after', updated_at = '2000-01-01T00:00:00Z', version = 99
WHERE id = '20000000-0000-0000-0000-000000000002';

DO $$
DECLARE
    plan_version integer;
    plan_updated_at timestamptz;
BEGIN
    SELECT version, updated_at INTO plan_version, plan_updated_at
    FROM workflow.plan
    WHERE id = '20000000-0000-0000-0000-000000000002';
    IF plan_version <> 2 THEN
        RAISE EXCEPTION 'plan touch must advance exactly once; got version %', plan_version;
    END IF;
    IF plan_updated_at <= '2000-01-01T00:00:00Z'::timestamptz THEN
        RAISE EXCEPTION 'plan touch did not advance updated_at';
    END IF;
END
$$;

INSERT INTO workflow.plan_sample (
    id, plan_id, direction, scenario, is_stand_in
) VALUES (
    '20000000-0000-0000-0000-000000000004',
    '20000000-0000-0000-0000-000000000002',
    'output',
    'first',
    TRUE
);
INSERT INTO workflow.plan_sample (
    id, plan_id, direction, scenario, is_stand_in
) VALUES (
    '20000000-0000-0000-0000-000000000005',
    '20000000-0000-0000-0000-000000000002',
    'output',
    'second',
    FALSE
);

UPDATE workflow.plan_sample
SET data = '{"changed":true}'::jsonb, updated_at = '2000-01-01T00:00:00Z'
WHERE id = '20000000-0000-0000-0000-000000000005';

DO $$
DECLARE
    sample_updated_at timestamptz;
BEGIN
    SELECT updated_at INTO sample_updated_at
    FROM workflow.plan_sample
    WHERE id = '20000000-0000-0000-0000-000000000005';
    IF sample_updated_at <= '2000-01-01T00:00:00Z'::timestamptz THEN
        RAISE EXCEPTION 'plan sample touch did not advance updated_at';
    END IF;

    BEGIN
        UPDATE workflow.plan_sample
        SET is_stand_in = TRUE
        WHERE id = '20000000-0000-0000-0000-000000000005';
        RAISE EXCEPTION 'second output stand-in was accepted';
    EXCEPTION WHEN unique_violation THEN
        NULL;
    END;
END
$$;

INSERT INTO workflow.plan_event (id, plan_id, kind)
VALUES (
    '20000000-0000-0000-0000-000000000006',
    '20000000-0000-0000-0000-000000000002',
    'probe'
);

DO $$
BEGIN
    BEGIN
        UPDATE workflow.plan_event
        SET kind = 'rewritten'
        WHERE id = '20000000-0000-0000-0000-000000000006';
        RAISE EXCEPTION 'plan event update was accepted';
    EXCEPTION WHEN SQLSTATE '55000' THEN
        NULL;
    END;

    BEGIN
        DELETE FROM workflow.plan_event
        WHERE id = '20000000-0000-0000-0000-000000000006';
        RAISE EXCEPTION 'plan event delete was accepted';
    EXCEPTION WHEN SQLSTATE '55000' THEN
        NULL;
    END;
END
$$;

ROLLBACK;
SQL

echo "==> [5/5] sanity check"
psql "$WF_TEST_DB_URL" -v ON_ERROR_STOP=1 -q <<'SQL'
DO $$
DECLARE
    tbl TEXT;
    missing TEXT := '';
BEGIN
    FOREACH tbl IN ARRAY ARRAY[
        'workflow.definition', 'workflow.definition_version', 'workflow.run',
        'workflow.checkpoint', 'workflow.node_outcome', 'workflow.node_events',
        'workflow.job', 'workflow.trigger', 'workflow.trigger_fire',
        'workflow.idempotency', 'workflow.recovery_audit', 'workflow.template',
        'workflow.node_data_slot', 'workflow.worker_heartbeat',
        'workflow.work_item', 'workflow.plan', 'workflow.plan_sample',
        'workflow.plan_event'
    ]
    LOOP
        IF to_regclass(tbl) IS NULL THEN
            missing := missing || ' ' || tbl;
        END IF;
    END LOOP;
    IF missing <> '' THEN
        RAISE EXCEPTION 'bootstrap_test_db: missing tables:%', missing;
    END IF;

    IF to_regclass('workflow.wf_plan_definition_node_unique') IS NULL THEN
        RAISE EXCEPTION 'bootstrap_test_db: workflow plan anchor uniqueness missing';
    END IF;

    IF to_regclass('workflow.wf_plan_one_output_stand_in') IS NULL THEN
        RAISE EXCEPTION 'bootstrap_test_db: one-output-stand-in uniqueness missing';
    END IF;

    IF to_regprocedure('workflow.plan_touch_row()') IS NULL THEN
        RAISE EXCEPTION 'bootstrap_test_db: standalone plan touch function missing';
    END IF;

    IF to_regprocedure('workflow.reject_plan_event_mutation()') IS NULL THEN
        RAISE EXCEPTION 'bootstrap_test_db: append-only plan event guard missing';
    END IF;

    IF NOT EXISTS (
        SELECT FROM information_schema.columns
        WHERE table_schema = 'workflow' AND table_name = 'node_data_slot'
          AND column_name = 'created_by' AND is_nullable = 'NO'
    ) OR EXISTS (
        SELECT FROM information_schema.columns
        WHERE table_schema = 'workflow' AND table_name = 'node_data_slot'
          AND column_name = 'user_id'
    ) THEN
        RAISE EXCEPTION 'bootstrap_test_db: node_data_slot owner-column convergence missing';
    END IF;

    IF NOT EXISTS (
        SELECT FROM information_schema.columns
        WHERE table_schema = 'workflow' AND table_name = 'run'
          AND column_name = 'created_by'
    ) THEN
        RAISE EXCEPTION 'bootstrap_test_db: workflow.run.created_by missing (baseline did not apply)';
    END IF;

    -- TriggerStore reads/writes created_by on workflow.trigger — the old
    -- reorg shim missed this rename; the baseline must never regress it.
    IF NOT EXISTS (
        SELECT FROM information_schema.columns
        WHERE table_schema = 'workflow' AND table_name = 'trigger'
          AND column_name = 'created_by'
    ) THEN
        RAISE EXCEPTION 'bootstrap_test_db: workflow.trigger.created_by missing (TriggerStore targets it)';
    END IF;

    IF NOT EXISTS (
        SELECT FROM auth.users
        WHERE id = '87a6e699-3622-4869-8843-d0867456c0dd'
    ) THEN
        RAISE EXCEPTION 'bootstrap_test_db: default TEST_USER_ID row missing from auth.users';
    END IF;

    IF to_regprocedure('workflow.run_announce_fn()') IS NULL THEN
        RAISE EXCEPTION 'bootstrap_test_db: workflow.run_announce_fn() missing (0020 content)';
    END IF;

    IF NOT EXISTS (
        SELECT FROM information_schema.columns
        WHERE table_schema = 'workflow' AND table_name = 'checkpoint'
          AND column_name = 'pending_bindings'
    ) THEN
        RAISE EXCEPTION 'bootstrap_test_db: workflow.checkpoint.pending_bindings missing (0021 content)';
    END IF;

    -- 0021 also DROPPED pending_writes — the baseline must not resurrect it.
    IF EXISTS (
        SELECT FROM information_schema.columns
        WHERE table_schema = 'workflow' AND table_name = 'checkpoint'
          AND column_name = 'pending_writes'
    ) THEN
        RAISE EXCEPTION 'bootstrap_test_db: workflow.checkpoint.pending_writes present (0021 dropped it; baseline drifted)';
    END IF;

    IF NOT EXISTS (
        SELECT FROM information_schema.columns
        WHERE table_schema = 'workflow' AND table_name = 'node_outcome'
          AND column_name = 'dispatch_id'
    ) THEN
        RAISE EXCEPTION 'bootstrap_test_db: workflow.node_outcome.dispatch_id missing (0023 content)';
    END IF;

    -- The 6-part correlation key is the idempotency guarantee (0023).
    IF NOT EXISTS (
        SELECT FROM pg_constraint
        WHERE conname = 'wf_node_outcome_correlation_key'
          AND conrelid = 'workflow.node_outcome'::regclass
    ) THEN
        RAISE EXCEPTION 'bootstrap_test_db: wf_node_outcome_correlation_key constraint missing (0023 content)';
    END IF;

    IF NOT EXISTS (
        SELECT FROM information_schema.columns
        WHERE table_schema = 'workflow' AND table_name = 'node_outcome'
          AND column_name = 'output_kind'
    ) THEN
        RAISE EXCEPTION 'bootstrap_test_db: workflow.node_outcome.output_kind missing (checkpointer stamps it on every row)';
    END IF;

    IF (
        SELECT count(*)
        FROM information_schema.columns
        WHERE table_schema = 'workflow'
          AND table_name = 'node_outcome'
          AND column_name IN (
              'output_kind_ok', 'output_kind_errors',
              'output_kind_version', 'output_kind_degraded'
          )
    ) <> 4 THEN
        RAISE EXCEPTION 'bootstrap_test_db: workflow.node_outcome versioned kind-verdict columns missing';
    END IF;

    IF NOT EXISTS (
        SELECT FROM information_schema.columns
        WHERE table_schema = 'workflow' AND table_name = 'run'
          AND column_name = 'conversation_id' AND data_type = 'uuid'
    ) THEN
        RAISE EXCEPTION 'bootstrap_test_db: workflow.run.conversation_id is not canonical UUID';
    END IF;

    IF NOT EXISTS (
        SELECT FROM information_schema.columns
        WHERE table_schema = 'workflow' AND table_name = 'run'
          AND column_name = 'request_attribution_complete'
    ) THEN
        RAISE EXCEPTION 'bootstrap_test_db: workflow.run.request_attribution_complete missing';
    END IF;

    IF NOT EXISTS (
        SELECT FROM information_schema.columns
        WHERE table_schema = 'workflow'
          AND table_name = 'definition_version'
          AND column_name = 'variables'
          AND is_nullable = 'NO'
          AND column_default = '''[]''::jsonb'
    ) THEN
        RAISE EXCEPTION 'bootstrap_test_db: workflow.definition_version.variables must be NOT NULL DEFAULT []';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM pg_enum e
        JOIN pg_type t ON t.oid = e.enumtypid
        JOIN pg_namespace n ON n.oid = t.typnamespace
        WHERE n.nspname = 'platform'
          AND t.typname = 'visibility'
          AND e.enumlabel = 'private'
    ) OR NOT EXISTS (
        SELECT 1
        FROM pg_enum e
        JOIN pg_type t ON t.oid = e.enumtypid
        JOIN pg_namespace n ON n.oid = t.typnamespace
        WHERE n.nspname = 'platform'
          AND t.typname = 'visibility'
          AND e.enumlabel = 'personal'
    ) THEN
        RAISE EXCEPTION 'bootstrap_test_db: platform.visibility private→personal upgrade did not converge';
    END IF;
END
$$;
SQL

echo "==> bootstrap complete: workflow.* schema ready (fresh-install path: 0100 + drift guard)"
