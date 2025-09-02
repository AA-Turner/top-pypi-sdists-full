# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-19 13:37:16
@LastEditTime: 2023-02-09 19:27:32
@LastEditors: HuangJianYi
@Description: 
"""
import threading, multiprocessing
from seven_cloudapp_frame.libs.common.frame_console import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.models.top_base_model import *
from seven_cloudapp_frame.models.db_models.act.act_info_model import *
from seven_cloudapp_frame.models.db_models.launch.launch_goods_model import *
from seven_cloudapp_frame.models.db_models.launch.launch_plan_model import *


class LaunchConsoleModel():
    """
    :description: 投放业务模型
    """
    def console_launch(self):
        """
        :description: 控制台投放
        :return: 
        :last_editors: HuangJianYi
        """
        k = threading.Thread(target=self.process_launch_goods, args=[])
        k.start()


    def get_online_url(self, app_id, act_id, module_id=0, act_type=0):
        """
        :description: 获取online_url
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:模块标识
        :param act_type:活动类型
        :return str
        :last_editors: HuangJianYi
        """
        page_index = ""
        page = share_config.get_value("page_index")
        if page:
            if isinstance(page,dict):
                cur_page = page.get(str(act_type),"")
                if cur_page:
                    page_index = "&page=" + CodingHelper.url_encode(cur_page)
            else:
                page_index = "&page=" + CodingHelper.url_encode(page)
        query = CodingHelper.url_encode(f"actid={act_id}")
        if module_id > 0:
            query = CodingHelper.url_encode(f"actid={act_id}&module_id={module_id}")
        online_url = f"https://m.duanqu.com/?_ariver_appid={app_id}{page_index}&query={query}"
        return online_url

    def process_launch_goods(self):
        """
        :description: 处理同步投放商品
        :return
        :last_editors: HuangJianYi
        """
        while True:
            try:
                time.sleep(0.1)
                heart_beat_monitor("process_launch_goods")
                redis_init = RedisExHelper.init()
                act_id = redis_init.lindex("queue_async_lauch",index=0)
                app_key = share_config.get_value("app_key")
                app_secret = share_config.get_value("app_secret")
                invoke_result_data = InvokeResultData()
                if act_id:
                    act_id = int(act_id)
                    act_info_model = ActInfoModel()
                    act_info_dict = act_info_model.get_dict_by_id(act_id,field="app_id,id")
                    if not act_info_dict:
                        continue
                    app_info_model = AppInfoModel()
                    app_info_dict = app_info_model.get_dict("app_id=%s",field="access_token", params=[act_info_dict["app_id"]])
                    if not app_info_dict:
                        continue
                    online_url = self.get_online_url(act_info_dict["app_id"],act_id)
                    launch_plan_model = LaunchPlanModel()
                    launch_plan_dict = launch_plan_model.get_dict("act_id=%s", order_by="id desc",field="launch_url", params=[act_id])
                    if not launch_plan_dict:
                        invoke_result_data = self.async_tb_launch_goods(act_info_dict["app_id"], act_info_dict["id"], online_url, app_info_dict["access_token"], app_key, app_secret)
                    else:
                        invoke_result_data = self.async_tb_launch_goods(act_info_dict["app_id"], act_info_dict["id"], launch_plan_dict["launch_url"], app_info_dict["access_token"], app_key, app_secret)
                    if invoke_result_data.success == False:
                        logger_error.error(f"同步投放商品失败,message:{invoke_result_data.error_message}")
            except Exception as ex:
                logger_error.error(f"同步投放商品失败,ex:{traceback.format_exc()}")
            finally:
                redis_init.lpop("queue_async_lauch")
                time.sleep(1)

    def async_tb_launch_goods(self, app_id, act_id, online_url, access_token, app_key, app_secret, is_log=False):
        """
        :description: 同步投放商品到淘宝（小程序投放-商品绑定/解绑）
        :param app_id：应用标识
        :param act_id：活动标识
        :param online_url:投放地址
        :param access_token:access_token
        :param app_key:app_key
        :param app_secret:app_secret
        :param is_log：是否记录返回信息
        :return 实体模型InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        top_base_model = TopBaseModel()
        launch_goods_model = LaunchGoodsModel()
        launch_goods_list = launch_goods_model.get_list("app_id=%s and act_id=%s and is_sync=0 and is_launch=1", params=[app_id, act_id])
        no_launch_goods_list = launch_goods_model.get_list("app_id=%s and act_id=%s and is_sync=0 and is_launch=0 and create_date!=launch_date", params=[app_id, act_id])

        no_launch_page_index = 0
        no_launch_page_size = 50
        launch_page_index = 0
        launch_page_size = 50

        try:
            # 同步不投放的商品
            if len(no_launch_goods_list) > 0:
                no_launch_page_total = int(len(no_launch_goods_list) / no_launch_page_size)
                if (len(no_launch_goods_list) % no_launch_page_size) > 0:
                    no_launch_page_total += 1
                for no_launch_page_index in range(0, no_launch_page_total):
                    cur_no_launch_goods_list = []
                    if no_launch_page_index == no_launch_page_total - 1:
                        cur_no_launch_goods_list = no_launch_goods_list[no_launch_page_index * no_launch_page_size:len(no_launch_goods_list)]
                    else:
                        cur_no_launch_goods_list = no_launch_goods_list[(no_launch_page_index * no_launch_page_size):((no_launch_page_index + 1) * no_launch_page_size)]
                    no_launch_goods_id_list = [str(no_launch_goods.goods_id) for no_launch_goods in cur_no_launch_goods_list]
                    no_launch_goods_id_list = list(set(no_launch_goods_id_list))
                    no_launch_goods_ids = ",".join(no_launch_goods_id_list)

                    update_no_launch_goods_list = []
                    # 淘宝top接口
                    invoke_result_data = top_base_model.miniapp_distribution_items_bind(no_launch_goods_ids, online_url, 'false', access_token, app_key, app_secret, is_log)
                    if invoke_result_data.success == False:
                        return invoke_result_data
                    resp = invoke_result_data.data
                    async_result = resp["miniapp_distribution_items_bind_response"]["model_list"]["distribution_order_bind_target_entity_open_result_dto"][0]["bind_result_list"]["distribution_order_bind_base_dto"]
                    for async_result_info in async_result:
                        no_launch_goods = [no_launch_goods for no_launch_goods in no_launch_goods_list if str(no_launch_goods.goods_id) == async_result_info["target_entity_id"]]
                        if len(no_launch_goods) > 0:
                            if async_result_info["success"] == True:
                                no_launch_goods[0].is_sync = 1
                                no_launch_goods[0].sync_date = SevenHelper.get_now_datetime()
                            else:
                                no_launch_goods[0].error_message = async_result_info["fail_msg"]
                            update_no_launch_goods_list.append(no_launch_goods[0])

                    launch_goods_model.update_list(update_no_launch_goods_list)

            # 同步投放的商品
            if len(launch_goods_list) > 0:
                launch_page_total = int(len(launch_goods_list) / launch_page_size)
                if (len(launch_goods_list) % launch_page_size) > 0:
                    launch_page_total += 1
                for launch_page_index in range(0, launch_page_total):
                    cur_launch_goods_list = []
                    if launch_page_index == launch_page_total - 1:
                        cur_launch_goods_list = launch_goods_list[launch_page_index * launch_page_size:len(launch_goods_list)]
                    else:
                        cur_launch_goods_list = launch_goods_list[(launch_page_index * launch_page_size):((launch_page_index + 1) * launch_page_size)]
                    launch_goods_id_list = [str(launch_goods.goods_id) for launch_goods in cur_launch_goods_list]
                    launch_goods_id_list = list(set(launch_goods_id_list))
                    launch_goods_ids = ",".join(launch_goods_id_list)

                    update_launch_goods_list = []
                    # 淘宝top接口
                    invoke_result_data = top_base_model.miniapp_distribution_items_bind(launch_goods_ids, online_url, 'true', access_token, app_key, app_secret, is_log)
                    if invoke_result_data.success == False:
                        return invoke_result_data
                    resp = invoke_result_data.data
                    async_result = resp["miniapp_distribution_items_bind_response"]["model_list"]["distribution_order_bind_target_entity_open_result_dto"][0]["bind_result_list"]["distribution_order_bind_base_dto"]
                    for async_result_info in async_result:
                        launch_goods = [launch_goods for launch_goods in launch_goods_list if str(launch_goods.goods_id) == async_result_info["target_entity_id"]]
                        if len(launch_goods) > 0:
                            if async_result_info["success"] == True:
                                launch_goods[0].is_sync = 1
                                launch_goods[0].sync_date = SevenHelper.get_now_datetime()
                            else:
                                launch_goods[0].is_launch = 0
                                launch_goods[0].is_sync = 1
                                launch_goods[0].error_message = async_result_info["fail_msg"]
                            update_launch_goods_list.append(launch_goods[0])
                    launch_goods_model.update_list(update_launch_goods_list)
            return invoke_result_data
        except Exception as ex:
            logger_error.error(f"同步投放商品失败,ex:{traceback.format_exc()}")
