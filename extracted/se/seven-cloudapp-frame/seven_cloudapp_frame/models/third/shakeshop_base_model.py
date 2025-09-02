# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2022-01-10 11:31:34
@LastEditTime: 2025-09-01 15:43:22
@LastEditors: HuangJianYi
@Description: 抖店接口业务模型
"""

import json
import time
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import MD5, SHA256, Hash
from cryptography.hazmat.primitives.hmac import HMAC
from seven_cloudapp_frame.libs.customize.seven_helper import SevenHelper
from seven_cloudapp_frame.models.seven_model import *
from seven_framework.base_model import *


class ShakeShopBaseModel():
    """
    :description: 抖店接口业务模型(IP白名单功能说明应用IP白名单功能:开发者需在开放平台控制台提前配置可信的IP白名单，只有属于IP白名单中的IP地址访问AP接口时，平台网关才允许通过，否则调用AP 接口将被拒绝)
    """
    def __init__(self, context, app_key: str, app_secret: str, app_type="SELF", code=None, shop_id: str = None, auth_subject_type: str = "MiniApp", proxy: str = None, test_mode=False, logging_error=None, logging_info=None):
        """
        :description:  初始化实例，自用型应用传入shop_id用于初始化access token，工具型应用传入code换取access token（如初始化时未传入，可以在访问抖店API之前调用init_token(code)进行token的初始化。
        :param context: 上下文
        :param app_key: app_key
        :param app_secret: app_secret
        :param app_type: app_type(SELF或TOOL)
        :param code: code
        :param shop_id: 店铺ID
        :param auth_subject_type:授权主体类型，配合auth_id字段使用，YunCang -云仓；WuLiuShang -物流商；WLGongYingShang -物流供应商；MiniApp -小程序；MCN-联盟MCN机构；DouKe-联盟抖客 ；Colonel-联盟团长；
        :param proxy: 代理
        :param test_mode: 是否测试沙盒
        :param logging_error: logging_error
        :param logging_info: logging_info
        :return 
        :last_editors: HuangJianYi
        """
        self.context = context
        self.logging_link_error = logging_error
        self.logging_link_info = logging_info
        self.app_key = app_key
        self.app_secret = app_secret
        self.app_type = app_type
        if self.app_type == "SELF" and not shop_id:
            raise Exception('shop_id不能为空')
        self.shop_id = shop_id
        self.auth_subject_type = auth_subject_type
        self.proxy = proxy
        self.test_mode = test_mode
        if self.test_mode:
            self._gate_way = 'https://openapi-sandbox.jinritemai.com'
        else:
            self._gate_way = 'https://openapi-fxg.jinritemai.com'
        self._version = 2
        self.redis_token_key = f"shakeshop_access_token:{str(app_key)}_{self.test_mode}"
        if shop_id:
            self.redis_token_key += f"_{shop_id}"
        redis_token = SevenHelper.redis_init(config_dict=config.get_value("platform_redis")).get(self.redis_token_key)
        if redis_token:
            redis_token = json.loads(redis_token)
        self._token = redis_token
        self._sign_method = 'hmac-sha256'
        if self._token:
            if self._token.get('expires_in') - int(time.time()) < 3000:
                self._refresh_token()
        else:
            exception_message = 'assess_token获取失败，请检查配置，店铺ID:' + str(shop_id)
            if self.app_type == "SELF":
                is_success, init_error_message = self.init_token()
                if is_success == False:
                    exception_message += ":" + init_error_message
                    raise Exception(exception_message)
            elif self.app_type == "TOOL" and code:
                is_success, init_error_message = self.init_token(code)
                if is_success == False:
                    exception_message += ":" + init_error_message
                    raise Exception(exception_message)

    def _sign(self, method: str, param_json: str, timestamp: str) -> str:
        param_pattern = 'app_key{}method{}param_json{}timestamp{}v{}'.format(self.app_key, method, param_json, timestamp, self._version)
        sign_pattern = '{}{}{}'.format(self.app_secret, param_pattern, self.app_secret)
        return self._hash_hmac(sign_pattern)

    def _hash_hmac(self, pattern: str) -> str:
        try:
            hmac = HMAC(key=self.app_secret.encode('UTF-8'), algorithm=SHA256(), backend=default_backend())
            hmac.update(pattern.encode('UTF-8'))
            signature = hmac.finalize()
            return signature.hex()
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            return None

    def _access_token(self) -> str:
        """
        :description: 获取access_token
        :return 
        :last_editors: HuangJianYi
        """
        if not self._token:
            raise Exception('no token info, call init_token() to initialize it.')
        try:
            if self._token.get('expires_in') - int(time.time()) < 3000:
                self._refresh_token()
            return self._token.get('access_token')
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            return None

    def init_token(self, code: str = '') -> bool:
        """
        :description: 初始化access_token
        :param code: 工具型应用从授权url回调中获取到的code，自用型应用无需传入。
        :return 
        :last_editors: HuangJianYi
        """
        is_success = True
        message = ""
        try:
            if self.app_type == "TOOL" and not code:
                raise Exception('code不能为空')
            path = '/token/create'
            grant_type = 'authorization_self' if self.app_type == "SELF" else 'authorization_code'
            params = {}
            params.update({'code': code if code else ''})
            params.update({'grant_type': grant_type})
            if self.app_type == "SELF":
                if self.test_mode:
                    params.update({'test_shop': '1'})
                elif self.auth_subject_type:
                    params.update({'auth_subject_type': self.auth_subject_type})
                    params.update({'auth_id': self.shop_id})
                elif self.shop_id:
                    params.update({'shop_id': self.shop_id})
                else:
                    raise Exception('shop_id不能为空')
            result = self._request(path=path, params=params, token_request=True)
            if result and result.get('code') == 10000 and result.get('data'):
                self._token = result.get('data')
                self._token.update({'expires_in': int(time.time()) + result.get('data').get('expires_in')})
                SevenHelper.redis_init(config_dict=config.get_value("platform_redis")).set(self.redis_token_key, json.dumps(self._token), ex=3600)
                is_success = True
            else:
                raise Exception("初始化失败：" + json.dumps({"request": params, "reponse": result}))
        except Exception as e:
            # if self.context:
            #     self.context.logging_link_error(traceback.format_exc())
            # elif self.logging_link_error:
            #     self.logging_link_error(traceback.format_exc())
            is_success = False
            message = traceback.format_exc()
        return is_success, message

    def _get_refresh_token(self) -> str:
        """
        :description: 获取refresh_token
        :return 
        :last_editors: HuangJianYi
        """
        if not self._token:
            return None
        try:
            return self._token.get('refresh_token')
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            return None

    def _refresh_token(self) -> None:
        """
        :description: 刷新refresh_token
        :return 
        :last_editors: HuangJianYi
        """
        path = '/token/refresh'
        refresh_token = self._get_refresh_token()
        grant_type = 'refresh_token'
        params = {}
        params.update({'grant_type': grant_type})
        params.update({'refresh_token': refresh_token})
        result = self._request(path=path, params=params, token_request=True)
        if result and result.get('err_no') == 0 and result.get('data'):
            self._token = result.get('data')
            self._token.update({'expires_in': int(time.time()) + result.get('data').get('expires_in')})
            SevenHelper.redis_init(config_dict=config.get_value("platform_redis")).set(self.redis_token_key, json.dumps(self._token), ex=3600)

    def _request(self, path: str, params: dict, token_request: bool = False, is_log: bool = False) -> json:
        """
        :description: 发起请求
        :param path: api地址
        :param params: 参数集合
        :param token_request: 是否token请求
        :param is_log: 是否记录日志
        :return 
        :last_editors: HuangJianYi
        """
        try:
            headers = {}
            headers.update({'Content-Type': 'application/json'})
            headers.update({'Accept': 'application/json'})
            headers.update({'User-Agent': 'newfire doudian python sdk(https://github.com/minibear2021/doudian)'})
            headers.update({'X-USE-PPE': '1'})
            headers.update({'X-TT-ENV': 'ppe_blind_boxes'})
            headers.update({'Origin-From': 'djt_ppe_2024-09-06'})
            timestamp = SevenHelper.get_now_datetime()
            param_json = json.dumps(params, sort_keys=True, separators=(',', ':'))
            method = path[1:].replace('/', '.')
            sign = self._sign(method=method, param_json=json.dumps(params, sort_keys=True, separators=(',', ':'), ensure_ascii=False), timestamp=timestamp)
            if token_request:
                url = self._gate_way + '{}?app_key={}&method={}&timestamp={}&v={}&sign_method={}&sign={}'.format(path, self.app_key, method, timestamp, self._version, self._sign_method, sign)
            else:
                access_token = self._access_token()
                url = self._gate_way + '{}?app_key={}&method={}&access_token={}&timestamp={}&v={}&sign_method={}&sign={}'.format(path, self.app_key, method, access_token, timestamp, self._version, self._sign_method, sign)
            log_info = ""
            if is_log == True:
                log_info = f'Request url:{url},Request headers:{headers},Request params:{param_json};'
            response = requests.post(url=url, data=param_json, headers=headers, proxies=self.proxy)
            if is_log == True:
                log_info += f'Response status code: {response.status_code},Response headers:{response.headers},Response content:' + response.content.decode('utf-8')
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)
            if response.status_code != 200:
                return None
            return json.loads(response.content)
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            return None

    def request(self, path: str, params: dict, is_log: bool = False) -> json:
        """
        :description: 请求抖店API接口
        :param path: 调用的API接口地址，示例：'/material/uploadImageSync'
        :param params: 业务参数字典，示例：{'folder_id':'70031975314169695161250','url':'http://www.demo.com/demo.jpg','material_name':'demo.jpg'}
        :param is_log: 是否记录日志
        :return 
        :last_editors: HuangJianYi
        """
        return self._request(path=path, params=params, is_log=is_log)

    def callback(self, headers: dict, body: bytes, is_log: bool = False) -> json:
        """
        :description: 验证处理消息推送服务收到信息Md5解密模式
        :param headers: headers
        :param body: body
        :param is_log: 是否记录日志
        :return 
        :last_editors: HuangJianYi
        """
        data: str = body.decode('UTF-8')
        if is_log == True:
            if self.context:
                self.context.logging_link_info(f'Callback Header:{headers},Callback Body:{body}')
            elif self.logging_link_info:
                self.logging_link_info(f'Callback Header:{headers},Callback Body:{body}')
        if not data:
            return None
        if headers.get('app-id') != self.app_key:
            return None
        event_sign: str = headers.get('event-sign')
        if not event_sign:
            return None
        h = Hash(algorithm=MD5(), backend=default_backend())
        h.update('{}{}{}'.format(self.app_key, data, self.app_secret).encode('UTF-8'))
        if h.finalize().hex() != event_sign:
            return None
        return json.loads(data)

    def callback_response_success(self):
        """
        :description: 抖店推送服务验证消息，需立即返回success
        :return 字典
        :last_editors: HuangJianYi
        """
        return {'code': 0, 'msg': 'success'}

    def callback_response_error(self, error_code: str = 40041, error_message: str = "解析推送数据失败"):
        """
        :description: 抖店推送服务验证消息，需立即返回success
        :param error_code: 错误码
        :param error_message: 错误信息
        :return 字典
        :last_editors: HuangJianYi
        """
        return {'code': error_code, 'message': error_message}

    def build_auth_url(self, service_id: str, state: str) -> str:
        """
        :description: 拼接授权URL，引导商家点击完成授权
        :param service_id: service_id
        :param state: state
        :return
        :last_editors: HuangJianYi
        """
        if self.app_type == "TOOL":
            return 'https://fuwu.jinritemai.com/authorize?service_id={}&state={}'.format(service_id, state)
        else:
            return None

    def openid_switch(self, open_id: str, open_id_type: int = 1, is_log=False):
        """
        :description: 提供抖音和抖店 Openid 转换功能(https://op.jinritemai.com/docs/api-docs/162/1973)
        :param open_id: 传入的openId
        :param open_id_type: openId类型，1-抖音openId 2-抖店openId
        :param is_log: 是否记录日志
        :return InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            params = {"open_id": open_id, "open_id_type": open_id_type}
            response = self.request(path="/open/openIdSwitch", params=params, is_log=is_log)
            if response and response.get("code") == 10000 and "data" in response:
                response_data = SevenHelper.json_loads(response)
                invoke_result_data.data = response_data["data"] # {"open_id": "dfsdfsgdrwds","open_id_type": "2"}
                return invoke_result_data
            else:
                if response and response.get("sub_code") and response.get("sub_msg"):
                    invoke_result_data.success = False
                    invoke_result_data.error_code = response.get("sub_code")
                    invoke_result_data.error_message = response.get("sub_msg")
                    return invoke_result_data
                raise Exception(f"openId转换失败:{SevenHelper.json_dumps(response)}")

        except Exception as e:
            log_title = f"抖店接口错误：抖音和抖店Openid转换功能(/open/openIdSwitch)"
            if self.context:
                self.context.logging_link_error(log_title + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(log_title + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "openid_switch"
            invoke_result_data.error_message = log_title
            return invoke_result_data

    def get_user_order_list(self, open_id, size=100, page=0, order_status=None, create_time_start=None, create_time_end=None, open_id_type="douyin", while_count=0, is_log=False, default_interval_day=90):
        """
        :description: 支持按抖音小程序open_id查询订单简要信息，仅电商小程序在C端面向用户呈现订单任务类场景使用(https://op.jinritemai.com/docs/api-docs/15/1915)
        :param open_id: 用户openId
        :param size: 单页大小，限制100以内
        :param page: 页码，0页开始
        :param order_status: 订单状态：all-全部，under_sure-待确认，unpaid-待支付，stock_up-待发货，on_delivery-已发货，received-已完成，closed-已关闭，to_groups-待成团
        :param create_time_start: 下单时间：开始，秒级时间戳
        :param create_time_end: 下单时间：截止，秒级时间戳
        :param open_id_type: 用户openId类型，固定为 douyin 抖音
        :param while_count: 循环请求次数 0-无限
        :param is_log: 是否记录日志
        :param default_interval_day: 默认近多少天数
        :return InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        all_order = []
        try:
            params = {"size": size, "open_id":open_id, "open_id_type":open_id_type}
            if order_status:
                params["order_status"] = order_status
            if default_interval_day > 0:
                interval_timestamp = default_interval_day * 24 * 60 * 60 # 90天
                now_timestamp = TimeHelper.get_now_timestamp()
                last_timestamp = now_timestamp - interval_timestamp # 近3个月的开始时间
                if not create_time_start or now_timestamp - create_time_start > interval_timestamp:
                    create_time_start = last_timestamp
                params["create_time_start"] = create_time_start
                params["create_time_end"] = create_time_end if create_time_end else now_timestamp
            else:
                if create_time_start:
                    params["create_time_start"] = create_time_start
                if create_time_end:
                    params["create_time_end"] = create_time_end
            has_next = True
            while has_next:
                params["page"] = page
                response = self.request(path="/order/getUserOrderList", params=params, is_log=is_log)
                if response and response.get("code") == 10000 and "data" in response:
                    response_data = SevenHelper.json_loads(response)
                    if len(response_data["data"]["shop_order_list"]) > 0:
                        all_order.extend(response_data["data"]["shop_order_list"])
                    page_count = SevenHelper.get_page_count(size, int(response_data["data"]["total"]))
                    if page_count == 0 or (page_count - 1 == page) or (while_count > 0 and while_count - 1 == page):
                        has_next = False
                else:
                    if response and response.get("sub_code") and response.get("sub_msg"):
                        invoke_result_data.success = False
                        invoke_result_data.error_code = response.get("sub_code")
                        invoke_result_data.error_message = response.get("sub_msg")
                        return invoke_result_data
                    raise Exception(f"按抖音小程序open_id查询订单简要信息失败:{SevenHelper.json_dumps(response)}")
                page = page + 1

            invoke_result_data.data = all_order
            return invoke_result_data

        except Exception as e:
            log_title = f"抖店接口错误：按抖音小程序open_id查询订单简要信息(/order/getUserOrderList)"
            if self.context:
                self.context.logging_link_error(log_title + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(log_title + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "get_user_order_list"
            invoke_result_data.error_message = log_title
            return invoke_result_data

    def order_detail(self, shop_order_id, is_log=False, is_cache=False):
        """
        :description: 订单详情查询(https://op.jinritemai.com/docs/api-docs/15/1343)
        :param shop_order_id: 店铺父订单号，抖店平台生成，平台下唯一；
        :param is_log: 是否记录日志
        :param is_cache: 是否缓存
        :return InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            redis_init = SevenHelper.redis_init()
            redis_key = f"shakeshop_order_detail:{shop_order_id}"
            if is_cache:
                response_data = redis_init.get(redis_key)
                if response_data:
                    response_data = SevenHelper.json_loads(response_data)
                    invoke_result_data.data = response_data
                    return invoke_result_data
            params = {"shop_order_id": shop_order_id}
            response = self.request(path="/order/orderDetail", params=params, is_log=is_log)
            if response and response.get("code") == 10000 and "data" in response:
                response_data = SevenHelper.json_loads(response)
                invoke_result_data.data = response_data["data"]
                if is_cache:
                    redis_init.set(redis_key, SevenHelper.json_dumps(response_data["data"]), ex=10*60)
                return invoke_result_data
            else:
                if response and response.get("sub_code") and response.get("sub_msg"):
                    invoke_result_data.success = False
                    invoke_result_data.error_code = response.get("sub_code")
                    invoke_result_data.error_message = response.get("sub_msg")
                    return invoke_result_data
                raise Exception(f"订单详情查询失败:{SevenHelper.json_dumps(response)}")

        except Exception as e:
            log_title = f"抖店接口错误：订单详情查询(/order/orderDetail)"
            if self.context:
                self.context.logging_link_error(log_title + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(log_title + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "order_detail"
            invoke_result_data.error_message = log_title
            return invoke_result_data

    def order_search_list(self, page=0, size=100, order_type=None, order_by=None, order_asc=None, product=None, create_time_start='', create_time_end='', custom_params={}, is_log=False):
        """
        :description: 根据条件检索满足要求的订单列表，支持下单时间和更新时间排序；最大支持查询近90天的数据(https://op.jinritemai.com/docs/api-docs/15/1342)
        :param page: 页码，0页开始
        :param size: 单页大小，限制100以内
        :param order_type: 订单类型 0、普通订单 2、虚拟商品订单 4、电子券（poi核销） 5、三方核销
        :param order_by: 排序条件(create_time 订单创建时间；update_time 订单更新时间；默认create_time；)
        :param order_asc: 排序类型，小到大或大到小，默认大到小
        :param product: 商品，number型代表商品ID，其它代表商品名称
        :param create_time_start: 下单时间：开始，秒级时间戳
        :param create_time_end: 下单时间：结束，秒级时间戳
        :param custom_params: 自定义参数字典
        :param is_log: 是否记录日志
        :return InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            params = {"page": page, "size": size}
            if order_type:
                params["order_type"] = order_type
            if order_by:
                params["order_by"] = order_by
            if order_asc:
                params["order_asc"] = order_asc
            if product:
                params["product"] = product
            if not create_time_start:
                interval_timestamp = 30 * 24 * 60 * 60 # 90天
                now_timestamp = TimeHelper.get_now_timestamp()
                create_time_start = now_timestamp - interval_timestamp # 近3个月的开始时间
                params["create_time_start"] = create_time_start
            if create_time_end:
                params["create_time_end"] = create_time_end

            params.update(custom_params)
            response = self.request(path="/order/searchList", params=params, is_log=is_log)
            if response and response.get("code") == 10000 and "data" in response:
                response_data = SevenHelper.json_loads(response)
                invoke_result_data.data = response_data["data"]
                return invoke_result_data
            else:
                if response and response.get("sub_code") and response.get("sub_msg"):
                    invoke_result_data.success = False
                    invoke_result_data.error_code = response.get("sub_code")
                    invoke_result_data.error_message = response.get("sub_msg")
                    return invoke_result_data
                raise Exception(f"订单列表查询失败:{SevenHelper.json_dumps(response)}")

        except Exception as e:
            log_title = f"抖店接口错误：订单列表查询(/order/searchList)"
            if self.context:
                self.context.logging_link_error(log_title + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(log_title + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "order_search_list"
            invoke_result_data.error_message = log_title
            return invoke_result_data

    def product_search_list(self, page=1, size=100, name="", product_id=[], status=0, product_type=-1, custom_params={}, field="product_id,name,img,status,discount_price,market_price,product_type,out_product_id,outer_product_id", is_log=False):
        """
        :description: 批量查询商品列表 使用场景：批量查询商家抖店商品信息 1、支持使用商品状态，商品类型、商品创建时间和更新时间筛选商品 2、最大支持1次查询1万条，如返回商品数据大于1万条，请增加筛选条件。
        :param page: 页码，0页开始
        :param size: 单页大小，限制100以内
        :param name: 商品标题，支持模糊匹配
        :param product_id: 商品id，最大支持传入100个
        :param status: 商品在店铺中状态: 0-在线；1-下线；2-删除；详见商品状态机：https://op.jinritemai.com/docs/question-docs/92/2070
        :param product_type: 商品类型；0-普通；1-新客商品；3-虚拟；6-玉石闪购；7-云闪购 ；127-其他类型；
        :param custom_params: 自定义参数字典
        :param is_log: 是否记录日志
        :return InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            params = {"page": page, "size": size}
            if name:
                params["name"] = name
            if len(product_id) > 0:
                params["product_id"] = product_id
            if status != -1:
                params["status"] = status
            if product_type != -1:
                params["product_type"] = product_type

            params.update(custom_params)
            response = self.request(path="/product/listV2", params=params, is_log=is_log)
            if response and response.get("code") == 10000 and "data" in response:
                response_data = SevenHelper.json_loads(response["data"])
                if field != "*":
                    fields = field.split(",")
                    response_data["data"] = [{field: item[field] for field in fields} for item in response_data["data"] if all(field in item for field in fields)]
                invoke_result_data.data = response_data
                return invoke_result_data
            else:
                if response and response.get("sub_code") and response.get("sub_msg"):
                    invoke_result_data.success = False
                    invoke_result_data.error_code = response.get("sub_code")
                    invoke_result_data.error_message = response.get("sub_msg")
                    return invoke_result_data
                raise Exception(f"批量查询商品列表失败:{SevenHelper.json_dumps(response)}")

        except Exception as e:
            log_title = f"抖店接口错误：批量查询商品列表(/product/listV2)"
            if self.context:
                self.context.logging_link_error(log_title + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(log_title + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "product_search_list"
            invoke_result_data.error_message = log_title
            return invoke_result_data

    def product_detail(self, product_id='', out_product_id='', is_log=False):
        """
        :description: 查询商品详情 使用场景：查询抖店商品详情信息 1、支持使用抖店商品id 2、商品外部开发者自定义编码查询
        :param product_id: 商品ID，抖店系统生成，店铺下唯一；长度19位
        :param out_product_id: 外部商家编码，商家自定义字段
        :param is_log: 是否记录日志
        :return InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            if not product_id and not out_product_id:
                raise Exception("商品ID不能为空")
            params = {}
            if product_id:
                params["product_id"] = product_id
            if out_product_id:
                params["out_product_id"] = out_product_id
            response = self.request(path="/product/detail", params=params, is_log=is_log)
            if response and response.get("code") == 10000 and "data" in response:
                response_data = SevenHelper.json_loads(response)
                invoke_result_data.data = response_data["data"]
                return invoke_result_data
            else:
                if response and response.get("sub_code") and response.get("sub_msg"):
                    invoke_result_data.success = False
                    invoke_result_data.error_code = response.get("sub_code")
                    invoke_result_data.error_message = response.get("sub_msg")
                    return invoke_result_data
                raise Exception(f"查询商品详情查询失败:{SevenHelper.json_dumps(response)}")

        except Exception as e:
            log_title = f"抖店接口错误：查询商品详情(/product/detail)"
            if self.context:
                self.context.logging_link_error(log_title + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(log_title + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "order_detail"
            invoke_result_data.error_message = log_title
            return invoke_result_data

    def sku_list(self, product_id, field="id,sku_status,product_id,price,sell_properties", custom_params={}, is_log=False):
        """
        :description: 获取商品sku列表 根据商品id获取商品的sku列表，支持返回预占库存信息
        :param product_id: 商品ID；抖店系统生成。
        :param field: 输出字段
        :param custom_params: 自定义参数字典
        :param is_log: 是否记录日志
        :return list
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            params = {"product_id": product_id}
            params.update(custom_params)
            response = self.request(path="/sku/list", params=params, is_log=is_log)
            if response and response.get("code") == 10000 and "data" in response:
                response_data = SevenHelper.json_loads(response)
                if field != "*":
                    fields = field.split(",")
                    response_data["data"] = [{field: item[field] for field in fields} for item in response_data["data"] if all(field in item for field in fields)]
                invoke_result_data.data = response_data["data"]
                return invoke_result_data
            else:
                if response and response.get("sub_code") and response.get("sub_msg"):
                    invoke_result_data.success = False
                    invoke_result_data.error_code = response.get("sub_code")
                    invoke_result_data.error_message = response.get("sub_msg")
                    return invoke_result_data
                raise Exception(f"获取商品sku列表失败:{SevenHelper.json_dumps(response)}")

        except Exception as e:
            log_title = "抖店接口错误：获取商品sku列表(/sku/list)"
            if self.context:
                self.context.logging_link_error(log_title + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(log_title + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "product_search_list"
            invoke_result_data.error_message = log_title
            return invoke_result_data

    def mini_activity_create(self, goods_id, activity_name, act_start_date, act_end_date, user_buy_limit=0, online_directly=False, is_log=False):
        """
        :description: 创建专属活动
        :param goods_id: 商品id
        :param activity_name: 活动名称
        :param act_start_date: 活动开始时间（时间字符串）
        :param act_end_date: 活动结束时间（时间字符串）
        :param user_buy_limit: 用户限购数量（0表示不限）
        :param online_directly: 是否直接上线活动（默认否）
        :param is_log: 是否记录日志
        :return: invoke_result_data
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            param = {}
            param["activity_name"] = activity_name
            param["product_id"] = goods_id
            param["activity_start_time"] = TimeHelper.format_time_to_timestamp(act_start_date)
            param["activity_end_time"] = TimeHelper.format_time_to_timestamp(act_end_date)
            if user_buy_limit > 0:
                param["user_buy_limit"] = user_buy_limit
            param["online_directly"] = online_directly
            response = self.request(path="/mini/activity/create", params=param, is_log=is_log)
            if response and response.get("code") == 10000 and "data" in response:
                response_data = SevenHelper.json_loads(response)
                invoke_result_data.data = response_data["data"]
                return invoke_result_data
            else:
                if response and response["sub_code"] and response["sub_msg"]:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = response["sub_code"]
                    invoke_result_data.error_message = response["sub_msg"]
                    return invoke_result_data
                raise Exception(f"创建专属活动失败:{SevenHelper.json_dumps(response)}")
        except Exception as e:
            log_title = f"抖店接口错误：创建专属活动(/mini/activity/create)"
            if self.context:
                self.context.logging_link_error(log_title + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(log_title + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "order_detail"
            invoke_result_data.error_message = log_title
            return invoke_result_data

    def mini_activity_edit(self, exclusive_act_id, act_start_date, act_end_date, user_buy_limit=0, is_log=False):
        """
        :description: 编辑专属活动
        :param exclusive_act_id: 专属活动id
        :param act_start_date: 活动开始时间（时间字符串）
        :param act_end_date: 活动结束时间（时间字符串）
        :param user_buy_limit: 用户限购数量（0表示不限）
        :param is_log: 是否记录日志
        :return: invoke_result_data
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            param = {}
            param["activity_id"] = exclusive_act_id
            param["activity_start_time"] = TimeHelper.format_time_to_timestamp(act_start_date)
            param["activity_end_time"] = TimeHelper.format_time_to_timestamp(act_end_date)
            param["user_buy_limit"] = user_buy_limit
            response = self.request(path="/mini/activity/edit", params=param, is_log=is_log)
            if response and response.get("code") == 10000 and "data" in response:
                response_data = SevenHelper.json_loads(response)
                invoke_result_data.data = response_data["data"]
                return invoke_result_data
            else:
                if response and response.get("sub_code") and response.get("sub_msg"):
                    invoke_result_data.success = False
                    invoke_result_data.error_code = response.get("sub_code")
                    invoke_result_data.error_message = response.get("sub_msg")
                    return invoke_result_data
                raise Exception(f"编辑专属活动失败:{SevenHelper.json_dumps(response)}")
        except Exception as e:
            log_title = f"抖店接口错误：编辑专属活动(/mini/activity/create)"
            if self.context:
                self.context.logging_link_error(log_title + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(log_title + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "order_detail"
            invoke_result_data.error_message = log_title
            return invoke_result_data

    def mini_activity_perate(self, exclusive_act_id, activity_operate_type, is_log=False):
        """
        :description: 变更专属活动状态
        :param exclusive_act_id: 专属活动id
        :param activity_operate_type: 1:活动上线 2:活动下线 3:活动删除，活动删除操作会自动移除商品标，商品标移除后，商品不再受小程序专享价活动规则的限制，请谨慎操作。 4:移除活动商品标。活动只有在下架或者过期的状态下才能操作商品解绑，商品解绑后，活动即作废无法再次恢复，请谨慎操作。
        :param is_log: 是否记录日志
        :return: invoke_result_data
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            param = {}
            param["activity_id"] = exclusive_act_id
            param["activity_operate_type"] = activity_operate_type
            response = self.request(path="/mini/activity/operate", params=param, is_log=is_log)
            if response and response.get("code") == 10000 and "data" in response:
                response_data = SevenHelper.json_loads(response)
                invoke_result_data.data = response_data["data"]
                return invoke_result_data
            else:
                if response and response.get("sub_code") and response.get("sub_msg"):
                    invoke_result_data.success = False
                    invoke_result_data.error_code = response.get("sub_code")
                    invoke_result_data.error_message = response.get("sub_msg")
                    return invoke_result_data
                raise Exception(f"变更专属活动状态失败:{SevenHelper.json_dumps(response)}")
        except Exception as e:
            log_title = f"抖店接口错误：变更专属活动状态(/mini/activity/operate)"
            if self.context:
                self.context.logging_link_error(log_title + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(log_title + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "order_detail"
            invoke_result_data.error_message = log_title
            return invoke_result_data

    def mini_activity_query(self, activity_id, product_id, page_index=1, page_size=10, is_log=False):
        """
        :description: 查询专属活动
        :param exclusive_act_id: 专属活动id
        :param product_id: 商品id
        :param page_index: 页索引
        :param page_size: 页大小
        :param is_log: 是否记录日志
        :return: invoke_result_data
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            param = {}
            param["page_index"] = page_index
            param["page_size"] = page_size
            if activity_id:
                param["activity_id"] = activity_id
            if product_id:
                param["product_id"] = product_id
            response = self.request(path="/mini/activity/query", params=param, is_log=is_log)
            if response and response.get("code") == 10000 and "data" in response:
                response_data = SevenHelper.json_loads(response)
                invoke_result_data.data = response_data["data"]
                return invoke_result_data
            else:
                if response and response.get("sub_code") and response.get("sub_msg"):
                    invoke_result_data.success = False
                    invoke_result_data.error_code = response.get("sub_code")
                    invoke_result_data.error_message = response.get("sub_msg")
                    return invoke_result_data
                raise Exception(f"查询专属活动失败:{SevenHelper.json_dumps(response)}")
        except Exception as e:
            log_title = "查询专属活动(/product/detail)"
            if self.context:
                self.context.logging_link_error(log_title + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(log_title + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "order_detail"
            invoke_result_data.error_message = "查询专属活动(/product/detail)"
            return invoke_result_data

    def m_get_member_info_by_open_id_list(self, app_id, open_id_list, extend_info_list=None, is_log=False):
        """
        :description: 【会员通商家】获取会员信息(https://op.jinritemai.com/docs/api-docs/66/2750)
        【会员通商家】批量获取会员信息
        注1：用户如果当前不是店铺会员，将无法获取会员信息
        注2：[OpenIdList]长度不能大于10
        注3：若用户满足接口调用当天店铺/品牌下90天内有支付单条件，则返回明文手机号，否则仅返回加密手机号，不返回明文手机号
        注4：使用补充信息查询时，会根据补充信息进行额外的校验。
        :param app_id: Int64,表明外部平台
        :param open_id_list: 会员对外的OpenID列表, ["openIdopenIdopenIdopenIdopenId1","openIdopenIdopenIdopenIdopenId2"]
        :param extend_info_list: 额外补充信息 [{"open_id":"同open_id_list中的open_id，对open_id_list中的open_id在查询时补充其他信息", "mask_mobile":"使用手机号掩码查询"}]
        :param is_log: 是否记录日志
        :return InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            params = {"app_id": app_id, "open_id_list": open_id_list}
            if extend_info_list:
                params['extend_info_list'] = extend_info_list
            response = self.request(path="/member/mGetMemberInfoByOpenIdList", params=params, is_log=is_log)
            if response and response.get("code") == 10000 and "data" in response:
                response_data = SevenHelper.json_loads(response)
                invoke_result_data.data = response_data["data"] # {"open_id": "dfsdfsgdrwds","open_id_type": "2"}
                return invoke_result_data
            else:
                if response and response.get("sub_code") and response.get("sub_msg"):
                    invoke_result_data.success = False
                    invoke_result_data.error_code = response.get("sub_code")
                    invoke_result_data.error_message = response.get("sub_msg")
                    return invoke_result_data
                raise Exception(f"获取会员信息失败:{SevenHelper.json_dumps(response)}")

        except Exception as e:
            log_title = f"抖店接口错误：【会员通商家】获取会员信息(/member/mGetMemberInfoByOpenIdList)"
            if self.context:
                self.context.logging_link_error(log_title + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(log_title + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "m_get_member_info_by_open_id_list"
            invoke_result_data.error_message = log_title
            return invoke_result_data

    def batch_get_union_id_by_open_id_list(self, app_id, open_id_list, is_log=False):
        """
        :description: 会员open_id转union_id，通过用于判断是否是品牌会员的订单，如果是返回union_id(https://op.jinritemai.com/docs/api-docs/66/1790)
        :param app_id: Int64,表明外部平台
        :param open_id_list: 会员对外的OpenID列表, ["openIdopenIdopenIdopenIdopenId1","openIdopenIdopenIdopenIdopenId2"]
        :param is_log: 是否记录日志
        :return InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            params = {"app_id": app_id, "open_id_list": open_id_list}
            response = self.request(path="/member/batchGetUnionIdByOpenIdList", params=params, is_log=is_log)
            if response and response.get("code") == 10000 and "data" in response:
                response_data = SevenHelper.json_loads(response)
                invoke_result_data.data = response_data["data"]
                return invoke_result_data
            else:
                if response and response.get("sub_code") and response.get("sub_msg"):
                    invoke_result_data.success = False
                    invoke_result_data.error_code = response.get("sub_code")
                    invoke_result_data.error_message = response.get("sub_msg")
                    return invoke_result_data
                raise Exception(f"会员open_id转union_id失败:{SevenHelper.json_dumps(response)}")

        except Exception as e:
            log_title = f"抖店接口错误：【会员通商家】会员open_id转union_id(/member/batchGetUnionIdByOpenIdList)"
            if self.context:
                self.context.logging_link_error(log_title + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(log_title + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "batch_get_union_id_by_open_id_list"
            invoke_result_data.error_message = log_title
            return invoke_result_data

    def batch_get_open_id_list_by_union_id(self, union_id_list, is_log=False):
        """
        :description: 服务商可以根据品牌维度的用户唯一身份UnionId来查询品牌下每个店铺的用户OpenId(https://op.jinritemai.com/docs/api-docs/66/2814)
        :param union_id_list: 注意： 1）该接口一次最多进行10个UnionId的解析。 2）任意一个unionId不合法都可能导致整个批量请求失败，请传入正确的unionId
        :param is_log: 是否记录日志
        :return InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            params = {"union_id_list": union_id_list}
            response = self.request(path="/member/batchGetOpenIdListByUnionId", params=params, is_log=is_log)
            if response and response.get("code") == 10000 and "data" in response:
                response_data = SevenHelper.json_loads(response)
                invoke_result_data.data = response_data["data"] # {"open_id": "dfsdfsgdrwds","open_id_type": "2"}
                return invoke_result_data
            else:
                if response and response.get("sub_code") and response.get("sub_msg"):
                    invoke_result_data.success = False
                    invoke_result_data.error_code = response.get("sub_code")
                    invoke_result_data.error_message = response.get("sub_msg")
                    return invoke_result_data
                raise Exception(f"UnionId查询品牌下每个店铺的用户OpenId失败:{SevenHelper.json_dumps(response)}")

        except Exception as e:
            log_title = f"抖店接口错误：UnionId查询品牌下每个店铺的用户OpenId(/member/batchGetOpenIdListByUnionId)"
            if self.context:
                self.context.logging_link_error(log_title + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(log_title + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "batch_get_open_id_list_by_union_id"
            invoke_result_data.error_message = log_title
            return invoke_result_data

    def batch_get_history_member_union_id(self, app_id, open_id_list, is_log=False):
        """
        :description:【品牌会员店铺专用】根据店铺会员的openId获取品牌维度的用户身份标识unionId(https://op.jinritemai.com/docs/api-docs/66/2136)
        该接口可以根据店铺会员的openId获取品牌维度的用户身份标识unionId。同品牌下跨店铺中存量的抖音会员，可以用这个接口查询unionId，相同的unionId表示是同一个用户。
        注1：店铺如果不是品牌店铺，将无法获取unionId
        注2：用户如果不是店铺会员，将无法获取unionId
        注3：【重要】即使查询返回unionId，不代表用户是品牌会员
        重要：从品牌方知晓哪些店铺升级为品牌店铺，然后去进行同品牌跨多店的历史会员品牌维度的信息补全，属于一次性操作
        :param app_id: Int64,表明外部平台
        :param open_id_list: 会员对外的OpenID列表，该接口一次最多进行20个Openld的解析
        :param is_log: 是否记录日志
        :return InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            params = {"app_id": app_id, "open_id_list": open_id_list}
            response = self.request(path="/member/batchGetHistoryMemberUnionId", params=params, is_log=is_log)
            if response and response.get("code") == 10000 and "data" in response:
                response_data = SevenHelper.json_loads(response)
                invoke_result_data.data = response_data["data"]
                return invoke_result_data
            else:
                if response and response.get("sub_code") and response.get("sub_msg"):
                    invoke_result_data.success = False
                    invoke_result_data.error_code = response.get("sub_code")
                    invoke_result_data.error_message = response.get("sub_msg")
                    return invoke_result_data
                raise Exception(f"根据店铺会员的openId获取品牌维度的用户身份标识unionId失败:{SevenHelper.json_dumps(response)}")

        except Exception as e:
            log_title = f"抖店接口错误：【品牌会员店铺专用】根据店铺会员的openId获取品牌维度的用户身份标识unionId(/member/batchGetHistoryMemberUnionId)"
            if self.context:
                self.context.logging_link_error(log_title + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(log_title + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "batch_get_history_member_union_id"
            invoke_result_data.error_message = log_title
            return invoke_result_data
