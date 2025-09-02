# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-19 09:23:14
@LastEditTime: 2025-01-26 10:12:37
@LastEditors: HuangJianYi
@Description: 
"""
from time import *
from requests_pkcs12 import post
import requests
from Crypto.Cipher import AES
import base64
import xmltodict
from xml.etree import ElementTree
import xml.etree.ElementTree as ET
from urllib.parse import quote
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import string
from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_framework.base_model import *
from seven_cloudapp_frame.models.seven_model import InvokeResultData


class WeChatHelper:
    """
    :description: 微信帮助类 1.临时登录凭证校验获取open_id、session_key  2.解析加密数据
    """
    logger_error = Logger.get_logger_by_name("log_error")


    @classmethod
    def get_web_authorize_url(self, redirect_uri, scope="snsapi_userinfo", app_id="", state="1"):
        """
        :description:获取网页授权链接, 注意：公众号必须是服务号并认证才可以使用网页授权
        :param redirect_uri：授权后重定向的回调地址
        :param scope：应用授权作用域，snsapi_base （不弹出授权页面，直接跳转，只能获取用户openid），snsapi_userinfo （弹出授权页面，可通过openid拿到昵称、性别、所在地。并且，即使在未关注的情况下，只要用户授权，也能获取其信息）
        :param app_id：公众号的唯一标识
        :param state：重定向后会带上state参数，开发者可以填写a-zA-Z0-9的参数值，最多128字节
        :return: 返回网页授权链接
        :last_editors: HuangJianYi
        """
        app_id = app_id if app_id else share_config.get_value("app_id")
        authorize_url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid={0}&redirect_uri={1}&response_type=code&scope={2}&state={3}&connect_redirect=1#wechat_redirect".format(app_id, CodingHelper.url_encode(redirect_uri), scope, CodingHelper.url_encode(state))
        return authorize_url

    @classmethod
    def get_web_authorize_userinfo(self, code, grant_type="authorization_code", app_id="", app_secret=""):
        """
        :description:获取网页授权用户信息
        :param code：登录票据
        :param grant_type：授权方式
        :param app_id：公众号的唯一标识
        :param app_secret：公众号的appsecret
        :return: 返回用户信息{ "openid": "OPENID","nickname": NICKNAME,"sex": 1,"province":"PROVINCE","city":"CITY","country":"COUNTRY","headimgurl":"https://thirdwx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/46","privilege":[ "PRIVILEGE1" "PRIVILEGE2"],"unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"}
        :last_editors: HuangJianYi
        """
        app_id = app_id if app_id else share_config.get_value("app_id")
        app_secret = app_secret if app_secret else share_config.get_value("app_secret")
        invoke_result_data = InvokeResultData()
        param = {
            'code': code,  # 用户点击按钮跳转到微信授权页, 微信处理完后重定向到redirect_uri, 并给我们加上code=xxx的参数, 这个code就是我们需要的
            'appid': app_id,
            'secret': app_secret,
            'grant_type': grant_type,
        }

        # 通过code获取access_token
        requset_url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
        response = None
        try:
            response = requests.get(requset_url, params=param)
            response_data = SevenHelper.json_loads(response.text)
            if response_data.__contains__("errcode") and response_data["errcode"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["errcode"]
                invoke_result_data.error_message = response_data["errmsg"]
                return invoke_result_data
            open_id = response_data['openid']
            access_token = response_data['access_token']
            requset_url = "https://api.weixin.qq.com/sns/userinfo"
            response = requests.get(requset_url, params={'access_token': access_token, 'openid': open_id, 'lang': "zh_CN"})
            response_data = SevenHelper.json_loads(response.text)
            if response_data.__contains__("errcode") and response_data["errcode"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["errcode"]
                invoke_result_data.error_message = response_data["errmsg"]
                return invoke_result_data
            invoke_result_data.data = response_data
            if invoke_result_data.data.__contains__("nickname"):
                invoke_result_data.data["nickname"] = invoke_result_data.data["nickname"].encode('ISO-8859-1').decode('utf-8')
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【get_web_authorize_userinfo】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    @classmethod
    def get_jsapi_ticket(self, app_id=""):
        """
        :description:获取jsapi_ticket,注意：需在公众号后台添加ip白名单，控制台去请求微信接口获取
        :param app_id:app_id
        :return: 返回ticket
        :last_editors: HuangJianYi
        """
        app_id = app_id if app_id else share_config.get_value("app_id")

        invoke_result_data = InvokeResultData()
        try:
            redis_key = f"wechat_jsapi_ticket:{str(app_id)}"
            redis_init = SevenHelper.redis_init(config_dict=share_config.get_value("platform_redis"))
            jsapi_ticket = redis_init.get(redis_key)
            if not jsapi_ticket:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "jsapi_ticket不存在"
                return invoke_result_data
            invoke_result_data.data = jsapi_ticket
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【get_jsapi_ticket】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    @classmethod
    def set_jsapi_ticket(self, app_id="", app_secret="", is_del=False):
        """
        :description:获取jsapi_ticket
        :param app_id:app_id
        :param app_secret:app_secret
        :param is_del:是否删除redis里的ticket
        :return: 返回ticket
        :last_editors: HuangJianYi
        """
        app_id = app_id if app_id else share_config.get_value("app_id")
        app_secret = app_secret if app_secret else share_config.get_value("app_secret")

        invoke_result_data = InvokeResultData()
        for i in range(2):
            if i == 0:
                invoke_result_data = self.get_access_token(app_id, app_secret)
            else:
                invoke_result_data = self.get_access_token(app_id, app_secret, True)

            if invoke_result_data.success == True:
                break
        if invoke_result_data.success == False:
            return invoke_result_data
        access_token = invoke_result_data.data

        try:
            response = None
            redis_key = f"wechat_jsapi_ticket:{str(app_id)}"
            redis_init = SevenHelper.redis_init(config_dict=share_config.get_value("platform_redis"))
            if is_del == True:
                redis_init.delete(redis_key)
            requset_url = f"https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={access_token}&type=jsapi"
            response = requests.get(requset_url)
            response_data = SevenHelper.json_loads(response.text)
            if response_data.__contains__("errcode") and response_data["errcode"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["errcode"]
                invoke_result_data.error_message = response_data["errmsg"]
                return invoke_result_data
            invoke_result_data.data = str(response_data["ticket"])
            redis_init.set(redis_key, invoke_result_data.data, ex=3600)
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【set_jsapi_ticket】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    @classmethod
    def get_share_sign_package(self, request_url, app_id=""):
        """
        :description:获取分享请求参数
        :param request_url:请求地址 如果是服务端获取地址则使用 request_url = self.request.headers['Referer']
        :param app_id:app_id
        :return: 返回分享请求参数
        :last_editors: HuangJianYi
        """
        app_id = app_id if app_id else share_config.get_value("app_id")

        invoke_result_data = InvokeResultData()
        request_url = request_url.split('#')[0]
        timestamp = int(time.time())
        invoke_result_data = self.get_jsapi_ticket(app_id)
        if invoke_result_data.success == False:
            return invoke_result_data
        js_ticket = invoke_result_data.data
        noncestr = self.get_nonce_str()
        param = {'noncestr': noncestr, 'jsapi_ticket': js_ticket, 'timestamp': timestamp, 'url': request_url}
        string_sign_temp = self.key_value_url(param, False)
        sign = hashlib.sha1(string_sign_temp.encode("utf8")).hexdigest()
        sign_package = {'appid': app_id, 'noncestr': noncestr, 'timestamp': timestamp, 'url': request_url, 'signature': sign}
        invoke_result_data.data = sign_package
        return invoke_result_data


    @classmethod
    def code2_session(self, code, grant_type="authorization_code", app_id="", app_secret=""):
        """
        :description:小程序临时登录凭证校验
        :param code：登录票据
        :param grant_type：授权方式
        :param app_id：app_id
        :param app_secret：app_secret
        :return: 返回字典包含字段 session_key,openid
        :last_editors: HuangJianYi
        """
        app_id = app_id if app_id else share_config.get_value("app_id")
        app_secret = app_secret if app_secret else share_config.get_value("app_secret")
        invoke_result_data = InvokeResultData()
        redis_key = f"{app_id}_wechat_login_code:{str(code)}"
        redis_init = SevenHelper.redis_init(config_dict=share_config.get_value("platform_redis"))
        code2_session_dict = redis_init.get(redis_key)
        if code2_session_dict:
            code2_session_dict = SevenHelper.json_loads(code2_session_dict)
            invoke_result_data.data = code2_session_dict
            return invoke_result_data
        param = {
            'js_code': code,  # 用户点击按钮跳转到微信授权页, 微信处理完后重定向到redirect_uri, 并给我们加上code=xxx的参数, 这个code就是我们需要的
            'appid': app_id,
            'secret': app_secret,
            'grant_type': grant_type,
        }

        # 通过code获取sessionkey
        requset_url = 'https://api.weixin.qq.com/sns/jscode2session'
        response = None
        try:
            response = requests.get(requset_url, params=param)
            response_data = SevenHelper.json_loads(response.text)
            if response_data.__contains__("errcode") and response_data["errcode"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["errcode"]
                invoke_result_data.error_message = response_data["errmsg"]
                return invoke_result_data
            open_id = response_data['openid']
            session_key = response_data['session_key']
            redis_init.set(redis_key, SevenHelper.json_dumps(response_data), ex=60 * 60)
            redis_init.set(f"{app_id}_wechat_sessionkey:{open_id}", session_key, ex=60 * 60)
            invoke_result_data.data = response_data
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【code2_session】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    @classmethod
    def get_access_token(self, app_id="", app_secret="", is_del=False, grant_type="client_credential", from_wechat_get = True):
        """
        :description:access_token 是微信的全局唯一调用凭据，开发者调用小程序支付时需要使用 access_token。access_token 的有效期为 2 个小时，需要定时刷新 access_token，重复获取会导致之前一次获取的 access_token 的有效期缩短为 5 分钟。建议开发者使用中控服务器统一获取和刷新 access_token，其他业务逻辑服务器所使用的 access_token 均来自于该中控服务器，不应该各自去刷新，否则容易造成冲突，导致 access_token 覆盖而影响业务；
        :description:注意：如果是公众号开发，需在公众号后台添加ip白名单，控制台去请求微信接口获取，小程序不用
        :param app_id:app_id
        :param app_secret:app_secret
        :param is_del:是否删除redis里的access_token
        :param grant_type: 获取access_token 时值为 client_credential
        :param from_wechat_get: 是否请求微信接口获取access_token并存到redis
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = app_id if app_id else share_config.get_value("app_id")
        app_secret = app_secret if app_secret else share_config.get_value("app_secret")

        invoke_result_data = InvokeResultData()

        try:
            redis_key = f"wechat_access_token:{str(app_id)}"
            redis_init = SevenHelper.redis_init(config_dict=share_config.get_value("platform_redis"))
            if is_del == True:
                redis_init.delete(redis_key)
            access_token = redis_init.get(redis_key)
            if access_token:
                invoke_result_data.data = access_token
                return invoke_result_data
            if from_wechat_get == True:
                invoke_result_data = self.set_access_token(app_id, app_secret, is_del, grant_type)
                if invoke_result_data.success == False:
                    return invoke_result_data
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【get_access_token】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    @classmethod
    def set_access_token(self, app_id="", app_secret="", is_del=False, grant_type="client_credential"):
        """
        :description:access_token 是微信的全局唯一调用凭据，开发者调用小程序支付时需要使用 access_token。access_token 的有效期为 2 个小时，需要定时刷新 access_token，重复获取会导致之前一次获取的 access_token 的有效期缩短为 5 分钟。建议开发者使用中控服务器统一获取和刷新 access_token，其他业务逻辑服务器所使用的 access_token 均来自于该中控服务器，不应该各自去刷新，否则容易造成冲突，导致 access_token 覆盖而影响业务；
        :param app_id:app_id
        :param app_secret:app_secret
        :param is_del:是否删除redis里的access_token
        :param grant_type: 获取access_token 时值为 client_credential
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = app_id if app_id else share_config.get_value("app_id")
        app_secret = app_secret if app_secret else share_config.get_value("app_secret")

        invoke_result_data = InvokeResultData()
        param = {
            'appid': app_id,
            'secret': app_secret,
            'grant_type': grant_type,
        }

        try:
            response = None
            redis_key = f"wechat_access_token:{str(app_id)}"
            redis_init = SevenHelper.redis_init(config_dict=share_config.get_value("platform_redis"))
            if is_del == True:
                redis_init.delete(redis_key)
            requset_url = 'https://api.weixin.qq.com/cgi-bin/token'
            response = requests.get(requset_url, params=param)
            response_data = SevenHelper.json_loads(response.text)
            if response_data.__contains__("errcode") and response_data["errcode"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["errcode"]
                invoke_result_data.error_message = response_data["errmsg"]
                return invoke_result_data
            invoke_result_data.data = str(response_data["access_token"])
            redis_init.set(redis_key, invoke_result_data.data, ex=3600)
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【set_access_token】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    @classmethod
    def send_template_message(self, open_id, template_id, page, request_data, miniprogram_state="formal", lang="zh_CN", app_id="", app_secret=""):
        """
        :description:发送订阅消息（https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/subscribe-message/subscribeMessage.send.html）
        :param open_id:接收者（用户）的 openid
        :param template_id:所需下发的订阅模板id
        :param page:点击模板卡片后的跳转页面，仅限本小程序内的页面。支持带参数,（示例index?foo=bar）。该字段不填则模板无跳转
        :param request_data:模板内容，格式形如 { “date2”: { “value”: any }, “thing3”: { “value”: any } }
        :param miniprogram_state:跳转小程序类型：developer为开发版；trial为体验版；formal为正式版；默认为正式版
        :param lang:进入小程序查看”的语言类型，支持zh_CN(简体中文)、en_US(英文)、zh_HK(繁体中文)、zh_TW(繁体中文)，默认为zh_CN
        :param app_id:app_id
        :param app_secret:app_secret
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = app_id if app_id else share_config.get_value("app_id")
        app_secret = app_secret if app_secret else share_config.get_value("app_secret")
        invoke_result_data = InvokeResultData()
        for i in range(2):
            if i == 0:
                invoke_result_data = self.get_access_token(app_id, app_secret)
            else:
                invoke_result_data = self.get_access_token(app_id, app_secret, True)

            if invoke_result_data.success == True:
                break
        if invoke_result_data.success == False:
            return invoke_result_data
        access_token = invoke_result_data.data
        try:
            requset_url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=' + access_token
            param = {"touser": open_id, "page": page, "lang": lang, "data": request_data, "template_id": template_id, "miniprogram_state": miniprogram_state}
            response = requests.post(requset_url, data=json.dumps(param, ensure_ascii=False).encode('utf-8'), headers={'Content-Type': 'application/json'})
            response_data = SevenHelper.json_loads(response.text)
            if response_data.__contains__("errcode") and response_data["errcode"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["errcode"]
                invoke_result_data.error_message = response_data["errmsg"]
                return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【发送订阅消息】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data
        return invoke_result_data

    @classmethod
    def get_user_phonenumber(self, code, app_id="", app_secret=""):
        """
        :description:code换取用户手机号。 每个code只能使用一次，code的有效期为5min
        :param code: 手机号获取凭证
        :param app_id:app_id
        :param app_secret:app_secret
        :return: InvokeResultData data里是个对象 {'phoneNumber': '15059331111', 'purePhoneNumber': '15059331111', 'countryCode': '86', 'watermark': {'timestamp': 1681202041, 'appid': 'wx7b10fe6577977c11'}}
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        if not code:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "code无效，请升级微信版本到8.0.16以上"
            return invoke_result_data
        for i in range(2):
            if i == 0:
                invoke_result_data = self.get_access_token(app_id, app_secret)
            else:
                invoke_result_data = self.get_access_token(app_id, app_secret, True)

            if invoke_result_data.success == True:
                break
        if invoke_result_data.success == False:
            return invoke_result_data
        access_token = invoke_result_data.data
        try:
            requset_url = 'https://api.weixin.qq.com/wxa/business/getuserphonenumber?access_token=' + access_token
            param = {'code': code}
            response = requests.post(requset_url, data=json.dumps(param, ensure_ascii=False).encode('utf-8'), headers={'Content-Type': 'application/json'})
            response_data = SevenHelper.json_loads(response.text)
            if response_data.__contains__("errcode") and response_data["errcode"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["errcode"]
                invoke_result_data.error_message = response_data["errmsg"]
                return invoke_result_data
            invoke_result_data.data = response_data["phone_info"]
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【授权手机号】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "授权手机号失败"
            return invoke_result_data

    @classmethod
    def create_qr_code_unlimit(self, page, scene="a=1", width=430, env_version="release", check_path=False, app_id="", app_secret=""):
        """
        :description:获取小程序/小游戏的二维码（注意：接口只能生成已发布的小程序的二维码。开发版的带参二维码可以在开发者工具预览时生成）
        :param page: 页面 page，例如 pages/index/index，根路径前不要填加 /，不能携带参数（参数请放在scene字段里），如果不填写这个字段，默认跳主页面
        :param scene: 最大32个可见字符，只支持数字，大小写英文以及部分特殊字符：!#$&'()*+,/:;=?@-._~，其它字符请自行编码为合法字符（因不支持%，中文无法使用 urlencode 处理，请使用其他编码方式）
        :param width: 二维码的宽度，单位 px，最小 280px，最大 1280px
        :param env_version: 要打开的小程序版本。正式版为 "release"，体验版为 "trial"，开发版为 "develop"。默认是正式版。
        :param check_path: 检查page 是否存在，为 true 时 page 必须是已经发布的小程序存在的页面（否则报错）；为 false 时允许小程序未发布或者 page 不存在
        :param app_id:app_id
        :param app_secret:app_secret
        :return: 图片二进制 数据类型Array<byte>
        :last_editors: HuangJianYi
        """
        app_id = app_id if app_id else share_config.get_value("app_id")
        app_secret = app_secret if app_secret else share_config.get_value("app_secret")

        invoke_result_data = InvokeResultData()
        redis_init = SevenHelper.redis_init(decode_responses=False)
        redis_key = "create_qr_code_unlimit:" + CryptoHelper.md5_encrypt(f"{page}_{scene}")
        redis_value = redis_init.get(redis_key)
        if redis_value:
            invoke_result_data.data = redis_value
            return invoke_result_data

        for i in range(2):
            if i == 0:
                invoke_result_data = self.get_access_token(app_id, app_secret)
            else:
                invoke_result_data = self.get_access_token(app_id, app_secret, True)

            if invoke_result_data.success == True:
                break
        if invoke_result_data.success == False:
            return invoke_result_data
        access_token = invoke_result_data.data
        response = None
        try:
            headers = {"Content-type": "application/json"}
            requset_url = 'https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token=' + access_token
            param = {"page": page, "scene": scene, "width": width, "env_version": env_version, "check_path":check_path}
            response = requests.post(requset_url, data=json.dumps(param, ensure_ascii=False).encode('utf-8'), headers=headers)
            response_data = SevenHelper.json_loads(response.text)
            if response_data.__contains__("errcode") and response_data["errcode"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["errcode"]
                invoke_result_data.error_message = response_data["errmsg"]
                return invoke_result_data
            invoke_result_data.data = response.content
            redis_init.set(redis_key, response.content, 30 * 24 * 3600)
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【create_qr_code_unlimit】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    @classmethod
    def create_qr_code(self, path, width=430, app_id="", app_secret=""):
        """
        :description:获取小程序二维码，适用于需要的码数量较少的业务场景。通过该接口生成的小程序码，永久有效，有数量限制
        :param path: 扫码进入的小程序页面路径，最大长度 128 字节，不能为空；对于小游戏，可以只传入 query 部分，来实现传参效果，如：传入 "?foo=bar"，即可在 wx.getLaunchOptionsSync 接口中的 query 参数获取到 {foo:"bar"}。
        :param width: 二维码的宽度，单位 px，最小 280px，最大 1280px
        :param app_id:app_id
        :param app_secret:app_secret
        :return: 图片二进制 数据类型Array<byte>
        :last_editors: HuangJianYi
        """
        app_id = app_id if app_id else share_config.get_value("app_id")
        app_secret = app_secret if app_secret else share_config.get_value("app_secret")

        invoke_result_data = InvokeResultData()
        redis_init = SevenHelper.redis_init(decode_responses=False)
        redis_key = "wechat_qr_code:" + CryptoHelper.md5_encrypt(f"{path}")
        redis_value = redis_init.get(redis_key)
        if redis_value:
            invoke_result_data.data = redis_value
            return invoke_result_data

        for i in range(2):
            if i == 0:
                invoke_result_data = self.get_access_token(app_id, app_secret)
            else:
                invoke_result_data = self.get_access_token(app_id, app_secret, True)

            if invoke_result_data.success == True:
                break
        if invoke_result_data.success == False:
            return invoke_result_data
        access_token = invoke_result_data.data
        response = None
        try:
            headers = {"Content-type": "application/json"}
            requset_url = 'https://api.weixin.qq.com/cgi-bin/wxaapp/createwxaqrcode?access_token=' + access_token
            param = {"path": path, "width": width}
            response = requests.post(requset_url, data=json.dumps(param, ensure_ascii=False).encode('utf-8'), headers=headers)
            response_data = SevenHelper.json_loads(response.text)
            if response_data.__contains__("errcode") and response_data["errcode"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["errcode"]
                invoke_result_data.error_message = response_data["errmsg"]
                return invoke_result_data
            invoke_result_data.data = response.content
            redis_init.set(redis_key, response.content, 30 * 24 * 3600)
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【create_qr_code】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    @classmethod
    def msg_sec_check(self, content, scene, open_id, nickname, app_id="", app_secret=""):
        """
        :description: 文本内容安全识别(https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/sec-center/sec-check/msgSecCheck.html)
        :param content：需检测的文本内容，文本字数的上限为2500字，需使用UTF-8编码
        :param scene：场景枚举值（1 资料；2 评论；3 论坛；4 社交日志）
        :param openid：用户的openid（用户需在近两小时访问过小程序）
        :param nickname：用户昵称
        :param app_id:app_id
        :param app_secret:app_secret
        :return:
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        app_id = app_id if app_id else share_config.get_value("app_id")
        app_secret = app_secret if app_secret else share_config.get_value("app_secret")
        invoke_result_data = InvokeResultData()
        for i in range(2):
            if i == 0:
                invoke_result_data = self.get_access_token(app_id, app_secret)
            else:
                invoke_result_data = self.get_access_token(app_id, app_secret, True)

            if invoke_result_data.success == True:
                break
        if invoke_result_data.success == False:
            return invoke_result_data
        access_token = invoke_result_data.data
        response = None
        try:
            requset_url = 'https://api.weixin.qq.com/wxa/msg_sec_check?access_token=' + access_token
            headers = {"Content-type": "application/json"}
            param = {"content": content, "scene": scene, "openid": open_id, "nickname": nickname, "version": 2}
            response = requests.post(requset_url, data=json.dumps(param, ensure_ascii=False).encode('utf-8'), headers=headers)
            response_data = SevenHelper.json_loads(response.text)
            if response_data.__contains__("errcode") and response_data["errcode"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["errcode"]
                invoke_result_data.error_message = response_data["errmsg"]
                return invoke_result_data
            invoke_result_data.data = response_data
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【msg_sec_check】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    @classmethod
    def media_check_async(self, media_url, media_type, scene, open_id, app_id="", app_secret=""):
        """
        :description: 音视频内容安全识别(https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/sec-center/sec-check/mediaCheckAsync.html)
        :param media_url：要检测的图片或音频的url，支持图片格式包括jpg, jepg, png, bmp, gif（取首帧），支持的音频格式包括mp3, aac, ac3, wma, flac, vorbis, opus, wav
        :param media_type：1:音频;2:图片
        :param scene：场景枚举值（1 资料；2 评论；3 论坛；4 社交日志）
        :param open_id：用户的openid（用户需在近两小时访问过小程序）
        :param app_id:app_id
        :param app_secret:app_secret
        :return:
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        app_id = app_id if app_id else share_config.get_value("app_id")
        app_secret = app_secret if app_secret else share_config.get_value("app_secret")
        invoke_result_data = InvokeResultData()
        for i in range(2):
            if i == 0:
                invoke_result_data = self.get_access_token(app_id, app_secret)
            else:
                invoke_result_data = self.get_access_token(app_id, app_secret, True)

            if invoke_result_data.success == True:
                break
        if invoke_result_data.success == False:
            return invoke_result_data
        access_token = invoke_result_data.data
        response = None
        try:
            requset_url = 'https://api.weixin.qq.com/wxa/media_check_async?access_token=' + access_token
            headers = {"Content-type": "application/json"}
            param = {"media_url": media_url,"media_type": media_type, "scene": scene, "openid": open_id, "version": 2}
            response = requests.post(requset_url, data=json.dumps(param, ensure_ascii=False).encode('utf-8'), headers=headers)
            response_data = SevenHelper.json_loads(response.text)
            if response_data.__contains__("errcode") and response_data["errcode"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["errcode"]
                invoke_result_data.error_message = response_data["errmsg"]
                return invoke_result_data
            invoke_result_data.data = response_data
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【media_check_async】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    @classmethod
    def decrypt_data_by_code(self, open_id, code, encrypted_Data, iv, app_id="", app_secret=""):
        """
        :description:解析加密数据，客户端判断是否登录状态，如果登录只传open_id不传code，如果是登录过期,要传code重新获取session_key
        :param open_id：open_id
        :param code：登录票据
        :param encrypted_Data：加密数据,微信返回加密参数
        :param iv：微信返回参数
        :param app_id：app_id
        :param app_secret：app_secret
        :return: 解密后的数据，用户信息或者手机号信息
        :last_editors: HuangJianYi
        """
        app_id = app_id if app_id else share_config.get_value("app_id")
        app_secret = app_secret if app_secret else share_config.get_value("app_secret")

        data = None
        if code:
            code2_session_dict = self.code2_session(code=code, app_id=app_id, app_secret=app_secret)
            if code2_session_dict:
                open_id = code2_session_dict["openid"]
        try:
            session_key = SevenHelper.redis_init().get(f"{app_id}_wechat_sessionkey:{open_id}")
            wx_data_crypt = WeChatDataCrypt(app_id, session_key)
            data = wx_data_crypt.decrypt(encrypted_Data, iv)  #data中是解密的信息
        except Exception as ex:
            self.logger_error.error("【decrypt_data_by_code】" + traceback.format_exc())
        return data

    @classmethod
    def decrypt_data(self, session_key, encrypted_Data, iv, app_id=""):
        """
        :description:解析加密数据
        :param session_key: session_key调用登录接口获得
        :param encrypted_Data：加密数据,微信返回加密参数
        :param iv：微信返回参数
        :param app_id: 微信小程序标识
        :return: 解密后的数据，用户信息或者手机号信息
        :last_editors: HuangJianYi
        """
        app_id = app_id if app_id else share_config.get_value("app_id")

        data = {}
        try:
            wx_data_crypt = WeChatDataCrypt(app_id, session_key)
            data = wx_data_crypt.decrypt(encrypted_Data, iv)  #data中是解密的信息
        except Exception as ex:
            ("【decrypt_data】" + traceback.format_exc())
        return data

    @classmethod
    def array_to_xml(self, array):
        """
        :description:array转xml
        :return:
        :last_editors: HuangJianYi
        """
        xml = ["<xml>"]
        for k, v in array.items():
            if v.isdigit():
                xml.append("<{0}>{1}</{0}>".format(k, v))
            else:
                xml.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))
        xml.append("</xml>")
        return "".join(xml)

    @classmethod
    def xml_to_array(self, xml):
        """
        :description:将xml转为array
        :return:
        :last_editors: HuangJianYi
        """
        array_data = {}
        root = ElementTree.fromstring(xml)
        for child in root:
            value = child.text
            array_data[child.tag] = value
        return array_data

    @classmethod
    def key_value_url(self, params, url_encode):
        """
        :description:   将键值对转为 key1=value1&key2=value2 对参数按照key=value的格式，并按照参数名ASCII字典序排序
        :param params：参数字典
        :param url_encode：是否url编码 True是False否
        :return: 
        :last_editors: HuangJianYi
        """
        slist = sorted(params)
        buff = []
        for k in slist:
            v = quote(params[k]) if url_encode else params[k]
            buff.append("{0}={1}".format(k, v))

        return "&".join(buff)

    @classmethod
    def get_nonce_str(self, length=32):
        """
        :description: 生成随机字符串
        :param length：长度
        :return: 
        :last_editors: HuangJianYi
        """
        import random
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        strs = []
        for x in range(length):
            strs.append(chars[random.randrange(0, len(chars))])
        return "".join(strs)

    @classmethod
    def get_sign(self, params, api_key):
        """
        :description:生成sign拼接API密钥
        :param api_key: api密钥
        :return: 
        :last_editors: HuangJianYi
        """
        string_a = WeChatHelper.key_value_url(params, False)
        string_sign_temp = string_a + '&key=' + api_key  # APIKEY, API密钥，需要在商户后台设置
        sign = (hashlib.md5(string_sign_temp.encode("utf-8")).hexdigest()).upper()
        return sign

    @classmethod
    def signature_v3(self, private_key_path, sign_str):
        """
        :description:  生成V3签名值
        :param private_key_path：私钥路径
        :param sign_str：签名字符串
        :return: 
        :last_editors: HuangJianYi
        """
        with open(private_key_path) as file:
            private_key = file.read()
        try:
            rsa_key = RSA.import_key(private_key)
            signer = PKCS1_v1_5.new(rsa_key)
            digest = SHA256.new(sign_str.encode('utf-8'))
            return base64.b64encode(signer.sign(digest)).decode('utf-8')
        except Exception:
            raise "WeixinPaySignIError"

    @classmethod
    def generate_scheme(self, app_id="", app_secret="", page="pages/index/index", query="", env_version="release", is_expire=True, expire_type=1, expire_interval=30, expire_time=0):
        """
        :description: 该接口用于获取小程序 scheme 码，适用于短信、邮件、外部网页、微信内等拉起小程序的业务场景。通过该接口，可以选择最长30天有效的小程序码，有数量限制，目前仅针对国内非个人主体的小程序开放
        :param app_id:app_id
        :param app_secret:app_secret
        :param page: 页面 page，例如 pages/theme/theme，根路径前不要填加
        :param query: 查询条件，例如 source_id=1&query1=q1
        :param env_version: 默认值"release"。要打开的小程序版本。正式版为"release"，体验版为"trial"，开发版为"develop"，仅在微信外打开时生效。
        :param is_expire: 到期失效的 scheme 码的失效时间，为 Unix 时间戳。生成的到期失效 scheme 码在该时间前有效。最长有效期为30天。is_expire 为 true 且 expire_type 为 0 时必填
        :param expire_type: 默认值0，到期失效的 scheme 码失效类型，失效时间：0，失效间隔天数：1
        :param expire_interval: 到期失效的 scheme 码的失效间隔天数。生成的到期失效 scheme 码在该间隔时间到达前有效。最长间隔天数为30天。is_expire 为 true 且 expire_type 为 1 时必填
        :param expire_time: 到期失效的 scheme 码的失效时间，为 Unix 时间戳。生成的到期失效 scheme 码在该时间前有效。最长有效期为30天。is_expire 为 true 且 expire_type 为 0 时必填
        :return: InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        if expire_type == 1 and expire_interval > 30:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "URL Scheme有效期最长30天"
            return invoke_result_data
        elif expire_type == 0 and TimeHelper.difference_days(expire_time, TimeHelper.get_now_timestamp()) > 30:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "URL Scheme有效期最长30天"
            return invoke_result_data

        redis_init = SevenHelper.redis_init(decode_responses=False)
        redis_key = "generate_scheme:" + CryptoHelper.md5_encrypt(f"{page}_{query}_{env_version}_{is_expire}_{expire_type}_{expire_interval}_{expire_time}")
        redis_value = redis_init.get(redis_key)
        if redis_value:
            invoke_result_data.data = redis_value.decode()
            return invoke_result_data

        for i in range(2):
            if i == 0:
                invoke_result_data = WeChatHelper.get_access_token(app_id, app_secret)
            else:
                invoke_result_data = WeChatHelper.get_access_token(app_id, app_secret, True)

            if invoke_result_data.success == True:
                break
        if invoke_result_data.success == False:
            return invoke_result_data

        access_token = invoke_result_data.data
        response = ""
        response_data = {}
        try:
            headers = {"Content-type": "application/json"}
            requset_url = 'https://api.weixin.qq.com/wxa/generatescheme?access_token=' + access_token
            param = {"jump_wxa": {"path": page, "query": query, "env_version": env_version}, "is_expire": is_expire, "expire_type": expire_type, "expire_interval": expire_interval, "expire_time": expire_time}
            response = requests.post(requset_url, data=json.dumps(param, ensure_ascii=False).encode('utf-8'), headers=headers)
            response_data = SevenHelper.json_loads(response.text)
            if response_data.__contains__("errcode") and response_data["errcode"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["errcode"]
                invoke_result_data.error_message = response_data["errmsg"]
                return invoke_result_data
            invoke_result_data.data = response_data['openlink']
            if expire_type == 1 and expire_interval > 0:
                redis_init.set(redis_key, invoke_result_data.data, expire_interval * 24 * 3600)
            elif expire_type == 0 and expire_time > 0:
                redis_init.set(redis_key, invoke_result_data.data, 300)
                redis_init.expireat(redis_key, expire_time)
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【generate_scheme】" + traceback.format_exc() + ":" + str(response.text))
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    @classmethod
    def generate_urllink(self, app_id="", app_secret="", page="pages/index/index", query="", env_version="release", is_expire=True, expire_type=1, expire_interval=30, expire_time=0, cloud_base=None):
        """
        :description: 获取小程序 URL Link，适用于短信、邮件、网页、微信内等拉起小程序的业务场景。通过该接口，可以选择最长30天有效的小程序链接，有数量限制，目前仅针对国内非个人主体的小程序开放
        :param app_id:app_id
        :param app_secret:app_secret
        :param page: 页面 page，例如 pages/theme/theme，根路径前不要填加
        :param query: 查询条件，例如 source_id=1&query1=q1
        :param env_version: 默认值"release"。要打开的小程序版本。正式版为"release"，体验版为"trial"，开发版为"develop"，仅在微信外打开时生效。
        :param is_expire: 到期失效的 scheme 码的失效时间，为 Unix 时间戳。生成的到期失效 scheme 码在该时间前有效。最长有效期为30天。is_expire 为 true 且 expire_type 为 0 时必填
        :param expire_type: 默认值0，到期失效的 scheme 码失效类型，失效时间：0，失效间隔天数：1
        :param expire_interval: 到期失效的 scheme 码的失效间隔天数。生成的到期失效 scheme 码在该间隔时间到达前有效。最长间隔天数为30天。is_expire 为 true 且 expire_type 为 1 时必填
        :param expire_time: 到期失效的 scheme 码的失效时间，为 Unix 时间戳。生成的到期失效 scheme 码在该时间前有效。最长有效期为30天。is_expire 为 true 且 expire_type 为 0 时必填
        :param cloud_base: 云开发静态网站自定义 H5 配置参数，可配置中转的云开发 H5 页面。不填默认用官方 H5 页面 例如{"env": "云开发环境，如：xxx", "domain": "静态网站自定义域名，不填则使用默认域名，如：xxx.xxx", "path": "云开发静态网站 H5 页面路径，不可携带 query如：/jump-wxa.html", "query": "云开发静态网站 H5 页面 query 参数，最大 1024 个字符，只支持数字，大小写英文以及部分特殊字符：`!#$&'()*+,/:;=?@-._~%``如：a=1&b=2", "resource_appid": "第三方批量代云开发时必填，表示创建该 env 的 appid （小程序/第三方平台）"}
        :return: InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        if expire_type == 1 and expire_interval > 30:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "URL Link有效期最长30天"
            return invoke_result_data
        elif expire_type == 0 and TimeHelper.difference_days(expire_time, TimeHelper.get_now_timestamp()) > 30:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "URL Link有效期最长30天"
            return invoke_result_data

        redis_init = SevenHelper.redis_init(decode_responses=False)
        redis_key = "generate_urllink:" + CryptoHelper.md5_encrypt(f"{page}_{query}_{env_version}_{is_expire}_{expire_type}_{expire_interval}_{expire_time}_{cloud_base}")
        redis_value = redis_init.get(redis_key)
        if redis_value:
            invoke_result_data.data = redis_value.decode()
            return invoke_result_data

        for i in range(2):
            if i == 0:
                invoke_result_data = WeChatHelper.get_access_token(app_id, app_secret)
            else:
                invoke_result_data = WeChatHelper.get_access_token(app_id, app_secret, True)

            if invoke_result_data.success == True:
                break
        if invoke_result_data.success == False:
            return invoke_result_data

        access_token = invoke_result_data.data
        response = ""
        response_data = {}
        try:
            headers = {"Content-type": "application/json"}
            requset_url = 'https://api.weixin.qq.com/wxa/generate_urllink?access_token=' + access_token
            param = {"path": page, "query": query, "env_version": env_version, "is_expire": is_expire, "expire_type": expire_type, "expire_interval": expire_interval, "expire_time": expire_time, "cloud_base": cloud_base}
            response = requests.post(requset_url, data=json.dumps(param, ensure_ascii=False).encode('utf-8'), headers=headers)
            response_data = SevenHelper.json_loads(response.text)
            if response_data.__contains__("errcode") and response_data["errcode"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["errcode"]
                invoke_result_data.error_message = response_data["errmsg"]
                return invoke_result_data
            invoke_result_data.data = response_data['url_link']
            if expire_type == 1 and expire_interval > 0:
                redis_init.set(redis_key, invoke_result_data.data, expire_interval * 24 * 3600)
            elif expire_type == 0 and expire_time > 0:
                redis_init.set(redis_key, invoke_result_data.data, 300)
                redis_init.expireat(redis_key, expire_time)
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【generate_urllink】" + traceback.format_exc() + ":" + str(response.text))
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    @classmethod
    def generate_shortlink(self, app_id="", app_secret="", page="pages/index/index", query="", page_title="", is_permanent=False):
        """
        :description: 获取小程序 Short Link，适用于微信内拉起小程序的业务场景。目前只开放给电商类目(具体包含以下一级类目：电商平台、商家自营、跨境电商)。通过该接口，可以选择生成到期失效和永久有效的小程序短链
        :param app_id:app_id
        :param app_secret:app_secret
        :param page: 页面 page，例如 pages/theme/theme，根路径前不要填加
        :param query: 查询条件，例如 source_id=1&query1=q1
        :param page_title: 页面标题，不能包含违法信息，超过20字符会用... 截断代替
        :param is_permanent: 默认值false。生成的 Short Link 类型，短期有效：false，永久有效：true
        :return: InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        redis_init = SevenHelper.redis_init(decode_responses=False)
        redis_key = "generate_shortlink:" + CryptoHelper.md5_encrypt(f"{page}_{query}_{page_title}_{is_permanent}")
        redis_value = redis_init.get(redis_key)
        if redis_value:
            invoke_result_data.data = redis_value.decode()
            return invoke_result_data

        for i in range(2):
            if i == 0:
                invoke_result_data = WeChatHelper.get_access_token(app_id, app_secret)
            else:
                invoke_result_data = WeChatHelper.get_access_token(app_id, app_secret, True)

            if invoke_result_data.success == True:
                break
        if invoke_result_data.success == False:
            return invoke_result_data

        access_token = invoke_result_data.data
        response = ""
        response_data = {}
        try:
            headers = {"Content-type": "application/json"}
            requset_url = 'https://api.weixin.qq.com/wxa/genwxashortlink?access_token=' + access_token
            param = {"page_url": f"{page}?{query}", "page_title": page_title, "is_permanent": is_permanent}
            response = requests.post(requset_url, data=json.dumps(param, ensure_ascii=False).encode('utf-8'), headers=headers)
            response_data = SevenHelper.json_loads(response.text)
            if response_data.__contains__("errcode") and response_data["errcode"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["errcode"]
                invoke_result_data.error_message = response_data["errmsg"]
                return invoke_result_data
            invoke_result_data.data = response_data['link']
            if is_permanent == True:
                redis_init.set(redis_key, invoke_result_data.data)
            else:
                redis_init.set(redis_key, invoke_result_data.data, 30 * 24 * 3600)
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【generate_shortlink】" + traceback.format_exc() + ":" + str(response.text))
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    @classmethod
    def get_delivery_list(self, app_id="", app_secret=""):
        """
        :description: 商户使用此接口获取所有运力id的列表
        :param app_id:app_id
        :param app_secret:app_secret
        :return: InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()

        redis_init = SevenHelper.redis_init(decode_responses=False)
        redis_key = "wx_delivery_list"
        redis_value = redis_init.get(redis_key)
        if redis_value:
            invoke_result_data.data = SevenHelper.json_loads(redis_value.decode())
            return invoke_result_data

        for i in range(2):
            if i == 0:
                invoke_result_data = WeChatHelper.get_access_token(app_id, app_secret)
            else:
                invoke_result_data = WeChatHelper.get_access_token(app_id, app_secret, True)

            if invoke_result_data.success == True:
                break
        if invoke_result_data.success == False:
            return invoke_result_data

        access_token = invoke_result_data.data
        response = ""
        response_data = {}
        try:
            headers = {"Content-type": "application/json"}
            requset_url = 'https://api.weixin.qq.com/cgi-bin/express/delivery/open_msg/get_delivery_list?access_token=' + access_token
            param = {}
            response = requests.post(requset_url, data=json.dumps(param, ensure_ascii=False).encode('utf-8'), headers=headers)
            response_data = SevenHelper.json_loads(response.text)
            if response_data.__contains__("errcode") and response_data["errcode"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["errcode"]
                invoke_result_data.error_message = response_data["errmsg"]
                return invoke_result_data
            invoke_result_data.data = response_data['delivery_list']
            for item in invoke_result_data.data:
                item["delivery_name"] = item["delivery_name"].encode('latin-1').decode('unicode_escape').encode('latin-1').decode('utf-8')
            redis_init.set(redis_key, SevenHelper.json_dumps(invoke_result_data.data), 24 * 3600)
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【get_delivery_list】" + traceback.format_exc() + ":" + str(response.text))
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    @classmethod
    def upload_shipping_info(self, open_id, order_number_type: int, transaction_id: str, logistics_type: int, delivery_mode: int, shipping_list: list, is_all_delivered: bool = False, app_id="", app_secret=""):
        """
        :description: 用户交易后，默认资金将会进入冻结状态，开发者在发货后，需要在小程序平台录入相关发货信息，平台会将发货信息以消息的形式推送给购买的微信用户。如果你已经录入发货信息，在用户尚未确认收货的情况下可以通过该接口修改发货信息，但一个支付单只能更新一次发货信息，请谨慎操作。
        :param open_id:open_id
        :param order_number_type:订单单号类型，用于确认需要上传详情的订单。枚举值1，使用下单商户号和商户侧单号；枚举值2，使用微信支付单号。
        :param transaction_id:原支付交易对应的微信订单号
        :param logistics_type:物流模式，发货方式枚举值：1、实体物流配送采用快递公司进行实体物流配送形式 2、同城配送 3、虚拟商品，虚拟商品，例如话费充值，点卡等，无实体配送形式 4、用户自提
        :param delivery_mode:发货模式，发货模式枚举值：1、UNIFIED_DELIVERY（统一发货）2、SPLIT_DELIVERY（分拆发货） 示例值: UNIFIED_DELIVERY
        :param shipping_list:物流信息列表，发货物流单列表，支持统一发货（单个物流单）和分拆发货（多个物流单）两种模式，多重性: [1, 10]
        :param is_all_delivered:分拆发货模式时必填，用于标识分拆发货模式下是否已全部发货完成，只有全部发货完成的情况下才会向用户推送发货完成通知。示例值: true/false
        :param app_id:app_id
        :param app_secret:app_secret
        :return: InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        for i in range(2):
            if i == 0:
                invoke_result_data = WeChatHelper.get_access_token(app_id, app_secret)
            else:
                invoke_result_data = WeChatHelper.get_access_token(app_id, app_secret, True)

            if invoke_result_data.success == True:
                break
        if invoke_result_data.success == False:
            return invoke_result_data

        access_token = invoke_result_data.data
        response = ""
        response_data = {}
        try:
            headers = {"Content-type": "application/json"}
            requset_url = 'https://api.weixin.qq.com/wxa/sec/order/upload_shipping_info?access_token=' + access_token
            param = {}
            param["order_key"] = {"order_number_type": order_number_type, "transaction_id": transaction_id}
            param["logistics_type"] = logistics_type
            param["delivery_mode"] = delivery_mode
            param["is_all_delivered"] = is_all_delivered
            param["shipping_list"] = shipping_list
            param["upload_time"] = TimeExHelper.convert_bj_to_rfc()
            param["payer"] = {"openid": open_id}
            response = requests.post(requset_url, data=json.dumps(param, ensure_ascii=False).encode('utf-8'), headers=headers)
            response_data = SevenHelper.json_loads(response.text)
            if response_data.__contains__("errcode") and response_data["errcode"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["errcode"]
                invoke_result_data.error_message = response_data["errmsg"]
                return invoke_result_data
            invoke_result_data.data = response_data
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【upload_shipping_info】" + traceback.format_exc() + ":" + str(response.text))
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data


class WeChatPayRequest(object):
    """
    :description: 微信支付请求类,配置文件内容 "wechat_pay": {"api_key": "","mch_id": "","certificate_url": "","private_key_url": ""}
    """
    """配置账号信息"""
    # =======【基本信息设置】=====================================
    # 微信公众号身份的唯一标识。审核通过后，在微信发送的邮件中查看
    app_id = ""
    # 受理商ID，身份标识
    mch_id = ""
    # API密钥，需要在商户后台设置
    api_key = ""
    # 证书地址,证书文件需要在商户后台下载
    certificate_url = ""
    # 商户私钥地址,文件需要在商户后台下载
    private_key_url = ""

    logger_error = Logger.get_logger_by_name("log_error")

    def __init__(self, app_id="", api_key="", mch_id="", certificate_url="", private_key_url=""):
        pay_config = share_config.get_value("wechat_pay")
        self.app_id = app_id if app_id else share_config.get_value("app_id")
        self.api_key = api_key if api_key else pay_config["api_key"]
        self.mch_id = mch_id if mch_id else pay_config["mch_id"]
        self.certificate_url = certificate_url if certificate_url else pay_config["certificate_url"]
        self.private_key_url = private_key_url if private_key_url else pay_config.get("private_key_url", "")

    def get_prepay_id(self, unified_order_url, params):
        """
        :description: 获取预支付单号prepay_id
        :param unifiedorder_url：微信下单地址
        :param params：请求参数字典
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        redis_key = f"{self.app_id}_wechat_prepay_id:" + str(params['out_trade_no'])
        redis_init = SevenHelper.redis_init()
        prepay_id = redis_init.get(redis_key)
        if prepay_id:
            invoke_result_data.data = prepay_id
            return invoke_result_data
        params['sign'] = WeChatHelper.get_sign(params, self.api_key)
        respone = requests.post(unified_order_url, self.convert_request_xml(params), headers={'Content-Type': 'application/xml'})
        response_data = xmltodict.parse(respone.text.encode('ISO-8859-1').decode('utf-8'))['xml']
        if response_data['return_code'] == 'SUCCESS':
            if response_data['result_code'] == 'SUCCESS':
                prepay_id = str(response_data['prepay_id'])
                redis_init.set(redis_key, prepay_id, ex=3600 * 1)
                invoke_result_data.data = prepay_id
                return invoke_result_data
            else:
                self.logger_error.error("【预支付单号】" + str(response_data))
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = response_data['err_code_des']
                return invoke_result_data
        else:
            self.logger_error.error("【预支付单号】" + str(response_data))
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = response_data['return_msg']
            return invoke_result_data

    def create_order(self, pay_order_no, body, total_fee, spbill_create_ip, notify_url, open_id="", time_expire="", trade_type="JSAPI"):
        """
        :description: 创建微信预订单
        :param pay_order_no：商户订单号(支付单号)
        :param body：订单描述
        :param total_fee：支付金额；单位元
        :param spbill_create_ip：客户端IP
        :param notify_url：微信支付结果异步通知地址
        :param open_id：微信open_id
        :param time_expire：交易结束时间
        :param trade_type：交易类型trade_type为JSAPI时，openid为必填参数！此参数为微信用户在商户对应appid下的唯一标识, 统一支付接口中，缺少必填参数openid！
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        spbill_create_ip = spbill_create_ip if SevenHelper.is_ip(spbill_create_ip) == True else "127.0.0.1"
        params = {
            'appid': self.app_id,  # appid
            'mch_id': self.mch_id,  # 商户号
            'nonce_str': WeChatHelper.get_nonce_str(),
            'body': body,
            'out_trade_no': str(pay_order_no),
            'total_fee': str(int(decimal.Decimal(str(total_fee)) * 100)),
            'spbill_create_ip': spbill_create_ip,
            'trade_type': trade_type,
            'notify_url': notify_url
        }
        if trade_type == "JSAPI":
            if open_id == "":
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "缺少必填参数open_id"
                return invoke_result_data
            else:
                params['openid'] = open_id
        if time_expire != "":
            params['time_expire'] = str(time_expire)

        # 开发者调用支付统一下单API生成预交易单
        unified_order_url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
        invoke_result_data = self.get_prepay_id(unified_order_url, params)
        if invoke_result_data.success == False:
            return invoke_result_data
        prepay_id = invoke_result_data.data
        params['prepay_id'] = prepay_id
        params['package'] = f"prepay_id={prepay_id}"
        params['timestamp'] = str(int(time.time()))
        sign_again_params = {'appId': params['appid'], 'nonceStr': params['nonce_str'], 'package': params['package'], 'signType': 'MD5', 'timeStamp': params['timestamp']}
        sign_again_params['sign'] = WeChatHelper.get_sign(sign_again_params, self.api_key)
        sign_again_params['paySign'] = sign_again_params['sign']
        invoke_result_data.data = sign_again_params
        return invoke_result_data  # 返回给app

    def query_order(self, pay_order_no="", transaction_id=""):
        """
        :description: 查询订单
        :param transaction_id：微信订单号
        :param pay_order_no：商户订单号(支付单号)
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        if transaction_id == "" and pay_order_no == "":
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "缺少必填参数transaction_id或pay_order_no"
            return invoke_result_data
        request_xml = ""
        try:
            params = {
                'appid': self.app_id,
                'mch_id': self.mch_id,
                'nonce_str': WeChatHelper.get_nonce_str(),
            }
            if transaction_id != "":
                params['transaction_id'] = str(transaction_id)
            if pay_order_no != "":
                params['out_trade_no'] = str(pay_order_no)
            params['sign'] = WeChatHelper.get_sign(params, self.api_key)
            request_xml = self.convert_request_xml(params)
            queryorder_url = 'https://api.mch.weixin.qq.com/pay/orderquery'
            respone = requests.post(queryorder_url, request_xml, headers={'Content-Type': 'application/xml'})
            response_data = xmltodict.parse(respone.text.encode('ISO-8859-1').decode('utf-8'))['xml']
            invoke_result_data.data = response_data
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【查询订单】" + traceback.format_exc() + ":" + str(request_xml))
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "查询订单出现异常"
            return invoke_result_data

    def close_order(self, pay_order_no=""):
        """
        :description: 关闭订单
        :param pay_order_no：商户订单号(支付单号)
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        if pay_order_no == "":
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "缺少必填参数pay_order_no"
            return invoke_result_data
        request_xml = ""
        try:
            params = {'appid': self.app_id, 'mch_id': self.mch_id, 'nonce_str': WeChatHelper.get_nonce_str(), 'out_trade_no': str(pay_order_no)}
            params['sign'] = WeChatHelper.get_sign(params, self.api_key)
            request_xml = self.convert_request_xml(params)
            queryorder_url = 'https://api.mch.weixin.qq.com/pay/closeorder'
            respone = requests.post(queryorder_url, request_xml, headers={'Content-Type': 'application/xml'})
            response_data = xmltodict.parse(respone.text.encode('ISO-8859-1').decode('utf-8'))['xml']
            invoke_result_data.data = response_data
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【关闭订单】" + traceback.format_exc() + ":" + str(request_xml))
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "关闭订单出现异常"
            return invoke_result_data

    def get_pay_status(self, pay_order_no, transaction_id=""):
        """
        :description: 查询订单状态
        :param pay_order_no：商户订单号(支付单号)
        :param transaction_id：微信订单号
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        invoke_result_data = self.query_order(pay_order_no, transaction_id)
        if invoke_result_data.success == False:
            return ""
        else:
            response_data = invoke_result_data.data
            if response_data['return_code'] == 'SUCCESS':
                if response_data['result_code'] == 'SUCCESS':
                    return str(response_data['trade_state'] if response_data.__contains__("trade_state") else "")  # SUCCESS--支付成功REFUND--转入退款NOTPAY--未支付CLOSED--已关闭REVOKED--已撤销(刷卡支付)USERPAYING--用户支付中PAYERROR--支付失败(其他原因，如银行返回失败)ACCEPT--已接收，等待扣款
                else:
                    return ""
            else:
                return ""

    def create_refund(self, refund_no, pay_order_no, notify_url, refund_fee, total_fee):
        """
        :description: 服务端退款请求
        :param refund_no:开发者侧的退款单号, 不可重复
        :param pay_order_no:商户分配订单号，标识进行退款的订单，开发者服务端的唯一订单号
        :param notify_url:退款通知地址
        :param refund_fee: 退款金额，单位[分]
        :param total_fee：支付金额；单位元
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        params = {
            'appid': self.app_id,  # appid
            'mch_id': self.mch_id,  # 商户号
            'nonce_str': WeChatHelper.get_nonce_str(),
            'out_trade_no': str(pay_order_no),
            'out_refund_no': str(refund_no),
            'notify_url': notify_url,
            'refund_fee': int(decimal.Decimal(str(refund_fee)) * 100),
            'sign_type': 'MD5',
            'total_fee': int(decimal.Decimal(str(total_fee)) * 100),
        }
        params['sign'] = WeChatHelper.get_sign(params, self.api_key)
        refund_url = 'https://api.mch.weixin.qq.com/secapi/pay/refund'
        respone = post(url=refund_url, data=self.convert_request_xml(params), headers={'Content-Type': 'application/xml'}, pkcs12_filename=self.certificate_url, pkcs12_password=self.mch_id)
        response_data = xmltodict.parse(respone.text.encode('ISO-8859-1').decode('utf-8'))['xml']
        if response_data['return_code'] == 'SUCCESS':
            if response_data['result_code'] == 'SUCCESS':
                invoke_result_data.data = response_data['refund_id']
                return invoke_result_data
            else:
                self.logger_error.error("【创建退款单】" + str(response_data))
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = response_data['err_code_des']
                return invoke_result_data
        else:
            self.logger_error.error("【创建退款单】" + str(response_data))
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = response_data['return_msg']
            return invoke_result_data

    def query_refund(self, refund_no):
        """
        :description: 查询退款单
        :param refund_no：商户退款单号
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        if refund_no == "":
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "缺少必填参数refund_no"
            return invoke_result_data
        request_xml = ""
        try:
            params = {'appid': self.app_id, 'mch_id': self.mch_id, 'nonce_str': WeChatHelper.get_nonce_str(), 'out_refund_no': str(refund_no), 'sign_type': 'MD5'}
            params['sign'] = WeChatHelper.get_sign(params, self.api_key)
            request_xml = self.convert_request_xml(params)
            queryrefund_url = 'https://api.mch.weixin.qq.com/pay/refundquery'
            respone = requests.post(queryrefund_url, request_xml, headers={'Content-Type': 'application/xml'})
            response_data = xmltodict.parse(respone.text.encode('ISO-8859-1').decode('utf-8'))['xml']
            invoke_result_data.data = response_data
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【查询退款单】" + traceback.format_exc() + ":" + str(request_xml))
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "查询退款单出现异常"
            return invoke_result_data

    def send_red_pack(self, mch_billno, send_name, re_openid, total_amount, total_num, wishing, client_ip, act_name, remark, scene_id=''):
        """
        :description: 发现金红包(https://pay.weixin.qq.com/wiki/doc/api/tools/cash_coupon.php?chapter=13_4&index=3)
        :param mch_billno：商户订单号(每个订单号必须唯一组成：mch_id+yyyymmdd+10位一天内不能重复的数字)
        :param send_name：商户名称(红包发送者名称)
        :param re_openid：接受红包的用户openid
        :param total_amount：付款金额，单位分
        :param total_num：红包发放总人数
        :param wishing：红包祝福语
        :param client_ip：该IP可传用户端或者服务端的IP
        :param act_name：活动名称
        :param remark：备注信息
        :param scene_id：发放红包使用场景，红包金额大于200或者小于1元时必传（PRODUCT_1:商品促销PRODUCT_2:抽奖PRODUCT_3:虚拟物品兑奖 PRODUCT_4:企业内部福利PRODUCT_5:渠道分润PRODUCT_6:保险回馈PRODUCT_7:彩票派奖PRODUCT_8:税务刮奖）
        :return: 当返回错误码为“SYSTEMERROR”时，请不要更换商户订单号，一定要使用原商户订单号重试，否则可能造成重复发放红包等资金风险
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        client_ip = client_ip if SevenHelper.is_ip(client_ip) == True else "127.0.0.1"
        request_xml = ""
        try:
            params = {'appid': self.app_id, 'mch_id': self.mch_id, 'nonce_str': WeChatHelper.get_nonce_str(), 'mch_billno': str(mch_billno), 'send_name': send_name, 're_openid': re_openid, 'total_amount': total_amount, 'total_num': total_num, 'wishing': wishing, 'client_ip': client_ip, 'act_name': act_name, 'remark': remark}
            if scene_id:
                params['scene_id'] = scene_id
            params['sign'] = WeChatHelper.get_sign(params, self.api_key)
            request_xml = self.convert_request_xml(params)
            requset_url = 'https://api.mch.weixin.qq.com/mmpaymkttransfers/sendredpack'
            # 重点是`cert=(certificate_url, private_key_url), verify=True`参数，查看源码后才知道是这样传ca证书
            respone = requests.post(requset_url, data=request_xml, cert=(self.certificate_url, self.private_key_url), verify=True)
            response_data = xmltodict.parse(respone.text.encode('ISO-8859-1').decode('utf-8'))['xml']
            if response_data['return_code'] == 'SUCCESS':
                if response_data['result_code'] == 'SUCCESS':
                    invoke_result_data.data = {"send_listid": response_data['send_listid']}
                    return invoke_result_data
                else:
                    self.logger_error.error("【发现金红包】" + str(response_data))
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = response_data['err_code_des']
                    return invoke_result_data
            invoke_result_data.data = response_data
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【发现金红包】" + traceback.format_exc() + ":" + str(request_xml))
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "发现金红包出现异常"
            return invoke_result_data

    def convert_request_xml(self, params):
        """
        :description:拼接XML
        :return: 
        :last_editors: HuangJianYi
        """
        xml = "<xml>"
        for k, v in params.items():
            # v = v.encode('utf8')
            # k = k.encode('utf8')
            xml += '<' + k + '>' + str(v) + '</' + k + '>'
        xml += "</xml>"
        return xml.encode("utf-8")


class WeChatPayReponse(object):
    """
    :description: 微信支付响应类
    """

    logger_error = Logger.get_logger_by_name("log_error")

    def __init__(self, reponse_xml, api_key=""):
        self.data = WeChatHelper.xml_to_array(reponse_xml)
        pay_config = share_config.get_value("wechat_pay")
        self.api_key = api_key if api_key else pay_config["api_key"]

    def check_sign(self):
        """
        :description: 校验签名
        :return:
        :last_editors: HuangJianYi
        """
        params = dict(self.data)  # make a copy to save sign
        del params['sign']
        sign = WeChatHelper.get_sign(params, self.api_key)  # 本地签名
        if self.data['sign'] == sign:
            return True
        return False

    def get_data(self):
        """
        :description: 获取微信的通知的数据
        :return:
        :last_editors: HuangJianYi
        """
        return self.data

    def convert_response_xml(self, msg, ok=True):
        """
        :description: 返回xml格式数据
        :return:
        :last_editors: HuangJianYi
        """
        code = "SUCCESS" if ok else "FAIL"
        return WeChatHelper.array_to_xml(dict(return_code=code, return_msg=msg))


class WeChatRefundReponse(object):
    """
    :description: 微信退款响应类
    """
    logger_error = Logger.get_logger_by_name("log_error")

    def __init__(self, reponse_xml, api_key=""):
        self.data = WeChatHelper.xml_to_array(reponse_xml)
        pay_config = share_config.get_value("wechat_pay")
        self.api_key = api_key if api_key else pay_config["api_key"]

    def get_data(self):
        """
        :description:获取微信的通知的数据
        :return: 
        :last_editors: HuangJianYi
        """
        return self.data

    def decode_req_info(self, req_info):
        """
        :description:解密退款通知加密参数req_info
        :return: 
        :last_editors: HuangJianYi
        """
        detail_info = CryptoHelper.aes_decrypt(req_info, CryptoHelper.md5_encrypt(self.api_key))
        dict_req_info = xmltodict.parse(detail_info)
        return dict_req_info

    def convert_response_xml(self, msg, ok=True):
        code = "SUCCESS" if ok else "FAIL"
        return WeChatHelper.array_to_xml(dict(return_code=code, return_msg=msg))


class WeChatDataCrypt:
    """
    :description: 微信数据解密帮助类
    """

    def __init__(self, app_id, session_key):
        self.app_id = app_id
        self.session_key = session_key

    def decrypt(self, encryptedData, iv):
        # base64 decode
        session_key = base64.b64decode(self.session_key)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)
        decrypted = {}
        cipher = AES.new(session_key, AES.MODE_CBC, iv)
        result_data = str(self._unpad(cipher.decrypt(encryptedData)), "utf-8")
        if result_data:
            decrypted = SevenHelper.json_loads(result_data)
        if decrypted:
            if decrypted['watermark']['appid'] != self.app_id:
                raise Exception('Invalid Buffer')
        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]


class WeChatPayV3Request(object):
    """
    微信V3支付请求
    """
    # 微信公众号身份的唯一标识。审核通过后，在微信发送的邮件中查看
    app_id = ""
    # 商户ID，身份标识
    mch_id = ""
    # API密钥，需要在商户后台设置
    api_key = ""
    # 证书地址,证书文件需要在商户后台下载
    certificate_url = ""
    # 商户私钥地址apiclient_key.pem 地址,文件需要在商户后台下载
    private_key_url = ""
    # 商户API证书序列号
    mch_serial_no = ""

    logger_error = Logger.get_logger_by_name("log_error")

    base_url = 'https://api.mch.weixin.qq.com'

    def __init__(self, app_id="", api_key="", mch_id="", mch_serial_no="", certificate_url="", private_key_url=""):

        pay_config = share_config.get_value("wechat_pay", {})
        self.app_id = app_id if app_id else share_config.get_value("app_id")
        self.mch_id = mch_id if mch_id else pay_config.get("mch_id", "")
        self.api_key = api_key if api_key else pay_config.get("api_key", "")
        self.mch_serial_no = mch_serial_no if mch_serial_no else pay_config.get("mch_serial_no", "")
        self.certificate_url = certificate_url if certificate_url else pay_config.get("certificate_url", "")
        self.private_key_url = private_key_url if private_key_url else pay_config.get("private_key_url", "")
        self.timestamp = str(int(time.time()))
        self.nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))

    def _generate_request_sign(self, url_path, data, method='POST'):
        """
        :description:  生成请求签名
        :param url_path：不包含域名的请求地址
        :param data：请求参数（post请求才需要传,get传None）
        :param method：请求方式
        :return: 
        :last_editors: HuangJianYi
        """
        sign_list = [method, url_path, self.timestamp, self.nonce_str]
        if data is not None:
            sign_list.append(data)
        else:
            sign_list.append('')
        sign_str = '\n'.join(sign_list) + '\n'
        return WeChatHelper.signature_v3(private_key_path=self.private_key_url, sign_str=sign_str)

    def _generate_pay_sign(self, app_id, package):
        """
        :description:  生成支付签名
        :param app_id：商户绑定的应用标识
        :param package：订单详情扩展字符串（示例值：prepay_id=wx201410272009395522657a690389285100）
        :return: 
        :last_editors: HuangJianYi
        """
        sign_list = [app_id, self.timestamp, self.nonce_str, package]
        sign_str = '\n'.join(sign_list) + '\n'
        return WeChatHelper.signature_v3(private_key_path=self.private_key_url, sign_str=sign_str)

    def _generate_auth_header(self, signature):
        """
        生成授权请求头
        """
        return f'WECHATPAY2-SHA256-RSA2048 mchid="{self.mch_id}",nonce_str="{self.nonce_str}",' \
               f'signature="{signature}",timestamp="{self.timestamp}",serial_no="{self.mch_serial_no}"'

    def transfer_one(self, open_id, out_batch_no, batch_name, batch_remark, total_amount):
        """
        :description:  单次商家转账
        :param open_id：open_id是微信用户在公众号appid下的唯一用户标识（appid不同，则获取到的openid就不同），可用于永久标记一个用户
        :param out_batch_no：商家批次单号（商户生成的唯一编号）
        :param batch_name：批次名称
        :param batch_remark：批次备注
        :param total_amount：转账总金额(单位：分)
        :return: 错误码返回SYSTEM_ERROR和NOT_ENOUGH和FREQUENCY_LIMITED 请勿更换商家转账批次单号，请使用相同参数再次调用API。否则可能造成资金损失
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        url_path = '/v3/transfer/batches'
        url = self.base_url + url_path
        transfer_detail_list = []
        transfer_detail = {}
        transfer_detail["out_detail_no"] = out_batch_no
        transfer_detail["transfer_amount"] = total_amount
        transfer_detail["transfer_remark"] = batch_remark
        transfer_detail["openid"] = open_id
        transfer_detail_list.append(transfer_detail)

        data = {'appid': self.app_id, 'out_batch_no': out_batch_no, "batch_name": batch_name, "batch_remark": batch_remark, "total_amount": total_amount, 'total_num': 1, "transfer_detail_list": transfer_detail_list}

        try:
            data = json.dumps(data)
            signature = self._generate_request_sign(url_path=url_path, data=data)
            # print("Authorization signature:", self._generate_auth_header(signature))
            headers = {'Authorization': self._generate_auth_header(signature), 'Content-Type': 'application/json'}
            res = requests.post(url=url, data=data, headers=headers, timeout=10)
            response_data = SevenHelper.json_loads(res.text)
            if response_data.__contains__("code") and response_data["code"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["code"]
                invoke_result_data.error_message = response_data["message"]
                return invoke_result_data
            invoke_result_data.data = response_data
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【v3_transfer_one】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    def transfer_list(self, out_batch_no, batch_name, batch_remark, total_amount, total_num, transfer_detail_list=[]):
        """
        :description:  批量商家转账
        :param out_batch_no：商家批次单号（商户生成的唯一编号）
        :param batch_name：批次名称
        :param batch_remark：批次备注
        :param total_amount：转账总金额
        :param total_num：转账总笔数
        :param transfer_detail_list：转账明细列表
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        url_path = '/v3/transfer/batches'
        url = self.base_url + url_path
        data = {'appid': self.app_id, 'out_batch_no': out_batch_no, "batch_name": batch_name, "batch_remark": batch_remark, "total_amount": total_amount, 'total_num': total_num, "transfer_detail_list": transfer_detail_list}

        try:
            data = json.dumps(data)
            signature = self._generate_request_sign(url_path=url_path, data=data)
            # print("Authorization signature:", self._generate_auth_header(signature))
            headers = {'Authorization': self._generate_auth_header(signature), 'Content-Type': 'application/json'}
            res = requests.post(url=url, data=data, headers=headers, timeout=10)
            response_data = SevenHelper.json_loads(res.text)
            if response_data.__contains__("code") and response_data["code"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["code"]
                invoke_result_data.error_message = response_data["message"]
                return invoke_result_data
            invoke_result_data.data = response_data
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【v3_transfer_list】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    def query_batches(self, batch_id, need_query_detail=False, offset=0, limit=20, detail_status=None):
        """
        :description:  商家转账批次单号查询批次单
        :param batch_id：微信批次单号
        :param need_query_detail：是否查询转账明细单(枚举值：true：是；false：否，默认否。商户可选择是否查询指定状态的转账明细单，当转账批次单状态为“FINISHED”（已完成）时，才会返回满足条件的转账明细单)
        :param offset：请求资源起始位置
        :param limit：最大资源条数
        :param detail_status：明细状态(查询指定状态的转账明细单，当need_query_detail为true时，该字段必填ALL:全部。需要同时查询转账成功和转账失败的明细单SUCCESS:转账成功。只查询转账成功的明细单FAIL:转账失败。只查询转账失败的明细单)
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        url_path = f'/v3/transfer/batches/batch-id/{batch_id}'
        data = {'need_query_detail': need_query_detail, 'offset': offset, 'limit': limit}
        if need_query_detail == True:
            detail_status = "ALL"
        if detail_status:
            data["detail_status"] = detail_status
        url_path = url_path + "?" + WeChatHelper.key_value_url(data, False)
        url = self.base_url + url_path
        data = None
        try:
            signature = self._generate_request_sign(url_path=url_path, data=data, method='GET')
            # print("Authorization signature:", self._generate_auth_header(signature))
            headers = {'Authorization': self._generate_auth_header(signature), 'Content-Type': 'application/json'}
            res = requests.get(url=url, data=data, headers=headers, timeout=10)
            response_data = SevenHelper.json_loads(res.text)
            if response_data.__contains__("code") and response_data["code"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["code"]
                invoke_result_data.error_message = response_data["message"]
                return invoke_result_data
            invoke_result_data.data = response_data
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【v3_query_batches】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    def query_batches_detail(self, batch_id, detail_id):
        """
        :description:  微信明细单号查询明细单
        :param batch_id：微信批次单号
        :param detail_id：微信明细单号
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        url_path = f'/v3/transfer/batches/batch-id/{batch_id}/details/detail-id/{detail_id}'
        url = self.base_url + url_path
        data = None
        try:
            signature = self._generate_request_sign(url_path=url_path, data=data, method='GET')
            # print("Authorization signature:", self._generate_auth_header(signature))
            headers = {'Authorization': self._generate_auth_header(signature), 'Content-Type': 'application/json'}
            res = requests.get(url=url, data=data, headers=headers, timeout=10)
            response_data = SevenHelper.json_loads(res.text)
            if response_data.__contains__("code") and response_data["code"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["code"]
                invoke_result_data.error_message = response_data["message"]
                return invoke_result_data
            invoke_result_data.data = response_data
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【v3_query_batches_detail】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    def create_order(self, pay_order_no, title, total_fee, open_id, notify_url, time_expire=''):
        """
        :description: 微信jsapi支付
        :param: pay_order_no: 商户系统内部订单号，只能是数字、大小写字母_-*且在同一个商户号下唯一
        :param: title: 商品描述
        :param: total_fee: 金额
        :param: open_id: open_id
        :param: notify_url: 步接收微信支付结果通知的回调地址，通知url必须为外网可访问的url，不能携带参数。 公网域名必须为https，如果是走专线接入，使用专线NAT IP或者私有回调域名可使用http
        :param: time_expire: 订单失效时间，遵循rfc3339标准格式，格式为yyyy-MM-DDTHH:mm:ss+TIMEZONE，yyyy-MM-DD表示年月日，T出现在字符串中，表示time元素的开头，HH:mm:ss表示时分秒，TIMEZONE表示时区（+08:00表示东八区时间，领先UTC8小时，即北京时间）。例如：2015-05-20T13:29:35+08:00表示，北京时间2015年5月20日 13点29分35秒。示例值：2018-06-08T10:34:56+08:00
        :last_editors: HuangJianYi
        """        
        invoke_result_data = InvokeResultData()
        if not pay_order_no or not title or not total_fee or not open_id or not notify_url:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "缺少必填参数"
            return invoke_result_data
            
        url_path = '/v3/pay/transactions/jsapi'
        url = self.base_url + url_path

        data = {
            "appid": self.app_id,
            "mchid": self.mch_id,
            "description": title,
            "out_trade_no": pay_order_no,
            "notify_url": notify_url,
            "amount":{
                "total": total_fee
            },
            "payer":{
                "openid": open_id
            }
        }
        # 可选参数处理
        if time_expire and isinstance(time_expire, str):
            data["time_expire"] = time_expire
            
        try:
            redis_key = f"{self.app_id}_wechat_prepay_id:" + str(pay_order_no)
            redis_init = SevenHelper.redis_init()
            prepay_id = redis_init.get(redis_key)
            if not prepay_id:
                data = json.dumps(data)
                signature = self._generate_request_sign(url_path=url_path, data=data)
                headers = {'Authorization': self._generate_auth_header(signature), 'Content-Type': 'application/json'}
                res = requests.post(url=url, data=data, headers=headers, timeout=10)
                response_data = SevenHelper.json_loads(res.text)
                if response_data.__contains__("code") and response_data["code"] != 0:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = response_data["code"]
                    invoke_result_data.error_message = response_data["message"]
                    return invoke_result_data
                prepay_id = response_data['prepay_id']
                redis_init.set(redis_key, prepay_id, 3600)
            # 构建唤起支付信息
            prepay_id = f"prepay_id={prepay_id}" # 预支付交易会话标识。用于后续接口调用中使用，该值有效期为2小时
            timestamp = self.timestamp
            nonce_str = self.nonce_str
            content = '{}\n{}\n{}\n{}\n'.format(self.app_id, timestamp, nonce_str, prepay_id)
            sign = WeChatHelper.signature_v3(self.private_key_url, content)

            pay_data = {
                "package": prepay_id,
                "noncestr": nonce_str,
                "timestamp": timestamp,
                "signtype":"RSA",
                "sign": sign
            }
            invoke_result_data.data = pay_data
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【v3_create_order】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    def query_order(self, pay_order_no):
        """
        :description: 查询订单状态
        :param pay_order_no: 商户订单号
        :return: InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        url_path = f'/v3/pay/transactions/out-trade-no/{pay_order_no}?mchid={self.mch_id}'
        url = self.base_url + url_path
        
        try:
            signature = self._generate_request_sign(url_path=url_path, data=None, method='GET')
            headers = {'Authorization': self._generate_auth_header(signature), 'Content-Type': 'application/json'}
            res = requests.get(url=url, headers=headers, timeout=10)
            response_data = SevenHelper.json_loads(res.text)
            if response_data.__contains__("code") and response_data["code"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["code"]
                invoke_result_data.error_message = response_data["message"]
                return invoke_result_data
            invoke_result_data.data = response_data
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【v3_query_order】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    def close_order(self, pay_order_no):
        """
        :description: 关闭订单
        :param pay_order_no: 商户订单号
        :return: InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        url_path = f'/v3/pay/transactions/out-trade-no/{pay_order_no}/close'
        url = self.base_url + url_path
        
        data = {
            "mchid": self.mch_id
        }

        try:
            data = json.dumps(data)
            signature = self._generate_request_sign(url_path=url_path, data=data)
            headers = {'Authorization': self._generate_auth_header(signature), 'Content-Type': 'application/json'}
            res = requests.post(url=url, data=data, headers=headers, timeout=10)
            response_data = SevenHelper.json_loads(res.text)
            if response_data.__contains__("code") and response_data["code"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["code"]
                invoke_result_data.error_message = response_data["message"]
                return invoke_result_data
            invoke_result_data.data = response_data
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【v3_close_order】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    def create_refund(self, pay_order_no, refund_no, total_fee, refund_fee, notify_url, reason=''):
        """
        :description: 创建退款（https://pay.weixin.qq.com/doc/v3/merchant/4012791903）
        :param pay_order_no: 原支付交易对应的商户订单号
        :param refund_no: 商户退款单号
        :param total_fee: 原订单金额
        :param refund_fee: 退款金额
        :param notify_url: 退款结果通知url
        :param reason: 若商户传了退款原因，该原因将在下发给用户的退款消息中显示,请注意：1、该退款原因参数的长度不得超过80个字节；2、当订单退款金额小于等于1元且为部分退款时，退款原因将不会在消息中体现。
        :return: InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        url_path = '/v3/refund/domestic/refunds'
        url = self.base_url + url_path
        
        data = {
            "transaction_id": pay_order_no,
            "out_refund_no": refund_no,
            "amount": {
                "refund": refund_fee,
                "total": total_fee,
                "currency": "CNY"
            },
            "notify_url": notify_url
        }
        if reason:
            data['reason'] = reason


        try:
            data = json.dumps(data)
            signature = self._generate_request_sign(url_path=url_path, data=data)
            headers = {'Authorization': self._generate_auth_header(signature), 'Content-Type': 'application/json'}
            res = requests.post(url=url, data=data, headers=headers, timeout=10)
            response_data = SevenHelper.json_loads(res.text)
            if response_data.__contains__("code") and response_data["code"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["code"]
                invoke_result_data.error_message = response_data["message"]
                return invoke_result_data
            invoke_result_data.data = response_data
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【v3_create_refund】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    def query_refund(self, refund_no):
        """
        :description: 查询退款
        :param refund_no: 商户退款单号
        :return: InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        url_path = f'/v3/refund/domestic/refunds/{refund_no}'
        url = self.base_url + url_path
        
        try:
            signature = self._generate_request_sign(url_path=url_path, data=None, method='GET')
            headers = {'Authorization': self._generate_auth_header(signature), 'Content-Type': 'application/json'}
            res = requests.get(url=url, headers=headers, timeout=10)
            response_data = SevenHelper.json_loads(res.text)
            if response_data.__contains__("code") and response_data["code"] != 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = response_data["code"]
                invoke_result_data.error_message = response_data["message"]
                return invoke_result_data
            invoke_result_data.data = response_data
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【v3_query_refund】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data


class WeChatPayV3Response(object):
    """
    微信V3支付响应
    """
    def __init__(self, public_key_url, api_key):

        pay_config = share_config.get_value("wechat_pay", {})
        self.api_key = api_key if api_key else pay_config.get("api_key", "")
        self.public_key_url = public_key_url if public_key_url else pay_config.get("public_key_url", "")

    def check_notify_sign(self, timestamp, nonce, body, response_signature):
        """
        :description: 回调验签
        :param timestamp：回调返回的时间搓
        :param nonce：回调返回的nonce
        :param body：回调返回的body
        :param response_signature：回调返回的签名值
        :last_editors: HuangJianYi
        """        
        body = body.decode("utf-8")
        sign_str = f"{timestamp}\n{nonce}\n{body}\n"
        digest = SHA256.new(sign_str.encode('UTF-8'))  # 对响应体进行RSA加密
        # 公钥
        with open(self.public_key_url) as file:
            public_key = file.read()
        public_rsa_key = RSA.importKey(public_key)
        public_signer = PKCS1_v1_5.new(public_rsa_key)
        return public_signer.verify(digest, base64.b64decode(response_signature))  # 验签

    def decode_notify_data(self, ciphertext, nonce, associated_data):
        """
        :description: 微信解密
        :param ciphertext：data["resource"]["ciphertext"]
        :param nonce：data["resource"]["nonce"]
        :param associated_data：data["resource"]["original_type"]
        :last_editors: HuangJianYi
        """        
        cipher = AES.new(self.api_key.encode(), AES.MODE_GCM, nonce=nonce.encode())
        cipher.update(associated_data.encode())
        en_data = base64.b64decode(ciphertext.encode('utf-8'))
        auth_tag = en_data[-16:]
        _en_data = en_data[:-16]
        plaintext = cipher.decrypt_and_verify(_en_data, auth_tag)
        return plaintext.decode()

    def parse_refund_response(self, response_data):
        """
        :description: 解析退款响应数据
        :param response_data: 退款响应数据
        :return: 解析后的退款数据
        :last_editors: HuangJianYi
        """
        result = {}
        try:
            if response_data.get("code") == 0:
                result = {
                    "refund_id": response_data.get("refund_id"),  # 微信退款单号
                    "out_refund_no": response_data.get("out_refund_no"),  # 商户退款单号
                    "transaction_id": response_data.get("transaction_id"),  # 微信订单号
                    "out_trade_no": response_data.get("out_trade_no"),  # 商户订单号
                    "refund_fee": response_data.get("amount", {}).get("refund"),  # 退款金额
                    "total_fee": response_data.get("amount", {}).get("total"),  # 订单总金额
                    "status": response_data.get("status"),  # 退款状态
                    "success_time": response_data.get("success_time"),  # 退款成功时间
                    "refund_account": response_data.get("refund_account"),  # 退款资金来源
                    "refund_request_source": response_data.get("refund_request_source")  # 退款发起来源
                }
            else:
                result = {
                    "error_code": response_data.get("code"),
                    "error_message": response_data.get("message")
                }
        except Exception as ex:
            result = {
                "error_code": "parse_error",
                "error_message": str(ex)
            }
        return result

    def verify_refund_response(self, response_data):
        """
        :description: 验证退款响应
        :param response_data: 退款响应数据
        :return: 验证结果
        :last_editors: HuangJianYi
        """
        try:
            if response_data.get("code") == 0:
                return True
            return False
        except Exception:
            return False

    def get_refund_status(self, response_data):
        """
        :description: 获取退款状态
        :param response_data: 退款响应数据
        :return: 退款状态
        :last_editors: HuangJianYi
        """
        try:
            return response_data.get("status")
        except Exception:
            return None
