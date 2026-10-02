"""
AGENTICSTAR Platform SDK - Configuration Access Layer
設定データの取得機能を提供

エージェント設定、ツール設定、システム設定、MCP設定等の読み込み
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional

from .data_access import DataAccess
from .config import PostgreSQLConfig

logger = logging.getLogger(__name__)

# CLIモードとして扱う実行モードの一覧
CLI_MODES = {"cli", "cli-api", "cli_api", "cli-rpc", "cli_rpc"}


class ConfigAccess:
    """
    設定データアクセスクラス

    各種設定テーブルからの読み込み機能を提供:
    - エージェント指示・設定
    - ツール設定
    - ガードレール設定
    - システム設定
    - MCP設定
    """

    def __init__(self, db: DataAccess):
        """
        Args:
            db: DataAccessインスタンス
        """
        self._db = db
        self.logger = logger

    def _is_cli_mode(self, mode: Optional[str] = None) -> bool:
        """CLIモードかどうかを判定"""
        effective_mode = mode or os.environ.get("EXECUTION_MODE", "pod")
        return effective_mode in CLI_MODES or effective_mode.startswith("cli")

    # =====================================================
    # AGENT INSTRUCTIONS
    # =====================================================

    async def get_agent_instructions(self, agent_type: str) -> Dict[str, Any]:
        """
        エージェント指示を取得

        Args:
            agent_type: エージェントタイプ ('intent', 'react', 'coordinator')

        Returns:
            Dict with keys: success, data (instructions string), error (optional)
        """
        self.logger.info(f"[IN] get_agent_instructions: agent_type={agent_type}")
        try:
            result = await self._db.select(
                table="agent_instructions",
                columns=["instructions"],
                where={"agent_type": agent_type},
            )

            # DBエラーを先にチェック
            if not result.get("success"):
                self.logger.error(f"[ERROR] get_agent_instructions: DB error for {agent_type}")
                return {
                    "success": False,
                    "error": result.get("error", "Database query failed"),
                    "error_code": result.get("error_code", "DATABASE_ERROR")
                }

            # データが存在するかチェック
            if result.get("data"):
                instructions = result["data"][0]["instructions"]
                self.logger.info(f"[OUT] get_agent_instructions: Found for {agent_type}")
                return {"success": True, "data": instructions}
            else:
                self.logger.warning(f"[OUT] get_agent_instructions: Not found for {agent_type}")
                return {
                    "success": False,
                    "error": f"No instructions found for agent type: {agent_type}",
                    "error_code": "INSTRUCTIONS_NOT_FOUND"
                }

        except Exception as e:
            self.logger.error(f"[ERROR] get_agent_instructions: {str(e)}")
            return {
                "success": False,
                "error": f"Database error: {str(e)}",
                "error_code": "DATABASE_ERROR"
            }

    # =====================================================
    # AGENT CONFIGURATIONS
    # =====================================================

    async def get_all_agent_configs(self) -> Dict[str, Any]:
        """
        全エージェント設定を一括取得

        Returns:
            Dict with keys: success, data ({agent_type: {config_level: config}}), error (optional)
        """
        self.logger.info("[IN] get_all_agent_configs")
        try:
            query = """
                SELECT agent_type, config, config_level
                FROM agent_configurations
                WHERE is_active = TRUE
                ORDER BY agent_type, config_level
            """

            result = await self._db.execute_query(query)

            # DBエラーを先にチェック
            if not result.get("success"):
                self.logger.error("[ERROR] get_all_agent_configs: DB error")
                return {
                    "success": False,
                    "error": result.get("error", "Database query failed"),
                    "error_code": result.get("error_code", "DATABASE_ERROR")
                }

            configs = {}
            if result.get("data"):
                for row in result["data"]:
                    agent_type = row['agent_type']
                    config_level = row['config_level']

                    if agent_type not in configs:
                        configs[agent_type] = {}

                    configs[agent_type][config_level] = row['config']

                self.logger.info(f"[OUT] get_all_agent_configs: Found {len(configs)} types")
            else:
                self.logger.info("[OUT] get_all_agent_configs: No configs found (empty result)")

            return {"success": True, "data": configs}

        except Exception as e:
            self.logger.error(f"[ERROR] get_all_agent_configs: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to get agent configs: {str(e)}",
                "error_code": "CONFIG_FETCH_ERROR"
            }

    async def get_agent_config(
        self,
        agent_type: str,
        requested_level: str = "default"
    ) -> Dict[str, Any]:
        """
        エージェント設定を取得（優先順位: user > requested_level > default）

        Args:
            agent_type: エージェントタイプ
            requested_level: リクエストレベル ('default', 'high_performance')

        Returns:
            Dict with keys: success, data ({config, level}), error (optional)
        """
        self.logger.info(f"[IN] get_agent_config: agent_type={agent_type}, level={requested_level}")
        try:
            # まずユーザー設定を確認
            user_config_query = """
                SELECT config FROM agent_configurations
                WHERE config_level = 'user' AND agent_type = $1 AND is_active = TRUE
            """
            result = await self._db.execute_query(user_config_query, (agent_type,))

            # DBエラーを先にチェック
            if not result.get("success"):
                self.logger.error(f"[ERROR] get_agent_config: DB error for {agent_type}")
                return {
                    "success": False,
                    "error": result.get("error", "Database query failed"),
                    "error_code": result.get("error_code", "DATABASE_ERROR")
                }

            if result.get("data"):
                self.logger.info(f"[OUT] get_agent_config: Found user config for {agent_type}")
                return {"success": True, "data": {"config": result["data"][0]['config'], "level": "user"}}

            # 次に要求されたレベルの設定を確認
            level_config_query = """
                SELECT config FROM agent_configurations
                WHERE config_level = $1 AND agent_type = $2 AND is_active = TRUE
            """
            result = await self._db.execute_query(level_config_query, (requested_level, agent_type))

            if not result.get("success"):
                self.logger.error(f"[ERROR] get_agent_config: DB error for {agent_type}")
                return {
                    "success": False,
                    "error": result.get("error", "Database query failed"),
                    "error_code": result.get("error_code", "DATABASE_ERROR")
                }

            if result.get("data"):
                self.logger.info(f"[OUT] get_agent_config: Found {requested_level} config for {agent_type}")
                return {"success": True, "data": {"config": result["data"][0]['config'], "level": requested_level}}

            # 最後にデフォルト設定を確認
            if requested_level != "default":
                result = await self._db.execute_query(level_config_query, ("default", agent_type))

                if not result.get("success"):
                    self.logger.error(f"[ERROR] get_agent_config: DB error for {agent_type}")
                    return {
                        "success": False,
                        "error": result.get("error", "Database query failed"),
                        "error_code": result.get("error_code", "DATABASE_ERROR")
                    }

                if result.get("data"):
                    self.logger.info(f"[OUT] get_agent_config: Found default config for {agent_type}")
                    return {"success": True, "data": {"config": result["data"][0]['config'], "level": "default"}}

            self.logger.warning(f"[OUT] get_agent_config: No config found for {agent_type}")
            return {
                "success": False,
                "error": f"No configuration found for agent: {agent_type}",
                "error_code": "CONFIG_NOT_FOUND"
            }

        except Exception as e:
            self.logger.error(f"[ERROR] get_agent_config: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "error_code": "DATABASE_ERROR"
            }

    # =====================================================
    # TOOL CONFIGURATIONS
    # =====================================================

    async def get_tool_config(self, tool_name: str) -> Dict[str, Any]:
        """
        ツール設定を取得

        Args:
            tool_name: ツール名

        Returns:
            Dict with keys: success, data ({config, tool_name}), error (optional)
        """
        self.logger.info(f"[IN] get_tool_config: tool_name={tool_name}")
        try:
            result = await self._db.select(
                table="tool_configurations",
                columns=["config"],
                where={"tool_name": tool_name, "is_active": True},
            )

            # DBエラーを先にチェック
            if not result.get("success"):
                self.logger.error(f"[ERROR] get_tool_config: DB error for {tool_name}")
                return {
                    "success": False,
                    "error": result.get("error", "Database query failed"),
                    "error_code": result.get("error_code", "DATABASE_ERROR")
                }

            if result.get("data"):
                self.logger.info(f"[OUT] get_tool_config: Found for {tool_name}")
                return {"success": True, "data": {"config": result["data"][0]['config'], "tool_name": tool_name}}

            self.logger.warning(f"[OUT] get_tool_config: Not found for {tool_name}")
            return {
                "success": False,
                "error": f"No configuration found for tool: {tool_name}",
                "error_code": "CONFIG_NOT_FOUND"
            }

        except Exception as e:
            self.logger.error(f"[ERROR] get_tool_config: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "error_code": "DATABASE_ERROR"
            }

    async def get_all_tool_configs(self) -> Dict[str, Any]:
        """
        全ツール設定を一括取得

        Returns:
            Dict with keys: success, data ({tool_name: config}), error (optional)
        """
        self.logger.info("[IN] get_all_tool_configs")
        try:
            query = """
                SELECT tool_name, config
                FROM tool_configurations
                WHERE is_active = TRUE
                ORDER BY tool_name
            """

            result = await self._db.execute_query(query)

            # DBエラーを先にチェック
            if not result.get("success"):
                self.logger.error("[ERROR] get_all_tool_configs: DB error")
                return {
                    "success": False,
                    "error": result.get("error", "Database query failed"),
                    "error_code": result.get("error_code", "DATABASE_ERROR")
                }

            configs = {}
            if result.get("data"):
                for row in result["data"]:
                    configs[row['tool_name']] = row['config']
                self.logger.info(f"[OUT] get_all_tool_configs: Found {len(configs)} tools")
            else:
                self.logger.info("[OUT] get_all_tool_configs: No configs found (empty result)")

            return {"success": True, "data": configs}

        except Exception as e:
            self.logger.error(f"[ERROR] get_all_tool_configs: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to get tool configs: {str(e)}",
                "error_code": "CONFIG_FETCH_ERROR"
            }

    # =====================================================
    # BANNED URLS
    # =====================================================

    async def get_banned_urls(self) -> Dict[str, Any]:
        """
        有効な禁止URLパターン一覧を取得

        Returns:
            Dict with keys: success, data (list of {pattern, reason}), error (optional)
        """
        self.logger.info("[IN] get_banned_urls")
        try:
            query = """
                SELECT pattern, reason
                FROM banned_urls
                WHERE active = true
                ORDER BY id
            """
            result = await self._db.execute_query(query)

            if not result.get("success"):
                self.logger.error("[ERROR] get_banned_urls: DB error")
                return {
                    "success": False,
                    "error": result.get("error", "Database query failed"),
                    "error_code": result.get("error_code", "DATABASE_ERROR")
                }

            if result.get("data"):
                self.logger.info(f"[OUT] get_banned_urls: Found {len(result['data'])} patterns")
                return {"success": True, "data": result["data"]}
            else:
                self.logger.info("[OUT] get_banned_urls: No banned URLs found")
                return {"success": True, "data": []}

        except Exception as e:
            self.logger.error(f"[ERROR] get_banned_urls: {str(e)}")
            return {
                "success": False,
                "error": f"Database error: {str(e)}",
                "error_code": "DATABASE_ERROR"
            }

    # =====================================================
    # GUARDRAILS SETTINGS
    # =====================================================

    async def get_guardrails_settings(self) -> Dict[str, Any]:
        """
        Guardrails設定を取得

        Returns:
            Dict with keys: success, data (settings dict)
        """
        self.logger.info("[IN] get_guardrails_settings")

        default_settings = {
            "prompt_shield_enabled": True,
            "moderation_threshold": 2,
            "pii_masking_enabled": True,
            # キルスイッチ(エージェント強制停止): null = 制限しない(既定)。
            # 許可値は 5/15/30/60/90/120 分。
            "agent_kill_timeout_minutes": None,
        }

        try:
            # columns=None (SELECT *) で取得する。agent_kill_timeout_minutes 列は
            # dbmigration 適用済みの環境にのみ存在するため、明示列指定にすると未適用環境で
            # クエリが失敗し guardrails 設定全体が default に落ちる回帰を生む。SELECT * なら
            # 列が在れば値が流れ、無ければキーが欠落するだけ (下の setdefault で None=制限しない)。
            # autonomous イメージのデプロイ順 (dbmigration 前/後) に依存しない。
            result = await self._db.select(
                table="guardrails_settings",
                columns=None,
                where={"id": 1},
            )

            # DBエラーを先にチェック
            if not result.get("success"):
                self.logger.error("[ERROR] get_guardrails_settings: DB error, using defaults")
                # Guardrailsはデフォルト値を返す（フォールバック）
                return {"success": True, "data": default_settings}

            if result.get("data"):
                row = result["data"][0]
                # SELECT * は id/updated_at/updated_by や将来追加列も含むため、既知キーだけに
                # 絞って返す (元の明示列 SELECT と同じ shape を維持。consumer が dict をログ
                # 出力しても余分な/将来の機微列が混入しない)。列未適用環境では当該キーが
                # row に無いので default (agent_kill_timeout_minutes=None=制限しない) で補完。
                settings = {k: row.get(k, default_settings[k]) for k in default_settings}
                self.logger.info("[OUT] get_guardrails_settings: Found")
                return {"success": True, "data": settings}
            else:
                self.logger.info("[OUT] get_guardrails_settings: No settings found, using defaults")
                return {"success": True, "data": default_settings}

        except Exception as e:
            self.logger.error(f"[ERROR] get_guardrails_settings: {str(e)}, using defaults")
            return {"success": True, "data": default_settings}

    # =====================================================
    # SYSTEM SETTINGS
    # =====================================================

    async def get_system_settings(self) -> Dict[str, Any]:
        """
        システム設定を取得（アクティブな全レコード）

        Returns:
            Dict with keys: success, data (list of settings)
        """
        self.logger.info("[IN] get_system_settings")
        try:
            query = """
                SELECT user_prompt, guardrail_text, is_active, priority
                FROM system_settings
                WHERE organization_id IS NULL AND is_active = true
            """
            result = await self._db.execute_query(query)

            # DBエラーを先にチェック
            if not result.get("success"):
                self.logger.error("[ERROR] get_system_settings: DB error")
                return {
                    "success": False,
                    "error": result.get("error", "Database query failed"),
                    "error_code": result.get("error_code", "DATABASE_ERROR")
                }

            if result.get("data"):
                self.logger.info(f"[OUT] get_system_settings: Found {len(result['data'])} settings")
                return {"success": True, "data": result["data"]}
            else:
                self.logger.info("[OUT] get_system_settings: No settings found (empty result)")
                return {"success": True, "data": []}

        except Exception as e:
            self.logger.error(f"[ERROR] get_system_settings: {str(e)}")
            return {
                "success": False,
                "error": f"Database error: {str(e)}",
                "error_code": "DATABASE_ERROR"
            }

    # =====================================================
    # MCP CONFIGURATIONS
    # =====================================================

    async def get_mcp_configurations(self, execution_mode: Optional[str] = None) -> Dict[str, Any]:
        """
        アクティブなMCPサーバー設定を取得（OAuth情報含む）

        Args:
            execution_mode: 実行モード ('cli', 'cli-api', 'pod')。Noneの場合は環境変数から取得

        Returns:
            Dict with keys: success, data (list of MCP configs)
            各MCP configには以下を含む:
            - name, server_url, cache_tools_list, headers, only_pod
            - use_oauth: OAuthを使用するかどうか
            - oauth_service: 紐づいたOAuthプロバイダーのservice名（github, slack等）
        """
        self.logger.info("[IN] get_mcp_configurations")
        try:
            # CLI系モードの場合、only_pod=falseまたはNULLのレコードのみ取得
            # oauth_providersとLEFT JOINしてOAuth情報も取得
            if self._is_cli_mode(execution_mode):
                query = """
                    SELECT m.id, m.name, m.server_url, m.cache_tools_list, m.headers, m.only_pod,
                           m.use_oauth, o.service as oauth_service, m.transport_type
                    FROM mcp_server_configurations m
                    LEFT JOIN oauth_providers o ON o.mcp_server_id = m.id AND o.is_enabled = TRUE
                    WHERE m.is_active = TRUE
                    AND (m.only_pod = FALSE OR m.only_pod IS NULL)
                    ORDER BY m.name
                """
                self.logger.info("CLI mode: Filtering out pod-only MCP servers")
            else:
                query = """
                    SELECT m.id, m.name, m.server_url, m.cache_tools_list, m.headers, m.only_pod,
                           m.use_oauth, o.service as oauth_service, m.transport_type
                    FROM mcp_server_configurations m
                    LEFT JOIN oauth_providers o ON o.mcp_server_id = m.id AND o.is_enabled = TRUE
                    WHERE m.is_active = TRUE
                    ORDER BY m.name
                """

            result = await self._db.execute_query(query)

            # DBエラーを先にチェック
            if not result.get("success"):
                self.logger.error("[ERROR] get_mcp_configurations: DB error")
                return {
                    "success": False,
                    "error": result.get("error", "Database query failed"),
                    "error_code": result.get("error_code", "DATABASE_ERROR")
                }

            if result.get("data"):
                configurations = []
                for row in result["data"]:
                    # headersをdictに変換
                    headers_raw = row['headers']
                    headers = None
                    if headers_raw:
                        if isinstance(headers_raw, str):
                            try:
                                headers = json.loads(headers_raw)
                            except Exception as e:
                                self.logger.warning(f"Failed to parse headers for '{row['name']}': {e}")
                                headers = None
                        elif isinstance(headers_raw, dict):
                            headers = headers_raw

                    if headers == {}:
                        headers = None

                    config = {
                        # 接続の識別子 (mcp_server_configurations.id)。統制 (external の禁止規則 / 確定した操作クラス) は
                        # 名前ではなくこれで接続を識別する (3.0req 指示書 26)
                        "id": row.get('id'),
                        "name": row['name'],
                        "server_url": row['server_url'],
                        "cache_tools_list": row['cache_tools_list'],
                        "headers": headers,
                        "only_pod": row.get('only_pod', False),
                        # OAuth情報
                        "use_oauth": row.get('use_oauth', False),
                        "oauth_service": row.get('oauth_service'),  # github, slack, google, office365等
                        # Transport type: 'sse', 'streamable_http', 'stdio'
                        "transport_type": row.get('transport_type', 'sse'),
                    }
                    configurations.append(config)

                self.logger.info(f"[OUT] get_mcp_configurations: Found {len(configurations)} MCP servers")
                return {"success": True, "data": configurations}
            else:
                self.logger.info("[OUT] get_mcp_configurations: No MCP configs found (empty result)")
                return {"success": True, "data": []}

        except Exception as e:
            self.logger.error(f"[ERROR] get_mcp_configurations: {str(e)}")
            return {
                "success": False,
                "error": f"Database error: {str(e)}",
                "error_code": "DATABASE_ERROR"
            }
