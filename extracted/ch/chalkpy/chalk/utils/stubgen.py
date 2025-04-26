import argparse
import os
import pathlib
import typing
import warnings
from collections import defaultdict
from typing import Any, Dict, List, NamedTuple, Optional, Tuple, Type, Union, cast

from typing_extensions import Annotated, get_args, get_origin

from chalk.features import Feature, Features, FeatureSetBase, Vector, FeatureWrapper, unwrap_feature
from chalk.importer import import_all_python_files_from_dir
from chalk.utils.paths import get_directory_root

try:
    from types import UnionType
except ImportError:
    UnionType = None


class ParsedAnnotation(NamedTuple):
    annotation: str
    include_in_protocol_cls: bool
    protocol_annotation: str


class ParsedFeaturesClass(NamedTuple):
    module: str
    annotations: Dict[str, ParsedAnnotation]


class StubGenerator:
    def __init__(self) -> None:
        super().__init__()
        self._parsed_feature_classes: Dict[str, ParsedFeaturesClass] = {}
        self._module_to_stubs: List[Type[Features]] = []
        self._imports: Dict[Tuple[str, ...], str] = {}  # Mapping of full module name to the name it is imported as

    def _add_import(
        self,
        item: Union[str, type, typing._SpecialForm],  # pyright: ignore[reportPrivateUsage]
        import_as: Optional[str] = None,
    ) -> str:
        """Add an import for item.

        If `item` is already imported, then it will not be imported again.
        Its existing import name will be returned

        Parameters
        ----------
        item
            The thing to import. Should be the full path to the item (e.g. `typing.Optional`)

        Returns
        -------
        str
            The name that `item` will be imported as.
        """
        if isinstance(item, typing._SpecialForm):  # pyright: ignore[reportPrivateUsage]
            item = str(item)
        if isinstance(item, FeatureWrapper):
            item = unwrap_feature(item).fqn
        if isinstance(item, type):
            item = f"{item.__module__}.{item.__name__}"
        if not isinstance(item, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(f"Invalid type for {item}: {type(item)}")
        item_split = tuple(item.split("."))
        if item_split[0] == "builtins":
            assert len(item_split) == 2
            return item_split[1]
        if item_split in self._imports:
            imported_name = self._imports[item_split]
            if import_as is not None and import_as != imported_name:
                raise ValueError(
                    f"Item {'.'.join(item_split)} already imported as {imported_name}; cannot be imported again as {import_as}"
                )
            return imported_name
        if import_as is None:
            import_as = self._get_import_name(item_split)
        self._imports[item_split] = import_as
        return self._imports[item_split]

    def _get_import_name(self, item_split: Tuple[str, ...]):
        if item_split[0] in ("typing", "typing_extensions"):
            assert len(item_split) == 2
            return item_split[1]
        item_split = tuple(x.replace("_", "__") for x in item_split)
        item = f"__stubgen_{'_'.join(item_split)}"
        return item

    def _register_imports_for_annotation(self, annotation: Any) -> Tuple[str, str]:
        """Register all necessary imports, and return a tuple of (protocol annotation, init annotation)"""
        if annotation == type(None):
            return "None", "None"
        if annotation is ...:
            return "...", "..."
        origin, args = get_origin(annotation), get_args(annotation)
        if origin is None:
            assert args == ()
            if isinstance(annotation, type) and issubclass(
                annotation, Vector
            ):  # pyright: ignore[reportUnnecessaryIsInstance]
                origin_name = self._add_import(Vector, import_as="Vector")
                return "Vector", "Vector"
            elif annotation.__module__ == "builtins":
                assert isinstance(annotation, type)
                return annotation.__name__, annotation.__name__
            else:
                ans = self._add_import(annotation)
                return ans, ans
        # Some sort of generic class, like a collection, or optional
        if origin == UnionType:
            # Convert new-style type unions to old-style typing.Unions
            origin = typing.Union
        if origin == Annotated:
            # If annotated, only pay attention to the first arg -- the actual type
            if args[1] == "__chalk_primary__":
                protocol_arg_name, init_arg_name = self._register_imports_for_annotation(args[0])
                return f"Primary[{protocol_arg_name}]", init_arg_name
            return self._register_imports_for_annotation(args[0])
        origin_name = self._add_import(cast(Any, origin))
        arg_names = [self._register_imports_for_annotation(arg) for arg in args]
        return (
            f"{origin_name}[" + ", ".join(x[0] for x in arg_names) + "]",
            f"{origin_name}[" + ", ".join(x[1] for x in arg_names) + "]",
        )

    def register_features_class(self, features_cls: Type[Features]):
        annotations: Dict[str, ParsedAnnotation] = {}
        for f in features_cls.features:
            assert isinstance(f, Feature)
            assert f.typ is not None
            if f.typ.as_dataframe() is not None:
                self._add_import("chalk.features.DataFrame", "DataFrame")
                annotations[f.attribute_name] = ParsedAnnotation(
                    "DataFrame",
                    include_in_protocol_cls=True,
                    protocol_annotation="DataFrame",
                )
            else:
                # Make a best-effort to figure out imports.
                proto_annotation, init_annotation = self._register_imports_for_annotation(f.typ.parsed_annotation)
                include_in_proto_cls = not f.is_windowed_pseudofeature and not f.is_autogenerated
                if include_in_proto_cls:
                    protocol_annotation = proto_annotation
                    if f.typ.as_features_cls() is not None:
                        protocol_annotation = "Any"
                    else:
                        as_feature = f.typ.as_feature()
                        if as_feature is not None:
                            protocol_annotation, init_annotation = self._register_imports_for_annotation(
                                as_feature.typ.parsed_annotation
                            )
                    annotations[f.attribute_name] = ParsedAnnotation(
                        init_annotation,
                        include_in_protocol_cls=include_in_proto_cls,
                        # If it's a features class (i.e. a has-one), not specifying
                        # the type in the protocol class so the type checker can
                        # still match feature classes that have a circular reference
                        protocol_annotation="Any" if (f.typ.as_features_cls() is not None) else protocol_annotation,
                    )
        name = features_cls.__chalk_namespace__.replace("::", "_")
        name_parts = name.split("_")
        name = "".join(x.title() for x in name_parts)
        if name in self._parsed_feature_classes:
            # We could have duplicates because of namespacing. That is fine because we do protocol matching so the actual name doesn't matter
            raise ValueError(
                f"Unable to generate stubs due to multiple features sets named '{features_cls.__chalk_namespace__}'. Feature set names must be unique. Please rename one of these feature sets."
            )
        self._parsed_feature_classes[name] = ParsedFeaturesClass(
            module=features_cls.__module__,
            annotations=annotations,
        )

    def generate_features_decorator_stub_file(self):
        self._add_import("typing.Optional", "Optional")
        self._add_import("typing.Any", "Any")
        self._add_import("typing.Protocol", "Protocol")
        self._add_import("typing.Type", "Type")
        self._add_import("typing.overload", "overload")
        self._add_import("typing.Iterator", "Iterator")
        self._add_import("chalk.features.feature_set.FeaturesMeta", "FeaturesMeta")
        self._add_import("chalk.features.Features", "Features")
        self._add_import("chalk.features.Feature", "Feature")
        self._add_import("chalk.features.primary.Primary", "Primary")
        self._add_import("chalk.utils.duration.Duration", "Duration")
        self._add_import("chalk.features.Tags", "Tags")
        lines = [
            "# AUTO-GENERATED FILE. Do not edit. Run `chalk stubgen` to generate.",
            "# fmt: off",
            "# isort: skip_file",
            "from __future__ import annotations",
            "",
        ]
        # sort the imports for consistency
        imports = sorted(self._imports.items())
        for imp, import_as in imports:
            module = imp[:-1]
            name = imp[-1]
            lines.append(f"from {'.'.join(module)} import {name} as {import_as}")
        lines.append("")

        # The overall strategy is to create 3 stub classes for each features class.
        #
        # In no particular order:
        #
        # Class 1: The metaclass. The metaclass includes @property descriptors for each class variable.
        # These descriptors are used to annotation class attributes as Type[feature]
        # Pyright requires that all annotations are types, not instances.
        #
        # Class 2: The class. The class includes an __init__ signature that includes all features, with the
        # correct type annotation. All features have a default value of `...`, since Chalk does not require feature
        # sets to be complete. Inside the __init__ body, all instance attributes are annotated. Placing the annotation
        # here, as opposed to the class body, does not conflict with the metaclass annotations
        #
        # Class 3: The protocol class. Since the @features decorator is passed the end user's class definition, and returns the
        # Chalk-ified version of it, we cannot "import" the user's class definition. So, we define a protocol class that contains the
        # same instance attributes. The type checker can match the user's class against the protocol.

        # Since we effectively duck type with Protocols, different feature sets with all the same attributes
        # and types cannot be distinguished
        # So, we will keep just one feature set for a given set of attributes and annotations
        attributes_and_annotations_to_feature_set_names: dict[frozenset[tuple[str, str]], list[str]] = defaultdict(list)
        for x_name, x in self._parsed_feature_classes.items():
            attributes_and_annotations_to_feature_set_names[
                frozenset((k, v.protocol_annotation) for (k, v) in x.annotations.items())
            ].append(x_name)
        feature_set_names_to_keep: set[str] = set()
        for feature_set_names in attributes_and_annotations_to_feature_set_names.values():
            # Sorting for stability
            feature_set_names_to_keep.add(sorted(feature_set_names)[0])
        self._parsed_feature_classes = {
            k: v for (k, v) in self._parsed_feature_classes.items() if k in feature_set_names_to_keep
        }

        # Update the base classes
        # Feature sets that are supersets of other feature classes must inherit from the base classes, due to how
        # @overload requires return and parameter types of the less specific classes to be supertypes
        parsed_features_class_name_to_bases: dict[str, list[str]] = {}
        for x_name, x in self._parsed_feature_classes.items():
            common_base_class_names: set[str] = set()
            for y_name, y in self._parsed_feature_classes.items():
                if x is not y:
                    if all(
                        x.annotations.get(attribute_name) == annotation
                        for attribute_name, annotation in y.annotations.items()
                    ):
                        # If all of y's annotations are a subset of x's, it's a possible base class
                        common_base_class_names.add(y_name)
            # Sorting the base classes in reverse order so the most specific will go first
            common_base_classes_sorted = sorted(
                common_base_class_names,
                key=lambda y_name: (len(self._parsed_feature_classes[y_name].annotations), y_name),
                reverse=True,
            )
            parsed_features_class_name_to_bases[x_name] = [*common_base_classes_sorted, "Features"]

        # An @overload is used to match each protocol class (class #3) to the typestub version of the class (class #2)
        # First, define all metaclasses, then the classes, then the protocols, most general to most specific
        # However, when defining the @overloads, go from most specific to most general, since the first matching @overload
        # is used
        # Also including the class name as part of the sort key for stability
        parsed_feature_classes = sorted(
            self._parsed_feature_classes.items(),
            key=lambda x: (len(x[1].annotations), x[0]),
        )

        for feature_cls_name, features_cls in parsed_feature_classes:
            # First generate the metaclass definition
            metaclasses_bases = ", ".join(
                (*(f"{base_class}Meta" for base_class in parsed_features_class_name_to_bases[feature_cls_name]), "type")
            )
            lines.append(
                f"""\
class {feature_cls_name}Meta({metaclasses_bases}):"""
            )
            for attribute, annotation in features_cls.annotations.items():
                lines.append(
                    f"""\
    @property
    def {attribute}(self) -> Type[{annotation.annotation}]: ...
"""
                )
            if len(features_cls.annotations) == 0:
                lines.append(
                    f"""\
    ...
"""
                )
            lines.append(
                f"""\
    def __iter__(self) -> Iterator[Feature]: ...
"""
            )

        for feature_cls_name, features_cls in parsed_feature_classes:
            # Next, generate the class definition
            bases = ", ".join(parsed_features_class_name_to_bases[feature_cls_name])
            lines.append(
                f"""\
class {feature_cls_name}({bases}, metaclass={feature_cls_name}Meta):"""
            )
            lines.append(
                f"""\
    def __init__(
        self,"""
            )
            for attribute, annotation in features_cls.annotations.items():
                lines.append(
                    f"""\
        {attribute}: {annotation.annotation} = ...,"""
                )
            lines.append(
                """\
    ):"""
            )
            for attribute, annotation in features_cls.annotations.items():
                lines.append(
                    f"""\
        self.{attribute}: {annotation.annotation}"""
                )
            if len(features_cls.annotations) == 0:
                lines.append(
                    f"""\
        ..."""
                )
            lines.append("")
        for feature_cls_name, features_cls in parsed_feature_classes:
            # Finally, generate the protocol class representing the features class that is being transformed
            lines.append(
                f"""\
class {feature_cls_name}Protocol(Protocol):"""
            )
            has_proto_annotation = False
            for attribute, annotation in features_cls.annotations.items():
                if not annotation.include_in_protocol_cls:
                    continue
                has_proto_annotation = True
                lines.append(
                    f"""\
    {attribute}: {annotation.protocol_annotation}"""
                )
            if not has_proto_annotation:
                lines.append(
                    f"""\
    ..."""
                )
            lines.append("")

        # Add overloads to the @features decorator to hint that it returns
        # instances of the classes defined above, not the classes defined in the user's module
        # This allows us to put all type stubs in one file, under the chalk/features/feature namespace,
        # rather than having to create a type stub for each user's feature class.
        proto_sorted_feature_classes = sorted(
            self._parsed_feature_classes.items(),
            key=lambda x: (
                sum(1 for annotation in x[1].annotations.values() if annotation.include_in_protocol_cls),
                x[0],
            ),
            reverse=True,
        )
        for features_cls_name, features_cls in proto_sorted_feature_classes:
            # For each features class, adding two overloads. The first overload transforms the definition
            # from the user's code into our stub. However, since we are technically importing the version that
            # has already been transformed with @features, we need to annotate how to handle a class that
            # has already been processed -- hence the second definition which is effectively a no-op.
            lines.append(
                f"""\
@overload
def features(item: Type[{features_cls_name}Protocol]) -> Type[{features_cls_name}]: ...
"""
            )

        # We also need to handle when the user annotates the features class with args, such as an owner or tags, e.g.
        # @features(owner=...)
        # class MyFeaturesClass:
        #     ...
        # To do this, we add one additional overload for features that returns a protocol class.
        # This protocol class implements __call__ with overloads, similar to the above
        lines.append(
            """\
@overload
def features(
    *,
    owner: Optional[str] = None,
    tags: Optional[Tags] = None,
    etl_offline_to_online: bool = ...,
    max_staleness: Optional[Duration] = ...,
    name: Optional[str] = None,
) -> __stubgen__features_proto: ...

class __stubgen__features_proto(Protocol):"""
        )
        for features_cls_name, features_cls in proto_sorted_feature_classes:
            overload = (
                "@overload" if len(parsed_feature_classes) > 1 else ""
            )  # It is incorrect to use @overload if there is just one definition
            lines.append(
                f"""\
    {overload}
    def __call__(self, item: Type[{features_cls_name}Protocol]) -> Type[{features_cls_name}]: ...
"""
            )
        if len(parsed_feature_classes) == 0:
            lines.append(
                """\
    ...
"""
            )
        return lines


def configure_stubgen_argparse(parser: argparse.ArgumentParser):
    parser.add_argument("--file_filter", help="Path containing only files to consider", nargs="?")
    parser.add_argument(
        "--root",
        type=str,
        default=None,
        help="Project root to scan for features definitions. By default, will find the directory root.",
    )
    parser.add_argument(
        "--stub_path",
        "-s",
        type=str,
        default=None,
        help="Folder containing custom type stubs. By default, will use the `typings` folder, relative to the project root",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        default=False,
        help="Whether to print verbose error messages when stubgen fail",
    )


def run_stubgen(
    args: argparse.Namespace,
    file_filter: Optional[str],
):
    root = args.root
    if root is None:
        root = get_directory_root() or pathlib.Path(os.getcwd())
    else:
        assert isinstance(root, str)
        root = os.path.abspath(root)
        root = pathlib.Path(root)
    stub_path = args.stub_path
    if stub_path is None:
        stub_path = str(root / "typings")
    assert isinstance(stub_path, str)
    file_allowlist = None
    if file_filter is not None and file_filter != "":
        with open(file_filter) as file_filter_contents:
            file_allowlist = [
                pathlib.Path(x.strip()) for x in file_filter_contents.readlines() if x.strip().endswith(".py")
            ]
    failed_imports = import_all_python_files_from_dir(
        project_root=root,
        file_allowlist=file_allowlist,
    )
    if len(failed_imports) > 0:
        warnings.warn(
            f"Stubs may be incomplete due to errors in loading the following files: {', '.join([x.filename for x in failed_imports])}"
        )
        if args.verbose:
            for x in failed_imports:
                print(f"Failed import: {x.filename}: {x.traceback}")
    stubgen = StubGenerator()
    for features_cls in FeatureSetBase.registry.values():
        try:
            stubgen.register_features_class(features_cls)
        except Exception as e:
            raise RuntimeError(f"Error processing features class {features_cls}") from e
    lines = stubgen.generate_features_decorator_stub_file()
    folder = os.path.join(stub_path, "chalk", "features")
    os.makedirs(folder, exist_ok=True)
    output_file = os.path.join(folder, "feature_set_decorator.pyi")
    with open(output_file, "w+") as f:
        f.write("\n".join(lines))
    print(f"Successfully wrote type stubs to {output_file}")
