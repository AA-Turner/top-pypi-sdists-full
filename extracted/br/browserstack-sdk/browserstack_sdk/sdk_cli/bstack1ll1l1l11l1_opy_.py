# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1lll111lll1_opy_ import bstack1ll1l1llll1_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1llll1l11ll_opy_,
    bstack1lllllll111_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1llll111l11_opy_ import bstack1ll1l1lllll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11lll1lll1_opy_
from bstack_utils.helper import bstack1l1lll11ll1_opy_
import threading
import os
import urllib.parse
class bstack1ll1ll1ll1l_opy_(bstack1ll1l1llll1_opy_):
    def __init__(self, bstack1llll1111l1_opy_):
        super().__init__()
        bstack1ll1l1lllll_opy_.bstack1ll11ll111l_opy_((bstack1lllll1l111_opy_.bstack1llll1lll1l_opy_, bstack1llll1l11ll_opy_.PRE), self.bstack1l1l11l111l_opy_)
        bstack1ll1l1lllll_opy_.bstack1ll11ll111l_opy_((bstack1lllll1l111_opy_.bstack1llll1lll1l_opy_, bstack1llll1l11ll_opy_.PRE), self.bstack1l1l111llll_opy_)
        bstack1ll1l1lllll_opy_.bstack1ll11ll111l_opy_((bstack1lllll1l111_opy_.bstack1lllll11ll1_opy_, bstack1llll1l11ll_opy_.PRE), self.bstack1l1l11ll111_opy_)
        bstack1ll1l1lllll_opy_.bstack1ll11ll111l_opy_((bstack1lllll1l111_opy_.bstack1lllll1lll1_opy_, bstack1llll1l11ll_opy_.PRE), self.bstack1l1l11l1111_opy_)
        bstack1ll1l1lllll_opy_.bstack1ll11ll111l_opy_((bstack1lllll1l111_opy_.bstack1llll1lll1l_opy_, bstack1llll1l11ll_opy_.PRE), self.bstack1l1l111l111_opy_)
        bstack1ll1l1lllll_opy_.bstack1ll11ll111l_opy_((bstack1lllll1l111_opy_.QUIT, bstack1llll1l11ll_opy_.PRE), self.on_close)
        self.bstack1llll1111l1_opy_ = bstack1llll1111l1_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11l111l_opy_(
        self,
        f: bstack1ll1l1lllll_opy_,
        bstack1l1l111l1ll_opy_: object,
        exec: Tuple[bstack1lllllll111_opy_, str],
        bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l11ll1_opy_ (u"ࠣ࡮ࡤࡹࡳࡩࡨࠣዴ"):
            return
        if not bstack1l1lll11ll1_opy_():
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡ࡮ࡤࡹࡳࡩࡨࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨድ"))
            return
        def wrapped(bstack1l1l111l1ll_opy_, launch, *args, **kwargs):
            response = self.bstack1l1l11l1l11_opy_(f.platform_index, instance.ref(), json.dumps({bstack1l11ll1_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩዶ"): True}).encode(bstack1l11ll1_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥዷ")))
            if response is not None and response.capabilities:
                if not bstack1l1lll11ll1_opy_():
                    browser = launch(bstack1l1l111l1ll_opy_)
                    return browser
                bstack1l1l111l11l_opy_ = json.loads(response.capabilities.decode(bstack1l11ll1_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦዸ")))
                if not bstack1l1l111l11l_opy_: # empty caps bstack1l1l111ll11_opy_ bstack1l1l111l1l1_opy_ bstack1l1l11ll11l_opy_ bstack1lll1ll1lll_opy_ or error in processing
                    return
                bstack1l1l11l1lll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l111l11l_opy_))
                f.bstack1llllll1ll1_opy_(instance, bstack1ll1l1lllll_opy_.bstack1l1l11l1ll1_opy_, bstack1l1l11l1lll_opy_)
                f.bstack1llllll1ll1_opy_(instance, bstack1ll1l1lllll_opy_.bstack1l1l111lll1_opy_, bstack1l1l111l11l_opy_)
                browser = bstack1l1l111l1ll_opy_.connect(bstack1l1l11l1lll_opy_)
                return browser
        return wrapped
    def bstack1l1l11ll111_opy_(
        self,
        f: bstack1ll1l1lllll_opy_,
        Connection: object,
        exec: Tuple[bstack1lllllll111_opy_, str],
        bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l11ll1_opy_ (u"ࠨࡤࡪࡵࡳࡥࡹࡩࡨࠣዹ"):
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦࡤࡪࡵࡳࡥࡹࡩࡨࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨዺ"))
            return
        if not bstack1l1lll11ll1_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1l11ll1_opy_ (u"ࠨࡲࡤࡶࡦࡳࡳࠨዻ"), {}).get(bstack1l11ll1_opy_ (u"ࠩࡥࡷࡕࡧࡲࡢ࡯ࡶࠫዼ")):
                    bstack1l1l111ll1l_opy_ = args[0][bstack1l11ll1_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡵࠥዽ")][bstack1l11ll1_opy_ (u"ࠦࡧࡹࡐࡢࡴࡤࡱࡸࠨዾ")]
                    session_id = bstack1l1l111ll1l_opy_.get(bstack1l11ll1_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡏࡤࠣዿ"))
                    f.bstack1llllll1ll1_opy_(instance, bstack1ll1l1lllll_opy_.bstack1l1l11l1l1l_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡪࡩࡴࡲࡤࡸࡨ࡮ࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠡࠤጀ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1l111l111_opy_(
        self,
        f: bstack1ll1l1lllll_opy_,
        bstack1l1l111l1ll_opy_: object,
        exec: Tuple[bstack1lllllll111_opy_, str],
        bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l11ll1_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࠣጁ"):
            return
        if not bstack1l1lll11ll1_opy_():
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡤࡱࡱࡲࡪࡩࡴࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨጂ"))
            return
        def wrapped(bstack1l1l111l1ll_opy_, connect, *args, **kwargs):
            response = self.bstack1l1l11l1l11_opy_(f.platform_index, instance.ref(), json.dumps({bstack1l11ll1_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨጃ"): True}).encode(bstack1l11ll1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤጄ")))
            if response is not None and response.capabilities:
                bstack1l1l111l11l_opy_ = json.loads(response.capabilities.decode(bstack1l11ll1_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥጅ")))
                if not bstack1l1l111l11l_opy_:
                    return
                bstack1l1l11l1lll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l111l11l_opy_))
                if bstack1l1l111l11l_opy_.get(bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫጆ")):
                    browser = bstack1l1l111l1ll_opy_.bstack1l1l11l11l1_opy_(bstack1l1l11l1lll_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1l11l1lll_opy_
                    return connect(bstack1l1l111l1ll_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1l111llll_opy_(
        self,
        f: bstack1ll1l1lllll_opy_,
        bstack1l1llll11ll_opy_: object,
        exec: Tuple[bstack1lllllll111_opy_, str],
        bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l11ll1_opy_ (u"ࠨ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠣጇ"):
            return
        if not bstack1l1lll11ll1_opy_():
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨገ"))
            return
        def wrapped(bstack1l1llll11ll_opy_, bstack1l1l11ll1l1_opy_, *args, **kwargs):
            contexts = bstack1l1llll11ll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack1l11ll1_opy_ (u"ࠣࡣࡥࡳࡺࡺ࠺ࡣ࡮ࡤࡲࡰࠨጉ") in page.url:
                                    return page
                    else:
                        return bstack1l1l11ll1l1_opy_(bstack1l1llll11ll_opy_)
        return wrapped
    def bstack1l1l11l1l11_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸ࠿ࠦࠢጊ") + str(req) + bstack1l11ll1_opy_ (u"ࠥࠦጋ"))
        try:
            r = self.bstack1lll111111l_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࡹࡵࡤࡥࡨࡷࡸࡃࠢጌ") + str(r.success) + bstack1l11ll1_opy_ (u"ࠧࠨግ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦጎ") + str(e) + bstack1l11ll1_opy_ (u"ࠢࠣጏ"))
            traceback.print_exc()
            raise e
    def bstack1l1l11l1111_opy_(
        self,
        f: bstack1ll1l1lllll_opy_,
        Connection: object,
        exec: Tuple[bstack1lllllll111_opy_, str],
        bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l11ll1_opy_ (u"ࠣࡡࡶࡩࡳࡪ࡟࡮ࡧࡶࡷࡦ࡭ࡥࡠࡶࡲࡣࡸ࡫ࡲࡷࡧࡵࠦጐ"):
            return
        if not bstack1l1lll11ll1_opy_():
            return
        def wrapped(Connection, bstack1l1l11l11ll_opy_, *args, **kwargs):
            return bstack1l1l11l11ll_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1ll1l1lllll_opy_,
        bstack1l1l111l1ll_opy_: object,
        exec: Tuple[bstack1lllllll111_opy_, str],
        bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l11ll1_opy_ (u"ࠤࡦࡰࡴࡹࡥࠣ጑"):
            return
        if not bstack1l1lll11ll1_opy_():
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡦࡰࡴࡹࡥࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨጒ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped