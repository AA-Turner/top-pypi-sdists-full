from daos.graph_add_op import CHGraph
from utils.ck_client import get_client
from utils.decorators import log_execute_time
from daos.graph_op import CHGraph as ch
from config.logger_design import get_logger
from config.config import ClusterConfig
from services.common import get_graph_vertexes, get_graph_edges
from services.sql_condition_operation import ConditionOperation
from utils.sql_replace_operation import SqlReplaceHandler
# from celery_tasks.tasks import graph_calculation_task

cluster_config = ClusterConfig()
sql_replace_handler = SqlReplaceHandler(cluster_config.is_cluster)
logger = get_logger()

operation_dict = {'avg': 'avg', 'sum': 'sum', 'min': 'min', 'max': 'max', 'count': 'count', }


def disconnect_client(client):
    if client:
        client.disconnect()


class ModelService(object):
    calculations = ["Pagerank", "Closeness", "Betweenness"]
    # 切换图空间
    def use_graph(self, graph_name, db):
        res = db.use_tables(graph_name)
        print(res)
        if res is None:
            logger.warning("graph name [" + graph_name + "] does not exist")
            return
        else:
            self.graph_name = graph_name
            self.graph_cfg = res
            logger.info("use graph [" + graph_name + "] done")

    def get_graph_task(self, graph_name, db):
        res = db.get_task(graph_name)
        print(res)
        if res is None:
            logger.warning("get_graph_task ,graph name [" + graph_name + "] does not exist")
            return
        else:
            logger.info("get_graph_task  [" + graph_name + "] done")
            return ",".join(('%s' %num for num in res))


    def search_subgraph_by_condition(self, data, config_param):
        """
        根据条件过滤查询子图
        """
        graph_name = data.get("subGraph")
        if not graph_name:
            return

        edge_types = data.get("edgeTypes")
        node_types = data.get("nodeTypes")

        db = config_param["db"]
        clickhouse_connect = config_param["clickhouse_connect"]
        graph_client = get_client(clickhouse_connect)
        graph = CHGraph(graph_client)
        self.use_graph(graph_name, db)

        edges = self.graph_cfg["edges"]
        vertexes = self.graph_cfg["vertexes"]

        if "edgeConditions" in data.keys():
            edge_conditions = data["edgeConditions"]
            edge_condition_dict, edge_order_dict, special_sql_dict = ConditionOperation().conditionalOperation(
                edge_conditions, edges)
        else:
            edge_condition_dict, edge_order_dict = {}, {}
        if "nodeConditions" in data.keys():
            node_conditions = data["nodeConditions"]
            node_condition_dict, node_order_dict, special_sql_dict = ConditionOperation().conditionalOperation(
                node_conditions, vertexes)
        else:
            node_condition_dict, node_order_dict = {}, {}

        ext_field_list = data.get("fieldList")
        result_type = data.get("resultType")

        data = {}
        path_data = {}
        edge_data_list = []
        vertexes_data_list = []

        if edge_types:
            edge_data_list = execute_controller(edge_types, edges, edge_condition_dict, edge_order_dict, graph, "edge",
                                               ext_field_list, result_type)

        if node_types:
            vertexes_data_list = execute_controller(node_types, vertexes, node_condition_dict, node_order_dict, graph,
                                                   "vertexes", ext_field_list, result_type)

        path_data["graphEdges"] = edge_data_list
        path_data["graphNodes"] = vertexes_data_list
        data["pathList"] = path_data
        # 释放链接
        disconnect_client(graph_client)
        return data

    def time_line_search(self, data, config_param):
        """
        时间轴获取点边的模型
        """
        res_data = {}

        graph_name = data.get("subGraph")
        if not graph_name:
            return

        db = config_param["db"]
        clickhouse_connect = config_param["clickhouse_connect"]
        graph_client = get_client(clickhouse_connect)
        graph = CHGraph(graph_client)
        self.use_graph(graph_name, db)

        res = None
        edges = self.graph_cfg["edges"]
        vertexes = self.graph_cfg["vertexes"]

        if "edgeConditions" in data.keys():
            edge_conditions = data["edgeConditions"]
            edge_condition_dict, edge_order_dict, special_sql_dict = ConditionOperation().conditionalOperation(
                edge_conditions, edges)
            if "sql" in special_sql_dict:
                res = execute_graph_sql(graph, special_sql_dict["sql"])
        elif "nodeConditions" in data.keys():
            node_conditions = data["nodeConditions"]
            node_condition_dict, node_order_dict, special_sql_dict = ConditionOperation().conditionalOperation(
                node_conditions, vertexes)
            if "sql" in special_sql_dict:
                res = execute_graph_sql(graph, special_sql_dict["sql"])

        if res:
            res_dict = res["data"]
            res_data["columns"] = res_dict["schema"]
            res_data["rowList"] = res_dict["detail"]
        # 释放链接
        disconnect_client(graph_client)
        return res_data

    def count_src_dst_round(self, data, config_param):
        """
        统计任意两点间的边
        """
        graph_name = data.get("subGraph")
        edge_types = data.get("edgeTypes")
        if not graph_name:
            return

        db = config_param["db"]
        clickhouse_connect = config_param["clickhouse_connect"]
        graph_client = get_client(clickhouse_connect)
        graph = CHGraph(graph_client)
        self.use_graph(graph_name, db)

        edges = self.graph_cfg["edges"]
        if "edgeConditions" in data:
            edge_conditions = data.get("edgeConditions")
            edge_condition_dict, edge_order_dict, special_sql_dict = ConditionOperation().conditionalOperation(
                edge_conditions, edges)
        else:
            edge_condition_dict, edge_order_dict = {}, {}

        if edge_types:
            edge_data_list = execute_controller(edge_types, edges, edge_condition_dict, edge_order_dict, graph,
                                               "edgeCount")
        else:
            edge_data_list = execute_controller(edges.keys(), edges, edge_condition_dict, edge_order_dict, graph,
                                               "edgeCount")
        res_data = {}
        res_list = []
        if edge_data_list:
            for res_dict in edge_data_list:
                res = res_dict["data"]
                res_data["columns"] = res["schema"]
                res_data["rowList"] = res["detail"]
                res_data["type"] = res_dict["type"]
                res_list.append(res_data)
        # 释放链接
        disconnect_client(graph_client)
        return res_list

    @log_execute_time(logger)
    def query_subgraph(self, data, config_params):
        """
        根据条件过滤查询子图
        """
        graphName = data.get("subGraph")
        if not graphName:
            raise Exception("subGraph name is None")

        db = config_params["db"]
        clickhouse_connect = config_params["clickhouse_connect"]
        graph_client = get_client(clickhouse_connect)
        graph = ch(graph_client)
        graph.use_graph(graphName, db)
        graph_cfg = graph.graph_cfg

        vertexes = get_graph_vertexes(graph_cfg, graph)
        edges = get_graph_edges(graph_cfg, graph)

        res_list = {}
        res_list["pathList"] = {}
        res_list["pathList"]["graphEdges"] = edges
        res_list["pathList"]["graphNodes"] = vertexes
        return res_list

    def statistics_operation_function(self, data, config_param):
        """
        统计子图中点或者边的数量
        """
        data = dispose_parse_params(data)
        graph_name = data.get("subGraph")
        graph_type = data.get("type")
        orderTypes = data.get("orderTypes") or ""
        if not graph_name:
            return

        db = config_param["db"]
        clickhouse_connect = config_param["clickhouse_connect"]
        graph_client = get_client(clickhouse_connect)
        graph = CHGraph(graph_client)

        operations = {"1": "count"}
        group_field = []
        order_operation = orderTypes
        field_list = []
        self.use_graph(graph_name, db)
        if graph_type:
            schemas = self.graph_cfg[graph_type]
            res = None
            for schema in schemas:
                execute_sql = join_sql(operations, group_field, order_operation,
                                      schema, schemas, field_list, graph_type)
                result_dict = execute_graph_sql(graph, execute_sql)
                res = self.dispose_statistics_operation_res(result_dict, res, schema)
            result = {graph_type: res}
        else:
            edges = self.graph_cfg["edges"]
            vertexes = self.graph_cfg["vertexes"]
            res_edge = None
            res_vertex = None
            for edge in edges:
                execute_sql = join_sql(operations, group_field, order_operation,
                                      edge, edges, field_list, "edges")
                result_dict = execute_graph_sql(graph, execute_sql)
                res_edge = self.dispose_statistics_operation_res(result_dict, res_edge, edge)
            for vertex in vertexes:
                execute_sql = join_sql(operations, group_field, order_operation,
                                      vertex, vertexes, field_list, "vertexes")
                result_dict = execute_graph_sql(graph, execute_sql)
                res_vertex = self.dispose_statistics_operation_res(result_dict, res_vertex, vertex)
            result = {"vertexes": res_vertex, "edges": res_edge}
        return result

    @staticmethod
    def dispose_statistics_operation_res(result_dict, res, type):
        if "typeValue" not in result_dict["data"]["schema"]:
            result_dict["data"]["schema"].append("typeValue")
        result_dict["data"]["detail"][0].append(type)
        if res:
            res["data"]["detail"].append(result_dict["data"]["detail"][0])
        else:
            res = result_dict
        return res

    def statistics_operation_attributes_function(self, data, config_param):
        """
        统计子图中点或者边的多个属性
        """
        data = dispose_parse_params(data)
        graph_name = data.get("subGraph")
        type_value = data.get("type")
        attributes = data.get("attributes")
        orderTypes = data.get("orderTypes") or ""
        if not graph_name or not attributes:
            return None

        # 获取客户端
        db = config_param["db"]
        clickhouse_connect = config_param["clickhouse_connect"]
        graph_client = get_client(clickhouse_connect)
        graph = CHGraph(graph_client)

        # 更新子图
        self.use_graph(graph_name, db)
        edges = self.graph_cfg["edges"]
        vertexes = self.graph_cfg["vertexes"]

        # 处理参数
        attribute_list = attributes.split(",")
        order_list = orderTypes.split(",") if orderTypes else ""

        res_list = []
        for i in range(len(attribute_list)):
            order_operation = order_list[i] if order_list else ""
            data_param = {"subGraph": graph_name, "type": type_value, "attribute": attribute_list[i],
                          "orderTypes": order_operation}
            if type_value in edges:
                index = edges[type_value]["fields"].index(attribute_list[i])
                field_type = edges[type_value]["types"][index]
                if field_type == "String":
                    data_param["statistics"] = "count"
                elif field_type == "Date":
                    data_param["statistics"] = "count"

            if type_value in vertexes:
                index = vertexes[type_value]["fields"].index(attribute_list[i])
                field_type = vertexes[type_value]["types"][index]
                if field_type == "String":
                    data_param["statistics"] = "count"
                elif field_type == "Date":
                    data_param["statistics"] = "count"
            res_one = self.statistics_operation_attribute_function(data_param, config_param, graph=graph)
            res_list.append(res_one)

        return res_list

    def statistics_operation_attribute_function(self, data, config_param, label_statistic=None, graph=None):
        """
        统计点或者边的单个属性
        """
        data = dispose_parse_params(data)
        graph_name = data.get("subGraph")
        type_value = data.get("type")
        attribute = data.get("attribute")
        statistics = data.get("statistics") or "def"
        orderTypes = data.get("orderTypes") or ""
        if not graph_name or not attribute:
            return

        # 处理参数
        attribute_arr = attribute.split(",")
        statistics_arr = statistics.split(",")
        if len(statistics_arr) != len(attribute_arr):
            return

        operations = {}
        for i in range(len(statistics_arr)):
            operations[attribute_arr[i]] = statistics_arr[i]
        if "def" in statistics_arr:
            group_field = None
        else:
            group_field = attribute_arr
        order_operation = orderTypes
        field_list = []

        # 获取客户端
        db = config_param["db"]
        clickhouse_connect = config_param["clickhouse_connect"]
        graph_client = get_client(clickhouse_connect)
        if not graph:
            graph = CHGraph(graph_client)

        # 更换子图
        self.use_graph(graph_name, db)
        edges = self.graph_cfg["edges"]
        vertexes = self.graph_cfg["vertexes"]
        if type_value in edges:
            edge_schema = edges[type_value]
            if label_statistic:
                group_field = [edge_schema["src"], edge_schema["dst"]]
            execute_sql = join_sql(operations, group_field, order_operation,
                                  type_value, edges, field_list, "edges")
        elif type_value in vertexes:
            vertex_schema = vertexes[type_value]
            if label_statistic:
                group_field = [vertex_schema["id"]]
            execute_sql = join_sql(operations, group_field, order_operation,
                                  type_value, vertexes, field_list, "vertexes")
        else:
            return None
        result_dict = execute_graph_sql(graph, execute_sql)

        return result_dict


    def calculation_attribute_select_function(self, data, config_param, label_statistic=None, graph=None):
        """
        计算属性查询
        """
        data = dispose_parse_params(data)
        graph_name = data.get("subGraph")
        compute = data.get("compute")
        task_id = data.get("taskId")
        if not graph_name:
            return
        # 获取客户端
        db = config_param["db"]
        clickhouse_connect = config_param["clickhouse_connect"]
        graph_client = get_client(clickhouse_connect)
        if not graph:
            graph = CHGraph(graph_client)

        # 更换子图
        # self.use_graph(graph_name, db)
        computes, task_str = self.execute_params_2_calculation(compute, task_id)
        if task_str is None:
            task_str = self.get_graph_task(graph_name, db)
        if task_str is None:
            return None
        column_str = ""
        for com in computes:
            column_str = column_str + " ,sumIf(val,graph_algorithm_type = '"+com+"') as  " + com

        execute_sql = "select id ,id_type " + column_str + "  from " + graph_name +\
                      ".calculation_attribute where task_id in " \
                      " ( "+task_str + ") group by id,id_type"
        result_dict = execute_graph_sql(graph, execute_sql)

        return result_dict


    def calculation_attribute_submit_function(self, data, config_param, label_statistic=None, graph=None):
        """
        计算任务提交
        """
        data = dispose_parse_params(data)
        graph_name = data.get("subGraph")
        compute = data.get("compute")
        task_id = data.get("taskId")
        logger.info("subGraph:"+graph_name+"   compute:"+compute+"  task_id:"+str(task_id))
        if not graph_name or not task_id or not compute:
            return None
        # 获取客户端
        db = config_param["db"]
        clickhouse_connect = config_param["clickhouse_connect"]
        graph_client = get_client(clickhouse_connect)
        if not graph:
            graph = CHGraph(graph_client)
        #对接计算任务接口调用
        try:
            pass
            # graph_calculation_task.delay(graph_name, task_id, compute)
        except Exception as e:
            print(e)
            logger.error(e)
            return "task filed"
        return "success"

    def execute_params_2_calculation(self, compute, task_id):
        """
        处理计算参数
        """
        if compute and task_id:
            return [compute], "\'"+str(task_id)+"\'"
        else:
            return self.calculations,None


