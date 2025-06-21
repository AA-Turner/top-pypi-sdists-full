# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1llll111111_opy_ import bstack1llll11l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1llll1ll1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1lllll1llll_opy_,
    bstack1111111111_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1lll111l11l_opy_ import bstack1ll1lllllll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l1111l1ll_opy_
from bstack_utils.helper import bstack1l1lll11ll1_opy_
import threading
import os
import urllib.parse
class bstack1lll11llll1_opy_(bstack1llll11l1ll_opy_):
    def __init__(self, bstack1lll1ll111l_opy_):
        super().__init__()
        bstack1ll1lllllll_opy_.bstack1ll111lll1l_opy_((bstack1lllll1l111_opy_.bstack1111111lll_opy_, bstack1lllll1llll_opy_.PRE), self.bstack1l1l1l111ll_opy_)
        bstack1ll1lllllll_opy_.bstack1ll111lll1l_opy_((bstack1lllll1l111_opy_.bstack1111111lll_opy_, bstack1lllll1llll_opy_.PRE), self.bstack1l1l1l11ll1_opy_)
        bstack1ll1lllllll_opy_.bstack1ll111lll1l_opy_((bstack1lllll1l111_opy_.bstack1lllll1l1l1_opy_, bstack1lllll1llll_opy_.PRE), self.bstack1l1l1l11l11_opy_)
        bstack1ll1lllllll_opy_.bstack1ll111lll1l_opy_((bstack1lllll1l111_opy_.bstack1lllll11111_opy_, bstack1lllll1llll_opy_.PRE), self.bstack1l1l11llll1_opy_)
        bstack1ll1lllllll_opy_.bstack1ll111lll1l_opy_((bstack1lllll1l111_opy_.bstack1111111lll_opy_, bstack1lllll1llll_opy_.PRE), self.bstack1l1l11lll11_opy_)
        bstack1ll1lllllll_opy_.bstack1ll111lll1l_opy_((bstack1lllll1l111_opy_.QUIT, bstack1lllll1llll_opy_.PRE), self.on_close)
        self.bstack1lll1ll111l_opy_ = bstack1lll1ll111l_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1l111ll_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        bstack1l1l1l111l1_opy_: object,
        exec: Tuple[bstack1111111111_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l1l1_opy_ (u"ࠣ࡮ࡤࡹࡳࡩࡨࠣኋ"):
            return
        if not bstack1l1lll11ll1_opy_():
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡ࡮ࡤࡹࡳࡩࡨࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨኌ"))
            return
        def wrapped(bstack1l1l1l111l1_opy_, launch, *args, **kwargs):
            response = self.bstack1l1l1l11lll_opy_(f.platform_index, instance.ref(), json.dumps({bstack1l1l1l1_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩኍ"): True}).encode(bstack1l1l1l1_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥ኎")))
            if response is not None and response.capabilities:
                if not bstack1l1lll11ll1_opy_():
                    browser = launch(bstack1l1l1l111l1_opy_)
                    return browser
                bstack1l1l1l1111l_opy_ = json.loads(response.capabilities.decode(bstack1l1l1l1_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦ኏")))
                if not bstack1l1l1l1111l_opy_: # empty caps bstack1l1l1l11111_opy_ bstack1l1l1l1ll11_opy_ bstack1l1l1l1l1l1_opy_ bstack1ll1l1lll1l_opy_ or error in processing
                    return
                bstack1l1l1l1ll1l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l1l1111l_opy_))
                f.bstack1lllll1111l_opy_(instance, bstack1ll1lllllll_opy_.bstack1l1l11lllll_opy_, bstack1l1l1l1ll1l_opy_)
                f.bstack1lllll1111l_opy_(instance, bstack1ll1lllllll_opy_.bstack1l1l1l1lll1_opy_, bstack1l1l1l1111l_opy_)
                browser = bstack1l1l1l111l1_opy_.connect(bstack1l1l1l1ll1l_opy_)
                return browser
        return wrapped
    def bstack1l1l1l11l11_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        Connection: object,
        exec: Tuple[bstack1111111111_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l1l1_opy_ (u"ࠨࡤࡪࡵࡳࡥࡹࡩࡨࠣነ"):
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦࡤࡪࡵࡳࡥࡹࡩࡨࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨኑ"))
            return
        if not bstack1l1lll11ll1_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1l1l1l1_opy_ (u"ࠨࡲࡤࡶࡦࡳࡳࠨኒ"), {}).get(bstack1l1l1l1_opy_ (u"ࠩࡥࡷࡕࡧࡲࡢ࡯ࡶࠫና")):
                    bstack1l1l1l11l1l_opy_ = args[0][bstack1l1l1l1_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡵࠥኔ")][bstack1l1l1l1_opy_ (u"ࠦࡧࡹࡐࡢࡴࡤࡱࡸࠨን")]
                    session_id = bstack1l1l1l11l1l_opy_.get(bstack1l1l1l1_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡏࡤࠣኖ"))
                    f.bstack1lllll1111l_opy_(instance, bstack1ll1lllllll_opy_.bstack1l1l11lll1l_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡪࡩࡴࡲࡤࡸࡨ࡮ࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠡࠤኗ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1l11lll11_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        bstack1l1l1l111l1_opy_: object,
        exec: Tuple[bstack1111111111_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l1l1_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࠣኘ"):
            return
        if not bstack1l1lll11ll1_opy_():
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡤࡱࡱࡲࡪࡩࡴࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨኙ"))
            return
        def wrapped(bstack1l1l1l111l1_opy_, connect, *args, **kwargs):
            response = self.bstack1l1l1l11lll_opy_(f.platform_index, instance.ref(), json.dumps({bstack1l1l1l1_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨኚ"): True}).encode(bstack1l1l1l1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤኛ")))
            if response is not None and response.capabilities:
                bstack1l1l1l1111l_opy_ = json.loads(response.capabilities.decode(bstack1l1l1l1_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥኜ")))
                if not bstack1l1l1l1111l_opy_:
                    return
                bstack1l1l1l1ll1l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l1l1111l_opy_))
                if bstack1l1l1l1111l_opy_.get(bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫኝ")):
                    browser = bstack1l1l1l111l1_opy_.bstack1l1l1l1l11l_opy_(bstack1l1l1l1ll1l_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1l1l1ll1l_opy_
                    return connect(bstack1l1l1l111l1_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1l1l11ll1_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        bstack1ll1111ll11_opy_: object,
        exec: Tuple[bstack1111111111_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l1l1_opy_ (u"ࠨ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠣኞ"):
            return
        if not bstack1l1lll11ll1_opy_():
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨኟ"))
            return
        def wrapped(bstack1ll1111ll11_opy_, bstack1l1l1l1l1ll_opy_, *args, **kwargs):
            contexts = bstack1ll1111ll11_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack1l1l1l1_opy_ (u"ࠣࡣࡥࡳࡺࡺ࠺ࡣ࡮ࡤࡲࡰࠨአ") in page.url:
                                    return page
                    else:
                        return bstack1l1l1l1l1ll_opy_(bstack1ll1111ll11_opy_)
        return wrapped
    def bstack1l1l1l11lll_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸ࠿ࠦࠢኡ") + str(req) + bstack1l1l1l1_opy_ (u"ࠥࠦኢ"))
        try:
            r = self.bstack1ll1ll111l1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࡹࡵࡤࡥࡨࡷࡸࡃࠢኣ") + str(r.success) + bstack1l1l1l1_opy_ (u"ࠧࠨኤ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦእ") + str(e) + bstack1l1l1l1_opy_ (u"ࠢࠣኦ"))
            traceback.print_exc()
            raise e
    def bstack1l1l11llll1_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        Connection: object,
        exec: Tuple[bstack1111111111_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l1l1_opy_ (u"ࠣࡡࡶࡩࡳࡪ࡟࡮ࡧࡶࡷࡦ࡭ࡥࡠࡶࡲࡣࡸ࡫ࡲࡷࡧࡵࠦኧ"):
            return
        if not bstack1l1lll11ll1_opy_():
            return
        def wrapped(Connection, bstack1l1l1l1l111_opy_, *args, **kwargs):
            return bstack1l1l1l1l111_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1ll1lllllll_opy_,
        bstack1l1l1l111l1_opy_: object,
        exec: Tuple[bstack1111111111_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l1l1_opy_ (u"ࠤࡦࡰࡴࡹࡥࠣከ"):
            return
        if not bstack1l1lll11ll1_opy_():
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡦࡰࡴࡹࡥࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨኩ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped