from __future__ import absolute_import

from tmo.api.iterator_base_api import IteratorBaseApi


class JobEventApi(IteratorBaseApi):

    path = "/api/jobEvents"
    type = "JOB_EVENT"

    def _get_header_params(self):
        return self._get_standard_header_params(
            accept_types=[
                self.json_type,
                "application/hal+json",
                "text/uri-list",
                "application/x-spring-data-compact+json",
            ]
        )

    def find_all(
        self,
        projection: str = None,
        page: int = None,
        size: int = None,
        sort: str = None,
    ):
        """
        returns all job events

        Parameters:
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order
           e.g. name?asc: sort name in ascending order, name?desc: sort name in descending order

        Returns:
            (dict): all job events
        """
        query_vars = ["projection", "page", "sort", "size", "sort"]
        query_vals = [projection, page, sort, size, sort]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=self.path,
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def find_by_id(self, job_event_id: str, projection: str = None):
        """
        returns a job event

        Parameters:
           job_event_id (str): job event id(uuid) to find
           projection (str): projection type

        Returns:
            (dict): job event
        """
        query_vars = ["id", "projection"]
        query_vals = [job_event_id, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/search/findById",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def find_by_job_id(
        self,
        job_id: str,
        projection: str = None,
        page: int = None,
        size: int = None,
        sort: str = None,
    ):
        """
        returns events of a job

        Parameters:
           job_id (str): job id(uuid) to find events
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order
           e.g. name?asc: sort name in ascending order, name?desc: sort name in descending order

        Returns:
            (dict): job events
        """
        query_vars = ["jobId", "projection", "page", "sort", "size", "sort"]
        query_vals = [job_id, projection, page, sort, size, sort]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/search/findByJobId",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def find_by_status(
        self,
        status: list[str],
        projection: str = None,
        page: int = None,
        size: int = None,
        sort: str = None,
    ):
        """
        returns job by status

        Parameters:
           status (str): job status
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order
           e.g. name?asc: sort name in ascending order, name?desc: sort name in descending order

        Returns:
            (dict): job events
        """
        query_vars = ["status", "projection", "page", "sort", "size"]
        query_vals = [status, projection, page, sort, size]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/search/findByStatusIn",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def find_job_between_intervals(
        self, start_time: str, end_time: str, projection: str = None
    ):
        """
        returns job events within the timestamp range

        Parameters:
           start_time (str): start time e.g: 2020-03-18T09:05:03.569Z
           end_time (str): end time e.g: 2020-03-24T09:05:03.569Z
           projection (str): projection type

        Returns:
            (dict): job events
        """
        query_vars = ["startAt", "endAt", "projection"]
        query_vals = [start_time, end_time, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/search/findByCreatedAtBetween",
            header_params=self._get_header_params(),
            query_params=query_params,
        )
