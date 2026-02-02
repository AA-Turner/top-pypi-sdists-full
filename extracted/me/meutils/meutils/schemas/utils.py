#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2025/10/31 17:57
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.str_utils.json_utils import json_path


def to_status(result, default_status="queued", mode: str = "openai") -> str:
    """

    :param result: response
    :param default_status:
    :param mode:
        openai "queued", "in_progress", "completed", "failed" => 映射到其他
    :return:

    {
    "id": "",
    "status": "unknown",
    "error": {
        "name": "Error",
        "message": "invalid params, task_id cannot by empty"
    }
}
    """
    if isinstance(result, str):
        result = {"status": result}

    if status := (
            result.get("status")
            or result.get("task_status")
            or result.get("state")
            or result.get("task_state")
            or json_path(result, expr="$..status")

    ):
        if isinstance(status, list):
            status = status[0]

        if isinstance(status, dict):  # fal
            status = "failed"

        status = str(status).lower()
        logger.debug(status)

        if status.startswith(
                (
                        "pro", "inpro", "pending", "task_status_queu", "sub", "start", "run", "inqueue", "queu",
                        "wait"
                )
        ):
            status = "queued"

        if status.startswith(("progr", "inprog", "in_progress", "gener")):
            status = "in_progress"

        if status.startswith(("succ", "ok", "compl", "task_status_succ")):
            status = "completed"

        if status.startswith(("fail", "error", "cancel", "task_status_fail")):
            status = "failed"

        if any(i in status for i in ("moder",)):  # 内容审核
            status = "failed"

        if any(i in status for i in ("feature_not_supported",)):
            status = "failed"


    return status or default_status


if __name__ == '__main__':
    result = {'id': 'cgt-20250613160030-2dvd7',
              'model': 'doubao-seedance-1-0-pro-250528',
              'status': 'succeeded',
              'content': {
                  'video_url': 'https://ark-content-generation-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-1-0-pro/02174980163157800000000000000000000ffffac182c17b26890.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYjg3ZjNlOGM0YzQyNGE1MmI2MDFiOTM3Y2IwMTY3OTE%2F20250613%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20250613T080120Z&X-Tos-Expires=86400&X-Tos-Signature=5e0928f738f49b93f54923549de4c65940c5007d5e86cb5ebadc756cca3aa03e&X-Tos-SignedHeaders=host'},
              'usage': {'completion_tokens': 246840, 'total_tokens': 246840},
              'created_at': 1749801631,
              'updated_at': 1749801680}
    _ = to_status(result)

    logger.debug(_)
