from yplib import *
from yplib.common_package import *
from yplib.file import get_file

__CONFIG_PATH = '.yp.config'

__CONFIG_PATH_BAK = '_yp.config'

# 创建一个线程本地存储对象
__THREAD_LOCAL_INDEX_DATA = threading.local()


def get_thread_local_index_data() -> dict[str, Any]:
    if not hasattr(__THREAD_LOCAL_INDEX_DATA, 'data'):
        __THREAD_LOCAL_INDEX_DATA.data = {}
    return __THREAD_LOCAL_INDEX_DATA.data


def is_all_chinese(text: str) -> bool:
    return bool(re.compile(r'^[\u4e00-\u9fff]+$').match(text))


def remove_chinese(text: str) -> str:
    return re.compile(r'[\u4e00-\u9fff]+').sub('', text)


def rreplace(s: str,
             old: str,
             new: str,
             count: int = 1) -> str:
    return new.join(s.rsplit(old, count))


def to_java_one(s: str) -> str:
    """
    将下划线命名转成驼峰命名
    例如 : user_id -> userId
    例如 : USER_ID -> userId
    例如 : gpsMaxMove_new -> gpsMaxMoveNew
    """
    if s is None or s == '':
        return ''
    r = ''.join(list(map(lambda x: (x[0].upper() + x[1:]) if len(x) > 1 else x[0].upper(), str(s).split('_'))))
    return r[0].lower() + r[1:]


def to_java(s: None | str | list[str] | tuple[str] | set[str]) -> None | str | list[str]:
    if s is None or s == '':
        return s
    if isinstance(s, list) or isinstance(s, tuple) or isinstance(s, set):
        return list(map(lambda x: to_java_one(x), s))
    return to_java_one(s)


def to_java_more(*args: Any) -> None | tuple:
    # 使用列表推导式进行过滤和映射
    r = [to_java(x) for x in args if x is not None]
    if not r:
        return None
    return tuple(r)


def to_underline_one(s: str) -> None | str:
    """
    将驼峰命名转成下划线命名
    例如: userId -> user_id
    """
    if not s:
        return s
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s])


def to_underline(s: None | str | list[str] | tuple[str] | set[str]) -> None | str | list[str]:
    if s == '' or s is None:
        return s
    if isinstance(s, list) or isinstance(s, tuple) or isinstance(s, set):
        return list(map(lambda x: to_underline_one(x), s))
    return to_underline_one(s)


def to_underline_more(*args: Any) -> None | tuple:
    # 使用列表推导式进行过滤和映射
    r = [to_underline(x) for x in args if x is not None]
    if not r:
        return None
    return tuple(r)


# 是否能用 json
def is_json_serializable(param: Any) -> bool:
    # 排除不能被 json 序列化的类型
    if isinstance(param, (bytes, complex, str, int, bool, float)):
        return False
    try:
        json.dumps(param)
        return True
    except (TypeError, OverflowError):
        return False


def is_json(myjson: Any) -> bool:
    """
    判断字符串是否是有效的JSON格式

    参数:
        myjson (str): 要检查的字符串

    返回:
        bool: 如果是有效JSON返回True，否则返回False
    """
    try:
        json.loads(myjson)
    except (ValueError, TypeError):
        return False
    return True


# 文件是否存在
def file_is_empty(file_name: str) -> bool:
    return file_name is None or file_name == '' or not os.path.exists(file_name)


# md5 算法
def do_md5(s: str) -> str:
    return hashlib.md5(s.encode(encoding='UTF-8')).hexdigest()


# sha256 算法
def do_sha256(s: str) -> str:
    h = hashlib.sha256()
    h.update(s.encode('utf-8'))
    return h.hexdigest()


# uuid 类型的随机数, 默认 32 位长度
def random_uuid(length: int = 32) -> str:
    r = uuid.uuid4().hex
    while len(r) < length:
        r += uuid.uuid4().hex
    return r[0:length]


def random_str(length: int = 64,
               start_str: int = 1,
               end_str: int = 32) -> str:
    """
    获得随机数
    length    ：随机数长度
    start_str ：随机数开始的字符的位置,从 1 开始, 包含start_str
    end_str   : 随机数结束的字符的位置, 不包含end_str
    默认的随机数是 : 数字+字母大小写
    """
    c_s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_'
    r = ''
    start_str = max(1, start_str)
    end_str = min(len(c_s), end_str)
    while len(r) < length:
        r += c_s[random.Random().randint(start_str, end_str) - 1]
    return r


# 字母的随机数, 默认小写
def random_letter(length: int = 10,
                  is_upper: bool = False) -> str:
    r = random_str(length=length, end_str=26)
    return r.upper() if is_upper else r


def random_int(length_or_start: int = 10,
               end: int = None) -> int:
    """
    数字的随机数, 返回 int
    也可以返回指定范围的随机数据
    """
    if end is None:
        return int(random_int_str(length=length_or_start))
    return random.Random().randint(int(length_or_start), int(end) - 1)


# 数字的随机数, 返回 str
def random_int_str(length: int = 10) -> str:
    return random_str(length=length, start_str=53, end_str=62)


def format_fixed_length_string(value: Any, target_length: int) -> str:
    """
    格式化字符串到指定长度，不足左补0，超出则保留右边字符。
    """
    value = str(value)
    if len(value) >= target_length:
        return value[-target_length:]
    return value.zfill(target_length)


# 去掉 str 中的 非数字字符, 然后, 再转化为 int
def to_int(s: Any = None) -> int:
    """
    去掉字符串中的非数字字符（保留小数点），并转为 int 类型。
    如果是 float 类型则转为 int（直接截断小数部分）。
    如果无法解析为数字，返回 0。
    """
    if s is None:
        return 0
    if isinstance(s, int):
        return s
    if isinstance(s, float):
        return int(s)
    s = str(s).strip()
    if not s:
        return 0
    negative = s.startswith('-')
    s_clean = re.sub(r'[^\d.]', '', s)
    if not s_clean or s_clean.count('.') > 1:
        return 0  # 防止非法格式如 "12.3.4"
    cleaned = f"-{s_clean}" if negative else s_clean
    try:
        # 支持带小数点的转 int（自动舍弃小数部分）
        return int(float(cleaned))
    except ValueError:
        return 0


def to_float(s: Any = None,
             precision: int = None) -> float:
    """
    将字符串中的非数字字符（除了小数点）去掉后转为 float。

    :param s: 输入值（可以是字符串或其他类型）
    :param precision: 小数部分保留的位数（多余部分直接截断）
    :return: 转换后的 float 值
    """
    if not s:
        return 0.0
    s = str(s).strip()
    if not s:
        return 0.0
    negative = s.startswith('-')
    # 提取所有数字和小数点
    s_clean = re.sub(r'[^\d.]', '', s)
    if not s_clean or s_clean.count('.') > 1:
        return 0.0  # 避免多个小数点造成 float 转换失败
    cleaned = f"-{s_clean}" if negative else s_clean
    try:
        value = float(cleaned)
    except ValueError:
        return 0.0
    if precision is not None:
        int_part, _, dec_part = cleaned.partition('.')
        dec_part = dec_part[:precision]
        cleaned = f"{int_part}.{dec_part}" if dec_part else int_part
        try:
            value = float(cleaned)
        except ValueError:
            return 0.0
    return value


