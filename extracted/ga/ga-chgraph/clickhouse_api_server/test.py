from  daos.graph_op import CHGraph
from clickhouse_driver import Client

if __name__ == '__main__':
    info = {"db": "anti_money_launder", "table": "transactions", "type": "transactions", "src": "orig_acct",
            "src_type": "accounts", "src_data_type": "String", "dst": "bene_acct", "dst_type": "accounts",
            "dst_data_type": "String", "rank": "record_time", "rank_data_type": "String",
            "fields": ["record_date", "record_time", "tran_id", "tx_type", "base_amt", "tran_timestamp", "is_sar",
                       "alert_id"],
            "types": ["String", "String", "String", "String", "String", "String", "String", "String"]}
    graph_client = Client(host="p54011v.hulk.shyc2.qihoo.net", port="9001",
                          user="admin",
                          password="cH520BgD")
    graph = CHGraph(graph_client)
    graph.create_subgraph_ext_table("vertexes", "7cf53539_81d6_4986_9745_86d2acfc97c6", info, False, "cluster_2shards_2replicas")