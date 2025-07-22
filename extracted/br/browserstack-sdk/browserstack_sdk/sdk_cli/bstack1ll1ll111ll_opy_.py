# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1lll1l1111l_opy_ import bstack1llll1l1l11_opy_
from browserstack_sdk.sdk_cli.bstack1llll1lll1l_opy_ import (
    bstack1lllllll11l_opy_,
    bstack1llllll1111_opy_,
    bstack1lllll1ll1l_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1ll1llll11l_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l11ll1l1l_opy_
from bstack_utils.helper import bstack1l1ll11llll_opy_
import threading
import os
import urllib.parse
class bstack1lll1lll1l1_opy_(bstack1llll1l1l11_opy_):
    def __init__(self, bstack1ll1ll1ll11_opy_):
        super().__init__()
        bstack1ll1llll11l_opy_.bstack1ll11l1l11l_opy_((bstack1lllllll11l_opy_.bstack1lllll11lll_opy_, bstack1llllll1111_opy_.PRE), self.bstack1l1l11ll111_opy_)
        bstack1ll1llll11l_opy_.bstack1ll11l1l11l_opy_((bstack1lllllll11l_opy_.bstack1lllll11lll_opy_, bstack1llllll1111_opy_.PRE), self.bstack1l1l11lllll_opy_)
        bstack1ll1llll11l_opy_.bstack1ll11l1l11l_opy_((bstack1lllllll11l_opy_.bstack111111111l_opy_, bstack1llllll1111_opy_.PRE), self.bstack1l1l11l1111_opy_)
        bstack1ll1llll11l_opy_.bstack1ll11l1l11l_opy_((bstack1lllllll11l_opy_.bstack1llllll11ll_opy_, bstack1llllll1111_opy_.PRE), self.bstack1l1l111llll_opy_)
        bstack1ll1llll11l_opy_.bstack1ll11l1l11l_opy_((bstack1lllllll11l_opy_.bstack1lllll11lll_opy_, bstack1llllll1111_opy_.PRE), self.bstack1l1l11l1ll1_opy_)
        bstack1ll1llll11l_opy_.bstack1ll11l1l11l_opy_((bstack1lllllll11l_opy_.QUIT, bstack1llllll1111_opy_.PRE), self.on_close)
        self.bstack1ll1ll1ll11_opy_ = bstack1ll1ll1ll11_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11ll111_opy_(
        self,
        f: bstack1ll1llll11l_opy_,
        bstack1l1l11llll1_opy_: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111l111_opy_ (u"ࠦࡱࡧࡵ࡯ࡥ࡫ࠦዩ"):
            return
        if not bstack1l1ll11llll_opy_():
            self.logger.debug(bstack111l111_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡱࡧࡵ࡯ࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤዪ"))
            return
        def wrapped(bstack1l1l11llll1_opy_, launch, *args, **kwargs):
            response = self.bstack1l1l11ll1l1_opy_(f.platform_index, instance.ref(), json.dumps({bstack111l111_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬያ"): True}).encode(bstack111l111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨዬ")))
            if response is not None and response.capabilities:
                if not bstack1l1ll11llll_opy_():
                    browser = launch(bstack1l1l11llll1_opy_)
                    return browser
                bstack1l1l11ll11l_opy_ = json.loads(response.capabilities.decode(bstack111l111_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢይ")))
                if not bstack1l1l11ll11l_opy_: # empty caps bstack1l1l11l1l1l_opy_ bstack1l1l11l1lll_opy_ bstack1l1l11l11ll_opy_ bstack1ll1l1ll1l1_opy_ or error in processing
                    return
                bstack1l1l11ll1ll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l11ll11l_opy_))
                f.bstack1111111111_opy_(instance, bstack1ll1llll11l_opy_.bstack1l1l11l11l1_opy_, bstack1l1l11ll1ll_opy_)
                f.bstack1111111111_opy_(instance, bstack1ll1llll11l_opy_.bstack1l1l111ll1l_opy_, bstack1l1l11ll11l_opy_)
                browser = bstack1l1l11llll1_opy_.connect(bstack1l1l11ll1ll_opy_)
                return browser
        return wrapped
    def bstack1l1l11l1111_opy_(
        self,
        f: bstack1ll1llll11l_opy_,
        Connection: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111l111_opy_ (u"ࠤࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠦዮ"):
            self.logger.debug(bstack111l111_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤዯ"))
            return
        if not bstack1l1ll11llll_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack111l111_opy_ (u"ࠫࡵࡧࡲࡢ࡯ࡶࠫደ"), {}).get(bstack111l111_opy_ (u"ࠬࡨࡳࡑࡣࡵࡥࡲࡹࠧዱ")):
                    bstack1l1l11lll1l_opy_ = args[0][bstack111l111_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨዲ")][bstack111l111_opy_ (u"ࠢࡣࡵࡓࡥࡷࡧ࡭ࡴࠤዳ")]
                    session_id = bstack1l1l11lll1l_opy_.get(bstack111l111_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡋࡧࠦዴ"))
                    f.bstack1111111111_opy_(instance, bstack1ll1llll11l_opy_.bstack1l1l111lll1_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack111l111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡦ࡬ࡷࡵࡧࡴࡤࡪࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࠧድ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1l11l1ll1_opy_(
        self,
        f: bstack1ll1llll11l_opy_,
        bstack1l1l11llll1_opy_: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111l111_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦዶ"):
            return
        if not bstack1l1ll11llll_opy_():
            self.logger.debug(bstack111l111_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡧࡴࡴ࡮ࡦࡥࡷࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤዷ"))
            return
        def wrapped(bstack1l1l11llll1_opy_, connect, *args, **kwargs):
            response = self.bstack1l1l11ll1l1_opy_(f.platform_index, instance.ref(), json.dumps({bstack111l111_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫዸ"): True}).encode(bstack111l111_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧዹ")))
            if response is not None and response.capabilities:
                bstack1l1l11ll11l_opy_ = json.loads(response.capabilities.decode(bstack111l111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨዺ")))
                if not bstack1l1l11ll11l_opy_:
                    return
                bstack1l1l11ll1ll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l11ll11l_opy_))
                if bstack1l1l11ll11l_opy_.get(bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧዻ")):
                    browser = bstack1l1l11llll1_opy_.bstack1l1l11l1l11_opy_(bstack1l1l11ll1ll_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1l11ll1ll_opy_
                    return connect(bstack1l1l11llll1_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1l11lllll_opy_(
        self,
        f: bstack1ll1llll11l_opy_,
        bstack1l1lllll11l_opy_: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111l111_opy_ (u"ࠤࡱࡩࡼࡥࡰࡢࡩࡨࠦዼ"):
            return
        if not bstack1l1ll11llll_opy_():
            self.logger.debug(bstack111l111_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡱࡩࡼࡥࡰࡢࡩࡨࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤዽ"))
            return
        def wrapped(bstack1l1lllll11l_opy_, bstack1l1l11lll11_opy_, *args, **kwargs):
            contexts = bstack1l1lllll11l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack111l111_opy_ (u"ࠦࡦࡨ࡯ࡶࡶ࠽ࡦࡱࡧ࡮࡬ࠤዾ") in page.url:
                                    return page
                    else:
                        return bstack1l1l11lll11_opy_(bstack1l1lllll11l_opy_)
        return wrapped
    def bstack1l1l11ll1l1_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack111l111_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴ࠻ࠢࠥዿ") + str(req) + bstack111l111_opy_ (u"ࠨࠢጀ"))
        try:
            r = self.bstack1lll1l11l1l_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack111l111_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࡵࡸࡧࡨ࡫ࡳࡴ࠿ࠥጁ") + str(r.success) + bstack111l111_opy_ (u"ࠣࠤጂ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111l111_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢጃ") + str(e) + bstack111l111_opy_ (u"ࠥࠦጄ"))
            traceback.print_exc()
            raise e
    def bstack1l1l111llll_opy_(
        self,
        f: bstack1ll1llll11l_opy_,
        Connection: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111l111_opy_ (u"ࠦࡤࡹࡥ࡯ࡦࡢࡱࡪࡹࡳࡢࡩࡨࡣࡹࡵ࡟ࡴࡧࡵࡺࡪࡸࠢጅ"):
            return
        if not bstack1l1ll11llll_opy_():
            return
        def wrapped(Connection, bstack1l1l11l111l_opy_, *args, **kwargs):
            return bstack1l1l11l111l_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1ll1llll11l_opy_,
        bstack1l1l11llll1_opy_: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111l111_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࠦጆ"):
            return
        if not bstack1l1ll11llll_opy_():
            self.logger.debug(bstack111l111_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡩ࡬ࡰࡵࡨࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤጇ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped