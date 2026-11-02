"""Deploying Airflow DAG code to an environment's DAG bucket with S3 keys.

``databaas dag deploy`` uploads the directory named by ``artifacts.dags`` in
``databaas.yml`` to the layout Airflow's ``DataBaasS3DagBundle`` reads:

    s3://<bucket>/dags/prod/<bundle>/
    s3://<bucket>/dags/dev/<slug>/<bundle>/

It authenticates with the environment's DAG deployment key from
``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY``, so it runs in CI without a
``databaas login``. Nothing here imports Airflow.
"""
