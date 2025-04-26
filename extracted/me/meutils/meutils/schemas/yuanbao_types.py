#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : yuanbao_types
# @Time         : 2024/6/11 19:01
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import pandas as pd

from meutils.pipe import *

import orjson as json
from urllib.parse import quote, unquote

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=onX3Rg"

BASE_URL = "https://hunyuan.tencent.com"
YUANBAO_BASE_URL = "https://yuanbao.tencent.com"

API_CONV_DETAIL = "/api/conv"
API_LOGIN = "/api/oalogin"
API_GENERATE_ID = "/api/generate/id"
API_GENERATE_ID_V2 = "/api/v2/generate/id"

API_CONV_LIST = "/api/convs"
API_DELETE_CONV = "/api/conv/delete"
API_CLEAR_CONV = "/api/convs/clear"
API_GENERATE_TITLE = "/api/chat/title"
API_TITLE_MODIFY = "/api/conv/title"
API_PRE_CHAT = "/api/chat/prechat"
API_CHAT = "/api/chat"
API_REPEAT = "/api/chat/repeat"
API_STOP_CHAT = "/api/stop/chat"
API_STOP_CONVERSATION = "/api/stop/conversation"
API_COMPARE_STOP_CONVERSATION = "/api/stop/relation_convs"
API_SUITABLE = "/api/ai/suitable"
API_MODELS = "/api/models"
API_COMPLAIN = "/api/ai/complaint"
API_INFO_GENERAL = "/api/info/general"
API_COMPARE_DETAIL = "/api/relation/conv"
API_MODEL_LIST = "/api/models"
API_GENERATE_COS_KEY = "/api/resource/genUploadInfo"
API_GENERATE_PROMPTS = "/api/generate/prompts"
API_CHAT_SHARE = "/api/convs/share"
API_CHAT_QUOTA_INFO = "/api/query/chat/quotainfo"
API_CHAT_FEEDBACK = "/api/ai/feedback"
API_CHAT_GET_SHARE = "/api/convs/share"
API_MINIPROGRAM_QRCODE = "/api/weixin/getwxaqrcode"
API_SHORTCUT_CREATE = "/api/v2/shortcut/create"
API_SHORTCUT_DELETE = "/api/v2/shortcut/delete"
API_SHORTCUT_UPDATE = "/api/v2/shortcut/update"
API_SHORTCUT_LIST = "/api/v2/shortcut/list"
API_SHORTCUT_MOVE = "/api/v2/shortcut/move"
API_SHORTCUT_TAG_CREATE = "/api/v2/shortcut/tag/create"
API_SHORTCUT_TAG_DELETE = "/api/v2/shortcut/tag/delete"
API_SHORTCUT_TAG_LIST = "/api/v2/shortcut/tag/list"
API_SHORTCUT_TAG_UPDATE = "/api/v2/shortcut/tag/update"
API_SHORTCUT_USE_REPORT = "/api/v2/shortcut/use_report"
API_SHORTCUT_RECOMMEND_LIST = "/api/v2/shortcut/recent"
API_MASSAGE_CENTER_LIST = "/api/message_center/list"
API_UPDATE_MASSAGE_CENTER_STATUS = "/api/message_center/update"
API_CHAT_SHARE_NEW = "/api/conversations/share"
API_CHAT_GET_SHARE_NEW = "/api/conversations/share"
API_GET_INSPIRATION_TEMPLATE_DETAIL = "/api/inspirations/template"
API_GET_PRIVACY_STATUS = "/api/privacy/status"
API_SET_PRIVACY_STATUS = "/api/privacy/agree"
API_GET_GUIDE_INFO = "/api/get_guidance_info"
API_SET_GUIDE_INFO = "/api/update_guidance_info"
API_GET_THIRD_PLUGIN_LIST = "/api/third_plugin/list"
API_GET_FILE_COS_URL = "/api/resource/download"
API_CHAT_GET_3D_SHARE = "/api/3d/creations/share"
API_GET_FILE_COS_URL_V1 = "/api/resource/v1/download"
RTX_USER_SEARCH = "/rtx_proxy/query"
ADMIN_CHAT_API_CONV_DETAIL = "/api/admin/conv"
ADMIN_CHAT_API_CONV_LIST = "/api/admin/convs"
ADMIN_API_CHAT_SHARE = "/api/admin/share"
ADMIN_API_LOGIN = "/api/admin/oalogin"
ADMIN_ACTION_API_FEEDBACK_DASHBOARD = "/api/admin/stats/feedback"
ADMIN_ACTION_FEEDBACK_DATA_LIST = "/api/admin/feeds/list"
ADMIN_ACTION_FEEDBACK_DATA_DETAIL = "/api/admin/feeds"
ADMIN_ACTION_API_FEEDBACK_EXPORT = "/api/admin/feeds/export"
ADMIN_API_ACCOUNT_LIST = "/api/admin/account/list"
ADMIN_API_ACCOUNT_UPDATE = "/api/admin/account/update"
ADMIN_API_ACCOUNT_UPDATE_BATCH = "/api/admin/account/update_batch"
ADMIN_API_ACCOUNT_IMPORT_BATCH = "/api/admin/account/import_batch"
ADMIN_API_SHARE_LIST = "/api/admin/share/list"
ADMIN_API_SHARE_OVERVIEW = "/api/admin/share/overview"
ADMIN_KNOWLEDGE_FAQ_LIST = "/api/admin/domain/list"
ADMIN_KNOWLEDGE_FAQ_DETAIL = "/api/admin/domain"
ADMIN_KNOWLEDGE_FAQ_CHECK = "/api/admin/domain/check"
ADMIN_KNOWLEDGE_FAQ_ADD = "/api/admin/domain/add"
ADMIN_KNOWLEDGE_FAQ_MODIFY = "/api/admin/domain/modifyValue"
ADMIN_KNOWLEDGE_FAQ_DELETE = "/api/admin/domain/delete"
ADMIN_KNOWLEDGE_GRAPH_LIST = "/api/admin/graph/list"
ADMIN_KNOWLEDGE_GRAPH_DETAIL = "/api/admin/domain"
ADMIN_KNOWLEDGE_GRAPH_CHECK = "/api/admin/graph/check"
ADMIN_KNOWLEDGE_GRAPH_ADD = "/api/admin/graph/add"
ADMIN_KNOWLEDGE_GRAPH_MODIFY = "/api/admin/graph/modifyValue"
ADMIN_KNOWLEDGE_GRAPH_DELETE = "/api/admin/graph/delete"
ADMIN_ACTION_REPORT_DATA = "/api/admin/stats/overview"
ADMIN_DEPOSIT_API_WHITE_LIST = "/api/admin/deposit/white/list"
ADMIN_DEPOSIT_API_WHITE_ADD = "/api/admin/deposit/white/add"
ADMIN_DEPOSIT_API_WHITE_UPDATE = "/api/admin/deposit/white/update"
ADMIN_DEPOSIT_API_WHITE_DEL = "/api/admin/deposit/white/delete"
ADMIN_API_OPENAPI_AUDIT_LIST = "/api/admin/auditOpenAPI/list/admin"
ADMIN_API_OPENAPI_AUDIT_EXPORT = "/api/admin/auditOpenAPI/list/export"
ADMIN_API_OPENAPI_OBS_DEPT_LIST = "/api/admin/obs/dept/list"
ADMIN_API_OPENAPI_OBS_PRODUCT_LIST = "/api/admin/obs/product/list"
ADMIN_API_OPENAPI_OBS_UPDATE_STATUS = "/api/admin/auditOpenAPI"
ADMIN_API_OPENAPI_OBS_AUDIT_DETAIL = "/api/admin/auditOpenAPI"
ADMIN_API_INFO_GENERAL = "/api/admin/info/general"
TENCENT_GET_USER_INFO = "/api/getuserinfo"
TENCENT_GET_SHARE_AVATAR = "/api/convs/shareuserimage"
ADMIN_DOMAIN_APPROVE_LIST = "/api/admin/domain/approve/list"
ADMIN_DOMAIN_APPROVE_APPLY = "/api/admin/domain/approve/apply"
ADMIN_DOMAIN_APPROVE_KEYS = "/api/admin/domain/approve/keys"
ADMIN_OPERATION_CONFIGURATION = "/api/admin/operations"
ADMIN_OPERATION_CONFIGURATION_UPDATE = "/api/admin/operations/update"
ADMIN_BADCASE_LIST = "/api/admin/badcase/list"
ADMIN_BADCASE_DETAIL = "/api/admin/badcase"
ADMIN_BADCASE_ADD = "/api/admin/badcase/add"
ADMIN_BADCASE_CHECK = "/api/admin/badcase/check"
ADMIN_BADCASE_IMPORT = "/api/admin/badcase/import"
ADMIN_BADCASE_UPDATE = "/api/admin/badcase/update"
WX_JS_GET_SIGN = "/api/weixin/get_sign"
APP_AGENT_LIST = "/api/agent/v2/list"
API_USERINFO_SETPROFILEIMAGE = "/api/userinfo/setprofileimage"
API_USERINFO_SETNICKNAME = "/api/userinfo/setnickname"
API_USERINFO_SETGENDER = "/api/userinfo/setgender"
API_GET_USER_AGENT_LIST = "/api/user/agent/list"
API_CHAT_TEXT_CHECK = "/api/user/agent/conversation/textcheck"
API_CHAT_FILE_PARSE = "/api/resource/fileParse"
API_GET_VOICE_SDK_TOKEN = "/api/generate/voice_tmpkey"

