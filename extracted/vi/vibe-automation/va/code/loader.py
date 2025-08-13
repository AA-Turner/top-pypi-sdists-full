"""Load user provided code and add instrumentation for use to capture exceptions"""

import ast
import sys
import logging
from typing import Any, Optional
from pathlib import Path
import importlib.util
from importlib.machinery import ModuleSpec
from importlib.abc import Loader as BaseLoader

log = logging.getLogger(__name__)


class InstrumentationTransformer(ast.NodeTransformer):
    """AST transformer that wraps statements with ExceptionTrap context manager"""

    def __init__(self, module_name: str):
        self.module_name = module_name
        self.in_function = False
        self.in_async_function = False
        self.function_depth = 0

    def visit_Module(self, node: ast.Module) -> ast.Module:
        """Visit module and instrument top-level statements"""
        node.body = self._instrument_body(node.body)
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """Visit function definition and process its body"""
        self.function_depth += 1
        was_in_function = self.in_function
        was_in_async_function = self.in_async_function
        self.in_function = True
        self.in_async_function = False  # This is a sync function

        # Transform the function body
        node.body = self._instrument_body(node.body)

        # Don't call generic_visit to avoid double processing

        self.in_function = was_in_function
        self.in_async_function = was_in_async_function
        self.function_depth -= 1
        return node

    def visit_AsyncFunctionDef(
        self, node: ast.AsyncFunctionDef
    ) -> ast.AsyncFunctionDef:
        """Visit async function definition and process its body"""
        self.function_depth += 1
        was_in_function = self.in_function
        was_in_async_function = self.in_async_function
        self.in_function = True
        self.in_async_function = True  # This is an async function

        # Transform the function body
        node.body = self._instrument_body(node.body)

        # Don't call generic_visit to avoid double processing

        self.in_function = was_in_function
        self.in_async_function = was_in_async_function
        self.function_depth -= 1
        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        """Visit class definition and process its methods"""
        # Process the class body (which contains methods)
        for i, item in enumerate(node.body):
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                node.body[i] = self.visit(item)
        return node

    def visit_With(self, node: ast.With) -> ast.With:
        """Visit with statement and instrument its body"""
        # Recursively instrument the body of the with statement
        node.body = self._instrument_body(node.body)
        return node

    def visit_AsyncWith(self, node: ast.AsyncWith) -> ast.AsyncWith:
        """Visit async with statement and instrument its body"""
        # Recursively instrument the body of the async with statement
        node.body = self._instrument_body(node.body)
        return node

    def _instrument_body(self, body: list[ast.stmt]) -> list[ast.stmt]:
        """Instrument a list of statements by wrapping each with ExceptionTrap"""
        if not body:
            return body

        instrumented = []

        for stmt in body:
            # Handle function/class definitions specially - visit them but don't wrap
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                instrumented.append(self.visit(stmt))
                continue

            # Handle with statements specially - instrument their bodies, then wrap the whole thing
            if isinstance(stmt, (ast.With, ast.AsyncWith)):
                # First visit the with statement to instrument its body
                visited_stmt = self.visit(stmt)
                # Then wrap the entire with statement
                wrapped = self._wrap_statement_with_trap(visited_stmt)
                instrumented.append(wrapped)
                continue

            # Skip certain statement types that shouldn't be wrapped
            if self._should_skip_statement(stmt):
                instrumented.append(stmt)
                continue

            # Create the wrapped statement
            wrapped = self._wrap_statement_with_trap(stmt)
            instrumented.append(wrapped)

        return instrumented

    def _should_skip_statement(self, stmt: ast.stmt) -> bool:
        """Check if a statement should be skipped from instrumentation"""
        # Skip import statements
        if isinstance(stmt, (ast.Import, ast.ImportFrom)):
            return True

        # Skip global/nonlocal declarations
        if isinstance(stmt, (ast.Global, ast.Nonlocal)):
            return True

        # Skip function/class definitions themselves (but their bodies will be instrumented)
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            return True

        # Skip docstrings (expression statements with string constants)
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
            if isinstance(stmt.value.value, str):
                return True

        # Skip pass statements
        if isinstance(stmt, ast.Pass):
            return True

        return False

    def _wrap_statement_with_trap(self, stmt: ast.stmt) -> ast.stmt:
        """Wrap a statement with the appropriate trap context manager based on async context"""

        # Choose the appropriate trap based on whether we're in an async function
        if self.in_async_function:
            # Create: async with va.exception_trap: <statement>
            context_expr = ast.Attribute(
                value=ast.Name(id="va", ctx=ast.Load()),
                attr="exception_trap",
                ctx=ast.Load(),
            )

            # Create the async with statement
            with_stmt = ast.AsyncWith(
                items=[ast.withitem(context_expr=context_expr, optional_vars=None)],
                body=[stmt],
            )
        else:
            # Create: with va.exception_trap: <statement>
            context_expr = ast.Attribute(
                value=ast.Name(id="va", ctx=ast.Load()),
                attr="exception_trap",
                ctx=ast.Load(),
            )

            # Create the sync with statement
            with_stmt = ast.With(
                items=[ast.withitem(context_expr=context_expr, optional_vars=None)],
                body=[stmt],
            )

        # Copy location information from the original statement
        ast.copy_location(with_stmt, stmt)

        return with_stmt


class InstrumentedLoader(BaseLoader):
    """Custom loader that instruments code with exception trapping"""

    def __init__(self, original_loader: BaseLoader, filepath: str):
        self.original_loader = original_loader
        self.filepath = filepath

    def exec_module(self, module: Any) -> None:
        """Execute the module with instrumentation"""
        # Read the source code
        source = Path(self.filepath).read_text()

        # Parse into AST
        tree = ast.parse(source, filename=self.filepath)

        # Apply instrumentation
        transformer = InstrumentationTransformer(module.__name__)
        instrumented_tree = transformer.visit(tree)

        # Fix missing locations in the AST
        ast.fix_missing_locations(instrumented_tree)

        # Compile the instrumented AST
        code = compile(instrumented_tree, self.filepath, "exec")

        # Import va to make va.exception_trap available
        import va

        module.__dict__["va"] = va

        # Execute the instrumented code in the module's namespace
        exec(code, module.__dict__)

    def create_module(self, spec: ModuleSpec) -> Optional[Any]:
        """Create module (delegate to original loader if it exists)"""
        if hasattr(self.original_loader, "create_module"):
            return self.original_loader.create_module(spec)
        return None


def load_instrumented_module(filepath: Path) -> Any:
    """Load a Python module with exception trap instrumentation"""
    module_name = filepath.stem

    # Create a module spec
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not create spec for {filepath}")

    # Replace the loader with our instrumented version
    original_loader = spec.loader
    spec.loader = InstrumentedLoader(original_loader, str(filepath))

    # Create and execute the module
    module = importlib.util.module_from_spec(spec)

    # Add to sys.modules so imports work
    sys.modules[module_name] = module

    # Execute the module
    spec.loader.exec_module(module)

    return module


def debug_print_instrumented_code(filepath: Path) -> str:
    """Debug function to print the instrumented code without executing it"""
    source = filepath.read_text()
    tree = ast.parse(source, filename=str(filepath))

    transformer = InstrumentationTransformer(filepath.stem)
    instrumented_tree = transformer.visit(tree)
    ast.fix_missing_locations(instrumented_tree)

    # Convert back to Python code for debugging
    return ast.unparse(instrumented_tree)
