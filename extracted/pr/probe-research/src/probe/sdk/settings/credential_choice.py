"""Which `/v1` credential a client reads with when it holds both a personal token and a team API key (D13, O4).

An explicit choice outranks an ambient one: an argument beats the environment, which beats the config file.
So a server given a key (argument or `PROBE_SERVICE_TOKEN`) never reads as a person whose login sits in this
box's config file. Two credentials at the same explicit rank are a mistake to name, never a silent pick.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class CredentialRank(IntEnum):
    """Where a credential came from; lower outranks higher."""

    ARGUMENT = 0
    ENVIRONMENT = 1
    CONFIG_FILE = 2


@dataclass(frozen=True, slots=True)
class CredentialChoice:
    """Whether `/v1` sends the team key rather than the personal token, and, for a tie, the error to raise on
    use. The token itself stays on `Settings`: sign-in and identity checks read the person's login."""

    should_use_service_token: bool = False
    conflict: str | None = None


_CONFLICTS = {
    CredentialRank.ARGUMENT: "both token= and service_token= were passed; pass one",
    CredentialRank.ENVIRONMENT: (
        "PROBE_TOKEN and PROBE_SERVICE_TOKEN are both set; unset one. PROBE_TOKEN reads as you, "
        "PROBE_SERVICE_TOKEN (a team API key) reads as the team's key"
    ),
}


def choose_api_credential(
    token: str | None,
    token_rank: CredentialRank | None,
    service_token: str | None,
    service_token_rank: CredentialRank | None,
) -> CredentialChoice:
    """Send the personal token unless a team key given more explicitly outranks it. A tie as an argument or in
    the environment is a conflict; a tie in the config file sends the token, as before."""
    if not token or not service_token or token_rank is None or service_token_rank is None:
        return CredentialChoice()
    if service_token_rank < token_rank:
        return CredentialChoice(should_use_service_token=True)
    if service_token_rank == token_rank and service_token_rank in _CONFLICTS:
        return CredentialChoice(conflict=_CONFLICTS[service_token_rank])
    return CredentialChoice()


def rank_of(argument: str | None, environment: str | None, config_file: str | None) -> CredentialRank | None:
    """Where the resolved value came from, by the usual precedence."""
    if argument:
        return CredentialRank.ARGUMENT
    if environment:
        return CredentialRank.ENVIRONMENT
    if config_file:
        return CredentialRank.CONFIG_FILE
    return None
