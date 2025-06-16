import urllib3
import copy

from yplib import *
from yplib import to_list, to_log_file
from yplib.common_package import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 有关 http 的工具类


# 创建一个线程本地存储对象
__THREAD_LOCAL_HTTP_UTIL_DATA = threading.local()


def get_thread_local_http_data() -> dict[str, Any]:
    if not hasattr(__THREAD_LOCAL_HTTP_UTIL_DATA, 'data'):
        __THREAD_LOCAL_HTTP_UTIL_DATA.data = {}
    return __THREAD_LOCAL_HTTP_UTIL_DATA.data


def get_and_save_data_to_thread_db(
        BASE_URL: str = None,
        url_common_param: dict = None,
        session: requests.Session | None = None,
        headers: dict = None,
        cookie: dict | None = None,  # 我也不知道类型
        auth: dict | None = None,  # 我也不知道类型
        r_json: bool = None) -> list[Any]:
    r_list = []
    # 输出非空字段
    for key, value in {
        'BASE_URL': BASE_URL,
        'url_common_param': url_common_param,
        'session': session,
        'headers': headers,
        'cookie': cookie,
        'auth': auth,
        'r_json': r_json,
    }.items():
        this_key = f'{key}__{key}'
        value_temp = value if value is not None else get_thread_local_http_data().get(this_key, None)
        value_temp2 = value_temp
        get_thread_local_http_data()[this_key] = value_temp
        # 需要深拷贝
        if key == 'headers' and value_temp is not None:
            value_temp2 = copy.deepcopy(value_temp)
        r_list.append(value_temp2)
    return r_list


# 是否打印日志
def get_or_set_http_log_flag(r_flag: bool = None) -> None:
    key = 'set_log_flag'
    http_log_data = get_thread_local_http_data()
    if r_flag is not None:
        http_log_data[key] = r_flag
    return http_log_data[key] if key in http_log_data else None


def do_parser(file_path: str = None,
              html_data: list[str] | str = '',
              selector=None) -> list[bs4.Tag]:
    """
    解析 html 中的数据
    file_path :   html 文件的路径
    html_data :   html 数据
    selector  :   选择器
    """
    if file_path is not None:
        html_str = ''.join(to_list(file_path))
    else:
        if isinstance(html_data, list):
            html_str = ''.join(html_data)
        else:
            html_str = str(html_data)
    return BeautifulSoup(html_str, 'html.parser').select(selector)


# div_list_content = do_parser(r'D:\notepad_file\202306\a.html', selector='table.reference')[4].select('tr')
#
# for i in range(len(div_list_content) - 1):
#     td = div_list_content[i + 1].select('td')
#     num = td[0].text
#     fun_name = td[1].select('a')[0].text
#     fun_desc = td[1].text.replace(fun_name, '')
#     print(f'{num} : {fun_name} , {fun_desc}')


def do_get_response(url: str = None,
                    session: requests.Session | None = None,
                    headers: dict | None = None,
                    cookie: dict | None = None,  # 我也不知道类型
                    auth: dict | None = None,  # 我也不知道类型
                    timeout: int = 1000,
                    verify: bool = False) -> requests.Response:
    """
    get 类型的请求
    session : session , 默认 : requests.session()
    headers : headers
    cookie  : cookie
    auth    : auth
    verify  : verify
    r_json : 返回的数据是否是一个 json 类型的数据
    """
    if session is None:
        session = requests.session()
    # requests.packages.urllib3.disable_warnings()
    return session.get(url=url, headers=headers, auth=auth, timeout=timeout, verify=verify, cookies=cookie)


def do_get(url: str = None,
           param: dict = None,
           session: requests.Session | None = None,
           headers: dict | None = None,
           cookie: dict | None = None,  # 我也不知道类型
           auth: dict | None = None,  # 我也不知道类型
           timeout: int = 1000,
           BASE_URL: str = None,
           url_common_param: dict = None,
           verify: bool = False,
           r_json: bool = True) -> dict | str:
    """
    param : 都是参数
    data  : 都是参数
    """
    [BASE_URL, url_common_param, session, headers, cookie, auth, r_json] = get_and_save_data_to_thread_db(
        BASE_URL=BASE_URL,
        url_common_param=url_common_param,
        session=session,
        headers=headers,
        cookie=cookie,
        auth=auth,
        r_json=r_json
    )
    start_time = time.time()
    url = get_url(url, BASE_URL, url_common_param=url_common_param)
    if param:
        url += ('&' if '?' in url else '?') + format_sorted_kv_string(param, sep='&', join='=', join_list=',')

    response = do_get_response(url=url, session=session, headers=headers, cookie=cookie, auth=auth, timeout=timeout, verify=verify)
    response.encoding = 'utf-8'
    r1 = json.loads(response.text.strip()) if r_json else response.text.strip()

    # for log 部分
    do_http_log(url=url,
                BASE_URL=BASE_URL,
                param=param,
                session=session,
                headers=headers,
                cookie=cookie,
                response=response,
                response_text=r1,
                method='get',
                elapsed_time_ms=to_int((time.time() - start_time) * 1000),
                r_json=r_json)

    return r1


# get url
def get_url(url: str = None,
            BASE_URL: str = None,
            url_common_param: dict = None) -> str:
    if BASE_URL is not None and url.startswith(BASE_URL):
        BASE_URL = ''
    r1 = ('' if BASE_URL is None else BASE_URL) + url
    if url_common_param is not None:
        r1 += ('&' if '?' in r1 else '?') + format_sorted_kv_string(url_common_param, sep='&', join='=', join_list=',')
    return r1


# 返回的是一个 json 数据
def do_get_json(url: str = None,
                param: dict = None,
                session: requests.Session | None = None,
                headers: dict | None = None,
                cookie: dict | None = None,  # 我也不知道类型
                auth: dict | None = None,  # 我也不知道类型
                timeout: int = 1000,
                BASE_URL: str = None,
                url_common_param: dict = None,
                verify: bool = False) -> dict:
    return do_get(url=url,
                  BASE_URL=BASE_URL,
                  url_common_param=url_common_param,
                  param=param,
                  session=session,
                  headers=headers,
                  cookie=cookie,
                  auth=auth,
                  timeout=timeout,
                  verify=verify,
                  r_json=True)


def do_download(url: str = None,
                file_name: str = None,
                file_path: str = 'download',
                session: requests.Session | None = None,
                headers: dict | None = None,
                cookie: dict | None = None,  # 我也不知道类型
                auth: dict | None = None,  # 我也不知道类型
                timeout: int = 1000,
                BASE_URL: str = None,
                url_common_param: dict = None,
                verify: bool = False) -> tuple[str, str, str] | None:
    r"""
    下载
    file_name   : 文件名 , 默认 txt
                  当文件名是 C:\Users\yangpu\Desktop\study\abc\d\e\f\a.txt 这种类型的时候, 可以直接创建文件夹,
                      会赋值 file_path=C:\Users\yangpu\Desktop\study\abc\d\e\f,
                            file_name=a.txt,
                            fixed_name=True
                  当文件名是 abc 的时候, 按照正常值,计算
    file_path   : 文件路径
    """
    url = get_url(url, BASE_URL, url_common_param=url_common_param)
    if session is None:
        session = requests.session()
    # requests.packages.urllib3.disable_warnings()
    response = session.get(url=url, headers=headers, auth=auth, timeout=timeout, verify=verify, cookies=cookie)
    if response.status_code != 200:
        to_log_file('error', url, response.status_code)
        return None
    # 默认的文件路径,
    file_name = url[url.rfind('/') + 1: len(url)] if file_name is None else file_name
    if file_name is not None:
        file_name = str(file_name)
        for sep in ['\\', '/']:
            # C:\Users\yangpu\Desktop\study\abc\d\e\f\a.txt
            f_n = file_name.split(sep)
            if len(f_n) > 1:
                # a.txt
                file_name = f_n[-1]
                # C:\Users\yangpu\Desktop\study\abc\d\e\f
                file_path = sep.join(f_n[0:-1])
    # 检查路径 file_path
    while file_path.endswith('/'):
        file_path = file_path[0:-1]
    check_file(file_path)
    # 去掉文件名称中的非法字符
    file_name = re.sub('[^a-zA-Z0-9._]', '', file_name)
    path_name = file_path + '/' + file_name
    # 重复下载的删掉以前的
    if os.path.exists(path_name):
        os.remove(path_name)
    # 下载的文件
    with open(path_name, 'wb') as f:
        f.write(response.content)
    # 返回全路径名称, 文件名, 路径名
    return path_name, file_name, file_path


def do_post_response(url: str = None,
                     param: dict = None,
                     session: requests.Session | None = None,
                     headers: dict | None = None,
                     cookie: dict | None = None,  # 我也不知道类型
                     auth: dict | None = None,  # 我也不知道类型
                     timeout: int = 1000,
                     url_common_param: dict = None,
                     verify: bool = False) -> requests.Response:
    """
    post 类型的请求
    data         : data post 体中的数据
    is_form_data : 是否是 form 表单
    headers      : headers
    cookie       : cookie
    auth         : auth
    verify       : verify
    r_json       : 返回的数据是否是一个 json 类型的数据
    """
    # headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # data = {}
    # data['a'] = APP_KEY
    # data['secretkey'] = SECRET_KEY
    # data['content'] = content
    # data['phone'] = obtainMobileIndonesia(mobile)
    # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    # response = requests.post(URL, headers=headers, verify=False, data=data)
    # response.encoding = 'utf-8'
    # text = response.text
    # text = text.replace('\n', '')
    # text = text.replace('\r', '')
    # return text
    if session is None:
        session = requests.session()
    # requests.packages.urllib3.disable_warnings()
    headers = headers or {}
    headers.setdefault('Content-Type', 'application/json;charset=UTF-8')
    return session.post(url=url,
                        data=param if headers['Content-Type'] == 'application/x-www-form-urlencoded' else json.dumps(param),
                        headers=headers,
                        auth=auth,
                        timeout=timeout,
                        verify=verify,
                        cookies=cookie)


