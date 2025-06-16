from yplib import *
from yplib.index import *


def get_file(file_path: str = None,
             path_prefix: str = None,
             prefix: str = None,
             path_contain: str = None,
             contain: str = None,
             path_suffix: str = None,
             suffix: str = None) -> list[str]:
    """
    有关文件的操作
    查询指定文件夹下面的所有的文件信息, 也可以是指定的文件
    file_path     : 文件路径
    path_prefix   : 文件路径,以 prefix 开头
    prefix        : 文件名称,以 prefix 开头
    path_contain  : 文件路径,含有
    contain       : 文件名称,含有
    path_suffix   : 文件路径,以 suffix 结尾
    suffix        : 文件名称,以 suffix 结尾
    return list
    """
    if file_path is None:
        file_path = os.path.dirname(os.path.abspath('.'))
    list_data = []
    get_file_all(file_path, list_data, path_prefix, prefix, path_contain, contain, path_suffix, suffix)
    # 去一下重复的数据
    return list(set(list_data))


def get_folder(file_path: str = None,
               prefix: str = None,
               contain: str = None,
               suffix: str = None) -> list[str]:
    """
    有关文件的操作, 只查询文件夹
    查询指定文件夹下面的所有的文件信息, 也可以是指定的文件
    param list
    return list
    """
    if file_path is None:
        file_path = os.path.dirname(os.path.abspath('.'))
    list_data = []
    get_folder_all(file_path, list_data, prefix, contain, suffix)
    # 去一下重复的数据
    return list(set(list_data))


# 是否包含指定的文件
def contain_file(file_path: str = None,
                 prefix: str = None,
                 contain: str = None,
                 suffix: str = None) -> bool:
    return len(get_file(file_path, prefix, contain, suffix)) > 0


def get_file_data_line(file_path: str = None,
                       find_str: str = 'find_str',
                       from_last: bool = True) -> str | None:
    """
    在指定的文件夹中查找包含指定字符串的数据
    file_path : 文件路径
    find_str : 查找的字符串
    from_last : 是否从文件的最后开始查找
    """
    file_list = get_file(file_path)
    for one_file in file_list:
        one_list = to_list(one_file)
        i = 0
        if from_last:
            i = len(one_list) - 1
        while -1 < i < len(one_list):
            one_line = one_list[i]
            if from_last:
                i -= 1
            else:
                i += 1
            if one_line.find(find_str) > -1:
                return one_line
    return None


# 查询指定文件夹下面的所有的文件信息, 也可以是指定的文件
def get_file_all(file_path: str = None,
                 list_data: list = None,
                 path_prefix: str = None,
                 prefix: str = None,
                 path_contain: str = None,
                 contain: str = None,
                 path_suffix: str = None,
                 suffix: str = None) -> None:
    if os.path.isdir(file_path):
        for root, dir_names, file_names in os.walk(file_path):
            for file_name in file_names:
                if (get_file_check(os.path.join(root, file_name), path_prefix, path_contain, path_suffix)
                        and get_file_check(file_name, prefix, contain, suffix)):
                    list_data.append(os.path.join(root, file_name))
            for dir_name in dir_names:
                get_file_all(os.path.join(root, dir_name), list_data, path_prefix, prefix, path_contain, contain, path_suffix, suffix)
    elif (get_file_check(file_path, prefix, contain, suffix)
          and get_file_check(file_path, path_prefix, path_contain, path_suffix)):
        list_data.append(file_path)


# 查询指定文件夹下面的所有的文件信息, 也可以是指定的文件
def get_folder_all(file_path: str = None,
                   list_data: list = None,
                   prefix: str = None,
                   contain: str = None,
                   suffix: str = None) -> None:
    if os.path.isdir(file_path):
        for root, dir_names, file_names in os.walk(file_path):
            for dir_name in dir_names:
                dir_name_path = os.path.join(root, dir_name)
                if get_file_check(dir_name_path, prefix, contain, suffix):
                    list_data.append(dir_name_path)
                else:
                    get_folder_all(dir_name_path, list_data, prefix, contain, suffix)


def get_file_check(
        name: str = None,
        prefix: str = None,
        contain: str = None,
        suffix: str = None) -> bool:
    """
    检查文件是否符合要求
    prefix  : 前缀
    contain : 包含这个字符
    suffix  : 后缀
    """
    if name is None or name == '':
        return False
    p = True
    c = True
    s = True
    if prefix is not None:
        p = name.startswith(prefix)
    if contain is not None:
        c = name.find(contain) > -1
    if suffix is not None:
        s = name.endswith(suffix)
    return p and c and s


def find_file_by_content(file_path: str = '',
                         contain_txt: str = None,
                         prefix: str = None,
                         contain: str = None,
                         suffix: str = None) -> bool | None:
    """
    检查文件内容是否包含指定的字符串
    慎用,否则, 执行时间可能比较长
    """
    list_file = get_file(file_path, prefix, contain, suffix)
    if len(list_file) == 0:
        to_log(f'no_matched_file : {file_path} , {contain_txt} , {prefix} , {contain} , {suffix}')
        return False
    if contain_txt is None:
        to_log(list_file)
        return True
    for one_file in list_file:
        try:
            text_file = open(one_file, 'r', encoding='utf-8')
            for line in text_file.readlines():
                if line.find(contain_txt) > -1:
                    if line.endswith('\n'):
                        line = line[0:-1]
                    to_log(one_file, line)
        except Exception as e:
            to_log(one_file, e)
            continue

# print(get_file_data_line(r'D:\notepad_file\202306\a.txt', 'payout', from_last=False))

# file_all = get_file(r'C:\Users\yang\Desktop\ticket\no.use', path_contain='03')
#
# for one_file in file_all:
#     print(one_file)

# get_file_data_line(r'D:\notepad_file\202306', 'a')
# get_file_by_content(r'D:\notepad_file\202306', 'a')
# print(get_file(r'D:\notepad_file\202306', 'a'))
# print(get_file(r'D:\notepad_file\202306'))
# print(get_file())
# print(os.path.abspath('.'))

#
# a_list = get_folder(r'D:\code\20220916\a-java\platform', contain='build')
# for a1 in a_list:
#     os.remove(a1)
#
# print(json.dumps(a_list))

# print('end')
