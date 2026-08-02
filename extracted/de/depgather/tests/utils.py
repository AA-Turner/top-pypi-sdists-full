import sys

from loguru import logger
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

logger.remove()

logger.add(
	sys.stderr,
	format="{message}",
)


def assert_eq_packages(a: set[Requirement], b: set[str]) -> None:
	lhs = {canonicalize_name(x.name) for x in a}
	rhs = {canonicalize_name(x) for x in b}

	missing = rhs - lhs
	extra = lhs - rhs

	assert lhs == rhs, (
		f"Extra in Expected (RHS): {sorted(missing)}\nExtra in Requirements: {sorted(extra)}"
	)


def assert_not_in_packages(a: set[Requirement], b: str) -> None:
	reqs = {canonicalize_name(d.name) for d in a}
	assert canonicalize_name(b) not in reqs


def assert_in_packages(a: set[Requirement], b: str) -> None:
	reqs = {canonicalize_name(d.name) for d in a}
	assert canonicalize_name(b) in reqs
