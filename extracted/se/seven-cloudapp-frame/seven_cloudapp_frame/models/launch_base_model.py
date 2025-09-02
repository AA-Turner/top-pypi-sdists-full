from asq.initiators import query
from seven_cloudapp_frame.models.seven_model import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.models.act_base_model import *
from seven_cloudapp_frame.models.top_base_model import *
from seven_cloudapp_frame.models.db_models.act.act_info_model import *
from seven_cloudapp_frame.models.db_models.act.act_prize_model import *
from seven_cloudapp_frame.models.db_models.launch.launch_goods_model import *
from seven_cloudapp_frame.models.db_models.price.price_gear_model import *
from seven_cloudapp_frame.models.db_models.launch.launch_plan_model import *

class LaunchBaseModel():
    """
    :description: 淘宝商品投放业务模型
    """
    def __init__(self, context=None, logging_error=None, logging_info=None):
        self.context = context
        self.logging_link_error = logging_error
        self.logging_link_info = logging_info

    def add_launch_goods(self, app_id, act_id, goods_id, old_goods_id, source_types):
        """
        :description: 添加商品投放
        :param app_id：应用标识
        :param act_id：活动标识
        :param goods_id：投放商品ID
        :param old_goods_id：旧投放商品ID，投放商品ID和旧投放商品ID不同的话，改变原该投放商品的状态
        :param source_types：商品来源（1活动奖品2价格档位） 多个逗号,分隔
        :return 实体模型InvokeResultData
        :last_editors: HuangJianYi
        """
        now_datetime = SevenHelper.get_now_datetime()
        act_base_model = ActBaseModel(context=self.context)
        launch_goods_model = LaunchGoodsModel(context=self.context)
        act_info_dict = act_base_model.get_act_info_dict(act_id)
        invoke_result_data = InvokeResultData()
        if act_info_dict and act_info_dict["is_launch"] == 0:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "无法进行投放"
            return invoke_result_data
        if not goods_id:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "投放商品ID不能为空或0"
            return invoke_result_data
        if goods_id != old_goods_id and old_goods_id:
            is_update = True
            if source_types:
                source_types = list(set(source_types.split(',')))
            for item in source_types:
                if int(item) == 1:
                    act_prize_total = ActPrizeModel(context=self.context).get_total("act_id=%s and goods_id=%s", params=[act_id, old_goods_id])
                    if act_prize_total > 0 :
                        is_update = False
                elif int(item) == 2:
                    price_gear_total = PriceGearModel(context=self.context).get_total("act_id=%s and goods_id=%s", params=[act_id, old_goods_id])
                    if price_gear_total > 0 :
                        is_update = False
            if is_update == True:
                launch_goods_model.update_table("is_launch=0,is_sync=0,launch_date=%s", "act_id=%s and goods_id=%s", params=[SevenHelper.get_now_datetime(), act_id, old_goods_id])

        total = launch_goods_model.get_total("goods_id=%s", params=[goods_id])
        if total <= 0:
            launch_goods = LaunchGoods()
            launch_goods.app_id = app_id
            launch_goods.act_id = act_id
            launch_goods.goods_id = goods_id
            launch_goods.is_launch = 0
            launch_goods.is_sync = 0
            launch_goods.create_date = now_datetime
            launch_goods.launch_date = now_datetime
            launch_goods.sync_date = now_datetime
            launch_goods_model.add_entity(launch_goods)

        return invoke_result_data

    def add_launch_goods_v2(self, app_id, act_id, goods_ids):
        """
        :description: 添加投放商品 投放2.0
        :param app_id：应用标识
        :param act_id：活动标识
        :param goods_ids:商品id串
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        if goods_ids != "":
            launch_goods_model = LaunchGoodsModel(context=self)
            goods_id_list = goods_ids.split(',')
            for goods_id in goods_id_list:
                total = launch_goods_model.get_total("goods_id=%s", params=[goods_id])
                if total <= 0:
                    launch_goods = LaunchGoods()
                    launch_goods.app_id = app_id
                    launch_goods.act_id = act_id
                    launch_goods.goods_id = goods_id
                    launch_goods.is_launch = 0
                    launch_goods.is_sync = 0
                    launch_goods.error_message = ""
                    launch_goods.create_date = SevenHelper.get_now_datetime()
                    launch_goods.launch_date = SevenHelper.get_now_datetime()
                    launch_goods_model.add_entity(launch_goods)
        return invoke_result_data

    def update_launch_goods(self, act_id, goods_id, source_types):
        """
        :description: 修改投放商品为未投放未同步
        :param app_id：应用标识
        :param act_id：活动标识
        :param goods_id：投放商品ID
        :param source_types：商品来源（1活动奖品商品2价格档位商品） 多个逗号,分隔
        :return 实体模型InvokeResultData
        :last_editors: HuangJianYi
        """
        act_base_model = ActBaseModel(context=self.context)
        launch_goods_model = LaunchGoodsModel(context=self.context)
        act_info_dict = act_base_model.get_act_info_dict(act_id)
        invoke_result_data = InvokeResultData()
        if act_info_dict and act_info_dict["is_launch"] == 0:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "无法进行投放"
            return invoke_result_data
        is_update = True
        if source_types:
            source_types = list(set(source_types.split(',')))
        for item in source_types:
            if int(item) == 1:
                act_prize_total = ActPrizeModel(context=self.context).get_total("act_id=%s and goods_id=%s", params=[act_id, goods_id])
                if act_prize_total > 0 :
                    is_update = False
            elif int(item) == 2:
                price_gear_total = PriceGearModel(context=self.context).get_total("act_id=%s and goods_id=%s", params=[act_id, goods_id])
                if price_gear_total > 0 :
                    is_update = False
        if is_update == True:
            launch_goods_model.update_table("is_launch=0,is_sync=0,launch_date=%s", "act_id=%s and goods_id=%s", params=[SevenHelper.get_now_datetime(), act_id, goods_id])
        return invoke_result_data

    def init_launch_goods(self, app_id, act_id, source_types, online_url):
        """
        :description: 初始化活动投放,用于创建活动时调用
        :param app_id:应用标识
        :param act_id:活动标识
        :param source_types：商品来源（1活动奖品商品2价格档位商品） 多个逗号,分隔
        :param online_url:投放地址
        :return 实体模型InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        act_base_model = ActBaseModel(context=self.context)
        act_info_dict = act_base_model.get_act_info_dict(act_id)
        if not act_info_dict:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "活动不存在"
            return invoke_result_data
        goods_id_list = []
        if source_types:
            source_types = list(set(source_types.split(',')))
        for item in source_types:
            if int(item) == 1:
                prize_goods_id_list = ActPrizeModel(context=self.context).get_dict_list("act_id=%s and goods_id!='' and is_del=0", field="goods_id", params=[act_id])
                if len(prize_goods_id_list) > 0:
                    goods_id_list += [str(goods_id["goods_id"]) for goods_id in prize_goods_id_list]
            elif int(item) == 2:
                gear_goods_id_list = PriceGearModel(context=self.context).get_dict_list("act_id=%s and goods_id!='' and is_del=0", field="goods_id", params=[act_id])
                if len(gear_goods_id_list) > 0:
                    goods_id_list += [str(goods_id["goods_id"]) for goods_id in gear_goods_id_list]
        goods_id_list = list(set(goods_id_list))
        if len(goods_id_list) == 0:
            result_data = {"url": online_url, "act_name": act_info_dict['act_name'], "goods_list": []}
            invoke_result_data.data = result_data
            return invoke_result_data

        launch_goods_model = LaunchGoodsModel(context=self.context)
        goods_exist_list = launch_goods_model.get_dict_list("act_id<>%s and " + SevenHelper.get_condition_by_str_list("goods_id",goods_id_list), field="goods_id", params=act_id)
        goods_id_exist_list = [str(i["goods_id"]) for i in goods_exist_list]
        goods_list = []
        now_datetime = SevenHelper.get_now_datetime()
        for goods_id in goods_id_list:
            launch_goods = LaunchGoods()
            launch_goods.app_id = app_id
            launch_goods.act_id = act_id
            launch_goods.goods_id = goods_id
            if goods_id in goods_id_exist_list:
                launch_goods.is_launch = 0
                launch_goods.is_sync = 0
            else:
                launch_goods.is_launch = 1
                launch_goods.is_sync = 1

            launch_goods.create_date = now_datetime
            launch_goods.launch_date = now_datetime
            launch_goods.sync_date = now_datetime
            goods_list.append(launch_goods)

        launch_goods_model.add_list(goods_list)
        result_data = {"url": online_url, "act_name": act_info_dict['act_name'], "goods_list": goods_id_list}
        invoke_result_data.data = result_data
        return invoke_result_data

    def async_launch_goods(self, app_id, act_id, online_url, access_token, app_key, app_secret, is_log=False):
        """
        :description: 同步投放商品（小程序投放-商品绑定/解绑）
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
        act_base_model = ActBaseModel(context=self.context)
        act_info_dict = act_base_model.get_act_info_dict(act_id)
        if not act_info_dict:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "活动不存在"
            return invoke_result_data
        top_base_model = TopBaseModel(context=self.context)
        launch_goods_model = LaunchGoodsModel(context=self.context)
        launch_goods_list = launch_goods_model.get_list("app_id=%s and act_id=%s and is_sync=0 and is_launch=1", params=[app_id,act_id])
        no_launch_goods_list = launch_goods_model.get_list("app_id=%s and act_id=%s and is_sync=0 and is_launch=0", params=[app_id,act_id])
        # 同步不投放的商品
        if len(no_launch_goods_list) > 0:

            no_launch_goods_id_list = [str(no_launch_goods.goods_id) for no_launch_goods in no_launch_goods_list]
            no_launch_goods_id_list = list(set(no_launch_goods_id_list))
            no_launch_goods_ids = ",".join(no_launch_goods_id_list)

            update_no_launch_goods_list = []
            # 淘宝top接口
            invoke_result_data = top_base_model.miniapp_distribution_items_bind(no_launch_goods_ids, online_url, 'false',access_token,app_key, app_secret, is_log)
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
            launch_goods_id_list = [str(launch_goods.goods_id) for launch_goods in launch_goods_list]
            launch_goods_id_list = list(set(launch_goods_id_list))
            launch_goods_ids = ",".join(launch_goods_id_list)

            update_launch_goods_list = []
            # 淘宝top接口
            invoke_result_data = top_base_model.miniapp_distribution_items_bind(launch_goods_ids, online_url, 'true',access_token,app_key, app_secret, is_log)
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

    def get_launch_goods_list(self, app_id, act_id, page_size, page_index, access_token, app_key, app_secret, goods_id="", launch_status=-1):
        """
        :description: 获取投放商品列表
        :param app_id:应用标识
        :param act_id:活动标识
        :param page_size:条数
        :param page_index:页数
        :param access_token:access_token
        :param app_key:app_key
        :param app_secret:app_secret
        :param goods_id:商品id
        :param launch_status:投放状态
        :return 实体模型InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        act_base_model = ActBaseModel(context=self.context)
        act_info_dict = act_base_model.get_act_info_dict(act_id)
        if not act_info_dict:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "活动不存在"
            return invoke_result_data
        launch_goods_model = LaunchGoodsModel(context=self.context)
        condition = "app_id=%s and act_id=%s"
        params = [app_id, act_id]
        if goods_id != "":
            condition += " and goods_id =%s"
            params.append(goods_id)
        if launch_status != -1:
            condition += " and is_launch=%s"
            params.append(launch_status)

        launch_goods_list, total = launch_goods_model.get_dict_page_list("*", page_index, page_size, condition, "", "id desc", params=params)

        top_base_model = TopBaseModel(context=self.context)
        #获取商品信息
        goods_list = []
        if len(launch_goods_list) > 0:
            goods_ids = ",".join([str(launch_goods["goods_id"]) for launch_goods in launch_goods_list])

            invoke_result_data = top_base_model.get_goods_list_by_goodsids(goods_ids, access_token,app_key,app_secret)
            if invoke_result_data.success == False:
                return invoke_result_data
            resq = invoke_result_data.data
            if "items_seller_list_get_response" in resq.keys():
                if "item" in resq["items_seller_list_get_response"]["items"].keys():
                    goods_list = resq["items_seller_list_get_response"]["items"]["item"]
            else:
                invoke_result_data.success = False
                invoke_result_data.error_code = resq["error_code"]
                invoke_result_data.error_message = resq["error_message"]
                return invoke_result_data
        if len(goods_list)>0:
            launch_goods_list = SevenHelper.merge_dict_list(launch_goods_list, "goods_id", goods_list, "num_iid", "pic_url,title")
        page_info = PageInfo(page_index, page_size, total, launch_goods_list)
        invoke_result_data.data = {"is_launch": act_info_dict['is_launch'], "page_info": page_info.__dict__}
        return invoke_result_data

    def reset_launch_goods(self, app_id, act_id, close_goods_id):
        """
        :description: 重置商品投放 删除已投放的记录并将活动投放状态改为未投放
        :param app_id:应用标识
        :param act_id:活动标识
        :param close_goods_id：投放失败时关闭投放的商品ID  多个逗号,分隔
        :return 实体模型InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        ActInfoModel(context=self).update_table("is_launch=0", "app_id=%s and id=%s", params=[app_id, act_id])
        ActBaseModel(context=self)._delete_act_info_dependency_key(app_id, act_id)
        if close_goods_id != "":
            close_goods_id_list = list(set(close_goods_id.split(",")))
            LaunchGoodsModel(context=self).update_table("is_launch=0,launch_date=%s", "act_id=%s and " + SevenHelper.get_condition_by_str_list("goods_id", close_goods_id_list), params=[SevenHelper.get_now_datetime(), act_id])
        else:
            LaunchGoodsModel(context=self).del_entity("app_id=%s and id=%s", params=[app_id, act_id])
        
        #保存投放计划信息
        tb_launch_plan = None
        if call_back_info != "":
            call_back_info = SevenHelper.json_loads(call_back_info)
            for cur_tb_launch_plan in call_back_info["putSuccessList"]:
                if cur_tb_launch_plan["sceneInfo"]["id"] == 1:
                    tb_launch_plan = cur_tb_launch_plan
                    break

        if tb_launch_plan:
            launch_plan_model = LaunchPlanModel(context=self)
            launch_plan = launch_plan_model.get_entity("tb_launch_id=%s", params=[tb_launch_plan["id"]])
            if not launch_plan:
                launch_plan = LaunchPlan()
                launch_plan.app_id = app_id
                launch_plan.act_id = act_id
                launch_plan.tb_launch_id = tb_launch_plan["id"]
                launch_plan.launch_url = tb_launch_plan["previewUrl"]
                launch_plan.start_date = tb_launch_plan["startTime"].replace('年', '-').replace('月', '-').replace('日', ' ') + tb_launch_plan["startTimeBottm"]
                launch_plan.end_date = tb_launch_plan["endTime"].replace('年', '-').replace('月', '-').replace('日', ' ') + tb_launch_plan["endTimeBottom"]
                if tb_launch_plan["status"] == "未开始":
                    launch_plan.status = 0
                elif tb_launch_plan["status"] == "进行中":
                    launch_plan.status = 1
                elif tb_launch_plan["status"] == "已结束":
                    launch_plan.status = 2
                launch_plan.create_date = SevenHelper.get_now_datetime()
                launch_plan.modify_date = SevenHelper.get_now_datetime()
                launch_plan_model.add_entity(launch_plan)
            return invoke_result_data
    
    def init_launch_goods_callback(self, app_id, act_id, close_goods_id, call_back_info):
        """
        :description: 初始化投放商品回调接口
        :param app_id：应用标识
        :param act_id：活动标识
        :param close_goods_id：投放失败时关闭投放的商品ID  多个逗号,分隔
        :param call_back_info：回调信息
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        if close_goods_id != "":
            close_goods_id_list = list(set(close_goods_id.split(",")))
            LaunchGoodsModel(context=self).update_table("is_launch=0,launch_date=%s", "act_id=%s and "+ SevenHelper.get_condition_by_str_list("goods_id",close_goods_id_list), params=[SevenHelper.get_now_datetime(),act_id])
        #保存投放计划信息
        tb_launch_plan = None
        if call_back_info != "":
            call_back_info = SevenHelper.json_loads(call_back_info)
            for cur_tb_launch_plan in call_back_info["putSuccessList"]:
                if cur_tb_launch_plan["sceneInfo"]["id"] == 1:
                    tb_launch_plan = cur_tb_launch_plan
                    break

        if tb_launch_plan:
            launch_plan_model = LaunchPlanModel(context=self)
            launch_plan = launch_plan_model.get_entity("tb_launch_id=%s", params=[tb_launch_plan["id"]])
            if not launch_plan:
                launch_plan = LaunchPlan()
                launch_plan.app_id = app_id
                launch_plan.act_id = act_id
                launch_plan.tb_launch_id = tb_launch_plan["id"]
                launch_plan.launch_url = tb_launch_plan["previewUrl"]
                launch_plan.start_date = tb_launch_plan["startTime"].replace('年', '-').replace('月', '-').replace('日', ' ') + tb_launch_plan["startTimeBottm"]
                launch_plan.end_date = tb_launch_plan["endTime"].replace('年', '-').replace('月', '-').replace('日', ' ') + tb_launch_plan["endTimeBottom"]
                if tb_launch_plan["status"] == "未开始":
                    launch_plan.status = 0
                elif tb_launch_plan["status"] == "进行中":
                    launch_plan.status = 1
                elif tb_launch_plan["status"] == "已结束":
                    launch_plan.status = 2
                launch_plan.create_date = SevenHelper.get_now_datetime()
                launch_plan.modify_date = SevenHelper.get_now_datetime()
                launch_plan_model.add_entity(launch_plan)
            ActInfoModel(context=self).update_table("is_launch=1", "id=%s", params=act_id)
            ActBaseModel(context=self)._delete_act_info_dependency_key(app_id,act_id)
            
        return invoke_result_data

    def get_launch_plan_status(self, act_id, access_token ,app_key, app_secret):
        """
        :description: 获取投放计划状态
        :param act_id：活动标识
        :param access_token:access_token
        :param app_key:app_key
        :param app_secret:app_secret
        :return 
        :last_editors: HuangJianYi
        """
        launch_status = 1  #投放状态，0:未开始， 1：进行中，2/3:已结束，其他为平台状态
        launch_plan_model = LaunchPlanModel(context=self)
        launch_plan_dict = launch_plan_model.get_dict("act_id=%s", order_by="id desc",field="tb_launch_id", params=[act_id])

        act_info_model = ActInfoModel(context=self)
        act_info_dict = act_info_model.get_dict("id=%s",field="is_launch", params=[act_id])
        if not launch_plan_dict:
            if act_info_dict:
                if act_info_dict["is_launch"] == 1:
                    return launch_status
                else:
                    return 0
            else:
                return 0
        top_base_model = TopBaseModel(context=self)
        invoke_result_data = top_base_model.miniapp_distribution_order_get(launch_plan_dict["tb_launch_id"], access_token, app_key, app_secret)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        tb_launch_status = invoke_result_data.data["miniapp_distribution_order_get_response"]["model"]["distribution_order_open_biz_dto"][0]["status"]
        if tb_launch_status == 0:
            tb_launch_status = 1
        if tb_launch_status == 2 and act_info_dict["is_launch"] == 0:
            tb_launch_status = 0
        launch_status = tb_launch_status
        return launch_status

    def can_launch_goods_list(self, page_index, page_size, goods_name, order_tag, order_by, access_token, app_key, app_secret, is_log=False):
        """
        :description: 导入商品列表（获取当前会话用户出售中的商品列表）
        :param page_index：页索引
        :param page_size：页大小
        :param goods_name：商品名称
        :param order_tag：order_tag
        :param order_by：排序类型
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        top_base_model = TopBaseModel(context=self)
        app_key, app_secret = self.get_app_key_secret()
        invoke_result_data = top_base_model.get_goods_list(page_index, page_size, goods_name, order_tag, order_by, access_token, app_key, app_secret, is_log=is_log)
        if invoke_result_data.success == False:
            return invoke_result_data

        goods_id_list = [str(goods["num_iid"]) for goods in invoke_result_data.data["items_onsale_get_response"]["items"]["item"]]
        goods_id_in_condition = SevenHelper.get_condition_by_str_list("goods_id", goods_id_list)
        launch_goods_model = LaunchGoodsModel(context=self)
        launch_goods_list = launch_goods_model.get_list(goods_id_in_condition)
        act_id_list = [launch_goods.act_id for launch_goods in launch_goods_list]
        act_id_list = list(set(act_id_list))
        act_id_in_condition = SevenHelper.get_condition_by_int_list("id",act_id_list)

        act_info_model = ActInfoModel(context=self)
        act_info_list = act_info_model.get_list(act_id_in_condition)

        for goods in invoke_result_data.data["items_onsale_get_response"]["items"]["item"]:
            launch_goods = query(launch_goods_list).first_or_default(None, lambda x: x.goods_id == str(goods["num_iid"]))
            if launch_goods:
                goods["is_select"] = 1
                goods["bind_act_id"] = launch_goods.act_id
                act_info = query(act_info_list).first_or_default(None, lambda x: x.id == goods["bind_act_id"])
                if act_info:
                    goods["bind_act_name"] = act_info.act_name
                else:
                    goods["bind_act_name"] = ""
            else:
                goods["is_select"] = 0
                goods["bind_act_id"] = 0
                goods["bind_act_name"] = ""
        
        return invoke_result_data

    def get_launch_progress(self,act_id):
        """
        :description: 获取投放进度
        :param act_id：活动标识
        :return 投放进度 0未完成  1：已完成
        :last_editors: HuangJianYi
        """
        redis_init = SevenHelper.redis_init()
        redis_data = redis_init.lrange("queue_async_lauch",0,-1)

        progress = 0 #投放进度  0未完成  1：已完成
        if not redis_data:
            progress = 1
        elif len(redis_data) == 0:
            progress = 1
        else:
            for data in redis_data:
                if str(act_id) == data:
                    progress = 0
                    break
        return progress
