"""Asynchronous hogland client. Mirror of :mod:`hogland._client`.

Same surface, ``async def`` everywhere, returns :class:`AsyncHogbox`
handles. Designed to coexist with the sync client — you can build both
in the same process from the same env vars.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from ._box import AsyncHogbox, _box_path, _snapshots_path
from ._http import (
    _UNSET,
    _build_create_body,
    _build_pen_create_body,
    _build_pen_patch_body,
    _pen_path,
    build_async_client,
    raise_for_status,
    token_provider_from_file,
)
from ._models import (
    AccessType,
    BoxSpec,
    BoxView,
    DiskClass,
    HogboxList,
    Limits,
    Me,
    Pen,
    PenList,
    SnapshotRecord,
)

if TYPE_CHECKING:
    import os
    from collections.abc import AsyncIterator, Callable, Mapping, Sequence
    from types import TracebackType

    import httpx


class AsyncHogland:
    """Async hogland API client."""

    def __init__(
        self,
        *,
        token: str | None = None,
        token_provider: Callable[[], str] | None = None,
        base_url: str | None = None,
        timeout: httpx.Timeout | float | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
        trust_env: bool = True,
    ) -> None:
        self._token_provider = token_provider
        self._http, self._base_url, self._token = build_async_client(
            base_url=base_url,
            token=token,
            timeout=timeout,
            transport=transport,
            token_provider=token_provider,
            trust_env=trust_env,
        )

    @classmethod
    def from_token_file(
        cls,
        path: str | os.PathLike[str],
        *,
        base_url: str | None = None,
        timeout: httpx.Timeout | float | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
        trust_env: bool = True,
    ) -> Self:
        """Construct a client that re-reads its bearer token from ``path``.

        See :meth:`hogland.Hogland.from_token_file` — same contract,
        async client. The provider callable is sync (a small local file
        read), matching the ``token_provider`` kwarg's shape.

        ``trust_env=False`` keeps the client off any environment egress proxy —
        pass it for in-cluster / PrivateLink callers.
        """
        return cls(
            token_provider=token_provider_from_file(path),
            base_url=base_url,
            timeout=timeout,
            transport=transport,
            trust_env=trust_env,
        )

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self._http.aclose()

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def token(self) -> str:
        if self._token_provider is not None:
            return self._token_provider()
        assert self._token is not None  # build_async_client resolved it
        return self._token

    async def me(self) -> Me:
        resp = await self._http.get("/v1/me")
        raise_for_status(resp)
        return Me.model_validate(resp.json())

    async def limits(self) -> Limits:
        resp = await self._http.get("/v1/limits")
        raise_for_status(resp)
        return Limits.model_validate(resp.json())

    async def create(
        self,
        *,
        cpus: float | None = None,
        memory_mib: int | None = None,
        disk_gib: int | None = None,
        disk_class: DiskClass | str | None = None,
        disk_mbps: int = 0,
        disk_iops: int = 0,
        net_mbps: float = 0,
        access_type: AccessType | str | None = None,
        snapshot_id: str | None = None,
        ssh_public_key: str | None = None,
        bootstrap: str | None = None,
        env: Mapping[str, str] | None = None,
        ttl_seconds: int | None = None,
        name: str | None = None,
        kind: str | None = None,
        tags: Sequence[str] | None = None,
        web_port: int | None = None,
    ) -> AsyncHogbox:
        body = _build_create_body(
            cpus=cpus,
            memory_mib=memory_mib,
            disk_gib=disk_gib,
            disk_class=disk_class,
            disk_mbps=disk_mbps,
            disk_iops=disk_iops,
            net_mbps=net_mbps,
            access_type=access_type,
            snapshot_id=snapshot_id,
            ssh_public_key=ssh_public_key,
            bootstrap=bootstrap,
            env=env,
            ttl_seconds=ttl_seconds,
            name=name,
            kind=kind,
            tags=tags,
            web_port=web_port,
        )
        resp = await self._http.post("/v1/hogboxes", json=body)
        raise_for_status(resp)
        view = BoxView.model_validate(resp.json())
        return AsyncHogbox(view, self)

    async def get(self, box_id: str) -> AsyncHogbox:
        resp = await self._http.get(_box_path(box_id))
        raise_for_status(resp)
        view = BoxView.model_validate(resp.json())
        return AsyncHogbox(view, self)

    async def list(
        self,
        *,
        status: str | None = None,
        kind: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> HogboxList:
        params: dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        if kind is not None:
            params["kind"] = kind
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        resp = await self._http.get("/v1/hogboxes", params=params or None)
        raise_for_status(resp)
        return HogboxList.model_validate(resp.json())

    async def iter_boxes(
        self,
        *,
        status: str | None = None,
        kind: str | None = None,
        page_size: int | None = None,
    ) -> AsyncIterator[BoxView]:
        """Async generator over all matching boxes, following pagination."""
        cursor: str | None = None
        while True:
            page = await self.list(status=status, kind=kind, limit=page_size, cursor=cursor)
            for item in page.items:
                yield item
            if not page.next_cursor:
                return
            cursor = page.next_cursor

    async def snapshot(self, box_id: str) -> SnapshotRecord:
        resp = await self._http.post(_snapshots_path(box_id))
        raise_for_status(resp)
        return SnapshotRecord.model_validate(resp.json())

    # ---- pens — see Hogland for the full docstrings -------------------------

    async def create_pen(
        self,
        name: str,
        *,
        source_alias: str | None = None,
        spec: BoxSpec | Mapping[str, Any] | None = None,
        on_idle: str | None = None,
        wake: str | None = None,
        metadata: Mapping[str, str] | None = None,
    ) -> Pen:
        body = _build_pen_create_body(
            name=name,
            source_alias=source_alias,
            spec=spec,
            on_idle=on_idle,
            wake=wake,
            metadata=metadata,
        )
        resp = await self._http.post("/v1/pens", json=body)
        raise_for_status(resp)
        return Pen.model_validate(resp.json())

    async def get_pen(self, name: str) -> Pen:
        resp = await self._http.get(_pen_path(name))
        raise_for_status(resp)
        return Pen.model_validate(resp.json())

    async def list_pens(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> PenList:
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        resp = await self._http.get("/v1/pens", params=params or None)
        raise_for_status(resp)
        return PenList.model_validate(resp.json())

    async def iter_pens(self, *, page_size: int | None = None) -> AsyncIterator[Pen]:
        cursor: str | None = None
        while True:
            page = await self.list_pens(limit=page_size, cursor=cursor)
            for item in page.items:
                yield item
            if not page.next_cursor:
                return
            cursor = page.next_cursor

    async def update_pen(
        self,
        name: str,
        *,
        current_box_id: str = _UNSET,
        latest_snapshot_id: str = _UNSET,
        source_alias: str = _UNSET,
        spec: BoxSpec | Mapping[str, Any] = _UNSET,
        on_idle: str = _UNSET,
        wake: str = _UNSET,
        metadata: Mapping[str, str] = _UNSET,
    ) -> Pen:
        body = _build_pen_patch_body(
            current_box_id=current_box_id,
            latest_snapshot_id=latest_snapshot_id,
            source_alias=source_alias,
            spec=spec,
            on_idle=on_idle,
            wake=wake,
            metadata=metadata,
        )
        resp = await self._http.patch(_pen_path(name), json=body)
        raise_for_status(resp)
        return Pen.model_validate(resp.json())

    async def delete_pen(self, name: str, *, expected_current_box_id: str | None = None) -> None:
        """Delete a pen, optionally fencing a stale cleanup worker by box ID."""
        params = (
            {"expected_current_box_id": expected_current_box_id}
            if expected_current_box_id is not None
            else None
        )
        resp = await self._http.delete(_pen_path(name), params=params)
        raise_for_status(resp)

    async def hibernate_pen(self, name: str) -> Pen:
        """Hibernate a pen: snapshot its box, tear the box down, and repoint
        ``latest_snapshot_id`` at the new snapshot. Idempotent. Restore with
        :meth:`wake_pen`.
        """
        resp = await self._http.post(_pen_path(name) + "/hibernate")
        raise_for_status(resp)
        return Pen.model_validate(resp.json())

    async def wake_pen(self, name: str) -> Pen:
        """Wake a hibernated pen: restore its box from ``latest_snapshot_id``
        and repoint ``current_box_id`` at it. Idempotent.
        """
        resp = await self._http.post(_pen_path(name) + "/wake")
        raise_for_status(resp)
        return Pen.model_validate(resp.json())
