"""
拼接sql
"""


class SqlMergeHandler(object):
    def __init__(self, graph_type, subgraph_name, edge_or_vertex_info, cluster_name=''):
        """
        graph_type: 边表还是顶点表
        is_distributed_table: true/false  分区表/本地表
        """
        self.graph_type = graph_type
        self.edge_or_vertex_info = edge_or_vertex_info
        self.cluster_name = cluster_name
        self.subgraph_name = subgraph_name

        self.table_name = self.__get_table_name_from_graph_config()  # 分区表的表名
        self.local_table_name = self.__get_local_table_name()  # 本地表的表名
        self.order_by_fields = self.__get_order_by_fields()

        if not self.table_name or not self.local_table_name:
            raise ValueError("SqlMergeHandler init failed")

        if not cluster_name:
            raise ValueError("cluster name is NULL")

    def __get_table_name_from_graph_config(self):
        table_name = self.edge_or_vertex_info.get("table")
        return "{}.{}".format(self.subgraph_name, table_name)

    def __get_order_by_fields(self):
        if self.graph_type == "edges":
            keys = ["src", "dst", "rank"]
        else:
            keys = ["id"]

        order_by_fields = [self.edge_or_vertex_info.get(item) for item in keys]
        return order_by_fields

    def __get_local_table_name(self):
        return self.table_name + '_shard'

    def get_table_fields_and_types_from_schema(self, table_schema_str):
        """
        获取表的所有字段和字段类型
        """
        start, end = 0, 0
        sentences = table_schema_str.split('\n')
        for idx, item in enumerate(sentences):
            field_types = item.split()
            if len(field_types) >= 2:
                field_name = field_types[0]
                field_type = field_types[1]
                if 'Nullable' in field_type:
                    field_name = field_name.replace("`", "")
                    if field_name in self.order_by_fields:
                        new_field_type = field_type.replace("Nullable(", "").replace(")", "")
                        field_types[1] = new_field_type
                        new_item = ' '.join(field_types)
                        sentences[idx] = new_item

            if item == "(":
                start = idx

            if item == ")":
                end = idx

            if item.startswith("ENGINE"):
                break

        fields_and_types_str = ''.join(sentences[start:end + 1])
        return fields_and_types_str

    # def get_table_fields_and_types(self):
    #     """
    #     封装字段和类型
    #     """
    #     sql_schema = "(\n    `id` Nullable(String),\n   " \
    #     " `task_id` Nullable(String),\n    " \
    #     "`graph_algorithm_type` Nullable(String),\n   " \
    #     " `val` Nullable(String),\n    " \
    #     "`create_time` DateTime64(3) DEFAULT now() CODEC(DoubleDelta, LZ4)\n)\n"

        # return sql_schema

    def get_cluster_table_engine(self, is_distributed_table):
        """
        Distributed(cluster_name, database, table, [sharding_key])
        """
        engine_str = "ENGINE = "
        names = self.local_table_name.split(".")
        table_name = names[1]
        if not is_distributed_table:
            engine_str += "ReplicatedMergeTree('/clickhouse/tables/" + self.local_table_name + "/{shard}', " \
                                                                                               "'{replica}')"
        else:
            engine_str += "Distributed(" + self.cluster_name + ", " + self.subgraph_name + ", " + table_name \
                + ", rand())"

        return engine_str

    def get_single_table_engine(self):
        """
        single engine
        """
        engine_str = "ENGINE = MergeTree"
        return engine_str

    def get_table_order_by_fields(self):
        order_by_fields = self.order_by_fields
        return " order by ({})".format(",".join(order_by_fields))

    def merge_sql_create_table(self, is_distributed_table, columns_str, engine_str, order_by_str):
        """
        合并建表语句
        """
        if not is_distributed_table:
            sql = "create table if not exists " + self.local_table_name + " on cluster " + self.cluster_name + columns_str + \
                  engine_str + order_by_str + " SETTINGS index_granularity = 8192"
        else:
            sql = "create table if not exists " + self.table_name + " on cluster " + self.cluster_name + ' as ' + \
                  self.local_table_name + " " + engine_str

        return sql


    def merge_single_sql_create_table(self, columns_str, engine_str, order_by_str):
        """
        合并建表语句
        """
        sql = "create table if not exists " + self.table_name + columns_str + \
               engine_str + order_by_str + " SETTINGS index_granularity = 8192"
        return sql


    def gen_create_table_sql(self, table_schema_str, is_distributed_table=False):
        """
        拼接集群sql
        """
        columns_str = self.get_table_fields_and_types_from_schema(table_schema_str)
        engine_str = self.get_cluster_table_engine(is_distributed_table)
        order_by_str = self.get_table_order_by_fields()
        sql = self.merge_sql_create_table(is_distributed_table, columns_str, engine_str, order_by_str)
        return sql

    def gen_create_new_table_sql(self, table_schema_str, is_distributed_table=False):
        """
        拼接集群sql
        """
        columns_str = self.get_table_fields_and_types_from_schema(table_schema_str)
        engine_str = self.get_cluster_table_engine(is_distributed_table)
        order_by_str = " order by (id)"
        sql = self.merge_sql_create_table(is_distributed_table, columns_str, engine_str, order_by_str)
        return sql




if __name__ == "__main__":
    sql_schema = "CREATE TABLE sub_graph_test_2.default_metagroups\n(\n    `group_id` Nullable(String),\n   " \
                 " `group_name` Nullable(String),\n    `num_members` Nullable(Int64),\n    " \
                 "`category_id` Nullable(String),\n    `category_name` Nullable(String),\n   " \
                 " `organizer_id` Nullable(String),\n    `group_urlname` Nullable(String),\n    " \
                 "`_time` DateTime64(3) DEFAULT now() CODEC(DoubleDelta, LZ4)\n)\nENGINE = MergeTree\n" \
                 "ORDER BY _time\nSETTINGS index_granularity = 8192"

    info = {
            "db":"sub_graph_test_2",
            "table":"default_metagroups",
            "id":"group_id",
            "label":"group_name",
            "type":"group",
            "id_data_type":"String",
            "fields":[
                "group_name",
                "num_members",
                "category_id",
                "category_name",
                "organizer_id",
                "group_urlname"
            ],
            "types":[
                "String",
                "Num",
                "String",
                "String",
                "String",
                "String"
            ]
        }
    handler = SqlMergeHandler("vertexes", "subgraph_test_11", info,
                              cluster_name="cluster_2shards_2replicas")
    sql = handler.gen_create_table_sql(sql_schema)
    print("local table sql: {}\n".format(sql))

    sql = handler.gen_create_table_sql(sql_schema, True)
    print("distribute table sql: {}\n".format(sql))
#     """-- auto-generated definition
# create table xiqianedge
# (
#     record_date    DateTime64(3),
#     record_time    DateTime64(3),
#     tran_id        Nullable(String),
#     orig_acct      Nullable(String),
#     bene_acct      Nullable(String),
#     tx_type        Nullable(String),
#     base_amt       Nullable(Float32),
#     tran_timestamp Nullable(String),
#     is_sar         Nullable(String),
#     alert_id       Nullable(String),
#     _time          DateTime64(3) alias record_time
# )
#     engine = MergeTree ORDER BY record_date
#         SETTINGS index_granularity = 8192;"""

