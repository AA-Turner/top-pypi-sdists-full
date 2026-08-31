"""Data-preparation utilities for building new geocif projects.

Each module is a standalone CLI (``python -m geocif.data_prep.<name>``) that
turns raw national statistics / boundary products into the exact artifacts the
geoprepare -> geocif pipeline consumes:

- ``build_mt_boundary``   : IBGE municipality mesh -> admin_2 boundary shapefile
                            (composite lowercase ADM2_NAME, IBGE code as num_ID)
- ``convert_tabela1612``  : IBGE SIDRA Tabela 1612 export -> hvstat-style wide
                            production-statistics CSV (yield t/ha, area ha,
                            production t; one row per municipality-year)
- ``validate_inputs``     : Gate-0 cross-checks between the two artifacts before
                            anything is uploaded to the cluster
"""
