#
# Copyright 2026 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import trafaret as t

from datarobot._compat import Int, NotRequired, String, TypedDict
from datarobot.models.api_object import APIObject
from datarobot.utils import assert_single_or_zero_parameter, parse_time

_UNSET = object()  # Sentinel to detect empty patch payload


class Emitter(TypedDict):
    type: str
    id: NotRequired[str]


class NewEvent(TypedDict):
    body: Dict[str, Any]
    emitter: Emitter
    event_type: NotRequired[str]


class EventUpdate(TypedDict):
    sequence_id: int
    body: NotRequired[Dict[str, Any]]
    event_type: NotRequired[str]
    emitter: NotRequired[Emitter]
    created_at: NotRequired[datetime]


class LifecycleTrigger(TypedDict, total=False):
    ttl: int
    eventCount: int
    tokenCount: int
    idle: int


class LifecycleOpts(TypedDict, total=False):
    softDelete: bool
    agentId: Optional[str]
    metadata: Dict[str, Any]


class LifecycleStrategy(TypedDict):
    type: str
    trigger: LifecycleTrigger
    opts: NotRequired[Optional[LifecycleOpts]]


def _build_patch_payload(**fields: object) -> Tuple[Dict[str, Any], List[str]]:
    """
    Build payload for PATCH requests, filtering out _UNSET values and tracking nullable attrs.
    """
    payload: Dict[str, Any] = {}
    keep_attrs: List[str] = []
    for key, value in fields.items():
        if value is _UNSET:
            continue
        payload[key] = value
        if value is None:
            keep_attrs.append(key)
    return payload, keep_attrs


def _update_attrs(instance: object, updated: object, attrs: Tuple[str, ...]) -> None:
    for attr in attrs:
        setattr(instance, attr, getattr(updated, attr))


