# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1llll11l11l_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1l1l_opy_ import (
    bstack1llllllllll_opy_,
    bstack1llll1lll11_opy_,
    bstack1lllll1ll1l_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1lll1ll11ll_opy_ import bstack1lll1llllll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11lll11lll_opy_
from bstack_utils.helper import bstack1l1ll111l1l_opy_
import threading
import os
import urllib.parse
class bstack1ll1ll111l1_opy_(bstack1llll11l11l_opy_):
    def __init__(self, bstack1lll11ll11l_opy_):
        super().__init__()
        bstack1lll1llllll_opy_.bstack1ll11lll111_opy_((bstack1llllllllll_opy_.bstack1llllll11ll_opy_, bstack1llll1lll11_opy_.PRE), self.bstack1l1l11llll1_opy_)
        bstack1lll1llllll_opy_.bstack1ll11lll111_opy_((bstack1llllllllll_opy_.bstack1llllll11ll_opy_, bstack1llll1lll11_opy_.PRE), self.bstack1l1l1l111l1_opy_)
        bstack1lll1llllll_opy_.bstack1ll11lll111_opy_((bstack1llllllllll_opy_.bstack1lllll1l1l1_opy_, bstack1llll1lll11_opy_.PRE), self.bstack1l1l11lllll_opy_)
        bstack1lll1llllll_opy_.bstack1ll11lll111_opy_((bstack1llllllllll_opy_.bstack1llllll111l_opy_, bstack1llll1lll11_opy_.PRE), self.bstack1l1l11lll11_opy_)
        bstack1lll1llllll_opy_.bstack1ll11lll111_opy_((bstack1llllllllll_opy_.bstack1llllll11ll_opy_, bstack1llll1lll11_opy_.PRE), self.bstack1l1l1l1111l_opy_)
        bstack1lll1llllll_opy_.bstack1ll11lll111_opy_((bstack1llllllllll_opy_.QUIT, bstack1llll1lll11_opy_.PRE), self.on_close)
        self.bstack1lll11ll11l_opy_ = bstack1lll11ll11l_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11llll1_opy_(
        self,
        f: bstack1lll1llllll_opy_,
        bstack1l1l11lll1l_opy_: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1lllllll11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llll1lll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1_opy_ (u"ࠨ࡬ࡢࡷࡱࡧ࡭ࠨያ"):
            return
        if not bstack1l1ll111l1l_opy_():
            self.logger.debug(bstack11l1_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦ࡬ࡢࡷࡱࡧ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦዬ"))
            return
        def wrapped(bstack1l1l11lll1l_opy_, launch, *args, **kwargs):
            response = self.bstack1l1l11l11ll_opy_(f.platform_index, instance.ref(), json.dumps({bstack11l1_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧይ"): True}).encode(bstack11l1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣዮ")))
            if response is not None and response.capabilities:
                if not bstack1l1ll111l1l_opy_():
                    browser = launch(bstack1l1l11lll1l_opy_)
                    return browser
                bstack1l1l11ll1l1_opy_ = json.loads(response.capabilities.decode(bstack11l1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤዯ")))
                if not bstack1l1l11ll1l1_opy_: # empty caps bstack1l1l11l1l1l_opy_ bstack1l1l11l1111_opy_ bstack1l1l11ll1ll_opy_ bstack1lll111l111_opy_ or error in processing
                    return
                bstack1l1l11ll11l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l11ll1l1_opy_))
                f.bstack1111111lll_opy_(instance, bstack1lll1llllll_opy_.bstack1l1l1l11111_opy_, bstack1l1l11ll11l_opy_)
                f.bstack1111111lll_opy_(instance, bstack1lll1llllll_opy_.bstack1l1l11l1lll_opy_, bstack1l1l11ll1l1_opy_)
                browser = bstack1l1l11lll1l_opy_.connect(bstack1l1l11ll11l_opy_)
                return browser
        return wrapped
    def bstack1l1l11lllll_opy_(
        self,
        f: bstack1lll1llllll_opy_,
        Connection: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1lllllll11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llll1lll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1_opy_ (u"ࠦࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠨደ"):
            self.logger.debug(bstack11l1_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦዱ"))
            return
        if not bstack1l1ll111l1l_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack11l1_opy_ (u"࠭ࡰࡢࡴࡤࡱࡸ࠭ዲ"), {}).get(bstack11l1_opy_ (u"ࠧࡣࡵࡓࡥࡷࡧ࡭ࡴࠩዳ")):
                    bstack1l1l11ll111_opy_ = args[0][bstack11l1_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣዴ")][bstack11l1_opy_ (u"ࠤࡥࡷࡕࡧࡲࡢ࡯ࡶࠦድ")]
                    session_id = bstack1l1l11ll111_opy_.get(bstack11l1_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡍࡩࠨዶ"))
                    f.bstack1111111lll_opy_(instance, bstack1lll1llllll_opy_.bstack1l1l11l1l11_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack11l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠿ࠦࠢዷ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1l1l1111l_opy_(
        self,
        f: bstack1lll1llllll_opy_,
        bstack1l1l11lll1l_opy_: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1lllllll11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llll1lll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࠨዸ"):
            return
        if not bstack1l1ll111l1l_opy_():
            self.logger.debug(bstack11l1_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡩ࡯࡯ࡰࡨࡧࡹࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦዹ"))
            return
        def wrapped(bstack1l1l11lll1l_opy_, connect, *args, **kwargs):
            response = self.bstack1l1l11l11ll_opy_(f.platform_index, instance.ref(), json.dumps({bstack11l1_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ዺ"): True}).encode(bstack11l1_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢዻ")))
            if response is not None and response.capabilities:
                bstack1l1l11ll1l1_opy_ = json.loads(response.capabilities.decode(bstack11l1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣዼ")))
                if not bstack1l1l11ll1l1_opy_:
                    return
                bstack1l1l11ll11l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l11ll1l1_opy_))
                if bstack1l1l11ll1l1_opy_.get(bstack11l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩዽ")):
                    browser = bstack1l1l11lll1l_opy_.bstack1l1l11l11l1_opy_(bstack1l1l11ll11l_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1l11ll11l_opy_
                    return connect(bstack1l1l11lll1l_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1l1l111l1_opy_(
        self,
        f: bstack1lll1llllll_opy_,
        bstack1l1llllll11_opy_: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1lllllll11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llll1lll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨዾ"):
            return
        if not bstack1l1ll111l1l_opy_():
            self.logger.debug(bstack11l1_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦዿ"))
            return
        def wrapped(bstack1l1llllll11_opy_, bstack1l1l11l1ll1_opy_, *args, **kwargs):
            contexts = bstack1l1llllll11_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack11l1_opy_ (u"ࠨࡡࡣࡱࡸࡸ࠿ࡨ࡬ࡢࡰ࡮ࠦጀ") in page.url:
                                    return page
                    else:
                        return bstack1l1l11l1ll1_opy_(bstack1l1llllll11_opy_)
        return wrapped
    def bstack1l1l11l11ll_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack11l1_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡺࡩࡧࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧጁ") + str(req) + bstack11l1_opy_ (u"ࠣࠤጂ"))
        try:
            r = self.bstack1ll1llllll1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11l1_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧጃ") + str(r.success) + bstack11l1_opy_ (u"ࠥࠦጄ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤጅ") + str(e) + bstack11l1_opy_ (u"ࠧࠨጆ"))
            traceback.print_exc()
            raise e
    def bstack1l1l11lll11_opy_(
        self,
        f: bstack1lll1llllll_opy_,
        Connection: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1lllllll11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llll1lll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1_opy_ (u"ࠨ࡟ࡴࡧࡱࡨࡤࡳࡥࡴࡵࡤ࡫ࡪࡥࡴࡰࡡࡶࡩࡷࡼࡥࡳࠤጇ"):
            return
        if not bstack1l1ll111l1l_opy_():
            return
        def wrapped(Connection, bstack1l1l11l111l_opy_, *args, **kwargs):
            return bstack1l1l11l111l_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1lll1llllll_opy_,
        bstack1l1l11lll1l_opy_: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1lllllll11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llll1lll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨገ"):
            return
        if not bstack1l1ll111l1l_opy_():
            self.logger.debug(bstack11l1_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡤ࡮ࡲࡷࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦጉ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped