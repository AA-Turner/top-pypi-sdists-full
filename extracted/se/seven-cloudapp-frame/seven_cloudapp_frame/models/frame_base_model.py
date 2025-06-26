# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-11 09:10:33
@LastEditTime: 2025-04-07 15:04:57
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.libs.customize.safe_helper import SafeHelper
from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.models.seven_model import *
from seven_cloudapp_frame.models.enum import *
from seven_cloudapp_frame.models.db_models.act.act_info_model import *
from seven_cloudapp_frame.models.db_models.act.act_module_model import *
from seven_cloudapp_frame.models.db_models.user.user_info_model import *
from seven_framework import *

class FrameBaseModel():
    """
    :description: 框架业务模型 用于被其他业务模型继承，调用模型之间通用的方法
    """
    def __init__(self, context=None, check_user_type=UserType.act.value):
        """
        :description: 初始化
        :param context:上下文
        :param check_user_type:检查用户类型
        :last_editors: HuangJianYi
        """
        self.context = context
        self.check_user_type = check_user_type
        self.acquire_lock_name = ""
        self.identifier = ""
        self.request_queue_name = ""
        self.handler_name = ""
        self.act_id = 0
        self.module_id = 0
        self.user_id = 0
        self.source_object_id = ""

    def sensitive_encrypt(self, data):
        """
        :description: 敏感字段加密（保存到数据库的时候，要注意字段长度，不够的话会被截断，导致后续的解密失败）
        :param data:数据
        :return:
        :last_editors: HuangJianYi
        """
        safe_config = share_config.get_value("safe_config",{})
        sensitive_encrypt_key = safe_config.get("sensitive_encrypt_key")
        if sensitive_encrypt_key and data:
            data = CryptoHelper.aes_encrypt(data, sensitive_encrypt_key)
        return data

    def sensitive_decrypt(self, data, decrypt_field_list :list = []):
        """
        :description: 敏感字段解密
        :param data:数据
        :param decrypt_field_list:需要解密的字段列表
        :return:
        :last_editors: HuangJianYi
        """
        status = 1
        try:
            safe_config = share_config.get_value("safe_config",{})
            sensitive_encrypt_key = safe_config.get("sensitive_encrypt_key")
            if sensitive_encrypt_key:
                if decrypt_field_list and not isinstance(data, str):
                    if isinstance(data, list):
                        for dict_item in data:
                            for key, value in dict_item.items():
                                if key in decrypt_field_list and dict_item[key]:
                                    dict_item[key] = CryptoHelper.aes_decrypt(dict_item[key], sensitive_encrypt_key)
                    elif isinstance(data, dict):
                        for key, value in data.items():
                            if key in decrypt_field_list and data[key]:
                                data[key] = CryptoHelper.aes_decrypt(data[key], sensitive_encrypt_key)
                elif data:
                    data = CryptoHelper.aes_decrypt(data, sensitive_encrypt_key)
        except Exception as ex:
            status = 0
            if self.context:
                self.context.logging_link_error(f"【敏感字段解密】,info:{str(data)},ex:" + traceback.format_exc())
        return data, status

    def score_algorithm_to_score(self, weight):
        """
        :description: 分数算法，获取分数 = 权重 * 分数因子 + 时间极大值  - 当前时间
        :param weight:权重值
        :return: 分数
        :last_editors: HuangJianYi
        """
        score_fator = 1_000_000_000 #分数因子
        max_timestamp = 2_000_000_000 #时间极大值，秒级别
        score = weight * score_fator + max_timestamp - TimeHelper.get_now_timestamp()
        return score

    def score_algorithm_to_weight(self, score):
        """
        :description: 分数算法，获取分数对应的权重值
        :param score:分数
        :return: 权重值
        :last_editors: HuangJianYi
        """
        score_fator = 1_000_000_000
        return int(score/score_fator)

    def lottery_algorithm_chance(self, prize_list, field_name="chance", is_upset_prize=True):
        """
        :description: 抽奖算法（概率）
        :param prize_list:奖品列表
        :param field_name:字段名称
        :param is_upset_prize:是否打乱奖品，减少多次抽奖得到同一个奖品的概率
        :return: 中奖的奖品
        :last_editors: HuangJianYi
        """
        if is_upset_prize == True:
            random.shuffle(prize_list)
        init_value = 0.00
        probability_list = []
        for prize in prize_list:
            current_prize = prize
            current_prize["start_probability"] = init_value
            current_prize["end_probability"] = init_value + float(prize[field_name])
            probability_list.append(current_prize)
            init_value = init_value + float(prize[field_name])
        prize_index = random.uniform(0.00, init_value)
        for prize in probability_list:
            if (prize["start_probability"] <= prize_index and prize_index < prize["end_probability"]):
                return prize

    def lottery_algorithm_probability(self, prize_list, field_name="probability", is_upset_prize=True):
        """
        :description: 抽奖算法（权重）
        :param prize_list:奖品列表
        :param field_name:字段名称
        :param is_upset_prize:是否打乱奖品，减少多次抽奖得到同一个奖品的概率
        :return: 中奖的奖品
        :last_editors: HuangJianYi
        """
        if is_upset_prize == True:
            random.shuffle(prize_list)
        init_value = 0
        probability_list = []
        for prize in prize_list:
            current_prize = prize
            current_prize["start_probability"] = init_value
            current_prize["end_probability"] = init_value + prize[field_name]
            probability_list.append(current_prize)
            init_value = init_value + prize[field_name]
        prize_index = random.randint(0, init_value - 1)
        for prize in probability_list:
            if (prize["start_probability"] <= prize_index and prize_index < prize["end_probability"]):
                return prize

    def lottery_algorithm_stock_probability(self, prize_list, field_name="probability", surplus_field_name="surplus", is_upset_prize=True):
        """
        :description: 抽奖算法（库存权重）
        :param prize_list:奖品列表
        :param field_name:权重字段名称
        :param surplus_field_name:库存字段名称
        :param is_upset_prize:是否打乱奖品，减少多次抽奖得到同一个奖品的概率
        :return: 中奖的奖品
        :last_editors: HuangJianYi
        """
        if is_upset_prize == True:
            random.shuffle(prize_list)
        init_value = 0
        probability_list = []
        for prize in prize_list:
            current_prize = prize
            if prize[surplus_field_name] > 0 and prize[field_name] > 0:
                current_prize["start_probability"] = init_value
                current_prize["end_probability"] = init_value + prize[field_name] * prize[surplus_field_name]
                probability_list.append(current_prize)
                init_value = init_value + prize[field_name] * prize[surplus_field_name]
        prize_index = random.randint(0, init_value - 1)
        for prize in probability_list:
            if (prize["start_probability"] <= prize_index and prize_index < prize["end_probability"]):
                return prize

    def rounding_algorithm(self, number):
        """
        :description: "四舍六入五成双"（也称为 banker's rounding 或 commercial rounding）算法通常在金融、会计、计量等领域中被广泛应用，尤其是在需要精确计数和汇总大量数据以避免系统性偏差的情况下。这种舍入方法的主要目的是减少长时间多次舍入累积误差，使得统计结果更为准确   
        :param number: 数值
        :return: number
        :last_editors: HuangJianYi
        """

        import math

        if number < 0.001:
            return 0

        int_part = int(number)
        decimal_part = abs(number - int_part)  # 直接取绝对值的小数部分

        # 如果小数部分长度不足三位，则直接四舍五入到两位小数
        if decimal_part * 1000 % 1 == 0:
            return round(number, 2)

        third_decimal_digit = (decimal_part * 100) % 10  # 获取第三位小数

        if third_decimal_digit != 5 or decimal_part * 10 % 1 == 0:  # 不是五或没有更精确的小数位
            rounded_number = round(number, 2)
        else:
            second_decimal_digit = (decimal_part * 100) // 10 % 10  # 获取第二位小数
            if second_decimal_digit % 2 == 0:  # 第二位小数为偶数，则向下舍弃
                decimal_part = math.floor(decimal_part * 100) / 100
            else:  # 第二位小数为奇数，则向上进位
                decimal_part = math.ceil(decimal_part * 100) / 100
            rounded_number = int_part + decimal_part

        return rounded_number

    def rewards_status(self):
        """
        :description: 给予奖励的子订单状态
        :param 
        :return: 
        :last_editors: HuangJianYi
        """
        status = [
            #等待卖家发货
            "WAIT_SELLER_SEND_GOODS",
            #卖家部分发货
            "SELLER_CONSIGNED_PART",
            #等待买家确认收货
            "WAIT_BUYER_CONFIRM_GOODS",
            #买家已签收（货到付款专用）
            "TRADE_BUYER_SIGNED",
            #交易成功
            "TRADE_FINISHED"
        ]
        return status

    def refund_status(self):
        """
        :description: 给予奖励的子订单退款状态
        :param 
        :return: 
        :last_editors: HuangJianYi
        """
        status = [
            #没有退款
            "NO_REFUND",
            #退款关闭
            "CLOSED",
            #卖家拒绝退款
            "WAIT_SELLER_AGREE",
            #卖家拒绝退款
            "SELLER_REFUSE_BUYER"
        ]
        return status

    def get_order_status_name(self, order_status):
        """
        :description: 获取订单状态名称 -1未付款-2付款中0未发货1已发货2不予发货3已退款4交易成功
        :param order_status：订单状态
        :return 订单状态名称
        :last_editors: HuangJianYi
        """
        if order_status == -1:
            return "未付款"
        elif order_status == -2:
            return "付款中"
        elif order_status == 0:
            return "未发货"
        elif order_status == 1:
            return "已发货"
        elif order_status == 2:
            return "不予发货"
        elif order_status == 3:
            return "已退款"
        else:
            return "交易成功"

    def get_business_sub_table(self, table_name, param_dict):
        """
        :description: 获取分表名称(目前框架支持的分表prize_order_tb、prize_roster_tb、stat_log_tb、task_count_tb、user_asset_tb、asset_log_tb、user_info_tb)
        :param table_name:表名
        :param param_dict:参数字典
        :return:
        :last_editors: HuangJianYi
        """
        if not param_dict or not table_name:
            return None
        sub_table_config = share_config.get_value("sub_table_config",{})
        table_config = sub_table_config.get(table_name, None)
        if not table_config:
            return None
        return SevenHelper.get_sub_table(param_dict.get("app_id", 0), table_config.get("sub_count", 10))

    def process_malice_request(self, handler_name, user_id, ip="", user_request_limit_num=30, ip_request_limit_num=30, cycle_type=1, limit_request_time=24):
        """
        :description: 处理恶意请求
        :param handler_name:接口名称
        :param user_id:用户标识
        :param ip:用户ip
        :param user_request_limit_num:用户请求上限数
        :param ip_request_limit_num:ip请求上限数
        :param cycle_type:累计周期类型(1-每分钟 2-每小时 3-每天)
        :param limit_request_time:限制请求时间(单位小时)
        :return:InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        if (not user_id and not ip) or not handler_name:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "参数不能为空或等于0"
            return invoke_result_data
        project_name = config.get_value('project_name','')
        redis_config = SafeHelper.get_redis_config()
        redis_init = RedisExHelper.init(config_dict=redis_config)
        if user_id:
            objectid_key = f"malice_request:objectid_1_{handler_name}_{user_id}:db_{project_name}"
            count_key = f"malice_request:count_1_{handler_name}_{user_id}:db_{project_name}"
            objectid_value = redis_init.get(objectid_key)
            if objectid_value:
                invoke_result_data.success = False
                invoke_result_data.error_code = "malice_request_1"
                invoke_result_data.error_message = "异常操作请稍后再试"
                return invoke_result_data
            count_value = redis_init.get(count_key)
            count_value = int(count_value) if count_value else 0
            if count_value >= user_request_limit_num:
                redis_init.set(objectid_key, 1, limit_request_time * 60 * 60)
            incr_value = redis_init.incr(count_key, 1)
            if incr_value == 1:
                if cycle_type == 1:
                    redis_init.expire(count_key, 60)
                elif cycle_type == 2:
                    redis_init.expire(count_key, 60*60)
                else:
                    redis_init.expire(count_key, 24*60*60)
        if ip:
            objectid_key = f"malice_request:objectid_2_{handler_name}_{ip}:db_{project_name}"
            count_key = f"malice_request:count_2_{handler_name}_{ip}:db_{project_name}"
            objectid_value = redis_init.get(objectid_key)
            if objectid_value:
                invoke_result_data.success = False
                invoke_result_data.error_code = "malice_request_2"
                invoke_result_data.error_message = "异常操作请稍后再试"
                return invoke_result_data
            count_value = redis_init.get(count_key)
            count_value = int(count_value) if count_value else 0
            if count_value >= ip_request_limit_num:
                redis_init.set(objectid_key, 1, limit_request_time * 60 * 60)
            incr_value = redis_init.incr(count_key, 1)
            if incr_value == 1:
                if cycle_type == 1:
                    redis_init.expire(count_key, 60)
                elif cycle_type == 2:
                    redis_init.expire(count_key, 60*60)
                else:
                    redis_init.expire(count_key, 24*60*60)
        return invoke_result_data

    def check_act_info(self, act_id, check_release=True):
        """
        :description: 检验活动信息
        :param act_id:活动标识
        :param check_release:校验活动信息发布
        :return:invoke_result_data
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        act_info_model = ActInfoModel(context=self.context, is_auto=True)
        act_info_dict = act_info_model.get_cache_dict_by_id(act_id,dependency_key=DependencyKey.act_info(act_id))
        if not act_info_dict or act_info_dict["is_del"] == 1:
            invoke_result_data.success = False
            invoke_result_data.error_code = "no_act"
            invoke_result_data.error_message = "活动信息不存在"
            return invoke_result_data
        if check_release == True and act_info_dict["is_release"] == 0:
            invoke_result_data.success = False
            invoke_result_data.error_code = "no_act"
            invoke_result_data.error_message = "活动已下架"
            return invoke_result_data
        now_date = SevenHelper.get_now_datetime()
        act_info_dict["start_date"] = str(act_info_dict["start_date"])
        act_info_dict["end_date"] = str(act_info_dict["end_date"])
        if act_info_dict["start_date"] != "" and act_info_dict["start_date"] != "1900-01-01 00:00:00":
            if now_date < act_info_dict["start_date"]:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "活动将在" + act_info_dict['start_date'] + "开启"
                return invoke_result_data
        if act_info_dict["end_date"] != "" and act_info_dict["end_date"] != "1900-01-01 00:00:00":
            if now_date > act_info_dict["end_date"]:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "活动已结束"
                return invoke_result_data
        invoke_result_data.data = act_info_dict
        return invoke_result_data

    def check_act_module(self, module_id, check_release=True):
        """
        :description: 检验活动模块
        :param module_id:活动模块标识
        :param check_release:校验活动信息发布
        :return:invoke_result_data
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        if module_id:
            act_module_model = ActModuleModel(context=self.context, is_auto=True)
            act_module_dict = act_module_model.get_cache_dict_by_id(module_id,dependency_key=DependencyKey.act_module(module_id))
            if not act_module_dict or act_module_dict["is_del"] == 1:
                invoke_result_data.success = False
                invoke_result_data.error_code = "no_module"
                invoke_result_data.error_message = "活动模块信息不存在"
                return invoke_result_data
            if check_release == True and act_module_dict["is_release"] == 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = "no_module"
                invoke_result_data.error_message = "活动模块已下架"
                return invoke_result_data
            now_date = SevenHelper.get_now_datetime()
            act_module_dict["start_date"] = str(act_module_dict["start_date"])
            act_module_dict["end_date"] = str(act_module_dict["end_date"])
            if act_module_dict["start_date"] != "" and act_module_dict["start_date"] != "1900-01-01 00:00:00":
                if now_date < act_module_dict["start_date"]:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "活动将在" + act_module_dict["start_date"] + "开启"
                    return invoke_result_data
            if act_module_dict["end_date"] != "" and act_module_dict["end_date"] != "1900-01-01 00:00:00":
                if now_date > act_module_dict["end_date"]:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "活动已结束"
                    return invoke_result_data
            invoke_result_data.data = act_module_dict
        return invoke_result_data

    def check_user_info(self, app_id, act_id, user_id, login_token, check_new_user, check_user_nick):
        """
        :description: 检验用户信息
        :param app_id:应用标识
        :param act_id:活动标识
        :param user_id:用户标识
        :param login_token:访问令牌
        :param check_new_user:是否新用户才能参与
        :param check_user_nick:是否校验昵称为空
        :return:invoke_result_data
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        user_info_model = UserInfoModel(context=self.context).set_sub_table(app_id)
        if self.check_user_type == UserType.app.value:
            act_id = 0
        id_md5 = CryptoHelper.md5_encrypt_int(f"{act_id}_{user_id}") if act_id > 0 else CryptoHelper.md5_encrypt_int(f"{app_id}_0_{user_id}")
        user_info_dict = user_info_model.get_cache_dict("id_md5=%s", limit="1", params=[id_md5], dependency_key=DependencyKey.user_info(act_id, id_md5))
        if not user_info_dict:
            invoke_result_data.success = False
            invoke_result_data.error_code = "no_user"
            invoke_result_data.error_message = "用户信息不存在"
            return invoke_result_data
        if user_info_dict["app_id"] != app_id and SafeHelper.authenticat_app_id(user_info_dict["app_id"], app_id) == False:
            invoke_result_data.success = False
            invoke_result_data.error_code = "no_power"
            invoke_result_data.error_message = "用户信息不存在"
            return invoke_result_data
        if user_info_dict["user_state"] == 1:
            invoke_result_data.success = False
            invoke_result_data.error_code = "user_exception"
            invoke_result_data.error_message = "账号异常,请联系客服处理"
            return invoke_result_data
        if check_new_user == True and user_info_dict["is_new"] == 0:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "不是新用户"
            return invoke_result_data
        if check_user_nick == True:
            if not user_info_dict["user_nick"] and not user_info_dict["user_nick_encrypt"]:
                invoke_result_data.success = False
                invoke_result_data.error_code = "no_authorize"
                invoke_result_data.error_message = "对不起,请先授权"
                return invoke_result_data
        if login_token and user_info_dict["login_token"] != login_token:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "已在另一台设备登录,无法操作"
            return invoke_result_data
        invoke_result_data.data = user_info_dict
        return invoke_result_data

    def check_request_queue(self, request_queue_name, request_limit_num, request_limit_time):
        """
        :description: 检验请求队列,用于流量削峰判断
        :param request_queue_name:请求队列名称
        :param request_limit_num:请求限制数(指的是当前接口在指定时间内可以请求的次数，用于流量削峰，减少短时间内的大量请求)；0不限制
        :param request_limit_time:请求限制时间；默认1秒
        :return:invoke_result_data
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        if request_limit_num > 0  and request_limit_time > 0:
            if SafeHelper.check_current_limit_by_time_window(request_queue_name, request_limit_num, request_limit_time) == True:
                invoke_result_data.success = False
                invoke_result_data.error_code = "current_limit"
                invoke_result_data.error_message = "当前人气火爆,请稍后再试"
                return invoke_result_data

        return invoke_result_data

    def business_process_executing(self, app_id, act_id, module_id, user_id, login_token, handler_name, check_new_user=False, check_user_nick=True, continue_request_expire=0, acquire_lock_name="", request_limit_num=0, request_limit_time=1, source_object_id="",check_act_info=True,check_act_module=True,check_user_info=True,check_act_info_release=True,check_act_module_release=True,execute_lock_expire=90):
        """
        :description: 业务执行前事件,核心业务如抽奖、做任务需要调用当前方法
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param login_token:访问令牌
        :param handler_name:接口名称
        :param check_new_user:是否新用户才能参与
        :param check_user_nick:是否校验昵称为空
        :param continue_request_expire:连续请求锁过期时间，为0不进行校验，单位秒 
        :param acquire_lock_name:分布式锁名称，为空则不开启分布式锁校验功能
        :param request_limit_num:【流量削峰】滑动窗口计数法,请求限制数(指的是当前接口在指定时间内可以请求的次数，减少短时间内的大量请求)；0不限制
        :param request_limit_time:【流量削峰】请求限制时间；默认1秒
        :param source_object_id:来源对象标识
        :param check_act_info:是否检验活动信息
        :param check_act_module:是否检验活动模块信息
        :param check_user_info:是否校验用户信息
        :param check_act_info_release:校验活动信息是否发布
        :param check_act_module_release:校验活动模块是否发布
        :param execute_lock_expire:执行锁过期时间，为0不进行校验，单位秒
        :return:
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        self.handler_name = handler_name
        self.act_id = act_id
        self.module_id = module_id
        self.user_id = user_id
        self.source_object_id = source_object_id
        self.execute_lock_key = ""

        if not act_id or not user_id or not handler_name:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "参数不能为空或等于0"
            return invoke_result_data

        #请求锁，请求太频繁限制
        redis_config = SafeHelper.get_redis_config()
        if continue_request_expire > 0:
            #为了防止项目设置的时间太长，影响用户体验，暂定不超过5
            continue_request_expire = 5 if continue_request_expire > 5 else continue_request_expire
            continue_request_key = f"request_business_executing:{handler_name}_{act_id}_{module_id}_{user_id}"
            if source_object_id:
                continue_request_key += f"_{source_object_id}"
            if redis_config.get("is_cluster", False) == True:
                continue_request_key += f":db_{config.get_value('project_name','')}"

            if SevenHelper.is_continue_request(continue_request_key, expire=continue_request_expire * 1000, config_dict=redis_config) == True:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = f"对不起,请{continue_request_expire}秒后再试"
                return invoke_result_data
        #执行锁
        if execute_lock_expire > 0:
            self.execute_lock_key = f"request_business_executed:{handler_name}_{act_id}_{module_id}_{user_id}"
            if source_object_id:
                self.execute_lock_key += f"_{source_object_id}"
            if redis_config.get("is_cluster", False) == True:
                self.execute_lock_key += f":db_{config.get_value('project_name','')}"
            if SevenHelper.is_continue_request(self.execute_lock_key, expire=execute_lock_expire * 1000, config_dict=redis_config) == True:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = f"请求处理中,请{execute_lock_expire}秒后再试"
                return invoke_result_data

        #校验活动
        act_info_dict = None
        if check_act_info == True:
            invoke_result_data = self.check_act_info(act_id,check_act_info_release)
            if invoke_result_data.success == False:
                return invoke_result_data
            act_info_dict = invoke_result_data.data
            authenticat_app_id = act_info_dict["app_id"]
            invoke_result_data.data = None
            if SafeHelper.authenticat_app_id(authenticat_app_id, app_id) == False:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "非法操作"
                return invoke_result_data
        #校验活动模块
        act_module_dict = None
        if check_act_module == True and module_id > 0:
            invoke_result_data = self.check_act_module(module_id,check_act_module_release)
            if invoke_result_data.success == False:
                return invoke_result_data
            act_module_dict = invoke_result_data.data
            authenticat_app_id = act_module_dict["app_id"]
            invoke_result_data.data = None
            if SafeHelper.authenticat_app_id(authenticat_app_id, app_id) == False:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "非法操作"
                return invoke_result_data
        #校验用户信息
        user_info_dict = None
        if check_user_info == True:
            invoke_result_data = self.check_user_info(app_id,act_id,user_id,login_token,check_new_user,check_user_nick)
            if invoke_result_data.success == False:
                return invoke_result_data
            user_info_dict = invoke_result_data.data
            invoke_result_data.data = None

        #流量削峰
        request_queue_name = ""
        if request_limit_num > 0 and request_limit_time > 0:
            request_queue_name = f"request_queue:{handler_name}_{act_id}_{module_id}"
            invoke_result_data = self.check_request_queue(request_queue_name,request_limit_num,request_limit_time)
            if invoke_result_data.success == False:
                return invoke_result_data

        #分布式锁名称存在才进行校验
        identifier = ""
        if acquire_lock_name:
            if redis_config.get("is_cluster", False) == True:
                acquire_lock_name += f":db_{config.get_value('project_name','')}"
            acquire_lock_status, identifier = RedisExHelper.acquire_lock(acquire_lock_name,config_dict=redis_config)
            if acquire_lock_status == False:
                invoke_result_data.success = False
                invoke_result_data.error_code = "acquire_lock"
                invoke_result_data.error_message = "当前人气火爆,请稍后再试"
                return invoke_result_data

        invoke_result_data.data = {}
        invoke_result_data.data["act_info_dict"] = act_info_dict
        invoke_result_data.data["act_module_dict"] = act_module_dict
        invoke_result_data.data["user_info_dict"] = user_info_dict
        invoke_result_data.data["identifier"] = identifier
        invoke_result_data.data["request_queue_name"] = request_queue_name

        self.acquire_lock_name = acquire_lock_name
        self.identifier = identifier
        self.request_queue_name = request_queue_name

        return invoke_result_data

    def business_process_executed(self, act_id=0, module_id=0, user_id=0, handler_name="", acquire_lock_name="", identifier="", request_queue_name="", source_object_id=""):
        """
        :description: 业务执行后事件，调用了业务执行前事件需要调用当前方法,参数可以不传，默认用business_process_executing方法传递的参数
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param handler_name:接口名称
        :param acquire_lock_name:分布式锁名称
        :param identifier:分布式锁标识
        :param request_queue_name:请求队列名称
        :param source_object_id:来源对象标识
        :return:
        :last_editors: HuangJianYi
        """
        if not acquire_lock_name:
            acquire_lock_name = self.acquire_lock_name
        if not identifier:
            identifier = self.identifier
        if not request_queue_name:
            request_queue_name = self.request_queue_name
        if not source_object_id:
            source_object_id = self.source_object_id
        if not handler_name:
            handler_name = self.handler_name
        if not act_id:
            act_id = self.act_id
        if not module_id:
            module_id = self.module_id
        if not user_id:
            user_id = self.user_id

        redis_config = SafeHelper.get_redis_config()
        if hasattr(self,"execute_lock_key"):
            RedisExHelper.init(config_dict=redis_config).delete(self.execute_lock_key)
        if acquire_lock_name and identifier:
            RedisExHelper.release_lock(acquire_lock_name, identifier, config_dict=redis_config)
