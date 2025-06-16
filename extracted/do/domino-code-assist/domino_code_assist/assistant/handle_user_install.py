import os
import pathlib
import site

from domino_code_assist.domino_api import get_domino_api
from domino_code_assist.settings import settings


def in_user_install_mode():
    return __file__.startswith(site.getuserbase())


def in_pre_run_script():
    if os.path.exists("/domino/launch/preRunScript.sh"):
        with open("/domino/launch/preRunScript.sh") as f:
            content = f.read()
            if " low-code-assistant" in content or "low_code_assistant" in content or " domino-code-assist" in content or "domino_code_assist" in content:
                return True
    return False


def symlink_solara_assets():
    prefix = site.getuserbase()

    src = prefix + "/share/solara/cdn"
    dst = pathlib.Path(prefix + "/share/jupyter/nbextensions/_solara")
    dst.mkdir(exist_ok=True, parents=True)
    dst_cdn = dst / "cdn"
    if not dst_cdn.exists():
        os.symlink(src, dst_cdn)


def write_requirements_txt():
    file = pathlib.Path("requirements.txt")
    content = "domino-code-assist\n"
    if file.exists():
        old_content = file.read_text()
        if not (
            "low_code_assistant" in old_content
            or "low-code-assistant" in old_content
            or "domino_code_assist" in old_content
            or "domino-code-assist" in old_content
        ):
            file.write_text(old_content + "\n" + content)
            return True
    else:
        file.write_text(content)
        return True
    return False


if in_user_install_mode():
    symlink_solara_assets()
    try:
        if not settings.domino_is_git_based:
            if not in_pre_run_script():
                if write_requirements_txt():
                    get_domino_api().sync_files("requirements.txt added by domino_code_assist")
    except Exception:
        pass