class MemorySpace(APIObject):
    """
    A container for chat sessions and their events.

    A memory space groups related sessions and memories together, providing an isolation
    boundary for conversational, semantic, and episodic memories in agentic applications.

    .. versionadded:: v3.15

    Attributes
    ----------
    id : str
        The ID of the memory space.
    user_id : str
        The ID of the user who owns the memory space.
    tenant_id : str
        The ID of the tenant.
    description : str or None
        Optional. A human-readable description.
    llm_model_name : str or None
       Optional. An LLM model name associated with the memory space (maximum 200 characters).
       Non-reasoning models such as ``gpt-4o`` are recommended. Reasoning-capable models are
       significantly slower for fact extraction without producing meaningfully better results.
    llm_base_url : str or None
        Optional. The chat API URL used for memory extraction.
        The memory service uses the DataRobot LLM gateway by default; set this only when
        the default does not work — for example, in air-gapped environments or when the
        required LLM model is not provided by the gateway and cannot be added.
    custom_instructions : str or None
        Optional. Custom prompt instructions for fact extraction (maximum 10,000 characters).
        ``None`` means the default memory extraction prompt is used.
    created_at : datetime.datetime
        The timestamp when the memory space was created.
    deduplication_key : str or None
        Optional key supplied at create time to prevent duplicate memory spaces.
        Echoed back by the server and used to detect repeat memory space creations
        by the same user. ``None`` when the memory space was created without a key.
    """

    _path = "memory/"
    _create_path = "memory/new/"

    _converter = t.Dict({
        t.Key("memory_space_id", to_name="id"): String(),
        t.Key("user_id"): String(),
        t.Key("tenant_id"): String(),
        t.Key("description", optional=True, default=None): t.Or(String(allow_blank=True), t.Null),
        t.Key("llm_model_name", optional=True, default=None): t.Or(String(allow_blank=True), t.Null),
        t.Key("llm_base_url", optional=True, default=None): t.Or(String(max_length=2083, allow_blank=True), t.Null),
        t.Key("custom_instructions", optional=True, default=None): t.Or(String(allow_blank=True), t.Null),
        t.Key("created_at"): parse_time,
        t.Key("deduplication_key", optional=True, default=None): t.Or(String(), t.Null),
    }).ignore_extra("*")

    def __init__(
        self,
        id: Optional[str] = None,
        user_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        description: Optional[str] = None,
        llm_model_name: Optional[str] = None,
        llm_base_url: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        created_at: Optional[datetime] = None,
        deduplication_key: Optional[str] = None,
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.description = description
        self.llm_model_name = llm_model_name
        self.llm_base_url = llm_base_url
        self.custom_instructions = custom_instructions
        self.created_at = created_at
        self.deduplication_key = deduplication_key

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.id}')"

    @classmethod
    def _url(cls, resource_id: Optional[str] = None) -> str:
        return cls._path if resource_id is None else f"{cls._path}{resource_id}/"

    @classmethod
    def create(
        cls,
        description: Optional[str] = None,
        llm_model_name: Optional[str] = None,
        llm_base_url: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        deduplication_key: Optional[str] = None,
    ) -> MemorySpace:
        """
        Create a new memory space.

        .. versionadded:: v3.15

        .. versionchanged:: v3.17
            Added optional ``deduplication_key`` parameter to prevent duplicate
            memory space creations.

        Parameters
        ----------
        description : str or None
            Optional. A human-readable description for the memory space.
        llm_model_name : str or None
            Optional. An LLM model name to associate with the memory space (maximum 200 characters).
            Non-reasoning models such as ``gpt-4o`` are recommended. Reasoning-capable models are
            significantly slower for fact extraction without producing meaningfully better results.
        llm_base_url : str or None
            Optional. Chat API URL used for memory extraction.
            The memory service uses the DataRobot LLM gateway by default; set this only when
            the default does not work — for example, in air-gapped environments or when the
            required LLM model is not provided by the gateway and cannot be added.
        custom_instructions : str or None
            Optional. Custom prompt instructions for fact extraction (maximum 10 000 characters).
        deduplication_key : str or None
            Optional. A 1-72 character key that prevents duplicate memory spaces. If
            a live memory space with the same key already exists for this user, the
            server returns ``409 Conflict`` and the SDK raises
            :class:`~datarobot.errors.MemorySpaceDeduplicationError`, which carries
            ``existing_memory_space_id`` so callers can adopt the winning memory
            space. ``None`` keys do not collide; soft-deleting a memory space frees
            the key.

        Returns
        -------
        MemorySpace
            The newly created memory space.

        Raises
        ------
        MemorySpaceDeduplicationError
            When ``deduplication_key`` is supplied and a live memory space with the
            same key already exists for this user.
        """
        payload: Dict[str, Any] = {}
        if description is not None:
            payload["description"] = description
        if llm_model_name is not None:
            payload["llm_model_name"] = llm_model_name
        if llm_base_url is not None:
            payload["llm_base_url"] = llm_base_url
        if custom_instructions is not None:
            payload["custom_instructions"] = custom_instructions
        if deduplication_key is not None:
            payload["deduplication_key"] = deduplication_key
        return cls.from_server_data(cls._client.post(cls._create_path, data=payload).json())

    @classmethod
    def list(
        cls,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        deduplication_key: Optional[str] = None,
    ) -> List[MemorySpace]:
        """
        List the memory spaces accessible to the current user.

        .. versionadded:: v3.15

        .. versionchanged:: v3.17
            Added optional ``deduplication_key`` filter.

        Parameters
        ----------
        offset : int or None
            Optional number of events to skip from the beginning.
        limit : int or None
            Optional. The maximum number of items to return.
        deduplication_key : str or None
            Optional. Filter to the memory space with this exact deduplication key.

        Returns
        -------
        list of MemorySpace
            The available memory spaces.
        """
        params = {
            k: v
            for k, v in {
                "offset": offset,
                "limit": limit,
                "deduplication_key": deduplication_key,
            }.items()
            if v is not None
        }
        return [cls.from_server_data(item) for item in cls._client.get(cls._path, params=params).json()["items"]]

    @classmethod
    def get(cls, memory_space_id: str) -> MemorySpace:
        """
        Get a memory space by its ID.

        .. versionadded:: v3.15

        Parameters
        ----------
        memory_space_id : str
            The ID of the memory space to retrieve.

        Returns
        -------
        MemorySpace
            The requested memory space.
        """
        return cls.from_location(cls._url(memory_space_id))

    def update(
        self,
        description: object = _UNSET,
        llm_model_name: object = _UNSET,
        llm_base_url: object = _UNSET,
        custom_instructions: object = _UNSET,
    ) -> None:
        """
        Update the memory space.

        If called without arguments, there is no effect. Pass ``None`` to clear a field.

        .. versionadded:: v3.15

        Parameters
        ----------
        description : str or None
            The new description. Pass ``None`` to clear the existing description.
        llm_model_name : str or None
            The new LLM model name (maximum 200 characters). Pass ``None`` to clear an existing LLM.
            Non-reasoning models such as ``gpt-4o`` are recommended. Reasoning-capable models are
            significantly slower for fact extraction without producing meaningfully better results.
        llm_base_url : str or None
            The new chat API URL used for memory extraction.
            Pass ``None`` to clear and fall back to the DataRobot LLM gateway (the default).
            Set the URL only when the gateway does not work — for example, in air-gapped
            environments or when the required LLM model is not provided by the gateway and cannot be added.
        custom_instructions : str or None
            The new custom instructions (maximum 10 000 characters). Pass ``None`` to revert to
            the default memory extraction prompt.
        """
        payload, keep_attrs = _build_patch_payload(
            description=description,
            llm_model_name=llm_model_name,
            llm_base_url=llm_base_url,
            custom_instructions=custom_instructions,
        )

        if not payload:
            return

        updated = self.from_server_data(
            self._client.patch(self._url(self.id), data=payload, keep_attrs=keep_attrs).json()
        )

        _update_attrs(self, updated, ("description", "llm_model_name", "llm_base_url", "custom_instructions"))

    def delete(self) -> None:
        """
        Delete the memory space.

        .. versionadded:: v3.15
        """
        self._client.delete(self._url(self.id))


