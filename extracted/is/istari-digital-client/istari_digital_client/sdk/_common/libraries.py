"""Libraries manager (reached via ``istari.libraries``).

Libraries, their members, and their packages are v3-backed. :meth:`Libraries.publish`
publishes a package a System branch declares in its publications.yaml, at the branch head;
:meth:`Libraries.publish_files` publishes Resource revisions directly, without a System.
Leaving out the version publishes the version the changes suggest.
"""

from __future__ import annotations

from functools import cached_property
from typing import Any, Callable, Iterable, List, TYPE_CHECKING, TypeVar
from uuid import UUID

from istari_digital_client.sdk._base import Page, _Manager
from istari_digital_client.sdk._common.dependency_types import (
    PublishPreview,
    package_name,
)
from istari_digital_client.sdk._common.library_types import (
    Library,
    Package,
    PackageFile,
    PackageVersion,
)
from istari_digital_client.sdk._exceptions import NotFoundError
from istari_digital_client.sdk._generated.storage_api.models.temporary_url import (
    TemporaryURL,
)
from istari_digital_client.sdk._generated.v3.models.files_publication_source_dto import (
    FilesPublicationSourceDto,
)
from istari_digital_client.sdk._generated.v3.models.library_create_dto import (
    LibraryCreateDto,
)
from istari_digital_client.sdk._generated.v3.models.library_membership_batch_update_dto import (
    LibraryMembershipBatchUpdateDto,
)
from istari_digital_client.sdk._generated.v3.models.library_membership_change_dto import (
    LibraryMembershipChangeDto,
)
from istari_digital_client.sdk._generated.v3.models.library_role import LibraryRole
from istari_digital_client.sdk._generated.v3.models.marking_dto import MarkingDto
from istari_digital_client.sdk._generated.v3.models.library_update_dto import (
    LibraryUpdateDto,
)
from istari_digital_client.sdk._generated.v3.models.package_publication_dto import (
    PackagePublicationDto,
)
from istari_digital_client.sdk._generated.v3.models.source import Source
from istari_digital_client.sdk._generated.v3.models.system_publication_source_dto import (
    SystemPublicationSourceDto,
)

if TYPE_CHECKING:
    from istari_digital_client.sdk._common.system_types import Branch
    from istari_digital_client.sdk._generated.v3.models.library_membership_dto import (
        LibraryMembershipDto,
    )
    from istari_digital_client.sdk._generated.v3.models.package_consumer_dto import (
        PackageConsumerDto,
    )
    from istari_digital_client.sdk._generated.v3.models.package_consumer_reference_dto import (
        PackageConsumerReferenceDto,
    )


T = TypeVar("T")


class _Keep:
    """The default of :meth:`Libraries.update`'s arguments: leave that setting as it is."""

    def __repr__(self) -> str:
        return "KEEP"


KEEP: Any = _Keep()


def _pages(
    mgr: _Manager,
    call: Callable[..., Any],
    *args: Any,
    bind: Callable[[Any], T] = lambda dto: dto,
    **filters: Any,
) -> Page[T]:
    """A lazy :class:`Page` over a cursor-paged listing, fetched 100 items (the server's cap) at a time."""
    return mgr._paginate(
        lambda cursor: mgr._call(
            call, *args, cursor=cursor, size=100, include_total=False, **filters
        ),
        bind,
    )


def _is_uuid(value: str) -> bool:
    try:
        UUID(str(value))
    except ValueError:
        return False
    return True


def _revision_id(revision: Any) -> str:
    if isinstance(revision, str):
        return revision
    revision_id = getattr(revision, "file_revision_id", None)
    if revision_id is None:
        raise ValueError(
            f"expected a revision id or a revision object, got {revision!r}"
        )
    return str(revision_id)


