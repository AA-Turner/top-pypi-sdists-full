# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll111llll1_opy_ import bstack1l1llll1l11_opy_
from browserstack_sdk.sdk_cli.bstack1ll11ll1_opy_ import (
    bstack111l11ll_opy_,
    bstack1lll1ll11_opy_,
    bstack1ll11l1l111_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack11llll11l1_opy_ import bstack11ll1l1l_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack111ll1ll_opy_
from bstack_utils.helper import bstack1l11l1111l_opy_
import threading
import os
import urllib.parse
class bstack1l1lll1l111_opy_(bstack1l1llll1l11_opy_):
    @staticmethod
    def bstack11llll111ll_opy_(bstack1ll1111lll_opy_: dict) -> bool:
        browser_name = (
            bstack1ll1111lll_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᘃ"))
            or bstack1ll1111lll_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩᘄ"))
            or bstack1ll1111lll_opy_.get(bstack1ll1lll_opy_ (u"ࠩࡧࡩ࡫ࡧࡵ࡭ࡶࡅࡶࡴࡽࡳࡦࡴࡗࡽࡵ࡫ࠧᘅ"))
            or bstack1ll1lll_opy_ (u"ࠪࠫᘆ")
        ).lower()
        return browser_name in bstack11l1111lll_opy_
    def __init__(self, bstack1l1lllll1ll_opy_):
        super().__init__()
        bstack11ll1l1l_opy_.bstack1l11l1lllll_opy_((bstack111l11ll_opy_.bstack11ll1lll1_opy_, bstack1lll1ll11_opy_.PRE), self.bstack11llll11ll1_opy_)
        bstack11ll1l1l_opy_.bstack1l11l1lllll_opy_((bstack111l11ll_opy_.bstack11ll1lll1_opy_, bstack1lll1ll11_opy_.PRE), self.bstack11lll1lll1l_opy_)
        bstack11ll1l1l_opy_.bstack1l11l1lllll_opy_((bstack111l11ll_opy_.bstack1ll11l1lll1_opy_, bstack1lll1ll11_opy_.PRE), self.bstack11lll1ll11l_opy_)
        bstack11ll1l1l_opy_.bstack1l11l1lllll_opy_((bstack111l11ll_opy_.bstack1ll1ll111l1_opy_, bstack1lll1ll11_opy_.PRE), self.bstack11llll1111l_opy_)
        bstack11ll1l1l_opy_.bstack1l11l1lllll_opy_((bstack111l11ll_opy_.bstack11ll1lll1_opy_, bstack1lll1ll11_opy_.PRE), self.bstack11lll1l1ll1_opy_)
        bstack11ll1l1l_opy_.bstack1l11l1lllll_opy_((bstack111l11ll_opy_.QUIT, bstack1lll1ll11_opy_.PRE), self.on_close)
        self.bstack1l1lllll1ll_opy_ = bstack1l1lllll1ll_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack11llll11ll1_opy_(
        self,
        f: bstack11ll1l1l_opy_,
        bstack11llll11l1l_opy_: object,
        exec: Tuple[bstack1ll11l1l111_opy_, str],
        bstack1ll11l1ll11_opy_: Tuple[bstack111l11ll_opy_, bstack1lll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1lll_opy_ (u"ࠦࡱࡧࡵ࡯ࡥ࡫ࠦᘇ"):
            return
        if not bstack1l11l1111l_opy_():
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡱࡧࡵ࡯ࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᘈ"))
            return
        def wrapped(bstack11llll11l1l_opy_, launch, *args, **kwargs):
            response = self.bstack11lll1l1l1l_opy_(f.platform_index, instance.ref(), json.dumps({bstack1ll1lll_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᘉ"): True}).encode(bstack1ll1lll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᘊ")))
            if response is not None and response.capabilities:
                if not bstack1l11l1111l_opy_():
                    browser = launch(bstack11llll11l1l_opy_)
                    return browser
                bstack1ll1111lll_opy_ = json.loads(response.capabilities.decode(bstack1ll1lll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᘋ")))
                if not bstack1ll1111lll_opy_: # empty caps bstack11llll11111_opy_ bstack11lll1ll111_opy_ bstack11lll1ll1ll_opy_ bstack11lll1ll1l1_opy_ or error in processing
                    return
                bstack11lll1l1lll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1ll1111lll_opy_))
                f.bstack1l1l11lll_opy_(instance, bstack11ll1l1l_opy_.bstack1l111ll111_opy_, bstack11lll1l1lll_opy_)
                f.bstack1l1l11lll_opy_(instance, bstack11ll1l1l_opy_.bstack11111l11l_opy_, bstack1ll1111lll_opy_)
                browser = bstack11llll11l1l_opy_.connect(bstack11lll1l1lll_opy_)
                return browser
        return wrapped
    def bstack11lll1ll11l_opy_(
        self,
        f: bstack11ll1l1l_opy_,
        Connection: object,
        exec: Tuple[bstack1ll11l1l111_opy_, str],
        bstack1ll11l1ll11_opy_: Tuple[bstack111l11ll_opy_, bstack1lll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1lll_opy_ (u"ࠤࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠦᘌ"):
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᘍ"))
            return
        if not bstack1l11l1111l_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1ll1lll_opy_ (u"ࠫࡵࡧࡲࡢ࡯ࡶࠫᘎ"), {}).get(bstack1ll1lll_opy_ (u"ࠬࡨࡳࡑࡣࡵࡥࡲࡹࠧᘏ")):
                    bstack11llll111l1_opy_ = args[0][bstack1ll1lll_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨᘐ")][bstack1ll1lll_opy_ (u"ࠢࡣࡵࡓࡥࡷࡧ࡭ࡴࠤᘑ")]
                    session_id = bstack11llll111l1_opy_.get(bstack1ll1lll_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡋࡧࠦᘒ"))
                    f.bstack1l1l11lll_opy_(instance, bstack11ll1l1l_opy_.bstack1ll1l1l111l_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡦ࡬ࡷࡵࡧࡴࡤࡪࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࠧᘓ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack11lll1l1ll1_opy_(
        self,
        f: bstack11ll1l1l_opy_,
        bstack11llll11l1l_opy_: object,
        exec: Tuple[bstack1ll11l1l111_opy_, str],
        bstack1ll11l1ll11_opy_: Tuple[bstack111l11ll_opy_, bstack1lll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1lll_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦᘔ"):
            return
        if not bstack1l11l1111l_opy_():
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡧࡴࡴ࡮ࡦࡥࡷࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᘕ"))
            return
        def wrapped(bstack11llll11l1l_opy_, connect, *args, **kwargs):
            response = self.bstack11lll1l1l1l_opy_(f.platform_index, instance.ref(), json.dumps({bstack1ll1lll_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᘖ"): True}).encode(bstack1ll1lll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᘗ")))
            if response is not None and response.capabilities:
                bstack1ll1111lll_opy_ = json.loads(response.capabilities.decode(bstack1ll1lll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᘘ")))
                if not bstack1ll1111lll_opy_:
                    return
                if bstack1ll1111lll_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᘙ")) and not self.bstack11llll111ll_opy_(bstack1ll1111lll_opy_):
                    bstack1ll1111lll_opy_[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᘚ")] = False
                    bstack11lll1lll11_opy_ = [bstack11lll1lllll_opy_ for bstack11lll1lllll_opy_ in bstack1ll1111lll_opy_ if bstack11lll1lllll_opy_.startswith(bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᘛ"))]
                    for bstack11lll1lllll_opy_ in bstack11lll1lll11_opy_:
                        del bstack1ll1111lll_opy_[bstack11lll1lllll_opy_]
                bstack11lll1l1lll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1ll1111lll_opy_))
                if bstack1ll1111lll_opy_.get(bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᘜ")):
                    browser = bstack11llll11l1l_opy_.connect_over_cdp(bstack11lll1l1lll_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack11lll1l1lll_opy_
                    return connect(bstack11llll11l1l_opy_, *args, **kwargs)
        return wrapped
    def bstack11lll1lll1l_opy_(
        self,
        f: bstack11ll1l1l_opy_,
        bstack1l11l11l1ll_opy_: object,
        exec: Tuple[bstack1ll11l1l111_opy_, str],
        bstack1ll11l1ll11_opy_: Tuple[bstack111l11ll_opy_, bstack1lll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1lll_opy_ (u"ࠧࡴࡥࡸࡡࡳࡥ࡬࡫ࠢᘝ"):
            return
        if not bstack1l11l1111l_opy_():
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡴࡥࡸࡡࡳࡥ࡬࡫ࠠ࡮ࡧࡷ࡬ࡴࡪࠬࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧᘞ"))
            return
        def wrapped(bstack1l11l11l1ll_opy_, bstack11lll1llll1_opy_, *args, **kwargs):
            contexts = bstack1l11l11l1ll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1ll1lll_opy_ (u"ࠢࡢࡤࡲࡹࡹࡀࡢ࡭ࡣࡱ࡯ࠧᘟ") in page.url:
                                return page
                            else:
                                return bstack11lll1llll1_opy_(bstack1l11l11l1ll_opy_)
                    else:
                        return bstack11lll1llll1_opy_(bstack1l11l11l1ll_opy_)
        return wrapped
    def bstack11lll1l1l1l_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᘠ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸ࠿ࠦࠢᘡ") + str(req) + bstack1ll1lll_opy_ (u"ࠥࠦᘢ"))
        try:
            r = self.bstack1l1ll1l1ll1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࡹࡵࡤࡥࡨࡷࡸࡃࠢᘣ") + str(r.success) + bstack1ll1lll_opy_ (u"ࠧࠨᘤ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᘥ") + str(e) + bstack1ll1lll_opy_ (u"ࠢࠣᘦ"))
            traceback.print_exc()
            raise e
    def bstack11llll1111l_opy_(
        self,
        f: bstack11ll1l1l_opy_,
        Connection: object,
        exec: Tuple[bstack1ll11l1l111_opy_, str],
        bstack1ll11l1ll11_opy_: Tuple[bstack111l11ll_opy_, bstack1lll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1lll_opy_ (u"ࠣࡡࡶࡩࡳࡪ࡟࡮ࡧࡶࡷࡦ࡭ࡥࡠࡶࡲࡣࡸ࡫ࡲࡷࡧࡵࠦᘧ"):
            return
        if not bstack1l11l1111l_opy_():
            return
        def wrapped(Connection, bstack11llll11l11_opy_, *args, **kwargs):
            return bstack11llll11l11_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack11ll1l1l_opy_,
        bstack11llll11l1l_opy_: object,
        exec: Tuple[bstack1ll11l1l111_opy_, str],
        bstack1ll11l1ll11_opy_: Tuple[bstack111l11ll_opy_, bstack1lll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1lll_opy_ (u"ࠤࡦࡰࡴࡹࡥࠣᘨ"):
            return
        if not bstack1l11l1111l_opy_():
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡦࡰࡴࡹࡥࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨᘩ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped