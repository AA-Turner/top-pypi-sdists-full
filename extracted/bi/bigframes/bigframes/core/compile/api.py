# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

from typing import Optional, Sequence, Tuple, TYPE_CHECKING

import google.cloud.bigquery as bigquery

from bigframes.core import rewrite
from bigframes.core.compile import compiler, configs

if TYPE_CHECKING:
    import bigframes.core.nodes
    import bigframes.core.ordering


class SQLCompiler:
    def compile(
        self,
        node: bigframes.core.nodes.BigFrameNode,
        *,
        ordered: bool = True,
        limit: Optional[int] = None,
    ) -> str:
        """Compile node into sql where rows are sorted with ORDER BY."""
        request = configs.CompileRequest(node, sort_rows=ordered, peek_count=limit)
        return compiler.compile_sql(request).sql

    def compile_raw(
        self,
        node: bigframes.core.nodes.BigFrameNode,
    ) -> Tuple[
        str, Sequence[bigquery.SchemaField], bigframes.core.ordering.RowOrdering
    ]:
        """Compile node into sql that exposes all columns, including hidden ordering-only columns."""
        request = configs.CompileRequest(
            node, sort_rows=False, materialize_all_order_keys=True
        )
        result = compiler.compile_sql(request)
        assert result.row_order is not None
        return result.sql, result.sql_schema, result.row_order


def test_only_ibis_inferred_schema(node: bigframes.core.nodes.BigFrameNode):
    """Use only for testing paths to ensure ibis inferred schema does not diverge from bigframes inferred schema."""
    import bigframes.core.schema

    node = compiler._replace_unsupported_ops(node)
    node = rewrite.bake_order(node)
    ir = compiler.compile_node(node)
    items = tuple(
        bigframes.core.schema.SchemaItem(name, ir.get_column_type(ibis_id))
        for name, ibis_id in zip(node.schema.names, ir.column_ids)
    )
    return bigframes.core.schema.ArraySchema(items)
