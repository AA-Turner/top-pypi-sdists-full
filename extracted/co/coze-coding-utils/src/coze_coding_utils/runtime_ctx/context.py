import os
import uuid
from dataclasses import dataclass
from typing import Optional, Dict, Mapping

# Header keys
HEADER_X_TT_LOGID = "x-tt-logid"
HEADER_X_TT_ENV = "x-tt-env"
HEADER_X_USE_PPE = "x-use-ppe"
HEADER_X_TT_ENV_FE = "x-tt-env-fe"
HEADER_X_RUN_MODE = "x-run-mode"
HEADER_RPC_PERSIST_RES_REC_BIZ_SCENE = "rpc-persist-res-rec-biz-scene"
HEADER_RPC_PERSIST_COZE_RECORD_ROOT_ID = (
    "rpc-persist-coze-record-root-id"  # root_id，串联一次完整请求，通常标识一次完整对话
)
HEADER_RPC_PERSIST_RES_REC_ROOT_ENTITY_TYPE = "rpc-persist-res-rec-root-entity-type"  # 对应最顶层实体类型，用于标识资源消耗的来源归属实体
HEADER_RPC_PERSIST_RES_REC_ROOT_ENTITY_ID = (
    "rpc-persist-res-rec-root-entity-id"  # 对应最顶层实体ID
)
HEADER_RPC_PERSIST_RES_REC_EXT_INFO = (
    "rpc-persist-res-rec-ext-info"  # 扩展信息，json字符串格式
)

# Environment variable keys
ENV_SPACE_ID = "COZE_PROJECT_SPACE_ID"
ENV_PROJECT_ID = "COZE_PROJECT_ID"


@dataclass(slots=True)
class Context:
    """运行时上下文，封装请求关联的标识与环境信息。"""

    run_id: str
    space_id: str
    project_id: str
    logid: str = ""
    method: str = ""

    x_run_mode: Optional[str] = None
    x_tt_env: Optional[str] = None
    x_use_ppe: Optional[str] = None
    x_tt_env_fe: Optional[str] = None

    rpc_persist_res_rec_biz_scene: Optional[str] = None
    rpc_persist_coze_record_root_id: Optional[str] = None
    rpc_persist_res_rec_root_entity_type: Optional[str] = None
    rpc_persist_res_rec_root_entity_id: Optional[str] = None
    rpc_persist_res_rec_ext_info: Optional[str] = None


def new_context(
    method: str,
    headers: Optional[Mapping[str, str]] = None,
) -> Context:
    """创建上下文对象，读取必要环境变量并可从请求头补充可选字段。"""
    ctx = Context(
        run_id=str(uuid.uuid4()),
        space_id=os.getenv(ENV_SPACE_ID, ""),
        project_id=os.getenv(ENV_PROJECT_ID, ""),
        method=method,
    )
    if headers:
        norm = {k.casefold(): v for k, v in headers.items()}
        HEADERS_TO_ATTR = {
            HEADER_X_TT_LOGID: "logid",
            HEADER_X_TT_ENV: "x_tt_env",
            HEADER_X_USE_PPE: "x_use_ppe",
            HEADER_X_TT_ENV_FE: "x_tt_env_fe",
            HEADER_X_RUN_MODE: "x_run_mode",
            HEADER_RPC_PERSIST_RES_REC_BIZ_SCENE: "rpc_persist_res_rec_biz_scene",
            HEADER_RPC_PERSIST_COZE_RECORD_ROOT_ID: "rpc_persist_coze_record_root_id",
            HEADER_RPC_PERSIST_RES_REC_ROOT_ENTITY_TYPE: "rpc_persist_res_rec_root_entity_type",
            HEADER_RPC_PERSIST_RES_REC_ROOT_ENTITY_ID: "rpc_persist_res_rec_root_entity_id",
            HEADER_RPC_PERSIST_RES_REC_EXT_INFO: "rpc_persist_res_rec_ext_info",
        }
        for hk, attr in HEADERS_TO_ATTR.items():
            val = norm.get(hk)
            if val:
                setattr(ctx, attr, val)
    return ctx


def default_headers(ctx: Context | None) -> Dict[str, str]:
    """从上下文生成请求头字典，仅包含已设置的字段。"""
    if not ctx:
        return {}
    headers: Dict[str, str] = {}
    ATTR_TO_HEADER = {
        "logid": HEADER_X_TT_LOGID,
        "x_tt_env": HEADER_X_TT_ENV,
        "x_use_ppe": HEADER_X_USE_PPE,
        "x_tt_env_fe": HEADER_X_TT_ENV_FE,
        "x_run_mode": HEADER_X_RUN_MODE,
        "rpc_persist_res_rec_biz_scene": HEADER_RPC_PERSIST_RES_REC_BIZ_SCENE,
        "rpc_persist_coze_record_root_id": HEADER_RPC_PERSIST_COZE_RECORD_ROOT_ID,
        "rpc_persist_res_rec_root_entity_type": HEADER_RPC_PERSIST_RES_REC_ROOT_ENTITY_TYPE,
        "rpc_persist_res_rec_root_entity_id": HEADER_RPC_PERSIST_RES_REC_ROOT_ENTITY_ID,
        "rpc_persist_res_rec_ext_info": HEADER_RPC_PERSIST_RES_REC_EXT_INFO,
    }
    for attr, hk in ATTR_TO_HEADER.items():
        v = getattr(ctx, attr)
        if v:
            headers[hk] = v
    return headers


__all__ = [
    "Context",
    "new_context",
]
