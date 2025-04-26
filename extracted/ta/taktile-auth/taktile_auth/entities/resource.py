from __future__ import annotations

import functools
import re
import typing as t

import pydantic

from taktile_auth.enums import Wildcard

PARTIAL_RE = re.compile(r"(^[^\*]*$)|(^[^\*]*\*$)")


def is_full_wildcard(v: str) -> str:
    assert v == "*" or "*" not in v
    return v


def is_partial_wildcard(v: str) -> str:
    assert re.fullmatch(PARTIAL_RE, v)
    return v


def is_fully_specified(v: str) -> str:
    assert "*" not in v
    return v


WILDCARD_CHECK = {
    Wildcard.allowed: is_full_wildcard,
    Wildcard.partial: is_partial_wildcard,
    Wildcard.not_allowed: is_fully_specified,
}


class Resource(pydantic.BaseModel):
    def __contains__(self, o: Resource) -> bool:
        """Checks if the queried resource 'o' is either equal
        or contained inside of 'self'.
        For each arg of the resource, checks if it is either a
        match with query's corresponding arg (including wildcards).
        """

        if self.schema()["title"] != o.schema()["title"]:
            return False

        for arg in self.dict().keys():
            allowed = getattr(self, arg)
            queried = getattr(o, arg)
            if not re.fullmatch(allowed.replace("*", ".*"), queried):
                return False
        return True

    def __hash__(self) -> int:
        return hash((type(self).__name__,) + tuple(self.__dict__.values()))

    class Config:
        allow_mutation = False


class ResourceDefinition(pydantic.BaseModel):
    resource_name: str
    args: t.Dict[str, Wildcard]

    def get_resource(self) -> t.Type[Resource]:
        return make_resource(
            resource_name=self.resource_name, args=HDict(self.args)
        )


class HDict(dict):  # type: ignore
    def __hash__(self) -> int:  # type: ignore
        return hash(frozenset(self.items()))


# performance counter probe
resources_built = 0


@functools.lru_cache(512)
def make_resource(resource_name: str, args: HDict) -> t.Type[Resource]:
    """
    Builds a resource class with the given name and args.
    Dynamic Pydantic model building is *really* expensive, hence we
    have this rubbish to save on it.
    See AUTH-1669 for the performance outcomes
    """
    global resources_built
    resources_built += 1
    fields: t.Any = {field_name: (str, ...) for field_name in args.keys()}
    validators = {
        f"{field_name}_validator": (
            pydantic.validator(field_name, allow_reuse=True)(
                WILDCARD_CHECK[check]
            )  # type: ignore
        )
        for field_name, check in args.items()
    }
    return t.cast(
        t.Type[Resource],
        pydantic.create_model(
            resource_name,
            **fields,
            __validators__=validators,  # type: ignore
            __base__=Resource,
        ),
    )
