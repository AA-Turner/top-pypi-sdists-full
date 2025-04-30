from __future__ import annotations

import ast
import dataclasses
import difflib
import inspect
import textwrap
from collections import defaultdict
from typing import TYPE_CHECKING, Callable, Dict, List, Mapping, NoReturn, Optional, Type, overload

from executing import Source

from chalk._lsp._class_finder import get_function_ast
from chalk._lsp.finders import (
    get_annotation_range,
    get_class_definition_range,
    get_comment_range,
    get_decorator_kwarg_value_range,
    get_feature_range,
    get_full_comment_range,
    get_full_range,
    get_function_arg_annotations,
    get_function_arg_values,
    get_function_decorator_arg_by_name,
    get_function_decorator_range,
    get_function_name,
    get_function_return_annotation,
    get_function_return_statement,
    get_key_from_dict_node,
    get_missing_return_annotation,
    get_property_range,
    get_property_value_call_range,
    get_property_value_range,
    get_sql_range,
    get_value_from_dict_node,
    get_variable_range,
    node_to_range,
)
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
from chalk.utils.source_parsing import should_skip_source_code_parsing
from chalk.utils.string import oxford_comma_list

if TYPE_CHECKING:
    import types

    from sqlglot.expressions import Select, Union

    from chalk.features import FeatureWrapper


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
    def has_errors(cls):
        return cls.lsp and len(cls.all_errors) > 0

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
                    cls._node_map[(wrapper, item)] = (node, frame)
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
            cls.all_errors[uri].append(diagnostic)
            del cls._exception_map[id(e)]
            del cls._strong_refs[id(e)]
            return True

        return False


class FeatureClassErrorBuilder:
    def __init__(self, uri: str, namespace: str, node: ast.ClassDef | None):
        super().__init__()
        self.uri = uri
        self.diagnostics: List[DiagnosticGQL] = []
        self.namespace = namespace
        self.node = node

    def property_range(self, feature_name: str) -> ast.AST | None:
        if self.node is None:
            return None

        return get_property_range(cls=self.node, name=feature_name)

    def annotation_range(self, feature_name: str) -> ast.AST | None:
        if self.node is None:
            return None

        return get_annotation_range(cls=self.node, name=feature_name)

    def property_value_range(self, feature_name: str) -> ast.AST | None:
        if self.node is None:
            return None

        return get_property_value_range(cls=self.node, name=feature_name)

    def property_value_kwarg_range(self, feature_name: str, kwarg: str) -> ast.AST | None:
        if self.node is None:
            return None

        return get_property_value_call_range(cls=self.node, name=feature_name, kwarg=kwarg)

    def decorator_kwarg_value_range(self, kwarg: str) -> ast.AST | None:
        if self.node is None:
            return None

        return get_decorator_kwarg_value_range(cls=self.node, kwarg=kwarg)

    def class_definition_range(self) -> RangeGQL | None:
        if self.node is None:
            return None

        return get_class_definition_range(cls=self.node, filename=self.uri)

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
                start=PositionGQL(
                    line=node.end_lineno,
                    character=node.end_col_offset - len(node.attr),
                ),
                end=PositionGQL(
                    line=node.end_lineno,
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
    ) -> DiagnosticBuilder:
        ...

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
    ) -> NoReturn:
        ...

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
            self.diagnostics.append(builder.diagnostic)
            LSPErrorBuilder.all_errors[uri].append(builder.diagnostic)
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
        self._uri = ...
        self._node = ...

    @property
    def uri(self):
        if self._uri is ...:
            self._load_node_and_uri()
        assert self._uri is not ...
        return self._uri

    @property
    def node(self):
        if self._node is ...:
            self._load_node_and_uri()
        assert self._node is not ...
        return self._node

    def _load_node_and_uri(self):
        """Lazily loading the node and uri on first use, because parsing the source is slow. If there are no errors, then no need to parse it"""
        source_info: Optional[FunctionSource] = None
        if not should_skip_source_code_parsing() and self._fn is not None:
            try:
                filename = inspect.getfile(self._fn)
                resolver_source = inspect.getsource(self._fn)
                dedent_source = resolver_source and textwrap.dedent(resolver_source)
                try:
                    tree = get_function_ast(self._fn)
                except:
                    tree = None
                source_info = FunctionSource(
                    filename=filename,
                    source=resolver_source,
                    dedent_source=dedent_source,
                    tree=tree,
                )
            except:
                pass

        self._uri = source_info.filename if source_info is not None else "__main__"
        self._node = source_info and source_info.tree

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
    ) -> DiagnosticBuilder:
        ...

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
    ) -> NoReturn:
        ...

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

        :param message: longform description of error with names of attributes, etc.
        :param label: shortform category of error
        :param code: unique identifier of error kind
        :param range: line number + offset of start and end of text with error
        :param code_href: code_href: link to doc
        :param severity: is it an error? a warning?
        :param raise_error: if we cannot proceed, raise with this error kind and the message.
        :param uri: filepath
        :return:
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

    def function_decorator(self) -> ast.AST | None:
        if self.node is None:
            return None

        return get_function_decorator_range(node=self.node)

    def function_decorator_arg_by_name(self, name: str) -> ast.AST | None:
        if self.node is None:
            return None

        return get_function_decorator_arg_by_name(node=self.node, name=name)

    def function_decorator_key_from_dict(self, decorator_field: str, arg_name: str) -> ast.AST | None:
        if self.node is None:
            return None
        decorator_arg = get_function_decorator_arg_by_name(node=self.node, name=decorator_field)
        if not isinstance(decorator_arg, ast.Dict):
            return decorator_arg
        return get_key_from_dict_node(decorator_arg, arg_name) or decorator_arg

    def function_decorator_value_from_dict(self, decorator_field: str, arg_name: str) -> ast.AST | None:
        if self.node is None:
            return None
        decorator_arg = get_function_decorator_arg_by_name(node=self.node, name=decorator_field)
        if not isinstance(decorator_arg, ast.Dict):
            return decorator_arg
        return get_value_from_dict_node(decorator_arg, arg_name) or decorator_arg

    def function_arg_values(self) -> Dict[str, ast.AST | None]:
        if self.node is None:
            return {}

        return get_function_arg_values(node=self.node)

    def function_arg_value_by_name(self, name: str) -> ast.AST | None:
        return self.function_arg_values().get(name)

    def function_arg_value_by_index(self, index: int) -> ast.AST | RangeGQL | None:
        if self.node is None:
            return None

        if len(self.node.args.args) == 0:
            return get_function_name(self.node, self.uri)
        if index < len(self.node.args.args):
            return self.node.args.args[index]
        return None

    def function_arg_annotations(self) -> Dict[str, ast.AST | None]:
        if self.node is None:
            return {}

        return get_function_arg_annotations(node=self.node)

    def function_arg_annotation_by_name(self, name: str) -> ast.AST | None:
        return self.function_arg_annotations().get(name)

    def function_arg_annotation_by_index(self, index: int) -> ast.AST | None:
        if self.node is None:
            return None

        if index < len(self.node.args.args):
            return self.node.args.args[index].annotation
        return None

    def function_return_annotation(self) -> ast.AST | RangeGQL | None:
        if self.node is None:
            return None

        node_or_none = get_function_return_annotation(node=self.node)
        return node_or_none or get_missing_return_annotation(self.node, self.uri)

    def function_return_statements(self) -> List[ast.AST | None]:
        if self.node is None:
            return []

        return get_function_return_statement(node=self.node)

    def function_name(self) -> RangeGQL | None:
        if self.node is None:
            return None

        return get_function_name(self.node, self.uri)

    def string_in_node(self, node: ast.AST, string: str, text: list[str]) -> RangeGQL | None:
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
                    start=PositionGQL(
                        line=i + 1,
                        character=starting_index,
                    ),
                    end=PositionGQL(line=i + 1, character=starting_index + len(string)),
                )
        return None


@dataclasses.dataclass
class FunctionSource:
    filename: str
    source: str | None
    dedent_source: str | None
    tree: ast.FunctionDef | ast.AsyncFunctionDef | None


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

        :param message: longform description of error with names of attributes, etc.
        :param label: shortform category of error
        :param code: unique identifier of error kind
        :param range: line number + offset of start and end of text with error
        :param code_href: code_href: link to doc
        :param severity: is it an error? a warning?
        :param raise_error: if we cannot proceed, raise with this error kind and the message.
        :param uri: filepath
        :return:
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
        return RangeGQL(
            start=PositionGQL(
                line=line_no,
                character=col,
            ),
            end=PositionGQL(
                line=line_no,
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


"""
The following helper methods are empirically proven to be correct.
The lines are 0 indexed and inclusive.
The character offsets are 1 indexed and non-inclusive
"""


def range_or_node_to_start_line(range_or_node: RangeGQL | ast.AST) -> int | None:
    if isinstance(range_or_node, RangeGQL):
        i = range_or_node.start.line
    else:
        i = getattr(range_or_node, "lineno", None)
        if i is None:
            return None
    return i - 1


def range_or_node_to_end_line(range_or_node: RangeGQL | ast.AST) -> int | None:
    if isinstance(range_or_node, RangeGQL):
        i = range_or_node.end.line
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
