from typing import overload
from enum import IntEnum
import typing

import QuantConnect
import QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages
import QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.CoinbaseBrokerageModel


class StopMarketOrdersNoLongerSupportedAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects Coinbase brokerage model rejections due to Stop Market orders, which are no longer supported."""

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


