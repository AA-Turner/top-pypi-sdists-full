#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : pdf
# @Time         : 2022/6/30 下午3:41
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *


def extract_text(file_or_text):
    import fitz  # pymupdf 速度更快

    _bytes = b''
    if isinstance(file_or_text, (str, Path)) and Path(file_or_text).is_file():
        _bytes = Path(file_or_text).read_bytes()
    elif isinstance(file_or_text, bytes):
        _bytes = file_or_text

    else:
        return file_or_text

    return '\n'.join(page.get_text().strip() for page in fitz.Document(stream=_bytes))


def pdf2text(file_or_dir_or_files, n_jobs=3):
    if isinstance(file_or_dir_or_files, str) or not isinstance(file_or_dir_or_files, Iterable):
        p = Path(file_or_dir_or_files)
        if p.is_file():
            file_or_dir_or_files = [p]
        elif p.is_dir():
            file_or_dir_or_files = p.glob('*.pdf')
        else:
            raise ValueError('无效文件')

    _ = file_or_dir_or_files | xJobs(lambda p: (p, extract_text(p)), n_jobs)

    return pd.DataFrame(_, columns=['filename', 'text'])


def pdf2table(filename, pages='1', suppress_stdout=False, **kwargs):
    import camelot
    tables = camelot.read_pdf(filename, pages=pages, suppress_stdout=suppress_stdout, **kwargs)
    for t in tables:
        yield t.df


def doc2text(filename):
    pass


def doc2text(filename):
    pass


def extract_images_from_pdf(file, output: Optional[str] = None):
    import fitz

    # 打开PDF文件

    pdf_document = fitz.open(file)

    # 遍历每一页

    for page_number in range(pdf_document.page_count):

        page = pdf_document.load_page(page_number)

        image_list = page.get_images(full=True)

        # 遍历每个图像

        for image_index, img in enumerate(image_list):
            xref = img[0]

            base_image = pdf_document.extract_image(xref)

            image_bytes = base_image["image"]

            image_ext = base_image["ext"]

            image_filename = f"{output or ''}/image{page_number + 1}_{image_index + 1}.{image_ext}"
            Path(image_filename).parent.mkdir(parents=True, exist_ok=True)

            # 将图像写入文件

            with open(image_filename, "wb") as image_file:
                image_file.write(image_bytes)


if __name__ == '__main__':
    with timer():
        # r = extract_text('上海证券交易所证券交易业务指南第8号——科创板股票做市（上证函〔2022〕1155号 20220715）-1757338961901 (1).pdf')
        r = extract_text('非上市公司股权估值指引（2025年修订 中证协发〔2025〕86号 20250425 20250601）-1757078360106.pdf')

        # r = extract_images_from_pdf('《锋利的jQuery》(高清扫描版-有书签)_副本_加水印.pdf', 'images')

    # import tiktoken
    # print(tiktoken.encoding_for_model('gpt-3.5-turbo'))
