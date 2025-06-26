from fastapi import FastAPI, APIRouter
from fastapi.exceptions import RequestValidationError
from google.oauth2.service_account import Credentials
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import BaseModel, Field
from redis.asyncio.client import Redis
from redis.exceptions import RedisError
from starlette.exceptions import HTTPException
from starlette.types import Lifespan, AppType
from sqlalchemy import MetaData
from typing import Optional
from uuid import UUID
from maleo_foundation.client.manager import MaleoFoundationClientManager
from maleo_foundation.enums import BaseEnums
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.transfers.general.token \
    import MaleoFoundationTokenGeneralTransfers
from maleo_foundation.models.transfers.parameters.token \
    import MaleoFoundationTokenParametersTransfers
from maleo_foundation.managers.cache import CacheConfigurations, CacheManagers
from maleo_foundation.managers.cache.redis import (
    RedisCacheNamespaces,
    RedisCacheConfigurations
)
from maleo_foundation.managers.db import DatabaseConfigurations, DatabaseManager
from maleo_foundation.managers.client.google.secret import GoogleSecretManager
from maleo_foundation.managers.client.google.storage import GoogleCloudStorage
from maleo_foundation.managers.middleware import (
    MiddlewareConfigurations,
    BaseMiddlewareConfigurations,
    CORSMiddlewareConfigurations,
    GeneralMiddlewareConfigurations,
    MiddlewareLoggers,
    MiddlewareManager
)
from maleo_foundation.types import BaseTypes
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_foundation.utils.loaders.yaml import YAMLLoader
from maleo_foundation.utils.logging import (
    SimpleConfig,
    ServiceLogger,
    MiddlewareLogger
)
from maleo_foundation.utils.merger import deep_merge

class Settings(BaseSettings):
    ENVIRONMENT: BaseEnums.EnvironmentType = Field(..., description="Environment")
    SERVICE_KEY: str = Field(..., description="Service's key")
    GOOGLE_CREDENTIALS_PATH: str = Field("credentials/maleo-google-service-account.json", description="Internal credential's file path")
    STATIC_CONFIGURATIONS_PATH: str = Field("configs/static.yaml", description="Maleo's static configurations path")
    RUNTIME_CONFIGURATIONS_PATH: str = Field("configs/runtime.yaml", description="Service's runtime configurations path")

class MaleoCredentials(BaseModel):
    id: int = Field(..., description="ID")
    uuid: UUID = Field(..., description="UUID")
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email")
    password: str = Field(..., description="Password")

class MiddlewareRuntimeConfigurations(BaseModel):
    base: BaseMiddlewareConfigurations = Field(..., description="Base middleware's configurations")

    class Config:
        arbitrary_types_allowed=True

class ServiceConfigurations(BaseModel):
    key: str = Field(..., description="Service's key")
    name: str = Field(..., description="Service's name")
    host: str = Field(..., description="Service's host")
    port: int = Field(..., description="Service's port")

class RuntimeConfigurations(BaseModel):
    service: ServiceConfigurations = Field(..., description="Service's configurations")
    middleware: MiddlewareRuntimeConfigurations = Field(..., description="Middleware's runtime configurations")
    database: str = Field(..., description="Database's name")

    class Config:
        arbitrary_types_allowed=True

class MiddlewareStaticConfigurations(BaseModel):
    general: GeneralMiddlewareConfigurations = Field(..., description="Middleware's general configurations")
    cors: CORSMiddlewareConfigurations = Field(..., description="CORS middleware's configurations")

    class Config:
        arbitrary_types_allowed=True

class MaleoClientConfiguration(BaseModel):
    key: str = Field(..., description="Client's key")
    name: str = Field(..., description="Client's name")
    url: str = Field(..., description="Client's URL")

class MaleoClientConfigurations(BaseModel):
    telemetry: MaleoClientConfiguration = Field(..., description="MaleoTelemetry client's configuration")
    metadata: MaleoClientConfiguration = Field(..., description="MaleoMetadata client's configuration")
    identity: MaleoClientConfiguration = Field(..., description="MaleoIdentity client's configuration")
    access: MaleoClientConfiguration = Field(..., description="MaleoAccess client's configuration")
    workshop: MaleoClientConfiguration = Field(..., description="MaleoWorkshop client's configuration")
    medix: MaleoClientConfiguration = Field(..., description="MaleoMedix client's configuration")
    fhir: MaleoClientConfiguration = Field(..., description="MaleoFHIR client's configuration")
    dicom: MaleoClientConfiguration = Field(..., description="MaleoDICOM client's configuration")
    scribe: MaleoClientConfiguration = Field(..., description="MaleoScribe client's configuration")
    cds: MaleoClientConfiguration = Field(..., description="MaleoCDS client's configuration")
    imaging: MaleoClientConfiguration = Field(..., description="MaleoImaging client's configuration")
    mcu: MaleoClientConfiguration = Field(..., description="MaleoMCU client's configuration")

    class Config:
        arbitrary_types_allowed=True

