import threading

from yplib import *


def do_multi_thread(all_list: list = None,
                    thread_num: int = 100,
                    thread_fun: callable = None) -> None:
    """
    all_list   : 所有的线程,需要处理的数据总数
    thread_num : 线程数量
    thread_fun : 每个线程需要执行的函数
    """
    # 线程数量
    if all_list is None:
        all_list = []
    t_num = int(thread_num) if thread_num is not None else 100
    need_param_list = len(all_list)
    # 所有的线程,需要做的任务总数
    one_thread_do_num = int(len(all_list) / t_num)
    one_thread_do_num = one_thread_do_num + 1 if int(len(all_list) % t_num) > 0 else one_thread_do_num
    for t_i in range(t_num):
        temp_list = all_list[t_i * one_thread_do_num:(t_i + 1) * one_thread_do_num]
        # 当数据量过多的时候,就不用开那么多的线程了
        if not len(temp_list) and need_param_list:
            continue
        # print('list_sub_index', t_i * one_thread_do_num, (t_i + 1) * one_thread_do_num)
        ta = threading.Thread(target=thread_fun, args=(t_i + 1, temp_list))
        ta.start()


def do_thread_to_run(thread_fun: callable = None) -> None:
    if thread_fun:
        ta = threading.Thread(target=thread_fun)
        ta.start()

##############################################################################################################
# from yplib import *

#
# def task():
#     print('use_thread_to_run__start')
#     time.sleep(2)
#     print('匿名函数被执行了')
#     print('use_thread_to_run__end')
#
#
# print('start')
# # do_thread_to_run(task)
# do_thread_to_run(lambda: print('匿名函数被执行了'))
# print('end')

# def do_thread_fun(index=1, do_list=[]):
#     # print(index, 'do_thread done', len(do_list), do_list[0])
#     print(index, 'do_thread done')


#
# sql = "SELECT data FROM tb_data WHERE JSON_EXTRACT(data, '$.type') = 'oss_data_ng' order by id desc limit 1;"
# id_list = json.loads(get_data_from_sql(sql=sql, db_config='dev_db')[0][0])['data']
#
# id_list = id_list[0:31]
# id_list = id_list[0:310]
#
# print('start')
# print(len(id_list))
#
# do_multi_thread(id_list, thread_fun=do_thread_fun, thread_num=5)


# do_multi_thread(thread_fun=do_thread_fun, thread_num=100)

# # 线程数量
# thread_count = 100
# # 所有的线程,需要做的任务总数
#
# one_thread_do_num = int(len(id_list) / thread_count) + 1 if int(len(id_list) % thread_count) > 0 else 0
#
# print(one_thread_do_num)
# for i in range(one_thread_do_num):
#     temp_list = id_list[use_length: use_length + 100]
#     ta = threading.Thread(target=do_thread, args=(temp_list, index))
#     ta.start()

# print('end')
