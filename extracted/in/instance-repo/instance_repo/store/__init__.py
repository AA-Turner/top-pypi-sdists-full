"""store — 数据面后端抽象（OSS / ACR / 元数据 registry）。

统一 apiserver-STS 模式：SDK 先向 apiserver 换 STS，再持 STS 直连 OSS/ACR。
为可测，底层 OSS 客户端与 skopeo 执行器均可注入（默认真实实现走 oss2 / skopeo，
标 pragma 不计入单测覆盖；单测注入 fake）。
"""
from .base import (
    BaseContentStore,
    BaseImageStore,
    BaseMetadataRegistry,
)
from .oss import OssContentStore
from .acr import AcrImageStore
from .registry import ApiMetadataRegistry

__all__ = [
    "BaseContentStore", "BaseImageStore", "BaseMetadataRegistry",
    "OssContentStore", "AcrImageStore", "ApiMetadataRegistry",
]
