# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 09:58:28 2023

@author: zlf
"""

import os
import email
import imaplib
import time
from email.utils import parseaddr,parsedate
from email.header import decode_header


# 自动生成文件名
def auto_file_name(file_name, local_path):
    try:
        # 分割文件名，反回其文件名和扩展名组成的元组
        name_suffix = os.path.splitext(file_name)
        num = 1
        while True:
            # 重新拼接文件名
            filename = f"{local_path}/{name_suffix[0]}({num}){name_suffix[-1]}"  # file(1).txt
            # 判断本地是否存在该文件
            isFile = os.path.isfile(filename)
            if isFile:
                num += 1
            else:
                break
        return filename
    except Exception as e:
        raise Exception(f"自动生成文件名发生异常抛出，原因：{e}")

# 字符编码转换
def decode_str(str_in):
    value, charset = decode_header(str_in)[0]
    if charset:
        value = value.decode(charset)
    return value

# def get_att(msg, savePath, subject):
#     for part in msg.walk():
#         if part.get_content_maintype() == 'multipart':
#             continue
#         # if part.get_content_maintype() == 'application':
#         #     continue
#         if part.get('Content-Disposition') is None:
#             continue
#         fileName = part.get_filename()
#         # 如果文件名为纯数字、字母时不需要解码，否则需要解码
#
#         # try:
#         #     fileName = decode_header(fileName)[0][0].decode(decode_header(fileName)[0][1])
#         # except Exception as e:
#         #     print(fileName, str(e), sep='>>>')
#
#
#         if fileName:
#             # emailPath = os.path.join(savePath, subject)
#             # if not os.path.exists(emailPath):
#             #     os.makedirs(emailPath)
#             filePath = os.path.join(savePath, fileName)
#             try:
#                 fp = open(filePath, 'wb')
#                 fp.write(part.get_payload(decode=True))
#                 fp.close()
#             except Exception as e:
#                 print(subject, str(e), sep='>>>')
#                 pass
#     return

def get_att(msg,savePath,subject):
    print("正在读取:"+subject)
    for part in msg.walk():
        fileName = part.get_filename()
        h = email.header.Header(fileName)
        dh = email.header.decode_header(h)
        if dh:
            filename = dh[0][0]
            filename = decode_str(str(filename, dh[0][1]))
            # print(filename)
            if os.path.splitext(filename)[-1] == '.xlsx' or os.path.splitext(filename)[-1] == '.xls':
                filePath = os.path.join(savePath, filename)
                # if not os.path.exists(filePath):
                data = part.get_payload(decode=True)
                fp = open(filePath, 'wb')
                fp.write(data)
                fp.close()
    return

def get_email(json_dict):
    try:
        emailType = json_dict["emailType"]  # 邮箱类型
        emailAddress = json_dict["emailAddress"]  # 邮箱账号
        emailPassword = json_dict["emailPassword"]  # 用户密码，授权码
        emailCount = json_dict["emailCount"]  # 邮件数量
        isReadEmail = json_dict["isReadEmail"]  # 是否仅未读邮件
        isSaveAttachment = json_dict["isSaveAttachment"]  # 是否保存附件
        savePath = json_dict["savePath"]
        startTime = json_dict['startTime']
        endTime = json_dict['endTime']
        smtpData = {
            "0": "imap.qq.com",  # qq邮箱
            "1": "imap.126.com",  # 126 邮箱
            "2": "imap.163.com",  # 163 邮箱
            "3": "mail.nesc.cn"
        }
        if emailType in ["0", "1", "2","3"]:
            mailHost = smtpData[emailType]
        else:
            raise Exception("暂时不支持该邮箱服务器，请重新选择新的邮箱服务器")

        if emailType == "2" or emailType == "1":
            imaplib.Commands['ID'] = 'AUTH'
            server = imaplib.IMAP4_SSL(mailHost)
            server.login(emailAddress, emailPassword)
            # 此处用于规避163和126获取邮件时会报错
            args = ("name", emailAddress, "contact", emailAddress, "version", "1.0.0", "vendor", "myclient")
            typ, dat = server._simple_command('ID', '("' + '" "'.join(args) + '")')
        else:
            # 连接pop服务器。如果没有使用SSL，将IMAP4_SSL()改成IMAP4()即可其他都不需要做改动
            server = imaplib.IMAP4(mailHost)
            # 登录--发送者账号和口令
            server.login(emailAddress, emailPassword)

        # 邮箱中的文件夹，默认为'INBOX'
        inbox = server.select("INBOX")
        # 是否仅未读邮件
        if isReadEmail:
            # 搜索匹配的邮件，第一个参数是字符集，None默认就是ASCII编码，第二个参数是查询条件，这里的ALL就是查找全部 UnSeen:未读邮件
            type1, emailData = server.search(None, "UnSeen")
        else:
            type1, emailData = server.search(None, "All")
        # 邮件列表,使用空格分割得到邮件索引
        msgList = emailData[0].split()
        msgList.reverse()

        for msg in msgList:
            type1, datas = server.fetch(msg, '(RFC822)')
            message = email.message_from_bytes(datas[0][1])
            # 获取标题
            subject = decode_str(message.get('subject'))
            mail_dt = message.get('date')
            date = time.strftime("%Y-%m-%d %H:%M:%S", parsedate(mail_dt))
            if date>=startTime and date<=endTime:
                if isSaveAttachment:
                    if savePath is None or savePath == "":
                        #如果没给保存路径，给与一个默认路径,不进行报错提示
                        savePath='../data'
                        # raise Exception("附件保存目录为空，请检查附件保存目录是否输入正确")
                    try:
                        get_att(message, savePath, subject)
                    except Exception as e:
                        print(str(e))
            elif date>endTime:
                continue
            elif date<startTime:
                # 倒序读邮件，如果时间下于开始时间，那么后面的邮件都不需要读了，直接终止程序
                break
        # 关闭连接
        server.close()
        print('嘿！！  下载好了呦！！<(￣︶￣)↗[GO!]')
    except Exception as e:
        print(str(e))
        # raise Exception(f'接收邮件异常抛出，原因: {e}')
    return
if __name__ == '__main__':
    json_dict={
        'emailType':'3',
        'emailAddress': '邮箱账号',
        'emailPassword': '密码',
        'emailCount': '',     # 邮件数量
        'isReadEmail': False, # 是否仅未读邮件
        'isSaveAttachment':True,# 是否保存附件
        'savePath': '../data',  # 保存目录
        'startTime':'2023-08-31 00:00:00', # 时间范围
        'endTime': '2023-09-07 15:00:00', # 时间范围
    }
    get_email(json_dict)
