# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll1llll11l_opy_ import bstack1lll1lll111_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1ll1l_opy_ import (
    bstack1lllll11111_opy_,
    bstack1llll1lllll_opy_,
    bstack1llllllll1l_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1ll1ll11l1l_opy_ import bstack1ll1lll1lll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1ll111l1_opy_
from bstack_utils.helper import bstack1l1ll1l1l1l_opy_
import threading
import os
import urllib.parse
class bstack1ll1ll111ll_opy_(bstack1lll1lll111_opy_):
    def __init__(self, bstack1lll1l11111_opy_):
        super().__init__()
        bstack1ll1lll1lll_opy_.bstack1ll111lll1l_opy_((bstack1lllll11111_opy_.bstack1lllll1ll11_opy_, bstack1llll1lllll_opy_.PRE), self.bstack1l1l111l1l1_opy_)
        bstack1ll1lll1lll_opy_.bstack1ll111lll1l_opy_((bstack1lllll11111_opy_.bstack1lllll1ll11_opy_, bstack1llll1lllll_opy_.PRE), self.bstack1l1l11l111l_opy_)
        bstack1ll1lll1lll_opy_.bstack1ll111lll1l_opy_((bstack1lllll11111_opy_.bstack1lllll1lll1_opy_, bstack1llll1lllll_opy_.PRE), self.bstack1l1l11l11l1_opy_)
        bstack1ll1lll1lll_opy_.bstack1ll111lll1l_opy_((bstack1lllll11111_opy_.bstack1llll1lll11_opy_, bstack1llll1lllll_opy_.PRE), self.bstack1l1l11l1111_opy_)
        bstack1ll1lll1lll_opy_.bstack1ll111lll1l_opy_((bstack1lllll11111_opy_.bstack1lllll1ll11_opy_, bstack1llll1lllll_opy_.PRE), self.bstack1l1l11ll1ll_opy_)
        bstack1ll1lll1lll_opy_.bstack1ll111lll1l_opy_((bstack1lllll11111_opy_.QUIT, bstack1llll1lllll_opy_.PRE), self.on_close)
        self.bstack1lll1l11111_opy_ = bstack1lll1l11111_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l111l1l1_opy_(
        self,
        f: bstack1ll1lll1lll_opy_,
        bstack1l1l11ll11l_opy_: object,
        exec: Tuple[bstack1llllllll1l_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1111l1l_opy_ (u"ࠥࡰࡦࡻ࡮ࡤࡪࠥዶ"):
            return
        if not bstack1l1ll1l1l1l_opy_():
            self.logger.debug(bstack1111l1l_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡰࡦࡻ࡮ࡤࡪࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣዷ"))
            return
        def wrapped(bstack1l1l11ll11l_opy_, launch, *args, **kwargs):
            response = self.bstack1l1l111l1ll_opy_(f.platform_index, instance.ref(), json.dumps({bstack1111l1l_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫዸ"): True}).encode(bstack1111l1l_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧዹ")))
            if response is not None and response.capabilities:
                if not bstack1l1ll1l1l1l_opy_():
                    browser = launch(bstack1l1l11ll11l_opy_)
                    return browser
                bstack1l1l11l1l1l_opy_ = json.loads(response.capabilities.decode(bstack1111l1l_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨዺ")))
                if not bstack1l1l11l1l1l_opy_: # empty caps bstack1l1l11l1ll1_opy_ bstack1l1l11ll111_opy_ bstack1l1l111l11l_opy_ bstack1llll11l111_opy_ or error in processing
                    return
                bstack1l1l11l11ll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l11l1l1l_opy_))
                f.bstack1lllllllll1_opy_(instance, bstack1ll1lll1lll_opy_.bstack1l1l111ll11_opy_, bstack1l1l11l11ll_opy_)
                f.bstack1lllllllll1_opy_(instance, bstack1ll1lll1lll_opy_.bstack1l1l111ll1l_opy_, bstack1l1l11l1l1l_opy_)
                browser = bstack1l1l11ll11l_opy_.connect(bstack1l1l11l11ll_opy_)
                return browser
        return wrapped
    def bstack1l1l11l11l1_opy_(
        self,
        f: bstack1ll1lll1lll_opy_,
        Connection: object,
        exec: Tuple[bstack1llllllll1l_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1111l1l_opy_ (u"ࠣࡦ࡬ࡷࡵࡧࡴࡤࡪࠥዻ"):
            self.logger.debug(bstack1111l1l_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡦ࡬ࡷࡵࡧࡴࡤࡪࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣዼ"))
            return
        if not bstack1l1ll1l1l1l_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1111l1l_opy_ (u"ࠪࡴࡦࡸࡡ࡮ࡵࠪዽ"), {}).get(bstack1111l1l_opy_ (u"ࠫࡧࡹࡐࡢࡴࡤࡱࡸ࠭ዾ")):
                    bstack1l1l11ll1l1_opy_ = args[0][bstack1111l1l_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧዿ")][bstack1111l1l_opy_ (u"ࠨࡢࡴࡒࡤࡶࡦࡳࡳࠣጀ")]
                    session_id = bstack1l1l11ll1l1_opy_.get(bstack1111l1l_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡊࡦࠥጁ"))
                    f.bstack1lllllllll1_opy_(instance, bstack1ll1lll1lll_opy_.bstack1l1l111llll_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡥ࡫ࡶࡴࡦࡺࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠣࠦጂ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1l11ll1ll_opy_(
        self,
        f: bstack1ll1lll1lll_opy_,
        bstack1l1l11ll11l_opy_: object,
        exec: Tuple[bstack1llllllll1l_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1111l1l_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࠥጃ"):
            return
        if not bstack1l1ll1l1l1l_opy_():
            self.logger.debug(bstack1111l1l_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡦࡳࡳࡴࡥࡤࡶࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣጄ"))
            return
        def wrapped(bstack1l1l11ll11l_opy_, connect, *args, **kwargs):
            response = self.bstack1l1l111l1ll_opy_(f.platform_index, instance.ref(), json.dumps({bstack1111l1l_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪጅ"): True}).encode(bstack1111l1l_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦጆ")))
            if response is not None and response.capabilities:
                bstack1l1l11l1l1l_opy_ = json.loads(response.capabilities.decode(bstack1111l1l_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧጇ")))
                if not bstack1l1l11l1l1l_opy_:
                    return
                bstack1l1l11l11ll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l11l1l1l_opy_))
                if bstack1l1l11l1l1l_opy_.get(bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ገ")):
                    browser = bstack1l1l11ll11l_opy_.bstack1l1l11l1l11_opy_(bstack1l1l11l11ll_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1l11l11ll_opy_
                    return connect(bstack1l1l11ll11l_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1l11l111l_opy_(
        self,
        f: bstack1ll1lll1lll_opy_,
        bstack1l1llll11ll_opy_: object,
        exec: Tuple[bstack1llllllll1l_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1111l1l_opy_ (u"ࠣࡰࡨࡻࡤࡶࡡࡨࡧࠥጉ"):
            return
        if not bstack1l1ll1l1l1l_opy_():
            self.logger.debug(bstack1111l1l_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡰࡨࡻࡤࡶࡡࡨࡧࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣጊ"))
            return
        def wrapped(bstack1l1llll11ll_opy_, bstack1l1l11l1lll_opy_, *args, **kwargs):
            contexts = bstack1l1llll11ll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack1111l1l_opy_ (u"ࠥࡥࡧࡵࡵࡵ࠼ࡥࡰࡦࡴ࡫ࠣጋ") in page.url:
                                    return page
                    else:
                        return bstack1l1l11l1lll_opy_(bstack1l1llll11ll_opy_)
        return wrapped
    def bstack1l1l111l1ll_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack1111l1l_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࠤጌ") + str(req) + bstack1111l1l_opy_ (u"ࠧࠨግ"))
        try:
            r = self.bstack1ll1ll11l11_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࠤጎ") + str(r.success) + bstack1111l1l_opy_ (u"ࠢࠣጏ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨጐ") + str(e) + bstack1111l1l_opy_ (u"ࠤࠥ጑"))
            traceback.print_exc()
            raise e
    def bstack1l1l11l1111_opy_(
        self,
        f: bstack1ll1lll1lll_opy_,
        Connection: object,
        exec: Tuple[bstack1llllllll1l_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1111l1l_opy_ (u"ࠥࡣࡸ࡫࡮ࡥࡡࡰࡩࡸࡹࡡࡨࡧࡢࡸࡴࡥࡳࡦࡴࡹࡩࡷࠨጒ"):
            return
        if not bstack1l1ll1l1l1l_opy_():
            return
        def wrapped(Connection, bstack1l1l111lll1_opy_, *args, **kwargs):
            return bstack1l1l111lll1_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1ll1lll1lll_opy_,
        bstack1l1l11ll11l_opy_: object,
        exec: Tuple[bstack1llllllll1l_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1111l1l_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࠥጓ"):
            return
        if not bstack1l1ll1l1l1l_opy_():
            self.logger.debug(bstack1111l1l_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡨࡲ࡯ࡴࡧࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣጔ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped