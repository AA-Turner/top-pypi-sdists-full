# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll1l1l11l1_opy_ import bstack1ll11llll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111l1_opy_ import (
    bstack1ll1lll1lll_opy_,
    bstack1lll11l111l_opy_,
    bstack1ll1llll111_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1ll11111l11_opy_ import bstack1l1lllll1ll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l11lll1ll_opy_
from bstack_utils.helper import bstack1l111lll111_opy_
import threading
import os
import urllib.parse
class bstack1ll1l11llll_opy_(bstack1ll11llll11_opy_):
    def __init__(self, bstack1l1llll1l11_opy_):
        super().__init__()
        bstack1l1lllll1ll_opy_.bstack1l1l11lll1l_opy_((bstack1ll1lll1lll_opy_.bstack1lll111ll1l_opy_, bstack1lll11l111l_opy_.PRE), self.bstack1l1111lll1l_opy_)
        bstack1l1lllll1ll_opy_.bstack1l1l11lll1l_opy_((bstack1ll1lll1lll_opy_.bstack1lll111ll1l_opy_, bstack1lll11l111l_opy_.PRE), self.bstack1l1111ll1l1_opy_)
        bstack1l1lllll1ll_opy_.bstack1l1l11lll1l_opy_((bstack1ll1lll1lll_opy_.bstack1lll11l11l1_opy_, bstack1lll11l111l_opy_.PRE), self.bstack1l111l111ll_opy_)
        bstack1l1lllll1ll_opy_.bstack1l1l11lll1l_opy_((bstack1ll1lll1lll_opy_.bstack1lll11111ll_opy_, bstack1lll11l111l_opy_.PRE), self.bstack1l1111ll1ll_opy_)
        bstack1l1lllll1ll_opy_.bstack1l1l11lll1l_opy_((bstack1ll1lll1lll_opy_.bstack1lll111ll1l_opy_, bstack1lll11l111l_opy_.PRE), self.bstack1l111l111l1_opy_)
        bstack1l1lllll1ll_opy_.bstack1l1l11lll1l_opy_((bstack1ll1lll1lll_opy_.QUIT, bstack1lll11l111l_opy_.PRE), self.on_close)
        self.bstack1l1llll1l11_opy_ = bstack1l1llll1l11_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1111lll1l_opy_(
        self,
        f: bstack1l1lllll1ll_opy_,
        bstack1l111l1111l_opy_: object,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1l11_opy_ (u"ࠧࡲࡡࡶࡰࡦ࡬ࠧᒣ"):
            return
        if not bstack1l111lll111_opy_():
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡲࡡࡶࡰࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥᒤ"))
            return
        def wrapped(bstack1l111l1111l_opy_, launch, *args, **kwargs):
            response = self.bstack1l111l11lll_opy_(f.platform_index, instance.ref(), json.dumps({bstack11l1l11_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᒥ"): True}).encode(bstack11l1l11_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᒦ")))
            if response is not None and response.capabilities:
                if not bstack1l111lll111_opy_():
                    browser = launch(bstack1l111l1111l_opy_)
                    return browser
                bstack1l1111llll1_opy_ = json.loads(response.capabilities.decode(bstack11l1l11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᒧ")))
                if not bstack1l1111llll1_opy_: # empty caps bstack1l111l11l11_opy_ bstack1l111l11111_opy_ bstack1l1111lll11_opy_ bstack1l1llll1ll1_opy_ or error in processing
                    return
                bstack1l111l11l1l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1111llll1_opy_))
                f.bstack1lll111ll11_opy_(instance, bstack1l1lllll1ll_opy_.bstack1l111l1l11l_opy_, bstack1l111l11l1l_opy_)
                f.bstack1lll111ll11_opy_(instance, bstack1l1lllll1ll_opy_.bstack1l1111ll11l_opy_, bstack1l1111llll1_opy_)
                browser = bstack1l111l1111l_opy_.connect(bstack1l111l11l1l_opy_)
                return browser
        return wrapped
    def bstack1l111l111ll_opy_(
        self,
        f: bstack1l1lllll1ll_opy_,
        Connection: object,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1l11_opy_ (u"ࠥࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠧᒨ"):
            self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥᒩ"))
            return
        if not bstack1l111lll111_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack11l1l11_opy_ (u"ࠬࡶࡡࡳࡣࡰࡷࠬᒪ"), {}).get(bstack11l1l11_opy_ (u"࠭ࡢࡴࡒࡤࡶࡦࡳࡳࠨᒫ")):
                    bstack1l111l11ll1_opy_ = args[0][bstack11l1l11_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢᒬ")][bstack11l1l11_opy_ (u"ࠣࡤࡶࡔࡦࡸࡡ࡮ࡵࠥᒭ")]
                    session_id = bstack1l111l11ll1_opy_.get(bstack11l1l11_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡌࡨࠧᒮ"))
                    f.bstack1lll111ll11_opy_(instance, bstack1l1lllll1ll_opy_.bstack1l111l1l111_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࠨᒯ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l111l111l1_opy_(
        self,
        f: bstack1l1lllll1ll_opy_,
        bstack1l111l1111l_opy_: object,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1l11_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࠧᒰ"):
            return
        if not bstack1l111lll111_opy_():
            self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡨࡵ࡮࡯ࡧࡦࡸࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥᒱ"))
            return
        def wrapped(bstack1l111l1111l_opy_, connect, *args, **kwargs):
            response = self.bstack1l111l11lll_opy_(f.platform_index, instance.ref(), json.dumps({bstack11l1l11_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᒲ"): True}).encode(bstack11l1l11_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᒳ")))
            if response is not None and response.capabilities:
                bstack1l1111llll1_opy_ = json.loads(response.capabilities.decode(bstack11l1l11_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᒴ")))
                if not bstack1l1111llll1_opy_:
                    return
                bstack1l111l11l1l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1111llll1_opy_))
                if bstack1l1111llll1_opy_.get(bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᒵ")):
                    browser = bstack1l111l1111l_opy_.bstack1l1111ll111_opy_(bstack1l111l11l1l_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l111l11l1l_opy_
                    return connect(bstack1l111l1111l_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1111ll1l1_opy_(
        self,
        f: bstack1l1lllll1ll_opy_,
        bstack1l1l11111ll_opy_: object,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1l11_opy_ (u"ࠥࡲࡪࡽ࡟ࡱࡣࡪࡩࠧᒶ"):
            return
        if not bstack1l111lll111_opy_():
            self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡲࡪࡽ࡟ࡱࡣࡪࡩࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥᒷ"))
            return
        def wrapped(bstack1l1l11111ll_opy_, bstack1l1111lllll_opy_, *args, **kwargs):
            contexts = bstack1l1l11111ll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack11l1l11_opy_ (u"ࠧࡧࡢࡰࡷࡷ࠾ࡧࡲࡡ࡯࡭ࠥᒸ") in page.url:
                                return page
                            else:
                                return bstack1l1111lllll_opy_(bstack1l1l11111ll_opy_)
                    else:
                        return bstack1l1111lllll_opy_(bstack1l1l11111ll_opy_)
        return wrapped
    def bstack1l111l11lll_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.client_worker_id = bstack11l1l11_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᒹ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡺࡩࡧࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧᒺ") + str(req) + bstack11l1l11_opy_ (u"ࠣࠤᒻ"))
        try:
            r = self.bstack1ll1ll11111_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧᒼ") + str(r.success) + bstack11l1l11_opy_ (u"ࠥࠦᒽ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᒾ") + str(e) + bstack11l1l11_opy_ (u"ࠧࠨᒿ"))
            traceback.print_exc()
            raise e
    def bstack1l1111ll1ll_opy_(
        self,
        f: bstack1l1lllll1ll_opy_,
        Connection: object,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1l11_opy_ (u"ࠨ࡟ࡴࡧࡱࡨࡤࡳࡥࡴࡵࡤ࡫ࡪࡥࡴࡰࡡࡶࡩࡷࡼࡥࡳࠤᓀ"):
            return
        if not bstack1l111lll111_opy_():
            return
        def wrapped(Connection, bstack1l111l1l1l1_opy_, *args, **kwargs):
            return bstack1l111l1l1l1_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1l1lllll1ll_opy_,
        bstack1l111l1111l_opy_: object,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1l11_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨᓁ"):
            return
        if not bstack1l111lll111_opy_():
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡤ࡮ࡲࡷࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦᓂ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped