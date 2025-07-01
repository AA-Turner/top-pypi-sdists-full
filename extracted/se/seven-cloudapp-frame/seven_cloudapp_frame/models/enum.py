# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2020-06-02 14:32:40
@LastEditTime: 2025-07-01 10:15:27
@LastEditors: HuangJianYi
:description: 枚举类
"""

from enum import Enum
from enum import unique


@unique
class QueueupOperateType(Enum):
    """
    :description: 排队系统操作类型
    """
    join = 1  #加入
    line_up = 2  #排到
    lottery = 3  #抽奖
    auto_exit = 4  #自动退出
    manual_exit = 5  #手动退出


@unique
class PlatType(Enum):
    """
    :description: 平台类型
    """
    tb = 1 #淘宝
    wx = 2 #微信
    dy = 3 #抖音
    web = 4 #站点
    jd = 5 #京东

@unique
class PageCountMode(Enum):
    """
    :description: 分页模式
    """
    none = 0 #无
    total = 1 #总数
    next = 2 #是否有下一页

@unique
class OperationType(Enum):
    """
    :description: 用户操作日志类型
    """
    add = 1 #新增
    update = 2 #编辑
    delete = 3 #删除
    review = 4 #还原
    copy = 5 #复制
    export = 6 #导出
    import_data = 7 #导入
    release = 8 #上架
    un_release = 9 #下架
    operate = 10 #操作


@unique
class FileStorageType(Enum):
    """
    :description: 文件存储类型
    """
    oss = 1  #阿里云
    cos = 2  #腾讯云
    bos = 3  #百度云


@unique
class SmsType(Enum):
    """
    :description: 短信渠道类型
    """
    ali = 1  #阿里云
    tencent = 2  #腾讯云
    bce = 3  #百度云

@unique
class UserType(Enum):
    """
    :description: 用户类型
    """
    product = 0  #产品用户
    app = 1  #应用用户
    act = 2  #活动用户


@unique
class TaskRewardType(Enum):
    """
    :description: 任务奖励类型
    """
    asset = 1 #资产
    prize = 2 #奖品
    card = 3 #卡片

@unique
class TaskCompleteType(Enum):
    """
    :description: 任务完成类型
    """
    day = 1 #每日任务
    week = 2 #每周任务
    month = 4 #每月任务
    long = 3 #持久任务

@unique
class TaskType(Enum):
    """
    docstring：任务类型 业务的自定义任务类型从201起
    """
    # 掌柜有礼、免费领取、新人有礼，格式：{"reward_value":0,"asset_object_id":""}  字段说明：reward_value:奖励值 asset_object_id:资产对象标识
    free_gift = 1
    # 单次签到，格式：{"reward_value":0,"asset_object_id":""}  字段说明：reward_value:奖励值 asset_object_id:资产对象标识
    one_sign = 2
    # 每周签到(指定天数签到)，格式：{"day_list":[{'day': 1, 'reward_value': 1}, {'day': 2, 'reward_value': 1}, {'day': 3, 'reward_value': 1}, {'day': 4, 'reward_value': 1}, {'day': 5, 'reward_value': 1}, {'day': 6, 'reward_value': 1}, {'day': 7, 'reward_value': 1}],"asset_object_id":""}  字段说明：day_array:每天奖励配置列表 asset_object_id:资产对象标识
    weekly_sign = 3
    # 邀请新用户，格式：{"reward_value":0,"satisfy_num":1,"limit_num":0,"asset_object_id":""} 字段说明：reward_value:奖励值 satisfy_num:满足数 limit_num:限制人数 asset_object_id:资产对象标识
    invite_new_user = 4
    # 邀请入会，格式：{"reward_value":0,"satisfy_num":1,"limit_num":0,"asset_object_id":""}  字段说明：reward_value:奖励值 satisfy_num:满足数 limit_num:限制人数 asset_object_id:资产对象标识
    invite_join_member = 5
    # 关注店铺，格式：{"reward_value":0,"once_favor_reward":0,"asset_object_id":""} 字段说明：reward_value:奖励值 once_favor_reward:已关注是否奖励1是0否 asset_object_id:资产对象标识
    favor_store = 6
    # 加入店铺会员，格式：{"reward_value":0,"once_member_reward":0,"asset_object_id":""} 字段说明：reward_value:奖励值 once_member_reward:已入会是否奖励1是0否 asset_object_id:资产对象标识
    join_member = 7
    # 收藏商品，格式：{"reward_value":0,"satisfy_num":1,"limit_num":0,"goods_ids":"","goods_list":[],"asset_object_id":""} 字段说明：reward_value:奖励值 satisfy_num:满足数 asset_object_id:资产对象标识 limit_num:完成限制数 goods_ids:商品ID串 goods_list:商品列表
    collect_goods = 8
    # 浏览商品，格式：{"reward_value":0,"satisfy_num":1,"limit_num":0,"goods_ids":"","goods_list":[],"asset_object_id":""} 字段说明：reward_value:奖励值 satisfy_num:满足数 asset_object_id:资产对象标识 limit_num:完成限制数 goods_ids:商品ID串 goods_list:商品列表
    browse_goods = 9
    # 浏览店铺(进店逛逛)，格式：{"reward_value":0,"satisfy_num":1,"limit_num":0,"asset_object_id":""} 或者 [{"id":1,"reward_value":0,"satisfy_num":1,"limit_num":0,"asset_object_id":""}] 字段说明：reward_value:奖励值 satisfy_num:满足数 limit_num:完成限制数 asset_object_id:资产对象标识
    browse_store = 10
    # 浏览直播间(观看直播间)，格式：{"reward_value":0,"satisfy_num":1,"limit_num":0,"link_url":"","asset_object_id":""} 或者 [{"id":1,"reward_value":0,"satisfy_num":1,"limit_num":0,"link_url":"","asset_object_id":""}] 字段说明：reward_value:奖励值 link_url:链接地址 satisfy_num:满足数 limit_num:完成限制数 asset_object_id:资产对象标识
    browse_live_room = 11
    # 浏览会场/专题，格式：[{"id":"","reward_value":0,"link_url":"","satisfy_num":1,"limit_num":1,"asset_object_id":""}] 字段说明：id:子任务类型,必填 reward_value:奖励值 satisfy_num:满足数  link_url:链接地址 asset_object_id:资产对象标识 limit_num:完成限制数
    browse_special_topic = 12
    # 累计签到，格式：{"day_list":[{'day': 1, 'reward_value': 1}, {'day': 2, 'reward_value': 1}],"asset_object_id":""} 字段说明： day_list:每天奖励配置列表 asset_object_id:资产对象标识
    cumulative_sign = 13
    # 分享，格式：{"reward_value":0,"satisfy_num":1,"limit_num":0,"asset_object_id":""} 字段说明：reward_value:奖励值 satisfy_num:满足数 limit_num:完成限制数 asset_object_id:资产对象标识
    share = 14
    # 邀请用户助力(不判断是否新用户，可重复邀请)，格式：{"reward_value":0,"satisfy_num":1,"limit_num":0,"asset_object_id":""} 字段说明：reward_value:奖励值 satisfy_num:满足数 limit_num:限制人数 asset_object_id:资产对象标识
    invite_user_help = 15
    # 神秘暗号，格式：{"reward_value":0,"secret_code":"","asset_object_id":""} 字段说明：reward_value:奖励值 secret_code:暗号 asset_object_id:资产对象标识
    secret_code = 16
    # 店铺会员积分兑换资产，格式：{"reward_value":1,"satisfy_num":1,"limit_num":1} 字段说明：reward_value:奖励值 satisfy_num:需要的积分 limit_num:完成限制数
    crm_point_exchange_asset = 17
    # 连续签到（天数是连续递增），格式：{"day_list":[{'day': 1, 'reward_value': 1}, {'day': 2, 'reward_value': 1}],"asset_object_id":""} 字段说明： day_list:每天奖励配置列表 asset_object_id:资产对象标识
    successive_sign = 18
    # 购买指定商品，格式：{"reward_value":0,"satisfy_num":1,"limit_num":0,"goods_ids":"","goods_list":[],"asset_object_id":""} 字段说明：reward_value:奖励值 satisfy_num:满足数 asset_object_id:资产对象标识 limit_num:完成限制数 goods_ids:商品ID串 goods_list:商品列表
    buy_appoint_goods = 19
    # 购买指定商品每多少金额，格式：{"reward_value":0,"satisfy_num":1,"limit_num":0,"goods_ids":"","goods_list":[],"asset_object_id":""} 字段说明：reward_value:奖励值 satisfy_num:满足数 asset_object_id:资产对象标识 limit_num:完成限制数 goods_ids:商品ID串 goods_list:商品列表
    buy_appoint_goods_price = 20
    # 购买指定商品档位金额任务，格式：{"gear_list":[{"id":1,"gear":0,"reward_type":1,"reward_name":"","asset_object_id":"","reward_value":1}],"goods_ids":"","goods_list":[]} 字段说明：id:前端生成的唯一标识 gear:档位阀值 reward_value:奖励值(等于0无法领取) reward_type:奖励类型 reward_name:奖励奖品名称 asset_object_id:对象标识(如果奖励类型是资产对应资产对象标识，如果是奖品对应奖品标识，如果是卡片对应卡片标识) goods_ids:商品ID串 goods_list:商品列表
    buy_appoint_goods_price_gear = 21
    # 购买全店商品每多少金额，格式：{"reward_value":0,"satisfy_num":1,"limit_num":0,"goods_ids":"","goods_list":[],"asset_object_id":""} 字段说明：reward_value:奖励值 satisfy_num:满足数 asset_object_id:资产对象标识 limit_num:完成限制数 goods_ids:排除的商品ID串 goods_list:排除的商品列表
    buy_store_price = 22
    # 购买全店商品档位金额任务，格式：{"gear_list":[{"id":1,"gear":0,"reward_type":1,"reward_name":"","asset_object_id":"","reward_value":1}],"goods_ids":"","goods_list":[]} 字段说明：id:前端生成的唯一标识 gear:档位阀值 reward_value:奖励值(等于0无法领取) reward_type:奖励类型 reward_name:奖励奖品名称 asset_object_id:对象标识(如果奖励类型是资产对应资产对象标识，如果是奖品对应奖品标识，如果是卡片对应卡片标识)  goods_ids:排除的商品ID串 goods_list:排除的商品列表
    buy_store_price_gear = 23
    # 每多少次抽盒/抽包/抽奖，格式：{"reward_value":0,"satisfy_num":1,"limit_num":0,"asset_object_id":""}  字段说明：reward_value:奖励值 satisfy_num:满足数（当大于1时才需要配置字段） limit_num:完成限制数 asset_object_id:资产对象标识
    lottery = 24
    #试抽，格式：{"reward_value":0,"limit_num":0,"asset_object_id":""}  字段说明：reward_value:奖励值 satisfy_num:满足数（当大于1时才需要配置字段） limit_num:完成限制数 asset_object_id:资产对象标识
    lottery_try = 25
    # 抽盒/抽包-档位任务，格式：{"gear_list":[{"id":1,"gear":0,"reward_type":1,"reward_name":"","asset_object_id":"","reward_value":1}]} 字段说明：id:前端生成的唯一标识 gear:档位阀值 reward_value:奖励值(等于0无法领取) reward_type:奖励类型 reward_name:奖励奖品名称 asset_object_id:对象标识(如果奖励类型是资产对应资产对象标识，如果是奖品对应奖品标识，如果是卡片对应卡片标识)
    lottery_gear = 26