def do_post_form_data(url: str = None,
                      param: dict = None,
                      session: requests.Session | None = None,
                      headers: dict | None = None,
                      cookie: dict | None = None,  # 我也不知道类型
                      auth: dict | None = None,  # 我也不知道类型
                      timeout: int = 1000,
                      url_common_param: dict = None,
                      BASE_URL: str = None,
                      verify: bool = False,
                      r_json: bool = True) -> dict:
    return do_post(url=url,
                   param=param,
                   session=session,
                   headers=headers,
                   cookie=cookie,
                   auth=auth,
                   timeout=timeout,
                   url_common_param=url_common_param,
                   BASE_URL=BASE_URL,
                   is_form_data=True,
                   verify=verify,
                   r_json=r_json)


def do_post(url: str = None,
            param: dict = None,
            session: requests.Session | None = None,
            headers: dict | None = None,
            cookie: dict | None = None,  # 我也不知道类型
            auth: dict | None = None,  # 我也不知道类型
            timeout: int = 1000,
            is_form_data=False,
            url_common_param: dict = None,
            BASE_URL: str = None,
            verify: bool = False,
            r_json: bool = True) -> dict | str:
    start_time = time.time()

    [BASE_URL, url_common_param, session, headers, cookie, auth, r_json] = get_and_save_data_to_thread_db(
        BASE_URL=BASE_URL,
        url_common_param=url_common_param,
        session=session,
        headers=headers,
        cookie=cookie,
        auth=auth,
        r_json=r_json
    )
    if is_form_data:
        headers = headers or {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

    url = get_url(url, BASE_URL, url_common_param=url_common_param)
    response = do_post_response(url=url,
                                param=param,
                                session=session,
                                headers=headers,
                                cookie=cookie,
                                auth=auth,
                                timeout=timeout,
                                verify=verify)
    response.encoding = 'utf-8'
    r1 = json.loads(response.text.strip()) if r_json else response.text.strip()

    # for log 部分
    do_http_log(url=url,
                BASE_URL=BASE_URL,
                param=param,
                session=session,
                headers=headers,
                cookie=cookie,
                response=response,
                response_text=r1,
                method='post',
                elapsed_time_ms=to_int((time.time() - start_time) * 1000),
                r_json=r_json)
    return r1


def do_http_log(url: str = None,
                BASE_URL: str = None,
                param: dict = None,
                session: requests.Session | None = None,
                headers: dict | None = None,
                cookie: dict | None = None,  # 我也不知道类型
                response: requests.Response | None = None,
                response_text: str | None = None,
                method: str = None,
                elapsed_time_ms: int = None,
                r_json: bool = False) -> None:
    if get_or_set_http_log_flag(None) is False:
        return
    # for log 部分
    temp_1 = get_thread_local_index_data()
    flag = temp_1.get('_use_fun_flag', False)
    if not flag:
        return
    log_fun = temp_1['_use_fun']
    log_fun('', line_with_space_count=1)
    # 日志字段列表
    log_fields = {
        'url': [get_url(url, BASE_URL), False],
        'method': [str(method).upper() if method is not None else method, False],
        'session': [session, False],
        'headers': [headers, True],
        'cookie': [cookie, False],
        'request_param': [param, True],
        'response': [response, False],
        'elapsed_time_ms': [elapsed_time_ms, False],
    }
    # 输出非空字段
    for key, [value, flag] in log_fields.items():
        if value is not None:
            if flag:
                log_fun(f'{key}:')
                r_temp = json.dumps(value, indent=4, ensure_ascii=False, sort_keys=True)
                r_temp = rreplace(r_temp, '\n}', '\n }', 1)
                log_fun(r_temp)
            else:
                log_fun(f'{key}:', value)
    # 输出响应正文
    log_fun('response_text:')
    r_temp = json.dumps(response_text, indent=4, ensure_ascii=False, sort_keys=True) if r_json else response_text
    r_temp = rreplace(r_temp, '\n}', '\n }', 1)
    log_fun(r_temp)
    log_fun(f'{str(method).upper() if method is not None else method}__END')
    log_fun()
    log_fun('####################################################################################################', line_with_space_count=-1)
