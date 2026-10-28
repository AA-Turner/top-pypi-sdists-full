"""Rich domain objects for libraries and packages (bound by :class:`Libraries`).

``Library`` wraps the v3 library DTO, ``Package`` the catalog row a library lists,
``PackageVersion`` one published version, and ``PackageFile`` one file inside it.
Each object's verbs delegate to the manager that produced it (SDK_REDESIGN.md §5.2).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from istari_digital_client.sdk._base import Archivable, ClientHaving, Page
from istari_digital_client.sdk._exceptions import NotFoundError
from istari_digital_client.sdk._generated.v3.models.library_dto import LibraryDto
from istari_digital_client.sdk._generated.v3.models.package_catalog_item_dto import (
    PackageCatalogItemDto,
)
from istari_digital_client.sdk._generated.v3.models.package_file_dto import (
    PackageFileDto,
)
from istari_digital_client.sdk._generated.v3.models.package_version_dto import (
    PackageVersionDto,
)

if TYPE_CHECKING:
    from istari_digital_client.sdk._common.libraries import Libraries, Packages
    from istari_digital_client.sdk._generated.v3.models.marking_dto import MarkingDto
    from istari_digital_client.sdk._generated.v3.models.library_membership_dto import (
        LibraryMembershipDto,
    )
    from istari_digital_client.sdk._generated.v3.models.library_role import LibraryRole
    from istari_digital_client.sdk._generated.v3.models.package_consumer_dto import (
        PackageConsumerDto,
    )
    from istari_digital_client.sdk._generated.v3.models.package_consumer_reference_dto import (
        PackageConsumerReferenceDto,
    )


class Library(LibraryDto, ClientHaving, Archivable):
    """A library: the namespace packages are published into."""

    if TYPE_CHECKING:
        _mgr: Libraries

    def packages(self, *, search: str | None = None) -> Page[Package]:
        """The packages in this library, by key."""
        return self._mgr.packages.list(self.id, search=search)

    def package(self, key: str) -> Package:
        """One package by key; raises NotFoundError naming the key."""
        return self._mgr.packages.get(self.id, key)

    def members(self) -> List[LibraryMembershipDto]:
        """Current members (user_id, role, owner)."""
        return self._mgr.members.list(self.id)

    def set_members(
        self, members: dict[str, str | LibraryRole | None]
    ) -> List[LibraryMembershipDto]:
        """Give each user id a role, or ``None`` to remove them; see :meth:`Members.set`."""
        return self._mgr.members.set(self.id, members)


class Package(PackageCatalogItemDto, ClientHaving):
    """A package as listed in its library.

    ``current_version`` is the most recently published version, ``newest_release`` the one a
    new requirement takes; either is None before there is one.
    """

    if TYPE_CHECKING:
        _mgr: Packages

    def versions(self) -> Page[PackageVersion]:
        """Every published version, most recently published first."""
        return self._mgr.versions(self.id)

    def latest(self) -> PackageVersion:
        """The newest release, neither withdrawn nor a pre-release; raises NotFoundError if there is none."""
        if self.newest_release is None:
            raise NotFoundError(f"package {self.key} has no active release")
        return self._mgr.version_of(self.id, self.newest_release.version)

    def version(self, version: str) -> PackageVersion:
        """One version by its exact version string."""
        return self._mgr.version_of(self.id, version)

    def consumers(self) -> Page[PackageConsumerDto]:
        """Branches whose head installs this package, each with how many of its folders."""
        return self._mgr.consumers(self.id)

    def actions(self) -> List[str]:
        """What the current user may do with this package (publish, yank, download, ...)."""
        return self._mgr.actions(self.id)


class PackageVersion(PackageVersionDto, ClientHaving):
    """One immutable published version."""

    if TYPE_CHECKING:
        _mgr: Packages

    def files(self) -> Page[PackageFile]:
        """The version's files the current user may view, in path order."""
        return self._mgr.files(self.id)

    def consumers(self) -> List[PackageConsumerReferenceDto]:
        """Every folder a branch head installs that holds this exact version."""
        return [
            c
            for c in self._mgr.consumer_references(self.package_id)
            if c.package_version_id == self.id
        ]

    def yank(self) -> PackageVersion:
        """Withdraw this version: updates never pick it, and folders that hold it keep it."""
        return self._mgr.yank(self.id)

    def restore(self) -> PackageVersion:
        """Undo a withdrawal."""
        return self._mgr.restore(self.id)

    def set_marking(self, marking: MarkingDto) -> PackageVersion:
        """Replace this version's classification and control tags (the package's stewards only)."""
        return self._mgr.set_marking(self.id, marking)


class PackageFile(PackageFileDto, ClientHaving):
    """One file of a package version that the current user may view."""

    if TYPE_CHECKING:
        _mgr: Packages

    def read_bytes(self) -> bytes:
        """Download the file through the package route, which enforces current access."""
        return self._mgr.download(self)

    def read_text(self, encoding: str = "utf-8") -> str:
        """Download and decode the file."""
        return self.read_bytes().decode(encoding)
