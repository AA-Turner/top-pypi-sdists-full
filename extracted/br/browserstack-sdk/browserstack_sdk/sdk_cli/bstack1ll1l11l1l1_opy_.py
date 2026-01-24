# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll111l111l_opy_ import bstack1ll1ll111l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11ll1l1_opy_ import (
    bstack1lll111lll1_opy_,
    bstack1lll1l1ll1l_opy_,
    bstack1lll1l1111l_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1ll11ll1ll1_opy_ import bstack1ll1ll11ll1_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l111lll11_opy_
from bstack_utils.helper import bstack1l1l1l111l1_opy_
import threading
import os
import urllib.parse
class bstack1ll1l11ll1l_opy_(bstack1ll1ll111l1_opy_):
    def __init__(self, bstack1ll1l1ll1ll_opy_):
        super().__init__()
        bstack1ll1ll11ll1_opy_.bstack1l1lll1ll11_opy_((bstack1lll111lll1_opy_.bstack1lll1l1l1l1_opy_, bstack1lll1l1ll1l_opy_.PRE), self.bstack1l111llllll_opy_)
        bstack1ll1ll11ll1_opy_.bstack1l1lll1ll11_opy_((bstack1lll111lll1_opy_.bstack1lll1l1l1l1_opy_, bstack1lll1l1ll1l_opy_.PRE), self.bstack1l11l111ll1_opy_)
        bstack1ll1ll11ll1_opy_.bstack1l1lll1ll11_opy_((bstack1lll111lll1_opy_.bstack1lll1l111ll_opy_, bstack1lll1l1ll1l_opy_.PRE), self.bstack1l11l11l111_opy_)
        bstack1ll1ll11ll1_opy_.bstack1l1lll1ll11_opy_((bstack1lll111lll1_opy_.bstack1lll11l11l1_opy_, bstack1lll1l1ll1l_opy_.PRE), self.bstack1l11l111111_opy_)
        bstack1ll1ll11ll1_opy_.bstack1l1lll1ll11_opy_((bstack1lll111lll1_opy_.bstack1lll1l1l1l1_opy_, bstack1lll1l1ll1l_opy_.PRE), self.bstack1l11l111l1l_opy_)
        bstack1ll1ll11ll1_opy_.bstack1l1lll1ll11_opy_((bstack1lll111lll1_opy_.QUIT, bstack1lll1l1ll1l_opy_.PRE), self.on_close)
        self.bstack1ll1l1ll1ll_opy_ = bstack1ll1l1ll1ll_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l111llllll_opy_(
        self,
        f: bstack1ll1ll11ll1_opy_,
        bstack1l11l11lll1_opy_: object,
        exec: Tuple[bstack1lll1l1111l_opy_, str],
        bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1111_opy_ (u"ࠤ࡯ࡥࡺࡴࡣࡩࠤᏪ"):
            return
        if not bstack1l1l1l111l1_opy_():
            self.logger.debug(bstack1l1111_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢ࡯ࡥࡺࡴࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᏫ"))
            return
        def wrapped(bstack1l11l11lll1_opy_, launch, *args, **kwargs):
            response = self.bstack1l11l1111l1_opy_(f.platform_index, instance.ref(), json.dumps({bstack1l1111_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᏬ"): True}).encode(bstack1l1111_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᏭ")))
            if response is not None and response.capabilities:
                if not bstack1l1l1l111l1_opy_():
                    browser = launch(bstack1l11l11lll1_opy_)
                    return browser
                bstack1l11l11l1l1_opy_ = json.loads(response.capabilities.decode(bstack1l1111_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᏮ")))
                if not bstack1l11l11l1l1_opy_: # empty caps bstack1l11l11111l_opy_ bstack1l11l11l1ll_opy_ bstack1l11l11ll1l_opy_ bstack1ll1l11lll1_opy_ or error in processing
                    return
                bstack1l11l11l11l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l11l11l1l1_opy_))
                f.bstack1lll11l1ll1_opy_(instance, bstack1ll1ll11ll1_opy_.bstack1l111lllll1_opy_, bstack1l11l11l11l_opy_)
                f.bstack1lll11l1ll1_opy_(instance, bstack1ll1ll11ll1_opy_.bstack1l11l111lll_opy_, bstack1l11l11l1l1_opy_)
                browser = bstack1l11l11lll1_opy_.connect(bstack1l11l11l11l_opy_)
                return browser
        return wrapped
    def bstack1l11l11l111_opy_(
        self,
        f: bstack1ll1ll11ll1_opy_,
        Connection: object,
        exec: Tuple[bstack1lll1l1111l_opy_, str],
        bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1111_opy_ (u"ࠢࡥ࡫ࡶࡴࡦࡺࡣࡩࠤᏯ"):
            self.logger.debug(bstack1l1111_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡥ࡫ࡶࡴࡦࡺࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᏰ"))
            return
        if not bstack1l1l1l111l1_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1l1111_opy_ (u"ࠩࡳࡥࡷࡧ࡭ࡴࠩᏱ"), {}).get(bstack1l1111_opy_ (u"ࠪࡦࡸࡖࡡࡳࡣࡰࡷࠬᏲ")):
                    bstack1l111llll11_opy_ = args[0][bstack1l1111_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦᏳ")][bstack1l1111_opy_ (u"ࠧࡨࡳࡑࡣࡵࡥࡲࡹࠢᏴ")]
                    session_id = bstack1l111llll11_opy_.get(bstack1l1111_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴࡉࡥࠤᏵ"))
                    f.bstack1lll11l1ll1_opy_(instance, bstack1ll1ll11ll1_opy_.bstack1l11l1111ll_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1l1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡤࡪࡵࡳࡥࡹࡩࡨࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠢࠥ᏶"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l11l111l1l_opy_(
        self,
        f: bstack1ll1ll11ll1_opy_,
        bstack1l11l11lll1_opy_: object,
        exec: Tuple[bstack1lll1l1111l_opy_, str],
        bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1111_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࠤ᏷"):
            return
        if not bstack1l1l1l111l1_opy_():
            self.logger.debug(bstack1l1111_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡥࡲࡲࡳ࡫ࡣࡵࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᏸ"))
            return
        def wrapped(bstack1l11l11lll1_opy_, connect, *args, **kwargs):
            response = self.bstack1l11l1111l1_opy_(f.platform_index, instance.ref(), json.dumps({bstack1l1111_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᏹ"): True}).encode(bstack1l1111_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᏺ")))
            if response is not None and response.capabilities:
                bstack1l11l11l1l1_opy_ = json.loads(response.capabilities.decode(bstack1l1111_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᏻ")))
                if not bstack1l11l11l1l1_opy_:
                    return
                bstack1l11l11l11l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l11l11l1l1_opy_))
                if bstack1l11l11l1l1_opy_.get(bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᏼ")):
                    browser = bstack1l11l11lll1_opy_.bstack1l11l11ll11_opy_(bstack1l11l11l11l_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l11l11l11l_opy_
                    return connect(bstack1l11l11lll1_opy_, *args, **kwargs)
        return wrapped
    def bstack1l11l111ll1_opy_(
        self,
        f: bstack1ll1ll11ll1_opy_,
        bstack1l1l1l1l111_opy_: object,
        exec: Tuple[bstack1lll1l1111l_opy_, str],
        bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1111_opy_ (u"ࠢ࡯ࡧࡺࡣࡵࡧࡧࡦࠤᏽ"):
            return
        if not bstack1l1l1l111l1_opy_():
            self.logger.debug(bstack1l1111_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠ࡯ࡧࡺࡣࡵࡧࡧࡦࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢ᏾"))
            return
        def wrapped(bstack1l1l1l1l111_opy_, bstack1l11l111l11_opy_, *args, **kwargs):
            contexts = bstack1l1l1l1l111_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l1111_opy_ (u"ࠤࡤࡦࡴࡻࡴ࠻ࡤ࡯ࡥࡳࡱࠢ᏿") in page.url:
                                return page
                            else:
                                return bstack1l11l111l11_opy_(bstack1l1l1l1l111_opy_)
                    else:
                        return bstack1l11l111l11_opy_(bstack1l1l1l1l111_opy_)
        return wrapped
    def bstack1l11l1111l1_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.client_worker_id = bstack1l1111_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤ᐀").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1l1111_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࠤᐁ") + str(req) + bstack1l1111_opy_ (u"ࠧࠨᐂ"))
        try:
            r = self.bstack1ll1111l1ll_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l1111_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࠤᐃ") + str(r.success) + bstack1l1111_opy_ (u"ࠢࠣᐄ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᐅ") + str(e) + bstack1l1111_opy_ (u"ࠤࠥᐆ"))
            traceback.print_exc()
            raise e
    def bstack1l11l111111_opy_(
        self,
        f: bstack1ll1ll11ll1_opy_,
        Connection: object,
        exec: Tuple[bstack1lll1l1111l_opy_, str],
        bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1111_opy_ (u"ࠥࡣࡸ࡫࡮ࡥࡡࡰࡩࡸࡹࡡࡨࡧࡢࡸࡴࡥࡳࡦࡴࡹࡩࡷࠨᐇ"):
            return
        if not bstack1l1l1l111l1_opy_():
            return
        def wrapped(Connection, bstack1l111llll1l_opy_, *args, **kwargs):
            return bstack1l111llll1l_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1ll1ll11ll1_opy_,
        bstack1l11l11lll1_opy_: object,
        exec: Tuple[bstack1lll1l1111l_opy_, str],
        bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1111_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࠥᐈ"):
            return
        if not bstack1l1l1l111l1_opy_():
            self.logger.debug(bstack1l1111_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡨࡲ࡯ࡴࡧࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᐉ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped