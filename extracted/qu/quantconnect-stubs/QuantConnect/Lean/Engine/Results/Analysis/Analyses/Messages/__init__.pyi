from typing import overload
from enum import IntEnum
import abc
import typing

import QuantConnect
import QuantConnect.Lean.Engine.Results.Analysis
import QuantConnect.Lean.Engine.Results.Analysis.Analyses
import QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages
import System.Text.RegularExpressions


class MessageAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis, metaclass=abc.ABCMeta):
    """
    Abstract base class for analyses that detect issues by scanning log or order event messages
    for one or more expected text fragments.
    """

    @property
    def expected_message_text(self) -> typing.List[str]:
        """
        The text fragments a message must all contain (case-insensitive) to identify the issue.
        Ignored when expected_message_pattern is set.
        
        
        This Property is protected.
        """
        ...

    @property
    def expected_message_pattern(self) -> System.Text.RegularExpressions.Regex:
        """
        Optional regex that identifies the issue message, taking precedence over
        expected_message_text. Use it for messages with variable parts fragments
        cannot pin down, like method names formatted by algorithm language.
        
        
        This Property is protected.
        """
        ...

    def match(self, messages: typing.Sequence[str], expected_messages: typing.List[str]) -> typing.Sequence[str]:
        """
        Returns messages from messages that contain all strings in expected_messages
        (case-insensitive).
        
        
        This Class is protected.
        """
        ...

    @overload
    def run(self, parameters: QuantConnect.Lean.Engine.Results.Analysis.ResultsAnalysisRunParameters) -> typing.Sequence[QuantConnect.Analysis]:
        ...

    @overload
    def run(self, messages: typing.Sequence[str], language: QuantConnect.Language) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Runs the analysis by scanning messages for the expected pattern or
        text fragments and returns results with solutions when matches are found.
        """
        ...

    def solutions(self, language: QuantConnect.Language) -> typing.List[str]:
        """This Class is protected."""
        ...


