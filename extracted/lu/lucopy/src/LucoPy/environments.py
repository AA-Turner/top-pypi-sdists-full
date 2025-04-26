import json
import pyspark

def get_dbutils(spark):
    try:
        from pyspark.dbutils import DBUtils
        dbutils = DBUtils(spark)
    except ImportError:
        import IPython
        dbutils = IPython.get_ipython().user_ns["dbutils"]
    return dbutils

def get_databricks_run_env(spark):
    
    dbutils = get_dbutils(spark)

    context = json.loads(dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson())
    org_id = context['tags']['orgId']
    workspace_url = f'https://{spark.conf.get("spark.databricks.workspaceUrl")}'

    run_env = {
        'platform': 'Databricks',
        'workspaceUrl': workspace_url,
        'orgId': org_id,
    }

    try:
        job_id = context['tags']['jobId']
        job_name = context['tags']['jobName']
        run_id = context['tags']['multitaskParentRunId']

        run_env['referenceUrl'] = f'{workspace_url}/?o={org_id}#job/{job_id}/run/{run_id}'
        run_env['jobId'] = job_id
        run_env['jobName'] = job_name
        run_env['runId'] = run_id

        return run_env
    
    except KeyError:
        browser_hash = context['tags']['browserHash']
        
        run_env['referenceUrl'] = f'{workspace_url}/?o={org_id}{browser_hash}'

        return run_env