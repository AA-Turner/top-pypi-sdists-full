"""Resource: one data domain on a client (`client.runs`, `client.projects`): typed reads that answer
with the server's named response models. The flat methods (`client.get_run`) keep returning dicts."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

from ..delivery.transport.transport import Page

if TYPE_CHECKING:
    from pydantic import BaseModel

    from .client import Client

    _Model = TypeVar("_Model", bound=BaseModel)


class Resource:
    """A client's view of one domain. Each verb calls the client's flat method, so a subclass's
    override (OfflineClient) or a patch on the client is honoured, then validates its answer into
    the route's response model: a field a newer server adds is ignored, but a value outside a
    closed vocabulary (a new run status) raises ValidationError, where the flat dict would not. On a
    list read one such row fails the whole call; the flat method still answers."""

    __slots__ = ("_client",)

    def __init__(self, client: Client) -> None:
        self._client = client

    @staticmethod
    def _to_model(model: type[_Model], body: Any) -> _Model:
        return model.model_validate(body)

    @staticmethod
    def _to_models(model: type[_Model], rows: Any) -> list[_Model]:
        return [model.model_validate(row) for row in rows]

    @staticmethod
    def _to_typed_page(model: type[_Model], page: Page) -> Page:
        """The same page with its items as `model`s; `next_cursor` unchanged."""
        return Page(items=[model.model_validate(row) for row in page.items], next_cursor=page.next_cursor)
