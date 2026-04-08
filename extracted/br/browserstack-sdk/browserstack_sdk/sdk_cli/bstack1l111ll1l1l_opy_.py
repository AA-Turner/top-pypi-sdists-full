# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1l11l1l1l11_opy_ import bstack1l111111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111111_opy_ import (
    bstack11l1ll1l1_opy_,
    bstack1lll1l11l1_opy_,
    bstack1l1l111l1l1_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1ll111ll_opy_ import bstack11ll1lllll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack111lllllll_opy_
from bstack_utils.helper import bstack1ll1ll111_opy_
import threading
import os
import urllib.parse
class bstack1l11l111lll_opy_(bstack1l111111l1l_opy_):
    @staticmethod
    def bstack11l1l111ll1_opy_(bstack1lllll1ll11_opy_: dict) -> bool:
        browser_name = (
            bstack1lllll1ll11_opy_.get(bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ៳"))
            or bstack1lllll1ll11_opy_.get(bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ៴"))
            or bstack1lllll1ll11_opy_.get(bstack111l_opy_ (u"ࠨࡦࡨࡪࡦࡻ࡬ࡵࡄࡵࡳࡼࡹࡥࡳࡖࡼࡴࡪ࠭៵"))
            or bstack111l_opy_ (u"ࠩࠪ៶")
        ).lower()
        return browser_name in bstack1l11111lll_opy_
    def __init__(self, bstack1l11ll1ll1l_opy_):
        super().__init__()
        bstack11ll1lllll_opy_.bstack11llll1l1l1_opy_((bstack11l1ll1l1_opy_.bstack11llll111l_opy_, bstack1lll1l11l1_opy_.PRE), self.bstack11l1l1l111l_opy_)
        bstack11ll1lllll_opy_.bstack11llll1l1l1_opy_((bstack11l1ll1l1_opy_.bstack11llll111l_opy_, bstack1lll1l11l1_opy_.PRE), self.bstack11l1l11l1ll_opy_)
        bstack11ll1lllll_opy_.bstack11llll1l1l1_opy_((bstack11l1ll1l1_opy_.bstack1l11lll1ll1_opy_, bstack1lll1l11l1_opy_.PRE), self.bstack11l1l1l11ll_opy_)
        bstack11ll1lllll_opy_.bstack11llll1l1l1_opy_((bstack11l1ll1l1_opy_.bstack1ll1111l1l1_opy_, bstack1lll1l11l1_opy_.PRE), self.bstack11l1l11l111_opy_)
        bstack11ll1lllll_opy_.bstack11llll1l1l1_opy_((bstack11l1ll1l1_opy_.bstack11llll111l_opy_, bstack1lll1l11l1_opy_.PRE), self.bstack11l1l111lll_opy_)
        bstack11ll1lllll_opy_.bstack11llll1l1l1_opy_((bstack11l1ll1l1_opy_.QUIT, bstack1lll1l11l1_opy_.PRE), self.on_close)
        self.bstack1l11ll1ll1l_opy_ = bstack1l11ll1ll1l_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack11l1l1l111l_opy_(
        self,
        f: bstack11ll1lllll_opy_,
        bstack11l1l1l11l1_opy_: object,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111l_opy_ (u"ࠥࡰࡦࡻ࡮ࡤࡪࠥ៷"):
            return
        if not bstack1ll1ll111_opy_():
            self.logger.debug(bstack111l_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡰࡦࡻ࡮ࡤࡪࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣ៸"))
            return
        def wrapped(bstack11l1l1l11l1_opy_, launch, *args, **kwargs):
            response = self.bstack11l1l11ll1l_opy_(f.platform_index, instance.ref(), json.dumps({bstack111l_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ៹"): True}).encode(bstack111l_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧ៺")))
            if response is not None and response.capabilities:
                if not bstack1ll1ll111_opy_():
                    browser = launch(bstack11l1l1l11l1_opy_)
                    return browser
                bstack1lllll1ll11_opy_ = json.loads(response.capabilities.decode(bstack111l_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨ៻")))
                if not bstack1lllll1ll11_opy_: # empty caps bstack11l1l111l1l_opy_ bstack11l1l11l1l1_opy_ bstack11l1l1111ll_opy_ bstack11l1l111l11_opy_ or error in processing
                    return
                bstack11l1l11lll1_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1lllll1ll11_opy_))
                f.bstack1l11l1ll11_opy_(instance, bstack11ll1lllll_opy_.bstack11l1ll111l_opy_, bstack11l1l11lll1_opy_)
                f.bstack1l11l1ll11_opy_(instance, bstack11ll1lllll_opy_.bstack1111lll1_opy_, bstack1lllll1ll11_opy_)
                browser = bstack11l1l1l11l1_opy_.connect(bstack11l1l11lll1_opy_)
                return browser
        return wrapped
    def bstack11l1l1l11ll_opy_(
        self,
        f: bstack11ll1lllll_opy_,
        Connection: object,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111l_opy_ (u"ࠣࡦ࡬ࡷࡵࡧࡴࡤࡪࠥ៼"):
            self.logger.debug(bstack111l_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡦ࡬ࡷࡵࡧࡴࡤࡪࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣ៽"))
            return
        if not bstack1ll1ll111_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack111l_opy_ (u"ࠪࡴࡦࡸࡡ࡮ࡵࠪ៾"), {}).get(bstack111l_opy_ (u"ࠫࡧࡹࡐࡢࡴࡤࡱࡸ࠭៿")):
                    bstack11l1l1l1111_opy_ = args[0][bstack111l_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧ᠀")][bstack111l_opy_ (u"ࠨࡢࡴࡒࡤࡶࡦࡳࡳࠣ᠁")]
                    session_id = bstack11l1l1l1111_opy_.get(bstack111l_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡊࡦࠥ᠂"))
                    f.bstack1l11l1ll11_opy_(instance, bstack11ll1lllll_opy_.bstack1ll11111111_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack111l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡥ࡫ࡶࡴࡦࡺࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠣࠦ᠃"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack11l1l111lll_opy_(
        self,
        f: bstack11ll1lllll_opy_,
        bstack11l1l1l11l1_opy_: object,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111l_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࠥ᠄"):
            return
        if not bstack1ll1ll111_opy_():
            self.logger.debug(bstack111l_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡦࡳࡳࡴࡥࡤࡶࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣ᠅"))
            return
        def wrapped(bstack11l1l1l11l1_opy_, connect, *args, **kwargs):
            response = self.bstack11l1l11ll1l_opy_(f.platform_index, instance.ref(), json.dumps({bstack111l_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ᠆"): True}).encode(bstack111l_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦ᠇")))
            if response is not None and response.capabilities:
                bstack1lllll1ll11_opy_ = json.loads(response.capabilities.decode(bstack111l_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧ᠈")))
                if not bstack1lllll1ll11_opy_:
                    return
                if bstack1lllll1ll11_opy_.get(bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᠉")) and not self.bstack11l1l111ll1_opy_(bstack1lllll1ll11_opy_):
                    bstack1lllll1ll11_opy_[bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ᠊")] = False
                    bstack11l1l1111l1_opy_ = [bstack11l1l11l11l_opy_ for bstack11l1l11l11l_opy_ in bstack1lllll1ll11_opy_ if bstack11l1l11l11l_opy_.startswith(bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ᠋"))]
                    for bstack11l1l11l11l_opy_ in bstack11l1l1111l1_opy_:
                        del bstack1lllll1ll11_opy_[bstack11l1l11l11l_opy_]
                bstack11l1l11lll1_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1lllll1ll11_opy_))
                if bstack1lllll1ll11_opy_.get(bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᠌")):
                    browser = bstack11l1l1l11l1_opy_.connect_over_cdp(bstack11l1l11lll1_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack11l1l11lll1_opy_
                    return connect(bstack11l1l1l11l1_opy_, *args, **kwargs)
        return wrapped
    def bstack11l1l11l1ll_opy_(
        self,
        f: bstack11ll1lllll_opy_,
        bstack11ll11lllll_opy_: object,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111l_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨ᠍"):
            return
        if not bstack1ll1ll111_opy_():
            self.logger.debug(bstack111l_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦ᠎"))
            return
        def wrapped(bstack11ll11lllll_opy_, bstack11l1l11llll_opy_, *args, **kwargs):
            contexts = bstack11ll11lllll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack111l_opy_ (u"ࠨࡡࡣࡱࡸࡸ࠿ࡨ࡬ࡢࡰ࡮ࠦ᠏") in page.url:
                                return page
                            else:
                                return bstack11l1l11llll_opy_(bstack11ll11lllll_opy_)
                    else:
                        return bstack11l1l11llll_opy_(bstack11ll11lllll_opy_)
        return wrapped
    def bstack11l1l11ll1l_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.client_worker_id = bstack111l_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨ᠐").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack111l_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡻࡪࡨࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷ࠾ࠥࠨ᠑") + str(req) + bstack111l_opy_ (u"ࠤࠥ᠒"))
        try:
            r = self.bstack11l11lll11_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack111l_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࡸࡻࡣࡤࡧࡶࡷࡂࠨ᠓") + str(r.success) + bstack111l_opy_ (u"ࠦࠧ᠔"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111l_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥ᠕") + str(e) + bstack111l_opy_ (u"ࠨࠢ᠖"))
            traceback.print_exc()
            raise e
    def bstack11l1l11l111_opy_(
        self,
        f: bstack11ll1lllll_opy_,
        Connection: object,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111l_opy_ (u"ࠢࡠࡵࡨࡲࡩࡥ࡭ࡦࡵࡶࡥ࡬࡫࡟ࡵࡱࡢࡷࡪࡸࡶࡦࡴࠥ᠗"):
            return
        if not bstack1ll1ll111_opy_():
            return
        def wrapped(Connection, bstack11l1l11ll11_opy_, *args, **kwargs):
            return bstack11l1l11ll11_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack11ll1lllll_opy_,
        bstack11l1l1l11l1_opy_: object,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111l_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࠢ᠘"):
            return
        if not bstack1ll1ll111_opy_():
            self.logger.debug(bstack111l_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡥ࡯ࡳࡸ࡫ࠠ࡮ࡧࡷ࡬ࡴࡪࠬࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧ᠙"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped