r"""Contain a generic LLM agent configuration."""

from __future__ import annotations

__all__ = ["AgentConfig"]

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin
from coola.hashing import hash_string
from coola.utils.string import truncate_str

from zenpyre.utils.config import ExtraFieldsConfig

if TYPE_CHECKING:
    from typing import Self

    from zenpyre.chat_models import BaseChatModelConfig


@dataclass(frozen=True)
class AgentConfig(ExtraFieldsConfig, MultilineDisplayMixin):
    r"""A generic LLM agent configuration.

    Subclass this to add provider- or agent-specific parameters as
    typed fields (e.g. ``max_tokens`` for OpenAI, ``top_k`` for
    Anthropic). Since this class is frozen, subclasses must also be
    frozen dataclasses. Additional fields do not need a default value:
    ``extra`` is declared keyword-only on
    :class:`~zenpyre.utils.config.ExtraFieldsConfig`, so it doesn't
    force subclass fields into a particular ordering.

    Fields added by subclasses are picked up automatically by
    :meth:`to_kwargs` (and therefore :meth:`cache_key`) via
    introspection; you don't need to override either method just to
    add a field.

    One thing subclasses *do* need to restate: ``@dataclass(frozen=True)``
    auto-generates a fresh ``__hash__`` for every dataclass-decorated
    class unless that class's own body defines ``__hash__`` — merely
    inheriting one does not suppress the override, and the
    auto-generated version would try to hash the unhashable ``extra``
    field. Any further subclass should include a delegating method of
    its own::

        def __hash__(self) -> int:
            return AgentConfig.__hash__(self)

    (A plain assignment like ``__hash__ = AgentConfig.__hash__`` also
    suppresses the auto-generation, but static type checkers such as
    pyright flag it as an "ambiguous base class override" because the
    inferred ``self`` type comes from the parent method rather than the
    subclass; the delegating-method form above avoids that.)

    Attributes:
        chat_model: The chat model configuration (see
            :class:`~zenpyre.chat_models.BaseChatModelConfig`) used by
            this agent.
        system_prompt: The system prompt that instructs the LLM on its
            role and task.
        system_prompt_id: An identifier for ``system_prompt``. Defaults
            to ``hash_string(system_prompt)`` when constructed via
            :meth:`from_kwargs` and left unset, so configs built from
            the same prompt text get the same id without callers
            needing to compute it themselves.
        extra: Additional keyword arguments merged into
            :meth:`to_kwargs`. Must not contain a key that collides
            with any of this config's own field names (including ones
            declared by a subclass).

    Example:
        ```pycon
        >>> from dataclasses import dataclass
        >>> from zenpyre.agents import AgentConfig
        >>> from zenpyre.chat_models import ChatModelConfig
        >>> config = AgentConfig.from_kwargs(
        ...     chat_model=ChatModelConfig(model="openai:gpt-4o"),
        ...     system_prompt="You are helpful.",
        ...     max_tokens=1024,
        ... )

        ```
    """

    chat_model: BaseChatModelConfig
    system_prompt: str
    system_prompt_id: str

    @classmethod
    def from_kwargs(
        cls,
        chat_model: BaseChatModelConfig,
        system_prompt: str,
        system_prompt_id: str | None = None,
        **kwargs: Any,
    ) -> Self:
        """Construct an :class:`AgentConfig` from a chat model
        configuration, a system prompt, and arbitrary keyword arguments.

        A convenience alternative to the regular constructor's
        ``extra={...}`` dict, letting callers pass extra fields
        directly as keyword arguments instead:
        ``AgentConfig.from_kwargs(chat_model, "You are helpful.", max_retries=3)``
        is equivalent to
        ``AgentConfig(chat_model=chat_model, system_prompt="You are helpful.", extra={"max_retries": 3})``.

        Args:
            chat_model: The chat model configuration used by this
                agent.
            system_prompt: The system prompt that instructs the LLM on
                its role and task.
            system_prompt_id: An identifier for ``system_prompt``. If
                ``None`` (the default), it is derived automatically via
                ``hash_string(system_prompt)``.
            **kwargs: Additional keyword arguments, stored as
                ``extra``.

        Returns:
            A new :class:`AgentConfig`.

        Raises:
            TypeError: If ``kwargs`` contains a ``"chat_model"``,
                ``"system_prompt"``, or ``"system_prompt_id"`` key,
                since Python's own argument binding intercepts it as a
                duplicate value for the corresponding explicit
                parameter before this method's body ever runs. For
                example, ``from_kwargs(cm, "prompt", **{"chat_model":
                other})`` raises ``TypeError: got multiple values for
                argument 'chat_model'``. (This is distinct from the
                ``ValueError`` the regular constructor raises for the
                same conceptual conflict when ``extra`` is passed
                directly as an already-built dict; that path isn't
                reachable through this method.)

        Example:
            ```pycon
            >>> from zenpyre.agents import AgentConfig
            >>> from zenpyre.chat_models import ChatModelConfig
            >>> cfg = AgentConfig.from_kwargs(
            ...     ChatModelConfig(model="gpt-4"), "You are helpful.", max_retries=3
            ... )
            >>> cfg.to_kwargs()["max_retries"]
            3

            ```
        """
        if system_prompt_id is None:
            system_prompt_id = hash_string(system_prompt, length=64)
        return super().from_kwargs(
            chat_model=chat_model,
            system_prompt=system_prompt,
            system_prompt_id=system_prompt_id,
            **kwargs,
        )

    def _get_repr_kwargs(self) -> dict[str, Any]:
        """Return the kwargs used by :class:`MultilineDisplayMixin` to
        build this config's repr, with ``system_prompt`` truncated so
        long prompts don't blow up the display.

        Returns:
            The same dict as :meth:`to_kwargs`, with ``system_prompt``
                replaced by a truncated version.
        """
        kwargs = self.to_kwargs()
        kwargs["system_prompt"] = truncate_str(kwargs["system_prompt"])
        return kwargs

    def __hash__(self) -> int:
        # @dataclass(frozen=True) auto-generates a fresh __hash__ for
        # every dataclass-decorated class unless __hash__ is already
        # present in that class's own body — merely inheriting one
        # does not suppress the override. Delegating here (rather than
        # repeating its logic) keeps ExtraFieldsConfig.__hash__ the
        # single authoritative implementation.
        return ExtraFieldsConfig.__hash__(self)
