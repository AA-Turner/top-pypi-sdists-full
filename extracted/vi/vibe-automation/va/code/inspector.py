"""Code inspection utilities using libcst."""

import sys
import logging
from typing import Optional

import libcst as cst

log = logging.getLogger("va.codegen.inspector")


class WithStatementFinder(cst.CSTVisitor):
    """Visitor to find a with statement at a specific line number."""

    METADATA_DEPENDENCIES = (cst.metadata.PositionProvider,)

    def __init__(self, target_line: int):
        super().__init__()
        self.target_line = target_line
        self.target_with: Optional[cst.With] = None

    def visit_With(self, node: cst.With) -> None:
        # Get position metadata if available
        try:
            position = self.get_metadata(cst.metadata.PositionProvider, node)
            if position and position.start.line == self.target_line:
                self.target_with = node
        except Exception:
            # Fallback: just take the first with statement we find
            # This is not ideal but better than nothing
            if not self.target_with:
                self.target_with = node


class WithBlockInspector:
    """Inspector for analyzing with statement blocks."""

    def __init__(self, filename: str, line_number: int):
        self.filename = filename
        self.line_number = line_number

    def is_with_block_empty(self) -> bool:
        """Check if the with block contains only pass or is empty using libcst."""
        try:
            # Read and parse the source file
            with open(self.filename, "r") as f:
                source_code = f.read()

            # Parse the source code with libcst
            tree = cst.parse_module(source_code)

            # Create metadata wrapper and find the with statement
            metadata_wrapper = cst.metadata.MetadataWrapper(tree)
            with_visitor = WithStatementFinder(self.line_number)

            metadata_wrapper.visit(with_visitor)

            if not with_visitor.target_with:
                log.debug(f"Could not find with statement at line {self.line_number}")
                return False

            # Check if the with statement body is empty (only contains pass or comments)
            return self._is_with_body_empty(with_visitor.target_with.body)

        except Exception as e:
            log.debug(f"Error checking if with block is empty: {e}")
            # If we can't determine, assume it's not empty to be safe
            return False

    def _is_with_body_empty(self, body: cst.IndentedBlock) -> bool:
        """Check if a with statement body contains only pass statements or comments."""
        if not body.body:
            return True

        for statement in body.body:
            # Check if it's a simple statement (like pass)
            if isinstance(statement, cst.SimpleStatementLine):
                for simple_stmt in statement.body:
                    if not isinstance(simple_stmt, cst.Pass):
                        return False
            else:
                # Any compound statement means it's not empty
                return False

        return True


def inspect_with_block_from_frame(frame_offset: int = 2) -> WithBlockInspector:
    """Create a WithBlockInspector from a stack frame.

    Frame offset determines which level of the call stack to inspect:
    - frame_offset=0: Current function (inspect_with_block_from_frame)
    - frame_offset=1: Function that called this one
    - frame_offset=2: Function that called the caller (default)
    - frame_offset=3: Three levels up the call stack

    Example call stack when used from AsyncStepContextManager:
        Frame 0: inspect_with_block_from_frame()
        Frame 1: _is_with_block_empty()
        Frame 2: AsyncStepContextManager.__aexit__()
        Frame 3: User's "async with page.step(...)" ← Usually the target

    Args:
        frame_offset: How many frames up the stack to look

    Returns:
        WithBlockInspector instance for the target location
    """
    frame = sys._getframe(frame_offset)
    filename = frame.f_code.co_filename
    lineno = frame.f_lineno
    return WithBlockInspector(filename, lineno)
