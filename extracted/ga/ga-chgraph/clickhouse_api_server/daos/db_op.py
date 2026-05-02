#!/usr/bin/env python3
"""
Test psycopg with CockroachDB.
"""
import time
import json
import copy
import logging
import psycopg2


# 查询所有图列表
# 查询所有原图列表
# 根据图名查询子图列表
# 根据图名查询schema
def show_graphs(conn, is_source, source_graph_name, graph_name):
    res = []
    con_is_source = ""
    if graph_name is not None and graph_name != '':
        sql = "SELECT graph_create_date,graph_name,graph_cfg,is_source,graph_source FROM name2cfg where graph_status=1 and graph_name=\'"+graph_name+"\'"
    else:
        if is_source is not None and is_source != '':
            con_is_source = " and is_source=\'" + is_source + "\'"

        con_source_graph_name = ""
        if source_graph_name is not None and source_graph_name != '':
            con_source_graph_name = " and graph_source=\'" + source_graph_name + "\'"

        sql = "SELECT graph_create_date,graph_name,graph_cfg,is_source,graph_source FROM name2cfg where graph_status=1 " \
              + con_is_source + con_source_graph_name

    with conn.cursor() as cur:
        cur.execute(sql)
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()

        # print(f"Balances at {time.asctime()}:")
        for row in rows:
            res.append({'graph_create_date': str(row[0]), 'graph_name': row[1],
                        'graph_cfg': row[2], 'is_source': row[3], 'graph_source':row[4]})
        return res


