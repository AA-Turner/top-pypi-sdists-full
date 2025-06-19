# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll1lll11l1_opy_ import bstack1lll1l11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1111_opy_ import (
    bstack1111111111_opy_,
    bstack11111l1ll1_opy_,
    bstack1llllll111l_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1ll1llllll1_opy_ import bstack1llll11lll1_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11lll11l1l_opy_
from bstack_utils.helper import bstack1l1ll11l1ll_opy_
import threading
import os
import urllib.parse
class bstack1llll1ll1ll_opy_(bstack1lll1l11ll1_opy_):
    def __init__(self, bstack1lll1llllll_opy_):
        super().__init__()
        bstack1llll11lll1_opy_.bstack1ll11ll1l1l_opy_((bstack1111111111_opy_.bstack1lllllll1l1_opy_, bstack11111l1ll1_opy_.PRE), self.bstack1l1l1ll1ll1_opy_)
        bstack1llll11lll1_opy_.bstack1ll11ll1l1l_opy_((bstack1111111111_opy_.bstack1lllllll1l1_opy_, bstack11111l1ll1_opy_.PRE), self.bstack1l1l1ll11l1_opy_)
        bstack1llll11lll1_opy_.bstack1ll11ll1l1l_opy_((bstack1111111111_opy_.bstack1lllll1lll1_opy_, bstack11111l1ll1_opy_.PRE), self.bstack1l1l1ll1l1l_opy_)
        bstack1llll11lll1_opy_.bstack1ll11ll1l1l_opy_((bstack1111111111_opy_.bstack111111lll1_opy_, bstack11111l1ll1_opy_.PRE), self.bstack1l1l1ll1l11_opy_)
        bstack1llll11lll1_opy_.bstack1ll11ll1l1l_opy_((bstack1111111111_opy_.bstack1lllllll1l1_opy_, bstack11111l1ll1_opy_.PRE), self.bstack1l1l1l1ll11_opy_)
        bstack1llll11lll1_opy_.bstack1ll11ll1l1l_opy_((bstack1111111111_opy_.QUIT, bstack11111l1ll1_opy_.PRE), self.on_close)
        self.bstack1lll1llllll_opy_ = bstack1lll1llllll_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1ll1ll1_opy_(
        self,
        f: bstack1llll11lll1_opy_,
        bstack1l1l1lll11l_opy_: object,
        exec: Tuple[bstack1llllll111l_opy_, str],
        bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111lll_opy_ (u"ࠢ࡭ࡣࡸࡲࡨ࡮ࠢቼ"):
            return
        if not bstack1l1ll11l1ll_opy_():
            self.logger.debug(bstack111lll_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠ࡭ࡣࡸࡲࡨ࡮ࠠ࡮ࡧࡷ࡬ࡴࡪࠬࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧች"))
            return
        def wrapped(bstack1l1l1lll11l_opy_, launch, *args, **kwargs):
            response = self.bstack1l1l1ll111l_opy_(f.platform_index, instance.ref(), json.dumps({bstack111lll_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨቾ"): True}).encode(bstack111lll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤቿ")))
            if response is not None and response.capabilities:
                if not bstack1l1ll11l1ll_opy_():
                    browser = launch(bstack1l1l1lll11l_opy_)
                    return browser
                bstack1l1l1l1llll_opy_ = json.loads(response.capabilities.decode(bstack111lll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥኀ")))
                if not bstack1l1l1l1llll_opy_: # empty caps bstack1l1l1ll1lll_opy_ bstack1l1l1l1ll1l_opy_ bstack1l1l1l1lll1_opy_ bstack1lll1l11l1l_opy_ or error in processing
                    return
                bstack1l1l1ll11ll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l1l1llll_opy_))
                f.bstack11111ll111_opy_(instance, bstack1llll11lll1_opy_.bstack1l1l1lll1l1_opy_, bstack1l1l1ll11ll_opy_)
                f.bstack11111ll111_opy_(instance, bstack1llll11lll1_opy_.bstack1l1l1l1l1ll_opy_, bstack1l1l1l1llll_opy_)
                browser = bstack1l1l1lll11l_opy_.connect(bstack1l1l1ll11ll_opy_)
                return browser
        return wrapped
    def bstack1l1l1ll1l1l_opy_(
        self,
        f: bstack1llll11lll1_opy_,
        Connection: object,
        exec: Tuple[bstack1llllll111l_opy_, str],
        bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111lll_opy_ (u"ࠧࡪࡩࡴࡲࡤࡸࡨ࡮ࠢኁ"):
            self.logger.debug(bstack111lll_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡪࡩࡴࡲࡤࡸࡨ࡮ࠠ࡮ࡧࡷ࡬ࡴࡪࠬࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧኂ"))
            return
        if not bstack1l1ll11l1ll_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack111lll_opy_ (u"ࠧࡱࡣࡵࡥࡲࡹࠧኃ"), {}).get(bstack111lll_opy_ (u"ࠨࡤࡶࡔࡦࡸࡡ࡮ࡵࠪኄ")):
                    bstack1l1l1llll1l_opy_ = args[0][bstack111lll_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤኅ")][bstack111lll_opy_ (u"ࠥࡦࡸࡖࡡࡳࡣࡰࡷࠧኆ")]
                    session_id = bstack1l1l1llll1l_opy_.get(bstack111lll_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡎࡪࠢኇ"))
                    f.bstack11111ll111_opy_(instance, bstack1llll11lll1_opy_.bstack1l1l1llll11_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack111lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠠࠣኈ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1l1l1ll11_opy_(
        self,
        f: bstack1llll11lll1_opy_,
        bstack1l1l1lll11l_opy_: object,
        exec: Tuple[bstack1llllll111l_opy_, str],
        bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111lll_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺࠢ኉"):
            return
        if not bstack1l1ll11l1ll_opy_():
            self.logger.debug(bstack111lll_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦࡣࡰࡰࡱࡩࡨࡺࠠ࡮ࡧࡷ࡬ࡴࡪࠬࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧኊ"))
            return
        def wrapped(bstack1l1l1lll11l_opy_, connect, *args, **kwargs):
            response = self.bstack1l1l1ll111l_opy_(f.platform_index, instance.ref(), json.dumps({bstack111lll_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧኋ"): True}).encode(bstack111lll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣኌ")))
            if response is not None and response.capabilities:
                bstack1l1l1l1llll_opy_ = json.loads(response.capabilities.decode(bstack111lll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤኍ")))
                if not bstack1l1l1l1llll_opy_:
                    return
                bstack1l1l1ll11ll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l1l1llll_opy_))
                if bstack1l1l1l1llll_opy_.get(bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ኎")):
                    browser = bstack1l1l1lll11l_opy_.bstack1l1l1lll1ll_opy_(bstack1l1l1ll11ll_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1l1ll11ll_opy_
                    return connect(bstack1l1l1lll11l_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1l1ll11l1_opy_(
        self,
        f: bstack1llll11lll1_opy_,
        bstack1ll111l11ll_opy_: object,
        exec: Tuple[bstack1llllll111l_opy_, str],
        bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111lll_opy_ (u"ࠧࡴࡥࡸࡡࡳࡥ࡬࡫ࠢ኏"):
            return
        if not bstack1l1ll11l1ll_opy_():
            self.logger.debug(bstack111lll_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡴࡥࡸࡡࡳࡥ࡬࡫ࠠ࡮ࡧࡷ࡬ࡴࡪࠬࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧነ"))
            return
        def wrapped(bstack1ll111l11ll_opy_, bstack1l1l1ll1111_opy_, *args, **kwargs):
            contexts = bstack1ll111l11ll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack111lll_opy_ (u"ࠢࡢࡤࡲࡹࡹࡀࡢ࡭ࡣࡱ࡯ࠧኑ") in page.url:
                                    return page
                    else:
                        return bstack1l1l1ll1111_opy_(bstack1ll111l11ll_opy_)
        return wrapped
    def bstack1l1l1ll111l_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack111lll_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡻࡪࡨࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷ࠾ࠥࠨኒ") + str(req) + bstack111lll_opy_ (u"ࠤࠥና"))
        try:
            r = self.bstack1lll1ll1l11_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack111lll_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࡸࡻࡣࡤࡧࡶࡷࡂࠨኔ") + str(r.success) + bstack111lll_opy_ (u"ࠦࠧን"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111lll_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥኖ") + str(e) + bstack111lll_opy_ (u"ࠨࠢኗ"))
            traceback.print_exc()
            raise e
    def bstack1l1l1ll1l11_opy_(
        self,
        f: bstack1llll11lll1_opy_,
        Connection: object,
        exec: Tuple[bstack1llllll111l_opy_, str],
        bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111lll_opy_ (u"ࠢࡠࡵࡨࡲࡩࡥ࡭ࡦࡵࡶࡥ࡬࡫࡟ࡵࡱࡢࡷࡪࡸࡶࡦࡴࠥኘ"):
            return
        if not bstack1l1ll11l1ll_opy_():
            return
        def wrapped(Connection, bstack1l1l1lll111_opy_, *args, **kwargs):
            return bstack1l1l1lll111_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1llll11lll1_opy_,
        bstack1l1l1lll11l_opy_: object,
        exec: Tuple[bstack1llllll111l_opy_, str],
        bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111lll_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࠢኙ"):
            return
        if not bstack1l1ll11l1ll_opy_():
            self.logger.debug(bstack111lll_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡥ࡯ࡳࡸ࡫ࠠ࡮ࡧࡷ࡬ࡴࡪࠬࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧኚ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped