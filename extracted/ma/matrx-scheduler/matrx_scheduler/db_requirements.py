# File: matrx_scheduler/db_requirements.py
# Declarative manifest of the host DB artifacts matrx-scheduler needs. Data
# only — imports nothing, names no host module paths. Consumed by matrx-orm's
# package_wiring generator (python db/generate.py or
# scripts/check_package_wiring.py --write), which resolves every table
# against the host's freshly-generated inventory (db/helpers/auto_config_*.py)
# and emits the aidream-side wiring module that calls
# matrx_scheduler.configure_db(...).
#
# The `scheduler` schema holds exactly the sch_* tables this package already
# has hand-written Pydantic mirrors for (matrx_scheduler.models); the rule
# form below picks up all four with their natural Pascal names — no
# aliasing needed (SchTask/SchAgentTask/SchTrigger/SchRun match 1:1).
#
# Consumed by: matrx_scheduler/_ext.py::get_db_model(name) — the injection
# accessor used by matrx_scheduler.api.user_queries for RLS-scoped per-user
# access via matrx_orm.rls_session (see that module's docstring).

DB_REQUIREMENTS = {
    "target": {
        "configure_import": "matrx_scheduler",
        "configure_call": "configure_db",
        "models_kwarg": "models",
    },
    "schemas": ["scheduler"],
}
