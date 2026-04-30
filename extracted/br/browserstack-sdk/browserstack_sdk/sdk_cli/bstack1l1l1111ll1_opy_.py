# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1l11l1ll1ll_opy_ import bstack1l1l1111111_opy_
from browserstack_sdk.sdk_cli.bstack1l11ll1ll1_opy_ import (
    bstack1lll11l1l1_opy_,
    bstack1111llll1l_opy_,
    bstack1l1ll11l1ll_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import bstack111l1l11l_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack111ll1l1l1_opy_
from bstack_utils.helper import bstack1lllllll11l_opy_
import threading
import os
import urllib.parse
class bstack1l1l1l111l1_opy_(bstack1l1l1111111_opy_):
    @staticmethod
    def bstack11l1lll11ll_opy_(bstack11111l1l1l_opy_: dict) -> bool:
        browser_name = (
            bstack11111l1l1l_opy_.get(bstack1l1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ᝽"))
            or bstack11111l1l1l_opy_.get(bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩ᝾"))
            or bstack11111l1l1l_opy_.get(bstack1l1111l_opy_ (u"ࠩࡧࡩ࡫ࡧࡵ࡭ࡶࡅࡶࡴࡽࡳࡦࡴࡗࡽࡵ࡫ࠧ᝿"))
            or bstack1l1111l_opy_ (u"ࠪࠫក")
        ).lower()
        return browser_name in bstack11l1111ll_opy_
    def __init__(self, bstack1l1l11ll111_opy_):
        super().__init__()
        bstack111l1l11l_opy_.bstack1l1111lllll_opy_((bstack1lll11l1l1_opy_.bstack1lll1l111_opy_, bstack1111llll1l_opy_.PRE), self.bstack11l1ll1ll1l_opy_)
        bstack111l1l11l_opy_.bstack1l1111lllll_opy_((bstack1lll11l1l1_opy_.bstack1lll1l111_opy_, bstack1111llll1l_opy_.PRE), self.bstack11l1ll1l1ll_opy_)
        bstack111l1l11l_opy_.bstack1l1111lllll_opy_((bstack1lll11l1l1_opy_.bstack1l1ll11llll_opy_, bstack1111llll1l_opy_.PRE), self.bstack11l1lll1l1l_opy_)
        bstack111l1l11l_opy_.bstack1l1111lllll_opy_((bstack1lll11l1l1_opy_.bstack1ll1111ll1l_opy_, bstack1111llll1l_opy_.PRE), self.bstack11l1lll1l11_opy_)
        bstack111l1l11l_opy_.bstack1l1111lllll_opy_((bstack1lll11l1l1_opy_.bstack1lll1l111_opy_, bstack1111llll1l_opy_.PRE), self.bstack11l1lll11l1_opy_)
        bstack111l1l11l_opy_.bstack1l1111lllll_opy_((bstack1lll11l1l1_opy_.QUIT, bstack1111llll1l_opy_.PRE), self.on_close)
        self.bstack1l1l11ll111_opy_ = bstack1l1l11ll111_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack11l1ll1ll1l_opy_(
        self,
        f: bstack111l1l11l_opy_,
        bstack11l1ll1ll11_opy_: object,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1111l_opy_ (u"ࠦࡱࡧࡵ࡯ࡥ࡫ࠦខ"):
            return
        if not bstack1lllllll11l_opy_():
            self.logger.debug(bstack1l1111l_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡱࡧࡵ࡯ࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤគ"))
            return
        def wrapped(bstack11l1ll1ll11_opy_, launch, *args, **kwargs):
            response = self.bstack11l1ll1lll1_opy_(f.platform_index, instance.ref(), json.dumps({bstack1l1111l_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬឃ"): True}).encode(bstack1l1111l_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨង")))
            if response is not None and response.capabilities:
                if not bstack1lllllll11l_opy_():
                    browser = launch(bstack11l1ll1ll11_opy_)
                    return browser
                bstack11111l1l1l_opy_ = json.loads(response.capabilities.decode(bstack1l1111l_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢច")))
                if not bstack11111l1l1l_opy_: # empty caps bstack11l1llll11l_opy_ bstack11l1lll111l_opy_ bstack11l1llll1l1_opy_ bstack11l1lll1111_opy_ or error in processing
                    return
                bstack11l1ll1l1l1_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack11111l1l1l_opy_))
                f.bstack111l1llll1_opy_(instance, bstack111l1l11l_opy_.bstack11111llll_opy_, bstack11l1ll1l1l1_opy_)
                f.bstack111l1llll1_opy_(instance, bstack111l1l11l_opy_.bstack1l111111l_opy_, bstack11111l1l1l_opy_)
                browser = bstack11l1ll1ll11_opy_.connect(bstack11l1ll1l1l1_opy_)
                return browser
        return wrapped
    def bstack11l1lll1l1l_opy_(
        self,
        f: bstack111l1l11l_opy_,
        Connection: object,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1111l_opy_ (u"ࠤࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠦឆ"):
            self.logger.debug(bstack1l1111l_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤជ"))
            return
        if not bstack1lllllll11l_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1l1111l_opy_ (u"ࠫࡵࡧࡲࡢ࡯ࡶࠫឈ"), {}).get(bstack1l1111l_opy_ (u"ࠬࡨࡳࡑࡣࡵࡥࡲࡹࠧញ")):
                    bstack11l1ll1l11l_opy_ = args[0][bstack1l1111l_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨដ")][bstack1l1111l_opy_ (u"ࠢࡣࡵࡓࡥࡷࡧ࡭ࡴࠤឋ")]
                    session_id = bstack11l1ll1l11l_opy_.get(bstack1l1111l_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡋࡧࠦឌ"))
                    f.bstack111l1llll1_opy_(instance, bstack111l1l11l_opy_.bstack1l1lllll1l1_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡦ࡬ࡷࡵࡧࡴࡤࡪࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࠧឍ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack11l1lll11l1_opy_(
        self,
        f: bstack111l1l11l_opy_,
        bstack11l1ll1ll11_opy_: object,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1111l_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦណ"):
            return
        if not bstack1lllllll11l_opy_():
            self.logger.debug(bstack1l1111l_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡧࡴࡴ࡮ࡦࡥࡷࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤត"))
            return
        def wrapped(bstack11l1ll1ll11_opy_, connect, *args, **kwargs):
            response = self.bstack11l1ll1lll1_opy_(f.platform_index, instance.ref(), json.dumps({bstack1l1111l_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫថ"): True}).encode(bstack1l1111l_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧទ")))
            if response is not None and response.capabilities:
                bstack11111l1l1l_opy_ = json.loads(response.capabilities.decode(bstack1l1111l_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨធ")))
                if not bstack11111l1l1l_opy_:
                    return
                if bstack11111l1l1l_opy_.get(bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧន")) and not self.bstack11l1lll11ll_opy_(bstack11111l1l1l_opy_):
                    bstack11111l1l1l_opy_[bstack1l1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨប")] = False
                    bstack11l1ll1llll_opy_ = [bstack11l1lll1ll1_opy_ for bstack11l1lll1ll1_opy_ in bstack11111l1l1l_opy_ if bstack11l1lll1ll1_opy_.startswith(bstack1l1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩផ"))]
                    for bstack11l1lll1ll1_opy_ in bstack11l1ll1llll_opy_:
                        del bstack11111l1l1l_opy_[bstack11l1lll1ll1_opy_]
                bstack11l1ll1l1l1_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack11111l1l1l_opy_))
                if bstack11111l1l1l_opy_.get(bstack1l1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪព")):
                    browser = bstack11l1ll1ll11_opy_.connect_over_cdp(bstack11l1ll1l1l1_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack11l1ll1l1l1_opy_
                    return connect(bstack11l1ll1ll11_opy_, *args, **kwargs)
        return wrapped
    def bstack11l1ll1l1ll_opy_(
        self,
        f: bstack111l1l11l_opy_,
        bstack11lll1ll1ll_opy_: object,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1111l_opy_ (u"ࠧࡴࡥࡸࡡࡳࡥ࡬࡫ࠢភ"):
            return
        if not bstack1lllllll11l_opy_():
            self.logger.debug(bstack1l1111l_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡴࡥࡸࡡࡳࡥ࡬࡫ࠠ࡮ࡧࡷ࡬ࡴࡪࠬࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧម"))
            return
        def wrapped(bstack11lll1ll1ll_opy_, bstack11l1lll1lll_opy_, *args, **kwargs):
            contexts = bstack11lll1ll1ll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l1111l_opy_ (u"ࠢࡢࡤࡲࡹࡹࡀࡢ࡭ࡣࡱ࡯ࠧយ") in page.url:
                                return page
                            else:
                                return bstack11l1lll1lll_opy_(bstack11lll1ll1ll_opy_)
                    else:
                        return bstack11l1lll1lll_opy_(bstack11lll1ll1ll_opy_)
        return wrapped
    def bstack11l1ll1lll1_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.client_worker_id = bstack1l1111l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢរ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸ࠿ࠦࠢល") + str(req) + bstack1l1111l_opy_ (u"ࠥࠦវ"))
        try:
            r = self.bstack11l1ll1lll_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࡹࡵࡤࡥࡨࡷࡸࡃࠢឝ") + str(r.success) + bstack1l1111l_opy_ (u"ࠧࠨឞ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1111l_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦស") + str(e) + bstack1l1111l_opy_ (u"ࠢࠣហ"))
            traceback.print_exc()
            raise e
    def bstack11l1lll1l11_opy_(
        self,
        f: bstack111l1l11l_opy_,
        Connection: object,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1111l_opy_ (u"ࠣࡡࡶࡩࡳࡪ࡟࡮ࡧࡶࡷࡦ࡭ࡥࡠࡶࡲࡣࡸ࡫ࡲࡷࡧࡵࠦឡ"):
            return
        if not bstack1lllllll11l_opy_():
            return
        def wrapped(Connection, bstack11l1llll111_opy_, *args, **kwargs):
            return bstack11l1llll111_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack111l1l11l_opy_,
        bstack11l1ll1ll11_opy_: object,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1111l_opy_ (u"ࠤࡦࡰࡴࡹࡥࠣអ"):
            return
        if not bstack1lllllll11l_opy_():
            self.logger.debug(bstack1l1111l_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡦࡰࡴࡹࡥࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨឣ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped