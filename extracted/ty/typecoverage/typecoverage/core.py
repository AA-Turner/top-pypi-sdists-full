"""
Typecoverage: strict CLI + library API to report untyped vars, args, returns.

Inputs accepted (CLI or API):
- Code strings
- Code objects
- Frame objects
- Functions or classes
- Path strings (globs like "**/*.py")
- ``pathlib.Path`` objects (files or directories)

Fully type hinted. Google-style docstrings. All imports are at top and use
``from a import b`` style.
"""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
from ast import (
    AST,
    AnnAssign,
    Assign,
    AsyncFor,
    AsyncFunctionDef,
    AsyncWith,
    Attribute,
    AugAssign,
    ClassDef,
    DictComp,
    ExceptHandler,
    For,
    FunctionDef,
    GeneratorExp,
    ListComp,
    Name,
    NamedExpr,
    NodeVisitor,
    SetComp,
    With,
    arg,
    comprehension,
    parse,
    withitem,
)
from ast import List as AstList
from ast import Tuple as AstTuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import suppress
from dataclasses import dataclass
from enum import Enum
from glob import glob
from inspect import getsource, stack
from json import dumps
from linecache import getline
from os import cpu_count, environ
from pathlib import Path
from re import IGNORECASE, Match, Pattern, compile
from sys import exit, platform, stdout
from textwrap import dedent, indent
from types import CodeType, FrameType, FunctionType, ModuleType
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    Union,
)

tomllib: Optional[Any] = None
with suppress(Exception):
    import tomllib

VERSION: str = "2.1.1"


class Emoji(Enum):
    """Emojis used throughout the application."""

    # Status indicators
    CHECK_MARK = "✓"
    CROSS_MARK = "❌"
    ARROW_RIGHT = "►"
    # File and folder icons
    FOLDER = "📁"
    CHART = "📊"
    BULB = "💡"
    # Category indicators
    RED_CIRCLE = "🔴"
    YELLOW_CIRCLE = "🟡"
    BLUE_CIRCLE = "🔵"


class Indentation:
    """Standardized indentation levels."""

    LEVEL_0: str = " "
    LEVEL_1: str = "  "
    LEVEL_2: str = "    "
    LEVEL_3: str = "      "
    LEVEL_4: str = "        "


class Colors(Enum):
    """ANSI color codes for terminal output."""

    # Core colors
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    # Text colors
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    GRAY = "\033[90m"
    # Bright colors
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    @classmethod
    def supports_color(cls) -> bool:
        """Check if terminal supports ANSI colors."""
        if environ.get("NO_COLOR"):
            return False
        if environ.get("FORCE_COLOR"):
            return True
        if not hasattr(stdout, "isatty") or not stdout.isatty():
            return False
        return environ.get("TERM", "") != "dumb"


IssueType = Literal[
    "untyped-argument",
    "untyped-return",
    "untyped-variable",
]

ScopeKind = Literal[
    "module",
    "function",
    "class",
    "comp",
    "other",
]

TargetLike = Union[
    str,
    Path,
    CodeType,
    FrameType,
    FunctionType,
    Type[Any],
    ModuleType,
    Callable,
]


@dataclass(frozen=True)
class Issue:
    """One finding of a missing annotation.

    Attributes:
        file: File path or pseudo-name where the issue was found.
        line: 1-based line number for the issue.
        column: 0-based column offset for the issue.
        type: Kind of issue (argument, return, variable).
        name: Identifier involved (function or variable name).
        context: Optional lines of source context around the issue.
    """

    file: Path
    line: int
    column: int
    type: IssueType
    name: str
    context: List[str]


@dataclass
class Stats:
    """Aggregate counters for issues.

    Attributes:
        total: Total number of issues.
        by_type: Mapping from IssueType to count.
    """

    total: int
    by_type: MutableMapping[IssueType, int]


@dataclass
class Scope:
    """Track state for a lexical scope.

    Attributes:
        kind: Scope kind (module, function, class, comp, other).
        defined: Names first defined in this scope.
        annotated: Names annotated in this scope.
        globals_: Names declared global in this scope.
        nonlocals: Names declared nonlocal in this scope.
    """

    kind: ScopeKind
    defined: Set[str]
    annotated: Set[str]
    globals_: Set[str]
    nonlocals: Set[str]


class TypeCoverage:
    """Main type checking class that handles all analysis functionality."""

    def __init__(self) -> None:
        """Initialize the TypeCoverage."""
        self.context_lines: int = 0

    # -------------------- config --------------------

    def _load_pyproject(self) -> Dict[str, Any]:
        """Load tool config from pyproject.toml if present."""
        if tomllib is None:
            return {}
        pp: Path = Path.cwd() / "pyproject.toml"
        if pp.exists():
            with suppress(Exception):
                data: Dict[str, Any] = tomllib.loads(pp.read_text("utf-8"))
                tool: Dict[str, Any] = data.get("tool", {})
                return dict(tool.get("typecoverage", {}))
        return {}

    # -------------------- suppression --------------------
    class CommentSuppression:
        """Detect type ignore and noqa suppressions."""

        TYPE_IGNORE_PATTERNS: List[Pattern[str]] = [
            compile(r"#\s*type\s*:\s*ignore(?:\[([^\]]+)\])?", IGNORECASE),
            compile(r"#\s*pyright\s*:\s*ignore(?:\[([^\]]+)\])?", IGNORECASE),
            compile(r"#\s*mypy\s*:\s*ignore(?:\[([^\]]+)\])?", IGNORECASE),
        ]
        NOQA_PATTERNS: List[Pattern[str]] = [
            compile(r"#\s*noqa(?:\s*:\s*([A-Z0-9,\s]+))?", IGNORECASE),
            compile(r"#\s*flake8\s*:\s*noqa(?:\s*:\s*([A-Z0-9,\s]+))?",
                    IGNORECASE),
            compile(r"#\s*ruff\s*:\s*noqa(?:\s*:\s*([A-Z0-9,\s]+))?",
                    IGNORECASE),
        ]
        ISSUE_TYPE_CODES: Dict[IssueType, Set[str]] = {
            "untyped-argument": {
                "ANN001",
                "ANN002",
                "ANN003",
                "ANN101",
                "ANN102",
                "ANN201",
                "ANN202",
                "reportMissingParameterType",
                "reportUntypedFunctionDecorator",
                "arg-type",
                "no-untyped-def",
                "type-arg",
            },
            "untyped-return": {
                "ANN201",
                "ANN202",
                "reportMissingReturnType",
                "reportUntypedFunctionDecorator",
                "return-value",
                "no-untyped-def",
                "type-return",
            },
            "untyped-variable": {
                "ANN001",
                "var-annotated",
                "reportMissingTypeStubs",
                "reportUnknownVariableType",
                "name-defined",
                "no-untyped-def",
                "type-var",
            },
        }

        @classmethod
        def is_suppressed(cls, line_text: str, issue_type: IssueType) -> bool:
            """Check if an issue type is suppressed by comments on the line.

            Args:
                line_text: The text content of the line to check.
                issue_type: The type of issue to check suppression for.

            Returns:
                bool: True if the issue is suppressed, False otherwise.
            """
            for pattern in cls.TYPE_IGNORE_PATTERNS:
                match: Optional[Match[str]] = pattern.search(line_text)
                if match:
                    codes: Optional[str] = match.group(1)
                    if codes is None:
                        return True
                    relevant: Set[str] = cls.ISSUE_TYPE_CODES.get(
                        issue_type, set())
                    specified: List[str] = [
                        c.strip() for c in codes.split(",")
                    ]
                    if any(code in relevant for code in specified):
                        return True
            for pattern in cls.NOQA_PATTERNS:
                match = pattern.search(line_text)
                if match:
                    codes = match.group(1)
                    if codes is None:
                        return True
                    relevant = cls.ISSUE_TYPE_CODES.get(issue_type, set())
                    specified = [c.strip() for c in codes.split(",")]
                    if any(code in relevant for code in specified):
                        return True
            return False

    # -------------------- AST visitor --------------------
    class UntypedVisitor(NodeVisitor):
        """AST visitor that records untyped constructs with real scoping.

        Each scope tracks first definitions and annotations. Only the initial
        untyped introduction of a name in its owning scope is reported.
        """

        def __init__(
            self,
            *,
            source: str,
            file: Path,
            context_lines: int,
            ignore_underscore_vars: bool = True,
            ignore_comprehensions: bool = True,
            ignore_except_vars: bool = True,
            ignore_for_targets: bool = True,
            ignore_context_vars: bool = True,
        ) -> None:
            """Init the visitor."""
            super().__init__()
            self.file: Path = file
            self.source_lines: List[str] = dedent(source).splitlines()
            self.issues: List[Issue] = []
            self.context_lines: int = context_lines
            self.ignore_underscore_vars: bool = ignore_underscore_vars
            self.ignore_comprehensions: bool = ignore_comprehensions
            self.ignore_except_vars: bool = ignore_except_vars
            self.ignore_for_targets: bool = ignore_for_targets
            self.ignore_context_vars: bool = ignore_context_vars
            self.typing_imports: Set[str] = set()
            self.in_for_loop: bool = False
            self._enum_depth: int = 0
            self._enum_classes: Set[str] = set()
            self._scopes: List[Scope] = [
                Scope(
                    kind="module",
                    defined=set(),
                    annotated=set(),
                    globals_=set(),
                    nonlocals=set(),
                )
            ]

        # ---------------- scope helpers
        def _push(self, kind: ScopeKind) -> None:
            """Push a new scope onto the scope stack."""
            self._scopes.append(
                Scope(
                    kind=kind,
                    defined=set(),
                    annotated=set(),
                    globals_=set(),
                    nonlocals=set(),
                ))

        def _pop(self) -> None:
            """Pop the current scope from the scope stack."""
            self._scopes.pop()

        def _cur(self) -> Scope:
            """Get the current scope."""
            return self._scopes[-1]

        def _module(self) -> Scope:
            """Get the module-level scope."""
            return self._scopes[0]

        def _resolve_def_scope(self, name: str) -> Scope:
            """Resolve the scope where a name is defined.

            Searches enclosing scopes for global or nonlocal declarations
            to determine the correct scope for a variable definition.

            Args:
                name: The name of the variable to resolve.

            Returns:
                Scope: The scope where the name is defined.
            """
            cur: Scope = self._cur()
            if name in cur.globals_:
                return self._module()
            if name in cur.nonlocals:
                i: int
                for i in range(len(self._scopes) - 2, 0, -1):
                    parent: Scope = self._scopes[i]
                    if parent.kind in ("function", "class", "other", "comp"):
                        return parent
            return cur

        # ---------------- utilities
        def _record_issue(self, *, node: AST, type_: IssueType,
                          name: str) -> None:
            """Record a type annotation issue.

            Creates an Issue object with relevant context and adds it to the
            list of issues if it's not suppressed by comments.

            Args:
                node: The AST node where the issue occurred.
                type_: The type of the issue (e.g., 'untyped-argument').
                name: The name of the variable or function involved.
            """
            lineno: int = getattr(node, "lineno", 1)
            col: int = getattr(node, "col_offset", 0)
            if 1 <= lineno <= len(self.source_lines):
                line_text: str = self.source_lines[lineno - 1]
                if TypeCoverage.CommentSuppression.is_suppressed(
                        line_text, type_):
                    return
            if lineno > 1:
                prev_line: str = self.source_lines[lineno - 2]
                if TypeCoverage.CommentSuppression.is_suppressed(
                        prev_line, type_):
                    return
            ctx: List[str] = self._get_context(lineno)
            issue: Issue = Issue(
                file=self.file,
                line=lineno,
                column=col,
                type=type_,
                name=name,
                context=ctx,
            )
            self.issues.append(issue)

        def _get_context(self, lineno: int) -> List[str]:
            """Get source code context lines around a given line number.

            Args:
                lineno: The line number to center the context around.

            Returns:
                List[str]: List of context lines from the source code.
            """
            if self.context_lines <= 0:
                return []
            start: int = max(1, lineno - self.context_lines)
            end: int = min(len(self.source_lines), lineno + self.context_lines)
            lines: List[str] = []
            i: int
            for i in range(start - 1, end):
                if i < len(self.source_lines):
                    lines.append(self.source_lines[i])
            return lines

        def _name_targets(self, target: AST) -> List[Any]:
            """Extract Name nodes from assignment targets.

            Recursively extracts all Name nodes from assignment targets,
            handling both simple names and complex targets like tuples
            and lists that may contain multiple names.

            Args:
                target: The AST node representing an assignment target.

            Returns:
                List[Name]: List of Name nodes found in the target.
            """
            names: List[Name] = []
            if isinstance(target, Name):
                names.append(target)
            elif isinstance(target, (AstTuple, AstList)):
                elt: AST
                for elt in target.elts:
                    names.extend(self._name_targets(elt))
            return names

        def _is_typing_import(self, name: str) -> bool:
            """Check if a name is from the typing module.

            Args:
                name: The identifier name to check.

            Returns:
                bool: True if the name is from typing imports.
            """
            return name in self.typing_imports

        def _is_enum_base(self, expr: AST) -> bool:
            """Check if an expression represents an Enum base class.

            Determines whether an AST expression represents an Enum class
            or one of its variants (IntEnum, StrEnum, Flag, IntFlag) from
            either direct imports or the enum module, or other enum classes
            that have been defined.

            Args:
                expr: The AST expression to check.

            Returns:
                bool: True if the expression is an Enum base class.
            """
            if isinstance(expr, Name):
                # Check for standard enum types
                if expr.id in {
                        "Enum",
                        "IntEnum",
                        "StrEnum",
                        "Flag",
                        "IntFlag",
                }:
                    return True
                # Check if this is a previously defined enum class
                # For simplicity, we'll track enum class names
                if hasattr(self,
                           '_enum_classes') and expr.id in self._enum_classes:
                    return True
            if isinstance(expr, Attribute):
                return getattr(expr.value, "id",
                               "") == "enum" and expr.attr in {
                                   "Enum",
                                   "IntEnum",
                                   "StrEnum",
                                   "Flag",
                                   "IntFlag",
                               }
            return False

        def _is_type_alias(self, node: AST) -> bool:
            """Determine if a variable assignment is a type alias.

            Checks if the assignment involves typing module constructs to
            identify type aliases, which are generally not reported as
            untyped variables.

            Args:
                node: The AST node representing the assignment target.

            Returns:
                bool: True if the assignment is likely a type alias.
            """
            # Enum members do not require annotations.
            if self._enum_depth > 0:
                return True
            assign_node: Optional[Name] = getattr(node, "parent_assign", None)
            value: Optional[AST] = getattr(assign_node, "value", None)
            value_id: Optional[str] = getattr(value, "id", None)
            value_value: Optional[AST] = getattr(value, "value", None)
            value_value_id: Optional[str] = getattr(value_value, "id", None)
            value_value_value: Optional[AST] = getattr(value_value, "value",
                                                       None)
            value_value_value_id: Optional[str] = getattr(
                value_value_value, "id", None)
            value_func: Optional[AST] = getattr(value, "func", None)
            value_func_id: Optional[str] = getattr(value_func, "id", None)
            value_func_value: Optional[AST] = getattr(value_func, "value",
                                                      None)
            value_func_value_id: Optional[str] = getattr(
                value_func_value, "id", None)
            if assign_node is not None and value is not None:
                if value_id is not None and value_id in self.typing_imports:
                    return True
                if hasattr(value, "func"):
                    if (value_func_id is not None
                            and value_func_id in self.typing_imports):
                        return True
                    if value_func_value_id == "typing":
                        return True
                if value_value is not None:
                    if (value_value_id is not None
                            and value_value_id in self.typing_imports):
                        return True
                    if value_value_value_id == "typing":
                        return True
            return False

        def _is_method_parameter(self, name: str, func: AST) -> bool:
            """Check if a parameter is a conventional 'self' or 'cls'
            parameter.

            Args:
                name: The parameter name to check.
                func: The AST node for the function definition.

            Returns:
                bool: True if the parameter is a conventional self/cls param.
            """
            if not isinstance(func, (FunctionDef, AsyncFunctionDef)):
                return False
            if (func.args.vararg and func.args.vararg.arg == name) or (
                    func.args.kwarg and func.args.kwarg.arg == name):
                return True
            if (func.args.args and len(func.args.args) > 0
                    and func.args.args[0].arg == name):
                if name in ("self", "cls", "mcs", "metacls"):
                    return True
                for scope in reversed(self._scopes[:-1]):
                    if scope.kind == "class":
                        return True
            return False

        # ---------------- recorders
        def _mark_param_annotated(self, func: AST) -> None:
            """Mark function parameters as annotated in their scope."""
            if not isinstance(func, (FunctionDef, AsyncFunctionDef)):
                return
            params: List[arg] = (
                list(func.args.posonlyargs) + list(func.args.args) +
                ([func.args.vararg] if func.args.vararg else []) +
                list(func.args.kwonlyargs) +
                ([func.args.kwarg] if func.args.kwarg else []))
            a: Optional[arg]
            for a in params:
                if a is None:
                    continue
                scope: Scope = self._cur()
                scope.defined.add(a.arg)
                if a.annotation is not None:
                    scope.annotated.add(a.arg)

        # ---------------- visitors
        def visit_Import(self, node: Any) -> None:
            """Handle import statements to track typing module imports.

            Processes import statements to identify when the typing module
            or its submodules are imported, which affects type alias detection
            and variable annotation requirements.

            Args:
                node: The Import AST node being visited.
            """
            for alias in node.names:
                if alias.name == "typing":
                    self.typing_imports.add("typing")
                elif alias.name.startswith("typing."):
                    name: str = alias.name.split(".", 1)[1]
                    self.typing_imports.add(name)

        def visit_ImportFrom(self, node: Any) -> None:
            """Handle from-import statements to track typing imports.

            Processes from-import statements to identify typing module
            imports, including star imports that bring in common typing
            constructs like Any, Union, Optional, etc.

            Args:
                node: The ImportFrom AST node being visited.
            """
            if node.module == "typing":
                common_typing_names: List[str] = [
                    "Any",
                    "Union",
                    "Optional",
                    "List",
                    "Dict",
                    "Tuple",
                    "Set",
                    "FrozenSet",
                    "Callable",
                    "Type",
                    "ClassVar",
                    "Literal",
                    "Final",
                    "TypeVar",
                    "Generic",
                    "Protocol",
                    "TypedDict",
                    "NamedTuple",
                    "Sequence",
                    "Mapping",
                    "MutableMapping",
                    "Counter",
                    "Deque",
                    "DefaultDict",
                    "Annotated",
                    "Self",
                    "Never",
                    "NoReturn",
                    "Required",
                    "NotRequired",
                    "TypeAlias",
                    "ParamSpec",
                    "TypeVarTuple",
                    "Unpack",
                    "Concatenate",
                    "LiteralString",
                ]
                for alias in node.names:
                    if alias.name == "*":
                        self.typing_imports.update(common_typing_names)
                    else:
                        self.typing_imports.add(alias.name)

        def visit_Global(self, node: Any) -> None:
            """Handle global declarations in the current scope.

            Processes global statements to track which variables are
            declared as global, affecting how variable definitions are
            resolved to their appropriate scopes.

            Args:
                node: The Global AST node being visited.
            """
            name: str
            for name in node.names:
                self._cur().globals_.add(name)

        def visit_Nonlocal(self, node: Any) -> None:
            """Handle nonlocal declarations in the current scope.

            Processes nonlocal statements to track which variables are
            declared as nonlocal, affecting how variable definitions are
            resolved to their appropriate enclosing scopes.

            Args:
                node: The Nonlocal AST node being visited.
            """
            name: str
            for name in node.names:
                self._cur().nonlocals.add(name)

        def visit_ClassDef(self, node: ClassDef) -> None:
            """Handle class definition nodes.

            Processes class definitions, creating a new class scope and
            detecting Enum classes which have special rules for member
            variable type annotations.

            Args:
                node: The ClassDef AST node being visited.
            """
            is_enum: bool = any(self._is_enum_base(b) for b in node.bases)
            if is_enum:
                self._enum_depth += 1
                # Track this class as an enum for future inheritance detection
                self._enum_classes.add(node.name)
            self._push("class")
            self.generic_visit(node)
            self._pop()
            if is_enum:
                self._enum_depth -= 1

        def visit_FunctionDef(self, node: FunctionDef) -> None:
            """Handle function definition nodes.

            Processes function definitions, creating a new function scope,
            checking for missing parameter and return type annotations,
            and handling special method parameters like 'self' and 'cls'.

            Args:
                node: The FunctionDef AST node being visited.
            """
            self._push("function")
            self._mark_param_annotated(node)
            args_all: List[arg] = (list(node.args.posonlyargs) +
                                   list(node.args.args) +
                                   list(node.args.kwonlyargs))
            a: arg
            for a in args_all:
                if a.annotation is None and not self._is_method_parameter(
                        a.arg, node):
                    self._record_issue(
                        node=a,
                        type_="untyped-argument",
                        name=a.arg,
                    )
            if node.returns is None:
                self._record_issue(
                    node=node,
                    type_="untyped-return",
                    name=node.name,
                )
            self.generic_visit(node)
            self._pop()

        def visit_AsyncFunctionDef(self, node: AsyncFunctionDef) -> None:
            """Handle async function definition nodes.

            Processes async function definitions similarly to regular
            functions, creating a new function scope and checking for
            missing parameter and return type annotations.

            Args:
                node: The AsyncFunctionDef AST node being visited.
            """
            self._push("function")
            self._mark_param_annotated(node)
            args_all_a: List[arg] = (list(node.args.posonlyargs) +
                                     list(node.args.args) +
                                     list(node.args.kwonlyargs))
            aa: arg
            for aa in args_all_a:
                if aa.annotation is None and not self._is_method_parameter(
                        aa.arg, node):
                    self._record_issue(
                        node=aa,
                        type_="untyped-argument",
                        name=aa.arg,
                    )
            if node.returns is None:
                self._record_issue(
                    node=node,
                    type_="untyped-return",
                    name=node.name,
                )
            self.generic_visit(node)
            self._pop()

        def visit_AnnAssign(self, node: AnnAssign) -> None:
            """Handle annotated assignment statements.

            Processes annotated assignments (var: Type = value) to mark
            the target variables as both defined and annotated in the
            appropriate scope.

            Args:
                node: The AnnAssign AST node being visited.
            """
            target_names: List[Name] = self._name_targets(node.target)
            n: Name
            for n in target_names:
                scope: Scope = self._resolve_def_scope(n.id)
                scope.defined.add(n.id)
                scope.annotated.add(n.id)
            self.generic_visit(node)

        def _define_if_first(self, name: str, node: AST) -> None:
            """Define a variable if it's the first occurrence in scope.

            Records a variable as defined if it hasn't been seen before
            in the current scope. Reports a type annotation issue if the
            variable lacks annotation and isn't filtered out by ignore rules.

            Args:
                name: The variable name being defined.
                node: The AST node where the definition occurs.
            """
            if self.ignore_underscore_vars and (name == "_" or name == "__"
                                                or name.startswith("_")):
                return
            if self._is_typing_import(name):
                return
            if self.in_for_loop and self.ignore_for_targets:
                return
            if self._is_type_alias(node):
                return
            scope: Scope = self._resolve_def_scope(name)
            if name in scope.defined:
                return
            if name not in scope.annotated:
                self._record_issue(
                    node=node,
                    type_="untyped-variable",
                    name=name,
                )
            scope.defined.add(name)

        def visit_Assign(self, node: Assign) -> None:
            """Handle regular assignment statements.

            Processes assignment statements to track variable definitions,
            handling multiple targets and type comments. Special handling
            for __all__ assignments and type alias detection.

            Args:
                node: The Assign AST node being visited.
            """
            t: AST
            attr_name: str = "parent_assign"
            for t in node.targets:
                names: List[Name] = self._name_targets(t)
                nm: Name
                for nm in names:
                    setattr(nm, attr_name, node)
                    if nm.id == "__all__":
                        scope: Scope = self._resolve_def_scope(nm.id)
                        scope.defined.add(nm.id)
                        scope.annotated.add(nm.id)
                        continue
                    self._define_if_first(nm.id, nm)
            # PEP 484: variable type comments
            type_cmt: Optional[str] = getattr(node, "type_comment", None)
            if type_cmt:
                for t in node.targets:
                    for nm in self._name_targets(t):
                        scope = self._resolve_def_scope(nm.id)
                        scope.defined.add(nm.id)
                        scope.annotated.add(nm.id)
            self.generic_visit(node)

        def visit_AugAssign(self, node: AugAssign) -> None:
            """Handle augmented assignment statements (+=, -=, etc.).

            Processes augmented assignments to track variable definitions
            for the target variables being modified.

            Args:
                node: The AugAssign AST node being visited.
            """
            names: List[Name] = self._name_targets(node.target)
            nm: Name
            for nm in names:
                self._define_if_first(nm.id, nm)
            self.generic_visit(node)

        def visit_NamedExpr(self, node: NamedExpr) -> None:
            """Handle named expressions (walrus operator :=).

            Processes named expressions to track variable definitions
            for the target variables being assigned.

            Args:
                node: The NamedExpr AST node being visited.
            """
            names: List[Name] = self._name_targets(node.target)
            nm: Name
            for nm in names:
                self._define_if_first(nm.id, nm)
            self.generic_visit(node)

        def visit_For(self, node: For) -> None:
            """Handle for loop statements.

            Processes for loops to track target variable definitions,
            with special handling when ignore_for_targets is enabled
            to skip reporting issues for loop variables.

            Args:
                node: The For AST node being visited.
            """
            old_in_for_loop: bool = self.in_for_loop
            self.in_for_loop = True
            names_f: List[Name] = self._name_targets(node.target)
            nm_f: Name
            for nm_f in names_f:
                self._define_if_first(nm_f.id, nm_f)
            self.in_for_loop = old_in_for_loop
            self.generic_visit(node)

        def visit_AsyncFor(self, node: AsyncFor) -> None:
            """Handle async for loop statements.

            Processes async for loops similarly to regular for loops,
            tracking target variable definitions with optional filtering.

            Args:
                node: The AsyncFor AST node being visited.
            """
            old_in_for_loop: bool = self.in_for_loop
            self.in_for_loop = True
            names_af: List[Name] = self._name_targets(node.target)
            nm_af: Name
            for nm_af in names_af:
                self._define_if_first(nm_af.id, nm_af)
            self.in_for_loop = old_in_for_loop
            self.generic_visit(node)

        def visit_With(self, node: With) -> None:
            """Handle with statement context managers.

            Processes with statements to track context manager target
            variables, with optional filtering when ignore_context_vars
            is enabled.

            Args:
                node: The With AST node being visited.
            """
            item: withitem
            for item in node.items:
                if item.optional_vars is None:
                    continue
                names_w: List[Name] = self._name_targets(item.optional_vars)
                nm_w: Name
                for nm_w in names_w:
                    if self.ignore_context_vars:
                        continue
                    self._define_if_first(nm_w.id, nm_w)
            self.generic_visit(node)

        def visit_AsyncWith(self, node: AsyncWith) -> None:
            """Handle async with statement context managers.

            Processes async with statements similarly to regular with
            statements, tracking context manager target variables.

            Args:
                node: The AsyncWith AST node being visited.
            """
            item_aw: withitem
            for item_aw in node.items:
                if item_aw.optional_vars is None:
                    continue
                names_aw: List[Name] = self._name_targets(
                    item_aw.optional_vars)
                nm_aw: Name
                for nm_aw in names_aw:
                    if self.ignore_context_vars:
                        continue
                    self._define_if_first(nm_aw.id, nm_aw)
            self.generic_visit(node)

        def visit_ExceptHandler(self, node: ExceptHandler) -> None:
            """Handle exception handler clauses.

            Processes except clauses to track exception variable definitions,
            with optional filtering when ignore_except_vars is enabled.

            Args:
                node: The ExceptHandler AST node being visited.
            """
            if node.name and not self.ignore_except_vars:
                nm_ex: str = node.name
                self._define_if_first(nm_ex, node)
            self.generic_visit(node)

        def _visit_comprehension(self, comps: List[comprehension]) -> None:
            """Handle comprehension generator expressions.

            Processes comprehension generators to track target variable
            definitions in a separate comprehension scope, with optional
            filtering when ignore_comprehensions is enabled.

            Args:
                comps: List of comprehension generator objects.
            """
            if self.ignore_comprehensions:
                return
            self._push("comp")
            comp: comprehension
            for comp in comps:
                names_c: List[Name] = self._name_targets(comp.target)
                nm_c: Name
                for nm_c in names_c:
                    self._define_if_first(nm_c.id, nm_c)
            self._pop()

        def visit_ListComp(self, node: ListComp) -> None:
            """Handle list comprehension expressions.

            Processes list comprehensions by delegating to the general
            comprehension handler for target variable tracking.

            Args:
                node: The ListComp AST node being visited.
            """
            self._visit_comprehension(node.generators)
            self.generic_visit(node)

        def visit_SetComp(self, node: SetComp) -> None:
            """Handle set comprehension expressions.

            Processes set comprehensions by delegating to the general
            comprehension handler for target variable tracking.

            Args:
                node: The SetComp AST node being visited.
            """
            self._visit_comprehension(node.generators)
            self.generic_visit(node)

        def visit_DictComp(self, node: DictComp) -> None:
            """Handle dictionary comprehension expressions.

            Processes dict comprehensions by delegating to the general
            comprehension handler for target variable tracking.

            Args:
                node: The DictComp AST node being visited.
            """
            self._visit_comprehension(node.generators)
            self.generic_visit(node)

        def visit_GeneratorExp(self, node: GeneratorExp) -> None:
            """Handle generator expression statements.

            Processes generator expressions by delegating to the general
            comprehension handler for target variable tracking.

            Args:
                node: The GeneratorExp AST node being visited.
            """
            self._visit_comprehension(node.generators)
            self.generic_visit(node)

    # -------------------- core analysis --------------------
    def _colorize(self, text: str, color: str, use_color: bool = True) -> str:
        """Apply ANSI color codes to text if color output is enabled.

        Args:
            text: The text string to colorize.
            color: The ANSI color code to apply.
            use_color: Whether to actually apply colors or return plain text.

        Returns:
            str: Colorized text with reset code appended, or plain text.
        """
        return f"{color}{text}{Colors.RESET.value}" if use_color else text

    def analyze_file(
        self,
        path: Path,
        *,
        context_lines: int,
        ignore_underscore_vars: bool = True,
        ignore_comprehensions: bool = True,
        ignore_except_vars: bool = True,
        ignore_for_targets: bool = True,
        ignore_context_vars: bool = True,
    ) -> Tuple[List[Issue], Optional[str]]:
        """Analyze a single Python file for missing type annotations.

        Reads the file content and delegates to analyze_source for the
        actual analysis work. Handles file reading errors gracefully.

        Args:
            path: Path to the Python file to analyze.
            context_lines: Number of context lines to include with issues.
            ignore_underscore_vars: Skip variables starting with underscore.
            ignore_comprehensions: Skip variables in comprehensions.
            ignore_except_vars: Skip exception handler variables.
            ignore_for_targets: Skip for loop target variables.
            ignore_context_vars: Skip context manager variables.

        Returns:
            Tuple containing list of issues and optional error message.
        """
        self.context_lines = context_lines
        text: str
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as exc:
            return ([], f"Failed to read {path}: {exc}")
        return self.analyze_source(
            name=str(path),
            text=text,
            context_lines=context_lines,
            ignore_underscore_vars=ignore_underscore_vars,
            ignore_comprehensions=ignore_comprehensions,
            ignore_except_vars=ignore_except_vars,
            ignore_for_targets=ignore_for_targets,
            ignore_context_vars=ignore_context_vars,
        )

    def analyze_source(
        self,
        *,
        name: str,
        text: str,
        context_lines: int,
        ignore_underscore_vars: bool = True,
        ignore_comprehensions: bool = True,
        ignore_except_vars: bool = True,
        ignore_for_targets: bool = True,
        ignore_context_vars: bool = True,
    ) -> Tuple[List[Issue], Optional[str]]:
        """Analyze an in-memory Python source string.

        Parses the source code into an AST and uses the UntypedVisitor
        to find missing type annotations. Handles syntax errors.

        Args:
            name: A pseudo-name for the source (e.g., filename).
            text: The Python source code as a string.
            context_lines: Number of context lines to include with issues.
            ignore_underscore_vars: Skip variables starting with underscore.
            ignore_comprehensions: Skip variables in comprehensions.
            ignore_except_vars: Skip exception handler variables.
            ignore_for_targets: Skip for loop target variables.
            ignore_context_vars: Skip context manager variables.

        Returns:
            Tuple containing list of issues and optional error message.
        """
        self.context_lines = context_lines
        # Dedent and strip the source before parsing
        processed_text: str = dedent(text)
        try:
            tree: AST = parse(processed_text, type_comments=True)
        except SyntaxError as syn:
            return (
                [],
                (f"Syntax error in {name}: line {syn.lineno} col {syn.offset}"
                 ),
            )
        visitor: TypeCoverage.UntypedVisitor = TypeCoverage.UntypedVisitor(
            source=processed_text,
            file=Path(name),
            context_lines=context_lines,
            ignore_underscore_vars=ignore_underscore_vars,
            ignore_comprehensions=ignore_comprehensions,
            ignore_except_vars=ignore_except_vars,
            ignore_for_targets=ignore_for_targets,
            ignore_context_vars=ignore_context_vars,
        )
        visitor.visit(tree)
        return (visitor.issues, None)

    def analyze_object(
        self,
        obj: Union[
            CodeType,
            FrameType,
            FunctionType,
            Type[Any],
            type,
            ModuleType,
            Callable,
        ],
        *,
        context_lines: int,
        name_hint: Optional[str] = None,
        ignore_underscore_vars: bool = True,
        ignore_comprehensions: bool = True,
        ignore_except_vars: bool = True,
        ignore_for_targets: bool = True,
        ignore_context_vars: bool = True,
    ) -> Tuple[List[Issue], Optional[str]]:
        """Analyze a live Python object by extracting its source.

        Retrieves source code for functions, classes, modules, or code objects
        and then analyzes the source using analyze_source. Handles cases where
        source code is not available (e.g., built-ins, compiled extensions).

        Args:
            obj: The Python object to analyze.
            context_lines: Number of context lines to include with issues.
            name_hint: An optional name hint for reporting.
            ignore_underscore_vars: Skip variables starting with underscore.
            ignore_comprehensions: Skip variables in comprehensions.
            ignore_except_vars: Skip exception handler variables.
            ignore_for_targets: Skip for loop target variables.
            ignore_context_vars: Skip context manager variables.

        Returns:
            Tuple containing list of issues and optional error message.
        """
        src: Optional[str] = None
        name: str = name_hint or getattr(obj, "__name__", "<object>")
        if (hasattr(obj, "__module__")
                and getattr(obj, "__module__", None) == "builtins"):
            return (
                [],
                f"Skipping built-in object {name} (no source available).",
            )
        if hasattr(obj, "__file__") and getattr(obj, "__file__", "").endswith(
            (".so", ".pyd", ".dll")):
            return (
                [],
                f"Skipping compiled extension {name} (no source available).",
            )
        try:
            src = getsource(obj)
            if src:
                src = src.strip()
                if not src:
                    src = None
                else:
                    try:
                        parse(src, type_comments=True)
                    except SyntaxError:
                        try:
                            dedented: str = dedent(src)
                            parse(dedented, type_comments=True)
                            src = dedented
                        except SyntaxError:
                            src = None
        except (OSError, TypeError, AttributeError):
            if isinstance(obj, FrameType):
                try:
                    code: CodeType = obj.f_code
                    filename: str = code.co_filename
                    start: int = getattr(obj, "f_lineno", 1)
                    buf: List[str] = []
                    i: int
                    for i in range(max(1, start - 10), start + 10):
                        line: Optional[str] = getline(filename, i)
                        if not line or line.strip() == "":
                            continue
                        buf.append(line)
                    if buf:
                        src = dedent("".join(buf))
                        name = f"{filename}:around:{start}"
                        try:
                            parse(src, type_comments=True)
                        except SyntaxError:
                            src = None
                except Exception:
                    src = None
            else:
                src = None
        if src is None:
            return ([], f"Skipping {name} (source not available or invalid).")
        return self.analyze_source(
            name=name,
            text=src,
            context_lines=context_lines,
            ignore_underscore_vars=ignore_underscore_vars,
            ignore_comprehensions=ignore_comprehensions,
            ignore_except_vars=ignore_except_vars,
            ignore_for_targets=ignore_for_targets,
            ignore_context_vars=ignore_context_vars,
        )

    # -------------------- path collection --------------------
    def _string_looks_like_glob(self, s: str) -> bool:
        """Check if a string contains glob pattern metacharacters.

        Args:
            s: The string to check for glob patterns.

        Returns:
            bool: True if string contains *, ?, or [] characters.
        """
        has_meta: bool = any(ch in s for ch in "*?[]")
        return has_meta

    def _collect_paths_from_str(
        self,
        s: str,
        *,
        recursive: bool,
        extensions: Sequence[str],
    ) -> List[Path]:
        """Resolve a string into a list of Python files to analyze.

        Handles glob patterns, file paths, and directory paths, expanding
        them into concrete file paths for analysis. Supports recursive
        directory traversal when requested.

        Args:
            s: String that may be a file path, directory, or glob pattern.
            recursive: Whether to recurse into subdirectories.
            extensions: Allowed file extensions to include.

        Returns:
            List[Path]: List of file paths to analyze.
        """
        paths: List[Path] = []
        p: Path = Path(s)
        if self._string_looks_like_glob(s):
            matches: List[str] = glob(s, recursive=recursive)
            m: str
            for m in matches:
                mp: Path = Path(m)
                if mp.is_file():
                    paths.append(mp)
            return self._filter_by_extension(paths, extensions)
        if p.exists():
            if p.is_file():
                return self._filter_by_extension([p], extensions)
            if p.is_dir():
                if recursive:
                    allp: List[Path] = [
                        pp for pp in p.rglob("*") if pp.is_file()
                    ]
                else:
                    allp = [pp for pp in p.iterdir() if pp.is_file()]
                return self._filter_by_extension(allp, extensions)
        return []

    def _filter_by_extension(self, paths: Sequence[Path],
                             exts: Sequence[str]) -> List[Path]:
        """Filter file paths by allowed extensions (case-insensitive).

        Args:
            paths: Sequence of file paths to filter.
            exts: Sequence of allowed file extensions (e.g., ['.py']).

        Returns:
            List[Path]: Filtered list of paths with matching extensions.
        """
        allowed: Set[str] = {e.lower() for e in exts}
        out: List[Path] = []
        pth: Path
        for pth in paths:
            if pth.suffix.lower() in allowed:
                out.append(pth)
        return out

    # -------------------- reporting --------------------
    def compute_stats(self, issues: Sequence[Issue]) -> Stats:
        """Compute statistics from a sequence of type annotation issues.

        Counts issues by type and calculates total count for summary
        reporting and exit code determination.

        Args:
            issues: Sequence of Issue objects to analyze.

        Returns:
            Stats: Object containing total count and per-type counts.
        """
        counts: Dict[IssueType, int] = {
            "untyped-argument": 0,
            "untyped-return": 0,
            "untyped-variable": 0,
        }
        it: Issue
        for it in issues:
            counts[it.type] += 1
        total: int = sum(counts.values())
        stats: Stats = Stats(total=total, by_type=counts)
        return stats

    def _format_issue_location(self,
                               issue: Issue,
                               use_color: bool = True) -> str:
        """Format an issue's file location with optional colors.

        Args:
            issue: The Issue object containing location information.
            use_color: Whether to apply ANSI color codes.

        Returns:
            str: Formatted location string (file:line:column).
        """
        file_str: str = self._colorize(str(issue.file), Colors.CYAN.value,
                                       use_color)
        line_str: str = self._colorize(str(issue.line), Colors.YELLOW.value,
                                       use_color)
        col_str: str = self._colorize(str(issue.column + 1),
                                      Colors.YELLOW.value, use_color)
        return f"{file_str}:{line_str}:{col_str}"

    def _format_issue_type(self,
                           issue_type: IssueType,
                           use_color: bool = True) -> str:
        """Format an issue type description with optional colors.

        Args:
            issue_type: The type of issue to format.
            use_color: Whether to apply ANSI color codes.

        Returns:
            str: Formatted and colorized issue type description.
        """
        type_colors: Dict[IssueType, str] = {
            "untyped-argument": Colors.BRIGHT_RED.value,
            "untyped-return": Colors.BRIGHT_YELLOW.value,
            "untyped-variable": Colors.BRIGHT_BLUE.value,
        }
        type_names: Dict[IssueType, str] = {
            "untyped-argument": "Missing type annotation for argument",
            "untyped-return": "Missing return type annotation",
            "untyped-variable": "Missing type annotation for variable",
        }
        color: str = type_colors.get(issue_type, Colors.WHITE.value)
        name: str = type_names.get(issue_type, issue_type)
        return self._colorize(name, color, use_color)

    def _format_context_lines(self,
                              issue: Issue,
                              use_color: bool = True) -> List[str]:
        """Format context lines around an issue with optional colors.

        Creates a formatted display of source code lines around the
        issue location, highlighting the specific line where the issue
        occurs and showing line numbers.

        Args:
            issue: The Issue object containing context information.
            use_color: Whether to apply ANSI color codes.

        Returns:
            List[str]: Formatted context lines with line numbers.
        """
        if not issue.context:
            return []
        lines: List[str] = []
        start_line: int = max(1, issue.line - self.context_lines)
        for i, line in enumerate(issue.context):
            line_num: int = start_line + i
            line_num_str: str = f"{line_num:4d}"
            is_issue_line: bool = line_num == issue.line
            if is_issue_line:
                prefix: str = self._colorize(Emoji.ARROW_RIGHT.value,
                                             Colors.BRIGHT_RED.value,
                                             use_color)
                line_num_colored: str = self._colorize(
                    line_num_str, Colors.BRIGHT_YELLOW.value, use_color)
                line_content: str = self._colorize(line.rstrip(),
                                                   Colors.WHITE.value,
                                                   use_color)
                lines.append(
                    indent(
                        f"{prefix} {line_num_colored} │ {line_content}",
                        Indentation.LEVEL_1,
                    ))
            else:
                prefix = " "
                line_num_colored = self._colorize(line_num_str,
                                                  Colors.GRAY.value, use_color)
                line_content = self._colorize(line.rstrip(), Colors.GRAY.value,
                                              use_color)
                lines.append(
                    indent(
                        f"{prefix} {line_num_colored} │ {line_content}",
                        Indentation.LEVEL_1,
                    ))
        return lines

    def render_text(
        self,
        *,
        issues: Sequence[Issue],
        stats: Optional[Stats],
        use_color: bool = True,
    ) -> str:
        """Render type annotation issues as human-readable text.

        Creates a comprehensive text report with file grouping, issue
        details, source code context, and optional statistics summary.
        Supports ANSI color formatting for enhanced readability.

        Args:
            issues: Sequence of Issue objects to render.
            stats: Optional statistics object for summary section.
            use_color: Whether to apply ANSI color codes.

        Returns:
            str: Formatted text report of all issues and statistics.
        """
        if not issues and (not stats or stats.total == 0):
            return self._colorize(
                f"{Emoji.CHECK_MARK.value} No type annotation issues found",
                Colors.BRIGHT_GREEN.value,
                use_color,
            )
        out_lines: List[str] = []
        files_to_issues: Dict[Path, List[Issue]] = {}
        for issue in issues:
            files_to_issues.setdefault(issue.file, []).append(issue)
        if issues:
            header: str = (f"Found {len(issues)} type annotation issue"
                           f"{'s' if len(issues) != 1 else ''}")
            out_lines.append(
                self._colorize(header, Colors.BOLD.value + Colors.WHITE.value,
                               use_color))
            out_lines.append("")
        for file_path, file_issues in sorted(files_to_issues.items()):
            file_header: str = f"{Emoji.FOLDER.value} {file_path}"
            out_lines.append(
                self._colorize(
                    file_header,
                    Colors.BOLD.value + Colors.CYAN.value,
                    use_color,
                ))
            for issue in sorted(file_issues, key=lambda x: x.line):
                location: str = self._format_issue_location(issue, use_color)
                issue_type: str = self._format_issue_type(
                    issue.type, use_color)
                name: str = self._colorize(f'"{issue.name}"',
                                           Colors.BRIGHT_WHITE.value,
                                           use_color)
                out_lines.append(
                    indent(
                        f"{location} - {issue_type} {name}",
                        Indentation.LEVEL_1,
                    ))
                context_lines: List[str] = self._format_context_lines(
                    issue, use_color)
                out_lines.extend(context_lines)
                if context_lines:
                    out_lines.append("")
            out_lines.append("")
        if stats is not None:
            out_lines.append(
                self._colorize(
                    f"{Emoji.CHART.value} Summary",
                    Colors.BOLD.value + Colors.WHITE.value,
                    use_color,
                ))
            if stats.total == 0:
                out_lines.append(
                    indent(
                        self._colorize(
                            f"{Emoji.CHECK_MARK.value} No issues found",
                            Colors.BRIGHT_GREEN.value,
                            use_color,
                        ),
                        Indentation.LEVEL_1,
                    ))
                out_lines.append("")
                out_lines.append(
                    indent(
                        self._colorize(
                            f"{Emoji.BULB.value} Tip: Issues can be "
                            f"suppressed using:",
                            Colors.DIM.value,
                            use_color,
                        ),
                        Indentation.LEVEL_1,
                    ))
                out_lines.append(
                    indent(
                        self._colorize("# type: ignore", Colors.DIM.value,
                                       use_color),
                        Indentation.LEVEL_2,
                    ))
                out_lines.append(
                    indent(
                        self._colorize(
                            "# type: ignore[reportMissingParameterType]",
                            Colors.DIM.value,
                            use_color,
                        ),
                        Indentation.LEVEL_2,
                    ))
                out_lines.append(
                    indent(
                        self._colorize("# noqa: ANN001", Colors.DIM.value,
                                       use_color),
                        Indentation.LEVEL_2,
                    ))
            else:
                total_color: str = (Colors.BRIGHT_RED.value if stats.total > 10
                                    else Colors.BRIGHT_YELLOW.value if
                                    stats.total > 5 else Colors.YELLOW.value)
                total_str: str = self._colorize(f"Total issues: {stats.total}",
                                                total_color, use_color)
                out_lines.append(indent(total_str, Indentation.LEVEL_1))
                type_info: List[Tuple[IssueType, str, str]] = [
                    (
                        "untyped-argument",
                        f"{Emoji.RED_CIRCLE.value} Missing argument types",
                        Colors.BRIGHT_RED.value,
                    ),
                    (
                        "untyped-return",
                        f"{Emoji.YELLOW_CIRCLE.value} Missing return types",
                        Colors.BRIGHT_YELLOW.value,
                    ),
                    (
                        "untyped-variable",
                        f"{Emoji.BLUE_CIRCLE.value} Missing variable types",
                        Colors.BRIGHT_BLUE.value,
                    ),
                ]
                for issue_type, label, color in type_info:
                    count: int = stats.by_type.get(issue_type, 0)
                    if count > 0:
                        count_str: str = self._colorize(
                            f"{label}: {count}", color, use_color)
                        out_lines.append(indent(count_str,
                                                Indentation.LEVEL_1))
                out_lines.append("")
                out_lines.append(
                    indent(
                        self._colorize(
                            f"{Emoji.BULB.value} Tip: Suppress issues using "
                            f"comments:",
                            Colors.DIM.value,
                            use_color,
                        ),
                        Indentation.LEVEL_1,
                    ))
                out_lines.append(
                    indent(
                        self._colorize(
                            "# type: ignore  (suppress all)",
                            Colors.DIM.value,
                            use_color,
                        ),
                        Indentation.LEVEL_2,
                    ))
                out_lines.append(
                    indent(
                        self._colorize(
                            "# noqa: ANN001  (suppress specific codes)",
                            Colors.DIM.value,
                            use_color,
                        ),
                        Indentation.LEVEL_2,
                    ))
        return "\n".join(out_lines)

    def render_json(
        self,
        *,
        issues: Sequence[Issue],
        stats: Optional[Stats],
    ) -> str:
        """Render type annotation issues as machine-readable JSON.

        Creates a structured JSON representation of issues and statistics
        suitable for programmatic processing or integration with other
        tools and workflows.

        Args:
            issues: Sequence of Issue objects to render.
            stats: Optional statistics object for summary data.

        Returns:
            str: JSON-formatted string containing issues and statistics.
        """
        serial_issues: List[Mapping[str, Any]] = []
        it: Issue
        for it in issues:
            entry: Dict[str, Any] = {
                "file": str(it.file),
                "line": it.line,
                "column": it.column,
                "type": it.type,
                "name": it.name,
                "context": list(it.context),
            }
            serial_issues.append(entry)
        by_file: Dict[str, int] = {}
        for it in issues:
            k: str = str(it.file)
            by_file[k] = by_file.get(k, 0) + 1
        payload: Dict[str, Any] = {
            "version": VERSION,
            "issues": serial_issues,
            "by_file": by_file,
        }
        if stats is not None:
            payload["statistics"] = {
                "total": stats.total,
                "untyped-argument": stats.by_type.get("untyped-argument", 0),
                "untyped-return": stats.by_type.get("untyped-return", 0),
                "untyped-variable": stats.by_type.get("untyped-variable", 0),
            }
        json_text: str = dumps(payload, indent=2, ensure_ascii=False)
        return json_text

    # -------------------- orchestration --------------------
    def _analyze_files_parallel(
        self,
        paths: Sequence[Path],
        *,
        context_lines: int,
        ignore_underscore_vars: bool,
        ignore_comprehensions: bool,
        ignore_except_vars: bool,
        ignore_for_targets: bool,
        ignore_context_vars: bool,
    ) -> Tuple[List[Issue], List[str]]:
        """Analyze many files using a thread pool (IO-bound).

        Distributes file analysis tasks across a thread pool to efficiently
        process multiple files concurrently. Collects issues and errors.

        Args:
            paths: Sequence of file paths to analyze.
            context_lines: Number of context lines for issues.
            ignore_underscore_vars: Skip underscore variables.
            ignore_comprehensions: Skip comprehension variables.
            ignore_except_vars: Skip exception variables.
            ignore_for_targets: Skip for loop target variables.
            ignore_context_vars: Skip context manager variables.

        Returns:
            Tuple of (list of issues, list of error messages).
        """
        issues_out: List[Issue] = []
        errors_out: List[str] = []
        max_workers: int = max(2, int(cpu_count() or 8))
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futs: Dict[Any, Path] = {
                ex.submit(
                    self.analyze_file,
                    pth,
                    context_lines=context_lines,
                    ignore_underscore_vars=ignore_underscore_vars,
                    ignore_comprehensions=ignore_comprehensions,
                    ignore_except_vars=ignore_except_vars,
                    ignore_for_targets=ignore_for_targets,
                    ignore_context_vars=ignore_context_vars,
                ):
                pth
                for pth in paths
            }
            for fut in as_completed(futs):
                try:
                    issues_f: List[Issue]
                    err_f: Optional[str]
                    issues_f, err_f = fut.result()
                except Exception as exc:  # pragma: no cover
                    errors_out.append(f"Failed analyzing file: {exc}")
                    continue
                if err_f is not None:
                    errors_out.append(err_f)
                else:
                    issues_out.extend(issues_f)
        return (issues_out, errors_out)

    def analyze_targets(
        self,
        *targets: TargetLike,
        context_lines: int = 0,
        recursive: bool = True,
        extensions: Sequence[str] = (".py", ),
        exclude: Sequence[str] = (),
        ignore_underscore_vars: bool = True,
        ignore_comprehensions: bool = True,
        ignore_except_vars: bool = True,
        ignore_for_targets: bool = True,
        ignore_context_vars: bool = True,
    ) -> Tuple[List[Issue], List[str]]:
        """Analyze any mix of supported targets and return issues and errors.

        Supports analyzing files, directories, globs, code strings, and
        live Python objects. Handles exclusions and parallel processing.

        Args:
            *targets: Variable number of targets to analyze.
            context_lines: Number of context lines for issues.
            recursive: Whether to search directories recursively.
            extensions: File extensions to include.
            exclude: Substrings to exclude from file paths.
            ignore_underscore_vars: Skip underscore variables.
            ignore_comprehensions: Skip comprehension variables.
            ignore_except_vars: Skip exception variables.
            ignore_for_targets: Skip for loop target variables.
            ignore_context_vars: Skip context manager variables.

        Returns:
            Tuple of (list of issues, list of error messages).
        """
        all_issues: List[Issue] = []
        errors: List[str] = []
        tgt: TargetLike
        for tgt in targets:
            if isinstance(tgt, str):
                s: str = tgt
                candidate_paths: List[Path] = self._collect_paths_from_str(
                    s, recursive=recursive, extensions=extensions)
                if candidate_paths:
                    paths: List[Path] = [
                        p for p in candidate_paths
                        if not any(x in str(p) for x in exclude)
                    ]
                    issues_f: List[Issue]
                    errs_f: List[str]
                    issues_f, errs_f = self._analyze_files_parallel(
                        paths,
                        context_lines=context_lines,
                        ignore_underscore_vars=ignore_underscore_vars,
                        ignore_comprehensions=ignore_comprehensions,
                        ignore_except_vars=ignore_except_vars,
                        ignore_for_targets=ignore_for_targets,
                        ignore_context_vars=ignore_context_vars,
                    )
                    all_issues.extend(issues_f)
                    errors.extend(errs_f)
                else:
                    issues_s: List[Issue]
                    err_s: Optional[str]
                    issues_s, err_s = self.analyze_source(
                        name="<string>",
                        text=s,
                        context_lines=context_lines,
                        ignore_underscore_vars=ignore_underscore_vars,
                        ignore_comprehensions=ignore_comprehensions,
                        ignore_except_vars=ignore_except_vars,
                        ignore_for_targets=ignore_for_targets,
                        ignore_context_vars=ignore_context_vars,
                    )
                    if err_s is not None:
                        errors.append(err_s)
                    else:
                        all_issues.extend(issues_s)
                continue
            if isinstance(tgt, Path):
                p2: Path = tgt
                if p2.is_file():
                    paths: List[Path] = [p2]
                elif p2.is_dir():
                    if recursive:
                        paths = [pp for pp in p2.rglob("*") if pp.is_file()]
                    else:
                        paths = [pp for pp in p2.iterdir() if pp.is_file()]
                else:
                    paths = []
                paths = [
                    pth
                    for pth in self._filter_by_extension(paths, extensions)
                    if not any(x in str(pth) for x in exclude)
                ]
                issues_p: List[Issue]
                errs_p: List[str]
                issues_p, errs_p = self._analyze_files_parallel(
                    paths,
                    context_lines=context_lines,
                    ignore_underscore_vars=ignore_underscore_vars,
                    ignore_comprehensions=ignore_comprehensions,
                    ignore_except_vars=ignore_except_vars,
                    ignore_for_targets=ignore_for_targets,
                    ignore_context_vars=ignore_context_vars,
                )
                all_issues.extend(issues_p)
                errors.extend(errs_p)
                continue
            if isinstance(tgt, (CodeType, FrameType, FunctionType, type,
                                ModuleType)) or (callable(tgt)
                                                 and hasattr(tgt, "__code__")):
                obj: Union[
                    CodeType,
                    FrameType,
                    FunctionType,
                    Type[Any],
                    type,
                    ModuleType,
                    Callable,
                ] = (tgt.__func__ if isinstance(tgt, (classmethod,
                                                      staticmethod)) else tgt)
                issues_o: List[Issue]
                err_o: Optional[str]
                issues_o, err_o = self.analyze_object(
                    obj,
                    context_lines=context_lines,
                    ignore_underscore_vars=ignore_underscore_vars,
                    ignore_comprehensions=ignore_comprehensions,
                    ignore_except_vars=ignore_except_vars,
                    ignore_for_targets=ignore_for_targets,
                    ignore_context_vars=ignore_context_vars,
                )
                if err_o is not None:
                    errors.append(err_o)
                else:
                    all_issues.extend(issues_o)
            else:
                errors.append(f"Unsupported target type: {type(tgt)!r}")
        return (all_issues, errors)

    def detect_untyped(
        self,
        *targets: TargetLike,
        context_lines: int = 0,
        format: Literal["text", "json"] = "text",
        statistics: bool = False,
        recursive: bool = True,
        extensions: Sequence[str] = (".py", ),
        exclude: Sequence[str] = (),
        force_color: bool = False,
        ignore_underscore_vars: bool = True,
        ignore_comprehensions: bool = True,
        ignore_except_vars: bool = True,
        ignore_for_targets: bool = True,
        ignore_context_vars: bool = True,
    ) -> str:
        """Analyze targets and return a formatted report.

        Orchestrates the analysis process, calling analyze_targets and then
        rendering the results in the specified format (text or JSON), with
        optional statistics and colorization. Also handles error reporting.

        Args:
            *targets: Variable number of targets to analyze.
            context_lines: Number of context lines for issues.
            format: Output format ('text' or 'json').
            statistics: Whether to include statistics in the report.
            recursive: Whether to search directories recursively.
            extensions: File extensions to include.
            exclude: Substrings to exclude from file paths.
            force_color: Force ANSI color output.
            ignore_underscore_vars: Skip variables starting with underscore.
            ignore_comprehensions: Skip variables in comprehensions.
            ignore_except_vars: Skip exception handler variables.
            ignore_for_targets: Skip for loop target variables.
            ignore_context_vars: Skip context manager variables.

        Returns:
            str: Formatted analysis report.
        """
        issues: List[Issue]
        errors: List[str]
        issues, errors = self.analyze_targets(
            *targets,
            context_lines=context_lines,
            recursive=recursive,
            extensions=extensions,
            exclude=exclude,
            ignore_underscore_vars=ignore_underscore_vars,
            ignore_comprehensions=ignore_comprehensions,
            ignore_except_vars=ignore_except_vars,
            ignore_for_targets=ignore_for_targets,
            ignore_context_vars=ignore_context_vars,
        )
        stats: Optional[Stats] = (self.compute_stats(issues)
                                  if statistics else None)
        use_color: bool = force_color or Colors.supports_color()
        body: str
        if format == "json":
            body = self.render_json(issues=issues, stats=stats)
        else:
            body = self.render_text(issues=issues,
                                    stats=stats,
                                    use_color=use_color)
            if errors:
                err: str
                error_header: str = self._colorize(
                    f"{Emoji.CROSS_MARK.value} Errors:",
                    Colors.BOLD.value + Colors.BRIGHT_RED.value,
                    use_color,
                )
                buf: List[str] = ([body, "", error_header]
                                  if body else [error_header])
                for err in errors:
                    error_line: str = indent(
                        self._colorize(f"• {err}", Colors.RED.value,
                                       use_color),
                        Indentation.LEVEL_1,
                    )
                    buf.append(error_line)
                body = "\n".join(buf)
        return body

    # -------------------- CLI --------------------
    def _create_parser(self) -> ArgumentParser:
        """Create the command-line argument parser.

        Builds an ArgumentParser with all supported command-line options
        for the typecoverage tool, including analysis options, output
        formatting, and filtering controls.

        Returns:
            ArgumentParser: Configured argument parser for the CLI.
        """
        parser: ArgumentParser
        parser = ArgumentParser(
            prog="typecoverage",
            description=(
                "Report untyped variables, arguments, and function returns."),
        )
        parser.add_argument(
            "targets",
            nargs="*",
            help=("Targets: paths, globs, or code strings (if not resolving "
                  "to a file)."),
        )
        parser.add_argument(
            "--recursive",
            action="store_true",
            help="Recurse into subdirectories when given directories.",
        )
        parser.add_argument(
            "--extensions",
            type=str,
            default=".py",
            metavar="EXTS",
            help="Comma-separated list of file extensions to include.",
        )
        parser.add_argument(
            "--exclude",
            type=str,
            default="",
            metavar="SUBS",
            help="Comma-separated substrings to skip (in file paths).",
        )
        parser.add_argument(
            "--context-lines",
            type=int,
            default=0,
            help="Number of source lines to show as context.",
        )
        parser.add_argument(
            "--format",
            choices=["text", "json"],
            default="text",
            help="Output format.",
        )
        parser.add_argument(
            "--statistics",
            action="store_true",
            help="Print a summary of issue counts.",
        )
        parser.add_argument(
            "--output",
            type=str,
            default="",
            metavar="FILE",
            help="Write output to FILE instead of stdout.",
        )
        parser.add_argument(
            "--exit-nonzero-on-issues",
            action="store_true",
            help="Exit with code 1 if any issues are found.",
        )
        parser.add_argument(
            "--fail-under",
            type=int,
            default=0,
            metavar="N",
            help="Exit non-zero if total issues >= N.",
        )
        parser.add_argument(
            "--version",
            action="store_true",
            help="Print version and exit.",
        )
        parser.add_argument(
            "--demo",
            action="store_true",
            help="Run code-string, function, frame, and glob demos.",
        )
        parser.add_argument(
            "--force-color",
            action="store_true",
            help="Force ANSI color output even if output is redirected.",
        )
        parser.add_argument(
            "--ignore-underscore-vars",
            action="store_true",
            default=True,
            help="Ignore variables with underscore names (default: True).",
        )
        parser.add_argument(
            "--no-ignore-underscore-vars",
            dest="ignore_underscore_vars",
            action="store_false",
            help="Don't ignore variables with underscore names.",
        )
        parser.add_argument(
            "--ignore-comprehensions",
            action="store_true",
            default=True,
            help="Ignore variables used in comprehensions (default: True).",
        )
        parser.add_argument(
            "--ignore-except-vars",
            action="store_true",
            default=True,
            help=("Ignore exception variables in except blocks"
                  "(default: True)."),
        )
        parser.add_argument(
            "--no-ignore-except-vars",
            dest="ignore_except_vars",
            action="store_false",
            help="Don't ignore exception variables in except blocks.",
        )
        parser.add_argument(
            "--ignore-for-targets",
            action="store_true",
            default=True,
            help="Ignore loop variables introduced in for/async for "
            "(default: True).",
        )
        parser.add_argument(
            "--no-ignore-for-targets",
            dest="ignore_for_targets",
            action="store_false",
            help="Do not ignore for/async for target variables.",
        )
        parser.add_argument(
            "--ignore-context-vars",
            action="store_true",
            default=True,
            help="Ignore context manager variables (default: True).",
        )
        parser.add_argument(
            "--no-ignore-context-vars",
            dest="ignore_context_vars",
            action="store_false",
            help="Do not ignore context manager variables.",
        )
        return parser

    def parse_args(self, argv: Optional[Sequence[str]] = None) -> Namespace:
        """Parse command-line arguments with pyproject.toml support.

        Parses command-line arguments and applies any default values
        found in the [tool.typecoverage] section of pyproject.toml in the
        current working directory.

        Args:
            argv: Optional argument list (uses sys.argv if None).

        Returns:
            Namespace: Parsed arguments with defaults applied.
        """
        parser: ArgumentParser = self._create_parser()
        cfg: Dict[str, Any] = self._load_pyproject()
        if cfg:
            parser.set_defaults(**cfg)
        args: Namespace = parser.parse_args(list(argv) if argv else None)
        return args

    def _split_csv(self, csv: str) -> List[str]:
        """Split a comma-separated string into a cleaned list.

        Args:
            csv: Comma-separated string to split.

        Returns:
            List[str]: List of trimmed, non-empty strings.
        """
        return [p for p in [p.strip() for p in csv.split(",")] if p]

    def parse_and_run(self, argv: Optional[Sequence[str]] = None) -> int:
        """Main CLI entry point that parses args and runs analysis.

        Complete CLI workflow: parses command-line arguments, performs
        analysis on specified targets, formats output, and returns
        appropriate exit code based on findings and failure thresholds.

        Args:
            argv: Optional argument list (uses sys.argv if None).

        Returns:
            int: Exit code (0 for success, 1 for issues found, 2 for errors).
        """
        # Windows console fix for ANSI when possible
        if platform == "win32":  # pragma: no cover (platform)
            with suppress(Exception):
                from colorama import just_fix_windows_console

                just_fix_windows_console()
        args: Namespace = self.parse_args(argv)
        if args.version:
            print(f"typecoverage version {VERSION}")
            return 0
        # Show help if no explicit targets and not in demo mode
        if not args.demo and not args.targets:
            self._create_parser().print_help()
            return 2
        if args.demo:
            code_str: str = ("def foo(x, y: int):\n"
                             "    z = x + y\n"
                             "    return z\n")
            frame: FrameType = stack()[0].frame
            this_file: Path = Path(__file__)
            glob_pat: str = str(this_file.parent / "*.py")
            report: str = self.detect_untyped(
                code_str,
                demo_func,
                DemoClass,
                frame,
                glob_pat,
                this_file,
                context_lines=1,
                statistics=True,
                force_color=bool(args.force_color),
                ignore_underscore_vars=True,
                ignore_comprehensions=True,
                ignore_except_vars=True,
                ignore_for_targets=True,
                ignore_context_vars=True,
            )
            print(report)
            return 0
        exts: List[str] = self._split_csv(args.extensions) or [".py"]
        excl: List[str] = self._split_csv(args.exclude)
        targets: List[str] = list(args.targets)
        # Perform analysis (so we have exact counts for exit behavior)
        issues: List[Issue]
        errors: List[str]
        issues, errors = self.analyze_targets(
            *targets,
            context_lines=int(args.context_lines),
            recursive=bool(args.recursive),
            extensions=exts,
            exclude=excl,
            ignore_underscore_vars=bool(args.ignore_underscore_vars),
            ignore_comprehensions=bool(args.ignore_comprehensions),
            ignore_except_vars=bool(args.ignore_except_vars),
            ignore_for_targets=bool(args.ignore_for_targets),
            ignore_context_vars=bool(args.ignore_context_vars),
        )
        stats: Optional[Stats] = (self.compute_stats(issues)
                                  if bool(args.statistics) else None)
        use_color: bool = bool(args.force_color) or Colors.supports_color()
        report_text: str
        if args.format == "json":
            report_text = self.render_json(issues=issues, stats=stats)
        else:
            report_text = self.render_text(issues=issues,
                                           stats=stats,
                                           use_color=use_color)
            if errors:
                error_header: str = self._colorize(
                    f"{Emoji.CROSS_MARK.value} Errors:",
                    Colors.BOLD.value + Colors.BRIGHT_RED.value,
                    use_color,
                )
                buf: List[str] = ([report_text, "", error_header]
                                  if report_text else [error_header])
                for err in errors:
                    error_line: str = indent(
                        self._colorize(f"• {err}", Colors.RED.value,
                                       use_color),
                        Indentation.LEVEL_1,
                    )
                    buf.append(error_line)
                report_text = "\n".join(buf)
        if args.output:
            out_path: Path = Path(args.output)
            try:
                out_path.write_text(report_text, encoding="utf-8")
            except Exception as exc:
                print(f"Failed to write output: {exc}")
                return 2
        else:
            print(report_text)
        total_issues: int = len(issues)
        if args.exit_nonzero_on_issues and total_issues > 0:
            return 1
        if int(args.fail_under or 0) and total_issues >= int(args.fail_under):
            return 1
        return 0


# Demo functions
def demo_func(a: int, b: int) -> int:
    """Demo function with typed args and return."""
    c: int = a + b
    return c


class DemoClass:
    """Demo class for class object source extraction."""

    def method(self, x, y: int) -> int:
        _ = x
        z: int = y
        return z


# Convenience functions for backward compatibility
def analyze_targets(*args, **kwargs) -> Tuple[List[Issue], List[str]]:
    """Backward compatibility function."""
    return TypeCoverage().analyze_targets(*args, **kwargs)


def detect_untyped(*args, **kwargs) -> str:
    """Backward compatibility function."""
    return TypeCoverage().detect_untyped(*args, **kwargs)


def parse_and_run(argv: Optional[Sequence[str]] = None) -> int:
    """Backward compatibility function."""
    return TypeCoverage().parse_and_run(argv)


# ----------------------------- file: typecoverage/__main__.py
"""
Module runner for ``python -m typecoverage``.
Uses the same CLI as ``typecoverage`` when installed as a package.
"""

if __name__ == "__main__":
    exit(parse_and_run())
