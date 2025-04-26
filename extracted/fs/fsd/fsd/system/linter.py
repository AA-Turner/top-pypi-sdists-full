import os
import re
import subprocess
import sys
import traceback
import warnings
import shlex
import logging
from dataclasses import dataclass
from pathlib import Path

from grep_ast import TreeContext, filename_to_lang
from grep_ast.tsl import get_parser  # noqa: E402

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("linter")

# tree_sitter is throwing a FutureWarning
warnings.simplefilter("ignore", category=FutureWarning)


class Linter:
    def __init__(self, encoding="utf-8", root=None):
        self.encoding = encoding
        self.root = root

        self.languages = dict(
            python=self.py_lint,
        )
        self.all_lint_cmd = None

    def set_linter(self, lang, cmd):
        if lang:
            self.languages[lang] = cmd
            return

        self.all_lint_cmd = cmd

    def lint_files(self, file_paths):
        """
        Lint multiple files and return results as a dictionary.
        
        Args:
            file_paths: List of file paths to lint
            
        Returns:
            Dictionary with file paths as keys and results as values in the format:
            {
                "error": Boolean indicating if errors were found,
                "text": Error message text,
                "lines": List of line numbers with errors
            }
        """
        if not file_paths:
            logger.debug("No files to lint")
            return {}
            
        results = {}
        for file_path in file_paths:
            # Skip if file_path is None or empty
            if not file_path:
                continue
                
            # Normalize file path to handle both absolute and relative paths
            abs_path = file_path
            if self.root and not os.path.isabs(file_path):
                abs_path = os.path.join(self.root, file_path)
            
            # Skip if file doesn't exist
            if not os.path.exists(abs_path):
                logger.debug(f"File not found: {abs_path}")
                results[file_path] = {
                    "error": False,
                    "text": "",
                    "lines": []
                }
                continue
            
            try:
                lint_result = self.lint(abs_path)
                if lint_result:
                    # Extract line numbers from the result
                    line_nums = []
                    
                    try:
                        # Try to extract line numbers from the tree context output
                        lines = lint_result.split('\n')
                        for i, line in enumerate(lines):
                            # Look for lines with the marker
                            if '█' in line:
                                # Extract line number from the beginning of the line
                                parts = line.split(':', 1)
                                if len(parts) > 1 and parts[0].strip().isdigit():
                                    line_nums.append(int(parts[0].strip()) - 1)  # Convert to 0-indexed
                        
                        # If no line numbers found using markers, try to find them in error messages
                        if not line_nums:
                            rel_fname = self.get_rel_fname(abs_path)
                            filenames_linenums = find_filenames_and_linenums(lint_result, [rel_fname])
                            if filenames_linenums:
                                _, found_lines = next(iter(filenames_linenums.items()))
                                line_nums = [num - 1 for num in found_lines]  # Convert to 0-indexed
                    except Exception as line_ex:
                        logger.debug(f"Error extracting line numbers: {str(line_ex)}")
                    
                    # Use the original file_path as the key in results to maintain caller's expectations
                    results[file_path] = {
                        "error": True,
                        "text": lint_result,
                        "lines": line_nums
                    }
                else:
                    results[file_path] = {
                        "error": False,
                        "text": "",
                        "lines": []
                    }
            except Exception as e:
                # Handle exceptions during linting
                error_msg = f"Error linting file: {str(e)}"
                logger.debug(f"Error linting {abs_path}: {str(e)}")
                results[file_path] = {
                    "error": True,
                    "text": error_msg,
                    "lines": []
                }
        
        return results

    def get_rel_fname(self, fname):
        if self.root:
            try:
                return os.path.relpath(fname, self.root)
            except ValueError:
                return fname
        else:
            return fname

    def run_cmd(self, cmd, rel_fname, code):
        cmd += " " + shlex.quote(rel_fname)

        returncode = 0
        stdout = ""
        try:
            returncode, stdout = run_cmd_subprocess(
                cmd,
                cwd=self.root,
                encoding=self.encoding,
            )
        except OSError as err:
            print(f"Unable to execute lint command: {err}")
            return
        errors = stdout
        if returncode == 0:
            return  # zero exit status

        res = f"## Running: {cmd}\n\n"
        res += errors

        return self.errors_to_lint_result(rel_fname, res)

    def errors_to_lint_result(self, rel_fname, errors):
        if not errors:
            return

        linenums = []
        filenames_linenums = find_filenames_and_linenums(errors, [rel_fname])
        if filenames_linenums:
            filename, linenums = next(iter(filenames_linenums.items()))
            linenums = [num - 1 for num in linenums]

        return LintResult(text=errors, lines=linenums)

    def lint(self, fname, cmd=None):
        rel_fname = self.get_rel_fname(fname)
        try:
            code = Path(fname).read_text(encoding=self.encoding, errors="replace")
        except OSError as err:
            print(f"Unable to read {fname}: {err}")
            return

        if cmd:
            cmd = cmd.strip()
        if not cmd:
            lang = filename_to_lang(fname)
            if not lang:
                return
            if self.all_lint_cmd:
                cmd = self.all_lint_cmd
            else:
                cmd = self.languages.get(lang)

        if callable(cmd):
            lintres = cmd(fname, rel_fname, code)
        elif cmd:
            lintres = self.run_cmd(cmd, rel_fname, code)
        else:
            lintres = basic_lint(rel_fname, code)

        if not lintres:
            return

        res = "# Fix any errors below, if possible.\n\n"
        res += lintres.text
        res += "\n"
        res += tree_context(rel_fname, code, lintres.lines)

        return res

    def py_lint(self, fname, rel_fname, code):
        basic_res = basic_lint(rel_fname, code)
        compile_res = lint_python_compile(fname, code)
        flake_res = self.flake8_lint(rel_fname)

        text = ""
        lines = set()
        for res in [basic_res, compile_res, flake_res]:
            if not res:
                continue
            if text:
                text += "\n"
            text += res.text
            lines.update(res.lines)

        if text or lines:
            return LintResult(text, lines)

    def flake8_lint(self, rel_fname):
        fatal = "E9,F821,F823,F831,F406,F407,F701,F702,F704,F706"
        flake8_cmd = [
            sys.executable,
            "-m",
            "flake8",
            f"--select={fatal}",
            "--show-source",
            "--isolated",
            rel_fname,
        ]

        text = f"## Running: {' '.join(flake8_cmd)}\n\n"

        try:
            result = subprocess.run(
                flake8_cmd,
                capture_output=True,
                text=True,
                check=False,
                encoding=self.encoding,
                errors="replace",
                cwd=self.root,
            )
            errors = result.stdout + result.stderr
        except Exception as e:
            errors = f"Error running flake8: {str(e)}"

        if not errors:
            return

        text += errors
        return self.errors_to_lint_result(rel_fname, text)


