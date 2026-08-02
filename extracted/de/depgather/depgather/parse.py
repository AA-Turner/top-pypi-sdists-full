from collections.abc import Iterable
from enum import StrEnum, auto
from pathlib import Path
from typing import Any

from packaging.requirements import Requirement

from depgather.native import NativeInfer
from depgather.pip_cli import PipResolver
from depgather.utils import conditional_log
from depgather.uv_cli import UvCli


class ResolverName(StrEnum):
	UV = auto()
	PIP = auto()
	NATIVE = auto()


RESOLVERS: dict[ResolverName, Any] = {
	ResolverName.UV: UvCli,
	ResolverName.PIP: PipResolver,
	ResolverName.NATIVE: NativeInfer,
}


def gather(
	requirementsPath: Path,
	skipDependencies: Iterable[str] = (),
	groups: Iterable[str] = (),
	extras: Iterable[str] = (),
	base_index_url: str = "https://pypi.org",
	preferred_resolver: ResolverName = ResolverName.UV,
) -> set[Requirement]:
	"""
	Resolve dependencies from a Python project specification.

	Attempts to resolve dependencies using uv; pip; and a native resolver if those fail.

	:param Iterable[str] skipDependencies: pkg names to exclude from the returned dependency set.
		Comparison is case-insensitive and applies to resolved package names. , defaults to ()
	:param Iterable[str] groups: Dependency groups to include during resolution. , defaults to ()

		Groups are named collections of dependencies defined by a build
		tool. They are typically used to separate runtime dependencies
		from development, test, documentation, or CI dependencies.
			- "dev"
			- "test"
			- "docs"

	:param Iterable[str] extras: Optional dependency sets. defaults to ()
		Extras allow a package to expose additional functionality that
		requires extra dependencies. They are commonly specified using
		bracket notation such as::

			requests[socks]
			sqlalchemy[postgresql]

			Enabling an extra causes its additional dependencies to be
			included in the resolved dependency graph.
	:param Path requirementsPath: path to a dependency specification file such as:

			- pyproject.toml
			- poetry.toml
			- requirements.txt
			- uv.lock
	:param str base_index_url: Package index URL used for dependency resolution.
		defaults to "https://pypi.org"

	:param ResolverName preferred_resolver: Preferred resolver to use, default=ResolverName.UV

	:return set[Requirement]: set of resolved package requirements. Returned requirements are
		typically pinned to specific versions when the resolver is able to
		determine them.

	:raises runtimeError: If dependency resolution fails in all resolvers.
	"""
	# logic to run each depending on conditions, implicit behavior here
	resolvers = RESOLVERS.copy()

	if preferred_resolver in resolvers:
		conditional_log(f"Using {preferred_resolver}")
		resolver = resolvers[preferred_resolver]
		del resolvers[preferred_resolver]
		try:
			return resolver.gather(
				skipDependencies=skipDependencies,
				groups=groups,
				extras=extras,
				requirementsPath=requirementsPath,
				base_index_url=base_index_url,
			)

		except RuntimeError as e:
			conditional_log(f"Preferred resolver, {preferred_resolver} failed")
			conditional_log(str(e))

	for name, resolver in resolvers.items():
		conditional_log(f"Using {name}")
		try:
			return resolver.gather(
				skipDependencies=skipDependencies,
				groups=groups,
				extras=extras,
				requirementsPath=requirementsPath,
				base_index_url=base_index_url,
			)

		except RuntimeError as e:
			conditional_log(str(e))

	msg = "All resolvers failed :("
	conditional_log(msg)
	raise RuntimeError(msg)
