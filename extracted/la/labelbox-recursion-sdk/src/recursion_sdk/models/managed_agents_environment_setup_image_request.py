from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsEnvironmentSetupImageRequest")



@_attrs_define
class ManagedAgentsEnvironmentSetupImageRequest:
    """ An immutable setup image published after a manual setup run passes. Identity includes the environment fingerprint,
    configured runner, observed base digest, and capture generation.

        Example:
            {'baseImageDigest': 'example', 'capturedAt': '2026-02-18T09:30:00Z', 'computeId': 'example', 'fingerprint':
                'example', 'generation': 1, 'image': 'example', 'imageId': 'example', 'runnerImage': 'example', 'setupRunId':
                'example', 'sizeBytes': 1, 'usable': True, 'warmup': 'example', 'warmupMessage': 'example'}

        Attributes:
            base_image_digest (str | Unset): Immutable base image reference observed by Agent Service.
            captured_at (datetime.datetime | Unset): When Agent Service reported the image ready.
            compute_id (str | Unset): Agent Service compute whose filesystem was captured.
            fingerprint (str | Unset): Environment configuration fingerprint this image was produced for.
            generation (int | Unset): Capture and boot contract generation.
            image (str | Unset): Immutable digest-pinned image reference.
            image_id (str | Unset): Agent Service image id.
            runner_image (str | Unset): Exact configured runner reference selected for the captured compute.
            setup_run_id (str | Unset): Manual setup run that produced this image.
            size_bytes (int | Unset): Captured filesystem layer size.
            usable (bool | Unset): Registry-free read-time projection for the active verified environment and configured
                runner. A moving tag may have changed since this projection; session admission resolves its exact digest before
                choosing the captured image or per-session setup.
            warmup (str | Unset): Agent Service warmup state: pulling, verifying, ready, failed, or unavailable.
            warmup_message (str | Unset): Bounded Agent Service explanation of the warmup state.
     """

    base_image_digest: str | Unset = UNSET
    captured_at: datetime.datetime | Unset = UNSET
    compute_id: str | Unset = UNSET
    fingerprint: str | Unset = UNSET
    generation: int | Unset = UNSET
    image: str | Unset = UNSET
    image_id: str | Unset = UNSET
    runner_image: str | Unset = UNSET
    setup_run_id: str | Unset = UNSET
    size_bytes: int | Unset = UNSET
    usable: bool | Unset = UNSET
    warmup: str | Unset = UNSET
    warmup_message: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        base_image_digest = self.base_image_digest

        captured_at: str | Unset = UNSET
        if not isinstance(self.captured_at, Unset):
            captured_at = self.captured_at.isoformat()

        compute_id = self.compute_id

        fingerprint = self.fingerprint

        generation = self.generation

        image = self.image

        image_id = self.image_id

        runner_image = self.runner_image

        setup_run_id = self.setup_run_id

        size_bytes = self.size_bytes

        usable = self.usable

        warmup = self.warmup

        warmup_message = self.warmup_message


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if base_image_digest is not UNSET:
            field_dict["baseImageDigest"] = base_image_digest
        if captured_at is not UNSET:
            field_dict["capturedAt"] = captured_at
        if compute_id is not UNSET:
            field_dict["computeId"] = compute_id
        if fingerprint is not UNSET:
            field_dict["fingerprint"] = fingerprint
        if generation is not UNSET:
            field_dict["generation"] = generation
        if image is not UNSET:
            field_dict["image"] = image
        if image_id is not UNSET:
            field_dict["imageId"] = image_id
        if runner_image is not UNSET:
            field_dict["runnerImage"] = runner_image
        if setup_run_id is not UNSET:
            field_dict["setupRunId"] = setup_run_id
        if size_bytes is not UNSET:
            field_dict["sizeBytes"] = size_bytes
        if usable is not UNSET:
            field_dict["usable"] = usable
        if warmup is not UNSET:
            field_dict["warmup"] = warmup
        if warmup_message is not UNSET:
            field_dict["warmupMessage"] = warmup_message

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        base_image_digest = d.pop("baseImageDigest", UNSET)

        _captured_at = d.pop("capturedAt", UNSET)
        captured_at: datetime.datetime | Unset
        if isinstance(_captured_at,  Unset):
            captured_at = UNSET
        else:
            captured_at = datetime.datetime.fromisoformat(_captured_at)




        compute_id = d.pop("computeId", UNSET)

        fingerprint = d.pop("fingerprint", UNSET)

        generation = d.pop("generation", UNSET)

        image = d.pop("image", UNSET)

        image_id = d.pop("imageId", UNSET)

        runner_image = d.pop("runnerImage", UNSET)

        setup_run_id = d.pop("setupRunId", UNSET)

        size_bytes = d.pop("sizeBytes", UNSET)

        usable = d.pop("usable", UNSET)

        warmup = d.pop("warmup", UNSET)

        warmup_message = d.pop("warmupMessage", UNSET)

        managed_agents_environment_setup_image_request = cls(
            base_image_digest=base_image_digest,
            captured_at=captured_at,
            compute_id=compute_id,
            fingerprint=fingerprint,
            generation=generation,
            image=image,
            image_id=image_id,
            runner_image=runner_image,
            setup_run_id=setup_run_id,
            size_bytes=size_bytes,
            usable=usable,
            warmup=warmup,
            warmup_message=warmup_message,
        )


        managed_agents_environment_setup_image_request.additional_properties = d
        return managed_agents_environment_setup_image_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
