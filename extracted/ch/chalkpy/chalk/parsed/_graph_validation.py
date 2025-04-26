from __future__ import annotations

import collections
import traceback
from collections import defaultdict
from typing import DefaultDict, Dict, List, Mapping

import pyarrow as pa

from chalk._lsp.error_builder import FeatureClassErrorBuilder, LSPErrorBuilder, ResolverErrorBuilder
from chalk.features import FeatureSetBase
from chalk.features._encoding.serialized_dtype import deserialize_dtype
from chalk.features.resolver import RESOLVER_REGISTRY
from chalk.parsed._metadata import (
    METADATA_STRING_TO_FEATURE_ATTRIBUTE_MAP,
    METADATA_STRING_TO_RESOLVER_ATTRIBUTE_MAP,
    MissingMetadataResolver,
    build_feature_log_for_each_severity,
    build_resolver_log_for_each_severity,
    get_missing_metadata,
    validate_feature_metadata,
)
from chalk.parsed.duplicate_input_gql import (
    GraphLogSeverity,
    ProjectSettingsGQL,
    UpdateGraphError,
    UpsertFeatureGQL,
    UpsertGraphGQL,
    UpsertResolverGQL,
)
from chalk.utils.duration import parse_chalk_duration
from chalk.utils.string import add_quotes, oxford_comma_list


class ClientLogBuilder:
    def __init__(self):
        super().__init__()
        self._logs: List[UpdateGraphError] = []

    def add_log(self, header: str, subheader: str, severity: GraphLogSeverity):
        self._logs.append(UpdateGraphError(header=header, subheader=subheader, severity=severity))

    def add_error(self, header: str, subheader: str):
        self.add_log(header=header, subheader=subheader, severity=GraphLogSeverity.ERROR)

    def add_warning(self, header: str, subheader: str):
        self.add_log(header=header, subheader=subheader, severity=GraphLogSeverity.WARNING)

    def add_info(self, header: str, subheader: str):
        self.add_log(header=header, subheader=subheader, severity=GraphLogSeverity.INFO)

    def get_logs(self) -> List[UpdateGraphError]:
        return self._logs


def _validate_primary_key(
    feature: UpsertFeatureGQL,
    builder: ClientLogBuilder,
    lsp_builder: FeatureClassErrorBuilder,
):
    if feature.scalarKind is not None and feature.scalarKind.primary:
        assert feature.scalarKind.dtype is not None, f"The serialized dtype is not set for feature '{feature.id.fqn}'"
        pa_dtype = deserialize_dtype(feature.scalarKind.dtype)
        if (
            not pa.types.is_integer(pa_dtype)
            and not pa.types.is_large_string(pa_dtype)
            and not pa.types.is_string(pa_dtype)
        ):
            lsp_builder.add_diagnostic(
                label="invalid type",
                message=f"Primary keys must be integers or strings. Feature '{feature.id.fqn}' has a type of '{pa_dtype}'",
                range=lsp_builder.annotation_range(feature.id.attributeName or feature.id.name),
                code="23",
            )
            builder.add_error(
                header=f'Invalid primary key type "{feature.id.fqn}"',
                subheader=(
                    f"Primary keys must be integers or strings. " f'Feature "{feature.id.fqn}" has a type of {pa_dtype}'
                ),
            )


def _validate_max_staleness(
    feature: UpsertFeatureGQL,
    builder: ClientLogBuilder,
    lsp_builder: FeatureClassErrorBuilder,
):
    if feature.maxStaleness is not None and feature.maxStaleness != "infinity":
        try:
            parse_chalk_duration(feature.maxStaleness)
        except ValueError as e:
            builder.add_error(
                header=f'Could not parse max_staleness for feature "{feature.id.fqn}"',
                subheader=f"Invalid max staleness. {e.args[0]}",
            )


def _validate_etl_to_online(
    feature: UpsertFeatureGQL,
    builder: ClientLogBuilder,
    lsp_builder: FeatureClassErrorBuilder,
):
    if feature.etlOfflineToOnline and feature.maxStaleness is None:
        builder.add_error(
            header=f'Missing max staleness for "{feature.id.fqn}"',
            subheader=f'The feature "{feature.id.fqn}" is set to ETL to online, but doesn\'t specify a max staleness. Any ETL to online would be immediately invalidated.',
        )


