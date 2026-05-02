from __future__ import print_function

import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)
sys.path.append(rootPath[0])
sys.path.append(rootPath[0] + "/" + rootPath[1])

print(sys.path)

import tornado.ioloop
import tornado.web

from tornado_swagger.model import register_swagger_model

from config.logger_design import get_logger
from config.data_load_config import load_config
from services.model import model_service_graph_search_one_hop, \
    model_service_graph_search_multi_hop, \
    model_service_graph_search_multi_hop_multi_edge, \
    model_service_graph_search_one_hop_multi_edge, \
    model_service_graph_search_multi_hop_common_vertexes, \
    model_service_graph_search_match_edge, \
    model_service_graph_search_match_vertex, \
    model_service_graph_search_multi_hop_multi_edge_common_vertexes, \
    model_service_graph_search_find_path, \
    model_service_register_graph, \
    model_service_delete_graph, \
    model_service_show_graph, \
    model_service_insert_edge, \
    model_service_insert_vertex, \
    model_service_summary_graph, \
    model_service_description_graph, \
    model_service_path_finding, \
    model_service_create_subgraph, \
    model_service_update_subgraph_by_multi_hop_multi_edge, \
    model_service_update_subgraph_by_match_edge, \
    model_service_update_subgraph_by_find_path_multi_edge, \
    model_service_destroy_subgraph, \
    model_service_metric_indegree, \
    model_service_metric_outdegree, \
    model_service_metric_degree, \
    model_service_metric_pagerank, \
    model_service_edge_match_property, \
    model_service_vertex_match_property, \
    model_service_query_edges, \
    model_service_query_vertexes, \
    model_service_time_static_subgraph, \
    model_service_graph, \
    model_service_graph_insert, \
    model_service_graph_delete, \
    model_service_graph_update, \
    model_service_ga_build

from controllers.graph import GetInfoData,\
    GetHealthData, GaBuildHandler, GraphHandler, GraphInsertHandler,\
    GraphDeleteHandler, GraphUpdateHandler, GraphSearchMatchEdgeHandler,\
    GraphSearchMultiHopMultiEdgeCommonVertexesHandler, GraphSearchOneHopMultiEdgeHandler,\
    GraphSearchMatchVertexHandler, GraphSearchMultiHopMultiEdgeHandler,\
    RegisterGraphHandler,\
    DeleteGraphHandler, ShowGraphHandler, SummaryGraphHandler, DescriptionGraphHandler,\
    InsertEdgeHandler, InsertVertexHandler, HealthServiceHandler, InfoServiceHandler,\
    FindPathHandler, SubgraphCreationHandler, MultiHopSubgraphUpdateHandler,\
    PathSubgraphUpdateHandler, EdgeSubgraphUpdateHandler, SubgraphDestroyHandler,\
    MetricDegreeHandler, MetricIndegreeHandler, MetricPagerankHandler,\
    MetricOutdegreeHandler, VertexQueryHandler, VertexMatchPropertyHandler,\
    EdgeQueryHandler, EdgeMatchPropertyHandler, TimeStaticSubgraphHandler,\
    GainSubgraph, GainSubgraphQuery, GainTimeLineCount, GainCountEdges,\
    GainGraphTypeSet, GainGraphTypeFunction, GainGraphTypeCount, GainGraphTaskSelect, GainGraphTaskSubmit


logger = get_logger()


class DataServiceConfigLoad(object):
    def __init__(self):
        print("clickhouse config load start")

    def load_config(self):
        return load_config()


