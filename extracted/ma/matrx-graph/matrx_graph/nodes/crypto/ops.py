"""Hash + random-identifier nodes.

These are convenience primitives, not authentication tools. Use
``secrets`` / a real KMS for anything cryptographic; these exist so a
workflow can compute a stable dedupe key (``crypto.hash``) or a fresh
id (``crypto.uuid``) without reaching for ``data.transform``.
"""

from __future__ import annotations

import hashlib
import secrets
import string
import time
import uuid
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.content_ir.model import KindModel
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success

_HASH_ALGOS = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
    "blake2b": hashlib.blake2b,
}


# ---------------------------------------------------------------------------
# crypto.hash
# ---------------------------------------------------------------------------


class HashInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(description="Text to hash.")


class HashConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    algorithm: Literal["md5", "sha1", "sha256", "sha512", "blake2b"] = Field(
        default="sha256",
        description="Hash algorithm — md5, sha1, sha256, sha512, or blake2b.",
    )
    truncate: int = Field(
        default=0,
        ge=0,
        le=128,
        description="If >0, truncate hex digest to this many characters.",
    )
    uppercase: bool = Field(default=False, description="Upper-case the hex digest.")


class HashOutput(KindModel, kind="hash_result"):
    digest: str = Field(description="The hex digest of the input text.")
    algorithm: str = Field(description="The algorithm used to compute the digest.")
    truncated_to: int | None = Field(
        default=None,
        description=(
            "Set when the digest was shortened. A truncated digest no longer "
            "verifies against ``algorithm``, and the payload must say so — a "
            "12-character value labeled 'sha256' invites a verification that "
            "can only fail."
        ),
    )


class HashExecutor:
    """Compute a content hash. Determinism-PURE, so safe to cache on resume."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="crypto.hash",
        category=NodeCategory.DATA,
        display_name="Data Fingerprint",
        description="Create a short, unique fingerprint of a piece of data.",
        input_schema=HashInput,
        output_schema=HashOutput,
        config_schema=HashConfig,
        input_kind="text",
        output_kind="hash_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="fingerprint",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: HashInput,
        config: HashConfig,
    ) -> NodeResult[HashOutput]:
        _ = ctx
        algo = _HASH_ALGOS[config.algorithm]
        digest = algo(inputs.text.encode("utf-8")).hexdigest()
        if config.truncate > 0:
            digest = digest[: config.truncate]
        if config.uppercase:
            digest = digest.upper()
        return success(
            HashOutput(
                digest=digest,
                algorithm=config.algorithm,
                truncated_to=config.truncate or None,
            )
        )


# ---------------------------------------------------------------------------
# crypto.uuid
# ---------------------------------------------------------------------------


class UuidInput(BaseModel):
    model_config = ConfigDict(extra="forbid")


class UuidConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: Literal[4, 7] = Field(
        default=4,
        description=("UUID version. 4 = random; 7 = timestamp-ordered (RFC 9562)."),
    )
    hyphenated: bool = Field(
        default=True,
        description="Include hyphens (8-4-4-4-12) vs a plain 32-character hex string.",
    )


class UuidOutput(KindModel, kind="uuid_value"):
    uuid: str = Field(description="The generated UUID string.")
    version: int | None = Field(
        default=None,
        description=(
            "The UUID version actually produced (4 = random, 7 = "
            "timestamp-ordered). Read from the value itself, not from the "
            "request — a consumer relying on time-ordering must be able to "
            "SEE that it got it."
        ),
    )


def _uuid7() -> uuid.UUID:
    """RFC 9562 UUIDv7 — 48-bit millisecond timestamp, then randomness.

    ``uuid.uuid7`` is a Python 3.14 addition; this package targets 3.13, where
    it does NOT exist. The previous ``getattr(uuid, "uuid7", uuid.uuid4)()``
    therefore fell through to uuid4 on every run of the actual runtime, so a
    workflow author who chose "timestamp-ordered" to get database insert
    locality silently received random ids — no error, no signal, and the
    payload did not even say which version it got.
    """
    ms = time.time_ns() // 1_000_000
    rand_a = secrets.randbits(12)
    rand_b = secrets.randbits(62)
    value = (ms & 0xFFFF_FFFF_FFFF) << 80
    value |= 0x7 << 76  # version
    value |= rand_a << 64
    value |= 0b10 << 62  # variant
    value |= rand_b
    return uuid.UUID(int=value)


class UuidExecutor:
    """Generate a fresh UUID. Non-deterministic — re-runs on resume."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="crypto.uuid",
        category=NodeCategory.DATA,
        display_name="Unique ID",
        description="Generate a unique ID.",
        input_schema=UuidInput,
        output_schema=UuidOutput,
        config_schema=UuidConfig,
        output_kind="uuid_value",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
        re_execute_on_resume=True,
        icon="fingerprint",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: UuidInput,
        config: UuidConfig,
    ) -> NodeResult[UuidOutput]:
        _ = ctx, inputs
        if config.version == 7:
            # Prefer the stdlib on 3.14+; our own RFC 9562 build below is what
            # makes the promise true on 3.13.
            generator = getattr(uuid, "uuid7", _uuid7)
            u = generator()
        else:
            u = uuid.uuid4()
        text = str(u) if config.hyphenated else u.hex
        return success(UuidOutput(uuid=text, version=u.version))


# ---------------------------------------------------------------------------
# crypto.random_string
# ---------------------------------------------------------------------------


_ALPHABETS = {
    "alphanumeric": string.ascii_letters + string.digits,
    "lowercase": string.ascii_lowercase,
    "uppercase": string.ascii_uppercase,
    "digits": string.digits,
    "url_safe": string.ascii_letters + string.digits + "-_",
    "hex": string.hexdigits.lower()[:16],
}


class RandomStringInput(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RandomStringConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    length: int = Field(default=16, ge=1, le=512, description="Number of characters to generate.")
    alphabet: Literal["alphanumeric", "lowercase", "uppercase", "digits", "url_safe", "hex"] = (
        Field(
            default="alphanumeric",
            description="Character set to draw from — alphanumeric, lowercase, "
            "uppercase, digits, url_safe, or hex.",
        )
    )


class RandomStringOutput(KindModel, kind="random_string_result"):
    value: str = Field(description="The generated random string.")


class RandomStringExecutor:
    """Generate a random string from a named alphabet. Uses ``secrets`` internally."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="crypto.random_string",
        category=NodeCategory.DATA,
        display_name="Random Text",
        description="Generate random characters, useful for codes and passwords.",
        input_schema=RandomStringInput,
        output_schema=RandomStringOutput,
        config_schema=RandomStringConfig,
        output_kind="random_string_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
        re_execute_on_resume=True,
        icon="shuffle",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: RandomStringInput,
        config: RandomStringConfig,
    ) -> NodeResult[RandomStringOutput]:
        _ = ctx, inputs
        alphabet = _ALPHABETS[config.alphabet]
        value = "".join(secrets.choice(alphabet) for _ in range(config.length))
        return success(RandomStringOutput(value=value))
