from __future__ import annotations

import collections
from typing import TYPE_CHECKING, Dict, List

from chalk.parsed.duplicate_input_gql import GraphLogSeverity, MetadataSettings, UpsertFeatureGQL, UpsertResolverGQL
from chalk.utils.string import to_camel_case

if TYPE_CHECKING:
    from chalk.parsed._graph_validation import ClientLogBuilder


MissingMetadata = Dict[GraphLogSeverity, List[str]]

METADATA_STRING_TO_FEATURE_ATTRIBUTE_MAP: Dict[str, str] = {
    "owner": "owner",
    "tags": "tags",
    "description": "description",
}

METADATA_STRING_TO_RESOLVER_ATTRIBUTE_MAP: Dict[str, str] = {
    "owner": "owner",
    "tags": "tags",
    "description": "doc",
    "doc": "doc",
    "docstring": "doc",
}


class MissingMetadataFeature:
    def __init__(self, feature: UpsertFeatureGQL, missing_metadata: MissingMetadata):
        super().__init__()
        self.feature = feature
        self.missing_metadata = missing_metadata


class MissingMetadataResolver:
    def __init__(self, resolver: UpsertResolverGQL, missing_metadata: MissingMetadata):
        super().__init__()
        self.resolver = resolver
        self.missing_metadata = missing_metadata


def build_feature_log_for_each_severity(
    builder: "ClientLogBuilder", missing_metadata_features: list[MissingMetadataFeature]
):
    if not missing_metadata_features:
        return

    for severity in GraphLogSeverity:
        log_or_none = get_missing_metadata_features_log(
            missing_metadata_features=missing_metadata_features, severity=GraphLogSeverity(severity)
        )
        if log_or_none is None:
            continue
        header, subheader = log_or_none
        builder.add_log(header=header, subheader=subheader, severity=GraphLogSeverity(severity))


def build_resolver_log_for_each_severity(
    builder: "ClientLogBuilder", missing_metadata_resolvers: list[MissingMetadataResolver]
):
    if not missing_metadata_resolvers:
        return

    for severity in GraphLogSeverity:
        for resolver in missing_metadata_resolvers:
            log_or_none = get_missing_metadata_resolver_log(
                missing_metadata_resolver=resolver, severity=GraphLogSeverity(severity)
            )
            if log_or_none is None:
                continue
            header, subheader = log_or_none
            builder.add_log(header=header, subheader=subheader, severity=GraphLogSeverity(severity))


def get_missing_metadata(
    entity: UpsertFeatureGQL | UpsertResolverGQL,
    settings: list[MetadataSettings],
    attribute_map: dict[str, str],
) -> MissingMetadata:
    res: MissingMetadata = collections.defaultdict(list)
    for setting in settings:
        metadata_name = setting.name
        try:
            severity = GraphLogSeverity(setting.missing.upper())
        except:
            """If this fails, _validate_metadata_config should log the error"""
            continue
        if metadata_name in attribute_map:
            attribute_name = attribute_map[metadata_name]
            value = getattr(entity, attribute_name)
            is_missing = value is None or (isinstance(value, list) and len(value) == 0)
            if is_missing:
                res[severity].append(metadata_name)
    return res


def validate_feature_metadata(
    settings: list[MetadataSettings],
    namespace_features: list[UpsertFeatureGQL],
) -> list[MissingMetadataFeature]:
    wrapped_features = []
    for nf in namespace_features:
        missing_metadata = get_missing_metadata(
            entity=nf,
            attribute_map=METADATA_STRING_TO_FEATURE_ATTRIBUTE_MAP,
            settings=settings,
        )
        if not missing_metadata:
            continue
        wrapped_features.append(MissingMetadataFeature(feature=nf, missing_metadata=missing_metadata))

    return wrapped_features


def get_missing_metadata_features_log(
    missing_metadata_features: list[MissingMetadataFeature], severity: GraphLogSeverity
) -> tuple[str, str] | None:
    if not missing_metadata_features:
        return None

    missing_messages = []
    feature_str = "feature"
    missing_metadata_header_str = "missing metadata"
    max_name_len = max([len(w.feature.id.name) for w in missing_metadata_features])
    feature_column_width = max(max_name_len, len(feature_str)) + 1
    get_padding = lambda s: feature_column_width - len(s)

    first_feature = missing_metadata_features[0].feature
    header = f'"{to_camel_case(first_feature.id.namespace)}" features have missing metadata'
    subheader = f"  Filepath: {first_feature.namespacePath}\n\n"

    for wrapper in missing_metadata_features:
        missing_metadata = wrapper.missing_metadata.get(severity)
        if not missing_metadata:
            continue
        padding_1 = get_padding(wrapper.feature.id.name)
        missing_metadata_str = ", ".join(missing_metadata)
        missing_messages.append(f"      {wrapper.feature.id.name}{' ' * padding_1}: {missing_metadata_str}")

    if not missing_messages:
        return None

    padding_2 = get_padding(feature_str)
    subheader += f"      {'-' * len(feature_str)}{' ' * padding_2}  {'-' * len(missing_metadata_header_str)}\n"
    subheader += f"      {feature_str}{' ' * padding_2}  {missing_metadata_header_str}\n"
    subheader += f"      {'-' * len(feature_str)}{' ' * padding_2}  {'-' * len(missing_metadata_header_str)}\n"
    subheader += "\n".join(missing_messages)

    return header, subheader


def get_missing_metadata_resolver_log(
    missing_metadata_resolver: MissingMetadataResolver, severity: GraphLogSeverity
) -> tuple[str, str] | None:
    missing_metadata = missing_metadata_resolver.missing_metadata.get(severity)
    if missing_metadata is None:
        return
    missing_metadata_str = ", ".join(missing_metadata)
    resolver_str = "resolver"
    missing_metadata_header_str = "missing metadata"
    resolver = missing_metadata_resolver.resolver
    max_name_len = len(resolver.fqn)
    feature_column_width = max(max_name_len, len(resolver_str)) + 1
    get_padding = lambda s: feature_column_width - len(s)
    padding_1 = get_padding(resolver.fqn)

    header = f'Resolver "{resolver.fqn}" has missing metadata'
    subheader = f"  Filepath: {missing_metadata_resolver.resolver.filename}\n\n"
    message = f"      {resolver.fqn}{' ' * padding_1}: {missing_metadata_str}"

    padding_2 = get_padding(resolver_str)
    subheader += f"      {'-' * len(resolver_str)}{' ' * padding_2}  {'-' * len(missing_metadata_header_str)}\n"
    subheader += f"      {resolver_str}{' ' * padding_2}  {missing_metadata_header_str}\n"
    subheader += f"      {'-' * len(resolver_str)}{' ' * padding_2}  {'-' * len(missing_metadata_header_str)}\n"
    subheader += message

    return header, subheader
