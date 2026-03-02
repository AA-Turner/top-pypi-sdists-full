from __future__ import absolute_import

from tmo.api.iterator_base_api import IteratorBaseApi


class JobApi(IteratorBaseApi):
    path = "/api/jobs"
    type = "JOB"

    def find_by_archived(
        self,
        archived: bool = False,
        projection: str = None,
        page: int = None,
        size: int = None,
        sort: str = None,
    ):
        raise NotImplementedError("Archiving not supported for Jobs")

    def _get_header_params(self):
        return self._get_standard_header_params(
            accept_types=[
                self.json_type,
                "application/hal+json",
                "text/uri-list",
                "application/x-spring-data-compact+json",
            ]
        )

    def find_job_events(self, job_id: str, projection: str = None):
        """
        returns events of a job

        Parameters:
           job_id (str): job id(uuid) to find events
           projection (str): projection type

        Returns:
            (dict): job events
        """
        query_vars = ["projection"]
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/{job_id}/events",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def find_by_job_event_id(
        self, job_id: str, job_event_id: str, projection: str = None
    ):
        """
        returns job event

        Parameters:
           job_id (str): job id(uuid)
           job_event_id (str): job event id(uuid)
           projection (str): projection type

        Returns:
            (dict): job event
        """
        query_vars = ["projection"]
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/{job_id}/events/{job_event_id}",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def find_by_deployment_id(self, deployment_id: str, projection: str = None):
        """
        returns list of jobs for a given deployment

        Parameters:
           deployment_id (str): deployment id(string) to find
           projection (str): projection type

        Returns:
            (dict): jobs
        """
        query_vars = ["deploymentId", "projection"]
        query_vals = [deployment_id, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/search/findByDeploymentId",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def wait(self, job_id: str, timeout_sec: int = 60):
        import time

        start_time_sec = time.time()

        while True:
            job = self.find_by_id(id=job_id, projection="expandJob")
            status = (
                job.get("status", "UNKNOWN") if isinstance(job, dict) else "UNKNOWN"
            )

            if status == "COMPLETED":
                return
            elif status in ["ERROR", "CANCELLED"]:
                raise SystemError(f"Job failed with status: {status}")

            elapsed = time.time() - start_time_sec
            if elapsed > timeout_sec:
                raise TimeoutError(
                    f"Timeout waiting for job to complete. Current status: {status}"
                )

            time.sleep(5)
