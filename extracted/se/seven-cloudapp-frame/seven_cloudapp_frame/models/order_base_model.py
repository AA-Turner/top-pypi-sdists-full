# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-09 09:24:43
@LastEditTime: 2025-08-19 09:40:26
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.libs.customize.safe_helper import SafeHelper
from seven_cloudapp_frame.libs.customize.wechat_helper import WeChatPayRequest
from seven_cloudapp_frame.models.user_base_model import UserBaseModel
from seven_cloudapp_frame.models.frame_base_model import FrameBaseModel
from seven_cloudapp_frame.models.seven_model import *
from seven_cloudapp_frame.models.app_base_model import *
from seven_cloudapp_frame.models.top_base_model import *
from seven_cloudapp_frame.models.price_base_model import *
from seven_cloudapp_frame.models.asset_base_model import *
from seven_cloudapp_frame.models.third.shakeshop_base_model import ShakeShopBaseModel
from seven_cloudapp_frame.models.db_models.act.act_module_model import *
from seven_cloudapp_frame.models.db_models.prize.prize_order_model import *
from seven_cloudapp_frame.models.db_models.prize.prize_roster_model import *
from seven_cloudapp_frame.models.db_models.tao.tao_pay_order_model import *
from seven_cloudapp_frame.models.db_models.third.third_pay_order_model import *
from seven_cloudapp_frame.models.db_models.third.third_main_order_model import *
from seven_cloudapp_frame.models.db_models.user.user_info_model import *
from seven_cloudapp_frame.models.db_models.tao.tao_coupon_model import *
from seven_cloudapp_frame.models.db_models.pay.pay_order_model import *
from seven_cloudapp_frame.models.db_models.refund.refund_order_model import *


