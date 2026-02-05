# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll1ll11l11_opy_ import bstack1ll1l11l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import (
    bstack1lll111lll1_opy_,
    bstack1lll1ll1l11_opy_,
    bstack1lll11lll1l_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1ll1l111l11_opy_ import bstack1ll111ll1l1_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack111l1l1111_opy_
from bstack_utils.helper import bstack1l1l1111ll1_opy_
import threading
import os
import urllib.parse
class bstack1ll1lllll11_opy_(bstack1ll1l11l1ll_opy_):
    def __init__(self, bstack1ll1llllll1_opy_):
        super().__init__()
        bstack1ll111ll1l1_opy_.bstack1l1ll11llll_opy_((bstack1lll111lll1_opy_.bstack1lll1l1l11l_opy_, bstack1lll1ll1l11_opy_.PRE), self.bstack1l11l111111_opy_)
        bstack1ll111ll1l1_opy_.bstack1l1ll11llll_opy_((bstack1lll111lll1_opy_.bstack1lll1l1l11l_opy_, bstack1lll1ll1l11_opy_.PRE), self.bstack1l11l111ll1_opy_)
        bstack1ll111ll1l1_opy_.bstack1l1ll11llll_opy_((bstack1lll111lll1_opy_.bstack1lll1l11l11_opy_, bstack1lll1ll1l11_opy_.PRE), self.bstack1l11l1111l1_opy_)
        bstack1ll111ll1l1_opy_.bstack1l1ll11llll_opy_((bstack1lll111lll1_opy_.bstack1lll1ll111l_opy_, bstack1lll1ll1l11_opy_.PRE), self.bstack1l11l11l11l_opy_)
        bstack1ll111ll1l1_opy_.bstack1l1ll11llll_opy_((bstack1lll111lll1_opy_.bstack1lll1l1l11l_opy_, bstack1lll1ll1l11_opy_.PRE), self.bstack1l11l111l11_opy_)
        bstack1ll111ll1l1_opy_.bstack1l1ll11llll_opy_((bstack1lll111lll1_opy_.QUIT, bstack1lll1ll1l11_opy_.PRE), self.on_close)
        self.bstack1ll1llllll1_opy_ = bstack1ll1llllll1_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l111111_opy_(
        self,
        f: bstack1ll111ll1l1_opy_,
        bstack1l11l111l1l_opy_: object,
        exec: Tuple[bstack1lll11lll1l_opy_, str],
        bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1ll1_opy_ (u"ࠣ࡮ࡤࡹࡳࡩࡨࠣᏰ"):
            return
        if not bstack1l1l1111ll1_opy_():
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡ࡮ࡤࡹࡳࡩࡨࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨᏱ"))
            return
        def wrapped(bstack1l11l111l1l_opy_, launch, *args, **kwargs):
            response = self.bstack1l111lllll1_opy_(f.platform_index, instance.ref(), json.dumps({bstack11l1ll1_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᏲ"): True}).encode(bstack11l1ll1_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᏳ")))
            if response is not None and response.capabilities:
                if not bstack1l1l1111ll1_opy_():
                    browser = launch(bstack1l11l111l1l_opy_)
                    return browser
                bstack1l11l11111l_opy_ = json.loads(response.capabilities.decode(bstack11l1ll1_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᏴ")))
                if not bstack1l11l11111l_opy_: # empty caps bstack1l111llll1l_opy_ bstack1l11l1111ll_opy_ bstack1l11l11l111_opy_ bstack1ll1l1l11l1_opy_ or error in processing
                    return
                bstack1l111lll11l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l11l11111l_opy_))
                f.bstack1lll1l1111l_opy_(instance, bstack1ll111ll1l1_opy_.bstack1l111llll11_opy_, bstack1l111lll11l_opy_)
                f.bstack1lll1l1111l_opy_(instance, bstack1ll111ll1l1_opy_.bstack1l11l111lll_opy_, bstack1l11l11111l_opy_)
                browser = bstack1l11l111l1l_opy_.connect(bstack1l111lll11l_opy_)
                return browser
        return wrapped
    def bstack1l11l1111l1_opy_(
        self,
        f: bstack1ll111ll1l1_opy_,
        Connection: object,
        exec: Tuple[bstack1lll11lll1l_opy_, str],
        bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1ll1_opy_ (u"ࠨࡤࡪࡵࡳࡥࡹࡩࡨࠣᏵ"):
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦࡤࡪࡵࡳࡥࡹࡩࡨࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨ᏶"))
            return
        if not bstack1l1l1111ll1_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack11l1ll1_opy_ (u"ࠨࡲࡤࡶࡦࡳࡳࠨ᏷"), {}).get(bstack11l1ll1_opy_ (u"ࠩࡥࡷࡕࡧࡲࡢ࡯ࡶࠫᏸ")):
                    bstack1l11l11l1l1_opy_ = args[0][bstack11l1ll1_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡵࠥᏹ")][bstack11l1ll1_opy_ (u"ࠦࡧࡹࡐࡢࡴࡤࡱࡸࠨᏺ")]
                    session_id = bstack1l11l11l1l1_opy_.get(bstack11l1ll1_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡏࡤࠣᏻ"))
                    f.bstack1lll1l1111l_opy_(instance, bstack1ll111ll1l1_opy_.bstack1l111lll1ll_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡪࡩࡴࡲࡤࡸࡨ࡮ࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠡࠤᏼ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l11l111l11_opy_(
        self,
        f: bstack1ll111ll1l1_opy_,
        bstack1l11l111l1l_opy_: object,
        exec: Tuple[bstack1lll11lll1l_opy_, str],
        bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1ll1_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࠣᏽ"):
            return
        if not bstack1l1l1111ll1_opy_():
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡤࡱࡱࡲࡪࡩࡴࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨ᏾"))
            return
        def wrapped(bstack1l11l111l1l_opy_, connect, *args, **kwargs):
            response = self.bstack1l111lllll1_opy_(f.platform_index, instance.ref(), json.dumps({bstack11l1ll1_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨ᏿"): True}).encode(bstack11l1ll1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ᐀")))
            if response is not None and response.capabilities:
                bstack1l11l11111l_opy_ = json.loads(response.capabilities.decode(bstack11l1ll1_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᐁ")))
                if not bstack1l11l11111l_opy_:
                    return
                bstack1l111lll11l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l11l11111l_opy_))
                if bstack1l11l11111l_opy_.get(bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᐂ")):
                    browser = bstack1l11l111l1l_opy_.bstack1l11l11l1ll_opy_(bstack1l111lll11l_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l111lll11l_opy_
                    return connect(bstack1l11l111l1l_opy_, *args, **kwargs)
        return wrapped
    def bstack1l11l111ll1_opy_(
        self,
        f: bstack1ll111ll1l1_opy_,
        bstack1l1l1l111ll_opy_: object,
        exec: Tuple[bstack1lll11lll1l_opy_, str],
        bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1ll1_opy_ (u"ࠨ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠣᐃ"):
            return
        if not bstack1l1l1111ll1_opy_():
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨᐄ"))
            return
        def wrapped(bstack1l1l1l111ll_opy_, bstack1l111lll1l1_opy_, *args, **kwargs):
            contexts = bstack1l1l1l111ll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack11l1ll1_opy_ (u"ࠣࡣࡥࡳࡺࡺ࠺ࡣ࡮ࡤࡲࡰࠨᐅ") in page.url:
                                return page
                            else:
                                return bstack1l111lll1l1_opy_(bstack1l1l1l111ll_opy_)
                    else:
                        return bstack1l111lll1l1_opy_(bstack1l1l1l111ll_opy_)
        return wrapped
    def bstack1l111lllll1_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.client_worker_id = bstack11l1ll1_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᐆ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣᐇ") + str(req) + bstack11l1ll1_opy_ (u"ࠦࠧᐈ"))
        try:
            r = self.bstack1ll1llll1ll_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣᐉ") + str(r.success) + bstack11l1ll1_opy_ (u"ࠨࠢᐊ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᐋ") + str(e) + bstack11l1ll1_opy_ (u"ࠣࠤᐌ"))
            traceback.print_exc()
            raise e
    def bstack1l11l11l11l_opy_(
        self,
        f: bstack1ll111ll1l1_opy_,
        Connection: object,
        exec: Tuple[bstack1lll11lll1l_opy_, str],
        bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1ll1_opy_ (u"ࠤࡢࡷࡪࡴࡤࡠ࡯ࡨࡷࡸࡧࡧࡦࡡࡷࡳࡤࡹࡥࡳࡸࡨࡶࠧᐍ"):
            return
        if not bstack1l1l1111ll1_opy_():
            return
        def wrapped(Connection, bstack1l111llllll_opy_, *args, **kwargs):
            return bstack1l111llllll_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1ll111ll1l1_opy_,
        bstack1l11l111l1l_opy_: object,
        exec: Tuple[bstack1lll11lll1l_opy_, str],
        bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1ll1_opy_ (u"ࠥࡧࡱࡵࡳࡦࠤᐎ"):
            return
        if not bstack1l1l1111ll1_opy_():
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡧࡱࡵࡳࡦࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᐏ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped