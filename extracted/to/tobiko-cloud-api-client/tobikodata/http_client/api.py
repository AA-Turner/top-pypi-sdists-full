import logging
import typing as t
from functools import cached_property

import httpx
from typing_extensions import Self

from tobikodata.helpers import urljoin
from tobikodata.http_client import BearerAuth, HttpClient, HttpClientError
from tobikodata.http_client.api_models.v1.dags import V1Dag
from tobikodata.http_client.api_models.v1.evaluations import V1EvaluationBase, V1RunEvaluation
from tobikodata.http_client.api_models.v1.runs import V1Run
from tobikodata.http_client.auth import AuthHttpClient, tcloud_sso

logger = logging.getLogger(__name__)


class _Base:
    def __init__(self, client: HttpClient, endpoint: str):
        self.client = client
        self.endpoint = endpoint


class V1DagApi(_Base):
    def get_dag_for_environment(self, environment: str) -> t.Optional[V1Dag]:
        """
        Return a DAG object representing the snapshot dependency graph for the specified environment name

        Args:
            environment: The environment name

        Returns:
            The dependency graph, or None if the environment doesnt exist
        """
        try:
            return self.client.get_deserialized(model=V1Dag, url_parts=[self.endpoint, environment])
        except HttpClientError as e:
            if e.status_code == 404:
                return None
            raise


class V1RunApi(_Base):
    def get_last_run_for_environment(self, environment: str) -> t.Optional[V1Run]:
        """
        Fetch information about the last run that occurred in the specified environment

        Args:
            environment: The environment name

        Returns:
            The last run, or None if the environment doesnt exist
        """
        return next(iter(self.search(environment=environment, last=True, limit=1)), None)

    def get_run_by_id(self, run_id: str) -> t.Optional[V1Run]:
        """
        Fetch a specific run by its identifier

        Args:
            run_id: The run identifier

        Returns:
            The run, or None if the identifier did not match any runs
        """
        try:
            return self.client.get_deserialized(model=V1Run, url_parts=[self.endpoint, run_id])
        except HttpClientError as e:
            if e.status_code == 404:
                return None
            raise e

    def search(
        self,
        environment: t.Optional[str] = None,
        last: bool = False,
        since_run_id: t.Optional[str] = None,
        sort: t.Literal["asc", "desc"] = "desc",
        limit: int = 100,
    ) -> t.List[V1Run]:
        """
        Search for runs based on the specified parameters

        Args:
            environment: Which environment to search in, or None for all environments
            last: Set to True to return just the most recent run that matches all the search terms
            since_run_id: Set to a run_id to return all the runs that happened since that run_id, or None to ignore
            sort: "asc" - oldest runs first, "desc" - newest runs first in the returned list
            limit: Maximum number of records to return

        Returns:
            A list of runs matching the search parameters
        """
        try:
            return self.client.get_many_deserialized(
                model=V1Run,
                url_parts=self.endpoint,
                params={
                    "environment": environment,
                    "last": last,
                    "since_run_id": since_run_id,
                    "sort": sort,
                    "limit": limit,
                },
            )
        except HttpClientError as e:
            if e.status_code == 404:
                return []
            raise e

    def get_evaluations_for_node(self, run_id: str, node_name: str) -> t.List[V1RunEvaluation]:
        """
        Fetch all the evaluations for a given DAG node within a given run.
        Note that there may be multiple evaluations for a single node if the scheduler broke up the work into batches
        or no evaluations at all if the scheduler skipped the node (which can happen if there are no intervals to run)

        Args:
            run_id: The run_id to search
            node_name: The name of the DAG node to fetch evaluations for

        Return:
            Any evaluations under the specified :run_id for the specifed :node_name
        """
        return self.get_evaluations(run_id, node_name)

    def get_evaluations(
        self, run_id: str, node_name: t.Optional[str] = None
    ) -> t.List[V1RunEvaluation]:
        """
        Fetch all the evaluations for a given DAG node within a given run.
        Note that there may be multiple evaluations for a single node if the scheduler broke up the work into batches
        or no evaluations at all if the scheduler skipped the node (which can happen if there are no intervals to run)

        Args:
            run_id: The run_id to search
            node_name: The name of the DAG node to fetch evaluations for, or None to fetch for all nodes

        Return:
            The list of matching evaluations
        """
        try:
            return self.client.get_many_deserialized(
                model=V1RunEvaluation,
                url_parts=[self.endpoint, run_id, "evaluations"],
                params={"node_name": node_name},
            )
        except HttpClientError as e:
            if e.status_code == 404:
                return []
            raise e


