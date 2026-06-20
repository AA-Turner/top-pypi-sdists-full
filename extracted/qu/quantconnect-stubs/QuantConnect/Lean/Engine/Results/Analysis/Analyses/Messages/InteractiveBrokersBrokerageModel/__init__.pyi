from typing import overload
from enum import IntEnum
import typing

import QuantConnect
import QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages
import QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.InteractiveBrokersBrokerageModel


class InvalidForexOrderSizeAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects Interactive Brokers brokerage model rejections where a Forex order is below the minimum required size."""

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


class UnsupportedExerciseForIndexAndCashSettledOptionsAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """
    Detects Interactive Brokers brokerage model rejections where a manual exercise was attempted
    for index or cash-settled options, which IB handles automatically at expiry.
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


