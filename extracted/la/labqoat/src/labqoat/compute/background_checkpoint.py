"""A checkpoint handle returned before its bytes have finished uploading."""

from concurrent.futures import Future

from labqoat.references import CheckpointRef, ResourceId, Sha256


class BackgroundCheckpoint(CheckpointRef[object]):
    """Know the run and step at once; wait for the upload only when the retained identity is read."""

    def __init__(self, upload: Future[CheckpointRef[object]], run_id: ResourceId, step: int) -> None:
        """Bind the pending upload without waiting for it."""
        object.__setattr__(self, "run_id", run_id)
        object.__setattr__(self, "step", step)
        object.__setattr__(self, "_upload", upload)

    @property
    def id(self) -> ResourceId:
        """The retained checkpoint's identity, waiting for the upload if it is still running."""
        return self.result().id

    @property
    def manifest_sha256(self) -> Sha256:
        """The retained manifest digest, waiting for the upload if it is still running."""
        return self.result().manifest_sha256

    def done(self) -> bool:
        """Whether the upload has ended, successfully or not."""
        upload: Future[CheckpointRef[object]] = self.__dict__["_upload"]
        return upload.done()

    def result(self) -> CheckpointRef[object]:
        """Wait for the upload and return the plain retained checkpoint, raising what made it fail."""
        upload: Future[CheckpointRef[object]] = self.__dict__["_upload"]
        return upload.result()

    def __eq__(self, other: object) -> bool:
        """Compare by retained identity, so a background handle equals the checkpoint it became."""
        return self.result() == (other.result() if isinstance(other, BackgroundCheckpoint) else other)

    def __hash__(self) -> int:
        """Hash like the retained checkpoint."""
        return hash(self.result())

    def __repr__(self) -> str:
        """Describe an unfinished upload without waiting for it."""
        if not self.done():
            return f"Checkpoint(run_id={self.run_id!r}, step={self.step}, uploading)"
        return repr(self.result())

    def __reduce__(self) -> tuple[object, ...]:
        """Copy and pickle as the plain retained checkpoint."""
        retained = self.result()
        return (self.retained, (retained.id, retained.run_id, retained.step, retained.manifest_sha256))

    @staticmethod
    def retained(identity: ResourceId, run_id: ResourceId, step: int, manifest_sha256: Sha256) -> CheckpointRef[object]:
        """Rebuild the plain checkpoint a finished upload stands for."""
        return CheckpointRef(id=identity, run_id=run_id, step=step, manifest_sha256=manifest_sha256)
