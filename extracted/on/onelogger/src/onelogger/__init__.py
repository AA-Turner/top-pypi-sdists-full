"""
OneLogger - A simple and efficient logging library
OneLogger - シンプルで効率的なロギングライブラリ
"""

# Import oneenv_decorator module to trigger the @oneenv template registration.
# テンプレート登録のため、oneenv_decorator モジュールを読み込みます。
import onelogger.oneenv_decorator

# Export OneLogger as Logger for ease-of-use / 利用しやすいようにエイリアスを提供
from .logger import OneLogger as Logger

# Define the public API of the package / パッケージの公開APIを定義
__all__ = ["Logger", "__version__"]

__version__ = "0.1.0"
