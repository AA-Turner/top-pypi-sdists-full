from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass
class MatrxPattern:
    """
    Represents a parsed MATRX pattern with its components.
    
    Attributes:
        table: The table name or group identifier (first component)
        column: The column or identifier name (second component)
        value: The actual value (third component)
        fields: Optional fields/attribute to retrieve (fourth component)
        raw: The original raw pattern string
        start_pos: Starting position in the source text
        end_pos: Ending position in the source text
    """
    table: str
    column: str
    value: str
    fields: str | None = None
    raw: str = ""
    start_pos: int = 0
    end_pos: int = 0
    
    def __repr__(self):
        field_str = f", fields='{self.fields}'" if self.fields else ""
        return f"MatrxPattern(table='{self.table}', column='{self.column}', value='{self.value}'{field_str})"

class MatrxPatternParser:
    """
    A robust parser for MATRX patterns in text.
    
    Pattern format: 
        Basic: <<MATRX>><<TABLE>><<COLUMN>>value<</MATRX>>
        With fields: <<MATRX>><<TABLE>><<COLUMN>>value<<FIELDS>>attribute<</MATRX>>
    
    Examples:
        - <<MATRX>><<CONTENT_BLOCKS>><<BLOCK_ID>>sample-thinking<</MATRX>>
        - <<MATRX>><<CONTENT_BLOCKS>><<ID>>uuid<<FIELDS>>template<</MATRX>>
        - <<MATRX>><<USERS>><<EMAIL>>user@example.com<<FIELDS>>name<</MATRX>>
    """
    
    # Regex pattern to match MATRX structures with optional fields
    # Matches: <<MATRX>><<...>><<...>>...<<FIELDS>>...<</MATRX>> or <<MATRX>><<...>><<...>>...<</MATRX>>
    PATTERN = re.compile(
        r'<<MATRX>>'                    # Opening tag
        r'<<([^>]+)>>'                  # First component (table/group) - captured
        r'<<([^>]+)>>'                  # Second component (column/identifier) - captured
        r'((?:(?!<<FIELDS>>|<</MATRX>>).)*?)'  # Third component (value) - captured, stops at <<FIELDS>> or <</MATRX>>
        r'(?:<<FIELDS>>([^<]+))?'        # Optional fourth component (fields) - captured
        r'<</MATRX>>',                  # Closing tag
        re.DOTALL | re.MULTILINE        # Allow newlines in values
    )
    
    @classmethod
    def parse(cls, text: str) -> list[MatrxPattern]:
        """
        Parse all MATRX patterns found in the given text.
        
        Args:
            text: The text to search for MATRX patterns
            
        Returns:
            List of MatrxPattern objects, one for each pattern found
        """
        patterns = []
        
        for match in cls.PATTERN.finditer(text):
            table = match.group(1).strip()
            column = match.group(2).strip()
            value = match.group(3).strip()
            fields = match.group(4).strip() if match.group(4) else None
            
            pattern = MatrxPattern(
                table=table,
                column=column,
                value=value,
                fields=fields,
                raw=match.group(0),
                start_pos=match.start(),
                end_pos=match.end()
            )
            patterns.append(pattern)
        
        return patterns
    
    @classmethod
    def parse_simple_variables(
        cls, 
        text: str, 
        variable_config: dict[str, dict[str, Any]]
    ) -> list[MatrxPattern]:
        """
        Parse simple {{variable_name}} patterns and convert them to MatrxPattern objects.
        
        Args:
            text: The text to search for {{variable}} patterns
            variable_config: Dictionary mapping variable names to their MATRX components.
                Each variable should have: table, column, value, and optionally fields.
                Field can be a string, list, or comma-separated string.
                
                Example:
                    {
                        "user_name": {
                            "table": "USERS",
                            "column": "ID", 
                            "value": "123",
                            "fields": "name"
                        },
                        "user_info": {
                            "table": "USERS",
                            "column": "ID",
                            "value": "123", 
                            "fields": ["name", "email"]  # or "name,email"
                        }
                    }
        
        Returns:
            List of MatrxPattern objects for variables found in the config.
            Variables not in config are ignored and left as-is.
        """
        patterns = []
        
        # Pattern to match {{variable_name}}
        simple_pattern = re.compile(r'\{\{([a-zA-Z_][a-zA-Z0-9_]*)\}\}')
        
        for match in simple_pattern.finditer(text):
            var_name = match.group(1)
            
            # Only process if variable is in config
            if var_name not in variable_config:
                continue
            
            config = variable_config[var_name]
            
            # Extract required components
            table = config.get("table", "")
            column = config.get("column", "")
            value = config.get("value", "")
            field_value = config.get("fields", None)
            
            # Normalize fields to string format (matching existing system)
            # The fields can be: None, string, list, or comma-separated string
            if field_value is None:
                fields = None
            elif isinstance(field_value, list):
                # Convert list to comma-separated string
                fields = ",".join(str(f).strip() for f in field_value)
            else:
                # Already a string (single field or comma-separated)
                fields = str(field_value).strip()
            
            pattern = MatrxPattern(
                table=table,
                column=column,
                value=value,
                fields=fields,
                raw=match.group(0),  # The full {{variable_name}}
                start_pos=match.start(),
                end_pos=match.end()
            )
            patterns.append(pattern)
        
        return patterns
    
    @classmethod
    def find_first(cls, text: str) -> MatrxPattern | None:
        """
        Find the first MATRX pattern in the text.
        
        Args:
            text: The text to search
            
        Returns:
            First MatrxPattern found, or None if no pattern exists
        """
        patterns = cls.parse(text)
        return patterns[0] if patterns else None
    
    @classmethod
    def parse_all(
        cls, 
        text: str, 
        variable_config: dict[str, dict[str, Any]] | None = None
    ) -> list[MatrxPattern]:
        """
        Parse both complex MATRX patterns and simple {{variable}} patterns.
        
        Args:
            text: The text to search
            variable_config: Optional config for simple variables. If None, only complex patterns are found.
        
        Returns:
            Combined list of all patterns, sorted by position in text
        """
        patterns = cls.parse(text)
        
        if variable_config:
            simple_patterns = cls.parse_simple_variables(text, variable_config)
            patterns.extend(simple_patterns)
            # Sort by start position to maintain text order
            patterns.sort(key=lambda p: p.start_pos)
        
        return patterns
    
    @classmethod
    def replace_patterns(cls, text: str, replacement_func) -> str:
        """
        Replace all MATRX patterns in text using a replacement function.
        
        Args:
            text: The text containing MATRX patterns
            replacement_func: A function that takes a MatrxPattern and returns a replacement string
            
        Returns:
            Text with all patterns replaced
        """
        patterns = cls.parse(text)
        
        # Replace from end to start to preserve positions
        result = text
        for pattern in reversed(patterns):
            replacement = replacement_func(pattern)
            result = result[:pattern.start_pos] + replacement + result[pattern.end_pos:]
        
        return result

# Quick-check compiled regex: avoids importing MatrxFetcher when no patterns exist.
_MATRX_QUICK_CHECK = re.compile(r'<<MATRX>>')

def resolve_matrx_patterns(text: str) -> str:
    """
    Single entry point: parse all <<MATRX>> patterns in *text* and replace
    them with content fetched from the database.

    Returns the original string unchanged if no patterns are found (fast path).
    """
    if not _MATRX_QUICK_CHECK.search(text):
        return text

    from matrx_ai.instructions.matrx_fetcher import MatrxFetcher

    patterns = MatrxPatternParser.parse(text)
    if not patterns:
        return text

    return MatrxFetcher.process_text_with_patterns(text, patterns)