@register_swagger_model
class modelServiceMetricIndegree(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_metric_indegree(data, config_params)


@register_swagger_model
class model_serviceGABuild(object):
    def __init__(self):
        print("model_service_ga_build model start")

    def model_operation(self, data, config_params):
        return model_service_ga_build(data, config_params)

@register_swagger_model
class modelServiceGraph(object):
    def __init__(self):
        print("model_service_graph model start")

    def model_operation(self, data, config_params):
        return model_service_graph(data, config_params)


@register_swagger_model
class modelServiceGraphInsert(object):
    def __init__(self):
        print("model_service_graph_insert model start")

    def model_operation(self, data, config_params):
        return model_service_graph_insert(data, config_params)


@register_swagger_model
class modelServiceGraphDelete(object):
    def __init__(self):
        print("model_service_graph_delete model start")

    def model_operation(self, data, config_params):
        return model_service_graph_delete(data, config_params)

@register_swagger_model
class modelServiceGraphUpdate(object):
    def __init__(self):
        print("model_service_graph_update model start")

    def model_operation(self, data, config_params):
        return model_service_graph_update(data, config_params)


@register_swagger_model
class modelServiceGraphSearchOneHop(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_graph_search_one_hop(data, config_params)

@register_swagger_model
class modelServiceGraphSearchMultiHop(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_graph_search_multi_hop(data, config_params)

@register_swagger_model
class modelServiceGraphSearchMultiHopMultiEdge(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_graph_search_multi_hop_multi_edge(data, config_params)

@register_swagger_model
class modelServiceGraphSearchOneHopMultiEdge(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_graph_search_one_hop_multi_edge(data, config_params)

@register_swagger_model
class modelServiceGraphSearchMultiHopCommonVertexes(object):
    """
    # multi_hop_common_vertexes
    """
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_graph_search_multi_hop_common_vertexes(data, config_params)

# one pop multi edge
@register_swagger_model
class modelServiceGraphSearchMatchEdge(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_graph_search_match_edge(data, config_params)

# one pop multi edge
@register_swagger_model
class modelServiceGraphSearchMatchVertex(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_graph_search_match_vertex(data, config_params)

# one pop multi edge
@register_swagger_model
class modelServiceGraphSearchMultiHopMultiEdgeCommonVertexes(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_graph_search_multi_hop_multi_edge_common_vertexes(data, config_params)

# one pop multi edge
@register_swagger_model
class modelServiceGraphSearchMultiHopMultiEdgeCommonVertexes(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_graph_search_multi_hop_multi_edge_common_vertexes(data, config_params)

@register_swagger_model
class modelServiceGraphSearchFindPath(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_graph_search_find_path(data, config_params)

@register_swagger_model
class modelServiceRegisterGraph(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_register_graph(data, config_params)

@register_swagger_model
class modelServiceDeleteGraph(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_delete_graph(data, config_params)

@register_swagger_model
class modelServiceShowGraph(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_show_graph(config_params)

@register_swagger_model
class modelServiceInsertEdge(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_insert_edge(data, config_params)

@register_swagger_model
class modelServiceInsertVertex(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_insert_vertex(data, config_params)

@register_swagger_model
class modelServiceSummaryGraph(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_summary_graph(data, config_params)

@register_swagger_model
class modelServiceDescriptionGraph(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_description_graph(data, config_params)

@register_swagger_model
class modelServicePathFinding(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_path_finding(data, config_params)

@register_swagger_model
class modelServiceSubgraphCreation(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_create_subgraph(data, config_params)

@register_swagger_model
class modelServiceMultiHopSubgraphUpdate(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_update_subgraph_by_multi_hop_multi_edge(data, config_params)

@register_swagger_model
class modelServicePathSubgraphUpdate(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_update_subgraph_by_find_path_multi_edge(data, config_params)

@register_swagger_model
class modelServiceEdgeSubgraphUpdate(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_update_subgraph_by_match_edge(data, config_params)

@register_swagger_model
class modelServiceSubgraphDestroy(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_destroy_subgraph(data, config_params)

@register_swagger_model
class modelServiceMetricOutdegree(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_metric_outdegree(data, config_params)

@register_swagger_model
class modelServiceMetricDegree(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_metric_degree(data, config_params)

@register_swagger_model
class modelServiceMetricPagerank(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_metric_pagerank(data, config_params)

@register_swagger_model
class modelServiceEdgeMatchProperty(object):
    def __init__(self):
        print("query edge prop model start")

    def model_operation(self, data, config_params):
        return model_service_edge_match_property(data, config_params)

@register_swagger_model
class modelServiceVertexMatchProperty(object):
    def __init__(self):
        print("query vertex prop model start")

    def model_operation(self, data, config_params):
        return model_service_vertex_match_property(data, config_params)

@register_swagger_model
class modelServiceQueryEdge(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_query_edges(data, config_params)

@register_swagger_model
class modelServiceQueryVertex(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_query_vertexes(data, config_params)

@register_swagger_model
class modelServiceTimeStaticSubgraph(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_time_static_subgraph(data, config_params)


class Application(tornado.web.Application):
    data_service = DataServiceConfigLoad()

    config_params = data_service.load_config()

    model_serviceGABuild = model_serviceGABuild()

    model_serviceGraphInsert = modelServiceGraphInsert()

    model_serviceGraphDelete = modelServiceGraphDelete()

    model_serviceGraphUpdate = modelServiceGraphUpdate()

    model_serviceGraph = modelServiceGraph()

    model_serviceGraphSearchOnePop = modelServiceGraphSearchOneHop()

    model_serviceGraphSearchMultiHopMultiEdge = modelServiceGraphSearchMultiHopMultiEdge()

    model_serviceGraphSearchMultiHop = modelServiceGraphSearchMultiHop()

    model_serviceGraphSearchOneHopMultiEdge = modelServiceGraphSearchOneHopMultiEdge()

    model_serviceGraphSearchMultiHopCommonVertexes = modelServiceGraphSearchMultiHopCommonVertexes()

    model_serviceGraphSearchMatchEdge = modelServiceGraphSearchMatchEdge()

    model_serviceGraphSearchMatchVertex = modelServiceGraphSearchMatchVertex()

    model_serviceGraphSearchMultiHopMultiEdgeCommonVertexes = modelServiceGraphSearchMultiHopMultiEdgeCommonVertexes()

    model_serviceGraphSearchFindPath = modelServiceGraphSearchFindPath()

    model_serviceRegisterGraph = modelServiceRegisterGraph()

    model_serviceDeleteGraph = modelServiceDeleteGraph()

    model_serviceShowGraph = modelServiceShowGraph()

    model_serviceInsertEdge = modelServiceInsertEdge()

    model_serviceInsertVertex = modelServiceInsertVertex()

    model_serviceSummaryGraph = modelServiceSummaryGraph()

    model_serviceDescriptionGraph = modelServiceDescriptionGraph()

    model_serviceFindPath = modelServicePathFinding()

    model_serviceSubgraphCreation = modelServiceSubgraphCreation()

    model_serviceMultiHopSubgraphUpdate = modelServiceMultiHopSubgraphUpdate()

    model_servicePathSubgraphUpdate = modelServicePathSubgraphUpdate()

    model_serviceEdgeSubgraphUpdate = modelServiceEdgeSubgraphUpdate()

    model_serviceSubgraphDestroy = modelServiceSubgraphDestroy()

    model_serviceMetricIndegree = modelServiceMetricIndegree()

    model_serviceMetricOutdegree = modelServiceMetricOutdegree()

    model_serviceMetricDegree = modelServiceMetricDegree()

    model_serviceMetricPagerank = modelServiceMetricPagerank()

    model_serviceEdgeMatchProperty = modelServiceEdgeMatchProperty()

    model_serviceVertexMatchProperty = modelServiceVertexMatchProperty()

    model_serviceQueryEdge = modelServiceQueryEdge()

    model_serviceQueryVertex = modelServiceQueryVertex()

    model_serviceTimeStaticSubgraph = modelServiceTimeStaticSubgraph()

    _routes = [
        tornado.web.url(r"/chgraph/api/v1/info", GetInfoData),
        tornado.web.url(r"/chgraph/api/v1/health", GetHealthData),
        tornado.web.url(r"/graph-db/api/v1/ga-build", GaBuildHandler,
                        {"model_service": model_serviceGABuild, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/graph", GraphHandler,
                        {"model_service": model_serviceGraph, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/graph-insert", GraphInsertHandler,
                        {"model_service": model_serviceGraphInsert, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/graph-delete", GraphDeleteHandler,
                        {"model_service": model_serviceGraphDelete, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/graph-update", GraphUpdateHandler,
                        {"model_service": model_serviceGraphUpdate, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/multi-hop", GraphSearchMultiHopMultiEdgeHandler,
                        {"model_service": model_serviceGraphSearchMultiHopMultiEdge, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/one-hop", GraphSearchOneHopMultiEdgeHandler,
                        {"model_service": model_serviceGraphSearchOneHopMultiEdge, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/edges", GraphSearchMatchEdgeHandler,
                        {"model_service": model_serviceGraphSearchMatchEdge, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/vertices", GraphSearchMatchVertexHandler,
                        {"model_service": model_serviceGraphSearchMatchVertex, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/multi-hop-common-vertices",
                        GraphSearchMultiHopMultiEdgeCommonVertexesHandler,
                        {"model_service": model_serviceGraphSearchMultiHopMultiEdgeCommonVertexes,
                         "config_params": config_params}),
        # tornado.web.url(r"/graph-db/api/v1/paths", graphSearchFindPathHandler,{"model_service": model_serviceGraphSearchFindPath,"config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/graph-registration", RegisterGraphHandler,
                        {"model_service": model_serviceRegisterGraph, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/graph-deletion", DeleteGraphHandler,
                        {"model_service": model_serviceDeleteGraph, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/graph-show", ShowGraphHandler,
                        {"model_service": model_serviceShowGraph, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/graph-summary/(?P<graph_name>\S*)", SummaryGraphHandler,
                        {"model_service": model_serviceSummaryGraph, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/graph-description/(?P<graph_name>\S*)", DescriptionGraphHandler,
                        {"model_service": model_serviceDescriptionGraph, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/edge-insertion", InsertEdgeHandler,
                        {"model_service": model_serviceInsertEdge, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/vertex-insertion", InsertVertexHandler,
                        {"model_service": model_serviceInsertVertex, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/health", HealthServiceHandler),
        tornado.web.url(r"/graph-db/api/v1/info", InfoServiceHandler),
        tornado.web.url(r"/graph-db/api/v1/path", FindPathHandler,
                        {"model_service": model_serviceFindPath, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/subgraph-creation", SubgraphCreationHandler,
                        {"model_service": model_serviceSubgraphCreation, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/subgraph-update-multi-hop", MultiHopSubgraphUpdateHandler,
                        {"model_service": model_serviceMultiHopSubgraphUpdate, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/subgraph-update-path", PathSubgraphUpdateHandler,
                        {"model_service": model_servicePathSubgraphUpdate, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/subgraph-update-edge", EdgeSubgraphUpdateHandler,
                        {"model_service": model_serviceEdgeSubgraphUpdate, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/subgraph-destruction", SubgraphDestroyHandler,
                        {"model_service": model_serviceSubgraphDestroy, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/metric-indegree", MetricIndegreeHandler,
                        {"model_service": model_serviceMetricIndegree, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/metric-outdegree", MetricOutdegreeHandler,
                        {"model_service": model_serviceMetricOutdegree, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/metric-degree", MetricDegreeHandler,
                        {"model_service": model_serviceMetricDegree, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/metric-pagerank", MetricPagerankHandler,
                        {"model_service": model_serviceMetricPagerank, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/vertex-property", VertexMatchPropertyHandler,
                        {"model_service": model_serviceVertexMatchProperty, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/edge-property", EdgeMatchPropertyHandler,
                        {"model_service": model_serviceEdgeMatchProperty, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/vertex-query", VertexQueryHandler,
                        {"model_service": model_serviceQueryVertex, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/edge-query", EdgeQueryHandler,
                        {"model_service": model_serviceQueryEdge, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/subgraph-time-statistic", TimeStaticSubgraphHandler,
                        {"model_service": model_serviceTimeStaticSubgraph, "config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/subgraph-filtration-statistic", GainSubgraph,
                        {"config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/time-line-count", GainTimeLineCount,
                        {"config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/round-edges-count", GainCountEdges,
                        {"config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/subgraph-query", GainSubgraphQuery,
                        {"config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/subgraph-type-statistics", GainGraphTypeCount,
                        {"config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/subgraph-type-statistics-set", GainGraphTypeSet,
                        {"config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/subgraph-type-statistics-function", GainGraphTypeFunction,
                        {"config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/subgraph-calculation-select", GainGraphTaskSelect,
                        {"config_params": config_params}),
        tornado.web.url(r"/graph-db/api/v1/subgraph-calculation-submit", GainGraphTaskSubmit,
                        {"config_params": config_params}),
    ]

    def get_routes(self):
        return self._routes

    def __init__(self):
        settings = {"debug": True}
        # setup_swagger(self._routes,
        #               swagger_url='/doc',
        #               api_base_url='/',
        #               description='',
        #               api_version='1.0.0',
        #               title='Journal API',
        #               contact='name@domain',
        #               schemes=['https'],
        #               security_definitions={
        #                   'ApiKeyAuth': {
        #                       'type': 'apiKey',
        #                       'in': 'header',
        #                       'name': 'X-API-Key'
        #                   }
        #               })
        super(Application, self).__init__(self._routes, **settings)


def main():
    App = Application()
    App.get_routes()
    App.listen(10110)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
