import json
import datetime
import traceback
import numpy as np

import services.model_sevice as mds

from daos.graph_op import CHGraph
from config.logger_design import get_logger
from utils.ck_client import get_client
from services.common import get_graph_edges, get_graph_vertexes

logger = get_logger()


def is_json(json_string):
    try:
        json.loads(json_string)
    except ValueError:
        return False
    return True


def model_service_ga_build(data, config_params):
    """
    创建子图
    """
    graph_name = data.get("graph")
    sql = data.get("sql")
    type = data.get("type")
    attrType = data.get("attrType")
    subGraph = data.get("subGraph")

    db = config_params.get("db")
    clickhouse_connect = config_params.get("clickhouse_connect")
    graph_client = get_client(clickhouse_connect)
    graph = CHGraph(graph_client)
    graph.use_graph(graph_name, db)

    graph_cfg = db.use_tables(graph_name)
    # db创建子图的表
    start = datetime.datetime.now()
    db.insert_tables(subGraph, json.dumps(graph_cfg), "sub", graph_name)
    end = datetime.datetime.now()
    logger.info("insert_tables count_times: {}".format(round((end - start).total_seconds(), 5) * 1000))

    # ck创建子图
    start = datetime.datetime.now()
    graph.create_subgraph(subGraph)
    end = datetime.datetime.now()
    logger.info("create_subgraph count_times: {}".format(round((end - start).total_seconds(), 5) * 1000))

    dict = graph_cfg[type][attrType]
    graph.use_graph(subGraph, db)

    # 更新子图
    start = datetime.datetime.now()
    graph.update_subgraph_by_sql(subGraph, dict, sql, type, attrType)
    end = datetime.datetime.now()
    logger.info("update_subgraph_by_sql count_times: {}".format(round((end - start).total_seconds(), 5) * 1000))

    # 获取子图的顶点的数据
    start = datetime.datetime.now()
    vertexes = get_graph_vertexes(graph_cfg, graph)
    end = datetime.datetime.now()
    logger.info("graphNodes.append count_times: {}".format(round((end - start).total_seconds(), 5) * 1000))

    # 获取子图边数据
    start = datetime.datetime.now()
    edges = get_graph_edges(graph_cfg, graph)
    end = datetime.datetime.now()
    logger.info("graphEdges.append count_times: {}".format(round((end - start).total_seconds(), 5) * 1000))

    GraphSet = {}
    GraphSet["pathList"] = {}
    GraphSet["columns"] = []
    GraphSet["rowList"] = []
    GraphSet["pathList"]["graphEdges"] = edges
    GraphSet["pathList"]["graphNodes"] = vertexes
    return GraphSet


def model_service_graph(data, config_params):
    if "is_source" in data.keys():
        is_source = data["is_source"]
    else:
        is_source = None

    if "source_graph_name" in data.keys():
        source_graph_name = data["source_graph_name"]
    else:
        source_graph_name = None

    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = None

    db = config_params["db"]
    res = db.show_tables(is_source, source_graph_name, graph_name)
    return res


def model_service_graph_insert(data, config_params):
    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        return "graph_name shouldn't be null"

    if "graph_cfg" in data.keys():
        graph_cfg = data["graph_cfg"]
        if not is_json(graph_cfg):
            return "schema is not json string"
    if "is_source" in data.keys():
        is_source = data["is_source"]
    else:
        return "is_source shouldn't be null"

    if "source_graph_name" in data.keys():
        source_graph_name = data["source_graph_name"]
    else:
        return "source_graph_name shouldn't be null"

    db = config_params["db"]
    res = db.insert_tables(graph_name, graph_cfg, is_source, source_graph_name)

    cluster_info = config_params.get("cluster", {})
    graph = config_params["graph"]
    graph.use_graph(source_graph_name, db)
    graph.create_subgraph(graph_name, cluster_info.get("is_cluster"), cluster_info.get("cluster_name"))

    return res


def model_service_graph_delete(data, config_params):
    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "cyber"

    db = config_params["db"]
    res = db.delete_tables(graph_name)

    return res


def model_service_graph_update(data, config_params):
    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "cyber"

    if "graph_cfg" in data.keys():
        graph_cfg = data["graph_cfg"]
    else:
        graph_cfg = "cyber"

    db = config_params["db"]
    res = db.update_tables(graph_name, graph_cfg)

    return res


