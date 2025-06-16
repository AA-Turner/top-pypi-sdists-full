from typing import Any

from yplib import *
from yplib.common_package import *
from pymysql.connections import Connection

# 创建一个线程本地存储对象
__THREAD_LOCAL_DB_DATA = threading.local().data = {}


# 有关数据库操作的类
def get_connect(database: str = None,
                user: str = None,
                password: str = None,
                charset: str = 'utf8mb4',
                port: int = 3306,
                host: str = None) -> Connection:
    return pymysql.connect(database=database, user=user, password=password, charset=charset, port=port, host=host)


def get_connect_from_config(db_config: str = None,
                            database: str = None,
                            user: str = None,
                            password: str = None,
                            charset: str = None,
                            port: int = None,
                            host: str = None) -> Connection:
    db_config = __THREAD_LOCAL_DB_DATA['get_connect_from_config_db_config'] = db_config or __THREAD_LOCAL_DB_DATA.get('get_connect_from_config_db_config', 'db')
    config_db = get_config_data(db_config)
    database = database or config_db.get('database')
    user = user or config_db.get('user')
    host = host or config_db.get('host')
    password = password or config_db.get('password')
    port = port or config_db.get('port', 3306)
    charset = charset or config_db.get('charset', 'utf8mb4')
    # 生成线程标识
    thread_key = f"{db_config}_{database}" if database else db_config
    conn_pool = __THREAD_LOCAL_DB_DATA.get('get_connect_from_config', {})
    # 获取连接，如果没有，则创建新的连接并保存到线程本地存储
    if thread_key not in conn_pool:
        conn_pool[thread_key] = get_connect(database=database, user=user, password=password, charset=charset, port=port, host=host)
        __THREAD_LOCAL_DB_DATA['get_connect_from_config'] = conn_pool  # 确保保存到线程本地存储
    return conn_pool[thread_key]


def exec_sql(sql: str = '',
             db_conn: Connection = None,
             db_config: str = None,
             commit: bool = True,
             is_log: bool = False,
             database: str = None) -> None:
    db_config = __THREAD_LOCAL_DB_DATA['exec_sql_db_config'] = db_config or __THREAD_LOCAL_DB_DATA.get('exec_sql_db_config', 'db')
    """
    执行 SQL 语句，并提交（默认提交）。

    :param sql: 需要执行的 SQL 语句（字符串或列表）。
    :param db_conn: 数据库连接对象，若为空则自动获取。
    :param db_config: 数据库配置名称。
    :param commit: 是否提交事务（默认提交）。
    :param is_log: 是否记录日志。
    :param database: 具体的数据库，会覆盖 db_config 中的设置。
    """
    if not sql:
        is_log and to_log_file("db_conn is None or sql is None or sql == '', so return")
        return
    # 获取数据库连接（使用线程本地存储）
    db_conn = db_conn or get_connect_from_config(db_config, database=database)
    db_cursor = db_conn.cursor()
    # 处理 SQL 语句
    sql_list = sql if isinstance(sql, (list, set)) else [sql]
    for s in sql_list:
        is_log and to_log_file(s)
        db_cursor.execute(str(s))
    if commit:
        db_conn.commit()


def get_doris_conn(db_config: str = None) -> Connection:
    db_config = __THREAD_LOCAL_DB_DATA['get_doris_conn_db_config'] = db_config or __THREAD_LOCAL_DB_DATA.get('get_doris_conn_db_config', 'doris')
    return get_connect_from_config(db_config)


# 执行 sql 语句, 并且提交, 默认值提交的了
def exec_doris_sql(sql: str = '',
                   db_config: str = None,
                   database: str = None) -> None:
    db_config = __THREAD_LOCAL_DB_DATA['exec_doris_sql_db_config'] = db_config or __THREAD_LOCAL_DB_DATA.get('exec_doris_sql_db_config', 'doris')
    database = __THREAD_LOCAL_DB_DATA['exec_doris_sql_database'] = database or __THREAD_LOCAL_DB_DATA.get('exec_doris_sql_database', 'mx_risk')
    exec_sql(sql, db_config=db_config, database=database)


def get_data_from_doris(sql: str = '',
                        db_config: str = None) -> tuple[tuple[Any, ...], ...]:
    db_config = __THREAD_LOCAL_DB_DATA['get_data_from_doris_db_config'] = db_config or __THREAD_LOCAL_DB_DATA.get('get_data_from_doris_db_config', 'doris')
    conn_doris = get_connect_from_config(db_config)
    cursor = conn_doris.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def get_data_from_doris_with_title(sql: str = '',
                                   db_config: str = None) -> tuple[tuple[tuple[Any, ...], ...], list[str]]:
    db_config = __THREAD_LOCAL_DB_DATA['get_data_from_doris_db_config'] = db_config or __THREAD_LOCAL_DB_DATA.get('get_data_from_doris_db_config', 'doris')
    conn_doris = get_connect_from_config(db_config)
    cursor = conn_doris.cursor()
    cursor.execute(sql)
    title_list = [desc[0] for desc in cursor.description]
    return cursor.fetchall(), title_list


