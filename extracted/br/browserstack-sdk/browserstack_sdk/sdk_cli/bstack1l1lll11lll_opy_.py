# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
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
from browserstack_sdk.sdk_cli.bstack1ll11l11l1l_opy_ import bstack1ll111l1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11lllll_opy_ import (
    bstack1ll1lll1ll1_opy_,
    bstack1ll1l1lll1l_opy_,
    bstack1ll1ll1l111_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1lll111l1l1_opy_ import bstack1lll11l11ll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack111111lll_opy_
from bstack_utils.helper import bstack1l111l1ll1l_opy_
import threading
import os
import urllib.parse
class bstack1ll111ll1ll_opy_(bstack1ll111l1l1l_opy_):
    def __init__(self, bstack1ll11l1lll1_opy_):
        super().__init__()
        bstack1lll11l11ll_opy_.bstack1l1ll1111ll_opy_((bstack1ll1lll1ll1_opy_.bstack1ll1l1l1111_opy_, bstack1ll1l1lll1l_opy_.PRE), self.bstack1l1111111l1_opy_)
        bstack1lll11l11ll_opy_.bstack1l1ll1111ll_opy_((bstack1ll1lll1ll1_opy_.bstack1ll1l1l1111_opy_, bstack1ll1l1lll1l_opy_.PRE), self.bstack1l111111ll1_opy_)
        bstack1lll11l11ll_opy_.bstack1l1ll1111ll_opy_((bstack1ll1lll1ll1_opy_.bstack1ll1ll1l11l_opy_, bstack1ll1l1lll1l_opy_.PRE), self.bstack1l11111l1l1_opy_)
        bstack1lll11l11ll_opy_.bstack1l1ll1111ll_opy_((bstack1ll1lll1ll1_opy_.bstack1ll1ll1l1l1_opy_, bstack1ll1l1lll1l_opy_.PRE), self.bstack1l1111l1111_opy_)
        bstack1lll11l11ll_opy_.bstack1l1ll1111ll_opy_((bstack1ll1lll1ll1_opy_.bstack1ll1l1l1111_opy_, bstack1ll1l1lll1l_opy_.PRE), self.bstack1l11111l11l_opy_)
        bstack1lll11l11ll_opy_.bstack1l1ll1111ll_opy_((bstack1ll1lll1ll1_opy_.QUIT, bstack1ll1l1lll1l_opy_.PRE), self.on_close)
        self.bstack1ll11l1lll1_opy_ = bstack1ll11l1lll1_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1111111l1_opy_(
        self,
        f: bstack1lll11l11ll_opy_,
        bstack1l11111ll1l_opy_: object,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1111_opy_ (u"ࠧࡲࡡࡶࡰࡦ࡬ࠧᔯ"):
            return
        if not bstack1l111l1ll1l_opy_():
            self.logger.debug(bstack1111_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡲࡡࡶࡰࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥᔰ"))
            return
        def wrapped(bstack1l11111ll1l_opy_, launch, *args, **kwargs):
            response = self.bstack1l111111l11_opy_(f.platform_index, instance.ref(), json.dumps({bstack1111_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᔱ"): True}).encode(bstack1111_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᔲ")))
            if response is not None and response.capabilities:
                if not bstack1l111l1ll1l_opy_():
                    browser = launch(bstack1l11111ll1l_opy_)
                    return browser
                bstack1lll1111ll1_opy_ = json.loads(response.capabilities.decode(bstack1111_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᔳ")))
                if not bstack1lll1111ll1_opy_: # empty caps bstack1l11111l1ll_opy_ bstack1l11111ll11_opy_ bstack1l11111111l_opy_ bstack1l11111llll_opy_ or error in processing
                    return
                bstack1l1111111ll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1lll1111ll1_opy_))
                f.bstack1lll1l11l1l_opy_(instance, bstack1lll11l11ll_opy_.bstack1lll11lll1l_opy_, bstack1l1111111ll_opy_)
                f.bstack1lll1l11l1l_opy_(instance, bstack1lll11l11ll_opy_.bstack1lll1111l11_opy_, bstack1lll1111ll1_opy_)
                browser = bstack1l11111ll1l_opy_.connect(bstack1l1111111ll_opy_)
                return browser
        return wrapped
    def bstack1l11111l1l1_opy_(
        self,
        f: bstack1lll11l11ll_opy_,
        Connection: object,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1111_opy_ (u"ࠥࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠧᔴ"):
            self.logger.debug(bstack1111_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥᔵ"))
            return
        if not bstack1l111l1ll1l_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1111_opy_ (u"ࠬࡶࡡࡳࡣࡰࡷࠬᔶ"), {}).get(bstack1111_opy_ (u"࠭ࡢࡴࡒࡤࡶࡦࡳࡳࠨᔷ")):
                    bstack1l11111l111_opy_ = args[0][bstack1111_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢᔸ")][bstack1111_opy_ (u"ࠣࡤࡶࡔࡦࡸࡡ࡮ࡵࠥᔹ")]
                    session_id = bstack1l11111l111_opy_.get(bstack1111_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡌࡨࠧᔺ"))
                    f.bstack1lll1l11l1l_opy_(instance, bstack1lll11l11ll_opy_.bstack1lll1l1l1l1_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࠨᔻ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l11111l11l_opy_(
        self,
        f: bstack1lll11l11ll_opy_,
        bstack1l11111ll1l_opy_: object,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1111_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࠧᔼ"):
            return
        if not bstack1l111l1ll1l_opy_():
            self.logger.debug(bstack1111_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡨࡵ࡮࡯ࡧࡦࡸࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥᔽ"))
            return
        def wrapped(bstack1l11111ll1l_opy_, connect, *args, **kwargs):
            response = self.bstack1l111111l11_opy_(f.platform_index, instance.ref(), json.dumps({bstack1111_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᔾ"): True}).encode(bstack1111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᔿ")))
            if response is not None and response.capabilities:
                bstack1lll1111ll1_opy_ = json.loads(response.capabilities.decode(bstack1111_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᕀ")))
                if not bstack1lll1111ll1_opy_:
                    return
                bstack1l1111111ll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1lll1111ll1_opy_))
                if bstack1lll1111ll1_opy_.get(bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᕁ")):
                    browser = bstack1l11111ll1l_opy_.bstack1l11111lll1_opy_(bstack1l1111111ll_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1111111ll_opy_
                    return connect(bstack1l11111ll1l_opy_, *args, **kwargs)
        return wrapped
    def bstack1l111111ll1_opy_(
        self,
        f: bstack1lll11l11ll_opy_,
        bstack1l11ll1l1ll_opy_: object,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1111_opy_ (u"ࠥࡲࡪࡽ࡟ࡱࡣࡪࡩࠧᕂ"):
            return
        if not bstack1l111l1ll1l_opy_():
            self.logger.debug(bstack1111_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡲࡪࡽ࡟ࡱࡣࡪࡩࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥᕃ"))
            return
        def wrapped(bstack1l11ll1l1ll_opy_, bstack1l111111l1l_opy_, *args, **kwargs):
            contexts = bstack1l11ll1l1ll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1111_opy_ (u"ࠧࡧࡢࡰࡷࡷ࠾ࡧࡲࡡ࡯࡭ࠥᕄ") in page.url:
                                return page
                            else:
                                return bstack1l111111l1l_opy_(bstack1l11ll1l1ll_opy_)
                    else:
                        return bstack1l111111l1l_opy_(bstack1l11ll1l1ll_opy_)
        return wrapped
    def bstack1l111111l11_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.client_worker_id = bstack1111_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᕅ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1111_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡺࡩࡧࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧᕆ") + str(req) + bstack1111_opy_ (u"ࠣࠤᕇ"))
        try:
            r = self.bstack1lll111l111_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1111_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧᕈ") + str(r.success) + bstack1111_opy_ (u"ࠥࠦᕉ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᕊ") + str(e) + bstack1111_opy_ (u"ࠧࠨᕋ"))
            traceback.print_exc()
            raise e
    def bstack1l1111l1111_opy_(
        self,
        f: bstack1lll11l11ll_opy_,
        Connection: object,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1111_opy_ (u"ࠨ࡟ࡴࡧࡱࡨࡤࡳࡥࡴࡵࡤ࡫ࡪࡥࡴࡰࡡࡶࡩࡷࡼࡥࡳࠤᕌ"):
            return
        if not bstack1l111l1ll1l_opy_():
            return
        def wrapped(Connection, bstack1l111111lll_opy_, *args, **kwargs):
            return bstack1l111111lll_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1lll11l11ll_opy_,
        bstack1l11111ll1l_opy_: object,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1111_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨᕍ"):
            return
        if not bstack1l111l1ll1l_opy_():
            self.logger.debug(bstack1111_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡤ࡮ࡲࡷࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦᕎ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped