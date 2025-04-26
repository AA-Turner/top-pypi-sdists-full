import re
from typing import Any, Callable, Dict, List, Mapping, Optional, Set, Tuple, Union

from mypy.lookup import lookup_fully_qualified
from mypy.nodes import (
    ARG_NAMED_OPT,
    ARG_OPT,
    ARG_POS,
    GDEF,
    Argument,
    AssignmentStmt,
    Block,
    CallExpr,
    ClassDef,
    Expression,
    JsonDict,
    MypyFile,
    NameExpr,
    PlaceholderNode,
    RefExpr,
    SymbolTable,
    SymbolTableNode,
    TypeInfo,
    Var,
)
from mypy.plugin import (
    AnalyzeTypeContext,
    ClassDefContext,
    DynamicClassDefContext,
    FunctionContext,
    MethodContext,
    Plugin,
    SemanticAnalyzerPluginInterface,
)
from mypy.plugins.common import add_method, deserialize_and_fixup_type
from mypy.types import Instance, NoneType, Type, UnboundType

from chalk.features import DataFrame, Features, feature, features
from chalk.features.dataframe._impl import DataFrameMeta


def _get_full_name(cls: Union[type, Callable]):
    return f"{cls.__module__}.{cls.__name__}"


class PluginKeywords:
    @staticmethod
    def fullname_is_dataframe_class(fullname: str):
        return re.match(r"chalk\.feature_n\.feature_[0-9]+\.feature.DataFrame", fullname) is not None

    feature_set_decorators = {_get_full_name(features)}

    dataframe_meta = _get_full_name(DataFrameMeta)

    feature_makers = {
        _get_full_name(feature),
    }

    features_class = _get_full_name(Features)

    dataframe_class = _get_full_name(DataFrame)

    @staticmethod
    def get_features_from_metadata(metadata: Optional[Mapping[str, JsonDict]]) -> List[str]:
        return metadata.get("features", {}).get("attributes", []) if metadata is not None else []

    @staticmethod
    def set_features_metadata(obj, cols: List[Any]) -> None:
        obj.metadata["features"] = {"attributes": cols}

    @staticmethod
    def get_dataframe_cols_from_metadata(metadata: Mapping[str, JsonDict]) -> List[str]:
        return metadata.get("dataframe", {}).get("columns", [])

    @staticmethod
    def set_dataframe_cols_metadata(obj, cols: List[str]) -> None:
        obj.metadata["dataframe"] = {"columns": cols}

    @staticmethod
    def get_dataframe_class_fullname(n: int) -> str:
        return f"chalk.feature_n.feature_{str(n)}.feature.DataFrame"

    @staticmethod
    def get_feature_class_fullname(n: int) -> str:
        return f"chalk.feature_n.feature_{str(n)}.feature.Features"

    any_typevar: str = f"chalk.feature_n.feature_2.feature.T1"


class FeatureWrapper:
    def __init__(
        self,
        name: str,
        feature_name: str,
        line: int,
        column: int,
        type: Optional[Type],
        info: TypeInfo,
    ):
        self.feature_name = feature_name
        self.name = name
        self.line = line
        self.column = column
        self.type = type
        self.info = info

    def to_argument(self) -> Argument:
        return Argument(
            variable=self.to_var(),
            type_annotation=self.type,
            initializer=None,
            kind=ARG_NAMED_OPT,
        )

    def to_var(self) -> Var:
        return Var(self.name, self.type)

    def serialize(self) -> JsonDict:
        assert self.type
        return {
            "name": self.name,
            "feature_name": self.feature_name,
            "line": self.line,
            "column": self.column,
            "fullname": self.info.fullname,
            "type": self.type.serialize(),
        }

    @classmethod
    def deserialize(cls, info: TypeInfo, data: JsonDict, api: SemanticAnalyzerPluginInterface) -> "FeatureWrapper":
        data = data.copy()
        if data.get("kw_only") is None:
            data["kw_only"] = False
        typ = deserialize_and_fixup_type(data.pop("type"), api)
        return cls(type=typ, info=info, **data)


def _collect_field_args(expr: Expression, ctx: ClassDefContext) -> Tuple[bool, Dict[str, Expression]]:
    """Returns a tuple where the first value represents whether
    the expression is a call to feature and the second is a
    dictionary of the keyword arguments that feature() was called with.
    """
    if (
        isinstance(expr, CallExpr)
        and isinstance(expr.callee, RefExpr)
        and expr.callee.fullname in PluginKeywords.feature_makers
    ):
        # feature() only takes keyword arguments.
        args = {}
        for name, arg, kind in zip(expr.arg_names, expr.args, expr.arg_kinds):
            if not kind.is_named():
                if kind.is_named(star=True):
                    # This means that `field` is used with `**` unpacking,
                    # the best we can do for now is not to fail.
                    # TODO: we can infer what's inside `**` and try to collect it.
                    message = 'Unpacking **kwargs in "feature()" is not supported'
                else:
                    message = '"feature()" does not accept positional arguments'
                ctx.api.fail(message, expr)
                return True, {}
            assert name is not None
            args[name] = arg
        return True, args
    return False, {}


