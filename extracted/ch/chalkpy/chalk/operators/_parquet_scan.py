from __future__ import annotations

from typing_extensions import final

from chalk import StaticOperator


@final
class ParquetScanOperator(StaticOperator):
    _chalk__operator_name = StaticOperator._chalk__operator_prefix + "parquet_scan"

    def __init__(self, files: tuple[str, ...], column_names: tuple[str, ...], *, aws_role_arn: str | None = None):
        super().__init__(files=files, column_names=column_names, parent=None)
        self.column_names = column_names
        self.files = files
        self.aws_role_arn = aws_role_arn