def model_service_graph_search_multi_hop_multi_edge(data, config_params):
    '''

    :param data:
    {
    "start_vertex_list":[
        "10.73.28.115",
        "10.78.55.20"
        ],
    "edge_name_list":[
        "tcpflow",
        "flow"
        ],
    "edge_con_list_list":[["downlink_length>10000", "protocol='http'"], ["record_date='2019-04-15'"]],
    "target_field_list":[
    "record_time"
    ]
}
    :param config_params:
    :return:
    '''

    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "cyber"

    # client = Client('10.217.62.41')
    # graph = CHGraph(client)
    graph = config_params["graph"]
    db = config_params["db"]
    graph.use_graph(graph_name, db)

    if "start_vertex_list" in data.keys():
        start_vertex_list = data["start_vertex_list"]
    else:
        start_vertex_list = ['10.73.28.115', '10.78.55.20']

    if "step" in data.keys():
        step = data["step"]
    else:
        step = 1

    if "edge_name_list" in data.keys():
        edge_name_list = data["edge_name_list"]
    else:
        edge_name_list = ["tcpflow", "flow"]

    if "direction" in data.keys():
        direction = data["direction"]
    else:
        direction = "forward"

    if "edge_con_list_list" in data.keys():
        edge_con_list_list = data["edge_con_list_list"]
    else:
        edge_con_list_list = [["downlink_length>10000", "protocol='http'"], ["record_date='2019-04-15'"]]

    if "target_field_list" in data.keys():
        target_field_list = data["target_field_list"]
    else:
        target_field_list = ["record_time"]

    if "only_last_step" in data.keys():
        only_last_step = data["only_last_step"]
    else:
        only_last_step = False

    if "plus_last_vertexes" in data.keys():
        plus_last_vertexes = data["plus_last_vertexes"]
    else:
        plus_last_vertexes = False

    global res
    try:
        res = graph.multi_hop_multi_edge(step,
                                         start_vertex_list,
                                         direction,
                                         edge_name_list,
                                         edge_con_list_list,
                                         target_field_list,
                                         only_last_step,
                                         plus_last_vertexes=plus_last_vertexes
                                         )
    except Exception as e:
        print(e)

    # print(res[1])
    result = dict()
    # result["result"] = res_list2
    # res_list2 = [x.to_dict() for x in res_list2]
    if only_last_step:
        if plus_last_vertexes:
            edge = res[0]
            vertex = res[1]
            for i in range(len(edge_name_list)):
                result["hop_" + str(step)] = {}
                result["hop_" + str(step)][edge_name_list[i]] = edge[i].values.tolist()
            if type(vertex) is np.ndarray:
                result["last_step_vertex"] = vertex.tolist()
            else:
                result["last_step_vertex"] = vertex
        else:
            edge = res
            for i in range(len(edge_name_list)):
                result["hop_" + str(step)] = {}
                result["hop_" + str(step)][edge_name_list[i]] = edge[i].values.tolist()
    else:
        is_empty = True
        is_blank_list = True
        for i in range(len(res)):
            for j in range(len(res[i])):
                is_empty = is_empty & res[i][j].empty
        # if len(res) == 0 or is_empty or res == [[[] for i in range(step)]]:
        if len(res) == 0 or is_empty:
            for i in range(step):
                result["hop_" + str(i + 1)] = {}
                for j in range(len(edge_name_list)):
                    result["hop_" + str(i + 1)][edge_name_list[j]] = []
        else:
            for i in range(step):
                result["hop_" + str(i + 1)] = {}
                for j in range(len(edge_name_list)):
                    if len(res[i]) == 0:
                        result["hop_" + str(i + 1)][edge_name_list[j]] = []
                    else:
                        result["hop_" + str(i + 1)][edge_name_list[j]] = res[i][j].values.tolist()
    return result


def model_service_graph_search_one_hop_multi_edge(data, config_params):
    '''
    {
        "start_vertex_list":[
            "10.73.28.115",
            "10.78.55.20"
            ],
        "edge_name_list":[
            "tcpflow",
            "flow"
            ],
        "edge_con_list_tcpflow":[["downlink_length>10000", "protocol='http'"], ["record_date='2019-04-15'"]],
        "edge_con_list_flow":["record_time"]
    }
    '''

    # print("model_service_graph_search_one_hop_multi_edge")

    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "cyber"

    # client = Client('10.217.62.41')
    # graph = CHGraph(client)

    graph = config_params["graph"]

    # graph_dir = "./config/tcpflow_flow.cfg.json"

    # graph = CHGraph(graph_dir, client)

    db = config_params["db"]
    graph.use_graph(graph_name, db)

    if "start_vertex_list" in data.keys():
        start_vertex_list = data["start_vertex_list"]
    else:
        start_vertex_list = ['10.73.28.115', '10.78.55.20']

    if "direction" in data.keys():
        direction = data["direction"]
    else:
        direction = "forward"

    if "edge_name_list" in data.keys():
        edge_name_list = data["edge_name_list"]
    else:
        edge_name_list = ["tcpflow", "flow"]

    if "edge_con_list_list" in data.keys():
        edge_con_list_list = data["edge_con_list_list"]
    else:
        edge_con_list_list = [["downlink_length>10000", "protocol='http'"], ["record_date='2019-04-15'"]]

    if "target_field_list" in data.keys():
        target_field_list = data["target_field_list"]
    else:
        target_field_list = ["record_time"]

    if "end_vertex_con_list" in data.keys():
        end_vertex_con_list = data["end_vertex_con_list"]
    else:
        end_vertex_con_list = None

    # if "edge_con_list_tcpflow" in data.keys():
    #     edge_con_list_tcpflow = data["edge_con_list_tcpflow"]
    # else:
    #     edge_con_list_tcpflow = ["downlink_length>10000", "protocol='http'"]
    #
    # if "edge_con_list_flow" in data.keys():
    #     edge_con_list_flow = data["edge_con_list_flow"]
    # else:
    #     edge_con_list_flow = ["record_date='2019-04-15'"]

    res_list2 = graph.one_hop_multi_edge(start_vertex_list,
                                         direction,
                                         edge_name_list,
                                         edge_con_list_list,
                                         target_field_list,
                                         end_vertex_con_list
                                         )

    print("res_list2")
    print(res_list2)

    result = dict()
    # result["result"] = res_list2
    for i in range(len(edge_name_list)):
        result[edge_name_list[i]] = res_list2[i].values.tolist()

    return result


