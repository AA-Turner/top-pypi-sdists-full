#!/usr/bin/env python

import os
import sys 
import socket
import json
import struct
import argparse
import xmltodict
import time
from typing import Union


PORT_TIP = 'GA服务的本机tcp端口';
COMMON_TIP = 'ga-utils get 300 --port 2004';
UTIL_NAME = 'ga-utils';


def xmltojson(xmlstr: str) -> str:
    xmlparse = xmltodict.parse(xmlstr, force_list=('GameObject', 'UWidget'))
    jsonstr = json.dumps(xmlparse,indent=1)
    return jsonstr

def deepLoop(data, child: str, callback):
    callback(data)
    if child in data:
        for item in data[child]:
            deepLoop(item, child, callback)

def getIds(data, child: str, attr: str) -> list[Union[int, str]]: 
    ids = [];
    def cb(node):
        if attr in node:
            ids.append(node[attr])
        else:
            ids.append(None)
    deepLoop(data, child, cb)
    return ids;

def handleIds(ids: list[Union[int, str]], isNumber: bool) -> list[Union[int, str]]:
    result = []
    origin = ids[1: ];
    if isNumber:
        for item in origin:
            result.append(int(item))
        return result
    else:
        return origin
def get_buffer(body: str):
    body_buffer = body.encode('UTF-8')
    head_buffer = struct.pack('<i', len(body_buffer))
    return body_buffer, head_buffer

def time_to_date(format_string="%Y-%m-%d %H:%M:%S"):
    time_stamp = int(time.time())
    time_array = time.localtime(time_stamp)
    str_date = time.strftime(format_string, time_array)
    return str_date
    
LOG_FILE = UTIL_NAME + '.' + time_to_date(format_string="%Y-%m-%d") + '.log'

def log(body):
    msg = body.decode('UTF-8')
    file = os.getcwd() + '/' + LOG_FILE
    with open(file, 'a', encoding='UTF-8') as f:
        f.write(time_to_date(format_string="%Y-%m-%d %H:%M:%S"))
        f.write(': ')
        f.write(msg)
        f.write('\n')


HOST = "127.0.0.1"  # The server's hostname or IP address
CMD_DUMP_TREE = 300
CMD_GET_POSITION = 103

cmd_tree = json.dumps({
    'cmd': CMD_DUMP_TREE,
    'value': ''
})
def dump_tree(client):
    body_buffer, head_buffer = get_buffer(cmd_tree)
    client.send(head_buffer)
    client.send(body_buffer)

def init_client(port: int, cmd: int):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try: 
        client.connect((HOST, port))
    except socket.error as e: 
        print('连接失败，请先检查' + PORT_TIP)
        print("Address-related error connecting to server: %s" % e) 
        sys.exit(1)
    print('连接成功，' + HOST + ':' + str(port))
    print('请求日志：' + LOG_FILE)
    dump_tree(client)
    data = client.recv(4)
    body_len = struct.unpack('<I', data)[0] 
    msg = client.recv(body_len)
    log(msg)
    print(msg)

    # 通过@id或者@name获取元素的位置信息
    if (cmd == CMD_GET_POSITION):
        tree_data = json.loads(msg.decode('UTF-8'))
        xml = json.loads(xmltojson(tree_data['data']['xml']))
        root = xml['AbstractRoot']
        child = 'GameObject'
        attr = '@id'
        isNumber = True
        if 'UWidget' in root:
            child = 'UWidget'
            attr = '@name'
            isNumber = False

        ids = getIds(root, child, attr)
        cmd_position = json.dumps({
            'cmd': CMD_GET_POSITION,
            'value': handleIds(ids, isNumber)
        })
        body_buffer, head_buffer = get_buffer(cmd_position)
        client.send(head_buffer)
        client.send(body_buffer)
        data = client.recv(4)
        body_len = struct.unpack('<I', data)[0] 
        msg = client.recv(body_len)
        log(msg)
        print(msg)
    

class C:
    pass

c = C()

def main():

    parser = argparse.ArgumentParser(
        prog=UTIL_NAME,
        description='通过GA协议获取数据，用于调试GA控件树。示例：' + COMMON_TIP,
        usage=COMMON_TIP
    )
    parser.add_argument('get', help='通过GA协议获取数据')
    parser.add_argument('cmd', type=int, help='协议CMD，300获取控件树名称和属性信息，103获取控件树的布局位置信息')
    parser.add_argument('-p', '--port', dest='port', type=int, help=PORT_TIP)
    args = parser.parse_args(namespace=c)
    if args.get:
        if args.port:
             init_client(int(args.port), int(args.cmd))
        else:
            print('请先指定' + PORT_TIP + '。示例：' + COMMON_TIP)
    else: 
        print(COMMON_TIP)
if __name__ == '__main__':
    main()
