from typing import overload
from enum import IntEnum
import typing

import QuantConnect
import QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages
import QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.TradierBrokerageModel


class ExtendedMarketHoursTradingNotSupportedOutsideExtendedSessionAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects Tradier brokerage model rejections where an extended-hours order was placed outside a valid extended trading session."""

    @property
    def issue(self) -> str:
        ...

    @property
    def weight(self) -> int:
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """This codeEntityType is protected."""
        ...

    def solutions(self, language: QuantConnect.Language) -> typing.List[str]:
        """This codeEntityType is protected."""
        ...


class SellShortOrderLastPriceBelow5Analysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects Tradier brokerage model rejections where a short-sell order was placed for a security priced below $5."""

    @property
    def issue(self) -> str:
        ...

    @property
    def weight(self) -> int:
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """This codeEntityType is protected."""
        ...

    def solutions(self, _: QuantConnect.Language) -> typing.List[str]:
        """This codeEntityType is protected."""
        ...


class TradierUnsupportedSecurityTypeAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects Tradier brokerage model rejections where the security type is not supported (only Equity and Option are supported)."""

    @property
    def issue(self) -> str:
        ...

    @property
    def weight(self) -> int:
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """This codeEntityType is protected."""
        ...

    def solutions(self, _: QuantConnect.Language) -> typing.List[str]:
        """This codeEntityType is protected."""
        ...


class ShortOrderIsGtcAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects Tradier brokerage model rejections where a GTC time-in-force was used for a short-sell order."""

    @property
    def issue(self) -> str:
        ...

    @property
    def weight(self) -> int:
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """This codeEntityType is protected."""
        ...

    def solutions(self, _: QuantConnect.Language) -> typing.List[str]:
        """This codeEntityType is protected."""
        ...


class UnsupportedTimeInForceTypeAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects Tradier brokerage model rejections where the time-in-force type is not Day or GTC."""

    @property
    def issue(self) -> str:
        ...

    @property
    def weight(self) -> int:
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """This codeEntityType is protected."""
        ...

    def solutions(self, _: QuantConnect.Language) -> typing.List[str]:
        """This codeEntityType is protected."""
        ...


class IncorrectOrderQuantityAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects Tradier brokerage model rejections where the order quantity is not a whole number."""

    @property
    def issue(self) -> str:
        ...

    @property
    def weight(self) -> int:
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """This codeEntityType is protected."""
        ...

    def solutions(self, _: QuantConnect.Language) -> typing.List[str]:
        """This codeEntityType is protected."""
        ...


