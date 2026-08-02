"""
Define the DepGatherInterface.

With a static gather method, which takes a requirementsPath, in
addition to a series of optional arguments for gathering requirements/ deps based on the
requirementsPath.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from pathlib import Path

from packaging.requirements import Requirement


class DepGatherInterface(ABC):
	"""Define the DepGatherInterface with a static gather method."""

	@staticmethod
	@abstractmethod
	def gather(
		requirementsPath: Path,
		skipDependencies: Iterable[str] = (),
		groups: Iterable[str] = (),
		extras: Iterable[str] = (),
		base_index_url: str = "https://pypi.org",
	) -> set[Requirement]:
		"""
		Static getter method, used to gather requirements/ deps based on the requirementsPath.

		:param Path requirementsPath: path to some requirements file. e.g. requirements.txt;
			pyproject.toml; uv.lock etc
		:param Iterable[str] skipDependencies: optional dependencies to ignore/ skip. for example
			explicitly choosing to ignore the project. e.g. {'depgather'}, defaults to ()
		:param Iterable[str] groups: dependency groups to include during resolution.
			e.g. {'dev', 'test', 'docs'}, defaults to ()
		:param Iterable[str] extras: dependency sets to enable during resolution. e.g. for depgather
			{"uv", "pip"}, defaults to ()
		:param str base_index_url: pypi index to reach out to to resolve deps,
			defaults to "https://pypi.org"
		:raises NotImplementedError: this is an interface, do not use directly either use an a class
			implementing the interface like `depgather.native.NativeInfer` or
			`depgather.parse.gather`


		:return set[Requirement]: set of requirements/ deps based on the requirementsPath and
			optional args
		"""
		msg = "This is the interface, call from an implemented "
		raise NotImplementedError(msg)
