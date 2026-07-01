from __future__ import annotations

import ast
import difflib
import inspect
import linecache
import types
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Dict, List, Mapping, NoReturn, Optional, Type, overload

from executing import Source

from chalk._lsp.finders import (
    get_comment_range,
    get_feature_range,
    get_full_comment_range,
    get_full_range,
    get_sql_range,
    get_variable_range,
    node_to_range,
)
from chalk.parsed.ast_context import get_project_ast_context
from chalk.parsed.duplicate_input_gql import (
    CodeActionGQL,
    CodeDescriptionGQL,
    DiagnosticGQL,
    DiagnosticRelatedInformationGQL,
    DiagnosticSeverityGQL,
    LocationGQL,
    PositionGQL,
    RangeGQL,
)
from chalk.utils.collections import OrderedSet
from chalk.utils.string import oxford_comma_list

if TYPE_CHECKING:
    import types

    from sqlglot.expressions import Select, Union

    from chalk.features import FeatureWrapper
    from chalk_rs import FeatureClassAST, ResolverAST


@dataclass
class FunctionCallerInfo:
    """Information about the caller of a function, including AST node and source details."""

    node: ast.Call | None
    source: str
    filename: str
    lineno: int
    caller_source: str | None


def get_function_caller_info(frame_offset: int = 1) -> FunctionCallerInfo:
    """Extract caller information including AST node and source details."""
    caller_source: str | None = None
    caller_filename: str | None = None
    caller_lineno: int | None = None
    caller_node: ast.Call | None = None
    source = ""

    current_frame = inspect.currentframe()
    if current_frame is not None:
        frame = current_frame
        for _ in range(frame_offset + 1):
            next_frame = frame.f_back
            if next_frame is None:
                break
            frame = next_frame

        caller_filename = inspect.getfile(frame)
        caller_lineno = inspect.getlineno(frame)
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        source = "".join(linecache.getlines(filename))

        try:
            tree = ast.parse(source, filename)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and node.lineno == lineno:
                    caller_source = ast.get_source_segment(source, node)
                    caller_node = node
                    break
        except Exception:
            pass

        if caller_source is None:
            try:
                caller_source = inspect.getsource(frame)
            except Exception:
                caller_source = None

    del current_frame

    return FunctionCallerInfo(
        node=caller_node,
        source=source,
        filename=caller_filename or "<unknown file>",
        lineno=caller_lineno or 0,
        caller_source=caller_source,
    )


class DiagnosticBuilder:
    def __init__(
        self,
        severity: DiagnosticSeverityGQL,
        message: str,
        uri: str,
        range: RangeGQL,
        label: str,
        code: str,
        code_href: str | None,
    ):
        super().__init__()
        self.uri = uri
        self.diagnostic = DiagnosticGQL(
            range=range,
            message=message,
            severity=severity,
            code=code,
            codeDescription=CodeDescriptionGQL(href=code_href) if code_href is not None else None,
            relatedInformation=[
                DiagnosticRelatedInformationGQL(
                    location=LocationGQL(uri=uri, range=range),
                    message=label,
                )
            ],
        )

    def with_range(
        self,
        range: RangeGQL | ast.AST | None,
        label: str,
    ) -> DiagnosticBuilder:
        if isinstance(range, ast.AST):
            range = node_to_range(range)
        if range is None:
            return self

        assert self.diagnostic.relatedInformation is not None
        self.diagnostic.relatedInformation.append(
            DiagnosticRelatedInformationGQL(
                location=LocationGQL(
                    uri=self.uri,
                    range=range,
                ),
                message=label,
            )
        )
        return self


_dummy_builder = DiagnosticBuilder(
    severity=DiagnosticSeverityGQL.Error,
    message="",
    uri="",
    range=RangeGQL(
        start=PositionGQL(line=0, character=0),
        end=PositionGQL(line=0, character=0),
    ),
    label="",
    code="",
    code_href=None,
)


class LSPErrorBuilder:
    lsp: bool = False
    """This should ONLY be True if we're running `chalk export`.
    DO NOT SET THIS TO TRUE IN ANY OTHER CONTEXT.
    Talk to Elliot if you think you need to set this to True."""

    all_errors: Mapping[str, list[DiagnosticGQL]] = defaultdict(list)
    all_edits: list[CodeActionGQL] = []

    _exception_map: dict[int, tuple[str, DiagnosticGQL]] = {}
    _strong_refs: dict[int, Exception] = {}
    """Maintain exception_map's keys `id(exception)`.
    This could be done better with weakrefs, but you
    cant naively use a weakref.WeakKeyDictionary because
    we can't depend on the __eq__ method of the exception
    object."""

    _node_map: dict[tuple[FeatureWrapper, str], tuple[ast.AST, types.FrameType]] = {}

    @classmethod
    def has_errors(cls) -> bool:
        # `all_errors` is a misnomer: add_diagnostic() appends every diagnostic
        # regardless of severity (Warning/Info/Hint included). Only Error-severity
        # diagnostics should block graph load, so filter here rather than treating
        # a non-empty collection as fatal.
        return cls.lsp and any(
            d.severity == DiagnosticSeverityGQL.Error for diagnostics in cls.all_errors.values() for d in diagnostics
        )

    @classmethod
    def save_node(cls, wrapper: FeatureWrapper, item: str):
        frame = inspect.currentframe()
        if frame is None:
            return
        i = 0
        while i < 2 and frame is not None:
            frame = frame.f_back
            i += 1
        if frame is None:
            return
        node_map_key = (wrapper, item)
        if node_map_key not in cls._node_map:
            try:
                node = Source.executing(frame).node
            except Exception:
                return
            if node is not None:  # pyright: ignore[reportUnnecessaryComparison]
                try:
                    cls._node_map[node_map_key] = (node, frame)
                except:
                    pass

    @classmethod
    def get_node(cls, wrapper: FeatureWrapper, item: str) -> tuple[ast.AST, types.FrameType] | None:
        return cls._node_map.get((wrapper, item))

    @classmethod
    def save_exception(cls, e: Exception, uri: str, diagnostic: DiagnosticGQL):
        """Save an exception to be promoted to a diagnostic later.
        Some exceptions are handled (e.g. hasattr(...) handles AttributeError)
        and should not become diagnostics unless the error isn't handled."""
        cls._exception_map[id(e)] = (uri, diagnostic)
        cls._strong_refs[id(e)] = e

    @classmethod
    def promote_exception(cls, e: Exception) -> bool:
        """Promote a previously saved exception to a diagnostic.
        Returns whether the exception was promoted."""
        if id(e) in cls._exception_map:
            uri, diagnostic = cls._exception_map[id(e)]

            # Check if this diagnostic already exists (deduplication)
            # Compare by message, range, and uri to detect duplicates
            for existing in cls.all_errors[uri]:
                if existing.message == diagnostic.message and existing.range == diagnostic.range:
                    # Already exists, don't add duplicate
                    del cls._exception_map[id(e)]
                    del cls._strong_refs[id(e)]
                    return False  # Not promoted, already exists

            # Not a duplicate, add it
            cls.all_errors[uri].append(diagnostic)
            del cls._exception_map[id(e)]
            del cls._strong_refs[id(e)]
            return True

        return False


class FeatureClassErrorBuilder:
    def __init__(
        self,
        uri: str,
        namespace: str,
        range_node: FeatureClassAST | None = None,
    ):
        super().__init__()
        self.uri = uri
        self.diagnostics: List[DiagnosticGQL] = []
        self.namespace = namespace
        self.range_node = range_node
        self.error_cache: OrderedSet[tuple[str, RangeGQL | ast.AST, str]] = OrderedSet()

    @staticmethod
    def _tuple_to_range(range_tuple: tuple[int, int, int, int] | None) -> RangeGQL | None:
        if range_tuple is None:
            return None
        start_line, start_char, end_line, end_char = range_tuple
        return RangeGQL(
            # Rust AST tuple locations are already 0-based LSP lines.
            start=PositionGQL(
                line=start_line,
                character=start_char,
            ),
            end=PositionGQL(
                line=end_line,
                character=end_char,
            ),
        )

    def property_range(self, feature_name: str) -> RangeGQL | None:
        if self.range_node is None:
            return None
        field = self.range_node.fields.get(feature_name)
        return None if field is None else self._tuple_to_range(field.field_name_location)

    def annotation_range(self, feature_name: str) -> RangeGQL | None:
        if self.range_node is None:
            return None
        field = self.range_node.fields.get(feature_name)
        return None if field is None else self._tuple_to_range(field.annotation)

    def property_value_range(self, feature_name: str) -> RangeGQL | None:
        if self.range_node is None:
            return None
        field = self.range_node.fields.get(feature_name)
        return None if field is None else self._tuple_to_range(field.feature_call)

    def property_value_kwarg_range(self, feature_name: str, kwarg: str) -> RangeGQL | None:
        if self.range_node is None:
            return None
        field = self.range_node.fields.get(feature_name)
        return None if field is None else self._tuple_to_range(field.kwargs.get(kwarg))

    def decorator_kwarg_value_range(self, kwarg: str) -> RangeGQL | None:
        return self.range_node and self._tuple_to_range(self.range_node.kwargs.get(kwarg))

    def class_definition_range(self) -> RangeGQL | None:
        return self.range_node and self._tuple_to_range(self.range_node.class_definition_location)

    def invalid_attribute(
        self,
        root_feature_str: str,
        root_is_feature_class: bool,
        item: str,
        candidates: List[str],
        back: int,
        saved_frame: FeatureWrapper | None = None,
    ):
        back = back + 1
        message = (
            f"Invalid attribute '{item}' on feature {'class ' if root_is_feature_class else ''}"
            + f"'{root_feature_str}'."
        )
        if not LSPErrorBuilder.lsp:
            # Short circuit if we're not in an LSP context. What follows is expensive.
            raise AttributeError(message)

        if saved_frame is not None:
            saved_node_and_frame = LSPErrorBuilder.get_node(saved_frame, item)
            if saved_node_and_frame is None:
                raise AttributeError(message)
            node, frame = saved_node_and_frame
        else:
            frame: Optional[types.FrameType] = inspect.currentframe()
            i = 0
            while i < back and frame is not None:
                frame = frame.f_back
                i += 1

            if frame is None or i != back:
                raise AttributeError(message)

            try:
                node = Source.executing(frame).node
            except Exception:
                raise AttributeError(message)

        uri = frame.f_locals.get("__file__")
        if isinstance(node, ast.Attribute):
            if node.end_lineno is None or node.end_col_offset is None:
                raise AttributeError(message)
            node = RangeGQL(
                # Python AST lines are 1-based; LSP positions are 0-based.
                start=PositionGQL(
                    line=node.end_lineno - 1,
                    character=node.end_col_offset - len(node.attr),
                ),
                end=PositionGQL(
                    line=node.end_lineno - 1,
                    character=node.end_col_offset,
                ),
            )

        candidates = [f"'{c}'" for c in candidates if not c.startswith("_")]
        if len(candidates) > 0:
            all_scores = [
                (
                    difflib.SequenceMatcher(a=item, b=candidate).quick_ratio(),
                    candidate,
                )
                for candidate in candidates
            ]
            all_scores.sort(key=lambda x: -x[0])

            if len(candidates) > 5:
                prefix = "The closest options are"
                candidates = [c for (_, c) in all_scores[:5]]
            elif len(candidates) == 1:
                prefix = "The only valid option is"
            else:
                prefix = "Valid options are"

            message += f" {prefix} {oxford_comma_list(candidates)}."

        self.add_diagnostic(
            message=message,
            range=node,
            label="Invalid attribute",
            code="55",
            raise_error=AttributeError,
            uri=uri,
        )

    @overload
    def add_diagnostic(
        self,
        message: str,
        label: str,
        code: str,
        *,
        range: RangeGQL | ast.AST | None,
        code_href: str | None = None,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        raise_error: None = ...,
        uri: str | None = ...,
    ) -> DiagnosticBuilder: ...

    @overload
    def add_diagnostic(
        self,
        message: str,
        label: str,
        code: str,
        *,
        range: RangeGQL | ast.AST | None,
        code_href: str | None = None,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        raise_error: Type[Exception],
        uri: str | None = ...,
    ) -> NoReturn: ...

    def add_diagnostic(
        self,
        message: str,
        label: str,
        code: str,
        range: RangeGQL | ast.AST | None,
        code_href: str | None = None,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        raise_error: Type[Exception] | None = None,
        uri: str | None = None,
    ) -> DiagnosticBuilder:
        uri = self.uri if uri is None else uri
        if not LSPErrorBuilder.lsp:
            if raise_error is not None:
                raise raise_error(message)
            return _dummy_builder
        default_error = TypeError
        if range is None:
            raise raise_error(message) if raise_error else default_error(message)
        if isinstance(range, ast.AST):
            range = node_to_range(range)
            if range is None:
                raise raise_error(message) if raise_error else default_error(message)

        builder = DiagnosticBuilder(
            severity=severity,
            message=message,
            uri=uri,
            range=range,
            label=label,
            code=code,
            code_href=code_href,
        )

        error = None if raise_error is None else raise_error(message)
        if error is None:
            if (message, range, uri) not in self.error_cache:
                self.diagnostics.append(builder.diagnostic)
                LSPErrorBuilder.all_errors[uri].append(builder.diagnostic)
                self.error_cache.add((message, range, uri))
        else:
            LSPErrorBuilder.save_exception(error, uri, builder.diagnostic)
            raise error

        return builder


