import os
import re
import subprocess
from collections.abc import Iterable
from itertools import chain
from pathlib import Path
from subprocess import CompletedProcess
from urllib.parse import urlparse

from loguru import logger
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

NAME_RE = re.compile(r"^(?!-)[A-Za-z0-9_.-]+$")

SUPPORTED_SUFFIXES = {".in", ".txt", ".toml", ".cfg", ".py", ".lock", ".json"}

DEPGATHER_VERBOSE: bool = bool(os.environ.get("DEPGATHER_VERBOSE"))


def sanitize(
	requirementsPath: Path,
	skipDependencies: Iterable[str] = (),
	groups: Iterable[str] = (),
	extras: Iterable[str] = (),
	base_index_url: str = "https://pypi.org",
) -> None:
	try:
		requirementsPath = requirementsPath.resolve(strict=True)
	except OSError as e:
		raise RuntimeError from e

	if not requirementsPath.exists():
		msg = f"Could not find specification of requirements ({requirementsPath})."
		raise RuntimeError(msg)

	if requirementsPath.suffix not in SUPPORTED_SUFFIXES:
		msg = f"unsupported requirements file type: {requirementsPath}"
		raise RuntimeError(msg)

	for x in chain(skipDependencies, groups, extras):
		if not isinstance(x, str):
			msg = f"expected str, got {type(x).__name__}"
			raise RuntimeError(msg)

		if not NAME_RE.fullmatch(x):
			msg = f"invalid name: {x!r}"
			raise RuntimeError(msg)

	parsed = urlparse(base_index_url)

	if not parsed.scheme.startswith("http"):
		msg = f"index URL must use HTTP(S): {base_index_url!r}"
		raise RuntimeError(msg)

	if not parsed.hostname:
		msg = f"invalid index URL: {base_index_url!r}"
		raise RuntimeError(msg)


def c14n_reqs(requirements: Iterable[Requirement]) -> set[Requirement]:
	for req in requirements:
		req.name = canonicalize_name(req.name)

	return set(requirements)


def enable_verbose() -> None:
	"""Mutate a global constant in the event a calling lib opts in for debug purposes."""
	global DEPGATHER_VERBOSE  # noqa: PLW0603
	DEPGATHER_VERBOSE = True


def conditional_log(msg: str) -> None:
	"""Log info if DEPGATHER_VERBOSE is set (env, or explicit opt in via enable_verbose)."""
	if DEPGATHER_VERBOSE:
		logger.info(msg)


def subprocess_run(command: list[str]) -> CompletedProcess[str]:
	try:
		result = subprocess.run(
			command,
			capture_output=True,
			text=True,
			check=False,
		)
		if result.returncode != 0:
			msg = f"Non-zero returncode: {result.stderr}, {result.stdout}"
			raise RuntimeError(msg)

	except OSError as e:
		raise RuntimeError from e
	else:
		return result
