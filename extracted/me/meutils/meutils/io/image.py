#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : image
# @Time         : 2022/6/15 上午11:33
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://blog.csdn.net/Q_452086192/article/details/125014538
# https://www.jb51.net/article/207138.htm

import mimetypes
from PIL import Image, ImageDraw

from meutils.pipe import *
from meutils.io.files_utils import to_url, to_bytes


async def describe_image(image: Union[str, bytes]):
    """
    图片转base64  webp会报错
    :param image: 图片路径或图片对象
    :return: base64字符串
    """
    _ = await to_bytes(image)
    img = Image.open(io.BytesIO(_))

    info = {
        'format': img.format,  # 图片格式
        'mode': img.mode,  # 颜色模式

        'width': img.width,  # 宽度
        'height': img.height,  # 高度
        'size': img.size,  # (宽度, 高度)

        'is_animated': getattr(img, 'is_animated', False),  # 是否是动图
        'n_frames': getattr(img, 'n_frames', 1),  # 帧数
        'info': img.info,  # 图片附加信息
    }
    return info


def crop_polygon(image: Union[str, bytes], outline_points, inline_points):
    if isinstance(image, bytes):
        image = io.BytesIO(image)

    # 打开图像
    img = Image.open(image)

    # 创建一个与原图大小相同的黑色遮罩
    mask = Image.new('L', img.size, 0)

    # 在遮罩上绘制白色多边形
    for points in outline_points:
        ImageDraw.Draw(mask).polygon(points, outline=1, fill=255)

    for points in inline_points:
        ImageDraw.Draw(mask).polygon(points, outline=1, fill=0)

    # 将遮罩应用到原图
    output = Image.new('RGBA', img.size, (0, 0, 0, 0))
    output.paste(img, (0, 0), mask)

    # # 将 PIL Image 转换为字节
    # buffer = io.BytesIO()
    # output.save(buffer, format="PNG")
    # byte_data = buffer.getvalue()
    #
    # return byte_data
    return output


def img2bytes(img, format=None):
    """

    @param img: Optional[Image | np.array]
    @param format:
    @return:
    """
    # cv2 = try_import("cv2", pip_name="opencv-python")
    import cv2

    # if isinstance(img, Image):
    #     img = np.asarray(img)

    # a = cv2.cvtColor(a, cv2.COLOR_RGB2BGR)
    _, img_encode = cv2.imencode(format, img)

    return img_encode.tobytes()


def bytes2img(_bytes):
    import cv2

    np_arr = np.frombuffer(_bytes, dtype=np.uint8)
    # np.asarray(bytearray(bs), dtype=np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img


def image_read(filename):
    import cv2

    filename = str(filename)
    _bytes = b''
    if filename.startswith('http'):
        _bytes = requests.get(filename, stream=True).content

    elif Path(filename).exists():
        _bytes = Path(filename).read_bytes()

    if _bytes:
        try:
            np_arr = np.frombuffer(_bytes, dtype=np.uint8)
            # np.asarray(bytearray(bs), dtype=np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            return img
        except Exception as e:
            logger.warning(e)
            return np.asarray((Image.open(io.BytesIO(_bytes)).convert('RGB')))


def base64_to_image(base64_str):
    """
    import jmespath
    d = json.load(open('clients.ipynb'))
    base64_str = jmespath.search('cells[*].attachments', d)[0]['27fa29dd-5f0a-48b0-8e76-334e70a23595.png']['image/png']

    """
    import cv2
    # 传入为RGB格式下的base64，传出为RGB格式的numpy矩阵
    byte_data = base64.b64decode(base64_str)  # 将base64转换为二进制
    encode_image = np.asarray(bytearray(byte_data), dtype="uint8")  # 二进制转换为一维数组
    img_array = cv2.imdecode(encode_image, cv2.IMREAD_COLOR)  # 用cv2解码为三通道矩阵
    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)  # BGR2RGB
    return img_array


def image_to_base64(image_path_or_url, for_image_url: bool = True):
    content_type = mimetypes.guess_type(image_path_or_url)[0] or "image/jpeg"
    logger.debug(content_type)

    if image_path_or_url.startswith('http'):
        data = httpx.get(image_path_or_url, follow_redirects=True, timeout=100).content
    else:
        data = Path(image_path_or_url).read_bytes()

    _ = base64.b64encode(data).decode('utf-8')
    if for_image_url:
        _ = f"data:{content_type};base64,{_}"
    return _


def base64_to_bytes(base64_image_string):
    """
    # 将字节数据写入图片文件
    image_data = base64_to_bytes(...)
    with open(filename, 'wb') as file:
        file.write(image_data)
    """
    return base64.b64decode(base64_image_string.split(",", 1)[-1])


@alru_cache()
async def image2nowatermark_image(url, picinfo: str = '', oss: str = 'glm', token: Optional[str] = None):
    if not url: return

    from meutils.apis.baidu.bdaitpzs import create_task, BDAITPZSRequest

    # response = await httpx.AsyncClient(timeout=100, headers=headers, follow_redirects=True).get(url)
    # response.raise_for_status()

    # 去水印
    # request = BDAITPZSRequest(original_url=url, thumb_url=url) # 网络错误
    request = BDAITPZSRequest(picInfo=image_to_base64(url), picInfo2=picinfo)
    if picinfo:
        request.type = 2
        request.picInfo2 = picinfo

    data = await create_task(request, is_async=False, token=token)
    base64_string = data['picArr'][-1]['src']
    file = base64_to_bytes(base64_string)

    if oss == 'kling':  # kuaishou
        from meutils.apis.kuaishou import klingai

        file_task = await klingai.upload(file, cookie=token)
        return file_task and file_task.url

    else:
        url = await to_url(file) or url
        return url


# alias
base64_to_img = base64_to_image

if __name__ == '__main__':
    url = "https://i1.mifile.cn/f/i/mioffice/img/slogan_5.png?1604383825042"
    #
    # print(image_read(url))
    # base64_image_string = image_to_base64("img.png").split(",")[1]
    # # print(base64_to_bytes(image_to_base64("img.png")))
    # image_data = base64.b64decode(base64_image_string)
    #
    # with open("demo1.png", 'wb') as file:
    #     file.write(base64_to_bytes(image_to_base64("img.png")))

    # import mimetypes

    # print(mimetypes.guess_type('img.webp')[0])
    # image_to_base64(url)
    s = """
    """
    # base64_to_file(s, 'x.png')

    # url = "https://sfile.chatglm.cn/chatglm-videoserver/image/50/5049bae9.png"
    url = "https://oss.ffire.cc/files/kling_watermark.png"
    # arun(image2nowatermark_image(url))
    # arun(url2url(url))

    from meutils.schemas.baidu_types import PICINFO2_RIGHT_BOTTOM

    url = "https://s22-def.ap4r.com/bs2/upload-ylab-stunt-sgp/se/ai_portal_sgp_queue_mmu_img2img_aiweb/7de17faa-cc11-48a6-b94a-e80fe7a34841/1.png"

    # arun(image2nowatermark_image(url, picinfo=PICINFO2_RIGHT_BOTTOM))
    with timer():
        arun(describe_image("https://oss.ffire.cc/files/kling_watermark.png"))
