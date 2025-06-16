from yplib import *
from yplib.mail_html import *
from yplib.index import *


def send_mail(title: str = None,
              content: str = None,
              attach_file: str | list[str] | set[str] = None,
              user: str = '',
              password: str = '',
              send: str = '',
              send_port: int = 0,
              receivers: list[str] = None) -> None:
    """
    title       : 标题
    content     : 内容, html 形式的
    attach_file : 附件, 全路径
    """
    if title is None:
        title = to_datetime(r_str=True)
    if content is None:
        content = to_datetime(r_str=True)
    message = MIMEMultipart()
    # message = MIMEText(content, 'html', 'utf-8')  # 内容, 格式, 编码
    message.attach(MIMEText(content, 'html', 'utf-8'))
    if attach_file is not None:
        a_f_l = []
        if isinstance(attach_file, str):
            a_f_l.append(str(attach_file))
        elif isinstance(attach_file, list) or isinstance(attach_file, set):
            for a in attach_file:
                a_f_l.append(str(a))
        for a_f in a_f_l:
            with open(a_f, 'r', encoding='utf-8') as f:
                att1 = MIMEText(f.read(), 'plain', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            att1["Content-Disposition"] = f'attachment; filename="{a_f}"'
            message.attach(att1)
    message['From'] = "{}".format(user)
    message['To'] = ",".join(receivers)
    message['Subject'] = str(title)
    smtpObj = smtplib.SMTP_SSL(send, send_port)  # 启用SSL发信, 端口一般是465
    # try:
    smtpObj.login(user, password)
    smtpObj.sendmail(user, receivers, message.as_string())
    # return True
    # except smtplib.SMTPException as e:
    #     print(e)
    #     return False
    # finally:
    smtpObj.close()


def mail_notify(error_obj: dict = None,
                title: str = 'mail_notify',
                is_error: bool = True) -> None:
    if error_obj is None:
        error_obj = {}
    email_info = get_config_data('email_info')
    send_mail(title=title + '--' + to_datetime_str(),
              content=get_mail_html(error_obj, is_error=is_error),
              attach_file=None,
              user=email_info['user'],
              password=email_info['password'],
              send=email_info['send'],
              send_port=email_info['send_port'],
              receivers=email_info['receivers'])


def to_email(content: str,
             title: str = 'to_email') -> None:
    email_info = get_config_data('email_info')
    send_mail(title=title + '--' + to_datetime(r_str=True),
              content=content,
              attach_file=None,
              user=email_info['user'],
              password=email_info['password'],
              send=email_info['send'],
              send_port=email_info['send_port'],
              receivers=email_info['receivers'])


def get_mail_html(data_obj: dict | list[dict],
                  no_title: bool = None,
                  is_error: bool = None) -> str:
    """
    获得 邮件的内容信息
    正常的数据, 标准数据, 只发一个的那种
    data_obj = {
    	title: "里面的一份小标题",
    	type: "error",
    	content: [
    		{ "调用次数": 100, "成功次数": 50 },
    		"总体还算可以的"
    	]
    }
    正常的数据, 标准数据, 发几个的那种
    data_obj = [
    	{
    		"title": "里面的一份小标题",
    		"type": "error",
    		"content": [
    			{ "调用次数": 100, "成功次数": 50 },
    			"总体还算可以的"
    		]
    	},
    	{
    		"title": "里面的一份正常的标题",
    		"content": [
    			{ "调用次数": 500, "成功次数": 500 },
    			"总体不行的"
    		]
    	}
    ]
    异常的数据, 也能发送, 发几个的那种
    data_obj = [
        {"调用次数": 100, "成功次数": 50},
        {"查询次数": 200, "失败次数": 150},
        {"value": 735, "name": "Direct"},
        "总体还算可以的"
    ]
    异常的数据, 也能发送, 只发一个的那种, 但是 没有 title 那一栏目
    data_obj = [
    	"调用次数100",
    	"调用次数200",
    	"调用次数300",
    	"调用次数400",
    	1,
    	2,
    	4.5,
    	True,
    	"阿斯顿发到付阿斯顿发到付阿斯顿发到"
    ]
    """
    html_list = []
    # 如果是 list , set . 并且, 里面都是简单的对象,没有复杂对象这种, 那就使用一个发送吧
    is_simple = False
    if isinstance(data_obj, list) or isinstance(data_obj, set):
        if len(list(filter(lambda x: is_json_serializable(x), data_obj))) == 0:
            # 都是一些简单的对象
            is_simple = True
    if is_simple:
        # 默认有 没有 title
        t_i_n = no_title if no_title is not None else True
        html_list.append(get_mail_html_one(data_obj, no_title=t_i_n, is_error=is_error))
    else:
        if isinstance(data_obj, list) or isinstance(data_obj, set):
            for data_one in data_obj:
                html_list.append(get_mail_html_one(data_one, no_title=no_title, is_error=is_error))
        else:
            html_list.append(get_mail_html_one(data_obj, no_title=no_title, is_error=is_error))
    return ''.join(mail_html(html_list))


def get_mail_html_one(data_obj: dict | list,
                      no_title: bool = None,
                      is_error: bool = None) -> str:
    """
    获得 邮件的内容信息
    data_obj =
    {
    	"title": "里面的一份小标题",
    	"type": "error",
    	"content": {
    		"调用次数1": 100,
    		"成功次数2": 50,
    		"调用次数3": 1020,
    		"成功次数4": 510,
    		"调用次数5": 1030,
    		"成功次数6": 550,
    		"调用次数7": 1090,
    		"成功次数8": 590
    	}
    }
    data_obj =
    {
    	"title": "里面的一份小标题",
    	"type": "error",
    	"content": [
    		"调用次数1",
    		"可以",
    		{"调用次数1": 100},
    		{"成功次数2": 50},
    	]
    }
    data_obj = {
    	"调用次数": 100,
    	"成功次数": 50
    }
    title_is_none : True 代表, 里面设置的 title 是无效的, 没有 title
    is_error      : True 代表, 里面设置的 type 是无效的, 一定是 error 类型
    """
    title = data_obj['title'] if 'title' in data_obj else str(to_datetime())
    type_t = data_obj['type'] if 'type' in data_obj else 'normal'
    content = data_obj['content'] if 'content' in data_obj else data_obj
    stripe = False
    html_list = []
    title = title if no_title is None else None if no_title else title
    error = type_t == 'error' if is_error is None else is_error
    if isinstance(content, list) or isinstance(content, set):
        for o_c in content:
            if isinstance(o_c, dict) or isinstance(o_c, tuple):
                for o_k in o_c:
                    html_list.extend(mail_content_html(key=o_k, value=o_c[o_k], error=error, stripe=stripe))
                    stripe = not stripe
            else:
                html_list.extend(mail_content_html(key=o_c, error=error, stripe=stripe))
                stripe = not stripe
    elif isinstance(content, dict) or isinstance(content, tuple):
        for o_k in content:
            html_list.extend(mail_content_html(key=o_k, value=content[o_k], error=error, stripe=stripe))
            stripe = not stripe
    else:
        html_list.extend(mail_content_html(key=str(content), error=error, stripe=stripe))
    return ''.join(mail_title_html(title=title, body=html_list, error=error))
