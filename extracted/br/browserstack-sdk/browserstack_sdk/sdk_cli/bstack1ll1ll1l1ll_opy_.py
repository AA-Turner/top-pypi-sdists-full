# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
from browserstack_sdk.sdk_cli.bstack1lll111lll1_opy_ import bstack1ll1l1llll1_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1llll1l11ll_opy_,
    bstack1lllllll111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l1l1l1_opy_ import bstack1ll1l1l1lll_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll111lll1_opy_ import bstack1ll1l1llll1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1ll1ll11lll_opy_(bstack1ll1l1llll1_opy_):
    bstack1ll11ll1111_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1ll1l1l1lll_opy_.bstack1ll11ll111l_opy_((bstack1lllll1l111_opy_.bstack1lllll1lll1_opy_, bstack1llll1l11ll_opy_.PRE), self.bstack1l1llllllll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1llllllll_opy_(
        self,
        f: bstack1ll1l1l1lll_opy_,
        driver: object,
        exec: Tuple[bstack1lllllll111_opy_, str],
        bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1ll11111ll1_opy_(hub_url):
            if not bstack1ll1ll11lll_opy_.bstack1ll11ll1111_opy_:
                self.logger.warning(bstack1l11ll1_opy_ (u"ࠢ࡭ࡱࡦࡥࡱࠦࡳࡦ࡮ࡩ࠱࡭࡫ࡡ࡭ࠢࡩࡰࡴࡽࠠࡥ࡫ࡶࡥࡧࡲࡥࡥࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥ࡯࡮ࡧࡴࡤࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡨࡶࡤࡢࡹࡷࡲ࠽ࠣረ") + str(hub_url) + bstack1l11ll1_opy_ (u"ࠣࠤሩ"))
                bstack1ll1ll11lll_opy_.bstack1ll11ll1111_opy_ = True
            return
        command_name = f.bstack1ll1l111111_opy_(*args)
        bstack1ll11111111_opy_ = f.bstack1l1llllll1l_opy_(*args)
        if command_name and command_name.lower() == bstack1l11ll1_opy_ (u"ࠤࡩ࡭ࡳࡪࡥ࡭ࡧࡰࡩࡳࡺࠢሪ") and bstack1ll11111111_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll11111111_opy_.get(bstack1l11ll1_opy_ (u"ࠥࡹࡸ࡯࡮ࡨࠤራ"), None), bstack1ll11111111_opy_.get(bstack1l11ll1_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥሬ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1l11ll1_opy_ (u"ࠧࢁࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࢂࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠡࡱࡵࠤࡦࡸࡧࡴ࠰ࡸࡷ࡮ࡴࡧ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢࡲࡶࠥࡧࡲࡨࡵ࠱ࡺࡦࡲࡵࡦ࠿ࠥር") + str(locator_value) + bstack1l11ll1_opy_ (u"ࠨࠢሮ"))
                return
            def bstack1llll1ll111_opy_(driver, bstack1ll11111l1l_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll11111l1l_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll111111l1_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1l11ll1_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳ࠮ࡵࡦࡶ࡮ࡶࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࠥሯ") + str(locator_value) + bstack1l11ll1_opy_ (u"ࠣࠤሰ"))
                    else:
                        self.logger.warning(bstack1l11ll1_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵ࠰ࡲࡴ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࡁࠧሱ") + str(response) + bstack1l11ll1_opy_ (u"ࠥࠦሲ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll11111l11_opy_(
                        driver, bstack1ll11111l1l_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1llll1ll111_opy_.__name__ = command_name
            return bstack1llll1ll111_opy_
    def __1ll11111l11_opy_(
        self,
        driver,
        bstack1ll11111l1l_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1ll111111l1_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1l11ll1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡴࡳ࡫ࡪ࡫ࡪࡸࡥࡥ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࠦሳ") + str(locator_value) + bstack1l11ll1_opy_ (u"ࠧࠨሴ"))
                bstack1ll11111lll_opy_ = self.bstack1ll1111111l_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1l11ll1_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭ࡩࡧࡤࡰ࡮ࡴࡧ࠮ࡴࡨࡷࡺࡲࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࢀࠤ࡭࡫ࡡ࡭࡫ࡱ࡫ࡤࡸࡥࡴࡷ࡯ࡸࡂࠨስ") + str(bstack1ll11111lll_opy_) + bstack1l11ll1_opy_ (u"ࠢࠣሶ"))
                if bstack1ll11111lll_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1l11ll1_opy_ (u"ࠣࡷࡶ࡭ࡳ࡭ࠢሷ"): bstack1ll11111lll_opy_.locator_type,
                            bstack1l11ll1_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣሸ"): bstack1ll11111lll_opy_.locator_value,
                        }
                    )
                    return bstack1ll11111l1l_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1l11ll1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡍࡤࡊࡅࡃࡗࡊࠦሹ"), False):
                    self.logger.info(bstack1llll111ll1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹ࠳࡭ࡪࡵࡶ࡭ࡳ࡭࠺ࠡࡵ࡯ࡩࡪࡶࠨ࠴࠲ࠬࠤࡱ࡫ࡴࡵ࡫ࡱ࡫ࠥࡿ࡯ࡶࠢ࡬ࡲࡸࡶࡥࡤࡶࠣࡸ࡭࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡧࡻࡸࡪࡴࡳࡪࡱࡱࠤࡱࡵࡧࡴࠤሺ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1l11ll1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳࡮ࡰ࠯ࡶࡧࡷ࡯ࡰࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࢁࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠽ࠣሻ") + str(response) + bstack1l11ll1_opy_ (u"ࠨࠢሼ"))
        except Exception as err:
            self.logger.warning(bstack1l11ll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡵࡩࡸࡻ࡬ࡵ࠼ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠦሽ") + str(err) + bstack1l11ll1_opy_ (u"ࠣࠤሾ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll111111ll_opy_, stage=STAGE.bstack11lllll111_opy_)
    def bstack1ll111111l1_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1l11ll1_opy_ (u"ࠤ࠳ࠦሿ"),
    ):
        self.bstack1ll11l111l1_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1l11ll1_opy_ (u"ࠥࠦቀ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1lll111111l_opy_.AISelfHealStep(req)
            self.logger.info(bstack1l11ll1_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨቁ") + str(r) + bstack1l11ll1_opy_ (u"ࠧࠨቂ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦቃ") + str(e) + bstack1l11ll1_opy_ (u"ࠢࠣቄ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1lllllll1_opy_, stage=STAGE.bstack11lllll111_opy_)
    def bstack1ll1111111l_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1l11ll1_opy_ (u"ࠣ࠲ࠥቅ")):
        self.bstack1ll11l111l1_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1lll111111l_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1l11ll1_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦቆ") + str(r) + bstack1l11ll1_opy_ (u"ࠥࠦቇ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤቈ") + str(e) + bstack1l11ll1_opy_ (u"ࠧࠨ቉"))
            traceback.print_exc()
            raise e