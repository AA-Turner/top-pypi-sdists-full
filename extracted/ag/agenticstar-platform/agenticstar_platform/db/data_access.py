"""
AGENTICSTAR Platform SDK - Generic Data Access Layer
汎用データアクセスレイヤー - テーブル操作の基本機能を提供

ビジネスロジックは含まず、純粋なDB操作のみを提供

Security:
    SQL Injection対策として、テーブル名・カラム名は厳格に検証されます。
    識別子は英数字・アンダースコア・ドットのみ許可されます。
"""

import functools
import json
import logging
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from .config import PostgreSQLConfig
from ..common.validation import (
    IdentifierValidationError,
    validate_identifier,
    validate_identifiers,
    validate_order_by,
)

logger = logging.getLogger(__name__)


def _identifier_error_to_result(func):
    """識別子検証エラーを戻り値 dict へ変換するデコレータ。

    DataAccess は結果を戻り値 dict で返す契約のため、識別子検証の失敗も
    例外を送出せず {"success": False, "error_code": "INVALID_IDENTIFIER"} で返す。
    不正な識別子はクエリ実行前に弾かれるため fail-closed は維持される。
    """
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except IdentifierValidationError as e:
            return {
                "success": False,
                "data": None,
                "error": str(e),
                "error_code": "INVALID_IDENTIFIER",
            }

    return wrapper


