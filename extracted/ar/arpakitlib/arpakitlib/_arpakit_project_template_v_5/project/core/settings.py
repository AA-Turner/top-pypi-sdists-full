import os
from functools import lru_cache
from typing import Any

import pytz
from pydantic import field_validator
from pydantic_core.core_schema import ValidationInfo

from arpakitlib.ar_json_util import transfer_data_to_json_str
from arpakitlib.ar_settings_util import SimpleSettings
from arpakitlib.ar_sqlalchemy_util import generate_sqlalchemy_url
from arpakitlib.ar_type_util import raise_for_type
from project.core.const import ProjectPaths


class Settings(SimpleSettings):
    prod_mode: bool = False

    def raise_if_prod_mode(self):
        if self.prod_mode:
            raise ValueError(f"self.prod_mode")

    def raise_if_mode_prod(self):
        self.raise_if_prod_mode()

    def raise_if_not_prod_mode(self):
        if not self.prod_mode:
            raise ValueError(f"not self.prod_mode")

    project_name: str | None = "project"

    common_project_name: str | None = project_name

    project_title: str | None = project_name

    common_project_title: str | None = project_name

    sqlalchemy_db_user: str | None = project_name

    sqlalchemy_db_password: str | None = project_name

    sqlalchemy_db_host: str | None = "127.0.0.1"

    sqlalchemy_db_port: int | None = 5432

    sqlalchemy_db_database: str | None = project_name

    sqlalchemy_sync_db_url: str | None = None

    @field_validator("sqlalchemy_sync_db_url", mode="after")
    def validate_sqlalchemy_sync_db_url(cls, v: Any, validation_info: ValidationInfo, **kwargs) -> str | None:
        if v is not None:
            return v

        return generate_sqlalchemy_url(
            base="postgresql",
            user=validation_info.data.get("sqlalchemy_db_user"),
            password=validation_info.data.get("sqlalchemy_db_password"),
            host=validation_info.data.get("sqlalchemy_db_host"),
            port=validation_info.data.get("sqlalchemy_db_port"),
            database=validation_info.data.get("sqlalchemy_db_database")
        )

    sqlalchemy_async_db_url: str | None = None

    @field_validator("sqlalchemy_async_db_url", mode="after")
    def validate_sqlalchemy_async_db_url(cls, v: Any, validation_info: ValidationInfo, **kwargs) -> str | None:
        if v is not None:
            return v

        return generate_sqlalchemy_url(
            base="postgresql+asyncpg",
            user=validation_info.data.get("sqlalchemy_db_user"),
            password=validation_info.data.get("sqlalchemy_db_password"),
            host=validation_info.data.get("sqlalchemy_db_host"),
            port=validation_info.data.get("sqlalchemy_db_port"),
            database=validation_info.data.get("sqlalchemy_db_database")
        )

    @property
    def is_any_sql_db_url_set(self) -> bool:
        if self.sqlalchemy_sync_db_url is not None:
            return True
        if self.sqlalchemy_async_db_url is not None:
            return True
        return False

    sqlalchemy_db_echo: bool = False

    api_port: int | None = 8080

    api_host: str | None = "localhost"

    api_reload: bool = False

    api_init_sqlalchemy_db: bool = False

    api_init_json_db: bool = False

    api_correct_api_keys: list[str] | None = ["1"]

    @field_validator("api_correct_api_keys", mode="before")
    def validate_api_correct_api_keys(cls, v: Any, validation_info: ValidationInfo, **kwargs) -> list[str] | None:
        if isinstance(v, str):
            v = [v]
        if isinstance(v, int):
            v = [str(v)]
        if isinstance(v, list):
            for i, v_ in enumerate(v):
                if isinstance(v_, int):
                    v[i] = str(v_)
        return v

    api_enable_sqladmin: bool = True

    api_start_operation_executor_worker: bool = False

    api_start_scheduled_operation_creator_worker: bool = False

    api_version: str = "0.0.1"

    api_create_first_data: bool = True

    api_workers: int = 4

    api_docs_url: str = "/secret/docs"

    api_redoc_url: str = "/secret/redoc"

    api_openapi_url: str = "/secret/openapi"

    api_uvicorn_timeout_keep_alive: int = 3

    api_uvicorn_limit_concurrency: int = 1000

    api_uvicorn_backlog: int = 2048

    sqladmin_secret_key: str | None = "85a9583cb91c4de7a78d7eb1e5306a04418c9c43014c447ea8ec8dd5deb4cf71"

    sqladmin_authorize_keys: list[str] | None = ["1"]

    @field_validator("sqladmin_authorize_keys", mode="before")
    def validate_sqladmin_authorize_keys(cls, v: Any, validation_info: ValidationInfo, **kwargs) -> list[str] | None:
        if isinstance(v, str):
            v = [v]
        if isinstance(v, int):
            v = [str(v)]
        if isinstance(v, list):
            for i, v_ in enumerate(v):
                if isinstance(v_, int):
                    v[i] = str(v_)
        return v

    sqladmin_port: int | None = 8081

    sqladmin_prefix: str | None = "/sqladmin"

    sqladmin_full_url: str = f"http://{api_host}:{api_port}"

    sqladmin_full_url_with_prefix: str = sqladmin_full_url + sqladmin_prefix

    tg_bot_token: str | None = None

    tg_bot_proxy_url: str | None = None

    tg_bot_init_sqlalchemy_db: bool = False

    tg_bot_init_json_db: bool = False

    tg_bot_webhook_server_hostname: str | None = "127.0.0.1"

    tg_bot_webhook_server_port: int | None = None

    tg_bot_webhook_path: str | None = "/tg_bot_webhook"

    tg_bot_webhook_secret: str | None = "09780c63-22b5-44e2-9b72-f0cf651f7a9a"

    tg_bot_webhook_url: str | None = None

    tg_bot_webhook_enabled: bool = False

    tg_bot_drop_pending_updates: bool = True

    tg_bot_start_operation_executor_worker: bool = False

    tg_bot_start_scheduled_operation_creator_worker: bool = False

    tg_bot_command_passwd: str | None = "1"

    tg_bot_admin_tg_ids: list[int] = [269870432]

    tg_bot_set_commands: bool = True

    var_dirpath: str | None = os.path.join(ProjectPaths.base_dirpath, "var")

    log_filepath: str | None = os.path.join(var_dirpath, "story.log")

    cache_dirpath: str | None = os.path.join(var_dirpath, "cache")

    media_dirpath: str | None = os.path.join(var_dirpath, "media")

    dump_dirpath: str | None = os.path.join(var_dirpath, "dump")

    json_db_dirpath: str | None = os.path.join(var_dirpath, f"{project_name}_json_db")

    local_timezone: str | None = None

    email_smtp_user: str | None = None

    email_smtp_password: str | None = None

    email_smtp_port: int | None = 465

    email_smtp_hostname: str | None = "smtp.yandex.ru"

    @property
    def local_timezone_as_pytz(self) -> Any:
        raise_for_type(self.local_timezone, str)
        return pytz.timezone(self.local_timezone)

    openai_api_key: str | None = None

    openai_api_base_url: str | None = "https://api.proxyapi.ru/openai/v1"

    tg_bot_notifier_token: str | None = None

    tg_bot_notifier_proxy_url: str | None = None


@lru_cache()
def get_cached_settings() -> Settings:
    if os.path.exists(ProjectPaths.env_filepath):
        return Settings(_env_file=ProjectPaths.env_filepath, _env_file_encoding="utf-8")
    return Settings()


if __name__ == '__main__':
    print(transfer_data_to_json_str(get_cached_settings().model_dump(mode="json")))
