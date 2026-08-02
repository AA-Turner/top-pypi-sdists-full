import ast
import logging

from python_agent.build_scanner import ast_utils
from python_agent.build_scanner.entities.v3.method_data import (
    MethodMetaData,
    MethodData,
)
from python_agent.packages import astor
from python_agent.packages import astunparse
from python_agent.utils import create_md5

log = logging.getLogger(__name__)


class MethodHasher(object):
    def __init__(self, method_cleaner_visitor_class):
        self.method_cleaner_visitor_class = method_cleaner_visitor_class

    def calculate_method_hash(self, node):
        copied_node = self.copy_node(node)
        if isinstance(node, ast.FunctionDef):
            copied_node = copied_node.body[0]
        if isinstance(node, ast.Lambda):
            copied_node = copied_node.body[0].value

        self.method_cleaner_visitor_class().visit(copied_node)

        return self.calculate_hash(copied_node)

    def calculate_hash(self, node):
        m = create_md5()
        m.update(astunparse.unparse(node).encode("utf-8"))
        return m.hexdigest()

    def _is_parameterless_method(self, args):
        if not args or not args.args:
            return True
        return False

    def _calculate_method_sig_hash(self, node):
        args = getattr(node, "args", None)
        if self._is_parameterless_method(args):
            return ""
        params_string = ",".join(map(astunparse.unparse, args.args))
        m = create_md5()
        m.update(params_string.encode("utf-8"))
        return m.hexdigest()

    def _calculate_method_position(self, node):
        lineno = node.lineno
        col_offset = node.col_offset
        if hasattr(node, "decorator_list") and node.decorator_list:
            lineno = node.decorator_list[-1].lineno + 1
            col_offset = min(node.decorator_list[-1].col_offset - 1, 0)
        return lineno, col_offset

    def build_method(self, file_data, name, node, lines):
        method_hash = self.calculate_method_hash(node)
        last_node = ast_utils.get_last_node(node)
        last_node_lineno = last_node.lineno
        last_node_col_offset = last_node.col_offset + len(
            astunparse.unparse(last_node).strip("\n")
        )
        lineno, col_offset = self._calculate_method_position(node)
        position = [lineno, col_offset]
        end_position = [last_node_lineno, last_node_col_offset]
        sig_hash = self._calculate_method_sig_hash(node)

        method_type = None
        is_anonymous = isinstance(node, ast.Lambda)
        if is_anonymous:
            method_type = "lambda"
        if name == "__init__":
            method_type = "constructor"
        unique_id = self.build_unique_id(
            file_data.filename, node.lineno, node.col_offset, file_data.hash
        )

        meta = MethodMetaData(method_type, is_anonymous)
        method = MethodData(
            unique_id, name, position, end_position, meta, method_hash, sig_hash, lines
        )
        return method

    def build_unique_id(self, filename, line, column, file_hash):
        unique_id = "%(filename)s|%(line)s|%(column)s|%(file_hash)s" % {
            "filename": filename,
            "line": line,
            "column": column,
            "file_hash": file_hash,
        }
        return unique_id

    def copy_node(self, node):
        # astunparse is not maintained anymore and creates 'wrong' code.
        # So we're using astor which creates the right code.
        # we use it in case there is an exception and not always since we do not want
        # to change hashes for all customers -> meaning, quality risks
        try:
            code = astunparse.unparse(node)
            copied_node = ast.parse(code)
            return copied_node
        except SyntaxError:
            log.warning("coping node using astor")
            code = astor.to_source(node)
            copied_node = ast.parse(code)
            return copied_node
