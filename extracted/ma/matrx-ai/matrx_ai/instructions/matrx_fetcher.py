"""
MATRX Data Fetcher

A robust, table-specific data fetching system that works with MATRX patterns.
Each table has its own method with appropriate defaults and post-processing.
"""
from __future__ import annotations

import uuid
from typing import Any

from matrx_ai.db._registry import get_model


def _get_RenderDefinition() -> Any:
    """Resolve the host-injected RenderDefinition model lazily.

    (skill.render_definition — the canonical block table; public.content_blocks
    was retired by the 2026-08 render-blocks canonicalization. The wire syntax
    ``<<MATRX>><<CONTENT_BLOCKS>>…`` keeps its durable table token.)

    Deferred to call time so importing this module never triggers
    DBNotConfiguredError. ``instructions/`` is on matrx-ai's EAGER import path
    (pulled in by unified_config / executor / unified_client), so it MUST stay
    import-safe in a minimal environment per the package contract — a
    module-level ``get_model(...)`` here broke ``import matrx_ai.*`` before
    ``configure()`` ran. Mirrors ``content_blocks_manager._get_RenderDefinition``.
    """
    return get_model("RenderDefinition")


def is_valid_uuid(value: str) -> bool:
    """Check if a string is a valid UUID."""
    try:
        uuid.UUID(str(value))
        return True
    except (ValueError, AttributeError):
        return False

class MatrxFetcher:
    """
    Fetches data from database based on table-specific configurations.
    
    Each table has a dedicated method that knows:
    - The appropriate Model to use
    - Default field to return
    - How to handle single vs multiple results
    - Any special post-processing needed
    """
    
    # Table-specific configurations. ``model`` is the registry NAME (resolved
    # lazily via get_model at fetch time), never a model class captured at
    # import — capturing the class here would require configure() before this
    # module could even load.
    TABLE_CONFIGS = {
        "CONTENT_BLOCKS": {
            "model": "RenderDefinition",
            "default_field": "template",
            "supported_fields": ["template", "label", "block_id", "category_id"],
        },
        # Add more tables as needed
        # "USERS": {
        #     "model": Users,
        #     "default_field": "email",
        #     "supported_fields": ["email", "name", "username"],
        # },
    }
    
    @classmethod
    def fetch(
        cls,
        table: str,
        column: str,
        value: str,
        fields: str | None = None,
    ) -> str:
        """
        Core fetch method that routes to table-specific handlers.
        
        Args:
            table: Table name (e.g., "CONTENT_BLOCKS")
            column: Column name to filter by (e.g., "BLOCK_ID", "ID")
            value: Value to search for
            fields: Optional field(s) to retrieve. If None, uses table default.
                   Can be comma-separated for multiple fields.
        
        Returns:
            Fetched text content
        """
        table = table.upper()
        
        # Route to table-specific method if it exists
        method_name = f"fetch_{table.lower()}"
        if hasattr(cls, method_name):
            method = getattr(cls, method_name)
            return method(column, value, fields)
        
        # Fallback to generic fetch
        return cls._fetch_generic(table, column, value, fields)
    
    @classmethod
    def fetch_content_blocks(
        cls,
        column: str,
        value: str,
        fields: str | None = None,
    ) -> str:
        """
        Fetch ContentBlocks with intelligent field handling.
        
        Args:
            column: Column to filter by (e.g., "BLOCK_ID", "ID", "CATEGORY_ID")
            value: Value to search for
            fields: Field(s) to retrieve. Defaults to "template".
                   Can be comma-separated like "template,label"
        
        Returns:
            Concatenated text from all matching records
        """
        # Normalize column name
        column = column.lower()
        
        # Get field(s) to retrieve
        all_fields = cls._parse_fields(fields, default="template")
        
        # Build query
        query_params = {column: value}
        results = _get_RenderDefinition().filter_sync(**query_params)
        
        # Extract and concatenate content
        output_parts = []
        for result in results:
            for field_name in all_fields:
                attr_value = getattr(result, field_name, "")
                if attr_value:  # Only add if there's content
                    output_parts.append(str(attr_value))
        
        return "\n\n".join(output_parts)
    
    @classmethod
    def _fetch_generic(
        cls,
        table: str,
        column: str,
        value: str,
        fields: str | None = None,
    ) -> str:
        """
        Generic fetch method for tables without specific handlers.
        
        This is a fallback that uses TABLE_CONFIGS.
        """
        config = cls.TABLE_CONFIGS.get(table)
        if not config:
            return f"[ERROR: Table '{table}' not configured]"

        model = get_model(config["model"])
        default_field = config["default_field"]
        
        # Get field(s) to retrieve
        all_fields = cls._parse_fields(fields, default=default_field)
        
        # Build query
        column = column.lower()
        query_params = {column: value}
        results = model.filter_sync(**query_params)
        
        # Extract and concatenate content
        output_parts = []
        for result in results:
            for field_name in all_fields:
                attr_value = getattr(result, field_name, "")
                if attr_value:
                    output_parts.append(str(attr_value))
        
        return "\n\n".join(output_parts)
    
    @classmethod
    def _parse_fields(cls, fields: str | None, default: str) -> list[str]:
        """
        Parse fields specification into a list of field names.
        
        Args:
            fields: Fields specification (None, single field, or comma-separated)
            default: Default fields to use if fields is None
        
        Returns:
            List of fields names
        """
        if not fields:
            return [default]
        
        # Handle comma-separated fields
        if "," in fields:
            return [f.strip() for f in fields.split(",") if f.strip()]
        
        return [fields.strip()]
    
    @classmethod
    def process_text_with_patterns(cls, text: str, patterns: list[Any]) -> str:
        """
        Replace all MATRX patterns in text with fetched content.
        
        Args:
            text: Original text containing MATRX patterns
            patterns: List of MatrxPattern objects from parser
        
        Returns:
            Text with all patterns replaced with fetched content
        """
        # Process patterns in reverse order to maintain string positions
        result = text
        for pattern in reversed(patterns):
            try:
                fetched = cls.fetch(
                    pattern.table,
                    pattern.column,
                    pattern.value,
                    pattern.fields,
                )
                result = result[:pattern.start_pos] + fetched + result[pattern.end_pos:]
            except Exception as e:
                error_msg = f"[FETCH_ERROR: {str(e)}]"
                result = result[:pattern.start_pos] + error_msg + result[pattern.end_pos:]
        
        return result

if __name__ == "__main__":
    from matrx_utils import clear_terminal, vcprint

    from matrx_ai.instructions.tests.variable_recognition_test import MatrxPatternParser
    
    clear_terminal()
    
    test_text = """
Here is a content block (default field - template):
---------------------
<<MATRX>><<CONTENT_BLOCKS>><<BLOCK_ID>>flashcards<</MATRX>>
---------------------

With single field (label only):
---------------------
<<MATRX>><<CONTENT_BLOCKS>><<BLOCK_ID>>flashcards<<FIELDS>>label<</MATRX>>
---------------------

With multiple fields (label,block_id):
---------------------
<<MATRX>><<CONTENT_BLOCKS>><<BLOCK_ID>>flashcards<<FIELDS>>label,template<</MATRX>>
---------------------
"""
    
    patterns = MatrxPatternParser.parse(test_text)
    vcprint(patterns, "Patterns", color="green")
    result = MatrxFetcher.process_text_with_patterns(test_text, patterns)
    vcprint(result, "Processed Text", color="cyan")

