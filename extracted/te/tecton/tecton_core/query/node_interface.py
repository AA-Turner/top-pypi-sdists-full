import copy
import uuid
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import attrs
import pandas
import pyarrow
import pypika
import pypika.functions
import pypika.terms
import sqlparse

from tecton_core.compute_mode import ComputeMode
from tecton_core.duckdb_factory import BUCKET_TRANSFORM_FUN
from tecton_core.query.dialect import Dialect
from tecton_core.query.executor_params import ExecutionContext
from tecton_core.query.sql_compat import CompatFunctions
from tecton_core.schema import Schema
from tecton_core.vendor.treelib import Tree


if TYPE_CHECKING:
    from tecton_core.query.pandas.node import ArrowExecNode


@dataclass
class NodeRef:
    """
    Used so we can more easily modify the QueryTree by inserting and removing nodes, e.g.
    def subtree_rewrite(subtree_node_ref):
        subtree_node_ref.node = NewNode(subtree_node_ref.node)
    """

    node: Union["QueryNode", "ArrowExecNode"]

    @property
    def columns(self) -> Sequence[str]:
        return self.node.columns

    @property
    def inputs(self) -> Sequence["NodeRef"]:
        return self.node.inputs

    @property
    def input_names(self) -> Optional[List[str]]:
        return self.node.input_names

    @property
    def name(self):
        return self.node.__class__.__name__ + "_" + str(self.node.node_id.hex[:8])

    def as_str(self) -> str:
        return self.node.as_str()

    @property
    def output_schema(self) -> Optional[Schema]:
        return self.node.output_schema

    @property
    def output_partitioning(self) -> "Partitioning":
        return self.node.output_partitioning

    def pretty_str(
        self,
        node_id: bool = True,
        name: bool = True,
        description: bool = True,
        columns: bool = False,
    ) -> str:
        """Returns a string that represents the query tree which has this NodeRef as the root node.

        Args:
            node_id: If True, the unique id associated with each node will be rendered.
            name: If True, the class names of the nodes will be rendered.
            description: If True, the actions of the nodes will be rendered.
            columns: If True, the columns of each node will be rendered as an appendix after tree itself.
        """
        assert name or description, "At least one of 'name' or 'description' must be True."
        if columns:
            assert node_id, "Can only show columns if 'node_id' is True."
        tree = self.create_tree(node_id=node_id, name=name, description=description)

        # key=False ensures that nodes on the same level are sorted by id and stdout=False ensures a string is returned
        tree_str = tree.show(key=False, stdout=False)

        if not columns:
            return tree_str

        node_columns = []
        max_node_id = tree.size()
        for unique_id in range(1, max_node_id + 1):
            node = tree.get_node(unique_id).data
            node_columns.append(f"<{unique_id}> " + f"{'|'.join(node.columns)}")

        return tree_str + "\n" + "\n".join(node_columns)

    def _to_query(self, partition_selector: Optional["PartitionSelector"] = None) -> pypika.queries.QueryBuilder:
        return self.node._to_query(partition_selector)

    def to_sql(self, pretty_sql: bool = False) -> str:
        """
        Attempts to recursively generate sql for this and child nodes.

        Args:
            pretty_sql: If True, the sql will be reformatted and returned as a more readable, multiline string. If False,
            the SQL will be returned as a one line string. For long queries, using pretty_sql=False has better performance.
        """
        return self.node.to_sql(pretty_sql=pretty_sql)

    def to_arrow_reader(
        self, context: ExecutionContext, partition_selector: Optional["PartitionSelector"] = None
    ) -> "pyarrow.RecordBatchReader":
        return self.node.to_arrow_reader(context, partition_selector)

    def create_tree(self, node_id: bool = True, name: bool = True, description: bool = True) -> Tree:
        """Creates a Tree to represent the query tree which has this NodeRef as the root node.

        The Tree is built so that it can immediately generate a string representation.

        Args:
            node_id: If True, the unique id associated with each node will be rendered.
            name: If True, the class names of the nodes will be rendered.
            description: If True, the actions of the nodes will be rendered.
        """
        tree = Tree()
        self._create_tree(tree=tree, parent_id=None, node_id=node_id, name=name, description=description)
        return tree

    def _create_tree(
        self,
        tree: Tree,
        prefix: str = "",
        parent_id: Optional[int] = None,
        node_id: bool = True,
        name: bool = True,
        description: bool = True,
    ) -> None:
        tag = ""

        # Node ids are assigned sequentially, starting with 1.
        unique_id = tree.size() + 1
        if node_id:
            tag += f"<{unique_id}> "

        tag += prefix

        # Add parameter names to the node class. For example, EntityFilterNode(feature_data, entities).
        node_name = self.node.__class__.__name__
        if self.input_names:
            node_name += f"({', '.join(self.input_names)})"

        if name and description:
            tag += f"{node_name}: {self.as_str()}"
        elif name:
            tag += f"{node_name}"
        elif description:
            tag += f"{self.as_str()}"

        # The rendering is messed up if the tag has a newline.
        assert "\n" not in tag

        # We attach this NodeRef so that it can be retrieved later by its node id.
        tree.create_node(tag=tag, identifier=unique_id, parent=parent_id, data=self.node)

        # Recursively handle all children.
        if self.input_names:
            assert len(self.input_names) == len(self.inputs), (
                f"`input_names` has length {len(self.input_names)} but `inputs` has length {len(self.inputs)}"
            )
            for input_name, i in zip(self.input_names, self.inputs):
                prefix = f"[{input_name}] "
                i._create_tree(
                    tree=tree,
                    prefix=prefix,
                    parent_id=unique_id,
                    node_id=node_id,
                    name=name,
                    description=description,
                )
        else:
            for i in self.inputs:
                i._create_tree(
                    tree=tree,
                    parent_id=unique_id,
                    node_id=node_id,
                    name=name,
                    description=description,
                )

    def deepcopy(self) -> "NodeRef":
        node_deepcopy = self.node.deepcopy()
        return node_deepcopy.as_ref()


