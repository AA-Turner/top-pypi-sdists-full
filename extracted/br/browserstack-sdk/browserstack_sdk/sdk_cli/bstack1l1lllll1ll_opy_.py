# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll11111111_opy_ import bstack1ll11l1ll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1ll1l_opy_ import (
    bstack1ll1l1l11ll_opy_,
    bstack1ll1llll111_opy_,
    bstack1ll1llll11l_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1lll111l11l_opy_ import bstack1lll111l1ll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1ll11l1l1_opy_
from bstack_utils.helper import bstack1l11ll1l1l1_opy_
import threading
import os
import urllib.parse
class bstack1ll1l111l11_opy_(bstack1ll11l1ll11_opy_):
    def __init__(self, bstack1ll11111ll1_opy_):
        super().__init__()
        bstack1lll111l1ll_opy_.bstack1l1l1lll1ll_opy_((bstack1ll1l1l11ll_opy_.bstack1ll1lllll11_opy_, bstack1ll1llll111_opy_.PRE), self.bstack1l11111llll_opy_)
        bstack1lll111l1ll_opy_.bstack1l1l1lll1ll_opy_((bstack1ll1l1l11ll_opy_.bstack1ll1lllll11_opy_, bstack1ll1llll111_opy_.PRE), self.bstack1l11111l1l1_opy_)
        bstack1lll111l1ll_opy_.bstack1l1l1lll1ll_opy_((bstack1ll1l1l11ll_opy_.bstack1ll1l1ll111_opy_, bstack1ll1llll111_opy_.PRE), self.bstack1l11111lll1_opy_)
        bstack1lll111l1ll_opy_.bstack1l1l1lll1ll_opy_((bstack1ll1l1l11ll_opy_.bstack1ll1lll11l1_opy_, bstack1ll1llll111_opy_.PRE), self.bstack1l1111111ll_opy_)
        bstack1lll111l1ll_opy_.bstack1l1l1lll1ll_opy_((bstack1ll1l1l11ll_opy_.bstack1ll1lllll11_opy_, bstack1ll1llll111_opy_.PRE), self.bstack1l1111l11l1_opy_)
        bstack1lll111l1ll_opy_.bstack1l1l1lll1ll_opy_((bstack1ll1l1l11ll_opy_.QUIT, bstack1ll1llll111_opy_.PRE), self.on_close)
        self.bstack1ll11111ll1_opy_ = bstack1ll11111ll1_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l11111llll_opy_(
        self,
        f: bstack1lll111l1ll_opy_,
        bstack1l111111l1l_opy_: object,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1lll1l_opy_ (u"ࠦࡱࡧࡵ࡯ࡥ࡫ࠦᔮ"):
            return
        if not bstack1l11ll1l1l1_opy_():
            self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡱࡧࡵ࡯ࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᔯ"))
            return
        def wrapped(bstack1l111111l1l_opy_, launch, *args, **kwargs):
            response = self.bstack1l11111ll11_opy_(f.platform_index, instance.ref(), json.dumps({bstack1lll1l_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᔰ"): True}).encode(bstack1lll1l_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᔱ")))
            if response is not None and response.capabilities:
                if not bstack1l11ll1l1l1_opy_():
                    browser = launch(bstack1l111111l1l_opy_)
                    return browser
                bstack1lll11l1ll1_opy_ = json.loads(response.capabilities.decode(bstack1lll1l_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᔲ")))
                if not bstack1lll11l1ll1_opy_: # empty caps bstack1l111111ll1_opy_ bstack1l11111ll1l_opy_ bstack1l1111l1111_opy_ bstack1l11111l1ll_opy_ or error in processing
                    return
                bstack1l111111l11_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1lll11l1ll1_opy_))
                f.bstack1lll1l11lll_opy_(instance, bstack1lll111l1ll_opy_.bstack1lll1l11ll1_opy_, bstack1l111111l11_opy_)
                f.bstack1lll1l11lll_opy_(instance, bstack1lll111l1ll_opy_.bstack1lll11ll1l1_opy_, bstack1lll11l1ll1_opy_)
                browser = bstack1l111111l1l_opy_.connect(bstack1l111111l11_opy_)
                return browser
        return wrapped
    def bstack1l11111lll1_opy_(
        self,
        f: bstack1lll111l1ll_opy_,
        Connection: object,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1lll1l_opy_ (u"ࠤࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠦᔳ"):
            self.logger.debug(bstack1lll1l_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᔴ"))
            return
        if not bstack1l11ll1l1l1_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1lll1l_opy_ (u"ࠫࡵࡧࡲࡢ࡯ࡶࠫᔵ"), {}).get(bstack1lll1l_opy_ (u"ࠬࡨࡳࡑࡣࡵࡥࡲࡹࠧᔶ")):
                    bstack1l11111l11l_opy_ = args[0][bstack1lll1l_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨᔷ")][bstack1lll1l_opy_ (u"ࠢࡣࡵࡓࡥࡷࡧ࡭ࡴࠤᔸ")]
                    session_id = bstack1l11111l11l_opy_.get(bstack1lll1l_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡋࡧࠦᔹ"))
                    f.bstack1lll1l11lll_opy_(instance, bstack1lll111l1ll_opy_.bstack1lll1111ll1_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡦ࡬ࡷࡵࡧࡴࡤࡪࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࠧᔺ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1111l11l1_opy_(
        self,
        f: bstack1lll111l1ll_opy_,
        bstack1l111111l1l_opy_: object,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1lll1l_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦᔻ"):
            return
        if not bstack1l11ll1l1l1_opy_():
            self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡧࡴࡴ࡮ࡦࡥࡷࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᔼ"))
            return
        def wrapped(bstack1l111111l1l_opy_, connect, *args, **kwargs):
            response = self.bstack1l11111ll11_opy_(f.platform_index, instance.ref(), json.dumps({bstack1lll1l_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᔽ"): True}).encode(bstack1lll1l_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᔾ")))
            if response is not None and response.capabilities:
                bstack1lll11l1ll1_opy_ = json.loads(response.capabilities.decode(bstack1lll1l_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᔿ")))
                if not bstack1lll11l1ll1_opy_:
                    return
                bstack1l111111l11_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1lll11l1ll1_opy_))
                if bstack1lll11l1ll1_opy_.get(bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᕀ")):
                    browser = bstack1l111111l1l_opy_.bstack1l1111l111l_opy_(bstack1l111111l11_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l111111l11_opy_
                    return connect(bstack1l111111l1l_opy_, *args, **kwargs)
        return wrapped
    def bstack1l11111l1l1_opy_(
        self,
        f: bstack1lll111l1ll_opy_,
        bstack1l11ll1ll11_opy_: object,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1lll1l_opy_ (u"ࠤࡱࡩࡼࡥࡰࡢࡩࡨࠦᕁ"):
            return
        if not bstack1l11ll1l1l1_opy_():
            self.logger.debug(bstack1lll1l_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡱࡩࡼࡥࡰࡢࡩࡨࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᕂ"))
            return
        def wrapped(bstack1l11ll1ll11_opy_, bstack1l11111l111_opy_, *args, **kwargs):
            contexts = bstack1l11ll1ll11_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1lll1l_opy_ (u"ࠦࡦࡨ࡯ࡶࡶ࠽ࡦࡱࡧ࡮࡬ࠤᕃ") in page.url:
                                return page
                            else:
                                return bstack1l11111l111_opy_(bstack1l11ll1ll11_opy_)
                    else:
                        return bstack1l11111l111_opy_(bstack1l11ll1ll11_opy_)
        return wrapped
    def bstack1l11111ll11_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.client_worker_id = bstack1lll1l_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᕄ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1lll1l_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡹࡨࡦࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦᕅ") + str(req) + bstack1lll1l_opy_ (u"ࠢࠣᕆ"))
        try:
            r = self.bstack1lll111lll1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦᕇ") + str(r.success) + bstack1lll1l_opy_ (u"ࠤࠥᕈ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1lll1l_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᕉ") + str(e) + bstack1lll1l_opy_ (u"ࠦࠧᕊ"))
            traceback.print_exc()
            raise e
    def bstack1l1111111ll_opy_(
        self,
        f: bstack1lll111l1ll_opy_,
        Connection: object,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1lll1l_opy_ (u"ࠧࡥࡳࡦࡰࡧࡣࡲ࡫ࡳࡴࡣࡪࡩࡤࡺ࡯ࡠࡵࡨࡶࡻ࡫ࡲࠣᕋ"):
            return
        if not bstack1l11ll1l1l1_opy_():
            return
        def wrapped(Connection, bstack1l111111lll_opy_, *args, **kwargs):
            return bstack1l111111lll_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1lll111l1ll_opy_,
        bstack1l111111l1l_opy_: object,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1lll1l_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧᕌ"):
            return
        if not bstack1l11ll1l1l1_opy_():
            self.logger.debug(bstack1lll1l_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦࡣ࡭ࡱࡶࡩࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥᕍ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped