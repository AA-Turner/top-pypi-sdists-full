"""
AGENTICSTAR Platform SDK - Context Manager Mixin
非同期Context Managerの共通実装
"""

import logging
from abc import ABC, abstractmethod
from typing import TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T", bound="AsyncContextManagerMixin")


class AsyncContextManagerMixin(ABC):
    """非同期Context Manager実装のためのMixin

    このMixinを継承することで、async with構文でのリソース管理が可能になります。

    Example:
        class MyClient(AsyncContextManagerMixin):
            async def close(self) -> None:
                # クリーンアップ処理
                pass

        async with MyClient() as client:
            await client.do_something()
        # 自動的にclose()が呼ばれる
    """

    async def __aenter__(self: T) -> T:
        """Context Manager: 開始時の処理

        Override可能: 初期化処理が必要な場合はオーバーライドしてください
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context Manager: 終了時にリソースをクローズ

        例外が発生してもclose()を確実に呼び出します
        """
        try:
            await self.close()
        except Exception as e:
            logger.warning(f"Error during context manager exit: {e}")

    @abstractmethod
    async def close(self) -> None:
        """リソースをクローズ

        実装クラスで必ずオーバーライドしてください
        """
        pass
