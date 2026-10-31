"""THE one input declaration — every agent variable, workflow input and step form field.

The JSON Schema in ``schema/`` is the source of truth; ``generated`` is its Pydantic twin
(``scripts/generate_input_declaration.py``); TypeScript ships as
``@ai-matrx/content-ir/input-declaration``. Never declare this shape anywhere else
(``scripts/check_one_input_declaration.py``).
"""

from matrx_ai.agents.input_declaration.generated import (
    VariableComponent,
    VariableContextBinding,
    VariableDefinition,
    VariableRecordBinding,
)
from matrx_ai.agents.input_declaration.source import (
    INPUT_DECLARATION_KINDS,
    SCHEMA_BASE_URI,
    SCHEMA_DIR,
    all_source_schemas,
    media_variable_types,
    schema_uri,
    source_schema,
    variable_component_types,
)
from matrx_ai.agents.input_declaration.upgrade import (
    normalize_component,
    stamp_binding,
    upgrade_agent_variable,
    upgrade_workflow_input,
)

__all__ = [
    "INPUT_DECLARATION_KINDS",
    "SCHEMA_BASE_URI",
    "SCHEMA_DIR",
    "VariableComponent",
    "VariableContextBinding",
    "VariableDefinition",
    "VariableRecordBinding",
    "all_source_schemas",
    "media_variable_types",
    "normalize_component",
    "schema_uri",
    "source_schema",
    "stamp_binding",
    "upgrade_agent_variable",
    "upgrade_workflow_input",
    "variable_component_types",
]
