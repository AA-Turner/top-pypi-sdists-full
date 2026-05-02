from __future__ import print_function
import ujson,json
import tornado.ioloop
import tornado.web

from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from services.model import model_service_graph_search_one_hop,\
    model_service_graph_search_multi_hop,\
    model_service_graph_search_multi_hop_multi_edge, \
    model_service_graph_search_one_hop_multi_edge,\
    model_service_graph_search_multi_hop_common_vertexes,\
    model_service_graph_search_match_edge,\
    model_service_graph_search_match_vertex,\
    model_service_graph_search_multi_hop_multi_edge_common_vertexes
import datetime
from config.data_load_config import load_config
from tornado_swagger.setup import setup_swagger
from tornado_swagger.model import register_swagger_model


class dataServiceConfigLoad(object):
    def __init__(self):
        print("clickhouse config load start")

    def load_config(self):
        return load_config()


class DateEncoder(json.JSONEncoder):  
    def default(self, obj):  
        if isinstance(obj, datetime.datetime):  
            return obj.strftime('%Y-%m-%d %H:%M:%S')  
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")  
        else:  
            return json.JSONEncoder.default(self, obj) 


# one pop

@register_swagger_model
class modelServiceGraphSearchOneHop(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_graph_search_one_hop(data, config_params)


class graphSearchOneHopHandler(tornado.web.RequestHandler):

    """
        Description end-point
        ---
        tags:
        - Example
        summary: Create user
    """

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        res = yield self.data_process_and_model()
        self.write(json.dumps(res, cls=DateEncoder))
        self.finish()

    @run_on_executor
    def data_process_and_model(self):
        data_json = ujson.loads(self.request.body)
        result_list = self.model.model_operation(data_json, self.config_params)
        result = {
            "result": result_list
        }
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return result


#multi pop
@register_swagger_model
class modelServiceGraphSearchMultiHop(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_graph_search_multi_hop(data, config_params)


class graphSearchMultiHopHandler(tornado.web.RequestHandler):


    """
        Description end-point
        ---
        tags:
        - Example
        summary: Create user
    """


    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        res = yield self.data_process_and_model()
        self.write(json.dumps(res, cls=DateEncoder))
        self.finish()

    @run_on_executor
    def data_process_and_model(self):
        data_json = ujson.loads(self.request.body)
        result_list = self.model.model_operation(data_json, self.config_params)
        result = {
            "result": result_list
        }
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return result


#multi pop multi edge

@register_swagger_model
class modelServiceGraphSearchMultiHopMultiEdge(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_graph_search_multi_hop_multi_edge(data, config_params)



class graphSearchMultiHopMultiEdgeHandler(tornado.web.RequestHandler):
    """
        Description end-point
        ---
        tags:
        - Example
        summary: Create user
    """

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        res = yield self.data_process_and_model()
        self.write(json.dumps(res, cls=DateEncoder))
        self.finish()

    @run_on_executor
    def data_process_and_model(self):
        data_json = ujson.loads(self.request.body)
        result_list = self.model.model_operation(data_json, self.config_params)
        result = {
            "result": result_list
        }
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return result


#one pop multi edge
@register_swagger_model
class modelServiceGraphSearchOneHopMultiEdge(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_graph_search_one_hop_multi_edge(data, config_params)


class graphSearchOneHopMultiEdgeHandler(tornado.web.RequestHandler):
    
    """
        Description end-point
        ---
        tags:
        - Example
        summary: Create user
    """

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        res = yield self.data_process_and_model()
        self.write(json.dumps(res, cls=DateEncoder))
        self.finish()

    @run_on_executor
    def data_process_and_model(self):
        data_json = ujson.loads(self.request.body)
        result_list = self.model.model_operation(data_json, self.config_params)
        result = {
            "result": result_list
        }
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return result


# multi_hop_common_vertexes

@register_swagger_model
class modelServiceGraphSearchMultiHopCommonVertexes(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_graph_search_multi_hop_common_vertexes(data, config_params)


class graphSearchMultiHopCommonVertexesHandler(tornado.web.RequestHandler):


    """
        Description end-point
        ---
        tags:
        - Example
        summary: Create user
    """
   

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        res = yield self.data_process_and_model()
        self.write(json.dumps(res, cls=DateEncoder))
        self.finish()

    @run_on_executor
    def data_process_and_model(self):
        data_json = ujson.loads(self.request.body)
        result_list = self.model.model_operation(data_json, self.config_params)
        result = {
            "result": result_list
        }
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return result


#one pop multi edge
@register_swagger_model
class modelServiceGraphSearchMatchEdge(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_graph_search_match_edge(data, config_params)


class graphSearchMatchEdgeHandler(tornado.web.RequestHandler):


    """
        Description end-point
        ---
        tags:
        - Example
        summary: Create user
    """


    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        res = yield self.data_process_and_model()
        self.write(json.dumps(res, cls=DateEncoder))
        self.finish()

    @run_on_executor
    def data_process_and_model(self):
        data_json = ujson.loads(self.request.body)
        result_list = self.model.model_operation(data_json, self.config_params)
        result = {
            "result": result_list
        }
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return result


#one pop multi edge

@register_swagger_model
class modelServiceGraphSearchMatchVertex(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_graph_search_match_vertex(data, config_params)

class graphSearchMatchVertexHandler(tornado.web.RequestHandler):


    """
        Description end-point
        ---
        tags:
        - Example
        summary: Create user
    """


    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        res = yield self.data_process_and_model()
        self.write(json.dumps(res, cls=DateEncoder))
        self.finish()

    @run_on_executor
    def data_process_and_model(self):
        data_json = ujson.loads(self.request.body)
        result_list = self.model.model_operation(data_json, self.config_params)
        result = {
            "result": result_list
        }
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return result


#one pop multi edge
@register_swagger_model
class modelServiceGraphSearchMultiHopMultiEdgeCommonVertexes(object):
    def __init__(self):
        print("clickhouse model start")

    def model_operation(self, data, config_params):
        return model_service_graph_search_multi_hop_multi_edge_common_vertexes(data, config_params)


class graphSearchMultiHopMultiEdgeCommonVertexesHandler(tornado.web.RequestHandler):

    """
        Description end-point
        ---
        tags:
        - Example
        summary: Create user
    """
    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        res = yield self.data_process_and_model()
        self.write(json.dumps(res, cls=DateEncoder))
        self.finish()

    @run_on_executor
    def data_process_and_model(self):
        data_json = ujson.loads(self.request.body)
        result_list = self.model.model_operation(data_json, self.config_params)
        result = {
            "result": result_list
        }
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return result

'''
def make_app():

    data_service = dataServiceConfigLoad()
    config_params = data_service.load_config()

    model_serviceGraphSearchOnePop = modelServiceGraphSearchOneHop()

    model_serviceGraphSearchMultiHopMultiEdge = modelServiceGraphSearchMultiHopMultiEdge()

    model_serviceGraphSearchMultiHop = modelServiceGraphSearchMultiHop()

    model_serviceGraphSearchOneHopMultiEdge = modelServiceGraphSearchOneHopMultiEdge()

    model_serviceGraphSearchMultiHopCommonVertexes = modelServiceGraphSearchMultiHopCommonVertexes()

    model_serviceGraphSearchMatchEdge = modelServiceGraphSearchMatchEdge()

    model_serviceGraphSearchMatchVertex = modelServiceGraphSearchMatchVertex()

    model_serviceGraphSearchMultiHopMultiEdgeCommonVertexes = modelServiceGraphSearchMultiHopMultiEdgeCommonVertexes()


    return tornado.web.Application([
        (r"/graphdb/api/v1/one_hop", graphSearchOneHopHandler, {"model_service": model_serviceGraphSearchOnePop, "config_params": config_params}),
        (r"/graphdb/api/v1/multi_hop_multi_edge", graphSearchMultiHopMultiEdgeHandler, {"model_service": model_serviceGraphSearchMultiHopMultiEdge, "config_params": config_params}),
        (r"/graphdb/api/v1/multi_hop", graphSearchMultiHopHandler, {"model_service": model_serviceGraphSearchMultiHop, "config_params": config_params}),
        (r"/graphdb/api/v1/one_hop_multi_edge", graphSearchOneHopMultiEdgeHandler, {"model_service": model_serviceGraphSearchOneHopMultiEdge, "config_params": config_params}),
        (r"/graphdb/api/v1/multi_hop_common_vertexes", graphSearchMultiHopCommonVertexesHandler,{"model_service": model_serviceGraphSearchMultiHopCommonVertexes, "config_params": config_params}),
        (r"/graphdb/api/v1/match_edge", graphSearchMatchEdgeHandler,{"model_service": model_serviceGraphSearchMatchEdge, "config_params": config_params}),
        (r"/graphdb/api/v1/match_vertex", graphSearchMatchVertexHandler,{"model_service": model_serviceGraphSearchMatchVertex, "config_params": config_params}),
        (r"/graphdb/api/v1/multi_hop_multi_edge_common_vertexes", graphSearchMultiHopMultiEdgeCommonVertexesHandler,{"model_service": model_serviceGraphSearchMultiHopMultiEdgeCommonVertexes, "config_params": config_params}),
    ], debug=True)
'''

class Application(tornado.web.Application):

    data_service = dataServiceConfigLoad()
    config_params = data_service.load_config()

    model_serviceGraphSearchOnePop = modelServiceGraphSearchOneHop()

    model_serviceGraphSearchMultiHopMultiEdge = modelServiceGraphSearchMultiHopMultiEdge()

    model_serviceGraphSearchMultiHop = modelServiceGraphSearchMultiHop()

    model_serviceGraphSearchOneHopMultiEdge = modelServiceGraphSearchOneHopMultiEdge()

    model_serviceGraphSearchMultiHopCommonVertexes = modelServiceGraphSearchMultiHopCommonVertexes()

    model_serviceGraphSearchMatchEdge = modelServiceGraphSearchMatchEdge()

    model_serviceGraphSearchMatchVertex = modelServiceGraphSearchMatchVertex()

    model_serviceGraphSearchMultiHopMultiEdgeCommonVertexes = modelServiceGraphSearchMultiHopMultiEdgeCommonVertexes()

    _routes = [
        tornado.web.url(r"/graphdb/api/v1/one_hop", graphSearchOneHopHandler, {"model_service": model_serviceGraphSearchOnePop, "config_params": config_params}),
        tornado.web.url(r"/graphdb/api/v1/multi_hop_multi_edge", graphSearchMultiHopMultiEdgeHandler, {"model_service": model_serviceGraphSearchMultiHopMultiEdge, "config_params": config_params}),
        tornado.web.url(r"/graphdb/api/v1/multi_hop", graphSearchMultiHopHandler, {"model_service": model_serviceGraphSearchMultiHop, "config_params": config_params}),
        tornado.web.url(r"/graphdb/api/v1/one_hop_multi_edge", graphSearchOneHopMultiEdgeHandler, {"model_service": model_serviceGraphSearchOneHopMultiEdge, "config_params": config_params}),
        tornado.web.url(r"/graphdb/api/v1/multi_hop_common_vertexes", graphSearchMultiHopCommonVertexesHandler,{"model_service": model_serviceGraphSearchMultiHopCommonVertexes, "config_params": config_params}),
        tornado.web.url(r"/graphdb/api/v1/match_edge", graphSearchMatchEdgeHandler,{"model_service": model_serviceGraphSearchMatchEdge, "config_params": config_params}),
        tornado.web.url(r"/graphdb/api/v1/match_vertex", graphSearchMatchVertexHandler,{"model_service": model_serviceGraphSearchMatchVertex, "config_params": config_params}),
        tornado.web.url(r"/graphdb/api/v1/multi_hop_multi_edge_common_vertexes", graphSearchMultiHopMultiEdgeCommonVertexesHandler,{"model_service": model_serviceGraphSearchMultiHopMultiEdgeCommonVertexes, "config_params": config_params}),
    ]

    def get_routes(self):
        #print(dir(self._routes[0]))
        #print(type(self._routes[0]))
        return self._routes

    def __init__(self):
        #setup_swagger(self._routes)
        settings = {"debug": True}
        setup_swagger(self._routes,
                      swagger_url='/doc',
                      api_base_url='/graphdb/api/v1/',
                      description='',
                      api_version='1.0.0',
                      title='Journal API',
                      contact='name@domain',
                      schemes=['https'],
                      security_definitions={
                          'ApiKeyAuth': {
                              'type': 'apiKey',
                              'in': 'header',
                              'name': 'X-API-Key'
                          }
                      })
        super(Application, self).__init__(self._routes, **settings)




if __name__ == "__main__":
    #app = make_app()

    App = Application()
    #Swagger_specification = export_swagger(App.get_routes())
    #print(Swagger_specification)
    App.get_routes()
    App.listen(10010)
    tornado.ioloop.IOLoop.current().start()
    #Swagger_specification = export_swagger(App.get_routes())
