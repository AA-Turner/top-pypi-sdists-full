from __future__ import absolute_import

from tmo.api.iterator_base_api import IteratorBaseApi


class DeploymentApi(IteratorBaseApi):
    path = "/api/deployments"
    type = "DEPLOYMENT"

    def _get_header_params(self):
        return self._get_standard_header_params(
            accept_types=[
                self.json_type,
                "application/hal+json",
                "text/uri-list",
                "application/x-spring-data-compact+json",
            ]
        )

    def find_by_archived(
        self,
        archived: bool = False,
        projection: str = None,
        page: int = None,
        size: int = None,
        sort: str = None,
    ):
        raise NotImplementedError("Archiving not supported for Deployments")

    def find_active_by_trained_model_and_engine_type(
        self, trained_model_id: str, engine_type: str, projection: str = None
    ):
        """
        returns deployments by trained model and engine type

        Parameters:
           trained_model_id (str): trained model id(string) to find
           engine_type (str): engine type(string) to find
           projection (str): projection type

        Returns:
            (dict): deployments
        """
        query_vars = ["trainedModelId", "engineType", "projection"]
        query_vals = [trained_model_id, engine_type, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/search/findActiveByTrainedModelIdAndEngineType",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def find_by_status(self, status: str, projection: str = None):
        """
        returns deployments by status
        Parameters:
           status (str): status(string) to find
           projection (str): projection type
        Returns:
            (dict): deployments
        """
        query_vars = ["status", "projection"]
        query_vals = [status, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/search/findByStatus",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def find_active(self, projection: str = None):
        """
        returns active deployments
        Parameters:
           projection (str): projection type
        Returns:
            (dict): deployments
        """
        query_vars = ["projection"]
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/search/findActive",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def find_by_deployment_job_id(
        self, deployment_job_id: str = None, projection: str = None
    ):
        """
        returns a deployment for specific deployment job id
        Parameters:
           deployment_job_id (str): deployment job id(string) to find
           projection (str): projection type
        Returns:
            (dict): deployments
        """
        query_vars = ["jobId", "projection"]
        query_vals = [deployment_job_id, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/search/findByJobId",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def find_active_by_task_id(self, task_id: str = None, projection: str = None):
        """
        returns active deployments for feature engineering task
        Parameters:
           task_id (str): feature engineering task id to find
           projection (str): projection type
        Returns:
            (dict): deployments
        """
        query_vars = ["taskId", "projection"]
        query_vals = [task_id, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/search/findActiveByTaskId",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def run_scoring(self, deployment_id: str, scoring_request: dict):
        """
        Run scoring for a deployment

        Parameters:
            deployment_id (str): deployment id
            scoring_request (dict): scoring request

        Returns:
            (dict): scoring response
        """
        return self.tmo_client.post_request(
            path=f"{self.path}/{deployment_id}/runCustomBatchPredictionNow",
            header_params=self._get_header_params(),
            query_params={},
            body=scoring_request,
        )
