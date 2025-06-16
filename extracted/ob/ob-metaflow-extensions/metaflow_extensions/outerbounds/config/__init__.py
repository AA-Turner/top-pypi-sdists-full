from metaflow.metaflow_config import from_conf

DEFAULT_AWS_CLIENT_PROVIDER = "obp"

DEFAULT_AZURE_CLIENT_PROVIDER = "obp"

DEFAULT_GCP_CLIENT_PROVIDER = "obp"


###
# On Demand Docker image build configuration
###
# Image builder service url
FAST_BAKERY_URL = from_conf("FAST_BAKERY_URL", None)


###
# NVCF configuration
###
# Maximum number of consecutive heartbeats that can be missed.
NVIDIA_HEARTBEAT_THRESHOLD = from_conf("NVIDIA_HEARTBEAT_THRESHOLD", "3")


###
# Snowpark configuration
###
# Snowflake account to use with the @snowpark decorator
SNOWPARK_ACCOUNT = from_conf("SNOWPARK_ACCOUNT")
# Snowflake user to use with the @snowpark decorator
SNOWPARK_USER = from_conf("SNOWPARK_USER")
# Snowflake password to use with the @snowpark decorator
SNOWPARK_PASSWORD = from_conf("SNOWPARK_PASSWORD")
# Snowflake role to use with the @snowpark decorator
SNOWPARK_ROLE = from_conf("SNOWPARK_ROLE")
# Snowflake database to use with the @snowpark decorator
SNOWPARK_DATABASE = from_conf("SNOWPARK_DATABASE")
# Snowflake warehouse to use with the @snowpark decorator
SNOWPARK_WAREHOUSE = from_conf("SNOWPARK_WAREHOUSE")
# Snowflake schema to use with the @snowpark decorator
SNOWPARK_SCHEMA = from_conf("SNOWPARK_SCHEMA")
