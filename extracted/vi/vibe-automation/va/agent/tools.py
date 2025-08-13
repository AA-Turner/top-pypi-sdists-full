import os
import inspect
import json
import logging
from typing import Dict, Any

import libcst as cst
from va.agent.code_buffer import CodeModificationBuffer

log = logging.getLogger(__name__)

RECOVERY_TOOLS = [
    {
        "name": "get_page_state",
        "description": "Get the current state of the browser page",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "execute_code",
        "description": "Execute Python code in the page context for immediate actions",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Python code to execute (e.g., 'await page.goto(\"url\")')",
                }
            },
            "required": ["code"],
        },
    },
    {
        "name": "insert_code",
        "description": "Insert code for missing workflow steps",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Python code to insert (will be properly indented)",
                }
            },
            "required": ["code"],
        },
    },
    {
        "name": "replace_code",
        "description": "Replace faulty code at the exception location",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Corrected Python code to replace the faulty code",
                }
            },
            "required": ["code"],
        },
    },
    {
        "name": "continue_workflow",
        "description": "Continue execution of the original workflow after recovery",
        "input_schema": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["retry", "skip"],
                    "description": "Whether to retry the failed line or skip it and continue from the next line",
                },
                "reason": {
                    "type": "string",
                    "description": "Explanation of the recovery action taken",
                },
            },
            "required": ["action", "reason"],
        },
    },
]


