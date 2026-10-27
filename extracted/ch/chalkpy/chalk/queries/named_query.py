from __future__ import annotations

import dataclasses
import inspect
import traceback
from typing import TYPE_CHECKING, Mapping, Sequence

from chalk._lsp.error_builder import LSPErrorBuilder
from chalk.features import Underscore, feature_to_query_str, unwrap_feature
from chalk.features.feature_wrapper import AliasedFeature, validate_output_column_name
from chalk.utils.object_inspect import get_source_object_starting
from chalk.utils.source_parsing import should_skip_source_code_parsing

if TYPE_CHECKING:
    from chalk.client.models import FeatureReference

MAX_NAMED_QUERY_FUNCTION_DEF_LEN = 400

RESOURCE_GROUPS_ALL_ENVIRONMENTS = "__all__"
"""Key in ``NamedQuery.resource_groups`` whose resource groups apply in every environment."""


class NamedQuery:
    def __init__(
        self,
        *,
        name: str,
        version: str | None = None,
        input: Sequence[FeatureReference] | None = None,
        output: Sequence[FeatureReference] | None = None,
        tags: Sequence[str] | None = None,
        description: str | None = None,
        owner: str | None = None,
        meta: Mapping[str, str] | None = None,
        staleness: Mapping[FeatureReference, str] | None = None,
        planner_options: Mapping[str, str | int | bool] | None = None,
        additional_logged_features: Sequence[FeatureReference] | None = None,
        valid_plan_not_required: bool = False,
        resource_groups: Sequence[str] | Mapping[str, Sequence[str]] | None = None,
    ):
        """Create a named query.

        Named queries are aliases for specific queries that can be used by API clients.

        Parameters
        ----------
        name
            A name for the named query—this can be versioned with the version parameter, but
            must otherwise be unique. The name of the named query shows up in the dashboard and
            is used to specify the outputs for a query.
        version:
            A string specifying the version of the named query: version is not required, but
            if specified it must be a valid "semantic version".
        input
            The features which will be provided by callers of this query.
            For example, `[User.id]`. Features can also be expressed as snakecased strings,
            e.g. `["user.id"]`.
        output
            Outputs are the features that you'd like to compute from the inputs.
            For example, `[User.age, User.name, User.email]`.

            If an empty sequence, the output will be set to all features on the namespace
            of the query. For example, if you pass as input `{"user.id": 1234}`, then the query
            is defined on the `User` namespace, and all features on the `User` namespace
            (excluding has-one and has-many relationships) will be used as outputs.

            An output can also be an expression returned as its own column, named with
            `.alias`: an aliased feature, e.g. `User.transaction_count["1d"].alias("tc_1d")`,
            or an aliased underscore expression on the query's namespace, e.g.
            `(_.age / 100).alias("age_pct")`. Expression columns are returned after the
            features, and features they reference are still computed, persisted, and
            logged under their own names.
        tags
            Allows selecting resolvers with these tags.
        description
            A description of the query. Rendered in the Chalk UI and used for search indexing.
        owner
            The owner of the query. This should be a Slack username or email address.
            This is used to notify the owner in case of incidents
        meta
            Additional metadata for the query.
        staleness
            Maximum staleness overrides for any output features or intermediate features.
            See https://docs.chalk.ai/docs/query-caching for more information.
        planner_options
            Dictionary of additional options to pass to the Chalk query engine.
            Values may be provided as part of conversations with Chalk support
            to enable or disable specific functionality.
        additional_logged_features
            If query logging is enabled, this will log the specified features in addition to
            the output features to the query log.
        valid_plan_not_required
            If `False` (which is the default), new main deployments will fail if the planner cannot
            generate a valid plan for the named query, preventing rollover of a bad deployment. If
            set to `True`, the query will not be preplanned and therefore will not be validated on
            deployment.
        resource_groups
            Scopes which query servers preplan this named query. Either a sequence of
            resource groups, or a mapping from environment id to sequences of resource
            groups. The sequence form applies in every environment and is shorthand for
            `{"__all__": [...]}`. In the mapping form, resource groups under the key
            `"__all__"` preplan the query in every environment, while resource groups
            under an environment id preplan it only in that environment; an environment
            with no matching entry does not preplan the query. By default, all resource
            groups in all environments plan every named query.


        Examples
        --------
        >>> from chalk import NamedQuery
        >>> # this query's name and version can be used to specify query outputs in an API request.
        >>> NamedQuery(
        ...     name="fraud_model",
        ...     version="1.0.0",
        ...     input=[User.id],
        ...     output=[User.age, User.fraud_score, User.credit_report.fico],
        ... )
        """
        super().__init__()
        self.errors = []

        filename = None
        source_line_start = None
        source_line_end = None
        source_code = None

        if not should_skip_source_code_parsing():
            try:
                internal_frame = inspect.currentframe()
                if internal_frame is not None:
                    definition_frame = internal_frame.f_back
                    if definition_frame is not None:
                        filename = definition_frame.f_code.co_filename
                        source_line_start = definition_frame.f_lineno
                        source_code, source_line_start, source_line_end = get_source_object_starting(definition_frame)
                    del internal_frame
            except Exception:
                pass

        self._input = None
        self._output = None
        self._output_expressions: list[NamedQueryOutputExpression] = []
        self._additional_logged_features = None
        self._input_raw = input
        self._output_raw = output
        self._additional_logged_features_raw = additional_logged_features
        self.name = name
        self.version = version and str(version)
        self.tags = [str(t) for t in tags] if tags else None
        self.filename = filename
        self.description = description
        self.owner = owner
        self.meta = meta
        self.staleness = {str(k): v for k, v in staleness.items()} if staleness else None
        self.planner_options = {k: str(v) for k, v in planner_options.items()} if planner_options else None
        self.source_line_start = source_line_start
        self.code = source_code
        self.source_line_end = source_line_end
        self.valid_plan_not_required = valid_plan_not_required
        if resource_groups is None:
            self.resource_groups = None
        elif isinstance(resource_groups, Mapping):
            self.resource_groups = {str(env): [str(rg) for rg in groups] for env, groups in resource_groups.items()}
        else:
            self.resource_groups = {RESOURCE_GROUPS_ALL_ENVIRONMENTS: [str(rg) for rg in resource_groups]}

        dup_nq = NAMED_QUERY_REGISTRY.get((name, version), None)
        if dup_nq is not None:
            self.errors.append(
                (
                    "Named query must be distinct on name and version, but found two named queries with name "
                    f"'{name}' and version '{version} in files '{dup_nq.filename}' and '{filename}'."
                )
            )

        NAMED_QUERY_REGISTRY[(name, version)] = self

    @property
    def input(self):
        if self._input is not None:
            return self._input
        try:
            if self._input_raw is None and self._output_raw is None:
                self._input = None
                self.errors.append("Must provide either input or output ")
            elif self._input_raw is not None:
                # feature_to_query_str (not str) so a projected has-many input keeps its columns,
                # e.g. `user.transactions[transaction.id]`.
                self._input = [feature_to_query_str(f) for f in self._input_raw]
            elif self._output_raw is not None:
                # Underscore expressions name no feature class, so they cannot imply an input.
                self._input = [
                    str(unwrap_feature(o.resolve() if isinstance(o, AliasedFeature) else o).primary_feature)
                    for o in self._output_raw
                    if not isinstance(o, Underscore)
                ]
                if not self._input:
                    raise ValueError("A named query whose outputs are all underscore expressions must declare `input`")
        except Exception as e:
            self._input = None
            if not LSPErrorBuilder.promote_exception(e):
                self.errors.append(
                    f"Error creating NamedQuery '{self.name} ({self.version})': {traceback.format_exc()}"
                )

        return self._input

    @property
    def output(self):
        if self._output is not None:
            return self._output
        try:
            if self._output_raw is not None:
                # Imported here: the output encoders import the client and graph serializer, which import this module.
                from chalk.features._encoding.outputs import parse_underscore_aliased_column

                output: list[str] = []
                output_expressions: list[NamedQueryOutputExpression] = []
                for o in self._output_raw:
                    if isinstance(o, AliasedFeature):
                        output_expressions.append(
                            NamedQueryOutputExpression(
                                name=o.name, expr=o.to_underscore(), namespace=o.resolve().root_namespace
                            )
                        )
                    elif isinstance(o, Underscore):
                        name, expr = parse_underscore_aliased_column(o)
                        validate_output_column_name(name)
                        output_expressions.append(NamedQueryOutputExpression(name=name, expr=expr, namespace=None))
                    else:
                        output.append(feature_to_query_str(o))
                # Features are returned under their fqns, which contain a '.', and expression columns under
                # names that do not, so only expression names can collide.
                names = [e.name for e in output_expressions]
                duplicates = sorted({n for n in names if names.count(n) > 1})
                if duplicates:
                    raise ValueError(f"Output column names must be unique, but found duplicates {duplicates}")
                # Only unrooted expressions need the input namespaces. Reading `input` re-raises, and records again,
                # an input error that `input` has already recorded, so it is read only when needed.
                unrooted = any(e.namespace is None for e in output_expressions)
                _validate_expression_names_against_features(output_expressions, (self.input or ()) if unrooted else ())
                self._output = output
                self._output_expressions = output_expressions
        except Exception as e:
            self._output = None
            if not LSPErrorBuilder.promote_exception(e):
                self.errors.append(
                    f"Error creating NamedQuery '{self.name} ({self.version})': {traceback.format_exc()}"
                )

        return self._output

    @property
    def output_expressions(self) -> list[NamedQueryOutputExpression]:
        """Expressions the query returns as additional columns, after the features in `output`."""
        _ = self.output
        return self._output_expressions

    @property
    def additional_logged_features(self):
        if self._additional_logged_features is not None:
            return self._additional_logged_features
        try:
            if self._additional_logged_features_raw is not None:
                self._additional_logged_features = [str(alf) for alf in self._additional_logged_features_raw]
        except Exception as e:
            self._additional_logged_features = None
            if not LSPErrorBuilder.promote_exception(e):
                self.errors.append(
                    f"Error creating NamedQuery '{self.name} ({self.version})': {traceback.format_exc()}"
                )

        return self._additional_logged_features


def _validate_expression_names_against_features(
    expressions: Sequence[NamedQueryOutputExpression], input: Sequence[str]
) -> None:
    # The engine rejects a column named like a feature of the namespace its expression is rooted at; an expression
    # without one is rooted at the query's, so it is checked against every input namespace.
    from chalk.features.feature_set import FeatureSetBase

    input_namespaces = sorted({fqn.split(".", 1)[0] for fqn in input})
    for e in expressions:
        for namespace in [e.namespace] if e.namespace is not None else input_namespaces:
            features_cls = FeatureSetBase.registry.get(namespace)
            if features_cls is not None and e.name in {f.name for f in features_cls.features}:
                raise ValueError(
                    f"Output column name '{e.name}' is a feature of '{namespace}'; choose a name that is not a "
                    + "feature name"
                )


@dataclasses.dataclass(frozen=True)
class NamedQueryOutputExpression:
    """An underscore expression a named query returns as a column named `name`."""

    name: str
    expr: Underscore
    namespace: str | None
    """The feature class `expr`'s `_` is, such as an aliased feature's root namespace; `None` for the query's."""


NAMED_QUERY_REGISTRY: dict[tuple[str, str | None], NamedQuery] = {}
