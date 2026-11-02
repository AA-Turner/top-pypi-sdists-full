# Declarative manifest of the host DB artifacts this package needs — DATA ONLY.
# Imports nothing, names no host module paths (aidream/_generated/FEATURE.md).
#
# matrx-rag OWNS its rag-schema models — every rag table, the rerank cache and
# the embedding cache included — as package-generated classes (models_rag.py,
# plus the docproc/public subsets it reads, models_docproc.py / models.py),
# written by the host's `python db/generate.py` through the `output:` entries in
# aidream's db/matrx_orm.yaml. They register in matrx_orm.model_registry on
# import and resolve through matrx_rag._ext.get_db_model(name); the host binds
# the pool with matrx_rag.configure(db_config_name=...). So there is nothing to
# resolve from the host inventory: declaring rag tables here would make the
# wiring generator inject the package's own classes back through the
# configure(db_models=...) override seam, which exists only for a host whose
# database genuinely differs. Same shape as matrx-seo / matrx-files.
DB_REQUIREMENTS = {
    "target": {
        "configure_import": "matrx_rag",
        "configure_call": "configure",
        "models_kwarg": None,
    },
    "schemas": [],
}
