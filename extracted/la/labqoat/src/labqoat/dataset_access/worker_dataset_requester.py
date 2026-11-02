"""Adapt pinned dataset access to the platform's assignment API."""

from dataclasses import dataclass
from urllib.parse import quote

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.references import AssetRef, ResolvedDatasetRef
from labqoat.storage.worker_asset_source import WorkerAssetSource
from labqoat.worker import WorkerApi


@dataclass(frozen=True, slots=True)
class WorkerDatasetRequester:
    """Use assignment authority to read only one of the worker's pinned inputs."""

    api: WorkerApi
    inputs: tuple[ResolvedDatasetRef[object], ...]

    def authorize(self, reference: AssetRef) -> None:
        """Require the live assignment's authority before every cached-file scope."""
        WorkerAssetSource(self.api).authorize(reference)

    def dataset_request(self, action: str, body: dict[str, JsonValue]) -> object:
        """Fetch the exact manifest or a server-authorized dataset asset."""
        from labqoat.dataset_access.revision_files import RevisionFiles

        selected = self._input(JsonDocument.expect_scalar(body["revision_id"], str))
        if action == "manifest":
            path = f"/api/v1/worker/datasets/manifest?ref={quote(str(selected.revision_id), safe='')}"
            response = self.api.json("GET", path)
            return RevisionFiles.capture(response, selected)
        if action == "download":
            digest = JsonDocument.expect_scalar(body["sha256"], str)
            from labqoat.references import Sha256

            Sha256.parse(digest)
            return WorkerAssetSource(self.api)
        raise ValueError("Unknown worker dataset action")

    def _input(self, revision_id: str) -> ResolvedDatasetRef[object]:
        """Reject manifest requests for undeclared revisions."""
        for reference in self.inputs:
            if str(reference.revision_id) == revision_id:
                return reference
        raise ValueError("Dataset is not an input of this run")
