"""
Simple example demonstrating the {{variable}} pattern parser.
Run this to test the new parse_simple_variables() method.
"""

from matrx_utils import clear_terminal, vcprint

from matrx_ai.instructions.pattern_parser import MatrxPatternParser

clear_terminal()

# Sample text with both types of patterns
text = """
Hello {{user_name}}, your role is {{user_role}}.

Here's a complex pattern:
<<MATRX>><<CONTENT_BLOCKS>><<BLOCK_ID>>flashcards<</MATRX>>

Your email: {{user_email}}
Some other {{unknown_var}} that's not in config (should be ignored).
"""

# Configuration for simple variables
variable_config = {
    "user_name": {"table": "USERS", "column": "ID", "value": "123", "fields": "name"},
    "user_role": {"table": "USERS", "column": "ID", "value": "123", "fields": "role"},
    "user_email": {"table": "USERS", "column": "ID", "value": "123", "fields": "email"},
    # Test with list of fields
    "user_info": {
        "table": "USERS",
        "column": "ID",
        "value": "123",
        "fields": ["name", "email", "role"],  # Will be converted to "name,email,role"
    },
}

all_patterns = MatrxPatternParser.parse_all(text, variable_config)
vcprint(all_patterns, "All Patterns", color="magenta")
