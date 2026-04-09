# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1l111llllll_opy_ import bstack1l11ll11111_opy_
from browserstack_sdk.sdk_cli.bstack11l1l1l11_opy_ import (
    bstack11111l1ll_opy_,
    bstack111llll1ll_opy_,
    bstack1l1lll111ll_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1l11111ll1_opy_ import bstack1111l11l1l_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11l111l11_opy_
from bstack_utils.helper import bstack1l1ll1ll1l_opy_
import threading
import os
import urllib.parse
class bstack1l1l11ll111_opy_(bstack1l11ll11111_opy_):
    @staticmethod
    def bstack11ll11111l1_opy_(bstack1111l1ll_opy_: dict) -> bool:
        browser_name = (
            bstack1111l1ll_opy_.get(bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ᝟"))
            or bstack1111l1ll_opy_.get(bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧᝠ"))
            or bstack1111l1ll_opy_.get(bstack11ll11_opy_ (u"ࠧࡥࡧࡩࡥࡺࡲࡴࡃࡴࡲࡻࡸ࡫ࡲࡕࡻࡳࡩࠬᝡ"))
            or bstack11ll11_opy_ (u"ࠨࠩᝢ")
        ).lower()
        return browser_name in bstack111llll11l_opy_
    def __init__(self, bstack1l11lll1l11_opy_):
        super().__init__()
        bstack1111l11l1l_opy_.bstack1l111l11l11_opy_((bstack11111l1ll_opy_.bstack1ll11lll1_opy_, bstack111llll1ll_opy_.PRE), self.bstack11ll11111ll_opy_)
        bstack1111l11l1l_opy_.bstack1l111l11l11_opy_((bstack11111l1ll_opy_.bstack1ll11lll1_opy_, bstack111llll1ll_opy_.PRE), self.bstack11l1lll1l1l_opy_)
        bstack1111l11l1l_opy_.bstack1l111l11l11_opy_((bstack11111l1ll_opy_.bstack1l1ll111l1l_opy_, bstack111llll1ll_opy_.PRE), self.bstack11l1lllll1l_opy_)
        bstack1111l11l1l_opy_.bstack1l111l11l11_opy_((bstack11111l1ll_opy_.bstack1ll1111lll1_opy_, bstack111llll1ll_opy_.PRE), self.bstack11l1lll11l1_opy_)
        bstack1111l11l1l_opy_.bstack1l111l11l11_opy_((bstack11111l1ll_opy_.bstack1ll11lll1_opy_, bstack111llll1ll_opy_.PRE), self.bstack11l1lll1ll1_opy_)
        bstack1111l11l1l_opy_.bstack1l111l11l11_opy_((bstack11111l1ll_opy_.QUIT, bstack111llll1ll_opy_.PRE), self.on_close)
        self.bstack1l11lll1l11_opy_ = bstack1l11lll1l11_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack11ll11111ll_opy_(
        self,
        f: bstack1111l11l1l_opy_,
        bstack11l1llll11l_opy_: object,
        exec: Tuple[bstack1l1lll111ll_opy_, str],
        bstack1l1ll1l11l1_opy_: Tuple[bstack11111l1ll_opy_, bstack111llll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll11_opy_ (u"ࠤ࡯ࡥࡺࡴࡣࡩࠤᝣ"):
            return
        if not bstack1l1ll1ll1l_opy_():
            self.logger.debug(bstack11ll11_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢ࡯ࡥࡺࡴࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᝤ"))
            return
        def wrapped(bstack11l1llll11l_opy_, launch, *args, **kwargs):
            response = self.bstack11l1llll1l1_opy_(f.platform_index, instance.ref(), json.dumps({bstack11ll11_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᝥ"): True}).encode(bstack11ll11_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᝦ")))
            if response is not None and response.capabilities:
                if not bstack1l1ll1ll1l_opy_():
                    browser = launch(bstack11l1llll11l_opy_)
                    return browser
                bstack1111l1ll_opy_ = json.loads(response.capabilities.decode(bstack11ll11_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᝧ")))
                if not bstack1111l1ll_opy_: # empty caps bstack11l1llll111_opy_ bstack11l1lll1lll_opy_ bstack11l1lllll11_opy_ bstack11l1llllll1_opy_ or error in processing
                    return
                bstack11l1lllllll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1111l1ll_opy_))
                f.bstack1l1l1111l1_opy_(instance, bstack1111l11l1l_opy_.bstack1111l1l11_opy_, bstack11l1lllllll_opy_)
                f.bstack1l1l1111l1_opy_(instance, bstack1111l11l1l_opy_.bstack11ll1l111l_opy_, bstack1111l1ll_opy_)
                browser = bstack11l1llll11l_opy_.connect(bstack11l1lllllll_opy_)
                return browser
        return wrapped
    def bstack11l1lllll1l_opy_(
        self,
        f: bstack1111l11l1l_opy_,
        Connection: object,
        exec: Tuple[bstack1l1lll111ll_opy_, str],
        bstack1l1ll1l11l1_opy_: Tuple[bstack11111l1ll_opy_, bstack111llll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll11_opy_ (u"ࠢࡥ࡫ࡶࡴࡦࡺࡣࡩࠤᝨ"):
            self.logger.debug(bstack11ll11_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡥ࡫ࡶࡴࡦࡺࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᝩ"))
            return
        if not bstack1l1ll1ll1l_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack11ll11_opy_ (u"ࠩࡳࡥࡷࡧ࡭ࡴࠩᝪ"), {}).get(bstack11ll11_opy_ (u"ࠪࡦࡸࡖࡡࡳࡣࡰࡷࠬᝫ")):
                    bstack11ll111111l_opy_ = args[0][bstack11ll11_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦᝬ")][bstack11ll11_opy_ (u"ࠧࡨࡳࡑࡣࡵࡥࡲࡹࠢ᝭")]
                    session_id = bstack11ll111111l_opy_.get(bstack11ll11_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴࡉࡥࠤᝮ"))
                    f.bstack1l1l1111l1_opy_(instance, bstack1111l11l1l_opy_.bstack1ll111l11l1_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack11ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡤࡪࡵࡳࡥࡹࡩࡨࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠢࠥᝯ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack11l1lll1ll1_opy_(
        self,
        f: bstack1111l11l1l_opy_,
        bstack11l1llll11l_opy_: object,
        exec: Tuple[bstack1l1lll111ll_opy_, str],
        bstack1l1ll1l11l1_opy_: Tuple[bstack11111l1ll_opy_, bstack111llll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll11_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࠤᝰ"):
            return
        if not bstack1l1ll1ll1l_opy_():
            self.logger.debug(bstack11ll11_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡥࡲࡲࡳ࡫ࡣࡵࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢ᝱"))
            return
        def wrapped(bstack11l1llll11l_opy_, connect, *args, **kwargs):
            response = self.bstack11l1llll1l1_opy_(f.platform_index, instance.ref(), json.dumps({bstack11ll11_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᝲ"): True}).encode(bstack11ll11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᝳ")))
            if response is not None and response.capabilities:
                bstack1111l1ll_opy_ = json.loads(response.capabilities.decode(bstack11ll11_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦ᝴")))
                if not bstack1111l1ll_opy_:
                    return
                if bstack1111l1ll_opy_.get(bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᝵")) and not self.bstack11ll11111l1_opy_(bstack1111l1ll_opy_):
                    bstack1111l1ll_opy_[bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᝶")] = False
                    bstack11ll1111111_opy_ = [bstack11l1lll11ll_opy_ for bstack11l1lll11ll_opy_ in bstack1111l1ll_opy_ if bstack11l1lll11ll_opy_.startswith(bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ᝷"))]
                    for bstack11l1lll11ll_opy_ in bstack11ll1111111_opy_:
                        del bstack1111l1ll_opy_[bstack11l1lll11ll_opy_]
                bstack11l1lllllll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1111l1ll_opy_))
                if bstack1111l1ll_opy_.get(bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᝸")):
                    browser = bstack11l1llll11l_opy_.connect_over_cdp(bstack11l1lllllll_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack11l1lllllll_opy_
                    return connect(bstack11l1llll11l_opy_, *args, **kwargs)
        return wrapped
    def bstack11l1lll1l1l_opy_(
        self,
        f: bstack1111l11l1l_opy_,
        bstack11llll11lll_opy_: object,
        exec: Tuple[bstack1l1lll111ll_opy_, str],
        bstack1l1ll1l11l1_opy_: Tuple[bstack11111l1ll_opy_, bstack111llll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll11_opy_ (u"ࠥࡲࡪࡽ࡟ࡱࡣࡪࡩࠧ᝹"):
            return
        if not bstack1l1ll1ll1l_opy_():
            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡲࡪࡽ࡟ࡱࡣࡪࡩࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥ᝺"))
            return
        def wrapped(bstack11llll11lll_opy_, bstack11l1llll1ll_opy_, *args, **kwargs):
            contexts = bstack11llll11lll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack11ll11_opy_ (u"ࠧࡧࡢࡰࡷࡷ࠾ࡧࡲࡡ࡯࡭ࠥ᝻") in page.url:
                                return page
                            else:
                                return bstack11l1llll1ll_opy_(bstack11llll11lll_opy_)
                    else:
                        return bstack11l1llll1ll_opy_(bstack11llll11lll_opy_)
        return wrapped
    def bstack11l1llll1l1_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.client_worker_id = bstack11ll11_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧ᝼").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11ll11_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡺࡩࡧࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧ᝽") + str(req) + bstack11ll11_opy_ (u"ࠣࠤ᝾"))
        try:
            r = self.bstack1l1l111l1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11ll11_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧ᝿") + str(r.success) + bstack11ll11_opy_ (u"ࠥࠦក"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤខ") + str(e) + bstack11ll11_opy_ (u"ࠧࠨគ"))
            traceback.print_exc()
            raise e
    def bstack11l1lll11l1_opy_(
        self,
        f: bstack1111l11l1l_opy_,
        Connection: object,
        exec: Tuple[bstack1l1lll111ll_opy_, str],
        bstack1l1ll1l11l1_opy_: Tuple[bstack11111l1ll_opy_, bstack111llll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll11_opy_ (u"ࠨ࡟ࡴࡧࡱࡨࡤࡳࡥࡴࡵࡤ࡫ࡪࡥࡴࡰࡡࡶࡩࡷࡼࡥࡳࠤឃ"):
            return
        if not bstack1l1ll1ll1l_opy_():
            return
        def wrapped(Connection, bstack11l1lll1l11_opy_, *args, **kwargs):
            return bstack11l1lll1l11_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1111l11l1l_opy_,
        bstack11l1llll11l_opy_: object,
        exec: Tuple[bstack1l1lll111ll_opy_, str],
        bstack1l1ll1l11l1_opy_: Tuple[bstack11111l1ll_opy_, bstack111llll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll11_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨង"):
            return
        if not bstack1l1ll1ll1l_opy_():
            self.logger.debug(bstack11ll11_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡤ࡮ࡲࡷࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦច"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped