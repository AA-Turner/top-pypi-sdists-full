# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-26 17:00:55
@LastEditTime: 2024-07-12 09:53:15
@LastEditors: HuangJianYi
@Description: 资讯模块
"""

from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.handlers.frame_base import *
from seven_cloudapp_frame.models.enum import *
from seven_cloudapp_frame.models.cms_base_model import *
from seven_cloudapp_frame.models.db_models.cms.cms_info_model import *


class SaveCmsInfoHandler(ClientBaseHandler):
    """
    :description: 保存资讯信息
    """
    @filter_check_params("info_title")
    def get_async(self):
        """
        :description: 保存资讯信息
        :params info_title:标题
        :return 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        place_id = self.get_param_int("place_id", 0)
        cms_id = self.get_param_int("cms_id", 0)
        info_title = self.get_param("info_title")
        simple_title = self.get_param("simple_title")
        simple_title_url = self.get_param("simple_title_url")
        info_type = self.get_param_int("info_type", 0)
        info_summary = self.get_param("info_summary")
        info_tag = self.get_param("info_tag")
        info_mark = self.get_param("info_mark")
        target_url = self.get_param("target_url")
        min_pic = self.get_param("min_pic")
        mid_pic = self.get_param("mid_pic")
        max_pic = self.get_param("max_pic")
        info_data = self.get_param("info_data")
        pic_collect_json = self.get_param("pic_collect_json")
        sort_index = self.get_param_int("sort_index", 0)
        is_release = self.get_param_int("is_release", 0)
        i1 = self.get_param_int("i1", 0)
        i2 = self.get_param_int("i2", 0)
        i3 = self.get_param_int("i3", 0)
        i4 = self.get_param_int("i4", 0)
        s1 = self.get_param("s1")
        s2 = self.get_param("s2")
        s3 = self.get_param("s3")
        s4 = self.get_param("s4")

        cms_base_model = CmsBaseModel(context=self)
        invoke_result_data = cms_base_model.save_cms_info(place_id, cms_id, app_id, act_id, info_title, simple_title, simple_title_url, info_type, info_summary, info_tag, info_mark, target_url, min_pic, mid_pic, max_pic, info_data, pic_collect_json, sort_index, is_release, i1, i2, i3, i4, s1, s2, s3, s4)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if invoke_result_data.data["is_add"] == True:
            # 记录日志
            self.create_operation_log(operation_type=OperationType.add.value, model_name=invoke_result_data.data["new"].__str__(), old_detail=None, update_detail=invoke_result_data.data["new"], title=info_title)
        else:
            self.create_operation_log(operation_type=OperationType.update.value, model_name=invoke_result_data.data["new"].__str__(), old_detail=invoke_result_data.data["old"], update_detail=invoke_result_data.data["new"], title=info_title)

        return self.response_json_success(invoke_result_data.data["new"].id)
    
    @filter_check_params("info_title")
    def post_async(self):
        """
        :description: 保存资讯信息
        :params info_title:标题
        :return 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        place_id = self.get_param_int("place_id", 0)
        cms_id = self.get_param_int("cms_id", 0)
        info_title = self.get_param("info_title")
        simple_title = self.get_param("simple_title")
        simple_title_url = self.get_param("simple_title_url")
        info_type = self.get_param_int("info_type", 0)
        info_summary = self.get_param("info_summary")
        info_tag = self.get_param("info_tag")
        info_mark = self.get_param("info_mark")
        target_url = self.get_param("target_url")
        min_pic = self.get_param("min_pic")
        mid_pic = self.get_param("mid_pic")
        max_pic = self.get_param("max_pic")
        info_data = self.get_param("info_data")
        pic_collect_json = self.get_param("pic_collect_json")
        sort_index = self.get_param_int("sort_index", 0)
        is_release = self.get_param_int("is_release", 0)
        i1 = self.get_param_int("i1", 0)
        i2 = self.get_param_int("i2", 0)
        i3 = self.get_param_int("i3", 0)
        i4 = self.get_param_int("i4", 0)
        s1 = self.get_param("s1")
        s2 = self.get_param("s2")
        s3 = self.get_param("s3")
        s4 = self.get_param("s4")

        cms_base_model = CmsBaseModel(context=self)
        invoke_result_data = cms_base_model.save_cms_info(place_id, cms_id, app_id, act_id, info_title, simple_title, simple_title_url, info_type, info_summary, info_tag, info_mark, target_url, min_pic, mid_pic, max_pic, info_data, pic_collect_json, sort_index, is_release, i1, i2, i3, i4, s1, s2, s3, s4)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if invoke_result_data.data["is_add"] == True:
            # 记录日志
            self.create_operation_log(operation_type=OperationType.add.value, model_name=invoke_result_data.data["new"].__str__(), old_detail=None, update_detail=invoke_result_data.data["new"], title=info_title)
        else:
            self.create_operation_log(operation_type=OperationType.update.value, model_name=invoke_result_data.data["new"].__str__(), old_detail=invoke_result_data.data["old"], update_detail=invoke_result_data.data["new"], title=info_title)

        return self.response_json_success(invoke_result_data.data["new"].id)



class UpdateCmsInfoHandler(ClientBaseHandler):
    """
    :description: 更新资讯信息
    """

    @filter_check_params("cms_id")
    def get_async(self):
        """
        :description: 更新资讯信息
        :params cms_id:资讯标识
        :return 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        place_id = self.get_param_int("place_id", 0)
        cms_id = self.get_param_int("cms_id", 0)
        info_title = self.get_param("info_title",None)
        simple_title = self.get_param("simple_title", None)
        simple_title_url = self.get_param("simple_title_url", None)
        info_type = self.get_param_int("info_type", -1)
        info_summary = self.get_param("info_summary", None)
        info_tag = self.get_param("info_tag", None)
        info_mark = self.get_param("info_mark", None)
        target_url = self.get_param("target_url", None)
        min_pic = self.get_param("min_pic", None)
        mid_pic = self.get_param("mid_pic", None)
        max_pic = self.get_param("max_pic", None)
        info_data = self.get_param("info_data", None)
        pic_collect_json = self.get_param("pic_collect_json", None)
        sort_index = self.get_param_int("sort_index", -1)
        is_release = self.get_param_int("is_release", -1)
        i1 = self.get_param_int("i1", -1)
        i2 = self.get_param_int("i2", -1)
        i3 = self.get_param_int("i3", -1)
        i4 = self.get_param_int("i4", -1)
        s1 = self.get_param("s1", None)
        s2 = self.get_param("s2", None)
        s3 = self.get_param("s3", None)
        s4 = self.get_param("s4", None)

        cms_base_model = CmsBaseModel(context=self)
        invoke_result_data = cms_base_model.save_cms_info(place_id, cms_id, app_id, act_id, info_title, simple_title, simple_title_url, info_type, info_summary, info_tag, info_mark, target_url, min_pic, mid_pic, max_pic, info_data, pic_collect_json, sort_index, is_release, i1, i2, i3, i4, s1, s2, s3, s4)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        self.create_operation_log(operation_type=OperationType.update.value, model_name=invoke_result_data.data["new"].__str__(), old_detail=invoke_result_data.data["old"], update_detail=invoke_result_data.data["new"], title=info_title)
        return self.response_json_success(invoke_result_data.data["new"].id)
    
    @filter_check_params("cms_id")
    def post_async(self):
        """
        :description: 更新资讯信息
        :params cms_id:资讯标识
        :return 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        place_id = self.get_param_int("place_id", 0)
        cms_id = self.get_param_int("cms_id", 0)
        info_title = self.get_param("info_title",None)
        simple_title = self.get_param("simple_title", None)
        simple_title_url = self.get_param("simple_title_url", None)
        info_type = self.get_param_int("info_type", -1)
        info_summary = self.get_param("info_summary", None)
        info_tag = self.get_param("info_tag", None)
        info_mark = self.get_param("info_mark", None)
        target_url = self.get_param("target_url", None)
        min_pic = self.get_param("min_pic", None)
        mid_pic = self.get_param("mid_pic", None)
        max_pic = self.get_param("max_pic", None)
        info_data = self.get_param("info_data", None)
        pic_collect_json = self.get_param("pic_collect_json", None)
        sort_index = self.get_param_int("sort_index", -1)
        is_release = self.get_param_int("is_release", -1)
        i1 = self.get_param_int("i1", -1)
        i2 = self.get_param_int("i2", -1)
        i3 = self.get_param_int("i3", -1)
        i4 = self.get_param_int("i4", -1)
        s1 = self.get_param("s1", None)
        s2 = self.get_param("s2", None)
        s3 = self.get_param("s3", None)
        s4 = self.get_param("s4", None)

        cms_base_model = CmsBaseModel(context=self)
        invoke_result_data = cms_base_model.save_cms_info(place_id, cms_id, app_id, act_id, info_title, simple_title, simple_title_url, info_type, info_summary, info_tag, info_mark, target_url, min_pic, mid_pic, max_pic, info_data, pic_collect_json, sort_index, is_release, i1, i2, i3, i4, s1, s2, s3, s4)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        self.create_operation_log(operation_type=OperationType.update.value, model_name=invoke_result_data.data["new"].__str__(), old_detail=invoke_result_data.data["old"], update_detail=invoke_result_data.data["new"], title=info_title)
        return self.response_json_success(invoke_result_data.data["new"].id)


class CmsInfoListHandler(ClientBaseHandler):
    """
    :description: 获取资讯列表
    """
    def get_async(self):
        """
        :description: 获取位置信息列表
        :params place_id:位置标识
        :return 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        place_id = self.get_param_int("place_id", 0)
        page_size = self.get_param_int("page_size", 20)
        page_index = self.get_param_int("page_index", 0)

        condition = None
        params = None
        order_by = "id desc"
        field = "*"
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_success({"data": []})
        else:
            condition = invoke_result_data.data["condition"] if invoke_result_data.data.__contains__("condition") else None
            params = invoke_result_data.data["params"] if invoke_result_data.data.__contains__("params") else None
            order_by = invoke_result_data.data["order_by"] if invoke_result_data.data.__contains__("order_by") else "id desc"
            field = invoke_result_data.data["field"] if invoke_result_data.data.__contains__("field") else "*"
        cms_base_model = CmsBaseModel(context=self)
        if condition and params:
            page_list, total = cms_base_model.get_cms_info_list_v2(place_id=place_id, page_size=page_size, page_index=page_index, order_by=order_by, field=field, condition=condition, params=params, is_cache=False)
        else:
            page_list, total = cms_base_model.get_cms_info_list(place_id=place_id, page_size=page_size, page_index=page_index, order_by=order_by, field=field, app_id=app_id, act_id=act_id, is_cache=False)
        page_info = PageInfo(page_index, page_size, total, self.business_process_executed(page_list, ref_params={}))
        return self.response_json_success(page_info)


