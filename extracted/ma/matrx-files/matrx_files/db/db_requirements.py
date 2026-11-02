# Declarative manifest of the host DB artifacts this package needs — DATA ONLY.
# Imports nothing, names no host module paths. Consumed by matrx-orm's
# package_wiring generator in the host (python db/generate.py), which resolves
# every schema/table against the host inventory and emits the host-side wiring
# module that calls this package's configure_db(...).
#
# INDEPENDENCE.md law #3: this manifest covers HOST mode. STANDALONE mode uses
# the package's own generated models (db/models.py) + migrations (db/migrations/)
# against the same schema — the two must describe the SAME structure.

DB_REQUIREMENTS = {
    "target": {
        "configure_import": "matrx_files",
        "configure_call": "configure_db",
        "models_kwarg": "models",
    },
    "schemas": [],  # e.g. ["files"]
}
