import pytest

from depgather.utils import subprocess_run


def test_command_does_not_exist() -> None:
	with pytest.raises(RuntimeError):
		subprocess_run(
			[
				"command_does_not_exist",
				"pip",
				"compile",
				"--color",
				"never",
			]
		)


def test_malformed_command() -> None:
	with pytest.raises(RuntimeError):
		subprocess_run(
			[
				"uv",
				"pip",
				"compile",
				"--color",
				"never",
			]
		)
