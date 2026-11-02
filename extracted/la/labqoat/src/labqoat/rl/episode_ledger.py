"""Episodes that already have a reward, kept where a later run can find them."""

import os
from pathlib import Path
from threading import Lock

from labqoat.rl.episode_record import EpisodeRecord


class EpisodeLedger:
    """Keep every episode's record in a file, one line each, so an interrupted rollout resumes where it stopped.

    Running the same tasks again with the same ledger starts only those that have no reward yet; a record
    without a reward is history, not an answer. One ledger is one batch of episodes: rewards earned by an
    earlier policy answer for a later one too unless each policy version gets a file of its own. A file in
    the run's scratch directory lasts as long as its worker; a volume outlasts it.
    """

    def __init__(self, path: Path | str) -> None:
        """Name the file without reading or creating it."""
        self._path = Path(path)
        self._writing = Lock()

    def completed(self) -> dict[str, EpisodeRecord]:
        """Return the latest rewarded record of each task; a line cut short by an interruption is ignored."""
        if not self._path.exists():
            return {}
        records: dict[str, EpisodeRecord] = {}
        for line in self._path.read_text().splitlines():
            try:
                record = EpisodeRecord.from_json(line)
            except (KeyError, TypeError, ValueError):
                continue
            if record.completed:
                records[record.task] = record
        return records

    def append(self, record: EpisodeRecord) -> None:
        """Add one record and make it durable before returning; concurrent callers write whole lines in turn."""
        line = record.to_json() + "\n"
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._writing, self._path.open("a") as file:
            file.write(line)
            file.flush()
            os.fsync(file.fileno())
