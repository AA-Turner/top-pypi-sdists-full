import json
import ujson
import datetime
import traceback
import tornado

from abc import ABC
from urllib import parse
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor

from config.logger_design import get_logger
from utils.common import success_request, fail_request
from services.model_sevice import ModelService

logger = get_logger()
config_location = {"version": "0.0.1", "begin_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


class GetInfoData(tornado.web.RequestHandler, ABC):
    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        res = yield self.data_process_and_model()
        self.write(json.dumps(res, cls=DateEncoder))
        self.finish()

    @run_on_executor
    def data_process_and_model(self):
        result = {
            "build": {
                "name": "CHGraph",
                "time": config_location["begin_time"],
                "version": config_location["version"],
            }
        }
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return result


class GetHealthData(tornado.web.RequestHandler, ABC):
    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        res = yield self.data_process_and_model()
        self.write(json.dumps(res, cls=DateEncoder))
        self.finish()

    @run_on_executor
    def data_process_and_model(self):
        result = {"status": "UP"}
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return result


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


class GaBuildHandler(tornado.web.RequestHandler):
    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(50)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        res = yield self.data_process_and_model()
        self.write(json.dumps(res, cls=DateEncoder))
        self.finish()

    @run_on_executor
    def data_process_and_model(self):
        data_json = ujson.loads(self.request.body)
        logger.info(data_json["sql"])
        try:
            result_list = self.model.model_operation(data_json, self.config_params)
            res = success_request(result_list, {})
        except Exception as e:
            logger.error(e)
            print(e.args)
            print(str(e))
            traceback.print_exc()
            res = fail_request({}, {}, e)
        result = res
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return result


class GraphHandler(tornado.web.RequestHandler):

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
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


class GraphInsertHandler(tornado.web.RequestHandler):

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


class GraphDeleteHandler(tornado.web.RequestHandler):
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
    def delete(self):
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


class GraphUpdateHandler(tornado.web.RequestHandler):
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
    def delete(self):
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


class graphSearchOneHopHandler(tornado.web.RequestHandler):

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """
        Description end-point
        ---
        tags:
        - graphSearchOneHop
        summary: Create user
        description: This is one hop algorithm.
        operationId: examples.api.api.createUser
        produces:
        - application/json
        parameters:
        - in: body
          name: body
          description: Created user object
          required: false
          schema:
            type: object
            properties:
              step:
                type: integer
                format: int64
              start_vertex_list:
                type:
                  - "list"
              edge_name_list:
                type: list
              graph_dir:
                type: string
              direction:
                type: string
              edge_con_list:
                type: list
              userStatus:
                type: integer
                format: int32
                description: User Status
        responses:
        "201":
          description: successful operation
        """

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


class graphSearchMultiHopHandler(tornado.web.RequestHandler):

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """
        Description end-point
        ---
        tags:
        - graphSearchMultiHop
        summary: Create user
        description: This can only be done by the logged in user.
        operationId: examples.api.api.createUser
        produces:
        - application/json
        parameters:
        - in: body
          name: body
          description: Created user object
          required: false
          schema:
            type: object
            properties:
              step:
                type: integer
                format: int64
              start_vertex_list:
                type:
                  - "list"
              edge_name_list:
                type: list
              graph_dir:
                type: string
              direction:
                type: string
              edge_con_list:
                type: list
              userStatus:
                type: integer
                format: int32
                description: User Status
        responses:
        "201":
          description: successful operation
        """

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


class GraphSearchMultiHopMultiEdgeHandler(tornado.web.RequestHandler):

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """
                       Description end-point
                       ---
                       tags:
                       - Vertex/Edge-Wise Operation:Search
                       summary: Multi-Hop
                       description: This is the multi-hop service.
                       operationId: examples.api.api.Multi-Hop
                       produces:
                       - application/json
                       parameters:
                       - in: body
                         name: body
                         description: multi-hop
                         required: false
                         schema:
                           type: object
                           properties:
                             step:
                               type: integer
                               default: 1
                             start_vertex_list:
                               type: list
                               default: ['10.73.28.115','10.78.55.20']
                             edge_name_list:
                               type: list
                               default: ["tcpflow", "flow"]
                             graph_name:
                               type: string
                               default: "cyber"
                             direction:
                               type: string
                               default: "forward"
                             edge_con_list_list:
                               type: list
                               default: [["downlink_length>10000", "protocol='http'"], ["record_date='2019-04-15'"]]
                             target_field_list:
                               type: list
                               default: ["record_time"]
                             only_last_step:
                               type: boolean
                               default: true
                             plus_last_vertexes:
                               type: boolean
                               default: false
                       responses:
                       "201":
                         description: successful operation
               """

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


class GraphSearchOneHopMultiEdgeHandler(tornado.web.RequestHandler):

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """
                               Description end-point
                               ---
                               tags:
                               - Vertex/Edge-Wise Operation:Search
                               summary: One Hop
                               description: This is the one hop service.
                               operationId: examples.api.api.OneHop
                               produces:
                               - application/json
                               parameters:
                               - in: body
                                 name: body
                                 description: one hop
                                 required: false
                                 schema:
                                   type: object
                                   properties:
                                     start_vertex_list:
                                       type: list
                                       default: ['10.73.28.115', '10.78.55.20']
                                     edge_name_list:
                                       type: list
                                       default: ["tcpflow", "flow"]
                                     graph_name:
                                       type: string
                                       default: "cyber"
                                     direction:
                                       type: string
                                       default: "forward"
                                     edge_con_list_list:
                                       type: list
                                       default: [["downlink_length>10000", "protocol='http'"], ["record_date='2019-04-15'"]]
                                     target_field_list:
                                       type: list
                                       default: ["record_time"]
                               responses:
                               "201":
                                 description: successful operation
                       """
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

class GraphSearchMultiHopCommonVertexesHandler(tornado.web.RequestHandler):
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
    def get(self):
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


class GraphSearchMatchEdgeHandler(tornado.web.RequestHandler):

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """
                               Description end-point
                               ---
                               tags:
                               - Vertex/Edge-Wise Operation:Search
                               summary: edge matching
                               description: This is the edge matching service.
                               operationId: examples.api.api.EdgeMatching
                               produces:
                               - application/json
                               parameters:
                               - in: body
                                 name: body
                                 description: edge
                                 required: false
                                 schema:
                                   type: object
                                   properties:
                                     edge_name:
                                       type: string
                                       default: "tcpflow"
                                     graph_name:
                                       type: string
                                       default: "cyber"
                                     edge_con_list:
                                       type: list
                                       default: ["downlink_length>100000000"]
                                     target_field_list:
                                       type: list
                                       default: ['record_time', 'downlink_length']
                               responses:
                               "201":
                                 description: successful operation
                       """
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

class GraphSearchMatchVertexHandler(tornado.web.RequestHandler):

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """
                                       Description end-point
                                       ---
                                       tags:
                                       - Vertex/Edge-Wise Operation:Search
                                       summary: vertices matching
                                       description: This is the vertices matching service.
                                       operationId: examples.api.api.VerticesMatching
                                       produces:
                                       - application/json
                                       parameters:
                                       - in: body
                                         name: body
                                         description: vertices
                                         required: false
                                         schema:
                                           type: object
                                           properties:
                                             vertex_name:
                                               type: string
                                               default: "ip"
                                             graph_name:
                                               type: string
                                               default: "cyber_plus"
                                             vertex_con_list:
                                               type: list
                                               default: ["speed>2","service_date=='2021-01-05'"]
                                             target_field_list:
                                               type: list
                                               default: ["service_date","speed"]
                                       responses:
                                       "201":
                                         description: successful operation
                               """
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


class GraphSearchMultiHopMultiEdgeCommonVertexesHandler(tornado.web.RequestHandler):

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """
                                      Description end-point
                                      ---
                                      tags:
                                      - Vertex/Edge-Wise Operation:Search
                                      summary: Multi-Hop Common Vertices
                                      description: This is the multi-hop common vertices service.
                                      operationId: examples.api.api.Multi_HopCommonVertices
                                      produces:
                                      - application/json
                                      parameters:
                                      - in: body
                                        name: body
                                        description: multi-hop common vertices
                                        required: false
                                        schema:
                                          type: object
                                          properties:
                                            step:
                                              type: integer
                                              default: 1
                                            start_vertex_list:
                                              type: list
                                              default: ['10.73.28.115', '10.78.55.20']
                                            edge_name_list:
                                              type: list
                                              default: ["tcpflow", "flow"]
                                            graph_name:
                                              type: string
                                              default: "cyber"
                                            direction:
                                              type: string
                                              default: "forward"
                                            edge_con_list_list:
                                              type: list
                                              default: [["protocol='http'"], ["record_date='2019-04-15'"]]
                                      responses:
                                      "201":
                                        description: successful operation
                              """
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

class graphSearchFindPathHandler(tornado.web.RequestHandler):

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """
                                             Description end-point
                                             ---
                                             tags:
                                             - Vertex/Edge-Wise Operation:Search
                                             summary: Path Finding
                                             description: This is path finding service.
                                             operationId: examples.api.api.PathFinding
                                             produces:
                                             - application/json
                                             parameters:
                                             - in: body
                                               name: body
                                               description: path
                                               required: false
                                               schema:
                                                 type: object
                                                 properties:
                                                   step_limit:
                                                     type: integer
                                                     default: 2
                                                   start_vertex:
                                                     type: string
                                                     default: '10.73.28.115'
                                                   end_vertex:
                                                     type: string
                                                     default: "10.78.55.20"
                                                   graph_name:
                                                     type: string
                                                     default: "cyber"
                                                   target_field_list:
                                                     type: list
                                                     default: ["record_time", "downlink_length"]
                                                   edge_con_list_list:
                                                     type: list
                                                     default: [["downlink_length>10000", "protocol='http'"], ["record_date='2019-04-15'"]]
                                                   edge_name_list:
                                                     type: list
                                                     default: ["tcpflow", "flow"]
                                             responses:
                                             "201":
                                               description: successful operation
                                     """
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


class RegisterGraphHandler(tornado.web.RequestHandler):

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        """
                                                     Description end-point
                                                     ---
                                                     tags:
                                                     - Graph-Wise Operation
                                                     summary: Register Graph
                                                     description: This is the graph registering service.
                                                     operationId: examples.api.api.RegisterGraph
                                                     produces:
                                                     - application/json
                                                     parameters:
                                                     - in: body
                                                       name: body
                                                       description: graph registering
                                                       required: false
                                                       schema:
                                                         type: object
                                                         properties:
                                                           graph_name:
                                                             type: string
                                                             default: "cyber"
                                                           graph_cfg:
                                                             type: string
                                                             default: '{"edges":{"tcpflow":{"db":"graph","table":"tcpflow","src":"source_ip","dst":"destination_ip","fields":["record_date","record_time","protocol","destination_port","uplink_length","downlink_length"]      },"flow":{"db":"graph","table":"flow","src":"source_ip","dst":"destination_ip","fields":["record_date","record_time","destination_port","uri"]} },"vertexes":{}}'
                                                     responses:
                                                     "201":
                                                       description: successful operation
                                             """

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


class DeleteGraphHandler(tornado.web.RequestHandler):
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
    def delete(self):
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


class ShowGraphHandler(tornado.web.RequestHandler):
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
    def get(self):
        """
                                                     Description end-point
                                                     ---
                                                     tags:
                                                     - Graph-Wise Operation
                                                     summary: Show Graph
                                                     description: This is the graph showing service.
                                                     operationId: examples.api.api.ShowGraph
                                                     produces:
                                                     - application/json
                                                     parameters:
                                                     - in: body
                                                       name: body
                                                       description: graph showing
                                                       required: false
                                                       schema:
                                                         type: object
                                                         properties:
                                                     responses:
                                                     "201":
                                                       description: successful operation
                                             """

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


class InsertEdgeHandler(tornado.web.RequestHandler):
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
        """
                                                     Description end-point
                                                     ---
                                                     tags:
                                                     - Vertex/Edge-Wise Operation:Insert
                                                     summary: Insert Edge
                                                     description: This is the edge inserting service.
                                                     operationId: examples.api.api.InsertEdge
                                                     produces:
                                                     - application/json
                                                     parameters:
                                                     - in: body
                                                       name: body
                                                       description: insert edge
                                                       required: false
                                                       schema:
                                                         type: object
                                                         properties:
                                                           edge_name:
                                                             type: string
                                                             default: "tcpflow"
                                                           graph_name:
                                                             type: string
                                                             default: "cyber_plus"
                                                           edge_schema:
                                                             type: list
                                                             default: ["record_time", "record_date", "source_ip", "destination_ip", "protocol", "destination_port", "uplink_length", "downlink_length"]
                                                           edge_data:
                                                             type: list
                                                             default: [["2019-04-11 18:48:59", "2019-04-11", "10.66.18.32", "184.173.90.200", "http", "80", 14725, 3116]]
                                                     responses:
                                                     "201":
                                                       description: successful operation
                                             """

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


class InsertVertexHandler(tornado.web.RequestHandler):

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        """
                                                     Description end-point
                                                     ---
                                                     tags:
                                                     - Vertex/Edge-Wise Operation:Insert
                                                     summary: Insert Vertex
                                                     description: This is the vertex inserting service.
                                                     operationId: examples.api.api.InsertVertex
                                                     produces:
                                                     - application/json
                                                     parameters:
                                                     - in: body
                                                       name: body
                                                       description: insert vertex
                                                       required: false
                                                       schema:
                                                         type: object
                                                         properties:
                                                           vertex_name:
                                                             type: string
                                                             default: "ip"
                                                           graph_name:
                                                             type: string
                                                             default: "cyber_plus"
                                                           vertex_schema:
                                                             type: list
                                                             default: ["service_date", "ip", "host", "speed"]
                                                           vertex_data:
                                                             type: list
                                                             default: [["2021-01-04","1.1.1.1","p47708v.hulk.shbt.qihoo.net","2"],["2021-01-05","1.1.1.2","p47709v.hulk.shbt.qihoo.net","3"]]
                                                     responses:
                                                     "201":
                                                       description: successful operation
                                             """

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


class SummaryGraphHandler(tornado.web.RequestHandler):
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
    def get(self, graph_name):
        """
                                                     Description end-point
                                                     ---
                                                     tags:
                                                     - Graph-Wise Operation
                                                     summary: Summary Graph
                                                     description: This is the graph summary service.
                                                     operationId: examples.api.api.SummaryGraph
                                                     produces:
                                                     - application/json
                                                     parameters:
                                                     - in: body
                                                       name: body
                                                       description: graph summary
                                                       required: false
                                                       schema:
                                                         type: object
                                                         properties:
                                                           graph_name:
                                                             type: string
                                                             default: "cyber"
                                                     responses:
                                                     "201":
                                                       description: successful operation
                                             """
        res = yield self.data_process_and_model(graph_name)
        self.write(json.dumps(res, cls=DateEncoder))
        self.finish()

    @run_on_executor
    def data_process_and_model(self, graph_name):
        # data_json = ujson.loads(self.request.body)
        result_list = self.model.model_operation(graph_name, self.config_params)
        result = {
            "result": result_list
        }
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return result


class DescriptionGraphHandler(tornado.web.RequestHandler):
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
    def get(self, graph_name):
        """
                                                     Description end-point
                                                     ---
                                                     tags:
                                                     - Graph-Wise Operation
                                                     summary: Description Graph
                                                     description: This is the graph description service.
                                                     operationId: examples.api.api.DescriptionGraph
                                                     produces:
                                                     - application/json
                                                     parameters:
                                                     - in: body
                                                       name: body
                                                       description: graph description
                                                       required: false
                                                       schema:
                                                         type: object
                                                         properties:
                                                           graph_name:
                                                             type: string
                                                             default: "cyber"
                                                     responses:
                                                     "201":
                                                       description: successful operation
                                             """

        res = yield self.data_process_and_model(graph_name)
        self.write(json.dumps(res, cls=DateEncoder))
        self.finish()

    @run_on_executor
    def data_process_and_model(self, graph_name):
        # data_json = ujson.loads(self.request.body)
        result_list = self.model.model_operation(graph_name, self.config_params)
        result = {
            "result": result_list
        }
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return result


class HealthServiceHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        """
               Description end-point
                ---
                tags:
                - health
                summary: health
                description: This is the health
                operationId: examples.api.api.health
                produces:
                - application/json
                parameters:
                - in: body
                  name: body
                  description: health
                  required: false
                  schema:
                    type: object
                    properties:
                      health:
                        type: str
                        default:  "health"
                responses:
                "201":
                  description: successful operation
        """
        res = yield self.data_process_and_model()
        self.write(ujson.dumps(res, ensure_ascii=False))
        self.finish("")

    @run_on_executor
    def data_process_and_model(self):
        json_datas = self.request.body.decode('utf8')
        result = {}
        result["status"] = "UP"
        return result


class InfoServiceHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        """
               Description end-point
                ---
                tags:
                - info
                summary: info
                description: This is the info
                operationId: examples.api.api.info
                produces:
                - application/json
                parameters:
                - in: body
                  name: body
                  description: info
                  required: false
                  schema:
                    type: object
                    properties:
                      info:
                        type: str
                        default:  "info"
                responses:
                "201":
                  description: successful operation
        """
        res = yield self.data_process_and_model()
        self.write(ujson.dumps(res, ensure_ascii=False))
        self.finish("")

    @run_on_executor
    def data_process_and_model(self):
        json_datas = self.request.body.decode('utf8')
        result = {}
        build = {}
        build["name"] = "graph-operation"
        build["time"] = "2021-01-29T20:20:41.578Z"
        build["version"] = "0.0.1-SNAPSHOT"
        result["build"] = build
        return result


class FindPathHandler(tornado.web.RequestHandler):

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """
                                                     Description end-point
                                                     ---
                                                     tags:
                                                     - Vertex/Edge-Wise Operation: Path
                                                     summary: Path
                                                     description: This is the path service.
                                                     operationId: examples.api.api.Path
                                                     produces:
                                                     - application/json
                                                     parameters:
                                                     - in: body
                                                       name: body
                                                       description: path
                                                       required: false
                                                       schema:
                                                         type: object
                                                         properties:
                                                           step_limit:
                                                             type: integer
                                                             default: "2"
                                                           graph_name:
                                                             type: string
                                                             default: "cyber_plus"
                                                           start_vertex_list:
                                                             type: list
                                                             default: ["1000007","100000","100"]
                                                           end_vertex_list:
                                                             type: list
                                                             default: ["343965","131254","51242","343965"]
                                                           edge_name_list:
                                                             type: list
                                                             default: ["userid_adgroup","adgroup_customer"]
                                                           edge_con_list_list:
                                                             type: list
                                                             default: [["record_date='2097-5-13'"],["record_date='2017-5-9'"]]
                                                           target_field_list:
                                                             type: list
                                                             default: [["record_date='2097-5-13'"],["record_date='2017-5-9'"]]
                                                     responses:
                                                     "201":
                                                       description: successful operation
                                             """

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


class SubgraphCreationHandler(tornado.web.RequestHandler):

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        """
                                                     Description end-point
                                                     ---
                                                     tags:
                                                     - Subgraph
                                                     summary: Subgraph Creation
                                                     description: This is the subgraph creation service.
                                                     operationId: examples.api.api.SubgraphCreation
                                                     produces:
                                                     - application/json
                                                     parameters:
                                                     - in: body
                                                       name: body
                                                       description: path
                                                       required: false
                                                       schema:
                                                         type: object
                                                         properties:
                                                           subgraph_name:
                                                             type: string
                                                             default: "taobao_sub"
                                                           graph_name:
                                                             type: string
                                                             default: "taobao"
                                                     responses:
                                                     "201":
                                                       description: successful operation
                                             """
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


class MultiHopSubgraphUpdateHandler(tornado.web.RequestHandler):

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        """
                               Description end-point
                               ---
                               tags:
                               - Subgraph
                               summary: Subgraph Update Multi-Hop
                               description: This is the multi-hop subgraph update service.
                               operationId: examples.api.api.SubgraphUpdateMultiHop
                               produces:
                               - application/json
                               parameters:
                               - in: body
                                 name: body
                                 description: subgraph update multi-hop
                                 required: false
                                 schema:
                                   type: object
                                   properties:
                                     step:
                                       type: integer
                                       default: 1
                                     start_vertex_list:
                                       type: list
                                       default: ['10.73.28.115','10.78.55.20']
                                     edge_name_list:
                                       type: list
                                       default: ["tcpflow", "flow"]
                                     graph_name:
                                       type: string
                                       default: "taobao"
                                     subgraph_name:
                                       type: string
                                       default: "taobao_sub"
                                     direction:
                                       type: string
                                       default: "forward"
                                     edge_con_list_list:
                                       type: list
                                       default: [["downlink_length>10000", "protocol='http'"], ["record_date='2019-04-15'"]]
                               responses:
                               "201":
                                 description: successful operation
                       """
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


class PathSubgraphUpdateHandler(tornado.web.RequestHandler):

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        """
                                                             Description end-point
                                                             ---
                                                             tags:
                                                             - Subgraph
                                                             summary: Subgraph Update Path
                                                             description: This is the path subgraph update service.
                                                             operationId: examples.api.api.SubgraphUpdatePath
                                                             produces:
                                                             - application/json
                                                             parameters:
                                                             - in: body
                                                               name: body
                                                               description: path
                                                               required: false
                                                               schema:
                                                                 type: object
                                                                 properties:
                                                                   step_limit:
                                                                     type: integer
                                                                     default: "2"
                                                                   graph_name:
                                                                     type: string
                                                                     default: "taobao"
                                                                   subgraph_name:
                                                                     type: string
                                                                     default: "taobao_sub"
                                                                   start_vertex_list:
                                                                     type: list
                                                                     default: ["1000007","100000","100"]
                                                                   end_vertex_list:
                                                                     type: list
                                                                     default: ["343965","131254","51242","343965"]
                                                                   edge_name_list:
                                                                     type: list
                                                                     default: ["userid_adgroup","adgroup_customer"]
                                                                   edge_con_list_list:
                                                                     type: list
                                                                     default: [["record_date='2097-5-13'"],["record_date='2017-5-9'"]]
                                                             responses:
                                                             "201":
                                                               description: successful operation
                                                     """

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


class EdgeSubgraphUpdateHandler(tornado.web.RequestHandler):

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        """
                                       Description end-point
                                       ---
                                       tags:
                                       - Subgraph
                                       summary: Subgraph Update Edge
                                       description: This is the edge subgraph update service.
                                       operationId: examples.api.api.SubgraphUpdateEdge
                                       produces:
                                       - application/json
                                       parameters:
                                       - in: body
                                         name: body
                                         description: subgraph update edge
                                         required: false
                                         schema:
                                           type: object
                                           properties:
                                             edge_name:
                                               type: string
                                               default: "tcpflow"
                                             graph_name:
                                               type: string
                                               default: "taobao"
                                             subgraph_name:
                                               type: string
                                               default: "taobao_sub"
                                             edge_con_list:
                                               type: list
                                               default: ["downlink_length>100000000"]
                                       responses:
                                       "201":
                                         description: successful operation
                               """
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


class SubgraphDestroyHandler(tornado.web.RequestHandler):

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        """
                                                     Description end-point
                                                     ---
                                                     tags:
                                                     - Subgraph
                                                     summary: Subgraph Destroy
                                                     description: This is the subgraph destroy update service.
                                                     operationId: examples.api.api.SubgraphDestroy
                                                     produces:
                                                     - application/json
                                                     parameters:
                                                     - in: body
                                                       name: body
                                                       description: Subgraph Destroy
                                                       required: false
                                                       schema:
                                                         type: object
                                                         properties:
                                                           subgraph_name:
                                                             type: string
                                                             default: "taobao_sub"
                                                           graph_name:
                                                             type: string
                                                             default: "taobao"
                                                     responses:
                                                     "201":
                                                       description: successful operation
                                             """
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


class MetricIndegreeHandler(tornado.web.RequestHandler):

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """
                                                     Description end-point
                                                     ---
                                                     tags:
                                                     - vertex/edge-wise operation: metric
                                                     summary: Metric Indegree
                                                     description: This is the metric indegree service.
                                                     operationId: examples.api.api.MetricIndegree
                                                     produces:
                                                     - application/json
                                                     parameters:
                                                     - in: body
                                                       name: body
                                                       description: Metric Indegree
                                                       required: false
                                                       schema:
                                                         type: object
                                                         properties:
                                                           edge_name:
                                                             type: string
                                                             default: "user_adgroup"
                                                           graph_name:
                                                             type: string
                                                             default: "taobao"
                                                           if_sort:
                                                             type: boolean
                                                             default: False
                                                           topk:
                                                             type: integer
                                                             default: -1
                                                     responses:
                                                     "201":
                                                       description: successful operation
                                             """
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


class MetricOutdegreeHandler(tornado.web.RequestHandler):

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """
                                                     Description end-point
                                                     ---
                                                     tags:
                                                     - vertex/edge-wise operation: metric
                                                     summary: Metric Outdegree
                                                     description: This is the metric outdegree service.
                                                     operationId: examples.api.api.MetricOutdegree
                                                     produces:
                                                     - application/json
                                                     parameters:
                                                     - in: body
                                                       name: body
                                                       description: Metric Outdegree
                                                       required: false
                                                       schema:
                                                         type: object
                                                         properties:
                                                           edge_name:
                                                             type: string
                                                             default: "user_adgroup"
                                                           graph_name:
                                                             type: string
                                                             default: "taobao"
                                                           if_sort:
                                                             type: boolean
                                                             default: False
                                                           topk:
                                                             type: integer
                                                             default: -1
                                                     responses:
                                                     "201":
                                                       description: successful operation
                                             """
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


class MetricDegreeHandler(tornado.web.RequestHandler):

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """
                                                     Description end-point
                                                     ---
                                                     tags:
                                                     - vertex/edge-wise operation: metric
                                                     summary: Metric Degree
                                                     description: This is the metric degree service.
                                                     operationId: examples.api.api.MetricDegree
                                                     produces:
                                                     - application/json
                                                     parameters:
                                                     - in: body
                                                       name: body
                                                       description: Metric Degree
                                                       required: false
                                                       schema:
                                                         type: object
                                                         properties:
                                                           edge_name:
                                                             type: string
                                                             default: "user_adgroup"
                                                           graph_name:
                                                             type: string
                                                             default: "taobao"
                                                           if_sort:
                                                             type: boolean
                                                             default: False
                                                           topk:
                                                             type: integer
                                                             default: -1
                                                     responses:
                                                     "201":
                                                       description: successful operation
                                             """
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


class MetricPagerankHandler(tornado.web.RequestHandler):

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """
                                                     Description end-point
                                                     ---
                                                     tags:
                                                     - vertex/edge-wise operation: metric
                                                     summary: Metric Pagerank
                                                     description: This is the metric pagerank service.
                                                     operationId: examples.api.api.MetricPagerank
                                                     produces:
                                                     - application/json
                                                     parameters:
                                                     - in: body
                                                       name: body
                                                       description: Metric Pagerank
                                                       required: false
                                                       schema:
                                                         type: object
                                                         properties:
                                                           edge_name:
                                                             type: string
                                                             default: "user_adgroup"
                                                           graph_name:
                                                             type: string
                                                             default: "taobao"
                                                           if_sort:
                                                             type: boolean
                                                             default: False
                                                           topk:
                                                             type: integer
                                                             default: -1
                                                           d:
                                                             type: float
                                                             default: 0.85
                                                           num_iter:
                                                             type: integer
                                                             default: 10
                                                     responses:
                                                     "201":
                                                       description: successful operation
                                             """
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


class EdgeMatchPropertyHandler(tornado.web.RequestHandler):

    def initialize(self, model_service, config_params):
        self.model = model_service
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """
                                                     Description end-point
                                                     ---
                                                     tags:
                                                     - Vertex/Edge-Wise Operation:Match
                                                     summary: Match Edge Property
                                                     description: This is the edge Property matching service.
                                                     operationId: examples.api.api.EdgePropertyMatching
                                                     produces:
                                                     - application/json
                                                     parameters:
                                                     - in: body
                                                       name: body
                                                       description: edge property matching
                                                       required: false
                                                       schema:
                                                         type: object
                                                         properties:
                                                           edge_name:
                                                             type: string
                                                             default: "transactions"
                                                           graph_name:
                                                             type: string
                                                             default: "anti_money_launder"
                                                           start_vertex_list:
                                                             type: list
                                                             default: ["770305"]
                                                           end_vertex_list:
                                                             type: list
                                                             default: ["402592"]
                                                           egde_con_list:
                                                             type: list
                                                             default: ["record_date < \'2017-05-11\'"]
                                                           target_field_list:
                                                             type: list
                                                             default: []
                                                     responses:
                                                     "201":
                                                       description: successful operation
                                             """

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


class VertexMatchPropertyHandler(tornado.web.RequestHandler):
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
    def get(self):
        """
                                                     Description end-point
                                                     ---
                                                     tags:
                                                     - Vertex/Edge-Wise Operation:Match
                                                     summary: Match Vertex Property
                                                     description: This is the vertex property matching service.
                                                     operationId: examples.api.api.VertexPropertyMatching
                                                     produces:
                                                     - application/json
                                                     parameters:
                                                     - in: body
                                                       name: body
                                                       description: vertex property matching
                                                       required: false
                                                       schema:
                                                         type: object
                                                         properties:
                                                           vertex_name:
                                                             type: string
                                                             default: "account"
                                                           graph_name:
                                                             type: string
                                                             default: "anti_money_launder"
                                                           vertex_id_list:
                                                             type: list
                                                             default: ['119309','151550']
                                                           vertex_con_list:
                                                             type: list
                                                             default: ["record_date < \'2017-05-11\'"]
                                                           target_field_list:
                                                             type: list
                                                             default: None
                                                     responses:
                                                     "201":
                                                       description: successful operation
                                             """

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


class EdgeQueryHandler(tornado.web.RequestHandler):
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
    def get(self):
        """
                                                     Description end-point
                                                     ---
                                                     tags:
                                                     - Vertex/Edge-Wise Operation:Match
                                                     summary: Match Edge Property
                                                     description: This is the edge Property matching service.
                                                     operationId: examples.api.api.EdgePropertyMatching
                                                     produces:
                                                     - application/json
                                                     parameters:
                                                     - in: body
                                                       name: body
                                                       description: edge property matching
                                                       required: false
                                                       schema:
                                                         type: object
                                                         properties:
                                                           edge_name:
                                                             type: string
                                                             default: "transactions"
                                                           graph_name:
                                                             type: string
                                                             default: "anti_money_launder"
                                                           edge_con_list:
                                                             type: list
                                                             default: ["record_date < \'2017-05-11\'"]
                                                           target_field_list:
                                                             type: list
                                                             default: []
                                                     responses:
                                                     "201":
                                                       description: successful operation
                                             """

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


class VertexQueryHandler(tornado.web.RequestHandler):
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
    def get(self):
        """
                                                     Description end-point
                                                     ---
                                                     tags:
                                                     - Vertex/Edge-Wise Operation:Match
                                                     summary: Match Vertex Property
                                                     description: This is the vertex property matching service.
                                                     operationId: examples.api.api.VertexPropertyMatching
                                                     produces:
                                                     - application/json
                                                     parameters:
                                                     - in: body
                                                       name: body
                                                       description: vertex property matching
                                                       required: false
                                                       schema:
                                                         type: object
                                                         properties:
                                                           vertex_name:
                                                             type: string
                                                             default: "account"
                                                           graph_name:
                                                             type: string
                                                             default: "anti_money_launder"
                                                           vertex_con_list:
                                                             type: list
                                                             default: ["record_date < \'2017-05-11\'"]
                                                           target_field_list:
                                                             type: list
                                                             default: None
                                                     responses:
                                                     "201":
                                                       description: successful operation
                                             """

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


class TimeStaticSubgraphHandler(tornado.web.RequestHandler):
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
    def get(self):
        """
                                                     Description end-point
                                                     ---
                                                     tags:
                                                     - Vertex/Edge-Wise Operation:Statistic
                                                     summary: Time Static Subgraph
                                                     description: This is the time static subgraph service.
                                                     operationId: examples.api.api.TimeStaticSubgraph
                                                     produces:
                                                     - application/json
                                                     parameters:
                                                     - in: body
                                                       name: body
                                                       description: time static subgraph
                                                       required: false
                                                       schema:
                                                         type: object
                                                         properties:
                                                           edge_name:
                                                             type: string
                                                             default: "account"
                                                           graph_name:
                                                             type: string
                                                             default: "anti_money_launder"
                                                           subgraph_name:
                                                             type: string
                                                             default: "sub_anti_money_laundry2"
                                                           edge_con_list:
                                                             type: list
                                                             default: ["record_date < '2017-05-11'"]
                                                           time_dimention:
                                                             type: string
                                                             default: "Minute"
                                                     responses:
                                                     "201":
                                                       description: successful operation
                                             """

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


class GainSubgraph(tornado.web.RequestHandler):
    """
    获取子图带条件
    """
    def initialize(self, config_params):
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
        try:
            data = data_json["countParams"]
            result_list = ModelService().search_subgraph_by_condition(data, self.config_params)
            res = success_request(result_list, {})
        except Exception as e:
            res = fail_request({}, {}, e)
            print(e.args)
            print(str(e))
            traceback.print_exc()
        result = res
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return result


class GainTimeLineCount(tornado.web.RequestHandler):
    """
    获取时间线统计接口
    """
    def initialize(self, config_params):
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
        data = data_json.get("countParams")
        try:
            result_list = ModelService().time_line_search(data, self.config_params)
            res = success_request(result_list, {})
        except Exception as e:
            res = fail_request({}, {}, e)
            print(e.args)
            print(str(e))
            traceback.print_exc()
        result = res
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return result


class GainSubgraphQuery(tornado.web.RequestHandler):
    """
    根据过滤条件查询子图
    """
    def initialize(self, config_params):
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
        try:
            data = data_json["requestParams"]
            result_list = ModelService().query_subgraph(data, self.config_params)
            res = success_request(result_list, {})
        except Exception as e:
            res = fail_request({}, {}, e)
            logger.error(str(e))
        result = res
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return result


class GainCountEdges(tornado.web.RequestHandler):
    """
    边统计
    """
    def initialize(self, config_params):
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
        data = data_json.get("countParams")
        try:
            result_list = ModelService().count_src_dst_round(data, self.config_params)
            res = success_request(result_list, {})
        except Exception as e:
            res = fail_request({}, {}, e)
            print(e.args)
            print(str(e))
            traceback.print_exc()
        result = res
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return result


class GainGraphTypeCount(tornado.web.RequestHandler):
    """
    获取子图不同类型的统计接口
    """
    def initialize(self, config_params):
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        res = yield self.data_process_and_model()
        self.write(json.dumps(res, cls=DateEncoder))
        self.finish()

    @run_on_executor
    def data_process_and_model(self):
        params = parse.parse_qs(parse.urlparse(self.request.uri).query)
        try:
            result_list = ModelService().statistics_operation_function(params, self.config_params)
            res = success_request(result_list, {})
        except Exception as e:
            res = fail_request({}, {}, e)
            print(e.args)
            print(str(e))
            traceback.print_exc()
        result = res
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return result


class GainGraphTypeSet(tornado.web.RequestHandler):
    """
    # 统计子图点或者边的多个属性接口
    """

    def initialize(self, config_params):
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        res = yield self.data_process_and_model()
        self.write(json.dumps(res, cls=DateEncoder))
        self.finish()

    @run_on_executor
    def data_process_and_model(self):
        params = parse.parse_qs(parse.urlparse(self.request.uri).query)
        try:
            result_list = ModelService().statistics_operation_attributes_function(params, self.config_params)
            res = success_request(result_list, {})
        except Exception as e:
            res = fail_request({}, {}, e)
            print(e.args)
            print(str(e))
            traceback.print_exc()
        result = res
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return result


class GainGraphTypeFunction(tornado.web.RequestHandler):
    """
    统计子图点或者边的单个属性接口
    """

    def initialize(self, config_params):
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        res = yield self.data_process_and_model()
        self.write(json.dumps(res, cls=DateEncoder))
        self.finish()

    @run_on_executor
    def data_process_and_model(self):
        params = parse.parse_qs(parse.urlparse(self.request.uri).query)
        try:
            result_list = ModelService().statistics_operation_attribute_function(params, self.config_params,
                                                                                 label_statistic="y")
            res = success_request(result_list, {})
        except Exception as e:
            res = fail_request({}, {}, e)
            print(e.args)
            print(str(e))
            traceback.print_exc()
        result = res
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return result

class GainGraphTaskSelect(tornado.web.RequestHandler):
    """
    统计子图点或者边的单个属性接口
    """

    def initialize(self, config_params):
        self.config_params = config_params

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        res = yield self.data_process_and_model()
        self.write(json.dumps(res, cls=DateEncoder))
        self.finish()

    @run_on_executor
    def data_process_and_model(self):
        params = parse.parse_qs(parse.urlparse(self.request.uri).query)
        try:
            result_list = ModelService().calculation_attribute_select_function(params, self.config_params)
            res = success_request(result_list, {})
        except Exception as e:
            res = fail_request({}, {}, e)
            print(e.args)
            print(str(e))
            traceback.print_exc()
        result = res
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return result

class GainGraphTaskSubmit(tornado.web.RequestHandler):
    """
    提交计算任务接口
    """

    def initialize(self, config_params):
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
        data = data_json.get("params")
        try:
            result_list = ModelService().calculation_attribute_submit_function(data, self.config_params)
            res = success_request(result_list, {})
        except Exception as e:
            res = fail_request({}, {}, e)
            print(e.args)
            print(str(e))
            traceback.print_exc()
        result = res
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return result