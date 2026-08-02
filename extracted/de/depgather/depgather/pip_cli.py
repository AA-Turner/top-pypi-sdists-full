"""
Define PipResolver with a static gather method, which takes a requirementsPath.

In addition to a series of optional arguments for gathering requirements/ deps based on the
requirementsPath.
"""

from __future__ import annotations

import json
import tempfile
from collections.abc import Iterable
from pathlib import Path
from typing import override

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

from depgather.interface import DepGatherInterface
from depgather.utils import c14n_reqs, sanitize, subprocess_run


class PipResolver(DepGatherInterface):
	@override
	@staticmethod
	def gather(
		requirementsPath: Path,
		skipDependencies: Iterable[str] = (),
		groups: Iterable[str] = (),  # ignored
		extras: Iterable[str] = (),  # ignored
		base_index_url: str = "https://pypi.org/simple",
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
		:raises RuntimeError: in the event that NativeInfer fails to parse the requirementsPath, or
			encounters some other RuntimeError

		:return set[Requirement]: set of requirements/ deps based on the requirementsPath and
			optional args
		"""
		sanitize(requirementsPath, skipDependencies, groups, extras, base_index_url)

		requirementsPathName = requirementsPath.as_posix()

		if requirementsPathName.endswith((".lock", ".toml", ".json")):
			msg = "pyproject toml, and lock files, and sboms are not supported."
			raise RuntimeError(msg)

		skip_names = {canonicalize_name(x) for x in skipDependencies}

		with tempfile.TemporaryDirectory() as tmp:
			report_path = Path(tmp) / "report.json"

			command = [
				"pip",
				"install",
				"--no-color",
				"--dry-run",
				"--quiet",
				"--report",
				str(report_path),
				"--index-url",
				base_index_url,
				"-r",
				str(requirementsPath),
			]

			result = subprocess_run(command)

			if result.returncode != 0:
				raise RuntimeError(result.stderr)

			report = json.loads(report_path.read_text())

			_requirements = {
				Requirement(
					f"{canonicalize_name(pkg['metadata']['name'])}=={pkg['metadata']['version']}"
				)
				for pkg in report.get("install", [])
				if canonicalize_name(pkg["metadata"]["name"]) not in skip_names
			}
			return c14n_reqs(_requirements)
