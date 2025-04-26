from __future__ import annotations

import sys
import types
import typing
from datetime import timedelta
from typing import TYPE_CHECKING, Any, Dict, FrozenSet, List, Optional, Set, Tuple, Type, TypeVar, Union, cast

from typing_extensions import Annotated, get_args, get_origin

from chalk._lsp.error_builder import LSPErrorBuilder
from chalk.features._encoding.http import HttpResponse
from chalk.utils.cached_type_hints import cached_get_type_hints
from chalk.utils.collections import is_optional
from chalk.utils.import_utils import import_only_type_checking_imports
from chalk.utils.json import JSON
from chalk.utils.log_with_context import get_logger

if TYPE_CHECKING:
    from google.protobuf.message import Message as ProtobufMessage

    from chalk import Document, Windowed
    from chalk.features import DataFrame, Feature, Features, Vector
    from chalk.streams import Windowed

_logger = get_logger(__name__)

T = TypeVar("T")
U = TypeVar("U")
JsonValue = TypeVar("JsonValue")


class ParsedAnnotation:
    __slots__ = (
        "_features_cls",
        "_attribute_name",
        "_is_nullable",
        "_is_feature_time",
        "_is_primary",
        "_is_document",
        "_underlying",
        "_unparsed_underlying",
        "_parsed_annotation",
        "_as_proto",
        "_as_document",
        "_as_features_cls",
        "_as_dataframe",
        "_as_vector",
        "_as_feature",
    )

    def __init__(
        self,
        features_cls: Optional[Type[Features]] = None,
        attribute_name: Optional[str] = None,
        *,
        underlying: Optional[Union[type, Annotated, Windowed]] = None,
    ) -> None:
        super().__init__()
        # Either pass in the underlying -- if it is already parsed -- or pass in the feature cls and attribute name
        self._features_cls = features_cls
        self._attribute_name = attribute_name
        self._is_nullable = False
        self._is_feature_time = False
        self._is_primary = False
        self._is_document = False
        self._underlying: Optional[Union[type, Feature]] = None
        self._unparsed_underlying = underlying
        self._parsed_annotation: Optional[type] = None
        if underlying is not None:
            if features_cls is not None and attribute_name is not None:
                raise ValueError("If specifying the underlying, do not specify (features_cls, attribute_name)")
        elif features_cls is None or attribute_name is None:
            raise ValueError(
                "If not specifying the underlying, then both the (features_cls, attribute_name) must be provided"
            )
        # Store the class and attribute name to later use typing.get_type_hints to
        # resolve any forward references in the type annotations
        # Resolution happens lazily -- after everything is imported -- to avoid circular imports

        # Caching some properties for faster lookup
        self._as_proto: Optional[Type[ProtobufMessage]] = None
        self._as_document: Optional[Type[Document]] = None
        self._as_features_cls: Optional[Type[Features]] = None
        self._as_dataframe: Optional[Type[DataFrame]] = None
        self._as_vector: Optional[Type[Vector]] = None
        self._as_feature: Optional[Feature] = None

    @property
    def parsed_annotation(self) -> type:
        """The parsed type annotation. It will be parsed if needed.

        Unlike `.underlying`, parsed annotation contains any container or optional types, such as
        list, dataframe, or Optional.
        """
        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._parsed_annotation is not None
        return self._parsed_annotation

    def __str__(self):
        if self._features_cls is not None and self._attribute_name is not None:
            typ = self._features_cls.__annotations__[self._attribute_name]
        else:
            typ = self._parsed_annotation or self._underlying or self._unparsed_underlying
        if sys.version_info >= (3, 9) and get_origin(typ) == typing.Annotated:
            typ = typ.__origin__  # pyright: ignore
        if isinstance(typ, type):
            typ = typ.__name__
        return str(typ)

    def _get_globals_for_forward_references(self) -> Dict[str, Any]:
        """
        If we're loading pickles from a notebook onto the branch server OR if we are loading forward references
        from separate files, we need special handling for forward references.
        """

        import typing

        import chalk
        from chalk.features import FeatureSetBase

        feature_classes = {feature_set.__name__: feature_set for feature_set in FeatureSetBase.registry.values()}

        if not getattr(self._features_cls, "__chalk_is_loaded_from_notebook__", False):
            return feature_classes

        return {
            # Support "typing.Optional[...]", "Optional[...]", etc."
            "typing": typing,
            **typing.__dict__,
            # Support "chalk.DataFrame[...]", "DataFrame[...]"
            "chalk": chalk,
            **chalk.__dict__,
            # Support forward references for cyclic has-one/has-many's
            **feature_classes,
        }

    def _parse_annotation(self):
        if self._unparsed_underlying is None:
            assert self._attribute_name is not None
            assert self._features_cls is not None
            try:
                # First, try to get the type hints without doing anything fancy
                # Everything should already be imported properly
                hints = cached_get_type_hints(self._features_cls, include_extras=True)
            except:
                # If there was an issue with that, then we'll fallback to trying to augment the globals, automatically injecting
                # feature sets and chalkpy imports under their respective names
                module = sys.modules.get(self._features_cls.__module__, None)
                existing_globalns = {}
                if module is not None:
                    existing_globalns.update(getattr(module, "__dict__", {}))
                existing_globalns.update(self._get_globals_for_forward_references())
                try:
                    hints = cached_get_type_hints(
                        self._features_cls,
                        include_extras=True,
                        globalns=existing_globalns if len(existing_globalns) > 0 else None,
                    )
                except:
                    # If there was an issue with THAT, we'll try to import files specified by
                    # TYPE_CHECKING only imports, and augment the globals again
                    if self._features_cls.__chalk_source_info__.filename is not None:
                        import_only_type_checking_imports(self._features_cls.__chalk_source_info__.filename)
                    existing_globalns.update(self._get_globals_for_forward_references())
                    try:
                        hints = cached_get_type_hints(
                            self._features_cls,
                            include_extras=True,
                            globalns=existing_globalns if len(existing_globalns) > 0 else None,
                        )
                    except:
                        # Last shot, in a notebook context, we may not have access to annotation types
                        import datetime as dt
                        from typing import Optional

                        from chalk import Windowed
                        from chalk.features import DataFrame, FeatureTime, Primary

                        existing_globalns.update(
                            {
                                "Optional": Optional,
                                "DataFrame": DataFrame,
                                "Primary": Primary,
                                "FeatureTime": FeatureTime,
                                "dt": dt,
                                "Windowed": Windowed,
                            }
                        )
                        try:
                            hints = cached_get_type_hints(
                                self._features_cls,
                                include_extras=True,
                                globalns=existing_globalns if len(existing_globalns) > 0 else None,
                            )
                        except Exception as e:
                            raise TypeError(
                                f"Could not get type hints of feature class '{self._features_cls}' from filename {self._features_cls.__chalk_source_info__.filename}: {str(e)}"
                            ) from e

            parsed_annotation = hints[self._attribute_name]
        else:
            parsed_annotation = self._unparsed_underlying

        try:
            self._parse_type(parsed_annotation)
        except Exception as e:
            if (
                # This is our catch-all, which we only want to run if someone else didn't already report an error.
                not LSPErrorBuilder.has_errors()
                and self._features_cls is not None
                and self._features_cls.__chalk_error_builder__
                is not None  # pyright: ignore[reportUnnecessaryComparison]
            ):
                try:
                    self._type_error(message=e.args[0], code="79")
                except:
                    pass
            raise e

    def _type_error(
        self,
        message: str,
        code: str,
        label: str = "invalid annotation",
        code_href: Optional[str] = "https://docs.chalk.ai/docs/feature-types",
    ):
        builder = self._features_cls and self._features_cls.__chalk_error_builder__
        if builder is not None:
            builder.add_diagnostic(
                message=message,
                label=label,
                code=code,
                code_href=code_href,
                range=(builder.annotation_range(self._attribute_name) or builder.property_range(self._attribute_name))
                if self._attribute_name
                else builder.class_definition_range(),
            )
        raise TypeError(message)

    def _parse_type(self, annotation: Union[type, Windowed, Annotated]):
        from chalk.features._vector import Vector
        from chalk.features.dataframe import DataFrame
        from chalk.features.feature_field import Feature
        from chalk.features.feature_set import Features
        from chalk.features.feature_wrapper import FeatureWrapper, unwrap_feature
        from chalk.streams import Windowed

        try:
            from google.protobuf.message import Message as ProtobufMessage
        except ImportError:
            ProtobufMessage = None

        # assert self._parsed_annotation is None, "The annotation was already parsed"
        if isinstance(annotation, Windowed):
            # If it's windowed, then unwrap it immediately, because Windowed annotations are really just a proxy to the underlying type
            annotation = annotation.kind
        self._parsed_annotation = cast(type, annotation)
        self._is_nullable = False
        self._is_primary = False
        self._is_feature_time = False
        if self._features_cls is not None and self._attribute_name is not None:
            # Return a more helpful error message, since we have context
            error_ctx = f"{self._features_cls.__name__}.{self._attribute_name}"
        else:
            error_ctx = ""
        origin = get_origin(annotation)

        if annotation is JSON:
            self._is_nullable = True
        elif origin in (
            Union,
            getattr(types, "UnionType", Union),
        ):  # using getattr as UnionType was introduced in python 3.10
            args = get_args(annotation)
            # If it's a union, then the only supported union is for nullable features. Validate this
            if len(args) != 2 or (None not in args and type(None) not in args):
                self._type_error(
                    f"Invalid annotation for feature {error_ctx}: Unions with non-None types are not allowed.",
                    code="71",
                    label="invalid annotation",
                )

            annotation = args[0] if args[1] in (None, type(None)) else args[1]
            if isinstance(annotation, type) and issubclass(annotation, DataFrame):
                self._type_error(
                    (
                        f"Invalid type annotation for feature '{error_ctx}': "
                        f"'{annotation}' refers to an Optional DataFrame. "
                        "Since DataFrames can be empty, the Optional is unnecessary. "
                        "Please refer to your DataFrame as a non-optional type, e.g. `DataFrame[FeatureClassB]`."
                    ),
                    code="78",
                    label="invalid annotation",
                )
                return
            origin = get_origin(annotation)
            self._is_nullable = True

        if origin in (Annotated, getattr(typing, "Annotated", Annotated)):
            args = get_args(annotation)
            annotation = args[0]
            if "__chalk_ts__" in args:
                self._is_feature_time = True
            if "__chalk_primary__" in args:
                self._is_primary = True
            if "__chalk_document__" in args:
                self._is_document = True
            origin = get_origin(annotation)

        # The only allowed collections here are Set, List, or DataFrame
        if origin in (set, Set):
            args = get_args(annotation)
            if len(args) != 1:
                self._type_error(
                    f"Set takes exactly one arg, but found {len(args)} type parameters",
                    code="72",
                    label="invalid set",
                )
            annotation = args[0]
        if origin in (frozenset, FrozenSet):
            args = get_args(annotation)
            if len(args) != 1:
                self._type_error(
                    f"FrozenSet takes exactly one arg, but found {len(args)} type parameters",
                    code="73",
                    label="invalid frozen set",
                )
            annotation = args[0]
        if origin in (tuple, Tuple):
            args = get_args(annotation)
            if len(args) != 2 or args[1] is not ... or args[0] is ...:
                self._type_error(
                    (
                        "Tuple should be given exactly two type parameters. "
                        "The first should be the type of the elements, and the second should be '...', "
                        "which indicates that the tuple is of variable length. "
                        "For example, 'Tuple[int, ...]' is a tuple of ints of variable length."
                    ),
                    code="74",
                    label="invalid tuple",
                )
            annotation = args[0]
        if origin in (list, List):
            args = get_args(annotation)
            if len(args) != 1:
                self._type_error(
                    f"List takes exactly one arg, but found {len(args)} type parameters",
                    code="75",
                    label="invalid list",
                )
            annotation = args[0]

        if origin in (dict, Dict):
            args = get_args(annotation)
            if len(args) != 2:
                self._type_error(
                    f"Dict takes exactly two args, but found `{Dict[args]}`",  # pyright: ignore
                    code="156",
                    label="invalid dict",
                )
            if is_optional(args[0]):
                self._type_error(
                    f"Dict keys cannot be optional types, found `{Dict[args]}`",  # pyright: ignore
                    code="157",
                    label="optional dict key not allowed",
                )
            if args[1] in (Any, object) or (get_origin(args[1]) == Union and not is_optional(args[1])):
                self._type_error(
                    f"Only homogeneous dicts supported, found `{Dict[args]}`",  # pyright: ignore
                    code="158",
                    label="`Any` as dict value type not allowed",
                )

            annotation = dict

        if isinstance(annotation, FeatureWrapper):
            # We never want FeatureWrappers; if this is the case, then unwrap it to the underlying feature
            annotation = unwrap_feature(annotation)

        if not isinstance(annotation, (type, Feature)) and annotation not in (
            JSON,
            HttpResponse[str],
            HttpResponse[bytes],
        ):
            if isinstance(annotation, str):
                self._type_error(
                    (
                        f"Invalid type annotation for feature '{error_ctx}': "
                        f"{self._parsed_annotation} seems to be an incorrectly formatted forward reference. "
                        f"Forward references must be surrounded by quotes, e.g. '\"list[object]\"', "
                        f"not 'list[\"object\"]'. "
                    ),
                    code="76",
                    label="invalid reference",
                )

            elif origin in (set, Set, frozenset, FrozenSet, list, List, tuple, Tuple):
                origin = cast(type, origin)
                self._type_error(
                    (
                        f"Invalid type annotation for feature '{error_ctx}': "
                        f"{origin.__name__} must be of scalar types, "
                        f"not {self._parsed_annotation}"
                    ),
                    code="77",
                    label="invalid generic",
                )

            else:
                self._type_error(
                    (
                        f"Invalid type annotation for feature '{error_ctx}': "
                        f"'{self._parsed_annotation}' does not reference a Python type, Chalk feature, "
                        "or a type annotation."
                    ),
                    code="78",
                    label="invalid annotation",
                )
            return

        self._underlying = annotation  # pyright: ignore[reportAttributeAccessIssue]
        if isinstance(self._underlying, type):
            if ProtobufMessage is not None and issubclass(self._underlying, ProtobufMessage):
                self._as_proto = self._underlying

            elif issubclass(self._underlying, Features):
                self._as_features_cls = self._underlying

            elif issubclass(self._underlying, DataFrame):
                if len(self._underlying.columns) == 0:
                    self._type_error(
                        (
                            f"Invalid type annotation for feature '{error_ctx}': "
                            f"'{self._parsed_annotation}' does not reference a Chalk feature class. "
                            "Please add your feature class to the type, e.g. `DataFrame[FeatureClassB]`. "
                        ),
                        code="78",
                        label="invalid annotation",
                    )
                    return
                if self._features_cls is not None and self._underlying.namespace == self._features_cls.namespace:
                    self._type_error(
                        (
                            f"Invalid type annotation for feature '{error_ctx}': "
                            f"'{self._parsed_annotation}' is a DataFrame that refers to its own feature class. "
                            "This is unsupported."
                        ),
                        code="78",
                        label="invalid annotation",
                    )
                    return

                self._as_dataframe = self._underlying

            elif issubclass(self._underlying, Vector):
                self._as_vector = self._underlying

            elif issubclass(self._underlying, timedelta):
                self._type_error(
                    (f"Invalid type annotation for feature '{error_ctx}': timedelta feature types are not supported."),
                    code="78",
                    label="invalid annotation",
                )
                return

        elif isinstance(self._underlying, Feature):
            self._as_feature = self._underlying

    def as_proto(self) -> Optional[Type[ProtobufMessage]]:
        if self._parsed_annotation is None:
            self._parse_annotation()
        return self._as_proto

    def as_document(self) -> Optional[Type[Document]]:
        if self._parsed_annotation is None:
            self._parse_annotation()
        if not self._is_document:
            return None
        return cast("Type[Document]", self._underlying)

    @property
    def is_nullable(self) -> bool:
        """Whether the type annotation is nullable."""
        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._is_nullable is not None
        return self._is_nullable

    def as_features_cls(self) -> Optional[Type[Features]]:
        if self._parsed_annotation is None:
            self._parse_annotation()
        return self._as_features_cls

    def as_dataframe(self) -> Optional[Type[DataFrame]]:
        if self._parsed_annotation is None:
            self._parse_annotation()
        return self._as_dataframe

    def as_vector(self) -> Optional[Type[Vector]]:
        if self._parsed_annotation is None:
            self._parse_annotation()
        return self._as_vector

    def as_feature(self) -> Optional[Feature]:
        if self._parsed_annotation is None:
            self._parse_annotation()
        return self._as_feature

    def is_primary(self) -> bool:
        if self._parsed_annotation is None:
            self._parse_annotation()
        return self._is_primary

    def is_feature_time(self) -> bool:
        if self._parsed_annotation is None:
            self._parse_annotation()
        return self._is_feature_time