class ResolverErrorBuilder:
    def __init__(
        self,
        fn: Callable | None,
    ):
        super().__init__()
        self._fn = fn
        self.diagnostics: List[DiagnosticGQL] = []
        self._uri: str | types.EllipsisType = ...
        self._resolver_node: ResolverAST | None | types.EllipsisType = ...

    @property
    def uri(self):
        if self._uri is ...:
            self._load_node_and_uri()
        assert self._uri is not ...
        return self._uri

    def _load_node_and_uri(self):
        """Lazily load resolver range info from the shared Rust AST index."""
        self._uri = "__main__"
        self._resolver_node = None

        if self._fn is None:
            return

        lookup_fn = getattr(self._fn, "fn", None)
        if not callable(lookup_fn):
            lookup_fn = self._fn
        if not callable(lookup_fn):
            return
        file_path = Path(lookup_fn.__code__.co_filename).resolve()
        try:
            index = get_project_ast_context(file_path.parent)
            self._uri = str(file_path)
            self._resolver_node = index.function_ast_in_file(str(file_path), lookup_fn.__name__)
            if self._resolver_node is None:
                self._resolver_node = index.function_ast(lookup_fn.__module__, lookup_fn.__name__)
        except Exception:
            self._resolver_node = None

    @property
    def resolver_node(self):
        if self._resolver_node is ...:
            self._load_node_and_uri()
        assert self._resolver_node is not ...
        return self._resolver_node

    @staticmethod
    def _tuple_to_range(range_tuple: tuple[int, int, int, int] | None) -> RangeGQL | None:
        if range_tuple is None:
            return None
        start_line, start_char, end_line, end_char = range_tuple
        return RangeGQL(
            # Rust AST tuple locations are already 0-based LSP lines.
            start=PositionGQL(
                line=start_line,
                character=start_char,
            ),
            end=PositionGQL(
                line=end_line,
                character=end_char,
            ),
        )

    @overload
    def add_diagnostic(
        self,
        message: str,
        label: str,
        code: str,
        range: RangeGQL | ast.AST | None,
        code_href: str | None = None,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        raise_error: None = ...,
        uri: str | None = ...,
    ) -> DiagnosticBuilder: ...

    @overload
    def add_diagnostic(
        self,
        message: str,
        label: str,
        code: str,
        *,
        range: RangeGQL | ast.AST | None,
        code_href: str | None = None,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        raise_error: Type[Exception] = ...,
        uri: str | None = ...,
    ) -> NoReturn: ...

    def add_diagnostic(
        self,
        message: str,
        label: str,
        code: str,
        range: RangeGQL | ast.AST | None,
        code_href: str | None = None,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        raise_error: Type[Exception] | None = None,
        uri: str | None = None,
    ) -> DiagnosticBuilder:
        """
        Parameters
        ----------
        message
            Longform description of error with names of attributes, etc.
        label
            Shortform category of error.
        code
            Unique identifier of error kind.
        range
            Line number and offsets of the start and end of text with error.
        code_href
            Link to docs.
        severity
            Whether this is an error or warning.
        raise_error
            If we cannot proceed, raise with this error kind and message.
        uri
            Filepath.

        Returns
        -------
        DiagnosticBuilder
        """
        if not LSPErrorBuilder.lsp:
            if raise_error is not None:
                raise raise_error(message)
            return _dummy_builder
        uri = self.uri if uri is None else uri
        default_error = TypeError
        if range is None:
            raise raise_error(message) if raise_error else default_error(message)

        if isinstance(range, ast.AST):
            range = node_to_range(range)
            if range is None:
                raise raise_error(message) if raise_error else default_error(message)

        builder = DiagnosticBuilder(
            severity=severity,
            message=message,
            uri=uri,
            range=range,
            label=label,
            code=code,
            code_href=code_href,
        )

        error = None if raise_error is None else raise_error(message)
        if error is None:
            self.diagnostics.append(builder.diagnostic)
            LSPErrorBuilder.all_errors[uri].append(builder.diagnostic)
        else:
            LSPErrorBuilder.save_exception(error, uri, builder.diagnostic)
            raise error
        return builder

    def function_decorator(self) -> RangeGQL | None:
        return self.resolver_node and self._tuple_to_range(self.resolver_node.decorator_location)

    def function_decorator_arg_by_name(self, name: str) -> RangeGQL | None:
        return self.resolver_node and self._tuple_to_range(self.resolver_node.kwargs.get(name))

    def function_decorator_key_from_dict(
        self,
        decorator_field: str,
        arg_name: str,
    ) -> RangeGQL | None:
        return self.resolver_node and self._tuple_to_range(
            self.resolver_node.kwarg_dict_key_names.get(decorator_field, {}).get(arg_name)
        )

    def function_decorator_value_from_dict(
        self,
        decorator_field: str,
        arg_name: str,
    ) -> RangeGQL | None:
        return self.resolver_node and self._tuple_to_range(
            self.resolver_node.kwarg_dict_values.get(decorator_field, {}).get(arg_name)
        )

    def function_arg_values(self) -> Dict[str, RangeGQL | None]:
        if self.resolver_node is None:
            return {}
        args = self.resolver_node.args
        ordered_names = self.resolver_node.args_in_order
        ordered_values: Dict[str, RangeGQL | None] = {
            name: self._tuple_to_range(args[name].arg_location) for name in ordered_names if name in args
        }
        unordered_values: Dict[str, RangeGQL | None] = {
            name: self._tuple_to_range(arg.arg_location) for name, arg in args.items() if name not in ordered_names
        }
        return ordered_values | unordered_values

    def function_arg_value_by_name(self, name: str) -> RangeGQL | None:
        return self.function_arg_values().get(name)

    def function_arg_value_by_index(self, index: int) -> RangeGQL | None:
        if self.resolver_node is None:
            return None

        args_in_order = self.resolver_node.args_in_order
        if len(args_in_order) == 0:
            return self.function_name()
        if index < len(args_in_order):
            return self.function_arg_values().get(args_in_order[index])
        return None

    def function_arg_annotations(self) -> Dict[str, RangeGQL | None]:
        if self.resolver_node is None:
            return {}
        args = self.resolver_node.args
        ordered_names = self.resolver_node.args_in_order
        ordered_values: Dict[str, RangeGQL | None] = {
            name: self._tuple_to_range(args[name].annotation) for name in ordered_names if name in args
        }
        unordered_values: Dict[str, RangeGQL | None] = {
            name: self._tuple_to_range(arg.annotation) for name, arg in args.items() if name not in ordered_names
        }
        return ordered_values | unordered_values

    def function_arg_annotation_by_name(self, name: str) -> RangeGQL | None:
        return self.function_arg_annotations().get(name)

    def function_arg_annotation_by_index(self, index: int) -> RangeGQL | None:
        if self.resolver_node is None:
            return None

        args_in_order = self.resolver_node.args_in_order
        if index < len(args_in_order):
            return self.function_arg_annotations().get(args_in_order[index])
        return None

    def function_return_annotation(self) -> RangeGQL | None:
        return self.resolver_node and (
            self._tuple_to_range(self.resolver_node.return_annotation)
            or self._tuple_to_range(self.resolver_node.missing_return_annotation)
        )

    def function_return_statements(self) -> List[RangeGQL | None]:
        if self.resolver_node is None:
            return []
        return [self._tuple_to_range(range_tuple) for range_tuple in self.resolver_node.return_statements]

    def function_name(self) -> RangeGQL | None:
        return self.resolver_node and self._tuple_to_range(self.resolver_node.resolver_name_location)

    def string_in_node(self, node: RangeGQL | ast.AST, string: str, text: list[str]) -> RangeGQL | None:
        start_line = range_or_node_to_start_line(node)
        end_line = range_or_node_to_end_line(node)
        if start_line is None or end_line is None:
            return None
        for i, line in enumerate(text):
            if i < start_line:
                continue
            if i > end_line:
                return None
            if i == start_line:
                start_char = range_or_node_to_start_char(node)
                if start_char is None:
                    return None
            else:
                start_char = 0
            if i == end_line:
                end_char = range_or_node_to_end_char(node)
                if end_char is None:
                    return None
            else:
                end_char = len(line)
            starting_index = line.find(string, start_char, end_char)
            if starting_index != -1:
                return RangeGQL(
                    # Line indexes are 0-based LSP lines.
                    start=PositionGQL(
                        line=i,
                        character=starting_index,
                    ),
                    end=PositionGQL(line=i, character=starting_index + len(string)),
                )
        return None