class OrderBaseModel(FrameBaseModel):
    """
    :description: 订单和中奖记录相关业务模型
    """
    def __init__(self, context=None,logging_error=None, logging_info=None):
        self.context = context
        self.logging_link_error = logging_error
        self.logging_link_info = logging_info
        self.db_connect_key, self.redis_config_dict = SevenHelper.get_connect_config("db_order","redis_order")
        super(OrderBaseModel,self).__init__(context)

    def _delete_prize_order_dependency_key(self, act_id, user_id, delay_delete_time=0.1, app_id=''):
        """
        :description: 删除订单依赖建
        :param act_id: 活动标识
        :param user_id: 用户标识
        :param delay_delete_time: 延迟删除时间，传0则不进行延迟
        :param app_id: 应用标识
        :return: 
        :last_editors: HuangJianYi
        """
        PrizeOrderModel().delete_dependency_key(DependencyKey.prize_order_list(act_id, user_id, app_id), delay_delete_time)

    def _delete_prize_roster_dependency_key(self, act_id, user_id, delay_delete_time=0.1, app_id=''):
        """
        :description: 删除中奖记录依赖建
        :param act_id: 活动标识
        :param user_id: 用户标识
        :param delay_delete_time: 延迟删除时间，传0则不进行延迟
        :param app_id: 应用标识
        :return: 
        :last_editors: HuangJianYi
        """
        PrizeRosterModel().delete_dependency_key(DependencyKey.prize_roster_list(act_id, user_id, app_id), delay_delete_time)

    def get_prize_order_list(self, app_id, act_id, user_id, open_id, nick_name, order_no, real_name, telephone, address, order_status, create_date_start, create_date_end, page_size=20, page_index=0, order_by="id desc", field="*", is_search_roster=False, is_cache=True, condition="", params=[], prize_roster_sub_table=None, page_count_mode="total", is_auto=False, decrypt_field_list=["real_name", "telephone", "province", "city", "county", "street", "address", "cs_modify_address"]):
        """
        :description: 用户奖品订单列表
        :param app_id：应用标识
        :param act_id：活动标识
        :param user_id：用户标识
        :param open_id：open_id
        :param order_no：订单号
        :param nick_name：用户昵称
        :param real_name：用户名字
        :param telephone：联系电话
        :param address：收货地址
        :param order_status：订单状态（-1未付款-2付款中0未发货1已发货2不予发货3已退款4交易成功）
        :param create_date_start：订单创建时间开始
        :param create_date_end：订单创建时间结束
        :param page_size：页大小
        :param page_index：页索引
        :param order_by：排序
        :param field：查询字段
        :param is_search_roster：是否查询订单关联中奖记录
        :param is_cache：是否缓存
        :param condition：条件
        :param params：参数化数组
        :param prize_roster_sub_table：奖品记录分表名称
        :param page_count_mode: 分页计数模式 total-计算总数(默认) next-计算是否有下一页(bool) none-不计算
        :param is_auto: True-走从库 False-走主库
        :param decrypt_field_list: 需要解密的字段列表        
        :return:
        :last_editors: HuangJianYi
        """
        real_name = self.sensitive_encrypt(real_name)
        telephone = self.sensitive_encrypt(telephone)


        page_list = []
        params_list = []
        condition_where = ConditionWhere()
        if app_id:
            condition_where.add_condition("app_id=%s")
            params_list.append(app_id)
        if act_id >= 0:
            condition_where.add_condition("act_id=%s")
            params_list.append(act_id)
        if condition:
            condition_where.add_condition(condition)
            params_list.extend(params)
        if user_id:
            condition_where.add_condition("user_id=%s")
            params_list.append(user_id)
        if open_id:
            condition_where.add_condition("open_id=%s")
            params_list.append(open_id)
        if order_no:
            condition_where.add_condition("order_no=%s")
            params_list.append(order_no)
        if nick_name:
            condition_where.add_condition("user_nick=%s")
            params_list.append(nick_name)
        if real_name:
            condition_where.add_condition("real_name=%s")
            params_list.append(real_name)
        if telephone:
            condition_where.add_condition("telephone=%s")
            params_list.append(telephone)
        if address:
            address = f"{address}%"
            condition_where.add_condition("address like %s")
            params_list.append(address)
        if order_status >=-2:
            condition_where.add_condition("order_status=%s")
            params_list.append(order_status)
        if create_date_start:
            condition_where.add_condition("create_date>=%s")
            params_list.append(create_date_start)
        if create_date_end:
            condition_where.add_condition("create_date<=%s")
            params_list.append(create_date_end)
        prize_order_model = PrizeOrderModel(context=self.context, is_auto=is_auto).set_sub_table(app_id)
        if is_cache:
            page_list = prize_order_model.get_cache_dict_page_list(field, page_index, page_size, condition_where.to_string(), "", order_by, params_list, dependency_key=DependencyKey.prize_order_list(act_id, user_id, app_id), page_count_mode=page_count_mode)
        else:
            page_list = prize_order_model.get_dict_page_list(field, page_index, page_size, condition_where.to_string(), "", order_by, params_list, page_count_mode)
        result = None
        if page_count_mode in ['total','next']:
            result = page_list[1]
            page_list = page_list[0]
        if is_search_roster == True:
            if not prize_roster_sub_table:
                prize_roster_sub_table = self.get_business_sub_table("prize_roster_tb",{"app_id":app_id})
            prize_roster_model = PrizeRosterModel(sub_table=prize_roster_sub_table, context=self.context)
            if page_list and len(page_list)>0:
                order_no_list = [str(i['order_no']) for i in page_list]
                prize_roster_list_dict = prize_roster_model.get_dict_list(SevenHelper.get_condition_by_str_list("order_no",order_no_list))
                for i in range(len(page_list)):
                    roster_list = [prize_roster for prize_roster in prize_roster_list_dict if page_list[i]["order_no"] == prize_roster["order_no"]]
                    page_list[i]["roster_list"] = roster_list
        # 敏感字段处理
        page_list, status = self.sensitive_decrypt(page_list, decrypt_field_list)

        if page_count_mode in ['total','next']:
            return page_list, result
        return page_list

    def update_prize_order_status(self,app_id,act_id,prize_order_id,order_status,express_company="",express_no="",prize_roster_sub_table=None):
        """
        :description: 更新用户奖品订单状态
        :param app_id：应用标识
        :param act_id：活动标识
        :param prize_order_id：奖品订单标识
        :param order_status：订单状态
        :param express_company：快递公司
        :param express_no：快递单号
        :param prize_roster_sub_table：奖品记录分表名称
        :return: 实体模型InvokeResultData
        :last_editors: HuangJianYi
        """
        now_datetime = SevenHelper.get_now_datetime()
        db_transaction = DbTransaction(db_config_dict=config.get_value(self.db_connect_key), context=self.context)
        prize_order_model = PrizeOrderModel(db_transaction=db_transaction, context=self.context).set_sub_table(app_id)
        if not prize_roster_sub_table:
            prize_roster_sub_table = self.get_business_sub_table("prize_roster_tb",{"app_id":app_id})
        prize_roster_model = PrizeRosterModel(sub_table=prize_roster_sub_table, db_transaction=db_transaction, context=self.context)
        invoke_result_data = InvokeResultData()

        prize_order = prize_order_model.get_entity_by_id(prize_order_id)
        if not prize_order:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message ="奖品订单信息不存在-1"
            return invoke_result_data
        if SafeHelper.authenticat_app_id(prize_order.app_id, app_id) == False:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message ="奖品订单信息不存在-2"
            return invoke_result_data
        try:
            db_transaction.begin_transaction()
            if order_status == 1:
                if not express_company and not express_no:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message ="快递公司或快递单号不能为空"
                    return invoke_result_data
                update_sql = "order_status=1,express_company=%s,express_no=%s,deliver_date=%s,modify_date=%s"
                params = [express_company, express_no, now_datetime, now_datetime, prize_order_id]
                prize_order_model.update_table(update_sql, "id=%s", params)
                prize_roster_model.update_table("logistics_status=1", "order_no=%s", [prize_order.order_no])
            elif order_status == 2:
                update_sql = "order_status=2,modify_date=%s"
                params = [now_datetime, prize_order_id]
                prize_order_model.update_table(update_sql, "id=%s", params)
                prize_roster_model.update_table("logistics_status=2", "order_no=%s", [prize_order.order_no])
            else:
                prize_order_model.update_table("order_status=%s,modify_date=%s", "id=%s", [order_status, now_datetime, prize_order_id])
                if order_status == 0:
                    prize_roster_model.update_table("logistics_status=0", "order_no=%s", [prize_order.order_no])
            result,message = db_transaction.commit_transaction(True)
            if result == False:
                raise Exception("执行事务失败",message)
            prize_order_model.delete_dependency_keys([DependencyKey.prize_order_list(prize_order.act_id, prize_order.user_id, prize_order.app_id), DependencyKey.prize_roster_list(prize_order.act_id, prize_order.user_id, prize_order.app_id)])

        except Exception as ex:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message ="操作失败"
            return invoke_result_data
        invoke_result_data.data = prize_order.__dict__
        return invoke_result_data

    def update_prize_order_seller_remark(self,app_id,act_id,prize_order_id,seller_remark):
        """
        :description: 更新用户奖品订单卖家备注
        :param app_id：应用标识
        :param act_id：活动标识
        :param prize_order_id：奖品订单标识
        :param seller_remark：卖家备注
        :return: 实体模型InvokeResultData
        :last_editors: HuangJianYi
        """
        now_datetime = SevenHelper.get_now_datetime()
        prize_order_model = PrizeOrderModel(context=self.context).set_sub_table(app_id)
        invoke_result_data = InvokeResultData()

        prize_order = prize_order_model.get_entity_by_id(prize_order_id)
        if not prize_order:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message ="奖品订单信息不存在-1"
            return invoke_result_data
        if SafeHelper.authenticat_app_id(prize_order.app_id, app_id) == False:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message ="奖品订单信息不存在-2"
            return invoke_result_data
        prize_order_model.update_table("seller_remark=%s,modify_date=%s", "id=%s", [seller_remark, now_datetime, prize_order_id])
        invoke_result_data.data = prize_order.__dict__
        return invoke_result_data

    def update_prize_order_receive_address(self, app_id, act_id, prize_order_id, province=None, city=None, county=None, street=None, address=None, real_name=None, telephone=None):
        """
        :description: 更新用户奖品订单收货地址
        :param app_id：应用标识
        :param act_id：活动标识
        :param prize_order_id：奖品订单标识
        :param province:省
        :param city:市
        :param county:区县
        :param street:街道
        :param address:地址
        :param real_name:用户名
        :param telephone:电话
        :return: 实体模型InvokeResultData
        :last_editors: HuangJianYi
        """

        now_datetime = SevenHelper.get_now_datetime()
        prize_order_model = PrizeOrderModel(context=self.context).set_sub_table(app_id)
        invoke_result_data = InvokeResultData()

        prize_order = prize_order_model.get_entity_by_id(prize_order_id)
        if not prize_order:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message ="奖品订单信息不存在-1"
            return invoke_result_data
        if SafeHelper.authenticat_app_id(prize_order.app_id, app_id) == False:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message ="奖品订单信息不存在-2"
            return invoke_result_data
        if province != None:
            prize_order.province = province
        if city != None:
            prize_order.city = city
        if county != None:
            prize_order.county = county
        if street != None:
            prize_order.street = street
        if address != None:
            prize_order.address = address
        if real_name != None:
            prize_order.real_name = real_name
        if telephone != None:
            prize_order.telephone = telephone
        prize_order_model.update_table("province=%s,city=%s,county=%s,street=%s,address=%s,real_name=%s,telephone=%s,modify_date=%s", "id=%s", [prize_order.province, prize_order.city, prize_order.county, prize_order.street, prize_order.address, prize_order.real_name, prize_order.telephone, now_datetime, prize_order_id])
        return invoke_result_data

    def import_prize_order(self, app_id, act_id, content_type, content, ref_head_name='小程序订单号', prize_roster_sub_table=None):
        """
        :description: 
        :param app_id：应用标识
        :param act_id：活动标识
        :param content_type：内容类型 1-base64字符串内容 2-json字符串内容
        :param content：字符串内容
        :param ref_head_name：关联表头名称
        :param prize_roster_sub_table：奖品记录分表名称
        :return 
        :last_editors: HuangJianYi
        """
        from seven_cloudapp_frame.libs.customize.excel_helper import ExcelExHelper

        invoke_result_data = InvokeResultData()

        prize_order_model = PrizeOrderModel(context=self.context).set_sub_table(app_id)
        if not prize_roster_sub_table:
            prize_roster_sub_table = self.get_business_sub_table("prize_roster_tb",{"app_id":app_id})
        prize_roster_model = PrizeRosterModel(sub_table=prize_roster_sub_table, context=self.context)
        data = []
        total_num = 0
        if content_type == 1:
            data = base64.decodebytes(str(content).encode())
            if not os.path.exists("temp"):
                os.makedirs("temp")
            path = "temp/" + UUIDHelper.get_uuid() + ".xlsx"
            with open(path, 'ba') as f:
                buf = bytearray(data)
                f.write(buf)
            f.close()
            order_no_index = -1
            express_no_index = -1
            express_company_index = -1

            data = ExcelExHelper.input(path)
            data_total = len(data)
            # 表格头部
            if data_total > 0:
                title_list = data[0]
                if ref_head_name in title_list:
                    order_no_index = title_list.index(ref_head_name)
                if "物流单号" in title_list:
                    express_no_index = title_list.index("物流单号")
                if "物流公司" in title_list:
                    express_company_index = title_list.index("物流公司")

            if order_no_index == -1 or express_no_index == -1 or express_company_index == -1:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message ="缺少必要字段，无法导入订单"
                return invoke_result_data
            # 数据导入
            for i in range(1, data_total):
                row = data[i]
                order_no = row[order_no_index]
                express_no = row[express_no_index]
                express_company = row[express_company_index]
                if order_no and express_no and express_company:
                    now_datetime = SevenHelper.get_now_datetime()
                    order_no = str(order_no).strip()
                    express_no = str(express_no).strip()
                    express_company = str(express_company).strip()
                    update_sql = "order_status=1,express_company=%s,express_no=%s,deliver_date=%s"
                    params = [express_company, express_no, now_datetime, order_no]
                    result = prize_order_model.update_table(update_sql, "order_no=%s", params)
                    if result == True:
                        prize_roster_model.update_table("logistics_status=1", "order_no=%s", [order_no])
                        total_num += 1
            os.remove(path)
        else:
            data = SevenHelper.json_loads(content)
            for row in data:
                order_no = row[ref_head_name]
                express_no = row['物流单号']
                express_company = row['物流公司']
                if order_no and express_no and express_company:
                    now_datetime = SevenHelper.get_now_datetime()
                    order_no = str(order_no).strip()
                    express_no = str(express_no).strip()
                    express_company = str(express_company).strip()
                    update_sql = "order_status=1,express_company=%s,express_no=%s,deliver_date=%s"
                    params = [express_company, express_no, now_datetime, order_no]
                    result = prize_order_model.update_table(update_sql, "order_no=%s", params)
                    if result == True:
                        prize_roster_model.update_table("logistics_status=1", "order_no=%s", [order_no])
                        total_num += 1
                else:
                    continue
        invoke_result_data.data = {"total_num": total_num}
        return invoke_result_data

    def select_prize_order(self,app_id,act_id,user_id,login_token,prize_ids,real_name,telephone,province,city,county,street,address):
        """
        :description: 选择奖品进行下单
        :param app_id：应用标识
        :param act_id：活动标识
        :param user_id：用户标识
        :param login_token:用户访问令牌
        :param prize_ids:用户奖品id串，逗号分隔（为空则将所有未下单的奖品进行下单）
        :param real_name:用户名
        :param telephone:电话
        :param province:省
        :param city:市
        :param county:区县
        :param street:街道
        :param address:地址
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        db_transaction = DbTransaction(db_config_dict=config.get_value(self.db_connect_key), context=self.context)
        prize_roster_model = PrizeRosterModel(db_transaction=db_transaction, context=self.context).set_sub_table(app_id)
        prize_order_model = PrizeOrderModel(db_transaction=db_transaction, context=self.context).set_sub_table(app_id)
        prize_ids_list = []
        if prize_ids:
            prize_ids_list = prize_ids.split(',')
            for prize_id in prize_ids_list:
                try:
                    prize_id = int(prize_id)
                except Exception as ex:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message ="存在无法识别的奖品标识"
                    return invoke_result_data
            prize_ids_list = list(set(prize_ids_list))

        #获取用户信息
        if act_id > 0 :
            user_info_model = UserInfoModel(context=self.context).set_sub_table(app_id)
            user_info_dict = user_info_model.get_dict("act_id=%s and user_id=%s", limit="1", params=[act_id, user_id])
            if not user_info_dict:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "用户不存在"
                return invoke_result_data
            if user_info_dict["login_token"] != login_token:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "已在另一台设备登录,无法操作"
                return invoke_result_data
            if int(user_info_dict["user_state"]) == 1:
                invoke_result_data.success = False
                invoke_result_data.error_code = "user_exception"
                invoke_result_data.error_message = "账号异常,请联系客服处理"
                return invoke_result_data

        acquire_lock_name = f"create_prize_order_queue_{act_id}_{user_id}" if act_id > 0 else f"create_prize_order_queue_{app_id}_0_{user_id}"
        acquire_lock_status, identifier = SevenHelper.redis_acquire_lock(acquire_lock_name)
        if acquire_lock_status == False:
            invoke_result_data.success = False
            invoke_result_data.error_code = "acquire_lock"
            invoke_result_data.error_message = "请求超时,请稍后再试"
            SevenHelper.redis_release_lock(acquire_lock_name, identifier)
            return invoke_result_data
        #用户奖品列表
        condition_where = ConditionWhere()
        params = []
        if app_id:
            condition_where.add_condition("app_id=%s")
            params.append(app_id)
        condition_where.add_condition("act_id=%s and user_id=%s and prize_status=0")
        params.append(act_id)
        if len(prize_ids_list) > 0:
            condition_where.add_condition(f"id in ({prize_ids})")

        prize_roster_list = prize_roster_model.get_list(condition_where.to_string(),params=params)
        if len(prize_roster_list) == 0:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "对不起,所选下单奖品不存在"
            SevenHelper.redis_release_lock(acquire_lock_name, identifier)
            return invoke_result_data
        if prize_ids:
            if len(prize_roster_list) != len(prize_ids_list):
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "对不起,所选下单奖品不存在"
                SevenHelper.redis_release_lock(acquire_lock_name, identifier)
                return invoke_result_data
        elif len(prize_roster_list) == 0:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "对不起,所选下单奖品不存在"
            SevenHelper.redis_release_lock(acquire_lock_name, identifier)
            return invoke_result_data

        now_date = SevenHelper.get_now_datetime()
        prize_order = PrizeOrder()
        prize_order.app_id = app_id
        prize_order.user_id = user_id
        prize_order.user_nick = user_info_dict["user_nick"]
        prize_order.open_id = user_info_dict["open_id"]
        prize_order.act_id = act_id
        prize_order.real_name = real_name
        prize_order.telephone = telephone
        prize_order.province = province
        prize_order.city = city
        prize_order.county = county
        prize_order.street = street
        prize_order.address = address
        prize_order.order_status = 0
        prize_order.create_date = now_date
        prize_order.modify_date = now_date
        prize_order.order_no = SevenHelper.create_order_id()

        for prize_roster in prize_roster_list:
            prize_roster.order_no = prize_order.order_no
            prize_roster.prize_status = 1
        try:
            db_transaction.begin_transaction()
            prize_order_model.add_entity(prize_order)
            prize_roster_model.update_list(prize_roster_list, "order_no,prize_status")
            result,message = db_transaction.commit_transaction(True)
            if result == False:
                raise Exception("执行事务失败",message)
            prize_roster_model.delete_dependency_key([DependencyKey.prize_roster_list(act_id, user_id, app_id),DependencyKey.prize_order_list(act_id, user_id, app_id)])
        except Exception as ex:
            if self.context:
                self.context.logging_link_error("create_prize_order:" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("create_prize_order:" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "对不起,下单失败"
            SevenHelper.redis_release_lock(acquire_lock_name, identifier)
            return invoke_result_data

        SevenHelper.redis_release_lock(acquire_lock_name, identifier)
        self._delete_prize_order_dependency_key(act_id,user_id)
        self._delete_prize_roster_dependency_key(act_id=act_id, user_id=user_id, app_id=app_id)
        invoke_result_data.data = prize_order.__dict__
        return invoke_result_data

    def get_tao_pay_order_list(self,app_id,act_id,user_id,open_id,nick_name,pay_date_start,pay_date_end,page_size=20,page_index=0,field="*",order_by="pay_date desc",condition="",params=[], is_auto=False):
        """
        :description: 淘宝用户购买订单列表
        :param app_id：应用标识
        :param act_id：活动标识
        :param user_id：用户唯一标识
        :param open_id：open_id
        :param nick_name：用户昵称
        :param pay_date_start：订单支付时间开始
        :param pay_date_end：订单支付时间结束
        :param page_size：页大小
        :param page_index：页索引
        :param field：查询字段
        :param order_by：排序
        :param condition：条件
        :param params：参数化数组
        :param is_auto: True-走从库 False-走主库 
        :return: PageInfo
        :last_editors: HuangJianYi
        """
        where = "app_id=%s and act_id=%s"
        params_list = [app_id,act_id]
        if condition:
            where += " AND " + condition
            params_list.extend(params)
        page_info = PageInfo(page_index, page_size, 0, [])

        if not act_id:
            return page_info
        if user_id:
            where += " AND user_id=%s"
            params_list.append(user_id)
        if open_id:
            where += " AND open_id=%s"
            params_list.append(open_id)
        if nick_name:
            where += " AND user_nick=%s"
            params_list.append(nick_name)
        if pay_date_start:
            where += " AND pay_date>=%s"
            params_list.append(pay_date_start)
        if pay_date_end:
            where += " AND pay_date<=%s"
            params_list.append(pay_date_end)
        page_list, total = TaoPayOrderModel(context=self.context, is_auto=is_auto).set_sub_table(app_id).get_dict_page_list(field, page_index, page_size, where, "", order_by, params_list)
        page_info = PageInfo(page_index, page_size, total, page_list)
        return page_info

    def _get_tao_pay_order_no_list(self, app_id, user_id):
        """
        :description: 获取已获取奖励的订单子编号列表
        :param app_id:应用标识
        :param user_id:用户标识
        :return: 
        :last_editors: HuangJianYi
        """
        redis_init = SevenHelper.redis_init(config_dict=self.redis_config_dict)
        pay_order_cache_key = f"sub_pay_order_no_list:appid_{app_id}_userid_{user_id}"
        pay_order_no_list = redis_init.lrange(pay_order_cache_key,0,-1)
        pay_order_list = []
        is_add = False
        if not pay_order_no_list or len(pay_order_no_list)<=0:
            tao_pay_order_model = TaoPayOrderModel(context=self.context).set_sub_table(app_id)
            pay_order_list = tao_pay_order_model.get_dict_list("app_id=%s and user_id=%s",field="sub_pay_order_no", params=[app_id,user_id])
            is_add = True

        if len(pay_order_list) >0:
            for item in pay_order_list:
                pay_order_no_list.append(item["sub_pay_order_no"])
                if is_add == True:
                    redis_init.lpush(pay_order_cache_key,item["sub_pay_order_no"])
                    redis_init.expire(pay_order_cache_key, 30 * 24 * 3600)
        return pay_order_no_list,redis_init,pay_order_cache_key

    def sync_tao_pay_order(self,app_id,act_id,module_id,user_id,login_token,handler_name,request_code,asset_type=3,goods_id="",sku_id="",ascription_type=1,app_key="",app_secret="",is_log=False,check_user_nick=True,continue_request_expire=1,support_presale_order=False,default_order_status=None, access_token=None):
        """
        :description: 同步淘宝支付订单给用户加资产
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param login_token:访问令牌
        :param handler_name:接口名称
        :param request_code:请求代码
        :param asset_type:资产类型(1-次数2-积分3-价格档位)
        :param goods_id:商品ID（资产类型为3-价格档位 无需填写）
        :param sku_id:sku_id (资产类型为3-价格档位 无需填写)
        :param ascription_type:归属类型（0-抽奖次数订单1-邮费次数订单2-任务订单）
        :param app_key:app_key
        :param app_secret:app_secret
        :param is_log:是否记录top请求日志
        :param check_user_nick:是否校验昵称为空
        :param continue_request_expire:连续请求过期时间，为0不进行校验，单位秒
        :param support_presale_order:是否支持预售订单
        :param default_order_status:默认订单状态，有传则用默认值，不然取淘宝获取的订单状态
        :param access_token:淘宝access_token
        :return 
        :last_editors: HuangJianYi
        """
        acquire_lock_name = f"sync_tao_pay_order:{act_id}_{module_id}_{user_id}"
        identifier = ""
        try:
            invoke_result_data = self.business_process_executing(app_id,act_id,module_id,user_id,login_token,handler_name,False,check_user_nick,continue_request_expire,acquire_lock_name)
            if invoke_result_data.success == True:
                act_info_dict = invoke_result_data.data["act_info_dict"]
                act_module_dict = invoke_result_data.data["act_module_dict"]
                user_info_dict = invoke_result_data.data["user_info_dict"]
                identifier = invoke_result_data.data["identifier"]

                if not access_token:
                    app_info_dict = AppBaseModel(context=self.context).get_app_info_dict(app_id, field='access_token')
                    access_token = app_info_dict["access_token"] if app_info_dict else ""
                top_base_model = TopBaseModel(context=self.context)
                order_data = []
                if act_info_dict['start_date'] != "":
                    invoke_result_data = top_base_model.get_buy_order_list(user_info_dict["open_id"], access_token,app_key,app_secret, act_info_dict['start_date'],is_log=is_log)
                    if invoke_result_data.success == True:
                        order_data = invoke_result_data.data
                else:
                    invoke_result_data = top_base_model.get_buy_order_list(user_info_dict["open_id"], access_token,app_key,app_secret,is_log=is_log)
                    if invoke_result_data.success == True:
                        order_data = invoke_result_data.data
                if len(order_data)>0:
                    pay_order_no_list,redis_init,pay_order_cache_key = self._get_tao_pay_order_no_list(app_id,user_id)

                    goods_ids_list = []
                    #满足奖励条件的订单
                    reward_order_list = []
                    #所有相关商品订单
                    all_order_list = []
                    if asset_type == 3:
                        price_base_model = PriceBaseModel(context=self.context)
                        price_gear_dict_list = price_base_model.get_price_gear_list(app_id,act_id,100,0,page_count_mode='none')
                        for price_gear_dict in price_gear_dict_list:
                            goods_ids_list.append(price_gear_dict["goods_id"])
                    else:
                        goods_ids_list.append(str(goods_id))

                    for item in order_data:
                        for order in item["orders"]["order"]:
                            if str(order["num_iid"]) in goods_ids_list:
                                order["step_paid_fee"] = item["step_paid_fee"] if "step_paid_fee" in item.keys() else 0
                                order["type"] = item["type"]
                                if "pay_time" in item:
                                    order["tid"] = item["tid"]
                                    order["pay_time"] = item["pay_time"]
                                if support_presale_order == True:
                                    if order["status"] in self.rewards_status() or (order["type"] == "step" and order["step_trade_status"] != "FRONT_NOPAID_FINAL_NOPAID"):
                                        reward_order_list.append(order)
                                else:
                                    if order["status"] in self.rewards_status():
                                        reward_order_list.append(order)

                                all_order_list.append(order)

                    pay_price = 0
                    pay_num = 0
                    buy_num = 0
                    tao_pay_order_list = []
                    for order in reward_order_list:
                        try:
                            #判断是否已经加过奖励
                            if order["oid"] not in pay_order_no_list:
                                asset_object_name = ""
                                asset_object_id = ""
                                if asset_type == 3:
                                    now_price_gear_dict = None
                                    for price_gear_dict in price_gear_dict_list:
                                        if (price_gear_dict["effective_date"] == '1900-01-01 00:00:00' or TimeHelper.format_time_to_datetime(price_gear_dict["effective_date"]) < TimeHelper.format_time_to_datetime(order["pay_time"])) and price_gear_dict["goods_id"] == str(order["num_iid"]):
                                            #关联类型：1商品skuid关联2商品id关联
                                            if price_gear_dict["relation_type"] == 1 and price_gear_dict["sku_id"] != str(order["sku_id"]):
                                                continue
                                            now_price_gear_dict = price_gear_dict
                                    if not now_price_gear_dict:
                                        continue
                                    asset_object_id = now_price_gear_dict["id"]
                                    asset_object_name = now_price_gear_dict["price_gear_name"]
                                else:
                                    if str(goods_id) != str(order["num_iid"]):
                                        continue
                                    if sku_id and str(sku_id) != str(order["sku_id"]):
                                        continue

                                tao_pay_order = TaoPayOrder()
                                tao_pay_order.app_id = app_id
                                tao_pay_order.act_id = act_id
                                tao_pay_order.ascription_type = ascription_type
                                tao_pay_order.user_id = user_id
                                tao_pay_order.open_id = user_info_dict["open_id"]
                                tao_pay_order.user_nick = user_info_dict["user_nick"]
                                tao_pay_order.main_pay_order_no = order['tid']
                                tao_pay_order.sub_pay_order_no = order['oid']
                                tao_pay_order.goods_code = order['num_iid']
                                tao_pay_order.goods_name = order['title']
                                tao_pay_order.s1 = order.get("outer_iid","")

                                buy_order_payment = 0
                                if "sku_id" in order.keys():
                                    tao_pay_order.sku_id = order['sku_id']
                                    sku_invoke_result_data = top_base_model.get_sku_name(int(order['num_iid']), int(order['sku_id']), access_token,app_key, app_secret,is_log)
                                    tao_pay_order.sku_name = sku_invoke_result_data.data if sku_invoke_result_data.success == True else ""
                                tao_pay_order.buy_num = order['num']
                                if "payment" not in order.keys():
                                    buy_order_invoke_result_data = top_base_model.get_buy_order_info(order['tid'], access_token, app_key, app_secret, is_log)
                                    if buy_order_invoke_result_data.success == False:
                                        continue
                                    buy_order_payment = decimal.Decimal(buy_order_invoke_result_data.data["payment"])
                                else:
                                    buy_order_payment = decimal.Decimal(order['payment'])
                                tao_pay_order.pay_price = buy_order_payment
                                tao_pay_order.order_status = order['status'] if not default_order_status else default_order_status
                                tao_pay_order.create_date = SevenHelper.get_now_datetime()
                                tao_pay_order.asset_type = asset_type
                                tao_pay_order.asset_object_id = asset_object_id
                                tao_pay_order.asset_object_name = asset_object_name
                                tao_pay_order.surplus_count = order['num']
                                tao_pay_order.pay_date = order['pay_time']
                                tao_pay_order_list.append(tao_pay_order)
                                if support_presale_order == True:
                                    buy_order_payment = decimal.Decimal(order["step_paid_fee"]) if order["type"] == "step" and decimal.Decimal(order["step_paid_fee"]) > 0 else buy_order_payment
                                pay_price = decimal.Decimal(pay_price) + buy_order_payment
                                pay_num = pay_num + 1
                                buy_num = buy_num + order['num']
                        except Exception as ex:
                            if self.context:
                                self.context.logging_link_info(str(order) + "【同步淘宝支付订单】" + traceback.format_exc())
                            elif self.logging_link_info:
                                self.logging_link_info(str(order) + "【同步淘宝支付订单】" + traceback.format_exc())
                            continue
                    if len(tao_pay_order_list) > 0:
                        result = TaoPayOrderModel(context=self.context).set_sub_table(app_id).add_list(tao_pay_order_list)
                        if result == True and buy_num > 0:
                            asset_base_model = AssetBaseModel(context=self.context)
                            invoke_result_data.data = {}
                            invoke_result_data.data["asset_list"] = []
                            for item in tao_pay_order_list:
                                only_id = str(item.sub_pay_order_no)
                                asset_invoke_result_data = asset_base_model.update_user_asset(app_id,act_id,module_id,user_id,user_info_dict["open_id"],user_info_dict["user_nick"],asset_type,item.buy_num,item.asset_object_id,1,"","","购买",only_id,handler_name,request_code,info_json={})
                                if asset_invoke_result_data.success == False:
                                    invoke_result_data.success = False
                                    invoke_result_data.error_code = "error"
                                    invoke_result_data.error_message = "变更资产失败"
                                else:
                                    redis_init.lpush(pay_order_cache_key,item.sub_pay_order_no)
                                    redis_init.expire(pay_order_cache_key, 30 * 24 * 3600)
                                    data = {}
                                    data["asset_type"] = asset_type
                                    data["asset_object_id"] = item.asset_object_id
                                    data["buy_num"] = item.buy_num
                                    invoke_result_data.data["asset_list"].append(data)
                            invoke_result_data.data["buy_num"] = buy_num
                            invoke_result_data.data["pay_price"] = pay_price
                            invoke_result_data.data["pay_num"] = pay_num
                        else:
                            invoke_result_data.success = False
                            invoke_result_data.error_code = "error"
                            invoke_result_data.error_message = "没有匹配订单"
                    else:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = "没有匹配订单"
                    if len(all_order_list) >0:
                        user_base_model = UserBaseModel(context=self.context)
                        black_status = user_base_model.check_pull_black(user_info_dict,act_info_dict["is_black"],act_info_dict["refund_count"],all_order_list, 1)
                        if black_status == True:
                            invoke_result_data.data = {} if not invoke_result_data.data or isinstance(invoke_result_data.data, list) else invoke_result_data.data
                            invoke_result_data.data["user_state"] = 1
                else:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "没有订单"
        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【同步淘宝支付订单】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【同步淘宝支付订单】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"
        finally:
            self.business_process_executed(act_id,module_id,user_id,handler_name,acquire_lock_name,identifier)

        return invoke_result_data

    def get_prize_roster_list(self,app_id,act_id,module_id,user_id,open_id="",user_nick="",order_no="",goods_type=-1,prize_type=-1,logistics_status=-1,prize_status=-1,pay_status=-1,page_size=20,page_index=0,create_date_start="",create_date_end="",order_by="id desc",field="*",condition="",params=[],is_cache=True, page_count_mode="total", is_auto=False):
        """
        :description: 用户中奖记录列表
        :description: 如果有进行数据缓存，创建中奖记录时需清掉依赖建
        :param app_id：应用标识
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param user_id：用户标识
        :param open_id：open_id
        :param user_nick：用户昵称
        :param order_no：订单号
        :param goods_type：物品类型（1虚拟2实物）
        :param prize_type：奖品类型(1现货2优惠券3红包4参与奖5预售)
        :param logistics_status：物流状态（0未发货1已发货2不予发货）
        :param prize_status：奖品状态（0未下单（未领取）1已下单（已领取）2已回购10已隐藏（删除）11无需发货）
        :param pay_status：支付状态(0未支付1已支付2已退款3处理中)
        :param page_size：页大小
        :param page_index：页索引
        :param create_date_start：开始时间
        :param create_date_end：结束时间
        :param order_by：排序
        :param field：查询字段
        :param condition：条件
        :param params：参数化数组
        :param is_cache：是否缓存
        :param page_count_mode: 分页计数模式 total-计算总数(默认) next-计算是否有下一页(bool) none-不计算
        :param is_auto: True-走从库 False-走主库 
        :return:
        :last_editors: HuangJianYi
        """
        condition_where = ConditionWhere()
        params_list = []
        if app_id:
            condition_where.add_condition("app_id=%s")
            params_list.append(app_id)
        if act_id >= 0:
            condition_where.add_condition("act_id=%s")
            params_list.append(act_id)
        if module_id:
            condition_where.add_condition("module_id=%s")
            params_list.append(module_id)
        if user_id:
            condition_where.add_condition("user_id=%s")
            params_list.append(user_id)
        if open_id:
            condition_where.add_condition("open_id=%s")
            params_list.append(open_id)
        if user_nick:
            condition_where.add_condition("user_nick=%s")
            params_list.append(user_nick)
        if order_no:
            condition_where.add_condition("order_no=%s")
            params_list.append(order_no)
        if goods_type !=-1:
            condition_where.add_condition("goods_type=%s")
            params_list.append(goods_type)
        if prize_type !=-1:
            condition_where.add_condition("prize_type=%s")
            params_list.append(prize_type)
        if logistics_status !=-1:
            condition_where.add_condition("logistics_status=%s")
            params_list.append(logistics_status)
        if prize_status !=-1:
            condition_where.add_condition("prize_status=%s")
            params_list.append(prize_status)
        if pay_status !=-1:
            condition_where.add_condition("pay_status=%s")
            params_list.append(pay_status)
        if create_date_start:
            condition_where.add_condition("create_date>=%s")
            params_list.append(create_date_start)
        if create_date_end:
            condition_where.add_condition("create_date<=%s")
            params_list.append(create_date_end)
        if condition:
            condition_where.add_condition(condition)
            params_list.extend(params)

        prize_roster_model = PrizeRosterModel(context=self.context, is_auto=is_auto).set_sub_table(app_id)
        if is_cache:
            page_list = prize_roster_model.get_cache_dict_page_list(field, page_index, page_size, condition_where.to_string(), "", order_by, params_list, dependency_key=DependencyKey.prize_roster_list(act_id,user_id,app_id), page_count_mode=page_count_mode)
        else:
            page_list = prize_roster_model.get_dict_page_list(field, page_index, page_size, condition_where.to_string(), "", order_by, params_list, page_count_mode)
        return page_list

    def get_horseracelamp_list(self, app_id, act_id, module_id, is_search_module=False, condition="", params=[], page_size=30):
        """
        :description: 获取跑马灯奖品列表
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param is_search_module:是否查询活动模块
        :param condition：条件
        :param params：参数数组
        :param page_size：页大小
        :return list
        :last_editors: HuangJianYi
        """
        condition_where = ConditionWhere()
        params_list = []
        if app_id:
            condition_where.add_condition("app_id=%s")
            params_list.append(app_id)
        if act_id >= 0:
            condition_where.add_condition("act_id=%s")
            params_list.append(act_id)
        if is_search_module == True and module_id:
            condition_where.add_condition("module_id=%s")
            params_list.append(module_id)
        if condition:
            condition_where.add_condition(condition)
            params_list.extend(params)
        act_prize_list_dict = ActPrizeModel(context=self.context, is_auto=True).get_cache_dict_list("act_id=%s and is_prize_notice=1 and is_del=0", field='id', params=[act_id], cache_expire=60)
        if act_prize_list_dict:
            if len(act_prize_list_dict) > 100:
                act_prize_list_dict = random.sample(act_prize_list_dict,50)

            prize_id_list = [str(i["id"]) for i in act_prize_list_dict]
            if len(prize_id_list) > 0:
                prize_ids = ",".join(prize_id_list)
                condition_where.add_condition("prize_id in (" + prize_ids + ")")
        prize_roster_model = PrizeRosterModel(context=self.context, is_auto=True).set_sub_table(app_id)
        prize_roster_list = prize_roster_model.get_cache_dict_list(condition_where.to_string(), "", "id desc", str(page_size), "user_id,user_nick,prize_name,tag_id,tag_name,module_name", params_list, cache_expire=60)
        total = int(len(prize_roster_list))
        if total == 0:
            prize_roster_list = []
        else:
            user_ids = SevenHelper.get_row_by_dict_list(prize_roster_list, "user_id")
            user_info_list_dict = UserInfoModel(context=self.context).set_sub_table(app_id).get_dict_list("act_id=%s and " + SevenHelper.get_condition_by_int_list("user_id", user_ids), field="user_id,avatar", params=[act_id])
            for i in range(len(prize_roster_list)):
                user_info_dict = query(user_info_list_dict).first_or_default(lambda x: int(x["user_id"]) == int(prize_roster_list[i]["user_id"]))
                prize_roster_list[i]["avatar"] = user_info_dict["avatar"] if user_info_dict else ""
                if prize_roster_list[i]["user_nick"]:
                    length = len(prize_roster_list[i]["user_nick"])
                    if length > 2:
                        user_nick = prize_roster_list[i]["user_nick"][0:length - 2] + "**"
                    else:
                        user_nick = prize_roster_list[i]["user_nick"][0:1] + "*"
                    prize_roster_list[i]["user_nick"] = user_nick
        act_module_list = []
        if total < page_size:
            add_num = page_size - total
            act_prize_model = ActPrizeModel(context=self.context, is_auto=True)
            prize_condition = "act_id=%s and is_prize_notice=1"
            prize_params = [act_id]

            if is_search_module == True:
                module_condition = "act_id=%s and is_fictitious=1"
                module_params = [act_id]
                if module_id >0:
                    module_condition += " and id=%s"
                    module_params = [act_id, module_id]
                act_module_list = ActModuleModel(context=self.context, is_auto=True).get_cache_list(module_condition, field="id,module_name", params=module_params,cache_expire=60)
                if len(act_module_list) > 0:
                    module_id_list = [str(i.id) for i in act_module_list]
                    module_ids = ",".join(module_id_list)
                    prize_condition += " and module_id in (" + module_ids + ")"
            false_act_prize_list = act_prize_model.get_cache_list(prize_condition, order_by="probability desc,chance desc", limit="30", field="prize_name,tag_id,tag_name,module_id", params=prize_params,cache_expire=60)
            if len(false_act_prize_list) > 0 and add_num > 0:
                now_datetime = TimeHelper.add_hours_by_format_time(hour=-random.randint(0, 1000))
                user_info_list_dict = UserInfoModel(context=self.context, is_auto=True).set_sub_table(false_act_prize_list[0].app_id).get_dict_list("act_id<%s and create_date>%s", field="user_nick,avatar", params=[act_id,now_datetime], limit=str(add_num))

                for i in range(len(user_info_list_dict)):
                    false_act_prize = false_act_prize_list[random.randint(0, len(false_act_prize_list)-1)]
                    if not false_act_prize:
                        continue
                    prize_roster = {}
                    user_nick = ""
                    if user_info_list_dict[i]["user_nick"]:
                        length = len(user_info_list_dict[i]["user_nick"])
                        if length > 2:
                            user_nick = user_info_list_dict[i]["user_nick"][0:length - 2] + "**"
                        else:
                            user_nick = user_info_list_dict[i]["user_nick"][0:1] + "*"
                    prize_roster["user_nick"] = user_nick
                    prize_roster["avatar"] = user_info_list_dict[i]["avatar"]
                    prize_roster["prize_name"] = false_act_prize.prize_name
                    prize_roster["tag_id"] = false_act_prize.tag_id
                    prize_roster["tag_name"] = false_act_prize.tag_name
                    act_module_filter = [act_module for act_module in act_module_list if false_act_prize.module_id == act_module.id]
                    prize_roster["module_name"] = act_module_filter[0].module_name if len(act_module_filter) > 0 else ""
                    prize_roster_list.append(prize_roster)

        return prize_roster_list

    def get_coupon_prize(self, app_id, act_id, user_id, user_prize_id, app_key, app_secret, is_log=False, access_token=None):
        """
        :description: 领取淘宝优惠券
        :param app_id：应用标识
        :param act_id：活动标识
        :param user_id：用户标识
        :param user_prize_id:用户奖品标识
        :param app_key:app_key
        :param app_secret:app_secret
        :param is_log:是否记录日志
        :param access_token:淘宝access_token
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        app_base_model = AppBaseModel(context=self.context)
        app_info_dict = app_base_model.get_app_info_dict(app_id)
        if not app_info_dict:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message ="小程序不存在"
            return invoke_result_data
        if not access_token:
            access_token = app_info_dict["access_token"]
        if access_token == "":
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message ="未授权请联系客服授权"
            return invoke_result_data
        prize_roster_model = PrizeRosterModel(context=self.context).set_sub_table(app_id)
        prize_roster_dict = prize_roster_model.get_cache_dict_by_id(user_prize_id, dependency_key=DependencyKey.prize_roster_list(act_id,user_id,app_id))
        if not prize_roster_dict or prize_roster_dict['user_id'] != user_id:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message ="奖品不存在"
            return invoke_result_data
        tao_coupon_model = TaoCouponModel(context=self.context)
        tao_coupon_dict = tao_coupon_model.get_dict(where="prize_id=%s", limit="1", params=[prize_roster_dict["prize_id"]])
        if not tao_coupon_dict or tao_coupon_dict['right_ename'] == "":
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message ="奖品不是优惠券,无需领取"
            return invoke_result_data
        top_base_model = TopBaseModel(context=self.context)
        top_invoke_result_data = top_base_model.alibaba_benefit_send(tao_coupon_dict['right_ename'], prize_roster_dict["open_id"], access_token, app_key, app_secret, is_log)
        if top_invoke_result_data.success == False:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message ="领取失败"
            return invoke_result_data
        resp = top_invoke_result_data.data
        if resp["alibaba_benefit_send_response"]:
            if resp["alibaba_benefit_send_response"]["result_success"] == True:
                prize_roster_model.update_table("prize_status=1", "id=%s", params=[user_prize_id])
                prize_roster_model.delete_dependency_key(DependencyKey.prize_roster_list(act_id, user_id, app_id))
                result = {}
                result["prize_name"] = resp["alibaba_benefit_send_response"]["prize_name"]
                invoke_result_data.data = result
                return invoke_result_data
            if resp["alibaba_benefit_send_response"]["result_code"] == "COUPON_INVALID_OR_DELETED":
                prize_roster_model.update_table("prize_status=10", "id=%s", params=[user_prize_id])
                prize_roster_model.delete_dependency_key(DependencyKey.prize_roster_list(act_id, user_id, app_id))
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message ="领取失败：优惠券无效或已删除"
                return invoke_result_data
            if resp["alibaba_benefit_send_response"]["result_code"] == "COUPON_NOT_EXISTS":
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message ="领取失败：优惠券不存在"
                return invoke_result_data
            if resp["alibaba_benefit_send_response"]["result_code"] == "APPLY_SINGLE_COUPON_COUNT_EXCEED_LIMIT":
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message ="领取失败：优惠券超过限额"
                return invoke_result_data
            if resp["alibaba_benefit_send_response"]["result_code"] == "USER_PERMISSION_EXCEED_MAX_RIGHT_COUNT_IN_DAY":
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message ="领取失败：同一张优惠券每天限领取一次"
                return invoke_result_data
            if resp["alibaba_benefit_send_response"]["result_code"] == "APPLY_ONE_SELLER_COUNT_EXCEED_LIMIT":
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message ="领取失败：用户优惠券超出10张限制"
                return invoke_result_data
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message ="领取失败"
            invoke_result_data.data = resp["alibaba_benefit_send_response"]["result_code"]
            return invoke_result_data

        else:
            result = resp["sub_msg"] if resp["sub_msg"] else ""
            if result == "" and resp["result_msg"]:
                result = resp["result_msg"]
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = f"领取失败:{result}"
            return invoke_result_data

    def create_wechat_refund(self, source_type, app_id, act_id, pay_order_no, refund_amount = 0, refund_reason = ""):
        """
        :description: 创建微信退款
        :param source_type：来源类型（1用户申请退款2人工审核退款3自动退款）
        :param app_id：应用标识
        :param act_id：活动标识
        :param pay_order_no：支付单号
        :param refund_reason：退款原因
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        pay_order_model = PayOrderModel(context=self.context)
        refund_order_model = RefundOrderModel(context=self.context)
        #请求太频繁限制
        if SevenHelper.is_continue_request(f"create_wechat_refund:{app_id}_{pay_order_no}", 1000) == False:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message ="请求太频繁,请稍后再试"
            return invoke_result_data

        pay_order = pay_order_model.get_entity("pay_order_no=%s", params=pay_order_no)
        if not pay_order:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message ="对不起，找不到支付订单"
            return invoke_result_data

        refund_order = refund_order_model.get_entity(where="pay_order_no=%s AND refund_status in (1,2)", params=[pay_order_no])
        if refund_order:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message ="对不起，退款处理中"
            return invoke_result_data
        if refund_amount <= 0:
            refund_amount = pay_order.pay_amount
        if pay_order.refund_amount + refund_amount > pay_order.pay_amount:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message ="退款总金额不能超过支付金额"
            return invoke_result_data

        refund_status = 0
        if source_type == 1:
            refund_reason = refund_reason
            refund_status = 1
        elif source_type == 2:
            refund_reason = "人工审核退款"
        elif source_type == 3:
            refund_reason = "自动退款"


        refund_no = SevenHelper.create_order_id()
        #创建退款预订单
        refund_order = RefundOrder()
        refund_order.app_id = app_id
        refund_order.act_id = act_id
        refund_order.user_id = pay_order.user_id
        refund_order.open_id = pay_order.open_id
        refund_order.pay_order_no = pay_order_no
        refund_order.refund_no = refund_no
        refund_order.out_order_no = pay_order.out_order_no
        refund_order.refund_amount = refund_amount
        refund_order.refund_status = refund_status
        refund_order.refund_reason = refund_reason
        refund_order.create_date = SevenHelper.get_now_datetime()
        refund_order.id = refund_order_model.add_entity(refund_order)
        if refund_order.id <= 0:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message ="对不起，创建退款订单失败"
            return invoke_result_data

        if source_type != 1:
            wechat_pay = share_config.get_value("wechat_pay")
            #退款异步通知地址
            notify_url = wechat_pay["notify_url"]
            result_data = WeChatPayRequest().create_refund(refund_no, pay_order.pay_order_no, notify_url, refund_amount, pay_order.pay_amount)
            if result_data.success == False:
                refund_order_model.del_entity("id=%s", params=refund_order.id)
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message ="对不起，创建退款订单异常"
                return invoke_result_data
            refund_order_model.update_table("refund_status=2", "id=%s", params=refund_order.id)
            invoke_result_data.data = refund_no

        return invoke_result_data

    def sync_shake_shop_pay_order(self, app_id, act_id, module_id, user_id, login_token, handler_name, request_code, is_log=False, asset_type=3, while_count=1, ascription_type=0, reward_order_status_list = [105, 2, 101, 3, 5]):
        """
        :description: 同步支付订单给用户加资产
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param login_token:访问令牌
        :param handler_name:接口名称
        :param request_code:请求代码
        :param is_log:是否记录日志
        :param asset_type:资产类型
        :param while_count:循环请求次数
        :param ascription_type:归属类型（0-抽奖次数订单1-邮费次数订单2-任务订单）
        :param reward_order_status_list:订单状态;1 待确认/待支付-订单创建完毕;105-已支付; 2-备货中； 101-部分发货; 3-已发货（全部发货）;4- 已取消;5 已完成（已收货）;
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        frane_base_model = FrameBaseModel(context=self.context)
        try:
            invoke_result_data = frane_base_model.business_process_executing(app_id,act_id,module_id,user_id,login_token,handler_name,False,False,1,f"sync_shake_shop_pay_order:{act_id}_{module_id}_{user_id}")
            if invoke_result_data.success == True:
                act_info_dict = invoke_result_data.data["act_info_dict"]
                user_info_dict = invoke_result_data.data["user_info_dict"]

                # 获取订单
                shake_shop_config = share_config.get_value('shake_shop',{})
                shake_shop_base_model = ShakeShopBaseModel(context=self.context, app_key=shake_shop_config["app_key"], app_secret=shake_shop_config["app_secret"], shop_id=shake_shop_config["shop_id"])
                # order_data = [{'create_time': 1711010884, 'order_id': '6928080569235084985', 'order_status': 2, 'pay_amount': 590, 'sku_order_list': [{'sku_info': {'product_id': 111111111, 'product_name': '【福利品】彩棠海棠花双头刷收纳架工具化妆刷收纳架防水女美妆工具', 'sku_id': 3254535}}]}]
                order_data = []
                if act_info_dict['start_date'] != "":
                    shake_shop_invoke_result_data = shake_shop_base_model.get_user_order_list(user_info_dict["open_id"], 100, 0, TimeHelper.format_time_to_timestamp(act_info_dict['start_date']), while_count=while_count, is_log=is_log)
                    if shake_shop_invoke_result_data.success == True:
                        order_data = shake_shop_invoke_result_data.data
                else:
                    shake_shop_invoke_result_data = shake_shop_base_model.get_user_order_list(user_info_dict["open_id"], 100, 0, while_count=while_count, is_log=is_log)
                    if shake_shop_invoke_result_data.success == True:
                        order_data = shake_shop_invoke_result_data.data

                if len(order_data) > 0:
                    redis_init = SevenHelper.redis_init()
                    pay_order_no_list, pay_order_cache_key = self._get_shake_shop_pay_order_no_list(app_id, user_id, redis_init)

                    goods_ids_list = []
                    #满足奖励条件的订单
                    reward_order_list = []
                    #所有相关商品订单
                    all_order_list = []
                    price_base_model = PriceBaseModel(context=self.context)
                    price_gear_dict_list = price_base_model.get_price_gear_list(app_id, act_id, 100, 0, page_count_mode='none')
                    for price_gear_dict in price_gear_dict_list:
                        goods_ids_list.append(price_gear_dict["goods_id"])

                    for item in order_data:
                        for order in item["sku_order_list"]:
                            if str(order["sku_info"]["product_id"]) in goods_ids_list:
                                order["main_order_id"] = item["order_id"]
                                order["product_id"] = order["sku_info"]["product_id"]
                                order["sku_id"] = order["sku_info"]["sku_id"]
                                order["product_name"] = order["sku_info"]["product_name"]
                                del order["sku_info"]
                                if item["order_status"] in reward_order_status_list:
                                    reward_order_list.append(order)
                                all_order_list.append(order)

                    all_order_detail_list = []
                    all_main_order_id_list = []
                    shop_order_detail = None
                    is_order_cache = False if len(all_order_list) <= 100 else True
                    for order in all_order_list:
                        if order["main_order_id"] not in all_main_order_id_list:
                            invoke_result_data_shake_shop = shake_shop_base_model.order_detail(order["main_order_id"], is_cache=is_order_cache)
                            if invoke_result_data_shake_shop.success == True:
                                shop_order_detail = invoke_result_data_shake_shop.data["shop_order_detail"]
                                all_order_detail_list.append(shop_order_detail)
                                all_main_order_id_list.append(order["main_order_id"])
                        else:
                            shop_order_detail = query(all_order_detail_list).first_or_default(None, lambda x: str(x['order_id']) == str(order['main_order_id']))
                        if not shop_order_detail or (user_info_dict["union_id"] and user_info_dict["union_id"] != shop_order_detail["doudian_open_id"]):
                            continue
                        sku_order=None
                        for sku_info_dict in shop_order_detail["sku_order_list"]:
                            if str(sku_info_dict["product_id"]) == str(order["product_id"]) and str(sku_info_dict["sku_id"]) == str(order["sku_id"]) and not sku_info_dict.get("is_use"):
                                sku_order=sku_info_dict
                                sku_info_dict["is_use"]=1
                                break
                        # sku_order = query(shop_order_detail["sku_order_list"]).first_or_default(None, lambda x: str(x["product_id"]) == str(order["product_id"]) and str(x["sku_id"]) == str(order["sku_id"]) and str(x["order_id"]) == str(order["order_id"]))
                        if not sku_order:
                            continue
                        order["order_status"] = sku_order["order_status"] # 子订单号状态
                        order["main_status"] = sku_order["main_status"] # 主流程状态
                        order["sub_order_no"] = sku_order["order_id"] # 子订单号
                        order["pay_time"] = TimeHelper.timestamp_to_format_time(int(sku_order['pay_time'])) # 支付时间
                        order["pay_amount"] = sku_order['pay_amount'] # 支付金额（单位：分）
                        order["item_num"] = sku_order['item_num'] # 订单商品数量
                        order["after_sale_info"] = sku_order['after_sale_info'] # 售后信息
                        order["spec"] = sku_order['spec'] # 规格信息
                        order["product_pic"] = sku_order["product_pic"]

                    pay_price = 0
                    pay_num = 0
                    buy_num = 0
                    pay_order_list = []
                    main_order_dict = {}
                    for order in reward_order_list:
                        try:
                            shop_order_detail = query(all_order_detail_list).first_or_default(None, lambda x: str(x['order_id']) == str(order['main_order_id']))
                            if not shop_order_detail:
                                continue
                            sku_order = query(shop_order_detail["sku_order_list"]).first_or_default(None, lambda x: str(x["product_id"]) == str(order["product_id"]) and str(x["sku_id"]) == str(order["sku_id"]) and str(x["order_id"]) == str(order["sub_order_no"]))
                            if sku_order:
                                # 申请售后中订单不予次数（除外：27-拒绝售后申请/28-售后失败）
                                if sku_order['after_sale_info'] and sku_order['after_sale_info'].get("after_sale_status") not in [0,27,28]:
                                    continue
                                order["order_status"] = sku_order["order_status"] # 子订单号状态
                                order["main_status"] = sku_order["main_status"] # 主流程状态
                                order["pay_time"] = TimeHelper.timestamp_to_format_time(int(sku_order['pay_time'])) # 支付时间
                                order["pay_amount"] = sku_order['pay_amount'] # 支付金额（单位：分）
                                order["item_num"] = sku_order['item_num'] # 订单商品数量
                                order["after_sale_info"] = sku_order['after_sale_info'] # 售后信息
                                order["spec"] = sku_order['spec'] # 规格信息
                                order["ext_json"] = {}
                                order["ext_json"]['encrypt_post_tel'] = sku_order['encrypt_post_tel']
                                order["ext_json"]['encrypt_post_receiver'] = sku_order['encrypt_post_receiver']
                                order["ext_json"]['province'] = sku_order['post_addr']["province"]["name"]
                                order["ext_json"]['city'] = sku_order['post_addr']["city"]["name"]
                                order["ext_json"]['town'] = sku_order['post_addr']["town"]["name"]
                                order["ext_json"]['street'] = sku_order['post_addr']["street"]["name"]
                                order["ext_json"]['post_detail'] = sku_order['post_addr']["encrypt_detail"]
                                order["ext_json"]["mask_post_receiver"] = sku_order['mask_post_receiver']
                                order["ext_json"]["mask_post_tel"] = sku_order['mask_post_tel']
                                order["ext_json"]["mask_detail"] = sku_order['mask_post_addr']['detail']
                                order["ext_json"]["goods_code"] = sku_order['code']
                                order["ext_json"]["open_address_id"] = shop_order_detail['open_address_id']

                            #判断是否已经加过奖励
                            if order["sub_order_no"] not in pay_order_no_list and int(order["order_status"]) in reward_order_status_list and order["after_sale_info"]["refund_status"] != '3': # 订单状态;1 待确认/待支付-订单创建完毕;105-已支付; 2-备货中； 101-部分发货; 3-已发货（全部发货）;4- 已取消;5 已完成（已收货）;
                                asset_object_name = ""
                                asset_object_id = ""
                                now_price_gear_dict = None
                                for price_gear_dict in price_gear_dict_list:
                                    if (price_gear_dict["effective_date"] == '1900-01-01 00:00:00' or TimeHelper.format_time_to_datetime(price_gear_dict["effective_date"]) < TimeHelper.format_time_to_datetime(order["pay_time"])) and price_gear_dict["goods_id"] == str(order["product_id"]):
                                        #关联类型：1商品skuid关联2商品id关联
                                        if price_gear_dict["relation_type"] == 1 and price_gear_dict["sku_id"] != str(order["sku_id"]):
                                            continue
                                        now_price_gear_dict = price_gear_dict
                                if not now_price_gear_dict:
                                    continue
                                asset_object_id = now_price_gear_dict["id"]
                                asset_object_name = now_price_gear_dict["price_gear_name"]

                                third_pay_order =ThirdPayOrder()
                                third_pay_order.app_id = app_id
                                third_pay_order.act_id = act_id
                                third_pay_order.user_id = user_id
                                third_pay_order.ascription_type = ascription_type
                                third_pay_order.open_id = user_info_dict["open_id"]
                                third_pay_order.user_nick = user_info_dict["user_nick"]
                                third_pay_order.main_pay_order_no = order['main_order_id']
                                third_pay_order.sub_pay_order_no = order['sub_order_no']
                                third_pay_order.goods_code = order['product_id']
                                third_pay_order.goods_name = order['product_name']
                                third_pay_order.goods_pic = order['product_pic']
                                third_pay_order.sku_id = order['sku_id']
                                third_pay_order.sku_name = SevenHelper.json_dumps(order['spec'])
                                third_pay_order.buy_num = order["item_num"]
                                third_pay_order.pay_price = decimal.Decimal(int(order["pay_amount"]) / 100)
                                third_pay_order.order_status = order['order_status']
                                third_pay_order.create_date = SevenHelper.get_now_datetime()
                                third_pay_order.asset_type = asset_type[str(now_price_gear_dict["business_type"])] if isinstance(asset_type, dict) else asset_type
                                third_pay_order.asset_object_id = asset_object_id
                                third_pay_order.asset_object_name = asset_object_name
                                third_pay_order.surplus_count = order['item_num']
                                third_pay_order.pay_date = order['pay_time']

                                main_order_key = f"{asset_object_id}_{order['main_order_id']}"
                                third_main_order = main_order_dict.get(main_order_key)
                                if third_main_order:
                                    third_main_order.buy_num += third_pay_order.buy_num
                                    third_main_order.pay_price += third_pay_order.pay_price
                                    third_main_order.surplus_count += third_pay_order.buy_num
                                    main_order_dict[main_order_key] = third_main_order
                                else:
                                    third_main_order = ThirdMainOrder()
                                    third_main_order.app_id = app_id
                                    third_main_order.act_id = act_id
                                    third_main_order.user_id = user_id
                                    third_main_order.ascription_type = ascription_type
                                    third_main_order.open_id = user_info_dict["open_id"]
                                    third_main_order.user_nick = user_info_dict["user_nick"]
                                    third_main_order.main_pay_order_no = order['main_order_id']
                                    third_main_order.buy_num = third_pay_order.buy_num
                                    third_main_order.pay_price = third_pay_order.pay_price
                                    third_main_order.order_status = order['order_status']
                                    third_main_order.create_date = SevenHelper.get_now_datetime()
                                    third_main_order.asset_type = third_pay_order.asset_type
                                    third_main_order.asset_object_id = asset_object_id
                                    third_main_order.asset_object_name = asset_object_name
                                    third_main_order.surplus_count = third_pay_order.buy_num
                                    third_main_order.pay_date = order['pay_time']
                                    order["ext_json"]["product_name"] = order['product_name']
                                    order["ext_json"]["product_pic"] = order['product_pic']
                                    third_main_order.ext_json = SevenHelper.json_dumps(order["ext_json"])
                                    main_order_dict[main_order_key] = third_main_order

                                payment = decimal.Decimal(int(order["pay_amount"]) / 100)
                                pay_price = decimal.Decimal(pay_price) + payment
                                pay_num = pay_num + 1
                                buy_num = buy_num + int(order['item_num'])

                                pay_order_list.append(third_pay_order)
                        except Exception as ex:
                            if self.context:
                                self.context.logging_link_info(str(order) + "【同步抖店支付订单】" + traceback.format_exc())
                            elif self.logging_link_info:
                                self.logging_link_info(str(order) + "【同步抖店支付订单】" + traceback.format_exc())
                            continue
                    if len(pay_order_list) > 0:
                        db_transaction = DbTransaction(db_config_dict=config.get_value(self.db_connect_key), context=self.context)
                        third_pay_order_model = ThirdPayOrderModel(db_transaction=db_transaction, context=self.context).set_sub_table(app_id)
                        third_main_order_model = ThirdMainOrderModel(db_transaction=db_transaction, context=self.context).set_sub_table(app_id)
                        db_transaction.begin_transaction()
                        third_pay_order_model.add_list(pay_order_list)
                        for third_main_order in main_order_dict.values():
                            third_main_order_model.add_update_entity(third_main_order,"buy_num=buy_num+%s,pay_price=pay_price+%s,surplus_count=surplus_count+%s", params=[third_main_order.buy_num, third_main_order.pay_price, third_main_order.surplus_count])
                        result, message = db_transaction.commit_transaction(True)
                        if result == True:
                            asset_base_model = AssetBaseModel(context=self.context)
                            invoke_result_data.data = {}
                            invoke_result_data.data["asset_list"] = []
                            for item in pay_order_list:
                                only_id = str(item.sub_pay_order_no)
                                asset_invoke_result_data = asset_base_model.update_user_asset(app_id,act_id,module_id,user_id,user_info_dict["open_id"],user_info_dict["user_nick"],item.asset_type,item.buy_num,item.asset_object_id,1,"","","购买",only_id,handler_name,request_code,info_json={})
                                if asset_invoke_result_data.success == False:
                                    invoke_result_data.success = False
                                    invoke_result_data.error_code = "error"
                                    invoke_result_data.error_message = asset_invoke_result_data.error_message
                                else:
                                    redis_init.lpush(pay_order_cache_key,item.sub_pay_order_no)
                                    redis_init.expire(pay_order_cache_key, 30 * 24 * 3600)
                                    data = {}
                                    data["asset_type"] = item.asset_type
                                    data["asset_object_id"] = item.asset_object_id
                                    data["buy_num"] = item.buy_num
                                    invoke_result_data.data["asset_list"].append(data)

                            invoke_result_data.data["buy_num"] = buy_num
                            invoke_result_data.data["pay_price"] = pay_price
                            invoke_result_data.data["pay_num"] = pay_num
                        else:
                            raise Exception("执行事务失败", message)
                    else:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = "没有匹配订单"
                    if len(all_order_list) > 0:
                        user_base_model = UserBaseModel(context=self.context)
                        black_status = user_base_model.check_pull_black(user_info_dict, act_info_dict["is_black"], act_info_dict["refund_count"], all_order_list, 3)
                        if black_status == True:
                            invoke_result_data.data = {} if not invoke_result_data.data else invoke_result_data.data
                            invoke_result_data.data["user_state"] = 1
                else:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "没有订单"
        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【同步抖店支付订单】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【同步抖店支付订单】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"
        finally:
            frane_base_model.business_process_executed()
        return invoke_result_data

    def _get_shake_shop_pay_order_no_list(self, app_id, user_id, redis_init):
        """
        :description: 获取抖店已存在的子订单编号列表
        :param app_id:应用标识
        :param user_id:用户标识
        :param redis_init:redis_init
        :return: 
        :last_editors: HuangJianYi
        """
        pay_order_cache_key = f"shake_shop:pay_order_no_list:appid_{app_id}_userid_{user_id}"
        pay_order_no_list = redis_init.lrange(pay_order_cache_key,0,-1)
        pay_order_list = []
        is_add = False
        if not pay_order_no_list or len(pay_order_no_list)<=0:
            third_pay_order_model = ThirdPayOrderModel(context=self.context)
            pay_order_list = third_pay_order_model.get_dict_list("app_id=%s and user_id=%s",field="sub_pay_order_no", params=[app_id,user_id])
            is_add = True

        if len(pay_order_list) > 0:
            for item in pay_order_list:
                pay_order_no_list.append(item["sub_pay_order_no"])
                if is_add == True:
                    redis_init.lpush(pay_order_cache_key,item["sub_pay_order_no"])
                    redis_init.expire(pay_order_cache_key, 30 * 24 * 3600)
        return pay_order_no_list,pay_order_cache_key
