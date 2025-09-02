# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2023-08-16 16:24:06
@LastEditTime: 2023-10-24 14:42:15
@LastEditors: HuangJianYi
@Description: 
"""
from seven_framework import *
from seven_cloudapp_frame.models.seven_model import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.libs.common import *


class BceSmsHelper:
    """
    :description: 百度云短信帮助类
    """
    logger_error = Logger.get_logger_by_name("log_error")

    @classmethod
    def get_sms_config(self):
        sms_bce_config = share_config.get_value("sms_bce_config", {"domain": "", "secret_id": "", "secret_key": "", "sign_id": "", "template_id": ""})
        self.domain = sms_bce_config.get("domain", "")
        self.secret_id = sms_bce_config.get("secret_id", "")
        self.secret_key = sms_bce_config.get("secret_key", "")
        self.sign_id = sms_bce_config.get("sign_id", "")
        self.template_id = sms_bce_config.get("template_id", "")

    @classmethod
    def send_message(self, code, phone_number):
        """
        :description:发送短信验证码 
        :param code: code
        :param phone_number: 手机号
        :return: 
        :last_editors: HuangJianYi
        """
        #从Python SDK导入SMS配置管理模块以及安全认证模块
        from baidubce.bce_client_configuration import BceClientConfiguration
        from baidubce.auth.bce_credentials import BceCredentials
        import baidubce.services.sms.sms_client as sms
        import baidubce.exception as ex

        invoke_result_data = InvokeResultData()
        try:
            sms_config = BceClientConfiguration(credentials=BceCredentials(self.secret_id, self.secret_key), endpoint=self.domain)
            #新建SmsClient
            sms_client = sms.SmsClient(sms_config)
            response = sms_client.send_message(signature_id=self.sign_id, template_id=self.template_id, mobile=phone_number, content_var_dict={'code': code, 'time': '30'})
            invoke_result_data.data = response
            return invoke_result_data
        except ex.BceHttpClientError as e:
            if isinstance(e.last_error, ex.BceServerError):
                self.logger_error.error(f"发送短信失败。Response:{e.last_error.status_code},code:{e.last_error.code},request_id:{e.last_error.request_id}")
            else:
                self.logger_error.error(f"发送短信失败。Unknown exception:{e}")
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "短信发送失败"
            return invoke_result_data


class AliSmsHelper:
    """
    :description: 阿里云短信帮助类
    """
    logger_error = Logger.get_logger_by_name("log_error")

    @classmethod
    def get_sms_config(self):
        sms_ali_config = share_config.get_value("sms_ali_config", {"domain":"", "secret_id": "", "secret_key": "", "region": "", "sign_name": "", "template_id": ""})
        self.domain = sms_ali_config.get("domain", "")
        self.secret_id = sms_ali_config.get("secret_id", "")
        self.secret_key = sms_ali_config.get("secret_key", "")
        self.region = sms_ali_config.get("region", "")
        self.sign_name = sms_ali_config.get("sign_name", "")
        self.template_id = sms_ali_config.get("template_id", "")

    @classmethod
    def send_message(self, code, phone_number):
        """
        :description:发送短信验证码 
        :param code: code
        :param phone_number: 手机号
        :return: 
        :last_editors: HuangJianYi
        """
        from aliyunsdkcore.client import AcsClient
        from aliyunsdkcore.request import CommonRequest

        invoke_result_data = InvokeResultData()
        try:
            client = AcsClient(self.secret_id, self.secret_key, self.region)
            request = CommonRequest()
            request.set_accept_format('json')
            request.set_domain(self.domain)
            request.set_method('POST')
            request.set_protocol_type('https')  # https | http
            request.set_version('2017-05-25')
            request.set_action_name('SendSms')

            request.add_query_param('RegionId', self.region)
            request.add_query_param('PhoneNumbers', phone_number)
            request.add_query_param('SignName', self.sign_name)
            request.add_query_param('TemplateCode', self.template_id)
            request.add_query_param('TemplateParam', "{\"code\":" + code + "}")
            response = client.do_action(request)
            invoke_result_data.data = dict(json.loads(response))
            return invoke_result_data
        except Exception as err:
            self.logger_error.error(f"短信发送错误:{err}")
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "短信发送失败"
            return invoke_result_data


class TencentSmsHelper:
    """
    :description: 腾讯云短信帮助类,需要安装模块tencentcloud-sdk-python==3.0.1174
    """
    logger_error = Logger.get_logger_by_name("log_error")

    @classmethod
    def get_sms_config(self):
        sms_tencent_config = share_config.get_value("sms_tencent_config", {"secret_id": "", "secret_key": "", "region": "", "sdk_app_id": "", "sign_name": "", "template_id": ""})
        self.secret_id = sms_tencent_config.get("secret_id","")
        self.secret_key = sms_tencent_config.get("secret_key", "")
        self.region = sms_tencent_config.get("region", "ap-guangzhou")
        self.sdk_app_id = sms_tencent_config.get("sdk_app_id", "")
        self.sign_name = sms_tencent_config.get("sign_name", "")
        self.template_id = sms_tencent_config.get("template_id", "")

    @classmethod
    def send_message(self, code, phone_number):
        """
        :description:发送短信验证码 ,需要安装模块tencentcloud-sdk-python==3.0.1174
        :param code: code
        :param phone_number: 手机号
        :return: 
        :last_editors: HuangJianYi
        """
        from tencentcloud.common import credential
        from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
        # 导入对应产品模块的client models。
        from tencentcloud.sms.v20210111 import sms_client, models
        # 导入可选配置类
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.common.profile.http_profile import HttpProfile

        invoke_result_data = InvokeResultData()
        try:
            self.get_sms_config()
            # 必要步骤：
            # 实例化一个认证对象，入参需要传入腾讯云账户密钥对secretId，secretKey。
            # 这里采用的是从环境变量读取的方式，需要在环境变量中先设置这两个值。
            # 你也可以直接在代码中写死密钥对，但是小心不要将代码复制、上传或者分享给他人，
            # 以免泄露密钥对危及你的财产安全。
            # SecretId、SecretKey 查询: https://console.cloud.tencent.com/cam/capi
            cred = credential.Credential(self.secret_id, self.secret_key)
            # cred = credential.Credential(
            #     os.environ.get(""),
            #     os.environ.get("")
            # )

            # 实例化一个http选项，可选的，没有特殊需求可以跳过。
            httpProfile = HttpProfile()
            # 如果需要指定proxy访问接口，可以按照如下方式初始化hp（无需要直接忽略）
            # httpProfile = HttpProfile(proxy="http://用户名:密码@代理IP:代理端口")
            httpProfile.reqMethod = "POST"  # post请求(默认为post请求)
            httpProfile.reqTimeout = 30  # 请求超时时间，单位为秒(默认60秒)
            httpProfile.endpoint = "sms.tencentcloudapi.com"  # 指定接入地域域名(默认就近接入)

            # 非必要步骤:
            # 实例化一个客户端配置对象，可以指定超时时间等配置
            clientProfile = ClientProfile()
            clientProfile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法
            clientProfile.language = "en-US"
            clientProfile.httpProfile = httpProfile

            # 实例化要请求产品(以sms为例)的client对象
            # 第二个参数是地域信息，可以直接填写字符串ap-guangzhou，支持的地域列表参考 https://cloud.tencent.com/document/api/382/52071#.E5.9C.B0.E5.9F.9F.E5.88.97.E8.A1.A8
            client = sms_client.SmsClient(cred, self.region, clientProfile)

            # 实例化一个请求对象，根据调用的接口和实际情况，可以进一步设置请求参数
            # 你可以直接查询SDK源码确定SendSmsRequest有哪些属性可以设置
            # 属性可能是基本类型，也可能引用了另一个数据结构
            # 推荐使用IDE进行开发，可以方便的跳转查阅各个接口和数据结构的文档说明
            req = models.SendSmsRequest()

            # 基本类型的设置:
            # SDK采用的是指针风格指定参数，即使对于基本类型你也需要用指针来对参数赋值。
            # SDK提供对基本类型的指针引用封装函数
            # 帮助链接：
            # 短信控制台: https://console.cloud.tencent.com/smsv2
            # 腾讯云短信小助手: https://cloud.tencent.com/document/product/382/3773#.E6.8A.80.E6.9C.AF.E4.BA.A4.E6.B5.81

            # 短信应用ID: 短信SdkAppId在 [短信控制台] 添加应用后生成的实际SdkAppId，示例如1400006666
            # 应用 ID 可前往 [短信控制台](https://console.cloud.tencent.com/smsv2/app-manage) 查看
            req.SmsSdkAppId = self.sdk_app_id
            # 短信签名内容: 使用 UTF-8 编码，必须填写已审核通过的签名
            # 签名信息可前往 [国内短信](https://console.cloud.tencent.com/smsv2/csms-sign) 或 [国际/港澳台短信](https://console.cloud.tencent.com/smsv2/isms-sign) 的签名管理查看
            req.SignName = self.sign_name
            # 模板 ID: 必须填写已审核通过的模板 ID
            # 模板 ID 可前往 [国内短信](https://console.cloud.tencent.com/smsv2/csms-template) 或 [国际/港澳台短信](https://console.cloud.tencent.com/smsv2/isms-template) 的正文模板管理查看
            req.TemplateId = self.template_id
            # 模板参数: 模板参数的个数需要与 TemplateId 对应模板的变量个数保持一致，，若无模板参数，则设置为空
            req.TemplateParamSet = [code]
            # 下发手机号码，采用 E.164 标准，+[国家或地区码][手机号]
            # 示例如：+8613711112222， 其中前面有一个+号 ，86为国家码，13711112222为手机号，最多不要超过200个手机号
            req.PhoneNumberSet = [f"+86{phone_number}"]
            # 用户的 session 内容（无需要可忽略）: 可以携带用户侧 ID 等上下文信息，server 会原样返回
            req.SessionContext = ""
            # 短信码号扩展号（无需要可忽略）: 默认未开通，如需开通请联系 [腾讯云短信小助手]
            req.ExtendCode = ""
            # 国内短信无需填写该项；国际/港澳台短信已申请独立 SenderId 需要填写该字段，默认使用公共 SenderId，无需填写该字段。注：月度使用量达到指定量级可申请独立 SenderId 使用，详情请联系 [腾讯云短信小助手](https://cloud.tencent.com/document/product/382/3773#.E6.8A.80.E6.9C.AF.E4.BA.A4.E6.B5.81)。
            req.SenderId = ""

            resp = client.SendSms(req)

            # 输出json格式的字符串回包
            try:
                result = json.loads(resp.to_json_string(indent=2))
                if result["SendStatusSet"][0]["Code"] == "Ok":
                    # 发送成功
                    return invoke_result_data
                else:
                    self.logger_error.error(f"短信发送失败:{resp.to_json_string(indent=2)}，错误码参考地址：https://cloud.tencent.com/document/api/382/52075")
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "exception"
                    invoke_result_data.error_message = "短信发送失败"
                    return invoke_result_data
            except:
                self.logger_error.error("【短信发送意外错误】" + traceback.format_exc())
                invoke_result_data.success = False
                invoke_result_data.error_code = "exception"
                invoke_result_data.error_message = "短信发送失败"
                return invoke_result_data

            # 当出现以下错误码时，快速解决方案参考
            # - [FailedOperation.SignatureIncorrectOrUnapproved](https://cloud.tencent.com/document/product/382/9558#.E7.9F.AD.E4.BF.A1.E5.8F.91.E9.80.81.E6.8F.90.E7.A4.BA.EF.BC.9Afailedoperation.signatureincorrectorunapproved-.E5.A6.82.E4.BD.95.E5.A4.84.E7.90.86.EF.BC.9F)
            # - [FailedOperation.TemplateIncorrectOrUnapproved](https://cloud.tencent.com/document/product/382/9558#.E7.9F.AD.E4.BF.A1.E5.8F.91.E9.80.81.E6.8F.90.E7.A4.BA.EF.BC.9Afailedoperation.templateincorrectorunapproved-.E5.A6.82.E4.BD.95.E5.A4.84.E7.90.86.EF.BC.9F)
            # - [UnauthorizedOperation.SmsSdkAppIdVerifyFail](https://cloud.tencent.com/document/product/382/9558#.E7.9F.AD.E4.BF.A1.E5.8F.91.E9.80.81.E6.8F.90.E7.A4.BA.EF.BC.9Aunauthorizedoperation.smssdkappidverifyfail-.E5.A6.82.E4.BD.95.E5.A4.84.E7.90.86.EF.BC.9F)
            # - [UnsupportedOperation.ContainDomesticAndInternationalPhoneNumber](https://cloud.tencent.com/document/product/382/9558#.E7.9F.AD.E4.BF.A1.E5.8F.91.E9.80.81.E6.8F.90.E7.A4.BA.EF.BC.9Aunsupportedoperation.containdomesticandinternationalphonenumber-.E5.A6.82.E4.BD.95.E5.A4.84.E7.90.86.EF.BC.9F)
            # - 更多错误，可咨询[腾讯云助手](https://tccc.qcloud.com/web/im/index.html#/chat?webAppId=8fa15978f85cb41f7e2ea36920cb3ae1&title=Sms)

        except TencentCloudSDKException as err:
            self.logger_error.error(f"短信发送错误:{err}，错误码参考地址：https://cloud.tencent.com/document/api/382/52075")
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "短信发送失败"
            return invoke_result_data