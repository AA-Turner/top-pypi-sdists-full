"""Snowflake dialect extension for sqlglot.

Subclasses the upstream Snowflake dialect via its documented extension mechanism
to work around parser limitations that block lineage extraction. Each override is
scoped as tightly as possible and its root cause is documented inline so the
override can be retired when the upstream issue is fixed.
"""

from sqlglot import exp
from sqlglot.dialects.snowflake import Snowflake
from sqlglot.tokens import TokenType


class CollateSnowflake(Snowflake):
    """Snowflake dialect with COPY-parameter parsing patched for qualified names."""

    class Parser(Snowflake.Parser):
        def _parse_copy_parameters(self):
            """Qualified unquoted values like ``FILE_FORMAT = LOAD.CSV_FORMAT`` fail on
            the upstream parser because ``LOAD`` is a reserved ``TokenType`` that
            ``_parse_field`` does not compose into a dotted reference, leaving
            ``CopyParameter.this`` unset. Reproduced on sqlglot 29.0.1 and 30.4.3.

            Behaviour matches upstream ``_parse_copy_parameters`` except the
            ``FILE_FORMAT`` branch also chains any trailing ``DOT``-separated
            segments via ``_parse_id_var(any_token=True)``.
            """
            sep = TokenType.COMMA if self.dialect.COPY_PARAMS_ARE_CSV else None
            options = []
            while self._curr and not self._match(TokenType.R_PAREN, advance=False):
                option = self._parse_var(any_token=True)
                prev = self._prev.text.upper()

                self._match(TokenType.EQ)
                self._match(TokenType.ALIAS)

                param = self.expression(exp.CopyParameter, this=option)

                if prev in self.COPY_INTO_VARLEN_OPTIONS and self._match(
                    TokenType.L_PAREN, advance=False
                ):
                    param.set("expressions", self._parse_wrapped_options())
                elif prev == "FILE_FORMAT":
                    expr = self._parse_field() or self._parse_id_var(any_token=True)
                    while self._match(TokenType.DOT):
                        part = self._parse_id_var(any_token=True)
                        if part is None:
                            break
                        expr = self.expression(exp.Dot, this=expr, expression=part)
                    param.set("expression", expr)
                elif (
                    prev == "FORMAT"
                    and self._prev.token_type == TokenType.ALIAS
                    and self._match_texts(("AVRO", "JSON"))
                ):
                    param.set("this", exp.var(f"FORMAT AS {self._prev.text.upper()}"))
                    param.set("expression", self._parse_field())
                else:
                    param.set(
                        "expression",
                        self._parse_unquoted_field() or self._parse_bracket(),
                    )

                options.append(param)

                if sep:
                    self._match(sep)

            return options
