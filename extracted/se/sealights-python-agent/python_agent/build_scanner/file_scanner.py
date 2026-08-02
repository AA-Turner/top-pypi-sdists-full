"""
file_scanner module is part of the build scan process.
For a given full python file path and its relative path:
    - Parse the code to ast
    - Traverse the tree
    - Calculate method hash for functions and lambdas
    - Calculate file hash
"""

import ast
import logging
import traceback

from python_agent.build_scanner.entities.v3.file_data import FileData
from python_agent.build_scanner.visitors import SealightsVisitor
from python_agent.packages import astunparse
from python_agent.utils import create_md5

log = logging.getLogger(__name__)


class FileScanner(object):
    def calculate_file_signature(self, full_path, rel_path):
        file_data = FileData(rel_path)
        try:
            with open(full_path, "r") as f:
                code = f.read()
            tree = ast.parse(code)
            file_data.hash = self.calculate_file_hash(tree)
            SealightsVisitor(file_data).visit(tree)
        except SyntaxError as e:
            file_data.error = traceback.format_exc()
            log.error(
                "File ignored due to syntax error. %s. problematic code: (%s)"
                % (full_path, e.text.strip())
            )
        except Exception:
            file_data.error = traceback.format_exc()
            log.error(
                "Failed creating mapping for file. Ignoring... %s" % full_path,
                exc_info=True,
            )
        return file_data

    def calculate_file_hash(self, node):
        # we parse and unparse the file code to eliminate comments
        m = create_md5()
        m.update(astunparse.unparse(node).encode("utf-8"))
        return m.hexdigest()
