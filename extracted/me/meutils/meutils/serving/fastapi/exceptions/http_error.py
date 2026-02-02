import json
import traceback
from functools import partial
from httpx import HTTPStatusError
from openai import APIStatusError

from fastapi import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from fastapi.exceptions import RequestValidationError, HTTPException

from meutils.notice.feishu import send_message_for_http as send_message

exc_set = {

    # gemini
    "IMAGE_PROHIBITED_CONTENT",
    "IMAGE_SAFETY",
    "Provided image is not valid",

    "Text Risk Not Pass",

    "The input or output was flagged as sensitive",
    "invalidReferenceImageSize",
    "string_too_long",

    "content moderation",
    "please check the prompt",

    "sensitive",
    "OversizeImage",
    "filtered by safety checks",
    "InvalidParameter",
    "Image size format should",
    "Content security",

    "Failed to load the image",
    "Timeout while downloading url",

    "not corrupted",

    "supported format",
    "format unsupported",
    "UnsupportedImageFormat",

    "invalid image",
    "Image Decode Error",

    "Image pixel is invalid",

    "cannot identify",
    "could not generate",

    "Image size format should be like",

    # 大小/分辨率
    "Image resolution exceeds maximum",
    "Image dimensions out of range",
    "Total pixel count overflow",
    "Image aspect ratio not allowed",
    # 体积/上传
    "Payload Too Large",
    "413 Request Entity Too Large",
    "File size exceeds upload limit",
    # 格式/编码
    "Input buffer contains unsupported image format",
    "detected content type",
    "File extension does not match MIME type",
    "Codec not available for this format",
    # 内容安全
    "Adult content detected",
    "Violence risk score above threshold",
    "Copyright fingerprint hit",
    # 解码/像素
    "Corrupt JPEG data: premature end of data segment",
    "Invalid JPEG marker",
    "PNG signature not found",
    "Unsupported color type",
    "VipsJpeg: out of order read",
    # 网络/存储
    "Connection reset while downloading image",
    "SSL handshake failed",
    "403 Forbidden",
    "S3 AccessDenied",
    "Read timed out",
    # 内存/限流
    "Image processing memory limit exceeded",
    "GPU out of memory",
    "Rate limit exceeded",
    "Concurrent generation limit reached",
    # 参数
    "Missing required field",
    "Invalid base64 padding",
    "Empty image data",
}

exc_replace_set = {
    "runware",
    "fal.ai",
    "api.ppinfra"
}


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    # print(exc)
    content = {
        "error":
            {
                "message": f"{exc.detail}",
                "type": "http-error",
            }
    }
    return JSONResponse(
        content=content,
        status_code=exc.status_code
    )


async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        content={"message": str(exc)},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


# todo videos
"""
400 {"title":"Bad Request","status":400,"message":"Invalid payload provided","instance":"/v2/video/generations?","timestamp":"2026-01-22T07:20:46.273Z","error":{"name":"BadRequestException","message":"Invalid payload provided","data":[{"received":"768P","code":"invalid_enum_value","options":["360p","540p","720p","1080p"],"path":["resolution"],"message":"Invalid enum value. Expected '360p' | '540p' | '720p' | '1080p', received '768P'"},{"received":"4","code":"invalid_enum_value","options":["5","8","10"],"path":["duration"],"message":"Invalid enum value. Expected '5' | '8' | '10', received '4'"}]}}
"""
"""oneapi kling o1 居然可以返回
{
    "message": "{\"code\":402,\"msg\":\"您的余额不足，请前往充值中心进行充值\",\"data\":null}",
    "data": {
        "code": 402,
        "error": {
            "message": "{\"code\":402,\"msg\":\"您的余额不足，请前往充值中心进行充值\",\"data\":null}",
            "type": "cf-api-error"
        }
    }
}

{
"message": e1["error"]["message"],

"data":e1
}




e1 = {
    "error": {
        "message": "{\"code\":402,\"msg\":\"您的余额不足，请前往充值中心进行充值\",\"data\":null}",
        "type": "cf-api-error"
    },
    "code": 402
}
"""


async def chatfire_api_exception_handler(request: Request, exc: Exception):
    content = {
        "error":
            {
                "message": f"{exc}",
                "type": "cf-api-error",
            },

        "code": status.HTTP_500_INTERNAL_SERVER_ERROR  # 默认 是否默认都不重试？
    }

    # 默认值
    reps = None
    if isinstance(exc, (HTTPStatusError, APIStatusError)):  # todo 透传状态码
        status_code = exc.response.status_code or 500

        content['code'] = status_code
        if (message := exc.response.text.strip()) and message.startswith("{"):  # 解析内层 code message
            _ = json.loads(message)
            content['code'] = _.get("code") or content['code']
            message = _.get("message") or _.get("msg") or message

        content['error']['message'] = message

        # 置换错误
        for to_replace in exc_replace_set:
            content['error']['message'] = content['error']['message'].replace(to_replace, '***')

        reps = JSONResponse(
            content=content,
            status_code=status_code,
        )

    if any(i.lower() in str(exc).lower() for i in {"Invalid Token"}):  # 不跳过重试
        reps = JSONResponse(
            content=content,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    elif any(i.lower() in str(exc).lower() for i in exc_set):  # 跳过重试
        reps = JSONResponse(
            content=content,
            status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
        )

        # return reps

    # send_message
    content_detail = f"{traceback.format_exc()}"  # 是不是最后几行就可以了
    #
    # from meutils.pipe import logger
    # logger.debug(content_detail)

    if any(code in content_detail for code in {'451', }):
        content_detail = ""

    send_message([content, content_detail], title=__name__)

    # from meutils.pipe import logger
    #
    # try:
    #
    #     logger.debug(request.headers)
    #     logger.debug(request.url)
    #     logger.debug(request.method)
    #     logger.debug(request.query_params._dict)
    #
    #     logger.debug(request.client)
    #     logger.debug(request.cookies)
    #
    #     payload  = await request.body()
    #
    #     # send_message(payload, title=__name__)
    #
    #     logger.debug(payload)
    #     logger.debug(payload)
    #
    #
    # except Exception as e:
    #     logger.debug(e)

    return reps or JSONResponse(
        content=content,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


if __name__ == '__main__':
    pass
