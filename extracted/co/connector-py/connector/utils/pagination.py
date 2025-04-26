"""Utilities for resource pagination.

When providing unified interface for several third-party APIs, we stand
before a problem how to define the pagination interface. On the level
of connectors, we decided to use ``page.token`` parameter that
will contain all information necessary to paginate over the third-party
interface.

The SDK provides basic class for representing third-party pagination and
utilities for converting the third-party pagination parameters from and
to next page token.

Since a third-party API can have very specific pagination parameters,
its representation in Lumos system is very generic. Since we are not
sure about how much third-party "endpoints" are to be called for one
call of connector method, we decided to use a list of pagination
parameters to be included in one next page token. We also expect that
paginations will differ for all third-party endpoints called during
one connector method call.

At the connector level, you have to define your own representation of
third-party pagination parameters by subclassing ``PaginationBase``
model and then create a class for converting third-party pagination
parameters to and from next page token. The class is created by passing
the pagination parameters model to ``create_next_page_token`` function.

The token created with the ``NextPageTokenInterface`` subclass can be
used as an input for the next method call. To access the decoded
third-party pagination, use the following: ::

    class ArgsWithNextPageToken(...):
        page: PaginationPageResp | None

    def your_method(args: ArgsWithNextPageToken) -> Response:
        paginations = NextPageToken(token=args.page.token).paginations()
        for pagination in paginations:
            # each pagination is the third-party pagination object
            pass

The token allows us to keep progress of pagination through subsequent
API calls and provides a kind of storage for a stateless process. This
is especially useful when the pagination over one kind of data (from the
Lumos API point of view) requires us to paginate over several kinds of
data (from the third-party API point of view). Listing entitlement
associations is a good example of such situation. Since we list all
associations of all entitlement types, we very likely have to paginate
over several different third-party endpoints. Very easy trick is to
"concatenate" all third-party endpoints that hold the data we need and
put the overall progress into the token. We can store all endpoints
that needs to be called for the next page into the next page token.

Example:
Assume we want 20 results per page and the third-party API has 30 active
users 35 licenses (one user can have more than one assigned license).
Calls to find-entitlement-associations will return the following:
    * first page holds users 1-20, next page will continue on the
    21st user
    * second page holds users 21-30 and since we have 10 more slots
    on the result page, it also fetches licenses 1-10
    * third page holds licenses 11-30
    * fourth page holds licenses 31-35 and should be the last (no
    next page token)
"""

import abc
import dataclasses
import typing as t

import msgpack  # type: ignore[import-untyped]
import pydantic

from connector.generated import Page


class PaginationBase(pydantic.BaseModel):
    """Base class for all third-party paginations.

    Connectors will most likely inherit this class and put the params
    specific to third-party API there.

    Attributes
    ----------
    endpoint:
        Name of endpoint that should be called by the connector. This
        could serve not only for http client but also for all other
        types. The information about where to send the "request" should
        go there.

    resource_type:
        Type of resource representing pagination entity. This could be
        used for logging purposes or for any other purpose where we
        need to know what kind of resource we are working with.

    """

    endpoint: str | None = None

    model_config = pydantic.ConfigDict(
        extra="forbid",
    )


PT = t.TypeVar("PT", bound=PaginationBase)


@dataclasses.dataclass
class NextPageTokenInterface(abc.ABC, t.Generic[PT]):
    """Interface for class that handles next page token serialization.

    Each connector has specific format of third-party API pagination
    represented with a subclass of ``PaginationBase``. The resulted
    token class will provide functionality to encode the third-party
    pagination parameters into next page token that is a part of
    connector interface.
    """

    token: str | None

    @classmethod
    @abc.abstractmethod
    def from_paginations(cls, paginations: list[PT]) -> "NextPageTokenInterface":
        """Encode group of paginations to token.

        This method is useful when we have to paginate over resource
        that is created as a concatenation of several third-party
        endpoints, e.g., list roles and licenses. Since the pagination
        over the result is not equal to pagination over its parts, we
        need to encode the pagination of all parts into one pagination
        over the result.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def paginations(self) -> list[PT]:
        """Decode token to group of paginations.

        This is an inversion of ``from_paginations`` and the following
        should hold true:
        ``list(Token.from_paginations(paginations).paginations())
        == paginations``.
        """
        raise NotImplementedError

    def to_page(self, size: int | None) -> Page:
        return Page(token=self.token, size=size)


def create_next_page_token(
    model: type[PT],
    class_name: str,
    docstring: str | None = None,
) -> type[NextPageTokenInterface[PT]]:
    """Create NextPageToken class for given model.

    See :py:class:``TokenInterface`` for more reference.

    The ``class_name`` is used to set the name for generated class so
    all classes don't have the same name. It is advised to use the
    same name we use for class identifier, i.e.
    ``NextPageToken = create_next_page_token(model, "NextPageToken")``

    Please note that mypy cannot determine the actual type of
    dynamically created class and will not even see it as a valid type.
    For this reason, it is recommended to do the following: ::

        if typing.TYPE_CHECKING:
            class NextPageToken(NextPageTokenInterface): pass
        else:
            NextPageToken = create_next_page_token(model, "NextPageToken)

    This will create the next page token class correctly in runtime
    while the correct type will be available for the type checker.
    """

    class Token(NextPageTokenInterface[PT]):
        """NextPageToken (de)serializer class."""

        @classmethod
        def from_paginations(cls, paginations: list[PT]) -> "Token":
            token_value: str | None
            if len(paginations) > 0:
                paginations_data = [pagination.model_dump() for pagination in paginations]
                token_value = msgpack.packb(paginations_data).hex()
            else:
                token_value = None

            return cls(
                token=token_value,
            )

        def paginations(self) -> list[PT]:
            if self.token is None:
                return []

            return [
                model(**pagination) for pagination in msgpack.unpackb(bytes.fromhex(self.token))
            ]

    Token.__name__ = class_name
    Token.__qualname__ = class_name
    Token.__doc__ = docstring or Token.__doc__
    return Token