def get_resolver_error_builder(fn: Callable) -> ResolverErrorBuilder:
    error_builder = ResolverErrorBuilder(fn=fn)
    return error_builder


class SQLFileResolverErrorBuilder:
    def __init__(self, uri: str, sql_string: str, has_import_errors: bool):
        super().__init__()
        self.uri = uri
        self.has_import_errors = has_import_errors
        self.diagnostics: List[DiagnosticGQL] = []
        self.sql_string = sql_string
        self.sql_lines = sql_string.splitlines()

    def add_diagnostic(
        self,
        message: str,
        label: str,
        code: str,
        range: RangeGQL | ast.AST | None,
        code_href: str | None = None,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        raise_error: Type[Exception] | None = None,
        uri: str | None = None,
    ) -> DiagnosticBuilder:
        """
        Parameters
        ----------
        message
            Longform description of error with names of attributes, etc.
        label
            Shortform category of error.
        code
            Unique identifier of error kind.
        range
            Line number and offsets of the start and end of text with error.
        code_href
            Link to docs.
        severity
            Whether this is an error or warning.
        raise_error
            If we cannot proceed, raise with this error kind and message.
        uri
            Filepath.

        Returns
        -------
        DiagnosticBuilder
        """
        if self.has_import_errors:
            # pass: we don't need lsp
            return _dummy_builder
        if not LSPErrorBuilder.lsp:
            if raise_error is not None:
                raise raise_error(message)
            return _dummy_builder
        default_error = TypeError
        if range is None:
            raise raise_error(message) if raise_error else default_error(message)
        uri = self.uri if uri is None else uri

        if isinstance(range, ast.AST):
            range = node_to_range(range)
            if range is None:
                raise raise_error(message) if raise_error else default_error(message)

        builder = DiagnosticBuilder(
            severity=severity,
            message=message,
            uri=uri,
            range=range,
            label=label,
            code=code,
            code_href=code_href,
        )

        error = None if raise_error is None else raise_error(message)
        if error is None:
            self.diagnostics.append(builder.diagnostic)
            LSPErrorBuilder.all_errors[uri].append(builder.diagnostic)
        else:
            LSPErrorBuilder.save_exception(error, uri, builder.diagnostic)
            raise error

        return builder

    def comment_range_by_key(self, name: str) -> RangeGQL | None:
        return get_comment_range(self.sql_lines, name)

    def full_comment_range(self) -> RangeGQL | None:
        return get_full_comment_range(self.sql_lines)

    def variable_range_by_name(self, name: str) -> RangeGQL | None:
        return get_variable_range(self.sql_lines, name)

    def value_range_by_name(self, glot: Select | Union, name: str) -> RangeGQL | None:
        return get_feature_range(self.sql_lines, glot, name)

    def custom_range(self, line_no: int, col: int, length: int | None = None) -> RangeGQL:
        length = length or 1
        # SQL/YAML parser metadata callers pass 1-based source lines.
        line = line_no - 1
        return RangeGQL(
            start=PositionGQL(
                line=line,
                character=col,
            ),
            end=PositionGQL(
                line=line,
                character=col + length,
            ),
        )

    def full_range(self) -> RangeGQL:
        return get_full_range(self.sql_lines)

    def sql_range(self) -> RangeGQL | None:
        return get_sql_range(self.sql_lines)

    def add_diagnostic_with_spellcheck(
        self,
        spellcheck_item: str,
        spellcheck_candidates: List[str],
        message: str,
        label: str,
        code: str,
        range: RangeGQL | ast.AST | None,
        code_href: str | None = None,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        raise_error: Type[Exception] | None = None,
        uri: str | None = None,
    ):
        if not LSPErrorBuilder.lsp:
            # Don't do anything special let's just add the diagnostic
            return self.add_diagnostic(
                message=message,
                label=label,
                code=code,
                range=range,
                code_href=code_href,
                severity=severity,
                raise_error=raise_error,
                uri=uri,
            )

        candidates = [f"'{c}'" for c in spellcheck_candidates if not c.split(".")[-1].startswith("_")]
        if len(candidates) > 0:
            all_scores = [
                (
                    difflib.SequenceMatcher(a=spellcheck_item, b=candidate).quick_ratio(),
                    candidate,
                )
                for candidate in candidates
            ]
            all_scores.sort(key=lambda x: -x[0])

            if len(candidates) > 5:
                prefix = "The closest options are"
                candidates = [c for (_, c) in all_scores[:5]]
            elif len(candidates) == 1:
                prefix = "The only valid option is"
            else:
                prefix = "Valid options are"
                candidates = [c for (_, c) in all_scores]

            message += f" {prefix} {oxford_comma_list(candidates)}."

        return self.add_diagnostic(
            message=message,
            label=label,
            code=code,
            range=range,
            code_href=code_href,
            severity=severity,
            raise_error=raise_error,
            uri=uri,
        )