def to_datetime(s: Any = None,
                pattern: str = None,
                r_str: bool = False) -> datetime | str:
    """
    @see https://www.runoob.com/python3/python3-date-time.html
    将字符串 s 转化成 datetime
    """
    if s is None or s == '':
        return str(datetime.today()) if r_str else datetime.today()
    s = str(s).replace('T', ' ').replace('Z', ' ').strip()
    r = None
    date_time_sdf = '%Y-%m-%d %H:%M:%S'
    m_s = {
        "^\\d{4}$": "%Y",
        "^\\d{6}$": "%Y%m",
        "^\\d{4}-\\d{1,2}$": "%Y-%m",
        "^\\d{8}$": "%Y%m%d",
        "^\\d{4}-\\d{1,2}-\\d{1,2}$": "%Y-%m-%d",
        "^\\d{8} {1}\\d{1,2}$": "%Y%m%d %H",
        "^\\d{4}-\\d{1,2}-\\d{1,2} {1}\\d{1,2}$": "%Y-%m-%d %H",
        "^\\d{8} {1}\\d{1,2}\\d{1,2}$": "%Y%m%d %H%M",
        "^\\d{4}-\\d{1,2}-\\d{1,2} {1}\\d{1,2}:\\d{1,2}$": "%Y-%m-%d %H:%M",
        "^\\d{8} {1}\\d{6}$": "%Y%m%d %H%M%S",
        "^\\d{4}-\\d{1,2}-\\d{1,2} {1}\\d{1,2}:\\d{1,2}:\\d{1,2}$": date_time_sdf,
        "^\\d{4}-\\d{1,2}-\\d{1,2} {1}\\d{1,2}:\\d{1,2}:\\d{1,2}.\\d{1,9}$": date_time_sdf,
        "^\\d{4}-\\d{1,2}-\\d{1,2}T{1}\\d{1,2}:\\d{1,2}:\\d{1,2}$": date_time_sdf,
        "^\\d{4}-\\d{1,2}-\\d{1,2}T{1}\\d{1,2}:\\d{1,2}:\\d{1,2}.\\d{1,9}$": date_time_sdf,
    }
    if pattern is not None:
        st = s.split('.')[0]
        st = st.replace('T', ' ')
        r = datetime.strptime(st, pattern)
    else:
        for m in m_s:
            if re.match(m, s):
                st = s.split('.')[0]
                st = st.replace('T', ' ')
                r = datetime.strptime(st, m_s[m])
    if r is None and re.match("^\\d{1,13}$", s):
        s_int = int(s)
        if len(s) > 10:
            s_int = int(s_int / 1000)
        time_arr = time.localtime(s_int)
        time_str = time.strftime(date_time_sdf, time_arr)
        r = datetime.strptime(time_str, date_time_sdf)
    if r is None:
        r = datetime.today()
    return str(r) if r_str else r


# 将字符串 s 转化成 datetime, 然后再次转化成 str
def to_datetime_str(s: Any = None) -> datetime | str:
    return to_datetime(s, r_str=True)


# 时间加减
def to_datetime_add(s: Any = None,
                    days: int = 0,
                    seconds: int = 0,
                    microseconds: int = 0,
                    milliseconds: int = 0,
                    minutes: int = 0,
                    hours: int = 0,
                    weeks: int = 0) -> datetime:
    return to_datetime(s) + timedelta(days=days, seconds=seconds, microseconds=microseconds,
                                      milliseconds=milliseconds, minutes=minutes, hours=hours,
                                      weeks=weeks)


# 将字符串 s 转化成 date 例如: 2021-02-03
def to_date(s: Any = None) -> str:
    return str(to_datetime(s))[0:10]


# 将字符串 s 转化成 date 例如: 20210203
def to_date_number(s: Any = None) -> str:
    return str(to_datetime(s))[0:10].replace('-', '')


def get_timestamp(s: Any = None) -> int:
    """获取 Unix 秒级时间戳"""
    return int(to_datetime(s).timestamp())


def get_timestamp_ms(s: Any = None) -> int:
    """获取 Unix 毫秒级时间戳"""
    return int(to_datetime(s).timestamp() * 1000)


# 时间加减
def to_date_add(s: Any = None,
                days: int = 0,
                seconds: int = 0,
                microseconds: int = 0,
                milliseconds: int = 0,
                minutes: int = 0,
                hours: int = 0,
                weeks: int = 0) -> str:
    return str(to_datetime_add(s=s, days=days, seconds=seconds, microseconds=microseconds,
                               milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks))[0:10]


# 转化成字符串
def to_str(param: Any = None) -> str:
    return json.dumps(param, ensure_ascii=False) if is_json_serializable(param) else str(param)


def match_str(pattern: str,
              str_a: str = '') -> str | None:
    """
    匹配字符串
    可以参考 正则表达式的操作, 可以使用 chatgpt 帮忙写出这段代码
    @see https://www.runoob.com/python3/python3-reg-expressions.html
    # 示例用法
    # 输出：t_admin
    print(match_str(r'create TABLE (\\w+)', 'CREATE TABLE t_admin (id bigint(20) NOT NULL'))
    这里的 斜杠w 去掉一个斜杠
    """
    match = re.search(pattern, str_a, re.I)
    if match:
        return match.group(1)
    else:
        return None


def format_sorted_kv_string(data_obj: Any,
                            sep: str = '&',
                            join: str = '=',
                            join_list: str = ',') -> str:
    """
    将 dict/json-like 对象按 key 排序后格式化为字符串。
    格式为 key1=value1&key2=value2，支持嵌套结构和列表拼接。

    :param data_obj: 任意结构的数据，如 dict、list、基础类型
    :param sep: 键值对之间的分隔符，默认 '&'
    :param join: key 与 value 的连接符，默认 '='
    :param join_list: 列表等多值类型的连接符，默认 ','
    :return: 格式化后的字符串
    """
    if isinstance(data_obj, (list, tuple, set)):
        return join_list.join(map(str, data_obj))

    if not isinstance(data_obj, dict):
        return str(data_obj)

    # 对 dict 按 key 排序
    sorted_items = sorted(data_obj.items(), key=lambda x: x[0])
    result = []

    for key, value in sorted_items:
        if is_json_serializable(value):
            value_str = format_sorted_kv_string(value, sep=sep, join=join, join_list=join_list)
        else:
            value_str = str(value)
        result.append(f"{key}{join}{value_str}")

    return sep.join(result)


# 将数据写入到 config 中
def set_config_data(file_name: str = 'config',
                    param: dict[str, Any] = None) -> None:
    set_data_in_user_home(file_name, {} if param is None else param)


# 从 config 中获得 配置数据
def get_config_data(file_name: str = 'config') -> dict[str, Any]:
    # print('get_config_data', file_name)
    config_data = get_data_from_user_home(file_name)
    # print('get_data_from_user_home', config_data)
    if not config_data:
        config_data = get_data_from_path(file_name)
    # print('get_data_from_path', config_data)
    return config_data


# 在当前用户的主目录中, 获得指定文件的数据
def get_data_from_user_home(file_name: str = 'config') -> dict[str, Any]:
    return get_data_from_path(file_name, os.path.expanduser("~"))


# 将 data 数据,在当前用户的主目录中, 获得指定文件的数据
def set_data_in_user_home(file_name: str = 'config',
                          param: dict[str, Any] = None) -> None:
    set_data_in_path(file_name, {} if param is None else param, os.path.expanduser("~"))


# 在当前的目录中, 获得指定文件的数据
def get_data_from_path(file_name: str = 'config',
                       file_path: str = None) -> dict[str, Any]:
    param = get_data_from_path_detail(file_name, file_path, __CONFIG_PATH)
    return param if param else get_data_from_path_detail(file_name, file_path, __CONFIG_PATH_BAK)


def get_data_from_path_detail(file_name: str = 'config',
                              file_path: str = None,
                              path_name: str = __CONFIG_PATH) -> dict[str, Any]:
    config_path = file_path + '/' + path_name if file_path else path_name
    # print('config_path_1', config_path)
    if not os.path.exists(config_path):
        # print('config_path_2', config_path)
        return {}
    file_path = config_path + '/' + file_name + '.json'
    # print('config_path_3', file_path)
    if not os.path.exists(file_path):
        return {}
    # print('to_json_from_file', file_path)
    return to_json_from_file(file_path)


# 在当前的目录中, 设置数据到指定路径下
def set_data_in_path(file_name: str = 'config',
                     param: str = None,
                     file_path: str = '') -> None:
    config_path = file_path + '/' + __CONFIG_PATH
    if not os.path.exists(config_path):
        os.mkdir(config_path)
    file_path = config_path + '/' + file_name + '.json'
    text_file = open(file_path, 'w', encoding='utf-8')
    text_file.write(to_str({} if param is None else param))
    text_file.close()


# 执行命令
def exec_command(command: str = None) -> None:
    if command is None:
        return
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"command executed error: {e}")


# 找到最新的 html 文件
def get_latest_file(
        file_path: str = None,
        path_prefix: str = None,
        prefix: str = None,
        path_contain: str = None,
        contain: str = None,
        path_suffix: str = None,
        suffix: str = None,
        full_path: bool = None) -> None | tuple[str, str] | str:
    """
    full_path: 是否返回完整的路径
    """
    html_list = get_file(file_path=file_path,
                         path_prefix=path_prefix,
                         prefix=prefix,
                         path_contain=path_contain,
                         contain=contain,
                         path_suffix=path_suffix,
                         suffix=suffix)
    html_list.sort(reverse=True)
    r1 = html_list[0] if len(html_list) > 0 else None
    if r1 is None:
        return None
    r1_short = r1
    for sep in ['\\', '/']:
        if sep in r1:
            r1_short = r1.split(sep)[-1]
            break
    if full_path is None:
        return r1_short, r1
    return r1 if full_path else r1_short


# 是否是 windows 系统
def is_win() -> bool:
    return platform.system().lower() == 'windows'


# 是否是 linux 系统, 不是 windows , 就是 linux 系统
def is_linux() -> bool:
    return not is_win()


def to_print(*args,
             time_prefix: bool = False,
             line_with_space_count: int = None,
             interval: int = None) -> str:
    """
    记录日志, 如果是对象会转化为 json
    数据直接 print, 不记录到文件
    例如: aaa
    interval: 间隔一段时间，打印一下, 单位: 秒，不要频繁打印
    time_prefix : 是否在前面加时间, 默认 False
    """
    d = ' '.join(map(lambda x: json.dumps(x) if is_json_serializable(x) else str(x), args))
    d = d.strip()
    lo = datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ' ' + d if time_prefix is True else d
    if lo is None or str(lo) == '':
        lo = to_datetime(r_str=True)
    prefix_space = ' ' * (line_with_space_count or 0)
    if interval is None or get_timestamp() - get_thread_local_index_data().get('to_print_time', 0) >= interval:
        get_thread_local_index_data()['to_print_time'] = get_timestamp()
        s = ''
        if interval is not None:
            s = str(to_datetime()) + ' '
        print(prefix_space + s + str(lo))
    return prefix_space + lo


def to_log(*args,
           time_prefix: bool = False,
           line_with_space_count: int = None,
           interval: int = None) -> str:
    """
    记录日志, 如果是对象会转化为 json
    前面加了时间
    例如: 2024-11-07 10:23:47 aaa
    """
    return to_print(*args,
                    time_prefix=time_prefix if time_prefix is not None else True,
                    line_with_space_count=line_with_space_count,
                    interval=interval)


def get_and_save_data_to_thread(file_path: str = None,
                                file_name: str = None,
                                file_name_prefix: str = None,
                                file_name_suffix: str = None,
                                interval: int = None,
                                line_with_space_count: int = None,
                                mode: str = 'a',
                                file_name_with_date: bool = False,
                                fun_name: callable = None) -> list:
    """
    将一些参数写入到 thread local 中, 方便后续使用
    """
    # 使用线程本地存储来存储文件路径和文件名称
    if file_name_with_date:
        file_name = get_file_name(file_name=file_path if file_name is None else file_name, is_date=True, suffix='')
    get_thread_local_index_data()['_use_fun_flag'] = True if mode != 'a' else get_thread_local_index_data().get('_use_fun_flag', False)
    fun_name_str = fun_name.__name__
    # 存储函数引用
    get_thread_local_index_data()['_use_fun'] = fun_name
    r_list = []
    # 输出非空字段
    for key, value in {
        'file_path': file_path,
        'file_name': file_name,
        'file_name_prefix': file_name_prefix,
        'file_name_suffix': file_name_suffix,
        'interval': interval,
        'line_with_space_count': line_with_space_count,
    }.items():
        this_key = f'{fun_name_str}__{key}'
        value_temp = value if value is not None else get_thread_local_index_data().get(this_key, None)
        get_thread_local_index_data()[this_key] = value_temp
        r_list.append(value_temp)
    return r_list


def to_print_file(*args,
                  file_path: str = None,
                  file_name: str = None,
                  file_name_with_date: bool = False,
                  file_name_prefix: str = None,
                  file_name_suffix: str = None,
                  line_with_space_count: int = None,
                  mode: str = 'a',
                  interval: int = None) -> str:
    """
    将 print 数据, 写入到 print_file 文件
    文件按照 日期自动创建
    例如: print_file/2020-01-01.txt
    to_print_file(query_string, mode='w', file_path=file_path, file_name=get_file_name(file_name=file_path, is_date=True))
    """
    [file_path, file_name, file_name_prefix, file_name_suffix, interval, line_with_space_count] = get_and_save_data_to_thread(
        file_path=file_path,
        file_name=file_name,
        file_name_prefix=file_name_prefix,
        file_name_suffix=file_name_suffix,
        interval=interval,
        mode=mode,
        file_name_with_date=file_name_with_date,
        line_with_space_count=line_with_space_count,
        fun_name=to_print_file
    )
    return to_txt(data_param=[to_print(*args, line_with_space_count=line_with_space_count, interval=interval)],
                  file_name=('' if file_name_prefix is None else file_name_prefix)
                            + (datetime.today().strftime('%Y-%m-%d') if file_name is None else file_name)
                            + ('' if file_name_suffix is None else file_name_suffix),
                  file_path=str(file_path if file_path is not None else 'to_print_file'),
                  mode=mode,
                  fixed_name=True,
                  suffix='.txt')


def to_print_txt(*args,
                 file_path: str = None,
                 file_name_with_date: bool = False,
                 file_name: str = None,
                 file_name_prefix: str = None,
                 file_name_suffix: str = None,
                 line_with_space_count: int = None,
                 mode: str = 'a',
                 interval: int = None) -> str:
    """
    将 print 数据, 写入到 print_txt 文件
    文件按照 日期自动创建
    例如: print_txt/2020-01-01.txt
    """
    [file_path, file_name, file_name_prefix, file_name_suffix, interval, line_with_space_count] = get_and_save_data_to_thread(
        file_path=file_path,
        file_name=file_name,
        file_name_prefix=file_name_prefix,
        file_name_suffix=file_name_suffix,
        interval=interval,
        mode=mode,
        file_name_with_date=file_name_with_date,
        line_with_space_count=line_with_space_count,
        fun_name=to_print_txt
    )
    return to_txt(data_param=[to_print(*args, line_with_space_count=line_with_space_count, interval=interval)],
                  file_name=('' if file_name_prefix is None else file_name_prefix)
                            + (datetime.today().strftime('%Y-%m-%d') if file_name is None else file_name)
                            + ('' if file_name_suffix is None else file_name_suffix),
                  file_path=str(file_path if file_path is not None else 'to_print_txt'),
                  mode=mode,
                  fixed_name=True,
                  suffix='.txt')


def to_log_file(*args,
                file_path: str = None,
                file_name_with_date: bool = False,
                file_name: str = None,
                file_name_prefix: str = None,
                file_name_suffix: str = None,
                line_with_space_count: int = None,
                time_prefix: bool = True,
                mode: str = 'a',
                interval: int = None) -> None:
    """
    将 log 数据, 写入到 log_file 文件
    文件按照 日期自动创建
    例如: log_file/2020-01-01.log
    """
    [file_path, file_name, file_name_prefix, file_name_suffix, interval, line_with_space_count] = get_and_save_data_to_thread(
        file_path=file_path,
        file_name=file_name,
        file_name_prefix=file_name_prefix,
        file_name_suffix=file_name_suffix,
        interval=interval,
        mode=mode,
        file_name_with_date=file_name_with_date,
        line_with_space_count=line_with_space_count,
        fun_name=to_log_file
    )
    to_txt(data_param=[to_log(*args, time_prefix=time_prefix, line_with_space_count=line_with_space_count, interval=interval)],
           file_name=('' if file_name_prefix is None else file_name_prefix)
                     + (datetime.today().strftime('%Y-%m-%d') if file_name is None else file_name)
                     + ('' if file_name_suffix is None else file_name_suffix),
           file_path=str(file_path if file_path is not None else 'to_log_file'),
           fixed_name=True,
           mode=mode,
           suffix='.log')


def to_log_txt(*args,
               file_path: str = None,
               file_name_with_date: bool = False,
               file_name: str = None,
               file_name_prefix: str = None,
               file_name_suffix: str = None,
               line_with_space_count: int = None,
               time_prefix: bool = True,
               mode: str = 'a',
               interval: int = None) -> None:
    """
    将 log 数据, 写入到 log_txt 文件夹中
    文件按照 日期自动创建
    例如: log_txt/2020-01-01.txt
    """
    [file_path, file_name, file_name_prefix, file_name_suffix, interval, line_with_space_count] = get_and_save_data_to_thread(
        file_path=file_path,
        file_name=file_name,
        file_name_prefix=file_name_prefix,
        file_name_suffix=file_name_suffix,
        interval=interval,
        mode=mode,
        file_name_with_date=file_name_with_date,
        line_with_space_count=line_with_space_count,
        fun_name=to_log_txt
    )
    to_txt(data_param=[to_log(*args, time_prefix=time_prefix, line_with_space_count=line_with_space_count, interval=interval)],
           file_name=('' if file_name_prefix is None else file_name_prefix)
                     + (datetime.today().strftime('%Y-%m-%d') if file_name is None else file_name)
                     + ('' if file_name_suffix is None else file_name_suffix),
           file_path=str(file_path if file_path is not None else 'to_log_txt'),
           mode=mode,
           fixed_name=True,
           suffix='.txt')


def check_file(file_name: str = None) -> None:
    r"""
    检查文件夹是否存在,不存在,就创建新的
    支持多级目录 , 例如: C:\Users\yangpu\Desktop\study\a\b\c\d\e\f
    """
    if file_name is None or file_name == '':
        return
    for sep in ['\\', '/']:
        f_n = file_name.split(sep)
        for i in range(1, len(f_n) + 1):
            # C:\Users\yangpu\Desktop\study\p.t
            p_n = sep.join(f_n[0:i])
            if not os.path.exists(p_n):
                os.mkdir(p_n)


def get_file_name(file_name: str = None,
                  suffix: str = '.txt',
                  is_date: bool = False) -> str:
    """
    获得文件名称
    按照  name_天小时分钟_秒毫秒随机数 的规则来生成
    """
    # %Y-%m-%d %H:%M:%S
    [year, month, day, hour, minute, second, ss] = datetime.today().strftime('%Y_%m_%d_%H_%M_%S_%f').split('_')
    s = year + month + day + hour + minute if is_date else month + day + hour + minute
    # 在 file_name 中, 检查是否有后缀
    if '.' in file_name:
        suffix = '.' + file_name.split('.')[-1]
        file_name = file_name[0:file_name.rfind('.')]
    # return str(file_name) + '_' + s + '_' + second + '-' + random_int_str(length=2) + suffix
    # 202506161803_4112
    return str(file_name) + '_' + s + '_' + second + random_int_str(length=2) + suffix


