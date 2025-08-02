"""Simplified code mutation system based on execution recording and diff generation."""

import difflib
import sys
from typing import List, Dict, Tuple
from dataclasses import dataclass

import libcst as cst


@dataclass
class WorkflowMutationEntry:
    """Records a single workflow code mutation."""

    filename: str
    line_number: int
    executed_code: str
    context_dict: Dict = None


class WorkflowMutation:
    """Tracks workflow code mutations and generates diffs showing what changed."""

    def __init__(self):
        self.mutations: List[WorkflowMutationEntry] = []

    def record_execution_from_frame(
        self, executed_code: str, context_dict: Dict = None, frame_offset: int = 2
    ):
        """Record execution from the current stack frame."""
        frame = sys._getframe(frame_offset)
        filename = frame.f_code.co_filename
        line_number = frame.f_lineno

        mutation = WorkflowMutationEntry(
            filename=filename,
            line_number=line_number,
            executed_code=executed_code,
            context_dict=context_dict,
        )
        self.mutations.append(mutation)

    def record_execution(
        self,
        filename: str,
        line_number: int,
        executed_code: str,
        context_dict: Dict = None,
    ):
        """Record execution with explicit file and line information."""
        mutation = WorkflowMutationEntry(
            filename=filename,
            line_number=line_number,
            executed_code=executed_code,
            context_dict=context_dict,
        )
        self.mutations.append(mutation)

    def generate_file_diff(self, filename: str) -> str:
        """Generate a unified diff for a specific file."""
        try:
            # Read original file
            with open(filename, "r") as f:
                original_lines = f.readlines()

            # Get all mutations for this file
            file_mutations = [
                mutation for mutation in self.mutations if mutation.filename == filename
            ]
            if not file_mutations:
                return ""

            # Apply mutations to create new version (bottom to top to avoid line number shifts)
            new_lines = original_lines.copy()
            file_mutations.sort(key=lambda x: x.line_number, reverse=True)

            for mutation in file_mutations:
                new_lines = self._replace_with_block(
                    new_lines, mutation.line_number, mutation.executed_code
                )

            # Generate diff - strip newlines from both to ensure consistency
            original_lines_clean = [line.rstrip("\n") for line in original_lines]
            new_lines_clean = [line.rstrip("\n") for line in new_lines]

            diff = difflib.unified_diff(
                original_lines_clean,
                new_lines_clean,
                fromfile=f"{filename} (original)",
                tofile=f"{filename} (with mutations)",
                lineterm="",
            )

            return "\n".join(diff)

        except Exception as e:
            return f"Error generating diff for {filename}: {e}"

    def _find_with_statement_boundaries(
        self, source_code: str, target_line: int
    ) -> Tuple[int, int]:
        """Use libcst to find the actual boundaries of a with statement body.

        Returns:
            tuple: (body_start_line, body_end_line) 1-indexed
        """
        tree = cst.parse_module(source_code)
        metadata_wrapper = cst.metadata.MetadataWrapper(tree)

        class WithStatementFinder(cst.CSTVisitor):
            METADATA_DEPENDENCIES = (cst.metadata.PositionProvider,)

            def __init__(self):
                super().__init__()
                self.body_start = None
                self.body_end = None

            def visit_With(self, node: cst.With) -> None:
                position = self.get_metadata(cst.metadata.PositionProvider, node)
                if position and position.start.line <= target_line <= position.end.line:
                    # Found the with statement that contains our target line
                    if isinstance(node.body, cst.IndentedBlock):
                        body_position = self.get_metadata(
                            cst.metadata.PositionProvider, node.body
                        )
                        if body_position:
                            self.body_start = body_position.start.line
                            self.body_end = body_position.end.line

        finder = WithStatementFinder()
        metadata_wrapper.visit(finder)

        if finder.body_start and finder.body_end:
            return finder.body_start, finder.body_end

        # Fallback to simple logic if AST parsing fails
        return target_line, target_line

    def _replace_with_block(
        self, lines: List[str], target_line: int, new_code: str
    ) -> List[str]:
        """Replace a with block with executed code using AST-based detection."""
        if target_line < 1 or target_line > len(lines):
            return lines

        # Use AST to find the actual with statement boundaries
        source_code = "".join(lines)
        try:
            body_start, body_end = self._find_with_statement_boundaries(
                source_code, target_line
            )
        except Exception:
            # Fall back to simple logic if AST parsing fails
            body_start = target_line + 1  # Body starts after the with statement
            body_end = self._find_with_block_end(lines, target_line - 1)

        # Get the indentation from the with statement line
        with_line_idx = target_line - 1
        with_line = lines[with_line_idx]
        with_indent = len(with_line) - len(with_line.lstrip())

        # Prepare new code with proper indentation
        new_code_lines = []
        code_lines = new_code.split("\n")

        for line in code_lines:
            if line.strip():  # Only indent non-empty lines
                new_code_lines.append(" " * (with_indent + 4) + line)
            # Skip empty lines to avoid extra blank lines in diff

        # Use libcst to add 'as context' to with statement if needed
        try:
            modified_source = self._add_context_to_with_statement_libcst(
                source_code, target_line
            )
        except Exception:
            # If libcst fails, use the original source unchanged
            modified_source = source_code
        modified_lines = modified_source.split("\n")

        # Ensure we have newlines at the end of lines (except the last one)
        if modified_lines:
            for i in range(len(modified_lines) - 1):
                modified_lines[i] += "\n"

        # Now apply the body replacement to the modified source
        try:
            body_start, body_end = self._find_with_statement_boundaries(
                modified_source, target_line
            )
        except Exception:
            # Fall back to original boundaries if parsing fails
            pass

        # Convert to 0-indexed for the modified lines
        body_start_idx = body_start - 1
        body_end_idx = body_end - 1

        # Replace the body content
        result_lines = []

        # Add all lines before the body
        for i in range(body_start_idx):
            result_lines.append(modified_lines[i])

        # Add the new code lines
        for line in new_code_lines:
            result_lines.append(line + "\n")

        # Add all lines after the body
        for i in range(body_end_idx + 1, len(modified_lines)):
            result_lines.append(modified_lines[i])

        return result_lines

    def _add_context_to_with_statement_libcst(
        self, source_code: str, target_line: int
    ) -> str:
        """Use libcst to add 'as context' to a with statement if it's missing."""
        tree = cst.parse_module(source_code)
        metadata_wrapper = cst.metadata.MetadataWrapper(tree)

        class WithStatementTransformer(cst.CSTTransformer):
            METADATA_DEPENDENCIES = (cst.metadata.PositionProvider,)

            def __init__(self, target_line):
                self.target_line = target_line
                super().__init__()

            def leave_With(
                self, original_node: cst.With, updated_node: cst.With
            ) -> cst.With:
                # Check if this is the with statement we want to modify
                position = self.get_metadata(
                    cst.metadata.PositionProvider, original_node
                )
                if (
                    position
                    and position.start.line <= self.target_line <= position.end.line
                ):
                    # Check if the first item already has an 'as' clause
                    if updated_node.items and updated_node.items[0].asname is not None:
                        return updated_node  # First item already has 'as' clause

                    # Add 'as context' to the first item
                    if updated_node.items:
                        new_items = []
                        for i, item in enumerate(updated_node.items):
                            if i == 0:  # Add 'as context' to the first item
                                new_item = item.with_changes(
                                    asname=cst.AsName(
                                        name=cst.Name("context"),
                                        whitespace_before_as=cst.SimpleWhitespace(" "),
                                        whitespace_after_as=cst.SimpleWhitespace(" "),
                                    )
                                )
                                new_items.append(new_item)
                            else:
                                new_items.append(item)

                        return updated_node.with_changes(items=new_items)

                return updated_node

        # Apply the transformation
        transformer = WithStatementTransformer(target_line)
        new_tree = metadata_wrapper.visit(transformer)

        # Generate the code back
        return new_tree.code

    def _find_with_block_end(self, lines: List[str], with_line_idx: int) -> int:
        """Find the end of a with block using simple indentation tracking."""
        with_line = lines[with_line_idx]
        with_indent = len(with_line) - len(with_line.lstrip())

        # Look for the next line that's at the same or lower indentation level
        last_block_line = with_line_idx
        for i in range(with_line_idx + 1, len(lines)):
            line = lines[i]
            if line.strip():  # Ignore empty lines
                line_indent = len(line) - len(line.lstrip())
                if line_indent <= with_indent:
                    return last_block_line
                else:
                    # This line is part of the with block
                    last_block_line = i
            else:
                # Empty line - could be part of the block or after it
                # We'll include it if the next non-empty line is still in the block
                continue

        return last_block_line

    def generate_all_diffs(self) -> Dict[str, str]:
        """Generate diffs for all files that have mutations."""
        diffs = {}
        unique_files = set(mutation.filename for mutation in self.mutations)

        for filename in unique_files:
            diff = self.generate_file_diff(filename)
            if diff:
                diffs[filename] = diff

        return diffs

    def print_all_diffs(self):
        """Print all diffs to stdout."""
        diffs = self.generate_all_diffs()

        if not diffs:
            print("No workflow mutations recorded.")
            return

        for filename, diff in diffs.items():
            print(f"\n{'=' * 60}")
            print(f"DIFF for {filename}")
            print("=" * 60)
            print(diff)

    def clear(self):
        """Clear all recorded mutations."""
        self.mutations.clear()


def record_step_execution(
    executed_code: str, context_dict: Dict = None, frame_offset: int = 2
):
    """Record a step execution from the current frame."""
    from va.automation import Automation

    automation = Automation.get_instance()
    if automation.mutation is None:
        raise RuntimeError(
            "WorkflowMutation is not initialized on the automation instance"
        )

    tracker = automation.mutation
    tracker.record_execution_from_frame(executed_code, context_dict, frame_offset + 1)
