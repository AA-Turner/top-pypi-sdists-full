# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class RoleEnum(str, enum.Enum):
    """
    * `ADMIN` - ADMIN
    * `DEVELOPER` - DEVELOPER
    * `MEMBER` - MEMBER
    * `API` - API
    * `SYSTEM` - SYSTEM
    * `MERGE_TEAM` - MERGE_TEAM
    """

    ADMIN = "ADMIN"
    DEVELOPER = "DEVELOPER"
    MEMBER = "MEMBER"
    API = "API"
    SYSTEM = "SYSTEM"
    MERGE_TEAM = "MERGE_TEAM"

    def visit(
        self,
        admin: typing.Callable[[], T_Result],
        developer: typing.Callable[[], T_Result],
        member: typing.Callable[[], T_Result],
        api: typing.Callable[[], T_Result],
        system: typing.Callable[[], T_Result],
        merge_team: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is RoleEnum.ADMIN:
            return admin()
        if self is RoleEnum.DEVELOPER:
            return developer()
        if self is RoleEnum.MEMBER:
            return member()
        if self is RoleEnum.API:
            return api()
        if self is RoleEnum.SYSTEM:
            return system()
        if self is RoleEnum.MERGE_TEAM:
            return merge_team()
