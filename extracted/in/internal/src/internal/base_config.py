from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    DEBUG: bool = False
    RUN_PORT: int = 5000
    TIME_ZONE: str = "Asia/Taipei"

    OPEN_API_URL: str = "/openapi.json"

    LOGGER_REQUEST_ENABLE: bool = True

    # Request
    REQUEST_VERIFY_SSL: bool = True
    REQUEST_PROXY: str = ''
    REQUEST_RETRY: int = 5
    REQUEST_CONN_POOL_TIMEOUT: float = 5
    REQUEST_CONN_TIMEOUT: float = 5
    REQUEST_WRITE_TIMEOUT: float = 5
    RESPONSE_READ_TIMEOUT: float = 5

    # AWS
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_KEY: str = ""
    AWS_REGION: str = ""
    AWS_PARAMETER_PATH_PREFIX: str = ""
    AWS_LOGGROUP_NAME: str = ""

    # MongoDB
    DATABASE_HOST: str = ''
    DATABASE_USERNAME: str = ''
    DATABASE_PASSWORD: str = ''
    DATABASE_PORT: int = 27017
    DATABASE_NAME: str = ""
    DATABASE_SSL: bool = False
    DATABASE_SSL_CA_CERTS: str = ""
    DATABASE_SERVER_SELECTION_TIMEOUT_MS: int = 5000
    DATABASE_CONNECT_TIMEOUT_MS: int = 10000
    DATABASE_AUTH_SOURCE: str = 'admin'

    # Micro Service
    AUTH_BASE_URL: str = "http://auth-service-api:5000"
    ORGANIZATION_BASE_URL: str = "http://organization-service-api:5000"
    CUSTOMER_BASE_URL: str = "http://customer-service-api:5000"
    CAR_BASE_URL: str = "http://car-service-api:5000"
    RELATIONSHIP_MANAGEMENT_BASE_URL: str = "http://relationship-management-service-api:5000"
    TICKET_BASE_URL: str = "http://ticket-service-api:5000"
    NOTIFY_BASE_URL: str = "http://notify-service-api:5000"
    THIRD_PARTY_BASE_URL: str = "http://third-party-service-api:5000"
    SCHEDULER_BASE_URL: str = "http://scheduler-service-api:5000"
    AUTO_DATA_PROCESSING_BASE_URL: str = "http://auto-data-processing-service-api:5000"

    # Exception Notify
    WEBHOOK_BASE_URL: str = ""

    # Default System Account Password
    SYSTEM_ACCOUNT: str = "cruisys"
    SYSTEM_PASSWORD: str = "cs50951855"
    SYSTEM_BRAND: str = "cruisys"
    SYSTEM_ORGANIZATION_ID: str = "cruisys"
    SYSTEM_NAME: str = "系統"
    SYSTEM_TITLE: str = ""

    # Redis URL
    REDIS_URL: str = ""

    class Config:
        case_sensitive = False
