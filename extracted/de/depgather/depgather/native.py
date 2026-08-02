"""
Define NativeInferState with a static gather method, which takes a requirementsPath.

In addition to a series of optional arguments for gathering requirements/ deps based on the
requirementsPath.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from configparser import ConfigParser, ParsingError
from importlib import metadata
from importlib.metadata._meta import PackageMetadata
from pathlib import Path
from typing import Any, override

import tomli
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from pydantic import BaseModel

from depgather.interface import DepGatherInterface
from depgather.models.cyclonedx import Bom
from depgather.models.spdx import SPDX
from depgather.utils import c14n_reqs, conditional_log, sanitize


class ReqContainer(BaseModel):
	name: str
	version: str | None = None

	def as_requirement(self) -> str:
		if self.version:
			return f"{self.name}=={self.version}"
		return self.name


class NativeInferState:
	def __init__(self) -> None:
		self.reqs: dict[str, Requirement] = {}

	def resolve(
		self,
		skipDependencies: Iterable[str],
	) -> set[Requirement]:
		skip_names: set[str] = {
			canonicalize_name("PYTHON"),
			*(canonicalize_name(d) for d in skipDependencies),
		}
		reqs: dict[str, Requirement] = {
			name: req
			for name, req in self.reqs.items()
			if canonicalize_name(req.name) not in skip_names
		}

		for requirement in reqs.copy().values():
			conditional_log(f"get deps for {requirement=}")
			try:
				pkgMetadata: PackageMetadata = metadata.metadata(requirement.name)
			except metadata.PackageNotFoundError:
				continue

			for dependency_str in pkgMetadata.get_all("Requires-Dist") or []:
				conditional_log(f"... checking {dependency_str}")
				dependency: Requirement = Requirement(dependency_str)

				# Ignore dependencies
				if canonicalize_name(dependency.name) in skip_names:
					continue

				marker = dependency.marker
				depextras: set[str] = dependency.extras | {""}
				conditional_log(f"... with extras={depextras}")
				if marker is not None:
					matched = any(marker.evaluate({"extra": extra}) for extra in depextras)
					if not matched:
						continue

				insertRequirement(reqs, dependency)

		return set(reqs.values())

	def gather_infer(
		self,
		groups: Iterable[str],
		extras: Iterable[str],
		requirementsPath: Path,
	) -> bool:
		self.enabledExtras = {e.lower() for e in extras}

		# determine using based on file type
		try:
			pyproject = tomli.loads(requirementsPath.read_text("utf-8"))

			if pyproject.get("project", {}).get("dependencies") is not None:
				return self.gather_pep631_requirements(
					groups=groups,
					extras=extras,
					pyproject=pyproject,
				)
			if pyproject.get("tool", {}).get("poetry", {}).get("dependencies") is not None:
				return self.gather_poetry_requirements(
					groups=groups,
					pyproject=pyproject,
				)

			return self.gather_requirements(
				requirementsPath=requirementsPath,
			)

		except tomli.TOMLDecodeError:
			# Parse setup.cfg
			try:
				cfg: ConfigParser = ConfigParser()
				cfg.read(requirementsPath)
				return self.gather_setupcfg(cfg, groups)
			except ParsingError:
				# Otherwise its requirements.txt
				return self.gather_requirements(
					requirementsPath=requirementsPath,
				)

	def gather_lock_requirements(
		self, pyproject: dict[str, Any], pakagekey: str = "package"
	) -> bool:
		for pkg in pyproject[pakagekey]:
			self.appendRequirement(
				ReqContainer(name=pkg["name"], version=pkg.get("version")).as_requirement()
			)

		return True

	def gather_cyclonedx_requirements(self, sbom: dict[str, Any]) -> bool:
		sbom_: Bom = Bom.model_validate(sbom)
		for x in sbom_.components:
			if "pkg:pypi/" in x.purl:
				self.appendRequirement(
					ReqContainer(
						name=x.name,
						version=x.version,
					).as_requirement()
				)

		return True

	def gather_spdx_requirements(self, sbom: dict[str, Any]) -> bool:
		sbom_: SPDX = SPDX.model_validate(sbom)
		for x in sbom_.packages:
			self.appendRequirement(
				ReqContainer(
					name=x.name,
					version=x.version_info,
				).as_requirement()
			)

		return True

	def gather_setupcfg(
		self,
		cfg: ConfigParser,
		groups: Iterable[str],
	) -> bool:
		requirements = [
			line.strip()
			for line in cfg.get("options", "install_requires", fallback="").splitlines()
			if line.strip()
		]
		for req in requirements:
			self.appendRequirement(req)
		_groups = {
			key: [line.strip() for line in value.splitlines() if line.strip()]
			for key, value in cfg["options.extras_require"].items()
		}
		for group in groups:
			group_reqs = _groups.get(group)
			if group_reqs:
				for req in group_reqs:
					self.appendRequirement(req)
		return True

	def gather_pep631_requirements(
		self,
		groups: Iterable[str],
		extras: Iterable[str],
		pyproject: dict[str, Any],
	) -> bool:
		try:
			project = pyproject["project"]
			reqLists: list[str] = project["dependencies"]
		except KeyError as error:
			msg = "Could not find specification of requirements (pyproject.toml)."
			raise RuntimeError(msg) from error

		for extra in extras:
			extra_info = project.get("optional-dependencies", {}).get(extra)
			if extra_info:
				reqLists.extend(extra_info)
		for group in groups:
			group_info = pyproject.get("dependency-groups", {}).get(group)
			if group_info:
				reqLists.extend(group_info)

		for req in reqLists:
			self.appendRequirement(req)

		return True

	def gather_poetry_requirements(
		self,
		groups: Iterable[str],
		pyproject: dict[str, Any],
	) -> bool:
		try:
			project = pyproject["tool"]["poetry"]
		except KeyError as error:
			msg = "Could not find specification of requirements (pyproject.toml)."
			raise RuntimeError(msg) from error

		dependency_sections = [project.get("dependencies", {})]

		for group in groups:
			dependency_sections.append(  # noqa: PERF401 # ignore suggestion to use list.extend here
				project.get("group", {}).get(group, {}).get("dependencies", {})
			)

		if "dev" in groups:
			dependency_sections.append(project.get("dev-dependencies", {}))

		for section in dependency_sections:
			for name in section:
				self.appendRequirement(name)

		return True

	def gather_requirements(
		self,
		requirementsPath: Path,
	) -> bool:
		if not requirementsPath.exists():
			msg = f"Could not find specification of requirements ({requirementsPath})."
			raise RuntimeError(msg)

		for _line in requirementsPath.read_text(encoding="utf-8").splitlines():
			line = _line.rstrip("\\").strip()
			if not line or line[0] in {"#", "-"}:
				continue
			self.appendRequirement(line.split("#")[0])

		return True

	def appendRequirement(self, req: str) -> None:
		requirement: Requirement = Requirement(req)
		insertRequirement(map_=self.reqs, requirement=requirement)


def insertRequirement(map_: dict[str, Requirement], requirement: Requirement) -> None:
	name = canonicalize_name(requirement.name)
	requirement.name = name
	conditional_log(f"adding {requirement.name}")
	map_[name] = requirement


class NativeInfer(DepGatherInterface):
	@staticmethod
	@override
	def gather(
		requirementsPath: Path,
		skipDependencies: Iterable[str] = (),
		groups: Iterable[str] = (),
		extras: Iterable[str] = (),
		base_index_url: str = "https://pypi.org",
	) -> set[Requirement]:
		"""
		Static getter method, used to gather requirements/ deps based on the requirementsPath.

		Note this depends entirely on the local environment to identify transitive deps, and this
		only goes one level deep. NativeInfer.gather is only recommended for lockfiles, for project
		files, it is preferred to use uv/pip etc.

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

		state: NativeInferState = NativeInferState()

		# when using a lockfile then gatherinfer only

		try:
			pyproject = tomli.loads(requirementsPath.read_text("utf-8"))
			if pyproject.get("package") is not None and state.gather_lock_requirements(
				pyproject=pyproject,
			):
				return c14n_reqs(state.reqs.values())

			if pyproject.get("packages") is not None and state.gather_lock_requirements(
				pyproject=pyproject, pakagekey="packages"
			):
				return c14n_reqs(state.reqs.values())

		except tomli.TOMLDecodeError:
			pass

		# when using a json sbom, also gatherinfer only
		try:
			sbom = json.loads(requirementsPath.read_text("utf-8"))
			if sbom.get("bomFormat") == "CycloneDX" and state.gather_cyclonedx_requirements(
				sbom=sbom
			):
				return c14n_reqs(state.reqs.values())
			if sbom.get("spdxVersion") is not None and state.gather_spdx_requirements(sbom=sbom):
				return c14n_reqs(state.reqs.values())
		except json.JSONDecodeError:
			pass

		if not state.gather_infer(groups, extras, requirementsPath):
			msg = f"Unable to find requirements for ({requirementsPath})."
			raise RuntimeError(msg)
		return c14n_reqs(state.resolve(skipDependencies))
