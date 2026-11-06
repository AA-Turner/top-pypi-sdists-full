"""Where the secrets of an agent come from.

An agent declares each secret once, by name, in ``Agent(secrets={name: origin})``. Destinations,
such as a sandbox's header bindings, pick a secret by that name and never hold its value. The
name has environment-variable syntax, so a self-hosted worker can take any secret from its shell.

The origins are secrets the customer owns. A connector's token never leaves the Connectors
Gateway, so it is not an origin.
"""

from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, field_validator

from mistralai.vibe_agents.agents_client import api_models


def validate_secret_name(name: str) -> str:
    """Return ``name`` when it can name a secret, or raise ``ValueError``."""

    if (problem := api_models.env_var_name_error(name)) is not None:
        raise ValueError(f"Secret name {name!r} {problem}")
    return name


class MistralSecret(BaseModel):
    """A secret of the Mistral Secret Manager.

    Build it with ``MistralSecret.workspace(NAME)``, or leave the reference out with
    ``MistralSecret()`` and bind it at deploy time with
    ``agents deploy --secret-binding NAME=secret:workspace:...``, which also overrides a reference.
    ``worker_env=True`` also sets the secret as an environment variable where your Python tools
    run, so they can read it; without it, the secret reaches only the destinations that name it.
    """

    # A value in `ref` may be a secret pasted by mistake, so no validation error may print the input.
    model_config = ConfigDict(extra="forbid", frozen=True, hide_input_in_errors=True)

    kind: Literal["mistral"] = "mistral"
    """Always ``"mistral"``: the Mistral Secret Manager."""
    ref: str | None = None
    """The secret's reference, such as ``"secret:workspace:NAME"``. ``None`` leaves it to
    ``agents deploy --secret-binding``."""
    worker_env: bool = False
    """Whether the secret is also an environment variable where your Python tools run."""

    @classmethod
    def workspace(cls, name: str, *, worker_env: bool = False) -> Self:
        """The workspace secret ``name`` of the Secret Manager.

        Args:
            name: The secret's name in the workspace.
            worker_env: Whether the secret is also an environment variable where your Python tools run.
        """

        return cls(ref=f"secret:workspace:{name}", worker_env=worker_env)

    @field_validator("ref")
    @classmethod
    def _validate_ref(cls, ref: str | None) -> str | None:
        # The rejected value is never echoed: it may be a secret pasted by mistake.
        if ref is not None and not api_models.is_valid_secret_reference(ref):
            raise ValueError(f"MistralSecret ref {api_models.SECRET_REFERENCE_ERROR}")
        return ref


# A union once a second origin exists, such as an external vault.
type SecretOrigin = MistralSecret


__all__ = [
    "MistralSecret",
    "SecretOrigin",
    "validate_secret_name",
]
