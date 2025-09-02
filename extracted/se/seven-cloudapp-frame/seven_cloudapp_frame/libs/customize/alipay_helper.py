# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2022-06-22 09:38:56
@LastEditTime: 2024-05-31 11:40:02
@LastEditors: HuangJianYi
@Description: 支付宝支付帮助类
"""
from seven_framework import TimeHelper, HTTPHelper, config
from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.models.seven_model import InvokeResultData
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from urllib.parse import quote_plus
from base64 import decodebytes, encodebytes
import json


class AliPayRequest(object):
    """
    :description: 支付宝支付帮助类.使用RSA2签名,配置文件内容 "ali_pay": {"app_id": "","app_private_key": "","alipay_public_key":"","pay_notify_url":"","refund_notify_url":""}
    """
    def __init__(self, app_id="", app_private_key="", alipay_public_key="", debug=False):
        """
        :description: 初始化
        :param app_id:支付宝分配给开发者的应用ID
        :param app_private_key:商户密钥
        :param alipay_public_key:支付宝公钥
        :param notify_url:异步通知地址
        :param debug:True沙箱 False正式环境
        :return:
        :last_editors: HuangJianYi
        """
        pay_config = share_config.get_value("ali_pay")
        self.app_id = app_id if app_id else pay_config["app_id"]
        app_private_key = app_private_key if app_private_key else pay_config["app_private_key"]
        alipay_public_key = alipay_public_key if alipay_public_key else pay_config["alipay_public_key"]
        self.app_private_key = RSA.importKey("-----BEGIN RSA PRIVATE KEY-----\n" + app_private_key + "\n-----END RSA PRIVATE KEY-----")
        self.alipay_public_key = RSA.importKey("-----BEGIN RSA PUBLIC KEY-----\n" + alipay_public_key + "\n-----END RSA PUBLIC KEY-----")

        if debug is True:
            self.__gateway = "https://openapi.alipaydev.com/gateway.do"
        else:
            self.__gateway = "https://openapi.alipay.com/gateway.do"
    
    def trade_precreate(self, pay_order_no, subject, total_amount, notify_url, time_expire="", return_url=""):
        """
        :description: 统一收单线下交易预创建
        :param pay_order_no:商户订单号。由商家自定义，64个字符以内，仅支持字母、数字、下划线且需保证在商户端不重复。
        :param subject:订单标题。注意：不可使用特殊字符，如 /，=，& 等。
        :param total_amount:【描述】订单总金额，单位为元，精确到小数点后两位，取值范围为 [0.01,100000000]，金额不能为 0。如果同时传入了【可打折金额】，【不可打折金额】，【订单总金额】三者，则必须满足如下条件：【订单总金额】=【可打折金额】+【不可打折金额】
        :param notify_url:异步通知地址
        :param time_expire:绝对超时时间，格式为yyyy-MM-dd HH:mm:ss
        :param return_url:同步通知地址(跳转地址),可为空
        :param product_code 【描述】销售产品码。如果签约的是当面付快捷版，则传 OFFLINE_PAYMENT；其它支付宝当面付产品传 FACE_TO_FACE_PAYMENT；不传则默认使用 FACE_TO_FACE_PAYMENT。
        :return:支付地址
        :last_editors: WangDe
        """
        invoke_result_data = InvokeResultData()
        biz_content = {
            "subject": subject,
            "out_trade_no": pay_order_no,
            "total_amount": total_amount,
            "product_code": "FACE_TO_FACE_PAYMENT",
        }
        if time_expire:
            biz_content["time_expire"] = time_expire

        data = self.convert_request_param("alipay.trade.precreate", biz_content, notify_url, return_url)
        url = self.__gateway + '?' + self.__key_value_url(data)
        response = HTTPHelper.get(url)
        response_data = json.loads(response.text)
        if "alipay_trade_precreate_response" in response_data.keys():
            if "code" in response_data["alipay_trade_precreate_response"]:
                if response_data["alipay_trade_precreate_response"]["code"] == "10000":
                    invoke_result_data.success = True                    
                else:
                    invoke_result_data.success = False
                invoke_result_data.data = response_data["alipay_trade_precreate_response"]
        return invoke_result_data

    def trade_page_pay(self, pay_order_no, subject, total_amount, notify_url, time_expire="", return_url="", http_method="GET"):
        """
        :description: PC场景下单
        :param pay_order_no:商户订单号。由商家自定义，64个字符以内，仅支持字母、数字、下划线且需保证在商户端不重复。
        :param subject:订单标题。注意：不可使用特殊字符，如 /，=，& 等。
        :param total_amount:订单总金额，单位为元，精确到小数点后两位，取值范围为 [0.01,100000000]。金额不能为0。
        :param notify_url:异步通知地址
        :param time_expire:绝对超时时间，格式为yyyy-MM-dd HH:mm:ss
        :param return_url:同步通知地址(跳转地址),可为空
        :param http_method:请求方式，get或post
        :return:GET请求返回地址，POST请求返回form表单
        :last_editors: HuangJianYi
        """
        biz_content = {
            "subject": subject,
            "out_trade_no": pay_order_no,
            "total_amount": total_amount,
            "product_code": "FAST_INSTANT_TRADE_PAY",
            "body":subject            
        }
        if not time_expire:
            time_expire = TimeHelper.add_days_by_format_time(day=1)
        biz_content["time_expire"] = time_expire
        data = self.convert_request_param("alipay.trade.page.pay", biz_content, notify_url, return_url)
        if http_method == "GET":
            url = self.__gateway + '?' + self.__key_value_url(data)
            return url
        else:
            return self.__build_form(self.__gateway, data)

    def trade_query(self, pay_order_no, trade_no):
        """
        :description: 查询订单
        :param pay_order_no:商户订单号。由商家自定义，64个字符以内，仅支持字母、数字、下划线且需保证在商户端不重复。
        :param trade_no:支付宝支付单号
        :return:订单信息
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        if pay_order_no:
            biz_content = {'out_trade_no': pay_order_no}
        if trade_no:
            biz_content = {'trado_no': trade_no}
        data = self.convert_request_param('alipay.trade.query', biz_content, "", "")
        url = self.__gateway + '?' + self.__key_value_url(data)
        response = HTTPHelper.get(url)
        response_data = json.loads(response.text)
        if "alipay_trade_query_response" in response_data.keys():
            if "code" in response_data["alipay_trade_query_response"]:
                if response_data["alipay_trade_query_response"]["code"] == "10000":
                    invoke_result_data.success = True
                else:
                    invoke_result_data.success = False
                invoke_result_data.data = response_data["alipay_trade_query_response"]
        return invoke_result_data

    def trade_close(self, pay_order_no, trade_no):
        """
        :description: 交易关闭 用于交易创建后，用户在一定时间内未进行支付，可调用该接口直接将未付款的交易进行关闭
        :param pay_order_no:商户订单号。由商家自定义，64个字符以内，仅支持字母、数字、下划线且需保证在商户端不重复。
        :param trade_no:支付宝支付单号
        :return:
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        if pay_order_no:
            biz_content = {'out_trade_no': pay_order_no}
        if trade_no:
            biz_content = {'trado_no': trade_no}
        data = self.convert_request_param('alipay.trade.close', biz_content, "", "")
        url = self.__gateway + '?' + self.__key_value_url(data)
        response = HTTPHelper.get(url)
        response_data = json.loads(response.text)
        if "alipay_trade_close_response" in response_data.keys():
            if "code" in response_data["alipay_trade_close_response"]:
                if response_data["alipay_trade_close_response"]["code"] == "10000":
                    invoke_result_data.success = True
                else:
                    invoke_result_data.success = False
                invoke_result_data.data = response_data["alipay_trade_close_response"]
        return invoke_result_data
    
    def trade_cancel(self, pay_order_no, trade_no):
        """
        :description: 交易关闭 用于交易创建后，用户在一定时间内未进行支付，可调用该接口直接将未付款的交易进行关闭
        :param pay_order_no:商户订单号。由商家自定义，64个字符以内，仅支持字母、数字、下划线且需保证在商户端不重复。
        :param trade_no:支付宝支付单号
        :return:
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        if pay_order_no:
            biz_content = {'out_trade_no': pay_order_no}
        if trade_no:
            biz_content = {'trado_no': trade_no}
        data = self.convert_request_param('alipay.trade.cancel', biz_content, "", "")
        url = self.__gateway + '?' + self.__key_value_url(data)
        response = HTTPHelper.get(url)
        response_data = json.loads(response.text)
        if "alipay_trade_cancel_response" in response_data.keys():
            if "code" in response_data["alipay_trade_cancel_response"]:
                if response_data["alipay_trade_cancel_response"]["code"] == "10000":
                    invoke_result_data.success = True
                else:
                    invoke_result_data.success = False
                invoke_result_data.data = response_data["alipay_trade_cancel_response"]
        return invoke_result_data

    def trade_refund(self, refund_amount, pay_order_no, trade_no, notify_url, return_url=""):
        """
        :description: 退款
        :param refund_amount:退款金额
        :param pay_order_no:商户订单号。由商家自定义，64个字符以内，仅支持字母、数字、下划线且需保证在商户端不重复。
        :param trade_no:支付宝支付单号
        :param notify_url:异步通知地址
        :param return_url:同步通知地址(跳转地址),可为空
        :return:退款结果
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        invoke_result_data.success = False
        invoke_result_data.error_code = "fail"
        invoke_result_data.error_message = "退款失败"
        if pay_order_no:
            biz_content = {'out_trade_no': pay_order_no}
        if trade_no:
            biz_content = {'trado_no': trade_no}
        biz_content['refund_amount'] = refund_amount
        data = self.convert_request_param('alipay.trade.refund', biz_content, notify_url, return_url)
        url = self.__gateway + '?' + self.__key_value_url(data)
        response = HTTPHelper.get(url)
        response_data = json.loads(response.text)
        if "alipay_trade_refund_response" in response_data.keys():
            if "code" in response_data["alipay_trade_refund_response"]:
                if response_data["alipay_trade_refund_response"]["code"] == "10000":
                    invoke_result_data.success = True
                    invoke_result_data.data = response_data["alipay_trade_refund_response"]
        return invoke_result_data

    def convert_request_param(self, method, biz_content, notify_url, return_url=""):
        """
        :description: 转换请求参数
        :param method:方法名
        :param biz_content:业务内容
        :param alipay_public_key:阿里公钥
        :param return_url:同步地址
        :return:请求参数字典
        :last_editors: HuangJianYi
        """
        data = {"app_id": self.app_id, "method": method, "charset": "utf-8", "sign_type": "RSA2", "timestamp": TimeHelper.get_now_format_time(), "version": "1.0", "biz_content": biz_content}
        if return_url:
            data["return_url"] = return_url
        if notify_url:
            data["notify_url"] = notify_url
        return data

    def __build_form(self, url, params):
        """
        :description: 内部方法，构造form表单输出结果
        :param pay_order_no:商户订单号。由商家自定义，64个字符以内，仅支持字母、数字、下划线且需保证在商户端不重复。
        :param subject:订单标题。注意：不可使用特殊字符，如 /，=，& 等。
        :param total_amount:订单总金额，单位为元，精确到小数点后两位，取值范围为 [0.01,100000000]。金额不能为0。
        :param notify_url:异步通知地址
        :param time_expire:绝对超时时间，格式为yyyy-MM-dd HH:mm:ss
        :param return_url:同步通知地址(跳转地址),可为空
        :param method:请求方式，get或post
        :return:支付地址
        :last_editors: HuangJianYi
        """
        form = "<form name=\"punchout_form\" method=\"post\" action=\""
        form += url
        form += "\">\n"
        if params:
            for k, v in params.items():
                if not v:
                    continue
                form += "<input type=\"hidden\" name=\""
                form += k
                form += "\" value=\""
                form += v.replace("\"", "&quot;")
                form += "\">\n"
        form += "<input type=\"submit\" value=\"立即支付\" style=\"display:none\" >\n"
        form += "</form>\n"
        form += "<script>document.forms[0].submit();</script>"
        return form
    
    def __key_value_url(self, data):
        """
        :description: 拼接参数
        :param data:参数字典
        :return:拼接后的字符串
        :last_editors: HuangJianYi
        """
        data.pop("sign", None)
        unsigned_items = self.__ordered_data(data)
        quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in unsigned_items)
        unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
        sign = self.get_sign(unsigned_string.encode("utf-8"))
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    def __ordered_data(self, data):
        """
        :description: 参数字典排序
        :param data:参数字典
        :param signature:签名值
        :return:排序后的字符串
        :last_editors: HuangJianYi
        """
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    def get_sign(self, data):
        """
        :description: 生成签名
        :param unsigned_string:参数拼接字符串
        :return:签名值
        :last_editors: HuangJianYi
        """
        key = self.app_private_key
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA256.new(data))
        sign = encodebytes(signature).decode("utf8").replace("\n", "")
        return sign

    def check_sign(self, data, signature):
        """
        :description: 校验签名
        :param data:参数字典
        :param signature:签名值
        :return:True签名成功 False签名失败 
        :last_editors: HuangJianYi
        """
        data.pop("sign_type")
        data.pop("sign")
        unsigned_items = self.__ordered_data(data)
        message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)
        signer = PKCS1_v1_5.new(self.alipay_public_key)
        digest = SHA256.new()
        digest.update(message.encode("utf8"))
        if signer.verify(digest, decodebytes(signature.encode("utf8"))):
            return True
        return False
