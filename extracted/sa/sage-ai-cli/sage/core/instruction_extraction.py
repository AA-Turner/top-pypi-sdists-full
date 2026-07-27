"""
Instruction Extraction for SAGE - Items 91-105 from Roadmap P0.

This module provides logic to extract explicit instructions from user requests.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class ExtractedInstruction:
    """An explicit instruction extracted from user request."""

    content: str
    type: str  # "include", "exclude", "format", "constraint"
    priority: int = 1  # 1-5, 1 is highest


class InstructionExtractor:
    """
    Items 91-105: Extracts explicit instructions from user requests.
    """

    # Item 91-92: Instruction markers
    MARKERS: ClassVar[list[str]] = [
        r"make\s+sure",
        r"ensure\s+that",
        r"you\s+must",
        r"please\s+",
        r"don't\s+",
        r"do\s+not\s+",
        r"always\s+",
        r"never\s+",
        r"strictly\s+",
    ]

    def extract(self, request: str) -> list[ExtractedInstruction]:
        """
        Items 91-105: Extract explicit instructions from request text.
        """
        instructions = []
        
        # Split request into sentences
        sentences = re.split(r"[.!?]\s*", request)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Check for markers
            has_marker = any(re.search(marker, sentence, re.IGNORECASE) for marker in self.MARKERS)
            
            if has_marker:
                # Determine type
                inst_type = "constraint"
                if any(kw in sentence.lower() for kw in ["don't", "do not", "never"]):
                    inst_type = "exclude"
                elif any(kw in sentence.lower() for kw in ["include", "contain", "show"]):
                    inst_type = "include"
                elif any(kw in sentence.lower() for kw in ["format", "list", "table"]):
                    inst_type = "format"
                    
                instructions.append(ExtractedInstruction(content=sentence, type=inst_type))
                
        return instructions
