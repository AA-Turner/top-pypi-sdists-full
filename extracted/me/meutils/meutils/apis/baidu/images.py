# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Project      : AI.  @by PyCharm
# # @File         : images
# # @Time         : 2025/12/24 16:20
# # @Author       : betterme
# # @WeChat       : meutils
# # @Software     : PyCharm
# # @Description  :
#
# from meutils.pipe import *
# from meutils.apis.proxy.kdlapi import get_one_proxy
# from meutils.decorators.retry import retrying, IgnoredRetryException
#
# from meutils.schemas.image_types import ImageRequest, ImagesResponse
#
#
# BASE_URL = "https://image.baidu.com"
# async def generate(payload, token: Optional[str] = None, response_format: str = "url"):
#     s = time.time()
#     # token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL, from_redis=True)
#     headers = {
#         # 'Cookie': token,
#         # 'User-Agent': ua.random,
#         # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
#     }
#
#     request_kwargs = {
#         "proxy": await get_one_proxy(),
#     }
#
#     # logger.debug(request_kwargs)
#
#     async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=120, **request_kwargs) as client:
#         response = await client.post("/aigc/pccreate", data=payload)  # pcEditTaskid
#         response.raise_for_status()
#         data = response.json()
#
#         logger.debug(data)
#
#         image_base64 = None
#         if task_id := data.get("pcEditTaskid"):
#             for i in range(30):
#                 await asyncio.sleep(3)
#                 try:
#                     response = await client.get(f'/aigc/pcquery?taskId={task_id}&', )  # todo: get任务未加代理
#                     # logger.debug(response.json())
#                     if data := response.json().get("picArr", []):
#                         image_base64 = data[0].get("src")
#                         break
#                 except Exception as e:
#                     logger.error(e)
#                     if i > 3:
#                         raise IgnoredRetryException(f"忽略重试: \n{response.text}")
#
#         if not image_base64:
#             raise Exception(f"NO WATERMARK FOUND: {data}")  #############
#
#         if response_format == "url":
#             url = await to_url(image_base64, filename=f"{shortuuid.random()}_hd.png", content_type="image/png")
#
#             return ImagesResponse(data=[{"url": url}], timings={"inference": time.time() - s})
#         else:
#             return ImagesResponse(data=[{"b64_json": image_base64}], timings={"inference": time.time() - s})
#
#
# if __name__ == '__main__':
#     image = "https://s3.ffire.cc/files/jimeng.jpg"
#     payload = {
#         "type": "1",  # 去水印
#
#         "picInfo": image,
#         # "picInfo2": mask,
#
#         # # 百度云盘 才会更快
#         # "image_source": "1",
#         # "original_url": baidu_url,
#         # # # 更快但是会有错误
#         # "thumb_url": baidu_url,
#         # 更快但是会有错误
#
#     }
#
#     request = ImageRequest(
#         # model="hunyuan-remove-watermark",
#
#         # model="remove-watermark",
#         model="clarity",
#         # model="expand",
#         # model="rmbg-2.0",
#
#         # image=url,
#         # mask=url,
#
#         # response_format="b64_json"
#     )
#     arun(generate(request))