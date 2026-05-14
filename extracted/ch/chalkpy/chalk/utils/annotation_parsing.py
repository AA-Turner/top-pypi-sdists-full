import ast
import inspect
import textwrap
from typing import Any, Callable, Dict, Optional

from chalk._lsp.error_builder import ResolverErrorBuilder
from chalk.df.ast_parser import convert_slice, eval_converted_expr
from chalk.utils.collections import get_unique_item


class ResolverAnnotationParser:
    def __init__(
        self,
        resolver: Callable,
        glbs: Optional[Dict[str, Any]],
        lcls: Optional[Dict[str, Any]],
        error_builder: ResolverErrorBuilder,
    ):
        super().__init__()
        self.resolver = resolver
        self.glbs = glbs
        self.lcls = lcls

        self._args = {arg.arg: arg for arg in self._get_resolver_args()}
        self.builder = error_builder

    def _get_resolver_args(self):
        source = inspect.getsource(self.resolver)
        parsed_source = ast.parse(textwrap.dedent(source))
        function_def = get_unique_item(parsed_source.body)
        if not isinstance(function_def, (ast.FunctionDef, ast.AsyncFunctionDef)):
            raise TypeError(f"The resolver must be a function. Received:\n\n{source}")
        args = function_def.args
        return [*args.posonlyargs, *args.args, *args.kwonlyargs]

    def parse_annotation(self, name: str):
        arg = self._args[name]
        annotation = arg.annotation
        if annotation is None:
            self.builder.add_diagnostic(
                message=(
                    f"Argument '{name}' for resolver '{self.resolver.__name__}' was not defined with a type annotation."
                ),
                code="84",
                label="missing annotation",
                range=self.builder.function_arg_value_by_name(name),
                raise_error=TypeError,
            )
        if isinstance(annotation, ast.Constant):
            val = annotation.value
            if not isinstance(val, str):
                self.builder.add_diagnostic(
                    message=f"Argument {name} has a Literal[...] type annotation, but it is not a string.",
                    code="85",
                    label="invalid annotation",
                    range=self.builder.function_arg_annotation_by_name(name),
                    raise_error=TypeError,
                )

            # string of type annotation
            val = ast.parse(val, mode="eval")
            if not isinstance(val, ast.Expr):
                self.builder.add_diagnostic(
                    message=f"Argument {name} has a Literal type annotation, but it is not a string.",
                    code="86",
                    label="invalid argument",
                    range=self.builder.function_arg_annotation_by_name(name),
                    raise_error=TypeError,
                )
            annotation = val.body

        if isinstance(annotation, ast.Subscript):
            # All fancy ast parsing would appear within the subscript of a df __getitem__
            annotation = ast.Subscript(
                value=annotation.value,
                slice=convert_slice(annotation.slice),  # pyright: ignore[reportArgumentType]
                ctx=annotation.ctx,
            )
        return eval_converted_expr(annotation, self.glbs, self.lcls)
