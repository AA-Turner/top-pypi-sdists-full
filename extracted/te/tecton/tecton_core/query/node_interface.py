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
import sqlparse

from tecton_core.compute_mode import ComputeMode
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

    def _to_query(self) -> pypika.queries.QueryBuilder:
        return self.node._to_query()

    def to_sql(self, pretty_sql: bool = False) -> str:
        """
        Attempts to recursively generate sql for this and child nodes.

        Args:
            pretty_sql: If True, the sql will be reformatted and returned as a more readable, multiline string. If False,
            the SQL will be returned as a one line string. For long queries, using pretty_sql=False has better performance.
        """
        return self.node.to_sql(pretty_sql=pretty_sql)

    def to_arrow_reader(self, context: ExecutionContext) -> "pyarrow.RecordBatchReader":
        return self.node.to_arrow_reader(context)

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
            assert len(self.input_names) == len(
                self.inputs
            ), f"`input_names` has length {len(self.input_names)} but `inputs` has length {len(self.inputs)}"
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

    def _to_query(self) -> pypika.queries.QueryBuilder:
        """
        Attempts to recursively generate sql query for this and child nodes.
        """
        raise NotImplementedError()

    @property
    def output_schema(self) -> Optional[Schema]:
        """
        Full schema of the output produced by this node
        """
        raise NotImplementedError

    def to_arrow_reader(self, context: ExecutionContext) -> "pyarrow.RecordBatchReader":
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
        if not hasattr(self, "_arrow_table"):
            self._arrow_table = pyarrow.Table.from_pandas(self.to_pandas())
        return self._arrow_table

    def to_spark(self):
        raise NotImplementedError


def recurse_query_tree(node_ref: NodeRef, f: Callable) -> None:
    f(node_ref.node)
    for child in node_ref.inputs:
        recurse_query_tree(child, f)
