from yplib.index import *


# mail 邮件中的 html 模板
def mail_html(body: list[str]) -> list[str]:
    s = ['<!DOCTYPE html>',
         '<html>',
         '<head>',
         '    <meta charset="utf-8"/>',
         '    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">',
         '    <title>-title-</title>',
         '</head>',
         '<body>',
         '-body-',
         '</body>',
         '</html>']
    return list(map(lambda x: x.replace('-title-', str(to_datetime())).replace('-body-', ''.join(body)), s))


# 邮件中的 title 的html 代码
def mail_title_html(title: str = None,
                    body: list[str] = None,
                    error: bool = False) -> list[str]:
    color = 'f35222' if error else '3ecf58'
    c = ['<div style="padding-bottom: 5px;background: white;text-align:center;">',
         '    <div style="border-radius:5px;">',
         '        <div style="padding: 5px;background:#-color-;border-radius:5px;">',
         '            <span style="font-size:17px;">-title-</span>',
         '        </div>',
         '        <div style="font-size:13px;text-align:center;border-radius:5px;">',
         '            -body-',
         '        </div>',
         '    </div>',
         '</div>']
    t = ['<div style="padding-bottom: 5px;background: white;text-align:center;">',
         '   <div style="font-size:13px;text-align:center;border-radius:5px;">',
         '       -body-',
         '   </div>',
         '</div>']
    return list(map(lambda x: x.replace('-title-', 'title' if title is None else title)
                    .replace('-body-', ''.join(body))
                    .replace('-color-', color), t if title is None else c))


# 邮件中的 content 的html 代码
def mail_content_html(key: str = None,
                      value: str = None,
                      error: bool = False,
                      stripe: bool = False) -> list[str]:
    color_normal_1 = 'bee9c6'
    color_normal_2 = 'cbf9d3'
    color_normal_colon = 'f3e4e4'
    color_normal_value = '9beda9'

    color_error_1 = 'e9b394'
    color_error_2 = 'e7b8d6'
    color_error_colon = 'e98c8c'
    color_error_value = 'ed90bb'
    if error:
        color_stripe = color_error_1 if stripe else color_error_2
        color_colon = color_error_colon
        color_value = color_error_value
    else:
        color_stripe = color_normal_1 if stripe else color_normal_2
        color_colon = color_normal_colon
        color_value = color_normal_value

    one = ['<div style="padding: 5px;background:#-color_stripe-;border-radius:5px;">',
           '    <span>-key-</span>',
           '</div>']
    key_value = ['<div style="border-radius:5px;padding:2px;background: #-color_stripe-;">',
                 '    <div style="width: 48%;display: inline-block;white-space: normal;word-wrap: break-word;">',
                 '        <div style="width: 92%;display: inline-block;text-align: right;">',
                 '            <span>-key-</span>',
                 '        </div>',
                 '        <div style="text-align: center;width: 10px;display: inline-block;float: right;border-radius: 3px;background: #-color_colon-;">',
                 '            <span>:</span>',
                 '        </div>',
                 '    </div>',
                 '    <div style="width: 50%;background: #-color_value-;display: inline-block;white-space: normal;word-wrap: break-word;border-radius:5px;">',
                 '        <div style="padding: 3px;">',
                 '            <span>-value-</span>',
                 '        </div>',
                 '    </div>',
                 '</div>']
    s = one if value is None else key_value
    return list(map(lambda x: x.replace('-color_stripe-', color_stripe)
                    .replace('-key-', str(key))
                    .replace('-value-', str(value))
                    .replace('-color_colon-', color_colon)
                    .replace('-color_value-', color_value), s))
