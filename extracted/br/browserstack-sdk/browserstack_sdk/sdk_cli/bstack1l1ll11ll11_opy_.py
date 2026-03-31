# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1l1l1l11111_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1l11111ll_opy_ import (
    bstack1ll1l1ll11_opy_,
    bstack1ll11ll1ll_opy_,
    bstack1ll111lllll_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1l1ll1l11l_opy_ import bstack1l111lllll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l1111l1_opy_
from bstack_utils.helper import bstack1l111l1111_opy_
import threading
import os
import urllib.parse
class bstack1l1llllll1l_opy_(bstack1ll111l11ll_opy_):
    @staticmethod
    def bstack11lll1ll1l1_opy_(bstack1111l1lll1_opy_: dict) -> bool:
        browser_name = (
            bstack1111l1lll1_opy_.get(bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᘬ"))
            or bstack1111l1lll1_opy_.get(bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨᘭ"))
            or bstack1111l1lll1_opy_.get(bstack1ll11_opy_ (u"ࠨࡦࡨࡪࡦࡻ࡬ࡵࡄࡵࡳࡼࡹࡥࡳࡖࡼࡴࡪ࠭ᘮ"))
            or bstack1ll11_opy_ (u"ࠩࠪᘯ")
        ).lower()
        return browser_name in bstack1111l111l1_opy_
    def __init__(self, bstack1l1l1l1ll11_opy_):
        super().__init__()
        bstack1l111lllll_opy_.bstack1l11lll1lll_opy_((bstack1ll1l1ll11_opy_.bstack1ll11lllll_opy_, bstack1ll11ll1ll_opy_.PRE), self.bstack11lll11ll1l_opy_)
        bstack1l111lllll_opy_.bstack1l11lll1lll_opy_((bstack1ll1l1ll11_opy_.bstack1ll11lllll_opy_, bstack1ll11ll1ll_opy_.PRE), self.bstack11lll1ll11l_opy_)
        bstack1l111lllll_opy_.bstack1l11lll1lll_opy_((bstack1ll1l1ll11_opy_.bstack1ll111lll11_opy_, bstack1ll11ll1ll_opy_.PRE), self.bstack11lll1l1lll_opy_)
        bstack1l111lllll_opy_.bstack1l11lll1lll_opy_((bstack1ll1l1ll11_opy_.bstack1ll1l1l1ll1_opy_, bstack1ll11ll1ll_opy_.PRE), self.bstack11lll1l1111_opy_)
        bstack1l111lllll_opy_.bstack1l11lll1lll_opy_((bstack1ll1l1ll11_opy_.bstack1ll11lllll_opy_, bstack1ll11ll1ll_opy_.PRE), self.bstack11lll1ll1ll_opy_)
        bstack1l111lllll_opy_.bstack1l11lll1lll_opy_((bstack1ll1l1ll11_opy_.QUIT, bstack1ll11ll1ll_opy_.PRE), self.on_close)
        self.bstack1l1l1l1ll11_opy_ = bstack1l1l1l1ll11_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack11lll11ll1l_opy_(
        self,
        f: bstack1l111lllll_opy_,
        bstack11lll1l1ll1_opy_: object,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll11_opy_ (u"ࠥࡰࡦࡻ࡮ࡤࡪࠥᘰ"):
            return
        if not bstack1l111l1111_opy_():
            self.logger.debug(bstack1ll11_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡰࡦࡻ࡮ࡤࡪࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᘱ"))
            return
        def wrapped(bstack11lll1l1ll1_opy_, launch, *args, **kwargs):
            response = self.bstack11lll1l1l11_opy_(f.platform_index, instance.ref(), json.dumps({bstack1ll11_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᘲ"): True}).encode(bstack1ll11_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᘳ")))
            if response is not None and response.capabilities:
                if not bstack1l111l1111_opy_():
                    browser = launch(bstack11lll1l1ll1_opy_)
                    return browser
                bstack1111l1lll1_opy_ = json.loads(response.capabilities.decode(bstack1ll11_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᘴ")))
                if not bstack1111l1lll1_opy_: # empty caps bstack11lll11llll_opy_ bstack11lll1l11l1_opy_ bstack11lll1ll111_opy_ bstack11lll1l111l_opy_ or error in processing
                    return
                bstack11lll1lll11_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1111l1lll1_opy_))
                f.bstack1l11lllll_opy_(instance, bstack1l111lllll_opy_.bstack1ll11l1lll_opy_, bstack11lll1lll11_opy_)
                f.bstack1l11lllll_opy_(instance, bstack1l111lllll_opy_.bstack1lll1l1111_opy_, bstack1111l1lll1_opy_)
                browser = bstack11lll1l1ll1_opy_.connect(bstack11lll1lll11_opy_)
                return browser
        return wrapped
    def bstack11lll1l1lll_opy_(
        self,
        f: bstack1l111lllll_opy_,
        Connection: object,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll11_opy_ (u"ࠣࡦ࡬ࡷࡵࡧࡴࡤࡪࠥᘵ"):
            self.logger.debug(bstack1ll11_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡦ࡬ࡷࡵࡧࡴࡤࡪࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᘶ"))
            return
        if not bstack1l111l1111_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1ll11_opy_ (u"ࠪࡴࡦࡸࡡ࡮ࡵࠪᘷ"), {}).get(bstack1ll11_opy_ (u"ࠫࡧࡹࡐࡢࡴࡤࡱࡸ࠭ᘸ")):
                    bstack11lll11ll11_opy_ = args[0][bstack1ll11_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧᘹ")][bstack1ll11_opy_ (u"ࠨࡢࡴࡒࡤࡶࡦࡳࡳࠣᘺ")]
                    session_id = bstack11lll11ll11_opy_.get(bstack1ll11_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡊࡦࠥᘻ"))
                    f.bstack1l11lllll_opy_(instance, bstack1l111lllll_opy_.bstack1ll1l1l1lll_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡥ࡫ࡶࡴࡦࡺࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠣࠦᘼ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack11lll1ll1ll_opy_(
        self,
        f: bstack1l111lllll_opy_,
        bstack11lll1l1ll1_opy_: object,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll11_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࠥᘽ"):
            return
        if not bstack1l111l1111_opy_():
            self.logger.debug(bstack1ll11_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡦࡳࡳࡴࡥࡤࡶࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᘾ"))
            return
        def wrapped(bstack11lll1l1ll1_opy_, connect, *args, **kwargs):
            response = self.bstack11lll1l1l11_opy_(f.platform_index, instance.ref(), json.dumps({bstack1ll11_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᘿ"): True}).encode(bstack1ll11_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᙀ")))
            if response is not None and response.capabilities:
                bstack1111l1lll1_opy_ = json.loads(response.capabilities.decode(bstack1ll11_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᙁ")))
                if not bstack1111l1lll1_opy_:
                    return
                if bstack1111l1lll1_opy_.get(bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᙂ")) and not self.bstack11lll1ll1l1_opy_(bstack1111l1lll1_opy_):
                    bstack1111l1lll1_opy_[bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᙃ")] = False
                    bstack11lll1l1l1l_opy_ = [bstack11lll11lll1_opy_ for bstack11lll11lll1_opy_ in bstack1111l1lll1_opy_ if bstack11lll11lll1_opy_.startswith(bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᙄ"))]
                    for bstack11lll11lll1_opy_ in bstack11lll1l1l1l_opy_:
                        del bstack1111l1lll1_opy_[bstack11lll11lll1_opy_]
                bstack11lll1lll11_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1111l1lll1_opy_))
                if bstack1111l1lll1_opy_.get(bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᙅ")):
                    browser = bstack11lll1l1ll1_opy_.connect_over_cdp(bstack11lll1lll11_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack11lll1lll11_opy_
                    return connect(bstack11lll1l1ll1_opy_, *args, **kwargs)
        return wrapped
    def bstack11lll1ll11l_opy_(
        self,
        f: bstack1l111lllll_opy_,
        bstack1l111lll1l1_opy_: object,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll11_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨᙆ"):
            return
        if not bstack1l111l1111_opy_():
            self.logger.debug(bstack1ll11_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦᙇ"))
            return
        def wrapped(bstack1l111lll1l1_opy_, bstack11lll11l1ll_opy_, *args, **kwargs):
            contexts = bstack1l111lll1l1_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1ll11_opy_ (u"ࠨࡡࡣࡱࡸࡸ࠿ࡨ࡬ࡢࡰ࡮ࠦᙈ") in page.url:
                                return page
                            else:
                                return bstack11lll11l1ll_opy_(bstack1l111lll1l1_opy_)
                    else:
                        return bstack11lll11l1ll_opy_(bstack1l111lll1l1_opy_)
        return wrapped
    def bstack11lll1l1l11_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.client_worker_id = bstack1ll11_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᙉ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1ll11_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡻࡪࡨࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷ࠾ࠥࠨᙊ") + str(req) + bstack1ll11_opy_ (u"ࠤࠥᙋ"))
        try:
            r = self.bstack1l1ll1ll111_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1ll11_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࡸࡻࡣࡤࡧࡶࡷࡂࠨᙌ") + str(r.success) + bstack1ll11_opy_ (u"ࠦࠧᙍ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᙎ") + str(e) + bstack1ll11_opy_ (u"ࠨࠢᙏ"))
            traceback.print_exc()
            raise e
    def bstack11lll1l1111_opy_(
        self,
        f: bstack1l111lllll_opy_,
        Connection: object,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll11_opy_ (u"ࠢࡠࡵࡨࡲࡩࡥ࡭ࡦࡵࡶࡥ࡬࡫࡟ࡵࡱࡢࡷࡪࡸࡶࡦࡴࠥᙐ"):
            return
        if not bstack1l111l1111_opy_():
            return
        def wrapped(Connection, bstack11lll1l11ll_opy_, *args, **kwargs):
            return bstack11lll1l11ll_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1l111lllll_opy_,
        bstack11lll1l1ll1_opy_: object,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll11_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࠢᙑ"):
            return
        if not bstack1l111l1111_opy_():
            self.logger.debug(bstack1ll11_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡥ࡯ࡳࡸ࡫ࠠ࡮ࡧࡷ࡬ࡴࡪࠬࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧᙒ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped