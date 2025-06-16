from yplib import *
from yplib.index import *


def get_markdown_text(data_obj: dict | list[dict],
                      no_title: bool = None,
                      is_error: bool = None) -> str:
    """
    获得 markdown 的内容信息
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
        html_list.append(get_markdown_one(data_obj, no_title=t_i_n, is_error=is_error))
    else:
        if isinstance(data_obj, list) or isinstance(data_obj, set):
            for data_one in data_obj:
                html_list.append(get_markdown_one(data_one, no_title=no_title, is_error=is_error))
        else:
            html_list.append(get_markdown_one(data_obj, no_title=no_title, is_error=is_error))
    return ''.join(html_list)


def get_markdown_one(data_obj: dict | list[dict],
                     no_title: bool = None,
                     is_error: bool = None) -> str:
    """
    获得 markdown 的内容信息
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
    type_1 = data_obj['type'] if 'type' in data_obj else 'normal'
    content = data_obj['content'] if 'content' in data_obj else data_obj
    stripe = False
    html_list = []
    title = title if no_title is None else None if no_title else title
    error = type_1 == 'error' if is_error is None else is_error
    if isinstance(content, list) or isinstance(content, set):
        for o_c in content:
            if isinstance(o_c, dict) or isinstance(o_c, tuple):
                for o_k in o_c:
                    html_list.extend(get_markdown_content(key=o_k, value=o_c[o_k], error=error))
                    stripe = not stripe
            else:
                html_list.extend(get_markdown_content(key=o_c, error=error))
                stripe = not stripe
    elif isinstance(content, dict) or isinstance(content, tuple):
        for o_k in content:
            html_list.extend(get_markdown_content(key=o_k, value=content[o_k], error=error))
            stripe = not stripe
    else:
        html_list.extend(get_markdown_content(key=str(content), error=error))
    return ''.join(get_markdown_title(title=title, body=html_list, error=error))


# markdown 中的 content 代码
def get_markdown_content(key: str = None,
                         value: str = None,
                         error: bool = False) -> list[str]:
    type_color = 'warning' if error else 'info'
    one = ['<font color="-type-">-key-</font>\n']
    key_value = ['<font color="comment">-key-</font> : <font color="-type-">-value-</font>\n']
    s = one if value is None else key_value
    return list(map(lambda x: x.replace('-type-', type_color)
                    .replace('-key-', str(key))
                    .replace('-value-', str(value)), s))


# markdown 中的 title 代码
def get_markdown_title(title: str = None,
                       body: list[str] = None,
                       error: bool = False) -> list[str]:
    if body is None:
        body = []
    type_color = 'warning' if error else 'info'
    c = ['### <font color="-type-">-title-</font>\n-body-']
    t = ['-body-']
    return list(map(lambda x: x.replace('-title-', 'title' if title is None else title)
                    .replace('-type-', type_color)
                    .replace('-body-', ''.join(body)), t if title is None else c))
