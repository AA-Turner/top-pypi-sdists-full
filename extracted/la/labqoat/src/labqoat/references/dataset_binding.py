"""Match authored dataset selectors to already resolved immutable worker inputs."""

from uuid import UUID

from labqoat.references.dataset_ref import DatasetRef
from labqoat.references.resolved_dataset_ref import ResolvedDatasetRef


class DatasetBinding:
    """Respect explicit revision identities without looking up mutable selectors again."""

    @staticmethod
    def select(
        reference: DatasetRef[object], inputs: tuple[ResolvedDatasetRef[object], ...]
    ) -> ResolvedDatasetRef[object]:
        """Require one pinned revision for this argument, even with multiple revisions of a family."""
        try:
            revision = UUID(reference.revision)
        except ValueError:
            revision = None
        matches = [
            item
            for item in inputs
            if item.repository == reference.repository and (revision is None or item.revision_id.value == revision)
        ]
        if len(matches) != 1:
            raise ValueError("Dataset argument requires one matching pinned input")
        if reference.schema_digest is not None and reference.schema_digest != matches[0].schema_digest:
            raise ValueError("Dataset input schema does not match the generated row binding")
        return matches[0]