class RecoveryTools:
    """Tools available to the LLM agent during recovery sessions."""

    def __init__(self, session: "RecoverySession"):
        self.session = session

    async def execute_python_command(self, code: str) -> str:
        """
        Execute Python code with access to local variables from the execution context.

        Args:
            code: Python code to execute

        Returns:
            String representation of the execution result or error
        """
        try:
            # Get the page object from the execution context
            local_vars = self.session.execution_context.get("local_vars", {})
            page = local_vars.get("page")
            browser = local_vars.get("browser")

            print(
                f"🔍 Available objects: page={page is not None}, browser={browser is not None}"
            )
            print(f"🔍 Page object type: {type(page)}")
            print(f"🔍 Browser object type: {type(browser)}")

            if not page:
                return "Error: No page object found in execution context"

            # Check if page is still alive
            try:
                current_url = page.url
                print(f"🔍 Current page URL: {current_url}")
            except Exception as page_error:
                print(f"⚠️  Page object is no longer valid: {page_error}")
                return f"Error: Page object is no longer valid: {page_error}"

            # Create execution context similar to _handle_execute_python_command
            captured_output = []
            execution_context = {
                "page": page,
                "browser": browser,
                "print": lambda *args: captured_output.append(
                    " ".join(str(arg) for arg in args)
                ),
            }

            # All workflow code is async, so always wrap in async function
            # Handle multi-line code properly
            if "\n" in code:
                # Multi-line code - indent each line properly
                indented_lines = []
                for line in code.split("\n"):
                    if line.strip():  # Non-empty line
                        indented_lines.append("    " + line)
                    else:
                        indented_lines.append("")  # Preserve empty lines
                indented_code = "\n".join(indented_lines)
            else:
                # Single line code
                indented_code = "    " + code

            async_command = f"""
async def __execute_command():
{indented_code}
    
__result = __execute_command()
"""
            exec(compile(async_command, "<string>", "exec"), execution_context)
            result = (
                await execution_context["__result"]
                if "__result" in execution_context
                else None
            )

            # Build response message
            response_parts = []
            if captured_output:
                response_parts.append("Output: " + "\n".join(captured_output))
            if result is not None:
                response_parts.append(f"Return value: {result}")
            if not response_parts:
                response_parts.append("Command executed successfully")

            result_str = "\n".join(response_parts)

            # Record this as a code modification
            # With exception trap instrumentation, we always have reliable exception context

            # Get the workflow file path
            workflow_file = os.environ.get("VA_WORKFLOW_FILE")
            print(f"🔍 Looking for exception in workflow file: {workflow_file}")

            # Get the traceback from the original exception
            tb = self.session.original_exception.__traceback__
            target_line = None

            # Walk through the traceback to find a frame in the actual workflow file
            while tb:
                frame = tb.tb_frame
                frame_filename = frame.f_code.co_filename
                print(f"  Checking frame: {frame_filename}, line {tb.tb_lineno}")

                # Check if this frame is in the user's workflow file
                if workflow_file:
                    try:
                        if os.path.samefile(frame_filename, workflow_file):
                            target_line = tb.tb_lineno
                            print(
                                f"🔍 Found exception at line {target_line} in workflow file {frame_filename}"
                            )
                            break
                    except (OSError, FileNotFoundError):
                        # Files might not exist or be comparable, try string comparison
                        if os.path.abspath(frame_filename) == os.path.abspath(
                            workflow_file
                        ):
                            target_line = tb.tb_lineno
                            print(
                                f"🔍 Found exception at line {target_line} in workflow file (string match)"
                            )
                            break

                tb = tb.tb_next

            # With exception trap, we always have the exact exception location
            if target_line:
                # Calculate the appropriate insertion line
                insertion_line = self._calculate_insertion_line(target_line)

                # Determine proper indentation from the target line
                current_workflow_code = self.session.get_final_workflow_code()
                lines = current_workflow_code.split("\n")
                if target_line <= len(lines):
                    original_line = lines[target_line - 1]
                    indentation = len(original_line) - len(original_line.lstrip())
                    # Apply indentation to each line of the code
                    indented_lines = []
                    for line in code.split("\n"):
                        if line.strip():  # Non-empty line
                            indented_lines.append(" " * indentation + line)
                        else:
                            indented_lines.append("")  # Preserve empty lines
                    indented_code = "\n".join(indented_lines)
                else:
                    # Fallback: use default indentation
                    indented_lines = []
                    for line in code.split("\n"):
                        if line.strip():
                            indented_lines.append(f"        {line}")
                        else:
                            indented_lines.append("")
                    indented_code = "\n".join(indented_lines)

                await self.update_workflow_code(insertion_line, indented_code)
                print(f"🔍 Inserting code at line {insertion_line}: {code.strip()}")

                # Update the final workflow code environment variable immediately
                final_code = self.session.get_final_workflow_code()
                os.environ["VA_FINAL_WORKFLOW_CODE"] = final_code
            else:
                print(
                    "⚠️  Could not determine exception line in workflow file, using fallback"
                )
                # Fallback: insert at the end of the workflow
                current_workflow_code = self.session.get_final_workflow_code()
                lines = current_workflow_code.split("\n")
                # Find the last line that contains actual code (not empty or just whitespace)
                for i in range(len(lines) - 1, -1, -1):
                    if lines[i].strip() and not lines[i].strip().startswith("#"):
                        target_line = i + 1  # Insert after this line

                        # Determine proper indentation from the found line
                        original_line = lines[i]
                        indentation = len(original_line) - len(original_line.lstrip())
                        indented_lines = []
                        for line in code.split("\n"):
                            if line.strip():
                                indented_lines.append(" " * indentation + line)
                            else:
                                indented_lines.append("")
                        indented_code = "\n".join(indented_lines)

                        await self.update_workflow_code(target_line, indented_code)
                        print(
                            f"🔍 Using fallback: inserting at line {target_line}: {code.strip()}"
                        )
                        break

            return result_str

        except Exception as e:
            error_msg = f"Execution error: {str(e)}"
            log.error(error_msg)
            return error_msg

    def _calculate_insertion_line(self, original_target_line: int) -> int:
        """
        Calculate the appropriate insertion line considering existing modifications.
        With exception trap instrumentation, we can uniformly handle all exceptions.

        Args:
            original_target_line: The original exception line number

        Returns:
            The line number where the next insertion should occur
        """
        # Check if there are any replacements that affect the target line
        for start_line, end_line, _ in self.session.code_buffer.replacements:
            if start_line <= original_target_line <= end_line:
                # If the target line was replaced, insert after the replacement
                return start_line + 1

        # With exception trap, we insert at the exception location
        # This allows the recovery to add code at the exact failure point
        insertions_at_line = len(
            [
                ins
                for ins in self.session.code_buffer.insertions
                if ins[0] == original_target_line
            ]
        )

        # Insert at the target line, accounting for existing insertions
        return original_target_line + insertions_at_line

    async def update_workflow_code(self, line_number: int, code: str) -> None:
        """
        Queue code insertion at a specific line in the workflow.

        Args:
            line_number: Line number to insert code (1-based)
            code: Code to insert
        """
        # Queue the insertion in the buffer
        self.session.code_buffer.queue_insertion(line_number, code)

    async def replace_workflow_code(
        self, start_line: int, end_line: int, new_code: str
    ) -> None:
        """
        Queue code replacement for a range of lines in the workflow.

        Args:
            start_line: Starting line number to replace (1-based, inclusive)
            end_line: Ending line number to replace (1-based, inclusive)
            new_code: New code to replace the range with
        """
        # Queue the replacement in the buffer
        self.session.code_buffer.queue_replacement(start_line, end_line, new_code)

    async def replace_faulty_code(self, code: str) -> str:
        """
        Replace faulty code at the exception location with corrected code using CST parsing.

        Args:
            code: The corrected code to use as replacement

        Returns:
            String representation of the operation result
        """
        try:
            # Check if this is a browser context or general code context
            local_vars = self.session.execution_context.get("local_vars", {})
            page = local_vars.get("page")
            has_browser_context = self.session.has_browser_context

            if has_browser_context and not page:
                return "Error: No page object found in execution context"

            # Check if page is still alive (only for browser contexts)
            if has_browser_context:
                try:
                    current_url = page.url
                    print(f"🔍 Current page URL: {current_url}")
                except Exception as page_error:
                    print(f"⚠️  Page object is no longer valid: {page_error}")
                    return f"Error: Page object is no longer valid: {page_error}"
            else:
                print("🔍 General code context - no page validation needed")

            # Get the workflow file path
            workflow_file = os.environ.get("VA_WORKFLOW_FILE")

            # Get the traceback from the original exception to find the faulty lines
            tb = self.session.original_exception.__traceback__
            target_lines = []

            # Walk through the traceback to find frames in the actual workflow file
            while tb:
                frame = tb.tb_frame
                frame_filename = frame.f_code.co_filename

                # For general code recovery, we may not have VA_WORKFLOW_FILE set
                # In that case, use any frame that's not from system/library files
                if workflow_file:
                    # Browser workflow case - use the specific workflow file
                    try:
                        if os.path.samefile(frame_filename, workflow_file):
                            target_line = tb.tb_lineno
                            target_lines.append(target_line)
                            print(
                                f"🔍 Found exception at line {target_line} in workflow file {frame_filename}"
                            )
                    except (OSError, ValueError):
                        # Files don't exist or can't be compared, skip
                        pass
                else:
                    # General code recovery case - find user code frames (not system/library)
                    if not any(
                        sys_path in frame_filename
                        for sys_path in [
                            "/usr/",
                            "/Library/",
                            "site-packages",
                            ".venv",
                            "__pycache__",
                        ]
                    ):
                        target_line = tb.tb_lineno
                        target_lines.append(target_line)
                        print(
                            f"🔍 Found exception at line {target_line} in user code {frame_filename}"
                        )

                tb = tb.tb_next

            if not target_lines:
                return "Error: Could not determine exception location in user code"

            # Use CST to find the statement containing the exception
            exception_line = target_lines[
                0
            ]  # Use the first (deepest) exception location
            start_line, end_line = self._find_statement_bounds_with_cst(
                self.session.original_workflow_code, exception_line
            )

            print(
                f"🔍 CST analysis: Replacing faulty code from lines {start_line} to {end_line}"
            )

            # Show the original faulty code
            lines = self.session.original_workflow_code.split("\n")
            print("🔍 Original faulty code:")
            for i in range(start_line - 1, min(end_line, len(lines))):
                print(f"  {i + 1}: {lines[i]}")

            # Determine proper indentation from the original code
            if start_line <= len(lines):
                original_line = lines[start_line - 1]
                indentation = len(original_line) - len(original_line.lstrip())
                # Apply indentation to each line of the replacement code
                code_lines = code.split("\n")
                indented_lines = []
                for i, line in enumerate(code_lines):
                    if line.strip():  # Non-empty line
                        indented_lines.append(" " * indentation + line)
                    else:
                        indented_lines.append("")  # Preserve empty lines
                indented_code = "\n".join(indented_lines)
            else:
                # Fallback indentation - indent each line
                code_lines = code.split("\n")
                indented_lines = []
                for line in code_lines:
                    if line.strip():
                        indented_lines.append(f"        {line}")
                    else:
                        indented_lines.append("")
                indented_code = "\n".join(indented_lines)

            # Queue the replacement
            await self.replace_workflow_code(start_line, end_line, indented_code)
            print(f"🔍 Replacement queued: {code.strip()}")

            # For general code contexts, execute the corrected code immediately to set local variables
            if not has_browser_context:
                try:
                    print(
                        "🔧 Executing corrected code immediately to set local variables..."
                    )

                    # Get the execution frame from the original exception
                    tb = self.session.original_exception.__traceback__
                    execution_frame = None
                    while tb:
                        execution_frame = tb.tb_frame
                        tb = tb.tb_next

                    if execution_frame:
                        # Prepare execution environment with the frame's globals and locals
                        exec_globals = execution_frame.f_globals.copy()
                        exec_locals = execution_frame.f_locals.copy()

                        # Execute the corrected code in the frame's context
                        exec(code, exec_globals, exec_locals)

                        # Update the original frame's local variables
                        for key, value in exec_locals.items():
                            if (
                                key not in execution_frame.f_locals
                                or execution_frame.f_locals[key] != value
                            ):
                                execution_frame.f_locals[key] = value
                                print(f"🔧 Set local variable: {key} = {value}")

                        print("✅ Local variables updated successfully")
                    else:
                        print("⚠️  Could not find execution frame to update variables")

                except Exception as exec_error:
                    print(
                        f"⚠️  Failed to execute corrected code immediately: {exec_error}"
                    )
                    # Continue anyway - the code replacement is still queued

            return f"Replaced faulty code on lines {start_line}-{end_line} with properly indented code"

        except Exception as e:
            error_msg = f"Replacement error: {str(e)}"
            log.error(error_msg)
            return error_msg

    def _find_statement_bounds_with_cst(
        self, source_code: str, target_line: int
    ) -> tuple[int, int]:
        """
        Use libcst to find the exact bounds of the statement containing the target line.

        Args:
            source_code: The source code to analyze
            target_line: The line number where the exception occurred (1-based)

        Returns:
            Tuple of (start_line, end_line) both 1-based and inclusive
        """
        # Parse the source code into a CST
        tree = cst.parse_module(source_code)

        # Use PositionProvider to get line information
        position_provider = cst.metadata.PositionProvider
        wrapper = cst.metadata.MetadataWrapper(tree)

        # Find the statement that contains the target line
        class StatementFinder(cst.CSTVisitor):
            def __init__(self, target_line: int, wrapper: cst.metadata.MetadataWrapper):
                super().__init__()
                self.target_line = target_line
                self.statement_bounds = None
                self.wrapper = wrapper

            def visit_SimpleStatementLine(self, node: cst.SimpleStatementLine) -> None:
                self._check_node_bounds(node)

            def visit_Expr(self, node: cst.Expr) -> None:
                self._check_node_bounds(node)

            def _check_node_bounds(self, node: cst.CSTNode) -> None:
                try:
                    position = self.wrapper.resolve(position_provider).get(node)
                    if position:
                        start_line = position.start.line
                        end_line = position.end.line

                        if start_line <= self.target_line <= end_line:
                            self.statement_bounds = (start_line, end_line)
                except Exception:
                    pass  # Continue searching if metadata fails for this node

        finder = StatementFinder(target_line, wrapper)

        try:
            wrapper.visit(finder)
            if finder.statement_bounds:
                print(f"🔍 CST found statement bounds: {finder.statement_bounds}")
                return finder.statement_bounds
        except Exception as e:
            print(f"🔍 CST metadata analysis failed: {e}")

        # If CST metadata fails, return single line as fallback
        return (target_line, target_line)

    async def get_page_state(self) -> Dict[str, Any]:
        """
        Get current browser page state and DOM information.

        Returns:
            Dictionary containing page state information
        """
        try:
            page = self.session.execution_context.get("local_vars", {}).get("page")
            if not page:
                return {"error": "No page object found in execution context"}

            # Get basic page information - handle sync/async properly
            try:
                if hasattr(page, "url"):
                    url = page.url
                else:
                    # Fallback to unknown if url property doesn't exist
                    url = "Unknown"

                if hasattr(page, "title"):
                    title = await page.title()
                else:
                    title = "Unknown"

                # Get page content (limited for safety)
                if hasattr(page, "content"):
                    content = await page.content()
                    content_preview = (
                        content[:1000] + "..." if len(content) > 1000 else content
                    )
                else:
                    content_preview = "Content unavailable"

                return {
                    "url": url,
                    "title": title,
                    "content_preview": content_preview,
                    "page_available": True,
                }
            except Exception as inner_e:
                # If we fail to get page details, at least return that page exists
                print(f"⚠️  Error getting page details: {inner_e}")
                return {
                    "url": "Unknown",
                    "title": "Unknown",
                    "content_preview": "Error retrieving content",
                    "page_available": True,
                    "error_details": str(inner_e),
                }

        except Exception as e:
            return {"error": f"Failed to get page state: {str(e)}"}

    async def get_execution_context(self) -> Dict[str, Any]:
        """
        Get current execution context including workflow goal and variables.

        Returns:
            Dictionary containing execution context
        """
        return {
            "workflow_goal": self.session.workflow_goal,
            "exception_message": str(self.session.original_exception),
            "exception_type": type(self.session.original_exception).__name__,
            "local_variables": list(
                self.session.execution_context.get("local_vars", {}).keys()
            ),
            "current_line": self.session.execution_context.get("current_line"),
            "modifications_made": (
                len(self.session.code_buffer.insertions)
                + len(self.session.code_buffer.deletions)
                + len(self.session.code_buffer.replacements)
            ),
        }


