"""Shared manager-side capability hooks — defined ONCE, composed by managers.

The object capability mixins in :mod:`istari_digital_client._base` (``Readable`` / ``Shareable`` /
``Taggable`` / ``Classifiable``) delegate to manager hooks. Those hook
implementations are generic, so they live here once and a manager opts in by
inheriting the mixin for each capability its objects support — rather than every
manager re-implementing them (SDK_REDESIGN.md §3.2/§5.4).

* :class:`_SupportsRead` — storage-backed content reads (Resource,
  ResourceRevision, Comment all use it).
* :class:`_SupportsAccess` / :class:`_SupportsControlTags` / :class:`_SupportsInfosec`
  — the v2-backed access / control-tag / infosec capabilities. These are keyed by an
  object's ``(kind, id)``, which the composing manager supplies via :meth:`_acl_ref`.
"""

from __future__ import annotations

from typing import Any

from istari_digital_client.sdk._base import _Manager
from istari_digital_client.sdk._generated.v2.models.access_relation import AccessRelation
from istari_digital_client.sdk._generated.v2.models.access_relationship import AccessRelationship
from istari_digital_client.sdk._generated.v2.models.access_resource_type import AccessResourceType
from istari_digital_client.sdk._generated.v2.models.access_subject_type import AccessSubjectType
from istari_digital_client.sdk._generated.v2.models.assign_infosec_level import AssignInfosecLevel
from istari_digital_client.sdk._generated.v2.models.infosec_level_object_type import InfosecLevelObjectType
from istari_digital_client.sdk._generated.v2.models.patch_op import PatchOp
from istari_digital_client.sdk._generated.v2.models.update_access_relationship import (
    UpdateAccessRelationship,
)


def _coerce_enum(enum_cls: Any, value: Any, argname: str) -> Any:
    """Coerce a string into ``enum_cls`` case-insensitively, raising a clear
    ``ValueError`` instead of the cryptic generated one.

    This keeps bad/unsupported values (e.g. infosec on a ``file`` resource, whose
    kind has no ``InfosecLevelObjectType`` member, or a wrong-case ``relation``)
    from surfacing as an opaque enum error from deep in the call. Enum members
    (which are ``str`` subclasses) round-trip unchanged.
    """
    if not isinstance(value, str):
        return value
    try:
        return enum_cls(value.lower())
    except ValueError:
        valid = ", ".join(m.value for m in enum_cls)
        raise ValueError(
            f"{argname} must be one of: {valid}; got {value!r}"
        ) from None


# resource kind -> (get_control_taggings, patch_control_taggings) v2 endpoint names.
# Control tags are typed per kind (no generic endpoint), so dispatch by kind here.
_CONTROL_TAG_ENDPOINTS = {
    "model": ("get_model_control_taggings", "patch_model_control_taggings"),
    "artifact": ("get_artifact_control_taggings", "patch_artifact_control_taggings"),
    "file": ("get_file_control_taggings", "patch_file_control_taggings"),
}


class _SupportsRead(_Manager):
    """Readable hook: read an object's content blob via storage."""

    def _read_contents(self, obj: Any) -> bytes:
        return self._engine.storage.read_contents(obj.content_token)


class _AclManager(_Manager):
    """Base for managers whose objects have a v2 ``(kind, id)`` identity."""

    def _acl_ref(self, obj: Any) -> tuple[str, str]:
        """Return ``(kind, id)`` for ``obj`` — overridden per manager."""
        raise NotImplementedError


class _SupportsAccess(_AclManager):
    """Shareable hooks: manage access relationships via the generic v2 endpoints."""

    def _create_access(
        self, obj: Any, *, subject_type: str, subject_id: str, relation: str
    ) -> Any:
        kind, resource_id = self._acl_ref(obj)
        return self._call(
            self._engine.v2_api.create_access,
            access_relationship=AccessRelationship(
                subject_type=_coerce_enum(AccessSubjectType, subject_type, "subject_type"),
                subject_id=subject_id,
                relation=_coerce_enum(AccessRelation, relation, "relation"),
                resource_type=_coerce_enum(AccessResourceType, kind, "resource kind"),
                resource_id=resource_id,
            ),
        )

    def _update_access(
        self, obj: Any, *, subject_type: str, subject_id: str, relation: str
    ) -> Any:
        kind, resource_id = self._acl_ref(obj)
        return self._call(
            self._engine.v2_api.update_access,
            _coerce_enum(AccessSubjectType, subject_type, "subject_type"),
            subject_id,
            _coerce_enum(AccessResourceType, kind, "resource kind"),
            resource_id,
            update_access_relationship=UpdateAccessRelationship(
                relation=_coerce_enum(AccessRelation, relation, "relation")
            ),
        )

    def _remove_access(self, obj: Any, *, subject_type: str, subject_id: str) -> None:
        kind, resource_id = self._acl_ref(obj)
        self._call(
            self._engine.v2_api.remove_access,
            _coerce_enum(AccessSubjectType, subject_type, "subject_type"),
            subject_id,
            _coerce_enum(AccessResourceType, kind, "resource kind"),
            resource_id,
        )

    def _list_access(self, obj: Any) -> Any:
        kind, resource_id = self._acl_ref(obj)
        return self._call(
            self._engine.v2_api.list_access,
            _coerce_enum(AccessResourceType, kind, "resource kind"),
            resource_id,
        )


class _SupportsControlTags(_AclManager):
    """Taggable hooks: control tags via the per-kind v2 endpoints."""

    def _control_tag_fns(self, obj: Any) -> tuple[Any, Any]:
        kind, _ = self._acl_ref(obj)
        try:
            get_name, patch_name = _CONTROL_TAG_ENDPOINTS[kind]
        except KeyError as exc:
            raise NotImplementedError(
                f"control tags are not supported for kind {kind!r}"
            ) from exc
        return (
            getattr(self._engine.v2_api, get_name),
            getattr(self._engine.v2_api, patch_name),
        )

    def _list_control_tags(self, obj: Any) -> Any:
        get_fn, _ = self._control_tag_fns(obj)
        return self._call(get_fn, self._acl_ref(obj)[1])

    def _add_control_tags(
        self, obj: Any, tag_ids: Any, *, reason: str | None = None
    ) -> Any:
        _, patch_fn = self._control_tag_fns(obj)
        return self._call(
            patch_fn,
            self._acl_ref(obj)[1],
            request_body=tag_ids,
            patch_op=PatchOp.SET,
            reason=reason,
        )

    def _remove_control_tags(
        self, obj: Any, tag_ids: Any, *, reason: str | None = None
    ) -> Any:
        _, patch_fn = self._control_tag_fns(obj)
        return self._call(
            patch_fn,
            self._acl_ref(obj)[1],
            request_body=tag_ids,
            patch_op=PatchOp.DELETE,
            reason=reason,
        )


class _SupportsInfosec(_AclManager):
    """Classifiable hook: assign an infosec level via the generic v2 endpoint."""

    def _assign_infosec_level(self, obj: Any, *, level: str) -> Any:
        kind, resource_id = self._acl_ref(obj)
        # file resources have no InfosecLevelObjectType member → clear ValueError
        # (supported: model, artifact, system, user) rather than a cryptic enum error.
        object_type = _coerce_enum(InfosecLevelObjectType, kind, "resource kind")
        return self._call(
            self._engine.v2_api.assign_infosec_level,
            object_type,
            resource_id,
            assign_infosec_level=AssignInfosecLevel(infosec_level_id=level),
        )
