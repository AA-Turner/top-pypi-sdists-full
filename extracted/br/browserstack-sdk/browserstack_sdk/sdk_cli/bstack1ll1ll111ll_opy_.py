# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack1lll1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import (
    bstack1lll1llllll_opy_,
    bstack1llllll1l1l_opy_,
    bstack1lll1llll11_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1ll1ll1llll_opy_ import bstack1ll1lll1l1l_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l1111l1l1_opy_
from bstack_utils.helper import bstack1llll1ll1l1_opy_
import threading
import os
import urllib.parse
class bstack1ll1ll111l1_opy_(bstack1lll1lllll1_opy_):
    def __init__(self, bstack1llll1ll11l_opy_):
        super().__init__()
        bstack1ll1lll1l1l_opy_.bstack1lllll1llll_opy_((bstack1lll1llllll_opy_.bstack1ll1ll1ll1l_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1ll1l1ll1ll_opy_)
        bstack1ll1lll1l1l_opy_.bstack1lllll1llll_opy_((bstack1lll1llllll_opy_.bstack1ll1ll1ll1l_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1ll1l1lllll_opy_)
        bstack1ll1lll1l1l_opy_.bstack1lllll1llll_opy_((bstack1lll1llllll_opy_.bstack1ll1l1ll11l_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1ll1l1l11l1_opy_)
        bstack1ll1lll1l1l_opy_.bstack1lllll1llll_opy_((bstack1lll1llllll_opy_.bstack1llll1lll11_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1ll1ll11l1l_opy_)
        bstack1ll1lll1l1l_opy_.bstack1lllll1llll_opy_((bstack1lll1llllll_opy_.bstack1ll1ll1ll1l_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1ll1l1l1lll_opy_)
        bstack1ll1lll1l1l_opy_.bstack1lllll1llll_opy_((bstack1lll1llllll_opy_.QUIT, bstack1llllll1l1l_opy_.PRE), self.on_close)
        self.bstack1llll1ll11l_opy_ = bstack1llll1ll11l_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1l1ll1ll_opy_(
        self,
        f: bstack1ll1lll1l1l_opy_,
        bstack1ll1l1l1l11_opy_: object,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1111_opy_ (u"ࠥࡰࡦࡻ࡮ࡤࡪࠥᅒ"):
            return
        if not bstack1llll1ll1l1_opy_():
            self.logger.debug(bstack11l1111_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡰࡦࡻ࡮ࡤࡪࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᅓ"))
            return
        def wrapped(bstack1ll1l1l1l11_opy_, launch, *args, **kwargs):
            response = self.bstack1ll1ll1111l_opy_(f.platform_index, instance.ref(), json.dumps({bstack11l1111_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᅔ"): True}).encode(bstack11l1111_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᅕ")))
            if response is not None and response.capabilities:
                if not bstack1llll1ll1l1_opy_():
                    browser = launch(bstack1ll1l1l1l11_opy_)
                    return browser
                bstack1ll1l1llll1_opy_ = json.loads(response.capabilities.decode(bstack11l1111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᅖ")))
                if not bstack1ll1l1llll1_opy_: # empty caps bstack1ll1l1lll1l_opy_ bstack1ll1ll11lll_opy_ bstack1ll1ll11111_opy_ bstack1ll1l1ll1l1_opy_ or error in processing
                    return
                bstack1ll1l1l11ll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1ll1l1llll1_opy_))
                f.bstack1llll111l11_opy_(instance, bstack1ll1lll1l1l_opy_.bstack1ll1ll1l111_opy_, bstack1ll1l1l11ll_opy_)
                f.bstack1llll111l11_opy_(instance, bstack1ll1lll1l1l_opy_.bstack1ll1ll11l11_opy_, bstack1ll1l1llll1_opy_)
                browser = bstack1ll1l1l1l11_opy_.connect(bstack1ll1l1l11ll_opy_)
                return browser
        return wrapped
    def bstack1ll1l1l11l1_opy_(
        self,
        f: bstack1ll1lll1l1l_opy_,
        Connection: object,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1111_opy_ (u"ࠣࡦ࡬ࡷࡵࡧࡴࡤࡪࠥᅗ"):
            self.logger.debug(bstack11l1111_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡦ࡬ࡷࡵࡧࡴࡤࡪࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᅘ"))
            return
        if not bstack1llll1ll1l1_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack11l1111_opy_ (u"ࠪࡴࡦࡸࡡ࡮ࡵࠪᅙ"), {}).get(bstack11l1111_opy_ (u"ࠫࡧࡹࡐࡢࡴࡤࡱࡸ࠭ᅚ")):
                    bstack1ll1l1lll11_opy_ = args[0][bstack11l1111_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧᅛ")][bstack11l1111_opy_ (u"ࠨࡢࡴࡒࡤࡶࡦࡳࡳࠣᅜ")]
                    session_id = bstack1ll1l1lll11_opy_.get(bstack11l1111_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡊࡦࠥᅝ"))
                    f.bstack1llll111l11_opy_(instance, bstack1ll1lll1l1l_opy_.bstack1ll1l1l1ll1_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack11l1111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡥ࡫ࡶࡴࡦࡺࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠣࠦᅞ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1ll1l1l1lll_opy_(
        self,
        f: bstack1ll1lll1l1l_opy_,
        bstack1ll1l1l1l11_opy_: object,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1111_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࠥᅟ"):
            return
        if not bstack1llll1ll1l1_opy_():
            self.logger.debug(bstack11l1111_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡦࡳࡳࡴࡥࡤࡶࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᅠ"))
            return
        def wrapped(bstack1ll1l1l1l11_opy_, connect, *args, **kwargs):
            response = self.bstack1ll1ll1111l_opy_(f.platform_index, instance.ref(), json.dumps({bstack11l1111_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᅡ"): True}).encode(bstack11l1111_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᅢ")))
            if response is not None and response.capabilities:
                bstack1ll1l1llll1_opy_ = json.loads(response.capabilities.decode(bstack11l1111_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᅣ")))
                if not bstack1ll1l1llll1_opy_:
                    return
                bstack1ll1l1l11ll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1ll1l1llll1_opy_))
                if bstack1ll1l1llll1_opy_.get(bstack11l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᅤ")):
                    browser = bstack1ll1l1l1l11_opy_.bstack1ll1l1ll111_opy_(bstack1ll1l1l11ll_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1ll1l1l11ll_opy_
                    return connect(bstack1ll1l1l1l11_opy_, *args, **kwargs)
        return wrapped
    def bstack1ll1l1lllll_opy_(
        self,
        f: bstack1ll1lll1l1l_opy_,
        bstack1ll1lll11l1_opy_: object,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1111_opy_ (u"ࠣࡰࡨࡻࡤࡶࡡࡨࡧࠥᅥ"):
            return
        if not bstack1llll1ll1l1_opy_():
            self.logger.debug(bstack11l1111_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡰࡨࡻࡤࡶࡡࡨࡧࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᅦ"))
            return
        def wrapped(bstack1ll1lll11l1_opy_, bstack1ll1ll11ll1_opy_, *args, **kwargs):
            contexts = bstack1ll1lll11l1_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack11l1111_opy_ (u"ࠥࡥࡧࡵࡵࡵ࠼ࡥࡰࡦࡴ࡫ࠣᅧ") in page.url:
                                    return page
                    else:
                        return bstack1ll1ll11ll1_opy_(bstack1ll1lll11l1_opy_)
        return wrapped
    def bstack1ll1ll1111l_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack11l1111_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࠤᅨ") + str(req) + bstack11l1111_opy_ (u"ࠧࠨᅩ"))
        try:
            r = self.bstack1lll1llll1l_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11l1111_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࠤᅪ") + str(r.success) + bstack11l1111_opy_ (u"ࠢࠣᅫ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1111_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᅬ") + str(e) + bstack11l1111_opy_ (u"ࠤࠥᅭ"))
            traceback.print_exc()
            raise e
    def bstack1ll1ll11l1l_opy_(
        self,
        f: bstack1ll1lll1l1l_opy_,
        Connection: object,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1111_opy_ (u"ࠥࡣࡸ࡫࡮ࡥࡡࡰࡩࡸࡹࡡࡨࡧࡢࡸࡴࡥࡳࡦࡴࡹࡩࡷࠨᅮ"):
            return
        if not bstack1llll1ll1l1_opy_():
            return
        def wrapped(Connection, bstack1ll1l1l1l1l_opy_, *args, **kwargs):
            return bstack1ll1l1l1l1l_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1ll1lll1l1l_opy_,
        bstack1ll1l1l1l11_opy_: object,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1111_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࠥᅯ"):
            return
        if not bstack1llll1ll1l1_opy_():
            self.logger.debug(bstack11l1111_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡨࡲ࡯ࡴࡧࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᅰ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped