import datetime

from config.logger_design import get_logger

logger = get_logger()


def get_graph_vertexes(graph_cfg, graph):
    vertexes = []
    i = 0
    for vertex, vertex_info in graph_cfg.get("vertexes").items():
        i += 1

        graph_node = {}
        selected_fields = []
        for key in ["id", "label"]:
            selected_fields.append(vertex_info.get(key))

        selected_fields.extend(vertex_info.get("fields") or [])
        start = datetime.datetime.now()
        try:
            vertex_query = graph.query_vertexes(vertex, [""], selected_fields, "df")
            end = datetime.datetime.now()
            logger.info("query_vertexes {} count_times: {}".format(i, round((end - start).total_seconds(), 5) * 1000))
        except Exception as e:
            raise Exception("vertex query failed: {}".format(str(e)))

        graph_node["type"] = vertex
        graph_node["data"] = vertex_query

        vertexes.append(graph_node)

    return vertexes


def get_graph_edges(graph_cfg, graph):
    edges = []
    i = 0
    for edge, edge_info in graph_cfg.get("edges").items():
        i += 1

        graph_edge = {}
        selected_fields = []
        for key in ["src", "dst", "rank"]:
            selected_fields.append(edge_info.get(key))
        selected_fields.extend(edge_info.get("fields") or [])
        start = datetime.datetime.now()
        try:
            edges_result = graph.query_edges(edge, [""], selected_fields, "df")
            end = datetime.datetime.now()
            logger.info("query_edge {} count_times: {}".format(i, round((end - start).total_seconds(), 5) * 1000))
        except Exception as e:
            raise Exception("edge query failed: {}".format(str(e)))

        graph_edge["type"] = edge
        graph_edge["data"] = edges_result
        graph_edge["id"] = edge

        edges.append(graph_edge)

    return edges
