# -*- coding:utf-8 -*-
from pathlib import Path
from shutil import rmtree
from subprocess import Popen, PIPE
from typing import Union

from .paths import get_usable_name


def unzip_7z(path: Union[str, Path],
             to_path: str,
             no_dir: bool = True,
             file_exists: str = 'skip',
             to_self_dir: bool = True) -> bool:
    """使用7z解压一个压缩文件
    :param path: 压缩文件路径
    :param to_path: 解压目标路径
    :param no_dir: 是否保留文件夹
    :param file_exists: 'skip' 'overwrite' 'rename'
    :param to_self_dir: 是否解压在独立文件夹中
    :return: 是否压缩成功
    """
    if file_exists == 'skip':
        exists = '-aos'
    elif file_exists == 'rename':
        exists = '-aou'
    elif file_exists == 'overwrite':
        exists = '-aoa'
    else:
        raise ValueError("file_exists参数只能传入'skip' 'overwrite' 'rename'")

    mode = 'e' if no_dir else 'x'
    seven_path = Path(__file__).parent / '7z\\7z.exe'
    z = seven_path if seven_path.exists() else '7z'

    if to_self_dir:
        name = Path(path).stem

        if Path(f'{to_path}\\{name}').exists():
            if file_exists == 'skip':
                return False
            elif file_exists == 'rename':
                name = get_usable_name(to_path, name)
            elif file_exists == 'overwrite':
                rmtree(f'{to_path}\\{name}')

        to_path = f'{to_path}\\{name}'

    Path(to_path).mkdir(parents=True, exist_ok=True)

    proc = Popen(f'{z} {mode} {exists} "{path}" "-o{to_path}"',
                 shell=True, stdout=PIPE, stderr=PIPE, bufsize=-1)
    proc.wait()

    return False if proc.communicate()[1] else True


def zip_7z(paths: Union[str, Path, list, tuple],
           to_path: str,
           zip_name: str = None,
           file_exists: str = 'rename') -> Union[bool, str]:
    """打包若干个路径
    :param paths: 要打包的文件路径，可传入多个路径。支持通配符*和?
    :param to_path: 打包文件保存路径
    :param zip_name: 打包文件名称，如果是打包单个路径，可以忽略，不带后缀
    :param file_exists: 'skip' 'overwrite' 'rename' 'merge'
    :return: 是否打包成功
    """
    if isinstance(paths, (str, Path)):
        paths = (paths,)

    if len(set(Path(x).name for x in paths)) < len(paths):
        raise ValueError('路径中有重名文件或文件夹')

    if not zip_name:
        if len(paths) == 1:
            zip_name = f'{Path(paths[0]).stem}.zip'
        else:
            raise ValueError('未传入压缩文件名参数')
    else:
        zip_name = f'{zip_name}.zip'

    full_path = Path(f'{to_path}\\{zip_name}')
    if full_path.exists():
        if file_exists == 'skip':
            return False
        elif file_exists == 'overwrite':
            full_path.unlink()
        elif file_exists == 'rename':
            zip_name = get_usable_name(to_path, zip_name)
        elif file_exists == 'merge':
            pass
        else:
            raise ValueError("只能传入 'skip' 'overwrite' 'rename' 'merge'")

    Path(to_path).mkdir(parents=True, exist_ok=True)
    full_path = f'{to_path}\\{zip_name}'

    files_list = []
    for f in paths:
        file = Path(f)
        if not file.exists():
            raise FileNotFoundError(f'找不到文件：{f}')
        files_list.append(f'"{file}"')
    files_str = ' '.join(files_list)

    seven_path = Path(__file__).parent / '7z\\7z.exe'
    z = seven_path if seven_path.exists() else '7z'

    proc = Popen(f'{z} a "{to_path}\\{zip_name}" {files_str}',
                 shell=True, stdout=PIPE, stderr=PIPE, bufsize=-1)
    proc.wait()

    return False if proc.communicate()[1] else full_path


def zip_a_dir(path: Union[str, Path],
              to_path: str,
              parent_dir: bool = False,
              ignore: Union[Path, str, list, tuple, set] = None,
              file_exists: str = 'rename',
              by_7z: bool = True) -> Union[bool, str]:
    """打包一个文件夹
    :param path: 文件夹路径
    :param to_path: 压缩文件保存位置
    :param parent_dir: 是否保留父级文件夹
    :param ignore: 忽略的文件，可传入一个或多个，如parent_dir为True则此参数无效
    :param file_exists: 'skip' 'overwrite' 'rename' 'merge'
    :param by_7z: 是否使用7z
    :return: 是否打包成功
    """
    path = Path(path)
    if not path.is_dir():
        raise TypeError('传入的不是文件夹')

    zip_name = path.name

    if parent_dir:
        paths = path

    else:
        if ignore is None:
            ignore = tuple()
        elif isinstance(ignore, (str, Path)):
            ignore = (ignore,)

        paths = tuple(file for file in path.iterdir() if file.name not in ignore)

    return zip_7z(paths, to_path, zip_name, file_exists) if by_7z else None

# def unzip(zip_path: str, to_path: str, no_folder=None):
#     乱码文件夹列表 = []  # 记录乱码的文件夹
#     with zipfile.ZipFile(zip_path, 'r') as f:
#         for fn in f.namelist():
#             根目录 = Path(to_path)
#             无乱码路径 = 根目录 / fn.encode("cp437").decode("gbk")
#             解压路径 = Path(f.extract(fn, path=to_path))  # 解压并获取路径对象
#
#             is_file = False if 解压路径.is_dir() else True
#             if not is_file and 无乱码路径 != 解压路径:
#                 乱码文件夹列表.append(解压路径)
#
#             路径 = 无乱码路径.parent / get_valid_name(无乱码路径.parent, 无乱码路径.name) if is_file else 无乱码路径
#             解压路径.rename(路径)  # 重命名乱码文件
#
#             if no_folder and is_file and 无乱码路径.parent != 根目录:
#                 # 移动文件到根目录
#                 文件名 = get_valid_name(根目录, 无乱码路径.name)
#                 无乱码路径.replace(根目录 / 文件名)
#
#     for i in 根目录.iterdir():
#         if i in 乱码文件夹列表 or no_folder:
#             shutil.rmtree(str(i), ignore_errors=True)
#
#
# def do_zip(源路径: str, 重命名: str = None, 包含文件夹: bool = False):
#     目标 = Path(源路径).parent
#     文件夹名 = Path(源路径).name
#     起始 = 0 if 包含文件夹 else len(文件夹名)
#     name = 文件夹名 if not 重命名 else 重命名
#     文件名 = f'{目标 / name}.zip'
#     zipf = zipfile.ZipFile(文件名, 'w')
#     pre_len = len(os.path.dirname(源路径))
#
#     for 父路径, 文件夹s, 文件s in os.walk(源路径):
#         for 文件 in 文件s:
#             文件路径 = os.path.join(父路径, 文件)
#             相对路径 = 文件路径[pre_len:].strip(os.path.sep)  # os.path.sep是路径分隔符，win是\
#             zipf.write(文件路径, 相对路径[起始:])
#
#     zipf.close()
#     return 文件名
