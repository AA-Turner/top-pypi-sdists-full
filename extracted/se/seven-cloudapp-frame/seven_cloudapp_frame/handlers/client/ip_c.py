# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-02 13:37:05
@LastEditTime: 2023-01-04 16:04:57
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.models.ip_base_model import *
from seven_cloudapp_frame.handlers.frame_base import *


class IpInfoListHandler(ClientBaseHandler):
    """
    :description: 获取ip列表
    """
    def get_async(self):
        """
        :description: 获取ip列表
        :param act_id：活动标识
        :param page_index：页索引
        :param page_size：页大小
        :param page_count_mode：分页模式(0-none 1-total 2-next)
        :return: list
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        page_index = self.get_param_int("page_index", 0)
        page_size = self.get_param_int("page_size", 10)
        page_count_mode = self.get_param_int("page_count_mode", 1)
        page_count_mode = SevenHelper.get_enum_key(PageCountMode, page_count_mode)
        page_list = IpBaseModel(context=self).get_ip_info_list(app_id, act_id, page_size, page_index, condition="is_release=1", page_count_mode=page_count_mode)
        if page_count_mode == "total":
            total = page_list[1]
            page_list = self.business_process_executed(page_list[0], ref_params={})
            return_info = PageInfo(page_index, page_size, total, page_list)
        elif page_count_mode == "next":
            is_next = page_list[1]
            page_list = self.business_process_executed(page_list[0], ref_params={})
            return_info = WaterPageInfo(page_list, is_next)
        else:
            return_info = self.business_process_executed(page_list, ref_params={})
        return self.response_json_success(return_info)