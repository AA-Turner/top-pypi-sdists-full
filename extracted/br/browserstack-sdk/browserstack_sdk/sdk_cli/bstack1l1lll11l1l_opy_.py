# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll111111l1_opy_ import bstack1l1ll1lll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1111l1l_opy_ import (
    bstack1ll1lllllll_opy_,
    bstack1ll1l1llll1_opy_,
    bstack1ll1l1ll1ll_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1l1llll11ll_opy_ import bstack1l1lllll11l_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack111l1l1l1_opy_
from bstack_utils.helper import bstack1l111lllll1_opy_
import threading
import os
import urllib.parse
class bstack1ll111l111l_opy_(bstack1l1ll1lll11_opy_):
    def __init__(self, bstack1ll111l1l1l_opy_):
        super().__init__()
        bstack1l1lllll11l_opy_.bstack1l1l1l111ll_opy_((bstack1ll1lllllll_opy_.bstack1lll1111111_opy_, bstack1ll1l1llll1_opy_.PRE), self.bstack1l11111l1l1_opy_)
        bstack1l1lllll11l_opy_.bstack1l1l1l111ll_opy_((bstack1ll1lllllll_opy_.bstack1lll1111111_opy_, bstack1ll1l1llll1_opy_.PRE), self.bstack1l1111l11l1_opy_)
        bstack1l1lllll11l_opy_.bstack1l1l1l111ll_opy_((bstack1ll1lllllll_opy_.bstack1ll1ll1111l_opy_, bstack1ll1l1llll1_opy_.PRE), self.bstack1l11111l1ll_opy_)
        bstack1l1lllll11l_opy_.bstack1l1l1l111ll_opy_((bstack1ll1lllllll_opy_.bstack1ll1ll1l11l_opy_, bstack1ll1l1llll1_opy_.PRE), self.bstack1l11111ll11_opy_)
        bstack1l1lllll11l_opy_.bstack1l1l1l111ll_opy_((bstack1ll1lllllll_opy_.bstack1lll1111111_opy_, bstack1ll1l1llll1_opy_.PRE), self.bstack1l1111l1l1l_opy_)
        bstack1l1lllll11l_opy_.bstack1l1l1l111ll_opy_((bstack1ll1lllllll_opy_.QUIT, bstack1ll1l1llll1_opy_.PRE), self.on_close)
        self.bstack1ll111l1l1l_opy_ = bstack1ll111l1l1l_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l11111l1l1_opy_(
        self,
        f: bstack1l1lllll11l_opy_,
        bstack1l1111ll111_opy_: object,
        exec: Tuple[bstack1ll1l1ll1ll_opy_, str],
        bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l11_opy_ (u"ࠤ࡯ࡥࡺࡴࡣࡩࠤᒙ"):
            return
        if not bstack1l111lllll1_opy_():
            self.logger.debug(bstack11l11_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢ࡯ࡥࡺࡴࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᒚ"))
            return
        def wrapped(bstack1l1111ll111_opy_, launch, *args, **kwargs):
            response = self.bstack1l11111l11l_opy_(f.platform_index, instance.ref(), json.dumps({bstack11l11_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᒛ"): True}).encode(bstack11l11_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᒜ")))
            if response is not None and response.capabilities:
                if not bstack1l111lllll1_opy_():
                    browser = launch(bstack1l1111ll111_opy_)
                    return browser
                bstack1l1111ll1l1_opy_ = json.loads(response.capabilities.decode(bstack11l11_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᒝ")))
                if not bstack1l1111ll1l1_opy_: # empty caps bstack1l1111l1111_opy_ bstack1l1111l1l11_opy_ bstack1l11111llll_opy_ bstack1l1llll1lll_opy_ or error in processing
                    return
                bstack1l11111ll1l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1111ll1l1_opy_))
                f.bstack1ll1lll111l_opy_(instance, bstack1l1lllll11l_opy_.bstack1l11111lll1_opy_, bstack1l11111ll1l_opy_)
                f.bstack1ll1lll111l_opy_(instance, bstack1l1lllll11l_opy_.bstack1l1111l1lll_opy_, bstack1l1111ll1l1_opy_)
                browser = bstack1l1111ll111_opy_.connect(bstack1l11111ll1l_opy_)
                return browser
        return wrapped
    def bstack1l11111l1ll_opy_(
        self,
        f: bstack1l1lllll11l_opy_,
        Connection: object,
        exec: Tuple[bstack1ll1l1ll1ll_opy_, str],
        bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l11_opy_ (u"ࠢࡥ࡫ࡶࡴࡦࡺࡣࡩࠤᒞ"):
            self.logger.debug(bstack11l11_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡥ࡫ࡶࡴࡦࡺࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᒟ"))
            return
        if not bstack1l111lllll1_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack11l11_opy_ (u"ࠩࡳࡥࡷࡧ࡭ࡴࠩᒠ"), {}).get(bstack11l11_opy_ (u"ࠪࡦࡸࡖࡡࡳࡣࡰࡷࠬᒡ")):
                    bstack1l1111l1ll1_opy_ = args[0][bstack11l11_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦᒢ")][bstack11l11_opy_ (u"ࠧࡨࡳࡑࡣࡵࡥࡲࡹࠢᒣ")]
                    session_id = bstack1l1111l1ll1_opy_.get(bstack11l11_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴࡉࡥࠤᒤ"))
                    f.bstack1ll1lll111l_opy_(instance, bstack1l1lllll11l_opy_.bstack1l1111ll1ll_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack11l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡤࡪࡵࡳࡥࡹࡩࡨࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠢࠥᒥ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1111l1l1l_opy_(
        self,
        f: bstack1l1lllll11l_opy_,
        bstack1l1111ll111_opy_: object,
        exec: Tuple[bstack1ll1l1ll1ll_opy_, str],
        bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l11_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࠤᒦ"):
            return
        if not bstack1l111lllll1_opy_():
            self.logger.debug(bstack11l11_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡥࡲࡲࡳ࡫ࡣࡵࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᒧ"))
            return
        def wrapped(bstack1l1111ll111_opy_, connect, *args, **kwargs):
            response = self.bstack1l11111l11l_opy_(f.platform_index, instance.ref(), json.dumps({bstack11l11_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᒨ"): True}).encode(bstack11l11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᒩ")))
            if response is not None and response.capabilities:
                bstack1l1111ll1l1_opy_ = json.loads(response.capabilities.decode(bstack11l11_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᒪ")))
                if not bstack1l1111ll1l1_opy_:
                    return
                bstack1l11111ll1l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1111ll1l1_opy_))
                if bstack1l1111ll1l1_opy_.get(bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᒫ")):
                    browser = bstack1l1111ll111_opy_.bstack1l1111l111l_opy_(bstack1l11111ll1l_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l11111ll1l_opy_
                    return connect(bstack1l1111ll111_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1111l11l1_opy_(
        self,
        f: bstack1l1lllll11l_opy_,
        bstack1l11llll1ll_opy_: object,
        exec: Tuple[bstack1ll1l1ll1ll_opy_, str],
        bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l11_opy_ (u"ࠢ࡯ࡧࡺࡣࡵࡧࡧࡦࠤᒬ"):
            return
        if not bstack1l111lllll1_opy_():
            self.logger.debug(bstack11l11_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠ࡯ࡧࡺࡣࡵࡧࡧࡦࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᒭ"))
            return
        def wrapped(bstack1l11llll1ll_opy_, bstack1l1111l11ll_opy_, *args, **kwargs):
            contexts = bstack1l11llll1ll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack11l11_opy_ (u"ࠤࡤࡦࡴࡻࡴ࠻ࡤ࡯ࡥࡳࡱࠢᒮ") in page.url:
                                return page
                            else:
                                return bstack1l1111l11ll_opy_(bstack1l11llll1ll_opy_)
                    else:
                        return bstack1l1111l11ll_opy_(bstack1l11llll1ll_opy_)
        return wrapped
    def bstack1l11111l11l_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.client_worker_id = bstack11l11_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᒯ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11l11_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࠤᒰ") + str(req) + bstack11l11_opy_ (u"ࠧࠨᒱ"))
        try:
            r = self.bstack1ll1l1l1lll_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11l11_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࠤᒲ") + str(r.success) + bstack11l11_opy_ (u"ࠢࠣᒳ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l11_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᒴ") + str(e) + bstack11l11_opy_ (u"ࠤࠥᒵ"))
            traceback.print_exc()
            raise e
    def bstack1l11111ll11_opy_(
        self,
        f: bstack1l1lllll11l_opy_,
        Connection: object,
        exec: Tuple[bstack1ll1l1ll1ll_opy_, str],
        bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l11_opy_ (u"ࠥࡣࡸ࡫࡮ࡥࡡࡰࡩࡸࡹࡡࡨࡧࡢࡸࡴࡥࡳࡦࡴࡹࡩࡷࠨᒶ"):
            return
        if not bstack1l111lllll1_opy_():
            return
        def wrapped(Connection, bstack1l1111ll11l_opy_, *args, **kwargs):
            return bstack1l1111ll11l_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1l1lllll11l_opy_,
        bstack1l1111ll111_opy_: object,
        exec: Tuple[bstack1ll1l1ll1ll_opy_, str],
        bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l11_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࠥᒷ"):
            return
        if not bstack1l111lllll1_opy_():
            self.logger.debug(bstack11l11_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡨࡲ࡯ࡴࡧࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᒸ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped