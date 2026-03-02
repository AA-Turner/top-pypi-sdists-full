# Arquivo responsável por gerenciar as configurações do usuário.

from pathlib import Path

from appdirs import user_config_dir
from appdirs import user_data_dir


base_dir = Path(__file__).parent
project_root = base_dir.parent
config_ini = project_root / "config.ini"
current_work_directory = Path.cwd()
# sample_zip = base_dir.joinpath("data/sample.zip")

user_data = Path(user_data_dir())
sample_zip = user_data.joinpath("quick-start/data/sample.zip")