def _validate_no_feature_times_as_input(
    fqn_to_feature: Mapping[str, UpsertFeatureGQL],
    resolver: UpsertResolverGQL,
    builder: ClientLogBuilder,
    lsp_builder: ResolverErrorBuilder,
):
    for i, inp in enumerate(resolver.inputs or []):
        if inp.underlying.fqn not in fqn_to_feature:
            lsp_builder.add_diagnostic(
                message=f"Resolver '{resolver.fqn}' requires an unrecognized feature '{inp.underlying.fqn}'",
                code="135",
                range=lsp_builder.function_arg_annotation_by_index(i),
                label="invalid resolver input",
            )
            builder.add_error(
                header=f"Resolver '{resolver.fqn}' requires an unknown feature '{inp.underlying.fqn}'",
                subheader="Please check the inputs to this resolver, and make sure they are all features.",
            )
        elif fqn_to_feature[inp.underlying.fqn].featureTimeKind is not None and resolver.kind != "offline":
            lsp_builder.add_diagnostic(
                message=(
                    f'The resolver "{resolver.fqn}" takes as input the\n'
                    f'feature "{inp.underlying.fqn}", a feature_time() type.\n'
                    f"Feature times can be returned from {resolver.kind} resolvers to\n"
                    "indicate data from the past, but cannot be accepted\n"
                    "as inputs."
                ),
                code="136",
                range=lsp_builder.function_arg_annotation_by_index(i),
                label="invalid resolver input",
            )
            builder.add_error(
                header=f"Feature times cannot be accepted as input to {resolver.kind} resolvers.",
                subheader=(
                    f'The resolver "{resolver.fqn}" takes as input the\n'
                    f'feature "{inp.underlying.fqn}", a feature_time() type.\n'
                    f"Feature times can be returned from {resolver.kind} resolvers to\n"
                    "indicate data from the past, but cannot be accepted\n"
                    "as inputs."
                ),
            )


def _validate_feature_names_unique(features: List[UpsertFeatureGQL], builder: ClientLogBuilder):
    counter: DefaultDict[str, int] = defaultdict(lambda: 0)
    for r in features:
        counter[r.id.fqn] += 1

    for fqn, count in counter.items():
        if count > 1:
            builder.add_error(
                header="Duplicate feature names",
                subheader=(
                    f'There are {count} features with the same name of "{fqn}". All features require a '
                    f"distinct name"
                ),
            )


def _validate_resolver_names_unique(resolvers: List[UpsertResolverGQL], builder: ClientLogBuilder):
    counter: DefaultDict[str, int] = defaultdict(lambda: 0)
    for r in resolvers:
        counter[r.fqn.split(".")[-1]] += 1

    for name, count in counter.items():
        if count > 1:
            builder.add_error(
                header="Duplicate resolver names",
                subheader=(
                    f'There are {count} resolvers with the same name of "{name}". All resolvers require a '
                    f"distinct name"
                ),
            )


def _validate_resolver_input(
    singleton_namespaces: set[str],
    resolver: UpsertResolverGQL,
    builder: ClientLogBuilder,
    lsp_builder: ResolverErrorBuilder,
):
    namespaces = []
    ns_to_arg_num: Dict[str, int] = {}

    for idx, input_ in enumerate(resolver.inputs or []):
        f = input_.path[0].parent if input_.path is not None and len(input_.path) > 0 else input_.underlying
        if f.namespace not in singleton_namespaces:
            ns_to_arg_num[f.namespace] = idx
            if f.namespace not in namespaces:
                namespaces.append(f.namespace)

    if len(namespaces) > 1:
        arg_num = list(ns_to_arg_num.values())[0]
        d = lsp_builder.add_diagnostic(
            message=f"""All inputs to a resolver should be rooted in the same namespace.
The resolver "{resolver.fqn}" takes inputs in the namespaces {oxford_comma_list(add_quotes(namespaces))}.

If you require features from many feature classes, reference them via their relationships, such as:
  User.bank_account.title,
  User.full_name""",
            code="131",
            range=lsp_builder.function_arg_annotation_by_index(arg_num),
            label="secondary namespace",
        )
        for ns, arg in ns_to_arg_num.items():
            if arg != arg_num:
                d.with_range(
                    lsp_builder.function_arg_annotation_by_index(arg),
                    label=f"other namespace {ns}",
                )

        builder.add_error(
            header=f'Resolver "{resolver.fqn}" requires features from multiple namespaces.',
            subheader=f"""All inputs to a resolver should be rooted in the same namespace.
The resolver "{resolver.fqn}" takes inputs in the namespaces {oxford_comma_list(add_quotes(namespaces))}.

If you require features from many feature classes, reference them via their relationships, such as:
  User.bank_account.title,
  User.full_name

{resolver.functionDefinition}
""",
        )