def model_service_graph_search_one_hop(data, config_params):
    '''
 {
     "start_vertex_list":[
         "10.73.28.115",
         "10.78.55.20"
         ],
     "edge_name":
         "tcpflow"
 }
 '''

    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "cyber"

    # client = Client('10.217.62.41')
    # graph = CHGraph(client)
    graph = config_params["graph"]

    # graph_dir = "./config/tcpflow_flow.cfg.json"

    # graph = CHGraph(graph_dir, client)

    db = config_params["db"]
    graph.use_graph(graph_name, db)

    if "start_vertex_list" in data.keys():
        start_vertex_list = data["start_vertex_list"]
    else:
        start_vertex_list = ['10.73.28.115', '10.78.55.20']

    if "direction" in data.keys():
        direction = data["direction"]
    else:
        direction = "forward"

    if "edge_name" in data.keys():
        edge_name = data["edge_name"]
    else:
        edge_name = ["tcpflow", "flow"]

    if "target_field_list" in data.keys():
        target_field_list = data["target_field_list"]
    else:
        target_field_list = ["record_time"]

    if "edge_con_list" in data.keys():
        edge_con_list = data["edge_con_list"]
    else:
        edge_con_list = ["downlink_length>10000", "protocol='http'"]

    if "end_vertex_con_list" in data.keys():
        end_vertex_con_list = data["end_vertex_con_list"]
    else:
        end_vertex_con_list = None

    res_list2 = graph.one_hop(start_vertex_list, direction,
                              edge_name, edge_con_list, target_field_list,
                              end_vertex_con_list)

    # result = dict()
    # result["result"] = res_list2

    return res_list2


def model_service_graph_search_multi_hop(data, config_params):
    '''

    :param data:
      {
    "start_vertex_list":[
        "10.73.28.115",
        "10.78.55.20"
        ],
        "step":2,
    "edge_name":
        "tcpflow",
    "edge_con_list":["downlink_length>10000", "protocol='http'"],
    "target_field_list":[
    "record_time"
    ]
}
    :param config_params:
    :return:
    '''

    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "cyber"

    # client = Client('10.217.62.41')
    # graph = CHGraph(client)

    graph = config_params["graph"]

    # graph_dir = "./config/tcpflow_flow.cfg.json"

    # graph = CHGraph(graph_dir, client)
    db = config_params["db"]
    graph.use_graph(graph_name, db)

    if "step" in data.keys():
        step = data["step"]
    else:
        step = 1

    if "start_vertex_list" in data.keys():
        start_vertex_list = data["start_vertex_list"]
    else:
        start_vertex_list = ['10.73.28.115', '10.78.55.20']

    if "direction" in data.keys():
        direction = data["direction"]
    else:
        direction = "forward"

    if "edge_name" in data.keys():
        edge_name = data["edge_name"]
    else:
        edge_name = "tcpflow"

    if "edge_con_list" in data.keys():
        edge_con_list = data["edge_con_list"]
    else:
        edge_con_list = ["downlink_length>10000", "protocol='http'"]

    if "target_field_list" in data.keys():
        target_field_list = data["target_field_list"]
    else:
        target_field_list = ["record_time"]

    if "plus_last_vertexes" in data.keys():
        plus_last_vertexes = data["plus_last_vertexes"]
    else:
        plus_last_vertexes = False

    if "end_vertex_con_list" in data.keys():
        end_vertex_con_list = data["end_vertex_con_list"]
    else:
        end_vertex_con_list = None

    if "only_last_step" in data.keys():
        only_last_step = data["only_last_step"]
    else:
        only_last_step = True

    res_list2 = graph.multi_hop(
        step,
        start_vertex_list,
        direction,
        edge_name,
        edge_con_list,
        target_field_list,
        only_last_step,
        plus_last_vertexes=plus_last_vertexes,
        end_vertex_con_list=end_vertex_con_list)

    # result = dict()
    # result["result"] = res_list2

    return res_list2


def model_service_graph_search_multi_hop_common_vertexes(data, config_params):
    '''

    :param data:
    {
       "step":1,
       "start_vertex_list":[
           "10.73.28.115",
           "10.78.55.20"
           ],
       "edge_name":
           "tcpflow",
       "edge_con_list":[ "protocol='http'"]
   }
    :param config_params:
    :return:
    '''

    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "cyber"

    # client = Client('10.217.62.41')
    # graph = CHGraph(client)

    graph = config_params["graph"]

    db = config_params["db"]
    graph.use_graph(graph_name, db)

    if "step" in data.keys():
        step = data["step"]
    else:
        step = 1

    if "direction" in data.keys():
        direction = data["direction"]
    else:
        direction = "forward"

    if "start_vertex_list" in data.keys():
        start_vertex_list = data["start_vertex_list"]
    else:
        start_vertex_list = ['10.73.28.115', '10.78.55.20']

    if "edge_name" in data.keys():
        edge_name = data["edge_name"]
    else:
        edge_name = "tcpflow"

    if "edge_con_list" in data.keys():
        edge_con_list = data["edge_con_list"]
    else:
        edge_con_list = ["protocol='http'"]

    res_list2 = graph.multi_hop_common_vertexes(step,
                                                start_vertex_list,
                                                direction,
                                                edge_name,
                                                edge_con_list)

    # result = dict()
    # result["result"] = res_list2

    return res_list2


def model_service_graph_search_match_edge(data, config_params):
    '''

    :param data:
     {
    "edge_name":
        "tcpflow",
    "edge_con_list":["downlink_length>100000000"],
    "target_field_list" :["record_time", "downlink_length"]
}
    :param config_params:
    :return:
    '''

    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "cyber"

    # client = Client('10.217.62.41')
    # graph = CHGraph(client)
    graph = config_params["graph"]

    # graph_dir = "./config/tcpflow_flow.cfg.json"

    # graph = CHGraph(graph_dir, client)

    db = config_params["db"]
    graph.use_graph(graph_name, db)

    if "edge_name" in data.keys():
        edge_name = data["edge_name"]
    else:
        edge_name = "tcpflow"

    if "edge_con_list" in data.keys():
        edge_con_list = data["edge_con_list"]
    else:
        edge_con_list = None

    if "target_field_list" in data.keys():
        target_field_list = data["target_field_list"]
    else:
        target_field_list = ['record_time', 'downlink_length']

    res_list2 = graph.match_edge(edge_name, edge_con_list, target_field_list)

    # result = dict()
    # result["result"] = res_list2

    return res_list2


def model_service_graph_search_match_vertex(data, config_params):
    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "cyber"

    # client = Client('10.217.62.41')
    # graph = CHGraph(client)

    graph = config_params["graph"]

    # graph_dir = "./config/tcpflow_flow.cfg.json"

    # graph = CHGraph(graph_dir, client)

    db = config_params["db"]
    graph.use_graph(graph_name, db)

    if "vertex_name" in data.keys():
        vertex_name = data["vertex_name"]
    else:
        vertex_name = 'tcp'

    if "vertex_con_list" in data.keys():
        vertex_con_list = data["vertex_con_list"]
    else:
        vertex_con_list = ["downlink_length>100000000"]

    if "target_field_list" in data.keys():
        target_field_list = data["target_field_list"]
    else:
        target_field_list = ['record_time']

    res_list2 = graph.match_vertex(vertex_name, vertex_con_list, target_field_list)

    return res_list2


def model_service_graph_search_multi_hop_multi_edge_common_vertexes(data, config_params):
    '''

    :param data:
    {
       "step":2,
       "start_vertex_list":[
           "10.73.28.115",
           "10.78.55.20"
           ],
       "edge_name_list":
           ["tcpflow", "flow"],
       "edge_con_list":[["downlink_length>10000", "protocol='http'"], ["record_date='2019-04-15'"]]
   }
    :param config_params:
    :return:
    '''

    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "cyber"

    # client = Client('10.217.62.41')
    # graph = CHGraph(client)
    graph = config_params["graph"]
    db = config_params["db"]
    graph.use_graph(graph_name, db)

    if "start_vertex_list" in data.keys():
        start_vertex_list = data["start_vertex_list"]
    else:
        start_vertex_list = ['10.73.28.115', '10.78.55.20']

    if "step" in data.keys():
        step = data["step"]
    else:
        step = 1

    if "edge_name_list" in data.keys():
        edge_name_list = data["edge_name_list"]
    else:
        edge_name_list = ["tcpflow", "flow"]

    if "direction" in data.keys():
        direction = data["direction"]
    else:
        direction = "forward"

    if "edge_con_list_list" in data.keys():
        edge_con_list_list = data["edge_con_list_list"]
    else:
        edge_con_list_list = [["downlink_length>10000", "protocol='http'"], ["record_date='2019-04-15'"]]

    res_list2 = graph.multi_hop_multi_edge_common_vertexes(step,
                                                           start_vertex_list,
                                                           direction,
                                                           edge_name_list,
                                                           edge_con_list_list,
                                                           )

    return res_list2


def model_service_graph_search_find_path(data, config_params):
    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "cyber"

    # client = Client('10.217.62.41')
    # graph = CHGraph(client)
    graph = config_params["graph"]
    db = config_params["db"]
    graph.use_graph(graph_name, db)

    if "start_vertex" in data.keys():
        start_vertex = data["start_vertex"]
    else:
        start_vertex = "10.73.28.115"

    if "end_vertex" in data.keys():
        end_vertex = data["end_vertex"]
    else:
        end_vertex = "10.78.55.20"

    if "edge_name_list" in data.keys():
        edge_name_list = data["edge_name_list"]
    else:
        edge_name_list = ["tcpflow", "flow"]

    if "edge_con_list_list" in data.keys():
        edge_con_list_list = data["edge_con_list_list"]
    else:
        edge_con_list_list = [["downlink_length>10000", "protocol='http'"], ["record_date='2019-04-15'"]]

    if "target_field_list" in data.keys():
        target_field_list = data["target_field_list"]
    else:
        target_field_list = ["record_time", "downlink_length"]

    if "step_limit" in data.keys():
        step_limit = data["step_limit"]
    else:
        step_limit = 2

    res_list2 = graph.find_path_multi_edge(start_vertex, end_vertex, edge_name_list, edge_con_list_list,
                                           target_field_list, step_limit)

    # print("res_list2")
    # print(res_list2)

    # result = dict()

    # result["result"] = res_list2

    return res_list2


def model_service_register_graph(data, config_params):
    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "cyber"

    if "graph_cfg" in data.keys():
        graph_cfg = data["graph_cfg"]
        if not is_json(graph_cfg):
            return "schema is not json string"

    graph = config_params["graph"]
    res = graph.register_graph(graph_name, graph_cfg)

    return res


def model_service_delete_graph(data, config_params):
    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "cyber"

    # client = Client('10.217.62.41')
    # graph = CHGraph(client)
    graph = config_params["graph"]

    res = graph.delete_graph(graph_name)

    return res


def model_service_show_graph(config_params):
    # client = Client('10.217.62.41')
    #
    # graph = CHGraph(client)
    graph = config_params["graph"]

    res = graph.show_graph()

    return list(res["graph_name"])


'''
def model_service_summary_graph(data, config_params):

    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "cyber"

    graph = config_params["graph"]

    res = graph.summary_graph(graph_name)

    return res
'''


def model_service_summary_graph(graph_name, config_params):
    pass
    # client = Client('10.217.62.41')
    #
    # graph = CHGraph(client)
    #
    # res = graph.summary_graph(graph_name)
    #
    # if res != None:
    #     return {"edge": res[0], "vertex": res[1]}
    # else:
    #     return "graph name [" + graph_name + "] does not exist"


