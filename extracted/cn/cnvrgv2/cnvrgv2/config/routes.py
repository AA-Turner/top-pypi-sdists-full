# VERSION
VERSION = "v2/version/"

# ORGANIZATION
ORGANIZATION_BASE = "v2/{0}/"
ORGANIZATION_SETTINGS = "v2/{0}/settings"
ORGANIZATION_USERS = "v2/{0}/users"
ORGANIZATION_MEMBERS = "v2/{0}/members"
ORGANIZATION_CREATE = "v2/organizations"

# USER
USER_BASE = "v2/users/"
USER_LOGIN = "v2/users/sign_in"
USER_CURRENT = "v2/users/me"
USER_MEMBERSHIPS = "v2/users/me/memberships/"

# MEMBER
MEMBERS_BASE = "v2/{0}/members"
MEMBERS_ALL_BASE = "v2/{0}/members/all"
MEMBER_BASE = "v2/{0}/members?email={1}"

# PROJECT
PROJECTS_BASE = "v2/{0}/projects/"
PROJECT_BASE = "v2/{0}/projects/{1}"
PROJECT_CLONE_SUFFIX = "clone"
PROJECT_BULK_DELETE_SUFFIX = "delete_projects"
PROJECT_DELETE_SECRET = "delete_secrets"
PROJECT_UPDATE_SECRET = "update_secrets"

# DATASET
DATASETS_BASE = "v2/{0}/datasets/"
DATASET_BASE = "v2/{0}/datasets/{1}"

# LIBHUB
LIBHUB_BASE = "v2/libhub/"
LIBRARIES_BASE = "v2/{0}/libhub/libraries/"
LIBRARY_BASE = "v2/{0}/libhub/libraries/{1}/"
USE_LIBRARY_SUFFIX = "use"
LIBRARY_VERSIONS_BASE = "v2/{0}/libhub/libraries/{1}/versions/"
LIBRARY_VERSION_BASE = "v2/{0}/libhub/libraries/{1}/versions/{2}"

# COMMIT
DATASET_COMMITS_BASE = "v2/{0}/datasets/{1}/commits/"
DATASET_COMMIT_BASE = "v2/{0}/datasets/{1}/commits/{2}"
PROJECT_COMMITS_BASE = "v2/{0}/projects/{1}/commits/"
PROJECT_COMMIT_BASE = "v2/{0}/projects/{1}/commits/"
COMMIT_REMOVE_FILES = "commits/{0}/remove_files?page[size]=1000&sort=id"

# QUERIES
QUERY_BASE = "v2/{0}/datasets/{1}/queries/{2}"
QUERIES_BASE = "v2/{0}/datasets/{1}/queries"

# IMAGE
IMAGES_BASE = "v2/{0}/images/"
IMAGE_BASE = "v2/{0}/images/{1}"

# REGISTRY
REGISTRIES_BASE = "v2/{0}/registries/"
REGISTRY_BASE = "v2/{0}/registries/{1}"

# LABELS
LABELS_BASE = "v2/{0}/labels/"
LABELS_DATAOWNER_BASE = "v2/{0}/{1}/{2}/labels"

# VOLUME
VOLUMES_BASE = "v2/{0}/volumes"
VOLUME_BASE = "v2/{0}/volumes/{1}"

# Storage_Class
STORAGE_CLASSES_BASE = "v2/{0}/storage_classes"
STORAGE_CLASS_BASE = "v2/{0}/storage_classes/{1}"

# FLOW
FLOWS_BASE = "v2/{0}/projects/{1}/flows/"
FLOW_BASE = "v2/{0}/projects/{1}/flows/{2}/"
FLOW_SET_SCHEDULE = "start-cron"
FLOW_STOP_SCHEDULE = "stop-cron"
CREATE_WITH_YAML = "create-with-yaml"
RUN_FLOW = "run"
FLOW_TOGGLE_WEBHOOK = "toggle-webhook"
FLOW_TOGGLE_DATASET_UPDATE = "toggle-dataset-update"
FLOW_LATEST_END_COMMITS = "latest-end-commits"
FLOW_REVIEWERS = "reviewers"

# FLOW_VERSION
FLOW_VERSIONS_BASE = "v2/{0}/projects/{1}/flows/{2}/flow-versions"
FLOW_VERSION_BASE = "v2/{0}/projects/{1}/flows/{2}/flow-versions/{3}"
FLOW_VERSION_INFO = "info"
FLOW_VERSION_STOP = "stop"