def insert_graph(conn, graph_name, graph_cfg, is_source, source_graph_name):
    """
    图元信息插入
    """
    sql = "SELECT graph_create_date,graph_name,graph_cfg,is_source,graph_source FROM name2cfg where graph_name=\'"\
          +graph_name+"\' and graph_status=1 "

    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        if len(rows) > 0:
            logger.warning("graph name ["+graph_name+"] already exists")
            return "graph name ["+graph_name+"] already exists"
        if is_source == "sub":
            cur.execute("SELECT graph_create_date,graph_name,graph_cfg,is_source,graph_source FROM name2cfg where"+
                        " graph_status=1 and is_source= 'main' and graph_source=\'"+source_graph_name+"\'")
            rows0 = cur.fetchall()
            conn.commit()

            subgraph_cfg = json.loads(copy.deepcopy(rows0[0][2]))
            for name in subgraph_cfg["edges"]:
                subgraph_cfg["edges"][name]["db"] = graph_name
            for name in subgraph_cfg["vertexes"]:
                subgraph_cfg["vertexes"][name]["db"] = graph_name
            graph_cfg = json.dumps(subgraph_cfg)

        cur.execute("UPSERT INTO name2cfg values (\'" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\',\'" + graph_name + "\',1,\'" + graph_cfg + "\',\'"+is_source+"\',\'"+source_graph_name+"\');")
        conn.commit()

        logger.info("register graph ["+graph_name+"] done")
        return "register graph ["+graph_name+"] done"

#图元信息逻辑删除
def delete_graph(conn, graph_name):
    sql = "SELECT graph_create_date,graph_name,graph_cfg,is_source,graph_source FROM name2cfg where graph_name=\'"\
          +graph_name+"\' and graph_status=1 "

    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        if len(rows) == 0:
            logger.warning("graph name ["+graph_name+"] does not exist")
            return "graph name ["+graph_name+"] does not exist"

        cur.execute("update name2cfg  set graph_status=0 WHERE graph_name=\'"+graph_name+"\' and graph_status=1")
        logger.info("delete graph [" + graph_name + "] done")
        return "delete graph [" + graph_name + "] done"

#图元信息逻辑删除
def update_graph(conn, graph_name, graph_cfg):
    sql = "SELECT graph_create_date,graph_name,graph_cfg,is_source,graph_source FROM name2cfg where graph_name=\'"\
          +graph_name+"\' and graph_status=1 "

    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        if len(rows) == 0:
            logger.warning("graph name ["+graph_name+"] does not exist")
            return "graph name ["+graph_name+"] does not exist"

        cur.execute("update name2cfg  set graph_cfg=\'"+graph_cfg+"\' WHERE graph_name=\'"+graph_name+"\' and graph_status=1")


        logger.info("delete graph [" + graph_name + "] done")

    return "delete graph [" + graph_name + "] done"


logger = logging.getLogger('DBoperator')


class DBoperator(object):
    def __init__(self, url):
        self.url = url
        logger.info('DBoperator Start')

        # with conn.cursor() as cur:
        #     cur.execute('create database if not exists data_platform_dev')
        #     cur.execute(
        #         'CREATE TABLE if not exists data_platform_dev.name2cfg (graph_create_date TIMESTAMP NULL,graph_name VARCHAR NULL,graph_status INT2 NULL,	graph_cfg VARCHAR NULL,	is_source VARCHAR NULL,graph_source VARCHAR NULL,	FAMILY "primary" (graph_create_date, graph_name, graph_status, graph_cfg, is_source, rowid, graph_source));')
        #
        #     logging.debug("CREATE TABLE if not exists data_platform_dev.name2cfg: status message: %s", cur.statusmessage)
        # conn.commit()

    def show_tables(self,is_source,source_graph_name,graph_name):
        url = self.url
        conn = psycopg2.connect(url)
        #c = psycopg2.connect("host=myhost dbname=mydb sslmode=verify-full sslcert=/root/.postgresql/aa/postgresql.crt sslkey=/root/.postgresql/aa/postgresql.key")

        res = show_graphs(conn, is_source, source_graph_name,graph_name)
        print(res)
        conn.close()
        return res

    def insert_tables(self, graph_name, graph_cfg, is_source, source_graph_name):
        url = self.url
        conn = psycopg2.connect(url)

        res = insert_graph(conn, graph_name, graph_cfg, is_source, source_graph_name)
        conn.close()
        return res

    def delete_tables(self,graph_name):
        url = self.url
        conn = psycopg2.connect(url)

        res = delete_graph(conn, graph_name)
        print(res)
        conn.close()
        return res

    def update_tables(self, graph_name, graph_cfg):
        url = self.url
        conn = psycopg2.connect(url)

        res = update_graph(conn, graph_name, graph_cfg)
        print(res)
        conn.close()
        return res

    def use_tables(self, graph_name):
        """
        图名称切换
        """
        url = self.url
        conn = psycopg2.connect(url)
        sql = "select graph_cfg from name2cfg where graph_name=\'" + graph_name + "\' and graph_status=1"

        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            conn.commit()
            if len(rows) == 0:
                logger.warning("graph name [" + graph_name + "] does not exist")
                return None
            self.graph_name = graph_name
            self.graph_cfg = json.loads(rows[0][0])
            logger.info("use graph [" + graph_name + "] done")
            conn.close()
        return self.graph_cfg

    def get_task(self, graph_name):
        """
        获取计算任务id
        """
        url = self.url
        conn = psycopg2.connect(url)
        sql = "select id from graph_calculation where subgraph_id=\'" + graph_name + "\' "
        ids = []
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            conn.commit()
            if len(rows) == 0:
                logger.warning("get_task name [" + graph_name + "] does not exist")
                return None
            self.graph_name = graph_name
            logger.info("get_id [" + graph_name + "] done")
            ids = rows[0]
            conn.close()
        task_ids = []
        for id in ids:
            task_id = self.get_one_task(id)
            if task_id:
                task_ids.append("\'"+str(task_id)+"\'")

        return task_ids
    def get_one_task(self, id):
        """
        获取计算任务id
        """
        url = self.url
        conn = psycopg2.connect(url)
        sql = "select id,operation_state from calculation_state where" \
              " graph_calculation_id=\'" + str(id) + "\' order by update_time desc limit 1"
        task_id = None
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            conn.commit()
            if len(rows) == 0:
                logger.warning("get_one_task does not exist")
                return None
            logger.info("get_one_task done")
            if rows[0][1] == 1:
                task_id = rows[0][0]
            conn.close()
        return task_id

    def get_name2config(self, graph_name):
        # conn = self.conn
        url = self.url
        conn = psycopg2.connect(url)
        sql = "select * from name2cfg where graph_name=\'" + graph_name + "\' and graph_status=1"

        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            conn.commit()
            if len(rows) == 0:
                logger.warning("graph name [" + graph_name + "] does not exist")
                return None
            self.graph_name = graph_name
            self.name2config = rows
            logger.info("use graph [" + graph_name + "] done")
            conn.close()
        return self.name2config


def main():
    conn = psycopg2.connect('postgresql://root@10.146.143.59:26257/data_platform_dev?sslmode=disable')
    is_source = ''
    source_graph_name = 'a'
    res = show_graphs(conn, is_source, source_graph_name)
    print(res)
    conn.close()

if __name__ == "__main__":
    main()
