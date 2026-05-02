import pandas as pd
import numpy as np
from config.logger_design import get_logger
from config.config import ClusterConfig
from utils.common import tostr
from utils.sql_merge_operation import SqlMergeHandler
from utils.sql_replace_operation import SqlReplaceHandler
from daos.common import deal_query_result, deal_query_result_sample, deal_query_result_sample_plus,\
    deal_query_result_with_paging
logger = get_logger()
cluster_config = ClusterConfig()
sql_replace_handler = SqlReplaceHandler(cluster_config.is_cluster)

class CHGraph(object):

    def __init__(self, client):
        self.client = client
        self.graph_name = None
        self.graph_cfg = None
        logger.info('CHGraph Start')

    def execute(self, sql):
        print(sql)
        res = self.client.query_dataframe(sql)
        logger.info("execute sql", sql)
        return res

    def create_subgraph(self, subgraph_name):
        """
        创建子图
        """
        success, msg = self.create_database(subgraph_name, cluster_config.is_cluster, cluster_config.cluster_name)
        if not success:
            return msg

        try:
            """
            创建子图的点边表
            """
            for keyword in ["edges", "vertexes"]:
                for _type, info in self.graph_cfg.get(keyword, {}).items():
                    self.create_subgraph_table(keyword, subgraph_name, info, cluster_config.is_cluster,
                                               cluster_config.cluster_name)
        except Exception as e:
            logger.error("create subgraph error. errMsg:{}".format(str(e)))
            return "subgraph is already exist or something wrong"
        try:
            """
            创建子图的计算属性表
            """
            for _type, info in self.graph_cfg.get("vertexes", {}).items():
                self.create_subgraph_ext_table("vertexes", subgraph_name, info, cluster_config.is_cluster,
                                           cluster_config.cluster_name)
                return
        except Exception as e:
            logger.error("create ext subgraph error. errMsg:{}".format(str(e)))
            return "create ext table filed !!"


    def use_graph(self, graph_name, db):
        """
        图名称切换
        """
        res = db.use_tables(graph_name)
        if not res:
            logger.error("graph name [" + graph_name + "] does not exist")
            return
        else:
            self.graph_name = graph_name
            self.graph_cfg = res
            logger.info("use graph [" + graph_name + "] done")

    def insert_edge(self, edge_name, edge_schema, edge_data):
        """
        插入边
        """
        if edge_name not in self.graph_cfg["edges"]:
            logger.warning("invalid edge: " + edge_name)
            return "invalid edge: " + edge_name

        edge_info = self.graph_cfg["edges"][edge_name]
        db_table = edge_info["db"] + "." + edge_info["table"]

        if edge_info["src"] not in edge_schema or edge_info["dst"] not in edge_schema:
            logger.warning("require src field and dst field of edge")
            return "require src field and dst field of edge"

        sql = "insert into " + db_table + " (" + ",".join(edge_schema) + ") values " + ",".join(
            [str(line) for line in edge_data])
        self.client.execute(sql)
        return "edge inserted success"

    # 插入点
    def insert_vertex(self, vertex_name, vertex_schema, vertex_data):

        if vertex_name not in self.graph_cfg["vertexes"]:
            logger.warning("invalid vertex: " + vertex_name)
            return "invalid vertex: " + vertex_name

        vertex_info = self.graph_cfg["vertexes"][vertex_name]
        db_table = vertex_info["db"] + "." + vertex_info["table"]

        if vertex_info["id"] not in vertex_schema:
            logger.warning("require id field of vertex")
            return "require id field of vertex"

        sql = "insert into " + db_table + " (" + ",".join(vertex_schema) + ") values " + ",".join(
            [str(line) for line in vertex_data])
        self.client.execute(sql)
        return "vertex inserted success"

    #############################################
    #################### vertex/edge-wise operation: search
    #############################################
    ## one_hop return edges
    ## one_hop does not require type(src) == type(dst)
    # 一跳，返回点集合，dataframe
    def one_hop(self,
                start_vertex_list,
                direction,
                edge_name,
                edge_con_list,
                target_field_list,
                end_vertex_con_list=None):

        if edge_name not in self.graph_cfg["edges"]:
            logger.warning("invalid edge: " + edge_name)
            return

        edge_info = self.graph_cfg["edges"][edge_name]
        db_table = edge_info["db"] + "." + edge_info["table"]

        if direction == "forward":
            start_vertex_list_con = edge_info["src"] + " in " + tostr(start_vertex_list)
        elif direction == "backward":
            start_vertex_list_con = edge_info["dst"] + " in " + tostr(start_vertex_list)
        elif direction == "bidirectional":
            start_vertex_list_con = "(" + edge_info["src"] + " in " + tostr(start_vertex_list) + " or " + edge_info[
                "dst"] + " in " + tostr(start_vertex_list) + ")"
        else:
            logger.warning("invalid direction")
            return "invalid direction"

        edge_con_list_con = ""
        if edge_con_list is not None and len(edge_con_list) > 0:
            edge_con_list_con = " and " + " and ".join(edge_con_list)

        target_field_list_con = edge_info["src"] + "," + edge_info["dst"] + "," + edge_info["rank"]
        if target_field_list is None:
            target_field_list_con += "," + ",".join(edge_info["fields"])
        elif type(target_field_list) == list and len(target_field_list) > 0:
            target_field_list_con += "," + ",".join(target_field_list)
        elif type(target_field_list) == str and target_field_list == "src":
            target_field_list_con = "DISTINCT " + edge_info["src"]
        elif type(target_field_list) == str and target_field_list == "dst":
            target_field_list_con = "DISTINCT " + edge_info["dst"]

        sql = "select " + target_field_list_con + " from " + db_table + " where " + \
              start_vertex_list_con + edge_con_list_con
        logger.info("[one_hop] origin sql: " + sql)

        sql = sql_replace_handler.deal_sql(sql)

        logger.info("[one_hop] new sql: {}".format(sql))

        res = self.client.query_dataframe(sql)

        return res

    # 多跳，多次单跳的结果
    ## multi_hop return edges
    ## multi_hop requires type(src) == type(dst)
    def multi_hop(self,
                  step,
                  start_vertex_list,
                  direction,
                  edge_name,
                  edge_con_list,
                  target_field_list,
                  only_last_step,
                  plus_last_vertexes=False,
                  end_vertex_con_list=None):

        multi_res = []

        multi_step_start_vertex_list = start_vertex_list

        for i in range(step):

            res = self.one_hop(multi_step_start_vertex_list,
                               direction,
                               edge_name,
                               edge_con_list,
                               target_field_list)

            if res.shape[0] == 0:
                logger.warning("multi-hop terminates at " + str(i + 1))
                break

            multi_res.append(res)

            if i == step - 1 and not plus_last_vertexes:
                continue

            # TODO: may have performance issue
            edge_info = self.graph_cfg["edges"][edge_name]
            if direction == "forward":
                multi_step_start_vertex_list = np.unique(res[edge_info['dst']].values)
            elif direction == "backward":
                multi_step_start_vertex_list = np.unique(res[edge_info['src']].values)
            elif direction == "bidirectional":
                logger.warning("bidirectional not implemented")
                return
            else:
                logger.warning("invalid direction")
                return "invalid direction"

        if only_last_step:
            if plus_last_vertexes:
                return (multi_res[-1], multi_step_start_vertex_list)
            else:
                return multi_res[-1]
        else:
            return multi_res

    # 多跳，多次单跳的结果，拿到公共顶点（好像暂时不会用到）
    # multi_hop_common_vertexes return common vertexes
    def multi_hop_common_vertexes(self,
                                  step,
                                  start_vertex_list,
                                  direction,
                                  edge_name,
                                  edge_con_list):

        end_set_list = []
        for i in range(len(start_vertex_list)):
            (res, vertex) = self.multi_hop(step,
                                           [start_vertex_list[i]],
                                           direction,
                                           edge_name,
                                           edge_con_list,
                                           [],
                                           True,
                                           True)
            if direction == "forward":
                end_set_list.append(set(vertex))
            elif direction == "backward":
                end_set_list.append(set(vertex))
            elif direction == "bidirectional":
                logger.warning("bidirectional not implemented")
                return
            else:
                logger.warning("invalid direction")
                return

        intersect = end_set_list[0]
        for i in range(1, len(end_set_list)):
            intersect &= end_set_list[i]

        return list(intersect)

    # 起点列表一跳，多种边，循环的方式拿到多次一跳的结果
    ## one_hop_multi_edge return edges
    ## one_hop_multi_edge does not require type(src) == type(dst)
    def one_hop_multi_edge(self,
                           start_vertex_list,
                           direction,
                           edge_name_list,
                           edge_con_list_list,
                           target_field_list,
                           end_vertex_con_list=None):

        res_list = []

        for edge_name in edge_name_list:
            if edge_name not in self.graph_cfg["edges"]:
                logger.warning("invalid edge: " + edge_name)
                return "invalid edge: " + edge_name

        for i in range(len(edge_name_list)):
            edge_name = edge_name_list[i]
            edge_con_list = edge_con_list_list[i]
            res = self.one_hop(start_vertex_list, direction, edge_name, edge_con_list, target_field_list)
            res_list.append(res)

        return res_list

    # 起点列表多跳多边，循环的方式拿到多次一跳多边的结果
    ## multi_hop_multi_edge return edges
    ## multi_hop_multi_edge requires type(src) == type(dst)
    def multi_hop_multi_edge(self,
                             step,
                             start_vertex_list,
                             direction,
                             edge_name_list,
                             edge_con_list_list,
                             target_field_list,
                             only_last_step,
                             plus_last_vertexes=False):

        multi_res = []

        multi_step_start_vertex_list = start_vertex_list

        for i in range(step):
            res = self.one_hop_multi_edge(multi_step_start_vertex_list,
                                          direction,
                                          edge_name_list,
                                          edge_con_list_list,
                                          target_field_list)

            multi_res.append(res)

            if sum([res_elem.shape[0] for res_elem in res]) == 0:
                logger.warning("multi-hop terminates at " + str(i + 1))
                multi_step_start_vertex_list = []
                break

            if i == step - 1 and not plus_last_vertexes:
                continue

            # TODO: may have performance issue
            if direction == "forward":
                tmp_list = []
                for ii in range(len(edge_name_list)):
                    if res[ii].shape[0] == 0:
                        continue
                    edge_name = edge_name_list[ii]
                    edge_info = self.graph_cfg["edges"][edge_name]
                    tmp_list.append(res[ii][edge_info['dst']].values)
                multi_step_start_vertex_list = np.unique(np.concatenate(tmp_list))
            elif direction == "backward":
                tmp_list = []
                for ii in range(len(edge_name_list)):
                    if res[ii].shape[0] == 0:
                        continue
                    edge_name = edge_name_list[ii]
                    edge_info = self.graph_cfg["edges"][edge_name]
                    tmp_list.append(res[ii][edge_info['src']].values)
                multi_step_start_vertex_list = np.unique(np.concatenate(tmp_list))
            elif direction == "bidirectional":
                logger.warning("bidirectional not implemented")
                return "bidirectional not implemented"
            else:
                logger.warning("invalid direction")
                return "invalid direction"

        if only_last_step:
            if plus_last_vertexes:
                return (multi_res[-1], multi_step_start_vertex_list)
            else:
                return multi_res[-1]
        else:
            return multi_res

        # 起点列表多跳多边，循环的方式拿到多次一跳多边的结果
        ## multi_hop_multi_edge return edges
        ## multi_hop_multi_edge requires type(src) == type(dst)

    def find_path_response(self,
                           start_vertex_list,
                           direction,
                           edge_name_list,
                           edge_con_list_list,
                           target_field_list):

        multi_step_start_vertex_list = start_vertex_list
        res = self.one_hop_multi_edge(multi_step_start_vertex_list,
                                      direction,
                                      edge_name_list,
                                      edge_con_list_list,
                                      target_field_list)

        # TODO: may have performance issue
        tmp_list = []
        if direction == "forward":

            for ii in range(len(edge_name_list)):
                if res[ii].shape[0] == 0:
                    tmp_list.append([])
                    continue
                edge_name = edge_name_list[ii]
                edge_info = self.graph_cfg["edges"][edge_name]
                tmp_list.append(np.unique(res[ii][edge_info['dst']].values))
            # multi_step_start_vertex_list = np.unique(np.concatenate(tmp_list))
        elif direction == "backward":
            for ii in range(len(edge_name_list)):
                if res[ii].shape[0] == 0:
                    tmp_list.append([])
                    continue
                edge_name = edge_name_list[ii]
                edge_info = self.graph_cfg["edges"][edge_name]
                tmp_list.append(np.unique(res[ii][edge_info['src']].values))
            # multi_step_start_vertex_list = np.unique(np.concatenate(tmp_list))
        elif direction == "bidirectional":
            logger.warning("bidirectional not implemented")
            return "bidirectional not implemented"
        else:
            logger.warning("invalid direction")
            return "invalid direction"
        return (res, tmp_list)

            # multi_hop_multi_edge_common_vertexes return common vertexes
    def multi_hop_multi_edge_common_vertexes(self,
                                             step,
                                             start_vertex_list,
                                             direction,
                                             edge_name_list,
                                             edge_con_list_list):

        end_set_list = []
        for i in range(len(start_vertex_list)):
            (res, vertex) = self.multi_hop_multi_edge(step,
                                                      [start_vertex_list[i]],
                                                      direction,
                                                      edge_name_list,
                                                      edge_con_list_list,
                                                      [],
                                                      True,
                                                      True)
            if direction == "forward":
                end_set_list.append(set(vertex))
            elif direction == "backward":
                end_set_list.append(set(vertex))
            elif direction == "bidirectional":
                logger.warning("bidirectional not implemented")
                return "bidirectional not implemented"
            else:
                logger.warning("invalid direction")
                return "invalid direction"

        intersect = end_set_list[0]
        for i in range(1, len(end_set_list)):
            intersect &= end_set_list[i]

        return list(intersect)

    # match_edge returns edges which satisfy constraints
    def match_edge(self,
                   edge_name,
                   edge_con_list,
                   target_field_list,
                   data_type="list"):

        if edge_name not in self.graph_cfg["edges"]:
            logger.warning("invalid edge: " + edge_name)
            return "invalid edge: " + edge_name

        edge_info = self.graph_cfg["edges"][edge_name]
        db_table = edge_info["db"] + "." + edge_info["table"]

        edge_con_list_con = ""
        if edge_con_list is not None and len(edge_con_list) > 0 and edge_con_list[0] != '':
            edge_con_list_con = " where " + " and ".join(edge_con_list)

        target_field_list_con = edge_info["src"] + "," + edge_info["dst"]
        if target_field_list is None:
            target_field_list_con += "," + ",".join(edge_info["fields"])
        elif len(target_field_list) > 0:
            target_field_list_con += "," + ",".join(target_field_list)

        sql = "select " + target_field_list_con + " from " + db_table + edge_con_list_con
        logger.info("sql: " + sql)
        res = deal_query_result_sample(data_type, self.client, sql)
        return res

    # match_vertex returns vertexes which satisfy constraints
    def match_vertex(self,
                     vertex_name,
                     vertex_con_list,
                     target_field_list,
                     data_type="list"):

        if vertex_name not in self.graph_cfg["vertexes"]:
            logger.warning("invalid vertex: " + vertex_name)
            return "invalid vertex: " + vertex_name

        vertex_info = self.graph_cfg["vertexes"][vertex_name]
        db_table = vertex_info["db"] + "." + vertex_info["table"]

        vertex_con_list_con = ""
        if vertex_con_list is not None and len(vertex_con_list) > 0:
            vertex_con_list_con = " where " + " and ".join(vertex_con_list)

        target_field_list_con = vertex_info["id"]
        if target_field_list is None:
            target_field_list_con += "," + ",".join(vertex_info["fields"])
        elif len(target_field_list) > 0:
            target_field_list_con += "," + ",".join(target_field_list)

        sql = "select " + target_field_list_con + " from " + db_table + vertex_con_list_con
        logger.info("sql: " + sql)
        res = deal_query_result_sample(data_type, self.client, sql)
        return res

    def find_path_multi_edge(self,
                             start_vertex_list,
                             end_vertex_list,
                             edge_name_list,
                             edge_con_list_list,
                             target_field_list,
                             step_limit):

        if step_limit > 3:
            # logger.warning("finding path longer than 2 not implemented")

            res4 = self.find_path_multi_edge_s4(start_vertex_list,
                                                end_vertex_list,
                                                edge_name_list,
                                                edge_con_list_list,
                                                target_field_list)

            res3 = self.find_path_multi_edge_s3(start_vertex_list,
                                                end_vertex_list,
                                                edge_name_list,
                                                edge_con_list_list,
                                                target_field_list)

            res2 = self.find_path_multi_edge_s2(start_vertex_list,
                                                end_vertex_list,
                                                edge_name_list,
                                                edge_con_list_list,
                                                target_field_list)

            res1 = self.find_path_multi_edge_s1(start_vertex_list,
                                                end_vertex_list,
                                                edge_name_list,
                                                edge_con_list_list,
                                                target_field_list)

            return [res1, res2, res3, res4]

        if step_limit > 2:
            res3 = self.find_path_multi_edge_s3(start_vertex_list,
                                                end_vertex_list,
                                                edge_name_list,
                                                edge_con_list_list,
                                                target_field_list)
            # logger.warning("finding path longer than 2 not implemented")
            res2 = self.find_path_multi_edge_s2(start_vertex_list,
                                                end_vertex_list,
                                                edge_name_list,
                                                edge_con_list_list,
                                                target_field_list)

            res1 = self.find_path_multi_edge_s1(start_vertex_list,
                                                end_vertex_list,
                                                edge_name_list,
                                                edge_con_list_list,
                                                target_field_list)
            return [res1, res2, res3]

        if step_limit > 1:
            res2 = self.find_path_multi_edge_s2(start_vertex_list,
                                                end_vertex_list,
                                                edge_name_list,
                                                edge_con_list_list,
                                                target_field_list)

            res1 = self.find_path_multi_edge_s1(start_vertex_list,
                                                end_vertex_list,
                                                edge_name_list,
                                                edge_con_list_list,
                                                target_field_list)
            return [res1, res2]

        if step_limit > 0:
            res1 = self.find_path_multi_edge_s1(start_vertex_list,
                                                end_vertex_list,
                                                edge_name_list,
                                                edge_con_list_list,
                                                target_field_list)
            return [res1]

    # return path of length 1 (list of df)
    def find_path_multi_edge_s1(self,
                                start_vertex_list,
                                end_vertex_list,
                                edge_name_list,
                                edge_con_list_list,
                                target_field_list):

        res_list = []

        for i in range(len(edge_name_list)):
            edge_name = edge_name_list[i]
            edge_con_list = edge_con_list_list[i]
            edge_info = self.graph_cfg["edges"][edge_name]
            start_vertex_list_con = edge_info["src"] + " in " + tostr(start_vertex_list)
            end_vertex_list_con = edge_info["dst"] + " in " + tostr(end_vertex_list)
            edge_con_list.append(start_vertex_list_con)
            edge_con_list.append(end_vertex_list_con)
            res = self.match_edge(edge_name, edge_con_list, target_field_list, data_type="df")
            res_list.append(res)

        return res_list

        # return path of length 2 (list of list of df)

    def find_path_multi_edge_s2(self,
                                start_vertex_list,
                                end_vertex_list,
                                edge_name_list,
                                edge_con_list_list,
                                target_field_list):

        (f_edges, f_vertices) = self.multi_hop_multi_edge(1, start_vertex_list, "forward",
                                                          edge_name_list, edge_con_list_list,
                                                          target_field_list, True, True)

        (b_edges, b_vertices) = self.multi_hop_multi_edge(1, end_vertex_list, "backward",
                                                          edge_name_list, edge_con_list_list,
                                                          target_field_list, True, True)

        transit_vertices = np.intersect1d(f_vertices, b_vertices, assume_unique=True)

        if len(transit_vertices) == 0:
            return [[pd.DataFrame([])] * len(edge_name_list), [pd.DataFrame([])] * len(edge_name_list)]

        f_edges_final = []
        for df in f_edges:
            if len(df) != 0:
                f_edges_final.append(df[df.iloc[:, 1].isin(transit_vertices)])
            else:
                f_edges_final.append(pd.DataFrame([]))
        b_edges_final = []
        for df in b_edges:
            if len(df) != 0:
                b_edges_final.append(df[df.iloc[:, 0].isin(transit_vertices)])
            else:
                b_edges_final.append(pd.DataFrame([]))
        return [f_edges_final, b_edges_final]

    def find_path_multi_edge_s3(self,
                                start_vertex_list,
                                end_vertex_list,
                                edge_name_list,
                                edge_con_list_list,
                                target_field_list):

        # f_vertices is ndarray  & f_edges is list of dataframe
        (first_edges, f_vertices) = self.multi_hop_multi_edge(1, start_vertex_list, "forward",
                                                              edge_name_list, edge_con_list_list,
                                                              target_field_list, True, True)
        # f_edges_final, b_edges_final is list of datdaframe
        if isinstance(f_vertices, pd.DataFrame):
            new_start_vertex_ids = f_vertices.tolist()
        else:
            new_start_vertex_ids = f_vertices
        [second_edges, third_edges_final] = self.find_path_multi_edge_s2(new_start_vertex_ids,
                                                                         end_vertex_list,
                                                                         edge_name_list,
                                                                         edge_con_list_list, target_field_list)

        # for  backward
        if second_edges == "":
            return [[pd.DataFrame([])] * len(edge_name_list), [pd.DataFrame([])] * len(edge_name_list),
                    [pd.DataFrame([])] * len(edge_name_list)]
        tmp_list = []
        for ii in range(len(edge_name_list)):
            if second_edges[ii].shape[0] == 0:
                continue
            edge_name = edge_name_list[ii]
            edge_info = self.graph_cfg["edges"][edge_name]
            tmp_list.append(second_edges[ii][edge_info['src']].values)
        if tmp_list == []:
            return [[pd.DataFrame([])] * len(edge_name_list), [pd.DataFrame([])] * len(edge_name_list),
                    [pd.DataFrame([])] * len(edge_name_list)]
        multi_step_start_vertex_list = np.unique(np.concatenate(tmp_list))
        transit_vertices = np.intersect1d(f_vertices, multi_step_start_vertex_list, assume_unique=True)
        if len(transit_vertices) == 0:
            return [[pd.DataFrame([])] * len(edge_name_list), [pd.DataFrame([])] * len(edge_name_list),
                    [pd.DataFrame([])] * len(edge_name_list)]
        first_edges_final = []
        for df in first_edges:
            if df.empty:
                first_edges_final.append(pd.DataFrame([]))
                continue
            first_edges_final.append(df[df.iloc[:, 1].isin(transit_vertices)])
        second_edges_final = []
        for df in second_edges:
            if df.empty:
                second_edges_final.append(pd.DataFrame([]))
                continue
            second_edges_final.append(df[df.iloc[:, 0].isin(transit_vertices)])

        return [first_edges_final, second_edges_final, third_edges_final]

    def find_path_multi_edge_s4(self,
                                start_vertex_list,
                                end_vertex_list,
                                edge_name_list,
                                edge_con_list_list,
                                target_field_list):

        # f_vertices is ndarray  & f_edges is list of dataframe
        (first_edges, f_vertices) = self.multi_hop_multi_edge(1, start_vertex_list, "forward",
                                                              edge_name_list, edge_con_list_list,
                                                              target_field_list, True, True)
        # f_edges_final, b_edges_final is list of datdaframe
        if isinstance(f_vertices, pd.DataFrame):
            new_start_vertex_ids = f_vertices.tolist()
        else:
            new_start_vertex_ids = f_vertices
        [second_edges, third_edges_final, fourth_edges_final] = self.find_path_multi_edge_s3(new_start_vertex_ids,
                                                                                             end_vertex_list,
                                                                                             edge_name_list,
                                                                                             edge_con_list_list,
                                                                                             target_field_list)
        if second_edges == "":
            return [[pd.DataFrame([])] * len(edge_name_list), [pd.DataFrame([])] * len(edge_name_list),
                    [pd.DataFrame([])] * len(edge_name_list), [pd.DataFrame([])] * len(edge_name_list)]
        tmp_list = []
        for ii in range(len(edge_name_list)):
            if second_edges[ii].shape[0] == 0:
                continue
            edge_name = edge_name_list[ii]
            edge_info = self.graph_cfg["edges"][edge_name]
            tmp_list.append(second_edges[ii][edge_info['src']].values)
        if tmp_list == []:
            return [[pd.DataFrame([])] * len(edge_name_list), [pd.DataFrame([])] * len(edge_name_list),
                    [pd.DataFrame([])] * len(edge_name_list), [pd.DataFrame([])] * len(edge_name_list)]
        multi_step_start_vertex_list = np.unique(np.concatenate(tmp_list))
        transit_vertices = np.intersect1d(f_vertices, multi_step_start_vertex_list, assume_unique=True)
        if len(transit_vertices) == 0:
            return [[pd.DataFrame([])] * len(edge_name_list), [pd.DataFrame([])] * len(edge_name_list),
                    [pd.DataFrame([])] * len(edge_name_list), [pd.DataFrame([])] * len(edge_name_list)]
        first_edges_final = []
        for df in first_edges:
            if df.empty:
                first_edges_final.append(pd.DataFrame([]))
                continue
            first_edges_final.append(df[df.iloc[:, 1].isin(transit_vertices)])
        second_edges_final = []
        for df in second_edges:
            if df.empty:
                second_edges_final.append(pd.DataFrame([]))
                continue
            second_edges_final.append(df[df.iloc[:, 0].isin(transit_vertices)])

        return [first_edges_final, second_edges_final, third_edges_final, fourth_edges_final]

        #############################################
        #################### subgraph
        #############################################

        # subgraph_name is recommended to be unique (ex. plus timestamp)

    def update_subgraph_by_multi_hop_multi_edge(self,
                                                main_graph,
                                                db,
                                                subgraph_name,
                                                step,
                                                start_vertex_list,
                                                direction,
                                                edge_name_list,
                                                edge_con_list_list):
        main_db = self.graph_cfg["edges"][edge_name_list[0]]["db"]

        multi_res = self.multi_hop_multi_edge(step, start_vertex_list, direction,
                                              edge_name_list, edge_con_list_list, None, False, False)
        self.use_graph(subgraph_name, db)
        try:
            for single_res in multi_res:
                for i in range(len(edge_name_list)):
                    if single_res[i].shape[0] == 0:
                        continue
                    edge_info = self.graph_cfg["edges"][edge_name_list[i]]
                    db_table = subgraph_name + "." + edge_info["table"]
                    schema_fields = edge_info.get("fields")
                    if schema_fields:
                        target_field_list_con = edge_info["src"] + "," + edge_info["dst"] + "," + \
                                                edge_info["rank"] + "," + ",".join(schema_fields)
                    else:
                        target_field_list_con = edge_info["src"] + "," + edge_info["dst"] + "," + \
                                                edge_info["rank"]

                    # TODO: list hurts performance and increases memory cost
                    col_list = [list(pd.to_datetime(single_res[i][col])) if str(
                        single_res[i][col].dtype) == "datetime64[ns]" else list(single_res[i][col].values) for col in
                                single_res[i].columns]
                    self.client.execute("insert into " + db_table + " (" + target_field_list_con + ") values", col_list,
                                        columnar=True)

                    src_info = self.graph_cfg["vertexes"][edge_info["src_type"]]
                    src_db_table_new = subgraph_name + "." + src_info["table"]
                    src_db_table_old = main_db + "." + src_info["table"]
                    src_target_field_list_con = src_info["id"] + "," + ",".join(src_info["fields"])
                    self.client.execute(
                        "insert into " + src_db_table_new + " (" + src_target_field_list_con + ") select distinct " + src_target_field_list_con + " from " + src_db_table_old + " where " +
                        src_info["id"] + " in " + tostr(col_list[0]))
                    dst_info = self.graph_cfg["vertexes"][edge_info["dst_type"]]
                    dst_db_table_new = subgraph_name + "." + dst_info["table"]
                    dst_db_table_old = main_db + "." + dst_info["table"]
                    dst_target_field_list_con = dst_info["id"] + "," + ",".join(dst_info["fields"])
                    self.client.execute(
                        "insert into " + dst_db_table_new + " (" + dst_target_field_list_con + ") select distinct " + dst_target_field_list_con + " from " + dst_db_table_old + " where " +
                        dst_info["id"] + " in " + tostr(col_list[1]))
            return multi_res
        except Exception as e:
            print(e)
            logger.error(e)

    def update_subgraph_by_match_edge(self,
                                      subgraph_name,
                                      edge_name,
                                      edge_con_list):

        res = self.match_edge(edge_name, edge_con_list, None, data_type='df')
        edge_info = self.graph_cfg["edges"][edge_name]
        db_table = subgraph_name + "." + edge_info["table"]
        target_field_list_con = edge_info["src"] + "," + edge_info["dst"] + "," + ",".join(edge_info["fields"])
        # TODO: list hurts performance and increases memory cost
        col_list = [list(pd.to_datetime(res[col])) if str(res[col].dtype) == "datetime64[ns]" else list(res[col].values)
                    for col in res.columns]
        try:
            self.client.execute("insert into " + db_table + " (" + target_field_list_con + ") values", col_list,
                                columnar=True)

            src_info = self.graph_cfg["vertexes"][edge_info["src_type"]]
            src_db_table_new = subgraph_name + "." + src_info["table"]
            src_db_table_old = src_info["db"] + "." + src_info["table"]
            src_target_field_list_con = src_info["id"] + "," + ",".join(src_info["fields"])
            self.client.execute(
                "insert into " + src_db_table_new + " (" + src_target_field_list_con + ") select " + src_target_field_list_con + " from " + src_db_table_old + " where " +
                src_info["id"] + " in " + tostr(col_list[0]))
            dst_info = self.graph_cfg["vertexes"][edge_info["dst_type"]]
            dst_db_table_new = subgraph_name + "." + dst_info["table"]
            dst_db_table_old = dst_info["db"] + "." + dst_info["table"]
            dst_target_field_list_con = dst_info["id"] + "," + ",".join(dst_info["fields"])
            self.client.execute(
                "insert into " + dst_db_table_new + " (" + dst_target_field_list_con + ") select " + dst_target_field_list_con + " from " + dst_db_table_old + " where " +
                dst_info["id"] + " in " + tostr(col_list[1]))

            return "The subgraph update success"
        except Exception as e:
            print(e)
            return "The subgraph update failed"

    def update_subgraph_by_sql(self, subgraph_name, dict, sql, type, attrType):
        """
        更新子图
        """
        def insert_subgraph_origin_data(stype):
            if stype == "vertexes":
                exec_sql = "select l.* from " + dict["db"] + "." + dict[
                    "table"] + " as l join (" + sql + ") as r on l." + dict["id"] + "=r.id"
            else:
                exec_sql = "select l.* from " + dict["db"] + "." + dict[
                    "table"] + " as l join (" + sql + ") as r on (l." + dict["src"] + " = r.src and l." + dict[
                               "dst"] + "= r.dst and l." + dict["rank"] + " = r.rank)"

            logger.info("[update_subgraph_by_sql] sql: {}".format(exec_sql))
            exec_sql = sql_replace_handler.deal_sql(exec_sql)
            logger.info("[update_subgraph_by_sql] is_cluster:{}    sql: {}".format(cluster_config.is_cluster, exec_sql))

            res = self.client.query_dataframe(exec_sql)
            column_fileds = res.columns.values
            target_field_list_con = ",".join(column_fileds)
            logger.info("[update_subgraph_by_sql] target_field_list_con: {}".format(target_field_list_con))

            col_list = [
                list(pd.to_datetime(res[col])) if str(res[col].dtype) == "datetime64[ns]" else list(res[col].values) for
                col in res.columns]

            if target_field_list_con:
                try:
                    prefix_sql = "insert into " + db_table + " (" + target_field_list_con + ") values"
                    logger.info("[update_subgraph_by_sql] sql: {}".format(prefix_sql))

                    self.client.execute(prefix_sql, col_list, columnar=True)
                except Exception as exc:
                    raise ValueError("update subgraph failed. errMsg:{}".format(str(exc)))

            return col_list, column_fileds

        db_table = self.__gen_table_name(subgraph_name, dict.get("table"))
        if type not in ["vertexes", "edges"]:
            raise ValueError("update subgraph failed. type not in (vertexes, edges).")

        col_list, column_fields = insert_subgraph_origin_data(type)
        total_num = 0
        if type == "vertexes":
            edge_infos = self.graph_cfg.get("edges") or {}
            try:
                tem = self.client.execute("select count(1) from " + db_table)
                total_num += tem[0][0]
                for edge_info in edge_infos:
                    if (edge_infos[edge_info]["src_type"] == attrType) and (
                            edge_infos[edge_info]["dst_type"] == attrType):
                        src_db_table_new = self.__gen_table_name(subgraph_name, edge_infos[edge_info]["table"])
                        src_db_table_old = self.__gen_table_name(dict["db"], edge_infos[edge_info]["table"])

                        insert_sql = "insert into " + src_db_table_new + " (*) select * from " + src_db_table_old + " where " +\
                            edge_infos[edge_info]["src"] + " in " + tostr(
                                col_list[np.where(column_fields == dict["id"])[0][0]]) +\
                            " and " + edge_infos[edge_info]["dst"] + " in " + tostr(col_list[np.where(column_fields == dict["id"])[0][0]])
                        logger.info("[update_subgraph_by_sql] sql: {}     type:{}".format(insert_sql, type))

                        self.client.execute(insert_sql)
                        tem = self.client.execute("select count(1) from " + src_db_table_new)
                        total_num += tem[0][0]
                        logger.info(src_db_table_new + "======>The subgraph update success")
            except Exception as e:
                logger.error("The subgraph update failed. errMsg: {}".format(str(e)))
                raise ValueError("update subgraph failed.")
        elif type == "edges":
            try:
                tem = self.client.execute("select count(1) from " + db_table)
                total_num += tem[0][0]

                for _type in ["src_type", "dst_type"]:
                    src_info = self.graph_cfg.get("vertexes", {}).get(dict[_type])
                    src_db_table_new = self.__gen_table_name(subgraph_name, src_info["table"])
                    src_db_table_old = self.__gen_table_name(dict["db"], src_info["table"])

                    if _type == "src_type":
                        in_id_value = tostr(col_list[np.where(column_fields == dict["src"])[0][0]])
                    else:
                        in_id_value = tostr(col_list[np.where(column_fields == dict["dst"])[0][0]])

                    insert_src_sql = "insert into " + src_db_table_new + " (*) select * from " + src_db_table_old + " where " + \
                                     src_info["id"] + " in " + in_id_value
                    logger.info("[update_subgraph_by_sql]  insert_sql:{}     type:{}".format(insert_src_sql, type))
                    self.client.execute(insert_src_sql)

                    tem = self.client.execute("select count(1) from " + src_db_table_new)
                    total_num += tem[0][0]

                logger.info("The subgraph update success")
            except Exception as e:
                logger.error("The subgraph update failed. errMsg: {}".format(str(e)))
                raise ValueError("The subgraph update failed")

        if total_num > 50000:
            logger.error("The subgraph size is too big. total num {}".format(total_num))
            raise ValueError("The subgraph size is too big")

    def update_subgraph_by_find_path_multi_edge(self,
                                                db,
                                                main_graph,
                                                subgraph_name,
                                                start_vertex_list,
                                                end_vertex_list,
                                                edge_name_list,
                                                edge_con_list_list,
                                                step_limit):
        main_db = self.graph_cfg["edges"][edge_name_list[0]]["db"]
        res = self.find_path_multi_edge(start_vertex_list, end_vertex_list,
                                        edge_name_list, edge_con_list_list,
                                        None, step_limit)

        self.use_graph(subgraph_name, db)
        for i in range(len(res)):
            if i == 0:  # path of length 1
                for k in range(len(edge_name_list)):
                    if res[i][k].shape[0] == 0:
                        continue
                    edge_info = self.graph_cfg["edges"][edge_name_list[k]]
                    db_table = subgraph_name + "." + edge_info["table"]
                    target_field_list_con = edge_info["src"] + "," + edge_info["dst"] + "," + edge_info["rank"] + ","\
                                            + ",".join(edge_info["fields"])
                    # TODO: list hurts performance and increases memory cost
                    # datetime64[ns] patch
                    # col_list = [list(res[i][k][col].values) for col in res[i][k].columns]
                    col_list = [
                        list(pd.to_datetime(res[i][k][col])) if str(res[i][k][col].dtype) == "datetime64[ns]" else list(
                            res[i][k][col].values) for col in res[i][k].columns]
                    self.client.execute("insert into " + db_table + " (" + target_field_list_con + ") values", col_list,
                                        columnar=True)
                    src_info = self.graph_cfg["vertexes"][edge_info["src_type"]]
                    src_db_table_new = subgraph_name + "." + src_info["table"]
                    src_db_table_old = main_db + "." + src_info["table"]
                    src_target_field_list_con = src_info["id"] + "," + ",".join(src_info["fields"])
                    self.client.execute(
                        "insert into " + src_db_table_new + " (" + src_target_field_list_con + ") select distinct " + src_target_field_list_con + " from " + src_db_table_old + " where " +
                        src_info["id"] + " in " + tostr(col_list[0]))
                    dst_info = self.graph_cfg["vertexes"][edge_info["dst_type"]]
                    dst_db_table_new = subgraph_name + "." + dst_info["table"]
                    dst_db_table_old = main_db + "." + dst_info["table"]
                    dst_target_field_list_con = dst_info["id"] + "," + ",".join(dst_info["fields"])
                    self.client.execute(
                        "insert into " + dst_db_table_new + " (" + dst_target_field_list_con + ") select distinct " + dst_target_field_list_con + " from " + dst_db_table_old + " where " +
                        dst_info["id"] + " in " + tostr(col_list[1]))

            else:  # path of length >=2
                for j in range(len(res[i])):
                    for k in range(len(edge_name_list)):
                        if res[i][j][k].shape[0] == 0:
                            continue
                        edge_info = self.graph_cfg["edges"][edge_name_list[k]]
                        db_table = subgraph_name + "." + edge_info["table"]
                        target_field_list_con = edge_info["src"] + "," + edge_info["dst"] + "," + edge_info["rank"]\
                                + "," + ",".join(edge_info["fields"])
                        # TODO: list hurts performance and increases memory cost
                        # datetime64[ns] patch
                        # col_list = [list(res[i][j][k][col].values) for col in res[i][j][k].columns]
                        col_list = [list(pd.to_datetime(res[i][j][k][col])) if str(
                            res[i][j][k][col].dtype) == "datetime64[ns]" else list(res[i][j][k][col].values) for col in
                                    res[i][j][k].columns]
                        self.client.execute("insert into " + db_table + " (" + target_field_list_con + ") values",
                                            col_list, columnar=True)
                        src_info = self.graph_cfg["vertexes"][edge_info["src_type"]]
                        src_db_table_new = subgraph_name + "." + src_info["table"]
                        src_db_table_old = main_db + "." + src_info["table"]
                        src_target_field_list_con = src_info["id"] + "," + ",".join(src_info["fields"])
                        self.client.execute(
                            "insert into " + src_db_table_new + " (" + src_target_field_list_con + ") select " + src_target_field_list_con + " from " + src_db_table_old + " where " +
                            src_info["id"] + " in " + tostr(col_list[0]))
                        dst_info = self.graph_cfg["vertexes"][edge_info["dst_type"]]
                        dst_db_table_new = subgraph_name + "." + dst_info["table"]
                        dst_db_table_old = main_db + "." + dst_info["table"]
                        dst_target_field_list_con = dst_info["id"] + "," + ",".join(dst_info["fields"])
                        self.client.execute(
                            "insert into " + dst_db_table_new + " (" + dst_target_field_list_con + ") select " + dst_target_field_list_con + " from " + dst_db_table_old + " where " +
                            dst_info["id"] + " in " + tostr(col_list[1]))
        return res

    #############################################
    #################### vertex/edge-wise operation: metric
    #############################################
    ## metric_indegree returns indegree of vertices (df)
    ## vertices without in-edge will be ignored
    def metric_indegree(self, edge_name, if_sort=False, topk=-1):

        if edge_name not in self.graph_cfg["edges"]:
            logger.warning("invalid edge: " + edge_name)
            return "invalid edge: " + edge_name

        edge_info = self.graph_cfg["edges"][edge_name]
        db_table = edge_info["db"] + "." + edge_info["table"]

        qualifier = ""
        if if_sort:
            qualifier += " order by indegree desc"
        if topk > 0:
            qualifier += " limit " + str(topk)

        sql = "select " + edge_info["dst"] + ", count(*) as indegree from " + db_table + " group by " + edge_info[
            "dst"] + qualifier
        logger.info("sql: " + sql)
        res = self.client.query_dataframe(sql)
        return res.to_dict()

    ## metric_outdegree returns outdegree of vertices (df)
    ## vertices without out-edge will be ignored
    def metric_outdegree(self, edge_name, if_sort=False, topk=-1):

        if edge_name not in self.graph_cfg["edges"]:
            logger.warning("invalid edge: " + edge_name)
            return "invalid edge: " + edge_name

        edge_info = self.graph_cfg["edges"][edge_name]
        db_table = edge_info["db"] + "." + edge_info["table"]

        qualifier = ""
        if if_sort:
            qualifier += " order by outdegree desc"
        if topk > 0:
            qualifier += " limit " + str(topk)

        sql = "select " + edge_info["src"] + ", count(*) as outdegree from " + db_table + " group by " + edge_info[
            "src"] + qualifier
        logger.info("sql: " + sql)
        res = self.client.query_dataframe(sql)
        return res.to_dict()

    ## metric_degree returns degree of vertices (df)
    ## vertices without edge will be ignored
    def metric_degree(self, edge_name, if_sort=False, topk=-1):

        if edge_name not in self.graph_cfg["edges"]:
            logger.warning("invalid edge: " + edge_name)
            return

        edge_info = self.graph_cfg["edges"][edge_name]
        db_table = edge_info["db"] + "." + edge_info["table"]

        qualifier = ""
        if if_sort:
            qualifier += " order by degree desc"
        if topk > 0:
            qualifier += " limit " + str(topk)

        sql_o = "select " + edge_info["src"] + " as vid, count(*) as degree from " + db_table + " group by " + \
                edge_info["src"]
        sql_i = "select " + edge_info["dst"] + " as vid, count(*) as degree from " + db_table + " group by " + \
                edge_info["dst"]
        sql = "select vid, sum(degree) as degree from (" + sql_o + " union all " + sql_i + ") group by vid" + qualifier
        logger.info("sql: " + sql)
        res = self.client.query_dataframe(sql)
        return res.to_dict()

    ## TODO
    ## metric_pagerank returns pagerank of vertices
    ## vertices without edge will be ignored
    def metric_pagerank(self, edge_name, d=0.85, num_iter=10, if_sort=False, topk=-1):

        if edge_name not in self.graph_cfg["edges"]:
            logger.warning("invalid edge: " + edge_name)
            return

        edge_info = self.graph_cfg["edges"][edge_name]
        db_table = edge_info["db"] + "." + edge_info["table"]

        qualifier = ""
        if if_sort:
            qualifier += " order by outdegree desc"
        if topk > 0:
            qualifier += " limit " + str(topk)

        sql = "select " + edge_info["src"] + "," + edge_info["dst"] + ",outdegree from (select " + edge_info[
            "src"] + ",count(*) as outdegree from " + db_table + " group by " + edge_info[
                  "src"] + ") as table_od join " + db_table + " using " + edge_info["src"] + qualifier

        logger.info("[metric_pagerank] sql: {}".format(sql))
        res = self.client.query_dataframe(sql)
        return res.to_dict()

    def vertex_match_property(self, vertex_id_list, vertex_name, vertex_con_list, target_field_list, page,
                              page_size, data_type="df"):
        propertys = self.graph_cfg["vertexes"]
        table_property = propertys[vertex_name]
        db_table = table_property["db"] + "." + table_property["table"]
        target_field_list_con = table_property["id"]
        if not target_field_list:
            table_fields = table_property["fields"]
            if table_fields:
                target_field_list_con += "," + ",".join(table_fields)
        else:
            target_field_list_con += "," + ",".join(target_field_list)

        vertex_con_list_con = " where " + table_property["id"] + " in " + tostr(vertex_id_list)
        if vertex_con_list is not None and len(vertex_con_list) > 0:
            vertex_con_list_con += " and " + " and ".join(vertex_con_list)

        num = self.client.execute("select count(1) from " + db_table + vertex_con_list_con)
        count = num[0][0]
        if page and page_size:
            vertex_con_list_con = vertex_con_list_con + " limit " + str(page_size * (page - 1)) + "," + str(page_size)

        sql = "select DISTINCT " + target_field_list_con + " from " + db_table + vertex_con_list_con
        logger.info("[vertex_match_property]  select sql: {}".format(sql))

        res = deal_query_result_with_paging(data_type, self.client, sql, page, page_size, count)
        return res

    def edge_match_property(self, start_vertex_list, end_vertex_list, edge_name, edge_con_list, target_field_list, page,
                            page_size,
                            data_type="df"):
        propertys = self.graph_cfg["edges"]
        table_property = propertys[edge_name]
        db_table = table_property["db"] + "." + table_property["table"]
        target_field_list_con = table_property["src"] + "," + table_property["dst"] + "," + table_property["rank"]
        if target_field_list is None or len(target_field_list) == 0:
            target_field_list_con += "," + ",".join(table_property["fields"])
        elif len(target_field_list) > 0:
            target_field_list_con += "," + ",".join(target_field_list)
        edge_con_list_con = " where " + table_property["src"] + " in " + tostr(start_vertex_list) + " and " \
                            + table_property["dst"] + " in " + tostr(end_vertex_list)
        if edge_con_list is not None and len(edge_con_list) > 0:
            edge_con_list_con += " and " + " and ".join(edge_con_list)

        num = self.client.execute(
            "select count(1) from ( select  distinct " + table_property["src"] + "," + table_property["dst"] + "," + table_property["rank"] + " from " + db_table + edge_con_list_con + " ) " )
        count = num[0][0]
        if page is not None and page_size is not None:
            edge_con_list_con = edge_con_list_con + " limit " + str(page_size * (page - 1)) + "," + str(page_size)

        sql = "select DISTINCT " + target_field_list_con + " from " + db_table + edge_con_list_con
        res = deal_query_result_with_paging(data_type, self.client, sql, page, page_size, count)
        return res

    # query_vertex returns distinct vertexes which satisfy constraints (df)
    def query_vertexes(self,
                       vertex_name,
                       vertex_con_list,
                       target_field_list,
                       data_type="list"):

        if vertex_name not in self.graph_cfg["vertexes"]:
            logger.warning("invalid vertex: " + vertex_name)
            return

        vertex_info = self.graph_cfg["vertexes"][vertex_name]
        db_table = vertex_info["db"] + "." + vertex_info["table"]

        vertex_con_list_con = ""
        if vertex_con_list is not None and vertex_con_list != ['']:
            vertex_con_list_con = " where " + " and ".join(vertex_con_list)

        target_field_list_con = vertex_info["id"]
        if target_field_list is None or target_field_list == ['']:
            target_field_list_con = "*"
        elif len(target_field_list) > 0:
            target_field_list_con += "," + ",".join(target_field_list)

        sql = "select distinct " + target_field_list_con + " from " + db_table + vertex_con_list_con
        sql = sql_replace_handler.deal_sql(sql)
        logger.info("[query_vertexes] is_cluster:{}    sql: {} ".format(cluster_config.is_cluster, sql))

        res = deal_query_result(data_type, self.client, sql)

        return res

    # query_edge returns distinct edges which satisfy constraints (df)
    def query_edges(self,
                    edge_name,
                    edge_con_list,
                    target_field_list,
                    data_type="list"):

        if edge_name not in self.graph_cfg["edges"]:
            logger.warning("invalid edge: " + edge_name)
            return

        edge_info = self.graph_cfg["edges"][edge_name]
        db_table = edge_info["db"] + "." + edge_info["table"]

        edge_con_list_con = ""
        if edge_con_list is not None and edge_con_list != ['']:
            edge_con_list_con = " where " + " and ".join(edge_con_list)

        target_field_list_con = edge_info["src"] + "," + edge_info["dst"]
        if target_field_list is None or target_field_list == ['']:
            target_field_list_con = "*"
            # target_field_list_con += "," + ",".join(edge_info["fields"])
        elif len(target_field_list) > 0:
            target_field_list_con += "," + ",".join(target_field_list)

        sql = "select distinct " + target_field_list_con + " from " + db_table + edge_con_list_con
        logger.info("[query_edges] is_cluster:{}     sql: {}".format(cluster_config.is_cluster, sql))
        res = deal_query_result(data_type, self.client, sql)
        return res

    def count_edge_by_time(self, edge_name, edge_con_list, time_field, time_dimention='Day', data_type='df'):
        edge_info = self.graph_cfg["edges"][edge_name]
        db_table = edge_info["db"] + "." + edge_info["table"]

        edge_con_list_con = ""
        if edge_con_list is not None and len(edge_con_list) > 0:
            edge_con_list_con = " where " + " and ".join(edge_con_list)

        sub_sql = "select distinct * from " + db_table + edge_con_list_con
        sql = "select A." + time_field + ", count() from " + "(" + sub_sql + ")" + " as A GROUP BY A." + time_field
        if time_dimention == 'Minute':
            sql = "select toStartOfMinute(A." + time_field + ") as Minute, count() from " + "(" + sub_sql + ")" + " as A GROUP BY Minute"
        elif time_dimention == 'Hour':
            sql = "select toStartOfHour(A." + time_field + ") as Hour, count() from " + "(" + sub_sql + ")" + " as A GROUP BY Hour"
        elif time_dimention == 'Day':
            sql = "select formatDateTime(A." + time_field + ",'%F') as Day, count() from " + "(" + sub_sql + ")" + " as A GROUP BY Day"
        elif time_dimention == 'Month':
            sql = "select toStartOfMonth(A." + time_field + ") as Month, count() from " + "(" + sub_sql + ")" + " as A GROUP BY Month"
        elif time_dimention == 'Year':
            sql = "select formatDateTime(A." + time_field + ",'%Y') as Year, count() from " + "(" + sub_sql + ")" + " as A GROUP BY Year"

        print(sql)
        res = deal_query_result_sample_plus(data_type, self.client, sql)
        return res

    def create_database(self, subgraph_name, is_cluster, cluster_name):
        """
        创建数据库
        """
        if is_cluster and not cluster_name:
            return False, "cluster name is None"

        if not is_cluster:
            sql = "create database if not exists " + subgraph_name
        else:
            sql = "create database if not exists " + subgraph_name + " on cluster " + cluster_name

        logger.info("[create_database] sql: {}".format(sql))

        try:
            self.client.execute(sql)
        except Exception as e:
            err_msg = "database {} create error. sql: {}     errMsg: {}".format(subgraph_name, sql, str(e))
            return False, err_msg

        return True, ''

    @staticmethod
    def __gen_table_name(prefix, suffix, mid="."):
        return "{}{}{}".format(prefix, mid, suffix)

    def create_subgraph_table(self, graph_type, subgraph_name, edge_or_vertex_info, is_cluster, cluster_name):
        """
        创建子图里的表
        """
        table_name = edge_or_vertex_info.get("table")
        old_table_name = self.__gen_table_name(edge_or_vertex_info.get("db"), table_name)
        if not is_cluster:
            new_table_name = self.__gen_table_name(subgraph_name, table_name)
            sql = "create table " + new_table_name + " as " + old_table_name
            self.client.execute(sql)
        else:
            table_schema_sql = "show create table " + old_table_name
            query = self.client.execute(table_schema_sql)
            if len(query) == 0:
                raise ValueError("query origin table schema failed")
            else:
                table_schema_str = query[0][0]

            handler = SqlMergeHandler(graph_type, subgraph_name, edge_or_vertex_info, cluster_name)
            # 创建本地表
            sql = handler.gen_create_table_sql(table_schema_str)
            logger.info("local table sql: {}".format(sql))
            self.client.execute(sql)

            # 创建分区表
            sql = handler.gen_create_table_sql(table_schema_str, True)
            logger.info("distributed table sql: {}".format(sql))
            self.client.execute(sql)

    def single_create_table_sql(self, table_name):
        """
        拼接single SQL
        """
        # 字段
        columns_str = "(\n    `id` String,\n   " \
                      " `task_id` String,\n    " \
                      " `id_type` String,\n    " \
                      "`graph_algorithm_type` Float64,\n   " \
                      " `val` String,\n    " \
                      "`create_time` DateTime64(3) DEFAULT now() CODEC(DoubleDelta, LZ4)\n)\n"
        engine_str = "ENGINE = MergeTree"
        order_by_str = "order by id"
        sql = "create table if not exists " + table_name + columns_str + \
              engine_str + order_by_str + " SETTINGS index_granularity = 8192"
        return sql
    def create_subgraph_ext_table(self, graph_type, subgraph_name, edge_or_vertex_info, is_cluster, cluster_name):
        """
        创建子图额外属性的表
        """
        table_name = "calculation_attribute"
        edge_or_vertex_info["table"] = table_name
        if not is_cluster:
            new_table_name = self.__gen_table_name(subgraph_name, table_name)
            sql = self.single_create_table_sql(new_table_name)
            self.client.execute(sql)
        else:
            table_schema_str = "(\n    id String,\n   " \
                      " id_type String,\n    " \
                      " task_id String,\n    " \
                      " graph_algorithm_type String,\n   " \
                      " val Float64,\n    " \
                      " create_time DateTime64(3) DEFAULT now() CODEC(DoubleDelta, LZ4)\n)\n"
            handler = SqlMergeHandler(graph_type, subgraph_name, edge_or_vertex_info, cluster_name)
            # 创建本地表
            sql = handler.gen_create_new_table_sql(table_schema_str)
            logger.info("local table sql: {}".format(sql))
            self.client.execute(sql)

            # 创建分区表
            sql = handler.gen_create_new_table_sql(table_schema_str, True)
            logger.info("distributed table sql: {}".format(sql))
            self.client.execute(sql)


