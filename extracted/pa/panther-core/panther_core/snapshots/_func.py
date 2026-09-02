import ast
import inspect
import logging
import textwrap
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, cast

__all__ = ["FuncTransformer", "snapshot_func"]


class FuncTransformer(ast.NodeTransformer):
    # pylint: disable=invalid-name,broad-except,eval-used

    def __init__(self, ns: Dict[Any, Any], local_names: Optional[List[str]] = None):
        self._ns = ns
        self._local_names = local_names or []
        self.errors: List[BaseException] = []

    # remove type annotations and decorators
    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
        try:
            self._local_names.append(node.name)

            node.returns = None
            if node.args.args:
                for arg in node.args.args:
                    self._local_names.append(arg.arg)
                    arg.annotation = None

            node.decorator_list.clear()

            return self._closure_delve(node)

        except BaseException as err:
            return self._report_error_and_skip(node, err)

    # read imports into _local_names
    def visit_Import(self, node: ast.Import) -> ast.AST:
        try:
            for name in node.names:
                self._local_names.append(name.asname or name.name)

            return self.generic_visit(node)

        except BaseException as err:
            return self._report_error_and_skip(node, err)

    # read from-imports into _local_names
    def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.AST:
        try:
            for name in node.names:
                self._local_names.append(name.asname or name.name)

            return self.generic_visit(node)

        except BaseException as err:
            return self._report_error_and_skip(node, err)

    # auto-resolve attributes to constant values
    def visit_Attribute(self, node: ast.Attribute) -> ast.AST:
        try:
            root_name, skip = self._attribute_root(node)
            if skip:
                return self.generic_visit(node)

            if isinstance(node.ctx, ast.Load) and (root_name not in self._local_names):
                return self._const_replace(node)

            return self.generic_visit(node)

        except BaseException as err:
            return self._report_error_and_skip(node, err)

    # auto-resolve names to constant values
    def visit_Name(self, node: ast.Name) -> ast.AST:
        try:
            if isinstance(node.ctx, ast.Store):
                self._local_names.append(node.id)
                return self.generic_visit(node)

            if isinstance(node.ctx, ast.Load) and (node.id not in self._local_names):
                return self._const_replace(node)

            return self.generic_visit(node)

        except BaseException as err:
            return self._report_error_and_skip(node, err)

    def visit_Lambda(self, node: ast.Lambda) -> ast.AST:
        try:
            return self._closure_delve(node)

        except BaseException as err:
            return self._report_error_and_skip(node, err)

    def _closure_delve(self, node: Union[ast.Lambda, ast.FunctionDef]) -> ast.AST:
        prev_args = self._local_names.copy()
        for arg in node.args.args:
            self._local_names.append(arg.arg)

        new_node = self.generic_visit(node)
        self._local_names = prev_args

        return new_node

    def _const_replace(self, node: ast.AST) -> Union[ast.Constant, ast.AST]:
        try:
            c = ast.unparse(node)  # nosec B307
            x = eval(c, self._ns)  # nosec B307

            const_node = ast.Constant(x)

            if inspect.isbuiltin(x):
                return self.generic_visit(node)

            if ast.unparse(cast(ast.AST, const_node))[0] == "<":
                return self.generic_visit(node)

            return const_node
        except BaseException as err:
            return self._report_error_and_skip(node, err)

    def _attribute_root(self, node: Union[ast.AST, ast.expr]) -> Tuple[str, bool]:
        if isinstance(node, ast.Name):
            return node.id, False

        if isinstance(node, ast.Constant):
            # ast.Constant.value is not an AST node, it's the actual Python value
            return "", True

        if isinstance(node, (ast.Attribute, ast.Subscript)):
            return self._attribute_root(node.value)

        if isinstance(node, ast.Call):
            return self._attribute_root(node.func)

        # else, it is a complex case, process children individually
        return "", True

    def _report_error_and_skip(self, node: ast.AST, err: BaseException) -> ast.AST:
        node_code = ast.unparse(node)
        logging.warning("unable to parse: %s", node_code)
        logging.error(err)
        self.errors.append(err)
        return self.generic_visit(node)


def snapshot_func(target_func: Callable) -> Tuple[str, List[BaseException]]:
    original_src = textwrap.dedent(inspect.getsource(target_func))
    original_tree = ast.parse(
        original_src,
        filename=(inspect.getsourcefile(target_func) or "unknown"),
        mode="exec",
    )

    v_nonlocal, v_global, _, _ = inspect.getclosurevars(target_func)
    transformer = FuncTransformer(ns={**v_nonlocal, **v_global})

    parsed_tree = transformer.visit(original_tree)
    parsed_src = ast.unparse(parsed_tree)

    return parsed_src, transformer.errors