@dataclass
class LintResult:
    text: str
    lines: list


def lint_python_compile(fname, code):
    try:
        compile(code, fname, "exec")  # USE TRACEBACK BELOW HERE
        return
    except Exception as err:
        end_lineno = getattr(err, "end_lineno", err.lineno)
        line_numbers = list(range(err.lineno - 1, end_lineno))

        tb_lines = traceback.format_exception(type(err), err, err.__traceback__)
        last_file_i = 0

        target = "# USE TRACEBACK"
        target += " BELOW HERE"
        for i in range(len(tb_lines)):
            if target in tb_lines[i]:
                last_file_i = i
                break

        tb_lines = tb_lines[:1] + tb_lines[last_file_i + 1 :]

    res = "".join(tb_lines)
    return LintResult(text=res, lines=line_numbers)


def basic_lint(fname, code):
    """
    Use tree-sitter to look for syntax errors, display them with tree context.
    """

    lang = filename_to_lang(fname)
    if not lang:
        return

    # Tree-sitter linter is not capable of working with typescript #1132
    if lang == "typescript":
        return

    try:
        parser = get_parser(lang)
    except Exception as err:
        print(f"Unable to load parser: {err}")
        return

    tree = parser.parse(bytes(code, "utf-8"))

    try:
        errors = traverse_tree(tree.root_node)
    except RecursionError:
        print(f"Unable to lint {fname} due to RecursionError")
        return

    if not errors:
        return

    return LintResult(text="", lines=errors)


def tree_context(fname, code, line_nums):
    context = TreeContext(
        fname,
        code,
        color=False,
        line_number=True,
        child_context=False,
        last_line=False,
        margin=0,
        mark_lois=True,
        loi_pad=3,
        # header_max=30,
        show_top_of_file_parent_scope=False,
    )
    line_nums = set(line_nums)
    context.add_lines_of_interest(line_nums)
    context.add_context()
    s = "s" if len(line_nums) > 1 else ""
    output = f"## See relevant line{s} below marked with █.\n\n"
    output += fname + ":\n"
    output += context.format()

    return output


# Traverse the tree to find errors
def traverse_tree(node):
    errors = []
    if node.type == "ERROR" or node.is_missing:
        line_no = node.start_point[0]
        errors.append(line_no)

    for child in node.children:
        errors += traverse_tree(child)

    return errors


def find_filenames_and_linenums(text, fnames):
    """
    Search text for all occurrences of <filename>:\\d+ and make a list of them
    where <filename> is one of the filenames in the list `fnames`.
    """
    pattern = re.compile(r"(\b(?:" + "|".join(re.escape(fname) for fname in fnames) + r"):\d+\b)")
    matches = pattern.findall(text)
    result = {}
    for match in matches:
        fname, linenum = match.rsplit(":", 1)
        if fname not in result:
            result[fname] = set()
        result[fname].add(int(linenum))
    return result


def run_cmd_subprocess(cmd, cwd=None, encoding="utf-8"):
    """
    Run a command in a subprocess and return the returncode and stdout.
    
    Args:
        cmd: Command to run
        cwd: Working directory
        encoding: Text encoding to use
        
    Returns:
        Tuple of (returncode, stdout)
    """
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding=encoding,
            errors="replace",
            cwd=cwd,
            check=False
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        logger.error(f"Error running command '{cmd}': {str(e)}")
        return 1, f"Error running command: {str(e)}"


def main():
    """
    Main function to parse files provided as command line arguments.
    """
    if len(sys.argv) < 2:
        print("Usage: python linter.py <file1> <file2> ...")
        sys.exit(1)

    linter = Linter(root=os.getcwd())
    for file_path in sys.argv[1:]:
        errors = linter.lint(file_path)
        if errors:
            print(errors)


if __name__ == "__main__":
    main()