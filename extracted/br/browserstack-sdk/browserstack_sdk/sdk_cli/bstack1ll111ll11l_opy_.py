# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1l1l1llll11_opy_ import bstack1ll1111l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1l11l_opy_ import (
    bstack1ll1l1l1lll_opy_,
    bstack1ll1ll1111l_opy_,
    bstack1ll1l1lll1l_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1ll1lllll1l_opy_ import bstack1ll1llllll1_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack111l11l11_opy_
from bstack_utils.helper import bstack111l1ll11l_opy_
import threading
import os
import urllib.parse
class bstack1l1lllll1ll_opy_(bstack1ll1111l1ll_opy_):
    def __init__(self, bstack1l1lll1l11l_opy_):
        super().__init__()
        bstack1ll1llllll1_opy_.bstack1l1l11llll1_opy_((bstack1ll1l1l1lll_opy_.bstack1ll1l111l1l_opy_, bstack1ll1ll1111l_opy_.PRE), self.bstack11llllll11l_opy_)
        bstack1ll1llllll1_opy_.bstack1l1l11llll1_opy_((bstack1ll1l1l1lll_opy_.bstack1ll1l111l1l_opy_, bstack1ll1ll1111l_opy_.PRE), self.bstack11lllllll11_opy_)
        bstack1ll1llllll1_opy_.bstack1l1l11llll1_opy_((bstack1ll1l1l1lll_opy_.bstack1ll1l11lll1_opy_, bstack1ll1ll1111l_opy_.PRE), self.bstack11llllll1l1_opy_)
        bstack1ll1llllll1_opy_.bstack1l1l11llll1_opy_((bstack1ll1l1l1lll_opy_.bstack1ll11ll1lll_opy_, bstack1ll1ll1111l_opy_.PRE), self.bstack11lllll1l11_opy_)
        bstack1ll1llllll1_opy_.bstack1l1l11llll1_opy_((bstack1ll1l1l1lll_opy_.bstack1ll1l111l1l_opy_, bstack1ll1ll1111l_opy_.PRE), self.bstack11llllll111_opy_)
        bstack1ll1llllll1_opy_.bstack1l1l11llll1_opy_((bstack1ll1l1l1lll_opy_.QUIT, bstack1ll1ll1111l_opy_.PRE), self.on_close)
        self.bstack1l1lll1l11l_opy_ = bstack1l1lll1l11l_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack11llllll11l_opy_(
        self,
        f: bstack1ll1llllll1_opy_,
        bstack11llllll1ll_opy_: object,
        exec: Tuple[bstack1ll1l1lll1l_opy_, str],
        bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1111l_opy_ (u"ࠢ࡭ࡣࡸࡲࡨ࡮ࠢᗒ"):
            return
        if not bstack111l1ll11l_opy_():
            self.logger.debug(bstack1111l_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠ࡭ࡣࡸࡲࡨ࡮ࠠ࡮ࡧࡷ࡬ࡴࡪࠬࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧᗓ"))
            return
        def wrapped(bstack11llllll1ll_opy_, launch, *args, **kwargs):
            response = self.bstack11lllll1111_opy_(f.platform_index, instance.ref(), json.dumps({bstack1111l_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᗔ"): True}).encode(bstack1111l_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᗕ")))
            if response is not None and response.capabilities:
                if not bstack111l1ll11l_opy_():
                    browser = launch(bstack11llllll1ll_opy_)
                    return browser
                bstack1lll111l1l1_opy_ = json.loads(response.capabilities.decode(bstack1111l_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᗖ")))
                if not bstack1lll111l1l1_opy_: # empty caps bstack11lllll1l1l_opy_ bstack11lllll11ll_opy_ bstack11lllll1ll1_opy_ bstack11lllll1lll_opy_ or error in processing
                    return
                bstack11llll1llll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1lll111l1l1_opy_))
                f.bstack1ll1lllll11_opy_(instance, bstack1ll1llllll1_opy_.bstack1lll1111ll1_opy_, bstack11llll1llll_opy_)
                f.bstack1ll1lllll11_opy_(instance, bstack1ll1llllll1_opy_.bstack1ll1lll1lll_opy_, bstack1lll111l1l1_opy_)
                browser = bstack11llllll1ll_opy_.connect(bstack11llll1llll_opy_)
                return browser
        return wrapped
    def bstack11llllll1l1_opy_(
        self,
        f: bstack1ll1llllll1_opy_,
        Connection: object,
        exec: Tuple[bstack1ll1l1lll1l_opy_, str],
        bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1111l_opy_ (u"ࠧࡪࡩࡴࡲࡤࡸࡨ࡮ࠢᗗ"):
            self.logger.debug(bstack1111l_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡪࡩࡴࡲࡤࡸࡨ࡮ࠠ࡮ࡧࡷ࡬ࡴࡪࠬࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧᗘ"))
            return
        if not bstack111l1ll11l_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1111l_opy_ (u"ࠧࡱࡣࡵࡥࡲࡹࠧᗙ"), {}).get(bstack1111l_opy_ (u"ࠨࡤࡶࡔࡦࡸࡡ࡮ࡵࠪᗚ")):
                    bstack11lllll11l1_opy_ = args[0][bstack1111l_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤᗛ")][bstack1111l_opy_ (u"ࠥࡦࡸࡖࡡࡳࡣࡰࡷࠧᗜ")]
                    session_id = bstack11lllll11l1_opy_.get(bstack1111l_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡎࡪࠢᗝ"))
                    f.bstack1ll1lllll11_opy_(instance, bstack1ll1llllll1_opy_.bstack1ll1llll1l1_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠠࠣᗞ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack11llllll111_opy_(
        self,
        f: bstack1ll1llllll1_opy_,
        bstack11llllll1ll_opy_: object,
        exec: Tuple[bstack1ll1l1lll1l_opy_, str],
        bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1111l_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺࠢᗟ"):
            return
        if not bstack111l1ll11l_opy_():
            self.logger.debug(bstack1111l_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦࡣࡰࡰࡱࡩࡨࡺࠠ࡮ࡧࡷ࡬ࡴࡪࠬࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧᗠ"))
            return
        def wrapped(bstack11llllll1ll_opy_, connect, *args, **kwargs):
            response = self.bstack11lllll1111_opy_(f.platform_index, instance.ref(), json.dumps({bstack1111l_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᗡ"): True}).encode(bstack1111l_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᗢ")))
            if response is not None and response.capabilities:
                bstack1lll111l1l1_opy_ = json.loads(response.capabilities.decode(bstack1111l_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᗣ")))
                if not bstack1lll111l1l1_opy_:
                    return
                bstack11llll1llll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1lll111l1l1_opy_))
                if bstack1lll111l1l1_opy_.get(bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᗤ")):
                    browser = bstack11llllll1ll_opy_.connect_over_cdp(bstack11llll1llll_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack11llll1llll_opy_
                    return connect(bstack11llllll1ll_opy_, *args, **kwargs)
        return wrapped
    def bstack11lllllll11_opy_(
        self,
        f: bstack1ll1llllll1_opy_,
        bstack1l11l1llll1_opy_: object,
        exec: Tuple[bstack1ll1l1lll1l_opy_, str],
        bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1111l_opy_ (u"ࠧࡴࡥࡸࡡࡳࡥ࡬࡫ࠢᗥ"):
            return
        if not bstack111l1ll11l_opy_():
            self.logger.debug(bstack1111l_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡴࡥࡸࡡࡳࡥ࡬࡫ࠠ࡮ࡧࡷ࡬ࡴࡪࠬࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧᗦ"))
            return
        def wrapped(bstack1l11l1llll1_opy_, bstack11llll1lll1_opy_, *args, **kwargs):
            contexts = bstack1l11l1llll1_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1111l_opy_ (u"ࠢࡢࡤࡲࡹࡹࡀࡢ࡭ࡣࡱ࡯ࠧᗧ") in page.url:
                                return page
                            else:
                                return bstack11llll1lll1_opy_(bstack1l11l1llll1_opy_)
                    else:
                        return bstack11llll1lll1_opy_(bstack1l11l1llll1_opy_)
        return wrapped
    def bstack11lllll1111_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.client_worker_id = bstack1111l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᗨ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1111l_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸ࠿ࠦࠢᗩ") + str(req) + bstack1111l_opy_ (u"ࠥࠦᗪ"))
        try:
            r = self.bstack1ll1ll1lll1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1111l_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࡹࡵࡤࡥࡨࡷࡸࡃࠢᗫ") + str(r.success) + bstack1111l_opy_ (u"ࠧࠨᗬ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111l_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᗭ") + str(e) + bstack1111l_opy_ (u"ࠢࠣᗮ"))
            traceback.print_exc()
            raise e
    def bstack11lllll1l11_opy_(
        self,
        f: bstack1ll1llllll1_opy_,
        Connection: object,
        exec: Tuple[bstack1ll1l1lll1l_opy_, str],
        bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1111l_opy_ (u"ࠣࡡࡶࡩࡳࡪ࡟࡮ࡧࡶࡷࡦ࡭ࡥࡠࡶࡲࡣࡸ࡫ࡲࡷࡧࡵࠦᗯ"):
            return
        if not bstack111l1ll11l_opy_():
            return
        def wrapped(Connection, bstack11lllll111l_opy_, *args, **kwargs):
            return bstack11lllll111l_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1ll1llllll1_opy_,
        bstack11llllll1ll_opy_: object,
        exec: Tuple[bstack1ll1l1lll1l_opy_, str],
        bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1111l_opy_ (u"ࠤࡦࡰࡴࡹࡥࠣᗰ"):
            return
        if not bstack111l1ll11l_opy_():
            self.logger.debug(bstack1111l_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡦࡰࡴࡹࡥࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨᗱ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped