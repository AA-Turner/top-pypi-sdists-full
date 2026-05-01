# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1l1l111l111_opy_ import bstack1l11l1l11ll_opy_
from browserstack_sdk.sdk_cli.bstack11l111l1l_opy_ import (
    bstack1ll1l1111l_opy_,
    bstack1l1l111lll_opy_,
    bstack1l1ll111lll_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack111l11ll_opy_ import bstack11ll1l1ll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack111l111lll_opy_
from bstack_utils.helper import bstack1l1l1l11_opy_
import threading
import os
import urllib.parse
class bstack1l11lll11ll_opy_(bstack1l11l1l11ll_opy_):
    @staticmethod
    def bstack11l1ll11lll_opy_(bstack1l11ll1l1_opy_: dict) -> bool:
        browser_name = (
            bstack1l11ll1l1_opy_.get(bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ឌ"))
            or bstack1l11ll1l1_opy_.get(bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪឍ"))
            or bstack1l11ll1l1_opy_.get(bstack111ll_opy_ (u"ࠪࡨࡪ࡬ࡡࡶ࡮ࡷࡆࡷࡵࡷࡴࡧࡵࡘࡾࡶࡥࠨណ"))
            or bstack111ll_opy_ (u"ࠫࠬត")
        ).lower()
        return browser_name in bstack1l1l111111_opy_
    def __init__(self, bstack1l11l1l1l1l_opy_):
        super().__init__()
        bstack11ll1l1ll_opy_.bstack1l111l1111l_opy_((bstack1ll1l1111l_opy_.bstack111l1ll111_opy_, bstack1l1l111lll_opy_.PRE), self.bstack11l1ll1l111_opy_)
        bstack11ll1l1ll_opy_.bstack1l111l1111l_opy_((bstack1ll1l1111l_opy_.bstack111l1ll111_opy_, bstack1l1l111lll_opy_.PRE), self.bstack11l1ll1ll1l_opy_)
        bstack11ll1l1ll_opy_.bstack1l111l1111l_opy_((bstack1ll1l1111l_opy_.bstack1l1ll1lll11_opy_, bstack1l1l111lll_opy_.PRE), self.bstack11l1ll11ll1_opy_)
        bstack11ll1l1ll_opy_.bstack1l111l1111l_opy_((bstack1ll1l1111l_opy_.bstack1ll1111l111_opy_, bstack1l1l111lll_opy_.PRE), self.bstack11l1lll111l_opy_)
        bstack11ll1l1ll_opy_.bstack1l111l1111l_opy_((bstack1ll1l1111l_opy_.bstack111l1ll111_opy_, bstack1l1l111lll_opy_.PRE), self.bstack11l1ll1ll11_opy_)
        bstack11ll1l1ll_opy_.bstack1l111l1111l_opy_((bstack1ll1l1111l_opy_.QUIT, bstack1l1l111lll_opy_.PRE), self.on_close)
        self.bstack1l11l1l1l1l_opy_ = bstack1l11l1l1l1l_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack11l1ll1l111_opy_(
        self,
        f: bstack11ll1l1ll_opy_,
        bstack11l1lll1l1l_opy_: object,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111ll_opy_ (u"ࠧࡲࡡࡶࡰࡦ࡬ࠧថ"):
            return
        if not bstack1l1l1l11_opy_():
            self.logger.debug(bstack111ll_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡲࡡࡶࡰࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥទ"))
            return
        def wrapped(bstack11l1lll1l1l_opy_, launch, *args, **kwargs):
            response = self.bstack11l1lll11l1_opy_(f.platform_index, instance.ref(), json.dumps({bstack111ll_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ធ"): True}).encode(bstack111ll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢន")))
            if response is not None and response.capabilities:
                if not bstack1l1l1l11_opy_():
                    browser = launch(bstack11l1lll1l1l_opy_)
                    return browser
                bstack1l11ll1l1_opy_ = json.loads(response.capabilities.decode(bstack111ll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣប")))
                if not bstack1l11ll1l1_opy_: # empty caps bstack11l1lll1lll_opy_ bstack11l1lll11ll_opy_ bstack11l1ll1l11l_opy_ bstack11l1ll1llll_opy_ or error in processing
                    return
                bstack11l1lll1ll1_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l11ll1l1_opy_))
                f.bstack11ll11l1_opy_(instance, bstack11ll1l1ll_opy_.bstack1ll1llll1_opy_, bstack11l1lll1ll1_opy_)
                f.bstack11ll11l1_opy_(instance, bstack11ll1l1ll_opy_.bstack1ll111ll_opy_, bstack1l11ll1l1_opy_)
                browser = bstack11l1lll1l1l_opy_.connect(bstack11l1lll1ll1_opy_)
                return browser
        return wrapped
    def bstack11l1ll11ll1_opy_(
        self,
        f: bstack11ll1l1ll_opy_,
        Connection: object,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111ll_opy_ (u"ࠥࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠧផ"):
            self.logger.debug(bstack111ll_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥព"))
            return
        if not bstack1l1l1l11_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack111ll_opy_ (u"ࠬࡶࡡࡳࡣࡰࡷࠬភ"), {}).get(bstack111ll_opy_ (u"࠭ࡢࡴࡒࡤࡶࡦࡳࡳࠨម")):
                    bstack11l1lll1111_opy_ = args[0][bstack111ll_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢយ")][bstack111ll_opy_ (u"ࠣࡤࡶࡔࡦࡸࡡ࡮ࡵࠥរ")]
                    session_id = bstack11l1lll1111_opy_.get(bstack111ll_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡌࡨࠧល"))
                    f.bstack11ll11l1_opy_(instance, bstack11ll1l1ll_opy_.bstack1ll1111ll11_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack111ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࠨវ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack11l1ll1ll11_opy_(
        self,
        f: bstack11ll1l1ll_opy_,
        bstack11l1lll1l1l_opy_: object,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111ll_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࠧឝ"):
            return
        if not bstack1l1l1l11_opy_():
            self.logger.debug(bstack111ll_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡨࡵ࡮࡯ࡧࡦࡸࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥឞ"))
            return
        def wrapped(bstack11l1lll1l1l_opy_, connect, *args, **kwargs):
            response = self.bstack11l1lll11l1_opy_(f.platform_index, instance.ref(), json.dumps({bstack111ll_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬស"): True}).encode(bstack111ll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨហ")))
            if response is not None and response.capabilities:
                bstack1l11ll1l1_opy_ = json.loads(response.capabilities.decode(bstack111ll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢឡ")))
                if not bstack1l11ll1l1_opy_:
                    return
                if bstack1l11ll1l1_opy_.get(bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨអ")) and not self.bstack11l1ll11lll_opy_(bstack1l11ll1l1_opy_):
                    bstack1l11ll1l1_opy_[bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩឣ")] = False
                    bstack11l1ll1lll1_opy_ = [bstack11l1ll1l1l1_opy_ for bstack11l1ll1l1l1_opy_ in bstack1l11ll1l1_opy_ if bstack11l1ll1l1l1_opy_.startswith(bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪឤ"))]
                    for bstack11l1ll1l1l1_opy_ in bstack11l1ll1lll1_opy_:
                        del bstack1l11ll1l1_opy_[bstack11l1ll1l1l1_opy_]
                bstack11l1lll1ll1_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l11ll1l1_opy_))
                if bstack1l11ll1l1_opy_.get(bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫឥ")):
                    browser = bstack11l1lll1l1l_opy_.connect_over_cdp(bstack11l1lll1ll1_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack11l1lll1ll1_opy_
                    return connect(bstack11l1lll1l1l_opy_, *args, **kwargs)
        return wrapped
    def bstack11l1ll1ll1l_opy_(
        self,
        f: bstack11ll1l1ll_opy_,
        bstack11lll1lll11_opy_: object,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111ll_opy_ (u"ࠨ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠣឦ"):
            return
        if not bstack1l1l1l11_opy_():
            self.logger.debug(bstack111ll_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨឧ"))
            return
        def wrapped(bstack11lll1lll11_opy_, bstack11l1lll1l11_opy_, *args, **kwargs):
            contexts = bstack11lll1lll11_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack111ll_opy_ (u"ࠣࡣࡥࡳࡺࡺ࠺ࡣ࡮ࡤࡲࡰࠨឨ") in page.url:
                                return page
                            else:
                                return bstack11l1lll1l11_opy_(bstack11lll1lll11_opy_)
                    else:
                        return bstack11l1lll1l11_opy_(bstack11lll1lll11_opy_)
        return wrapped
    def bstack11l1lll11l1_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.client_worker_id = bstack111ll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣឩ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack111ll_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣឪ") + str(req) + bstack111ll_opy_ (u"ࠦࠧឫ"))
        try:
            r = self.bstack111111ll1l_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack111ll_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣឬ") + str(r.success) + bstack111ll_opy_ (u"ࠨࠢឭ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111ll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧឮ") + str(e) + bstack111ll_opy_ (u"ࠣࠤឯ"))
            traceback.print_exc()
            raise e
    def bstack11l1lll111l_opy_(
        self,
        f: bstack11ll1l1ll_opy_,
        Connection: object,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111ll_opy_ (u"ࠤࡢࡷࡪࡴࡤࡠ࡯ࡨࡷࡸࡧࡧࡦࡡࡷࡳࡤࡹࡥࡳࡸࡨࡶࠧឰ"):
            return
        if not bstack1l1l1l11_opy_():
            return
        def wrapped(Connection, bstack11l1ll1l1ll_opy_, *args, **kwargs):
            return bstack11l1ll1l1ll_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack11ll1l1ll_opy_,
        bstack11l1lll1l1l_opy_: object,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111ll_opy_ (u"ࠥࡧࡱࡵࡳࡦࠤឱ"):
            return
        if not bstack1l1l1l11_opy_():
            self.logger.debug(bstack111ll_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡧࡱࡵࡳࡦࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢឲ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped