#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2023/5/18 16:39
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *


def doc2docx(doc_paths, outdir='.', max_workers=1):
    """todo: 多进程阻塞"""
    if isinstance(doc_paths, str):
        doc_paths = [doc_paths]
    max_workers = min(max_workers, len(doc_paths))
    func = partial(_doc2docx, outdir=outdir)
    return doc_paths | xProcessPoolExecutor(func, max_workers) | xlist


def _doc2docx(doc_path, outdir='.'):
    if Path(doc_path).is_file():
        cmd = 'libreoffice --headless --convert-to docx'.split() + [doc_path, '--outdir', outdir]
        p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        p.wait(timeout=16)
        stdout, stderr = p.communicate()
        if stderr:
            raise subprocess.SubprocessError(stderr)
        return stdout.decode()
    return False


def stream2tempfile4process(
        stream: Union[str, bytes] = b"temp",
        process_fn: Callable[[os.PathLike], Any] = lambda p: p.read_text(),
        delete=True
):
    # 创建临时文件
    import tempfile

    with tempfile.NamedTemporaryFile(delete=delete) as temp_file:
        p = Path(temp_file.name)
        if isinstance(stream, str):  # 写
            p.write_text(stream)
        else:
            p.write_bytes(stream)
        return process_fn(p)  # 读


def stream_parser(file_stream):
    """
        from fastapi import FastAPI, File, UploadFile

        file_stream = UploadFile(open(''))

        filename, file_stream = stream_parser(file_stream)
    """
    filename = ''
    # from fastapi import FastAPI, File, UploadFile
    if hasattr(file_stream, 'file'):
        filename = file_stream.file.name or file_stream.filename
        file_stream = file_stream.file
        if isinstance(file_stream, io.TextIOWrapper):  # 转 bytes
            file_stream = file_stream.buffer
        file_stream = file_stream.read()

    # st.file_uploader
    elif hasattr(file_stream, 'read'):
        filename = file_stream.name
        if isinstance(file_stream, io.TextIOWrapper):  # 转 bytes
            file_stream = file_stream.buffer
        file_stream = file_stream.read()

    # ValueError: I/O operation on closed file.
    # with file_stream:
    #     file_stream = file_stream.buffer.read()

    elif (
            isinstance(file_stream, (str, os.PathLike))
            and len(file_stream) < 256
            and Path(file_stream).is_file()
    ):
        filename = str(file_stream)
        file_stream = open(filename).read()

    elif isinstance(file_stream, (bytes, bytearray)):
        pass

    return filename, file_stream
