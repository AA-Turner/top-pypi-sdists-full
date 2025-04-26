#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2024/6/12 08:34
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.oss.minio_oss import Minio

from PIL import Image, ImageDraw


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


def crop_image(
        image: Union[Path, str, bytes],

        width: Optional[int] = None,
        height: Optional[int] = None,
        x: int = 0,
        y: int = 0,

        debug: bool = False
):
    """
        crop_image(image="https://sfile.chatglm.cn/testpath/4f520e7f-c2f5-5555-8d1f-4fda0fec0e9d_0.png", height=950, debug=True)

    :param image:
    :param width:
    :param height:
    :param x:
    :param y:
    :param debug:
    :return:
    """
    if isinstance(image, bytes):
        image = io.BytesIO(image)

    elif isinstance(image, str) and image.startswith("http"):
        response = httpx.get(image)
        image = io.BytesIO(response.content)

    image = Image.open(image)  # .convert('RGB')

    width = width or image.width
    height = height or image.height
    cropped_image = image.crop((x, y, x + width, y + height))

    if debug:
        logger.debug(image.size)
        logger.debug(cropped_image.size)
        cropped_image.show()

    return cropped_image  # .save('output.png')


def crop_image_and_upload(
        image: Union[Path, str, bytes],

        width: Optional[int] = None,
        height: Optional[int] = None,
        x: int = 0,
        y: int = 0,

        debug: bool = False,

        file_id: Optional[str] = None
):
    # 创建一个 BytesIO 对象用于保存字节数据
    # byte_io = io.BytesIO()

    # 将图像保存到 BytesIO 对象中
    # image.save(byte_io, format='PNG')
    # 获取字节数据
    # byte_data = byte_io.getvalue()

    image = crop_image(image, width, height, x, y, debug)

    file_id = file_id or shortuuid.random()
    filename = f"{file_id}.png"
    image.save(filename)

    # 上传
    client = Minio()
    client.fput_object('files', filename, file_path=filename, content_type='image/png')

    # 删除临时文件
    Path(filename).unlink(True)
    return client.get_file_url(filename)


def del_watermark():  # 去水印
    import poimage
    # poimage = try_import("poimage")
    # 支持jpg、png等所有图片格式
    poimage.del_watermark(
        input_image="img.png",
        output_image='img_.png'
    )


if __name__ == '__main__':
    # (left, top, right, bottom)

    # 调用该函数传入图片路径、裁剪起始点坐标(x, y)以及宽度和高度
    # crop_image("yuanbao.jpeg", height= 998, debug=True)
    # crop_image("zhipu.png", 0, 0, 1024, 950)
    # crop_image(Path("yuanbao.jpeg").read_bytes(), height=998, debug=True)

    # r = requests.get("https://sfile.chatglm.cn/testpath/4f520e7f-c2f5-5555-8d1f-4fda0fec0e9d_0.png")
    # print(r.content)

    image = crop_image(
        image="https://sfile.chatglm.cn/testpath/4f520e7f-c2f5-5555-8d1f-4fda0fec0e9d_0.png",
        height=950,
        debug=True
    )

    print(crop_image_and_upload(
        image="https://sfile.chatglm.cn/testpath/4f520e7f-c2f5-5555-8d1f-4fda0fec0e9d_0.png",
        height=950,
        debug=True))
