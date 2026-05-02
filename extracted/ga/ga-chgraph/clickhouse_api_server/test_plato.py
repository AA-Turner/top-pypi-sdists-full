from clickhouse_driver import Client
import wirte_file
import run_plato
import os

graph_client = Client(host="tob44.bigdata.lycc.qihoo.net")

sql = "create table default.testxiqianedge  as 0a7b0a48_3b55_4b7c_b620_20a2b081d30e.xiqianedge    engine = MergeTree ORDER BY record_date "
graph_client.execute(sql)

# graph_client = Client(host="sysdae01v.bdg.shbt.qihoo.net", user="default", password="bgdtdauqe")
# res = graph_client.query_dataframe("select orig_acct,bene_acct from  0b0f4551_8ef5_4ebf_8242_5e8fae43fdb2.xiqianedge")
# wirte_file.write_local_file("pagerank.csv",res)
# out_path = os.getcwd() + os.sep + "out"
# if not os.path.exists(out_path):
#     os.mkdir(out_path)
#
# args={"wnum":4,"work_cores":4,"input":os.getcwd() + os.sep + "data"+ os.sep + "pagerank.csv" , "output": out_path}
# params={}
# run_plato.run_pagerank(args,params)