from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING, Any
from uuid import uuid4

import sqlalchemy
from email_validator import validate_email
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from arpakitlib.ar_datetime_util import now_utc_dt
from arpakitlib.ar_enumeration_util import Enumeration
from arpakitlib.ar_str_util import make_none_if_blank
from arpakitlib.ar_type_util import raise_for_type
from project.sqlalchemy_db_.sqlalchemy_model.common import SimpleDBM

if TYPE_CHECKING:
    from project.sqlalchemy_db_.sqlalchemy_model.user_token import UserTokenDBM
    from project.sqlalchemy_db_.sqlalchemy_model.verification_code import VerificationCodeDBM


def generate_default_user_password() -> str:
    return (
        "userpassword"
        f"{str(uuid4()).replace('-', '')}"
        f"{str(now_utc_dt().timestamp()).replace('.', '')}"
    )


class UserDBM(SimpleDBM):
    __tablename__ = "user"

    class Roles(Enumeration):
        admin = "admin"
        client = "client"

    fullname: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        nullable=True,
    )
    email: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        nullable=True,
        unique=True
    )
    username: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        nullable=True,
        unique=True
    )
    roles: Mapped[list[str]] = mapped_column(
        sqlalchemy.ARRAY(sqlalchemy.TEXT),
        nullable=False,
        index=True,
        insert_default=[Roles.client],
    )
    is_active: Mapped[bool] = mapped_column(
        sqlalchemy.Boolean,
        nullable=False,
        index=True,
        insert_default=True,
        server_default="true",
    )
    is_verified: Mapped[bool] = mapped_column(
        sqlalchemy.Boolean,
        nullable=False,
        index=True,
        insert_default=False,
        server_default="false",
    )
    password: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        nullable=True,
        index=True,
        insert_default=generate_default_user_password,
    )
    tg_id: Mapped[int | None] = mapped_column(
        sqlalchemy.BIGINT,
        nullable=True,
        unique=True
    )
    tg_bot_last_action_dt: Mapped[dt.datetime | None] = mapped_column(
        sqlalchemy.TIMESTAMP(timezone=True),
        nullable=True
    )
    tg_data: Mapped[dict[str, Any]] = mapped_column(
        sqlalchemy.JSON,
        nullable=False,
        index=False,
        insert_default={},
        server_default="{}",
    )

    # many to one
    user_tokens: Mapped[list[UserTokenDBM]] = relationship(
        "UserTokenDBM",
        uselist=True,
        back_populates="user",
        foreign_keys="UserTokenDBM.user_id",
        cascade="all, delete-orphan"
    )
    verification_codes: Mapped[list[VerificationCodeDBM]] = relationship(
        "VerificationCodeDBM",
        uselist=True,
        back_populates="user",
        foreign_keys="VerificationCodeDBM.user_id",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        parts = [f"id={self.id}"]
        if self.email is not None:
            parts.append(f"email={self.email}")
        if self.username is not None:
            parts.append(f"username={self.username}")
        return f"{self.entity_name} ({', '.join(parts)})"

    @validates("fullname")
    def _validate_fullname(self, key, value, *args, **kwargs):
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError(f"{key=}, {value=}, value is not str")
        value = make_none_if_blank(value.strip())
        return value

    @validates("email")
    def _validate_email(self, key, value, *args, **kwargs):
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError(f"{key=}, {value=}, value is not str")
        value = make_none_if_blank(value.strip())
        if value is None:
            return None
        validate_email(value)
        return value

    @validates("username")
    def _validate_username(self, key, value, *args, **kwargs):
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError(f"{key=}, {value=}, value is not str")
        value = make_none_if_blank(value.strip())
        return value

    @validates("tg_data")
    def _validate_tg_data(self, key, value, *args, **kwargs):
        if value is None:
            value = {}
        if not isinstance(value, dict):
            raise ValueError(f"{key=}, {value=}, value is not str")
        return value

    @property
    def sdp_allowed_roles(self) -> list[str]:
        return self.Roles.values_list()

    @property
    def roles_has_admin(self) -> bool:
        return self.Roles.admin in self.roles

    @property
    def sdp_roles_has_admin(self) -> bool:
        return self.roles_has_admin

    @property
    def roles_has_client(self) -> bool:
        return self.Roles.client in self.roles

    @property
    def sdp_roles_has_client(self) -> bool:
        return self.roles_has_client

    def compare_roles(self, roles: list[str] | str) -> bool:
        if isinstance(roles, str):
            roles = [roles]
        raise_for_type(roles, list)
        return bool(set(roles) & set(self.roles))

    @property
    def tg_data_first_name(self) -> str | None:
        if self.tg_data and "first_name" in self.tg_data:
            return self.tg_data["first_name"]
        return None

    @property
    def sdp_tg_data_first_name(self) -> str | None:
        return self.tg_data_first_name

    @property
    def tg_data_last_name(self) -> str | None:
        if self.tg_data and "last_name" in self.tg_data:
            return self.tg_data["last_name"]
        return None

    @property
    def sdp_tg_data_last_name(self) -> str | None:
        return self.tg_data_last_name

    @property
    def tg_data_language_code(self) -> str | None:
        if self.tg_data and "language_code" in self.tg_data:
            return self.tg_data["language_code"]
        return None

    @property
    def sdp_tg_data_language_code(self) -> str | None:
        return self.tg_data_language_code

    @property
    def tg_data_username(self) -> str | None:
        if self.tg_data and "username" in self.tg_data:
            return self.tg_data["username"]
        return None

    @property
    def sdp_tg_data_username(self) -> str | None:
        return self.tg_data_username

    @property
    def tg_data_at_username(self) -> str | None:
        if self.tg_data_username:
            return f"@{self.tg_data_username}"
        return None

    @property
    def sdp_tg_data_at_username(self) -> str | None:
        return self.tg_data_at_username

    @property
    def tg_data_fullname(self) -> str | None:
        if not self.tg_data_first_name and not self.tg_data_last_name:
            return None
        res = ""
        if self.tg_data_first_name:
            res += self.tg_data_first_name
        if self.tg_data_last_name:
            res += " " + self.tg_data_last_name
        return res

    @property
    def sdp_tg_data_fullname(self) -> str | None:
        return self.tg_data_fullname

    @property
    def tg_data_link_by_username(self) -> str | None:
        if not self.tg_data_username:
            return None
        return f"https://t.me/{self.tg_data_username}"

    @property
    def sdp_tg_data_link_by_username(self) -> str | None:
        return self.tg_data_link_by_username

    @property
    def email_prefix(self) -> str | None:
        if self.email is None:
            return None
        if self.email.count("@") != 1:
            return None
        return self.email.split("@")[0]

    @property
    def sdp_email_prefix(self) -> str | None:
        return self.email_prefix
