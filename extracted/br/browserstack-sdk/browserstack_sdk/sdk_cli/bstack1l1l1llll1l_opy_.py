# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1l1ll11l111_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.sdk_cli.bstack111l11ll11_opy_ import (
    bstack11lll111_opy_,
    bstack1l11l11l1_opy_,
    bstack1ll11ll1l11_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1l1ll1111l_opy_ import bstack111l111ll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1ll111ll11_opy_
from bstack_utils.helper import bstack11lll11l1_opy_
import threading
import os
import urllib.parse
class bstack1ll111l1ll1_opy_(bstack1ll111l11ll_opy_):
    @staticmethod
    def bstack11lll11ll1l_opy_(bstack1ll111ll1l_opy_: dict) -> bool:
        browser_name = (
            bstack1ll111ll1l_opy_.get(bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᘛ"))
            or bstack1ll111ll1l_opy_.get(bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬᘜ"))
            or bstack1ll111ll1l_opy_.get(bstack1ll1lll_opy_ (u"ࠬࡪࡥࡧࡣࡸࡰࡹࡈࡲࡰࡹࡶࡩࡷ࡚ࡹࡱࡧࠪᘝ"))
            or bstack1ll1lll_opy_ (u"࠭ࠧᘞ")
        ).lower()
        return browser_name in bstack1l1l11l1ll_opy_
    def __init__(self, bstack1l1lll111ll_opy_):
        super().__init__()
        bstack111l111ll_opy_.bstack1l11ll11111_opy_((bstack11lll111_opy_.bstack1l111ll1l1_opy_, bstack1l11l11l1_opy_.PRE), self.bstack11lll1l11l1_opy_)
        bstack111l111ll_opy_.bstack1l11ll11111_opy_((bstack11lll111_opy_.bstack1l111ll1l1_opy_, bstack1l11l11l1_opy_.PRE), self.bstack11lll1l1l1l_opy_)
        bstack111l111ll_opy_.bstack1l11ll11111_opy_((bstack11lll111_opy_.bstack1ll11l11ll1_opy_, bstack1l11l11l1_opy_.PRE), self.bstack11lll11lll1_opy_)
        bstack111l111ll_opy_.bstack1l11ll11111_opy_((bstack11lll111_opy_.bstack1ll1l1lllll_opy_, bstack1l11l11l1_opy_.PRE), self.bstack11lll1l1lll_opy_)
        bstack111l111ll_opy_.bstack1l11ll11111_opy_((bstack11lll111_opy_.bstack1l111ll1l1_opy_, bstack1l11l11l1_opy_.PRE), self.bstack11lll1llll1_opy_)
        bstack111l111ll_opy_.bstack1l11ll11111_opy_((bstack11lll111_opy_.QUIT, bstack1l11l11l1_opy_.PRE), self.on_close)
        self.bstack1l1lll111ll_opy_ = bstack1l1lll111ll_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack11lll1l11l1_opy_(
        self,
        f: bstack111l111ll_opy_,
        bstack11lll1ll1l1_opy_: object,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1lll_opy_ (u"ࠢ࡭ࡣࡸࡲࡨ࡮ࠢᘟ"):
            return
        if not bstack11lll11l1_opy_():
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠ࡭ࡣࡸࡲࡨ࡮ࠠ࡮ࡧࡷ࡬ࡴࡪࠬࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧᘠ"))
            return
        def wrapped(bstack11lll1ll1l1_opy_, launch, *args, **kwargs):
            response = self.bstack11lll11llll_opy_(f.platform_index, instance.ref(), json.dumps({bstack1ll1lll_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᘡ"): True}).encode(bstack1ll1lll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᘢ")))
            if response is not None and response.capabilities:
                if not bstack11lll11l1_opy_():
                    browser = launch(bstack11lll1ll1l1_opy_)
                    return browser
                bstack1ll111ll1l_opy_ = json.loads(response.capabilities.decode(bstack1ll1lll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᘣ")))
                if not bstack1ll111ll1l_opy_: # empty caps bstack11lll1ll111_opy_ bstack11lll1l1111_opy_ bstack11lll1ll11l_opy_ bstack11lll1lll11_opy_ or error in processing
                    return
                bstack11lll1lll1l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1ll111ll1l_opy_))
                f.bstack1lll1111ll_opy_(instance, bstack111l111ll_opy_.bstack1lll111l_opy_, bstack11lll1lll1l_opy_)
                f.bstack1lll1111ll_opy_(instance, bstack111l111ll_opy_.bstack11l11l11_opy_, bstack1ll111ll1l_opy_)
                browser = bstack11lll1ll1l1_opy_.connect(bstack11lll1lll1l_opy_)
                return browser
        return wrapped
    def bstack11lll11lll1_opy_(
        self,
        f: bstack111l111ll_opy_,
        Connection: object,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1lll_opy_ (u"ࠧࡪࡩࡴࡲࡤࡸࡨ࡮ࠢᘤ"):
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡪࡩࡴࡲࡤࡸࡨ࡮ࠠ࡮ࡧࡷ࡬ࡴࡪࠬࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧᘥ"))
            return
        if not bstack11lll11l1_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1ll1lll_opy_ (u"ࠧࡱࡣࡵࡥࡲࡹࠧᘦ"), {}).get(bstack1ll1lll_opy_ (u"ࠨࡤࡶࡔࡦࡸࡡ࡮ࡵࠪᘧ")):
                    bstack11lll1l1l11_opy_ = args[0][bstack1ll1lll_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤᘨ")][bstack1ll1lll_opy_ (u"ࠥࡦࡸࡖࡡࡳࡣࡰࡷࠧᘩ")]
                    session_id = bstack11lll1l1l11_opy_.get(bstack1ll1lll_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡎࡪࠢᘪ"))
                    f.bstack1lll1111ll_opy_(instance, bstack111l111ll_opy_.bstack1ll1ll111ll_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠠࠣᘫ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack11lll1llll1_opy_(
        self,
        f: bstack111l111ll_opy_,
        bstack11lll1ll1l1_opy_: object,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1lll_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺࠢᘬ"):
            return
        if not bstack11lll11l1_opy_():
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦࡣࡰࡰࡱࡩࡨࡺࠠ࡮ࡧࡷ࡬ࡴࡪࠬࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧᘭ"))
            return
        def wrapped(bstack11lll1ll1l1_opy_, connect, *args, **kwargs):
            response = self.bstack11lll11llll_opy_(f.platform_index, instance.ref(), json.dumps({bstack1ll1lll_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᘮ"): True}).encode(bstack1ll1lll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᘯ")))
            if response is not None and response.capabilities:
                bstack1ll111ll1l_opy_ = json.loads(response.capabilities.decode(bstack1ll1lll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᘰ")))
                if not bstack1ll111ll1l_opy_:
                    return
                if bstack1ll111ll1l_opy_.get(bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᘱ")) and not self.bstack11lll11ll1l_opy_(bstack1ll111ll1l_opy_):
                    bstack1ll111ll1l_opy_[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᘲ")] = False
                    bstack11lll1l111l_opy_ = [bstack11lll1l11ll_opy_ for bstack11lll1l11ll_opy_ in bstack1ll111ll1l_opy_ if bstack11lll1l11ll_opy_.startswith(bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᘳ"))]
                    for bstack11lll1l11ll_opy_ in bstack11lll1l111l_opy_:
                        del bstack1ll111ll1l_opy_[bstack11lll1l11ll_opy_]
                bstack11lll1lll1l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1ll111ll1l_opy_))
                if bstack1ll111ll1l_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᘴ")):
                    browser = bstack11lll1ll1l1_opy_.connect_over_cdp(bstack11lll1lll1l_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack11lll1lll1l_opy_
                    return connect(bstack11lll1ll1l1_opy_, *args, **kwargs)
        return wrapped
    def bstack11lll1l1l1l_opy_(
        self,
        f: bstack111l111ll_opy_,
        bstack1l111llll1l_opy_: object,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1lll_opy_ (u"ࠣࡰࡨࡻࡤࡶࡡࡨࡧࠥᘵ"):
            return
        if not bstack11lll11l1_opy_():
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡰࡨࡻࡤࡶࡡࡨࡧࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᘶ"))
            return
        def wrapped(bstack1l111llll1l_opy_, bstack11lll1l1ll1_opy_, *args, **kwargs):
            contexts = bstack1l111llll1l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1ll1lll_opy_ (u"ࠥࡥࡧࡵࡵࡵ࠼ࡥࡰࡦࡴ࡫ࠣᘷ") in page.url:
                                return page
                            else:
                                return bstack11lll1l1ll1_opy_(bstack1l111llll1l_opy_)
                    else:
                        return bstack11lll1l1ll1_opy_(bstack1l111llll1l_opy_)
        return wrapped
    def bstack11lll11llll_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᘸ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴ࠻ࠢࠥᘹ") + str(req) + bstack1ll1lll_opy_ (u"ࠨࠢᘺ"))
        try:
            r = self.bstack1l1llll1lll_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࡵࡸࡧࡨ࡫ࡳࡴ࠿ࠥᘻ") + str(r.success) + bstack1ll1lll_opy_ (u"ࠣࠤᘼ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᘽ") + str(e) + bstack1ll1lll_opy_ (u"ࠥࠦᘾ"))
            traceback.print_exc()
            raise e
    def bstack11lll1l1lll_opy_(
        self,
        f: bstack111l111ll_opy_,
        Connection: object,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1lll_opy_ (u"ࠦࡤࡹࡥ࡯ࡦࡢࡱࡪࡹࡳࡢࡩࡨࡣࡹࡵ࡟ࡴࡧࡵࡺࡪࡸࠢᘿ"):
            return
        if not bstack11lll11l1_opy_():
            return
        def wrapped(Connection, bstack11lll1ll1ll_opy_, *args, **kwargs):
            return bstack11lll1ll1ll_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack111l111ll_opy_,
        bstack11lll1ll1l1_opy_: object,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1lll_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࠦᙀ"):
            return
        if not bstack11lll11l1_opy_():
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡩ࡬ࡰࡵࡨࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᙁ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped