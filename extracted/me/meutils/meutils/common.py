#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : common
# @Time         : 2020/11/12 11:42 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 单向引用，避免循环引用

import io
import os
import gc
import re
import sys
import time
import copy
import types
import typing
import uuid
import zipfile
import datetime
import operator
import inspect
import textwrap
import socket
import logging
import tempfile
import warnings

warnings.filterwarnings("ignore")

import functools
from functools import wraps

import argparse
import traceback
import threading
import multiprocessing
import base64
import shutil
import random
import asyncio
import importlib
import itertools
import pickle
import textwrap
import subprocess
import wget
import toml
import yaml
import typer
import json
import mimetypes
import joblib
from joblib.hashing import hash
import httpx
import requests
import wrapt
import shortuuid
# import sklearn  #######
import numpy as np
import pandas as pd

from typing import *
from pathlib import Path
from queue import Queue
from pprint import pprint
from abc import abstractmethod
from dataclasses import dataclass
from urllib.parse import unquote, unquote_plus, urlparse, urljoin
from functools import reduce, lru_cache, partial

from collections import Counter, OrderedDict
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# import matplotlib.pyplot as plt  #######
# from matplotlib.font_manager import FontProperties  #######
#
# FONT = FontProperties(fname=get_resolve_path('./data/SimHei.ttf', __file__))

# matplotlib.use('Agg'): matplotlib 这个库，这个库在使用时会创建额外的线程。如果你的应用不需要使用到 matplotlib，你可以考虑移除这个库，这可能能够解决问题。如果你的应用需要使用 matplotlib，但是并不需要它的图形界面功能，你可以尝试在导入 matplotlib 之前设置 matplotlib 的后端为 'Agg'
# plt.rcParams['axes.unicode_minus'] = False

from loguru import logger
# logger.remove()
# logger.add(sys.stderr, format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <4}</level> - <level>{message}</level>')


from tqdm.auto import tqdm

tqdm.pandas()

from pydantic import BaseModel, Field
from faker import Faker  # https://www.cnblogs.com/aichixigua12/p/13236092.html

fake_zh = Faker(locale='zh_CN')

# from PIL import Image, ImageGrab
# image
# im = ImageGrab.grabclipboard() 获取剪切板的图片
# json
import jsonpath
import json_repair

# 第三方
from meutils.other.crontab import CronTab
from meutils.other.besttable import Besttable

# ME
from meutils._utils import *
from meutils.init.evn import *
from meutils.init.oo import __O000OO0O0000OO00O
from meutils.hash_utils import murmurhash
from meutils.cache_utils import ttl_cache, disk_cache, diskcache
from meutils.decorators import decorator, args, singleton, timer, background, background_task
from meutils.path_utils import get_module_path, get_resolve_path, sys_path_append, path2list, get_config

lock = threading.Lock()
__O000OO0O0000OO00O()

from dotenv import load_dotenv

load_dotenvs = lambda dotenv_paths: [load_dotenv(p, verbose=True) for p in dotenv_paths]

EVN = os.getenv('EVN', "/Users/betterme/PycharmProjects/AI/.env")
load_dotenv(
    EVN,  # EVN=传入绝对路径 todo: 自定义 .env.secret
    verbose=True
)

cli = typer.Typer(name="MeUtils CLI")

# 常量
CPU_NUM = os.cpu_count()

HOST_NAME = DOMAIN_NAME = LOCAL_HOST = LOCAL = HOST = PORT = ''

HOME_CACHE = Path.home() / ".cache"

try:
    if not hasattr(typing, 'Literal'):
        import typing
        import typing_extensions

        Literal = typing_extensions.Literal
        typing.Literal = Literal

    if not hasattr(functools, 'cached_property'):
        from cached_property import cached_property
    else:
        from functools import cached_property

    from IPython.core.interactiveshell import InteractiveShell

    InteractiveShell.ast_node_interactivity = "all"  # 多行输出

    from rich import print as rprint

    HOST_NAME = socket.gethostname()
    DOMAIN_NAME = socket.getfqdn(HOST_NAME)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as _st:
        _st.connect(('10.255.255.255', 1))
        HOST, PORT = _st.getsockname()

    # import orjson as json  # dumps 结果是字节型
    # json.dumps = partial(json.dumps, option=json.OPT_NON_STR_KEYS)

    from icecream import ic

    ic.configureOutput(includeContext=True)

