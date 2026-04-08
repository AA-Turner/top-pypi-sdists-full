from typing import overload
from enum import IntEnum
import typing

import QuantConnect
import QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages
import QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.AlpacaBrokerageModel


class TradingOutsideRegularHoursNotSupportedAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects Alpaca brokerage model rejections due to an attempt to trade outside regular market hours."""

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