API_LOGIN_OUT = "/api/login/logout"
API_UNREGISTER = "/api/unregister"
API_PHONE_LOGIN = "/api/login/phonelogin"
API_PHONE_CHANGE = "/api/changephonenumber"
API_WECHAT_CHANGE = "/api/changeweixin"
API_WECHAT_UNBIND = "/api/unbundleweixin"
GET_AGENT_INFO = "/api/user/agent/list"
GET_AGENT_CHAT_ID = "/api/generate/id"
GET_AGENT_CHAT = "/api/user/agent/v1/conversation"
GET_EXTERNAL_AGENT_CHAT = "/api/external/user/agent/conversation"
STOP_AGENT_CHAT = "/api/stop/chat"
CLEAR_AGENT_CONTEXT = "/api/stop/conversation"
REPEAT_AGENT_CHAT = "/api/chat/repeat"
AGENT_CHAT = "/api/chat"
HINT_PROMPT = "/api/user/agent/conversation/prompthint"
IMAGE_ASSETS_HISTORY = "/api/image/assets/get"
DELETE_IMAGE_ASSETS = "/api/image/assets/delete"
GET_AGENT_LIST = "/api/user/agent/list"
GET_PERSONAL_AGENT_LIST = "/api/agent/personal/agent/list"
SUITABLE_AGENT_CHAT = "/api/ai/suitable"
COMPLAIN_AGENT_CHAT = "/api/ai/complaint"
FEEDBACK_AGENT_CHAT = "/api/ai/feedback"
SHARE_AGENT_CHAT = "/api/conversations/share"
SHARE_AGENT_CHAT_V2 = "/api/conversations/v2/share"
GET_SHARE_MINI_QRCODE = "/api/weixin/getwxaqrcode"
GET_SHARE_IMAGE = "/api/aigc/v1/screenshot"
GET_AGENT_SHARE = "/api/conversations/share"
GET_DISCOVERY_CHAT = "/api/agent/conversation/discovery"
GET_AGENT_SQUARE_LIST = "/api/agent/list"
DELETE_AGENT = "/api/user/agent/delete"
UPDATE_AGENT = "/api/user/agent/update"
GET_AGENT_GUIDE = "/api/user/agent/v2/guide"
DELETE_AGENT_HISTORY = "/api/user/agent/conversation/clear"
GET_AGENT_RECOMMEND = "/api/agent/recommend"
GET_CHAT_LONGTEXT = "/api/conversation/longtext"
EXPORT_LONGTEXT = "/api/conversation/longtext/download"
GET_COS_URL = "/api/resource/v1/download"
GET_CHAT_LIST = "/api/convs"
GET_CHAT_DETAIL = "/api/conv"
GET_DISCOVERY_CARD = "/api/discovery/highlights"
GET_SHARE_PICBOOK = "/api/image/agent/ai_picture_book/asset/share"
GET_AGENT_FEEDS = "/api/agent/startFeeds"
GET_AGENT_TOOL_GUIDE = "/api/agent/toolsGuide"
GET_AGENT_GREETING_BASIC = "/api/homePageInfo"
GET_AGENT_GREETING_SPECIAL_COLUMN = "/api/user/agent/v3/guide"
GET_AGENT_GREETING_SPECIAL_COLUMN_DETAIL = "/api/user/agent/guide/detail"
GET_PROMPT_HINTS = "/api/user/agent/conversation/prompthint"


class SSEData(BaseModel):
    # data: {"type": "text"}
    # event: speech_type
    # data: status
    # event: speech_type
    # data: text
    # data: {"type": "text", "msg": "计算"}
    # data: {"type": "text", "msg": "结果为"}
    # data: {"type": "text", "msg": ":"}
    # data: {"type": "text", "msg": "\n"}
    # data: {"type": "text", "msg": "\n"}
    # data: {"type": "text", "msg": "1"}
    # data: {"type": "text", "msg": " +"}
    # data: {"type": "text", "msg": " "}
    # data: {"type": "text", "msg": "1"}
    # data: {"type": "text", "msg": " ="}
    # data: {"type": "text", "msg": " "}
    # data: {"type": "text", "msg": "2"}

    # data: {"type": "progress", "value": 0.1875}

    # data: {"type": "image",
    #        "imageUrlLow": "https://hunyuan-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2img/87c56543f333a5c9dff7cc4985dc84cb/20240611191629h0_bb05437fd6e3d380880af18cb8246dee.png?q-sign-algorithm=sha1\u0026q-ak=AKID0qSq0xJRL7h3A4nIYJFrFOJ1VlnbIm26\u0026q-sign-time=1718104589;1749640589\u0026q-key-time=1718104589;1749640589\u0026q-header-list=host\u0026q-url-param-list=\u0026q-signature=b8129ea17df63a7616f744fd466bf3ce00946601",
    #        "imageUrlHigh": "https://hunyuan-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2img/87c56543f333a5c9dff7cc4985dc84cb/20240611191629h0_bb05437fd6e3d380880af18cb8246dee.png?q-sign-algorithm=sha1\u0026q-ak=AKID0qSq0xJRL7h3A4nIYJFrFOJ1VlnbIm26\u0026q-sign-time=1718104589;1749640589\u0026q-key-time=1718104589;1749640589\u0026q-header-list=host\u0026q-url-param-list=\u0026q-signature=b8129ea17df63a7616f744fd466bf3ce00946601",
    #        "seed": 2452899368,
    #        "prompt": "画一条可爱的小狗，它有着毛茸茸的外表和充满活力的眼神，它正在一个安逸的家里玩耍，背景是舒适的沙发和视图玩具，这张画的风格是生动和活泼，构图使得小狗看起来非常可爱"}
    # data: {"type": "text",
    #        "msg": "AI生成完成，如想继续做画，请继续完整描述需求，如：请帮我生成一张图片：轻舟已过万重山，水墨画风格"}

    # data: [plugin:]
    # data: [MSGINDEX:24]
    # data: {"type": "meta", "messageId": "676eff07-56e5-4e11-8568-181a94f0f2e5_24", "index": 24,
    #        "replyId": "676eff07-56e5-4e11-8568-181a94f0f2e5_23", "replyIndex": 23,
    #        "traceId": "be3839b9012cbd49e7a67434093adfdf", "guideId": 0, "unSupportRepeat": false}
    # data: [TRACEID:be3839b9012cbd49e7a67434093adfdf]
    # data: [DONE]

    content: str = ""
    reasoning_content: str = ""
    search_content: str = ""

    image: Optional[str] = None

    chunk: str = ""

    def __init__(self, **data):
        super().__init__(**data)

        # logger.debug(self.chunk)

        chunk = self.chunk.lstrip("data:")

        content = ""
        if '"type":"progress"' in chunk:
            content = json.loads(chunk).get("msg", "")

        elif '{"type":"image"' in chunk:
            chunk = json.loads(chunk)
            prompt = chunk.get("prompt", "")
            url = unquote(chunk.get("imageUrlHigh", ""))
            self.image = url

            content = f"![{prompt}]({url})\n\n"

        elif '{"type":"text"' in chunk:
            content = json.loads(chunk).get("msg", "")
        #
        # elif '{"type":"card"' in self.data:
        #     pass

        # df['title'] = "[" + df['title'] + "](" + df['url'] + ")"
        # df['image'] = "![](" + df['image'] + ")"

        elif '{"type":"think"' in chunk:  # 思考中...
            self.reasoning_content = json.loads(chunk).get("content", "")

        elif '{"type":"searchGuid"' in chunk:  # 思考中...
            self.search_content = json.loads(chunk).get("docs", "")

        self.content = content


if __name__ == '__main__':
    data = """data: {"type": "text", "msg": "计算"}"""
    print(SSEData(chunk=data))