def model_service_description_graph(graph_name, config_params):
    # client = Client('10.217.62.41')
    # graph = CHGraph(client)
    graph = config_params["graph"]

    res = graph.describe_graph(graph_name)

    return res


def model_service_insert_edge(data, config_params):
    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "cyber_plus"

    # client = Client('10.217.62.41')
    # graph = CHGraph(client)
    graph = config_params["graph"]

    if "edge_name" in data.keys():
        edge_name = data["edge_name"]
    else:
        edge_name = "tcpflow"

    if "edge_schema" in data.keys():
        edge_schema = data["edge_schema"]
    else:
        edge_schema = ["record_time", "record_date", "source_ip", "destination_ip", "protocol", "destination_port",
                       "uplink_length", "downlink_length"]

    if "edge_data" in data.keys():
        edge_data = data["edge_data"]
        for i, item_edge in enumerate(edge_data):
            edge_data[i] = tuple(item_edge)
    else:
        edge_data = [("2019-04-11 18:48:59", "2019-04-11", "10.66.18.32", "184.173.90.200", "http", "80", 14725, 3116)]

    db = config_params["db"]
    graph.use_graph(graph_name, db)
    res = graph.insert_edge(edge_name, edge_schema, edge_data)

    return res


def model_service_insert_vertex(data, config_params):
    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "cyber_plus"

    # client = Client('10.217.62.41')
    # graph = CHGraph(client)
    graph = config_params["graph"]

    if "vertex_name" in data.keys():
        vertex_name = data["vertex_name"]
    else:
        vertex_name = "ip"

    if "vertex_schema" in data.keys():
        vertex_schema = data["vertex_schema"]
    else:
        vertex_schema = ["service_date", "ip", "host", "speed"]

    if "vertex_data" in data.keys():
        vertex_data = data["vertex_data"]
        for i, item_vertex in enumerate(vertex_data):
            vertex_data[i] = tuple(item_vertex)
    else:
        vertex_data = [("2021-01 04", "1.1.1.1", "p47708v.hulk.shbt.qihoo.net", "2"),
                       ("2021-01-05", "1.1.1.2", "p47709v.hulk.shbt.qihoo.net", "3")]

    db = config_params["db"]
    graph.use_graph(graph_name, db)
    res = graph.insert_vertex(vertex_name, vertex_schema, vertex_data)

    return res


def model_service_path_finding(data, config_params):
    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "cyber_plus"

    # client = Client('10.217.62.41')
    #
    # graph = CHGraph(client)
    graph = config_params["graph"]

    if "start_vertex_list" in data.keys():
        start_vertex_list = data["start_vertex_list"]
    else:
        start_vertex_list = []

    if "end_vertex_list" in data.keys():
        end_vertex_list = data["end_vertex_list"]
    else:
        end_vertex_list = ['115.102.0.56']

    if "edge_name_list" in data.keys():
        edge_name_list = data["edge_name_list"]
    else:
        edge_name_list = ["service_date", "ip", "host", "speed"]

    if "edge_con_list_list" in data.keys():
        edge_con_list_list = data["edge_con_list_list"]
    else:
        edge_con_list_list = []

    if "target_field_list" in data.keys():
        target_field_list = data["target_field_list"]
    else:
        target_field_list = ['record_time']

    if "step_limit" in data.keys():
        step_limit = data["step_limit"]
    else:
        step_limit = 1

    db = config_params["db"]
    graph.use_graph(graph_name, db)

    res = graph.find_path_multi_edge(start_vertex_list, end_vertex_list, edge_name_list, edge_con_list_list,
                                     target_field_list, step_limit)

    print("res3")
    print(res)

    # try:
    #    res = graph.find_path_multi_edge(start_vertex_list, end_vertex_list, edge_name_list, edge_con_list_list, target_field_list, step_limit)
    # except Exception as e:
    #    print(e)
    #    return "Find path multi edge failed."

    result = {}

    if step_limit == 1:
        result["hop_" + str(1)] = {}
        for j in range(len(edge_name_list)):
            result["hop_" + str(1)][edge_name_list[j]] = res[0][j].values.tolist()
    elif step_limit >= 2:
        for i in range(1, step_limit + 1):
            result["s_" + str(i)] = {}
            if i == 1:
                result["s_" + str(i)] = {}
                for j in range(len(edge_name_list)):
                    result["s_" + str(i)][edge_name_list[j]] = res[i - 1][j].values.tolist()
            else:
                result["s_" + str(i)] = {}
                for h in range(step_limit):
                    result["s_" + str(i)]["hop_" + str(h + 1)] = {}
                    for j in range(len(edge_name_list)):
                        if h < len(res[i - 1]):
                            result["s_" + str(i)]["hop_" + str(h + 1)][edge_name_list[j]] = res[i - 1][h][
                                j].values.tolist()
                            result["s_" + str(i)]["hop_" + str(h + 1)][edge_name_list[j]] = res[i - 1][h][
                                j].values.tolist()
                        else:
                            result["s_" + str(i)]["hop_" + str(h + 1)][edge_name_list[j]] = []
                            result["s_" + str(i)]["hop_" + str(h + 1)][edge_name_list[j]] = []

    return result


def model_service_create_subgraph(data, config_params):
    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "taobao"

    if "subgraph_name" in data.keys():
        subgraph_name = data["subgraph_name"]
    else:
        subgraph_name = "taobao_sub"

    # client = Client('10.217.62.41')
    #
    # graph = CHGraph(client)
    graph = config_params["graph"]

    db = config_params["db"]
    graph.use_graph(graph_name, db)

    try:
        cluster_info = config_params.get("cluster", {})
        status = graph.create_subgraph(subgraph_name, cluster_info.get("is_cluster"), cluster_info.get("cluster_name"))
        return status
    except Exception:
        return "subgraph create failed"


