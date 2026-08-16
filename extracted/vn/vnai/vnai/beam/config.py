import os
import atexit
import json
import logging
from typing import Dict, Optional, Any
from vnai import get_api_key
logger = logging.getLogger(__name__)
_CONFIG_API_BASE = "https://vnstocks.com/api/config"
_CONFIG_CACHE: Dict[str, Any] = {}

def _clear_all_caches():
    _CONFIG_CACHE.clear()
atexit.register(_clear_all_caches)

def clear_config_cache(name: Optional[str] = None) -> None:
    if name:
        if name in _CONFIG_CACHE:
            del _CONFIG_CACHE[name]
    else:
        _CONFIG_CACHE.clear()

def list_cached_configs() -> list:
    return list(_CONFIG_CACHE.keys())

def _parse_payload(raw_data: str, token: str) -> str:
    import base64
    try:
        buffer = base64.b64decode(raw_data)
        salt = token.encode('utf-8')
        stream = bytearray(len(buffer))
        for i in range(len(buffer)):
            stream[i] = buffer[i] ^ salt[i % len(salt)]
        return stream.decode('utf-8')
    except Exception as e:
        logger.error(f"Lỗi giải mã dữ liệu config: {e}")
        return ""

def load_config(name: str, format: str = "auto") -> Optional[Any]:
    if name in _CONFIG_CACHE:
        return _CONFIG_CACHE[name]
    api_key = get_api_key()
    if not api_key:
        logger.warning(
            "Không tìm thấy API key. Vui lòng đăng nhập tại https://vnstocks.com/account#api-key "
            "để lấy API key. Sau đó cấu hình bằng lệnh:\n"
            "from vnstock.core.utils.auth import register_user\n"
            "register_user('<API_KEY>')"
        )
        return None
    url = f"{_CONFIG_API_BASE}/{name}"
    try:
        import requests
        response = requests.get(
            url=url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "User-Agent": "vnai-config-loader",
            },
            timeout=30,
        )
        if response.status_code == 200:
            content = response.text
            if response.headers.get("X-Data-Format") == "buffer":
                content = _parse_payload(content, api_key)
            if format == "text":
                _CONFIG_CACHE[name] = content
                return content
            try:
                data = json.loads(content)
                _CONFIG_CACHE[name] = data
                return data
            except json.JSONDecodeError as e:
                if format == "json":
                    logger.error(f"Lỗi parse JSON cho config '{name}': {e}")
                    return None
                else:
                    logger.debug(f"Config '{name}' không phải JSON, trả về nguyên bản (raw text).")
                    _CONFIG_CACHE[name] = content
                    return content
        elif response.status_code == 401:
            logger.warning(
                "API key không hợp lệ hoặc hết hạn. "
                "Cập nhật tại: https://vnstocks.com/account#api-key"
            )
        elif response.status_code == 403:
            logger.warning(
                f"Không đủ quyền truy cập config '{name}'. "
                f"Nâng cấp tại: https://vnstocks.com/insiders-program"
            )
        elif response.status_code == 404:
            logger.info(f"Config '{name}' không tồn tại.")
        elif response.status_code == 429:
            logger.warning("Đã vượt giới hạn tốc độ truy cập. Vui lòng thử lại sau.")
        else:
            logger.error(f"Lỗi khi tải config '{name}': HTTP {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"Lỗi kết nối khi tải config '{name}': {e}")
        return None