class ClientConfigurations(BaseModel):
    maleo: MaleoClientConfigurations = Field(..., description="Maleo client's configurations")

    class Config:
        arbitrary_types_allowed=True

class StaticConfigurations(BaseModel):
    middleware: MiddlewareStaticConfigurations = Field(..., description="Middleware's static configurations")
    client: ClientConfigurations = Field(..., description="Client's configurations")

    class Config:
        arbitrary_types_allowed=True

class Configurations(BaseModel):
    service: ServiceConfigurations = Field(..., description="Service's configurations")
    middleware: MiddlewareConfigurations = Field(..., description="Middleware's configurations")
    cache: CacheConfigurations = Field(..., description="Cache's configurations")
    database: DatabaseConfigurations = Field(..., description="Database's configurations")
    client: ClientConfigurations = Field(..., description="Client's configurations")

    class Config:
        arbitrary_types_allowed=True

class Loggers(BaseModel):
    application: ServiceLogger = Field(..., description="Application logger")
    repository: ServiceLogger = Field(..., description="Repository logger")
    database: ServiceLogger = Field(..., description="Database logger")
    middleware: MiddlewareLoggers = Field(..., description="Middleware logger")

    class Config:
        arbitrary_types_allowed=True

class ServiceManager:
    def __init__(
        self,
        db_metadata: MetaData,
        log_config: SimpleConfig,
        settings: Optional[Settings] = None
    ):
        self._db_metadata = db_metadata #* Declare DB Metadata
        self._log_config = log_config #* Declare log config
        self._settings = settings if settings is not None else Settings() #* Initialize settings
        #* Disable google cloud logging if environment is local
        if self._settings.ENVIRONMENT == "local":
            self._log_config.google_cloud_logging = None
        self._load_google_credentials()
        self._initialize_secret_manager()
        self._load_maleo_credentials()
        self._load_configs()
        self._load_keys()
        self._initialize_loggers()
        self._initialize_cache()
        self._initialize_cloud_storage()
        self._initialize_db()
        self._initialize_foundation()

    @property
    def log_config(self) -> SimpleConfig:
        return self._log_config

    @property
    def settings(self) -> Settings:
        return self._settings

    def _load_google_credentials(self) -> None:
        self._google_credentials = Credentials.from_service_account_file(self._settings.GOOGLE_CREDENTIALS_PATH)

    @property
    def google_credentials(self) -> None:
        return self._google_credentials

    def _initialize_secret_manager(self) -> None:
        self._secret_manager = GoogleSecretManager(
            log_config=self._log_config,
            service_key=self._settings.SERVICE_KEY,
            credentials=self._google_credentials
        )

    @property
    def secret_manager(self) -> GoogleSecretManager:
        return self._secret_manager

    def _load_maleo_credentials(self) -> None:
        environment = (
            BaseEnums.EnvironmentType.STAGING
            if self._settings.ENVIRONMENT == BaseEnums.EnvironmentType.LOCAL
            else self._settings.ENVIRONMENT
        )
        id = int(self._secret_manager.get(f"maleo-service-account-id-{environment}"))
        uuid = self._secret_manager.get(f"maleo-service-account-uuid-{environment}")
        email = self._secret_manager.get("maleo-service-account-email")
        username = self._secret_manager.get("maleo-service-account-username")
        password = self._secret_manager.get("maleo-service-account-password")
        self._maleo_credentials = MaleoCredentials(
            id=id,
            uuid=UUID(uuid),
            username=username,
            email=email,
            password=password
        )

    @property
    def maleo_credentials(self) -> MaleoCredentials:
        return self._maleo_credentials

    def _load_configs(self) -> None:
        #* Load static configurations
        static_configurations_path = Path(self._settings.STATIC_CONFIGURATIONS_PATH)
        if static_configurations_path.exists() and static_configurations_path.is_file():
            static_configurations = YAMLLoader.load_from_path(self._settings.STATIC_CONFIGURATIONS_PATH)
        else:
            data = self._secret_manager.get(f"maleo-static-config-{self._settings.ENVIRONMENT}")
            static_configurations = YAMLLoader.load_from_string(data)
        static_configs = StaticConfigurations.model_validate(static_configurations)

        #* Load runtime configurations
        runtime_configurations_path = Path(self._settings.RUNTIME_CONFIGURATIONS_PATH)
        if runtime_configurations_path.exists() and runtime_configurations_path.is_file():
            runtime_configurations = YAMLLoader.load_from_path(self._settings.RUNTIME_CONFIGURATIONS_PATH)
        else:
            data = self._secret_manager.get(f"{self._settings.SERVICE_KEY}-runtime-config-{self._settings.ENVIRONMENT}")
            runtime_configurations = YAMLLoader.load_from_string(data)
        runtime_configs = RuntimeConfigurations.model_validate(runtime_configurations)

        #* Load redis cache configurations
        namespaces = RedisCacheNamespaces(base=self._settings.SERVICE_KEY)
        host = self._secret_manager.get(name=f"maleo-redis-host-{self._settings.ENVIRONMENT}")
        password = self._secret_manager.get(name=f"maleo-redis-password-{self._settings.ENVIRONMENT}")
        redis = RedisCacheConfigurations(namespaces=namespaces, host=host, password=password)
        cache = CacheConfigurations(redis=redis)

        #* Load database configurations
        password = self._secret_manager.get(name=f"maleo-db-password-{self._settings.ENVIRONMENT}")
        host = self._secret_manager.get(name=f"maleo-db-host-{self._settings.ENVIRONMENT}")
        database = DatabaseConfigurations(
            password=password,
            host=host,
            database=runtime_configs.database
        )

        #* Load whole configurations
        merged_configs = deep_merge(
            static_configs.model_dump(),
            runtime_configs.model_dump(exclude={"database"}),
            {"cache": cache.model_dump()},
            {"database": database.model_dump()}
        )
        self._configs = Configurations.model_validate(merged_configs)

    @property
    def configs(self) -> Configurations:
        return self._configs

    def _load_keys(self) -> None:
        password = self._secret_manager.get(name="maleo-key-password")
        private = self._secret_manager.get(name="maleo-private-key")
        public = self._secret_manager.get(name="maleo-public-key")
        self._keys = BaseGeneralSchemas.RSAKeys(
            password=password,
            private=private,
            public=public
        )

    @property
    def keys(self) -> BaseGeneralSchemas.RSAKeys:
        return self._keys

    def _initialize_loggers(self) -> None:
        #* Service's loggers
        application = ServiceLogger(
            type=BaseEnums.LoggerType.APPLICATION,
            service_key=self._configs.service.key,
            **self._log_config.model_dump()
        )
        database = ServiceLogger(
            type=BaseEnums.LoggerType.DATABASE,
            service_key=self._configs.service.key,
            **self._log_config.model_dump()
        )
        repository = ServiceLogger(
            type=BaseEnums.LoggerType.REPOSITORY,
            service_key=self._configs.service.key,
            **self._log_config.model_dump()
        )
        #* Middleware's loggers
        base = MiddlewareLogger(
            middleware_type=BaseEnums.MiddlewareLoggerType.BASE,
            service_key=self._configs.service.key,
            **self._log_config.model_dump()
        )
        authentication = MiddlewareLogger(
            middleware_type=BaseEnums.MiddlewareLoggerType.AUTHENTICATION,
            service_key=self._configs.service.key,
            **self._log_config.model_dump()
        )
        middleware = MiddlewareLoggers(base=base, authentication=authentication)
        self._loggers = Loggers(
            application=application,
            repository=repository,
            database=database,
            middleware=middleware
        )

    @property
    def loggers(self) -> Loggers:
        return self._loggers

    def _initialize_cache(self) -> None:
        self._redis = Redis(
            host=self._configs.cache.redis.host,
            port=self._configs.cache.redis.port,
            db=self._configs.cache.redis.db,
            password=self._configs.cache.redis.password,
            decode_responses=self._configs.cache.redis.decode_responses,
            health_check_interval=self._configs.cache.redis.health_check_interval
        )
        self._cache = CacheManagers(redis=self._redis)

    @property
    def redis(self) -> Redis:
        return self._redis

    @property
    def cache(self) -> CacheManagers:
        return self._cache

    def check_redis_connection(self) -> bool:
        try:
            self._redis.ping()
            self._loggers.application.info("Redis connection check successful.")
            return True
        except RedisError as e:
            self._loggers.application.error(f"Redis connection check failed: {e}", exc_info=True)
            return False

    def _initialize_cloud_storage(self) -> None:
        environment = (
            BaseEnums.EnvironmentType.STAGING
            if self._settings.ENVIRONMENT == BaseEnums.EnvironmentType.LOCAL
            else self._settings.ENVIRONMENT
        )
        self._cloud_storage = GoogleCloudStorage(
            log_config=self._log_config,
            service_key=self._settings.SERVICE_KEY,
            bucket_name=f"maleo-suite-{environment}",
            credentials=self._google_credentials,
            redis=self._redis
        )

    @property
    def cloud_storage(self) -> GoogleCloudStorage:
        return self._cloud_storage

    def _initialize_db(self) -> None:
        self._database = DatabaseManager(
            metadata=self._db_metadata,
            logger=self._loggers.database,
            url=self._configs.database.url
        )

    @property
    def database(self) -> DatabaseManager:
        return self._database

    def _initialize_foundation(self) -> None:
        self._foundation = MaleoFoundationClientManager(
            log_config=self._log_config,
            service_key=self._settings.SERVICE_KEY
        )

    @property
    def foundation(self) -> MaleoFoundationClientManager:
        return self._foundation

    @property
    def token(self) -> BaseTypes.OptionalString:
        payload = MaleoFoundationTokenGeneralTransfers.BaseEncodePayload(
            iss=None,
            sub=str(self._maleo_credentials.id),
            sr="administrator",
            u_i=self._maleo_credentials.id,
            u_uu=self._maleo_credentials.uuid,
            u_u=self._maleo_credentials.username,
            u_e=self._maleo_credentials.email,
            u_ut="service",
            exp_in=1
        )
        parameters = MaleoFoundationTokenParametersTransfers.Encode(
            key=self._keys.private,
            password=self._keys.password,
            payload=payload
        )
        result = self._foundation.services.token.encode(parameters=parameters)
        return result.data.token if result.success else None

    def create_app(
        self,
        router: APIRouter,
        lifespan: Optional[Lifespan[AppType]] = None
    ) -> FastAPI:
        self._loggers.application.info("Creating FastAPI application")
        root_path = "" if self._settings.ENVIRONMENT == "local" else f"/{self._configs.service.key.removeprefix("maleo-")}"
        self._app = FastAPI(
            title=self._configs.service.name,
            lifespan=lifespan,
            root_path=root_path
        )
        self._loggers.application.info("FastAPI application created successfully")

        #* Add middleware(s)
        self._loggers.application.info("Configuring middlewares")
        self._middleware = MiddlewareManager(
            app=self._app,
            configurations=self._configs.middleware,
            keys=self._keys,
            loggers=self._loggers.middleware,
            maleo_foundation=self._foundation
        )
        self._middleware.add_all()
        self._loggers.application.info("Middlewares added successfully")

        #* Add exception handler(s)
        self._loggers.application.info("Adding exception handlers")
        self._app.add_exception_handler(
            exc_class_or_status_code=RequestValidationError,
            handler=BaseExceptions.validation_exception_handler
        )
        self._app.add_exception_handler(
            exc_class_or_status_code=HTTPException,
            handler=BaseExceptions.http_exception_handler
        )
        self._loggers.application.info("Exception handlers added successfully")

        #* Include router
        self._loggers.application.info("Including routers")
        self._app.include_router(router)
        self._loggers.application.info("Routers included successfully")

        return self._app

    @property
    def app(self) -> FastAPI:
        return self._app

    async def dispose(self) -> None:
        self._loggers.application.info("Disposing service manager")
        if self._redis is not None:
            await self._redis.close()
            self._redis = None
        if self._database is not None:
            self._database.dispose()
            self._database = None
        self._loggers.application.info("Service manager disposed successfully")
        if self._loggers is not None:
            self._loggers.application.info("Disposing logger")
            self._loggers.application.dispose()
            self._loggers.database.info("Disposing logger")
            self._loggers.database.dispose()
            self._loggers.middleware.base.info("Disposing logger")
            self._loggers.middleware.base.dispose()
            self._loggers.middleware.authentication.info("Disposing logger")
            self._loggers.middleware.authentication.dispose()
            self._loggers = None