import os.path

from arpakitlib.ar_json_util import transfer_data_to_json_str
from project.core.const import ProjectPaths
from project.core.settings import get_cached_settings, Settings


def __command():
    print(transfer_data_to_json_str(get_cached_settings().model_dump(mode="json")))
    Settings.save_env_example_to_file(filepath=os.path.join(ProjectPaths.base_dirpath, "example.env"))


if __name__ == '__main__':
    __command()