class Libraries(_Manager):
    """Create, find, and update libraries; publish packages into them.

    Usage::

        lib = istari.libraries.get("components")                  # key or id
        for package in lib.packages():
            print(package.key, package.current_version)
        gearbox = istari.libraries.package("components/gearbox")
        preview = istari.libraries.preview_publish(branch, "components/gearbox")
        print(preview.suggested_version, preview.changes)
        version = preview.publish(release_notes="Stiffer housing")
    """

    @cached_property
    def packages(self) -> Packages:
        """Packages of any library, keyed by library id (``istari.libraries.packages.get(lib_id, key)``)."""
        return Packages(self._engine)

    @cached_property
    def members(self) -> Members:
        """Membership of any library, keyed by library id."""
        return Members(self._engine)

    # --- capability hooks ---------------------------------------------------

    def _archive(self, obj: Any, *, reason: str | None = None) -> None:
        self._call(self._engine.v3_api.archive_library, obj.id)

    def _restore(self, obj: Any, *, reason: str | None = None) -> None:
        self._call(self._engine.v3_api.restore_library, obj.id)

    # --- CRUD ---------------------------------------------------------------

    def create(
        self,
        key: str,
        *,
        description: str | None = None,
        shared_with_tenant: bool = False,
        control_tag_ids: List[str] | None = None,
        infosec_level_id: str | None = None,
        members: dict[str, str | LibraryRole | None] | None = None,
    ) -> Library:
        """Create a library (tenant administrators only). The key is permanent.

        ``infosec_level_id`` classifies the library itself. ``members`` maps user ids to a role,
        as :meth:`Members.set` takes them.
        """
        dto = self._call(
            self._engine.v3_api.create_library,
            LibraryCreateDto(
                key=key,
                description=description,
                infosec_level_id=infosec_level_id,
            ),
        )
        # The library is created first; sharing and tags are then set, sending only the ones given.
        changes: dict[str, Any] = {}
        if shared_with_tenant:
            changes["shared_with_tenant"] = True
        if control_tag_ids:
            changes["control_tag_ids"] = control_tag_ids
        if changes:
            dto = self._call(
                self._engine.v3_api.update_library,
                dto.id,
                LibraryUpdateDto(**changes),
            )
        library = Library._bind(dto, mgr=self)
        if members:
            self.members.set(library.id, members)
        return library

    def get(self, key_or_id: str) -> Library:
        """Fetch a library by key or id; a missing key raises NotFoundError naming it."""
        if _is_uuid(key_or_id):
            return Library._bind(
                self._call(self._engine.v3_api.get_library, key_or_id), mgr=self
            )
        for library in self.list(search=key_or_id):
            if library.key == key_or_id:
                return library
        raise NotFoundError(f"no library with key {key_or_id!r} is visible to you")

    def list(
        self, *, search: str | None = None, archived: bool | None = None
    ) -> Page[Library]:
        """Libraries visible to the current user."""
        return _pages(
            self,
            self._engine.v3_api.list_libraries,
            search=search,
            archived=archived,
            bind=lambda dto: Library._bind(dto, mgr=self),
        )

    def update(
        self,
        library_id: str,
        *,
        description: str | None = KEEP,
        shared_with_tenant: bool = KEEP,
        control_tag_ids: List[str] = KEEP,
        infosec_level_id: str | None = KEEP,
    ) -> Library:
        """Change description, tenant sharing, or the control tags and classification that gate the library.

        Only the settings passed change. ``description=None`` clears the description and
        ``infosec_level_id=None`` clears the classification.
        """
        changes: dict[str, Any] = {
            name: value
            for name, value in {
                "description": description,
                "shared_with_tenant": shared_with_tenant,
                "control_tag_ids": control_tag_ids,
                "infosec_level_id": infosec_level_id,
            }.items()
            if value is not KEEP
        }
        dto = self._call(
            self._engine.v3_api.update_library,
            library_id,
            LibraryUpdateDto(**changes),
        )
        return Library._bind(dto, mgr=self)

    def package(self, name: str) -> Package:
        """One package by name, ``library/package``; raises NotFoundError naming it."""
        keys = package_name(name)
        return self.packages.get(self.get(keys["library"]).id, keys["package"])

    # --- publishing ---------------------------------------------------------

    def publish(
        self,
        branch: Branch,
        package: str,
        *,
        version: str | None = None,
        release_notes: str | None = None,
        marking: MarkingDto | None = None,
    ) -> PackageVersion:
        """Publish ``package`` (``library/package``) as the branch's publications.yaml declares it.

        The files come from the branch head. ``version`` defaults to the suggested one (see
        :meth:`preview_publish`). ``marking`` defaults to the latest version's. An existing version
        is refused and nothing is written.
        """
        return self._publish(
            _system_source(branch, package), version, release_notes, marking
        )

    def preview_publish(
        self, branch: Branch, package: str, *, version: str | None = None
    ) -> PublishPreview:
        """What publishing ``package`` from the branch head would do: the suggested version and the changes."""
        return self._preview(_system_source(branch, package), version)

    def publish_files(
        self,
        library: Library | str,
        package: str,
        revisions: Iterable[Any],
        *,
        version: str | None = None,
        release_notes: str | None = None,
        description: str | None = None,
        marking: MarkingDto | None = None,
    ) -> PackageVersion:
        """Publish Resource revisions as a version of ``package`` in ``library``, without a System.

        ``revisions`` are revision ids or objects with a ``file_revision_id``; each file sits at
        its name in the package root. ``library`` is a key, an id, or a :class:`Library`; a
        package key new to it creates the package. ``version`` defaults to the suggested one.
        """
        source = FilesPublicationSourceDto(
            library_id=self._library_id(library),
            package=package,
            description=description,
            revision_ids=[_revision_id(revision) for revision in revisions],
        )
        return self._publish(source, version, release_notes, marking)

    def _publish(
        self,
        source: SystemPublicationSourceDto | FilesPublicationSourceDto,
        version: str | None,
        release_notes: str | None,
        marking: MarkingDto | None,
    ) -> PackageVersion:
        if version is None:
            version = self._preview(source, None).suggested_version
        return self._send_publication(
            PackagePublicationDto(
                source=Source(source),
                version=version,
                release_notes=release_notes,
                marking=marking,
            )
        )

    def _preview(
        self,
        source: SystemPublicationSourceDto | FilesPublicationSourceDto,
        version: str | None,
    ) -> PublishPreview:
        request = PackagePublicationDto(source=Source(source), version=version)
        dto = self._call(self._engine.v3_api.preview_package_publication, request)
        return PublishPreview._bind_request(dto, mgr=self, request=request)

    def _send_publication(self, request: PackagePublicationDto) -> PackageVersion:
        dto = self._call(self._engine.v3_api.publish_package, request)
        return self.packages._bind_version(dto)

    def _library_id(self, library: Library | str) -> str:
        if isinstance(library, str):
            return library if _is_uuid(library) else self.get(library).id
        return library.id