except Exception as e:
    pass


def download(url, filename: Optional[str] = None):
    filename = filename or Path(url).name

    with httpx.Client(follow_redirects=True, timeout=100) as client:
        response = client.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename


class BaseConfig(BaseModel):
    """基础配置"""
    _path: str = None

    @classmethod
    def init(cls):
        """init from path[zk/yaml]"""
        assert cls._path is not None, "请指定 _path"
        return cls.parse_path(cls._path)

    @classmethod
    def parse_path(cls, path):
        if Path(path).is_file():
            return cls.parse_yaml(cls._path)
        else:
            return cls.parse_zk(cls._path)

    @classmethod
    def parse_yaml(cls, path):
        json = yaml.safe_load(Path(path).read_bytes())
        return cls.parse_obj(json)

    @classmethod
    def parse_zk(cls, path):
        from meutils.zk_utils import get_zk_config
        json = get_zk_config(path)
        return cls.parse_obj(json)

    @classmethod
    def parse_env(cls):
        return cls.parse_obj(os.environ)


# limit memory
def limit_memory(memory=16):
    """
    :param memory: 默认限制内存为 16G
    :return:
    """
    import resource

    rsrc = resource.RLIMIT_AS
    # res_mem=os.environ["RESOURCE_MEM"]
    memlimit = memory * 1024 ** 3
    resource.setrlimit(rsrc, (memlimit, memlimit))
    # soft, hard = resource.getrlimit(rsrc)
    logger.info("memory limit as: %s G" % memory)


def magic_cmd(cmd='ls', parse_fn=lambda s: s, print_output=False):
    """

    :param cmd:
    :param parse_fn: lambda s: s.split('\n')
    :param print_output:
    :return:
    """
    cmd = ' '.join(cmd.split())
    status, output = subprocess.getstatusoutput(cmd)
    output = output.strip()

    logger.info(f"CMD: {cmd}")
    logger.info(f"CMD Status: {status}")

    if print_output:
        logger.info(f"CMD Output: {output}")

    return status, parse_fn(output)


def run_command(command='ls'):
    """
    运行Shell命令并输出其输出
    """
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, shell=True, universal_newlines=True
    )
    while True:
        # 读取Shell命令的输出
        key = str(time.time())
        output = process.stdout.readline()
        if output == "" and process.poll() is not None:
            break
        if output:
            # 实时显示输出
            print(output.strip())

    return process.poll()


def is_open(ip='88.01.012.01'[::-1], port=7000, timeout=0.5):
    """
        互联网 is_open('baidu.com:80')

    @param ip:
    @param port:
    @param timeout:
    @return:
    """
    if ':' in ip:
        ip, port = ip.split(':')

    socket.setdefaulttimeout(timeout)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((ip, int(port)))  # is_open("da.gd", 80) is_open("www.da.gd", 443)
            s.shutdown(socket.SHUT_RDWR)
            return True
        except:
            return False


def get_var_name(var):
    """获取变量字符串名
        a=1
        b=1
        c=1
        只会取 a, 因是通过 id 确定 key
    """
    _locals = sys._getframe(1).f_locals
    for k, v in _locals.items():
        if id(var) == id(v):  # 相同值可能有误判
            return k


def get_current_fn():
    """获取执行函数的函数名
        def f(): # f
            print(get_current_fn())
    @return:
    """
    # inspect.currentframe().f_back === sys._getframe().f_back
    # f_name = inspect.getframeinfo(inspect.currentframe().f_back)[2]  # 最外层

    f_name = sys._getframe(1).f_code.co_name  # sys._getframe(1) 外层 sys._getframe(0) 内层
    return f_name


@lru_cache()
def get_function_params(fn: Optional[Callable] = None):
    if fn is None:
        import openai
        fn = openai.OpenAI(api_key='').chat.completions.create

    params = inspect.signature(fn).parameters
    return list(params.keys())


def clear(ignore=('TYPE_CHECKING', 'logger', 'START_TIME', 'CPU_NUM', 'HOST_NAME', 'LOCAL_HOST', 'LOCAL')):
    """销毁全局变量
    TODO：可添加过滤规则
    """
    keys = []
    ignore = set(ignore)
    for key, value in globals().items():
        if key.startswith('_') or key in ignore:
            continue
        if callable(value) or value.__class__.__name__ == "module":
            continue
        keys.append(key)

    logger.debug("销毁全局变量: " + list4log(keys))
    for key in keys:
        del globals()[key]
    return keys


def show_code(func):
    sourcelines, _ = inspect.getsourcelines(func)
    _ = textwrap.dedent("".join(sourcelines))
    print(_)
    return _


def file_replace(file, old, new):
    p = Path(file)
    _ = (
        p.read_text()
        .replace(old, new)
    )
    p.write_text(_)


def exec_callback(source, **namespace):
    """

    @param source:
    @param namespace: source 入参
    @return: 出参
    """
    namespace = namespace or {}
    exec(source, namespace)
    namespace.pop('__builtins__')
    return namespace  # output


def pkl_dump(obj, file):
    with lock:
        try:
            with open(file, 'wb') as f:
                return pickle.dump(obj, f)
        except IOError:
            return False


def pkl_load(file):
    try:
        with open(file, 'rb') as f:
            return pickle.load(f)
    except IOError:
        return False


class MeBackgroundTasks(object):
    """
    def func(x):
        print(f'Sleeping: {x}')
        time.sleep(x)
        print(f'DONE: {x}')

    bk = BackgroundTasks()
    bk.add_task(func, x=1)
    bk.add_task(func, x=2)
    bk.add_task(func, x=3)
    """

    def __init__(self, max_workers=None, thread_name_prefix='🐶BackgroundTasks'):
        self.pool = ThreadPoolExecutor(max_workers, thread_name_prefix)

    def add_task(self, func, *args, **kwargs):
        future = self.pool.submit(func, *args, **kwargs)  # pool.map(fn, *iterables, timeout=None, chunksize=1)
        future.add_done_callback(lambda x: logger.error(future.exception()) if future.exception() else None)


background_tasks = MeBackgroundTasks()


# import uuid
# uuid.uuid4().hex
# attrs = [attr for attr in dir(i) if not callable(getattr(i, attr)) and not attr.startswith("__")]


def try_import(
        module_name: str, *, pip_name: Optional[str] = None, package: Optional[str] = None
) -> Any:
    """Dynamically imports a module and raises a helpful exception if the module is not
    installed."""
    module = None
    try:
        module = importlib.import_module(module_name, package)
    except ImportError:
        raise ImportError(
            f"Could not import {module_name} python package. "
            f"Please install it with `pip install {pip_name or module_name}`."
        )
    return module


def obj_to_dict(obj):
    """类对象转字典"""
    if isinstance(obj, list):
        return [obj_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: obj_to_dict(v) for k, v in obj.items()}
    elif hasattr(obj, '__dict__'):
        return obj_to_dict(obj.__dict__)
    else:
        return obj


def dict_to_model(data: Dict[str, Any], model_name: str = 'DynamicModel'):
    s = f"""class {model_name}(BaseModel):"""
    for k, v in data.items():
        _type = type(v).__name__
        if isinstance(_type, str):
            v = f"'{v}'"
        s += f"\n\t{k}: {_type} = {v}"
        print(s)

    from pydantic import create_model

    # 动态创建模型类
    model_fields = {}
    for key, value in data.items():
        if isinstance(value, dict):
            model_fields[key] = (dict_to_model(value), ...)
        elif isinstance(value, list) and value:
            if isinstance(value[0], dict):
                model_fields[key] = (List[dict_to_model(value[0])], ...)
            else:
                model_fields[key] = (List[type(value[0])], ...)
        else:
            model_fields[key] = (type(value), ...)

    model = create_model(model_name, **model_fields)

    # 创建模型对象
    model_obj = model(**data)

    return model_obj


def _hot_reload(*paths):
    """可以是文件夹"""

    from watchfiles import watch

    for changes in watch(*paths):
        logger.debug(changes)

        file = list(changes)[0][1]

        try:
            if file.endswith('env') or file.startswith('env.'):  # todo: 可增加其他条件
                load_dotenv(file, override=True)  # 覆盖
            elif file.endswith('.toml'):
                os.environ['TOML_CONFIG'] = json.dumps(toml.load(open(file)))
            elif file.endswith(('.yaml', '.yml')):
                os.environ['YAML_CONFIG'] = json.dumps(yaml.safe_load(open(file)))
            elif file.endswith('.json'):
                os.environ['JSON_CONFIG'] = json.dumps(json.load(open(file)))

            # logger.warning(os.getenv('a'))
            # logger.warning(os.getenv('TOML_CONFIG'))
            # logger.warning(os.getenv('YAML_CONFIG'))
            # logger.warning(os.getenv('JSON_CONFIG'))

        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc().strip())


def hot_reload(*paths, is_background: bool = False):
    if is_background:
        background_task(_hot_reload)(*paths)
    else:
        _hot_reload(*paths)


def to_markdown(text):
    from IPython.display import Markdown
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


def is_jupyter():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True  # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type, e.g. python script
    except NameError:
        return False  # Probably standard Python interpreter


def try_tasks(tasks: List[Callable], handle_error: Optional[Callable] = None, *args, **kwargs):
    """
        try_tasks([lambda x: 1 / x, lambda x: 2 / x], handle_error=lambda x: 3 / (x + 0.000001), x=0)
    """
    for i, task in enumerate(tasks):
        try:
            return task(*args, **kwargs)  # 尝试执行操作，如果操作成功，则跳出循环
        except Exception as e:
            _ = f"Task {i} failed: {e}"
            logging.error(_)
            # if is_trace:
            #     logging.error(traceback.format_exc().strip())

    if handle_error:
        return handle_error(*args, **kwargs)


def ttl_fn(ttl: int = 60):
    return time.time() // ttl  # 缓存时间


def storage_to_cookie(storage: Union[str, Path, dict]):
    if isinstance(storage, Path) or (isinstance(storage, str) and len(storage) < 256 and Path(storage).is_file()):
        storage = json.loads(Path(storage).read_bytes())
    elif isinstance(storage, str):
        storage = json.loads(storage)

    storage = storage['cookies']

    import jsonpath
    cookies = [f"{n}={v}" for n, v in
               zip(jsonpath.jsonpath(storage, "$..name"), jsonpath.jsonpath(storage, "$..value"))]
    return '; '.join(cookies)


@lru_cache()
def url2fileview(url):
    encoded_url = base64.b64encode(url.encode()).decode()
    # import urllib.parse
    # encoded_url = urllib.parse.quote(encoded_url)

    return f"https://v.ffire.cc/onlinePreview?url={encoded_url}"


if __name__ == '__main__':
    pass
    # s = "import pandas as pd; output = pd.__version__"
    # s = "import os; output = os.popen(cmd).read().split()"
    # print(exec_callback(s, cmd='ls'))
    # with timer() as t:
    #     time.sleep(3)
    #
    # status, output = magic_cmd('ls')
    # print(status, output)
    #
    # d = {'a': 1, 'b': 2}
    # print(bjson(d))
    # print(BaseConfig.parse_obj(d))

    # print(show_code(show_code))
    # print(get_var_name(s))

    # print(try_tasks([lambda x: 1 / x, lambda x: 2 / x], handle_error=lambda x: 3 / (x + 0.000001), x=0))
    # print(get_function_params(hot_reload))
    # print(url2view("https://sf-maas-uat-prod.oss-cn-shanghai.aliyuncs.com/outputs/dd25c8e0-fc6b-4d9b-aede-f6a489b04dee_00001_.png"))
    # print(get_function_params())

    pass
