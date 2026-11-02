"""
`seq.Secret` — a user's BYO credential, referenced by NAME ONLY.

WHY name-only, no value parameter anywhere in the API: the credential value must be physically unable to
enter the SDK process or the registration. `from_name` is the only constructor and it takes a bare name;
the value lives in the platform's secret store and is injected into the policy subprocess at worker bootstrap
.
This is "not taking the value and dropping it" - the plaintext never has an argument to arrive through.



"""
from __future__ import annotations

from sequence_base.contract import SecretRef

from seq.errors import PolicyDefinitionError







_MAX_SECRET_NAME_LEN = 64
_ALLOWED = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-")


def _validate_secret_name(name: str) -> str:
    """Reject any name that could steer the `user-<uid>-<name>` path or is otherwise unusable.

    WHY here (in the constructor) and not at deploy: the name is the only thing we accept, so it is the
    only thing to validate, and rejecting at authoring time is the readable-error contract.
    """

    if not isinstance(name, str):
        raise PolicyDefinitionError(f"secret name must be a str, got {type(name).__name__}")

    if not name:
        raise PolicyDefinitionError("secret name must be non-empty")

    if len(name) > _MAX_SECRET_NAME_LEN:
        raise PolicyDefinitionError(
            f"secret name too long ({len(name)} > {_MAX_SECRET_NAME_LEN})"
        )


    if name in (".", ".."):
        raise PolicyDefinitionError(f"secret name {name!r} is a path-traversal segment")


    bad = sorted(set(name) - _ALLOWED)
    if bad:
        raise PolicyDefinitionError(
            f"secret name {name!r} contains disallowed character(s) {bad}; "
            "use only letters, digits, '.', '_', '-'"
        )

    if ".." in name:
        raise PolicyDefinitionError(f"secret name {name!r} contains '..' (path traversal)")
    return name


class Secret:
    """A handle to a user secret. Carries only the name; `_ref()` lowers it to the wire `SecretRef`."""

    __slots__ = ("name",)

    def __init__(self, name: str) -> None:

        self.name = _validate_secret_name(name)

    @classmethod
    def from_name(cls, name: str) -> "Secret":
        """The ONLY constructor exposed to users — name-only by design.

        WHY no `from_dict`/value form: see the module docstring — a value parameter is exactly what must
        not exist, so it does not.
        """
        return cls(name)

    def _ref(self) -> SecretRef:
        """Lower to the shared wire type the registration stores (name only)."""
        return SecretRef(name=self.name)

    def __repr__(self) -> str:
        return f"Secret.from_name({self.name!r})"