@attrs.frozen
class QueryNode:
    dialect: Dialect = attrs.field()
    compute_mode: ComputeMode = attrs.field()
    func: CompatFunctions = attrs.field(kw_only=True)
    node_id: uuid.UUID = attrs.field(init=False)

    def __attrs_post_init__(self):
        object.__setattr__(self, "node_id", uuid.uuid4())

    @func.default
    def _compat_functions_factory(self):
        return CompatFunctions.for_dialect(self.dialect, self.compute_mode)

    def with_dialect(self, dialect: Dialect, compute_mode: Optional[ComputeMode] = None) -> "QueryNode":
        for node_ref in self.inputs:
            if isinstance(node_ref.node, QueryNode):
                node_ref.node = node_ref.node.with_dialect(dialect, compute_mode)
        return attrs.evolve(self, dialect=dialect, func=CompatFunctions.for_dialect(dialect, compute_mode))

    def deepcopy(self) -> "QueryNode":
        # We avoid using copy.deepcopy as it runs into pickling issues. Instead, we attempt to deepcopy each attribute
        # that requires it.
        node_deepcopy = copy.copy(self)
        field_names = [f.name for f in node_deepcopy.__attrs_attrs__]
        for field_name in field_names:
            field = getattr(node_deepcopy, field_name)
            if isinstance(field, NodeRef):
                child_ref_copy = field.deepcopy()
                changes = {field_name: child_ref_copy}
                node_deepcopy = attrs.evolve(node_deepcopy, **changes)
        return node_deepcopy

    @property
    def columns(self) -> Sequence[str]:
        """
        The columns in the projectlist coming out of this node.
        """
        raise NotImplementedError()

    def as_ref(self) -> NodeRef:
        return NodeRef(self)

    # used for recursing through the tree for tree rewrites
    @property
    def inputs(self) -> Sequence[NodeRef]:
        raise NotImplementedError()

    @property
    def input_names(self) -> Optional[List[str]]:
        """Returns a list of names for the inputs of this node, if all inputs have names. Otherwise returns None.

        If a list is returned, the order of the names should correspond to the order of nodes in the `inputs` property.
        """
        return None

    def as_str(self) -> str:
        """
        Returns a human-readable description of the operation implemented by this node.
        Used by tecton.TectonDataFrame.explain
        """
        raise NotImplementedError()

    def to_sql(self, pretty_sql: bool = False) -> str:
        """
        Attempts to recursively generate sql for this and child nodes.

        Args:
            pretty_sql: If True, the sql will be reformatted and returned as a more readable, multiline string. If False,
            the SQL will be returned as a one line string. For long queries, using pretty_sql=False has better performance.
        """
        sql_str = self._to_query().get_sql()
        if pretty_sql:
            # This can take a very long time for long queries
            return sqlparse.format(sql_str, reindent=True)
        return sql_str

    def get_sql_views(self, pretty_sql: bool = False) -> List[Tuple[str, str]]:
        """
        Get optional sql views for this node. List of Tuple(view_name, view_sql)
        """
        return []

    def _to_query(self, partition_selector: Optional["PartitionSelector"] = None) -> pypika.queries.QueryBuilder:
        """
        Attempts to recursively generate sql query for this and child nodes.
        :param partition_selector:
        """
        raise NotImplementedError()

    @property
    def output_schema(self) -> Optional[Schema]:
        """
        Full schema of the output produced by this node
        """
        raise NotImplementedError

    @property
    def output_partitioning(self) -> "Partitioning":
        """
        Partitioning of the output produced by this node
        """
        assert len(self.inputs), f"{self.__class__} must implement output_partitioning property"
        if len(self.inputs) > 1:
            assert all(
                self.inputs[0].output_partitioning.is_equivalent(inp.output_partitioning) for inp in self.inputs[1:]
            ), (
                f"All inputs into {self.__class__} node must have the same partitioning: {[i.output_partitioning for i in self.inputs]}"
            )

        return self.inputs[0].output_partitioning

    def to_arrow_reader(
        self, context: ExecutionContext, partition_selector: Optional["PartitionSelector"] = None
    ) -> "pyarrow.RecordBatchReader":
        raise NotImplementedError