def model_service_update_subgraph_by_multi_hop_multi_edge(data, config_params):
    subgraph_name = data.get("subgraph_name")
    edge_name_list = data.get("edge_name_list")
    node_name_list = data.get("node_name_list")
    direction = data.get("direction") or "forward"
    edge_con_list_list = data.get("edge_con_list_list") or [[]]
    step = data.get("step") or 1
    start_vertex_list = data.get("start_vertex_list") or ['10.73.28.115', '10.78.55.20']
    if not node_name_list or not edge_name_list or not subgraph_name:
        return

    db = config_params["db"]
    clickhouse_connect = config_params["clickhouse_connect"]
    graph_client = get_client(clickhouse_connect)
    graph = CHGraph(graph_client)

    try:
        name2config = db.get_name2config(subgraph_name)
        main_graph = name2config[0][5]
        graph_schema = name2config[0][3]
        schema = json.loads(graph_schema)
        graph.use_graph(main_graph, db)

        res = graph.update_subgraph_by_multi_hop_multi_edge(
            main_graph,
            db,
            subgraph_name,
            step,
            start_vertex_list,
            direction,
            edge_name_list,
            edge_con_list_list
        )
        graphEdges = []
        for h in range(step):
            for j in range(len(edge_name_list)):
                res_tem = res[h][j].values.tolist()
                if len(graphEdges) == len(edge_name_list):
                    graph_edge = graphEdges[j]
                    graph_edge["data"]["detail"] = graph_edge["data"]["detail"] + res_tem
                else:
                    graph_edge = {"data": {"detail": res_tem}}

                graph_edge["type"] = edge_name_list[j]
                schema_tem = res[h][j].columns.values.tolist()
                graph_edge["data"]["schema"] = schema_tem
                if len(graphEdges) < len(edge_name_list):
                    graphEdges.append(graph_edge)
        field_list = schema["vertexes"][node_name_list[0]]["fields"]
        result = model_get_vertex_by_edge(config_params, main_graph, subgraph_name, graphEdges, node_name_list,
                                          field_list)
        return result
    except Exception as e:
        traceback.print_exc()
        print(e)
        logger.error(e)
        return "update subgraph by multi hop multi edge failed"


def model_get_vertex_by_edge(config_params, graph_name, subgraph_name, graphEdges, node_name_list, field_list=None):
    node_tem = []
    for edge_one in range(len(graphEdges)):
        if graphEdges[edge_one]["data"]["detail"]:
            node_one = np.array(graphEdges[edge_one]["data"]["detail"])[:, 0:2].flatten().tolist()
            node_tem += node_one
    if node_tem:
        node_data = {"subGraph": graph_name, "nodeTypes": node_name_list}
        conditions = []
        if node_name_list:
            for l in range(len(node_name_list)):
                condition = {"type": node_name_list[l], "id": node_tem}
                conditions.append(condition)
            node_data["nodeConditions"] = conditions
        node_data["resultType"] = "def"
        if field_list:
            node_data["fieldList"] = field_list
        model_service = mds.ModelService()
        result = model_service.search_subgraph_by_condition(node_data, config_params)
        graphNodes = result["pathList"]["graphNodes"]
        new_graphNodes = convert_def_node(graphNodes)

        result["pathList"]["graphNodes"] = new_graphNodes
        result["pathList"]["graphEdges"] = graphEdges
    else:
        result = {"pathList": {"graphEdges": graphEdges, "graphNodes": node_tem}}

    return result


def convert_def_node(graphNodes):
    new_graphNodes = []
    for graphNode in graphNodes:
        defdata = graphNode["data"]
        schema = defdata.iloc[:, :].columns.values.tolist()
        field_data = defdata.iloc[:, :].values.tolist()
        new_data = {"schema": schema, "detail": field_data}
        new_graphNode = {"data": new_data, "type": graphNode["type"]}
        new_graphNodes.append(new_graphNode)
    return new_graphNodes


def model_service_update_subgraph_by_match_edge(data, config_params):
    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "taobao"

    if "subgraph_name" in data.keys():
        subgraph_name = data["subgraph_name"]
    else:
        subgraph_name = "taobao_sub"

    if "edge_name" in data.keys():
        edge_name = data["edge_name"]
    else:
        edge_name = "user_adgroup"

    if "edge_con_list" in data.keys():
        edge_con_list = data["edge_con_list"]
    else:
        edge_con_list = [
            "record_date='2017-05-12'",
            "record_time>'2017-05-12 23:30:00'",
            "pid='430548_1007'"]

    # client = Client('10.217.62.41')
    #
    # graph = CHGraph(client)
    graph = config_params["graph"]
    db = config_params["db"]
    graph.use_graph(graph_name, db)

    try:
        status = graph.update_subgraph_by_match_edge(subgraph_name, edge_name, edge_con_list)
        return status
    except Exception as e:
        print(e)
        return "update subgraph by match edge failed"


