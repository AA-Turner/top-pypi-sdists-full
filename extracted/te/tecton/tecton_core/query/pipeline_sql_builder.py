import hashlib
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

import attrs
import pypika

from tecton_core import specs
from tecton_core.id_helper import IdHelper
from tecton_core.materialization_context import MaterializationContext
from tecton_core.pipeline import pipeline_common
from tecton_core.query import sql_compat
from tecton_core.query.dialect import Dialect
from tecton_proto.args.pipeline__client_pb2 import Pipeline
from tecton_proto.args.pipeline__client_pb2 import PipelineNode


@attrs.frozen
class PipelineSqlBuilder:
    pipeline: Pipeline
    id_to_transformation: Dict[str, specs.TransformationSpec]
    renamed_inputs_map: Dict[str, str]
    materialization_context: MaterializationContext
    """
    Attributes:
        pipeline: The pipeline proto to generate sql for
        transformations: List of TransformationSpecs that may be referenced by the pipeline.
        renamed_inputs_map: Mapping of input_name (field in PipelineNode) to new alias (how to refer to the input as CTE alias).
            For MaterializedFVs which are the only ones currently supporting sql mode, inputs referenced by input_name are always data sources.
        materialization_context: The materialization context to evaluate the pipeline with.
    """

    def _get_queries(self) -> List[Tuple[str, str]]:
        """
        Do a DFS through all transformations in the pipeline. The root of the pipeline should be at the end of the list.
        Each element is a tuple of (node_sql, node_alias).

        Then, to execute the pipeline, just do
            WITH (alias1) as (node_sql1),
            WITH (alias2) as (node_sql2),
            ...
        """
        root = self.pipeline.root
        return self._get_queries_helper(root)

    def get_pipeline_query(
        self, dialect: Dialect, input_name_to_query_map: Dict[str, pypika.queries.QueryBuilder]
    ) -> pypika.queries.QueryBuilder:
        """
        Generate the pypika query to evaluate a Feature View pipeline

        :param dialect: the SQL dialect
        :param input_name_to_query_map: A dict mapping data source input names to their respective pypika queries
        :return: pypika Query
        """
        queries = self._get_queries()
        # the base query is the query from the root of the pipeline (at the end of the list)
        res = (
            sql_compat.CompatFunctions.for_dialect(dialect)
            .query()
            .from_(sql_compat.CustomQuery(queries[-1][0]))
            .select("*")
        )
        # add CTE for each of the inputs, aliased to the unique name
        for k in self.renamed_inputs_map:
            res = res.with_(input_name_to_query_map[k], self.renamed_inputs_map[k])
        for t_node in queries[:-1]:
            query, alias = t_node
            res = res.with_(sql_compat.CustomQuery(query), alias)
        return res

    def _get_queries_helper(self, subtree: PipelineNode) -> List[Tuple[str, str]]:
        ret: List[Tuple[str, str]] = []
        for i in subtree.transformation_node.inputs:
            if i.node.HasField("transformation_node"):
                ret.extend(self._get_queries_helper(i.node))
        ret.append(self._get_query(subtree))
        return ret

    def _node_to_value(self, pipeline_node: PipelineNode) -> Any:  # noqa: ANN401
        """
        This returns the value of the node to be used as the input to the transformation_node that is its parent.
        The transformation defined by the user can look like:
        return f"SELECT {context.end_time} timestamp, d.* from {data_source} d join {transformation_output} t on d.x = t.y + {constant}"
        """
        if pipeline_node.HasField("transformation_node"):
            return unique_node_alias(pipeline_node)
        elif pipeline_node.HasField("data_source_node"):
            return self.renamed_inputs_map[pipeline_node.data_source_node.input_name]
        elif pipeline_node.HasField("materialization_context_node"):
            return self.materialization_context
        elif pipeline_node.HasField("context_node"):
            return self.materialization_context
        elif pipeline_node.HasField("constant_node"):
            return pipeline_common.constant_node_to_value(pipeline_node.constant_node)
        else:
            msg = f"Unknown PipelineNode type: {pipeline_node}"
            raise NotImplementedError(msg)

    def _get_query(self, pipeline_node: PipelineNode) -> Tuple[str, str]:
        """
        Construct a query for the given transformation node.
        Returns a tuple of (query_sql, unique_node_alias).
        The caller will be able to construct a CTE mapping the query_sql to the node_alias.
        """
        if pipeline_node.HasField("data_source_node"):
            # Stream Ingest with no transformation
            ds_table_name = self._node_to_value(pipeline_node)
            return f"SELECT * FROM {ds_table_name}", unique_node_alias(pipeline_node)

        assert pipeline_node.HasField("transformation_node")
        transformation_node = pipeline_node.transformation_node
        args: List[Any] = []
        kwargs: Dict[str, Any] = {}
        for transformation_input in transformation_node.inputs:
            node_value = self._node_to_value(transformation_input.node)
            if transformation_input.HasField("arg_index"):
                assert len(args) == transformation_input.arg_index
                args.append(node_value)
            elif transformation_input.HasField("arg_name"):
                kwargs[transformation_input.arg_name] = node_value
            else:
                msg = f"Unknown argument type for Input node: {transformation_input}"
                raise KeyError(msg)
        transformation = self.id_to_transformation[IdHelper.to_string(transformation_node.transformation_id)]
        user_function = transformation.user_function
        sql = user_function(*args, **kwargs)
        return sql, unique_node_alias(pipeline_node)


def unique_node_alias(node: PipelineNode) -> str:
    return f"node_{hashlib.md5(node.SerializeToString()).hexdigest()}"
