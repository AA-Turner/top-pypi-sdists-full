#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : re_utils
# @Time         : 2022/5/12 下午2:03
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import json
import mimetypes
import re

from meutils.pipe import *
from urllib.parse import unquote, unquote_plus

zh = re.compile('[a-zA-Z\u4e00-\u9fa5]+')  # 中文 + 字母
nozh = re.compile('[^a-zA-Z\u4e00-\u9fa5]+')  # 中文 + 字母

HTML_PARSER = re.compile(r'```html(.*?)```', re.DOTALL)


# re.sub(r'=(.+)', r'=123','s=xxxxx')

@lru_cache()
def has_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fff]')  # 基本汉字 Unicode 范围
    return bool(pattern.search(text))


@lru_cache()
def remove_date_suffix(filename):
    """
    # 测试示例
    filenames = [
        "claude-3-5-haiku-20241022",
        "o1-mini-2024-09-12",
        "gpt-3.5-turbo-0125"
    ]

    # 输出结果
    for fname in filenames:
        print(remove_date_suffix(fname))
    :param filename:
    :return:
    """
    # 匹配日期格式（YYYYMMDD 或 YYYY-MM-DD）
    pattern = r'(-\d{8}|-\d{4}-\d{2}-\d{2}|-\d+)$'
    # 使用正则表达式替换日期后缀
    return re.sub(pattern, '', filename)


def get_parse_and_index(text, pattern):
    """
    text = 'The quick brown cat jumps over the lazy dog'
    get_parse_and_index(text, r'cat')
    """
    # 编译正则表达式模式
    regex = re.compile(pattern)

    # 使用re.finditer匹配文本并返回匹配对象迭代器
    matches = regex.finditer(text)

    # 遍历匹配对象迭代器，输出匹配项及其在文本中的位置
    for match in matches:  # 大数据
        yield match.start(), match.end(), match.group()


@lru_cache()
def parse_url(text: str, for_image=False, fn: Optional[Callable] = None):
    if text.strip().startswith("http") and len(re.findall("http", text)) == 1:  # http开头且是单链接
        return text.split(maxsplit=1)[:1]

    fn = fn or (lambda x: x.removesuffix(")"))

    # url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+|#]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    # url_pattern = r"((https?|ftp|www\\.)?:\\/\\/)?([a-zA-Z0-9.-]+\\.[a-zA-Z]{2,})(:[0-9]+)?(\\/[^\\s]*)?"

    if for_image:
        text = unquote_plus(text)
        # suffix = [
        #     ".jpg",
        #     ".jpeg",
        #     ".png",
        #     ".gif",
        #     ".bmp",
        #     ".tiff",
        #     ".psd",
        #     ".ai",
        #     ".svg",
        #     ".webp",
        #     ".ico",
        #     ".raw",
        #     ".dng"
        # ]
        # url_pattern = r'https?://[\w\-\.]+/\S+\.(?:png|jpg|jpeg|gif)'
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[#]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.(?:jpg|jpeg|png|gif|svg|webp)'

        # "https://i.miji.bid/2025/06/10/d018000aed9b872c7b248dccf14c4450.pngA" 纠正

    urls = re.findall(url_pattern, text)

    valid_urls = []
    for url in urls:
        url = fn(url.strip(r"\n"))

        valid_urls.append(url)

    return valid_urls


def parse_url_from_json():
    pass


def parse_command_string(command_str: str) -> dict:
    """
    解析一个类似 "prompt --key1 value1 --key2 value2" 格式的字符串。

    Args:
        command_str: 输入的命令行字符串。

    Returns:
        一个包含 prompt 和解析后参数的字典。
        例如: {"prompt": "画条狗", "size": "1:1", "n": 10}
    """
    # 初始化结果字典
    result = {}

    # 使用正则表达式找到第一个参数 '--' 的位置
    # 这比简单的 split 更健壮，可以处理 prompt 中包含 '--' 的情况（虽然不常见）
    match = re.search(r'\s--\w', command_str)

    if not match:
        # 如果没有找到任何参数，整个字符串都是 prompt
        result['prompt'] = command_str.strip()
        return result

    first_arg_index = match.start()

    # 提取 prompt 和参数部分
    prompt = command_str[:first_arg_index].strip()
    args_str = command_str[first_arg_index:].strip()

    result['prompt'] = prompt

    # 将参数字符串按空格分割成列表
    # 例如 "--size 1:1 --n 10" -> ['--size', '1:1', '--n', '10']
    args_list = args_str.split()

    # 遍历参数列表，每次处理一个键值对
    i = 0
    while i < len(args_list):
        arg = args_list[i]

        # 确认当前项是一个参数键（以 '--' 开头）
        if arg.startswith('--'):
            key = arg[2:]  # 去掉 '--' 前缀

            # 检查后面是否跟着一个值
            if i + 1 < len(args_list) and not args_list[i + 1].startswith('--'):
                value = args_list[i + 1]

                # 尝试将值转换为整数，如果失败则保留为字符串
                try:
                    processed_value = int(value)
                except ValueError:
                    processed_value = value

                # 布尔型
                if processed_value in ['true', 'yes', 'on']:
                    processed_value = True
                elif processed_value in ['false', 'no', 'off']:
                    processed_value = False

                result[key] = processed_value

                i += 2  # 跳过键和值，移动到下一个参数
            else:
                # 处理没有值的参数，例如 --test，可以设为 True 或忽略
                result[key] = True  # 或者可以写 pass 直接忽略
                i += 1
        else:
            # 如果某一项不是以 '--' 开头，它可能是格式错误，直接跳过
            i += 1

    return result


def parse_base64(text, pattern=r'!\[.*?\]\((.*?)\)'):
    """
    :param text:
    :param pattern:
        pattern=r'!\[.*?\]\((data:image/.*?)\)'
    :return:
    """
    base64_strings = re.findall(pattern, text)
    return base64_strings


if __name__ == '__main__':
    # from urllib.parse import urlparse
    #
    #
    # def is_valid_url(url):
    #     try:
    #         result = urlparse(url)
    #         return all([result.scheme, result.netloc])
    #     except:
    #         return False

    text = """7个正规url
    这是一段包含URL的文本，https://www.google.com 是一个URL，另一个URL是http://www.baidu.com
    解读这个文本https://www.url1.com
    https://www.url2.com 解读这个文本
    http://www.url2.com 解读这个文本

    https://www.url2.com解读这个文本

    总结 waptianqi.2345.com/wea_history/58238.html

    总结 https://waptianqi.2345.com/wea_history/58238.htm
    解释下这张照片 https://img-home.csdnimg.cn/images/20201124032511.png
        解释下这张https://img-home.csdnimg.cn/images/x.png

        img-home.csdnimg.cn/images/20201124032511.png


    https://oss.ffire.cc/files/百炼系列手机产品介绍.docx
    
    https://mj101-1317487292.cos.ap-shanghai.myqcloud.com/ai/test.pdf\n\n文档里说了什么？

    
        https://oss.ffire.cc/files/%E6%8B%9B%E6%A0%87%E6%96%87%E4%BB%B6%E5%A4%87%E6%A1%88%E8%A1%A8%EF%BC%88%E7%AC%AC%E4%BA%8C%E6%AC%A1%EF%BC%89.pdf 这个文件讲了什么？

    """

    # https://oss.ffire.cc/files/%E6%8B%9B%E6%A0%87%E6%96%87%E4%BB%B6%E5%A4%87%E6%A1%88%E8%A1%A8%EF%BC%88%E7%AC%AC%E4%BA%8C%E6%AC%A1%EF%BC%89.pdf 正则匹配会卡死
    # from urllib3.util import parse_url
    # text = "@firebot /换衣 https://oss.ffire.cc/files/try-on.png"
    # text = "@firebot /换衣 https://oss.ffire.cc/files/try-on.pn"

    # print(parse_url(text))
    # print(parse_url(text, for_image=True))
    print(parse_url(text, for_image=False))

    d = {"url": "https://mj101-1317487292.cos.ap-shanghai.myqcloud.com/ai/test.pdf\n\n总结下"}
    # print(parse_url(str(d)))

    text = "https://sc-maas.oss-cn-shanghai.aliyuncs.com/outputs/bb305b60-d258-4542-8b07-5ced549e9896_0.png?OSSAccessKeyId=LTAI5tQnPSzwAnR8NmMzoQq4&Expires=1739948468&Signature=NAswPSXj4AGghDuoNX5rVFIidcs%3D 笑起来"

    print(parse_url(text))

    # print(parse_url("[](https://oss.ffire.cc/cdn/2025-03-20/YbHhMbrXV82XGn4msunAJw)"))

    # print('https://mj101-1317487292.cos.ap-shanghai.myqcloud.com/ai/test.pdf\\n\\n'.strip(r"\n"))

    # print(parse_url("http://154.3.0.117:39666/docs#/default/get_content_preview_spider_playwright_get"))

    # print(parse_url(text, True))
    text = """
https://p26-bot-workflow-sign.byteimg.com/tos-cn-i-mdko3gqilj/f13171faeed2447b8b9c301ba912f25c.jpg~tplv-mdko3gqilj-image.image?rk3s=81d4c505&x-expires=1779880356&x-signature=AJop4%2FM8VjCUfjqiEzUugprc0CI%3D&x-wf-file_name=B0DCGKG71N.MAIN.jpg

还有这种url，两个.jpg的也能兼容么

https://i.miji.bid/2025/06/10/d018000aed9b872c7b248dccf14c4450.pngA
    """
    print(parse_url(text, for_image=True))

    # print(parse_url(text, for_image=False))

    # text = """https://photog.art/api/oss/R2yh8N Convert this portrait into a straight-on,front-facing ID-style headshot."""
    # print(parse_url(text))
    #
    # valid_urls = parse_url(text, for_image=True)

    print(mimetypes.guess_type("xx.ico"))

    text = "这是一个示例文本，包含一个图片：![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABAAAAAQACAIAAADwf7zUAAAgAElEQ) 这张图片很棒。"
    # text = "这是一个示例文本，。"

    print(parse_base64(text * 2))
