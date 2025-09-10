from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from arpakitlib.ar_enumeration_util import Enumeration
from arpakitlib.ar_str_util import make_none_if_blank
from project.sqlalchemy_db_.sqlalchemy_model.common import SimpleDBM

if TYPE_CHECKING:
    from project.sqlalchemy_db_.sqlalchemy_model.user import UserDBM


def generate_default_verification_code_value() -> str:
    alphabet: list = list("JZSDQWRLGFZX" + "123456789")
    return "".join(alphabet[randint(0, len(alphabet) - 1)] for _ in range(7))


class VerificationCodeDBM(SimpleDBM):
    __tablename__ = "verification_code"

    class Types(Enumeration):
        register_or_authenticate = "register_or_authenticate"
        reset_email = "reset_email"

    type: Mapped[str] = mapped_column(
        sqlalchemy.TEXT,
        nullable=False,
        index=True,
    )
    value: Mapped[str] = mapped_column(
        sqlalchemy.TEXT,
        nullable=False,
        index=True,
        insert_default=generate_default_verification_code_value,
    )
    recipient: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        nullable=True,
        index=True,
    )
    user_id: Mapped[int | None] = mapped_column(
        sqlalchemy.BIGINT,
        sqlalchemy.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(
        sqlalchemy.BOOLEAN,
        nullable=False,
        index=True,
        insert_default=True,
        server_default="true"
    )

    # one to many
    user: Mapped[UserDBM | None] = relationship(
        "UserDBM",
        uselist=False,
        back_populates="verification_codes",
        foreign_keys=[user_id]
    )

    def __repr__(self) -> str:
        parts = [
            f"id={self.id}",
            f"type={self.type}"
        ]
        if self.recipient is not None:
            parts.append(f"recipient={self.recipient}")
        elif self.user_id is not None:
            parts.append(f"user_id={self.user_id}")
        return f"{self.entity_name} ({', '.join(parts)})"

    # ---validators---

    @validates("type")
    def _validate_type(self, key, value, *args, **kwargs):
        if not isinstance(value, str):
            raise ValueError(f"{key=}, {value=}, value is not str")
        value = value.strip()
        if not value:
            raise ValueError(f"{key=}, {value=}, value is empty")
        if value not in self.Types.values_list():
            raise ValueError(f"{value} not in {self.Types.values_list()}")
        return value

    @validates("recipient")
    def _validate_recipient(self, key, value, *args, **kwargs):
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError(f"{key=}, {value=}, value is not str")
        value = make_none_if_blank(value.strip())
        return value

    # ---more---

    # ---SDP---

    @property
    def sdp_allowed_types(self) -> list[str]:
        return self.Types.values_list()
