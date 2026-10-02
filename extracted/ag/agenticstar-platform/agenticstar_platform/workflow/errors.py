"""`agenticstar_platform.workflow` の例外。"""
from __future__ import annotations


class WorkflowError(RuntimeError):
    """runner 側の失敗（設定 / 契約 / 保存）。Agent 関数は呼ばれていないか、既に終わっている。"""


class WorkflowConfigError(WorkflowError):
    """executor が注入する env（protocol / base URL / token / execution ID）の欠落・不一致。汎用 DB 設定へ fallback しない。"""


class RuntimeApiError(WorkflowError):
    """front runtime API の応答が契約外（HTTP status と code を持つ）。"""

    def __init__(self, status: int, code: str, message: str = ""):
        super().__init__(f"{status} {code}: {message}".strip())
        self.status = status
        self.code = code
        self.message = message


class ExecutionTerminal(WorkflowError):
    """execution は既に terminal（executor の異常終端など）。Agent 関数を再実行する理由にしない（03 §4）。"""


class AuditNotPersisted(WorkflowError):
    """tool.invoked の監査が保存できなかった。その操作へ進めない（03 §3 手順 4）。"""


class InputIntegrityError(WorkflowError):
    """入力 artifact の digest / size / path が manifest と一致しない。"""


class OutputCollectionError(WorkflowError):
    """宣言 output の回収で契約違反（path / size / regular file / symlink）。"""
