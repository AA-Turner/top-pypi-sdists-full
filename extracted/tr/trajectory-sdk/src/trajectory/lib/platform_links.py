"""Links to customer platform resources and selected run evidence."""

from collections.abc import Sequence
from typing import Literal
from urllib.parse import quote, urlencode, urlsplit

from trajectory import Client


class PlatformLinks:
  def __init__(
    self, organization_key: str, platform_url: str = "https://platform.trajectory.ai"
  ) -> None:
    origin = urlsplit(platform_url)
    if (
      origin.scheme not in {"https", "http"}
      or not origin.netloc
      or origin.username is not None
      or origin.password is not None
      or origin.path not in {"", "/"}
      or origin.query
      or origin.fragment
    ):
      raise ValueError(
        "platform_url must be a trusted HTTP(S) origin without credentials or a path"
      )
    self._root = f"{platform_url.rstrip('/')}/{self._segment(organization_key)}"

  @classmethod
  def from_client(cls, client: Client, platform_url: str | None = None) -> "PlatformLinks":
    """Build production links after one organization lookup; allow an explicit UI origin."""
    if platform_url is None:
      if str(client.base_url).rstrip("/") != "https://api.trajectory.ai":
        raise ValueError("Pass the platform_url associated with this client's API environment")
      platform_url = "https://platform.trajectory.ai"
    # Validate the supplied origin before making the organization request.
    cls("check", platform_url)
    organization = client.organizations.retrieve_current()
    return cls(organization["organization_key"], platform_url)

  @staticmethod
  def _segment(value: str) -> str:
    if not value or value in {".", ".."}:
      raise ValueError(
        "A platform resource identifier must be nonempty and cannot be a dot segment"
      )
    return quote(value, safe="")

  def agent(self, agent_id: str) -> str:
    return f"{self._root}/agents/{self._segment(agent_id)}"

  def spec(self, agent_id: str, bench_id: str) -> str:
    return f"{self.agent(agent_id)}/benchmarks/{self._segment(bench_id)}"

  def evaluation(self, eval_run_id: str, trajectory_id: str | None = None) -> str:
    url = f"{self._root}/evaluate/runs/{self._segment(eval_run_id)}/trajectories"
    return f"{url}?{urlencode({'tid': trajectory_id})}" if trajectory_id is not None else url

  def comparison(self, agent_id: str, bench_id: str, eval_run_ids: Sequence[str]) -> str:
    if isinstance(eval_run_ids, (str, bytes)):
      raise TypeError("eval_run_ids must be a sequence of run IDs, such as [run_id]")
    url = f"{self.agent(agent_id)}/evaluation/{self._segment(bench_id)}"
    query = urlencode([("run", run_id) for run_id in eval_run_ids])
    return f"{url}?{query}" if query else url

  def training(
    self,
    training_run_id: str,
    step: int | None = None,
    trajectory_id: str | None = None,
    task_uid: str | None = None,
    source: Literal["training", "validation"] = "training",
    focus: Literal["errors", "tool-failures", "success", "failed", "mixed"] | None = None,
  ) -> str:
    if step is not None and (isinstance(step, bool) or not isinstance(step, int) or step < 0):
      raise ValueError("step must be a nonnegative integer")
    if trajectory_id is not None and step is None:
      raise ValueError("A training trajectory link needs its recorded step")
    if task_uid is not None and trajectory_id is None:
      raise ValueError("task_uid selects a task for a trajectory")
    if source not in {"training", "validation"}:
      raise ValueError("source must be training or validation")
    if focus not in {None, "errors", "tool-failures", "success", "failed", "mixed"}:
      raise ValueError("Unsupported training focus")
    query = urlencode(
      {
        key: value
        for key, value in {
          "step": step,
          "trajectory": trajectory_id,
          "task": task_uid,
          "source": source if source == "validation" else None,
          "focus": focus,
        }.items()
        if value is not None
      }
    )
    url = f"{self._root}/models/{self._segment(training_run_id)}"
    return f"{url}?{query}" if query else url

  def deployment(self, deployment_id: str) -> str:
    return f"{self._root}/deployments/{self._segment(deployment_id)}"

  def production(self, agent_id: str, trajectory_id: str | None = None) -> str:
    url = f"{self.agent(agent_id)}/production-trajectories"
    return f"{url}/{self._segment(trajectory_id)}" if trajectory_id is not None else url