def join_sql(operations, group_field, order_operation,
            type_vertex, schema, field_list, subgraph_type):
    """
    拼接sql,查询表数量
    """
    field_list = field_list if field_list else []
    for operation in operations:
        if operation in field_list:
            continue
        field_list.append(operation)

    if group_field:
        for field in group_field:
            if field in field_list:
                continue
            field_list.append(field)

    operList = statistics_operation(operations)
    operStr = ','.join(operList)
    group_s = ""
    operStr_new = operStr
    if group_field:
        group_str = ','.join(group_field)
        operStr_new = group_str + "," + operStr_new
        group_s = " group by " + group_str
    main_sql = main_sql_value(type_vertex, schema, field_list, subgraph_type)
    if main_sql:
        sql = "select " + operStr_new + " from (" + main_sql + ")" + group_s + " order by " + operStr + "  " + order_operation
        return sql


def statistics_operation(operations):
    """
    处理Statistics函数
    """
    operList = []
    for operation in operations:
        oper = operations[operation]
        if oper in operation_dict:
            operList.append(operation_dict[oper] + '(' + operation + ')')
        else:
            operList.append(operation)
    return operList


def main_sql_value(type_value, schema, field_list, subgraph_type):
    """
    点子图主sql
    """
    sql = None
    if type_value in schema:
        value = schema[type_value]
        if subgraph_type == "vertexes":
            if field_list:
                fields = ",".join(field_list)
                sql = "select distinct " + value["id"] + "," + fields + " from " + value["db"] + "." + value["table"]
            else:
                sql = "select distinct " + value["id"] + "," + " from " + value["db"] + "." + value["table"]
        else:
            if field_list:
                fields = ",".join(field_list)
                sql = "select distinct " + value["src"] + "," + value["dst"] + "," + value["rank"] + "," + fields \
                      + " from " + value["db"] + "." + value["table"]
            else:
                sql = "select distinct " + value["src"] + "," + value["dst"] + "," + value["rank"] + "," + " from " \
                      + value["db"] + "." + value["table"]
    return sql


def execute_controller(array, schema, condition_dict, order_dict, graph, type,
                      ext_field_list=None, result_type=None):
    """
    执行多条sql，并拼接返回
    """
    result = []
    for key in array:
        data = schema[key]
        condition = condition_splice(key, condition_dict)
        order = condition_splice(key, order_dict)
        if type == "edge":
            main_sql = edges_splice(data, ext_field_list)
        elif type == "edgeCount":
            main_sql = edges_count_splice(data)
            group_splice = edges_group_splice(data)
        else:
            main_sql = vertexes_splice(data, ext_field_list)

        if main_sql:
            if type == "edgeCount":
                sql = main_sql + condition + group_splice + order
            else:
                sql = main_sql + condition + order
            vertexes_data = execute_graph_sql(graph, sql, key, result_type)
            result.append(vertexes_data)
    return result


def edges_group_splice(edges_schema):
    src = edges_schema.get("src")
    dst = edges_schema.get("dst")

    if not src or not dst:
        return

    group_splice = " group by " + src + "," + dst + " "
    return group_splice


def execute_graph_sql(graph, sql, type=None, result_type=None):
    """
    组合sql执行，返回图对象
    """
    result_dict = {}

    new_sql = sql_replace_handler.deal_sql(sql)
    logger.info("[execute_graph_sql] is_cluster:{}      sql:{}".format(sql_replace_handler.is_cluster, new_sql))
    res = graph.execute(new_sql)

    if result_type:
        result_dict["data"] = res
    else:
        data = {}
        schemas = res.columns.values.tolist()
        field_data = res.values.tolist()
        data["schema"] = schemas
        data["detail"] = field_data
        result_dict["data"] = data

    if type:
        result_dict["type"] = type
    return result_dict


def condition_splice(type, condition={}):
    """
    拼接条件
    """
    if len(condition) > 0 and type in condition:
        return condition[type]
    return ""


def vertexes_splice(vertexes_schema, ext_field_list=None):
    """
    拼接点主体查询sql
    """
    db = vertexes_schema.get("db") or "default"
    table = vertexes_schema.get("table")
    id = vertexes_schema.get("id")
    label = vertexes_schema.get("label")

    for item in [table, id, label]:
        if not item:
            return

    if not ext_field_list:
        ext_field_list = vertexes_schema.get("fields")

    for item in [id, label]:
        if item in ext_field_list:
            ext_field_list.remove(item)

    ext_field = ",".join(ext_field_list) if ext_field_list else None
    if ext_field:
        main_sql = "select distinct " + id + "," + label + ", " + ext_field + " from " + db + "." + table
    else:
        main_sql = "select distinct " + id + "," + label + " from " + db + "." + table
    return main_sql


def edges_splice(edges_schema, ext_field_list=None):
    """
    拼接边主体查询sql
    """
    db = edges_schema.get("db") or "default"
    table = edges_schema.get("table")
    src = edges_schema.get("src")
    dst = edges_schema.get("dst")
    rank = edges_schema.get("rank")

    for item in [table, src, dst, rank]:
        if not item:
            return

    if not ext_field_list:
        ext_field_list = edges_schema.get("fields")

    for item in [src, dst, rank]:
        if item in ext_field_list:
            ext_field_list.remove(item)

    ext_field = ",".join(ext_field_list) if ext_field_list else None
    if ext_field:
        main_sql = "select distinct " + src + ", " + dst + "," + rank + " ," + ext_field + "  from  " + db + "." + table
    else:
        main_sql = "select distinct " + src + ", " + dst + "," + rank + "  from  " + db + "." + table
    return main_sql


def edges_count_splice(edges_schema):
    """
    拼接边主体查询sql
    """
    db = edges_schema.get("db") or "default"
    table = edges_schema.get("table")
    src = edges_schema.get("src")
    dst = edges_schema.get("dst")
    rank = edges_schema.get("rank")

    for item in [table, src, dst, rank]:
        if not item:
            return

    main_sql = "select " + src + ", " + dst + ", count(1) count  from  " + db + "." + table
    return main_sql


def group_attribute_operation(group_attribute):
    """
    拼接group by
    暂时不用，没有处理聚合函数
    """
    if group_attribute:
        group = ",".join(group_attribute)
        return "group by " + group


def dispose_parse_params(data):
    """
    处理parse.parse_qs方法获取的get参数
    """
    for key in data.keys():
        if isinstance(data[key], list):
            data[key] = data[key][0]
    return data


def main():
    from clickhouse_driver import Client
    graphClient = Client(host="10.202.255.93", port="9090", user="default", password="root")
    from daos.graph_op import CHGraph
    graph = CHGraph(graphClient)
    res = graph.execute("select * from anti_money_launder.transactions limit 10")
    list = res.columns.values.tolist();
    print(res.values.tolist())
    print(list)


def test():
    from config import data_load_config as config
    config_params = config.load_config()
    str(config_params["db"])
    print(str(config_params["db"]))
    dict_data = {"subGraph": "anti_money_launder"}
    model_service = ModelService()
    result_dict = model_service.search_subgraph_by_condition(dict_data, config_params)
    print(result_dict)


def test_function():
    from config import data_load_config as config
    config_params = config.load_config()
    str(config_params["db"])
    print(str(config_params["db"]))

    dict_data = {"subGraph": "0b58bfda_7bf5_4661_ae21_5079057afe49", "type": "xiqianvertex",
                 "attributes": "type,acct_stat"}
    model_service = ModelService()
    result_dict = model_service.statistics_operation_attributes_function(dict_data, config_params)
    print(result_dict)


if __name__ == '__main__':
    # main()
    test_function()
