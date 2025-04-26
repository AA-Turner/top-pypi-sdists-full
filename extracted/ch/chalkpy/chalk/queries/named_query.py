from __future__ import annotations

import inspect
import traceback
from typing import TYPE_CHECKING, Mapping, Sequence

from chalk.features import unwrap_feature
from chalk.utils.object_inspect import get_source_object_starting
from chalk.utils.source_parsing import should_skip_source_code_parsing

if TYPE_CHECKING:
    from chalk.client.models import FeatureReference

MAX_NAMED_QUERY_FUNCTION_DEF_LEN = 400


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
            If False (which is the default), new main deployments will fail if the planner cannot
            generate a valid plan for the named query, preventing rollover of a bad deployment. If
            set to True, the query will not be preplanned and therefore will not be validated on
            deployment.


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
                        source_code, source_line_start, source_line_end = get_source_object_starting(definition_frame)
            except Exception:
                pass

        self._input = None
        self._output = None
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
                self._input = [str(f) for f in self._input_raw]
            elif self._output_raw is not None:
                self._input = [str(unwrap_feature(o).primary_feature) for o in self._output_raw]
        except Exception:
            self._input = None
            self.errors.append(traceback.format_exc())

        return self._input

    @property
    def output(self):
        if self._output is not None:
            return self._output
        try:
            if self._output_raw is not None:
                self._output = [str(o) for o in self._output_raw]
        except Exception:
            self._output = None
            self.errors.append(f"Error creating NamedQuery '{self.name} ({self.version})': {traceback.format_exc()}")

        return self._output

    @property
    def additional_logged_features(self):
        if self._additional_logged_features is not None:
            return self._additional_logged_features
        try:
            if self._additional_logged_features_raw is not None:
                self._additional_logged_features = [str(alf) for alf in self._additional_logged_features_raw]
        except Exception:
            self._additional_logged_features = None
            self.errors.append(f"Error creating NamedQuery '{self.name} ({self.version})': {traceback.format_exc()}")

        return self._additional_logged_features


NAMED_QUERY_REGISTRY: dict[tuple[str, str | None], NamedQuery] = {}
