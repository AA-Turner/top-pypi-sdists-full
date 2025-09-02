# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2020-05-02 15:17:41
@LastEditTime: 2024-08-23 14:17:31
@LastEditors: HuangJianYi
:description: 自定义实体模型
"""

class InvokeResult():
    """
    :description: 接口返回实体
    :return: InvokeResult
    :last_editors: HuangJianYi
    """
    def __init__(self):
        self.success = True
        self.data = InvokeResultData().__dict__


class InvokeResultData():
    """
    :description: 接口返回实体
    :return: InvokeResultData
    :last_editors: HuangJianYi
    """
    def __init__(self):
        self.success = True
        self.data = None
        self.error_code = ""
        self.error_message = ""


class FileUploadInfo():
    """
    :description: 文件上传信息实体
    :return: FileUploadInfo
    :last_editors: HuangJianYi
    """
    def __init__(self):
        # 检查值
        self.md5_value = ""
        # 上传路经
        self.resource_path = ""
        # 原文件名
        self.original_name = ""
        # 文件路经
        self.file_path = ""
        # 图片宽度
        self.image_width = 0
        # 图片高度
        self.image_height = 0


class PageInfo():
    """
    :description: 分页列表实体
    :last_editors: HuangJianYi
    """
    def __init__(self, page_index=0, page_size=10, record_count=0, data=None):
        """
        :description: 分页列表实体
        :param page_index：当前索引号
        :param page_size：页大小
        :param record_count：总记录数
        :param data：数据
        :return: PageInfo
        :last_editors: HuangJianYi
        """
        # 数据
        self.data = data
        # 当前索引号
        self.page_index = page_index
        # 页大小
        self.page_size = page_size
        # 总记录数
        self.record_count = record_count

        # 页数
        if page_size == 0:
            self.page_count = 0
        else:
            self.page_count = record_count / page_size + 1
            if record_count % page_size == 0:
                self.page_count = record_count / page_size
            self.page_count = int(self.page_count)

        # 当前页号
        self.page_no = page_index + 1

        # 上一页索引
        self.previous_index = page_index - 1 if page_index > 0 else 0

        # 下一页索引
        self.next_index = page_index + 1
        if self.page_count == 0:
            self.next_index = 0
        if self.page_no >= self.page_count:
            self.next_index = self.page_index

        # 是否下一页
        self.is_next = True
        if self.page_count == 0:
            self.is_next = False
        if self.page_no >= self.page_count:
            self.is_next = False

        # 是否上一页
        self.is_previous = True
        if page_index == 0:
            self.is_previous = False


class WaterPageInfo():
    """
    :description: 瀑布流分页列表实体
    :last_editors: HuangJianYi
    """
    def __init__(self, data=None, is_next=False):
        """
        :description: 瀑布流分页列表实体
        :param data：数据
        :param is_next：是否有下一页（True是False否）
        :return: WaterPageInfo
        :last_editors: HuangJianYi
        """
        # 数据
        self.data = data
        # 是否下一页
        self.is_next = is_next


class ConditionWhere():
    """
    @description: 条件拼接实体
    """
    def __init__(self):
        
        self.condition_list = []

    def add_condition(self, condition):
        """
        :description: 添加条件
        :param condition:条件
        :return:
        :last_editors: HuangJianYi
        """
        self.condition_list.append(condition)

    def to_string(self, split_str="and"):
        """
        :description: 拼接成字符串
        :param split_str:分隔符
        :return:
        :last_editors: HuangJianYi
        """
        return str(" " + split_str + " ").join(self.condition_list)


class DependencyKey():
    """
    @description: 依赖建
    """
    @classmethod
    def user_account(self, open_id):
        """
        :description: 用户账号单条数据
        :param open_id: open_id
        :return str
        :last_editors: HuangJianYi
        """
        return f"user_account:openid_{open_id}"

    @classmethod
    def app_info(self, app_id):
        """
        :description: 活动单条数据
        :param act_id: 应用标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"app_info:appid_{app_id}"

    @classmethod
    def act_info(self, act_id):
        """
        :description: 活动单条数据
        :param act_id: 活动标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"act_info:actid_{act_id}"

    @classmethod
    def act_info_list(self, app_id):
        """
        :description: 活动列表
        :param app_id: 应用标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"act_info_list:appid_{app_id}"

    @classmethod
    def act_module(self, module_id):
        """
        :description: 活动模块单条数据
        :param module_id: 模块标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"act_module:moduleid_{module_id}"
    
    @classmethod
    def act_module_list(self, act_id):
        """
        :description: 活动模块列表
        :param act_id: 活动标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"act_module_list:actid_{act_id}"
    
    @classmethod
    def asset_log_list(self, act_id, user_id):
        """
        :description: 资产流水列表
        :param act_id: 活动标识
        :param user_id: 用户标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"asset_log_list:actid_{act_id}_userid_{user_id}"

    @classmethod
    def store_asset_log_list(self, app_id):
        """
        :description: 商家资产流水列表
        :param app_id: 应用标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"store_asset_log_list:appid_{app_id}"
    
    @classmethod
    def cms_info_list(self, place_id):
        """
        :description: 位置信息列表
        :param place_id: 位置标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"cms_info_list:placeid_{place_id}"

    @classmethod
    def dict_info_list(self, parent_id, dict_type):
        """
        :description: 字典信息列表
        :param parent_id: 父节点标识
        :param dict_type: 字典类型
        :return str
        :last_editors: HuangJianYi
        """
        if parent_id and dict_type:
            return f"dict_info_list:parentid_{parent_id}_dicttype_{dict_type}"
        if parent_id:
            return f"dict_info_list:parentid_{parent_id}"
        if dict_type:
            return f"dict_info_list:dicttype_{dict_type}"

    @classmethod
    def ip_info(self, ip_id):
        """
        :description: ip信息单条数据
        :param ip_id: ip标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"ip_info:ipid_{ip_id}"

    @classmethod
    def ip_info_list(self, act_id, type_id=0):
        """
        :description: 位置信息列表
        :param act_id: 活动标识
        :param type_id: ip类型标识
        :return str
        :last_editors: HuangJianYi
        """
        if type_id:
            return f"ip_info_list:actid_{act_id}_typeid_{type_id}"
        else:
            return f"ip_info_list:actid_{act_id}"

    @classmethod
    def ip_type(self, type_id):
        """
        :description: ip类型单条数据
        :param type_id: ip类型标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"ip_type:typeid_{type_id}"

    @classmethod
    def ip_type_list(self, act_id):
        """
        :description: ip类型列表
        :param act_id: 活动标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"ip_type_list:actid_{act_id}"

    @classmethod
    def prize_order_list(self, act_id, user_id=0, app_id=''):
        """
        :description: 奖品订单列表
        :param act_id: 活动标识
        :param user_id: 用户标识
        :param app_id: 应用标识
        :return str
        :last_editors: HuangJianYi
        """
        dependency_key = f"prize_order_list:actid_{act_id}"
        if user_id:
            dependency_key += f"_userid_{user_id}"
        if act_id == 0 and app_id:
            dependency_key += f"_appid_{app_id}"
        return dependency_key

    @classmethod
    def prize_roster_list(self, act_id, user_id=0, app_id=''):
        """
        :description: 中奖记录列表
        :param act_id: 活动标识
        :param user_id: 用户标识
        :param app_id: 应用标识
        :return str
        :last_editors: HuangJianYi
        """
        act_id = act_id if act_id > 0 else 0
        dependency_key = f"prize_roster_list:actid_{act_id}"
        if user_id:
            dependency_key += f"_userid_{user_id}"
        if act_id == 0 and app_id:
            dependency_key += f"_appid_{app_id}"
        return dependency_key

    @classmethod
    def price_gear_list(self, act_id):
        """
        :description: 价格档位列表
        :param act_id: 活动标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"price_gear_list:actid_{act_id}"
    
    @classmethod
    def act_prize(self, prize_id):
        """
        :description: 活动奖品单条数据
        :param prize_id: 活动奖品标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"act_prize:prizeid_{prize_id}"

    @classmethod
    def act_prize_list(self, act_id, module_id=0):
        """
        :description: 活动奖品列表
        :param act_id: 活动标识
        :param module_id: 模块标识
        :return str
        :last_editors: HuangJianYi
        """
        dependency_key = f"act_prize_list:actid_{act_id}"
        if module_id:
            dependency_key += f"_moduleid_{module_id}"
        return dependency_key

    @classmethod
    def coupon(self, coupon_id):
        """
        :description: 淘宝优惠券单条数据
        :param coupon_id: 淘宝优惠券标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"coupon:id_{coupon_id}"

    @classmethod
    def coupon_list(self, act_id):
        """
        :description: 淘宝优惠券列表
        :param act_id: 活动标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"coupon_list:id_{act_id}"

    @classmethod
    def task_info(self, task_id):
        """
        :description: 任务单条数据
        :param task_id: 任务标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"task_info:taskid_{task_id}"

    @classmethod
    def task_info_list(self, act_id):
        """
        :description: 任务列表
        :param act_id: 活动标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"task_info_list:actid_{act_id}"

    @classmethod
    def user_info(self, act_id, id_md5, open_id=""):
        """
        :description: 用户信息单条数据
        :param act_id：活动标识
        :param id_md5：用户md5标识
        :param open_id：open_id
        :return str
        :last_editors: HuangJianYi
        """
        if id_md5:
            return f"user_info:actid_{act_id}_idmd5_{id_md5}"
        else:
            return f"user_info:actid_{act_id}_openid_{open_id}"

    @classmethod
    def user_address_list(self, act_id, user_id):
        """
        :description: 用户地址列表
        :param act_id: 活动标识
        :param user_id: 用户标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"user_address_list:actid_{act_id}_userid_{user_id}"
        
    @classmethod
    def user_black(self, act_id, user_id):
        """
        :description: 用户黑名单单条数据
        :param act_id：活动标识
        :param user_id: 用户标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"user_black:{act_id}_{user_id}"

    @classmethod
    def invite_log_member_list(self, act_id, user_id):
        """
        :description: 邀请加入会员记录
        :param act_id：活动标识
        :param user_id: 用户标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"invite_log_member_list:actid_{act_id}_userid_{user_id}"

    @classmethod
    def invite_log_list(self, act_id, user_id):
        """
        :description: 邀请进入小程序记录
        :param act_id：活动标识
        :param user_id: 用户标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"invite_log_list:actid_{act_id}_userid_{user_id}"
     
    @classmethod
    def collect_log(self, act_id, user_id):
        """
        :description: 收藏日志
        :param act_id：活动标识
        :param user_id: 用户标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"collect_log:actid_{act_id}_userid_{user_id}"

    @classmethod
    def browse_log(self, act_id, user_id):
        """
        :description: 浏览日志
        :param act_id：活动标识
        :param user_id: 用户标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"browse_log:actid_{act_id}_userid_{user_id}"
    
    @classmethod
    def invite_user_help_list(self, id_md5, user_id):
        """
        :description: 邀请用户助力记录
        :param id_md5：id_md5
        :param user_id：邀请人用户标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"invite_help_list:{id_md5}_{user_id}"
    
    @classmethod
    def app_relation(self, app_id):
        """
        :description: 应用关联
        :param app_id：app_id
        :return str
        :last_editors: HuangJianYi
        """
        return f"app_relation:appid_{app_id}"
    
    
    @classmethod
    def user_asset(self, act_id, user_id):
        """
        :description: 用户资产
        :param act_id：活动标识
        :param user_id：用户标识
        :return str
        :last_editors: HuangJianYi
        """
        return f"user_asset:actid_{act_id}_userid_{user_id}"
    
    
