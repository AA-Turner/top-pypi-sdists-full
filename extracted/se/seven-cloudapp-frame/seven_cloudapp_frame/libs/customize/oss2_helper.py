# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-15 11:30:45
@LastEditTime: 2023-08-15 09:58:31
@LastEditors: HuangJianYi
@Description: 
"""
import oss2
import os
from seven_framework import *
from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.libs.customize.file_helper import *


class OSS2Helper:
    """
    :description: 阿里云存储帮助类 上传文件、数据导入excel并返回下载地址
    :param {type} 
    :return: 
    :last_editors: HuangJianYi
    """
    @classmethod
    def upload(self, file_name, local_file='', folder='', is_auto_name=True, data=None):
        """
        :description: 上传文件
        :param file_name：文件名称
        :param local_file：本地文件地址
        :param folder：本地文件地址
        :param is_auto_name：是否生成随机文件名
        :param data：需要上传的数据
        :return: 
        :last_editors: HuangJianYi
        """
        return OSSHelper.upload(file_name, local_file, folder, is_auto_name, data)

    @classmethod
    def export_excel(self, import_data):
        """
        :description: 把数据导入excel并返回下载地址
        :param import_data:导入数据
        :return excel下载地址
        :last_editors: HuangJianYi
        """
        return OSSHelper.export_excel(import_data)