class V1EvaluationsApi(_Base):
    def get_evaluation_by_id(self, evaluation_id: str) -> t.Optional[V1EvaluationBase]:
        """
        Fetch an evaluation record by its ID.

        Args:
            evaluation_id: The id of the evaluation to fetch

        Return:
            The evaluation, or None if the supplied evaluation_id didnt match a record
        """
        try:
            return self.client.get_deserialized(
                model=V1EvaluationBase,
                url_parts=[self.endpoint, evaluation_id],
            )
        except HttpClientError as e:
            if e.status_code == 404:
                return None
            raise e

    def get_latest_evaluations_for_environment(self, environment: str) -> t.List[V1EvaluationBase]:
        """
        Snapshots can be evaluated multiple times (eg every time a cadence run triggers or when the snapshot backing
        an an incremental model is processed in batches).

        This returns the most recent evaluation record for each Snapshot in the specified environment.

        Args:
            environment: The environment to fetch evaluations for

        Return:
            A list of matching evaluation records. If the environment doesnt exist, an empty list is returned.
        """
        return self.search(environment=environment, latest=True, limit=None)

    def search(
        self,
        run_id: t.Optional[str] = None,
        plan_id: t.Optional[str] = None,
        environment: t.Optional[str] = None,
        latest: t.Optional[bool] = None,
        node_name: t.Optional[str] = None,
        sort: t.Literal["asc", "desc"] = "asc",
        limit: t.Optional[int] = 100,
    ) -> t.List[V1EvaluationBase]:
        try:
            return self.client.get_many_deserialized(
                model=V1EvaluationBase,
                url_parts=[self.endpoint],
                params={
                    "run_id": run_id,
                    "plan_id": plan_id,
                    "environment": environment,
                    "latest": latest,
                    "node_name": node_name,
                    "sort": sort,
                    "limit": limit,
                },
            )
        except HttpClientError as e:
            if e.status_code == 404:
                return []
            raise e


class V1ApiClient(_Base):
    def __init__(self, client: HttpClient):
        super().__init__(client=client, endpoint=urljoin(str(client._client.base_url), "/api/v1"))

    @cached_property
    def dags(self) -> V1DagApi:
        return V1DagApi(self.client, urljoin(self.endpoint, "dags"))

    @cached_property
    def runs(self) -> V1RunApi:
        return V1RunApi(self.client, urljoin(self.endpoint, "runs"))

    @cached_property
    def evaluations(self) -> V1EvaluationsApi:
        return V1EvaluationsApi(self.client, urljoin(self.endpoint, "evaluations"))

    @classmethod
    def create(
        cls,
        base_url: t.Optional[str] = None,
        token: t.Optional[str] = None,
        oauth_client_id: t.Optional[str] = None,
        oauth_client_secret: t.Optional[str] = None,
        headers: t.Optional[t.Dict[str, str]] = None,
        client: t.Optional[httpx.Client] = None,
    ) -> Self:
        if client and not base_url:
            base_url = str(client.base_url)

        if not base_url:
            raise ValueError(
                "base_url must be supplied if no pre-configured http client is supplied"
            )

        if token:
            if oauth_client_id:
                raise ValueError(
                    "You must supply either an API token or OAuth credentials, not both"
                )

            logger.warning(
                "API token authentication is deprecated. Please switch to OAuth Client ID / Client Secret"
            )

        if not client:
            # note: follow_redirects is enabled because it offers the best user experience in corporate networks
            # when its almost guaranteed there is some kind of proxy messing with the traffic
            # in addition, FastAPI automatically redirects from route("") to route("/") if route("") isnt defined
            # which raises an exception in httpx.Client unless follow_redirects is enabled
            client = httpx.Client(base_url=base_url, follow_redirects=True)

        http_client_kwargs: t.Dict[str, t.Any] = dict(
            headers=headers,
            health_ready=urljoin(base_url, "api/state-sync/enterprise-version"),
            client=client,
        )

        client_wrapper: HttpClient

        if oauth_client_id:
            sso_auth = tcloud_sso(
                client_id=oauth_client_id, client_secret=oauth_client_secret, logger=logger
            )
            client_wrapper = AuthHttpClient(sso=sso_auth, **http_client_kwargs)
        else:
            auth = BearerAuth(token=token) if token else None
            client_wrapper = HttpClient(auth=auth, **http_client_kwargs)

        return cls(client_wrapper)