class DataframeWrapper(ABC):
    """
    A wrapper around pyspark, pandas, snowflake, etc dataframes provides a common interface through which we
    can register views.
    """

    @property
    @abstractmethod
    def _dataframe(self) -> Any:  # noqa: ANN401
        """
        The underlying dataframe
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def columns(self) -> List[str]:
        """
        The columns of the dataframe
        """
        raise NotImplementedError

    @property
    def schema(self) -> Schema:
        """
        The schema of the dataframe
        """
        raise NotImplementedError

    @property
    def _temp_table_name(self):
        """
        Gets the temp view name registered by register()
        """
        return f"TMP_TABLE_{id(self._dataframe)}"

    def to_pandas(self) -> pandas.DataFrame:
        raise NotImplementedError

    def to_arrow(self) -> "pyarrow.Table":
        """
        Get the results as arrow Table
        """
        if not hasattr(self, "_arrow_table") or self._arrow_table is None:
            self._arrow_table = pyarrow.Table.from_pandas(self.to_pandas())
        return self._arrow_table

    def to_spark(self):
        raise NotImplementedError


class Partitioning(ABC):
    @property
    def number_of_partitions(self) -> int:
        raise NotImplementedError

    def is_equivalent(self, other: "Partitioning") -> bool:
        raise NotImplementedError

    def partition_expression(self, partition_by: pypika.Field) -> pypika.terms.Term:
        raise NotImplementedError


class SinglePartition(Partitioning):
    @property
    def number_of_partitions(self) -> int:
        return 1

    def is_equivalent(self, other: "Partitioning") -> bool:
        return other.number_of_partitions == 1

    def partition_expression(self, partition_by: pypika.Field) -> pypika.terms.Term:
        return pypika.terms.LiteralValue(1)


class JoinKeyHashPartitioning(Partitioning):
    def __init__(self, join_keys: List[str], buckets: int) -> None:
        self._join_keys = join_keys
        self._buckets = buckets

    @property
    def number_of_partitions(self) -> int:
        return self._buckets

    def is_equivalent(self, other: "Partitioning") -> bool:
        return (
            isinstance(other, JoinKeyHashPartitioning)
            and other._buckets == self._buckets
            and other._join_keys[0] == self._join_keys[0]
        )

    def partition_expression(self, partition_by: pypika.Field) -> pypika.terms.Term:
        return pypika.terms.Function(BUCKET_TRANSFORM_FUN, partition_by, pypika.terms.LiteralValue(str(self._buckets)))


class JoinKeyRangePartitioning(Partitioning):
    def __init__(self, join_keys: List[str], boundaries: List[Union[int, str]]) -> None:
        self._join_keys = join_keys
        self._boundaries = boundaries

    @property
    def number_of_partitions(self) -> int:
        return len(self._boundaries) + 1

    def is_equivalent(self, other: "Partitioning") -> bool:
        return (
            isinstance(other, JoinKeyRangePartitioning)
            and other._join_keys == self._join_keys
            and other._boundaries == self._boundaries
        )

    def partition_expression(self, partition_by: pypika.Field) -> pypika.terms.Term:
        """
        Find the partition index by join key value.
        Iterates over list of boundaries until find the first boundary which is greater than current value
        and returns its index.

        Example:
            boundaries: [3, 7, 10]
            meaning we have 4 partitions: [-inf, 3), [3, 7), [7, 10), [10, inf)
            input 2 -> should return 0
            input 4 -> should return 1
            input 7 -> should return 2
            input 11 -> should return 3
        """
        case = pypika.Case()
        for idx, boundary in enumerate(self._boundaries):
            # WHEN entity_id < boundary THEN idx
            case = case.when(partition_by < boundary, idx)
        # ELSE last partition index
        return case.else_(len(self._boundaries))

    def boundaries_for_partition(self, partition_idx: int) -> Tuple[Any, Any]:
        if partition_idx == 0:
            return None, self._boundaries[0]

        if partition_idx == len(self._boundaries):
            return self._boundaries[-1], None

        return self._boundaries[partition_idx - 1], self._boundaries[partition_idx]


@dataclass
class PartitionSelector:
    partition_indexes: List[int]
    total_number_of_partitions: int

    def as_str(self) -> str:
        return f"{[idx + 1 for idx in self.partition_indexes]} of {self.total_number_of_partitions} partitions"


class EmptyPartition(Exception):
    pass


def recurse_query_tree(node_ref: NodeRef, f: Callable) -> None:
    f(node_ref.node)
    for child in node_ref.inputs:
        recurse_query_tree(child, f)