def collect_attributes(ctx: ClassDefContext) -> Optional[List[FeatureWrapper]]:
    """Collect all attributes declared in the dataclass and its parents.

    All assignments of the form

      a: SomeType
      b: SomeOtherType = ...

    are collected.
    """
    # First, collect attributes belonging to the current class.
    cls = ctx.cls
    attrs: List[FeatureWrapper] = []
    known_attrs: Set[str] = set()
    for stmt in cls.defs.body:
        # Any assignment that doesn't use the new type declaration
        # syntax can be ignored out of hand.
        if not (isinstance(stmt, AssignmentStmt) and stmt.new_syntax):
            continue

        # a: int, b: str = 1, 'foo' is not supported syntax so we
        # don't have to worry about it.
        lhs = stmt.lvalues[0]
        if not isinstance(lhs, NameExpr):
            continue

        sym = cls.info.names.get(lhs.name)
        if sym is None:
            # This name is likely blocked by a star import. We don't need to defer because
            # defer() is already called by mark_incomplete().
            continue

        node = sym.node
        if isinstance(node, PlaceholderNode):
            # This node is not ready yet.
            return None
        assert isinstance(node, Var)

        # x: ClassVar[int] is ignored by dataclasses.
        if not hasattr(node, "is_classvar"):
            continue
        if node.is_classvar:
            continue

        # has_field_call, field_args = _collect_field_args(stmt.rvalue, ctx)

        known_attrs.add(lhs.name)

        attrs.append(
            FeatureWrapper(
                name=lhs.name,
                feature_name=lhs.name,
                line=stmt.line,
                column=stmt.column,
                type=sym.type,
                info=cls.info,
            )
        )

    return attrs


def features_decorator_callback(ctx: ClassDefContext) -> None:
    info = ctx.cls.info
    attributes = collect_attributes(ctx)
    if attributes is None:
        # Some definitions are not ready, defer() should be already called.
        return
    for attr in attributes:
        if attr.type is None:
            ctx.api.defer()
            return

    if ("__init__" not in info.names or info.names["__init__"].plugin_generated) and attributes:
        args = [attr.to_argument() for attr in attributes]

        if info.fallback_to_any:
            # Make positional args optional since we don't know their order.
            # This will at least allow us to typecheck them if they are called
            # as kwargs
            for arg in args:
                if arg.kind == ARG_POS:
                    arg.kind = ARG_OPT

            # nameless_var = Var('')
            # args = [
            #    Argument(nameless_var, AnyType(TypeOfAny.explicit), None, ARG_STAR),
            #    *args,
            #    Argument(nameless_var, AnyType(TypeOfAny.explicit), None, ARG_STAR2),
            # ]

        add_method(
            ctx,
            "__init__",
            args=args,
            return_type=NoneType(),
        )

    for attr in attributes:
        class_name = attr.feature_name.replace(".", "__")
        class_def = ClassDef(class_name, Block([]))
        fullname = ctx.api.qualified_name(class_name)
        class_def.fullname = fullname

        attr_info = TypeInfo(SymbolTable(), class_def, ctx.api.cur_mod_id)
        class_def.info = attr_info
        attr_type_type = getattr(attr.type, "type", None)
        if attr_type_type is None:
            continue
        attr_info.mro = [attr_info, attr_type_type]
        # meta = ctx.api.named_type('chalk.features.FeatureComparisonMeta')
        # attr_info.declared_metaclass = meta
        attr.info = attr_info
        if getattrs(attr, "type.type.declared_metaclass.type.fullname") == PluginKeywords.dataframe_meta:
            PluginKeywords.set_dataframe_cols_metadata(
                obj=attr_info,
                cols=[
                    a.name if isinstance(a, UnboundType) else a.type.fullname for a in getattr(attr.type, "args", [])
                ],
            )

        # Guide here: https://github.com/python/mypy/blob/5bd2641ab53d4261b78a5f8f09c8d1e71ed3f14a/test-data/unit/plugins/dyn_class_from_method.py
        table_node = SymbolTableNode(kind=GDEF, node=attr_info, plugin_generated=True)
        ctx.api.add_symbol_table_node(attr.name, table_node)

    PluginKeywords.set_features_metadata(info, [attr.serialize() for attr in attributes])

    return None


def features_variadic_generic_callback(ctx: AnalyzeTypeContext) -> Type:
    args = ctx.type.args
    arg_types = [ctx.api.analyze_type(arg) for arg in args]
    if len(arg_types) == 1:
        return arg_types[0]

    if len(arg_types) == 0:
        return ctx.type

    return ctx.api.named_type(
        PluginKeywords.get_feature_class_fullname(len(arg_types)),
        sorted(arg_types, key=lambda x: x.type.name if hasattr(x, "type") else ""),
    )


def init_features_callback(ctx: FunctionContext) -> Type:
    return_type = ctx.default_return_type.type

    kwarg_names = [arg[0] for arg in ctx.arg_names if isinstance(arg, list) and len(arg) == 1]

    symbol_table_params = sorted([return_type.names.get(k) for k in kwarg_names], key=lambda x: x.fullname)

    if len(symbol_table_params) == 1:
        return Instance(symbol_table_params[0].node, args=[])

    if len(kwarg_names) == 0:
        return ctx.default_return_type

    feature_wrapper = lookup_fully_qualified(
        name=PluginKeywords.get_feature_class_fullname(len(kwarg_names)),
        modules=ctx.api.modules,
    )

    args = []
    for tp in symbol_table_params:
        node = tp.node
        if isinstance(tp.node, Var):
            node = node.info
        if isinstance(node, TypeInfo):
            s = Instance(node, args=[])
            args.append(s)

    return Instance(
        typ=feature_wrapper.node,
        args=args,
    )


def add_attributes_to_dataframe(ctx: AnalyzeTypeContext) -> Type:
    args = ctx.type.args
    arg_types = [ctx.api.analyze_type(arg) for arg in args]

    override_types = []
    for a in arg_types:
        features = PluginKeywords.get_features_from_metadata(getattrs(a, "type.metadata") or {})
        if len(features) > 0:
            for f in features:
                override_types.append(UnboundType(f["fullname"]))

    if len(override_types) > 0:
        return ctx.api.named_type(
            PluginKeywords.get_dataframe_class_fullname(len(override_types)),
            sorted(override_types, key=lambda x: x.name),
        )

    if len(args) > 0:
        return ctx.api.named_type(
            PluginKeywords.get_dataframe_class_fullname(len(arg_types)),
            sorted(arg_types, key=lambda x: getattrs(x, "type.name") or ""),
        )

    return ctx.type


def narrow_dataframe_maker(
    parent_members_fullnames: List[str],
) -> Callable[[AnalyzeTypeContext], Type]:
    def dataframe_callback(ctx: AnalyzeTypeContext) -> Type:
        args = [a for a in ctx.type.args if getattrs(a, "base_type_name") != "typing.Any"]
        filtered_members = [ctx.api.analyze_type(arg) for arg in args]
        filtered_members_not_in_parent = set([f.type.fullname for f in filtered_members]) - set(
            parent_members_fullnames
        )

        def format_name(names: List[str]):
            return ", ".join(sorted([".".join([a for a in n.split(".") if a][-2:]) for n in names]))

        if len(filtered_members_not_in_parent) > 0:
            ctx.api.fail(
                f"""Could not narrow DataFrame. Missing {format_name(list(filtered_members_not_in_parent))}
Parent:         {format_name(parent_members_fullnames)}
Child:          {format_name([f.type.fullname for f in filtered_members])}
Child - Parent: {format_name(list(filtered_members_not_in_parent))}""",
                ctx.type,
            )

        if len(filtered_members) == 0:
            return ctx.type

        named_type = ctx.api.named_type(
            PluginKeywords.get_dataframe_class_fullname(len(filtered_members)),
            sorted(filtered_members, key=lambda x: x.type.fullname),
        )

        return named_type

    return dataframe_callback


def getattrs(obj: Any, path: str):
    current = obj
    for p in path.split("."):
        current = getattr(current, p, None)
    return current


class ChalkPlugin(Plugin):
    def get_type_analyze_hook(self, fullname: str) -> Optional[Callable[[AnalyzeTypeContext], Type]]:
        if PluginKeywords.features_class == fullname:
            return features_variadic_generic_callback

        if PluginKeywords.dataframe_class == fullname:
            return add_attributes_to_dataframe

        if PluginKeywords.fullname_is_dataframe_class(fullname):
            return add_attributes_to_dataframe

        # The property we're accessing is a dataframe
        fully_qualified = self.lookup_fully_qualified(fullname)

        if fully_qualified is not None:
            dataclass_type_params = PluginKeywords.get_dataframe_cols_from_metadata(
                getattrs(fully_qualified, "node.metadata") or {}
            )
            if len(dataclass_type_params) > 0:
                return narrow_dataframe_maker(dataclass_type_params)

        return None

    def get_method_hook(self, fullname: str) -> Optional[Callable[[MethodContext], Type]]:
        if fullname.startswith("chalk.sql.integrations") and fullname.endswith("query"):
            # TODO: Support chalk query
            return None
        return None

    def get_dynamic_class_hook(self, fullname: str) -> Optional[Callable[[DynamicClassDefContext], None]]:
        return None

    def get_function_hook(self, fullname: str) -> Optional[Callable[[FunctionContext], Type]]:
        fully_qualified = self.lookup_fully_qualified(fullname)
        node_metadata = (getattrs(fully_qualified, "node.metadata") or {}).get("features", {}).get("attributes")

        if node_metadata is not None:
            return init_features_callback

        return None

    def get_class_decorator_hook(self, fullname: str) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname in PluginKeywords.feature_set_decorators:
            return features_decorator_callback

        return None

    def get_additional_deps(self, file: MypyFile) -> list[tuple[int, str, int]]:
        fullname = file.fullname
        assert isinstance(fullname, str)
        if fullname.startswith("chalk.features"):
            return [(10, f"chalk.feature_n.feature_{str(n)}.feature", -1) for n in range(1, 257)]
        return []


def plugin(version: str):
    return ChalkPlugin
