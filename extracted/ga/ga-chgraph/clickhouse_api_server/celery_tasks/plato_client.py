"""
plato调用客户端
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import datetime
import subprocess
import pandas as pd
import psycopg2

from config.logger_design import get_logger
from config.config import plato_config
from config.data_load_config import load_config

from utils.common import unzip_file

logger = get_logger()


class PlatoException(Exception):
    pass


class PlatoClient(object):
    def __init__(self, sub_graph, task_id, calculation_type):
        """
        :param sub_graph: 子图名称
        """
        global_config = load_config()
        db = global_config.get("db")
        ck_client = global_config.get("graphClient")

        self.sub_graph = sub_graph
        self.db = db
        self.ck_client = ck_client
        self.task_id = task_id
        self.calculation_type = calculation_type
        self.current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.output_file_dir = self.get_output_file_dir()

    def get_sub_graph_config(self):
        graph_config = self.db.use_tables(self.sub_graph)
        self.sub_graph_config = graph_config

    def get_output_file_dir(self):
        parent_dir = self.current_dir
        output_file_dir = os.path.join(parent_dir, 'output/')
        if not os.path.exists(output_file_dir):
            os.mkdir(output_file_dir)

        return output_file_dir

    @staticmethod
    def gen_calculation_config(cal_type, input_file, output_file):
        """
        图算法配置
        """
        calculation_config = {
            "Pagerank": {
                "param_list": ["ROOT_DIR", "WNUM", "WCORES", "INPUT", "OUTPUT", "IS_DIRECTED",
                              "EPS", "DAMPING", "ITERATIONS"],
                "value_list": [plato_config.plato_install_path, "4", "4", input_file, output_file, "false",
                               "0.0001", "0.85", "100"],
                "shell": "run_pagerank_local.sh"
            },
            "Betweenness": {
                "param_list": ["ROOT_DIR", "WNUM", "WCORES", "INPUT", "OUTPUT", "IS_DIRECTED",
                               "ALPHA", "PART_BY_IN", "CHOSEN", "MAX_ITERATION", "CONSTANT"],
                "value_list": [plato_config.plato_install_path, "4", "4", input_file, output_file, "true",
                               "-1", "false", "-1", "0", "2"],
                "shell": "run_bnc_local.sh"
            },
            "Closeness": {
                "param_list": ["ROOT_DIR", "WNUM", "WCORES", "INPUT", "OUTPUT", "IS_DIRECTED",
                               "ALPHA", "PART_BY_IN", "NUM_SAMPLES"],
                "value_list": [plato_config.plato_install_path, "4", "4", input_file, output_file, "true",
                               "-1", "false", "10"],
                "shell": "run_cnc_local.sh"
            }
        }

        return calculation_config.get(cal_type)

    def get_edge_infos(self):
        edges = []
        edge_config = self.sub_graph_config.get("edges") or {}
        for edge_name, info in edge_config.items():
            edges.append(info)
        self.edges = edges

    def get_vertex_infos(self):
        vertex_config = self.sub_graph_config.get("vertexes") or {}
        self.vertexes = vertex_config

    def get_vertexes_data(self, table_name, field_name):
        """
        从clickhouse中获取顶点数据
        """
        logger.info("[PlatoClient]-[get_vertexes_data]  table_name:{}    field_name:{}".format(table_name,
                                                                                        field_name))
        sql = "select distinct " + field_name + " from " + table_name + " order by " + field_name
        df = self.ck_client.query_dataframe(sql)
        if df.empty:
            return []
        columns = df.columns.tolist()
        vertexs = df[columns[0]].tolist()
        return vertexs

    @staticmethod
    def mapping_vertexes(start=0, vertexes=None):
        """
        处理顶点数据
        """
        vertexes_map = {}
        for item in vertexes or []:
            vertexes_map[item] = start
            start += 1
        return start, vertexes_map

    def get_edges_data(self, table_name, field_names):
        field_names_str = ','.join(field_names)
        sql = "select distinct " + field_names_str + " from " + table_name
        logger.info("[get_edges_data] sql: {}".format(sql))

        df = self.ck_client.query_dataframe(sql)
        if df.empty:
            return []

        data = []
        df = df.sort_values(by=field_names)
        df = df[field_names[0:2]]
        for record in df.to_records(index=False):
            data.append(record.tolist())

        return data

    @staticmethod
    def mapping_edges(edges, vertexes_map, vertex_types):
        if list(vertexes_map.keys()) != vertex_types:
            logger.error("映射边数据错误: vertex_types:{}   vertexes_map.keys:{} ".format(vertex_types,
                                                                    vertexes_map.keys()))
            raise PlatoException("映射边数据错误.")
        data = []
        for (src, dist) in edges:
            src_idx = vertexes_map.get(vertex_types[0]).get(src)    # 注意df中src的指的类型
            if src_idx is None:
                raise PlatoException("边数据替换报错：起点{}找不到对应的下标".format(src))
            dist_idx = vertexes_map.get(vertex_types[0]).get(dist) if len(vertex_types) == 1 else\
                                           vertexes_map.get(vertex_types[1]).get(dist)
            if dist_idx is None:
                raise PlatoException("边数据替换报错：终点{}找不到对应的下标".format(dist))

            data.append([src_idx, dist_idx])

        return data

    def get_vertexes_mapping_data(self, edge_info):
        """
        获取映射后的顶点数据
        """
        vertexes_map = {}
        db_name = edge_info.get("db")
        src_type = edge_info.get("src_type")
        dst_type = edge_info.get("dst_type")
        if src_type == dst_type:
            vertex_types = ["src_type"]
        else:
            vertex_types = ["src_type", "dst_type"]

        start = 0
        for _type in vertex_types:
            vertex_type = edge_info.get(_type)
            if vertex_type not in vertexes_map:
                vertexes_map[vertex_type] = {}

            vertex_table_name = self.vertexes.get(vertex_type, {}).get("table")
            full_table_name = "{}.{}".format(db_name, vertex_table_name)
            src_field_name = self.vertexes.get(vertex_type, {}).get("id")

            vertexes_data = self.get_vertexes_data(full_table_name, src_field_name)
            _start, vertexes_idx_data = self.mapping_vertexes(start, vertexes_data)
            start = _start
            vertexes_map[vertex_type].update(vertexes_idx_data)

        return vertexes_map

    def get_edge_mapping_data(self, edge_info, vertex_idx_data):
        """
        把边的定点数据进行映射
        :param edge_info: {"dst":"", "src":"", "table":"", "db":""}
        :param vertex_idx_data: {"group":{"定点ID"：0， "定点ID"：1， "定点ID"：2}, "friend":{}}
        """
        db_name = edge_info.get("db")
        table_name = edge_info.get("table")
        table_name = "{}.{}".format(db_name, table_name)

        field_names = []
        for field in ["src", "dst", "rank"]:
            field_names.append(edge_info.get(field))

        vertex_types = []
        for field in ["src_type", "dst_type"]:
            val = edge_info.get(field)
            if val not in vertex_types:
                vertex_types.append(val)

        edge_data = self.get_edges_data(table_name, field_names)
        edge_idx_data = self.mapping_edges(edge_data, vertex_idx_data, vertex_types)
        return edge_idx_data

    def write_to_csv(self, edge_data):
        """
        把映射后的边数据写入到csv文件中，只包含起点和终点
        """
        output_file_name = "{}_{}_input.csv".format(str(self.task_id).replace("-", ""),
                                                    self.calculation_type.lower())
        output_file_path = os.path.join(self.output_file_dir, output_file_name)
        df = pd.DataFrame(edge_data)
        df.to_csv(output_file_path, header=False, index=False)

        logger.info("write to csv success !!!  file_path:{}".format(output_file_path))
        return output_file_path

    def execute_plato(self, edge_info_file):
        """
        调用plato
        """
        output_file_path = os.path.join(self.output_file_dir, '{}/'.format(self.calculation_type))
        cal_config = self.gen_calculation_config(self.calculation_type, edge_info_file,
                                                 output_file_path)
        cal_param_val = cal_config.get("value_list")
        cal_sh_dir = os.path.join(self.current_dir, "shells/plato_shell/")
        cmds = ["bash", "{}{}".format(cal_sh_dir, cal_config.get("shell"))]
        cmds.extend(cal_param_val)
        logger.info("[execute_plato] commands: {}".format(cmds))

        res = subprocess.run(cmds, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        if res.returncode == 0:
            return True, "", output_file_path

        return False, res.stderr, output_file_path

    @staticmethod
    def read_from_csv(file_path):
        file_name = "0003_0000.csv.gz"
        if not os.path.exists(os.path.join(file_path, file_name)):
            raise PlatoException("在{}没有找到文件{}".format(file_path, file_name))
        else:
            unzip_file_path = unzip_file(file_path, file_name)
        df = pd.read_csv(unzip_file_path, names=['A', 'B'])
        data = []
        for record in df.to_records(index=False):
            data.append(record.tolist())

        return data

    def write_to_ck(self, vertex_cal_data, vertex_idx_data):
        """
        将图计算结果写入到clickhouse
        """
        graph_cal_res_table_name = "calculation_attribute"
        idx_vertex_data = {}
        for _type, info in vertex_idx_data.items():
            for vertex_id, idx in info.items():
                idx_vertex_data[idx] = [vertex_id, _type]

        insert_data = []
        table_name = "{}.{}".format(self.sub_graph, graph_cal_res_table_name)
        for (vertex_id, val) in vertex_cal_data:
            new_vertex_id, vertex_type = idx_vertex_data.get(vertex_id)
            if new_vertex_id is None:
                raise PlatoException("写入clickhouse失败. {}对应的顶点不存在".format(vertex_id))
            record = [str(self.task_id), self.calculation_type, str(new_vertex_id), vertex_type, float(val),
                      datetime.datetime.now()]
            insert_data.append(record)

        field_names = "(task_id,graph_algorithm_type,id,id_type, val, create_time)"
        sql = "insert into " + table_name + field_names + " values "
        logger.info("[write_to_ck]  sql: {}".format(sql))
        self.ck_client.execute(sql, insert_data)

    def change_graph_cal_task_status(self, task_status):
        """
        修改图算法对应的任务的状态
        """
        task_table_name = "calculation_state"
        sql = "update " + task_table_name + " set operation_state=" + str(task_status) + "," + \
              "update_time=current_timestamp() where id=" + str(self.task_id) + ";"
        logger.info("[change_graph_cal_task_status] sql:{}".format(sql))

        conn = psycopg2.connect(self.db.url)
        logger.info("[change_graph_cal_task_status] self.db.url:{}".format(self.db.url))

        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()

        conn.close()

    def run(self):
        try:
            self.get_sub_graph_config()
            self.get_edge_infos()
            self.get_vertex_infos()

            if not self.edges:
                raise PlatoException("子图的边类型配置为空. edge_config:{}".format(self.sub_graph_config))

            for edge_info in self.edges:
                vertex_idx_data = self.get_vertexes_mapping_data(edge_info)
                edge_idx_data = self.get_edge_mapping_data(edge_info, vertex_idx_data)
                edge_data_file = self.write_to_csv(edge_idx_data)
                success, err_msg, output_file_path = self.execute_plato(edge_data_file)
                if not success:
                    logger.error("执行图计算shell脚本失败: {}".format(err_msg))
                    raise PlatoException("执行图计算shell脚本失败.")

                vertex_cal_data = self.read_from_csv(output_file_path)
                self.write_to_ck(vertex_cal_data, vertex_idx_data)
        except Exception as exc:
            logger.error("调用plato失败：{}".format(str(exc)))
            success = 2      # 失败
        else:
            success = 1      # 成功
        finally:
            if self.ck_client:
                self.ck_client.disconnect()      # 关闭链接

        self.change_graph_cal_task_status(success)

        logger.info("execute plato completed!!!  task_id:{} ".format(self.task_id))


if __name__ == "__main__":
    client = PlatoClient("7cf53539_81d6_4986_9745_86d2acfc97c6", 7, 'pagerank')
    print("subgraph config: {}\n".format(client.sub_graph_config))

    client.get_edge_infos()
    print("client.edges: {}\n".format(client.edges))

    for edge_info in client.edges:
        print("edge_info:{}\n".format(edge_info))

        vertex_idx_data = client.get_vertexes_mapping_data(edge_info)
        print("vertex_idx_data: {}\n".format(vertex_idx_data))

        edge_idx_data = client.get_edge_mapping_data(edge_info, vertex_idx_data)
        print("edge_idx_data: {}\n".format(edge_idx_data))

        edge_data_file = client.write_to_csv(edge_idx_data)
        success, err_msg, output_file_path = client.execute_plato(edge_data_file)
        print("success:{}    err_msg:{}        output_file_path:{}".format(success, err_msg,
                                                                           output_file_path))
        # output_file_path = os.path.join(client.output_file_dir, 'pagerank/')
        print("output_file_path: ", output_file_path)

        vertex_cal_data = client.read_from_csv(output_file_path)
        print("vertex_cal_data: {}\n".format(vertex_cal_data))

        client.write_to_ck(vertex_cal_data, vertex_idx_data)

        client.change_graph_cal_task_status(1)


