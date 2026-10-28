"""Hand-written types for a branch's packages: requirements, publications, updates, and previews.

``Requirements`` and ``Publications`` are editable builders that render to the generated
manifest models (dependencies.yaml and publications.yaml). ``Preview`` is the result of
``branch.preview(...)``, and
``PublishPreview`` the result of ``branch.preview_publish(...)``; each can be committed or
published in place.

Packages are named ``library/package``.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Iterable, Iterator, List

from istari_digital_client._package_names import split_package_name
from istari_digital_client.sdk._base import ClientHaving
from istari_digital_client.sdk._generated.v2.models.branch_commit_preview_dto import (
    BranchCommitPreviewDto,
)
from istari_digital_client.sdk._generated.v2.models.dependencies_manifest import (
    DependenciesManifest,
)
from istari_digital_client.sdk._generated.v2.models.dependency_update import (
    DependencyUpdate,
)
from istari_digital_client.sdk._generated.v2.models.folder_ref import FolderRef
from istari_digital_client.sdk._generated.v2.models.package_name import PackageName
from istari_digital_client.sdk._generated.v2.models.placement import Placement
from istari_digital_client.sdk._generated.v2.models.publication_definition import (
    PublicationDefinition,
)
from istari_digital_client.sdk._generated.v2.models.publications_manifest import (
    PublicationsManifest,
)
from istari_digital_client.sdk._generated.v2.models.requirement import Requirement
from istari_digital_client.sdk._generated.v2.models.resolved_folder_dto import (
    ResolvedFolderDto,
)
from istari_digital_client.sdk._generated.v3.models.package_publication_preview_dto import (
    PackagePublicationPreviewDto,
)

if TYPE_CHECKING:
    from istari_digital_client.sdk._common.branches import Branches
    from istari_digital_client.sdk._common.libraries import Libraries
    from istari_digital_client.sdk._common.library_types import PackageVersion
    from istari_digital_client.sdk._common.system_types import Branch
    from istari_digital_client.sdk._generated.v2.models.resolution_change_dto import (
        ResolutionChangeDto,
    )
    from istari_digital_client.sdk._generated.v3.models.package_publication_dto import (
        PackagePublicationDto,
    )

_VERSION = re.compile(r"^(0|[1-9]\d*)(?:\.(0|[1-9]\d*)(?:\.(0|[1-9]\d*)([-+].*)?)?)?$")


def folder_name(version: str, updates: str = "minor") -> str:
    """The folder a requirement installs into: ``1.x`` for minor updates, ``1.2.x`` for patches, the pinned version for none.

    ``"1"`` and ``"1.2"`` mean ``1.0.0`` and ``1.2.0``, as they do on the server.
    """
    match = _VERSION.fullmatch(version.strip())
    if match is None:
        raise ValueError(f"{version!r} is not a version number such as 1.2.0")
    major, minor, patch, suffix = match.groups()
    if updates == "minor":
        return f"{major}.x"
    if updates == "patch":
        return f"{major}.{minor or 0}.x"
    return f"{major}.{minor or 0}.{patch or 0}{suffix or ''}"


def package_name(name: str) -> dict[str, str]:
    """The manifest keys for ``library/package``."""
    library, package = split_package_name(name)
    return {"library": library, "package": package}


def _updates(entry: Requirement) -> str:
    return entry.updates.value if entry.updates else "minor"


def _label(entry: Any) -> str:
    return f"{entry.library}/{entry.package}"


class Requirements:
    """The packages a branch requires: its dependencies.yaml.

    A requirement takes minor updates from a version (installed in ``.istari-deps/<library>/<package>/1.x``),
    only patches (``.../1.2.x``), or is pinned to it (``.../1.2.1``). A package is required at most
    once per major version, so ``1.x`` and ``2.x`` can be installed side by side.

    Edit with :meth:`add` and :meth:`remove`, then ``branch.preview(reqs)`` and
    ``preview.commit()``, or ``branch.commit(dependencies=reqs, resolve=True)``.
    """

    def __init__(
        self,
        requirements: Iterable[Requirement] = (),
        *,
        newest: Callable[[str], str] | None = None,
    ) -> None:
        """Start from existing requirements; ``newest`` maps a package name to its newest release."""
        self._entries: List[Requirement] = list(requirements)
        self._newest = newest

    @classmethod
    def from_manifest(
        cls,
        manifest: DependenciesManifest | None,
        *,
        newest: Callable[[str], str] | None = None,
    ) -> Requirements:
        """Wrap a manifest returned by the server."""
        return cls(manifest.dependencies or [] if manifest else [], newest=newest)

    def add(
        self,
        package: str,
        version: str | None = None,
        *,
        updates: str = "minor",
        place: dict[str, str] | None = None,
    ) -> Requirements:
        """Require ``package``, named ``library/package``.

        ``updates`` is ``"minor"`` (take later 1.x releases), ``"patch"`` (later 1.2.x only) or
        ``"none"`` (pinned to ``version``). ``version`` defaults to the package's newest release. ``place`` maps paths in the package to System
        paths where the file or folder should also appear; without it, a replaced requirement
        keeps its placements.

        A requirement of the same package and major version is replaced, so
        ``add(name, "1.1.0", updates="none")`` pins a ``1.x`` requirement to 1.1.0, and
        ``add(name, "2.0.0")`` installs ``2.x`` next to ``1.x``.
        """
        if version is None:
            if self._newest is None:
                raise ValueError(
                    f"give a version for {package}; requirements read from a branch "
                    "look up the newest release"
                )
            version = self._newest(package)
        major = folder_name(version)
        replaced = [
            i
            for i, e in enumerate(self._entries)
            if _label(e) == package and folder_name(e.version) == major
        ]
        fields: dict[str, Any] = {
            **package_name(package),
            "version": version,
            "updates": updates,
        }
        if place is not None:
            fields["placements"] = [
                Placement.model_validate({"from": src, "to": dst})
                for src, dst in place.items()
            ] or None
        elif replaced and self._entries[replaced[0]].placements:
            fields["placements"] = self._entries[replaced[0]].placements
        requirement = Requirement(**fields)
        if replaced:
            self._entries[replaced[0]] = requirement
            for i in reversed(replaced[1:]):
                del self._entries[i]
        else:
            self._entries.append(requirement)
        return self

    def remove(self, package: str, *, folder: str | None = None) -> Requirements:
        """Stop requiring ``package``, or only its ``folder`` (such as ``"1.x"``); a missing one is not an error."""
        self._entries = [
            e
            for e in self._entries
            if not (
                _label(e) == package
                and folder in (None, folder_name(e.version, _updates(e)))
            )
        ]
        return self

    def to_manifest(self) -> DependenciesManifest:
        """The generated manifest model a commit sends."""
        return DependenciesManifest(dependencies=list(self._entries))

    def __iter__(self) -> Iterator[Requirement]:
        return iter(self._entries)

    def __len__(self) -> int:
        return len(self._entries)

    def __repr__(self) -> str:
        rules = {"minor": "", "patch": " patches only", "none": " pinned"}
        parts = [f"{_label(e)} {e.version}{rules[_updates(e)]}" for e in self._entries]
        return "Requirements(" + ", ".join(parts) + ")"


class Publications:
    """The packages a branch publishes: its publications.yaml.

    Each package is a named selection of the System's files and folders, published at their
    System paths. It requires what the System requires, less the packages in ``leave_out``.
    """

    def __init__(self, definitions: Iterable[PublicationDefinition] = ()) -> None:
        """Start from existing definitions (usually the branch's current manifest)."""
        self._entries: List[PublicationDefinition] = list(definitions)

    @classmethod
    def from_manifest(cls, manifest: PublicationsManifest | None) -> Publications:
        """Wrap a manifest returned by the server."""
        return cls(manifest.packages or [] if manifest else [])

    def add(
        self,
        package: str,
        files: Iterable[str],
        *,
        description: str | None = None,
        exclude: Iterable[str] = (),
        leave_out: Iterable[str] = (),
    ) -> Publications:
        """Publish ``files`` (System paths of files or folders) as ``package`` (``library/package``).

        A folder includes everything under it, files added later too; ``exclude`` lists paths
        under ``files`` to leave out. ``leave_out`` names packages the System requires that
        this package does not. The System's placements inside ``files`` travel with the
        package. Re-adding a package replaces its entry.
        """
        self.remove(package)
        fields: dict[str, Any] = {
            **package_name(package),
            "files": list(files),
        }
        if description is not None:
            fields["description"] = description
        if exclude:
            fields["exclude"] = list(exclude)
        if leave_out:
            fields["leave_out"] = [
                PackageName.model_validate(package_name(name)) for name in leave_out
            ]
        self._entries.append(PublicationDefinition(**fields))
        return self

    def remove(self, package: str) -> Publications:
        """Stop publishing ``package``; a missing one is not an error."""
        self._entries = [e for e in self._entries if _label(e) != package]
        return self

    def to_manifest(self) -> PublicationsManifest:
        """The generated manifest model a commit sends."""
        return PublicationsManifest(packages=list(self._entries))

    def __iter__(self) -> Iterator[PublicationDefinition]:
        return iter(self._entries)

    def __len__(self) -> int:
        return len(self._entries)

    def __repr__(self) -> str:
        return "Publications(" + ", ".join(_label(e) for e in self._entries) + ")"


# Which ``1.x`` folders a commit moves to the newest release of their line: ``"all"``, or folder
# rows from ``branch.updates()`` or ``branch.packages()``.
FolderUpdates = str | ResolvedFolderDto | Iterable[ResolvedFolderDto]


def dependency_update(update: FolderUpdates) -> DependencyUpdate:
    """The commit's update request: ``"all"`` for every ``1.x`` folder, or the given folder rows.

    Rows come from ``branch.updates()`` or ``branch.packages()``; only their ``package_id`` and
    ``folder`` are sent.
    """
    if isinstance(update, str):
        if update != "all":
            raise ValueError(
                f'update must be "all" or folders from branch.updates(), not {update!r}'
            )
        return DependencyUpdate(all=True)
    rows = [update] if isinstance(update, ResolvedFolderDto) else list(update)
    if not rows:
        raise ValueError("no updates given")
    return DependencyUpdate(
        folders=[
            FolderRef(package_id=row.package_id, folder=row.folder) for row in rows
        ]
    )


class Preview(BranchCommitPreviewDto, ClientHaving):
    """What a commit would install, as changes against the branch head; from ``branch.preview(...)``.

    ``package_count`` and ``file_count`` describe the result; ``file_count`` counts only the
    files the caller may view. ``changes`` lists what differs from the head, split into
    :attr:`package_changes` and :attr:`placement_changes`. Check ``warnings`` and ``errors``,
    then :meth:`commit`. The commit carries this preview's id, so the server refuses it if the
    versions it would install have changed since.
    """

    _TRANSIENT_ATTRS: ClassVar[frozenset[str]] = frozenset({"_mgr", "_branch"})

    if TYPE_CHECKING:
        _mgr: Branches
        _branch: Branch
        _dependencies: Any
        _update: Any

    @classmethod
    def _bind_preview(
        cls, dto: Any, *, mgr: Any, branch: Branch, dependencies: Any, update: Any
    ) -> Preview:
        preview = cls._bind(dto, mgr=mgr)
        object.__setattr__(preview, "_branch", branch)
        object.__setattr__(preview, "_dependencies", dependencies)
        object.__setattr__(preview, "_update", update)
        return preview

    @property
    def package_changes(self) -> List[ResolutionChangeDto]:
        """Package folders the commit adds, removes, or moves to another version.

        ``folder`` is the folder after the change, or the removed one; on a changed row
        ``previous_version`` is the version the head has in it. A folder's files move with it,
        so they are not listed.
        """
        return [change for change in self.changes or [] if change.folder is not None]

    @property
    def placement_changes(self) -> List[ResolutionChangeDto]:
        """Placed files the commit adds, changes, or removes; ``file`` is the placement."""
        return [change for change in self.changes or [] if change.file is not None]

    @property
    def ok(self) -> bool:
        """True when the preview has no errors."""
        return not self.errors

    def commit(self, *, message: str | None = None) -> Branch:
        """Commit exactly this plan to the branch; raises ConflictError if it no longer holds."""
        if self.errors:
            raise ValueError(
                "the preview has errors and cannot be committed: "
                + "; ".join(f"{e.code}: {e.message}" for e in self.errors)
            )
        return self._mgr.commit(
            self._branch,
            dependencies=self._dependencies,
            resolve=True,
            update=self._update,
            preview_id=self.preview_id,
            message=message,
        )


class PublishPreview(PackagePublicationPreviewDto, ClientHaving):
    """What publishing a package would do; from ``branch.preview_publish(...)``.

    ``suggested_version`` is the next minor version after ``latest_version`` (the next patch
    below 1.0), and ``removed_file_count`` says how many of its files this one drops. ``changes`` lists the files added, changed or removed (the first few hundred of
    ``change_count``). ``file_count`` and ``requirement_count`` describe the new version.
    """

    if TYPE_CHECKING:
        _mgr: Libraries
        _request: PackagePublicationDto

    @classmethod
    def _bind_request(cls, dto: Any, *, mgr: Any, request: Any) -> PublishPreview:
        preview = cls._bind(dto, mgr=mgr)
        object.__setattr__(preview, "_request", request)
        return preview

    def publish(
        self, *, version: str | None = None, release_notes: str | None = None
    ) -> PackageVersion:
        """Publish the previewed source, at ``version`` or else the previewed or suggested version."""
        chosen = version or self.version or self.suggested_version
        return self._mgr._send_publication(
            self._request.model_copy(
                update={"version": chosen, "release_notes": release_notes}
            )
        )