class RecoverySession:
    """Manages the state and context of a recovery session."""

    def __init__(
        self,
        original_exception: Exception,
        execution_frame,
        workflow_code: str,
        has_browser_context: bool,
    ):
        self.original_exception = original_exception
        self.original_workflow_code = workflow_code  # Keep original for reference
        self.code_buffer = CodeModificationBuffer(workflow_code)
        self.ready_to_continue = False
        self.has_browser_context = has_browser_context

        # Recovery action tracking for PDB resumption
        self.continue_action = None  # "retry" or "skip"
        self.exception_line = self._extract_exception_line(execution_frame)

        # Extract execution context from the frame
        self.execution_context = self._extract_execution_context(execution_frame)
        self.workflow_goal = self._extract_workflow_goal(execution_frame)

        # Initialize tools
        self.tools = RecoveryTools(self)

    async def handle_tool_call(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """Handle tool calls from the LLM."""
        try:
            if tool_name == "get_page_state":
                state = await self.tools.get_page_state()
                return json.dumps(state, indent=2)

            elif tool_name == "execute_code":
                code = tool_input.get("code", "")
                result = await self.tools.execute_python_command(code)
                return f"Executed: {code}\nResult: {result}"

            elif tool_name == "insert_code":
                code = tool_input.get("code", "")
                result = await self.tools.execute_python_command(code)
                return f"Code inserted successfully: {code}\nResult: {result}"

            elif tool_name == "replace_code":
                code = tool_input.get("code", "")
                result = await self.tools.replace_faulty_code(code)
                return f"Code replaced successfully: {code}\nResult: {result}"

            elif tool_name == "continue_workflow":
                action = tool_input.get("action", "retry")
                reason = tool_input.get("reason", "")
                # Store the continue action for PDB resumption
                self.continue_action = action
                return f"Continuing workflow with action='{action}': {reason}"

            else:
                return f"Unknown tool: {tool_name}"

        except Exception as e:
            return f"Tool execution failed: {str(e)}"

    def _extract_exception_line(self, frame) -> int:
        """Extract the line number where the exception occurred."""
        try:
            # Try to get line number from current frame
            if frame and hasattr(frame, "f_lineno"):
                return frame.f_lineno

            # Try to get line from exception traceback
            if (
                hasattr(self, "original_exception")
                and self.original_exception.__traceback__
            ):
                tb = self.original_exception.__traceback__
                while tb:
                    if tb.tb_frame == frame:
                        return tb.tb_lineno
                    tb = tb.tb_next

            # Fallback to first available line number
            return getattr(frame, "f_lineno", 1) if frame else 1
        except Exception as e:
            log.error(f"Failed to extract exception line: {e}")
            return 1

    def _extract_execution_context(self, frame) -> Dict[str, Any]:
        """Extract execution context from the current frame."""
        try:
            context = {
                "local_vars": frame.f_locals.copy() if frame else {},
                "global_vars": frame.f_globals.copy() if frame else {},
                "current_line": frame.f_lineno if frame else None,
                "filename": frame.f_code.co_filename if frame else None,
                "function_name": frame.f_code.co_name if frame else None,
            }

            # If no page object in current frame, walk back through exception traceback
            if "page" not in context["local_vars"] and hasattr(
                self, "original_exception"
            ):
                tb = self.original_exception.__traceback__
                while tb:
                    tb_frame = tb.tb_frame
                    if "page" in tb_frame.f_locals:
                        print(
                            f"🔍 Found page object in frame: {tb_frame.f_code.co_name}"
                        )
                        page_obj = tb_frame.f_locals["page"]
                        print(f"🔍 Page object type in frame: {type(page_obj)}")
                        print(
                            f"🔍 Page object has url method: {hasattr(page_obj, 'url')}"
                        )
                        context["local_vars"].update(tb_frame.f_locals)
                        break
                    tb = tb.tb_next

            print(
                f"🔍 Execution context variables: {list(context['local_vars'].keys())}"
            )

            # Debug the actual page object we captured
            if "page" in context["local_vars"]:
                page_obj = context["local_vars"]["page"]
                print(f"🔍 Final page object type: {type(page_obj)}")
                print(f"🔍 Final page object repr: {repr(page_obj)}")

            return context
        except Exception as e:
            log.error(f"Failed to extract execution context: {e}")
            return {}

    def _extract_workflow_goal(self, frame) -> str:
        """Extract workflow goal from function docstring."""
        try:
            # Try multiple approaches to extract the workflow goal

            # Approach 1: Walk up the call stack to find the main function
            current_frame = frame
            while current_frame:
                if current_frame.f_code.co_name == "main":
                    # Try to get the module from globals
                    main_func = current_frame.f_globals.get("main")
                    if main_func and callable(main_func):
                        docstring = inspect.getdoc(main_func)
                        if docstring:
                            return docstring

                    # Try to get module from inspect
                    module = inspect.getmodule(current_frame)
                    if module and hasattr(module, "main"):
                        main_func = getattr(module, "main")
                        docstring = inspect.getdoc(main_func)
                        if docstring:
                            return docstring

                current_frame = current_frame.f_back

            # Approach 2: Check for common workflow patterns in the original workflow code
            if hasattr(self, "original_workflow_code") and self.original_workflow_code:
                lines = self.original_workflow_code.split("\n")
                for line in lines:
                    line = line.strip()
                    # Look for docstring patterns
                    if line.startswith('"""') and not line.endswith('"""'):
                        # Multi-line docstring
                        for i, next_line in enumerate(
                            lines[lines.index(line) + 1 :], 1
                        ):
                            if next_line.strip().endswith('"""'):
                                docstring = "\n".join(
                                    lines[lines.index(line) : lines.index(line) + i + 1]
                                )
                                docstring = docstring.strip('"""').strip()
                                if docstring:
                                    return docstring
                                break
                    elif (
                        line.startswith('"""')
                        and line.endswith('"""')
                        and len(line) > 6
                    ):
                        # Single line docstring
                        docstring = line.strip('"""').strip()
                        if docstring:
                            return docstring

            return "No specific workflow goal found - will analyze current state to determine next steps"
        except Exception as e:
            log.error(f"Failed to extract workflow goal: {e}")
            return "No specific workflow goal found - will analyze current state to determine next steps"

    def get_final_workflow_code(self) -> str:
        """Get the final modified workflow code."""
        return self.code_buffer.apply_all_modifications()

    def get_modification_summary(self) -> str:
        """Get a summary of all modifications made during recovery."""
        return self.code_buffer.get_modification_summary()
