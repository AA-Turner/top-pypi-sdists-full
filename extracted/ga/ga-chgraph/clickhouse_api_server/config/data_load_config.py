import os
import ujson
from utils.ck_client import get_client
from daos.graph_op import CHGraph
from daos.db_op import DBoperator
from config.logger_design import get_logger

logger = get_logger()


def load_config():
    print("服务所有配置开始加载")
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    clickhouse_config_dir = os.path.join(parent_dir, "graph_config.json")

    with open(clickhouse_config_dir, 'r') as f:
        clickhouse_config = ujson.load(f)

    # clickhouse config
    clickhouse_ip = os.getenv("HOST_DAISY") if os.getenv("HOST_DAISY") else clickhouse_config["ip"]
    clickhouse_port = os.getenv("PORT_TCP_DAISY") if os.getenv("PORT_TCP_DAISY") else clickhouse_config["port"]
    clickhouse_user = os.getenv("USERNAME_DAISY") if os.getenv("USERNAME_DAISY") else clickhouse_config["user"]
    clickhouse_pwd = os.getenv("PASSWORD_DAISY") if os.getenv("PASSWORD_DAISY") else clickhouse_config["password"]
    print(clickhouse_ip, clickhouse_port, clickhouse_user, clickhouse_pwd)
    logger.info("clickhouse_ip is: " + clickhouse_ip)

    # rocksdb config
    db_ip = os.getenv("DB_HOST") if os.getenv("DB_HOST") else clickhouse_config["dbip"]
    db_port = os.getenv("DB_PORT") if os.getenv("DB_PORT") else clickhouse_config["dbport"]
    db_user = os.getenv("DB_USERNAME") if os.getenv("DB_USERNAME") else clickhouse_config["dbuser"]
    db_pwd = os.getenv("DB_PASSWORD") if os.getenv("DB_PASSWORD") else clickhouse_config["dbpassword"]
    db_table = os.getenv("DB_NAME") if os.getenv("DB_NAME") else clickhouse_config["dbtable"]
    db_ssl_mode = os.getenv("DB_SSL_MODE") if os.getenv("DB_SSL_MODE") else clickhouse_config["sslMode"]

    # 创建连接
    clickhouse_connect = {"ip": clickhouse_ip, "port": clickhouse_port, "user": clickhouse_user}
    if clickhouse_pwd:
        clickhouse_connect["password"] = clickhouse_pwd

    graphClient = get_client(clickhouse_connect)
    graph = CHGraph(graphClient)

    if db_pwd:
        url = 'postgresql://' + db_user + ':' + db_pwd + '@' + db_ip + ':' + db_port + '/' + db_table + '?sslmode=require'
    else:
        url = 'postgresql://' + db_user + '@' + db_ip + ':' + db_port + '/' + db_table + '?sslmode=disable'

    db = DBoperator(url)

    print("服务所有配置加载结束")

    config_params = {
        "graph": graph,
        "db": db,
        "graphClient": graphClient,
        "clickhouse_connect": clickhouse_connect
    }
    return config_params


if __name__ == "__main__":
    sql = "show create table sub_graph_test_2.default_metagroups"
    configs = load_config()
    client = configs.get("graphClient")
    rest = client.execute(sql)
    print(rest)

    rest1 = client.execute("show create table default.default_metagroups")
    print("parent graph schema: {}".format(rest1))