class FunctionCallErrorBuilder:
    """Error builder for functions that are called (not decorated).

    Unlike FeatureClassErrorBuilder and ResolverErrorBuilder which operate on decorators,
    this error builder works with function calls like make_stream_resolver().
    """

    def __init__(self, caller_info: FunctionCallerInfo):
        super().__init__()
        self.caller_info = caller_info
        self.diagnostics: List[DiagnosticGQL] = []
        self.error_cache: OrderedSet[tuple[str, RangeGQL | ast.AST, str]] = OrderedSet()

    @property
    def uri(self) -> str:
        return self.caller_info.filename

    def function_arg_range_by_name(self, name: str) -> RangeGQL | None:
        """Get the range for a function argument by its keyword name."""
        node = self.caller_info.node
        if node is None:
            return None
        for keyword in node.keywords:
            if keyword.arg == name:
                return node_to_range(keyword.value)
        return None

    @overload
    def add_diagnostic(
        self,
        message: str,
        label: str,
        code: str,
        *,
        range: RangeGQL | ast.AST | None,
        code_href: str | None = None,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        raise_error: None = ...,
        uri: str | None = ...,
    ) -> DiagnosticBuilder: ...

    @overload
    def add_diagnostic(
        self,
        message: str,
        label: str,
        code: str,
        *,
        range: RangeGQL | ast.AST | None,
        code_href: str | None = None,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        raise_error: Type[Exception],
        uri: str | None = ...,
    ) -> NoReturn: ...

    def add_diagnostic(
        self,
        message: str,
        label: str,
        code: str,
        range: RangeGQL | ast.AST | None,
        code_href: str | None = None,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        raise_error: Type[Exception] | None = None,
        uri: str | None = None,
    ) -> DiagnosticBuilder:
        """Add a diagnostic for validation errors in function calls.

        Parameters
        ----------
        message
            Longform description of error with names of attributes, etc.
        label
            Shortform category of error.
        code
            Unique identifier of error kind.
        range
            Line number and offsets of the start and end of text with error.
        code_href
            Link to docs.
        severity
            Whether this is an error or warning.
        raise_error
            If we cannot proceed, raise with this error kind and message.
        uri
            Filepath.

        Returns
        -------
        DiagnosticBuilder
            DiagnosticBuilder for chaining additional ranges.
        """
        uri = self.uri if uri is None else uri
        if not LSPErrorBuilder.lsp:
            if raise_error is not None:
                raise raise_error(message)
            return _dummy_builder

        default_error = TypeError
        if range is None:
            raise raise_error(message) if raise_error else default_error(message)

        if isinstance(range, ast.AST):
            range = node_to_range(range)
            if range is None:
                raise raise_error(message) if raise_error else default_error(message)

        builder = DiagnosticBuilder(
            severity=severity,
            message=message,
            uri=uri,
            range=range,
            label=label,
            code=code,
            code_href=code_href,
        )

        error = None if raise_error is None else raise_error(message)
        if error is None:
            if (message, range, uri) not in self.error_cache:
                self.diagnostics.append(builder.diagnostic)
                LSPErrorBuilder.all_errors[uri].append(builder.diagnostic)
                self.error_cache.add((message, range, uri))
        else:
            LSPErrorBuilder.save_exception(error, uri, builder.diagnostic)
            raise error

        return builder


def build_diagnostic_from_message(
    message: str, code: str, source_line_start: int | None, source_line_end: int | None
) -> DiagnosticGQL:
    if source_line_start is None or source_line_start <= 0 or source_line_end is None or source_line_end <= 0:
        start_line = 0
        end_line = 0
    else:
        # Source spans are 1-based inclusive; LSP lines are 0-based with exclusive ends.
        start_line = source_line_start - 1
        end_line = source_line_end
    return DiagnosticGQL(
        message=message,
        range=RangeGQL(
            start=PositionGQL(line=start_line, character=0),
            end=PositionGQL(line=end_line, character=0),
        ),
        severity=DiagnosticSeverityGQL.Error,
        code=code,
        codeDescription=None,
    )


"""
The following helper methods are empirically proven to be correct.
The lines are 0 indexed and inclusive.
The character offsets are 1 indexed and non-inclusive
"""


def range_or_node_to_start_line(range_or_node: RangeGQL | ast.AST) -> int | None:
    if isinstance(range_or_node, RangeGQL):
        return range_or_node.start.line
    else:
        i = getattr(range_or_node, "lineno", None)
        if i is None:
            return None
    return i - 1


def range_or_node_to_end_line(range_or_node: RangeGQL | ast.AST) -> int | None:
    if isinstance(range_or_node, RangeGQL):
        return range_or_node.end.line
    else:
        i = getattr(range_or_node, "end_lineno", None)
        if i is None:
            return None
    return i - 1


def range_or_node_to_start_char(range_or_node: RangeGQL | ast.AST) -> int | None:
    if isinstance(range_or_node, RangeGQL):
        i = range_or_node.start.character
    else:
        i = getattr(range_or_node, "col_offset", None)
        if i is None:
            return None
    return i


def range_or_node_to_end_char(range_or_node: RangeGQL | ast.AST) -> int | None:
    if isinstance(range_or_node, RangeGQL):
        i = range_or_node.end.character
    else:
        i = getattr(range_or_node, "end_col_offset", None)
        if i is None:
            return None
    return max(i - 1, 0)
