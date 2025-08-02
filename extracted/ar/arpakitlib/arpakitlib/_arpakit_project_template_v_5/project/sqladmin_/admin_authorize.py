import logging

import fastapi
import sqlalchemy
from sqladmin.authentication import AuthenticationBackend

from arpakitlib.ar_str_util import make_none_if_blank, strip_if_not_none
from project.core.settings import get_cached_settings
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import UserTokenDBM, UserDBM

SQLADMIN_AUTHORIZE_KEY = "sqladmin_authorize_key"


class SQLAdminAuth(AuthenticationBackend):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        super().__init__(secret_key=get_cached_settings().sqladmin_secret_key)

    async def login(self, request: fastapi.Request) -> bool:
        form = await request.form()

        username = make_none_if_blank(strip_if_not_none(form.get("username")))
        password = make_none_if_blank(strip_if_not_none(form.get("password")))

        if (
                get_cached_settings().sqladmin_authorize_keys is not None
                and (username is not None or password is not None)
        ):
            if (
                    (
                            is_username_correct := username in get_cached_settings().sqladmin_authorize_keys
                    )
                    or
                    (
                            is_password_correct := password in get_cached_settings().sqladmin_authorize_keys
                    )
            ):
                if is_username_correct:
                    request.session.update({SQLADMIN_AUTHORIZE_KEY: username})
                elif is_password_correct:
                    request.session.update({SQLADMIN_AUTHORIZE_KEY: password})
                return True

        if get_cached_sqlalchemy_db() is not None and (username is not None or password is not None):
            with get_cached_sqlalchemy_db().new_session() as session:
                query = session.query(UserTokenDBM)
                query = query.join(
                    UserDBM
                ).filter(
                    UserTokenDBM.is_active == True
                ).filter(
                    UserDBM.is_active.is_(True)
                )
                if username is not None:
                    query = query.filter(UserTokenDBM.value == username)
                elif password is not None:
                    query = query.filter(UserTokenDBM.value == password)
                else:
                    raise ValueError("no username and no password")
                user_token = query.one_or_none()
                if user_token is not None and user_token.user.compare_roles(UserDBM.Roles.admin):
                    request.session.update({SQLADMIN_AUTHORIZE_KEY: user_token.value})
                    return True

        if get_cached_sqlalchemy_db() is not None and (username is not None and password is not None):
            with get_cached_sqlalchemy_db().new_session() as session:
                query = session.query(UserDBM)
                query = query.filter(
                    UserDBM.is_active == True
                )
                _or_conditions = [
                    UserDBM.long_id == username,
                    UserDBM.slug == username,
                    UserDBM.email == username,
                    UserDBM.username == username,
                ]
                if username.isdigit():
                    _or_conditions.append(UserDBM.id == int(username))
                query = query.filter(sqlalchemy.or_(*_or_conditions))
                query = query.filter(UserDBM.password == password)
                user_dbm: UserDBM | None = query.one_or_none()
                if user_dbm is not None and user_dbm.compare_roles(UserDBM.Roles.admin):
                    new_user_token_dbm = UserTokenDBM(user_id=user_dbm.id)
                    session.add(new_user_token_dbm)
                    session.commit()
                    session.refresh(new_user_token_dbm)
                    request.session.update({SQLADMIN_AUTHORIZE_KEY: new_user_token_dbm.value})
                    return True

        return False

    async def logout(self, request: fastapi.Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: fastapi.Request) -> bool:
        sqladmin_auth_key = request.session.get(SQLADMIN_AUTHORIZE_KEY)
        if sqladmin_auth_key:
            sqladmin_auth_key = sqladmin_auth_key.strip()
        sqladmin_auth_key = make_none_if_blank(sqladmin_auth_key)

        if get_cached_settings().sqladmin_authorize_keys is not None and sqladmin_auth_key is not None:
            if sqladmin_auth_key in get_cached_settings().sqladmin_authorize_keys:
                return True

        if get_cached_sqlalchemy_db() is not None and sqladmin_auth_key is not None:
            with get_cached_sqlalchemy_db().new_session() as session:
                query = session.query(
                    UserTokenDBM
                ).filter(
                    UserTokenDBM.value == sqladmin_auth_key
                ).filter(
                    UserTokenDBM.is_active == True
                )
                user_token_dbm: UserTokenDBM | None = query.one_or_none()
                if user_token_dbm is not None and user_token_dbm.user.compare_roles(UserDBM.Roles.admin):
                    return True

        return False
