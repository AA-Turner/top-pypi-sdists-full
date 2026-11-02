"""Product Python model generation from captured schemas, separate from REST SDK emission."""

from labqoat.json_document import JsonValue
from labqoat.schema_codegen.record_graph import RecordGraph


class SchemaGenerator:
    """Generate typed public constructors and decoding without importing authored Python."""

    @staticmethod
    def generate(schema: dict[str, JsonValue], name: str) -> dict[str, str]:
        """Return deterministic class-per-file sources and declaration-only package re-exports."""
        return RecordGraph(schema, name).generate()