class DeleteCmsInfoHandler(ClientBaseHandler):
    """
    :description: 删除资讯
    """

    @filter_check_params("cms_id")
    def get_async(self):
        """
        :description: 删除资讯
        :param app_id：应用标识
        :param cms_id：资讯标识
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        cms_id = self.get_param_int("cms_id", 0)
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        title_prefix = invoke_result_data.data["title_prefix"] if invoke_result_data.data.__contains__("title_prefix") else "资讯"
        cms_base_model = CmsBaseModel(context=self)
        invoke_result_data = cms_base_model.delete_cms_info(app_id, cms_id)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        self.create_operation_log(operation_type=OperationType.delete.value, model_name="cms_info_tb", title=title_prefix + ";" + invoke_result_data.data["info_title"])
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success()


class ReleaseCmsInfoHandler(ClientBaseHandler):
    """
    :description: 上下架资讯
    """

    @filter_check_params("cms_id")
    def get_async(self):
        """
        :description: 上下架资讯
        :param app_id：应用标识
        :param cms_id：资讯标识
        :param is_release: 是否发布 1-是 0-否
        :return:
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        cms_id = self.get_param_int("cms_id", 0)
        is_release = self.get_param_int("is_release", 0)
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        title_prefix = invoke_result_data.data["title_prefix"] if invoke_result_data.data.__contains__("title_prefix") else "资讯"
        cms_base_model = CmsBaseModel(context=self)
        invoke_result_data = cms_base_model.release_cms_info(app_id, cms_id, is_release)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        operation_type = OperationType.release.value if is_release == 1 else OperationType.un_release.value
        self.create_operation_log(operation_type=operation_type, model_name="cms_info_tb", title=title_prefix + ";" + invoke_result_data.data["info_title"])
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success()
