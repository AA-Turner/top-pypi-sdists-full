# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1l1l1l1ll1l_opy_ import bstack1l11llll11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l111_opy_ import (
    bstack11l111l1l_opy_,
    bstack1111111ll_opy_,
    bstack1l1ll1ll111_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1ll1111ll_opy_ import bstack111ll11111_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11l11ll11_opy_
from bstack_utils.helper import bstack1l111llll1_opy_
import threading
import os
import urllib.parse
class bstack1l11ll1llll_opy_(bstack1l11llll11l_opy_):
    @staticmethod
    def bstack11l1lll11ll_opy_(bstack111l11ll1l_opy_: dict) -> bool:
        browser_name = (
            bstack111l11ll1l_opy_.get(bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ᝻"))
            or bstack111l11ll1l_opy_.get(bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ᝼"))
            or bstack111l11ll1l_opy_.get(bstack111ll11_opy_ (u"ࠧࡥࡧࡩࡥࡺࡲࡴࡃࡴࡲࡻࡸ࡫ࡲࡕࡻࡳࡩࠬ᝽"))
            or bstack111ll11_opy_ (u"ࠨࠩ᝾")
        ).lower()
        return browser_name in bstack11l1l11ll1_opy_
    def __init__(self, bstack1l11l1l111l_opy_):
        super().__init__()
        bstack111ll11111_opy_.bstack1l1111111ll_opy_((bstack11l111l1l_opy_.bstack1ll1l11ll1_opy_, bstack1111111ll_opy_.PRE), self.bstack11l1lll1lll_opy_)
        bstack111ll11111_opy_.bstack1l1111111ll_opy_((bstack11l111l1l_opy_.bstack1ll1l11ll1_opy_, bstack1111111ll_opy_.PRE), self.bstack11l1llll1l1_opy_)
        bstack111ll11111_opy_.bstack1l1111111ll_opy_((bstack11l111l1l_opy_.bstack1l1l1llll11_opy_, bstack1111111ll_opy_.PRE), self.bstack11l1ll1ll11_opy_)
        bstack111ll11111_opy_.bstack1l1111111ll_opy_((bstack11l111l1l_opy_.bstack1ll1111lll1_opy_, bstack1111111ll_opy_.PRE), self.bstack11l1ll1llll_opy_)
        bstack111ll11111_opy_.bstack1l1111111ll_opy_((bstack11l111l1l_opy_.bstack1ll1l11ll1_opy_, bstack1111111ll_opy_.PRE), self.bstack11l1ll1ll1l_opy_)
        bstack111ll11111_opy_.bstack1l1111111ll_opy_((bstack11l111l1l_opy_.QUIT, bstack1111111ll_opy_.PRE), self.on_close)
        self.bstack1l11l1l111l_opy_ = bstack1l11l1l111l_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack11l1lll1lll_opy_(
        self,
        f: bstack111ll11111_opy_,
        bstack11l1llll1ll_opy_: object,
        exec: Tuple[bstack1l1ll1ll111_opy_, str],
        bstack1l1ll11l11l_opy_: Tuple[bstack11l111l1l_opy_, bstack1111111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111ll11_opy_ (u"ࠤ࡯ࡥࡺࡴࡣࡩࠤ᝿"):
            return
        if not bstack1l111llll1_opy_():
            self.logger.debug(bstack111ll11_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢ࡯ࡥࡺࡴࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢក"))
            return
        def wrapped(bstack11l1llll1ll_opy_, launch, *args, **kwargs):
            response = self.bstack11l1lll1l11_opy_(f.platform_index, instance.ref(), json.dumps({bstack111ll11_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪខ"): True}).encode(bstack111ll11_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦគ")))
            if response is not None and response.capabilities:
                if not bstack1l111llll1_opy_():
                    browser = launch(bstack11l1llll1ll_opy_)
                    return browser
                bstack111l11ll1l_opy_ = json.loads(response.capabilities.decode(bstack111ll11_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧឃ")))
                if not bstack111l11ll1l_opy_: # empty caps bstack11l1ll1l1ll_opy_ bstack11l1lll111l_opy_ bstack11l1lllll11_opy_ bstack11l1llll11l_opy_ or error in processing
                    return
                bstack11l1lll1111_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack111l11ll1l_opy_))
                f.bstack11l1ll11ll_opy_(instance, bstack111ll11111_opy_.bstack111llll1ll_opy_, bstack11l1lll1111_opy_)
                f.bstack11l1ll11ll_opy_(instance, bstack111ll11111_opy_.bstack1lllll1l1l_opy_, bstack111l11ll1l_opy_)
                browser = bstack11l1llll1ll_opy_.connect(bstack11l1lll1111_opy_)
                return browser
        return wrapped
    def bstack11l1ll1ll11_opy_(
        self,
        f: bstack111ll11111_opy_,
        Connection: object,
        exec: Tuple[bstack1l1ll1ll111_opy_, str],
        bstack1l1ll11l11l_opy_: Tuple[bstack11l111l1l_opy_, bstack1111111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111ll11_opy_ (u"ࠢࡥ࡫ࡶࡴࡦࡺࡣࡩࠤង"):
            self.logger.debug(bstack111ll11_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡥ࡫ࡶࡴࡦࡺࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢច"))
            return
        if not bstack1l111llll1_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack111ll11_opy_ (u"ࠩࡳࡥࡷࡧ࡭ࡴࠩឆ"), {}).get(bstack111ll11_opy_ (u"ࠪࡦࡸࡖࡡࡳࡣࡰࡷࠬជ")):
                    bstack11l1lll11l1_opy_ = args[0][bstack111ll11_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦឈ")][bstack111ll11_opy_ (u"ࠧࡨࡳࡑࡣࡵࡥࡲࡹࠢញ")]
                    session_id = bstack11l1lll11l1_opy_.get(bstack111ll11_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴࡉࡥࠤដ"))
                    f.bstack11l1ll11ll_opy_(instance, bstack111ll11111_opy_.bstack1ll11111lll_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack111ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡤࡪࡵࡳࡥࡹࡩࡨࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠢࠥឋ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack11l1ll1ll1l_opy_(
        self,
        f: bstack111ll11111_opy_,
        bstack11l1llll1ll_opy_: object,
        exec: Tuple[bstack1l1ll1ll111_opy_, str],
        bstack1l1ll11l11l_opy_: Tuple[bstack11l111l1l_opy_, bstack1111111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111ll11_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࠤឌ"):
            return
        if not bstack1l111llll1_opy_():
            self.logger.debug(bstack111ll11_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡥࡲࡲࡳ࡫ࡣࡵࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢឍ"))
            return
        def wrapped(bstack11l1llll1ll_opy_, connect, *args, **kwargs):
            response = self.bstack11l1lll1l11_opy_(f.platform_index, instance.ref(), json.dumps({bstack111ll11_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩណ"): True}).encode(bstack111ll11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥត")))
            if response is not None and response.capabilities:
                bstack111l11ll1l_opy_ = json.loads(response.capabilities.decode(bstack111ll11_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦថ")))
                if not bstack111l11ll1l_opy_:
                    return
                if bstack111l11ll1l_opy_.get(bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬទ")) and not self.bstack11l1lll11ll_opy_(bstack111l11ll1l_opy_):
                    bstack111l11ll1l_opy_[bstack111ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ធ")] = False
                    bstack11l1ll1lll1_opy_ = [bstack11l1lll1l1l_opy_ for bstack11l1lll1l1l_opy_ in bstack111l11ll1l_opy_ if bstack11l1lll1l1l_opy_.startswith(bstack111ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧន"))]
                    for bstack11l1lll1l1l_opy_ in bstack11l1ll1lll1_opy_:
                        del bstack111l11ll1l_opy_[bstack11l1lll1l1l_opy_]
                bstack11l1lll1111_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack111l11ll1l_opy_))
                if bstack111l11ll1l_opy_.get(bstack111ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨប")):
                    browser = bstack11l1llll1ll_opy_.connect_over_cdp(bstack11l1lll1111_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack11l1lll1111_opy_
                    return connect(bstack11l1llll1ll_opy_, *args, **kwargs)
        return wrapped
    def bstack11l1llll1l1_opy_(
        self,
        f: bstack111ll11111_opy_,
        bstack11llll111l1_opy_: object,
        exec: Tuple[bstack1l1ll1ll111_opy_, str],
        bstack1l1ll11l11l_opy_: Tuple[bstack11l111l1l_opy_, bstack1111111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111ll11_opy_ (u"ࠥࡲࡪࡽ࡟ࡱࡣࡪࡩࠧផ"):
            return
        if not bstack1l111llll1_opy_():
            self.logger.debug(bstack111ll11_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡲࡪࡽ࡟ࡱࡣࡪࡩࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥព"))
            return
        def wrapped(bstack11llll111l1_opy_, bstack11l1llll111_opy_, *args, **kwargs):
            contexts = bstack11llll111l1_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack111ll11_opy_ (u"ࠧࡧࡢࡰࡷࡷ࠾ࡧࡲࡡ࡯࡭ࠥភ") in page.url:
                                return page
                            else:
                                return bstack11l1llll111_opy_(bstack11llll111l1_opy_)
                    else:
                        return bstack11l1llll111_opy_(bstack11llll111l1_opy_)
        return wrapped
    def bstack11l1lll1l11_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.client_worker_id = bstack111ll11_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧម").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack111ll11_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡺࡩࡧࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧយ") + str(req) + bstack111ll11_opy_ (u"ࠣࠤរ"))
        try:
            r = self.bstack1l1l1l1l1l_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack111ll11_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧល") + str(r.success) + bstack111ll11_opy_ (u"ࠥࠦវ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111ll11_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤឝ") + str(e) + bstack111ll11_opy_ (u"ࠧࠨឞ"))
            traceback.print_exc()
            raise e
    def bstack11l1ll1llll_opy_(
        self,
        f: bstack111ll11111_opy_,
        Connection: object,
        exec: Tuple[bstack1l1ll1ll111_opy_, str],
        bstack1l1ll11l11l_opy_: Tuple[bstack11l111l1l_opy_, bstack1111111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111ll11_opy_ (u"ࠨ࡟ࡴࡧࡱࡨࡤࡳࡥࡴࡵࡤ࡫ࡪࡥࡴࡰࡡࡶࡩࡷࡼࡥࡳࠤស"):
            return
        if not bstack1l111llll1_opy_():
            return
        def wrapped(Connection, bstack11l1lll1ll1_opy_, *args, **kwargs):
            return bstack11l1lll1ll1_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack111ll11111_opy_,
        bstack11l1llll1ll_opy_: object,
        exec: Tuple[bstack1l1ll1ll111_opy_, str],
        bstack1l1ll11l11l_opy_: Tuple[bstack11l111l1l_opy_, bstack1111111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111ll11_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨហ"):
            return
        if not bstack1l111llll1_opy_():
            self.logger.debug(bstack111ll11_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡤ࡮ࡲࡷࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦឡ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped