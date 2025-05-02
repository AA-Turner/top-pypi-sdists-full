import datetime
import typing

import kubernetes.client

class V1PodSecurityContext:
    app_armor_profile: typing.Optional[kubernetes.client.V1AppArmorProfile]
    fs_group: typing.Optional[int]
    fs_group_change_policy: typing.Optional[str]
    run_as_group: typing.Optional[int]
    run_as_non_root: typing.Optional[bool]
    run_as_user: typing.Optional[int]
    se_linux_change_policy: typing.Optional[str]
    se_linux_options: typing.Optional[kubernetes.client.V1SELinuxOptions]
    seccomp_profile: typing.Optional[kubernetes.client.V1SeccompProfile]
    supplemental_groups: typing.Optional[list[int]]
    supplemental_groups_policy: typing.Optional[str]
    sysctls: typing.Optional[list[kubernetes.client.V1Sysctl]]
    windows_options: typing.Optional[kubernetes.client.V1WindowsSecurityContextOptions]
    
    def __init__(self, *, app_armor_profile: typing.Optional[kubernetes.client.V1AppArmorProfile] = ..., fs_group: typing.Optional[int] = ..., fs_group_change_policy: typing.Optional[str] = ..., run_as_group: typing.Optional[int] = ..., run_as_non_root: typing.Optional[bool] = ..., run_as_user: typing.Optional[int] = ..., se_linux_change_policy: typing.Optional[str] = ..., se_linux_options: typing.Optional[kubernetes.client.V1SELinuxOptions] = ..., seccomp_profile: typing.Optional[kubernetes.client.V1SeccompProfile] = ..., supplemental_groups: typing.Optional[list[int]] = ..., supplemental_groups_policy: typing.Optional[str] = ..., sysctls: typing.Optional[list[kubernetes.client.V1Sysctl]] = ..., windows_options: typing.Optional[kubernetes.client.V1WindowsSecurityContextOptions] = ...) -> None:
        ...
    def to_dict(self) -> V1PodSecurityContextDict:
        ...
class V1PodSecurityContextDict(typing.TypedDict, total=False):
    appArmorProfile: typing.Optional[kubernetes.client.V1AppArmorProfileDict]
    fsGroup: typing.Optional[int]
    fsGroupChangePolicy: typing.Optional[str]
    runAsGroup: typing.Optional[int]
    runAsNonRoot: typing.Optional[bool]
    runAsUser: typing.Optional[int]
    seLinuxChangePolicy: typing.Optional[str]
    seLinuxOptions: typing.Optional[kubernetes.client.V1SELinuxOptionsDict]
    seccompProfile: typing.Optional[kubernetes.client.V1SeccompProfileDict]
    supplementalGroups: typing.Optional[list[int]]
    supplementalGroupsPolicy: typing.Optional[str]
    sysctls: typing.Optional[list[kubernetes.client.V1SysctlDict]]
    windowsOptions: typing.Optional[kubernetes.client.V1WindowsSecurityContextOptionsDict]
