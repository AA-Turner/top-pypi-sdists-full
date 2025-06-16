import site
import sys
from pathlib import Path
from typing import Optional

import pydantic

prefix = Path(sys.prefix)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
in_git = (PROJECT_ROOT / ".git").exists()

if in_git:
    # for development we use the prefix directory instead of the real prefix
    prefix = PROJECT_ROOT / "prefix"

if __file__.startswith(site.getuserbase()):
    # when installed in user mode, we use the user directory
    prefix = Path(site.getuserbase())

domino_snippet_builtin_dir_default = prefix / "share" / "domino-code-assist" / "snippets"


class Settings(pydantic.BaseSettings):
    domino_code_assist_dev: Optional[bool]
    domino_code_assist_exception_guard: bool = True
    snowflake_user: Optional[str]
    snowflake_password: Optional[str]
    snowflake_account: Optional[str]

    redshift_host: Optional[str]
    redshift_user: Optional[str]
    redshift_password: Optional[str]

    domino_api_class: Optional[str]

    domino_user_api_key: Optional[str]
    domino_project_id: Optional[str]
    domino_project_owner: Optional[str]
    domino_project_name: Optional[str]
    domino_api_host: Optional[str]
    domino_alternative_api_host: Optional[str]
    domino_run_id: Optional[str]
    domino_hardware_tier_id: Optional[str]

    domino_working_dir: str
    domino_datasets_dir: str = "/domino/datasets/"

    domino_snippet_builtin_dir: Path = domino_snippet_builtin_dir_default

    path_translated: Optional[str]
    domino_repos_dir: Optional[str]
    domino_imported_code_dir: Optional[str]
    domino_notebook_deploy_filename = ".dca_deployed.ipynb"

    domino_is_git_based: Optional[bool]

    class Config:
        case_sensitive = False
        env_file = ".env"


settings = Settings()
