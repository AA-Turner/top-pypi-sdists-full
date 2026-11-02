"""A terminal authoritative data-publication failure."""

from labqoat._generated.dataset_publication import DatasetPublication
from labqoat.errors.api_error import ApiError


class PublicationFailedError(ApiError):
    """Retain captured revision state and source-located failure evidence."""

    def __init__(self, revision: DatasetPublication) -> None:
        """Expose the failed resource without discarding its validation details."""
        super().__init__(f"Dataset publication {revision.id} failed: {revision.failure}")
        self.revision = revision
