# RFC3986 compliant connection type (Airflow 3.0+)
MCD_GATEWAY_CONNECTION_TYPE = "mcd-gateway"
# Legacy connection type for backward compatibility (Airflow 1.x, 2.x)
MCD_GATEWAY_CONNECTION_TYPE_LEGACY = "mcd_gateway"

MCD_GATEWAY_SCOPE = "AirflowCallbacks"
MCD_GATEWAY_HOSTS = [
    "integrations.getmontecarlo.com",
    "integrations.dev.getmontecarlo.com",
]
