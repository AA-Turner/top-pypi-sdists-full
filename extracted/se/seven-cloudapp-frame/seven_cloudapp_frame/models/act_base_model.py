# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-28 09:54:51
@LastEditTime: 2025-03-24 15:57:20
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.models.seven_model import *
from seven_cloudapp_frame.libs.customize.safe_helper import SafeHelper

from seven_cloudapp_frame.models.db_models.base.base_info_model import *
from seven_cloudapp_frame.models.db_models.act.act_type_model import *
from seven_cloudapp_frame.models.db_models.app.app_info_model import *
from seven_cloudapp_frame.models.db_models.act.act_info_model import *
from seven_cloudapp_frame.models.db_models.act.act_prize_model import *
from seven_cloudapp_frame.models.db_models.launch.launch_plan_model import *
from seven_cloudapp_frame.models.db_models.launch.launch_goods_model import *
from seven_cloudapp_frame.models.top_base_model import TopBaseModel

class ActBaseModel():
    """
    :description: 活动信息业务模型
    """
    def __init__(self,context=None,logging_error=None,logging_info=None):
        self.context = context
        self.logging_link_error = logging_error
        self.logging_link_info = logging_info

    def _delete_act_info_dependency_key_v2(self, **args):
        """
        :description: 删除活动信息依赖建
        :param args: 必须指定参数名的可变长度的关键字参数（类似字典）
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = args.get("app_id", "") # 应用标识
        act_id = args.get("act_id", 0) # 活动标识
        delay_delete_time = args.get("delay_delete_time", 0.01) # 延迟删除时间
        dependency_key_list = []
        if act_id:
            dependency_key_list.append(DependencyKey.act_info(act_id)) 
        if app_id:
            dependency_key_list.append(DependencyKey.act_info_list(app_id))
        return ActInfoModel().delete_dependency_key(dependency_key_list, delay_delete_time)

    def _delete_act_info_dependency_key(self, app_id, act_id, delay_delete_time=0.01):
        """
        :description: 删除活动信息依赖建
        :param app_id: 应用标识
        :param act_id: 活动标识
        :param delay_delete_time: 延迟删除时间，传0则不进行延迟
        :return: 
        :last_editors: HuangJianYi
        """
        return self._delete_act_info_dependency_key_v2(app_id=app_id, act_id=act_id, delay_delete_time=delay_delete_time)

    def get_act_info_dict(self,act_id,is_cache=True,is_filter=True, field="*"):
        """
        :description: 获取活动信息
        :param act_id: 活动标识
        :param is_cache: 是否缓存
        :param is_filter: 是否过滤未发布或删除的数据
        :param field: 查询字段
        :return: 返回活动信息
        :last_editors: HuangJianYi
        """
        act_info_model = ActInfoModel(context=self.context, is_auto=True)
        if is_cache:
            dependency_key = DependencyKey.act_info(act_id)
            act_info_dict = act_info_model.get_cache_dict_by_id(primary_key_id=act_id, dependency_key=dependency_key, cache_expire=600, field=field)
        else:
            act_info_dict = act_info_model.get_dict_by_id(act_id, field)
        if is_filter == True:
            if not act_info_dict or act_info_dict["is_release"] == 0 or act_info_dict["is_del"] == 1:
                return None
        return act_info_dict

    def get_act_info_list(self, app_id, act_name, is_del, page_size, page_index, is_cache=True, act_type=-1, is_release=-1, order_by="id asc", business_type=-1):
        """
        :description: 获取活动信息列表
        :param app_id: 应用标识
        :param act_name: 活动名称
        :param is_del: 是否回收站1是0否
        :param page_size: 条数
        :param page_index: 页数
        :param is_cache: 是否缓存
        :param act_type: 活动类型
        :param is_release: 是否发布（1是0否）
        :param order_by: 排序
        :param business_type: 业务类型
        :return: 
        :last_editors: HuangJianYi
        """
        condition_where = ConditionWhere()
        condition_where.add_condition("app_id=%s")
        params = [app_id]
        if is_del !=-1:
            condition_where.add_condition("is_del=%s")
            params.append(is_del)
        if is_release !=-1:
            condition_where.add_condition("is_release=%s")
            params.append(is_release)
        if act_type !=-1:
            condition_where.add_condition("act_type=%s")
            params.append(act_type)
        if business_type !=-1:
            condition_where.add_condition("business_type=%s")
            params.append(business_type)
        if act_name:
            condition_where.add_condition("act_name=%s")
            params.append(act_name)

        if is_cache:
            page_list, total = ActInfoModel(context=self.context, is_auto=True).get_cache_dict_page_list(field="*", page_index=page_index, page_size=page_size, where=condition_where.to_string(), group_by="", order_by=order_by, params=params, dependency_key=DependencyKey.act_info_list(app_id), cache_expire=300)
        else:
            page_list, total = ActInfoModel(context=self.context).get_dict_page_list(field="*", page_index=page_index, page_size=page_size, where=condition_where.to_string(), group_by="", order_by=order_by, params=params)
        for page in page_list:
            page["share_desc_json"] = SevenHelper.json_loads(page["share_desc_json"]) if page["share_desc_json"] else {}
            page["rule_desc_json"] = SevenHelper.json_loads(page["rule_desc_json"]) if page["rule_desc_json"] else []
            page["agreement_json"] = SevenHelper.json_loads(page["agreement_json"]) if page["agreement_json"] else []
            page["brand_json"] = SevenHelper.json_loads(page["brand_json"]) if page["brand_json"] else {}
            page["finish_menu_config_json"] = SevenHelper.json_loads(page["finish_menu_config_json"]) if page["finish_menu_config_json"] else []
            page["finish_status"] = page["is_finish"]
        return page_list, total

    def add_act_info(self, app_id, act_name, act_type, theme_id, share_desc_json, rule_desc_json, close_word="抱歉，程序维护中", is_share=-1, is_rule=-1, is_release=-1, start_date=None, end_date=None, is_black=-1, refund_count=-1, join_ways=-1, is_fictitious=-1, store_url=None, i1=-1, i2=-1, i3=-1, i4=-1, i5=-1, s1=None, s2=None, s3=None, s4=None, s5=None, d1=None, d2=None, is_visit_store=-1, agreement_json=[], brand_json={}, business_type=-1):
        """
        :description: 添加活动信息
        :param app_id: 应用标识
        :param act_name: 活动名称
        :param act_type: 活动类型
        :param theme_id: 主题标识
        :param share_desc_json: 分享配置
        :param rule_desc_json: 规则配置
        :param is_share: 是否开启分享
        :param is_rule: 是否开启规则
        :param is_release: 是否发布
        :param start_date: 开始时间
        :param end_date: 结束时间
        :param is_black：是否开启退款惩罚
        :param refund_count：退款成功次数
        :param join_ways: 活动参与条件（0所有1关注店铺2加入会员3指定用户）
        :param is_fictitious: 是否开启虚拟中奖（1是0否）
        :param store_url: 店铺地址
        :param i1: i1
        :param i2: i2
        :param i3: i3
        :param i4: i4
        :param i5: i5
        :param s1: s1
        :param s2: s2
        :param s3: s3
        :param s4: s4
        :param s5: s5
        :param d1: d1
        :param d2: d2
        :param is_visit_store: 是否开启访问店铺
        :param agreement_json: 协议配置（用户协议或隐私条款）
        :param brand_json: 品牌配置
        :param business_type: 业务类型
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        if not app_id:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "参数不能为空或等于0"
            return invoke_result_data
        if not act_name:
            base_info_model = BaseInfoModel(context=self.context)
            base_info_dict = base_info_model.get_cache_dict()
            if not base_info_dict:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "基础信息不存在"
                return invoke_result_data
        act_type_model = ActTypeModel(context=self.context)
        act_type_info = act_type_model.get_entity("id=%s", params=act_type)
        if not act_type_info:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "活动类型信息不存在"
            return invoke_result_data

        now_datetime = SevenHelper.get_now_datetime()
        act_info_model = ActInfoModel(context=self.context)
        
        act_info = ActInfo()
        act_info.app_id = app_id
        if not act_name:
            act_count = act_info_model.get_total("app_id=%s", params=[app_id])
            act_info.act_name = base_info_dict["product_name"] + "_" + str(act_count + 1)
        else:
            act_info.act_name = act_name
        act_info.act_type = act_type
        act_info.theme_id = theme_id
        act_info.close_word = close_word
        act_info.share_desc_json = share_desc_json if share_desc_json else {}
        act_info.rule_desc_json = rule_desc_json if rule_desc_json else []
        act_info.start_date = start_date if start_date else now_datetime
        act_info.end_date =  end_date if end_date else "2900-01-01 00:00:00"
        act_info.task_asset_type_json = act_type_info.task_asset_type_json
        act_info.is_release = is_release if is_release != -1 else 1
        act_info.release_date = now_datetime
        act_info.create_date = now_datetime
        act_info.modify_date = now_datetime
        act_info.is_share = is_share if is_share !=-1 else 0
        act_info.is_rule = is_rule if is_rule !=-1 else 0
        act_info.is_black = is_black if is_black != -1 else 0
        act_info.refund_count = refund_count if refund_count != -1 else 0
        act_info.join_ways = join_ways if join_ways != -1 else 0
        act_info.is_fictitious = is_fictitious if is_fictitious != -1 else 0
        act_info.store_url = store_url if store_url else ''
        act_info.i1 = i1 if i1 !=-1 else 0
        act_info.i2 = i2 if i2 !=-1 else 0
        act_info.i3 = i3 if i3 !=-1 else 0
        act_info.i4 = i4 if i4 !=-1 else 0
        act_info.i5 = i5 if i5 !=-1 else 0
        act_info.s1 = s1 if s1 !=None else ''
        act_info.s2 = s2 if s2 !=None else ''
        act_info.s3 = s3 if s3 !=None else ''
        act_info.s4 = s4 if s4 !=None else ''
        act_info.s5 = s5 if s5 !=None else ''
        act_info.d1 = d1 if d1 !=None else '1900-01-01 00:00:00'
        act_info.d2 = d2 if d2 !=None else '1900-01-01 00:00:00'
        act_info.is_visit_store = is_visit_store if is_visit_store !=-1 else 0
        act_info.agreement_json = agreement_json if agreement_json else []
        act_info.brand_json = brand_json if brand_json else {}
        act_info.business_type = business_type if business_type !=-1 else 0
        act_info.id = act_info_model.add_entity(act_info)
        invoke_result_data.data = act_info
        self._delete_act_info_dependency_key(app_id=app_id, act_id=act_info.id)
        return invoke_result_data

    def update_act_info(self, app_id, act_id, act_name, theme_id, is_share, share_desc_json, is_rule, rule_desc_json, is_release, start_date, end_date, is_black, refund_count, join_ways, is_fictitious, close_word="抱歉，程序维护中", store_url=None, i1=-1, i2=-1, i3=-1, i4=-1, i5=-1, s1=None, s2=None, s3=None, s4=None, s5=None, d1=None, d2=None, is_visit_store=-1, agreement_json=[], brand_json={}, business_type=-1, is_set_cache=True):
        """
        :description: 修改活动信息
        :param app_id: 应用标识
        :param act_id：活动标识
        :param act_name：活动名称
        :param is_release：是否发布
        :param theme_id: 主题标识
        :param is_share: 是否开启分享
        :param share_desc_json: 分享配置
        :param is_rule: 是否开启规则
        :param rule_desc_json: 规则配置
        :param start_date: 开始时间
        :param end_date: 结束时间
        :param is_black：是否开启退款惩罚
        :param refund_count：退款成功次数
        :param join_ways: 活动参与条件（0所有1关注店铺2加入会员3指定用户）
        :param is_fictitious: 是否开启虚拟中奖（1是0否）
        :param close_word: 关闭文案
        :param store_url: 店铺地址
        :param i1: i1
        :param i2: i2
        :param i3: i3
        :param i4: i4
        :param i5: i5
        :param s1: s1
        :param s2: s2
        :param s3: s3
        :param s4: s4
        :param s5: s5
        :param d1: d1
        :param d2: d2
        :param is_visit_store: 是否开启访问店铺
        :param agreement_json: 协议配置（用户协议或隐私条款）
        :param brand_json: 品牌配置
        :param business_type: 业务类型
        :param is_set_cache: 是否设置缓存，默认True False-则是删除依赖建
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        act_info_model = ActInfoModel(context=self.context)
        act_info = act_info_model.get_entity_by_id(act_id)
        if not act_info or act_info.app_id != app_id:
            invoke_result_data.success = False
            invoke_result_data.error_code = "no_act"
            invoke_result_data.error_message = "活动信息不存在"
            return invoke_result_data
        old_act_info = deepcopy(act_info)
        now_datetime = SevenHelper.get_now_datetime()
        if act_name !=None:
            act_info.act_name = act_name
        if theme_id !=-1:
            act_info.theme_id = theme_id
        if is_share !=-1:
            act_info.is_share = is_share
        if share_desc_json !=None:
            act_info.share_desc_json = share_desc_json
        if is_rule !=-1:
            act_info.is_rule = is_rule
        if rule_desc_json !=None:
            act_info.rule_desc_json = rule_desc_json
        if is_release !=-1:
            act_info.is_release = is_release
            act_info.release_date = now_datetime
        if start_date !=None:
            act_info.start_date = start_date
        if end_date !=None:
            act_info.end_date = end_date
        if is_black !=-1:
            act_info.is_black = is_black
        if refund_count !=-1:
            act_info.refund_count = refund_count
        if join_ways !=-1:
            act_info.join_ways = join_ways
        if is_fictitious !=-1:
            act_info.is_fictitious = is_fictitious
        if close_word !=None:
            act_info.close_word = close_word
        if is_visit_store !=-1:
            act_info.is_visit_store = is_visit_store
        if store_url !=None:
            act_info.store_url = store_url
        if i1 !=-1:
            act_info.i1 = i1
        if i2 !=-1:
            act_info.i2 = i2
        if i3 !=-1:
            act_info.i3 = i3
        if i4 !=-1:
            act_info.i4 = i4
        if i5 !=-1:
            act_info.i5 = i5
        if s1 !=None:
            act_info.s1 = s1
        if s2 !=None:
            act_info.s2 = s2
        if s3 !=None:
            act_info.s3 = s3
        if s4 !=None:
            act_info.s4 = s4
        if s5 !=None:
            act_info.s5 = s5
        if d1 !=None:
            act_info.d1 = d1
        if d2 !=None:
            act_info.d2 = d2
        if agreement_json !=None:
            act_info.agreement_json = agreement_json
        if brand_json !=None:
            act_info.brand_json = brand_json
        if business_type !=-1:
            act_info.business_type = business_type

        act_info.modify_date = now_datetime
        act_info_model.update_entity(act_info,exclude_field_list="finish_menu_config_json,is_finish,task_asset_type_json,is_launch")
        result = {}
        result["old"] = old_act_info
        result["new"] = act_info
        invoke_result_data.data = result
        if is_set_cache == True:
            self._delete_act_info_dependency_key(app_id=app_id, act_id=0)
            act_info_model.set_cache_dict_by_id(act_info.id, act_info.__dict__, DependencyKey.act_info(act_info.id)) # 更新缓存
        else:
            self._delete_act_info_dependency_key(app_id=app_id, act_id=act_info.id)

        return invoke_result_data

    def update_act_info_status(self, app_id, act_id, is_del, is_set_cache=True):
        """
        :description: 删除或者还原活动
        :param app_id：应用标识
        :param act_id：活动标识
        :param is_del：0-还原，1-删除
        :param is_set_cache: 是否设置缓存，默认True False-则是删除依赖建
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        act_info_model = ActInfoModel(context=self.context)
        act_info_dict = act_info_model.get_dict_by_id(act_id)
        if not act_info_dict or SafeHelper.authenticat_app_id(act_info_dict["app_id"], app_id) == False:
            invoke_result_data.success = False
            invoke_result_data.error_code = "no_act"
            invoke_result_data.error_message = "活动信息不存在"
            return invoke_result_data
        is_release = 0
        modify_date = SevenHelper.get_now_datetime()
        invoke_result_data.success = act_info_model.update_table("is_del=%s,is_release=%s,release_date=%s,modify_date=%s", "id=%s", [is_del, is_release, modify_date, modify_date, act_id])
        if is_set_cache == True:
            act_info_dict['is_del'] = is_del
            act_info_dict['is_release'] = is_release
            act_info_dict['release_date'] = modify_date
            act_info_dict['modify_date'] = modify_date
            self._delete_act_info_dependency_key(app_id=app_id, act_id=0)
            act_info_model.set_cache_dict_by_id(act_id, act_info_dict, DependencyKey.act_info(act_id)) # 更新缓存
        else:
            self._delete_act_info_dependency_key(app_id=app_id, act_id=act_id)

        invoke_result_data.data = act_info_dict
        return invoke_result_data

    def release_act_info(self, app_id, act_id, is_release, is_set_cache=True):
        """
        :description: 活动上下架
        :param app_id：应用标识
        :param act_id：活动标识
        :param is_release: 是否发布 1-是 0-否
        :param is_set_cache: 是否设置缓存，默认True False-则是删除依赖建
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        act_info_model = ActInfoModel(context=self.context)
        act_info_dict = act_info_model.get_dict_by_id(act_id)
        if not act_info_dict or SafeHelper.authenticat_app_id(act_info_dict["app_id"], app_id) == False:
            invoke_result_data.success = False
            invoke_result_data.error_code = "no_act"
            invoke_result_data.error_message = "活动信息不存在"
            return invoke_result_data
        modify_date = SevenHelper.get_now_datetime()

        invoke_result_data.success = act_info_model.update_table("release_date=%s,is_release=%s", "id=%s", [modify_date, is_release, act_id])
        if is_set_cache == True:
            act_info_dict['is_release'] = is_release
            act_info_dict['release_date'] = modify_date
            self._delete_act_info_dependency_key(app_id=app_id, act_id=0)
            act_info_model.set_cache_dict_by_id(act_id, act_info_dict, DependencyKey.act_info(act_id)) # 更新缓存
        else:
            self._delete_act_info_dependency_key(app_id=app_id, act_id=act_id)
        invoke_result_data.data = act_info_dict
        return invoke_result_data

    def next_progress(self,app_id,act_id,finish_key):
        """
        :description: 下一步配置
        :param app_id：应用标识
        :param finish_key：完成key，由前端控制是否完成配置，完成时需传参数值finish_config 代表最后一步
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        base_info_model = BaseInfoModel(context=self.context, is_auto=True)
        base_info = base_info_model.get_entity()
        if not base_info:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "基础信息不存在"
            return invoke_result_data
        act_info_model = ActInfoModel(context=self.context)
        act_info = act_info_model.get_dict_by_id(act_id)
        if not act_info:
            invoke_result_data.success = False
            invoke_result_data.error_code = "no_act"
            invoke_result_data.error_message = "活动信息不存在"
            return invoke_result_data
        menu_config_json = SevenHelper.json_loads(base_info.menu_config_json)
        menu = [menu for menu in menu_config_json if menu["key"] == finish_key]
        if len(menu) == 0:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "对不起，无此菜单"
            return invoke_result_data
        if act_info["finish_menu_config_json"] != "" and finish_key in act_info["finish_menu_config_json"]:
            return invoke_result_data
        if act_info["finish_menu_config_json"] == "":
            act_info["finish_menu_config_json"] = "[]"
        finish_menu_config_json = SevenHelper.json_loads(act_info["finish_menu_config_json"])
        finish_menu_config_json.append(finish_key)

        result_finish_menu_config_json = []
        for item in finish_menu_config_json:
            is_exist = [item2 for item2 in menu_config_json if item2["key"] == item]
            if len(is_exist) > 0:
                result_finish_menu_config_json.append(item)
        is_finish = 0
        if finish_key == "finish_config" and act_info["is_finish"] == 0:
            is_finish = 1
        result_finish_menu_config_json = SevenHelper.json_dumps(result_finish_menu_config_json)
        act_info_model.update_table("finish_menu_config_json=%s,is_finish=%s", "id=%s", [result_finish_menu_config_json, is_finish, act_id])
        if is_finish == 1 and app_id:
            app_info_model = AppInfoModel(context=self.context)
            app_info_model.update_table("is_setting=1", "app_id=%s", [app_id])
        return invoke_result_data
    
    def del_act_launch(self, app_id, act_id, access_token, app_key, app_secret):
        """
        :description: 删除活动投放,在删除活动前调用，投放中的活动不允许删除活动
        :param app_id：应用标识
        :param act_id: 活动标识
        :param access_token: access_token
        :param app_key: app_key
        :param app_secret: app_secret
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        launch_plan_model = LaunchPlanModel(context=self.context)
        launch_plan = launch_plan_model.get_entity("act_id=%s",order_by="id desc",params=[act_id])
        if launch_plan:
            top_base_model = TopBaseModel(context=self.context)
            invoke_result_data = top_base_model.miniapp_distribution_order_get(launch_plan.tb_launch_id,access_token,app_key,app_secret)
            if invoke_result_data.success==True:
                tb_launch_status = invoke_result_data.data["miniapp_distribution_order_get_response"]["model"]["distribution_order_open_biz_dto"][0]["status"]
                if tb_launch_status != 2:
                    invoke_result_data.success=False
                    invoke_result_data.error_code="error"
                    invoke_result_data.error_message="请先中止投放计划"
                    return invoke_result_data
        ActInfoModel(context=self).update_table("is_launch=0", "app_id=%s and id=%s", params=[app_id, act_id])
        ActBaseModel(context=self)._delete_act_info_dependency_key(app_id=app_id, act_id=act_id)
        LaunchGoodsModel(context=self).del_entity("app_id=%s and act_id=%s", params=[app_id, act_id])