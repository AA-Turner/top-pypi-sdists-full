"""
molar http 客户端
"""

from enum import Enum
from pathlib import Path

from joblib import Parallel, delayed
import requests


from fyuneru.http_utils import find_labels, get_item_info, get_task_info
from fyuneru.lib import mkdir, read_json, tqdm_loguru, write_json


class MolarDomain(Enum):
    """
    域名
    """

    CN = "https://app.molardata.com"
    OTHER = "https://app.abaka.ai"


def init_export(
    export_config: dict,
    token: str,
    domain: str = MolarDomain.CN.value,
    n_jobs: int = 64,
    tmp_dir: Path = Path(".data/tmp"),
) -> dict:
    __session = requests.Session()
    task_id = export_config["taskId"]
    tmp_dir = tmp_dir / task_id
    mkdir(tmp_dir)
    task_info_tmp = tmp_dir / "task_info.json"
    if not task_info_tmp.exists():
        while not (task_config := get_task_info(task_id, token, domain)):
            continue
        task_config = task_config["data"]
        write_json(data=task_config, file=task_info_tmp)
    task_config = read_json(task_info_tmp)
    item_id_s = export_config["exportMetadata"]["match"]["itemIds"]
    data_s = Parallel(n_jobs=n_jobs, backend="threading")(
        delayed(get_item)(task_id, item_id, token, domain, __session, tmp_dir)
        for item_id in tqdm_loguru(item_id_s, desc="get item")
    )
    return {
        "task": task_config,
        "config": export_config,
        "data": data_s,
    }


def get_item(
    task_id: str,
    item_id: str,
    token: str,
    domain: str,
    session: requests.Session,
    tmp_dir: Path,
) -> dict:
    item_tmp = tmp_dir / f"{item_id}.json"
    if item_tmp.exists():
        return read_json(item_tmp)

    while not (
        item_info := get_item_info(
            item_id=item_id, token=token, domain=domain, session=session
        )
    ):
        continue
    while not (
        labels := find_labels(
            task_id=task_id,
            item_id=item_id,
            token=token,
            domain=domain,
            session=session,
        )
    ):
        continue
    info = item_info["data"]
    labels = labels["data"]
    item_dict = {
        "_id": item_id,
        "info": info["info"],
        "labels": labels,
        "item": info["item"],
        "_": info,
    }
    write_json(data=item_dict, file=item_tmp)
    return item_dict