def get_data_line_one_from_doris(sql: str = '',
                                 db_config: str = None) -> list | None:
    db_config = __THREAD_LOCAL_DB_DATA['get_data_line_one_from_doris_db_config'] = db_config or __THREAD_LOCAL_DB_DATA.get('get_data_line_one_from_doris_db_config', 'doris')
    data_list = get_data_from_doris(sql, db_config=db_config)
    if len(data_list):
        return list(data_list[0])
    return None


# 执行 sql 语句, 不提交
def exec_sql_un_commit(sql: str = '',
                       db_conn: Connection = None,
                       db_config: str = None,
                       database: str = None) -> None:
    db_config = __THREAD_LOCAL_DB_DATA['exec_sql_un_commit_db_config'] = db_config or __THREAD_LOCAL_DB_DATA.get('exec_sql_un_commit_db_config', 'db')
    exec_sql(sql=sql, db_conn=db_conn, db_config=db_config, commit=False, database=database)


# 执行 sql 获得 数据
def get_data_from_sql(sql: str = '',
                      db_conn: Connection = None,
                      db_config: str = None,
                      is_log: bool = False,
                      database: str = None) -> tuple[tuple[Any, ...], ...] | None:
    db_config = __THREAD_LOCAL_DB_DATA['get_data_from_sql_db_config'] = db_config or __THREAD_LOCAL_DB_DATA.get('get_data_from_sql_db_config', 'db')
    if not sql:
        is_log and to_log_file("db_conn is None or sql is None or sql == '', so return")
        return None
    db_conn = db_conn or get_connect_from_config(db_config, database=database)
    db_cursor = db_conn.cursor()
    is_log and to_log_file(sql)
    db_cursor.execute(str(sql))
    return db_cursor.fetchall()


def extract_sql(log_content: str = '') -> tuple[str | None, str | None]:
    """
    从日志中提取一组 SQL 执行信息：
    1. 优先使用 Preparing 的 SQL。
    2. 将 Preparing 中的 ? 替换成 Parameters 中的参数。
    3. 提取 Total 总数。
    4. 如果没有 Preparing，则使用 Executing。
    """
    # 正则模式
    sql_executing_pattern = re.compile(r"Executing:\s*(.*)")
    sql_preparing_pattern = re.compile(r"Preparing:\s*(.*)")
    sql_parameters_pattern = re.compile(r"Parameters:\s*(.*)")
    sql_total_pattern = re.compile(r"Total:\s*(\d+)")

    # 处理逻辑
    lines = log_content.splitlines()
    executing_sql = None
    preparing_sql = None
    parameters_sql = None
    total_sql = None

    for line in lines:
        if "Executing:" in line:
            match = sql_executing_pattern.search(line)
            if match:
                executing_sql = match.group(1).strip()

        elif "Preparing:" in line:
            match = sql_preparing_pattern.search(line)
            if match:
                preparing_sql = match.group(1).strip()

        elif "Parameters:" in line:
            match = sql_parameters_pattern.search(line)
            if match:
                parameters_sql = match.group(1).strip()

        elif "Total:" in line:
            match = sql_total_pattern.search(line)
            if match:
                total_sql = match.group(1).strip()

    # 选择 SQL
    sql = preparing_sql or executing_sql

    # 替换参数
    if preparing_sql and parameters_sql:
        params_list = []
        # 解析参数
        for param in parameters_sql.split(", "):
            if "(" in param and param.endswith(")"):
                value, _type = param.rsplit("(", 1)
                value = value.strip()
                if value.lower() == "null":
                    params_list.append("NULL")
                else:
                    params_list.append(f"'{value}'")
            else:
                params_list.append(f"'{param.strip()}'")

        # 替换 ? 为参数
        for param in params_list:
            sql = sql.replace("?", param, 1)

    return sql, total_sql


def format_sql(sql: str) -> str:
    return sqlparse.format(sql, reindent=True, keyword_case="upper")


def deal_sql(sql: str) -> str:
    sql = sql.replace('\n', ' ')
    sql = re.sub(r'\s+', ' ', sql).strip()
    return sql


def compress_sql(sql: str) -> str:
    return re.sub(r'\s+', ' ', str(sql).replace('\n', ' ').replace('\r', ' ')).strip()
