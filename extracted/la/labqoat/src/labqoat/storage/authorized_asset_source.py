"""One assignment authorization per leased asset, whichever request reaches the service first."""

from pathlib import Path

from labqoat.references import AssetRef
from labqoat.storage.worker_asset_source import WorkerAssetSource


class AuthorizedAssetSource:
    """Let a transfer stand as the authorization it already is, and ask separately only for cached bytes."""

    def __init__(self, source: WorkerAssetSource) -> None:
        """Wrap one assignment-scoped source without contacting the service."""
        self._source = source
        self._transferred: set[AssetRef] = set()

    def download_to(self, reference: AssetRef, destination: Path) -> None:
        """Transfer through the service, which checks this assignment's authority over the exact asset."""
        self._source.download_to(reference, destination)
        self._transferred.add(reference)

    def confirm(self, reference: AssetRef) -> None:
        """Authorize bytes that were already on this node; a transfer just made needs no second request."""
        if reference not in self._transferred:
            self._source.authorize(reference)
