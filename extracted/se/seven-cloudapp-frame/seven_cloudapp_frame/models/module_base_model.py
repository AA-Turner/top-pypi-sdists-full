# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-05 10:54:36
@LastEditTime: 2025-08-12 16:09:22
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.libs.customize.safe_helper import SafeHelper
from seven_cloudapp_frame.models.seven_model import *

from seven_cloudapp_frame.models.db_models.act.act_module_model import *
from seven_cloudapp_frame.models.db_models.price.price_gear_model import *

class ModuleBaseModel():
    """
    :description: 活动模块业务模型
    """
    def __init__(self, context=None, logging_error=None, logging_info=None):
        self.context = context
        self.logging_link_error = logging_error
        self.logging_link_info = logging_info


    def _delete_act_module_dependency_key(self, act_id, module_id, delay_delete_time=0.01):
        """
        :description: 删除活动模块依赖建
        :param act_id: 活动标识
        :param module_id: 活动模块标识
        :param delay_delete_time: 延迟删除时间，传0则不进行延迟
        :return: 
        :last_editors: HuangJianYi
        """
        dependency_key_list = []
        if module_id:
            dependency_key_list.append(DependencyKey.act_module(module_id))
        if act_id:
            dependency_key_list.append(DependencyKey.act_module_list(act_id))
        ActModuleModel().delete_dependency_key(dependency_key_list, delay_delete_time)


    def get_act_module_dict(self,module_id,is_cache=True,is_filter=True):
        """
        :description: 获取活动模块
        :param module_id: 模块标识
        :param is_cache: 是否缓存
        :param is_filter: 是否过滤未发布或删除的数据
        :return: 返回活动模块
        :last_editors: HuangJianYi
        """
        act_module_model = ActModuleModel(context=self.context)
        if is_cache:
            dependency_key = DependencyKey.act_module(module_id)
            act_module_dict = act_module_model.get_cache_dict_by_id(module_id,dependency_key=dependency_key)
        else:
            act_module_dict = act_module_model.get_dict_by_id(module_id)
        if is_filter == True:
            if not act_module_dict or act_module_dict["is_release"] == 0 or act_module_dict["is_del"] == 1:
                return None
        return act_module_dict

    def get_act_module_list(self,app_id,act_id,module_name,start_date,end_date,is_del,page_size,page_index,order_by="sort_index desc,id asc",condition="",params=[],is_cache=True):
        """
        :description: 获取活动信息列表
        :param app_id: 应用标识
        :param act_id: 活动标识
        :param module_name: 模块名称
        :param start_date：开始时间
        :param end_date：结束时间
        :param is_del: 是否回收站1是0否
        :param page_size: 条数
        :param page_index: 页数
        :param order_by：排序
        :param condition：条件
        :param params：参数化数组
        :param is_cache: 是否缓存
        :return: 
        :last_editors: HuangJianYi
        """
        params_list = []
        condition_where = ConditionWhere()
        if app_id:
            condition_where.add_condition("app_id=%s")
            params_list.append(app_id)
        if act_id != 0:
            condition_where.add_condition("act_id=%s")
            params_list.append(act_id)
        if condition:
            condition_where.add_condition(condition)
            params_list.extend(params)
        if is_del !=-1:
            condition_where.add_condition("is_del=%s")
            params_list.append(is_del)
        if module_name:
            condition_where.add_condition("module_name=%s")
            params_list.append(module_name)
        if start_date != "":
            condition_where.add_condition("start_date>=%s")
            params_list.append(start_date)
        if end_date != "":
            condition_where.add_condition("end_date<=%s")
            params_list.append(end_date)
        if is_cache:
            page_list, total = ActModuleModel(context=self.context, is_auto=True).get_cache_dict_page_list(field="*", page_index=page_index, page_size=page_size, where=condition_where.to_string(), group_by="", order_by=order_by, params=params_list,dependency_key=DependencyKey.act_module_list(act_id), cache_expire=300)
        else:
            page_list, total = ActModuleModel(context=self.context).get_dict_page_list(field="*", page_index=page_index, page_size=page_size, where=condition_where.to_string(), group_by="", order_by=order_by, params=params_list)
        return page_list, total

    def save_act_module(self,app_id,act_id,module_id,module_name,module_sub_name,start_date,end_date,module_pic,module_desc,price,price_gear_id,ip_id,join_ways,is_fictitious,sort_index,is_release,i1,i2,i3,i4,i5,s1,s2,s3,s4,s5,d1,d2,business_type=0,module_type=0, exclude_field_list='', is_set_cache=True):
        """
        :description: 添加活动模块信息
        :param app_id: 应用标识
        :param act_id: 活动标识
        :param business_type: 业务类型(0无1机台2活动)
        :param module_id: 活动模块标识
        :param module_name: 模块名称
        :param module_sub_name: 模块短名称
        :param start_date: 开始时间
        :param end_date: 结束时间
        :param module_pic: 模块图片
        :param module_desc: 描述信息
        :param price: 价格
        :param price_gear_id: 档位标识
        :param ip_id: IP标识
        :param join_ways: 活动参与条件（0所有1关注店铺2加入会员3指定用户）
        :param is_fictitious: 是否开启虚拟中奖（1是0否）
        :param sort_index: 排序
        :param is_release: 是否发布（1是0否）
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
        :param business_type: 业务类型(0无1机台2活动)
        :param module_type: 模块类型
        :param exclude_field_list: 排除更新的字段
        :param is_set_cache: 是否设置缓存，默认True False-则是删除依赖建
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        if not act_id:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "参数不能为空或等于0"
            return invoke_result_data

        is_add = False
        old_act_module = None
        now_datetime = SevenHelper.get_now_datetime()
        act_module_model = ActModuleModel(context=self.context)
        act_module = None
        if module_id > 0:
            act_module = act_module_model.get_entity_by_id(module_id)
            if not act_module or SafeHelper.authenticat_app_id(act_module.app_id, app_id) == False:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "活动模块信息不存在"
                return invoke_result_data
            old_act_module = deepcopy(act_module)
        if not act_module:
            is_add = True
            act_module = ActModule()

        act_module.app_id = app_id
        act_module.act_id = act_id
        act_module.business_type = business_type
        act_module.module_name = module_name
        act_module.module_sub_name = module_sub_name
        act_module.module_type = module_type
        act_module.start_date = start_date
        act_module.end_date = end_date
        act_module.module_pic = module_pic
        act_module.module_desc = module_desc
        act_module.price = price
        act_module.price_gear_id = price_gear_id
        act_module.ip_id = ip_id
        act_module.join_ways = join_ways
        act_module.is_fictitious = is_fictitious
        act_module.sort_index = sort_index
        act_module.is_release = is_release
        act_module.release_date = now_datetime
        act_module.i1 = i1
        act_module.i2 = i2
        act_module.i3 = i3
        act_module.i4 = i4
        act_module.i5 = i5
        act_module.s1 = s1
        act_module.s2 = s2
        act_module.s3 = s3
        act_module.s4 = s4
        act_module.s5 = s5
        act_module.d1 = d1
        act_module.d2 = d2
        act_module.modify_date = now_datetime

        if is_add:
            act_module.create_date = now_datetime
            act_module.id = act_module_model.add_entity(act_module)
        else:
            if not exclude_field_list:
                exclude_field_list = 'app_id,act_id'
            act_module_model.update_entity(act_module,exclude_field_list=exclude_field_list)
        result = {}
        result["is_add"] = is_add
        result["new"] = act_module
        result["old"] = old_act_module
        invoke_result_data.data = result
        if is_set_cache == True and act_module.id > 0:
            self._delete_act_module_dependency_key(act_id, 0)
            act_module_model.set_cache_dict_by_id(act_module.id, act_module.__dict__, dependency_key=DependencyKey.act_module(act_module.id))
        else:
            self._delete_act_module_dependency_key(act_id, act_module.id)
        return invoke_result_data

    def update_act_module_status(self,app_id, module_id, is_del, is_set_cache=True):
        """
        :description: 删除或者还原活动模块
        :param app_id：应用标识
        :param act_id：活动标识
        :param is_del：0-还原，1-删除
        :param is_set_cache: 是否设置缓存，默认True False-则是删除依赖建
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        act_module_model = ActModuleModel(context=self.context)
        act_module_dict = act_module_model.get_dict_by_id(module_id)
        if not act_module_dict or SafeHelper.authenticat_app_id(act_module_dict["app_id"], app_id) == False:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "活动模块信息不存在"
            return invoke_result_data
        is_release = 0
        modify_date = SevenHelper.get_now_datetime()
        invoke_result_data.success = act_module_model.update_table("is_del=%s,is_release=%s,release_date=%s,modify_date=%s", "id=%s", [is_del, is_release, modify_date, modify_date, module_id])
        if is_set_cache == True:
            act_module_dict['is_del'] = is_del
            act_module_dict['is_release'] = is_release
            act_module_dict['release_date'] = modify_date
            act_module_dict['modify_date'] = modify_date
            self._delete_act_module_dependency_key(act_module_dict['act_id'], 0)
            act_module_model.set_cache_dict_by_id(module_id, act_module_dict, dependency_key=DependencyKey.act_module(module_id))
        else:
            self._delete_act_module_dependency_key(act_module_dict['act_id'], module_id)
        invoke_result_data.data = act_module_dict
        return invoke_result_data

    def release_act_module(self, app_id, module_id, is_release, is_set_cache=True):
        """
        :description: 活动模块上下架
        :param app_id：应用标识
        :param module_id：活动模块标识
        :param is_release: 是否发布 1-是 0-否
        :param is_set_cache: 是否设置缓存，默认True False-则是删除依赖建
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        act_module_model = ActModuleModel(context=self.context)
        act_module_dict = act_module_model.get_dict_by_id(module_id)
        if not act_module_dict or SafeHelper.authenticat_app_id(act_module_dict["app_id"], app_id) == False:
            invoke_result_data.success = False
            invoke_result_data.error_code = "no_module"
            invoke_result_data.error_message = "活动信息不存在"
            return invoke_result_data
        invoke_result_data.success = act_module_model.update_table("release_date=%s,is_release=%s", "id=%s", [SevenHelper.get_now_datetime(), is_release, module_id])
        if is_set_cache == True:
            act_module_dict['release_date'] = SevenHelper.get_now_datetime()
            act_module_dict['is_release'] = is_release
            self._delete_act_module_dependency_key(act_module_dict['act_id'], 0)
            act_module_model.set_cache_dict_by_id(module_id, act_module_dict, dependency_key=DependencyKey.act_module(module_id))
        else:
            self._delete_act_module_dependency_key(act_module_dict['act_id'], module_id)
        invoke_result_data.data = act_module_dict
        return invoke_result_data

    def update_act_module_price(self,app_id,act_id,prize_gear_id):
        """
        :description: 更新活动模块价格
        :param app_id：应用标识
        :param act_id：活动标识
        :param prize_gear_id：档位标识
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        act_module_model = ActModuleModel(context=self.context)
        price_gear_model = PriceGearModel(context=self.context)
        price_gear_dict = price_gear_model.get_dict_by_id(prize_gear_id)
        if not price_gear_dict or SafeHelper.authenticat_app_id(price_gear_dict["app_id"], app_id) == False or price_gear_dict["act_id"] != act_id:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "价格档位信息不存在"
            return invoke_result_data
        invoke_result_data.success = act_module_model.update_table("price=%s", "act_id=%s and price_gears_id=%s", params=[price_gear_dict["price"], act_id, prize_gear_id])
        self._delete_act_module_dependency_key(act_id,0)
        return invoke_result_data
