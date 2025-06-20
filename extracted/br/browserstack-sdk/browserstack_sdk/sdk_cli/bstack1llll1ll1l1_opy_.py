# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1ll1ll1llll_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1lll1_opy_ import (
    bstack1111111l11_opy_,
    bstack1llllll1111_opy_,
    bstack1llll1ll1ll_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1lll11l1l11_opy_ import bstack1lll1lll1l1_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l11ll1l1l_opy_
from bstack_utils.helper import bstack1l1ll111ll1_opy_
import threading
import os
import urllib.parse
class bstack1lll1l11l1l_opy_(bstack1ll1ll1llll_opy_):
    def __init__(self, bstack1lll1l111ll_opy_):
        super().__init__()
        bstack1lll1lll1l1_opy_.bstack1ll1l11l1l1_opy_((bstack1111111l11_opy_.bstack1llllll11l1_opy_, bstack1llllll1111_opy_.PRE), self.bstack1l1l1l1ll11_opy_)
        bstack1lll1lll1l1_opy_.bstack1ll1l11l1l1_opy_((bstack1111111l11_opy_.bstack1llllll11l1_opy_, bstack1llllll1111_opy_.PRE), self.bstack1l1l1l1111l_opy_)
        bstack1lll1lll1l1_opy_.bstack1ll1l11l1l1_opy_((bstack1111111l11_opy_.bstack1lllllll1ll_opy_, bstack1llllll1111_opy_.PRE), self.bstack1l1l1l111ll_opy_)
        bstack1lll1lll1l1_opy_.bstack1ll1l11l1l1_opy_((bstack1111111l11_opy_.bstack1lllll11lll_opy_, bstack1llllll1111_opy_.PRE), self.bstack1l1l1l1l111_opy_)
        bstack1lll1lll1l1_opy_.bstack1ll1l11l1l1_opy_((bstack1111111l11_opy_.bstack1llllll11l1_opy_, bstack1llllll1111_opy_.PRE), self.bstack1l1l1l1ll1l_opy_)
        bstack1lll1lll1l1_opy_.bstack1ll1l11l1l1_opy_((bstack1111111l11_opy_.QUIT, bstack1llllll1111_opy_.PRE), self.on_close)
        self.bstack1lll1l111ll_opy_ = bstack1lll1l111ll_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1l1ll11_opy_(
        self,
        f: bstack1lll1lll1l1_opy_,
        bstack1l1l1l1lll1_opy_: object,
        exec: Tuple[bstack1llll1ll1ll_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1111111l11_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll11_opy_ (u"ࠢ࡭ࡣࡸࡲࡨ࡮ࠢኊ"):
            return
        if not bstack1l1ll111ll1_opy_():
            self.logger.debug(bstack11ll11_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠ࡭ࡣࡸࡲࡨ࡮ࠠ࡮ࡧࡷ࡬ࡴࡪࠬࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧኋ"))
            return
        def wrapped(bstack1l1l1l1lll1_opy_, launch, *args, **kwargs):
            response = self.bstack1l1l11lll1l_opy_(f.platform_index, instance.ref(), json.dumps({bstack11ll11_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨኌ"): True}).encode(bstack11ll11_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤኍ")))
            if response is not None and response.capabilities:
                if not bstack1l1ll111ll1_opy_():
                    browser = launch(bstack1l1l1l1lll1_opy_)
                    return browser
                bstack1l1l11lllll_opy_ = json.loads(response.capabilities.decode(bstack11ll11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥ኎")))
                if not bstack1l1l11lllll_opy_: # empty caps bstack1l1l1l11lll_opy_ bstack1l1l11llll1_opy_ bstack1l1l1l11ll1_opy_ bstack1lll11111ll_opy_ or error in processing
                    return
                bstack1l1l11lll11_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l11lllll_opy_))
                f.bstack1llllllllll_opy_(instance, bstack1lll1lll1l1_opy_.bstack1l1l1l11l1l_opy_, bstack1l1l11lll11_opy_)
                f.bstack1llllllllll_opy_(instance, bstack1lll1lll1l1_opy_.bstack1l1l1l11111_opy_, bstack1l1l11lllll_opy_)
                browser = bstack1l1l1l1lll1_opy_.connect(bstack1l1l11lll11_opy_)
                return browser
        return wrapped
    def bstack1l1l1l111ll_opy_(
        self,
        f: bstack1lll1lll1l1_opy_,
        Connection: object,
        exec: Tuple[bstack1llll1ll1ll_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1111111l11_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll11_opy_ (u"ࠧࡪࡩࡴࡲࡤࡸࡨ࡮ࠢ኏"):
            self.logger.debug(bstack11ll11_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡪࡩࡴࡲࡤࡸࡨ࡮ࠠ࡮ࡧࡷ࡬ࡴࡪࠬࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧነ"))
            return
        if not bstack1l1ll111ll1_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack11ll11_opy_ (u"ࠧࡱࡣࡵࡥࡲࡹࠧኑ"), {}).get(bstack11ll11_opy_ (u"ࠨࡤࡶࡔࡦࡸࡡ࡮ࡵࠪኒ")):
                    bstack1l1l1l1l1ll_opy_ = args[0][bstack11ll11_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤና")][bstack11ll11_opy_ (u"ࠥࡦࡸࡖࡡࡳࡣࡰࡷࠧኔ")]
                    session_id = bstack1l1l1l1l1ll_opy_.get(bstack11ll11_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡎࡪࠢን"))
                    f.bstack1llllllllll_opy_(instance, bstack1lll1lll1l1_opy_.bstack1l1l1l11l11_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack11ll11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠠࠣኖ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1l1l1ll1l_opy_(
        self,
        f: bstack1lll1lll1l1_opy_,
        bstack1l1l1l1lll1_opy_: object,
        exec: Tuple[bstack1llll1ll1ll_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1111111l11_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll11_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺࠢኗ"):
            return
        if not bstack1l1ll111ll1_opy_():
            self.logger.debug(bstack11ll11_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦࡣࡰࡰࡱࡩࡨࡺࠠ࡮ࡧࡷ࡬ࡴࡪࠬࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧኘ"))
            return
        def wrapped(bstack1l1l1l1lll1_opy_, connect, *args, **kwargs):
            response = self.bstack1l1l11lll1l_opy_(f.platform_index, instance.ref(), json.dumps({bstack11ll11_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧኙ"): True}).encode(bstack11ll11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣኚ")))
            if response is not None and response.capabilities:
                bstack1l1l11lllll_opy_ = json.loads(response.capabilities.decode(bstack11ll11_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤኛ")))
                if not bstack1l1l11lllll_opy_:
                    return
                bstack1l1l11lll11_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l11lllll_opy_))
                if bstack1l1l11lllll_opy_.get(bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪኜ")):
                    browser = bstack1l1l1l1lll1_opy_.bstack1l1l1l1l1l1_opy_(bstack1l1l11lll11_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1l11lll11_opy_
                    return connect(bstack1l1l1l1lll1_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1l1l1111l_opy_(
        self,
        f: bstack1lll1lll1l1_opy_,
        bstack1ll1111l1l1_opy_: object,
        exec: Tuple[bstack1llll1ll1ll_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1111111l11_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll11_opy_ (u"ࠧࡴࡥࡸࡡࡳࡥ࡬࡫ࠢኝ"):
            return
        if not bstack1l1ll111ll1_opy_():
            self.logger.debug(bstack11ll11_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡴࡥࡸࡡࡳࡥ࡬࡫ࠠ࡮ࡧࡷ࡬ࡴࡪࠬࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧኞ"))
            return
        def wrapped(bstack1ll1111l1l1_opy_, bstack1l1l1l1l11l_opy_, *args, **kwargs):
            contexts = bstack1ll1111l1l1_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack11ll11_opy_ (u"ࠢࡢࡤࡲࡹࡹࡀࡢ࡭ࡣࡱ࡯ࠧኟ") in page.url:
                                    return page
                    else:
                        return bstack1l1l1l1l11l_opy_(bstack1ll1111l1l1_opy_)
        return wrapped
    def bstack1l1l11lll1l_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack11ll11_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡻࡪࡨࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷ࠾ࠥࠨአ") + str(req) + bstack11ll11_opy_ (u"ࠤࠥኡ"))
        try:
            r = self.bstack1llll1l1l11_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11ll11_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࡸࡻࡣࡤࡧࡶࡷࡂࠨኢ") + str(r.success) + bstack11ll11_opy_ (u"ࠦࠧኣ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥኤ") + str(e) + bstack11ll11_opy_ (u"ࠨࠢእ"))
            traceback.print_exc()
            raise e
    def bstack1l1l1l1l111_opy_(
        self,
        f: bstack1lll1lll1l1_opy_,
        Connection: object,
        exec: Tuple[bstack1llll1ll1ll_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1111111l11_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll11_opy_ (u"ࠢࡠࡵࡨࡲࡩࡥ࡭ࡦࡵࡶࡥ࡬࡫࡟ࡵࡱࡢࡷࡪࡸࡶࡦࡴࠥኦ"):
            return
        if not bstack1l1ll111ll1_opy_():
            return
        def wrapped(Connection, bstack1l1l1l111l1_opy_, *args, **kwargs):
            return bstack1l1l1l111l1_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1lll1lll1l1_opy_,
        bstack1l1l1l1lll1_opy_: object,
        exec: Tuple[bstack1llll1ll1ll_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1111111l11_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll11_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࠢኧ"):
            return
        if not bstack1l1ll111ll1_opy_():
            self.logger.debug(bstack11ll11_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡥ࡯ࡳࡸ࡫ࠠ࡮ࡧࡷ࡬ࡴࡪࠬࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧከ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped