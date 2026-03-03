# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll11ll11l1_opy_ import bstack1ll1l1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import (
    bstack1ll1ll1l1l1_opy_,
    bstack1lll111l1l1_opy_,
    bstack1ll1lll1111_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1ll1111111l_opy_ import bstack1ll11l1111l_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11llll11ll_opy_
from bstack_utils.helper import bstack1l11l1111ll_opy_
import threading
import os
import urllib.parse
class bstack1ll11llll11_opy_(bstack1ll1l1l11l1_opy_):
    def __init__(self, bstack1l1llllll11_opy_):
        super().__init__()
        bstack1ll11l1111l_opy_.bstack1l1l1lll11l_opy_((bstack1ll1ll1l1l1_opy_.bstack1lll1111l11_opy_, bstack1lll111l1l1_opy_.PRE), self.bstack1l111l11l1l_opy_)
        bstack1ll11l1111l_opy_.bstack1l1l1lll11l_opy_((bstack1ll1ll1l1l1_opy_.bstack1lll1111l11_opy_, bstack1lll111l1l1_opy_.PRE), self.bstack1l111l111ll_opy_)
        bstack1ll11l1111l_opy_.bstack1l1l1lll11l_opy_((bstack1ll1ll1l1l1_opy_.bstack1lll111lll1_opy_, bstack1lll111l1l1_opy_.PRE), self.bstack1l1111l1ll1_opy_)
        bstack1ll11l1111l_opy_.bstack1l1l1lll11l_opy_((bstack1ll1ll1l1l1_opy_.bstack1ll1ll1l11l_opy_, bstack1lll111l1l1_opy_.PRE), self.bstack1l1111llll1_opy_)
        bstack1ll11l1111l_opy_.bstack1l1l1lll11l_opy_((bstack1ll1ll1l1l1_opy_.bstack1lll1111l11_opy_, bstack1lll111l1l1_opy_.PRE), self.bstack1l111l11lll_opy_)
        bstack1ll11l1111l_opy_.bstack1l1l1lll11l_opy_((bstack1ll1ll1l1l1_opy_.QUIT, bstack1lll111l1l1_opy_.PRE), self.on_close)
        self.bstack1l1llllll11_opy_ = bstack1l1llllll11_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l111l11l1l_opy_(
        self,
        f: bstack1ll11l1111l_opy_,
        bstack1l1111ll1l1_opy_: object,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll111_opy_ (u"ࠤ࡯ࡥࡺࡴࡣࡩࠤᒠ"):
            return
        if not bstack1l11l1111ll_opy_():
            self.logger.debug(bstack11ll111_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢ࡯ࡥࡺࡴࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᒡ"))
            return
        def wrapped(bstack1l1111ll1l1_opy_, launch, *args, **kwargs):
            response = self.bstack1l1111ll1ll_opy_(f.platform_index, instance.ref(), json.dumps({bstack11ll111_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᒢ"): True}).encode(bstack11ll111_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᒣ")))
            if response is not None and response.capabilities:
                if not bstack1l11l1111ll_opy_():
                    browser = launch(bstack1l1111ll1l1_opy_)
                    return browser
                bstack1l111l1111l_opy_ = json.loads(response.capabilities.decode(bstack11ll111_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᒤ")))
                if not bstack1l111l1111l_opy_: # empty caps bstack1l1111l1lll_opy_ bstack1l1111ll11l_opy_ bstack1l111l1l111_opy_ bstack1ll11lll1ll_opy_ or error in processing
                    return
                bstack1l1111lllll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l111l1111l_opy_))
                f.bstack1lll11l1111_opy_(instance, bstack1ll11l1111l_opy_.bstack1l111l11ll1_opy_, bstack1l1111lllll_opy_)
                f.bstack1lll11l1111_opy_(instance, bstack1ll11l1111l_opy_.bstack1l111l11111_opy_, bstack1l111l1111l_opy_)
                browser = bstack1l1111ll1l1_opy_.connect(bstack1l1111lllll_opy_)
                return browser
        return wrapped
    def bstack1l1111l1ll1_opy_(
        self,
        f: bstack1ll11l1111l_opy_,
        Connection: object,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll111_opy_ (u"ࠢࡥ࡫ࡶࡴࡦࡺࡣࡩࠤᒥ"):
            self.logger.debug(bstack11ll111_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡥ࡫ࡶࡴࡦࡺࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᒦ"))
            return
        if not bstack1l11l1111ll_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack11ll111_opy_ (u"ࠩࡳࡥࡷࡧ࡭ࡴࠩᒧ"), {}).get(bstack11ll111_opy_ (u"ࠪࡦࡸࡖࡡࡳࡣࡰࡷࠬᒨ")):
                    bstack1l1111ll111_opy_ = args[0][bstack11ll111_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦᒩ")][bstack11ll111_opy_ (u"ࠧࡨࡳࡑࡣࡵࡥࡲࡹࠢᒪ")]
                    session_id = bstack1l1111ll111_opy_.get(bstack11ll111_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴࡉࡥࠤᒫ"))
                    f.bstack1lll11l1111_opy_(instance, bstack1ll11l1111l_opy_.bstack1l111l111l1_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack11ll111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡤࡪࡵࡳࡥࡹࡩࡨࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠢࠥᒬ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l111l11lll_opy_(
        self,
        f: bstack1ll11l1111l_opy_,
        bstack1l1111ll1l1_opy_: object,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll111_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࠤᒭ"):
            return
        if not bstack1l11l1111ll_opy_():
            self.logger.debug(bstack11ll111_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡥࡲࡲࡳ࡫ࡣࡵࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᒮ"))
            return
        def wrapped(bstack1l1111ll1l1_opy_, connect, *args, **kwargs):
            response = self.bstack1l1111ll1ll_opy_(f.platform_index, instance.ref(), json.dumps({bstack11ll111_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᒯ"): True}).encode(bstack11ll111_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᒰ")))
            if response is not None and response.capabilities:
                bstack1l111l1111l_opy_ = json.loads(response.capabilities.decode(bstack11ll111_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᒱ")))
                if not bstack1l111l1111l_opy_:
                    return
                bstack1l1111lllll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l111l1111l_opy_))
                if bstack1l111l1111l_opy_.get(bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᒲ")):
                    browser = bstack1l1111ll1l1_opy_.bstack1l1111lll1l_opy_(bstack1l1111lllll_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1111lllll_opy_
                    return connect(bstack1l1111ll1l1_opy_, *args, **kwargs)
        return wrapped
    def bstack1l111l111ll_opy_(
        self,
        f: bstack1ll11l1111l_opy_,
        bstack1l11llllll1_opy_: object,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll111_opy_ (u"ࠢ࡯ࡧࡺࡣࡵࡧࡧࡦࠤᒳ"):
            return
        if not bstack1l11l1111ll_opy_():
            self.logger.debug(bstack11ll111_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠ࡯ࡧࡺࡣࡵࡧࡧࡦࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᒴ"))
            return
        def wrapped(bstack1l11llllll1_opy_, bstack1l111l11l11_opy_, *args, **kwargs):
            contexts = bstack1l11llllll1_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack11ll111_opy_ (u"ࠤࡤࡦࡴࡻࡴ࠻ࡤ࡯ࡥࡳࡱࠢᒵ") in page.url:
                                return page
                            else:
                                return bstack1l111l11l11_opy_(bstack1l11llllll1_opy_)
                    else:
                        return bstack1l111l11l11_opy_(bstack1l11llllll1_opy_)
        return wrapped
    def bstack1l1111ll1ll_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.client_worker_id = bstack11ll111_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᒶ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11ll111_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࠤᒷ") + str(req) + bstack11ll111_opy_ (u"ࠧࠨᒸ"))
        try:
            r = self.bstack1l1llllll1l_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11ll111_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࠤᒹ") + str(r.success) + bstack11ll111_opy_ (u"ࠢࠣᒺ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᒻ") + str(e) + bstack11ll111_opy_ (u"ࠤࠥᒼ"))
            traceback.print_exc()
            raise e
    def bstack1l1111llll1_opy_(
        self,
        f: bstack1ll11l1111l_opy_,
        Connection: object,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll111_opy_ (u"ࠥࡣࡸ࡫࡮ࡥࡡࡰࡩࡸࡹࡡࡨࡧࡢࡸࡴࡥࡳࡦࡴࡹࡩࡷࠨᒽ"):
            return
        if not bstack1l11l1111ll_opy_():
            return
        def wrapped(Connection, bstack1l1111lll11_opy_, *args, **kwargs):
            return bstack1l1111lll11_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1ll11l1111l_opy_,
        bstack1l1111ll1l1_opy_: object,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll111_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࠥᒾ"):
            return
        if not bstack1l11l1111ll_opy_():
            self.logger.debug(bstack11ll111_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡨࡲ࡯ࡴࡧࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᒿ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped