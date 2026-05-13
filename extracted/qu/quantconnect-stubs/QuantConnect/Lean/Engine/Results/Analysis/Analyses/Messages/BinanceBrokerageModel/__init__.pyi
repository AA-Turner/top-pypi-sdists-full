from typing import overload
from enum import IntEnum
import typing

import QuantConnect
import QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages
import QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.BinanceBrokerageModel


class UnsupportedOrderTypeWithLinkToSupportedTypesAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects Binance brokerage model rejections due to an unsupported order type."""

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


