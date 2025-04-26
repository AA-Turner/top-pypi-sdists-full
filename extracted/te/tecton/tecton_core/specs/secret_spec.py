from typeguard import typechecked

from tecton_core.specs import utils
from tecton_proto.common import secret__client_pb2 as secret_pb2


@utils.frozen_strict
class SecretSpec:
    """Base class for secret spec."""

    scope: str
    key: str
    is_local: bool

    @classmethod
    @typechecked
    def from_proto(cls, proto: secret_pb2.SecretReference) -> "SecretSpec":
        return cls(
            scope=proto.scope,
            key=proto.key,
            is_local=proto.is_local,
        )