def to_txt(data_param: Any,
           file_name: str = 'txt',
           file_path: str = 'txt',
           fixed_name: bool = False,
           mode: str = 'a',
           suffix: str = '.txt',
           sep_list: str = '\t',
           file_name_is_date: bool = False) -> str:
    r"""
    将 list 中的数据以 json 或者基本类型的形式写入到文件中
    data_param   : 数组数据, 也可以不是数组
    file_name   : 文件名 , 默认 txt
                  当文件名是 C:\Users\yangpu\Desktop\study\abc\d\e\f\a.sql 这种类型的时候, 可以直接创建文件夹,
                      会赋值 file_name=a,
                            file_path=C:\Users\yangpu\Desktop\study\abc\d\e\f,
                            fixed_name=True,
                            suffix=.sql
                  当文件名是 abc 的时候, 按照正常值,计算
    file_path   : 文件路径
    fixed_name  : 是否固定文件名
    suffix      : 文件后缀, 默认 .txt
    sep_list    : 当 data_param 是 list(list) 类型的时候 使用 sep_list 作为分割内部的分隔符,
                  默认使用 \t 作为分隔符, 如果为 None , 则按照 json 去处理这个 list
    """
    file_name = str(file_name)
    for sep in ['\\', '/']:
        f_n = file_name.split(sep)
        if len(f_n) > 1:
            file_name = f_n[-1]
            file_path = sep.join(f_n[0:-1])
            if '.' in file_name:
                suffix = '.' + file_name.split('.')[-1]
                file_name = file_name[0:file_name.rfind('.')]
                fixed_name = True

    # 检查路径 file_path
    while file_path.endswith('/'):
        file_path = file_path[0:-1]
    check_file(file_path)

    # 在 file_name 中, 检查是否有后缀
    if '.' in file_name:
        suffix = '.' + file_name.split('.')[-1]
        file_name = file_name[0:file_name.rfind('.')]

    # 生成 file_name
    if fixed_name:
        file_name = file_name + suffix
    else:
        file_name = get_file_name(file_name, suffix, is_date=file_name_is_date)
    # 文件路径
    file_name_path = file_name
    if file_path != '':
        file_name_path = file_path + '/' + file_name
    # 写入文件
    text_file = open(file_name_path, mode, encoding='utf-8')
    if isinstance(data_param, set):
        data_param = list(data_param)
    if not isinstance(data_param, list):
        text_file.write(to_str(data_param) + '\n')
    else:
        for one in data_param:
            if isinstance(one, (list, tuple, set)) and sep_list is not None:
                text_file.write(str(sep_list).join(list(map(lambda x: to_str(x), one))) + '\n')
            else:
                text_file.write(to_str(one) + '\n')
    text_file.close()
    return file_name_path


# 将 list 中的数据写入到固定的文件中,自己设置文件后缀
def to_txt_file(data_param: Any,
                file_name: str = None,
                mode: str = 'a') -> str:
    file_name = get_file_name('to_txt_file', is_date=True) if file_name is None else file_name
    suffix = '.txt'
    f = file_name
    for sep in ['\\', '/']:
        f_n = file_name.split(sep)
        if len(f_n) > 1:
            f = file_name
    if '.' in f:
        suffix = '.' + f.split('.')[-1]
        file_name = file_name.replace(suffix, '')
    return to_txt(data_param=data_param,
                  file_name=file_name,
                  file_path='to_txt_file',
                  suffix=suffix,
                  fixed_name=True,
                  mode=mode)


# 将 list 中的数据写入到固定的文件中,自己设置文件后缀
def to_file(data_param: Any,
            file_name: str = None,
            mode: str = 'a') -> str:
    file_name = get_file_name('to_file', is_date=True) if file_name is None else file_name
    suffix = '.txt'
    f = file_name
    for sep in ['\\', '/']:
        f_n = file_name.split(sep)
        if len(f_n) > 1:
            f = file_name
    if '.' in f:
        suffix = '.' + f.split('.')[-1]
        file_name = file_name.replace(suffix, '')
    return to_txt(data_param=data_param,
                  file_name=file_name,
                  file_path='file',
                  suffix=suffix,
                  fixed_name=True,
                  mode=mode)


def to_list(file_name: str = 'a.txt',
            sep: str = None,
            sep_line: str = None,
            sep_line_contain: str = None,
            sep_line_prefix: str = None,
            sep_line_suffix: str = None,
            sep_all: str = None,
            ignore_start_with: list[str] | set[str] | str = None,
            ignore_end_with: list[str] | set[str] | str | None = None,
            start_index: int = None,
            start_line: str = None,
            end_index: int = None,
            end_line: str = None,
            count: int = None,
            sheet_index: int = 1,
            column_index: list[str] | set[str] | str | None = None,
            column_date: list[str] | set[str] | str | None = None,
            column_datetime: list[str] | set[str] | str | None = None) -> list:
    """
    当读取 txt 之类的文件的时候
    将 txt 文件读取到 list 中, 每一行自动过滤掉行前行后的特殊字符
    sep             : 是否对每一行进行分割,如果存在这个字段,就分割
    sep_all         : 将文件转化成一个字符串,然后对这个字符串,再次总体分割
    start_index     : 从这个地方开始读取,从1开始标号 , 包含这一行
    start_line      : 从这个地方开始读取,从第一行开始找到这个字符串开始标记 , 包含这一行
    end_index       : 读取到这个地方结束,从1开始标号 , 不包含这一行
    end_line        : 读取到这个地方结束,从第一行开始找到这个字符串开始标记 , 不包含这一行
    count           : 读取指定的行数
    ##############################################
    当读取 excel 之类的文件的时候
    将 excel 文件读取到 list 中, 可以指定 sheet, 也可以指定列 column_index(列) ,自动过滤掉每个单元格前后的特殊字符
    sheet           : 从 1 开始编号,
    column_index    : 从 1 开始编号, 指定列
    column_index    : 如果是指定值, 这个时候返回的是一个 list, 没有嵌套 list
    column_index    : 如果是 '1,2,3,4'   [1,2,3,4], 返回的是一个嵌套 list[list]
    column_date     : 指定日期格式的列,规则与 column_index 一样
    column_datetime : 指定日期格式的列,规则与 column_index 一样
    返回的数据一定是一个 list
    """
    if file_name.endswith('.xls') or file_name.endswith('.xlsx'):
        return to_list_from_excel(file_name=file_name,
                                  sheet_index=sheet_index,
                                  column_index=column_index,
                                  column_date=column_date,
                                  column_datetime=column_datetime)
    return to_list_from_txt(file_name=file_name,
                            sep=sep,
                            sep_line=sep_line,
                            sep_line_contain=sep_line_contain,
                            sep_line_prefix=sep_line_prefix,
                            sep_line_suffix=sep_line_suffix,
                            sep_all=sep_all,
                            ignore_start_with=ignore_start_with,
                            ignore_end_with=ignore_end_with,
                            start_index=start_index,
                            start_line=start_line,
                            end_index=end_index,
                            end_line=end_line,
                            count=count)