class Event(APIObject):
    """
    A single action or chat message within a :class:`Session`.

    Events are always scoped to a session. Use :meth:`Session.post_event`,
    :meth:`Session.events`, and :meth:`Session.update_event` to manage them.

    .. versionadded:: v3.15

    Attributes
    ----------
    body : dict or None
        The event payload.
    event_type : str or None
        An application-defined event-type label.
    emitter_type : str or None
        The type of entity that emitted the event (e.g., ``"agent"`` or ``"user"``).
    emitter_id : str or None
        The ID of the entity that generated the event.
    sequence_id : int or None
        The ordinal position of the event within its session.
    created_at : datetime.datetime or None
        The timestamp when the event was created.
    """

    _converter = t.Dict({
        t.Key("body", optional=True, default=None): t.Or(t.Dict({}).allow_extra("*"), t.Null),
        t.Key("event_type", optional=True, default=None): t.Or(String(allow_blank=True), t.Null),
        t.Key("emitter_type", optional=True, default=None): t.Or(String(allow_blank=True), t.Null),
        t.Key("emitter_id", optional=True, default=None): t.Or(String(allow_blank=True), t.Null),
        t.Key("sequence_id", optional=True, default=None): t.Or(Int(), t.Null),
        t.Key("created_at", optional=True, default=None): t.Or(t.Null, t.Call(parse_time)),
    }).ignore_extra("*")

    def __init__(
        self,
        body: Optional[Dict[str, Any]] = None,
        event_type: Optional[str] = None,
        emitter_type: Optional[str] = None,
        emitter_id: Optional[str] = None,
        sequence_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        self.body = body
        self.event_type = event_type
        self.emitter_type = emitter_type
        self.emitter_id = emitter_id
        self.sequence_id = sequence_id
        self.created_at = created_at

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(sequence_id={self.sequence_id})"


class Session(APIObject):
    """
    A chat session within a :class:`MemorySpace`.

    Sessions track conversations between participants and store the sequence of
    :class:`Event` objects that reflect either a single message or a state.

    .. versionadded:: v3.15

    Attributes
    ----------
    id : str
        The session ID.
    participants : list of str
        IDs of the participants in this session.
    description : str or None
        Optional. A human-readable description.
    metadata : dict or None
        Optional. Application-defined metadata.
    created_at : datetime.datetime
        The timestamp when the session was created.
    lifecycle_strategies : list of dict
        The lifecycle strategy configurations attached to this session. See the
        *Notes* section below for the dict shape, allowed values, and examples.
    version : int or None
        A monotonic counter incremented by the server on every successful update.
        Populated when the session is loaded from the server; ``None`` for
        manually constructed instances or older servers that do not return it.
        Used as the default ``If-Match`` precondition on :meth:`update`.
    deduplication_key : str or None
        Optional key supplied at create time to prevent duplicate sessions.
        Echoed back by the server and used to detect repeat session creations
        within the same memory space. ``None`` when the session was created
        without a key.
    memory_space_id : str or None
        The ID of the parent memory space. This value is set automatically.

    Notes
    -----
    **Lifecycle strategies**

    Each entry in ``lifecycle_strategies`` is a ``dict`` with three keys:

    - ``type`` (``str``, required) - one of:

        - ``"soft_delete"`` - mark the session as deleted when the trigger fires.
          Soft-deleted sessions are excluded from listings and their events
          become unreadable, but the record is retained for audit.
        - ``"extract_memories"`` - run memory extraction over the session's
          events and persist the resulting memories into the parent memory
          space when the trigger fires.

    - ``trigger`` (``dict``, required) - exactly one key, all integer-valued:

        - ``{"ttl": <seconds>}`` - elapsed time since session creation.
          ``1 <= ttl <= 63_072_000`` (2 years).
        - ``{"eventCount": <n>}`` - cumulative event count in the session.
          ``1 <= n <= 1_000_000``.
        - ``{"tokenCount": <n>}`` - cumulative token count over event message
          content. ``1 <= n <= 100_000_000``.
        - ``{"idle": <seconds>}`` - time since the last event (falls back to
          session creation time when there are no events).
          ``1 <= idle <= 63_072_000``.

    - ``opts`` (``dict`` or ``None``, optional) - strategy-specific options:

        - ``"soft_delete"`` - no options; pass ``None`` or omit.
        - ``"extract_memories"``:

            - ``softDelete`` (``bool``, default ``True``) - also soft-delete the
              session after extracting memories.
            - ``agentId`` (``str`` or ``None``) - agent ID attached to extracted
              memories.
            - ``metadata`` (``dict`` or ``None``) - metadata attached to extracted
              memories.

    When ``lifecycle_strategies`` is omitted or empty on :meth:`Session.create`,
    the server attaches a default ``"soft_delete"`` strategy with a 180-day TTL.
    A session may have at most 5 strategies.

    Examples
    --------
    .. code-block:: python

        # Delete the session after 7 days.
        [{"type": "soft_delete", "trigger": {"ttl": 604800}}]

        # Extract memories after 100 events; keep the session live afterwards.
        [{
            "type": "extract_memories",
            "trigger": {"eventCount": 100},
            "opts": {"softDelete": False, "agentId": "support-bot"},
        }]

        # Combine strategies: extract once idle for an hour, hard-cap with a 30-day TTL.
        [
            {"type": "extract_memories", "trigger": {"idle": 3600}},
            {"type": "soft_delete", "trigger": {"ttl": 2592000}},
        ]
    """

    _path = "memory/{}/sessions/"
    _events_path = "memory/{}/sessions/{}/events/"
    _events_batch_path = "memory/{}/sessions/{}/events/batch/"

    _converter = t.Dict({
        t.Key("id"): String(),
        t.Key("participants"): t.List(String()),
        t.Key("description", optional=True, default=None): t.Or(String(allow_blank=True), t.Null),
        t.Key("metadata", optional=True, default=None): t.Or(t.Dict({}).allow_extra("*"), t.Null),
        t.Key("created_at"): parse_time,
        t.Key("lifecycle_strategies"): t.List(t.Dict({}).allow_extra("*")),
        t.Key("version", optional=True, default=None): t.Or(Int(), t.Null),
        t.Key("deduplication_key", optional=True, default=None): t.Or(String(), t.Null),
    }).ignore_extra("*")

    def __init__(
        self,
        id: Optional[str] = None,
        participants: Optional[List[str]] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        created_at: Optional[datetime] = None,
        lifecycle_strategies: Optional[List[LifecycleStrategy]] = None,
        version: Optional[int] = None,
        deduplication_key: Optional[str] = None,
    ) -> None:
        self.id = id
        self.participants = participants
        self.description = description
        self.metadata = metadata
        self.created_at = created_at
        self.lifecycle_strategies = lifecycle_strategies
        self.version = version
        self.deduplication_key = deduplication_key
        self.memory_space_id: Optional[str] = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.id}')"

    @classmethod
    def _url(cls, memory_space_id: str, session_id: Optional[str] = None) -> str:
        base = cls._path.format(memory_space_id)
        return base if session_id is None else f"{base}{session_id}/"

    def _self_url(self) -> str:
        assert self.memory_space_id is not None
        return self._url(self.memory_space_id, self.id)

    def _events_url(self, sequence_id: Optional[int] = None) -> str:
        assert self.memory_space_id is not None
        base = self._events_path.format(self.memory_space_id, self.id)
        return base if sequence_id is None else f"{base}{sequence_id}/"

    def _events_batch_url(self) -> str:
        assert self.memory_space_id is not None
        return self._events_batch_path.format(self.memory_space_id, self.id)

    def _set_context(self, memory_space_id: str) -> Session:
        self.memory_space_id = memory_space_id
        return self

    @classmethod
    def create(
        cls,
        memory_space_id: str,
        participants: List[str],
        lifecycle_strategies: Optional[List[LifecycleStrategy]] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        deduplication_key: Optional[str] = None,
    ) -> Session:
        """
        Create a new session in a memory space.

        Every session must have at least one lifecycle strategy. If ``lifecycle_strategies``
        is not provided or is an empty list, the server attaches a default strategy.

        .. versionadded:: v3.15

        .. versionchanged:: v3.17
            Added optional ``deduplication_key`` parameter to prevent duplicate
            session creations.

        Parameters
        ----------
        memory_space_id : str
            The ID of the memory space to create the session in.
        participants : list of str
            IDs of the participants in the session.
        lifecycle_strategies : list of dict or None
            Optional. The lifecycle strategy configurations. Each item is a
            ``dict`` with ``type``, ``trigger``, and optional ``opts`` keys -
            see the *Notes* section on :class:`Session` for the full shape,
            allowed values, and working examples. When omitted or empty, the
            server attaches a default ``"soft_delete"`` strategy with a 180-day
            TTL. At most 5 strategies may be attached to a session.
        description : str or None
            Optional. A human-readable description.
        metadata : dict or None
            Optional. Application-defined metadata.
        deduplication_key : str or None
            Optional. A 1-72 character key that prevents duplicate sessions. If
            a live session with the same key already exists in this memory
            space, the server returns ``409 Conflict`` and the SDK raises
            :class:`~datarobot.errors.MemorySessionDeduplicationError`, which
            carries ``existing_session_id`` so callers can adopt the winning
            session. ``None`` keys do not collide; the same key may be reused
            across different memory spaces; soft-deleting a session frees the key.

        Returns
        -------
        Session
            The newly created session.

        Raises
        ------
        MemorySessionDeduplicationError
            When ``deduplication_key`` is supplied and a live session with the
            same key already exists in this memory space.
        """
        payload = {
            "participants": participants,
            "lifecycle_strategies": lifecycle_strategies or [],
        }

        if description is not None:
            payload["description"] = description

        if metadata is not None:
            payload["metadata"] = metadata

        if deduplication_key is not None:
            payload["deduplication_key"] = deduplication_key

        data = cls._client.post(cls._url(memory_space_id), data=payload).json()
        return cls.from_server_data(data)._set_context(memory_space_id)

    @classmethod
    def list(
        cls,
        memory_space_id: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        participants: Optional[List[str]] = None,
        description: Optional[str] = None,
    ) -> List[Session]:
        """
        List the sessions within a single memory space.

        .. versionadded:: v3.15

        Parameters
        ----------
        memory_space_id : str
            The ID of the memory space.
        offset : int or None
            Optional number of events to skip from the beginning.
        limit : int or None
            Optional maximum number of items to return.
        participants : list of str or None
            Optional filter by participant IDs.
        description : str or None
            Optional filter by description.

        Returns
        -------
        list of Session
            The matching sessions.
        """
        params = {
            k: v
            for k, v in {
                "offset": offset,
                "limit": limit,
                "participants": participants,
                "description": description,
            }.items()
            if v is not None
        }

        data = cls._client.get(cls._url(memory_space_id), params=params).json()["items"]
        return [cls.from_server_data(item)._set_context(memory_space_id) for item in data]

    @classmethod
    def get(cls, memory_space_id: str, session_id: str) -> Session:
        """
        Get a session by its ID.

        .. versionadded:: v3.15

        Parameters
        ----------
        memory_space_id : str
            The ID of the memory space.
        session_id : str
            The ID of the session to retrieve.

        Returns
        -------
        Session
            The requested session.
        """
        return cls.from_location(cls._url(memory_space_id, session_id))._set_context(memory_space_id)

    def update(
        self,
        description: object = _UNSET,
        metadata: object = _UNSET,
        if_match: object = _UNSET,
    ) -> None:
        """
        Update the session.

        If called without arguments, there is no effect. Pass ``None`` to clear a field.

        By default the SDK uses ``version`` (set by a prior load) as an
        optimistic-concurrency precondition. If the server's stored version no
        longer matches, it returns ``409`` (surfaced as
        :class:`datarobot.errors.ClientError`). The caller is expected to reload
        the session via :meth:`get` and retry.

        .. versionadded:: v3.15

        Parameters
        ----------
        description : str or None
            The new description. Pass ``None`` to clear.
        metadata : dict or None
            The new metadata. Pass ``None`` to clear.
        if_match : int or None
            Optimistic-concurrency precondition. When omitted, the SDK uses
            ``version`` automatically. Pass ``None`` to opt out (legacy
            last-writer-wins). Pass an integer to override the version.
        """
        payload, keep_attrs = _build_patch_payload(description=description, metadata=metadata)

        if not payload:
            return

        effective_if_match = self.version if if_match is _UNSET else if_match

        kwargs: Dict[str, Any] = {"data": payload, "keep_attrs": keep_attrs}
        if effective_if_match is not None:
            kwargs["headers"] = {"If-Match": f'"{effective_if_match}"'}

        updated = self.from_server_data(self._client.patch(self._self_url(), **kwargs).json())

        _update_attrs(self, updated, ("description", "metadata", "version"))

    def delete(self) -> None:
        """
        Delete the session.

        .. versionadded:: v3.15
        """
        self._client.delete(self._self_url())

    def post_event(
        self,
        body: Dict[str, Any],
        emitter: Emitter,
        event_type: Optional[str] = None,
    ) -> Event:
        """
        Create an event in this session.

        .. versionadded:: v3.15

        Parameters
        ----------
        body : dict
            The event payload.
        emitter : dict
            Identifies the entity that produced the event, which
            typically contains ``"type"`` and ``"id"`` keys.
        event_type : str or None
            Optional. An application-defined event-type label.

        Returns
        -------
        Event
            The newly created event.
        """
        payload: Dict[str, Any] = {"body": body, "emitter": emitter}

        if event_type is not None:
            payload["type"] = event_type

        data = self._client.post(self._events_url(), data=payload).json()
        return Event.from_server_data(data)

    def events(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        last_n: Optional[int] = None,
        event_type: Optional[str] = None,
    ) -> List[Event]:
        """
        List the events in this session.

        Provide either ``offset`` or ``last_n``, but not both.

        .. versionadded:: v3.15

        Parameters
        ----------
        offset : int or None
            Optional . The number of events to skip from the beginning.
        limit : int or None
            Optional. The maximum number of events to return.
        last_n : int or None
            Optional. The number of most recent events to return. This value is mutually exclusive
            with ``offset``.
        event_type : str or None
            Optional. An event-type label.

        Returns
        -------
        list of Event
            The matching events.
        """
        assert_single_or_zero_parameter(("offset", "last_n"), offset, last_n)

        params = {
            k: v
            for k, v in {"offset": offset, "limit": limit, "last_n": last_n, "event_type": event_type}.items()
            if v is not None
        }

        data = self._client.get(self._events_url(), params=params).json()["items"]
        return [Event.from_server_data(item) for item in data]

    def update_event(
        self,
        sequence_id: int,
        body: object = _UNSET,
        event_type: object = _UNSET,
        emitter: object = _UNSET,
        created_at: Optional[datetime] = None,
    ) -> Optional[Event]:
        """
        Update an event by its sequence ID.

        When ``created_at`` is provided, the server uses it for optimistic concurrency
        control. Specifically, if the event has been modified since that timestamp, the server rejects
        the update. The caller must handle this error and reload the event before retrying.

        .. versionadded:: v3.15

        Parameters
        ----------
        sequence_id : int
            The ordinal position of the event to update.
        body : dict or None
            The new event payload.
        event_type : str or None
            The new event-type label.
        emitter : dict or None
            The new emitter information; the type of entity that emitted the event (e.g., ``"agent"`` or ``"user"``).
        created_at : datetime.datetime or None
            Optional timestamp for optimistic concurrency control.

        Returns
        -------
        Event or None
            The updated event, or ``None`` if called with no changes.
        """
        payload, keep_attrs = _build_patch_payload(body=body, type=event_type, emitter=emitter)
        if not payload:
            return None

        params = {}
        if created_at is not None:
            params.update({"createdAt": created_at.isoformat()})

        data = self._client.patch(
            self._events_url(sequence_id), data=payload, params=params, keep_attrs=keep_attrs
        ).json()
        return Event.from_server_data(data)

    def post_events(self, events: List[NewEvent]) -> List[Event]:
        """
        Append a batch of events to this session atomically.

        The entire batch is appended in a single transaction; if any item fails
        validation, no events are created. Server-side limit is 200 events per
        request.

        .. versionadded:: v3.17

        Parameters
        ----------
        events : list of NewEvent
            Events to append, in order. Each item requires ``body`` and
            ``emitter`` and may include an ``event_type``.

        Returns
        -------
        list of Event
            The newly created events, in the same order as the input.
        """
        payload_events: List[Dict[str, Any]] = []
        for event in events:
            item: Dict[str, Any] = {"body": event["body"], "emitter": event["emitter"]}
            event_type = event.get("event_type")
            if event_type is not None:
                item["type"] = event_type
            payload_events.append(item)

        data = self._client.post(self._events_batch_url(), data={"events": payload_events}).json()
        return [Event.from_server_data(item) for item in data["items"]]

    def update_events(self, events: List[EventUpdate]) -> List[Event]:
        """
        Update a batch of events in this session atomically.

        Each item identifies the target event by ``sequence_id`` and must set
        at least one of ``body``, ``event_type``, ``emitter``. Duplicate
        ``sequence_id`` values are rejected. The whole batch is applied in a
        single transaction; any failure rolls back every change. Server-side
        limit is 200 events per request.

        ``created_at`` is per-item optimistic concurrency: if provided and the
        target event has been modified since that timestamp, the update is
        rejected and the batch rolls back.

        .. versionadded:: v3.17

        Parameters
        ----------
        events : list of EventUpdate
            Events to update. Each item requires ``sequence_id`` and at least
            one of ``body``, ``event_type``, ``emitter``. ``created_at`` is
            an optional per-item version check.

        Returns
        -------
        list of Event
            The updated events.
        """
        payload_events: List[Dict[str, Any]] = []
        for event in events:
            item: Dict[str, Any] = {"sequence_id": event["sequence_id"]}
            if "body" in event:
                item["body"] = event["body"]
            if "event_type" in event:
                item["type"] = event["event_type"]
            if "emitter" in event:
                item["emitter"] = event["emitter"]
            created_at = event.get("created_at")
            if created_at is not None:
                item["created_at"] = created_at
            payload_events.append(item)

        data = self._client.patch(self._events_batch_url(), data={"events": payload_events}).json()
        return [Event.from_server_data(item) for item in data["items"]]