# WORKFLOW
WORKFLOW_STANDALONE_BASE = "v2/{0}/workflows/"
WORKFLOWS_BASE = "v2/{0}/projects/{1}/workflows/"
WORKFLOWS_BASE_NEW = "v2/{0}/projects/{1}/{2}/"
WORKFLOW_BASE = "v2/{0}/projects/{1}/workflows/{2}/"
WORKFLOW_STOP_SUFFIX = "stop"
WORKFLOW_RESTART_SUFFIX = "restart"
WORKFLOW_SYNC_SUFFIX = "sync"
WORKFLOW_LIST_TYPE_SUFFIX = "?filter={{" \
                            "\"operator\":\"AND\"," \
                            "\"conditions\":[{{\"key\":\"job_type\",\"operator\":\"is\",\"value\":\"{0}\"}}]" \
                            "}}"
WORKflOW_START_SUFFIX = "start"
WORKflOW_START_TENSORBOARD_SUFFIX = "start_tensorboard"
WORKflOW_STOP_TENSORBOARD_SUFFIX = "stop_tensorboard"
WORKFLOW_WRITE_LOGS_SUFFIX = "write_logs"
WORKFLOW_GET_LOGS_SUFFIX = "logs"
WORKFLOW_TAG_SUFFIX = "tags"
WORKFLOW_UPDATE_SUFFIX = "update"
WORKFLOW_ARTIFACTS_SUFFIX = "artifacts"

# WORKSPACE
WORKSPACES_BASE = "v2/{0}/projects/{1}/workspaces/"
WORKSPACE_BASE = "v2/{0}/projects/{1}/workspaces/{2}/"
WORKSPACE_BUILD_IMAGE_SUFFIX = "build_image"
WORKSPACE_ACTIVATE_BUILD_IMAGE_ON_STOP_SUFFIX = "activate_build_image_on_stop"
WORKSPACE_DISABLE_BUILD_IMAGE_ON_STOP_SUFFIX = "disable_build_image_on_stop"

# EXPERIMENT
EXPERIMENTS_BASE = "v2/{0}/projects/{1}/experiments/"
EXPERIMENT_BASE = "v2/{0}/projects/{1}/experiments/{2}/"
EXPERIMENT_RERUN_SUFFIX = "rerun"
EXPERIMENT_FINISH_SUFFIX = "finish"
EXPERIMENT_CHARTS_SUFFIX = "charts"
EXPERIMENT_GET_UTILIZATION_SUFFIX = "get_utilization"
EXPERIMENT_CHART_SUFFIX = "charts/{0}"
EXPERIMENT_WRITE_LOGS = "write_logs"
EXPERIMENT_LOGS_SUFFIX = "logs?offset={0}&search={1}&filter={2}&page[after]={3}&page[before]={4}"
EXPERIMENT_HYPER_SUFFIX = "hyper"
EXPERIMENT_INFO_SUFFIX = "info"

# WEBAPP
WEBAPPS_BASE = "v2/{0}/projects/{1}/webapps/"
WEBAPP_BASE = "v2/{0}/projects/{1}/webapps/{2}/"

# ENDPOINT
ENDPOINTS_BASE = "v2/{0}/projects/{1}/endpoints"
ENDPOINT_BASE = "v2/{0}/projects/{1}/endpoints/{2}/"
UPDATE_MODEL_VERSION = "update_model"
ENDPOINT_FEEDBACK_LOOP = "feedback_loop"
ROLLBACK_MODEL_VERSION = "rollback_session/{0}"
ENDPOINT_SAMPLE_CODE = "sample_code"
ENDPOINT_REPLICAS = "replicas"
ENDPOINT_POLL_CHARTS = "poll_charts"
ENDPOINT_STATUS = "status"
ENDPOINT_BATCH_SCALE_UP = "batch_scale_up"
ENDPOINT_BATCH_SCALE_DOWN = "batch_scale_down"
ENDPOINT_RULES = "rules"
ENDPOINT_GET_PREDICTIONS = "get_predictions"

# COMMON
GET_BY_NAME_SUFFIX = "get_by_name"

# RESOURCES
MACHINES_BASE = "v2/{0}/resources/machines/computes"
SPARK_DRIVERS_BASE = "v2/{0}/resources/spark_driver"
CLUSTERS_BASE = "v2/{0}/resources"
MACHINE_BASE = "v2/{0}/resources/machines/computes/{1}"
SPARK_DRIVER_BASE = "v2/{0}/resources/spark_driver/{1}"
CLUSTER_BASE = "v2/{0}/resources/{1}"
CLUSTER_RESOURCE_REQUEST = "resource_request"
# TEMPLATE
TEMPLATES_BASE = "v2/{0}/resources/{1}/{2}/computes"
TEMPLATE_BASE = "v2/{0}/resources/{1}/{2}/computes/{3}"

# SSH
SSH_BASE = "v2/{0}/job_ssh/{1}"
SSH_START_SUFFIX = "start"
SSH_STATUS_SUFFIX = "status"

# GIT
GIT = "git"

# DATASOURCE
DATASOURCES_BASE = "v2/{0}/datasources/"
DATASOURCE_BASE = "v2/{0}/datasources/{1}"
