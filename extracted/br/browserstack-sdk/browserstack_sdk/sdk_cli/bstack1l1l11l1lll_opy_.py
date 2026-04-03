# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
from browserstack_sdk.sdk_cli.bstack1l1l1ll111l_opy_ import bstack1l11lll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1ll1ll_opy_ import (
    bstack1l1111l1l1_opy_,
    bstack1ll111111l_opy_,
    bstack1l1ll1111l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l11l11ll11_opy_ import bstack1l1l111l1ll_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1l1ll111l_opy_ import bstack1l11lll1l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1111llll1l_opy_ import bstack11l1111l1l_opy_
import traceback
import os
import threading
import time
class bstack1l11l111l1l_opy_(bstack1l11lll1l1l_opy_):
    bstack1l111l11111_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1l1l111l1ll_opy_.bstack1l1111ll11l_opy_((bstack1l1111l1l1_opy_.bstack1l1llllll11_opy_, bstack1ll111111l_opy_.PRE), self.bstack11lllll1111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11lllll1111_opy_(
        self,
        f: bstack1l1l111l1ll_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll1111l1_opy_, str],
        bstack1l1ll1ll1ll_opy_: Tuple[bstack1l1111l1l1_opy_, bstack1ll111111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack11llll1l1ll_opy_(hub_url):
            if not bstack1l11l111l1l_opy_.bstack1l111l11111_opy_:
                self.logger.warning(bstack1ll1l11_opy_ (u"ࠣ࡮ࡲࡧࡦࡲࠠࡴࡧ࡯ࡪ࠲࡮ࡥࡢ࡮ࠣࡪࡱࡵࡷࠡࡦ࡬ࡷࡦࡨ࡬ࡦࡦࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡩ࡯ࡨࡵࡥࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡩࡷࡥࡣࡺࡸ࡬࠾ࠤᚂ") + str(hub_url) + bstack1ll1l11_opy_ (u"ࠤࠥᚃ"))
                bstack1l11l111l1l_opy_.bstack1l111l11111_opy_ = True
            return
        command_name = f.bstack1l111l1ll1l_opy_(*args)
        bstack11llll1l111_opy_ = f.bstack11llll1llll_opy_(*args)
        if command_name and command_name.lower() == bstack1ll1l11_opy_ (u"ࠥࡪ࡮ࡴࡤࡦ࡮ࡨࡱࡪࡴࡴࠣᚄ") and bstack11llll1l111_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack11llll1l111_opy_.get(bstack1ll1l11_opy_ (u"ࠦࡺࡹࡩ࡯ࡩࠥᚅ"), None), bstack11llll1l111_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᚆ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1ll1l11_opy_ (u"ࠨࡻࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࢃ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡲࡶࠥࡧࡲࡨࡵ࠱ࡹࡸ࡯࡮ࡨ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡳࡷࠦࡡࡳࡩࡶ࠲ࡻࡧ࡬ࡶࡧࡀࠦᚇ") + str(locator_value) + bstack1ll1l11_opy_ (u"ࠢࠣᚈ"))
                return
            def bstack1l1ll1llll1_opy_(driver, bstack11llll1ll1l_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack11llll1ll1l_opy_(driver, *args, **kwargs)
                    response = self.bstack11lllll11l1_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1ll1l11_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴ࠯ࡶࡧࡷ࡯ࡰࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࠦᚉ") + str(locator_value) + bstack1ll1l11_opy_ (u"ࠤࠥᚊ"))
                    else:
                        self.logger.warning(bstack1ll1l11_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶ࠱ࡳࡵ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣࡶࡪࡹࡰࡰࡰࡶࡩࡂࠨᚋ") + str(response) + bstack1ll1l11_opy_ (u"ࠦࠧᚌ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__11lllll111l_opy_(
                        driver, bstack11llll1ll1l_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1l1ll1llll1_opy_.__name__ = command_name
            return bstack1l1ll1llll1_opy_
    def __11lllll111l_opy_(
        self,
        driver,
        bstack11llll1ll1l_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack11lllll11l1_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1ll1l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡵࡴ࡬࡫࡬࡫ࡲࡦࡦ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࠧᚍ") + str(locator_value) + bstack1ll1l11_opy_ (u"ࠨࠢᚎ"))
                bstack11llll1lll1_opy_ = self.bstack11llll1ll11_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1ll1l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡵࡩࡸࡻ࡬ࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࢁࠥ࡮ࡥࡢ࡮࡬ࡲ࡬ࡥࡲࡦࡵࡸࡰࡹࡃࠢᚏ") + str(bstack11llll1lll1_opy_) + bstack1ll1l11_opy_ (u"ࠣࠤᚐ"))
                if bstack11llll1lll1_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1ll1l11_opy_ (u"ࠤࡸࡷ࡮ࡴࡧࠣᚑ"): bstack11llll1lll1_opy_.locator_type,
                            bstack1ll1l11_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤᚒ"): bstack11llll1lll1_opy_.locator_value,
                        }
                    )
                    return bstack11llll1ll1l_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1ll1l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡎࡥࡄࡆࡄࡘࡋࠧᚓ"), False):
                    self.logger.info(bstack1l1ll1ll11l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠭࡮࡫ࡶࡷ࡮ࡴࡧ࠻ࠢࡶࡰࡪ࡫ࡰࠩ࠵࠳࠭ࠥࡲࡥࡵࡶ࡬ࡲ࡬ࠦࡹࡰࡷࠣ࡭ࡳࡹࡰࡦࡥࡷࠤࡹ࡮ࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࠥࡲ࡯ࡨࡵࠥᚔ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1ll1l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭࡯ࡱ࠰ࡷࡨࡸࡩࡱࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠾ࠤᚕ") + str(response) + bstack1ll1l11_opy_ (u"ࠢࠣᚖ"))
        except Exception as err:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡶࡪࡹࡵ࡭ࡶ࠽ࠤࡪࡸࡲࡰࡴ࠽ࠤࠧᚗ") + str(err) + bstack1ll1l11_opy_ (u"ࠤࠥᚘ"))
        raise exception
    @measure(event_name=EVENTS.bstack11llll1l11l_opy_, stage=STAGE.bstack1ll11l11_opy_)
    def bstack11lllll11l1_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1ll1l11_opy_ (u"ࠥ࠴ࠧᚙ"),
    ):
        self.bstack1l11111111l_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1ll1l11_opy_ (u"ࠦࠧᚚ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        req.client_worker_id = bstack1ll1l11_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦ᚛").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1llll11l11_opy_.AISelfHealStep(req)
            self.logger.info(bstack1ll1l11_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣ᚜") + str(r) + bstack1ll1l11_opy_ (u"ࠢࠣ᚝"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨ᚞") + str(e) + bstack1ll1l11_opy_ (u"ࠤࠥ᚟"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11llll1l1l1_opy_, stage=STAGE.bstack1ll11l11_opy_)
    def bstack11llll1ll11_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1ll1l11_opy_ (u"ࠥ࠴ࠧᚠ")):
        self.bstack1l11111111l_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        req.client_worker_id = bstack1ll1l11_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᚡ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1llll11l11_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1ll1l11_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᚢ") + str(r) + bstack1ll1l11_opy_ (u"ࠨࠢᚣ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᚤ") + str(e) + bstack1ll1l11_opy_ (u"ࠣࠤᚥ"))
            traceback.print_exc()
            raise e