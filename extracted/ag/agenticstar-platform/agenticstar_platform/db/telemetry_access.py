"""
AGENTICSTAR Platform SDK - Telemetry Access Layer
テレメトリ・監査ログの保存・取得機能を提供

NIST監査対応のai_telemetryテーブルへのCRUD操作
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from .data_access import DataAccess

logger = logging.getLogger(__name__)


# ai_telemetry.tools_used は PostgreSQL の integer (int4)。範囲外の値を渡すと
# asyncpg が送信時に落ち、その行の telemetry 保存ごと失敗する。
_PG_INT4_MAX = 2_147_483_647


def _normalize_tools_used(value: Any) -> Optional[int]:
    """
    tools_used を ai_telemetry.tools_used (integer) の型へ正規化する。

    「使用ツール数」と「使用ツール一覧」のどちらを渡されても列側の型を int
    ひとつに固定するための contract 実装。正規化できない値は列を汚さず
    NULL にする (telemetry 保存自体を型エラーで落とさない)。

    - None                  -> None   (未計測。0 とは区別する)
    - bool                  -> None   (True/False を 1/0 と誤解釈しない)
    - int                   -> int    (0..int4 上限。負値・範囲外は None)
    - list / tuple          -> len()  (一覧を渡された場合は要素数へ)
    - それ以外               -> None
    """
    if value is None:
        return None
    if isinstance(value, bool):
        # bool は int のサブクラスなので、True/False を 1/0 と誤解釈する前に弾く
        logger.debug("tools_used is a bool; storing NULL")
        return None
    if isinstance(value, int):
        count = value
    elif isinstance(value, (list, tuple)):
        count = len(value)
    else:
        logger.debug(f"tools_used has unsupported type {type(value).__name__}; storing NULL")
        return None

    if not 0 <= count <= _PG_INT4_MAX:
        # 範囲外 (負値・int4 上限超過) を渡して INSERT ごと失敗させるより、
        # 列を NULL にして行を残す。
        logger.debug(f"tools_used={count} is outside PostgreSQL integer range; storing NULL")
        return None
    return count


class TelemetryAccess:
    """
    テレメトリデータアクセスクラス

    ai_telemetryテーブルへの保存・取得機能を提供:
    - save_telemetry: テレメトリデータの保存
    - list_telemetry: テレメトリデータの一覧取得
    - get_telemetry: 個別テレメトリデータの取得
    """

    def __init__(self, db: DataAccess):
        """
        Args:
            db: DataAccessインスタンス
        """
        self._db = db
        self.logger = logger

    async def save_telemetry(self, telemetry_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        汎用テレメトリーデータをPostgreSQLに保存（NIST監査対応）

        Args:
            telemetry_data: テレメトリーデータ（任意の構造）

                必須フィールド:
                - conversation_id: 会話ID
                - agent_type: エージェントタイプ (intent, react, coordinator, tool等)

                既知カラム (ai_telemetry の named column に直接入る):
                - timestamp, service, operation, duration_ms,
                  intent_type, confidence_score, tools_used, success,
                  agent_level, task_complexity,
                  current_message, context_summary, suggested_approach,
                  conversation_goal, final_content, metadata

                未知フィールドは全て metadata jsonb に自動格納される。

                tools_used の契約 (ai_telemetry.tools_used は integer):
                - int / list / tuple を受け付け、list・tuple は要素数へ正規化する
                  (呼び出し側が「回数」と「一覧」のどちらを渡しても列の型は int に固定)。
                - 未計測は NULL、計測した上で 0 回だった場合は 0。両者は区別する
                  ので、未計測を 0 に丸めてはならない。
                - int4 の範囲外 (負値・上限超過) や解釈不能な型は列を汚さず NULL。
                  「列の値が原因で INSERT が落ちる」ことは無い。
                  (metadata へ退避した生値が JSON 非互換な場合は、他の metadata
                  フィールドと同じく jsonb 化の段階で保存が失敗しうる。)
                - ツール名などの内訳は列ではなく metadata jsonb 側へ入れる
                  (例: autonomous の tools.summary)。列が生値を完全に表現できない場合
                  (list の内訳・型違い・範囲外) は生値を metadata['tools_used'] へ残す
                  ので、0.5.37 以前に metadata へ入っていた情報は失われない。
                  plain int の場合のみ列が完全な表現なので退避しない。

                Marketplace で LLM 駆動 agent のコスト/利用可視化を行う場合、
                以下の **推奨フィールド名** を使うとプラットフォーム共通の集計が可能:

                - prompt_tokens (int):     入力トークン数 (OpenAI/LiteLLM の usage.prompt_tokens 互換)
                - completion_tokens (int): 出力トークン数 (同 usage.completion_tokens 互換)
                - total_tokens (int):      prompt + completion
                - model (str):             LiteLLM 形式の識別子
                                          (例: "azure/gpt-4.1", "bedrock/anthropic.claude-3-5-sonnet")

                例:
                    await telemetry.save_telemetry({
                        "conversation_id": conversation_id,
                        "agent_type": "my_marketplace_agent",
                        "service": "my-agent-service",
                        "operation": "generate_response",
                        "duration_ms": 1234,
                        "success": True,
                        # 以下は自動で metadata jsonb に格納される (規約フィールド)
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens,
                        "model": "azure/gpt-4.1",
                    })

                集計クエリ例 (cross-agent cost analytics):
                    SELECT metadata->>'model' AS model,
                           agent_type,
                           SUM((metadata->>'prompt_tokens')::int) AS prompt_tokens,
                           SUM((metadata->>'completion_tokens')::int) AS completion_tokens,
                           COUNT(*) AS invocations
                    FROM ai_telemetry
                    WHERE timestamp > NOW() - INTERVAL '30 days'
                    GROUP BY model, agent_type;

        Returns:
            Dict with keys: success, data, error (optional), error_code (optional)
        """
        try:
            # 必須フィールドチェック
            if 'conversation_id' not in telemetry_data:
                return {
                    "success": False,
                    "error": "conversation_id is required",
                    "error_code": "MISSING_FIELD"
                }

            if 'agent_type' not in telemetry_data:
                return {
                    "success": False,
                    "error": "agent_type is required",
                    "error_code": "MISSING_FIELD"
                }

            # 防御コピー（呼び出し元のdictを破壊しない）
            telemetry_data = dict(telemetry_data)

            # デフォルト値の設定
            if 'timestamp' not in telemetry_data:
                telemetry_data['timestamp'] = datetime.now()

            # metadataフィールドの処理
            metadata = telemetry_data.get('metadata', {})
            if not isinstance(metadata, dict):
                metadata = {}

            # すべての追加フィールドをmetadataに含める
            known_fields = {
                'timestamp', 'service', 'operation', 'duration_ms',
                'conversation_id', 'intent_type', 'confidence_score',
                'tools_used', 'success',
                'agent_type', 'agent_level', 'task_complexity',
                'current_message', 'context_summary', 'suggested_approach',
                'conversation_goal', 'final_content', 'metadata'
            }

            # PII保護のため除外するフィールド
            excluded_fields = {'conversation_history'}

            for key, value in telemetry_data.items():
                if key not in known_fields and key not in excluded_fields:
                    metadata[key] = value

            # tools_used は named column (integer) へ入れる。0.5.37 以前は known_fields に
            # 無かったため生値が metadata jsonb に入っていたので、列が生値を完全に表現できない
            # 場合 (list の内訳・型違い・int4 範囲外) だけは生値を metadata へ残し、
            # patch リリースでの silent data loss を避ける。
            # 生値がそのまま列に入る plain int の場合のみ、重複を避けて退避しない。
            #
            # 判定は値の比較 (==/!=) ではなく型で行う。生値は任意型でありうるため、
            # 比較すると相手の __eq__ が走り、numpy 配列のように「真偽が曖昧」で
            # 例外になる型では telemetry 保存ごと落ちる。
            # 代入は上書き (setdefault ではない)。0.5.37 以前は未知フィールドの代入で
            # top-level 値が metadata 側の同名キーを上書きしていたため、その動作に揃える。
            raw_tools_used = telemetry_data.get('tools_used')
            tools_used_column = _normalize_tools_used(raw_tools_used)
            column_is_lossless = (
                isinstance(raw_tools_used, int)
                and not isinstance(raw_tools_used, bool)
                and tools_used_column is not None
            )
            if raw_tools_used is not None and not column_is_lossless:
                metadata['tools_used'] = raw_tools_used

            metadata_json = json.dumps(metadata, ensure_ascii=False) if metadata else None

            # INSERT クエリ
            query = """
                INSERT INTO ai_telemetry (
                    timestamp, service, operation, duration_ms,
                    conversation_id,
                    intent_type, confidence_score, tools_used, success,
                    agent_type, agent_level, task_complexity,
                    current_message, context_summary, suggested_approach,
                    conversation_goal, final_content, metadata,
                    created_at
                ) VALUES (
                    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19
                )
            """

            params = (
                telemetry_data.get('timestamp'),
                telemetry_data.get('service', 'autonomous-agent'),
                telemetry_data.get('operation'),
                telemetry_data.get('duration_ms'),
                telemetry_data['conversation_id'],
                telemetry_data.get('intent_type'),
                telemetry_data.get('confidence_score'),
                tools_used_column,
                telemetry_data.get('success'),
                telemetry_data['agent_type'],
                telemetry_data.get('agent_level'),
                telemetry_data.get('task_complexity'),
                telemetry_data.get('current_message'),
                telemetry_data.get('context_summary'),
                telemetry_data.get('suggested_approach'),
                telemetry_data.get('conversation_goal'),
                telemetry_data.get('final_content'),
                metadata_json,
                datetime.now()  # created_at
            )

            result = await self._db.execute_query(query, params)

            if result.get("success"):
                self.logger.debug(
                    f"Telemetry saved: conversation_id={telemetry_data['conversation_id']}, "
                    f"agent_type={telemetry_data['agent_type']}"
                )
                return {"success": True, "data": "Telemetry saved"}
            else:
                self.logger.error(f"Failed to save telemetry: {result.get('error')}")
                return {
                    "success": False,
                    "error": result.get("error"),
                    "error_code": result.get("error_code"),
                }

        except Exception as e:
            self.logger.error(f"Error saving telemetry: {str(e)}")
            return {
                "success": False,
                "error": f"Error saving telemetry: {str(e)}",
                "error_code": "TELEMETRY_ERROR"
            }

    async def list_telemetry(
        self,
        conversation_id: Optional[str] = None,
        service: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """
        テレメトリデータの一覧を取得

        Args:
            conversation_id: 会話IDでフィルタ（オプション）
            service: サービス名でフィルタ（オプション）
            limit: 取得件数上限（デフォルト: 100）
            offset: オフセット（デフォルト: 0）

        Returns:
            Dict with keys: success, data (List[Dict]), error (optional)
        """
        self.logger.info(
            f"[IN] list_telemetry: conversation_id={conversation_id}, "
            f"service={service}, limit={limit}, offset={offset}"
        )
        try:
            conditions = []
            params: list = []
            param_index = 1

            if conversation_id:
                conditions.append(f"conversation_id = ${param_index}")
                params.append(conversation_id)
                param_index += 1

            if service:
                conditions.append(f"service = ${param_index}")
                params.append(service)
                param_index += 1

            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

            query = f"""
                SELECT id, timestamp, service, operation, duration_ms,
                       conversation_id, intent_type, confidence_score,
                       tools_used, success,
                       agent_type, agent_level, task_complexity,
                       metadata, created_at
                FROM ai_telemetry
                {where_clause}
                ORDER BY created_at DESC
                LIMIT ${param_index} OFFSET ${param_index + 1}
            """
            params.extend([limit, offset])

            result = await self._db.execute_query(query, tuple(params))

            if not result.get("success"):
                self.logger.error(f"[ERROR] list_telemetry: {result.get('error')}")
                return {
                    "success": False,
                    "error": result.get("error"),
                    "error_code": result.get("error_code", "DATABASE_ERROR"),
                }

            data = result.get("data", [])
            self.logger.info(f"[OUT] list_telemetry: Retrieved {len(data)} records")
            return {"success": True, "data": data}

        except Exception as e:
            self.logger.error(f"[ERROR] list_telemetry: {str(e)}")
            return {
                "success": False,
                "error": f"Error listing telemetry: {str(e)}",
                "error_code": "TELEMETRY_ERROR",
            }

    async def get_telemetry(self, telemetry_id: str) -> Optional[Dict[str, Any]]:
        """
        個別テレメトリデータを取得

        Args:
            telemetry_id: テレメトリID

        Returns:
            テレメトリデータのDict、またはNone（データなし/エラー時）
        """
        self.logger.info(f"[IN] get_telemetry: id={telemetry_id}")
        try:
            result = await self._db.execute_query(
                "SELECT * FROM ai_telemetry WHERE id = $1",
                (telemetry_id,)
            )

            if result.get("success") and result.get("data"):
                self.logger.info(f"[OUT] get_telemetry: Found record for id={telemetry_id}")
                return result["data"][0]

            self.logger.warning(f"[OUT] get_telemetry: Not found for id={telemetry_id}")
            return None

        except Exception as e:
            self.logger.error(f"[ERROR] get_telemetry: {str(e)}")
            return None