def _system_source(branch: Branch, package: str) -> SystemPublicationSourceDto:
    return SystemPublicationSourceDto(branch_id=branch.id, **package_name(package))


class Members(_Manager):
    """Membership of a library, keyed by library id. Each member has one role."""

    def list(self, library_id: str) -> List[LibraryMembershipDto]:
        """Current members: ``user_id``, ``role``, and ``owner`` (the owner has no role and holds every one)."""
        return list(self._call(self._engine.v3_api.list_library_members, library_id))

    def set(
        self, library_id: str, members: dict[str, str | LibraryRole | None]
    ) -> List[LibraryMembershipDto]:
        """Give each user id a role (``reader``, ``publisher``, or ``maintainer``); ``None`` removes the member.

        Each role includes the ones before it: readers see and use the packages, publishers also
        create and publish them, maintainers also manage members, tags, and withdrawn versions.
        Members not named keep their role.
        """
        changes = [
            LibraryMembershipChangeDto(
                user_id=user_id, role=None if role is None else LibraryRole(role)
            )
            for user_id, role in members.items()
        ]
        return list(
            self._call(
                self._engine.v3_api.set_library_members,
                library_id,
                LibraryMembershipBatchUpdateDto(members=changes),
            )
        )


class Packages(_Manager):
    """Packages and versions of any library, keyed by library or package id."""

    def _bind_version(self, dto: Any) -> PackageVersion:
        return PackageVersion._bind(dto, mgr=self)

    def list(self, library_id: str, *, search: str | None = None) -> Page[Package]:
        """The library's catalog rows."""
        return _pages(
            self,
            self._engine.v3_api.list_library_packages,
            library_id,
            search=search,
            bind=lambda dto: Package._bind(dto, mgr=self),
        )

    def get(self, library_id: str, key: str) -> Package:
        """One package by key within a library."""
        for package in self.list(library_id, search=key):
            if package.key == key:
                return package
        raise NotFoundError(f"no package {key!r} in library {library_id}")

    def actions(self, package_id: str) -> List[str]:
        """The current user's allowed actions on a package."""
        dto = self._call(self._engine.v3_api.get_package, package_id)
        return [getattr(a, "value", a) for a in dto.allowed_actions]

    def versions(self, package_id: str) -> Page[PackageVersion]:
        """Published versions, most recently published first."""
        return _pages(
            self,
            self._engine.v3_api.list_package_versions,
            package_id,
            bind=self._bind_version,
        )

    def version_of(self, package_id: str, version: str) -> PackageVersion:
        """One version by exact version string."""
        for candidate in self.versions(package_id):
            if candidate.version == version:
                return candidate
        raise NotFoundError(f"package {package_id} has no version {version}")

    def version(self, version_id: str) -> PackageVersion:
        """One version by id."""
        return self._bind_version(
            self._call(self._engine.v3_api.get_package_version, version_id)
        )

    def files(self, version_id: str) -> Page[PackageFile]:
        """A version's files the current user may view, in path order."""
        return _pages(
            self,
            self._engine.v3_api.list_package_version_files,
            version_id,
            recursive=True,
            bind=lambda node: PackageFile._bind(node.file, mgr=self),
        )

    def consumers(self, package_id: str) -> Page[PackageConsumerDto]:
        """Branches whose head installs the package, with how many of its folders."""
        return _pages(
            self, self._engine.v3_api.list_package_consuming_systems, package_id
        )

    def consumer_references(
        self, package_id: str, *, system_id: str | None = None
    ) -> Page[PackageConsumerReferenceDto]:
        """Every folder of the package a branch head installs, optionally within one System."""
        return _pages(
            self,
            self._engine.v3_api.list_package_consumer_references,
            package_id,
            system_id=system_id,
        )

    def yank(self, version_id: str) -> PackageVersion:
        """Withdraw a version: updates never pick it, and folders that hold it keep it."""
        return self._bind_version(
            self._call(self._engine.v3_api.yank_package_version, version_id)
        )

    def restore(self, version_id: str) -> PackageVersion:
        """Undo a withdrawal."""
        return self._bind_version(
            self._call(self._engine.v3_api.restore_package_version, version_id)
        )

    def set_marking(self, version_id: str, marking: MarkingDto) -> PackageVersion:
        """Replace a published version's classification and control tags (the package's stewards only)."""
        return self._bind_version(
            self._call(
                self._engine.v3_api.set_package_version_marking, version_id, marking
            )
        )

    def download(self, file: PackageFile) -> bytes:
        """Download one package file; the route enforces current package, tag, and level access."""
        grant = self._call(self._engine.v3_api.download_package_version_file, file.id)
        return bytes(
            self._call(
                self._engine.storage_api._download,  # noqa: SLF001
                TemporaryURL(url=grant.url, expires=grant.expires),
            )
        )
