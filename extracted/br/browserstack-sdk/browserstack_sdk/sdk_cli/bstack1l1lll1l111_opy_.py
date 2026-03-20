# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1l1ll1l11ll_opy_ import bstack1l1lllllll1_opy_
from browserstack_sdk.sdk_cli.bstack1llll1ll1l_opy_ import (
    bstack111ll1lll1_opy_,
    bstack11lllll11l_opy_,
    bstack1ll11llllll_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack11l1l1ll1_opy_ import bstack1l1l11ll1l_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1ll1l1ll1l_opy_
from bstack_utils.helper import bstack11l1111l1l_opy_
import threading
import os
import urllib.parse
class bstack1ll1111l111_opy_(bstack1l1lllllll1_opy_):
    def __init__(self, bstack1l1l1l1l11l_opy_):
        super().__init__()
        bstack1l1l11ll1l_opy_.bstack1l1l111lll1_opy_((bstack111ll1lll1_opy_.bstack1l1111ll11_opy_, bstack11lllll11l_opy_.PRE), self.bstack11llll11ll1_opy_)
        bstack1l1l11ll1l_opy_.bstack1l1l111lll1_opy_((bstack111ll1lll1_opy_.bstack1l1111ll11_opy_, bstack11lllll11l_opy_.PRE), self.bstack11lll1ll1l1_opy_)
        bstack1l1l11ll1l_opy_.bstack1l1l111lll1_opy_((bstack111ll1lll1_opy_.bstack1ll11llll11_opy_, bstack11lllll11l_opy_.PRE), self.bstack11llll11l11_opy_)
        bstack1l1l11ll1l_opy_.bstack1l1l111lll1_opy_((bstack111ll1lll1_opy_.bstack1ll1l11lll1_opy_, bstack11lllll11l_opy_.PRE), self.bstack11lll1llll1_opy_)
        bstack1l1l11ll1l_opy_.bstack1l1l111lll1_opy_((bstack111ll1lll1_opy_.bstack1l1111ll11_opy_, bstack11lllll11l_opy_.PRE), self.bstack11lll1lll11_opy_)
        bstack1l1l11ll1l_opy_.bstack1l1l111lll1_opy_((bstack111ll1lll1_opy_.QUIT, bstack11lllll11l_opy_.PRE), self.on_close)
        self.bstack1l1l1l1l11l_opy_ = bstack1l1l1l1l11l_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack11llll11ll1_opy_(
        self,
        f: bstack1l1l11ll1l_opy_,
        bstack11llll11111_opy_: object,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11lll1_opy_ (u"ࠦࡱࡧࡵ࡯ࡥ࡫ࠦᘇ"):
            return
        if not bstack11l1111l1l_opy_():
            self.logger.debug(bstack11lll1_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡱࡧࡵ࡯ࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᘈ"))
            return
        def wrapped(bstack11llll11111_opy_, launch, *args, **kwargs):
            response = self.bstack11llll1111l_opy_(f.platform_index, instance.ref(), json.dumps({bstack11lll1_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᘉ"): True}).encode(bstack11lll1_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᘊ")))
            if response is not None and response.capabilities:
                if not bstack11l1111l1l_opy_():
                    browser = launch(bstack11llll11111_opy_)
                    return browser
                bstack111llll1_opy_ = json.loads(response.capabilities.decode(bstack11lll1_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᘋ")))
                if not bstack111llll1_opy_: # empty caps bstack11lll1lllll_opy_ bstack11lll1ll11l_opy_ bstack11llll111l1_opy_ bstack11llll11l1l_opy_ or error in processing
                    return
                bstack11llll111ll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack111llll1_opy_))
                f.bstack1ll1ll1l1l_opy_(instance, bstack1l1l11ll1l_opy_.bstack11l1111lll_opy_, bstack11llll111ll_opy_)
                f.bstack1ll1ll1l1l_opy_(instance, bstack1l1l11ll1l_opy_.bstack1l1l111l11_opy_, bstack111llll1_opy_)
                browser = bstack11llll11111_opy_.connect(bstack11llll111ll_opy_)
                return browser
        return wrapped
    def bstack11llll11l11_opy_(
        self,
        f: bstack1l1l11ll1l_opy_,
        Connection: object,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11lll1_opy_ (u"ࠤࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠦᘌ"):
            self.logger.debug(bstack11lll1_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᘍ"))
            return
        if not bstack11l1111l1l_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack11lll1_opy_ (u"ࠫࡵࡧࡲࡢ࡯ࡶࠫᘎ"), {}).get(bstack11lll1_opy_ (u"ࠬࡨࡳࡑࡣࡵࡥࡲࡹࠧᘏ")):
                    bstack11lll1ll111_opy_ = args[0][bstack11lll1_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨᘐ")][bstack11lll1_opy_ (u"ࠢࡣࡵࡓࡥࡷࡧ࡭ࡴࠤᘑ")]
                    session_id = bstack11lll1ll111_opy_.get(bstack11lll1_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡋࡧࠦᘒ"))
                    f.bstack1ll1ll1l1l_opy_(instance, bstack1l1l11ll1l_opy_.bstack1ll1ll1ll1l_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack11lll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡦ࡬ࡷࡵࡧࡴࡤࡪࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࠧᘓ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack11lll1lll11_opy_(
        self,
        f: bstack1l1l11ll1l_opy_,
        bstack11llll11111_opy_: object,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11lll1_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦᘔ"):
            return
        if not bstack11l1111l1l_opy_():
            self.logger.debug(bstack11lll1_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡧࡴࡴ࡮ࡦࡥࡷࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᘕ"))
            return
        def wrapped(bstack11llll11111_opy_, connect, *args, **kwargs):
            response = self.bstack11llll1111l_opy_(f.platform_index, instance.ref(), json.dumps({bstack11lll1_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᘖ"): True}).encode(bstack11lll1_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᘗ")))
            if response is not None and response.capabilities:
                bstack111llll1_opy_ = json.loads(response.capabilities.decode(bstack11lll1_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᘘ")))
                if not bstack111llll1_opy_:
                    return
                bstack11llll111ll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack111llll1_opy_))
                if bstack111llll1_opy_.get(bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᘙ")):
                    browser = bstack11llll11111_opy_.connect_over_cdp(bstack11llll111ll_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack11llll111ll_opy_
                    return connect(bstack11llll11111_opy_, *args, **kwargs)
        return wrapped
    def bstack11lll1ll1l1_opy_(
        self,
        f: bstack1l1l11ll1l_opy_,
        bstack1l11l111lll_opy_: object,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11lll1_opy_ (u"ࠤࡱࡩࡼࡥࡰࡢࡩࡨࠦᘚ"):
            return
        if not bstack11l1111l1l_opy_():
            self.logger.debug(bstack11lll1_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡱࡩࡼࡥࡰࡢࡩࡨࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᘛ"))
            return
        def wrapped(bstack1l11l111lll_opy_, bstack11lll1ll1ll_opy_, *args, **kwargs):
            contexts = bstack1l11l111lll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack11lll1_opy_ (u"ࠦࡦࡨ࡯ࡶࡶ࠽ࡦࡱࡧ࡮࡬ࠤᘜ") in page.url:
                                return page
                            else:
                                return bstack11lll1ll1ll_opy_(bstack1l11l111lll_opy_)
                    else:
                        return bstack11lll1ll1ll_opy_(bstack1l11l111lll_opy_)
        return wrapped
    def bstack11llll1111l_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.client_worker_id = bstack11lll1_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᘝ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11lll1_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡹࡨࡦࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦᘞ") + str(req) + bstack11lll1_opy_ (u"ࠢࠣᘟ"))
        try:
            r = self.bstack1l1lll11l11_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11lll1_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦᘠ") + str(r.success) + bstack11lll1_opy_ (u"ࠤࠥᘡ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11lll1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᘢ") + str(e) + bstack11lll1_opy_ (u"ࠦࠧᘣ"))
            traceback.print_exc()
            raise e
    def bstack11lll1llll1_opy_(
        self,
        f: bstack1l1l11ll1l_opy_,
        Connection: object,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11lll1_opy_ (u"ࠧࡥࡳࡦࡰࡧࡣࡲ࡫ࡳࡴࡣࡪࡩࡤࡺ࡯ࡠࡵࡨࡶࡻ࡫ࡲࠣᘤ"):
            return
        if not bstack11l1111l1l_opy_():
            return
        def wrapped(Connection, bstack11lll1lll1l_opy_, *args, **kwargs):
            return bstack11lll1lll1l_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1l1l11ll1l_opy_,
        bstack11llll11111_opy_: object,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11lll1_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧᘥ"):
            return
        if not bstack11l1111l1l_opy_():
            self.logger.debug(bstack11lll1_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦࡣ࡭ࡱࡶࡩࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥᘦ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped