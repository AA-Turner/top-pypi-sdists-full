# ============================================================
# DATASOURCE CONSTANTS
# ============================================================

DS_NAME = "sdk_aws_ds"
DS_ID = 84902

# ============================================================
# ASSET CONSTANTS
# ============================================================

ASSET_UID = "sdk_snowflake_ds.SDK_DB.PUBLIC.CLIENTLIST_SOURCEAPP"

ASSET_TAG = "sdk_asset"

ASSET_UID_TABLE = "sdk_snowflake_ds.SDK_DB.POSITIONS"

# ============================================================
# PIPELINE CONSTANTS
# ============================================================

PIPELINE_UID = "torch.external.integration.demo-default"
PIPELINE_NAME = "SDK External Integration Pipeline - Default"

PIPELINE_UID_WITH_CONTINUATION_ID = "adoc.test.pipeline.sanity.continuation"
PIPELINE_NAME_WITH_CONTINUATION_ID = "ADOC Test Pipeline Sanity ContinuationId"

PIPELINE_UID_DELETION = "adoc_pipeline_to_delete"
PIPELINE_NAME_DELETION = "ETL Pipeline To Delete"

PIPELINE_UID_CONTINUATION = "adoc.test.pipeline.sanity.continuation"

PIPELINE_JOB_UID = "read_data_from_s3"

JOB_UID_READ = "customers.read"
JOB_UID_GENERATE = "customers.generate_sales"
JOB_UID_SALES = "aggregated_sales"

# ============================================================
# EXPLICIT TIME PIPELINE CONSTANTS
# ============================================================

EXPLICIT_PIPELINE_UID = "torch.external.integration.time-travel"
EXPLICIT_PIPELINE_NAME = "External Integration – Time Travel (Explicit Time)"

# ============================================================
# EXTERNAL INTEGRATION CONSTANTS
# ============================================================

S3_DS = "sdk_aws_ds"
SDK_SNOWFLAKE_DATA_SOURCE = "sdk_snowflake_ds"

S3_CUSTOMER = "customers_raw"
S3_SNOWFLAKE_CUSTOMERS = "SDK_DB.PUBLIC.TELCO_CUSTOMER_NETWORK_SCORE"
SNOWFLAKE_SERVICES = "SDK_DB.PUBLIC.TMOBILE_SERVICESBYCUSTOMER_V2"

# ============================================================
# POLICY CONSTANTS
# ============================================================

# -------------------------
# Freshness
# -------------------------

FRESHNESS_POLICY_NAME = (
    "SALES_PIPELINE_CLEAN-fresh-and-vol-policy-77428679"
)

# -------------------------
# Data Quality
# -------------------------

DQ_POLICY_NAME = "sdk_sko_full_dq_policy"

DQ_POLICY_BACKWARD_COMPATIBLE_NAME = "sdk_full_telecom_policy"
INCREMENTAL_DQ_POLICY_NAME = "sdk_erp_transactions_incremental"

INCREMENTAL_DQ_ID = "sdk_semistructured_dq_incremental_id"
INCREMENTAL_DQ_DATE_TIME="sdk_sales_pipeline_dq_date_incremental"
INCREMENTAL_DQ_DATE_TIME_ASSET_ID=77428679

FILE_EVENT_BASED_DQ_POLICY = "sdk_customers_json_file_event_based_dq"
FILE_EVENT_BASED_DQ_BACKING_ASSET_ID=77429408

KAFKA_DQ_POLICY_NAME = "sdk_kafka_timestamp_dq_policy"
KAFKA_DQ_POLICY_BACKING_ASSET_ID=77429436

# -------------------------
# Reconciliation
# -------------------------

RECON_POLICY_NAME = "sdk_sales_recon_policy"

SELECTIVE_RECON_POLICY_BACKWARD_COMPATIBLE_NAME = RECON_POLICY_NAME
INCREMENTAL_RECON_POLICY_NAME = "sdk_sales_incremental_date_recon_policy"
INCREMENTAL_DQ_RECON_TIME_ASSET_ID=77428678

FILE_EVENT_BASED_RECON_POLICY = "file_event_based_recon_policy"

KAFKA_RECON_POLICY_NAME = "sdk_kafka_timestamp_recon_policy"

FILE_BASED_ASSET_UID = "sdk_aws_ds.customers_raw"
KAFKA_ASSET_UID = "sdk_kafka.sdk_cust_sink_kafka"
TABLE_ASSET_UID = "sdk_snowflake_ds.SDK_DB.PUBLIC.CLINET_DEMOGRAPHIC"

# ============================================================
# CSV / DATA GENERATION
# ============================================================

CSV_SIZE = 30

# ============================================================
# RETRY SETTINGS
# ============================================================

RETRY_INTERVAL = 60
MAX_RETRIES = 0
