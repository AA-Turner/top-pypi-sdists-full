"""内部ツールの「操作種別」(ASTER 3.0 MT-A08 / MT-R06、2026-09-14)。

管理画面の禁止設定は内部ツールを個別の関数名ではなく **操作種別** で選ぶ (「テキスト書き込み」「ファイルの読み取り」
「ファイル転送」「コマンド実行」「ブラウザ操作」「デスクトップ操作」)。種別 → 組み込み tool 名の対応は SDK が持ち、
`mapping_version` で固定する (policy snapshot は保存時の版で再現する。旧版の表は削除せず残す)。

- 対応は **tool 名の完全一致集合** (glob 無し)。runtime の read / write / destructive 分類とは別物 (種別は tool の
  系統、分類は操作の性質)。`bash` は「コマンド実行」だけに入れる = テキスト書き込みツールを禁止しても
  コマンドやブラウザ経由の書き込みは止まらない (画面の説明にもその旨を出す)。
- 公開 (admin / front のヘルプ DTO) に出してよいのは種別 ID・表示名・説明・版だけ。tool 名の一覧は出さず、説明文にも
  内部の tool 名 (lsp / diagnostics / bash / box_* 等) を書かない (RRC-04。操作の表現で説明する)。
"""
from __future__ import annotations

from typing import Any

MAPPING_VERSION = 1
SUPPORTED_MAPPING_VERSIONS: tuple[int, ...] = (1,)

#: version → {kind_id → {label_ja, label_en, description_ja, description_en, tools}}
_MAPPINGS: dict[int, dict[str, dict[str, Any]]] = {
    1: {
        "text_write": {
            "label_ja": "テキスト書き込み", "label_en": "Text write",
            "description_ja": "ワークスペース内のファイルの作成・編集。コマンド実行やブラウザ操作による書き込みは含まない",
            "description_en": "Creating or editing workspace files. Writes made through command execution or browser automation are not covered",
            "tools": ("write", "edit", "multiedit", "multi_edit", "apply_patch", "notebook_edit", "write_workspace"),
        },
        "file_read": {
            "label_ja": "ファイルの読み取り", "label_en": "File read",
            "description_ja": "ワークスペース内のファイル・ディレクトリの読み取り (コード解析による読み取りを含む)",
            "description_en": "Reading workspace files and directories (including reads performed by code analysis)",
            "tools": ("read", "glob", "grep", "ls", "read_workspace", "lsp", "diagnostics"),
        },
        "file_transfer": {
            "label_ja": "ファイル転送", "label_en": "File transfer",
            "description_ja": "ファイルを外部ストレージや利用者との間で送受信する操作 (アップロード・ダウンロード・外部ストレージへの保存)",
            "description_en": "Moving files to or from external storage or the user (upload / download / saving to external storage)",
            "tools": ("upload", "download", "upload_file", "download_file", "react_upload_file", "download_image",
                      "box_upload", "box_download", "box_upload_version", "box_create_folder", "box_list_folder",
                      "upload_to_ftp"),
        },
        "command_exec": {
            "label_ja": "コマンド実行", "label_en": "Command execution",
            "description_ja": "シェルコマンドの実行。ファイル操作・通信など複数の行為を含みうるので、他の種別を禁止しても代替経路になりうる",
            "description_en": "Shell command execution. It can perform many kinds of actions, so it remains a path around other kinds",
            "tools": ("bash",),
        },
        "browser": {
            "label_ja": "ブラウザ操作", "label_en": "Browser automation",
            "description_ja": "ブラウザの自動操作 (閲覧・入力・送信)。Web 経由の書き込みを含みうる",
            "description_en": "Browser automation (navigate / fill / submit). May write through web apps",
            "tools": ("browser", "parallel_browsing"),
        },
        "desktop": {
            "label_ja": "デスクトップ操作", "label_en": "Desktop automation",
            "description_ja": "デスクトップアプリの自動操作 (macOS)。ブラウザ操作より広い範囲の行為を含む",
            "description_en": "Desktop application automation (macOS). Broader than browser automation",
            "tools": ("macos_app_control", "macos_applescript", "macos_execute_task", "macos_hotkey", "macos_send_keys",
                      "macos_ui_interact", "macos_inspect_ui"),
        },
    },
}


def kind_tools(kind: str, mapping_version: int = MAPPING_VERSION) -> frozenset[str]:
    """種別 → 組み込み tool 名の集合 (指定版の表)。未知の版 / 種別は KeyError。"""
    return frozenset(_MAPPINGS[int(mapping_version)][kind]["tools"])


def kind_ids(mapping_version: int = MAPPING_VERSION) -> tuple[str, ...]:
    return tuple(_MAPPINGS[int(mapping_version)].keys())


def is_supported_mapping_version(version: Any) -> bool:
    return isinstance(version, int) and not isinstance(version, bool) and version in SUPPORTED_MAPPING_VERSIONS


def internal_operation_kinds(mapping_version: int = MAPPING_VERSION) -> dict[str, Any]:
    """公開してよい形 (admin / front のヘルプ・選択肢 DTO): 種別 ID・表示名・説明・版だけ。tool 名は出さない。"""
    table = _MAPPINGS[int(mapping_version)]
    return {
        "mapping_version": int(mapping_version),
        "kinds": [{"id": k, "label_ja": v["label_ja"], "label_en": v["label_en"],
                   "description_ja": v["description_ja"], "description_en": v["description_en"]}
                  for k, v in table.items()],
    }


def internal_operation_mapping(mapping_version: int = MAPPING_VERSION) -> dict[str, Any]:
    """サーバー / SDK 内部向けの完全な表 (tool 名込み)。ヘルプ DTO には流さない。"""
    table = _MAPPINGS[int(mapping_version)]
    return {"mapping_version": int(mapping_version), "kinds": {k: sorted(v["tools"]) for k, v in table.items()}}