class DataAccess:
    """
    汎用データアクセスクラス

    テーブル操作の基本機能を提供:
    - insert: 単一レコード挿入
    - upsert: 挿入または更新
    - select: 条件付き検索
    - update: 条件付き更新
    - delete: 条件付き削除
    - execute_query: 生SQLクエリ実行

    Security:
        全てのテーブル名・カラム名は common.validation.validate_identifier() で検証されます。
        不正な識別子が渡された場合は例外を送出せず、
        success=False / error_code="INVALID_IDENTIFIER" の dict を返します。

    Example:
        # マネージャーインスタンスを渡す
        manager = PostgreSQLManager(config)
        async with DataAccess(manager) as da:
            result = await da.select("users", where={"id": 1})
    """

    def __init__(self, db):
        """
        Args:
            db: データベースマネージャーインスタンス
                PostgreSQLManager（DB直結）またはApiPostgreSQLManager（HTTP API経由）
                initialize(), close(), execute_query(), fetch_one(), fetch_all() を実装していること
        """
        self.db = db
        self.logger = logger

    async def __aenter__(self) -> "DataAccess":
        """Context Manager: 開始時にデータベース接続を初期化"""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context Manager: 終了時にデータベース接続をクローズ"""
        await self.close()

    async def initialize(self) -> None:
        """データベース接続を初期化"""
        await self.db.initialize()

    def is_initialized(self) -> bool:
        """データベース接続が初期化されているか確認"""
        if hasattr(self.db, 'is_initialized'):
            return self.db.is_initialized()
        # TODO: 後方互換フォールバック、次のメジャーバージョンで削除
        if hasattr(self.db, 'pool'):
            return self.db.pool is not None
        return True

    async def ensure_initialized(self) -> None:
        """データベース接続が初期化されていなければ初期化"""
        if not self.is_initialized():
            await self.initialize()

    async def close(self) -> None:
        """データベース接続を閉じる"""
        await self.db.close()

    async def execute_query(
        self, query: str, params: tuple = ()
    ) -> Dict[str, Any]:
        """
        生SQLクエリを実行

        Args:
            query: SQLクエリ
            params: クエリパラメータ

        Returns:
            Dict with keys: success, data, error (optional)
        """
        return await self.db.execute_query(query, params)

    @_identifier_error_to_result
    async def insert(
        self,
        table: str,
        data: Dict[str, Any],
        returning: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        単一レコードを挿入

        Args:
            table: テーブル名
            data: 挿入するデータ {column: value}
            returning: 返却するカラム名のリスト

        Returns:
            Dict with keys: success, data, error (optional)
            不正なテーブル名・カラム名の場合は success=False /
            error_code="INVALID_IDENTIFIER" の dict を返す
        """
        # SQL Injection対策: 識別子を検証
        safe_table = validate_identifier(table, "table")
        columns = list(data.keys())
        safe_columns = validate_identifiers(columns, "column")

        placeholders = [f"${i+1}" for i in range(len(safe_columns))]
        values = [self._serialize_value(v) for v in data.values()]

        query = f"INSERT INTO {safe_table} ({', '.join(safe_columns)}) VALUES ({', '.join(placeholders)})"

        if returning:
            safe_returning = validate_identifiers(returning, "returning column")
            query += f" RETURNING {', '.join(safe_returning)}"

        return await self.db.execute_query(query, tuple(values))

    @_identifier_error_to_result
    async def upsert(
        self,
        table: str,
        data: Dict[str, Any],
        conflict_columns: List[str],
        update_columns: Optional[List[str]] = None,
        returning: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        挿入または更新（UPSERT）

        Args:
            table: テーブル名
            data: 挿入/更新するデータ {column: value}
            conflict_columns: 競合判定に使うカラム
            update_columns: 競合時に更新するカラム（Noneの場合は全カラム）
            returning: 返却するカラム名のリスト

        Returns:
            Dict with keys: success, data, error (optional)
            不正なテーブル名・カラム名の場合は success=False /
            error_code="INVALID_IDENTIFIER" の dict を返す
        """
        # SQL Injection対策: 識別子を検証
        safe_table = validate_identifier(table, "table")
        columns = list(data.keys())
        safe_columns = validate_identifiers(columns, "column")
        safe_conflict_columns = validate_identifiers(conflict_columns, "conflict column")

        placeholders = [f"${i+1}" for i in range(len(safe_columns))]
        values = [self._serialize_value(v) for v in data.values()]

        # 更新対象カラムを決定
        if update_columns is None:
            update_columns = [c for c in columns if c not in conflict_columns]
        safe_update_columns = validate_identifiers(update_columns, "update column")

        # UPDATE SET句を構築
        update_set = ", ".join(
            [f"{col} = EXCLUDED.{col}" for col in safe_update_columns]
        )

        query = f"""
            INSERT INTO {safe_table} ({', '.join(safe_columns)})
            VALUES ({', '.join(placeholders)})
            ON CONFLICT ({', '.join(safe_conflict_columns)})
            DO UPDATE SET {update_set}
        """

        if returning:
            safe_returning = validate_identifiers(returning, "returning column")
            query += f" RETURNING {', '.join(safe_returning)}"

        return await self.db.execute_query(query, tuple(values))

    @_identifier_error_to_result
    async def select(
        self,
        table: str,
        columns: Optional[List[str]] = None,
        where: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        条件付き検索

        Args:
            table: テーブル名
            columns: 取得するカラム（Noneの場合は全カラム）
            where: 検索条件 {column: value}
            order_by: ソート指定（例: "created_at DESC"）
            limit: 取得件数上限

        Returns:
            Dict with keys: success, data (List[Dict]), error (optional)
            不正なテーブル名・カラム名の場合は success=False /
            error_code="INVALID_IDENTIFIER" の dict を返す
        """
        # SQL Injection対策: 識別子を検証
        safe_table = validate_identifier(table, "table")

        if columns is None:
            select_cols = "*"
        else:
            safe_columns = validate_identifiers(columns, "column")
            select_cols = ", ".join(safe_columns)

        query = f"SELECT {select_cols} FROM {safe_table}"
        params: List[Any] = []

        if where:
            conditions = []
            param_index = 1
            for col, val in where.items():
                safe_col = validate_identifier(col, "where column")
                if val is None:
                    conditions.append(f"{safe_col} IS NULL")
                else:
                    conditions.append(f"{safe_col} = ${param_index}")
                    params.append(self._serialize_value(val))
                    param_index += 1
            query += f" WHERE {' AND '.join(conditions)}"

        if order_by:
            safe_order_by = validate_order_by(order_by)
            query += f" ORDER BY {safe_order_by}"

        if limit is not None:
            if not isinstance(limit, int) or limit < 0:
                raise ValueError(f"Invalid limit value: {limit}")
            query += f" LIMIT {limit}"

        return await self.db.execute_query(query, tuple(params))

    async def select_one(
        self,
        table: str,
        columns: Optional[List[str]] = None,
        where: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        単一レコードを取得

        Args:
            table: テーブル名
            columns: 取得するカラム
            where: 検索条件

        Returns:
            Dict (結果がある場合) or None

            None は「該当レコードなし」だけでなく、検索が失敗した場合
            （不正な識別子・DBエラー等、select() が success=False を返す場合）
            も含む。エラー内容（error / error_code）を区別したい場合は
            select() を直接使うこと。
        """
        result = await self.select(table, columns, where, limit=1)
        if result.get("success") and result.get("data"):
            return result["data"][0]
        return None

    @_identifier_error_to_result
    async def update(
        self,
        table: str,
        data: Dict[str, Any],
        where: Dict[str, Any],
        returning: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        条件付き更新

        Args:
            table: テーブル名
            data: 更新するデータ {column: value}
            where: 更新条件 {column: value}
            returning: 返却するカラム名のリスト

        Returns:
            Dict with keys: success, data, error (optional)
            不正なテーブル名・カラム名の場合は success=False /
            error_code="INVALID_IDENTIFIER" の dict を返す
        """
        # SQL Injection対策: 識別子を検証
        safe_table = validate_identifier(table, "table")

        # SET句を構築
        set_columns = list(data.keys())
        safe_set_columns = validate_identifiers(set_columns, "set column")
        set_clause = ", ".join([f"{col} = ${i+1}" for i, col in enumerate(safe_set_columns)])
        params: List[Any] = [self._serialize_value(v) for v in data.values()]

        # WHERE句を構築
        where_columns = list(where.keys())
        safe_where_columns = validate_identifiers(where_columns, "where column")
        where_clause = " AND ".join(
            [f"{col} = ${len(safe_set_columns) + i + 1}" for i, col in enumerate(safe_where_columns)]
        )
        params.extend([self._serialize_value(v) for v in where.values()])

        query = f"UPDATE {safe_table} SET {set_clause} WHERE {where_clause}"

        if returning:
            safe_returning = validate_identifiers(returning, "returning column")
            query += f" RETURNING {', '.join(safe_returning)}"

        return await self.db.execute_query(query, tuple(params))

    @_identifier_error_to_result
    async def delete(
        self,
        table: str,
        where: Dict[str, Any],
        returning: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        条件付き削除

        Args:
            table: テーブル名
            where: 削除条件 {column: value}
            returning: 返却するカラム名のリスト

        Returns:
            Dict with keys: success, data, error (optional)
            不正なテーブル名・カラム名の場合は success=False /
            error_code="INVALID_IDENTIFIER" の dict を返す
        """
        # SQL Injection対策: 識別子を検証
        safe_table = validate_identifier(table, "table")

        # WHERE句を構築
        conditions = []
        params: List[Any] = []
        param_index = 1
        for col, val in where.items():
            safe_col = validate_identifier(col, "where column")
            if val is None:
                conditions.append(f"{safe_col} IS NULL")
            else:
                conditions.append(f"{safe_col} = ${param_index}")
                params.append(self._serialize_value(val))
                param_index += 1

        query = f"DELETE FROM {safe_table} WHERE {' AND '.join(conditions)}"

        if returning:
            safe_returning = validate_identifiers(returning, "returning column")
            query += f" RETURNING {', '.join(safe_returning)}"

        return await self.db.execute_query(query, tuple(params))

    def _serialize_value(self, value: Any) -> Any:
        """
        値をDB保存用にシリアライズ

        Args:
            value: シリアライズする値

        Returns:
            シリアライズされた値
        """
        if isinstance(value, dict) or isinstance(value, list):
            return json.dumps(value, ensure_ascii=False)
        return value
