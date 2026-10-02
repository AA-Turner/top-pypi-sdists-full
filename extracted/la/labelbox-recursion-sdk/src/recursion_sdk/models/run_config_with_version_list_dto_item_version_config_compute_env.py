from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.run_config_with_version_list_dto_item_version_config_compute_env_run_verbs import RunConfigWithVersionListDtoItemVersionConfigComputeEnvRunVerbs





T = TypeVar("T", bound="RunConfigWithVersionListDtoItemVersionConfigComputeEnv")



@_attrs_define
class RunConfigWithVersionListDtoItemVersionConfigComputeEnv:
    """ Declared execution environment for a snapshot run config's persistent compute (container ref, shared/grade dirs, and
    image-supplied solver verbs). Omit to inherit the platform defaults.

        Attributes:
            container_ref (str | Unset): Child-container name the platform runs the solver/grade verbs in (via docker exec).
                Omit to inherit the platform default.
            shared_mount_dir (str | Unset): Directory bind-mounted from the pod into the container where grade mounts land
                and are read. Omit to inherit the platform default.
            grade_output_dir (str | Unset): Directory a compute_exec grade writes $GRADE_OUTPUT into (on a path the exec
                side both writes and reads). Omit to inherit the platform default.
            run_verbs (RunConfigWithVersionListDtoItemVersionConfigComputeEnvRunVerbs | Unset): Image-supplied solver-
                lifecycle verb scripts. Omit to use the platform default verbs.
     """

    container_ref: str | Unset = UNSET
    shared_mount_dir: str | Unset = UNSET
    grade_output_dir: str | Unset = UNSET
    run_verbs: RunConfigWithVersionListDtoItemVersionConfigComputeEnvRunVerbs | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_config_with_version_list_dto_item_version_config_compute_env_run_verbs import RunConfigWithVersionListDtoItemVersionConfigComputeEnvRunVerbs # noqa: PLC0415
        container_ref = self.container_ref

        shared_mount_dir = self.shared_mount_dir

        grade_output_dir = self.grade_output_dir

        run_verbs: dict[str, Any] | Unset = UNSET
        if not isinstance(self.run_verbs, Unset):
            run_verbs = self.run_verbs.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if container_ref is not UNSET:
            field_dict["containerRef"] = container_ref
        if shared_mount_dir is not UNSET:
            field_dict["sharedMountDir"] = shared_mount_dir
        if grade_output_dir is not UNSET:
            field_dict["gradeOutputDir"] = grade_output_dir
        if run_verbs is not UNSET:
            field_dict["runVerbs"] = run_verbs

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_config_with_version_list_dto_item_version_config_compute_env_run_verbs import RunConfigWithVersionListDtoItemVersionConfigComputeEnvRunVerbs # noqa: PLC0415
        d = dict(src_dict)
        container_ref = d.pop("containerRef", UNSET)

        shared_mount_dir = d.pop("sharedMountDir", UNSET)

        grade_output_dir = d.pop("gradeOutputDir", UNSET)

        _run_verbs = d.pop("runVerbs", UNSET)
        run_verbs: RunConfigWithVersionListDtoItemVersionConfigComputeEnvRunVerbs | Unset
        if isinstance(_run_verbs,  Unset):
            run_verbs = UNSET
        else:
            run_verbs = RunConfigWithVersionListDtoItemVersionConfigComputeEnvRunVerbs.from_dict(_run_verbs)




        run_config_with_version_list_dto_item_version_config_compute_env = cls(
            container_ref=container_ref,
            shared_mount_dir=shared_mount_dir,
            grade_output_dir=grade_output_dir,
            run_verbs=run_verbs,
        )

        return run_config_with_version_list_dto_item_version_config_compute_env

