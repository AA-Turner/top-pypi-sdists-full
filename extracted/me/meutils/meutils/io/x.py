import io

from PIL import Image
import os

from meutils.io.files_utils import to_bytes


async def get_image_format(file):
    file = await to_bytes(file)
    file = io.BytesIO(file)

    try:
        with Image.open(file) as img:
            logger.debug(img.mode)
            # format 属性返回大写的格式名，如 'JPEG', 'PNG', 'GIF' 等
            return img.format
    except Exception as e:
        return f"错误: {e}"


if __name__ == '__main__':
    from meutils.pipe import *

    url = "https://s3.ffire.cc/cdn/20260131/wXfXShqBw3uW5etgvsaL4v.jpeg"
    url = "wXfXShqBw3uW5etgvsaL4v.jpeg"
    url = "https://s3.ffire.cc/cdn/20260131/sNQLXjrfPFph26no3Jizvs.jpeg"
    url = "https://s3.ffire.cc/files/jimeng.jpg"
    url = "https://v3.fal.media/files/penguin/XoW0qavfF-ahg-jX4BMyL_image.webp"
    arun(get_image_format(url))
