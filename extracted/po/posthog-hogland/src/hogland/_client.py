"""Synchronous hogland client.

The top-level entry point most users want:

.. code-block:: python

    from hogland import Hogland

    client = Hogland()  # reads HOG_TOKEN + HOG_HOST from env
    box = client.create(cpus=4, memory_mib=8192, disk_gib=50)
    try:
        result = box.exec(["uname", "-a"])
        print(result.stdout)
    finally:
        box.delete()

Or with a ``with`` block — :class:`hogland.Hogbox` is a context manager
that calls ``delete`` on exit, matching Modal's ``SandboxBase`` shape:

.. code-block:: python

    with client.create(cpus=4, memory_mib=8192) as box:
        box.exec(["echo", "hi"])
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from ._box import Hogbox, _box_path, _snapshots_path
from ._http import (
    _UNSET,
    _build_create_body,
    _build_pen_create_body,
    _build_pen_patch_body,
    _pen_path,
    build_sync_client,
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
    from collections.abc import Callable, Iterator, Mapping, Sequence
    from types import TracebackType

    import httpx


class Hogland:
    """Synchronous hogland API client."""

    def __init__(
        self,
        *,
        token: str | None = None,
        token_provider: Callable[[], str] | None = None,
        base_url: str | None = None,
        timeout: httpx.Timeout | float | None = None,
        transport: httpx.BaseTransport | None = None,
        trust_env: bool = True,
    ) -> None:
        """Construct the client.

        Args:
            token: Bearer token. Falls back to ``$HOG_TOKEN``. Required
                unless ``token_provider`` is given.
            token_provider: Callable returning the bearer token, invoked
                on every request. Takes precedence over ``token`` /
                ``$HOG_TOKEN``. Use for credentials that rotate, such as
                K8s projected ServiceAccount tokens (see
                :meth:`from_token_file`).
            base_url: API base URL, e.g. ``https://hogland.prod-us.posthog.dev``.
                Falls back to ``$HOG_HOST``, then to the default.
            timeout: Per-request timeout in seconds, or an ``httpx.Timeout``.
                Defaults to 30s overall / 10s connect.
            transport: Override the httpx transport. Used by tests to
                plug in ``respx`` or a fake.
            trust_env: When ``False``, ignore ``HTTP(S)_PROXY`` / ``NO_PROXY``
                and other environment configuration. Pass ``False`` when the
                caller reaches hogland over an in-cluster / PrivateLink path
                that must not go through an egress proxy.
        """
        self._token_provider = token_provider
        self._http, self._base_url, self._token = build_sync_client(
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
        transport: httpx.BaseTransport | None = None,
        trust_env: bool = True,
    ) -> Self:
        """Construct a client that re-reads its bearer token from ``path``.

        Built for K8s projected ServiceAccount token volumes: kubelet
        rewrites the file roughly every 50 minutes, and reading it per
        request (rather than once at construction) means the client
        never presents a stale credential. The file must exist when the
        client is constructed.

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

    # ---- context manager --------------------------------------------------

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._http.close()

    # ---- public properties ------------------------------------------------

    @property
    def base_url(self) -> str:
        """Resolved API base URL."""
        return self._base_url

    @property
    def token(self) -> str:
        """Current bearer token. Useful for hand-rolled proxy calls.

        With a ``token_provider`` this invokes the provider, so the
        value is as fresh as the next request's would be.
        """
        if self._token_provider is not None:
            return self._token_provider()
        assert self._token is not None  # build_sync_client resolved it
        return self._token

    # ---- account ----------------------------------------------------------

    def me(self) -> Me:
        """Return the caller's identity, as the server sees it."""
        resp = self._http.get("/v1/me")
        raise_for_status(resp)
        return Me.model_validate(resp.json())

    def limits(self) -> Limits:
        """Return the server-advertised valid ranges for box sizing."""
        resp = self._http.get("/v1/limits")
        raise_for_status(resp)
        return Limits.model_validate(resp.json())

    # ---- box CRUD ---------------------------------------------------------

    def create(
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
    ) -> Hogbox:
        """Create a hogbox and return a handle to it.

        The handle is a context manager that calls ``delete`` on exit.
        Sizing arguments map 1:1 to ``BoxSpec`` fields — see
        ``openapi.yaml`` for the authoritative range constraints.

        ``cpus`` / ``memory_mib`` / ``disk_gib`` / ``disk_class`` default
        to ``None`` so they're omitted from the request and the server's
        ``applyDefaults`` fills them in (1 CPU, 1 GiB, 10 GiB, ``mirrored``).
        Critically, this is also what makes ``snapshot_id=`` restores
        work: per the spec, ``cpus`` / ``memory_mib`` must be omitted on
        restore so they inherit from the snapshot, or match the
        snapshot exactly. Passing ``cpus=`` / ``memory_mib=`` explicitly
        on restore requires them to match the snapshot's machine config.

        ``access_type`` defaults to ``"none"`` on cold boot when no
        ``ssh_public_key`` is given (the box is driven via exec / files /
        proxy — the SDK's own surface). The server's ``ssh-public``
        default would reject a keyless create. Pass
        ``access_type="ssh-public"`` (or ``ssh-private``) together with
        ``ssh_public_key=`` for shell access; restores inherit the
        snapshot's access type and keys as before.

        ``env`` is materialised inside the box at ``/etc/hogbox-env``
        (mode 600, shell-escaped) before ``bootstrap`` runs and before
        sshd starts. Keys must match ``[A-Za-z_][A-Za-z0-9_]*``; up to
        50 entries, ≤ 4 KiB each, ≤ 16 KiB rendered total. Values must
        not contain NUL or CR bytes. Prefer this over rendering
        ``export KEY=$(shlex.quote VAL)`` into ``bootstrap`` — declarative,
        safe, never leaks into ``ps``.

        ``ttl_seconds`` bounds idle lifetime. The reaper destroys boxes
        whose last mutating call (exec, file IO, snapshot, pause/resume,
        proxy, patch) is older than this. ``None`` (the default) means
        the server picks (24 h). Explicit values must be in
        ``[60, 604800]`` — one minute through one week.

        ``web_port`` opts the box into HTTP exposure at its own per-box
        hostname: the in-guest port is served at
        ``https://<box>.<box-edge>/`` (read it back with
        :meth:`Hogbox.web_url`). Must be in ``[1, 65535]`` when set;
        requires the box's ``exec`` boot feature. ``None`` (default) =
        not exposed.
        """
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
        resp = self._http.post("/v1/hogboxes", json=body)
        raise_for_status(resp)
        view = BoxView.model_validate(resp.json())
        return Hogbox(view, self)

    def get(self, box_id: str) -> Hogbox:
        """Fetch an existing hogbox by id."""
        resp = self._http.get(_box_path(box_id))
        raise_for_status(resp)
        view = BoxView.model_validate(resp.json())
        return Hogbox(view, self)

    def list(
        self,
        *,
        status: str | None = None,
        kind: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> HogboxList:
        """List the caller's hogboxes."""
        params: dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        if kind is not None:
            params["kind"] = kind
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        resp = self._http.get("/v1/hogboxes", params=params or None)
        raise_for_status(resp)
        return HogboxList.model_validate(resp.json())

    def iter_boxes(
        self,
        *,
        status: str | None = None,
        kind: str | None = None,
        page_size: int | None = None,
    ) -> Iterator[BoxView]:
        """Yield boxes across pages, transparently following ``next_cursor``.

        Use this when you might have more boxes than fit in one page
        (default page size is server-controlled, currently ~100).
        """
        cursor: str | None = None
        while True:
            page = self.list(status=status, kind=kind, limit=page_size, cursor=cursor)
            yield from page.items
            if not page.next_cursor:
                return
            cursor = page.next_cursor

    # ---- snapshots --------------------------------------------------------

    def snapshot(self, box_id: str) -> SnapshotRecord:
        """Snapshot the named box. Convenience for callers without a handle."""
        resp = self._http.post(_snapshots_path(box_id))
        raise_for_status(resp)
        return SnapshotRecord.model_validate(resp.json())

    # ---- pens ---------------------------------------------------------------
    #
    # A pen is the stable named identity over the box lifecycle — boxes
    # rotate IDs on every create-from-snapshot, the pen persists (minted
    # immutable id, CurrentBoxID / LatestSnapshotID pointers, attribution
    # metadata). The intended flow for e.g. PR previews: derive the pen
    # name deterministically ("preview-pr-1234"), create it once, and
    # PATCH the pointers as boxes come and go. See docs/PENS.md in the
    # hogland repo for the concept and the hibernate/wake roadmap.

    def create_pen(
        self,
        name: str,
        *,
        source_alias: str | None = None,
        spec: BoxSpec | Mapping[str, Any] | None = None,
        on_idle: str | None = None,
        wake: str | None = None,
        metadata: Mapping[str, str] | None = None,
    ) -> Pen:
        """Create a pen. Raises :class:`ConflictError` if the name exists.

        ``name`` is owner-scoped, lowercase alphanumeric plus ``-``
        (≤ 32 chars). ``on_idle`` (``"destroy"``/``"hibernate"``) and
        ``wake`` (``"manual"``/``"on-request"``) are persisted but not
        yet enforced server-side; ``wake="on-request"`` requires an
        exposed spec. ``metadata`` is display-only attribution (repo,
        PR number, backlink URL, …) — ≤ 16 entries, label-safe keys,
        values ≤ 512 bytes, never used in server decisions and not a
        secrets channel.
        """
        body = _build_pen_create_body(
            name=name,
            source_alias=source_alias,
            spec=spec,
            on_idle=on_idle,
            wake=wake,
            metadata=metadata,
        )
        resp = self._http.post("/v1/pens", json=body)
        raise_for_status(resp)
        return Pen.model_validate(resp.json())

    def get_pen(self, name: str) -> Pen:
        """Fetch one of the caller's pens by name."""
        resp = self._http.get(_pen_path(name))
        raise_for_status(resp)
        return Pen.model_validate(resp.json())

    def list_pens(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> PenList:
        """List the caller's pens (newest first)."""
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        resp = self._http.get("/v1/pens", params=params or None)
        raise_for_status(resp)
        return PenList.model_validate(resp.json())

    def iter_pens(self, *, page_size: int | None = None) -> Iterator[Pen]:
        """Yield pens across pages, transparently following ``next_cursor``."""
        cursor: str | None = None
        while True:
            page = self.list_pens(limit=page_size, cursor=cursor)
            yield from page.items
            if not page.next_cursor:
                return
            cursor = page.next_cursor

    def update_pen(
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
        """Partial-update a pen — only kwargs you pass are sent.

        Explicit empties are meaningful: ``current_box_id=""`` clears
        the pointer (e.g. after the box is destroyed) and
        ``metadata={}`` clears the map. A non-empty ``metadata``
        replaces the whole map (no merge), matching the server's
        replace-not-merge PATCH semantics. Passing ``None`` raises
        ``ValueError`` — it's ambiguous between "omit" and "clear", so
        the call tells you which spelling you meant.
        """
        body = _build_pen_patch_body(
            current_box_id=current_box_id,
            latest_snapshot_id=latest_snapshot_id,
            source_alias=source_alias,
            spec=spec,
            on_idle=on_idle,
            wake=wake,
            metadata=metadata,
        )
        resp = self._http.patch(_pen_path(name), json=body)
        raise_for_status(resp)
        return Pen.model_validate(resp.json())

    def delete_pen(self, name: str, *, expected_current_box_id: str | None = None) -> None:
        """Delete a pen and its current box/snapshot.

        Passing ``expected_current_box_id`` fences stale cleanup workers: the
        server returns a conflict instead of deleting a pen repointed by a
        newer worker.
        """
        params = (
            {"expected_current_box_id": expected_current_box_id}
            if expected_current_box_id is not None
            else None
        )
        resp = self._http.delete(_pen_path(name), params=params)
        raise_for_status(resp)

    def hibernate_pen(self, name: str) -> Pen:
        """Hibernate a pen: snapshot its box, tear the box down, and repoint
        ``latest_snapshot_id`` at the new snapshot. Idempotent — hibernating an
        already-hibernated pen is a no-op. Restore it with :meth:`wake_pen`.
        """
        resp = self._http.post(_pen_path(name) + "/hibernate")
        raise_for_status(resp)
        return Pen.model_validate(resp.json())

    def wake_pen(self, name: str) -> Pen:
        """Wake a hibernated pen: restore its box from ``latest_snapshot_id``
        and repoint ``current_box_id`` at it. Idempotent — waking a pen that
        already has a live box is a no-op.
        """
        resp = self._http.post(_pen_path(name) + "/wake")
        raise_for_status(resp)
        return Pen.model_validate(resp.json())
