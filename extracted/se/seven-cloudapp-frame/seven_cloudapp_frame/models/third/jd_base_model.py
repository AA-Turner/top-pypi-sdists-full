# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2023-09-26 16:52:07
@LastEditTime: 2024-05-27 10:51:31
@LastEditors: HuangJianYi
:Description:
"""
import traceback
from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.models.seven_model import InvokeResultData
from seven_cloudapp_frame.libs.customize.seven_helper import SevenHelper
from seven_framework import CryptoHelper, JsonHelper, TimeHelper
from seven_jd.jd.api import JosOauthRpcXidPin2XidRequest

from seven_jd.jd.api.base import *
from seven_jd.jd.api.rest.AreasCityGetRequest import AreasCityGetRequest
from seven_jd.jd.api.rest.AreasCountyGetRequest import AreasCountyGetRequest
from seven_jd.jd.api.rest.AreasProvinceGetRequest import AreasProvinceGetRequest
from seven_jd.jd.api.rest.AreasTownGetRequest import AreasTownGetRequest
from seven_jd.jd.api.rest.MiniappMixUserInfoRequest import MiniappMixUserInfoRequest
from seven_jd.jd.api.rest.LockCertsSaveRequest import LockCertsSaveRequest
from seven_jd.jd.api.rest.PalceorderSubmitRequest import PalceorderSubmitRequest
from seven_jd.jd.api.rest.BatchAddSkuAddRequest import BatchAddSkuAddRequest
from seven_jd.jd.api.rest.SellerVenderInfoGetRequest import SellerVenderInfoGetRequest
from seven_jd.jd.api.rest.VenderShopQueryRequest import VenderShopQueryRequest
from seven_jd.jd.api.rest.UserGetUserInfoByOpenIdRequest import UserGetUserInfoByOpenIdRequest
from seven_jd.jd.api.rest.UserGetUserInfoByXIdRequest import UserGetUserInfoByXIdRequest
from seven_jd.jd.api.rest.VenderAuthFindUserRequest import VenderAuthFindUserRequest
from seven_jd.jd.api.rest.SkuReadSearchSkuListRequest import SkuReadSearchSkuListRequest
from seven_jd.jd.api.rest.PopOrderGetRequest import PopOrderGetRequest
from seven_jd.jd.api.rest.JosTokenSourceToOpenIdRequest import JosTokenSourceToOpenIdRequest
from seven_jd.jd.api.rest.PopJmCenterUserGetEncryptPinNewRequest import PopJmCenterUserGetEncryptPinNewRequest
from seven_jd.jd.api.rest.UserRelatedRpcI18nServiceGetOpenIdRequest import UserRelatedRpcI18nServiceGetOpenIdRequest
from seven_jd.jd.api.rest.OrderOperateRequest import OrderOperateRequest
from seven_jd.jd.api.rest.VerifySaveRequest import VerifySaveRequest
from seven_jd.jd.api.rest.OrderCancelRequest import OrderCancelRequest
from seven_jd.jd.api.rest.ApplyRepealSaveRequest import ApplyRepealSaveRequest
from seven_jd.jd.api.rest.CertListQueryRequest import CertListQueryRequest
from seven_jd.jd.api.rest.PreviewSaveRequest import PreviewSaveRequest
from seven_jd.jd.api.rest.CertUnlockRequest import CertUnlockRequest


class JdBaseModel():
    """
    :description: 京东jos接口业务模型（为了不让框架越来越重，框架不默认安装seven_jd模块，需手动配置安装）
    """

    def __init__(self, app_key, app_secret, context=None, logging_error=None, logging_info=None):
        self.app_key = app_key
        self.app_secret = app_secret
        self.context = context
        self.logging_link_error = logging_error
        self.logging_link_info = logging_info

    def access_token(self, code, grant_type="authorization_code"):
        """
        :description：小程序临时登录凭证校验，基于OAuth2.0授权
        :param code：登录票据
        :param grant_type：授权方式
        :return: 返回字典包含字段 access_token,open_id
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        redis_key = f"{self.app_key}_jd_login_code:{code}"
        redis_init = SevenHelper.redis_init()
        access_token_dict = redis_init.get(redis_key)
        if access_token_dict:
            access_token_dict = SevenHelper.json_loads(access_token_dict)
            invoke_result_data.data = access_token_dict
            return invoke_result_data

        param = {
            'code': code,  # 用户点击按钮跳转到授权页, 处理完后重定向到redirect_uri, 并给我们加上code=xxx的参数, 这个code就是我们需要的
            'app_key': self.app_key,
            'app_secret': self.app_secret,
            'grant_type': grant_type,
        }

        # 通过 code 获取 access_token
        request_url = 'https://open-oauth.jd.com/oauth2/access_token'
        try:
            response = requests.get(request_url, params=param)
            response_data = SevenHelper.json_loads(response.text)
            if response_data["code"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["code"]
                invoke_result_data.error_message = response_data["msg"]
                invoke_result_data.data = response_data
                return invoke_result_data

            # open_id = response_data['open_id']
            # session_key = response_data['session_key']
            # redis_init.set(redis_key, SevenHelper.json_dumps(response_data), ex=60 * 60)
            # redis_init.set(f"{app_id}_wechat_sessionkey:{open_id}", session_key, ex=60 * 60)

            invoke_result_data.data = response_data

            return invoke_result_data
        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【access_token】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【access_token】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "error_access_token"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    def seller_vender_info(self, access_token):
        """
        :description: 查询商家基本信息，包括商家编号,商家类型,店铺编号,店铺名称,主营类目编号
        :param access_token：访问令牌
        :return {"jingdong_vender_shop_query_responce": {"col_type": 0, "vender_id": 0, "shop_name": "官方旗舰店", "shop_id": 0, "cate_main": 0}}
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = SellerVenderInfoGetRequest()

        try:
            resp = req.getResponse(access_token)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_seller_vender_info_get_responce" in resp:
                invoke_result_data.data = resp['jingdong_seller_vender_info_get_responce']['vender_info_result']

            return invoke_result_data
        except Exception as e:
            invoke_result_data.success = False
            invoke_result_data.error_code = "seller_vender_info"
            invoke_result_data.error_message = "京东接口错误：查询商家基本信息(jingdong.seller.vender.info.get)"
            return invoke_result_data

    def vender_shop_query(self, access_token):
        """
        :description: 查询商家基本店铺信息，包括商家编号,店铺编号,店铺名称,开店时间,logoUrl,店铺简介,主营类目编号,主营类目名称
        :param access_token：访问令牌
        :return {"jingdong_vender_shop_query_responce": {"shop_jos_result": {"brief": "", "vender_id": 0, "shop_id": 0, "category_main": 0, "logo_url": "", "category_main_name": "文娱", "open_time": 1, "shop_name": "官方旗舰店"}, "code": "0"}}
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = VenderShopQueryRequest()

        try:
            resp = req.getResponse(access_token)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_vender_shop_query_responce" in resp:
                invoke_result_data.data = resp['jingdong_vender_shop_query_responce']['shop_jos_result']

            return invoke_result_data
        except Exception as e:
            invoke_result_data.success = False
            invoke_result_data.error_code = "vender_shop_query"
            invoke_result_data.error_message = "京东接口错误：查询商家基本店铺信息(jingdong.vender.shop.query)"
            return invoke_result_data

    def get_userinfo_by_openid(self, access_token, open_id):
        """
        :description: 根据openId获取用户信息
        :param access_token：访问令牌
        :param open_id：open_id
        :return {"jingdong_user_getUserInfoByOpenId_responce":{"getuserinfobyappidandopenid_result":{"code":0,"data":{"gendar":0,"nickName":"歪*****西","imageUrl":""}},"code":"0"}}
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = UserGetUserInfoByOpenIdRequest()
        req.openId = open_id

        try:
            resp = req.getResponse(access_token)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_user_getUserInfoByOpenId_responce" in resp:
                invoke_result_data.data = resp['jingdong_user_getUserInfoByOpenId_responce'][
                    'getuserinfobyappidandopenid_result']

            return invoke_result_data
        except Exception as e:
            invoke_result_data.success = False
            invoke_result_data.error_code = "get_userinfo_by_openid"
            invoke_result_data.error_message = "京东接口错误：根据openId获取用户信息(jingdong.user.getUserInfoByOpenId)"
            return invoke_result_data

    def get_userinfo_by_xid(self, access_token, xid):
        """
        :description: 根据xid获取用户信息
        :param access_token：访问令牌
        :param xid：xid
        :return {"jingdong_user_getUserInfoByXId_responce":{"getuserinfobyappidandopenid_result":{"code":0,"data":{"gendar":2,"nickName":"nickName"}},"code":"0"}}
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = UserGetUserInfoByXIdRequest()
        req.XId = xid

        try:
            resp = req.getResponse(access_token)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_user_getUserInfoByXId_responce" in resp:
                invoke_result_data.data = \
                    resp['jingdong_user_getUserInfoByXId_responce']['getuserinfobyappidandopenid_result']['data']

            return invoke_result_data
        except Exception as e:
            invoke_result_data.success = False
            invoke_result_data.error_code = "get_userinfo_by_xid"
            invoke_result_data.error_message = "京东接口错误：根据xid获取用户信息(jingdong.user.getUserInfoByXId)"
            return invoke_result_data

    def vender_auth_find_user(self, access_token, pin):
        """
        :description: 根据pin查询用户信息,识别主子pin
        :param access_token：访问令牌
        :param pin：pin
        :return {"jingdong_vender_auth_findUser_responce":{"result":{"authLogin":{"userType":0,"status":1},"success":true},"code":"0"}} userType账号类型：1主账号，0子账号; status账号状态：1有效
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = VenderAuthFindUserRequest()
        req.pin = pin

        try:
            resp = req.getResponse(access_token)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_vender_auth_findUser_responce" in resp:
                invoke_result_data.data = resp['jingdong_vender_auth_findUser_responce']['result']['authLogin']

            return invoke_result_data
        except Exception as e:
            invoke_result_data.success = False
            invoke_result_data.error_code = "vender_auth_find_user"
            invoke_result_data.error_message = "京东接口错误：根据pin查询用户信息,识别主子pin(jingdong.vender.auth.findUser)"
            return invoke_result_data

    def oauth_rpc_xid_pin_2_xid(self, access_token, pin, is_log=False):
        """
        :description: 将pin转化为Xid
        :param access_token：访问令牌
        :param pin：pin
        :param is_log：是否记录请求日志
        :京东返回 {'jingdong_jos_oauth_rpc_xid_pin2Xid_responce': {'code': '0', 'returnType': {'code': 0, 'data': 'o*AAQ2VMNweFJXvq0fAvKFvwKXYWFlN2V-TL3ae5er69vpBBF9FJU', 'requestId': 'b6fea80470c44bb49eb84c5c9e9922d0'}}}
        :return xid
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = JosOauthRpcXidPin2XidRequest()
        req.userPin = pin
        req.appKey = self.app_key

        try:
            resp = req.getResponse(access_token)
            if is_log:
                log_info = "【req】：" + str(req.__dict__) + "【resp】：" + str(resp) + \
                           "【access_token】：" + access_token + "【将pin转化为Xid】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_jos_oauth_rpc_xid_pin2Xid_responce" in resp:
                return_type = invoke_result_data.data = resp['jingdong_jos_oauth_rpc_xid_pin2Xid_responce']['returnType']
                if int(return_type["code"]) != 0:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = return_type["code"]
                    invoke_result_data.error_message = return_type["msg"]
                    return invoke_result_data
                invoke_result_data.data = return_type["data"]

            return invoke_result_data
        except Exception as e:
            invoke_result_data.success = False
            invoke_result_data.error_code = "oauth_rpc_xid_pin_2_xid"
            invoke_result_data.error_message = "京东接口错误：将pin转化为Xid(jingdong.jos.oauth.rpc.xid.pin2Xid)"
            return invoke_result_data

    def miniapp_mix_user_info(self, code, is_log=False):
        """
        :description: 小程序用户信息标识
        :param code: 登录票据
        :param is_log：是否记录请求日志
        :return {'jingdong_miniapp_mixUserInfo_responce': {'code': '0', 'result': {'code': '0', 'mixUserInfo': {'xId': 'o*AAQ2VMNweFJXvq0fAvKFvwKXYWFlN21QRryiD7Ee-xKj1WWh0Xk3SvqnsOapoBq355aRCFpn', 'openId': 'ZX0EbOgVSOawkpIywbU9Uxr-PRVjCE-RdAs4xSZuSyg'}}}}
        :return {'jingdong_miniapp_mixUserInfo_responce': {'code': '0', 'result': {'code': 10102, 'error': 'code已过期'}}}
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = MiniappMixUserInfoRequest()
        req.code = code

        try:
            resp = req.getResponse()

            if is_log:
                log_info = str(resp) + "【小程序用户信息标识】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_miniapp_mixUserInfo_responce" in resp:
                result = resp['jingdong_miniapp_mixUserInfo_responce']['result']
                if int(result['code']) != 0:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = result['code']
                    invoke_result_data.error_message = result['error']
                    return invoke_result_data

                invoke_result_data.data = result["mixUserInfo"]

            return invoke_result_data
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "miniapp_mix_user_info"
            invoke_result_data.error_message = "京东接口错误：小程序用户信息标识(jingdong.miniapp.mixUserInfo)"
            return invoke_result_data

    def sku_read_search_sku_list(self, access_token, field="wareId,skuId,jdPrice,logo,skuName,wareTitle", ware_title="",
                                 ware_ids="", sku_ids="", sku_status="", page_index=1, page_size=50,
                                 order_filed="skuId", order_type="desc", is_log=False):
        """
        :description: SKU搜索服务
        :param access_token: access_token
        :param field: 自定义返回字段，如：wareId,skuId,jdPrice,logo,skuName,wareTitle
        :param ware_title: 商品名称
        :param ware_ids: 商品ID，最多10个ID
        :param sku_ids: SKU ID，最多20个ID
        :param sku_status: SKU状态：1:上架 2:下架 4:删除 默认查询上架下架商品
        :param page_index: 页码，从1开始
        :param page_size: 每页条数，最大50
        :param order_filed: 排序字段.目前支持skuId、stockNum
        :param order_type: 排序类型：asc、desc
        :return {"jingdong_sku_read_searchSkuList_responce":{"code":"0","page":{'pageSize':50,'data':[{'wareTitle':'迪士尼抽卡盒子','skuName':'迪士尼抽卡盒子 红色','logo':'jfs/t1/178132/32/39357/47776/6511591bF692c352c/e56422468ea44066.png','skuId':10086982152177,'wareId':10024838828001,'props':[],'jdPrice':2.8,'outerId':'','status':1}],'totalItem':1,'pageNo':1}}}
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = SkuReadSearchSkuListRequest()
        req.field = field
        req.wareTitle = ware_title
        req.wareId = ware_ids
        req.skuId = sku_ids
        req.skuStatuValue = sku_status
        req.pageNo = page_index
        req.page_size = page_size
        req.orderFiled = order_filed
        req.orderType = order_type

        try:
            resp = req.getResponse(access_token)

            if is_log:
                log_info = str(resp) + "【access_token】：" + access_token + "【SKU搜索服务】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_sku_read_searchSkuList_responce" in resp:
                invoke_result_data.data = resp['jingdong_sku_read_searchSkuList_responce']['page']

            return invoke_result_data
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "sku_read_search_sku_list"
            invoke_result_data.error_message = "京东接口错误：SKU搜索服务(jingdong.sku.read.searchSkuList)"
            return invoke_result_data

    def get_openid_by_token(self, access_token, token, source="01"):
        """
        :description: 根据token获取openId
        :param access_token: access_token
        :param token: 京麦或者微信手Q的token
        :param source: 01 表示京麦token 02 表示微信手Qt的token
        :return {"jingdong_jos_token_source_to_openId_responce":{"result":{"msg":"appkey无效, 请检查app_key是否填写正确","code":"0","openId":"gNwhwU2CJg-NDJkKdkShYTbfTTFzvqZp_R6RInEVsSA","requestId":"894fcc558ed44920b9a8aa15e39176a2"}}}
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = JosTokenSourceToOpenIdRequest()
        req.token = token
        req.source = source
        req.appKey = self.app_key

        try:
            resp = req.getResponse(access_token)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_jos_token_source_to_openId_responce" in resp:
                invoke_result_data.data = resp['jingdong_jos_token_source_to_openId_responce']['result']

            return invoke_result_data
        except Exception as e:
            invoke_result_data.success = False
            invoke_result_data.error_code = "get_openid_by_token"
            invoke_result_data.error_message = "京东接口错误：根据token获取openId(jingdong.jos.token.source.to.openId)"
            return invoke_result_data

    def get_pin_by_token(self, access_token, token, source="01"):
        """
        :description: 根据京东或微信token获取用户加密pin
        :param access_token: access_token
        :param token: 京东或者微信token
        :param source: 01:京东App，02：微信
        :return {"jingdong_pop_jm_center_user_getEncryptPinNew_responce":{"returnType":{"code":"0","pin":"test","requestId":"12133434","message":"获取pin出现未知异常"}}}
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = PopJmCenterUserGetEncryptPinNewRequest()
        req.token = token
        req.source = source

        try:
            resp = req.getResponse(access_token)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_pop_jm_center_user_getEncryptPinNew_responce" in resp:
                invoke_result_data.data = resp['jingdong_pop_jm_center_user_getEncryptPinNew_responce']['returnType']

            return invoke_result_data
        except Exception as e:
            invoke_result_data.success = False
            invoke_result_data.error_code = "get_pin_by_token"
            invoke_result_data.error_message = "京东接口错误：根据京东或微信token获取用户加密pin(jingdong.pop.jm.center.user.getEncryptPinNew)"
            return invoke_result_data

    def get_open_id_by_pin(self, access_token, pin):
        """
        :description: 加密PIN获取openID
        :param access_token: access_token
        :param pin: 加密PIN
        :return {"jingdong_UserRelatedRpcI18nService_getOpenId_responce":{"result":{"msg":"错误信息","code":"0","data":"782789173981","requestId":"342ce495"}}}
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = UserRelatedRpcI18nServiceGetOpenIdRequest()
        req.pin = pin

        try:
            resp = req.getResponse(access_token)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_UserRelatedRpcI18nService_getOpenId_responce" in resp:
                invoke_result_data.data = resp['jingdong_UserRelatedRpcI18nService_getOpenId_responce']['result']

            return invoke_result_data
        except Exception as e:
            invoke_result_data.success = False
            invoke_result_data.error_code = "get_pin_by_token"
            invoke_result_data.error_message = "京东接口错误：加密PIN获取openID(jingdong.UserRelatedRpcI18nService.getOpenId)"
            return invoke_result_data

    def get_xid_by_openid(self, access_token, open_id):
        """
        :description: openId2.0将openId转为xid
        :param access_token: access_token
        :param open_id: open_id
        :return {"jingdong_jos_oauth_rpc_xid_openId2Xid_responce":{"returnType":{"code":0,"data":"o*AAR9mjrxGZ5Wj8k5FP68f7gyZThhYR8Q5ykrlQh11yRuPiTIiZANgjfTy9UJKMkmEyte2JFC","requestId":"422373ebc9314c259496ced65c996f5a"},"code":"0"}}
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = UserRelatedRpcI18nServiceGetOpenIdRequest()
        req.appKey = self.app_key
        req.openId = open_id

        try:
            resp = req.getResponse(access_token)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_jos_oauth_rpc_xid_openId2Xid_responce" in resp:
                invoke_result_data.data = resp['jingdong_jos_oauth_rpc_xid_openId2Xid_responce']['returnType']

            return invoke_result_data
        except Exception as e:
            invoke_result_data.success = False
            invoke_result_data.error_code = "get_pin_by_token"
            invoke_result_data.error_message = "京东接口错误：openId2.0将openId转为xid(jingdong.jos.oauth.rpc.xid.openId2Xid)"
            return invoke_result_data

    def lock_certs_save(self, access_token, vender_id, transaction_id, certList, is_log=False):
        """
        :description: 锁定卡密
        :param access_token: access_token
        :param vender_id: 商家唯一标识，必填
        :transaction_id： 交易ID，必填，做幂等,要保证唯一
        :param certList: [{"cardNum":"","pwd":null,"verifyingTimes":null,"mobile":null}]
            cardNum: 卡号， 必填，需使用AES加密，CryptoHelper.aes_encrypt(card_num, "07afbc8bca08bc5139d36b3239ab3408")
            pwd: 密码，非必填，非空时需使用AES加密
            verifyingTimes: 核销次数，非必填
            mobile: 手机号，非必填
        :param is_log: 是否记录日志
        :京东接口返回 {'jingdong_lockCerts_save_responce': {'code': '0', 'ydResponse': {'result': {'msg': '未查询到商家或结果不唯一', 'code': 404}, 'requestId': 'dc9d88a1-81ae-4da5-976d-a36707f18a45', 'success': True}}}
        :京东接口返回 {'jingdong_lockCerts_save_responce': {'code': '0', 'ydResponse': {'result': {'msg': 'Success', 'code': 200, 'data': {'errMsg': '凭证数量不一致', 'status': 3}}, 'requestId': '94adc061-e89e-4bce-be49-2457bba2672e', 'success': True}}}
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = LockCertsSaveRequest()
        aes_key1 = share_config.get_value("jd_config",{}).get("aes_key1","17f72a775ec0a96ad52b662206c7bceb")
        aes_key2 = share_config.get_value("jd_config",{}).get("aes_key2","07afbc8bca08bc5139d36b3239ab3408")
        for cert in certList:
            cert_num = CryptoHelper.aes_decrypt(cert["cardNum"], aes_key1)
            cert["cardNum"] = CryptoHelper.aes_encrypt(cert_num, aes_key2)
            pwd = CryptoHelper.aes_decrypt(cert["pwd"], aes_key1)
            cert["pwd"] = CryptoHelper.aes_encrypt(pwd, aes_key2)

        data = {
            "transactionId": transaction_id,
            "certList": certList
        }

        req.data = JsonHelper.json_dumps(data)
        req.merchantCode = vender_id

        try:
            resp = req.getResponse(access_token)

            if is_log:
                log_info = "【req】：" + str(req.__dict__) + "【resp】：" + str(resp) + \
                           "【access_token】：" + access_token + "【锁定卡密】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_lockCerts_save_responce" in resp:
                if resp['jingdong_lockCerts_save_responce']['ydResponse']['success'] == False:
                    error = resp['jingdong_lockCerts_save_responce']['ydResponse']['error']
                    invoke_result_data.success = False
                    invoke_result_data.error_code = error['code']
                    invoke_result_data.error_message = error['status']
                    return invoke_result_data
                else:
                    result = resp['jingdong_lockCerts_save_responce']['ydResponse']['result']
                    if int(result['code']) != 200:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = result['code']
                        invoke_result_data.error_message = result['msg']
                        return invoke_result_data
                    else:
                        if int(result["data"]["status"]) != 1:
                            invoke_result_data.success = False
                            invoke_result_data.error_code = result['data']['status']
                            invoke_result_data.error_message = result['data']['errMsg']
                            return invoke_result_data

                        invoke_result_data.data = result["data"]

            return invoke_result_data
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "lock_certs_save"
            invoke_result_data.error_message = "京东接口错误：锁定卡密(jingdong.lockCerts.save)"
            return invoke_result_data

    def palce_order_submit(self, access_token, xid, user_ip, business_data_id, order_source,
                           name, mobile, county_id, town_id, address,
                           goods_sku_id, goods_quantity, is_log=False, pin=None):
        """
        :description: 代下单提单
        :param access_token: access_token
        :param xid: 用户标识,如果京东出现CRM_USER_NOT_LOGIN报错，需要传入real_pin
        :param user_ip: 用户IP
        :param business_data_id: 业务数据ID
        :param order_source: 订单来源，1：PC端，2：移动端APP，3：移动端M版，4：手Q端，5：微信端
        :param name: 联系人姓名
        :param mobile: 联系人手机号
        :param county_id: 县Id
        :param town_id: 街道Id
        :param address: 具体地址
        :param goods_sku_id: 实物skuId
        :param goods_quantity: 实物数量
        :param is_log: 是否记录日志
        :param pin: real_pin
        :京东接口返回 {'jingdong_palceorder_submit_responce': {'code': '0', 'ydResponse': {'requestId': '42414ee9-ca52-47a7-a109-86fe58dc889b', 'success': True, 'result': {'success': True, 'errCode': 1500, 'errMsg': 'ERP下单成功', 'data': {'businessDataId': '11038016', 'orderId': 2334831, 'erpRootOrderId': 277099412543, 'erpRootOrderFee': 2, 'resultFlag': 1}}}}}
        :京东接口返回 {'jingdong_palceorder_submit_responce': {'code': '0', 'ydResponse': {'requestId': '4c5a5a1d-46ca-4848-8847-0b1c4a250ee0', 'success': False, 'error': {'code': 500, 'status': 'CRM_INTERNAL_ERROR'}}}}
        :return {'businessDataId': '11038016', 'orderId': 2334831, 'erpRootOrderId': 277099412543, 'erpRootOrderFee': 2, 'resultFlag': 1}
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        # 该接口调用日期
        promise_date = TimeHelper.get_now_format_time("%Y-%m-%d")

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = PalceorderSubmitRequest()

        data = {
            "userIp": user_ip,
            # "clientIp": "127.0.0.1",
            "businessDataId": business_data_id,
            "erpRootOrderFee": 0,  # erp订单金额
            "orderSource": order_source,
            "address": {
                "name": name,
                "mobile": mobile,
                "countyId": county_id,
                "townId": town_id,
                "address": address
            },
            "goodsDetails": [
                {
                    "goodsSkuId": goods_sku_id,
                    "goodsPrice": 0,  # 实物下单价格，填0
                    "goodsQuantity": goods_quantity,
                    # "goodsName": null # 实物名称，非必填
                }
            ],
            "shipmentTimeType": 3,  # 配送时间类型，1：只工作日送货，2：只双休日、假日送货，3：工作日、双休日与假日均可送货，4：指定日期送货
            "orderCtg": 1,  # 订单类型，1：普通订单，2：预定订单
            # "sendPay": null, # sendPay打标，对方填写
            "promiseDate": promise_date,  # 期望配送时间，格式：yyyy-MM-dd
            # "promiseType": null, # 配送类型，shipmentTimeType传4的话必填，3表示311，4表示411，固定传3
            # "promiseTimeRange": null # 承诺配送时间段，shipmentTimeType传4的话必填，格式：09:00-12:00
        }

        req.data = SevenHelper.json_dumps(data)
        if xid and not pin:
            req.xid_buyer = xid
        if pin:
            req.pin = pin

        try:
            resp = req.getResponse(access_token)
            if is_log:
                log_info = "【req】：" + str(req.__dict__) + "【resp】：" + str(resp) + \
                           "【access_token】：" + access_token + "【代下单提单】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_palceorder_submit_responce" in resp:
                if resp['jingdong_palceorder_submit_responce']['ydResponse']['success'] == False:
                    error = resp['jingdong_palceorder_submit_responce']['ydResponse']['error']
                    invoke_result_data.success = False
                    invoke_result_data.error_code = error['code']
                    invoke_result_data.error_message = error['status']
                    return invoke_result_data
                else:
                    result = resp['jingdong_palceorder_submit_responce']['ydResponse']['result']
                    if result.__contains__('success') and result['success'] == False:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = result["errCode"]
                        result_message = result.get("data",{}).get("resultMessage","")
                        invoke_result_data.error_message = result["errMsg"] if not result_message else result_message
                        return invoke_result_data
                    else:
                        # 1500：ERP下单成功，1502：ERP下单处理中
                        if result["errCode"] not in [1500, 1502]:
                            invoke_result_data.success = False
                            invoke_result_data.error_code = result["errCode"]
                            result_message = result.get("data", {}).get("resultMessage", "")
                            invoke_result_data.error_message = result["errMsg"] if not result_message else result_message
                            return invoke_result_data
                        invoke_result_data.data = result["data"]

            return invoke_result_data
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "palce_order_submit"
            invoke_result_data.error_message = "京东接口错误：代下单提单(jingdong.palceorder.submit)"
            return invoke_result_data

    def pop_order_get(self, access_token, order_id, optional_fields="xid_buyer,pin", order_state="", is_log=False):
        """
        :description: 检索单个SOP订单信息
        :param access_token: access_token
        :param order_id: 订单号，必填
        :param optional_fields: 需返回的字段列表，必填
        :param order_state: 订单状态，非必填
        :京东接口返回 {'jingdong_pop_order_get_responce':{'code':'0','orderDetailInfo':{'orderInfo':{'orderId':'281046817987','xid_buyer':'o*AAQ2VMNweFJXvq0fAvKFvwKXYWFlN21QRryiD7Ee-xKj1WWh0Xk3SvqnsOapoBq355aRCFpn','pin':'201027097-175237','sendpayMap':'{"9":"2","26":"2","29":"1","34":"3","39":"1","51":"6","62":"1","64":"3","173":"2","186":"1","190":"2","239":"2","342":"1"}','orderExt':'{"site":301,"businessOrderId":"281046817987","orderLevel":1,"isCancel":0,"orderCenterStatusName":"卡密提取中","modified":1695899555000,"sourceClient":2,"businessOrderStatus":16,"recycle":9,"jmiOrderStatus":4,"payStatus":1,"payType":1,"featureMap":{"imageUnit":{"imagePath":"jfs/t1/108850/20/44952/52675/64eb7963Fb435da18/1e8134f0d39cd51b.jpg","businessCode":"n0"},"rechargeType":1,"areaCode":99,"brandCode":693349,"quantity":1,"sendPay":125},"businessOrderStatusName":"正在充值","settleVenderId":13237223}','orderSource':'移动端订单','storeId':'0','storeOrder':'','realPin':'201027097-175237'},'apiResult':{'chineseErrCode':'成功','englishErrCode':'success','success':True,'numberCode':10100000}}}}
        :return {'orderId':'281046817987','xid_buyer':'o*AAQ2VMNweFJXvq0fAvKFvwKXYWFlN21QRryiD7Ee-xKj1WWh0Xk3SvqnsOapoBq355aRCFpn','pin':'201027097-175237','sendpayMap':'{"9":"2","26":"2","29":"1","34":"3","39":"1","51":"6","62":"1","64":"3","173":"2","186":"1","190":"2","239":"2","342":"1"}','orderExt':'{"site":301,"businessOrderId":"281046817987","orderLevel":1,"isCancel":0,"orderCenterStatusName":"卡密提取中","modified":1695899555000,"sourceClient":2,"businessOrderStatus":16,"recycle":9,"jmiOrderStatus":4,"payStatus":1,"payType":1,"featureMap":{"imageUnit":{"imagePath":"jfs/t1/108850/20/44952/52675/64eb7963Fb435da18/1e8134f0d39cd51b.jpg","businessCode":"n0"},"rechargeType":1,"areaCode":99,"brandCode":693349,"quantity":1,"sendPay":125},"businessOrderStatusName":"正在充值","settleVenderId":13237223}','orderSource':'移动端订单','storeId':'0','storeOrder':'','realPin':'201027097-175237'}
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = PopOrderGetRequest()
        req.order_state = order_state
        req.optional_fields = optional_fields
        req.order_id = order_id

        try:
            resp = req.getResponse(access_token)

            if is_log:
                log_info = "【req】：" + str(req.__dict__) + "【resp】：" + str(resp) + \
                           "【access_token】：" + access_token + "【检索单个SOP订单信息】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_pop_order_get_responce" in resp:
                api_result = resp['jingdong_pop_order_get_responce']['orderDetailInfo']['apiResult']
                if api_result == False:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = api_result['numberCode']
                    invoke_result_data.error_message = api_result['chineseErrCode']
                    return invoke_result_data
                if "orderInfo" in resp['jingdong_pop_order_get_responce']['orderDetailInfo']:
                    invoke_result_data.data = resp['jingdong_pop_order_get_responce']['orderDetailInfo']["orderInfo"]
                else:
                    invoke_result_data.data = {}
            return invoke_result_data
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "pop_order_get"
            invoke_result_data.error_message = "京东接口错误：检索单个SOP订单信息(jingdong.pop.order.get)"
            return invoke_result_data

    def batch_add_sku_add(self, access_token, vender_id, sku_list, effective_duration=180, is_log=False):
        """
        :description: 批量添加商品
        :param access_token: access_token
        :param vender_id: 商家唯一标识，必填
        :param sku_list: sku 列表，必填
            skuId: sku id
            skuName: sku 名称
        :param is_log: 是否记录日志
        :京东接口返回 {'jingdong_batchAddSku_add_responce':{'code':'0','ydResponse':{'requestId':'3d5282ec-bd2f-472b-907d-ab159c3278da','success':True,'result':{'code':200,'msg':'Success','data':{'status':1}}}}}
        :return {'status':1}
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = BatchAddSkuAddRequest()

        for sku_data in sku_list:
            sku_data["effectiveDuration"] = effective_duration  # 有效时长，非必填
            sku_data["timeUnit"] = 1  # 有效期单位，非必填，1-天，2-月，3-年
            # sku_data["deadline"] = "" # 有效截止日期，非必填，Long
            sku_data["effectiveMode"] = 1  # 生效模式, 必填，1-立即生效，2-指定日期生效
            # sku_data["effectiveTime"]= "" # 生效时间，非必填，Long
            sku_data["limitTimes"] = 1  # 核销次数限制，必填
            sku_data["businessType"] = 162  # 业务类型，必填

        data = sku_list

        req.data = JsonHelper.json_dumps(data)
        req.merchantCode = vender_id

        try:
            resp = req.getResponse(access_token)

            if is_log:
                log_info = "【req】：" + str(req.__dict__) + "【resp】：" + str(resp) + \
                           "【access_token】：" + access_token + "【批量添加商品】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_batchAddSku_add_responce" in resp:
                if resp['jingdong_batchAddSku_add_responce']['ydResponse']['success'] == False:
                    error = resp['jingdong_batchAddSku_add_responce']['ydResponse']['error']
                    invoke_result_data.success = False
                    invoke_result_data.error_code = error['code']
                    invoke_result_data.error_message = error['status']
                    return invoke_result_data
                else:
                    result = resp['jingdong_batchAddSku_add_responce']['ydResponse']['result']
                    if int(result['code']) != 200:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = result['code']
                        invoke_result_data.error_message = result['msg']
                        return invoke_result_data
                    else:
                        if int(result["data"]["status"]) != 1:
                            invoke_result_data.success = False
                            invoke_result_data.error_code = result['data']['status']
                            invoke_result_data.error_message = result['data']['errMsg']
                            return invoke_result_data
                        invoke_result_data.data = result["data"]

            return invoke_result_data
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "batch_add_sku"
            invoke_result_data.error_message = "京东接口错误：批量添加商品(jingdong.batchAddSku.add)"
            return invoke_result_data

    def order_operate(self, access_token, order_id, is_log=False):
        """
        :description: 订单放行
        :param access_token: access_token
        :param order_id: 订单号
        :param is_log: 是否记录日志
        :京东接口返回 {'jingdong_order_operate_responce':{'code':'0','ydResponse':{'requestId':'9d637c9f-b761-4200-89fa-f34da9b78286','success':True,'result':{'success':True,'canRetry':True,'code':'000000','message':'执行成功！','timestamp':0}}}}
        :return {'success': True, 'canRetry': True, 'code': '000000', 'message': '执行成功！', 'timestamp': 0}
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = OrderOperateRequest()

        data = {
            "orderId": order_id,
        }

        req.data = JsonHelper.json_dumps(data)

        try:
            resp = req.getResponse(access_token)

            if is_log:
                log_info = "【req】：" + str(req.__dict__) + "【resp】：" + str(resp) + \
                           "【access_token】：" + access_token + "【订单放行】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_order_operate_responce" in resp:
                if resp['jingdong_order_operate_responce']['ydResponse']['success'] == False:
                    error = resp['jingdong_batchAddSku_add_responce']['ydResponse']['error']
                    invoke_result_data.success = False
                    invoke_result_data.error_code = error['code']
                    invoke_result_data.error_message = error['status']
                    return invoke_result_data
                else:
                    result = resp['jingdong_order_operate_responce']['ydResponse']['result']
                    if result['success'] == False:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = result['code']
                        invoke_result_data.error_message = result['message']
                        return invoke_result_data
                    invoke_result_data.data = result

            return invoke_result_data
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "order_operate"
            invoke_result_data.error_message = "京东接口错误：订单放行(jingdong.order.operate)"
            return invoke_result_data

    def verify_save(self, access_token, vender_id, transaction_id, certList, is_log=False):
        """
        :description: 卡密核销
        :param access_token: access_token
        :param vender_id: 商家唯一标识，必填
        :transaction_id： 交易ID，必填，要保证唯一，跟锁卡密的transaction_id彼此独立的值
        :param certList: [{"cardNum":"","pwd":null,"verifyingTimes":1,"mobile":null}]
            cardNum: 卡号， 必填，需使用AES加密，CryptoHelper.aes_encrypt(card_num, "07afbc8bca08bc5139d36b3239ab3408")
            pwd: 密码，非必填，非空时需使用AES加密
            verifyingTimes: 核销次数，必填
            mobile: 手机号，非必填
        :param is_log: 是否记录日志
        :京东接口返回 {'jingdong_verify_save_responce': {'code': '0', 'YdResponse': {'requestId': '010229f7-1ca9-4be8-8f61-af21eb0d553d', 'success': True, 'result': {'code': 404, 'msg': '未查询到商家或结果不唯一'}}}}
        :京东接口返回 {'jingdong_verify_save_responce': {'code': '0', 'YdResponse': {'requestId': '80e860b9-557b-4d0b-9f63-f8b95b9f4bd6', 'success': True, 'result': {'code': 200, 'msg': 'Success', 'data': {'status': 1, 'errMsg': 'Success'}}}}}
        :return {'status': 1, 'errMsg': 'Success'}
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = VerifySaveRequest()
        aes_key1 = share_config.get_value("jd_config",{}).get("aes_key1","17f72a775ec0a96ad52b662206c7bceb")
        aes_key2 = share_config.get_value("jd_config",{}).get("aes_key2","07afbc8bca08bc5139d36b3239ab3408")
        for cert in certList:
            cert_num = CryptoHelper.aes_decrypt(cert["cardNum"], aes_key1)
            cert["cardNum"] = CryptoHelper.aes_encrypt(cert_num, aes_key2)
            pwd = CryptoHelper.aes_decrypt(cert["pwd"], aes_key1)
            cert["pwd"] = CryptoHelper.aes_encrypt(pwd, aes_key2)

        data = {
            "transactionId": transaction_id,
            "verifyingCertList": certList
        }

        req.data = JsonHelper.json_dumps(data)
        req.merchantCode = vender_id

        try:
            resp = req.getResponse(access_token)

            if is_log:
                log_info = "【req】：" + str(req.__dict__) + "【resp】：" + str(resp) + \
                           "【access_token】：" + access_token + "【卡密核销】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_verify_save_responce" in resp:
                if resp['jingdong_verify_save_responce']['ydResponse']['success'] == False:
                    error = resp['jingdong_verify_save_responce']['ydResponse']['error']
                    invoke_result_data.success = False
                    invoke_result_data.error_code = error['code']
                    invoke_result_data.error_message = error['status']
                    return invoke_result_data
                else:
                    result = resp['jingdong_verify_save_responce']['ydResponse']['result']
                    if int(result['code']) != 200:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = result['code']
                        invoke_result_data.error_message = result['msg']
                        return invoke_result_data
                    else:
                        if int(result["data"]["status"]) != 1:
                            invoke_result_data.success = False
                            invoke_result_data.error_code = result['data']['status']
                            invoke_result_data.error_message = result['data']['errMsg']
                            return invoke_result_data

                        invoke_result_data.data = result["data"]

            return invoke_result_data
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "verify_save"
            invoke_result_data.error_message = "京东接口错误：卡密核销(jingdong.verify.save)"
            return invoke_result_data
        
    def areas_province_get(self, is_log=False):
        """
        :description: 获取省级地址列表
        :param is_log: 是否记录日志
        :return
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = AreasProvinceGetRequest()

        try:
            resp = req.getResponse()

            if is_log:
                log_info = "【req】：" + str(req.__dict__) + "【resp】：" + str(resp) + "【获取省级地址列表】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_areas_province_get_responce" in resp:
                result = resp['jingdong_areas_province_get_responce']['baseAreaServiceResponse']
                if int(result['resultCode']) != 1:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = result['resultCode']
                    invoke_result_data.error_message = "失败"
                    return invoke_result_data

                invoke_result_data.data = result["data"]

            return invoke_result_data
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "areas_province_get"
            invoke_result_data.error_message = "京东接口错误：获取省级地址列表(jingdong.areas.province.get)"
            return invoke_result_data

    def areas_city_get(self, parent_id, is_log=False):
        """
        :description: 获取市级信息列表
        :param is_log: 是否记录日志
        :return
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = AreasCityGetRequest()
        req.parent_id = parent_id

        try:
            resp = req.getResponse()

            if is_log:
                log_info = "【req】：" + str(req.__dict__) + "【resp】：" + str(resp) + "【获取市级信息列表】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_areas_city_get_responce" in resp:
                result = resp['jingdong_areas_city_get_responce']['baseAreaServiceResponse']
                if int(result['resultCode']) != 1:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = result['resultCode']
                    invoke_result_data.error_message = "失败"
                    return invoke_result_data

                invoke_result_data.data = result["data"]

            return invoke_result_data
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "areas_city_get"
            invoke_result_data.error_message = "京东接口错误：获取市级信息列表(jingdong.areas.city.get)"
            return invoke_result_data

    def areas_county_get(self, parent_id, is_log=False):
        """
        :description: 获取区县级信息列表
        :param is_log: 是否记录日志
        :return
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = AreasCountyGetRequest()
        req.parent_id = parent_id

        try:
            resp = req.getResponse()

            if is_log:
                log_info = "【req】：" + str(req.__dict__) + "【resp】：" + str(resp) + "【获取区县级信息列表】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_areas_county_get_responce" in resp:
                result = resp['jingdong_areas_county_get_responce']['baseAreaServiceResponse']
                if int(result['resultCode']) != 1:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = result['resultCode']
                    invoke_result_data.error_message = "失败"
                    return invoke_result_data

                invoke_result_data.data = result["data"]

            return invoke_result_data
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "areas_county_get"
            invoke_result_data.error_message = "京东接口错误：获取区县级信息列表(jingdong.areas.county.get)"
            return invoke_result_data

    def areas_town_get(self, parent_id, is_log=False):
        """
        :description: 获取乡镇级信息列表
        :param is_log: 是否记录日志
        :return
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = AreasTownGetRequest()
        req.parent_id = parent_id

        try:
            resp = req.getResponse()

            if is_log:
                log_info = "【req】：" + str(req.__dict__) + "【resp】：" + str(resp) + "【获取乡镇级信息列表】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_areas_town_get_responce" in resp:
                result = resp['jingdong_areas_town_get_responce']['baseAreaServiceResponse']
                if int(result['resultCode']) != 1:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = result['resultCode']
                    invoke_result_data.error_message = "失败"
                    return invoke_result_data

                invoke_result_data.data = result["data"]

            return invoke_result_data
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "areas_town_get"
            invoke_result_data.error_message = "京东接口错误：获取乡镇级信息列表(jingdong.areas.town.get)"
            return invoke_result_data

    def order_cancel(self, access_token, business_data_id, cancel_reason_type, erp_order_id, is_log=False):
        """
        :description: 代下单取消，状态变更要等10分钟
        :param access_token: access_token
        :param business_data_id: 业务数据ID
        :param cancel_reason_type: 取消原因，610: 不想买了，611: 其他原因，612: 操作有误（商品、地址等选错），613: 商品无货
        :param erp_order_id: erp订单号
        :param is_log: 是否记录日志
        :京东接口返回 {'jingdong_order_cancel_responce': {'code': '0', 'ydResponse': {'requestId': '74e98e59-4bf7-4e02-b955-5fae7252e44b', 'success': True, 'result': {'success': True, 'errCode': 200, 'errMsg': '成功'}}}}
        :return {}
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = OrderCancelRequest()

        data = {
            "businessDataId": business_data_id,
            "cancelReasonType": cancel_reason_type,
            "erpOrderId": erp_order_id
        }

        req.data = SevenHelper.json_dumps(data)

        try:
            resp = req.getResponse(access_token)
            if is_log:
                log_info = "【req】：" + str(req.__dict__) + "【resp】：" + str(resp) + \
                           "【access_token】：" + access_token + "【代下单取消】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_order_cancel_responce" in resp:
                if resp['jingdong_order_cancel_responce']['ydResponse']['success'] == False:
                    error = resp['jingdong_order_cancel_responce']['ydResponse']['error']
                    invoke_result_data.success = False
                    invoke_result_data.error_code = error['code']
                    invoke_result_data.error_message = error['status']
                    return invoke_result_data
                else:
                    result = resp['jingdong_order_cancel_responce']['ydResponse']['result']
                    if result['success'] == False:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = result["errCode"]
                        invoke_result_data.error_message = result["errMsg"]
                        return invoke_result_data
                    else:
                        if int(result["errCode"]) != 200:
                            invoke_result_data.success = False
                            invoke_result_data.error_code = result["errCode"]
                            invoke_result_data.error_message = result["errMsg"]
                            return invoke_result_data
                        else:
                            invoke_result_data.data = {}

            return invoke_result_data
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "order_cancel"
            invoke_result_data.error_message = "京东接口错误：代下单取消(jingdong.order.cancel)"
            return invoke_result_data

    def apply_repeal_save(self, access_token, vender_id, transaction_id, card_num_list, sku_id, is_log=False, is_test=False):
        """
        :description: 卡密作废
        :param access_token: access_token
        :param transaction_id： 业务唯一标识
        :param card_num_list: 卡号列表，最多50条
        :param sku_id: sku编号
        :param is_log: 是否记录日志
        :param is_test: 是否京东测试环境
        :京东接口返回 {'jingdong_applyRepeal_save_responce': {'code': '0', 'ydResponse': {'requestId': 'ac8b0bc8-38d0-4be2-bc00-911f06aa2d84', 'success': True, 'result': {'code': 200, 'msg': 'Success', 'data': {'status': 1}}}}}
        :京东接口返回 {'jingdong_applyRepeal_save_responce': {'code': '0', 'ydResponse': {'requestId': 'e3589da6-272e-4c12-af51-821060b16bec', 'success': True, 'result': {'code': 200, 'msg': 'Success', 'data': {'status': 3, 'errMsg': {'1942795943': '凭证状态错误，不允许作废'}}}}}}
        :return {'status': 1}
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = ApplyRepealSaveRequest() if is_test == False else ApplyRepealSaveRequest(domain="api-dev.jd.com")
        aes_key1 = share_config.get_value("jd_config",{}).get("aes_key1","17f72a775ec0a96ad52b662206c7bceb")
        new_list = []
        for cert in card_num_list:
            cert = CryptoHelper.aes_decrypt(cert, aes_key1)
            new_list.append(cert)

        data = {
            "transactionId": transaction_id,
            "operationWay": 2,  # 操作方式（1、按批，2、按卡券），目前只支持按卡券
            "cardNumList": new_list,
            "skuId": sku_id
        }

        req.data = JsonHelper.json_dumps(data)
        req.merchantCode = vender_id

        try:
            resp = req.getResponse(access_token) if is_test == False else req.getResponse(access_token, ssl=True)
            if is_log:
                log_info = "【req】：" + str(req.__dict__) + "【resp】：" + str(resp) + \
                           "【access_token】：" + access_token + "【卡密作废】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_applyRepeal_save_responce" in resp:
                if resp['jingdong_applyRepeal_save_responce']['ydResponse']['success'] == False:
                    error = resp['jingdong_applyRepeal_save_responce']['ydResponse']['error']
                    invoke_result_data.success = False
                    invoke_result_data.error_code = error['code']
                    invoke_result_data.error_message = error['status']
                    return invoke_result_data
                else:
                    result = resp['jingdong_applyRepeal_save_responce']['ydResponse']['result']
                    if int(result['code']) != 200:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = result['code']
                        invoke_result_data.error_message = result['msg']
                        return invoke_result_data
                    else:
                        invoke_result_data.data = result["data"]

            return invoke_result_data
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "apply_repeal_save"
            invoke_result_data.error_message = "京东接口错误：卡密作废(jingdong.applyRepeal.save)"
            return invoke_result_data

    def cert_list_query(self, access_token, page_num, page_size, vender_id, card_num_list, is_log=False, is_test=False):
        """
        :description: 凭证信息查询
        :param access_token: access_token
        :param page_num：页数，从1开始
        :param page_size：条数
        :param vender_id: 商家编号
        :param card_num_list: 卡号列表，最多50条
        :param is_log: 是否记录日志
        :param is_test: 是否京东测试环境
        :京东接口返回 {'jingdong_certList_query_responce':{'code':'0','ydResponse':{'requestId':'1214f40c-2193-4ca6-a03c-5c8561e851c9','success':True,'result':{'code':200,'msg':'Success','data':{'pageNum':1,'pageSize':10,'total':1,'pages':1,'startRow':1,'endRow':1,'list':[{'merchantCardId':'14414000000001173678405107863552','merchantCode':'144140','businessType':162,'cardNum':'4t+nEP9DGBboaIk5ougkkw==','cardPwd':'6kHSL6urRrs8RJQYMmvYlg==','erpOrderId':283715797911,'skuId':10089809110197,'skuName':'万代【一番赏测试】次数01','invalidStatus':2,'expiredStatus':1,'verifiedStatus':1,'reserveStatus':1,'certType':1,'limitTimes':1,'verifiedTimes':0,'providedTime':'2023-11-13T09:38:57.000+0000','effectiveTime':'2023-11-13T09:38:57.000+0000','invalidTime':'2023-11-13T10:40:48.000+0000','expiredTime':'2024-05-11T15:59:59.000+0000','multiCertType':1,'cardPwdType':1,'ext':'{"url":"c:1942795943;p:538098;"}','leftVerifyTime':1}],'prePage':0,'nextPage':0,'hasPreviousPage':False,'hasNextPage':False,'navigatePages':8,'navigatepageNums':[1],'navigateFirstPage':1,'navigateLastPage':1,'showPage':True,'firstPage':True,'lastPage':True}}}}}
        :return {'pageNum':1,'pageSize':10,'total':1,'pages':1,'startRow':1,'endRow':1,'list':[{'merchantCardId':'14414000000001173678405107863552','merchantCode':'144140','businessType':162,'cardNum':'fvKJ2b/a2BtcGBMg7pWRcQ==','cardPwd':'e2yog83ocTAKPBAaHPhgaw==','erpOrderId':283715797911,'skuId':10089809110197,'skuName':'万代【一番赏测试】次数01','invalidStatus':2,'expiredStatus':1,'verifiedStatus':1,'reserveStatus':1,'certType':1,'limitTimes':1,'verifiedTimes':0,'providedTime':'2023-11-13T09:38:57.000+0000','effectiveTime':'2023-11-13T09:38:57.000+0000','invalidTime':'2023-11-13T10:40:48.000+0000','expiredTime':'2024-05-11T15:59:59.000+0000','multiCertType':1,'cardPwdType':1,'ext':'{"url":"c:1942795943;p:538098;"}','leftVerifyTime':1}],'prePage':0,'nextPage':0,'hasPreviousPage':False,'hasNextPage':False,'navigatePages':8,'navigatepageNums':[1],'navigateFirstPage':1,'navigateLastPage':1,'showPage':True,'firstPage':True,'lastPage':True}
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = CertListQueryRequest() if is_test == False else CertListQueryRequest(domain="api-dev.jd.com")
        aes_key1 = share_config.get_value("jd_config",{}).get("aes_key1","17f72a775ec0a96ad52b662206c7bceb")
        new_list = []
        for cert in card_num_list:
            cert = CryptoHelper.aes_decrypt(cert, aes_key1)
            new_list.append(cert)

        data = {
            "pageNum": page_num,
            "pageSize": page_size,
            "data": {
                "merchantCode": vender_id,
                "businessType": 162,  # 业务类型，必填
                "cardNumList": new_list
            }
        }

        req.data = JsonHelper.json_dumps(data)
        req.merchantCode = vender_id

        try:
            resp = req.getResponse(access_token) if is_test == False else req.getResponse(access_token, ssl=True)

            if is_log:
                log_info = "【req】：" + str(req.__dict__) + "【resp】：" + str(resp) + \
                           "【access_token】：" + access_token + "【凭证信息查询】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_certList_query_responce" in resp:
                if resp['jingdong_certList_query_responce']['ydResponse']['success'] == False:
                    error = resp['jingdong_applyRepeal_save_responce']['ydResponse']['error']
                    invoke_result_data.success = False
                    invoke_result_data.error_code = error['code']
                    invoke_result_data.error_message = error['status']
                    return invoke_result_data
                else:
                    result = resp['jingdong_certList_query_responce']['ydResponse']['result']
                    if int(result['code']) != 200:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = result['code']
                        invoke_result_data.error_message = result['msg']
                        return invoke_result_data
                    else:
                        data = result["data"]
                        if data["list"]:
                            aes_key2 = share_config.get_value("jd_config",{}).get("aes_key2","07afbc8bca08bc5139d36b3239ab3408")
                            aes_key1 = share_config.get_value("jd_config",{}).get("aes_key1","17f72a775ec0a96ad52b662206c7bceb")
                            for item in data["list"]:
                                item["cardNum"] = CryptoHelper.aes_decrypt(item["cardNum"], aes_key2)
                                item["cardNum"] = CryptoHelper.aes_encrypt(item["cardNum"], aes_key1)
                                item["cardPwd"] = CryptoHelper.aes_decrypt(item["cardPwd"], aes_key2)
                                item["cardPwd"] = CryptoHelper.aes_encrypt(item["cardPwd"], aes_key1)
                        invoke_result_data.data = data

            return invoke_result_data
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "cert_list_query"
            invoke_result_data.error_message = "京东接口错误：凭证信息查询(jingdong.certList.query)"
            return invoke_result_data
        
    def preview_save(self, access_token, vender_id, cert_num, pwd, is_log=False):
        """
        :description: 卡密预核销
        :param access_token: access_token
        :param vender_id: 商家唯一标识，必填
        :param cert_num： 凭证卡号，必填
        :param pwd: 凭证密码，必填
        :param is_log: 是否记录日志
        :京东接口返回 {'jingdong_preview_save_responce': {'code': '0', 'ydResponse': {'result': {'msg': 'Success', 'code': 200, 'data': {'merchantCode': 'AAS1UanKBUa3lLivtMkpxKjo7ymwTjweiEnhD/KP27MG4c1oMXpetfXTpr47DOOZL3U=', 'effectiveTime': '2023-11-07T01:32:56.000+0000', 'lastVerifiedTime': '2023-11-07T01:37:51.000+0000', 'verified': True, 'leftTimes': 0, 'invalidTime': '2023-11-07T01:37:51.000+0000', 'expiredTime': '2024-05-05T15:59:59.000+0000', 'skuName': '万代【一番赏测试】次数01', 'providedTime': '2023-11-07T01:32:56.000+0000', 'encrypt_orderId': 'AAS1UanKBUa3lLivtMkpxKjomCb8583VWheLxpyGIhYjW0w03k5njlpjqG9GksGxVWE=', 'reserved': False, 'realLeftTimes': 0, 'businessType': 162, 'skuId': 'AAS1UanKBUa3lLivtMkpxKjoYDdHrmSoGfyBTFrSx0e8HXriJZhXwYY3jkby2eDBkGA='}}, 'requestId': '5a1f112b-4f9d-407a-a115-0d378535db94', 'success': True}}}
        :return {'merchantCode': 'AAS1UanKBUa3lLivtMkpxKjo7ymwTjweiEnhD/KP27MG4c1oMXpetfXTpr47DOOZL3U=', 'effectiveTime': '2023-11-07T01:32:56.000+0000', 'lastVerifiedTime': '2023-11-07T01:37:51.000+0000', 'verified': True, 'leftTimes': 0, 'invalidTime': '2023-11-07T01:37:51.000+0000', 'expiredTime': '2024-05-05T15:59:59.000+0000', 'skuName': '万代【一番赏测试】次数01', 'providedTime': '2023-11-07T01:32:56.000+0000', 'encrypt_orderId': 'AAS1UanKBUa3lLivtMkpxKjomCb8583VWheLxpyGIhYjW0w03k5njlpjqG9GksGxVWE=', 'reserved': False, 'realLeftTimes': 0, 'businessType': 162, 'skuId': 'AAS1UanKBUa3lLivtMkpxKjoYDdHrmSoGfyBTFrSx0e8HXriJZhXwYY3jkby2eDBkGA='}
        :last_editors: SunYiTan
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = PreviewSaveRequest()

        cert_num = CryptoHelper.aes_decrypt(cert_num, "17f72a775ec0a96ad52b662206c7bceb")
        cert_num = CryptoHelper.aes_encrypt(cert_num, "07afbc8bca08bc5139d36b3239ab3408")
        pwd = CryptoHelper.aes_decrypt(pwd, "17f72a775ec0a96ad52b662206c7bceb")
        pwd = CryptoHelper.aes_encrypt(pwd, "07afbc8bca08bc5139d36b3239ab3408")

        data = {
            "cardNum": cert_num,
            "pwd": pwd
        }

        req.data = JsonHelper.json_dumps(data)
        req.merchantCode = vender_id

        try:
            resp = req.getResponse(access_token)

            if is_log:
                log_info = "【req】：" + str(req.__dict__) + "【resp】：" + str(resp) + \
                           "【access_token】：" + access_token + "【卡密预核销】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_preview_save_responce" in resp:
                if resp['jingdong_preview_save_responce']['ydResponse']['success'] == False:
                    error = resp['jingdong_preview_save_responce']['ydResponse']['error']
                    invoke_result_data.success = False
                    invoke_result_data.error_code = error['code']
                    invoke_result_data.error_message = error['status']
                    return invoke_result_data
                else:
                    result = resp['jingdong_preview_save_responce']['ydResponse']['result']
                    if int(result['code']) != 200:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = result['code']
                        invoke_result_data.error_message = result['msg']
                        return invoke_result_data
                    else:
                        invoke_result_data.data = result["data"]

            return invoke_result_data
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "preview_save"
            invoke_result_data.error_message = "京东接口错误：卡密预核销(jingdong.preview.save)"
            return invoke_result_data

    def cert_unlock(self, access_token, vender_id, transaction_id, certList, is_log=False, is_test=False):
        """
        :description: 卡密解锁
        :param access_token: access_token
        :param vender_id: 商家唯一标识，必填
        :transaction_id： 交易ID，必填，做幂等
        :param certList: [{"cardNum":"","pwd":null,"verifyingTimes":null,"mobile":null}]
            cardNum: 卡号， 必填，需使用AES加密，CryptoHelper.aes_encrypt(card_num, "07afbc8bca08bc5139d36b3239ab3408")
            pwd: 密码，非必填，非空时需使用AES加密
            verifyingTimes: 核销次数，非必填
            mobile: 手机号，非必填
        :param is_log: 是否记录日志
        :param is_test: 是否京东测试环境
        :京东接口返回 {'jingdong_cert_unlock_responce': {'code': '0', 'ydResponse': {'requestId': '87b2ba6e-0b2d-45c2-a301-d5cfe13c5c47', 'success': True, 'result': {'code': 200, 'msg': 'Success', 'data': {'status': 1, 'errMsg': 'Success'}}}}}
        :return {'status': 1, 'errMsg': 'Success'}
        :last_editors: SunYiTan
        """
        invoke_result_data = InvokeResultData()

        jd.setDefaultAppInfo(self.app_key, self.app_secret)
        req = CertUnlockRequest() if is_test == False else CertUnlockRequest(domain="api-dev.jd.com")
        aes_key1 = share_config.get_value("jd_config",{}).get("aes_key1","17f72a775ec0a96ad52b662206c7bceb")
        aes_key2 = share_config.get_value("jd_config",{}).get("aes_key2","07afbc8bca08bc5139d36b3239ab3408")
        for cert in certList:
            cert_num = CryptoHelper.aes_decrypt(cert["cardNum"], aes_key1)
            cert["cardNum"] = CryptoHelper.aes_encrypt(cert_num, aes_key2)
            pwd = CryptoHelper.aes_decrypt(cert["pwd"], aes_key1)
            cert["pwd"] = CryptoHelper.aes_encrypt(pwd, aes_key2)

        data = {
            "transactionId": transaction_id,
            "certList": certList
        }

        req.data = JsonHelper.json_dumps(data)
        req.merchantCode = vender_id

        print(str(req.__dict__))

        try:
            resp = req.getResponse(access_token) if is_test == False else req.getResponse(access_token, ssl=True)

            if is_log:
                log_info = "【req】：" + str(req.__dict__) + "【resp】：" + str(resp) + \
                           "【access_token】：" + access_token + "【卡密解锁】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)

            if "error_response" in resp:
                invoke_result_data.success = False
                invoke_result_data.error_code = resp['error_response']['code']
                invoke_result_data.error_message = resp['error_response']['zh_desc']
                return invoke_result_data

            if "jingdong_cert_unlock_responce" in resp:
                if resp['jingdong_cert_unlock_responce']['ydResponse']['success'] == False:
                    error = resp['jingdong_cert_unlock_responce']['ydResponse']['error']
                    invoke_result_data.success = False
                    invoke_result_data.error_code = error['code']
                    invoke_result_data.error_message = error['status']
                    return invoke_result_data
                else:
                    result = resp['jingdong_cert_unlock_responce']['ydResponse']['result']
                    if int(result['code']) != 200:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = result['code']
                        invoke_result_data.error_message = result['msg']
                        return invoke_result_data
                    else:
                        if int(result["data"]["status"]) != 1:
                            invoke_result_data.success = False
                            invoke_result_data.error_code = result['data']['status']
                            invoke_result_data.error_message = result['data']['errMsg']
                            return invoke_result_data

                        invoke_result_data.data = result["data"]

            return invoke_result_data
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "cert_unlock"
            invoke_result_data.error_message = "京东接口错误：卡密解锁(jingdong.cert.unlock)"
            return invoke_result_data