def _validate_resolver_output(
    resolver: UpsertResolverGQL, builder: ClientLogBuilder, lsp_builder: ResolverErrorBuilder
):
    output = resolver.output
    features = output.features or []
    dataframes = output.dataframes or []
    if len(features) == 0 and len(dataframes) == 0:
        lsp_builder.add_diagnostic(
            message=f'Resolver "{resolver.fqn}" does not define outputs. All resolvers must have an output',
            code="132",
            range=lsp_builder.function_return_annotation(),
            label="invalid resolver output",
            code_href="https://docs.chalk.ai/docs/python-resolvers#outputs",
        )
        builder.add_error(
            header=f'Resolver "{resolver.fqn}" does not define outputs.',
            subheader="See https://docs.chalk.ai/docs/python-resolvers#outputs for information about valid resolver outputs.",
        )

    if len(dataframes) > 1:
        lsp_builder.add_diagnostic(
            message=f'Resolver "{resolver.fqn}" defines multiple DataFrames as output. At most one is permitted',
            code="133",
            range=lsp_builder.function_return_annotation(),
            label="invalid resolver output",
            code_href="https://docs.chalk.ai/docs/python-resolvers#outputs",
        )
        builder.add_error(
            header=f'Resolver "{resolver.fqn}" defines multiple DataFrames as output.',
            subheader="See https://docs.chalk.ai/docs/python-resolvers#outputs for information about valid resolver outputs.",
        )

    if len(features) > 0 and len(dataframes) > 0:
        lsp_builder.add_diagnostic(
            message=(
                f'Resolver "{resolver.fqn}" returns both relationships and scalar features. '
                f"Only one or the other is permitted."
            ),
            code="134",
            range=lsp_builder.function_return_annotation(),
            label="invalid resolver output",
            code_href="https://docs.chalk.ai/docs/python-resolvers#outputs",
        )
        builder.add_error(
            header=f'Resolver "{resolver.fqn}" returns both relationships and scalar features.',
            subheader="See https://docs.chalk.ai/docs/python-resolvers#outputs for information about valid resolver outputs.",
        )

    # Want to validate this but only have feature id instead of feature
    # if len(resolver.inputs) == 0 and len(dataframes) == 1 and len([pkey for pkey in dataframes[0].columns if pkey.primary]) != 1:
    #     builder.add_error(
    #         header=f'Resolver "{resolver.fqn}" must return a primary feature',
    #         subheader="See https://docs.chalk.ai/docs/python-resolvers#outputs for information about valid resolver outputs.",
    #     )
    # for output_feature in features:
    #     if is_underlying_has_many(output_feature):
    #         if len([pkey for pkey in output_feature.underlying.df.columns if pkey.primary]) != 1:
    #         builder.add_error(
    #             header=f'Resolver "{resolver.fqn}" must return a primary feature in has-many outputs',
    #             subheader="See https://docs.chalk.ai/docs/python-resolvers#outputs for information about valid resolver outputs.",
    #         )
    # Bring this back.


#     if len(features) > 0:
#         namespaces = list(set(f.namespace for f in features))
#         if len(namespaces) > 1:
#             builder.add_error(
#                 header=f'Resolver "{resolver.fqn}" outputs features from multiple namespaces.',
#                 subheader=f"""All outputs of a resolver should be rooted in the same namespace.
# The resolver "{resolver.fqn}" outputs features in the namespaces {oxford_comma_list(namespaces)}.
# See https://docs.chalk.ai/docs/python-resolvers#outputs for information about valid resolver outputs.
#
# {resolver.functionDefinition}
# """,
#             )


# FIXME CHA-66 we should validate that joins are all pkey on pkey joins. no non-primary keys, no self-joins, no constants
def _validate_joins(feature: UpsertFeatureGQL, builder: ClientLogBuilder, lsp_builder: FeatureClassErrorBuilder):
    pass


def _validate_feature_names(
    feature: UpsertFeatureGQL, builder: ClientLogBuilder, lsp_builder: FeatureClassErrorBuilder
):
    if feature.id.name.startswith("__") or feature.id.name.startswith("_chalk"):
        lsp_builder.add_diagnostic(
            message="Feature names cannot begin with '_chalk' or '__'.",
            range=lsp_builder.property_range(feature.id.attributeName or feature.id.name),
            label="protected name",
            code="24",
        )
        builder.add_error(
            header="Feature uses protected name",
            subheader="Feature names cannot begin with '_chalk' or '__'.",
        )

    if feature.id.namespace.startswith("__") or feature.id.namespace.startswith("_chalk"):
        lsp_builder.add_diagnostic(
            message="Feature classes cannot have names that begin with '_chalk' or '__'.",
            label="protected namespace",
            range=lsp_builder.decorator_kwarg_value_range("name") or lsp_builder.class_definition_range(),
            code="25",
        )
        builder.add_error(
            header="Feature class uses protected namespace",
            subheader=(
                f'The feature "{feature.id.fqn}" belongs to the protected namespace "{feature.id.namespace}". '
                f'Feature namespaces cannot begin with "_chalk" or "__". Please rename this feature set.'
            ),
        )


def _validate_metadata(
    features: list[UpsertFeatureGQL],
    resolvers: list[UpsertResolverGQL],
    builder: ClientLogBuilder,
    request_config: ProjectSettingsGQL | None,
):
    if not (request_config and request_config.validation):
        return

    if request_config.validation.feature and request_config.validation.feature.metadata:
        namespace_to_features = collections.defaultdict(list)
        for f in features:
            namespace_to_features[f.id.namespace].append(f)

        for ns_features in namespace_to_features.values():
            wf = validate_feature_metadata(
                settings=request_config.validation.feature.metadata, namespace_features=ns_features
            )
            build_feature_log_for_each_severity(builder=builder, missing_metadata_features=wf)
    if request_config.validation.resolver and request_config.validation.resolver.metadata:
        missing_resolver_metadatas: list[MissingMetadataResolver] = []
        for r in resolvers:
            metadata = get_missing_metadata(
                entity=r,
                attribute_map=METADATA_STRING_TO_RESOLVER_ATTRIBUTE_MAP,
                settings=request_config.validation.resolver.metadata,
            )
            missing_resolver_metadatas.append(MissingMetadataResolver(resolver=r, missing_metadata=metadata))
        build_resolver_log_for_each_severity(builder, missing_resolver_metadatas)


def _validate_metadata_config(
    builder: ClientLogBuilder,
    request_config: ProjectSettingsGQL | None,
):
    if not (request_config and request_config.validation):
        return

    severities_lower = [e.lower() for e in GraphLogSeverity]

    if request_config.validation.feature and request_config.validation.feature.metadata:
        for missing_metadata in request_config.validation.feature.metadata:
            metadata_name = missing_metadata.name
            severity = missing_metadata.missing

            severity_upper = severity.upper()
            try:
                GraphLogSeverity(severity_upper)
            except ValueError:
                severity_choices = '" or "'.join(severities_lower)
                builder.add_warning(
                    header=f'Found invalid log severity "{severity}" config for missing metadata',
                    subheader=(
                        f'The required feature metadata "{metadata_name}" is associated with an invalid log severity "{severity}".'
                        f' Please use "{severity_choices}" in chalk.yml'
                    ),
                )

            if metadata_name not in METADATA_STRING_TO_FEATURE_ATTRIBUTE_MAP:
                builder.add_warning(
                    header=f'Found invalid feature metadata "{metadata_name}" in config',
                    subheader=(
                        f'The required metadata "{metadata_name}" is not a valid feature metadata.'
                        f" Please consider removing it from chalk.yml"
                    ),
                )

    if request_config.validation.resolver and request_config.validation.resolver.metadata:
        for missing_metadata in request_config.validation.resolver.metadata:
            metadata_name = missing_metadata.name
            severity = missing_metadata.missing

            severity_upper = severity.upper()
            try:
                GraphLogSeverity(severity_upper)
            except ValueError:
                severity_choices = '" or "'.join(severities_lower)
                builder.add_warning(
                    header=f'Found invalid log severity "{severity}" config for missing metadata',
                    subheader=(
                        f'The required feature metadata "{metadata_name}" is associated with an invalid log severity "{severity}".'
                        f' Please use "{severity_choices}" in chalk.yml'
                    ),
                )

            if metadata_name not in METADATA_STRING_TO_RESOLVER_ATTRIBUTE_MAP:
                builder.add_warning(
                    header=f'Found invalid feature metadata "{metadata_name}" in config',
                    subheader=(
                        f'The required metadata "{metadata_name}" is not a valid feature metadata.'
                        f" Please consider removing it from chalk.yml"
                    ),
                )


def _validate_namespace_primary_key(
    namespace: str,
    features: List[UpsertFeatureGQL],
    builder: ClientLogBuilder,
    singleton_namespaces: set[str],
):
    if namespace in singleton_namespaces:
        return

    primary_features = list(f for f in features if f.scalarKind and f.scalarKind.primary)

    if len(primary_features) == 0:
        builder.add_error(
            header=f"Feature set '{namespace}' is missing a primary feature",
            subheader=f"Please add an 'int' or 'str' feature to '{namespace}', annotated with '= feature(primary=True)'",
        )
    elif len(primary_features) > 1:
        names = ", ".join([f.id.name for f in primary_features])
        builder.add_error(
            header=f"Feature set '{namespace}' has too many primary features",
            subheader=f"Found primary features: {names}. Composite primary keys are not supported. Please mark only a single feature as primary.",
        )


def validate_graph(request: UpsertGraphGQL) -> List[UpdateGraphError]:
    """Beware: errors here will only be acted upon `chalk apply --branch`.
    Regular deployments will have their graph errors acted upon by the server.
    """
    singleton_namespaces = {c.name for c in request.featureClasses or [] if c.isSingleton}

    namespaces: Dict[str, List[UpsertFeatureGQL]] = defaultdict(list)

    for feature in request.features or []:
        namespaces[feature.id.namespace].append(feature)

    builder = ClientLogBuilder()

    # Validate the features
    _validate_feature_names_unique(request.features or [], builder)
    _validate_metadata_config(builder, request.config)
    _validate_metadata(request.features or [], request.resolvers or [], builder, request.config)

    for namespace, features in namespaces.items():
        _validate_namespace_primary_key(
            namespace=namespace,
            features=features,
            builder=builder,
            singleton_namespaces=singleton_namespaces,
        )

    garbage_feature_builder = FeatureClassErrorBuilder(uri="garbage.py", namespace="garbage", node=None)
    for feature in request.features or []:
        lsp_builder = (
            FeatureSetBase.registry[feature.id.namespace].__chalk_error_builder__
            if feature.id.namespace in FeatureSetBase.registry and LSPErrorBuilder.lsp
            else garbage_feature_builder
        )
        _validate_primary_key(feature, builder, lsp_builder)
        _validate_max_staleness(feature, builder, lsp_builder)
        _validate_joins(feature, builder, lsp_builder)
        _validate_etl_to_online(feature, builder, lsp_builder)
        _validate_feature_names(feature, builder, lsp_builder)

    # Validate the resolvers
    fqn_to_feature = {f.id.fqn: f for f in request.features or []}

    _validate_resolver_names_unique(request.resolvers or [], builder)
    garbage_resolver_builder = ResolverErrorBuilder(fn=None)
    for resolver in request.resolvers or []:
        try:
            lsp_builder = garbage_resolver_builder
            if LSPErrorBuilder.lsp:
                maybe_resolver = RESOLVER_REGISTRY.get_resolver(resolver.fqn)
                if maybe_resolver is not None:
                    if maybe_resolver.is_sql_file_resolver:
                        continue
                    lsp_builder = maybe_resolver.lsp_builder
            _validate_resolver_input(
                singleton_namespaces=singleton_namespaces,
                resolver=resolver,
                builder=builder,
                lsp_builder=lsp_builder,
            )
            _validate_resolver_output(resolver, builder, lsp_builder)

            # TODO we still allow this
            # _validate_resolver_feature_cycles(fqn_to_feature=fqn_to_feature, resolver=resolver, builder=builder)

            # TODO Some customers currently still do stuff like:
            # >>> def some_resolver(uid: User.id) -> DataFrame[Transaction]: ....
            # So don't even warn about it
            # _validate_resolver_input_and_output_namespace(resolver, builder)

            _validate_no_feature_times_as_input(
                fqn_to_feature=fqn_to_feature, resolver=resolver, builder=builder, lsp_builder=lsp_builder
            )
        except Exception:
            err = traceback.format_exc()
            builder.add_error(
                header=f'Failed to validate resolver "{resolver.fqn}"',
                subheader=f"Please check the resolver for syntax errors.\nRaw error: {err}",
            )

    return builder.get_logs()
