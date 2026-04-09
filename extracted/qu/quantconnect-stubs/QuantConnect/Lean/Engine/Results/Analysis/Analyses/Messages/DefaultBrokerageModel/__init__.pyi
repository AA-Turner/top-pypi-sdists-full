from typing import overload
from enum import IntEnum
import typing

import QuantConnect
import QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages
import QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.DefaultBrokerageModel


class UnsupportedCrossZeroByOrderTypeAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects brokerage model rejections where the order type does not support crossing zero (flipping position direction in a single order)."""

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


class UnsupportedMarketOnOpenOrdersForFutureAndFutureOptionsAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects brokerage model rejections where a MarketOnOpen order was placed for a Futures or Future Options contract."""

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


class NoDataForSymbolAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects brokerage model rejections where no data is available for the ordered security."""

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


class InvalidOrderSizeAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects brokerage model rejections where the order value (price × |quantity|) is below the security's minimum order size."""

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


class InvalidOrderQuantityAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects brokerage model rejections where the order quantity (in quote currency) is below the security's minimum order size."""

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


class UnsupportedMarketOnOpenOrderTimeAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """
    Detects brokerage model rejections where a MarketOnOpen order was placed without the required
    minimum time gap before the intended fill bar.
    """

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


class OrderUpdateNotSupportedAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects brokerage model rejections where the brokerage does not support updating orders."""

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


class UnsupportedTimeInForceAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects brokerage model rejections where the order's time-in-force setting is not supported."""

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


class UnsupportedOrderTypeAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects brokerage model rejections where the submitted or updated order type is not supported."""

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


class UnsupportedSecurityTypeAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects brokerage model rejections where the security type is not supported."""

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


class UnsupportedUpdateQuantityOrderAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects brokerage model rejections where the order type does not allow its quantity to be updated."""

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


class UnsupportedCrossZeroOrderUpdateAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects brokerage model rejections where an order update would cause the position to cross zero."""

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


