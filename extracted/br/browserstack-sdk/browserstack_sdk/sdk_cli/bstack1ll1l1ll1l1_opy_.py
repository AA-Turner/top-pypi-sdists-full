# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
from browserstack_sdk.sdk_cli.bstack1ll1llll11l_opy_ import bstack1lll1lll111_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1ll1l_opy_ import (
    bstack1lllll11111_opy_,
    bstack1llll1lllll_opy_,
    bstack1llllllll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1lll1l111ll_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll1llll11l_opy_ import bstack1lll1lll111_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1lll1lll1l1_opy_(bstack1lll1lll111_opy_):
    bstack1ll111ll1ll_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1lll1l111ll_opy_.bstack1ll111lll1l_opy_((bstack1lllll11111_opy_.bstack1llll1lll11_opy_, bstack1llll1lllll_opy_.PRE), self.bstack1ll1111111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1111111l_opy_(
        self,
        f: bstack1lll1l111ll_opy_,
        driver: object,
        exec: Tuple[bstack1llllllll1l_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1l1lllllll1_opy_(hub_url):
            if not bstack1lll1lll1l1_opy_.bstack1ll111ll1ll_opy_:
                self.logger.warning(bstack1111l1l_opy_ (u"ࠤ࡯ࡳࡨࡧ࡬ࠡࡵࡨࡰ࡫࠳ࡨࡦࡣ࡯ࠤ࡫ࡲ࡯ࡸࠢࡧ࡭ࡸࡧࡢ࡭ࡧࡧࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡪࡰࡩࡶࡦࠦࡳࡦࡵࡶ࡭ࡴࡴࡳࠡࡪࡸࡦࡤࡻࡲ࡭࠿ࠥሪ") + str(hub_url) + bstack1111l1l_opy_ (u"ࠥࠦራ"))
                bstack1lll1lll1l1_opy_.bstack1ll111ll1ll_opy_ = True
            return
        command_name = f.bstack1ll111llll1_opy_(*args)
        bstack1ll1111l111_opy_ = f.bstack1ll111111l1_opy_(*args)
        if command_name and command_name.lower() == bstack1111l1l_opy_ (u"ࠦ࡫࡯࡮ࡥࡧ࡯ࡩࡲ࡫࡮ࡵࠤሬ") and bstack1ll1111l111_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll1111l111_opy_.get(bstack1111l1l_opy_ (u"ࠧࡻࡳࡪࡰࡪࠦር"), None), bstack1ll1111l111_opy_.get(bstack1111l1l_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧሮ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1111l1l_opy_ (u"ࠢࡼࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫ࡽ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠣࡳࡷࠦࡡࡳࡩࡶ࠲ࡺࡹࡩ࡯ࡩࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡴࡸࠠࡢࡴࡪࡷ࠳ࡼࡡ࡭ࡷࡨࡁࠧሯ") + str(locator_value) + bstack1111l1l_opy_ (u"ࠣࠤሰ"))
                return
            def bstack1lllll11l1l_opy_(driver, bstack1ll11111lll_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll11111lll_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll11111111_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1111l1l_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵ࠰ࡷࡨࡸࡩࡱࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࠧሱ") + str(locator_value) + bstack1111l1l_opy_ (u"ࠥࠦሲ"))
                    else:
                        self.logger.warning(bstack1111l1l_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷ࠲ࡴ࡯࠮ࡵࡦࡶ࡮ࡶࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࢀࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡃࠢሳ") + str(response) + bstack1111l1l_opy_ (u"ࠧࠨሴ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll11111l1l_opy_(
                        driver, bstack1ll11111lll_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1lllll11l1l_opy_.__name__ = command_name
            return bstack1lllll11l1l_opy_
    def __1ll11111l1l_opy_(
        self,
        driver,
        bstack1ll11111lll_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1ll11111111_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1111l1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭ࡩࡧࡤࡰ࡮ࡴࡧ࠮ࡶࡵ࡭࡬࡭ࡥࡳࡧࡧ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࠨስ") + str(locator_value) + bstack1111l1l_opy_ (u"ࠢࠣሶ"))
                bstack1ll111111ll_opy_ = self.bstack1ll11111l11_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1111l1l_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡶࡪࡹࡵ࡭ࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࢂࠦࡨࡦࡣ࡯࡭ࡳ࡭࡟ࡳࡧࡶࡹࡱࡺ࠽ࠣሷ") + str(bstack1ll111111ll_opy_) + bstack1111l1l_opy_ (u"ࠤࠥሸ"))
                if bstack1ll111111ll_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1111l1l_opy_ (u"ࠥࡹࡸ࡯࡮ࡨࠤሹ"): bstack1ll111111ll_opy_.locator_type,
                            bstack1111l1l_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥሺ"): bstack1ll111111ll_opy_.locator_value,
                        }
                    )
                    return bstack1ll11111lll_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1111l1l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡏ࡟ࡅࡇࡅ࡙ࡌࠨሻ"), False):
                    self.logger.info(bstack1lll11lll1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭ࡩࡧࡤࡰ࡮ࡴࡧ࠮ࡴࡨࡷࡺࡲࡴ࠮࡯࡬ࡷࡸ࡯࡮ࡨ࠼ࠣࡷࡱ࡫ࡥࡱࠪ࠶࠴࠮ࠦ࡬ࡦࡶࡷ࡭ࡳ࡭ࠠࡺࡱࡸࠤ࡮ࡴࡳࡱࡧࡦࡸࠥࡺࡨࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࠦ࡬ࡰࡩࡶࠦሼ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1111l1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡰࡲ࠱ࡸࡩࡲࡪࡲࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࢃࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠿ࠥሽ") + str(response) + bstack1111l1l_opy_ (u"ࠣࠤሾ"))
        except Exception as err:
            self.logger.warning(bstack1111l1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡷ࡫ࡳࡶ࡮ࡷ࠾ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠨሿ") + str(err) + bstack1111l1l_opy_ (u"ࠥࠦቀ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll11111ll1_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def bstack1ll11111111_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1111l1l_opy_ (u"ࠦ࠵ࠨቁ"),
    ):
        self.bstack1ll1l1111ll_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1111l1l_opy_ (u"ࠧࠨቂ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1ll1ll11l11_opy_.AISelfHealStep(req)
            self.logger.info(bstack1111l1l_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣቃ") + str(r) + bstack1111l1l_opy_ (u"ࠢࠣቄ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨቅ") + str(e) + bstack1111l1l_opy_ (u"ࠤࠥቆ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1llllllll_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def bstack1ll11111l11_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1111l1l_opy_ (u"ࠥ࠴ࠧቇ")):
        self.bstack1ll1l1111ll_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1ll1ll11l11_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1111l1l_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨቈ") + str(r) + bstack1111l1l_opy_ (u"ࠧࠨ቉"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦቊ") + str(e) + bstack1111l1l_opy_ (u"ࠢࠣቋ"))
            traceback.print_exc()
            raise e