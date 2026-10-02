"""
AGENTICSTAR Platform SDK - Runtime ヘルパー

marketplace runner Pod 起動時のユーティリティ。
"""

import asyncio
import logging
import time

logger = logging.getLogger(__name__)


async def wait_for_egress(
    host: str = "127.0.0.1",
    port: int = 15001,
    timeout: float = 15.0,
    interval: float = 0.2,
) -> bool:
    """外部 egress 用サイドカー（envoy）の TCP 受付開始を待つ。

    marketplace Pod は envoy native サイドカー（``HTTP_PROXY=127.0.0.1:15001``）経由で
    外部通信する。agent が起動直後に最初の外部呼び出し（入力ガードレール → PII 等）を
    すると envoy が未 ready で接続失敗し、初回ターンの moderation / PII がスキップ
    され得る。処理開始前に本メソッドで疎通を待つことで、この起動レースを防ぐ。

    Args:
        host: 待機先ホスト（既定 envoy inbound 127.0.0.1）
        port: 待機先ポート（既定 15001）
        timeout: 最大待機秒
        interval: 再試行間隔秒

    Returns:
        True: ready を確認 / False: timeout（呼び出し側は続行可。fail-open）
    """
    deadline = time.monotonic() + timeout
    attempt = 0
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        attempt += 1
        try:
            fut = asyncio.open_connection(host, port)
            # 接続試行は残り時間を超えない（全体 timeout を厳守）
            _, writer = await asyncio.wait_for(fut, timeout=min(interval, remaining))
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass
            logger.info(
                f"[wait_for_egress] egress sidecar ready at {host}:{port} (attempt {attempt})"
            )
            return True
        except Exception:
            # 次試行まで待機（deadline を超えない範囲で）
            nap = min(interval, deadline - time.monotonic())
            if nap > 0:
                await asyncio.sleep(nap)

    logger.warning(
        f"[wait_for_egress] egress sidecar not ready at {host}:{port} after {timeout}s; "
        f"proceeding (fail-open)"
    )
    return False
