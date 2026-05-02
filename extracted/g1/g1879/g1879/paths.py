# -*- encoding:utf-8 -*-
# @Author    : g1879
# @date      : 2021/6/03
# @email     : g1879@qq.com
# @File      : paths.py
"""
文件、文件夹处理常用方法
"""
from pathlib import Path
from re import sub, search
from shutil import rmtree
from typing import Union, List


def find_path(path: Union[Path, str],
              keys: Union[str, list, tuple, set, dict],
              file_or_dir: str = 'file',
              fuzzy: bool = True,
              find_in_sub: bool = True,
              name_or_suffix: str = 'name',
              match_case: bool = True,
              return_one: bool = True,
              each_key: bool = True,
              deep_first: bool = False) -> Union[Path, List[Path], dict]:
    """根据关键字查找文件或文件夹，返回Path对象或其组成的列表或字典                       \n
    :param path: 在这个文件夹路径下查找
    :param keys: 关键字，可输入多个
    :param file_or_dir: 查找文件还是文件夹，可传入 'file' 'dir' 'both'
    :param fuzzy: 是否模糊匹配
    :param find_in_sub: 是否进入子文件夹查找
    :param name_or_suffix: 在文件名还是后缀名中匹配，可传入 'name' 'suffix' 'full'
    :param match_case: 是否区分大小写
    :param return_one: 只返回第一个结果还是返回全部结果
    :param each_key: 是否分开返回每个key的结果
    :param deep_first: 是否深度优先搜索
    :return: Path对象或其组成的列表或字典
    """
    # -------------- 处理关键字 --------------
    if isinstance(keys, str):
        keys = (keys,)

    keys = map(lambda x: str(x), keys)

    if name_or_suffix == 'suffix':
        keys = map(lambda x: x if x.startswith('.') else f'.{x}', keys)

    if not match_case:
        keys = map(lambda x: x.lower(), keys)

    keys = set(keys)

    # -------------- 执行查找操作 --------------
    results = {x: None for x in keys} if each_key else []

    folders = []
    for item in Path(path).iterdir():
        # 判断模式是否和当前类型一致，不一致则跳过该文件（夹）
        if ((file_or_dir == 'both')
                or (file_or_dir == 'file' and item.is_file())
                or (file_or_dir == 'dir' and item.is_dir())):
            # 准备待匹配的部分
            if name_or_suffix == 'name':
                find_str = item.stem
            elif name_or_suffix == 'suffix':
                find_str = item.suffix
            elif name_or_suffix == 'full':
                find_str = item.name
            else:
                raise ValueError("name_or_suffix参数只能传入'name', 'suffix', 'full'")

            # 若不区分大小写，全部转为小写
            if not match_case:
                find_str = find_str.lower()

            # 对关键字进行匹配
            is_it = None
            item_keys = []
            for key in tuple(keys):
                if (fuzzy and key in find_str) or (not fuzzy and find_str == key):
                    is_it = True
                    item_keys.append(key)

                    if return_one:
                        keys.remove(key)

                    if not each_key:
                        break

            # 若匹配成功，即该文件（夹）为结果（之一）
            if is_it:
                # 用字典返回每个key的结果
                if each_key:
                    for k in item_keys:
                        # 如果只要第一个结果，且该key值已经有结果，就跳到下一个
                        if return_one and results.get(k, None):
                            continue

                        if results.get(k, None) is None:
                            results[k] = item if return_one else [item]
                        else:
                            results[k].append(item)

                # 用列表或Path对象返回全部结果
                else:
                    if return_one:
                        return item
                    else:
                        results.append(item)

        # -------------- 如果是文件夹，调用自己，进入下层 --------------
        if item.is_dir() and find_in_sub and keys:
            # 广度优先，记录文件夹，等下再处理
            if not deep_first:
                folders.append(item)

            # 深度优先，遇到文件夹即时进入查找
            else:
                sub_results = find_path(item, keys, file_or_dir, fuzzy, find_in_sub, name_or_suffix,
                                        match_case, return_one, each_key, deep_first)
                results = _merge_results(results, sub_results, each_key, return_one)

    # 广度优先，上面判断完文件，再逐个进入该层文件夹查找
    if not deep_first:
        for item in folders:
            sub_results = find_path(item, keys, file_or_dir, fuzzy, find_in_sub, name_or_suffix,
                                    match_case, return_one, each_key, deep_first)
            results = _merge_results(results, sub_results, each_key, return_one)

    return results


def clean_dir(path: str, ignore: Union[str, list, tuple] = None) -> None:
    """清空一个文件夹，除了ignore里的文件和文件夹                  \n
    :param path: 要清空的文件夹路径
    :param ignore: 忽略列表或文件（夹）全名
    :return: None
    """
    if isinstance(ignore, str):
        ignore = (ignore,)

    for f in Path(path).iterdir():
        if not ignore or f.name not in ignore:
            if f.is_file():
                f.unlink()
            elif f.is_dir():
                rmtree(f, True)


def get_usable_path(path: Union[str, Path]) -> Path:
    """检查文件或文件夹是否有重名，并返回可以使用的路径           \n
    :param path: 文件或文件夹路径
    :return: 可用的路径，Path对象
    """
    path = Path(path)
    parent = path.parent
    path = parent / make_valid_name(path.name)
    name = path.stem if path.is_file() else path.name
    ext = path.suffix if path.is_file() else ''

    first_time = True

    while path.exists():
        r = search(r'(.*)_(\d+)$', name)

        if not r or (r and first_time):
            src_name, num = name, '1'
        else:
            src_name, num = r.group(1), int(r.group(2)) + 1

        name = f'{src_name}_{num}'
        path = parent / f'{name}{ext}'
        first_time = None

    return path


def get_usable_name(path: Union[str, Path], name: str) -> str:
    """检查文件或文件夹是否重名，并返回可以使用的名称                  \n
    :param path: 文件夹路径
    :param name: 要检查的名称
    :return: 可用的文件名
    """
    return get_usable_path(Path(path) / name).name


def get_desktop() -> str:
    """获取桌面路径"""
    from winreg import QueryValueEx, OpenKey, HKEY_CURRENT_USER
    return QueryValueEx(
        OpenKey(HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'),
        "Desktop")[0]


def get_size(path: Union[str, Path], unit: str = None) -> Union[int, float]:
    """获取文件或文件夹大小                  \n
    :param path: 文件或文件夹路径
    :param unit: 单位，'k' 'm' 'g'
    :return: 文件或文件夹大小，非占用空间
    """
    from os import walk
    from os.path import getsize, join, isdir, exists

    path = str(path)

    if not exists(path):
        raise FileNotFoundError
    elif isdir(path):
        size = 0
        for root, dirs, files in walk(path):
            size += sum([getsize(join(root, name)) for name in files])
    else:
        size = getsize(path)

    unit = unit.lower() if unit else None
    if unit == 'k':
        return size / 1024
    elif unit == 'm':
        return size / 1048576
    elif unit == 'g':
        return size / 1073741824
    else:
        return size


def get_long(txt) -> int:
    """返回字符串中字符个数（一个汉字是2个字符）          \n
    :param txt: 字符串
    :return: 字符个数
    """
    txt_len = len(txt)
    return int((len(txt.encode('utf-8')) - txt_len) / 2 + txt_len)


def make_valid_name(full_name: str) -> str:
    """获取有效的文件名                  \n
    :param full_name: 文件名
    :return: 可用的文件名
    """
    # ----------------去除前后空格----------------
    full_name = full_name.strip()

    # ----------------使总长度不大于255个字符（一个汉字是2个字符）----------------
    r = search(r'(.*)(\.[^.]+$)', full_name)  # 拆分文件名和后缀名
    if r:
        name, ext = r.group(1), r.group(2)
        ext_long = len(ext)
    else:
        name, ext = full_name, ''
        ext_long = 0

    while get_long(name) > 255 - ext_long:
        name = name[:-1]

    full_name = f'{name}{ext}'

    # ----------------去除不允许存在的字符----------------
    return sub(r'[<>/\\|:*?\n]', ' ', full_name)


def _merge_results(par_results: Union[dict, list],
                   sub_results: Union[dict, list, Path],
                   each_key: bool,
                   return_one: bool) -> Union[dict, list, Path]:
    """合并查找结果                                      \n
    :param par_results: 父级查找结果
    :param sub_results: 子文件夹查找结果
    :param each_key: 是否分开返回每个key的结果
    :param return_one: 只返回第一个结果还是返回全部结果
    :return: 合并后的结果
    """
    # 用字典返回每个关键字结果
    if each_key and any(sub_results.values()):
        # 将父字典和子字典的结果合并
        for k in tuple(x for x in sub_results if sub_results[x]):
            if par_results.get(k, None) is None:
                par_results[k] = sub_results[k] if return_one else [sub_results[k]]
            else:
                par_results[k].extend(sub_results[k])

    # 用列表或Path对象返回查找结果
    elif not each_key and sub_results:
        if return_one:
            return sub_results
        else:
            par_results.extend(sub_results)

    return par_results
