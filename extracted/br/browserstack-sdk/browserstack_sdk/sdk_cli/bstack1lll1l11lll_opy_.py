# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import bstack1lll11l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1llll1lll1l_opy_ import (
    bstack1lllll1l1l1_opy_,
    bstack1llllllllll_opy_,
    bstack1lllllllll1_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1llll1111ll_opy_ import bstack1lll1ll1l11_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l111ll1ll_opy_
from bstack_utils.helper import bstack1l1llll11ll_opy_
import threading
import os
import urllib.parse
class bstack1llll11ll1l_opy_(bstack1lll11l11ll_opy_):
    def __init__(self, bstack1llll11111l_opy_):
        super().__init__()
        bstack1lll1ll1l11_opy_.bstack1ll1l11lll1_opy_((bstack1lllll1l1l1_opy_.bstack1111111l1l_opy_, bstack1llllllllll_opy_.PRE), self.bstack1l1l11lll1l_opy_)
        bstack1lll1ll1l11_opy_.bstack1ll1l11lll1_opy_((bstack1lllll1l1l1_opy_.bstack1111111l1l_opy_, bstack1llllllllll_opy_.PRE), self.bstack1l1l11lll11_opy_)
        bstack1lll1ll1l11_opy_.bstack1ll1l11lll1_opy_((bstack1lllll1l1l1_opy_.bstack1lllll1lll1_opy_, bstack1llllllllll_opy_.PRE), self.bstack1l1l11l1111_opy_)
        bstack1lll1ll1l11_opy_.bstack1ll1l11lll1_opy_((bstack1lllll1l1l1_opy_.bstack11111111l1_opy_, bstack1llllllllll_opy_.PRE), self.bstack1l1l11ll1l1_opy_)
        bstack1lll1ll1l11_opy_.bstack1ll1l11lll1_opy_((bstack1lllll1l1l1_opy_.bstack1111111l1l_opy_, bstack1llllllllll_opy_.PRE), self.bstack1l1l11l111l_opy_)
        bstack1lll1ll1l11_opy_.bstack1ll1l11lll1_opy_((bstack1lllll1l1l1_opy_.QUIT, bstack1llllllllll_opy_.PRE), self.on_close)
        self.bstack1llll11111l_opy_ = bstack1llll11111l_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11lll1l_opy_(
        self,
        f: bstack1lll1ll1l11_opy_,
        bstack1l1l11ll11l_opy_: object,
        exec: Tuple[bstack1lllllllll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1lllll1l1l1_opy_, bstack1llllllllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l1ll_opy_ (u"ࠧࡲࡡࡶࡰࡦ࡬ࠧዱ"):
            return
        if not bstack1l1llll11ll_opy_():
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡲࡡࡶࡰࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥዲ"))
            return
        def wrapped(bstack1l1l11ll11l_opy_, launch, *args, **kwargs):
            response = self.bstack1l1l11l1ll1_opy_(f.platform_index, instance.ref(), json.dumps({bstack1l1l1ll_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ዳ"): True}).encode(bstack1l1l1ll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢዴ")))
            if response is not None and response.capabilities:
                if not bstack1l1llll11ll_opy_():
                    browser = launch(bstack1l1l11ll11l_opy_)
                    return browser
                bstack1l1l11l1l1l_opy_ = json.loads(response.capabilities.decode(bstack1l1l1ll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣድ")))
                if not bstack1l1l11l1l1l_opy_: # empty caps bstack1l1l11l1lll_opy_ bstack1l1l1l11111_opy_ bstack1l1l11l1l11_opy_ bstack1ll1ll1l1l1_opy_ or error in processing
                    return
                bstack1l1l11ll111_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l11l1l1l_opy_))
                f.bstack1lllllll111_opy_(instance, bstack1lll1ll1l11_opy_.bstack1l1l11lllll_opy_, bstack1l1l11ll111_opy_)
                f.bstack1lllllll111_opy_(instance, bstack1lll1ll1l11_opy_.bstack1l1l111lll1_opy_, bstack1l1l11l1l1l_opy_)
                browser = bstack1l1l11ll11l_opy_.connect(bstack1l1l11ll111_opy_)
                return browser
        return wrapped
    def bstack1l1l11l1111_opy_(
        self,
        f: bstack1lll1ll1l11_opy_,
        Connection: object,
        exec: Tuple[bstack1lllllllll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1lllll1l1l1_opy_, bstack1llllllllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l1ll_opy_ (u"ࠥࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠧዶ"):
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥዷ"))
            return
        if not bstack1l1llll11ll_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1l1l1ll_opy_ (u"ࠬࡶࡡࡳࡣࡰࡷࠬዸ"), {}).get(bstack1l1l1ll_opy_ (u"࠭ࡢࡴࡒࡤࡶࡦࡳࡳࠨዹ")):
                    bstack1l1l111llll_opy_ = args[0][bstack1l1l1ll_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢዺ")][bstack1l1l1ll_opy_ (u"ࠣࡤࡶࡔࡦࡸࡡ࡮ࡵࠥዻ")]
                    session_id = bstack1l1l111llll_opy_.get(bstack1l1l1ll_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡌࡨࠧዼ"))
                    f.bstack1lllllll111_opy_(instance, bstack1lll1ll1l11_opy_.bstack1l1l11ll1ll_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1l1l1ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࠨዽ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1l11l111l_opy_(
        self,
        f: bstack1lll1ll1l11_opy_,
        bstack1l1l11ll11l_opy_: object,
        exec: Tuple[bstack1lllllllll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1lllll1l1l1_opy_, bstack1llllllllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l1ll_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࠧዾ"):
            return
        if not bstack1l1llll11ll_opy_():
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡨࡵ࡮࡯ࡧࡦࡸࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥዿ"))
            return
        def wrapped(bstack1l1l11ll11l_opy_, connect, *args, **kwargs):
            response = self.bstack1l1l11l1ll1_opy_(f.platform_index, instance.ref(), json.dumps({bstack1l1l1ll_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬጀ"): True}).encode(bstack1l1l1ll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨጁ")))
            if response is not None and response.capabilities:
                bstack1l1l11l1l1l_opy_ = json.loads(response.capabilities.decode(bstack1l1l1ll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢጂ")))
                if not bstack1l1l11l1l1l_opy_:
                    return
                bstack1l1l11ll111_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l11l1l1l_opy_))
                if bstack1l1l11l1l1l_opy_.get(bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨጃ")):
                    browser = bstack1l1l11ll11l_opy_.bstack1l1l11l11l1_opy_(bstack1l1l11ll111_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1l11ll111_opy_
                    return connect(bstack1l1l11ll11l_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1l11lll11_opy_(
        self,
        f: bstack1lll1ll1l11_opy_,
        bstack1l1lllll111_opy_: object,
        exec: Tuple[bstack1lllllllll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1lllll1l1l1_opy_, bstack1llllllllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l1ll_opy_ (u"ࠥࡲࡪࡽ࡟ࡱࡣࡪࡩࠧጄ"):
            return
        if not bstack1l1llll11ll_opy_():
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡲࡪࡽ࡟ࡱࡣࡪࡩࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥጅ"))
            return
        def wrapped(bstack1l1lllll111_opy_, bstack1l1l11l11ll_opy_, *args, **kwargs):
            contexts = bstack1l1lllll111_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack1l1l1ll_opy_ (u"ࠧࡧࡢࡰࡷࡷ࠾ࡧࡲࡡ࡯࡭ࠥጆ") in page.url:
                                    return page
                    else:
                        return bstack1l1l11l11ll_opy_(bstack1l1lllll111_opy_)
        return wrapped
    def bstack1l1l11l1ll1_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡹࡨࡦࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦጇ") + str(req) + bstack1l1l1ll_opy_ (u"ࠢࠣገ"))
        try:
            r = self.bstack1lll11ll1l1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l1l1ll_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦጉ") + str(r.success) + bstack1l1l1ll_opy_ (u"ࠤࠥጊ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1ll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣጋ") + str(e) + bstack1l1l1ll_opy_ (u"ࠦࠧጌ"))
            traceback.print_exc()
            raise e
    def bstack1l1l11ll1l1_opy_(
        self,
        f: bstack1lll1ll1l11_opy_,
        Connection: object,
        exec: Tuple[bstack1lllllllll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1lllll1l1l1_opy_, bstack1llllllllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l1ll_opy_ (u"ࠧࡥࡳࡦࡰࡧࡣࡲ࡫ࡳࡴࡣࡪࡩࡤࡺ࡯ࡠࡵࡨࡶࡻ࡫ࡲࠣግ"):
            return
        if not bstack1l1llll11ll_opy_():
            return
        def wrapped(Connection, bstack1l1l11llll1_opy_, *args, **kwargs):
            return bstack1l1l11llll1_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1lll1ll1l11_opy_,
        bstack1l1l11ll11l_opy_: object,
        exec: Tuple[bstack1lllllllll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1lllll1l1l1_opy_, bstack1llllllllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l1ll_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧጎ"):
            return
        if not bstack1l1llll11ll_opy_():
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦࡣ࡭ࡱࡶࡩࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥጏ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped