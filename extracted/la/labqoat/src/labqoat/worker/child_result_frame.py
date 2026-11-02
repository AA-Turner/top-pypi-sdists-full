"""Owned child-result frames are validated before acknowledgement or subscription resumption."""

from labqoat.json_document import JsonDocument
from labqoat.worker.worker_api_error import WorkerApiError
from labqoat.compute.child_observation_evidence import ChildObservationEvidence


class ChildResultFrame:
    """Reject duplicate, empty and foreign results without exposing retained child payloads."""

    @staticmethod
    def capture(
        response: JsonDocument, expected: set[str], parent_attempt_id: str | None = None
    ) -> dict[str, JsonDocument]:
        """Return independently keyed terminal outcomes within the observed parent's authority."""
        if "error" in response:
            raise WorkerApiError("Child completion was rejected", 409)
        results = [JsonDocument.expect_dict(item) for item in JsonDocument.expect_list(response["items"])]
        indexed = {JsonDocument.expect_scalar(item["id"], str): item for item in results}
        if not indexed or len(indexed) != len(results) or not indexed.keys() <= expected:
            raise WorkerApiError("Child completion batch contains invalid identities", 422)
        for item in results:
            ChildObservationEvidence.capture(item, parent_attempt_id)
        return indexed
