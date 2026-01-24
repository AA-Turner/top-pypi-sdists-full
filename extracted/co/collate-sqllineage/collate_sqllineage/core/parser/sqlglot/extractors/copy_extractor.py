from sqlglot import exp
from sqlglot.expressions import Expression

from collate_sqllineage.core.models import AnalyzerContext, Path
from collate_sqllineage.core.parser.sqlglot.extractors.lineage_holder_extractor import (
    LineageHolderExtractor,
)
from collate_sqllineage.core.parser.sqlglot.models import (
    SqlGlotSubQueryLineageHolder,
    SqlGlotTable,
)


class CopyExtractor(LineageHolderExtractor):
    """
    COPY statement lineage extractor for sqlglot (Postgres, Redshift, Snowflake).
    Handles:
    - COPY table FROM 'path'
    - COPY INTO table FROM 'path'
    """

    SUPPORTED_STMT_TYPES = ["copy_statement"]

    def __init__(self, dialect: str):
        super().__init__(dialect)

    def extract(
        self,
        statement: Expression,
        context: AnalyzerContext,
        is_sub_query: bool = False,
    ) -> SqlGlotSubQueryLineageHolder:
        """
        Extract lineage for COPY statements.
        :param statement: a sqlglot Expression
        :param context: 'AnalyzerContext'
        :param is_sub_query: determine if the statement is a subquery
        :return 'SqlGlotSubQueryLineageHolder' object
        """
        holder = self._init_holder(context)

        if isinstance(statement, exp.Copy):
            # COPY target table
            if statement.this and isinstance(statement.this, exp.Table):
                holder.add_write(SqlGlotTable.of(statement.this))

            # COPY source files (paths)
            if hasattr(statement, "args") and "files" in statement.args:
                files = statement.args["files"]
                if files:
                    for file_expr in files:
                        # Handle direct Literal (Postgres/Redshift: COPY FROM 'path')
                        if isinstance(file_expr, exp.Literal):
                            path_str = file_expr.this
                            if path_str:
                                holder.add_read(Path(path_str))
                        # Handle Table with Literal (Snowflake: COPY INTO FROM 'path')
                        elif isinstance(file_expr, exp.Table):
                            if isinstance(file_expr.this, exp.Literal):
                                path_str = file_expr.this.this
                                if path_str:
                                    holder.add_read(Path(path_str))

        return holder