def model_service_update_subgraph_by_find_path_multi_edge(data, config_params):
    graph_name = data.get("graph_name")

    if "subgraph_name" in data.keys():
        subgraph_name = data.get("subgraph_name")
    else:
        subgraph_name = graph_name + "_sub"

    db = config_params["db"]
    clickhouse_connect = config_params["clickhouse_connect"]
    graph_client = get_client(clickhouse_connect)
    graph = CHGraph(graph_client)

    start_vertex_list = data.get("start_vertex_list")
    end_vertex_list = data.get("end_vertex_list")
    edge_name_list = data.get("edge_name_list")
    node_name_list = data.get("node_name_list") or []
    if not start_vertex_list or not end_vertex_list or not edge_name_list:
        return

    edge_con_list_list = data.get("edge_con_list_list") or [[]]
    step_limit = data.get("step_limit") or 1

    try:
        name2config = db.get_name2config(subgraph_name)
        main_graph_name = name2config[0][5]
        graph_schema = name2config[0][3]
        schema = json.loads(graph_schema)
        graph.use_graph(main_graph_name, db)

        res = graph.update_subgraph_by_find_path_multi_edge(db,
                                                            main_graph_name,
                                                            subgraph_name,
                                                            start_vertex_list,
                                                            end_vertex_list,
                                                            edge_name_list,
                                                            edge_con_list_list,
                                                            step_limit)
        graphEdges = []
        if step_limit == 1:
            for j in range(len(edge_name_list)):
                graph_edge = {"data": {}}
                res_tem = res[0][j].values.tolist()
                schema_tem = res[0][j].columns.values.tolist()
                graph_edge["type"] = edge_name_list[j]
                graph_edge["data"]["schema"] = schema_tem
                graph_edge["data"]["detail"] = res_tem
                graphEdges.append(graph_edge)
        elif step_limit >= 2:
            for i in range(1, step_limit + 1):
                if i == 1:
                    for j in range(len(edge_name_list)):
                        graph_edge = {"data": {}}
                        res_tem = res[i - 1][j].values.tolist()
                        schema_tem = res[i - 1][j].columns.values.tolist()
                        graph_edge["type"] = edge_name_list[j]
                        graph_edge["data"]["schema"] = schema_tem
                        graph_edge["data"]["detail"] = res_tem
                        graphEdges.append(graph_edge)
                else:
                    for h in range(step_limit):
                        for j in range(len(edge_name_list)):
                            if h < len(res[i - 1]):
                                graph_edge = graphEdges[j]
                                res_tem = res[i - 1][h][j].values.tolist()
                                schema_tem = res[i - 1][h][j].columns.values.tolist()
                                graph_edge["type"] = edge_name_list[j]
                                if schema_tem:
                                    graph_edge["data"]["schema"] = schema_tem
                                graph_edge["data"]["detail"] = graph_edge["data"]["detail"] + res_tem
                            else:
                                continue

        field_list = schema["vertexes"][node_name_list[0]]["fields"]
        result = model_get_vertex_by_edge(config_params, main_graph_name, subgraph_name, graphEdges, node_name_list,
                                          field_list)
    except Exception as e:
        print(e)
        print(e.args)
        traceback.print_exc()
        logger.error(e)
        return "subgraph by find path multi edge failed"
    return result


def model_service_destroy_subgraph(data, config_params):
    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "cyber"

    if "subgraph_name" in data.keys():
        subgraph_name = data["subgraph_name"]
    else:
        subgraph_name = "taobao_sub"

    # client = Client('10.217.62.41')
    #
    # graph = CHGraph(client)
    graph = config_params["graph"]
    db = config_params["db"]
    graph.use_graph(graph_name, db)

    try:
        status = graph.destroy_subgraph(subgraph_name)
        return status
    except Exception:
        return "destroy subgraph failed"


def model_service_metric_indegree(data, config_params):
    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "taobao"

    if "edge_name" in data.keys():
        edge_name = data["edge_name"]
    else:
        edge_name = "user_adgroup"

    if "if_sort" in data.keys():
        if_sort = data["if_sort"]
    else:
        if_sort = False

    if "topk" in data.keys():
        topk = data["topk"]
    else:
        topk = False

    # client = Client('10.217.62.41')
    #
    # graph = CHGraph(client)
    graph = config_params["graph"]
    db = config_params["db"]
    graph.use_graph(graph_name, db)

    try:
        status = graph.metric_indegree(edge_name, if_sort, topk)
        return status
    except Exception:
        return "metric indegree compute failed"


def model_service_metric_outdegree(data, config_params):
    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "taobao"

    if "edge_name" in data.keys():
        edge_name = data["edge_name"]
    else:
        edge_name = "user_adgroup"

    if "if_sort" in data.keys():
        if_sort = data["if_sort"]
    else:
        if_sort = False

    if "topk" in data.keys():
        topk = data["topk"]
    else:
        topk = False

    # client = Client('10.217.62.41')
    #
    # graph = CHGraph(client)
    graph = config_params["graph"]
    db = config_params["db"]
    graph.use_graph(graph_name, db)

    try:
        status = graph.metric_outdegree(edge_name, if_sort, topk)
        return status
    except Exception:
        return "metric outdegree compute failed"


def model_service_metric_degree(data, config_params):
    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "taobao"

    if "edge_name" in data.keys():
        edge_name = data["edge_name"]
    else:
        edge_name = "user_adgroup"

    if "if_sort" in data.keys():
        if_sort = data["if_sort"]
    else:
        if_sort = False

    if "topk" in data.keys():
        topk = data["topk"]
    else:
        topk = False

    # client = Client('10.217.62.41')
    #
    # graph = CHGraph(client)
    graph = config_params["graph"]
    db = config_params["db"]
    graph.use_graph(graph_name, db)

    try:
        status = graph.metric_degree(edge_name, if_sort, topk)
        return status
    except Exception:
        return "metric degree compute failed"


def model_service_metric_pagerank(data, config_params):
    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "taobao"

    if "edge_name" in data.keys():
        edge_name = data["edge_name"]
    else:
        edge_name = "user_adgroup"

    if "if_sort" in data.keys():
        if_sort = data["if_sort"]
    else:
        if_sort = False

    if "num_iter" in data.keys():
        num_iter = data["num_iter"]
    else:
        num_iter = 10

    if "topk" in data.keys():
        topk = data["topk"]
    else:
        topk = -1

    if "d" in data.keys():
        d = data["d"]
    else:
        d = 0.85

    # client = Client('10.217.62.41')
    #
    # graph = CHGraph(client)
    graph = config_params["graph"]
    db = config_params["db"]
    graph.use_graph(graph_name, db)

    try:
        status = graph.metric_pagerank(edge_name, d, num_iter, if_sort, topk)
        return status
    except Exception as e:
        print(e)
        return "metric pagerank compute failed"


def model_service_vertex_match_property(data, config_params):
    graph_name = data.get("graph_name")
    if not graph_name:
        return "graph_name shouldn't be null"

    vertex_id_list = data.get("vertex_id_list")
    if not vertex_id_list:
        return "vertex_id_list shouldn't be null"

    vertex_name = data.get("vertex_name")
    if not vertex_name:
        return "vertex_name shouldn't be null"

    vertex_con_list = data.get("vertex_con_list")
    target_field_list = data.get("target_field_list")
    page = data.get("page")
    page_size = data.get("page_size")

    graph = config_params["graph"]
    db = config_params["db"]
    graph.use_graph(graph_name, db)

    try:
        vertex_property = graph.vertex_match_property(vertex_id_list,
                                                      vertex_name,
                                                      vertex_con_list,
                                                      target_field_list,
                                                      page,
                                                      page_size,
                                                      )
        return vertex_property
    except Exception as e:
        logger.error("model_service_vertex_match_property error: {}".format(str(e)))
        return "vertex match property failed"


def model_service_edge_match_property(data, config_params):
    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        return "graph_name shouldn't be null"

    if "start_vertex_list" in data.keys():
        start_vertex_list = data["start_vertex_list"]
    else:
        return "start_vertex_list shouldn't be null"

    if "end_vertex_list" in data.keys():
        end_vertex_list = data["end_vertex_list"]
    else:
        return "end_vertex_list shouldn't be null"

    if "edge_name" in data.keys():
        edge_name = data["edge_name"]
    else:
        return "edge_name shouldn't be null"

    if "edge_con_list" in data.keys():
        edge_con_list = data["edge_con_list"]
    else:
        edge_con_list = None

    if "target_field_list" in data.keys():
        target_field_list = data["target_field_list"]
    else:
        target_field_list = None
    if "page" in data.keys():
        page = data["page"]
    else:
        page = None
    if "page_size" in data.keys():
        page_size = data["page_size"]
    else:
        page_size = None
    # client = Client('10.217.62.41')
    #
    # graph = CHGraph(client)
    graph = config_params["graph"]
    db = config_params["db"]
    graph.use_graph(graph_name, db)

    try:
        edge_property = graph.edge_match_property(
            start_vertex_list,
            end_vertex_list,
            edge_name,
            edge_con_list,
            target_field_list,
            page,
            page_size
        )
        return edge_property
    except Exception as e:
        print(e)
        return "edge match property failed"


def model_service_query_vertexes(data, config_params):
    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "anti_money_launder"

    if "vertex_name" in data.keys():
        vertex_name = data["vertex_name"]
    else:
        vertex_name = "account"

    if "vertex_con_list" in data.keys():
        vertex_con_list = data["vertex_con_list"]
    else:
        vertex_con_list = None

    if "target_field_list" in data.keys():
        target_field_list = data["target_field_list"]
    else:
        target_field_list = None

    # client = Client('10.217.62.41')
    #
    # graph = CHGraph(client)
    graph = config_params["graph"]
    db = config_params["db"]
    graph.use_graph(graph_name, db)

    try:
        vertex_query = graph.query_vertexes(
            vertex_name,
            vertex_con_list,
            target_field_list,
        )
        return vertex_query
    except Exception as e:
        print(e)
        return "vertex query failed"


def model_service_query_edges(data, config_params):
    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "anti_money_launder"

    if "edge_name" in data.keys():
        edge_name = data["edge_name"]
    else:
        edge_name = "transactions"

    if "edge_con_list" in data.keys():
        edge_con_list = data["edge_con_list"]
    else:
        edge_con_list = None

    if "target_field_list" in data.keys():
        target_field_list = data["target_field_list"]
    else:
        target_field_list = None

    # client = Client('10.217.62.41')
    #
    # graph = CHGraph(client)
    graph = config_params["graph"]
    db = config_params["db"]
    graph.use_graph(graph_name, db)

    try:
        edges_result = graph.query_edges(
            edge_name,
            edge_con_list,
            target_field_list,
        )
        return edges_result
    except Exception as e:
        print(e)
        return "edge query failed"


def model_service_time_static_subgraph(data, config_params):
    if "graph_name" in data.keys():
        graph_name = data["graph_name"]
    else:
        graph_name = "anti_money_launder"

    if "time_field" in data.keys():
        time_field = data["time_field"]
    else:
        time_field = "record_date"

    if "edge_name" in data.keys():
        edge_name = data["edge_name"]
    else:
        edge_name = "transactions"

    if "edge_con_list" in data.keys():
        edge_con_list = data["edge_con_list"]
    else:
        edge_con_list = ["record_date < '2017-05-11'"]

    if "time_dimention" in data.keys():
        time_dimention = data["time_dimention"]
    else:
        time_dimention = "Day"

    # client = Client('10.217.62.41')
    #
    # graph = CHGraph(client)
    graph = config_params["graph"]
    db = config_params["db"]
    graph.use_graph(graph_name, db)

    try:
        time_static_result = graph.count_edge_by_time(
            edge_name,
            edge_con_list,
            time_field,
            time_dimention
        )
        return time_static_result
    except Exception as e:
        print(e)
        return "subgraph time static failed"
