# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
from browserstack_sdk.sdk_cli.bstack1lll11l11l1_opy_ import bstack1llll11l111_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1lll_opy_ import (
    bstack1lllll1lll1_opy_,
    bstack1llllll1111_opy_,
    bstack1lllll1ll11_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1lll1lll11l_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll11l11l1_opy_ import bstack1llll11l111_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1llll11l1ll_opy_(bstack1llll11l111_opy_):
    bstack1ll11l11l1l_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1lll1lll11l_opy_.bstack1ll11l111l1_opy_((bstack1lllll1lll1_opy_.bstack1llll1llll1_opy_, bstack1llllll1111_opy_.PRE), self.bstack1ll11111l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11111l1l_opy_(
        self,
        f: bstack1lll1lll11l_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llllll11ll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1ll1111ll1l_opy_(hub_url):
            if not bstack1llll11l1ll_opy_.bstack1ll11l11l1l_opy_:
                self.logger.warning(bstack1111lll_opy_ (u"ࠦࡱࡵࡣࡢ࡮ࠣࡷࡪࡲࡦ࠮ࡪࡨࡥࡱࠦࡦ࡭ࡱࡺࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢ࡬ࡲ࡫ࡸࡡࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧሥ") + str(hub_url) + bstack1111lll_opy_ (u"ࠧࠨሦ"))
                bstack1llll11l1ll_opy_.bstack1ll11l11l1l_opy_ = True
            return
        command_name = f.bstack1ll11lll11l_opy_(*args)
        bstack1ll111111ll_opy_ = f.bstack1ll1111l1ll_opy_(*args)
        if command_name and command_name.lower() == bstack1111lll_opy_ (u"ࠨࡦࡪࡰࡧࡩࡱ࡫࡭ࡦࡰࡷࠦሧ") and bstack1ll111111ll_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll111111ll_opy_.get(bstack1111lll_opy_ (u"ࠢࡶࡵ࡬ࡲ࡬ࠨረ"), None), bstack1ll111111ll_opy_.get(bstack1111lll_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢሩ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1111lll_opy_ (u"ࠤࡾࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦࡿ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡵࡲࠡࡣࡵ࡫ࡸ࠴ࡵࡴ࡫ࡱ࡫ࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡯ࡳࠢࡤࡶ࡬ࡹ࠮ࡷࡣ࡯ࡹࡪࡃࠢሪ") + str(locator_value) + bstack1111lll_opy_ (u"ࠥࠦራ"))
                return
            def bstack1lllll1llll_opy_(driver, bstack1ll11111lll_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll11111lll_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll1111l11l_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1111lll_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷ࠲ࡹࡣࡳ࡫ࡳࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࠢሬ") + str(locator_value) + bstack1111lll_opy_ (u"ࠧࠨር"))
                    else:
                        self.logger.warning(bstack1111lll_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹ࠭࡯ࡱ࠰ࡷࡨࡸࡩࡱࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠾ࠤሮ") + str(response) + bstack1111lll_opy_ (u"ࠢࠣሯ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll11111ll1_opy_(
                        driver, bstack1ll11111lll_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1lllll1llll_opy_.__name__ = command_name
            return bstack1lllll1llll_opy_
    def __1ll11111ll1_opy_(
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
            response = self.bstack1ll1111l11l_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1111lll_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡸࡷ࡯ࡧࡨࡧࡵࡩࡩࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࠣሰ") + str(locator_value) + bstack1111lll_opy_ (u"ࠤࠥሱ"))
                bstack1ll1111ll11_opy_ = self.bstack1ll1111l1l1_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1111lll_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡸࡥࡴࡷ࡯ࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫ࡽࠡࡪࡨࡥࡱ࡯࡮ࡨࡡࡵࡩࡸࡻ࡬ࡵ࠿ࠥሲ") + str(bstack1ll1111ll11_opy_) + bstack1111lll_opy_ (u"ࠦࠧሳ"))
                if bstack1ll1111ll11_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1111lll_opy_ (u"ࠧࡻࡳࡪࡰࡪࠦሴ"): bstack1ll1111ll11_opy_.locator_type,
                            bstack1111lll_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧስ"): bstack1ll1111ll11_opy_.locator_value,
                        }
                    )
                    return bstack1ll11111lll_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1111lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡊࡡࡇࡉࡇ࡛ࡇࠣሶ"), False):
                    self.logger.info(bstack1llll1l1ll1_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡶࡪࡹࡵ࡭ࡶ࠰ࡱ࡮ࡹࡳࡪࡰࡪ࠾ࠥࡹ࡬ࡦࡧࡳࠬ࠸࠶ࠩࠡ࡮ࡨࡸࡹ࡯࡮ࡨࠢࡼࡳࡺࠦࡩ࡯ࡵࡳࡩࡨࡺࠠࡵࡪࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࠡ࡮ࡲ࡫ࡸࠨሷ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1111lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰ࡲࡴ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࡁࠧሸ") + str(response) + bstack1111lll_opy_ (u"ࠥࠦሹ"))
        except Exception as err:
            self.logger.warning(bstack1111lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹࡀࠠࡦࡴࡵࡳࡷࡀࠠࠣሺ") + str(err) + bstack1111lll_opy_ (u"ࠧࠨሻ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll1111l111_opy_, stage=STAGE.bstack11111lll_opy_)
    def bstack1ll1111l11l_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1111lll_opy_ (u"ࠨ࠰ࠣሼ"),
    ):
        self.bstack1ll1l111lll_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1111lll_opy_ (u"ࠢࠣሽ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1lll1llll11_opy_.AISelfHealStep(req)
            self.logger.info(bstack1111lll_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥሾ") + str(r) + bstack1111lll_opy_ (u"ࠤࠥሿ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111lll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣቀ") + str(e) + bstack1111lll_opy_ (u"ࠦࠧቁ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll11111l11_opy_, stage=STAGE.bstack11111lll_opy_)
    def bstack1ll1111l1l1_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1111lll_opy_ (u"ࠧ࠶ࠢቂ")):
        self.bstack1ll1l111lll_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1lll1llll11_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1111lll_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣቃ") + str(r) + bstack1111lll_opy_ (u"ࠢࠣቄ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111lll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨቅ") + str(e) + bstack1111lll_opy_ (u"ࠤࠥቆ"))
            traceback.print_exc()
            raise e