import pytest

from trajectory._testing import client_for


@pytest.mark.parametrize(
  ("resource", "method", "args", "kwargs"),
  [
    ("datasets", "list", (), {"agent_id": "agent-id"}),
    ("datasets.members", "list", ("dataset-id",), {}),
    ("projects", "list_training_runs", ("agent-id",), {}),
    ("projects", "list_evaluation_runs", ("agent-id",), {}),
    ("rl.runs", "list_step_metrics", ("run-id",), {}),
    ("sft.runs", "list_step_metrics", ("run-id",), {}),
    ("sft.losses", "list_held_out_losses", ("run-id",), {}),
  ],
)
def test_first_page_omits_none_cursor(
  resource: str, method: str, args: tuple[str, ...], kwargs: dict[str, str]
) -> None:
  with client_for({"items": [], "has_more": False, "training_run_id": "run-id"}, 200) as (
    client,
    requests,
  ):
    target = client
    for part in resource.split("."):
      target = getattr(target, part)
    getattr(target, method)(*args, cursor=None, **kwargs)

  assert len(requests) == 1
  assert "cursor" not in requests[0].url.params
