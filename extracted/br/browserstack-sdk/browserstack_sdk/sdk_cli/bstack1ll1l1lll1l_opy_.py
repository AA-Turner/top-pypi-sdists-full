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
from browserstack_sdk.sdk_cli.bstack1lll11ll111_opy_ import bstack1ll1l1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1l1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1lllll111ll_opy_,
    bstack1llll1ll111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1ll111l_opy_ import bstack1ll1l1ll111_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll11ll111_opy_ import bstack1ll1l1l11l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1lll1l111l1_opy_(bstack1ll1l1l11l1_opy_):
    bstack1ll11l11l11_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1ll1l1ll111_opy_.bstack1ll111l11ll_opy_((bstack1lllll1l111_opy_.bstack1llllllllll_opy_, bstack1lllll111ll_opy_.PRE), self.bstack1l1llllllll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1llllllll_opy_(
        self,
        f: bstack1ll1l1ll111_opy_,
        driver: object,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1l1lllllll1_opy_(hub_url):
            if not bstack1lll1l111l1_opy_.bstack1ll11l11l11_opy_:
                self.logger.warning(bstack1ll11ll_opy_ (u"ࠣ࡮ࡲࡧࡦࡲࠠࡴࡧ࡯ࡪ࠲࡮ࡥࡢ࡮ࠣࡪࡱࡵࡷࠡࡦ࡬ࡷࡦࡨ࡬ࡦࡦࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡩ࡯ࡨࡵࡥࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡩࡷࡥࡣࡺࡸ࡬࠾ࠤሩ") + str(hub_url) + bstack1ll11ll_opy_ (u"ࠤࠥሪ"))
                bstack1lll1l111l1_opy_.bstack1ll11l11l11_opy_ = True
            return
        command_name = f.bstack1ll111ll1l1_opy_(*args)
        bstack1ll11111lll_opy_ = f.bstack1ll11111l11_opy_(*args)
        if command_name and command_name.lower() == bstack1ll11ll_opy_ (u"ࠥࡪ࡮ࡴࡤࡦ࡮ࡨࡱࡪࡴࡴࠣራ") and bstack1ll11111lll_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll11111lll_opy_.get(bstack1ll11ll_opy_ (u"ࠦࡺࡹࡩ࡯ࡩࠥሬ"), None), bstack1ll11111lll_opy_.get(bstack1ll11ll_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦር"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1ll11ll_opy_ (u"ࠨࡻࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࢃ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡲࡶࠥࡧࡲࡨࡵ࠱ࡹࡸ࡯࡮ࡨ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡳࡷࠦࡡࡳࡩࡶ࠲ࡻࡧ࡬ࡶࡧࡀࠦሮ") + str(locator_value) + bstack1ll11ll_opy_ (u"ࠢࠣሯ"))
                return
            def bstack1llll1l1ll1_opy_(driver, bstack1ll11111ll1_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll11111ll1_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll11111l1l_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1ll11ll_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴ࠯ࡶࡧࡷ࡯ࡰࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࠦሰ") + str(locator_value) + bstack1ll11ll_opy_ (u"ࠤࠥሱ"))
                    else:
                        self.logger.warning(bstack1ll11ll_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶ࠱ࡳࡵ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣࡶࡪࡹࡰࡰࡰࡶࡩࡂࠨሲ") + str(response) + bstack1ll11ll_opy_ (u"ࠦࠧሳ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll1111111l_opy_(
                        driver, bstack1ll11111ll1_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1llll1l1ll1_opy_.__name__ = command_name
            return bstack1llll1l1ll1_opy_
    def __1ll1111111l_opy_(
        self,
        driver,
        bstack1ll11111ll1_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1ll11111l1l_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1ll11ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡵࡴ࡬࡫࡬࡫ࡲࡦࡦ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࠧሴ") + str(locator_value) + bstack1ll11ll_opy_ (u"ࠨࠢስ"))
                bstack1ll11111111_opy_ = self.bstack1ll111111l1_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1ll11ll_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡵࡩࡸࡻ࡬ࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࢁࠥ࡮ࡥࡢ࡮࡬ࡲ࡬ࡥࡲࡦࡵࡸࡰࡹࡃࠢሶ") + str(bstack1ll11111111_opy_) + bstack1ll11ll_opy_ (u"ࠣࠤሷ"))
                if bstack1ll11111111_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1ll11ll_opy_ (u"ࠤࡸࡷ࡮ࡴࡧࠣሸ"): bstack1ll11111111_opy_.locator_type,
                            bstack1ll11ll_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤሹ"): bstack1ll11111111_opy_.locator_value,
                        }
                    )
                    return bstack1ll11111ll1_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1ll11ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡎࡥࡄࡆࡄࡘࡋࠧሺ"), False):
                    self.logger.info(bstack1lll111ll1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠭࡮࡫ࡶࡷ࡮ࡴࡧ࠻ࠢࡶࡰࡪ࡫ࡰࠩ࠵࠳࠭ࠥࡲࡥࡵࡶ࡬ࡲ࡬ࠦࡹࡰࡷࠣ࡭ࡳࡹࡰࡦࡥࡷࠤࡹ࡮ࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࠥࡲ࡯ࡨࡵࠥሻ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1ll11ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭࡯ࡱ࠰ࡷࡨࡸࡩࡱࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠾ࠤሼ") + str(response) + bstack1ll11ll_opy_ (u"ࠢࠣሽ"))
        except Exception as err:
            self.logger.warning(bstack1ll11ll_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡶࡪࡹࡵ࡭ࡶ࠽ࠤࡪࡸࡲࡰࡴ࠽ࠤࠧሾ") + str(err) + bstack1ll11ll_opy_ (u"ࠤࠥሿ"))
        raise exception
    @measure(event_name=EVENTS.bstack1l1llllll1l_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def bstack1ll11111l1l_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1ll11ll_opy_ (u"ࠥ࠴ࠧቀ"),
    ):
        self.bstack1ll11l11lll_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1ll11ll_opy_ (u"ࠦࠧቁ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1ll1llllll1_opy_.AISelfHealStep(req)
            self.logger.info(bstack1ll11ll_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢቂ") + str(r) + bstack1ll11ll_opy_ (u"ࠨࠢቃ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧቄ") + str(e) + bstack1ll11ll_opy_ (u"ࠣࠤቅ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll111111ll_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def bstack1ll111111l1_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1ll11ll_opy_ (u"ࠤ࠳ࠦቆ")):
        self.bstack1ll11l11lll_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1ll1llllll1_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1ll11ll_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧቇ") + str(r) + bstack1ll11ll_opy_ (u"ࠦࠧቈ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥ቉") + str(e) + bstack1ll11ll_opy_ (u"ࠨࠢቊ"))
            traceback.print_exc()
            raise e