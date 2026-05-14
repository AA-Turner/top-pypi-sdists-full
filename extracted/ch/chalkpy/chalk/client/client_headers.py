CHALK_FEATURES_VERSIONED_HEADER = "X-Chalk-Features-Versioned"
"""
Setting this header to "true" indicates that the client is aware of feature versioning and will rewrite feature names to account for versioning.
This means that version resolution will not be handled server-side.
"""

CHALK_ENV_ID_HEADER = "X-Chalk-Env-Id"
"""The environment ID header specifies which environment the request is being made against."""

# FIXME: We should NOT be using the X-Chalk-Client-Id for anything, as it is NOT authenticated
CHALK_CLIENT_ID_HEADER = "X-Chalk-Client-Id"
"""The client ID header specifies the client making the request."""

CHALK_DEPLOYMENT_TAG_HEADER = "X-Chalk-Deployment-Tag"
"""The deployment tag header specifies the deployment tag for the request."""

CHALK_PREVIEW_DEPLOYMENT_HEADER = "X-Chalk-Preview-Deployment"
"""The preview deployment header specifies the preview deployment id for the request. Unused."""

CHALK_BRANCH_ID_HEADER = "X-Chalk-Branch-Id"
"""The branch ID header specifies which branch this request is being made against."""

CHALK_DEPLOYMENT_TYPE_HEADER = "X-Chalk-Deployment-Type"
"""The deployment type header is used during routing to determine which service to route the request to, i.e. "engine","engine-grpc, or "branch"."""

CHALK_QUERY_NAME_HEADER = "X-Chalk-Query-Name"
"""The query name header specifies the name of the query being executed."""

CHALK_SERVER_HEADER = "X-Chalk-Server"
"""The server header specifies which metadata plane api server the request should be sent to."""

# lowercase headers used for the gRPC client

CHALK_ENV_ID_HEADER_LOWERCASE = CHALK_ENV_ID_HEADER.lower()
"""Python gRPC client internals require lowercase header keys"""

CHALK_GRPC_TRACE_ID_HEADER = "x-chalk-trace-id"
"""The trace ID header specifies the trace ID for the request for the gRPC client."""

CHALK_SERVER_HEADER_LOWERCASE = CHALK_SERVER_HEADER.lower()
"""Python gRPC client internals require lowercase header keys"""

CHALK_DEPLOYMENT_TAG_HEADER_LOWERCASE = CHALK_DEPLOYMENT_TAG_HEADER.lower()
"""Python gRPC client internals require lowercase header keys"""

CHALK_DEPLOYMENT_TYPE_HEADER_LOWERCASE = CHALK_DEPLOYMENT_TYPE_HEADER.lower()
"""Python gRPC client internals require lowercase header keys"""
