# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1lll1lll1l1_opy_ import bstack1lll1l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1ll11_opy_ import (
    bstack1lll1l1ll1l_opy_,
    bstack1lll1ll11ll_opy_,
    bstack1lll1l1l11l_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1lll1l111l1_opy_ import bstack1lll1lll11l_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l1l1111ll_opy_
from bstack_utils.helper import bstack1l11llll111_opy_
import threading
import os
import urllib.parse
class bstack1ll1ll11lll_opy_(bstack1lll1l1l1l1_opy_):
    def __init__(self, bstack1ll1lll11l1_opy_):
        super().__init__()
        bstack1lll1lll11l_opy_.bstack1lll1l1l1ll_opy_((bstack1lll1l1ll1l_opy_.bstack1lll1llllll_opy_, bstack1lll1ll11ll_opy_.PRE), self.bstack1l11l111l11_opy_)
        bstack1lll1lll11l_opy_.bstack1lll1l1l1ll_opy_((bstack1lll1l1ll1l_opy_.bstack1lll1llllll_opy_, bstack1lll1ll11ll_opy_.PRE), self.bstack1l11l111lll_opy_)
        bstack1lll1lll11l_opy_.bstack1lll1l1l1ll_opy_((bstack1lll1l1ll1l_opy_.bstack1ll1llllll1_opy_, bstack1lll1ll11ll_opy_.PRE), self.bstack1l11l1111l1_opy_)
        bstack1lll1lll11l_opy_.bstack1lll1l1l1ll_opy_((bstack1lll1l1ll1l_opy_.bstack1lll1ll111l_opy_, bstack1lll1ll11ll_opy_.PRE), self.bstack1l11l11l1l1_opy_)
        bstack1lll1lll11l_opy_.bstack1lll1l1l1ll_opy_((bstack1lll1l1ll1l_opy_.bstack1lll1llllll_opy_, bstack1lll1ll11ll_opy_.PRE), self.bstack1l11l111ll1_opy_)
        bstack1lll1lll11l_opy_.bstack1lll1l1l1ll_opy_((bstack1lll1l1ll1l_opy_.QUIT, bstack1lll1ll11ll_opy_.PRE), self.on_close)
        self.bstack1ll1lll11l1_opy_ = bstack1ll1lll11l1_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l111l11_opy_(
        self,
        f: bstack1lll1lll11l_opy_,
        bstack1l111lll1ll_opy_: object,
        exec: Tuple[bstack1lll1l1l11l_opy_, str],
        bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11lllll_opy_ (u"ࠥࡰࡦࡻ࡮ࡤࡪࠥ᐀"):
            return
        if not bstack1l11llll111_opy_():
            self.logger.debug(bstack11lllll_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡰࡦࡻ࡮ࡤࡪࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᐁ"))
            return
        def wrapped(bstack1l111lll1ll_opy_, launch, *args, **kwargs):
            response = self.bstack1l11l11l11l_opy_(f.platform_index, instance.ref(), json.dumps({bstack11lllll_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᐂ"): True}).encode(bstack11lllll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᐃ")))
            if response is not None and response.capabilities:
                if not bstack1l11llll111_opy_():
                    browser = launch(bstack1l111lll1ll_opy_)
                    return browser
                bstack1l111llll1l_opy_ = json.loads(response.capabilities.decode(bstack11lllll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᐄ")))
                if not bstack1l111llll1l_opy_: # empty caps bstack1l11l111111_opy_ bstack1l111lllll1_opy_ bstack1l111lll1l1_opy_ bstack1ll11l111ll_opy_ or error in processing
                    return
                bstack1l111lll11l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l111llll1l_opy_))
                f.bstack1lll1ll1lll_opy_(instance, bstack1lll1lll11l_opy_.bstack1l111lll111_opy_, bstack1l111lll11l_opy_)
                f.bstack1lll1ll1lll_opy_(instance, bstack1lll1lll11l_opy_.bstack1l11l1111ll_opy_, bstack1l111llll1l_opy_)
                browser = bstack1l111lll1ll_opy_.connect(bstack1l111lll11l_opy_)
                return browser
        return wrapped
    def bstack1l11l1111l1_opy_(
        self,
        f: bstack1lll1lll11l_opy_,
        Connection: object,
        exec: Tuple[bstack1lll1l1l11l_opy_, str],
        bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11lllll_opy_ (u"ࠣࡦ࡬ࡷࡵࡧࡴࡤࡪࠥᐅ"):
            self.logger.debug(bstack11lllll_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡦ࡬ࡷࡵࡧࡴࡤࡪࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᐆ"))
            return
        if not bstack1l11llll111_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack11lllll_opy_ (u"ࠪࡴࡦࡸࡡ࡮ࡵࠪᐇ"), {}).get(bstack11lllll_opy_ (u"ࠫࡧࡹࡐࡢࡴࡤࡱࡸ࠭ᐈ")):
                    bstack1l11l111l1l_opy_ = args[0][bstack11lllll_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧᐉ")][bstack11lllll_opy_ (u"ࠨࡢࡴࡒࡤࡶࡦࡳࡳࠣᐊ")]
                    session_id = bstack1l11l111l1l_opy_.get(bstack11lllll_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡊࡦࠥᐋ"))
                    f.bstack1lll1ll1lll_opy_(instance, bstack1lll1lll11l_opy_.bstack1l111llll11_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack11lllll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡥ࡫ࡶࡴࡦࡺࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠣࠦᐌ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l11l111ll1_opy_(
        self,
        f: bstack1lll1lll11l_opy_,
        bstack1l111lll1ll_opy_: object,
        exec: Tuple[bstack1lll1l1l11l_opy_, str],
        bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11lllll_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࠥᐍ"):
            return
        if not bstack1l11llll111_opy_():
            self.logger.debug(bstack11lllll_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡦࡳࡳࡴࡥࡤࡶࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᐎ"))
            return
        def wrapped(bstack1l111lll1ll_opy_, connect, *args, **kwargs):
            response = self.bstack1l11l11l11l_opy_(f.platform_index, instance.ref(), json.dumps({bstack11lllll_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᐏ"): True}).encode(bstack11lllll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᐐ")))
            if response is not None and response.capabilities:
                bstack1l111llll1l_opy_ = json.loads(response.capabilities.decode(bstack11lllll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᐑ")))
                if not bstack1l111llll1l_opy_:
                    return
                bstack1l111lll11l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l111llll1l_opy_))
                if bstack1l111llll1l_opy_.get(bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᐒ")):
                    browser = bstack1l111lll1ll_opy_.bstack1l11l11111l_opy_(bstack1l111lll11l_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l111lll11l_opy_
                    return connect(bstack1l111lll1ll_opy_, *args, **kwargs)
        return wrapped
    def bstack1l11l111lll_opy_(
        self,
        f: bstack1lll1lll11l_opy_,
        bstack1lll11lll1l_opy_: object,
        exec: Tuple[bstack1lll1l1l11l_opy_, str],
        bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11lllll_opy_ (u"ࠣࡰࡨࡻࡤࡶࡡࡨࡧࠥᐓ"):
            return
        if not bstack1l11llll111_opy_():
            self.logger.debug(bstack11lllll_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡰࡨࡻࡤࡶࡡࡨࡧࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᐔ"))
            return
        def wrapped(bstack1lll11lll1l_opy_, bstack1l11l11l111_opy_, *args, **kwargs):
            contexts = bstack1lll11lll1l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack11lllll_opy_ (u"ࠥࡥࡧࡵࡵࡵ࠼ࡥࡰࡦࡴ࡫ࠣᐕ") in page.url:
                                return page
                            else:
                                return bstack1l11l11l111_opy_(bstack1lll11lll1l_opy_)
                    else:
                        return bstack1l11l11l111_opy_(bstack1lll11lll1l_opy_)
        return wrapped
    def bstack1l11l11l11l_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.client_worker_id = bstack11lllll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᐖ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11lllll_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴ࠻ࠢࠥᐗ") + str(req) + bstack11lllll_opy_ (u"ࠨࠢᐘ"))
        try:
            r = self.bstack1ll1l1l1ll1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11lllll_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࡵࡸࡧࡨ࡫ࡳࡴ࠿ࠥᐙ") + str(r.success) + bstack11lllll_opy_ (u"ࠣࠤᐚ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᐛ") + str(e) + bstack11lllll_opy_ (u"ࠥࠦᐜ"))
            traceback.print_exc()
            raise e
    def bstack1l11l11l1l1_opy_(
        self,
        f: bstack1lll1lll11l_opy_,
        Connection: object,
        exec: Tuple[bstack1lll1l1l11l_opy_, str],
        bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11lllll_opy_ (u"ࠦࡤࡹࡥ࡯ࡦࡢࡱࡪࡹࡳࡢࡩࡨࡣࡹࡵ࡟ࡴࡧࡵࡺࡪࡸࠢᐝ"):
            return
        if not bstack1l11llll111_opy_():
            return
        def wrapped(Connection, bstack1l111llllll_opy_, *args, **kwargs):
            return bstack1l111llllll_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1lll1lll11l_opy_,
        bstack1l111lll1ll_opy_: object,
        exec: Tuple[bstack1lll1l1l11l_opy_, str],
        bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11lllll_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࠦᐞ"):
            return
        if not bstack1l11llll111_opy_():
            self.logger.debug(bstack11lllll_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡩ࡬ࡰࡵࡨࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᐟ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped