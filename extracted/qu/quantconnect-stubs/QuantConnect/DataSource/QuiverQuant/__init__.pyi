from typing import overload
from enum import IntEnum
import typing

import QuantConnect.DataSource.QuiverQuant
import QuantConnect.Orders
import System


class OwnershipType(IntEnum):
    """SEC Form 4 direct or indirect ownership classification"""

    UNKNOWN = 0
    """Default value used when no ownership flag is provided or the value is unrecognized"""

    DIRECT = 1
    """D - Direct ownership of the security by the reporting person"""

    INDIRECT = 2
    """I - Indirect ownership of the security (e.g., through a trust or family member)"""


class TransactionCode(IntEnum):
    """SEC Form 4 transaction codes (see https://www.sec.gov/files/forms-3-4-5.pdf)"""

    SALE = -1
    """S - Open market or private sale of non-derivative or derivative security"""

    OTHER = 1
    """
    J - Other acquisition or disposition (describe transaction). Also used as the
    default value when no transaction code is provided.
    """

    PURCHASE = 2
    """P - Open market or private purchase of non-derivative or derivative security"""

    VOLUNTARY_REPORT = 3
    """V - Transaction voluntarily reported earlier than required"""

    GRANT_OR_AWARD = 4
    """A - Grant, award, or other acquisition pursuant to Rule 16b-3(d)"""

    DISPOSITION_TO_ISSUER = 5
    """D - Disposition to the issuer of issuer equity securities pursuant to Rule 16b-3(e)"""

    EXERCISE_PAYMENT_WITH_SECURITIES = 6
    """
    F - Payment of exercise price or tax liability by delivering or withholding securities
    incident to the receipt, exercise, or vesting of a security issued in accordance with Rule 16b-3
    """

    DISCRETIONARY_TRANSACTION = 7
    """I - Discretionary transaction in accordance with Rule 16b-3(f)"""

    EXERCISE_OR_CONVERSION_EXEMPT = 8
    """M - Exercise or conversion of derivative security exempted pursuant to Rule 16b-3"""

    CONVERSION_OF_DERIVATIVE = 9
    """C - Conversion of derivative security"""

    SHORT_DERIVATIVE_EXPIRATION = 10
    """E - Expiration of short derivative position"""

    LONG_DERIVATIVE_EXPIRATION_WITH_VALUE = 11
    """H - Expiration (or cancellation) of long derivative position with value received"""

    OUT_OF_MONEY_EXERCISE = 12
    """O - Exercise of out-of-the-money derivative security"""

    IN_MONEY_EXERCISE = 13
    """X - Exercise of in-the-money or at-the-money derivative security"""

    GIFT = 14
    """G - Bona fide gift"""

    SMALL_ACQUISITION = 15
    """L - Small acquisition under Rule 16a-6"""

    ACQUISITION_BY_WILL = 16
    """W - Acquisition or disposition by will or the laws of descent and distribution"""

    VOTING_TRUST_DEPOSIT = 17
    """Z - Deposit into or withdrawal from voting trust"""

    EQUITY_SWAP = 18
    """K - Transaction in equity swap or instrument with similar characteristics"""

    TENDER_DISPOSITION = 19
    """U - Disposition pursuant to a tender of shares in a change of control transaction"""


class AcquiredDisposedCode(IntEnum):
    """SEC Form 4 indicator of whether the transaction was an acquisition or a disposal"""

    UNKNOWN = 0
    """Default value used when no acquired/disposed flag is provided or the value is unrecognized"""

    ACQUIRED = 1
    """A - Share acquisition"""

    DISPOSED = 2
    """D - Share disposal"""


class QuiverQuantCsvExtensions(System.Object):
    """
    Compact CSV serialization helpers for Quiver enums and primitives. Keeps the
    on-disk format short (single SEC letters, 0/1 booleans, -1/0/1 trade direction)
    while preserving full enum names in code.
    """

    @staticmethod
    def to_acquired_disposed_code(value: str) -> QuantConnect.DataSource.QuiverQuant.AcquiredDisposedCode:
        ...

    @staticmethod
    @overload
    def to_csv(value: QuantConnect.DataSource.QuiverQuant.TransactionCode) -> str:
        ...

    @staticmethod
    @overload
    def to_csv(value: QuantConnect.DataSource.QuiverQuant.OwnershipType) -> str:
        ...

    @staticmethod
    @overload
    def to_csv(value: QuantConnect.DataSource.QuiverQuant.AcquiredDisposedCode) -> str:
        ...

    @staticmethod
    @overload
    def to_csv(value: typing.Optional[bool]) -> str:
        ...

    @staticmethod
    @overload
    def to_csv(value: QuantConnect.Orders.OrderDirection) -> str:
        ...

    @staticmethod
    def to_nullable_bool(value: str) -> typing.Optional[bool]:
        ...

    @staticmethod
    def to_order_direction(value: str) -> QuantConnect.Orders.OrderDirection:
        ...

    @staticmethod
    def to_ownership_type(value: str) -> QuantConnect.DataSource.QuiverQuant.OwnershipType:
        ...

    @staticmethod
    def to_transaction_code(value: str) -> QuantConnect.DataSource.QuiverQuant.TransactionCode:
        ...


