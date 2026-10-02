from __future__ import absolute_import

from tmo.api.base_api import BaseApi


class MessageApi(BaseApi):
    name = "Message API"
    path = "message"
    type = "MESSAGE"

    def send_job_event(self, event: dict):
        """
        send a job event

        Parameters:
           event (dict): event to send

        Returns:
            (dict): event
        """

        return self._send_event("jobevents", event)

    def send_progress_event(self, event: dict):
        """
        send a progress event

        Parameters:
           event (dict): event to send

        Returns:
            (dict): event
        """

        return self._send_event("jobprogress", event)

    def _send_event(self, topic, event):

        header_params = {"Content-Type": self.json_type}
        query_params = {"type": "topic"}

        return self.tmo_client.post_request(
            f"{self.base_path + self.path}/{topic}", header_params, query_params, event
        )
