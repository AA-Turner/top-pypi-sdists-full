"""What a rollout's episodes came to, together."""

from dataclasses import dataclass
from statistics import fmean

from labqoat.rl.episode_record import EpisodeRecord


@dataclass(frozen=True)
class RolloutReport:
    """Every task's episode record, in the order the tasks were given."""

    records: tuple[EpisodeRecord, ...]

    @property
    def rewards(self) -> dict[str, float]:
        """Return each rewarded task's reward by task."""
        return {record.task: record.reward for record in self.records if record.reward is not None}

    @property
    def failed(self) -> tuple[EpisodeRecord, ...]:
        """Return the records of tasks that produced no reward."""
        return tuple(record for record in self.records if not record.completed)

    def mean_reward(self, missing: float | None = None) -> float:
        """Average the rewards; zero when there is nothing to average.

        Tasks without a reward are left out unless ``missing`` gives them one. Leaving them out flatters a
        policy whose hard tasks are the ones that time out, so pass the reward a failure deserves when the
        number is compared between policies.
        """
        rewards = list(self.rewards.values())
        if missing is not None:
            rewards.extend([missing] * len(self.failed))
        return fmean(rewards) if rewards else 0.0

    def solve_rate(self, threshold: float = 1.0) -> float:
        """Return the share of all tasks whose reward reached ``threshold``; a task without a reward did not.

        A policy learns little from tasks it always or never solves, so check this before training on a set.
        """
        solved = sum(1 for reward in self.rewards.values() if reward >= threshold)
        return solved / len(self.records) if self.records else 0.0

    def metrics(self) -> dict[str, float]:
        """Summarize the rollout as numbers a run can log for one step."""
        return {
            "episodes": float(len(self.records)),
            "episodes_failed": float(len(self.failed)),
            "reward_mean": self.mean_reward(),
            "episode_seconds_mean": fmean(record.seconds for record in self.records) if self.records else 0.0,
        }
