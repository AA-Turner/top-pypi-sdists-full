"""
AGENTICSTAR Platform SDK - Pod Runtime Management
Podライフサイクル管理 - 状態遷移と終了処理

Pod起動時のステータス設定、終了時のステータス更新と自己スケールダウンを統合
"""

import logging
from typing import Any, Awaitable, Callable, Dict, Optional

from .data_access import DataAccess

logger = logging.getLogger(__name__)

# 自己スケールダウン用コールバック: execution_id を受けて Pod を replicas=0 にする
ScaleDownCallback = Callable[[str], Awaitable[None]]


class PodRuntime:
    """
    Podライフサイクル管理クラス

    execution_podsテーブルへのステータス管理と、
    Pod終了時の自己スケールダウンを統合:
    - start(): Pod起動時にrunningステータスを設定
    - final(): Pod終了時にステータス更新 + 自己スケールダウン

    自己スケールダウンの方式は環境依存（StatefulSet replicas=0 / Sandbox CR 等）の
    ため、``scale_down_callback`` で注入する。未指定時は後方互換として
    ``src.utils.self_scaler.scale_down_self`` を遅延 import で試み、見つからない
    環境では「スキップした」旨を info ログに残すだけで失敗扱いにしない
    （会話応答・ステータス更新自体は完了させる）。
    """

    def __init__(
        self,
        db: DataAccess,
        execution_id: str,
        pod_name: str,
        scale_down_callback: Optional[ScaleDownCallback] = None,
    ):
        """
        Args:
            db: DataAccessインスタンス
            execution_id: 実行ID
            pod_name: Pod名
            scale_down_callback: Pod 終了時に呼ぶ自己スケールダウン処理（任意）。
                ``async def cb(execution_id: str) -> None`` 形式。未指定時は
                後方互換フォールバックを試みる。
        """
        self._db = db
        self._execution_id = execution_id
        self._pod_name = pod_name
        self._scale_down_callback = scale_down_callback
        self.logger = logger

    async def start(self) -> Dict[str, Any]:
        """
        Pod起動: ステータスをrunning/healthyに設定

        Returns:
            Dict with keys: success, data, error (optional)
        """
        self.logger.info(f"[IN] PodRuntime.start: execution_id={self._execution_id}, pod_name={self._pod_name}")
        result = await self._save_pod_status("running", "healthy")
        if result.get("success"):
            self.logger.info(f"[OUT] PodRuntime.start: Pod status set to running")
        else:
            self.logger.error(f"[ERROR] PodRuntime.start: Failed to set pod status: {result.get('error')}")
        return result

    async def final(self, status: str = "completed") -> Dict[str, Any]:
        """
        Pod終了: ステータス更新 → 自己スケールダウン

        Args:
            status: 終了ステータス ('completed', 'failed')

        Returns:
            Dict with execution_id and status
        """
        self.logger.info(f"[IN] PodRuntime.final: execution_id={self._execution_id}, status={status}")

        # 1. DBステータス更新
        await self._save_pod_status(status, "stopped")

        # 2. 自己スケールダウン（注入されたコールバック優先、未指定なら後方互換フォールバック）
        scale_down = self._scale_down_callback or self._resolve_legacy_scale_down()
        if scale_down is None:
            self.logger.info(
                f"[OUT] PodRuntime.final: no scale_down_callback configured and no legacy "
                f"scaler available; skipping self scale-down for {self._execution_id}"
            )
        else:
            try:
                await scale_down(self._execution_id)
                self.logger.info(f"[OUT] PodRuntime.final: Scale down completed for {self._execution_id}")
            except Exception as e:
                self.logger.error(f"[ERROR] PodRuntime.final: Scale down failed: {e}")

        return {"execution_id": self._execution_id, "status": status}

    @staticmethod
    def _resolve_legacy_scale_down() -> Optional[ScaleDownCallback]:
        """後方互換: 利用側アプリが ``src.utils.self_scaler`` を同梱していれば使う。

        SDK のみで最小実装した（``src`` パッケージを持たない）環境では None を返し、
        ``final()`` 側でスキップ扱いにする（``No module named 'src'`` で落とさない）。
        """
        try:
            from src.utils.self_scaler import scale_down_self  # type: ignore
            logger.warning(
                "PodRuntime: scale_down_callback 未注入のため legacy フォールバック "
                "(src.utils.self_scaler.scale_down_self) を使用。呼び出し側で "
                "scale_down_callback を明示注入してください（SDK→src 逆依存の暫定回避・将来削除予定）。"
            )
            return scale_down_self
        except ImportError:
            # モジュール不在（SDKのみの最小実装）→ None でスキップ。
            # import 成功後の他例外はバグの可能性があるので握りつぶさず伝播させる。
            return None

    async def _save_pod_status(self, pod_status: str, health_status: str) -> Dict[str, Any]:
        """
        execution_podsテーブルにステータス保存（UPSERT）

        Args:
            pod_status: Podステータス (running, completed, failed)
            health_status: ヘルス状態 (healthy, stopped, unknown)

        Returns:
            Dict with keys: success, data, error (optional)
        """
        query = """
            INSERT INTO execution_pods
            (execution_id, pod_name, pod_status, health_status, created_at, updated_at)
            VALUES ($1, $2, $3, $4, NOW(), NOW())
            ON CONFLICT (execution_id)
            DO UPDATE SET
                pod_name = EXCLUDED.pod_name,
                pod_status = EXCLUDED.pod_status,
                health_status = EXCLUDED.health_status,
                updated_at = NOW(),
                last_health_check = CASE
                    WHEN EXCLUDED.health_status != execution_pods.health_status THEN NOW()
                    ELSE execution_pods.last_health_check
                END
        """
        return await self._db.execute_query(
            query, (self._execution_id, self._pod_name, pod_status, health_status)
        )
