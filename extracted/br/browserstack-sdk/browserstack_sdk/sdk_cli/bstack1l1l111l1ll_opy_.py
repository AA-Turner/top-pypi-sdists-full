# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1l11lll1l1l_opy_ import bstack1l11ll1l111_opy_
from browserstack_sdk.sdk_cli.bstack11111ll111_opy_ import (
    bstack1111ll1l11_opy_,
    bstack1llll11lll_opy_,
    bstack1l1ll11ll11_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack111lll11ll_opy_ import bstack11ll1l111l_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11ll11l111_opy_
from bstack_utils.helper import bstack1lll1ll1ll_opy_
import threading
import os
import urllib.parse
class bstack1l11l11lll1_opy_(bstack1l11ll1l111_opy_):
    @staticmethod
    def bstack11l1lll11l1_opy_(bstack1111l111ll_opy_: dict) -> bool:
        browser_name = (
            bstack1111l111ll_opy_.get(bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᝢ"))
            or bstack1111l111ll_opy_.get(bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪᝣ"))
            or bstack1111l111ll_opy_.get(bstack1ll_opy_ (u"ࠪࡨࡪ࡬ࡡࡶ࡮ࡷࡆࡷࡵࡷࡴࡧࡵࡘࡾࡶࡥࠨᝤ"))
            or bstack1ll_opy_ (u"ࠫࠬᝥ")
        ).lower()
        return browser_name in bstack1l1lll11l1_opy_
    def __init__(self, bstack1l1l1ll11ll_opy_):
        super().__init__()
        bstack11ll1l111l_opy_.bstack1l1111111l1_opy_((bstack1111ll1l11_opy_.bstack1l1l1l11l_opy_, bstack1llll11lll_opy_.PRE), self.bstack11l1llll11l_opy_)
        bstack11ll1l111l_opy_.bstack1l1111111l1_opy_((bstack1111ll1l11_opy_.bstack1l1l1l11l_opy_, bstack1llll11lll_opy_.PRE), self.bstack11l1llll1ll_opy_)
        bstack11ll1l111l_opy_.bstack1l1111111l1_opy_((bstack1111ll1l11_opy_.bstack1l1ll1l1111_opy_, bstack1llll11lll_opy_.PRE), self.bstack11l1lll1111_opy_)
        bstack11ll1l111l_opy_.bstack1l1111111l1_opy_((bstack1111ll1l11_opy_.bstack1ll11111ll1_opy_, bstack1llll11lll_opy_.PRE), self.bstack11l1llll111_opy_)
        bstack11ll1l111l_opy_.bstack1l1111111l1_opy_((bstack1111ll1l11_opy_.bstack1l1l1l11l_opy_, bstack1llll11lll_opy_.PRE), self.bstack11l1lll1ll1_opy_)
        bstack11ll1l111l_opy_.bstack1l1111111l1_opy_((bstack1111ll1l11_opy_.QUIT, bstack1llll11lll_opy_.PRE), self.on_close)
        self.bstack1l1l1ll11ll_opy_ = bstack1l1l1ll11ll_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack11l1llll11l_opy_(
        self,
        f: bstack11ll1l111l_opy_,
        bstack11l1ll1ll1l_opy_: object,
        exec: Tuple[bstack1l1ll11ll11_opy_, str],
        bstack1l1ll1lll11_opy_: Tuple[bstack1111ll1l11_opy_, bstack1llll11lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll_opy_ (u"ࠧࡲࡡࡶࡰࡦ࡬ࠧᝦ"):
            return
        if not bstack1lll1ll1ll_opy_():
            self.logger.debug(bstack1ll_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡲࡡࡶࡰࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥᝧ"))
            return
        def wrapped(bstack11l1ll1ll1l_opy_, launch, *args, **kwargs):
            response = self.bstack11l1ll1llll_opy_(f.platform_index, instance.ref(), json.dumps({bstack1ll_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᝨ"): True}).encode(bstack1ll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᝩ")))
            if response is not None and response.capabilities:
                if not bstack1lll1ll1ll_opy_():
                    browser = launch(bstack11l1ll1ll1l_opy_)
                    return browser
                bstack1111l111ll_opy_ = json.loads(response.capabilities.decode(bstack1ll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᝪ")))
                if not bstack1111l111ll_opy_: # empty caps bstack11l1lllll11_opy_ bstack11l1lll1lll_opy_ bstack11l1ll1lll1_opy_ bstack11l1lll11ll_opy_ or error in processing
                    return
                bstack11l1llllll1_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1111l111ll_opy_))
                f.bstack1l1l1l1l_opy_(instance, bstack11ll1l111l_opy_.bstack11llll1l11_opy_, bstack11l1llllll1_opy_)
                f.bstack1l1l1l1l_opy_(instance, bstack11ll1l111l_opy_.bstack11l1111l1l_opy_, bstack1111l111ll_opy_)
                browser = bstack11l1ll1ll1l_opy_.connect(bstack11l1llllll1_opy_)
                return browser
        return wrapped
    def bstack11l1lll1111_opy_(
        self,
        f: bstack11ll1l111l_opy_,
        Connection: object,
        exec: Tuple[bstack1l1ll11ll11_opy_, str],
        bstack1l1ll1lll11_opy_: Tuple[bstack1111ll1l11_opy_, bstack1llll11lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll_opy_ (u"ࠥࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠧᝫ"):
            self.logger.debug(bstack1ll_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥᝬ"))
            return
        if not bstack1lll1ll1ll_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1ll_opy_ (u"ࠬࡶࡡࡳࡣࡰࡷࠬ᝭"), {}).get(bstack1ll_opy_ (u"࠭ࡢࡴࡒࡤࡶࡦࡳࡳࠨᝮ")):
                    bstack11l1llll1l1_opy_ = args[0][bstack1ll_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢᝯ")][bstack1ll_opy_ (u"ࠣࡤࡶࡔࡦࡸࡡ࡮ࡵࠥᝰ")]
                    session_id = bstack11l1llll1l1_opy_.get(bstack1ll_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡌࡨࠧ᝱"))
                    f.bstack1l1l1l1l_opy_(instance, bstack11ll1l111l_opy_.bstack1l1lllll11l_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࠨᝲ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack11l1lll1ll1_opy_(
        self,
        f: bstack11ll1l111l_opy_,
        bstack11l1ll1ll1l_opy_: object,
        exec: Tuple[bstack1l1ll11ll11_opy_, str],
        bstack1l1ll1lll11_opy_: Tuple[bstack1111ll1l11_opy_, bstack1llll11lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࠧᝳ"):
            return
        if not bstack1lll1ll1ll_opy_():
            self.logger.debug(bstack1ll_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡨࡵ࡮࡯ࡧࡦࡸࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥ᝴"))
            return
        def wrapped(bstack11l1ll1ll1l_opy_, connect, *args, **kwargs):
            response = self.bstack11l1ll1llll_opy_(f.platform_index, instance.ref(), json.dumps({bstack1ll_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬ᝵"): True}).encode(bstack1ll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨ᝶")))
            if response is not None and response.capabilities:
                bstack1111l111ll_opy_ = json.loads(response.capabilities.decode(bstack1ll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢ᝷")))
                if not bstack1111l111ll_opy_:
                    return
                if bstack1111l111ll_opy_.get(bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᝸")) and not self.bstack11l1lll11l1_opy_(bstack1111l111ll_opy_):
                    bstack1111l111ll_opy_[bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᝹")] = False
                    bstack11l1lll111l_opy_ = [bstack11l1lllll1l_opy_ for bstack11l1lllll1l_opy_ in bstack1111l111ll_opy_ if bstack11l1lllll1l_opy_.startswith(bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᝺"))]
                    for bstack11l1lllll1l_opy_ in bstack11l1lll111l_opy_:
                        del bstack1111l111ll_opy_[bstack11l1lllll1l_opy_]
                bstack11l1llllll1_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1111l111ll_opy_))
                if bstack1111l111ll_opy_.get(bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᝻")):
                    browser = bstack11l1ll1ll1l_opy_.connect_over_cdp(bstack11l1llllll1_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack11l1llllll1_opy_
                    return connect(bstack11l1ll1ll1l_opy_, *args, **kwargs)
        return wrapped
    def bstack11l1llll1ll_opy_(
        self,
        f: bstack11ll1l111l_opy_,
        bstack11lll1ll1l1_opy_: object,
        exec: Tuple[bstack1l1ll11ll11_opy_, str],
        bstack1l1ll1lll11_opy_: Tuple[bstack1111ll1l11_opy_, bstack1llll11lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll_opy_ (u"ࠨ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠣ᝼"):
            return
        if not bstack1lll1ll1ll_opy_():
            self.logger.debug(bstack1ll_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨ᝽"))
            return
        def wrapped(bstack11lll1ll1l1_opy_, bstack11l1lll1l11_opy_, *args, **kwargs):
            contexts = bstack11lll1ll1l1_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1ll_opy_ (u"ࠣࡣࡥࡳࡺࡺ࠺ࡣ࡮ࡤࡲࡰࠨ᝾") in page.url:
                                return page
                            else:
                                return bstack11l1lll1l11_opy_(bstack11lll1ll1l1_opy_)
                    else:
                        return bstack11l1lll1l11_opy_(bstack11lll1ll1l1_opy_)
        return wrapped
    def bstack11l1ll1llll_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.client_worker_id = bstack1ll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣ᝿").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1ll_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣក") + str(req) + bstack1ll_opy_ (u"ࠦࠧខ"))
        try:
            r = self.bstack1ll11ll11l_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1ll_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣគ") + str(r.success) + bstack1ll_opy_ (u"ࠨࠢឃ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧង") + str(e) + bstack1ll_opy_ (u"ࠣࠤច"))
            traceback.print_exc()
            raise e
    def bstack11l1llll111_opy_(
        self,
        f: bstack11ll1l111l_opy_,
        Connection: object,
        exec: Tuple[bstack1l1ll11ll11_opy_, str],
        bstack1l1ll1lll11_opy_: Tuple[bstack1111ll1l11_opy_, bstack1llll11lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll_opy_ (u"ࠤࡢࡷࡪࡴࡤࡠ࡯ࡨࡷࡸࡧࡧࡦࡡࡷࡳࡤࡹࡥࡳࡸࡨࡶࠧឆ"):
            return
        if not bstack1lll1ll1ll_opy_():
            return
        def wrapped(Connection, bstack11l1lll1l1l_opy_, *args, **kwargs):
            return bstack11l1lll1l1l_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack11ll1l111l_opy_,
        bstack11l1ll1ll1l_opy_: object,
        exec: Tuple[bstack1l1ll11ll11_opy_, str],
        bstack1l1ll1lll11_opy_: Tuple[bstack1111ll1l11_opy_, bstack1llll11lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll_opy_ (u"ࠥࡧࡱࡵࡳࡦࠤជ"):
            return
        if not bstack1lll1ll1ll_opy_():
            self.logger.debug(bstack1ll_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡧࡱࡵࡳࡦࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢឈ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped