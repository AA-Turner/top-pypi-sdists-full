from nexuscli import exception
from nexuscli.api import util
from nexuscli.api.base_collection import BaseCollection


class TaskCollection(BaseCollection):
    # Moved from beta to v1:
    # https://github.com/sonatype/nexus-public/commit/a6a8abcdcba3fd1947884f05f913d0da6939261c
    @util.with_min_version('3.12.1')
    def raw_list(self) -> list:
        """
        List of all script names on the Nexus 3 service.

        :return: a list of names
        :raises exception.NexusClientAPIError: if list cannot be retrieved; i.e.: any HTTP code
        other than 200.
        """
        # TODO: handle pagination
        return self._service_get('tasks')

    @util.with_min_version('3.12.1')
    def show(self, task_id: str) -> dict:
        """
        Get a single task by id

        :raises exception.NexusClientAPIError: if task cannot be retrieved
        """
        resp = self._http.get(f'tasks/{task_id}')

        if resp.status_code == 404:
            raise exception.NotFound(task_id)

        util.validate_response(resp, 200)

        return resp.json()

    @util.with_min_version('3.12.1')
    def run(self, task_id: str) -> None:
        """
        Run a task by id

        :raises exception.NexusClientAPIError: if task cannot be run
        """
        resp = self._http.post(f'tasks/{task_id}/run')

        if resp.status_code == 404:
            raise exception.NotFound(task_id)

        if resp.status_code == 405:
            raise exception.TaskDisabled(task_id)

        util.validate_response(resp, 204)

    @util.with_min_version('3.12.1')
    def stop(self, task_id: str) -> None:
        """
        Stop a running task by id

        :raises exception.NexusClientAPIError: if task cannot be stopped
        """
        resp = self._http.post(f'tasks/{task_id}/stop')

        if resp.status_code == 404:
            raise exception.NotFound(task_id)

        if resp.status_code == 409:
            raise exception.NexusClientAPIError('Unable to stop task')

        util.validate_response(resp, 204)
