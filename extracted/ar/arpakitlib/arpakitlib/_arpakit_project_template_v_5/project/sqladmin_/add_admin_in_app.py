from fastapi import FastAPI
from sqladmin import Admin

from project.core.settings import get_cached_settings
from project.sqladmin_.admin_authorize import SQLAdminAuth
from project.sqladmin_.model_view import SimpleMV
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db


def add_sqladmin_in_app(
        *,
        app: FastAPI,
        base_url: str = "/sqladmin",
        favicon_url: str | None = None
) -> FastAPI:
    authentication_backend = SQLAdminAuth()

    admin = Admin(
        app=app,
        engine=get_cached_sqlalchemy_db().engine,
        base_url=base_url,
        authentication_backend=authentication_backend,
        title=get_cached_settings().project_name,
        favicon_url=favicon_url
    )

    for model_view in SimpleMV.__subclasses__():
        admin.add_model_view(model_view)

    return app
