import json
from typing import Any

from project.core.const import ProjectPaths


def get_arpakitlib_project_template_info() -> dict[str, Any]:
    with open(ProjectPaths.arpakit_lib_project_template_info_filepath, mode="r", encoding="utf-8") as fr:
        return json.load(fp=fr)


def __example():
    print(get_arpakitlib_project_template_info())


if __name__ == '__main__':
    __example()
