"""
Define UvCli with a static gather method, which takes a requirementsPath.

In addition to a series of optional arguments for gathering requirements/ deps based on the
requirementsPath.

Supports:
- pep631 pyproject.toml
- requirements.in
- requirements.txt
- setup.py
- script.py

"""

from __future__ import annotations

import shutil
import tempfile
from collections.abc import Iterable
from pathlib import Path
from typing import override

import requirements
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

from depgather.interface import DepGatherInterface
from depgather.utils import c14n_reqs, sanitize, subprocess_run


class UvCli(DepGatherInterface):
	@staticmethod
	@override
	def gather(
		requirementsPath: Path,
		skipDependencies: Iterable[str] = (),
		groups: Iterable[str] = (),
		extras: Iterable[str] = (),
		base_index_url: str = "https://pypi.org",
	) -> set[Requirement]:
		sanitize(requirementsPath, skipDependencies, groups, extras, base_index_url)

		requirementsPathName = requirementsPath.as_posix()

		if requirementsPathName.endswith((".lock", "lock.toml", ".json")):
			msg = "lock files, and sboms are not supported, use `NativeInfer.gather`."
			raise RuntimeError(msg)

		if not requirementsPathName.endswith("pyproject.toml") and requirementsPathName.endswith(
			".toml"
		):
			temp_dir_path = Path(tempfile.mkdtemp())
			destination_file = temp_dir_path / "pyproject.toml"
			shutil.copy(requirementsPath, destination_file)
			requirementsPathName = destination_file.as_posix()

		command = [
			"uv",
			"pip",
			"compile",
			"--color",
			"never",
			"--index",
			base_index_url,
			requirementsPathName,
		]

		for group in groups:
			command.extend(["--group", group])

		for extra in extras:
			command.extend(["--extra", extra])

		result = subprocess_run(command)

		# outputs a requirements.txt file
		reqs = requirements.parse(result.stdout)

		skipDependencies_c14n = [canonicalize_name(x) for x in skipDependencies]

		_requirements = {
			Requirement(x.line)
			for x in reqs
			if x.name and canonicalize_name(x.name) not in skipDependencies_c14n
		}
		return c14n_reqs(_requirements)
