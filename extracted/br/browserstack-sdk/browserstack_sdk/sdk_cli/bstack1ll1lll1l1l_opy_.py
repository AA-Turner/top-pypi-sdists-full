# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1llll1ll1l1_opy_ import bstack1lll1ll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import (
    bstack1lllll1ll11_opy_,
    bstack1llllll1ll1_opy_,
    bstack1111111l1l_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1ll1lllll1l_opy_ import bstack1lll111111l_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1ll11l1ll1_opy_
from bstack_utils.helper import bstack1l1lll11111_opy_
import threading
import os
import urllib.parse
class bstack1lll1llllll_opy_(bstack1lll1ll1l1l_opy_):
    def __init__(self, bstack1ll1ll1ll1l_opy_):
        super().__init__()
        bstack1lll111111l_opy_.bstack1ll11l11lll_opy_((bstack1lllll1ll11_opy_.bstack11111111l1_opy_, bstack1llllll1ll1_opy_.PRE), self.bstack1l1l11lll11_opy_)
        bstack1lll111111l_opy_.bstack1ll11l11lll_opy_((bstack1lllll1ll11_opy_.bstack11111111l1_opy_, bstack1llllll1ll1_opy_.PRE), self.bstack1l1l11l1ll1_opy_)
        bstack1lll111111l_opy_.bstack1ll11l11lll_opy_((bstack1lllll1ll11_opy_.bstack1111111l11_opy_, bstack1llllll1ll1_opy_.PRE), self.bstack1l1l11ll1ll_opy_)
        bstack1lll111111l_opy_.bstack1ll11l11lll_opy_((bstack1lllll1ll11_opy_.bstack1llllllll11_opy_, bstack1llllll1ll1_opy_.PRE), self.bstack1l1l1l1111l_opy_)
        bstack1lll111111l_opy_.bstack1ll11l11lll_opy_((bstack1lllll1ll11_opy_.bstack11111111l1_opy_, bstack1llllll1ll1_opy_.PRE), self.bstack1l1l11llll1_opy_)
        bstack1lll111111l_opy_.bstack1ll11l11lll_opy_((bstack1lllll1ll11_opy_.QUIT, bstack1llllll1ll1_opy_.PRE), self.on_close)
        self.bstack1ll1ll1ll1l_opy_ = bstack1ll1ll1ll1l_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11lll11_opy_(
        self,
        f: bstack1lll111111l_opy_,
        bstack1l1l11ll1l1_opy_: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll1l1_opy_ (u"ࠧࡲࡡࡶࡰࡦ࡬ࠧካ"):
            return
        if not bstack1l1lll11111_opy_():
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡲࡡࡶࡰࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥኬ"))
            return
        def wrapped(bstack1l1l11ll1l1_opy_, launch, *args, **kwargs):
            response = self.bstack1l1l11ll111_opy_(f.platform_index, instance.ref(), json.dumps({bstack11ll1l1_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ክ"): True}).encode(bstack11ll1l1_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢኮ")))
            if response is not None and response.capabilities:
                if not bstack1l1lll11111_opy_():
                    browser = launch(bstack1l1l11ll1l1_opy_)
                    return browser
                bstack1l1l1l11l1l_opy_ = json.loads(response.capabilities.decode(bstack11ll1l1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣኯ")))
                if not bstack1l1l1l11l1l_opy_: # empty caps bstack1l1l11ll11l_opy_ bstack1l1l1l111ll_opy_ bstack1l1l1l111l1_opy_ bstack1ll1lllll11_opy_ or error in processing
                    return
                bstack1l1l11lll1l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l1l11l1l_opy_))
                f.bstack1lllll1ll1l_opy_(instance, bstack1lll111111l_opy_.bstack1l1l11lllll_opy_, bstack1l1l11lll1l_opy_)
                f.bstack1lllll1ll1l_opy_(instance, bstack1lll111111l_opy_.bstack1l1l1l11111_opy_, bstack1l1l1l11l1l_opy_)
                browser = bstack1l1l11ll1l1_opy_.connect(bstack1l1l11lll1l_opy_)
                return browser
        return wrapped
    def bstack1l1l11ll1ll_opy_(
        self,
        f: bstack1lll111111l_opy_,
        Connection: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll1l1_opy_ (u"ࠥࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠧኰ"):
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥ኱"))
            return
        if not bstack1l1lll11111_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack11ll1l1_opy_ (u"ࠬࡶࡡࡳࡣࡰࡷࠬኲ"), {}).get(bstack11ll1l1_opy_ (u"࠭ࡢࡴࡒࡤࡶࡦࡳࡳࠨኳ")):
                    bstack1l1l11l1l11_opy_ = args[0][bstack11ll1l1_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢኴ")][bstack11ll1l1_opy_ (u"ࠣࡤࡶࡔࡦࡸࡡ࡮ࡵࠥኵ")]
                    session_id = bstack1l1l11l1l11_opy_.get(bstack11ll1l1_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡌࡨࠧ኶"))
                    f.bstack1lllll1ll1l_opy_(instance, bstack1lll111111l_opy_.bstack1l1l11l11ll_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࠨ኷"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1l11llll1_opy_(
        self,
        f: bstack1lll111111l_opy_,
        bstack1l1l11ll1l1_opy_: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll1l1_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࠧኸ"):
            return
        if not bstack1l1lll11111_opy_():
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡨࡵ࡮࡯ࡧࡦࡸࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥኹ"))
            return
        def wrapped(bstack1l1l11ll1l1_opy_, connect, *args, **kwargs):
            response = self.bstack1l1l11ll111_opy_(f.platform_index, instance.ref(), json.dumps({bstack11ll1l1_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬኺ"): True}).encode(bstack11ll1l1_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨኻ")))
            if response is not None and response.capabilities:
                bstack1l1l1l11l1l_opy_ = json.loads(response.capabilities.decode(bstack11ll1l1_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢኼ")))
                if not bstack1l1l1l11l1l_opy_:
                    return
                bstack1l1l11lll1l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l1l11l1l_opy_))
                if bstack1l1l1l11l1l_opy_.get(bstack11ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨኽ")):
                    browser = bstack1l1l11ll1l1_opy_.bstack1l1l1l11l11_opy_(bstack1l1l11lll1l_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1l11lll1l_opy_
                    return connect(bstack1l1l11ll1l1_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1l11l1ll1_opy_(
        self,
        f: bstack1lll111111l_opy_,
        bstack1ll1111111l_opy_: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll1l1_opy_ (u"ࠥࡲࡪࡽ࡟ࡱࡣࡪࡩࠧኾ"):
            return
        if not bstack1l1lll11111_opy_():
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡲࡪࡽ࡟ࡱࡣࡪࡩࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥ኿"))
            return
        def wrapped(bstack1ll1111111l_opy_, bstack1l1l11l1lll_opy_, *args, **kwargs):
            contexts = bstack1ll1111111l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack11ll1l1_opy_ (u"ࠧࡧࡢࡰࡷࡷ࠾ࡧࡲࡡ࡯࡭ࠥዀ") in page.url:
                                    return page
                    else:
                        return bstack1l1l11l1lll_opy_(bstack1ll1111111l_opy_)
        return wrapped
    def bstack1l1l11ll111_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡹࡨࡦࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦ዁") + str(req) + bstack11ll1l1_opy_ (u"ࠢࠣዂ"))
        try:
            r = self.bstack1lll1l1ll1l_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦዃ") + str(r.success) + bstack11ll1l1_opy_ (u"ࠤࠥዄ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣዅ") + str(e) + bstack11ll1l1_opy_ (u"ࠦࠧ዆"))
            traceback.print_exc()
            raise e
    def bstack1l1l1l1111l_opy_(
        self,
        f: bstack1lll111111l_opy_,
        Connection: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll1l1_opy_ (u"ࠧࡥࡳࡦࡰࡧࡣࡲ࡫ࡳࡴࡣࡪࡩࡤࡺ࡯ࡠࡵࡨࡶࡻ࡫ࡲࠣ዇"):
            return
        if not bstack1l1lll11111_opy_():
            return
        def wrapped(Connection, bstack1l1l11l1l1l_opy_, *args, **kwargs):
            return bstack1l1l11l1l1l_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1lll111111l_opy_,
        bstack1l1l11ll1l1_opy_: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll1l1_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧወ"):
            return
        if not bstack1l1lll11111_opy_():
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦࡣ࡭ࡱࡶࡩࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥዉ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped