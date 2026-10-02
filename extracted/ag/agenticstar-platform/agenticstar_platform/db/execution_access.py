"""
AGENTICSTAR Platform SDK - Execution Access Layer
実行データの取得機能を提供

会話履歴（messages）の取得など、実行コンテキストの読み取り
"""

import json
import logging
from typing import Any, Dict, List, Optional

from .data_access import DataAccess

logger = logging.getLogger(__name__)


class ExecutionAccess:
    """
    実行データアクセスクラス

    execution_dataテーブルからの読み取り機能を提供:
    - 会話履歴（messages）の取得
    """

    def __init__(self, db: DataAccess):
        """
        Args:
            db: DataAccessインスタンス
        """
        self._db = db
        self.logger = logger

    async def get_messages(self, execution_id: str) -> Optional[List[Dict[str, Any]]]:
        """
        会話履歴を取得

        Args:
            execution_id: 実行ID

        Returns:
            メッセージのリスト、またはNone（データなし/エラー時）
        """
        self.logger.info(f"[IN] get_messages: execution_id={execution_id}")
        try:
            result = await self._db.execute_query(
                "SELECT messages FROM execution_data WHERE id = $1",
                (execution_id,)
            )

            if not result.get("success") or not result.get("data"):
                self.logger.warning(f"[OUT] get_messages: No data found for {execution_id}")
                return None

            messages = result["data"][0].get("messages")

            # JSON文字列の場合はデシリアライズ
            if isinstance(messages, str):
                try:
                    messages = json.loads(messages)
                except (json.JSONDecodeError, TypeError):
                    self.logger.warning(f"[WARN] get_messages: Failed to parse messages JSON for {execution_id}")
                    return None

            self.logger.info(f"[OUT] get_messages: Retrieved {len(messages) if messages else 0} messages for {execution_id}")
            return messages

        except Exception as e:
            self.logger.error(f"[ERROR] get_messages: {str(e)}")
            return None