def to_list_from_excel(file_name: str = 'a.xls',
                       sheet_index: int = 1,
                       column_index: list | int | str | None = None,
                       column_date: list | int | str | None = None,
                       column_datetime: list | int | str | None = None) -> list:
    """
    当读取 excel 之类的文件的时候
    将 excel 文件读取到 list 中, 可以指定 sheet, 也可以指定列 column_index(列) ,自动过滤掉每个单元格前后的特殊字符
    sheet_index     : 从 1 开始编号,
    column_index    : 从 1 开始编号, 指定列, 如果是指定值是一个, 这个时候返回的是一个 list, 没有嵌套 list
                       如果是 '1,2,3,4'   [1,2,3,4], 返回的是一个嵌套 list[list]
    column_date     : 指定日期格式的列,规则与 column_index 一样
    column_datetime : 指定日期格式的列,规则与 column_index 一样
    """
    if file_is_empty(file_name):
        return []
    data_list = list()
    # excel 表格解析成 list 数据
    list_index = []
    for one_index in [column_index, column_date, column_datetime]:
        list_index_one = None
        if one_index is not None:
            list_index_one = []
            if isinstance(one_index, int):
                list_index_one.append(one_index)
            if isinstance(one_index, str):
                i_list = one_index.split(',')
                for i in i_list:
                    list_index_one.append(int(i))
            if isinstance(one_index, list):
                for i in one_index:
                    list_index_one.append(int(i))
        list_index.append(list_index_one)
    list_all = []
    for one_list in list_index:
        if one_list is not None:
            for o in one_list:
                list_all.append(o)
    if len(list_all) > 0 and list_index[0] is not None:
        list_index[0] = list_all
    # 是否是单 list 类型的数据
    list_only_one = False
    if list_index[0] is not None and len(list_index[0]) == 1:
        list_only_one = True
    # 是 xls 格式
    if file_name.endswith('.xls'):
        book = xlrd.open_workbook(file_name)  # 打开一个excel
        sheet = book.sheet_by_index(sheet_index - 1)  # 根据顺序获取sheet
        for i in range(sheet.nrows):  # 0 1 2 3 4 5
            rows = sheet.row_values(i)
            row_data = []
            for j in range(len(rows)):
                cell_data = str(rows[j]).strip()
                is_date = False
                is_datetime = False
                # 日期格式的列
                if list_index[1] is not None and j + 1 in list_index[1]:
                    cell_data = to_date(xlrd.xldate_as_datetime(to_int(rows[j]), 0))
                    is_date = True
                    row_data.append(cell_data)
                    if list_only_one:
                        row_data = cell_data
                # 日期时间格式的列
                if not is_date and list_index[2] is not None and j + 1 in list_index[2]:
                    cell_data = to_datetime(xlrd.xldate_as_datetime(to_int(rows[j]), 0))
                    is_datetime = True
                    row_data.append(cell_data)
                    if list_only_one:
                        row_data = cell_data
                # 指定需要的列
                if not is_date and not is_datetime:
                    if list_index[0] is None:
                        row_data.append(cell_data)
                    else:
                        # 指定需要的列
                        if j + 1 in list_index[0]:
                            row_data.append(cell_data)
                            if list_only_one:
                                row_data = cell_data
            data_list.append(row_data)
    # 是 xlsx 格式
    if file_name.endswith('.xlsx'):
        wb = openpyxl.load_workbook(filename=file_name, read_only=True)
        ws = wb[wb.sheetnames[sheet_index - 1]]
        for rows in ws.rows:
            row_data = []
            for j in range(len(rows)):
                cell_data = str(rows[j].value).strip()
                is_date = False
                is_datetime = False
                # 日期格式的列
                if list_index[1] is not None and j + 1 in list_index[1]:
                    cell_data = to_date(cell_data)
                    is_date = True
                    row_data.append(cell_data)
                    if list_only_one:
                        row_data = cell_data
                # 日期时间格式的列
                if not is_date and list_index[2] is not None and j + 1 in list_index[2]:
                    cell_data = to_datetime(cell_data)
                    is_datetime = True
                    row_data.append(cell_data)
                    if list_only_one:
                        row_data = cell_data
                # 指定需要的列
                if not is_date and not is_datetime:
                    if list_index[0] is None:
                        row_data.append(cell_data)
                    else:
                        # 指定需要的列
                        if j + 1 in list_index[0]:
                            row_data.append(cell_data)
                            if list_only_one:
                                row_data = cell_data
            data_list.append(row_data)
    return data_list


def to_list_from_txt_with_blank_line(file_name: str = 'a.txt') -> list:
    """
    将一个文件中以空行作为分隔符,
    组成一个 list(list) 数据
    多行空行,自动合并到一行空行
    """
    return to_list_from_txt(file_name, sep_line='')


def to_list_list(data_list: list = None,
                 count: int = 10) -> list:
    """
    将 list 切分成 list(list)
    组成一个 list(list) 数据
    多行空行,自动合并到一行空行
    """
    if data_list is None:
        data_list = []
    r_list = []
    o_list = []
    c = 0
    for i in range(len(data_list)):
        o_list.append(data_list[i])
        c += 1
        if c == count:
            r_list.append(o_list)
            o_list = []
            c = 0
    if len(o_list):
        r_list.append(o_list)
    return r_list


def to_list_json_from_txt(file_name: str = 'a.txt',
                          start_index: int = None,
                          start_line: str = None,
                          start_line_exclude: str | list[str] | set[str] = None,
                          end_index: int = None,
                          end_line: str = None,
                          end_line_exclude: str | list[str] | set[str] = None,
                          count: int = None) -> list:
    """
    将一个文件中的数据按照行来区分,
    会自动过滤掉空格行,
    组成一个 list[json] 数据
    可以将以下文本转 list[json]
    {"accessKey":"1","signature":"4","timestamp":"1747639787"}
    {"accessKey":"2","signature":"5","timestamp":"1747639787"}
    {"accessKey":"3","signature":"6","timestamp":"1747639787"}
    """
    return to_list_from_txt(file_name,
                            start_index=start_index,
                            start_line=start_line,
                            start_line_exclude=start_line_exclude,
                            end_index=end_index,
                            end_line=end_line,
                            end_line_exclude=end_line_exclude,
                            count=count,
                            line_json=True)


# 将多个文件 读取成 list
def to_list_from_txt_list(file_list: list[Any] = None) -> list:
    if file_list is None:
        file_list = []
    data_list = []
    for a in file_list:
        data_list.extend(to_list_from_txt(file_name=a))
    return data_list


