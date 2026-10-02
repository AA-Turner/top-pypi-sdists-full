"""
AGENTICSTAR Platform SDK - 設定ユーティリティ

TOML 読み込みと ``${ENV}`` プレースホルダ展開を共通化する。

標準ライブラリ ``tomllib`` (Python 3.11+) を使用するため、外部 ``toml``
パッケージへの依存は不要。また deploy ガイドが想定する
``host = "${POSTGRESQL_HOST}"`` 形式のプレースホルダを、プラットフォームが
注入した環境変数で解決する（従来の ``from_toml`` は未解決のまま渡していた）。
"""

import os
import re
from typing import Any

# ${VAR} および ${VAR:-default} に対応
_ENV_PLACEHOLDER = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-([^}]*))?\}")


def expand_env_placeholders(value: Any) -> Any:
    """文字列中の ``${VAR}`` / ``${VAR:-default}`` を環境変数で再帰的に置換する。

    - ``${VAR}``          → ``os.environ["VAR"]``（未設定ならプレースホルダを保持）
    - ``${VAR:-default}`` → ``VAR`` が未設定なら ``default``

    dict / list は再帰的に処理する。未解決の ``${VAR}`` はそのまま残す
    （誤った接続先を黙って合成しないため）。

    制約（仕様として明記）:
    - エスケープ構文は無し（``\\${VAR}`` も VAR が設定済みなら展開される）。
    - ネスト（``${${X}}``）や default 値中の ``}`` は非対応。
    """
    if isinstance(value, str):
        def _replace(match: "re.Match[str]") -> str:
            name = match.group(1)
            default = match.group(2)
            if name in os.environ:
                return os.environ[name]
            if default is not None:
                return default
            return match.group(0)

        return _ENV_PLACEHOLDER.sub(_replace, value)
    if isinstance(value, dict):
        return {k: expand_env_placeholders(v) for k, v in value.items()}
    if isinstance(value, list):
        return [expand_env_placeholders(v) for v in value]
    return value


def load_toml_section(toml_path: str, section: str) -> dict:
    """TOML ファイルを読み込み、指定セクションを ``${ENV}`` 展開して返す。

    Args:
        toml_path: TOML ファイルパス
        section: セクション名（ドット区切りでネスト対応。例: ``"memory.llm"``）

    Returns:
        ``${ENV}`` 展開済みのセクション辞書

    Note:
        標準ライブラリ ``tomllib`` を使用するため外部依存は不要。
    """
    import tomllib

    with open(toml_path, "rb") as f:
        data: Any = tomllib.load(f)

    for key in section.split("."):
        data = data[key]

    return expand_env_placeholders(data)
