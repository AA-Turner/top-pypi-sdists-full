#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : test
# @Time         : 2024/10/17 18:45
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import io

from meutils.pipe import *

from PIL import Image, ImageDraw

# data = json.loads(Path('p1.json').read_text())
#
data = json.loads(Path('p2.json').read_text())

from PIL import Image, ImageDraw

def crop_polygon(image_path, outline_points, inline_points):
    if isinstance(image_path, bytes):
        image_path = io.BytesIO(image_path)

    # 打开图像
    img = Image.open(image_path)
    print(img.size)

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


if __name__ == '__main__':
    # 使用示例
    # image_path = 'img.png'
    image_path = 'test.jpg'
    image_path = open('test.jpg', 'rb').read()

    # points = list(np.array(points))
    n = 3567 / 1280
    n = 2.75
    n = 1

    outline_points = []
    inline_points = []

    for outlines in data['foreground'][0].get('outlines', []):
        _ = list(map(lambda point: (point['x'], point['y']), outlines['line']))
        outline_points.append(_)

    for inlines in data['foreground'][0].get('inlines', []):
        _ = list(map(lambda point: (point['x'], point['y']), inlines['line']))
        inline_points.append(_)

    result = crop_polygon(image_path, outline_points, inline_points)
    result.save('output1111.png')

    type(result)