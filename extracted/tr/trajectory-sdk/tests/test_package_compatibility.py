from trajectory.types import Usage as RootUsage
from trajectory.types.inference import Usage


def test_usage_remains_available_from_inference_types() -> None:
  assert Usage is RootUsage
