import os
from dataclasses import dataclass
from typing import List, Optional, Union

from flytekit import ImageSpec, Resources, Secret
from mashumaro.mixins.json import DataClassJSONMixin
from mashumaro.mixins.yaml import DataClassYAMLMixin

WORKSPACE_IMAGE_NAME = "workspace"


class ImageSpecConfig(DataClassYAMLMixin, DataClassJSONMixin, ImageSpec):
    def __hash__(self):
        return hash(self.to_dict().__str__())


class ResourceConfig(DataClassYAMLMixin, Resources):
    pass


class SecretConfig(DataClassYAMLMixin, DataClassJSONMixin, Secret):
    key: str
    env_var: Optional[str] = None


@dataclass
class WorkspaceConfig(DataClassYAMLMixin, DataClassJSONMixin):
    name: str
    project: str
    domain: str
    description: Optional[str] = None
    container_image: Optional[Union[ImageSpecConfig, str]] = None
    secrets: Optional[List[SecretConfig]] = None
    resources: Optional[ResourceConfig] = None
    accelerator: Optional[str] = None
    on_startup: Optional[Union[str, List[str]]] = None
    workspace_root: str = "~/workspace"
    working_dir: Optional[str] = "content"
    ttl_seconds: int = 1200  # 20 minutes is the default up time

    def __post_init__(self):
        # Quick hack to always build image
        if isinstance(self.container_image, ImageSpecConfig):
            from union.ucimage._image_builder import _register_union_image_builder

            _register_union_image_builder()

            if os.getenv("UNION_DEV"):
                from union._testing import imagespec_with_local_union

                image_spec = imagespec_with_local_union(builder="union")
            else:
                image_spec = ImageSpec(builder="union")

            _user_image_spec = self.container_image
            self.container_image = ImageSpecConfig(
                name=f"{WORKSPACE_IMAGE_NAME}-{self.container_image.name}",
                base_image=_user_image_spec.base_image,
                builder=image_spec.builder,
                packages=[
                    *(image_spec.packages or []),
                    *(_user_image_spec.packages or []),
                ],
                source_root=image_spec.source_root,
                apt_packages=[
                    *(_user_image_spec.apt_packages or []),
                    "git",
                    "sudo",
                    "wget",
                    "vim",
                ],
                commands=[
                    "wget https://github.com/cli/cli/releases/download/v2.49.0/gh_2.49.0_linux_amd64.deb "
                    "-O /tmp/gh.deb",
                    "apt install /tmp/gh.deb",
                    "wget https://github.com/coder/code-server/releases/download/v4.23.1/code-server_4.23.1_amd64.deb "
                    "-O /tmp/code-server.deb",
                    "apt install /tmp/code-server.deb",
                    *(_user_image_spec.commands or []),
                ],
            )


_DEFAULT_CONFIG_YAML_FOR_BASE_IMAGE = """\
name: my-workspace
description: my workspace
# Make sure that the project and domain exists
project: {default_project}
domain: development
container_image: public.ecr.aws/unionai/workspace-base:py3.11-latest
secrets: null
resources:
    cpu: "2"
    mem: "4Gi"
    gpu: null
accelerator: null
on_startup: null
ttl_seconds: 1200
workspace_root: "~/workspace"
working_dir: "content"
"""

_DEFAULT_CONFIG_YAML_FOR_IMAGE_SPEC = """\
name: my-workspace
description: my workspace
project: {default_project}
domain: development
# container_image supports the union.ImageSpec arguments
container_image:
    name: null
    base_image: null
    builder: "union"
    packages:
    - scikit-learn
    env: null
    commands: null
secrets: null
resources:
    cpu: "2"
    mem: "4Gi"
    gpu: null
accelerator: null
on_startup: null
ttl_seconds: 1200
workspace_root: "~/workspace"
working_dir: "content"
"""
