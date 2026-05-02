# -*- coding:utf-8 -*-
# win32com安装方法：python -m pip install pypiwin32
from pathlib import Path
from shutil import copy, rmtree
from typing import Union

from win32com import client

from .paths import get_usable_name
from .zip import unzip_7z


def get_pics_in_docx(path: Union[str, Path], to_path: str = None) -> str:
    """获取docx中的图片，存放源路径在独立文件夹中                  \n
    :param path: docx文件路径
    :param to_path: 图片文件夹保存路径，默认和docx文件相同
    :return: 存放图片的文件夹路径
    """
    path = Path(path)

    new_name = get_usable_name(path.parent, path.name)
    zip_path = f'{path.parent}\\{new_name[:new_name.rfind(".")]}.zip'
    copy(str(path), zip_path)

    to_path = to_path or path.parent
    folder_path = f'{to_path}\\{get_usable_name(to_path, path.stem)}'
    unzip_7z(zip_path, folder_path, True, 'overwrite', False)
    Path(zip_path).unlink()

    for i in Path(folder_path).iterdir():
        if i.is_dir():
            rmtree(str(i))
            continue

        if i.suffix not in ('.jpg', '.jpeg', '.png', '.gif', '.bmp'):
            i.unlink()

    return folder_path


def doc_to_docx(path: Union[Path, str], del_src: bool = True) -> bool:
    """把doc格式另存为docx格式                  \n
    :param path: doc文件路径
    :param del_src: 另存之后是否删除源文件
    :return: 是否成功
    """
    word = None

    try:
        word = client.Dispatch("Kwps.Application")  # 调用WPS程序
    except:
        try:
            word = client.gencache.EnsureDispatch('Word.Application')  # 调用Office程序
        except:
            pass

    if word:
        docx = word.Documents.Open(str(path))
        docx.SaveAs(f"{path}x", 51)
        docx.Close()

        if del_src:
            Path(path).unlink()

        return True

    return False
