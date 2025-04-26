#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2024/9/21 14:02
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import pandas as pd

from meutils.pipe import *


def to_html_plus(df, title='Title', subtitle='Subtitle', return_filename=False):
    from jinja2 import Environment, PackageLoader
    env = Environment(loader=PackageLoader('meutils'))
    template = env.get_template('df_html.j2')

    html_content = template.render(df_to_html=df.to_html(), title=title, subtitle=subtitle)
    if return_filename:
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.html', delete=False) as file:
            # logger.debug(file.name)
            file.write(html_content)
            file.seek(0)
            return file.name
    return html_content


if __name__ == '__main__':
    to_html_plus(pd.DataFrame(range(10)))