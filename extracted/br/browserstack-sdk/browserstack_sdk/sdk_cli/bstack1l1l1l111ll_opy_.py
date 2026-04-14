# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1l1l1111ll1_opy_ import bstack1l11ll1l11l_opy_
from browserstack_sdk.sdk_cli.bstack1111ll1ll1_opy_ import (
    bstack1l1l11ll1l_opy_,
    bstack1ll1llll1l_opy_,
    bstack1l1ll1lllll_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack111l1ll11l_opy_ import bstack11ll1llll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1lll1lll_opy_
from bstack_utils.helper import bstack11ll1l1l1l_opy_
import threading
import os
import urllib.parse
class bstack1l11l11l11l_opy_(bstack1l11ll1l11l_opy_):
    @staticmethod
    def bstack11l1lll11ll_opy_(bstack11l111111_opy_: dict) -> bool:
        browser_name = (
            bstack11l111111_opy_.get(bstack1l111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ᝻"))
            or bstack11l111111_opy_.get(bstack1l111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ᝼"))
            or bstack11l111111_opy_.get(bstack1l111l_opy_ (u"ࠧࡥࡧࡩࡥࡺࡲࡴࡃࡴࡲࡻࡸ࡫ࡲࡕࡻࡳࡩࠬ᝽"))
            or bstack1l111l_opy_ (u"ࠨࠩ᝾")
        ).lower()
        return browser_name in bstack1ll1111l1_opy_
    def __init__(self, bstack1l11l1lllll_opy_):
        super().__init__()
        bstack11ll1llll_opy_.bstack1l11111ll11_opy_((bstack1l1l11ll1l_opy_.bstack1ll1ll1lll_opy_, bstack1ll1llll1l_opy_.PRE), self.bstack11l1lll1ll1_opy_)
        bstack11ll1llll_opy_.bstack1l11111ll11_opy_((bstack1l1l11ll1l_opy_.bstack1ll1ll1lll_opy_, bstack1ll1llll1l_opy_.PRE), self.bstack11l1lll1lll_opy_)
        bstack11ll1llll_opy_.bstack1l11111ll11_opy_((bstack1l1l11ll1l_opy_.bstack1l1ll1l1l11_opy_, bstack1ll1llll1l_opy_.PRE), self.bstack11l1llll1l1_opy_)
        bstack11ll1llll_opy_.bstack1l11111ll11_opy_((bstack1l1l11ll1l_opy_.bstack1l1llllllll_opy_, bstack1ll1llll1l_opy_.PRE), self.bstack11l1ll1lll1_opy_)
        bstack11ll1llll_opy_.bstack1l11111ll11_opy_((bstack1l1l11ll1l_opy_.bstack1ll1ll1lll_opy_, bstack1ll1llll1l_opy_.PRE), self.bstack11l1lll1l11_opy_)
        bstack11ll1llll_opy_.bstack1l11111ll11_opy_((bstack1l1l11ll1l_opy_.QUIT, bstack1ll1llll1l_opy_.PRE), self.on_close)
        self.bstack1l11l1lllll_opy_ = bstack1l11l1lllll_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack11l1lll1ll1_opy_(
        self,
        f: bstack11ll1llll_opy_,
        bstack11l1ll1llll_opy_: object,
        exec: Tuple[bstack1l1ll1lllll_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l111l_opy_ (u"ࠤ࡯ࡥࡺࡴࡣࡩࠤ᝿"):
            return
        if not bstack11ll1l1l1l_opy_():
            self.logger.debug(bstack1l111l_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢ࡯ࡥࡺࡴࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢក"))
            return
        def wrapped(bstack11l1ll1llll_opy_, launch, *args, **kwargs):
            response = self.bstack11l1lll111l_opy_(f.platform_index, instance.ref(), json.dumps({bstack1l111l_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪខ"): True}).encode(bstack1l111l_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦគ")))
            if response is not None and response.capabilities:
                if not bstack11ll1l1l1l_opy_():
                    browser = launch(bstack11l1ll1llll_opy_)
                    return browser
                bstack11l111111_opy_ = json.loads(response.capabilities.decode(bstack1l111l_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧឃ")))
                if not bstack11l111111_opy_: # empty caps bstack11l1ll1l1ll_opy_ bstack11l1lll11l1_opy_ bstack11l1llll1ll_opy_ bstack11l1ll1ll11_opy_ or error in processing
                    return
                bstack11l1lllll11_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack11l111111_opy_))
                f.bstack11111ll11l_opy_(instance, bstack11ll1llll_opy_.bstack11llll1l11_opy_, bstack11l1lllll11_opy_)
                f.bstack11111ll11l_opy_(instance, bstack11ll1llll_opy_.bstack11lll111l_opy_, bstack11l111111_opy_)
                browser = bstack11l1ll1llll_opy_.connect(bstack11l1lllll11_opy_)
                return browser
        return wrapped
    def bstack11l1llll1l1_opy_(
        self,
        f: bstack11ll1llll_opy_,
        Connection: object,
        exec: Tuple[bstack1l1ll1lllll_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l111l_opy_ (u"ࠢࡥ࡫ࡶࡴࡦࡺࡣࡩࠤង"):
            self.logger.debug(bstack1l111l_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡥ࡫ࡶࡴࡦࡺࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢច"))
            return
        if not bstack11ll1l1l1l_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1l111l_opy_ (u"ࠩࡳࡥࡷࡧ࡭ࡴࠩឆ"), {}).get(bstack1l111l_opy_ (u"ࠪࡦࡸࡖࡡࡳࡣࡰࡷࠬជ")):
                    bstack11l1llll11l_opy_ = args[0][bstack1l111l_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦឈ")][bstack1l111l_opy_ (u"ࠧࡨࡳࡑࡣࡵࡥࡲࡹࠢញ")]
                    session_id = bstack11l1llll11l_opy_.get(bstack1l111l_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴࡉࡥࠤដ"))
                    f.bstack11111ll11l_opy_(instance, bstack11ll1llll_opy_.bstack1ll1111lll1_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1l111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡤࡪࡵࡳࡥࡹࡩࡨࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠢࠥឋ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack11l1lll1l11_opy_(
        self,
        f: bstack11ll1llll_opy_,
        bstack11l1ll1llll_opy_: object,
        exec: Tuple[bstack1l1ll1lllll_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l111l_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࠤឌ"):
            return
        if not bstack11ll1l1l1l_opy_():
            self.logger.debug(bstack1l111l_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡥࡲࡲࡳ࡫ࡣࡵࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢឍ"))
            return
        def wrapped(bstack11l1ll1llll_opy_, connect, *args, **kwargs):
            response = self.bstack11l1lll111l_opy_(f.platform_index, instance.ref(), json.dumps({bstack1l111l_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩណ"): True}).encode(bstack1l111l_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥត")))
            if response is not None and response.capabilities:
                bstack11l111111_opy_ = json.loads(response.capabilities.decode(bstack1l111l_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦថ")))
                if not bstack11l111111_opy_:
                    return
                if bstack11l111111_opy_.get(bstack1l111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬទ")) and not self.bstack11l1lll11ll_opy_(bstack11l111111_opy_):
                    bstack11l111111_opy_[bstack1l111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ធ")] = False
                    bstack11l1ll1ll1l_opy_ = [bstack11l1lll1l1l_opy_ for bstack11l1lll1l1l_opy_ in bstack11l111111_opy_ if bstack11l1lll1l1l_opy_.startswith(bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧន"))]
                    for bstack11l1lll1l1l_opy_ in bstack11l1ll1ll1l_opy_:
                        del bstack11l111111_opy_[bstack11l1lll1l1l_opy_]
                bstack11l1lllll11_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack11l111111_opy_))
                if bstack11l111111_opy_.get(bstack1l111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨប")):
                    browser = bstack11l1ll1llll_opy_.connect_over_cdp(bstack11l1lllll11_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack11l1lllll11_opy_
                    return connect(bstack11l1ll1llll_opy_, *args, **kwargs)
        return wrapped
    def bstack11l1lll1lll_opy_(
        self,
        f: bstack11ll1llll_opy_,
        bstack11lll1ll11l_opy_: object,
        exec: Tuple[bstack1l1ll1lllll_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l111l_opy_ (u"ࠥࡲࡪࡽ࡟ࡱࡣࡪࡩࠧផ"):
            return
        if not bstack11ll1l1l1l_opy_():
            self.logger.debug(bstack1l111l_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡲࡪࡽ࡟ࡱࡣࡪࡩࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥព"))
            return
        def wrapped(bstack11lll1ll11l_opy_, bstack11l1lll1111_opy_, *args, **kwargs):
            contexts = bstack11lll1ll11l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l111l_opy_ (u"ࠧࡧࡢࡰࡷࡷ࠾ࡧࡲࡡ࡯࡭ࠥភ") in page.url:
                                return page
                            else:
                                return bstack11l1lll1111_opy_(bstack11lll1ll11l_opy_)
                    else:
                        return bstack11l1lll1111_opy_(bstack11lll1ll11l_opy_)
        return wrapped
    def bstack11l1lll111l_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.client_worker_id = bstack1l111l_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧម").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1l111l_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡺࡩࡧࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧយ") + str(req) + bstack1l111l_opy_ (u"ࠣࠤរ"))
        try:
            r = self.bstack1l1l1111l1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l111l_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧល") + str(r.success) + bstack1l111l_opy_ (u"ࠥࠦវ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l111l_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤឝ") + str(e) + bstack1l111l_opy_ (u"ࠧࠨឞ"))
            traceback.print_exc()
            raise e
    def bstack11l1ll1lll1_opy_(
        self,
        f: bstack11ll1llll_opy_,
        Connection: object,
        exec: Tuple[bstack1l1ll1lllll_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l111l_opy_ (u"ࠨ࡟ࡴࡧࡱࡨࡤࡳࡥࡴࡵࡤ࡫ࡪࡥࡴࡰࡡࡶࡩࡷࡼࡥࡳࠤស"):
            return
        if not bstack11ll1l1l1l_opy_():
            return
        def wrapped(Connection, bstack11l1llll111_opy_, *args, **kwargs):
            return bstack11l1llll111_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack11ll1llll_opy_,
        bstack11l1ll1llll_opy_: object,
        exec: Tuple[bstack1l1ll1lllll_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l111l_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨហ"):
            return
        if not bstack11ll1l1l1l_opy_():
            self.logger.debug(bstack1l111l_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡤ࡮ࡲࡷࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦឡ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped