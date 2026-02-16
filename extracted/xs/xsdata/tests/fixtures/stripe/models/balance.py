from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(order=True, frozen=True, kw_only=True)
class ConnectReserved:
    class Meta:
        name = "connect_reserved"

    amount: int = field(
        metadata={
            "type": "Element",
        }
    )
    currency: str = field(
        metadata={
            "type": "Element",
        }
    )


@dataclass(order=True, frozen=True, kw_only=True)
class SourceTypes:
    class Meta:
        name = "source_types"

    bank_account: int = field(
        metadata={
            "type": "Element",
        }
    )
    card: int = field(
        metadata={
            "type": "Element",
        }
    )


@dataclass(order=True, frozen=True, kw_only=True)
class Available:
    class Meta:
        name = "available"

    amount: int = field(
        metadata={
            "type": "Element",
        }
    )
    currency: str = field(
        metadata={
            "type": "Element",
        }
    )
    source_types: SourceTypes = field(
        metadata={
            "type": "Element",
        }
    )


@dataclass(order=True, frozen=True, kw_only=True)
class Pending:
    class Meta:
        name = "pending"

    amount: int = field(
        metadata={
            "type": "Element",
        }
    )
    currency: str = field(
        metadata={
            "type": "Element",
        }
    )
    source_types: SourceTypes = field(
        metadata={
            "type": "Element",
        }
    )


@dataclass(order=True, frozen=True, kw_only=True)
class Balance:
    class Meta:
        name = "balance"

    object_value: str = field(
        metadata={
            "name": "object",
            "type": "Element",
        }
    )
    available: tuple[Available, ...] = field(
        default_factory=tuple,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    connect_reserved: tuple[ConnectReserved, ...] = field(
        default_factory=tuple,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    livemode: bool = field(
        metadata={
            "type": "Element",
        }
    )
    pending: tuple[Pending, ...] = field(
        default_factory=tuple,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
