# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1lll11ll111_opy_ import bstack1ll1l1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1l1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1lllll111ll_opy_,
    bstack1llll1ll111_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1ll1lll1111_opy_ import bstack1lll1lll111_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1lll1ll1ll_opy_
from bstack_utils.helper import bstack1l1l1lll111_opy_
import threading
import os
import urllib.parse
class bstack1ll1l1l111l_opy_(bstack1ll1l1l11l1_opy_):
    def __init__(self, bstack1ll1ll1l1l1_opy_):
        super().__init__()
        bstack1lll1lll111_opy_.bstack1ll111l11ll_opy_((bstack1lllll1l111_opy_.bstack1llll1l1l11_opy_, bstack1lllll111ll_opy_.PRE), self.bstack1l1l11ll11l_opy_)
        bstack1lll1lll111_opy_.bstack1ll111l11ll_opy_((bstack1lllll1l111_opy_.bstack1llll1l1l11_opy_, bstack1lllll111ll_opy_.PRE), self.bstack1l1l11l111l_opy_)
        bstack1lll1lll111_opy_.bstack1ll111l11ll_opy_((bstack1lllll1l111_opy_.bstack1lllll1ll11_opy_, bstack1lllll111ll_opy_.PRE), self.bstack1l1l111ll11_opy_)
        bstack1lll1lll111_opy_.bstack1ll111l11ll_opy_((bstack1lllll1l111_opy_.bstack1llllllllll_opy_, bstack1lllll111ll_opy_.PRE), self.bstack1l1l111l11l_opy_)
        bstack1lll1lll111_opy_.bstack1ll111l11ll_opy_((bstack1lllll1l111_opy_.bstack1llll1l1l11_opy_, bstack1lllll111ll_opy_.PRE), self.bstack1l1l111l1ll_opy_)
        bstack1lll1lll111_opy_.bstack1ll111l11ll_opy_((bstack1lllll1l111_opy_.QUIT, bstack1lllll111ll_opy_.PRE), self.on_close)
        self.bstack1ll1ll1l1l1_opy_ = bstack1ll1ll1l1l1_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11ll11l_opy_(
        self,
        f: bstack1lll1lll111_opy_,
        bstack1l1l11ll1l1_opy_: object,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll11ll_opy_ (u"ࠤ࡯ࡥࡺࡴࡣࡩࠤድ"):
            return
        if not bstack1l1l1lll111_opy_():
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢ࡯ࡥࡺࡴࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢዶ"))
            return
        def wrapped(bstack1l1l11ll1l1_opy_, launch, *args, **kwargs):
            response = self.bstack1l1l11l1111_opy_(f.platform_index, instance.ref(), json.dumps({bstack1ll11ll_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪዷ"): True}).encode(bstack1ll11ll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦዸ")))
            if response is not None and response.capabilities:
                if not bstack1l1l1lll111_opy_():
                    browser = launch(bstack1l1l11ll1l1_opy_)
                    return browser
                bstack1l1l11l11ll_opy_ = json.loads(response.capabilities.decode(bstack1ll11ll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧዹ")))
                if not bstack1l1l11l11ll_opy_: # empty caps bstack1l1l111llll_opy_ bstack1l1l11l1l11_opy_ bstack1l1l11l1l1l_opy_ bstack1ll1l1llll1_opy_ or error in processing
                    return
                bstack1l1l111l1l1_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l11l11ll_opy_))
                f.bstack1llll1l1lll_opy_(instance, bstack1lll1lll111_opy_.bstack1l1l11l1ll1_opy_, bstack1l1l111l1l1_opy_)
                f.bstack1llll1l1lll_opy_(instance, bstack1lll1lll111_opy_.bstack1l1l11ll111_opy_, bstack1l1l11l11ll_opy_)
                browser = bstack1l1l11ll1l1_opy_.connect(bstack1l1l111l1l1_opy_)
                return browser
        return wrapped
    def bstack1l1l111ll11_opy_(
        self,
        f: bstack1lll1lll111_opy_,
        Connection: object,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll11ll_opy_ (u"ࠢࡥ࡫ࡶࡴࡦࡺࡣࡩࠤዺ"):
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡥ࡫ࡶࡴࡦࡺࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢዻ"))
            return
        if not bstack1l1l1lll111_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1ll11ll_opy_ (u"ࠩࡳࡥࡷࡧ࡭ࡴࠩዼ"), {}).get(bstack1ll11ll_opy_ (u"ࠪࡦࡸࡖࡡࡳࡣࡰࡷࠬዽ")):
                    bstack1l1l11l1lll_opy_ = args[0][bstack1ll11ll_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦዾ")][bstack1ll11ll_opy_ (u"ࠧࡨࡳࡑࡣࡵࡥࡲࡹࠢዿ")]
                    session_id = bstack1l1l11l1lll_opy_.get(bstack1ll11ll_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴࡉࡥࠤጀ"))
                    f.bstack1llll1l1lll_opy_(instance, bstack1lll1lll111_opy_.bstack1l1l111l111_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡤࡪࡵࡳࡥࡹࡩࡨࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠢࠥጁ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1l111l1ll_opy_(
        self,
        f: bstack1lll1lll111_opy_,
        bstack1l1l11ll1l1_opy_: object,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll11ll_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࠤጂ"):
            return
        if not bstack1l1l1lll111_opy_():
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡥࡲࡲࡳ࡫ࡣࡵࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢጃ"))
            return
        def wrapped(bstack1l1l11ll1l1_opy_, connect, *args, **kwargs):
            response = self.bstack1l1l11l1111_opy_(f.platform_index, instance.ref(), json.dumps({bstack1ll11ll_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩጄ"): True}).encode(bstack1ll11ll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥጅ")))
            if response is not None and response.capabilities:
                bstack1l1l11l11ll_opy_ = json.loads(response.capabilities.decode(bstack1ll11ll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦጆ")))
                if not bstack1l1l11l11ll_opy_:
                    return
                bstack1l1l111l1l1_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l11l11ll_opy_))
                if bstack1l1l11l11ll_opy_.get(bstack1ll11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬጇ")):
                    browser = bstack1l1l11ll1l1_opy_.bstack1l1l11l11l1_opy_(bstack1l1l111l1l1_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1l111l1l1_opy_
                    return connect(bstack1l1l11ll1l1_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1l11l111l_opy_(
        self,
        f: bstack1lll1lll111_opy_,
        bstack1l1lllll11l_opy_: object,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll11ll_opy_ (u"ࠢ࡯ࡧࡺࡣࡵࡧࡧࡦࠤገ"):
            return
        if not bstack1l1l1lll111_opy_():
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠ࡯ࡧࡺࡣࡵࡧࡧࡦࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢጉ"))
            return
        def wrapped(bstack1l1lllll11l_opy_, bstack1l1l111lll1_opy_, *args, **kwargs):
            contexts = bstack1l1lllll11l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack1ll11ll_opy_ (u"ࠤࡤࡦࡴࡻࡴ࠻ࡤ࡯ࡥࡳࡱࠢጊ") in page.url:
                                    return page
                    else:
                        return bstack1l1l111lll1_opy_(bstack1l1lllll11l_opy_)
        return wrapped
    def bstack1l1l11l1111_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣጋ") + str(req) + bstack1ll11ll_opy_ (u"ࠦࠧጌ"))
        try:
            r = self.bstack1ll1llllll1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣግ") + str(r.success) + bstack1ll11ll_opy_ (u"ࠨࠢጎ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧጏ") + str(e) + bstack1ll11ll_opy_ (u"ࠣࠤጐ"))
            traceback.print_exc()
            raise e
    def bstack1l1l111l11l_opy_(
        self,
        f: bstack1lll1lll111_opy_,
        Connection: object,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll11ll_opy_ (u"ࠤࡢࡷࡪࡴࡤࡠ࡯ࡨࡷࡸࡧࡧࡦࡡࡷࡳࡤࡹࡥࡳࡸࡨࡶࠧ጑"):
            return
        if not bstack1l1l1lll111_opy_():
            return
        def wrapped(Connection, bstack1l1l111ll1l_opy_, *args, **kwargs):
            return bstack1l1l111ll1l_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1lll1lll111_opy_,
        bstack1l1l11ll1l1_opy_: object,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll11ll_opy_ (u"ࠥࡧࡱࡵࡳࡦࠤጒ"):
            return
        if not bstack1l1l1lll111_opy_():
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡧࡱࡵࡳࡦࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢጓ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped