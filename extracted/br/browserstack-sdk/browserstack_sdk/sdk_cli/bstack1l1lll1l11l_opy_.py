# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
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
from browserstack_sdk.sdk_cli.bstack1l1llllllll_opy_ import bstack1ll11111l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import (
    bstack1ll1l1l11l1_opy_,
    bstack1ll1l11ll1l_opy_,
    bstack1ll1l1l111l_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1lll1111l11_opy_ import bstack1lll111l1l1_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l11l11l11_opy_
from bstack_utils.helper import bstack1lll111l1_opy_
import threading
import os
import urllib.parse
class bstack1l1ll111l1l_opy_(bstack1ll11111l11_opy_):
    def __init__(self, bstack1l1lllllll1_opy_):
        super().__init__()
        bstack1lll111l1l1_opy_.bstack1l1l1111111_opy_((bstack1ll1l1l11l1_opy_.bstack1ll1l1lll11_opy_, bstack1ll1l11ll1l_opy_.PRE), self.bstack11llll1llll_opy_)
        bstack1lll111l1l1_opy_.bstack1l1l1111111_opy_((bstack1ll1l1l11l1_opy_.bstack1ll1l1lll11_opy_, bstack1ll1l11ll1l_opy_.PRE), self.bstack11lllll1l11_opy_)
        bstack1lll111l1l1_opy_.bstack1l1l1111111_opy_((bstack1ll1l1l11l1_opy_.bstack1ll1ll111l1_opy_, bstack1ll1l11ll1l_opy_.PRE), self.bstack11llllll1l1_opy_)
        bstack1lll111l1l1_opy_.bstack1l1l1111111_opy_((bstack1ll1l1l11l1_opy_.bstack1ll1l11l11l_opy_, bstack1ll1l11ll1l_opy_.PRE), self.bstack11lllll111l_opy_)
        bstack1lll111l1l1_opy_.bstack1l1l1111111_opy_((bstack1ll1l1l11l1_opy_.bstack1ll1l1lll11_opy_, bstack1ll1l11ll1l_opy_.PRE), self.bstack11llllll11l_opy_)
        bstack1lll111l1l1_opy_.bstack1l1l1111111_opy_((bstack1ll1l1l11l1_opy_.QUIT, bstack1ll1l11ll1l_opy_.PRE), self.on_close)
        self.bstack1l1lllllll1_opy_ = bstack1l1lllllll1_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack11llll1llll_opy_(
        self,
        f: bstack1lll111l1l1_opy_,
        bstack11llllll1ll_opy_: object,
        exec: Tuple[bstack1ll1l1l111l_opy_, str],
        bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll111_opy_ (u"ࠦࡱࡧࡵ࡯ࡥ࡫ࠦᖗ"):
            return
        if not bstack1lll111l1_opy_():
            self.logger.debug(bstack1ll111_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡱࡧࡵ࡯ࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᖘ"))
            return
        def wrapped(bstack11llllll1ll_opy_, launch, *args, **kwargs):
            response = self.bstack11lllllll1l_opy_(f.platform_index, instance.ref(), json.dumps({bstack1ll111_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᖙ"): True}).encode(bstack1ll111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᖚ")))
            if response is not None and response.capabilities:
                if not bstack1lll111l1_opy_():
                    browser = launch(bstack11llllll1ll_opy_)
                    return browser
                bstack1lll1111ll1_opy_ = json.loads(response.capabilities.decode(bstack1ll111_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᖛ")))
                if not bstack1lll1111ll1_opy_: # empty caps bstack11lllll1111_opy_ bstack11lllll11l1_opy_ bstack11lllll1lll_opy_ bstack11lllllll11_opy_ or error in processing
                    return
                bstack11lllll1ll1_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1lll1111ll1_opy_))
                f.bstack1ll1ll1lll1_opy_(instance, bstack1lll111l1l1_opy_.bstack1lll111l1ll_opy_, bstack11lllll1ll1_opy_)
                f.bstack1ll1ll1lll1_opy_(instance, bstack1lll111l1l1_opy_.bstack1ll1lll1l1l_opy_, bstack1lll1111ll1_opy_)
                browser = bstack11llllll1ll_opy_.connect(bstack11lllll1ll1_opy_)
                return browser
        return wrapped
    def bstack11llllll1l1_opy_(
        self,
        f: bstack1lll111l1l1_opy_,
        Connection: object,
        exec: Tuple[bstack1ll1l1l111l_opy_, str],
        bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll111_opy_ (u"ࠤࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠦᖜ"):
            self.logger.debug(bstack1ll111_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᖝ"))
            return
        if not bstack1lll111l1_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1ll111_opy_ (u"ࠫࡵࡧࡲࡢ࡯ࡶࠫᖞ"), {}).get(bstack1ll111_opy_ (u"ࠬࡨࡳࡑࡣࡵࡥࡲࡹࠧᖟ")):
                    bstack11llllll111_opy_ = args[0][bstack1ll111_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨᖠ")][bstack1ll111_opy_ (u"ࠢࡣࡵࡓࡥࡷࡧ࡭ࡴࠤᖡ")]
                    session_id = bstack11llllll111_opy_.get(bstack1ll111_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡋࡧࠦᖢ"))
                    f.bstack1ll1ll1lll1_opy_(instance, bstack1lll111l1l1_opy_.bstack1ll1lll111l_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1ll111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡦ࡬ࡷࡵࡧࡴࡤࡪࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࠧᖣ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack11llllll11l_opy_(
        self,
        f: bstack1lll111l1l1_opy_,
        bstack11llllll1ll_opy_: object,
        exec: Tuple[bstack1ll1l1l111l_opy_, str],
        bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll111_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦᖤ"):
            return
        if not bstack1lll111l1_opy_():
            self.logger.debug(bstack1ll111_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡧࡴࡴ࡮ࡦࡥࡷࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᖥ"))
            return
        def wrapped(bstack11llllll1ll_opy_, connect, *args, **kwargs):
            response = self.bstack11lllllll1l_opy_(f.platform_index, instance.ref(), json.dumps({bstack1ll111_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᖦ"): True}).encode(bstack1ll111_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᖧ")))
            if response is not None and response.capabilities:
                bstack1lll1111ll1_opy_ = json.loads(response.capabilities.decode(bstack1ll111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᖨ")))
                if not bstack1lll1111ll1_opy_:
                    return
                bstack11lllll1ll1_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1lll1111ll1_opy_))
                if bstack1lll1111ll1_opy_.get(bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᖩ")):
                    browser = bstack11llllll1ll_opy_.connect_over_cdp(bstack11lllll1ll1_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack11lllll1ll1_opy_
                    return connect(bstack11llllll1ll_opy_, *args, **kwargs)
        return wrapped
    def bstack11lllll1l11_opy_(
        self,
        f: bstack1lll111l1l1_opy_,
        bstack1l11l1ll11l_opy_: object,
        exec: Tuple[bstack1ll1l1l111l_opy_, str],
        bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll111_opy_ (u"ࠤࡱࡩࡼࡥࡰࡢࡩࡨࠦᖪ"):
            return
        if not bstack1lll111l1_opy_():
            self.logger.debug(bstack1ll111_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡱࡩࡼࡥࡰࡢࡩࡨࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᖫ"))
            return
        def wrapped(bstack1l11l1ll11l_opy_, bstack11lllll1l1l_opy_, *args, **kwargs):
            contexts = bstack1l11l1ll11l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1ll111_opy_ (u"ࠦࡦࡨ࡯ࡶࡶ࠽ࡦࡱࡧ࡮࡬ࠤᖬ") in page.url:
                                return page
                            else:
                                return bstack11lllll1l1l_opy_(bstack1l11l1ll11l_opy_)
                    else:
                        return bstack11lllll1l1l_opy_(bstack1l11l1ll11l_opy_)
        return wrapped
    def bstack11lllllll1l_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.client_worker_id = bstack1ll111_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᖭ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1ll111_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡹࡨࡦࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦᖮ") + str(req) + bstack1ll111_opy_ (u"ࠢࠣᖯ"))
        try:
            r = self.bstack1ll1lll11ll_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1ll111_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦᖰ") + str(r.success) + bstack1ll111_opy_ (u"ࠤࠥᖱ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᖲ") + str(e) + bstack1ll111_opy_ (u"ࠦࠧᖳ"))
            traceback.print_exc()
            raise e
    def bstack11lllll111l_opy_(
        self,
        f: bstack1lll111l1l1_opy_,
        Connection: object,
        exec: Tuple[bstack1ll1l1l111l_opy_, str],
        bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll111_opy_ (u"ࠧࡥࡳࡦࡰࡧࡣࡲ࡫ࡳࡴࡣࡪࡩࡤࡺ࡯ࡠࡵࡨࡶࡻ࡫ࡲࠣᖴ"):
            return
        if not bstack1lll111l1_opy_():
            return
        def wrapped(Connection, bstack11lllll11ll_opy_, *args, **kwargs):
            return bstack11lllll11ll_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1lll111l1l1_opy_,
        bstack11llllll1ll_opy_: object,
        exec: Tuple[bstack1ll1l1l111l_opy_, str],
        bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll111_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧᖵ"):
            return
        if not bstack1lll111l1_opy_():
            self.logger.debug(bstack1ll111_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦࡣ࡭ࡱࡶࡩࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥᖶ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped