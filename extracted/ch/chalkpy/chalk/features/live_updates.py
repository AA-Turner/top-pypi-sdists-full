from __future__ import annotations

import warnings

from chalk._gen.chalk.graph.v1 import graph_pb2
from chalk.features import Feature, FeatureWrapper
from chalk.features.feature_set import FeatureSetBase
from chalk.features.resolver import RESOLVER_REGISTRY
from chalk.parsed.to_proto import ToProtoConverter
from chalk.sql._internal.sql_file_resolver import NOTEBOOK_DEFINED_SQL_RESOLVERS
from chalk.utils import notebook
from chalk.utils.environment_parsing import env_var_bool
from chalk.utils.log_with_context import get_logger

_logger = get_logger(__name__)


class OverlayGraphWarning(UserWarning):
    pass


def _build_overlay_graph() -> graph_pb2.OverlayGraph | None:
    if not notebook.is_notebook():
        return None
    notebook_resolvers = [x for x in RESOLVER_REGISTRY.get_all_resolvers() if not notebook.is_defined_in_module(x)]
    notebook_resolvers.extend(rr.resolver for rr in NOTEBOOK_DEFINED_SQL_RESOLVERS.values() if rr.resolver is not None)
    graph = ToProtoConverter.convert_graph(
        features_registry={k: v for k, v in FeatureSetBase.registry.items() if not notebook.is_defined_in_module(v)},
        resolver_registry=notebook_resolvers,
        sql_source_registry=[],
        sql_source_group_registry=[],
        stream_source_registry=[],
        named_query_registry={},
    )
    # Grab newly-defined feature fields for feature classes that already exist in the customer source.
    overlay_namespaces = {x.name for x in graph.feature_sets}
    overlay_field_protos: list[graph_pb2.FeatureType] = []
    for ns, overlay_attr_names in FeatureSetBase.__chalk_notebook_defined_feature_fields__.items():
        if ns in overlay_namespaces:
            continue
        feature_cls = FeatureSetBase.registry[ns]
        for attr_name in overlay_attr_names:
            field = getattr(feature_cls, attr_name)
            assert isinstance(field, FeatureWrapper)
            feat = field._chalk_get_underlying()  # pyright: ignore[reportPrivateUsage]
            assert isinstance(feat, Feature)
            overlay_field_protos.append(ToProtoConverter.convert_feature(feat))
    if len(graph.feature_sets) == 0 and len(graph.resolvers) == 0 and len(overlay_field_protos) == 0:
        return None
    return graph_pb2.OverlayGraph(
        feature_sets=graph.feature_sets,
        resolvers=graph.resolvers,
        feature_fields=overlay_field_protos,
    )


def build_overlay_graph() -> graph_pb2.OverlayGraph | None:
    """
    Build an 'overlay graph' of features/resolvers defined in a notebook that are not present in the customer source.
    This can be attached to a query request to run a query against a custom graph.
    :return: None if not in notebook or there are no notebook-defined features/resolvers.
    """
    if not notebook.is_notebook():
        return None
    try:
        return _build_overlay_graph()
    except Exception as e:
        if env_var_bool("CHALK_DONT_SUPPRESS_OVERLAY_GRAPH_ERRORS"):
            raise
        # Not throwing here since this will interrupt running queries in notebook, which will be
        # very hard to recover from for the customer
        msg = (
            "An exception was raised while trying to collect notebook-generated features & resolvers."
            "\nThis means that if new features or resolvers were defined in the current notebook session, "
            "they will not used when executing queries against the Chalk server."
            f"\n\nThe exception was: {e}"
        )
        warnings.warn(msg, OverlayGraphWarning)
        return None
