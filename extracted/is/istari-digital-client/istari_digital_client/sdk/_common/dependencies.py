"""Dependencies sub-manager (reached via ``istari.systems.dependencies``).

Everything about a branch's packages: what it requires, what it publishes, the folders its
snapshot installs, which ``1.x`` folders have an update, and downloading an exact snapshot.
Every method takes a :class:`Branch` first; :class:`Branch` exposes the same verbs as one-line
conveniences. Publishing is on ``istari.libraries``.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from istari_digital_client.materialization import (
    MaterializationResult,
    materialize_system_tree,
)
from istari_digital_client.sdk._base import Page, _Manager
from istari_digital_client.sdk._common.dependency_types import (
    Publications,
    Requirements,
)
from istari_digital_client.sdk._exceptions import NotFoundError
from istari_digital_client.sdk._common.libraries import Libraries, _pages

if TYPE_CHECKING:
    from istari_digital_client.sdk._common.system_types import Branch
    from istari_digital_client.sdk._generated.v2.models.dependency_resolution_dto import (
        DependencyResolutionDto,
    )
    from istari_digital_client.sdk._generated.v2.models.installed_file_dto import (
        InstalledFileDto,
    )
    from istari_digital_client.sdk._generated.v2.models.requirer_dto import RequirerDto
    from istari_digital_client.sdk._generated.v2.models.resolved_folder_dto import (
        ResolvedFolderDto,
    )


class Dependencies(_Manager):
    """Package requirements, publications, installed folders, updates, and checkout for branches."""

    def requirements(self, branch: Branch) -> Requirements:
        """An editable copy of the branch's requirements; ``add`` without a version takes the newest release."""
        dto = self._call(
            self._engine.v2_api.get_dependencies_manifest,
            branch._system_id,
            branch_id=branch.id,
            snapshot_id=branch.snapshot_id,
        )
        return Requirements.from_manifest(dto.manifest, newest=self._newest_release)

    def publications(self, branch: Branch) -> Publications:
        """An editable copy of the packages the branch publishes."""
        dto = self._call(
            self._engine.v2_api.get_publications_manifest,
            branch._system_id,
            branch_id=branch.id,
            snapshot_id=branch.snapshot_id,
        )
        return Publications.from_manifest(dto.manifest)

    def lock(self, branch: Branch, *, text: bool = False) -> DependencyResolutionDto:
        """A summary of what the branch's snapshot installs: folder, file, and update counts.

        ``text=True`` also returns dependencies.lock.json in ``rendered_lockfile``. The folders
        themselves come from :meth:`packages`, the files from :meth:`files`.
        """
        return self._call(
            self._engine.v2_api.get_dependency_resolution,
            branch.snapshot_id,
            include_lock=text or None,
        )

    def packages(
        self,
        branch: Branch,
        *,
        under: ResolvedFolderDto | RequirerDto | None = None,
        own: bool = False,
        search: str | None = None,
    ) -> Page[ResolvedFolderDto]:
        """The package folders the snapshot installs, in path order.

        ``under`` (a row of this listing, or one of its ``required_by``) lists only the folders
        that folder's version requires; ``own`` only those dependencies.yaml requires; ``search``
        those whose library or package key matches. Each row has the version the folder holds,
        what requires it, and, for a ``1.x`` folder with a newer release, ``update_version``.
        """
        return _pages(
            self,
            self._engine.v2_api.list_resolved_packages,
            branch.snapshot_id,
            requirer_package_id=under.package_id if under else None,
            requirer_folder=under.folder if under else None,
            own=own or None,
            search=search,
        )

    def files(
        self, branch: Branch, *, under: str | None = None, search: str | None = None
    ) -> Page[InstalledFileDto]:
        """The package files the snapshot puts in the tree, placements included, optionally under a folder.

        A large System installs tens of thousands of files; iterating fetches them page by page.
        """
        return _pages(
            self,
            self._engine.v2_api.list_resolved_files,
            branch.snapshot_id,
            prefix=under,
            search=search,
        )

    def updates(self, branch: Branch) -> Page[ResolvedFolderDto]:
        """The ``1.x`` folders whose line has a newer release (``update_version``) than the version they hold.

        Apply one with ``branch.preview(update=row).commit()``, or all with ``update="all"``.
        """
        return _pages(
            self,
            self._engine.v2_api.list_resolved_packages,
            branch.snapshot_id,
            updates_only=True,
        )

    def checkout(
        self,
        branch: Branch,
        destination: str | os.PathLike[str],
        *,
        overwrite: bool = False,
    ) -> MaterializationResult:
        """Download the branch's exact snapshot, package folders and the lock included, under ``destination``.

        Raises ``PackageContentDeniedError`` naming the files the current user may not read;
        nothing is written in that case.
        """
        return materialize_system_tree(
            self._engine.v2_api, branch.snapshot_id, destination, overwrite=overwrite
        )

    def _newest_release(self, name: str) -> str:
        """The newest active release of a package, not a pre-release: what a new requirement takes."""
        release = Libraries(self._engine).package(name).newest_release
        if release is None:
            raise NotFoundError(f"{name} has no active release")
        return release.version
