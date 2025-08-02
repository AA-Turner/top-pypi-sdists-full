# These are intentionally not configurable by the user. The CLI is meant to connect to
# a proxy database running "locally" as a Docker container, so we're just setting some
# reasonable values here. If the connection doesn't work with these values, then it
# almost certainly won't work with any other values. No point in adding yet more flags
# to the already long list of flags for database connections.
PROXY_DB_CONNECTION_TIMEOUT_SECONDS = 5
PROXY_DB_CONNECTION_RETIRES = 3