def to_list_from_txt(file_name: str = 'a.txt',
                     sep: str = None,
                     sep_line: str = None,
                     sep_line_contain: str = None,
                     sep_line_prefix: str = None,
                     sep_line_suffix: str = None,
                     sep_line_with_space_count: int = None,
                     sep_is_front: bool = True,
                     sep_all: str = None,
                     ignore_start_with: list | int | str | None = None,
                     ignore_end_with: list | int | str | None = None,
                     line_join: str = None,
                     line_json: bool = None,
                     start_index: int = None,
                     start_line: str = None,
                     start_line_exclude: str | list[str] | set[str] = None,
                     end_index: int = None,
                     end_line: str = None,
                     end_line_exclude: str | list[str] | set[str] = None,
                     count: int = None) -> list:
    """
    将 txt 文件转化成 list 的方法
    当读取 txt 之类的文件的时候
    将 txt 文件读取到 list 中, 每一行自动过滤掉行前行后的特殊字符
    sep                        : 对每一行进行分割,将 list(str) 转化为 list(list(str)), 或者将 list(list(str)) 转化为 list(list(list(str)))
    sep_line                   : 这一行是一个分隔符, 分隔符与这行一样, 将 list(str) 转化为 list(list(str))
    sep_line_with_space_count  : 分隔符是空格的个数, 将 list(str) 转化为 list(list(str))
    sep_line_contain           : 这一行是一个分隔符,包含这个行分隔符的做分割, 将 list(str) 转化为 list(list(str))
    sep_line_prefix            : 这一行是一个分隔符,以这个分隔符作为前缀的, 将 list(str) 转化为 list(list(str))
    sep_line_suffix            : 这一行是一个分隔符,以这个分隔符作为后缀的, 将 list(str) 转化为 list(list(str))
    sep_is_front               : 这一行，分割行，是包含到前面，还是包含到
    sep_all                    : 将文件转化成一个字符串,然后对这个字符串,再次总体分割 将 list(str) 转化为 str , 然后再次转化成 list(str)
    ignore_start_with          : 忽略以这个为开头的行
    ignore_end_with            : 忽略以这个为结尾的行
    line_join                  : 将 list(list(str)) 转化成 list(str) 类型的数据
    line_json                  : 将 list(str) 转化成 list(json) 类型的数据, 会自动过滤掉空格行
    start_index                : 从这个地方开始读取,从1开始标号 , 包含这一行
    start_line                 : 从这个地方开始读取,从第一行开始找到这个字符串开始标记 , 包含这一行
    start_line_exclude         : 从这个地方开始读取,从第一行开始找到这个字符串开始标记 , 不包含这一行, 返回的是一个 list(' '.join(one_line_list))
    end_index                  : 读取到这个地方结束,从1开始标号 , 不包含这一行
    end_line                   : 读取到这个地方结束,从第一行开始找到这个字符串开始标记 , 不包含这一行
    end_line_exclude           : 读取到这个地方结束,从第一行开始找到这个字符串开始标记 , 不包含这一行, 返回的是一个 list(' '.join(one_line_list))
    count                      : 读取指定的行数
    """
    if file_is_empty(file_name=file_name):
        return []
    data_list = []
    # 普通文件的解析
    d_list = open(file_name, 'r', encoding='utf-8').readlines()
    # 数量
    c = 0
    start_flag = None
    end_flag = None
    if start_line is not None:
        start_flag = False
    if end_line is not None:
        end_flag = False
    for i in range(len(d_list)):
        line = d_list[i].strip()
        # 判断开始位置
        if start_index is not None and i + 1 < to_int(start_index):
            continue
        # 判断结束位置
        if end_index is not None and i + 1 >= to_int(end_index):
            continue
        # 判断数量
        if count is not None and c >= to_int(count):
            continue
        # 开始标记位
        if start_flag is not None and not start_flag and line.find(start_line) > -1:
            # 如果有标记位置,就是 True
            start_flag = True
        # 开始标记位
        if end_flag is not None and not end_flag and line.find(end_line) > -1:
            # 如果有标记位置,就是 True
            end_flag = True
        if start_flag is not None and not start_flag:
            # 有开始标记位参数,并且,还没有走到开始标记位
            continue
        elif end_flag is not None and end_flag:
            # 有结束标记位参数,并且,已经走到了结束标记位
            continue
        c += 1
        can_add = True
        if ignore_start_with is not None:
            if isinstance(ignore_start_with, list) or isinstance(ignore_start_with, set):
                for ss in ignore_start_with:
                    if line.startswith(str(ss)):
                        can_add = False
            elif isinstance(ignore_start_with, str):
                if line.startswith(str(ignore_start_with)):
                    can_add = False
        if ignore_end_with is not None:
            if isinstance(ignore_end_with, list) or isinstance(ignore_end_with, set):
                for ss in ignore_end_with:
                    if line.endswith(str(ss)):
                        can_add = False
            elif isinstance(ignore_end_with, str):
                if line.endswith(str(ignore_end_with)):
                    can_add = False
        if can_add:
            data_list.append(line)

    # 更复杂的切分, 中间的部分 会转成 ' '.join(one_line_list)
    if start_line_exclude is not None and end_line_exclude is not None:
        data_list1 = data_list
        start_flag = False
        start_flag_once = False
        end_flag = False
        one_data_list = []
        data_list = []
        for i in range(len(data_list1)):
            line = data_list1[i].strip()
            # 开始标记位
            if not start_flag:
                if isinstance(start_line_exclude, list) or isinstance(start_line_exclude, set):
                    for ss in start_line_exclude:
                        if line.find(str(ss)) > -1:
                            # 如果有标记位置,就是 True
                            start_flag = True
                            start_flag_once = True
                else:
                    if line.find(str(start_line_exclude)) > -1:
                        # 如果有标记位置,就是 True
                        start_flag = True
                        start_flag_once = True
            # 结束标记位
            if not end_flag:
                if isinstance(end_line_exclude, list) or isinstance(end_line_exclude, set):
                    for ss in end_line_exclude:
                        if line.find(str(ss)) > -1:
                            # 如果有标记位置,就是 True
                            end_flag = True
                else:
                    if line.find(str(end_line_exclude)) > -1:
                        # 如果有标记位置,就是 True
                        end_flag = True
            if not start_flag:
                # 有开始标记位参数,并且,还没有走到开始标记位
                continue
            elif end_flag:
                # 有结束标记位参数,并且,已经走到了结束标记位
                start_flag = False
                end_flag = False
                start_flag_once = False
                # print(one_data_list)
                data_list.append(' '.join(one_data_list).strip())
                one_data_list = []
                continue
            # 去掉 start_line_exclude 包含行
            if start_flag_once:
                start_flag_once = False
                line = ''
            if start_flag and not end_flag:
                one_data_list.append(line)
        if len(one_data_list):
            data_list.append(' '.join(one_data_list).strip())

    if sep_all is not None:
        # 全部划分, 重新分割成 list(str)
        data_list = ''.join(data_list).split(str(sep_all))
    # 有行分隔符, 将会把 list(str) 转化成 list(list)
    if len(list(filter(lambda x: x is not None, [sep_line, sep_line_prefix, sep_line_contain, sep_line_suffix, sep_line_with_space_count]))):
        # 当是这种情况的时候,返回的数据结果
        r_list = []
        # 数据中的一行 list 数据
        one_list = []
        # 空格数量
        space_count = 0
        for d_o in data_list:
            space_count = space_count + 1 if not d_o.strip() else 0
            # 过滤掉空行,无效行
            if len(d_o.strip()) and sep_is_front:
                one_list.append(d_o)
            # 这一行, 等于 sep_line
            if ((sep_line is not None and d_o == sep_line) or
                    # 这一行, 包含 sep_line_contain
                    (sep_line_contain is not None and d_o.find(sep_line_contain) != -1) or
                    # 这一行, 是否是以 sep_line_prefix 开头
                    (sep_line_prefix is not None and d_o.startswith(sep_line_prefix)) or
                    # 这一行, 是否是以 sep_line_suffix 结尾
                    (sep_line_suffix is not None and d_o.endswith(sep_line_suffix))):
                if len(one_list):
                    r_list.append(one_list)
                    one_list = []
            if len(d_o.strip()) and not sep_is_front:
                one_list.append(d_o)
            # 按照空格行的数量来进行分割
            if sep_line_with_space_count is not None and space_count == sep_line_with_space_count:
                if len(one_list):
                    r_list.append(one_list)
                    one_list = []
                space_count = 0
        # 最后的一条数据,兼容一下
        if len(one_list):
            r_list.append(one_list)
        data_list = r_list
    # 对这个 list 进行行内再次分割
    if sep is not None:
        r_list = []
        for line in data_list:
            # list(str) 情况
            if isinstance(line, str):
                r_list.append(line.split(str(sep)))
            # list(list) 情况
            elif isinstance(line, list):
                a_list = []
                for o_line in line:
                    a_list.append(o_line.split(str(sep)))
                r_list.append(a_list)
        data_list = r_list
    # data_list 中的每一个元素都转化成 str
    if line_join is not None:
        data_list = list(map(lambda x: str(line_join).join(x), data_list))
    # data_list 中的每一个元素都转化成 先转化成str, 然后再转化成json
    if line_json is not None and line_json:
        data_list = list(map(lambda x:
                             json.loads(str('' if line_join is None else line_join).join(x)),
                             list(filter(lambda x: x is not None and len(str(x)), data_list))
                             )
                         )
    return data_list


# 读取文件中的数据,返回一个 str
def to_str_from_file(file_name: str = 'a.txt',
                     str_join: str = ' ',
                     ignore_start_with: list | int | str | None = None,
                     ignore_end_with: list | int | str | None = None,
                     start_index: int = None,
                     start_line: str = None,
                     end_index: int = None,
                     end_line: str = None,
                     count: int = None) -> str:
    return to_data_from_file(file_name=file_name,
                             ignore_start_with=ignore_start_with,
                             ignore_end_with=ignore_end_with,
                             str_join=str_join,
                             start_index=start_index,
                             start_line=start_line,
                             end_index=end_index,
                             end_line=end_line,
                             count=count,
                             r_str=True)


# 读取文件中的数据,返回一个 json
def to_json_from_file(file_name: str = 'a.txt',
                      start_index: int = None,
                      start_line: str = None,
                      end_index: int = None,
                      end_line: str = None,
                      count: int = None) -> dict[str, Any]:
    return to_data_from_file(file_name=file_name,
                             start_index=start_index,
                             start_line=start_line,
                             end_index=end_index,
                             end_line=end_line,
                             ignore_start_with=['//', '/*', '#'],
                             count=count,
                             r_json=True)


def to_data_from_file(file_name: str = 'a.txt',
                      sep: str = None,
                      sep_line: str = None,
                      sep_all: str = None,
                      ignore_start_with: list | int | str | None = None,
                      ignore_end_with: list | int | str | None = None,
                      start_index: int = None,
                      start_line: str = None,
                      end_index: int = None,
                      end_line: str = None,
                      count: int = None,
                      sheet_index: int = 1,
                      column_index: list | int | str | None = None,
                      column_date: list | int | str | None = None,
                      column_datetime: list | int | str | None = None,
                      r_json: bool = False,
                      str_join: str = '',
                      r_str: bool = False) -> str | dict[str, Any]:
    """
    在 to_list 方法上再嵌套一层,
    r_str    : 返回的数据是否是一个 字符串, ''.join(list)
    str_join : 返回的数据是否是一个 字符串, str_join.join(list), 用 str_join 做连接
    r_json   : 返回的数据是否是一个 json 类型的数据
    """
    d = to_list(file_name=file_name,
                sep=sep,
                sep_line=sep_line,
                sep_all=sep_all,
                ignore_start_with=ignore_start_with,
                ignore_end_with=ignore_end_with,
                start_index=start_index,
                start_line=start_line,
                end_index=end_index,
                end_line=end_line,
                count=count,
                sheet_index=sheet_index,
                column_index=column_index,
                column_date=column_date,
                column_datetime=column_datetime)
    return str_join.join(d) if r_str else json.loads(str_join.join(d)) if r_json else d


# 将文件导出成excel格式的
def to_excel(data_list: set | list | tuple | None,
             file_name: str = None,
             file_path: str = 'excel') -> None:
    if file_name is None:
        file_name = 'excel'
    file_name = str(file_name)
    while file_path.endswith('/'):
        file_path = file_path[0:-1]
    check_file(file_path)
    # 实例化对象excel对象
    excel_obj = openpyxl.Workbook()
    # excel 内第一个sheet工作表
    excel_obj_sheet = excel_obj[excel_obj.sheetnames[0]]
    # 给单元格赋值
    for one_data in data_list:
        s_list = []
        if isinstance(one_data, list) or isinstance(one_data, set):
            for one in one_data:
                if isinstance(one, dict) or isinstance(one, list):
                    s = json.dumps(one)
                else:
                    s = str(one)
                s_list.append(s)
            excel_obj_sheet.append(s_list)
        else:
            if is_json_serializable(one_data):
                s = json.dumps(one_data)
            else:
                s = str(one_data)
            excel_obj_sheet.append([s])

    # 文件保存
    excel_obj.save(file_path + '/' + get_file_name(file_name, '.xlsx', True))


def to_csv(data_list: set | list | tuple | dict,
           file_name: str = None,
           file_path: str = 'csv') -> None:
    """
    将文件导出成csv格式的
    data_list 格式
    data_list = [['Name', 'Age', 'Gender'],
                 ['Alice', 25, 'Female'],
                 ['Bob', 30, 'Male'],
                 ['Charlie', 35, 'Male']]
    data_list = [{
          "a": 1,
          "b": 2,
      },{
          "a": 1,
          "b": 2,
    }]
    file_name = 'data'
    """
    if file_name is None:
        file_name = 'csv'
    file_name = get_file_name(file_name, '.csv', True)
    while file_path.endswith('/'):
        file_path = file_path[0:-1]
    check_file(file_path)
    d_list = []
    if isinstance(data_list, tuple):
        d_list = list(data_list)
    else:
        if len(data_list) and (isinstance(data_list[0], dict) or isinstance(data_list[0], tuple)):
            title_list = []
            for key in data_list[0]:
                title_list.append(key)
            d_list.append(title_list)
            for one_data in data_list:
                one_list = []
                for k in title_list:
                    one_list.append(one_data[k])
                d_list.append(one_list)
        else:
            d_list = data_list
    with open(file_path + '/' + file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(d_list)
