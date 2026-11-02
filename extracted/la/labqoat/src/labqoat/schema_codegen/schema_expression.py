"""Source expressions for exact canonical captured-schema validators."""

from labqoat.schemas.schema_document import SchemaDocument


class SchemaExpression:
    """Keep schema literals deterministic and shared across records and structural union branches."""

    @staticmethod
    def render(schema: SchemaDocument) -> str:
        """Reconstruct only trusted schema data through the ordinary validation boundary."""
        return f"SchemaDocument.capture(JsonDocument.expect_dict(Identity.decode({schema.canonical.decode()!r})))"
