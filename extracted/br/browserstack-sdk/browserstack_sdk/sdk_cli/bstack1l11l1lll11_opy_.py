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
from browserstack_sdk.sdk_cli.bstack1l111llllll_opy_ import bstack1l11ll11111_opy_
from browserstack_sdk.sdk_cli.bstack11l1l1l11_opy_ import (
    bstack11111l1ll_opy_,
    bstack111llll1ll_opy_,
    bstack1l1lll111ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l11l111111_opy_ import bstack1l1l1ll11ll_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l111llllll_opy_ import bstack1l11ll11111_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1l11l1l11_opy_ import bstack1ll111lll_opy_
import traceback
import os
import threading
import time
class bstack1l1l11l1l1l_opy_(bstack1l11ll11111_opy_):
    bstack11llllllll1_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1l1l1ll11ll_opy_.bstack1l111l11l11_opy_((bstack11111l1ll_opy_.bstack1ll1111lll1_opy_, bstack111llll1ll_opy_.PRE), self.bstack11llll1ll1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11llll1ll1l_opy_(
        self,
        f: bstack1l1l1ll11ll_opy_,
        driver: object,
        exec: Tuple[bstack1l1lll111ll_opy_, str],
        bstack1l1ll1l11l1_opy_: Tuple[bstack11111l1ll_opy_, bstack111llll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack11llll1l1l1_opy_(hub_url):
            if not bstack1l1l11l1l1l_opy_.bstack11llllllll1_opy_:
                self.logger.warning(bstack11ll11_opy_ (u"ࠣ࡮ࡲࡧࡦࡲࠠࡴࡧ࡯ࡪ࠲࡮ࡥࡢ࡮ࠣࡪࡱࡵࡷࠡࡦ࡬ࡷࡦࡨ࡬ࡦࡦࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡩ࡯ࡨࡵࡥࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡩࡷࡥࡣࡺࡸ࡬࠾ࠤᚂ") + str(hub_url) + bstack11ll11_opy_ (u"ࠤࠥᚃ"))
                bstack1l1l11l1l1l_opy_.bstack11llllllll1_opy_ = True
            return
        command_name = f.bstack1l111ll11ll_opy_(*args)
        bstack11llll1l11l_opy_ = f.bstack11llll1lll1_opy_(*args)
        if command_name and command_name.lower() == bstack11ll11_opy_ (u"ࠥࡪ࡮ࡴࡤࡦ࡮ࡨࡱࡪࡴࡴࠣᚄ") and bstack11llll1l11l_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack11llll1l11l_opy_.get(bstack11ll11_opy_ (u"ࠦࡺࡹࡩ࡯ࡩࠥᚅ"), None), bstack11llll1l11l_opy_.get(bstack11ll11_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᚆ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack11ll11_opy_ (u"ࠨࡻࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࢃ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡲࡶࠥࡧࡲࡨࡵ࠱ࡹࡸ࡯࡮ࡨ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡳࡷࠦࡡࡳࡩࡶ࠲ࡻࡧ࡬ࡶࡧࡀࠦᚇ") + str(locator_value) + bstack11ll11_opy_ (u"ࠢࠣᚈ"))
                return
            def bstack1l1lll11111_opy_(driver, bstack11llll1l1ll_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack11llll1l1ll_opy_(driver, *args, **kwargs)
                    response = self.bstack11llll1l111_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack11ll11_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴ࠯ࡶࡧࡷ࡯ࡰࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࠦᚉ") + str(locator_value) + bstack11ll11_opy_ (u"ࠤࠥᚊ"))
                    else:
                        self.logger.warning(bstack11ll11_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶ࠱ࡳࡵ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣࡶࡪࡹࡰࡰࡰࡶࡩࡂࠨᚋ") + str(response) + bstack11ll11_opy_ (u"ࠦࠧᚌ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__11llll1llll_opy_(
                        driver, bstack11llll1l1ll_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1l1lll11111_opy_.__name__ = command_name
            return bstack1l1lll11111_opy_
    def __11llll1llll_opy_(
        self,
        driver,
        bstack11llll1l1ll_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack11llll1l111_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack11ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡵࡴ࡬࡫࡬࡫ࡲࡦࡦ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࠧᚍ") + str(locator_value) + bstack11ll11_opy_ (u"ࠨࠢᚎ"))
                bstack11lllll111l_opy_ = self.bstack11llll1ll11_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack11ll11_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡵࡩࡸࡻ࡬ࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࢁࠥ࡮ࡥࡢ࡮࡬ࡲ࡬ࡥࡲࡦࡵࡸࡰࡹࡃࠢᚏ") + str(bstack11lllll111l_opy_) + bstack11ll11_opy_ (u"ࠣࠤᚐ"))
                if bstack11lllll111l_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack11ll11_opy_ (u"ࠤࡸࡷ࡮ࡴࡧࠣᚑ"): bstack11lllll111l_opy_.locator_type,
                            bstack11ll11_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤᚒ"): bstack11lllll111l_opy_.locator_value,
                        }
                    )
                    return bstack11llll1l1ll_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack11ll11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡎࡥࡄࡆࡄࡘࡋࠧᚓ"), False):
                    self.logger.info(bstack1l1ll1lll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠭࡮࡫ࡶࡷ࡮ࡴࡧ࠻ࠢࡶࡰࡪ࡫ࡰࠩ࠵࠳࠭ࠥࡲࡥࡵࡶ࡬ࡲ࡬ࠦࡹࡰࡷࠣ࡭ࡳࡹࡰࡦࡥࡷࠤࡹ࡮ࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࠥࡲ࡯ࡨࡵࠥᚔ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack11ll11_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭࡯ࡱ࠰ࡷࡨࡸࡩࡱࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠾ࠤᚕ") + str(response) + bstack11ll11_opy_ (u"ࠢࠣᚖ"))
        except Exception as err:
            self.logger.warning(bstack11ll11_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡶࡪࡹࡵ࡭ࡶ࠽ࠤࡪࡸࡲࡰࡴ࠽ࠤࠧᚗ") + str(err) + bstack11ll11_opy_ (u"ࠤࠥᚘ"))
        raise exception
    @measure(event_name=EVENTS.bstack11lllll11l1_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def bstack11llll1l111_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack11ll11_opy_ (u"ࠥ࠴ࠧᚙ"),
    ):
        self.bstack1l11111l1l1_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack11ll11_opy_ (u"ࠦࠧᚚ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        req.client_worker_id = bstack11ll11_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦ᚛").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1l1l111l1_opy_.AISelfHealStep(req)
            self.logger.info(bstack11ll11_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣ᚜") + str(r) + bstack11ll11_opy_ (u"ࠢࠣ᚝"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨ᚞") + str(e) + bstack11ll11_opy_ (u"ࠤࠥ᚟"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11lllll1111_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def bstack11llll1ll11_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack11ll11_opy_ (u"ࠥ࠴ࠧᚠ")):
        self.bstack1l11111l1l1_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        req.client_worker_id = bstack11ll11_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᚡ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1l1l111l1_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack11ll11_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᚢ") + str(r) + bstack11ll11_opy_ (u"ࠨࠢᚣ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᚤ") + str(e) + bstack11ll11_opy_ (u"ࠣࠤᚥ"))
            traceback.print_exc()
            raise e