from typing import overload
from enum import IntEnum
import typing

import QuantConnect
import QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages
import QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.TradingTechnologiesBrokerageModel


class InvalidStopLimitOrderLimitPriceAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """
    Detects Trading Technologies brokerage model rejections where a stop-limit order's limit price
    is on the wrong side of the stop price.
    """

    @property
    def issue(self) -> str:
        ...

    @property
    def weight(self) -> int:
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """This Property is protected."""
        ...

    def solutions(self, _: QuantConnect.Language) -> typing.List[str]:
        """This Class is protected."""
        ...


class InvalidStopLimitOrderPriceAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """
    Detects Trading Technologies brokerage model rejections where a stop-limit order's stop price
    is on the wrong side of the current market price.
    """

    @property
    def issue(self) -> str:
        ...

    @property
    def weight(self) -> int:
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """This Property is protected."""
        ...

    def solutions(self, _: QuantConnect.Language) -> typing.List[str]:
        """This Class is protected."""
        ...


class InvalidStopMarketOrderPriceAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """
    Detects Trading Technologies brokerage model rejections where a stop-market order's stop price
    is on the wrong side of the current market price.
    """

    @property
    def issue(self) -> str:
        ...

    @property
    def weight(self) -> int:
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """This Property is protected."""
        ...

    def solutions(self, _: QuantConnect.Language) -> typing.List[str]:
        """This Class is protected."""
        ...


