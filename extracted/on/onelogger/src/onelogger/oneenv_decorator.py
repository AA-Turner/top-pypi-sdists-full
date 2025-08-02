"""
OneLogger Environment Template for OneEnv
OneLogger用のOneEnv環境変数テンプレート

This module provides the environment variable templates required for OneLogger
using the oneenv decorator.
このモジュールは、oneenvデコレータを使用して、OneLoggerに必要な環境変数テンプレートを提供します.

Reference: [OneEnv README](https://github.com/kitfactory/oneenv/blob/main/README.md)
"""

from oneenv import oneenv

@oneenv
def one_logger_template():
    """
    Environment variable template for OneLogger.
    OneLogger用の環境変数テンプレートです.
    """
    return {
        "LOG_LEVEL": {
            "description": """Specifies the logging level used by OneLogger. Valid options are DEBUG, INFO, WARNING, ERROR, and CRITICAL. This setting determines the minimum severity level of log messages that will be recorded.

OneLoggerが使用するログレベルを指定します。利用可能な値は DEBUG, INFO, WARNING, ERROR, CRITICAL です。この設定により、記録されるログメッセージの最小の重大度が決定されます。""",
            "default": "INFO",
            "required": True,
            "choices": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        },
        "LOG_OUTPUT": {
            "description": """Specifies the destination for log output. Options include 'console' for standard output, 'file' for file logging, or 'both' for both destinations.

ログの出力先を指定します。'console' は標準出力、'file' はファイル出力、'both' は両方への出力を意味します。""",
            "default": "console",
            "required": True,
            "choices": ["console", "file", "both"]
        },
        "LOG_FILE_PATH": {
            "description": """Specifies the log file path when LOG_OUTPUT is set to 'file' or 'both'.

LOG_OUTPUTが'file'または'both'の場合に使用されるログファイルのパスを指定します。""",
            "default": "app.log",
            "required": False,
            "choices": []
        },
        "LOG_FORMAT": {
            "description": """Specifies the format of log messages. 'plain' produces human-readable text logs, while 'json' outputs logs in structured JSON format for easy parsing.

ログメッセージのフォーマットを指定します。'plain' は読みやすいテキスト形式、'json' は解析しやすいJSON形式で出力します。""",
            "default": "plain",
            "required": True,
            "choices": ["plain", "json"]
        },
        "LOG_TIMESTAMP_FORMAT": {
            "description": """Defines the format for timestamps in log messages using strftime notation.

ログメッセージ内のタイムスタンプのフォーマットをstrftime規則に従って定義します。""",
            "default": "%Y-%m-%d %H:%M:%S",
            "required": False,
            "choices": []
        },
        "LOG_ROTATION_TYPE": {
            "description": """Specifies the log rotation strategy when using file output. 'size' rotates when the file reaches a specified size, while 'date' rotates logs on a daily basis.

ファイル出力時のローテーション方式を指定します。'size' は一定サイズに達した時、'date' は日付ごとにログファイルをローテーションします。""",
            "default": "size",
            "required": True,
            "choices": ["size", "date"]
        },
        "LOG_MAX_FILE_SIZE": {
            "description": """Specifies the maximum file size (in bytes) for log rotation when LOG_ROTATION_TYPE is 'size'.

'size' ローテーション方式での最大ファイルサイズ（バイト単位）を指定します。""",
            "default": "10485760",
            "required": True,
            "choices": []
        },
        "LOG_BACKUP_COUNT": {
            "description": """Specifies the number of backup log files to retain after a rotation occurs.

ローテーション後に保持するバックアップログファイルの数を指定します。""",
            "default": "5",
            "required": True,
            "choices": []
        },
        "LOG_BUFFER_TIME": {
            "description": """Specifies the buffering time in seconds for log output to reduce I/O frequency and improve performance.

ログ出力のバッファリング時間（秒単位）を指定します。これにより、I/O回数が減りパフォーマンスが向上します。""",
            "default": "1",
            "required": False,
            "choices": []
        },
        "LOG_INCLUDE_PID": {
            "description": """Specifies whether the process ID (PID) should be included in log messages.

ログメッセージにプロセスID（PID）を含めるかどうかを指定します。""",
            "default": "true",
            "required": False,
            "choices": ["true", "false"]
        },
        "LOG_INCLUDE_THREAD": {
            "description": """Specifies whether the thread ID should be included in log messages, aiding in debugging multi-threaded applications.

マルチスレッド環境でのデバッグを支援するため、ログにスレッドIDを含めるかどうかを指定します。""",
            "default": "true",
            "required": False,
            "choices": ["true", "false"]
        },
        "LOG_APP_NAME": {
            "description": """Specifies the application name to be included in log messages, useful for distinguishing logs from multiple running applications.

複数のアプリケーションが同時に実行される場合に、ログを識別するためのアプリケーション名を指定します。""",
            "default": "MyApp",
            "required": False,
            "choices": []
        },
        "LOG_STACKTRACE": {
            "description": """Specifies whether to include the exception's stack trace in log messages, which is useful for debugging errors.

エラー発生時に例外のスタックトレースをログメッセージに含めるかどうかを指定し、デバッグに役立てます。""",
            "default": "true",
            "required": False,
            "choices": ["true", "false"]
        },
        "LOG_ASYNC": {
            "description": """Specifies whether asynchronous logging should be enabled to improve performance by processing log messages in a background thread.

パフォーマンス向上のため、ログメッセージをバックグラウンドスレッドで処理する非同期ロギングを有効にするかどうかを指定します。""",
            "default": "false",
            "required": False,
            "choices": ["true", "false"]
        },
        "LOG_INCLUDE_SOURCE": {
            "description": """Specifies whether to include source information—namely, the filename and line number—in log messages. This helps identify the origin of log entries during debugging sessions.

ログメッセージに、発生元を特定するためのソース情報（ファイル名および行番号）を含めるかどうかを指定します。""",
            "default": "false",
            "required": False,
            "choices": ["true", "false"]
        },
        "LOG_STRIP_COLORS": {
            "description": """Specifies whether to remove ANSI color codes from log messages when writing to files. This is useful to keep log files clean and readable while maintaining colored output in the console.

ファイルに書き込む際にANSIカラーコードを除去するかどうかを指定します。コンソールでは色付き出力を維持しながら、ログファイルを読みやすく保つのに役立ちます。""",
            "default": "false",
            "required": False,
            "choices": ["true", "false"]
        },
        "NO_COLOR": {
            "description": """When set to any value, completely disables color output in all destinations. This follows the NO_COLOR standard (https://no-color.org/).

任意の値を設定すると、全ての出力先でカラー出力を完全に無効化します。これはNO_COLOR標準（https://no-color.org/）に従います。""",
            "default": "",
            "required": False,
            "choices": []
        }
    } 