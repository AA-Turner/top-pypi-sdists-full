# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-11-26 10:22:44
@LastEditTime: 2024-01-31 10:47:43
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.models.seven_model import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.libs.customize.safe_helper import SafeHelper
from seven_cloudapp_frame.models.seven_model import PageInfo
from seven_cloudapp_frame.models.db_models.cms.cms_info_model import *

class CmsBaseModel():
    """
    :description: 资讯相关业务模型 用于后台或者中台案例和教程等配置信息、字典表用于管理标签、分类等信息
    """

    def __init__(self, context=None, logging_error=None, logging_info=None):
        self.context = context
        self.logging_link_error = logging_error
        self.logging_link_info = logging_info
        self.db_connect_key, self.redis_config_dict = SevenHelper.get_connect_config("db_cms","redis_cms")

    def _delete_cms_info_dependency_key(self, place_id, delay_delete_time=0.01):
        """
        :description: 删除资讯信息依赖建
        :param place_id: 位置标识
        :param act_id: 活动标识
        :param delay_delete_time: 延迟删除时间，传0则不进行延迟
        :return: 
        :last_editors: HuangJianYi
        """
        CmsInfoModel().delete_dependency_key(DependencyKey.cms_info_list(place_id), delay_delete_time)

    def save_cms_info(self, place_id, cms_id, app_id, act_id, info_title=None, simple_title=None, simple_title_url=None, info_type=-1, info_summary=None, info_tag=None, info_mark=None, target_url=None, min_pic=None, mid_pic=None, max_pic=None, info_data=None, pic_collect_json=None, sort_index=-1, is_release=-1, i1=-1, i2=-1, i3=-1, i4=-1, s1=None, s2=None, s3=None, s4=None):
        """
        :description: 保存资讯信息
        :param place_id：位置标识
        :param cms_id：信息标识
        :param app_id：应用标识
        :param act_id：活动标识
        :param info_title：信息标题
        :param simple_title：信息短标题
        :param simple_title_url：短标题链接
        :param info_type：短标题链接
        :param info_summary：短标题链接
        :param info_tag：信息标签[文章内容特性][砍人事件]
        :param info_mark：信息标记[首发,推荐,独家，热门]
        :param target_url：跳转地址
        :param min_pic：信息小图
        :param mid_pic：信息中图
        :param max_pic：信息大图
        :param info_data：信息内容
        :param pic_collect_json：图集json
        :param sort_index：排序
        :param is_release：是否发布（1是0否）
        :param i1：i1
        :param i2：i2
        :param i3：i3
        :param i4：i4
        :param s1：s1
        :param s2：s2
        :param s3：s3
        :param s4：s4
        :return
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        old_cms_info = None
        cms_info = None
        is_add = False
        cms_info_model = CmsInfoModel(context=self.context)
        if cms_id > 0:
            cms_info = cms_info_model.get_entity_by_id(cms_id)
            if not cms_info or SafeHelper.authenticat_app_id(cms_info.app_id, app_id) == False:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "信息不存在"
                return invoke_result_data
            old_cms_info = deepcopy(cms_info)
        if not cms_info:
            is_add = True
            cms_info = CmsInfo()
        if is_add:
            cms_info.place_id = place_id
            cms_info.app_id = app_id
            cms_info.act_id = act_id
            cms_info.info_title = info_title
            cms_info.simple_title = simple_title
            cms_info.simple_title_url = simple_title_url
            cms_info.info_type = info_type
            cms_info.info_summary = info_summary
            cms_info.info_tag = info_tag
            cms_info.info_mark = info_mark
            cms_info.target_url = target_url
            cms_info.min_pic = min_pic
            cms_info.mid_pic = mid_pic
            cms_info.max_pic = max_pic
            cms_info.info_data = info_data
            cms_info.pic_collect_json = pic_collect_json if pic_collect_json else []
            cms_info.sort_index = sort_index
            cms_info.i1 = i1
            cms_info.i2 = i2
            cms_info.i3 = i3
            cms_info.i4 = i4
            cms_info.s1 = s1
            cms_info.s2 = s2
            cms_info.s3 = s3
            cms_info.s4 = s4
            cms_info.modify_date = SevenHelper.get_now_datetime()
            cms_info.is_release = is_release
            if is_release == 1:
                cms_info.release_date = cms_info.modify_date
            cms_info.create_date = cms_info.modify_date
            cms_info.id = cms_info_model.add_entity(cms_info)
        else:
            cms_info.info_title = info_title if info_title !=None else cms_info.info_title
            cms_info.simple_title = simple_title if simple_title !=None  else cms_info.simple_title
            cms_info.simple_title_url = simple_title_url if simple_title_url !=None else cms_info.simple_title_url
            cms_info.info_type = info_type if info_type !=-1 else cms_info.info_type
            cms_info.info_summary = info_summary if info_summary !=None else cms_info.info_summary
            cms_info.info_tag = info_tag if info_tag !=None else cms_info.info_tag
            cms_info.info_mark = info_mark if info_mark !=None else cms_info.info_mark
            cms_info.target_url = target_url if target_url !=None else cms_info.target_url
            cms_info.min_pic = min_pic if min_pic !=None else cms_info.min_pic
            cms_info.mid_pic = mid_pic if mid_pic !=None else cms_info.mid_pic
            cms_info.max_pic = max_pic if max_pic !=None else cms_info.max_pic
            cms_info.info_data = info_data if info_data !=None else cms_info.info_data
            cms_info.pic_collect_json = pic_collect_json if pic_collect_json !=None else cms_info.pic_collect_json
            cms_info.sort_index = sort_index if sort_index !=-1 else cms_info.sort_index
            cms_info.i1 = i1 if i1 !=-1 else cms_info.i1
            cms_info.i2 = i2 if i2 !=-1 else cms_info.i2
            cms_info.i3 = i3 if i3 !=-1 else cms_info.i3
            cms_info.i4 = i4 if i4 !=-1 else cms_info.i4
            cms_info.s1 = s1 if s1 !=None else cms_info.s1
            cms_info.s2 = s2 if s2 !=None else cms_info.s2
            cms_info.s3 = s3 if s3 !=None else cms_info.s3
            cms_info.s4 = s4 if s4 !=None else cms_info.s4
            cms_info.modify_date = SevenHelper.get_now_datetime()
            cms_info.is_release = is_release if is_release !=-1 else cms_info.is_release
            if is_release == 1:
                cms_info.release_date = cms_info.modify_date
            cms_info_model.update_entity(cms_info,exclude_field_list="place_id,app_id,act_id,create_date")
        result = {}
        result["is_add"] = is_add
        result["new"] = cms_info
        result["old"] = old_cms_info
        invoke_result_data.data = result
        self._delete_cms_info_dependency_key(place_id)
        return invoke_result_data

    def delete_cms_info(self,app_id,cms_id):
        """
        :description: 删除资讯信息
        :param app_id：应用标识
        :param cms_id：资讯标识
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        cms_info_model = CmsInfoModel(context=self.context)
        cms_info_dict = cms_info_model.get_dict_by_id(cms_id)
        if not cms_info_dict or SafeHelper.authenticat_app_id(cms_info_dict["app_id"], app_id) == False:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "资讯信息不存在"
            return invoke_result_data
        invoke_result_data.success = cms_info_model.del_entity("id=%s",params=[cms_info_dict["id"]])
        self._delete_cms_info_dependency_key(cms_info_dict["place_id"])
        invoke_result_data.data = cms_info_dict
        return invoke_result_data

    def release_cms_info(self,app_id,cms_id,is_release):
        """
        :description: 活动奖品上下架
        :param app_id：应用标识
        :param cms_id：资讯标识
        :param is_release: 是否发布 1-是 0-否
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        cms_info_model = CmsInfoModel(context=self.context)
        cms_info_dict = cms_info_model.get_dict_by_id(cms_id)
        if not cms_info_dict or SafeHelper.authenticat_app_id(cms_info_dict["app_id"], app_id) == False:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "资讯信息不存在"
            return invoke_result_data
        modify_date = SevenHelper.get_now_datetime()
        invoke_result_data.success = cms_info_model.update_table("modify_date=%s,is_release=%s", "id=%s", [modify_date, is_release, cms_id])
        self._delete_cms_info_dependency_key(cms_info_dict["place_id"])
        invoke_result_data.data = cms_info_dict
        return invoke_result_data

    def get_cms_info_list(self, place_id, page_size, page_index, order_by="id desc",field="*", app_id="", act_id=0, is_cache=True, page_count_mode="total"):
        """
        :description: 位置信息列表
        :param place_id：位置标识
        :param page_size：页大小
        :param page_index：页索引
        :param order_by：排序
        :param field：查询字段
        :param app_id：应用标识
        :param act_id：活动标识
        :param is_cache：是否缓存
        :param page_count_mode: 分页计数模式 total-计算总数(默认) next-计算是否有下一页(bool) none-不计算       
        :return:
        :last_editors: HuangJianYi
        """
        page_list = []
        condition = "place_id=%s and is_release=1"
        params = [place_id]
        if app_id:
            condition+=" and app_id=%s"
            params.append(app_id)
        if act_id:
            condition+=" and act_id=%s"
            params.append(act_id)

        if is_cache == True:
            page_list =  CmsInfoModel(context=self.context, is_auto=True).get_cache_dict_page_list(field=field, page_index=page_index, page_size=page_size, where=condition, group_by="", order_by=order_by, params=params, dependency_key=DependencyKey.cms_info_list(place_id), cache_expire=600, page_count_mode=page_count_mode)
        else:
            page_list = CmsInfoModel(context=self.context).get_dict_page_list(field=field, page_index=page_index, page_size=page_size, where=condition, group_by="", order_by=order_by,params=params,page_count_mode=page_count_mode)

        return page_list

    def get_cms_info_list_v2(self, place_id, page_size, page_index, order_by="id desc", field="*", condition=None, params=None, is_cache=True, page_count_mode="total"):
        """
        :description: 位置信息列表
        :param place_id：位置标识
        :param page_size：页大小
        :param page_index：页索引
        :param order_by：排序
        :param field：查询字段
        :param condition：查询条件
        :param params：参数数组
        :param is_cache：是否缓存
        :param page_count_mode: 分页计数模式 total-计算总数(默认) next-计算是否有下一页(bool) none-不计算       
        :return:
        :last_editors: HuangJianYi
        """
        page_list = []
        condition_where = ConditionWhere()
        condition_where.add_condition("place_id=%s")
        params_list = [place_id]
        if condition:
            condition_where.add_condition(condition)
            params_list.extend(params)

        if is_cache == True:
            page_list = CmsInfoModel(context=self.context, is_auto=True).get_cache_dict_page_list(field=field, page_index=page_index, page_size=page_size, where=condition_where.to_string(), group_by="", order_by=order_by, params=params_list, dependency_key=DependencyKey.cms_info_list(place_id), cache_expire=600, page_count_mode=page_count_mode)
        else:
            page_list =  CmsInfoModel(context=self.context).get_dict_page_list(field=field, page_index=page_index, page_size=page_size, where=condition_where.to_string(), group_by="", order_by=order_by,params=params_list,page_count_mode=page_count_mode)

        return page_list