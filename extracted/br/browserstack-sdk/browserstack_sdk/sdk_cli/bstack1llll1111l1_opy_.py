# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
from browserstack_sdk.sdk_cli.bstack1llll1ll11l_opy_ import bstack1ll1llll1l1_opy_
from browserstack_sdk.sdk_cli.bstack11111l1l11_opy_ import (
    bstack11111lll11_opy_,
    bstack1111111l1l_opy_,
    bstack111111ll11_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1lllll1_opy_ import bstack1lll11ll1ll_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll1ll11l_opy_ import bstack1ll1llll1l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1ll1llll1ll_opy_(bstack1ll1llll1l1_opy_):
    bstack1ll1ll11l1l_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1lll11ll1ll_opy_.bstack1ll1l111l1l_opy_((bstack11111lll11_opy_.bstack11111l111l_opy_, bstack1111111l1l_opy_.PRE), self.bstack1ll11ll1l11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11ll1l11_opy_(
        self,
        f: bstack1lll11ll1ll_opy_,
        driver: object,
        exec: Tuple[bstack111111ll11_opy_, str],
        bstack1111111lll_opy_: Tuple[bstack11111lll11_opy_, bstack1111111l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1ll11ll11l1_opy_(hub_url):
            if not bstack1ll1llll1ll_opy_.bstack1ll1ll11l1l_opy_:
                self.logger.warning(bstack1llllll_opy_ (u"ࠢ࡭ࡱࡦࡥࡱࠦࡳࡦ࡮ࡩ࠱࡭࡫ࡡ࡭ࠢࡩࡰࡴࡽࠠࡥ࡫ࡶࡥࡧࡲࡥࡥࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥ࡯࡮ࡧࡴࡤࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡨࡶࡤࡢࡹࡷࡲ࠽ࠣᆀ") + str(hub_url) + bstack1llllll_opy_ (u"ࠣࠤᆁ"))
                bstack1ll1llll1ll_opy_.bstack1ll1ll11l1l_opy_ = True
            return
        bstack1ll1l1lll1l_opy_ = f.bstack1ll1ll1111l_opy_(*args)
        bstack1ll11ll111l_opy_ = f.bstack1ll11ll1lll_opy_(*args)
        if bstack1ll1l1lll1l_opy_ and bstack1ll1l1lll1l_opy_.lower() == bstack1llllll_opy_ (u"ࠤࡩ࡭ࡳࡪࡥ࡭ࡧࡰࡩࡳࡺࠢᆂ") and bstack1ll11ll111l_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll11ll111l_opy_.get(bstack1llllll_opy_ (u"ࠥࡹࡸ࡯࡮ࡨࠤᆃ"), None), bstack1ll11ll111l_opy_.get(bstack1llllll_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥᆄ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1llllll_opy_ (u"ࠧࢁࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࢂࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠡࡱࡵࠤࡦࡸࡧࡴ࠰ࡸࡷ࡮ࡴࡧ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢࡲࡶࠥࡧࡲࡨࡵ࠱ࡺࡦࡲࡵࡦ࠿ࠥᆅ") + str(locator_value) + bstack1llllll_opy_ (u"ࠨࠢᆆ"))
                return
            def bstack11111lllll_opy_(driver, bstack1ll11ll1111_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll11ll1111_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll11ll1l1l_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1llllll_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳ࠮ࡵࡦࡶ࡮ࡶࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࠥᆇ") + str(locator_value) + bstack1llllll_opy_ (u"ࠣࠤᆈ"))
                    else:
                        self.logger.warning(bstack1llllll_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵ࠰ࡲࡴ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࡁࠧᆉ") + str(response) + bstack1llllll_opy_ (u"ࠥࠦᆊ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll11l1lll1_opy_(
                        driver, bstack1ll11ll1111_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack11111lllll_opy_.__name__ = bstack1ll1l1lll1l_opy_
            return bstack11111lllll_opy_
    def __1ll11l1lll1_opy_(
        self,
        driver,
        bstack1ll11ll1111_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1ll11ll1l1l_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1llllll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡴࡳ࡫ࡪ࡫ࡪࡸࡥࡥ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࠦᆋ") + str(locator_value) + bstack1llllll_opy_ (u"ࠧࠨᆌ"))
                bstack1ll11ll11ll_opy_ = self.bstack1ll11l1llll_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1llllll_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭ࡩࡧࡤࡰ࡮ࡴࡧ࠮ࡴࡨࡷࡺࡲࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࢀࠤ࡭࡫ࡡ࡭࡫ࡱ࡫ࡤࡸࡥࡴࡷ࡯ࡸࡂࠨᆍ") + str(bstack1ll11ll11ll_opy_) + bstack1llllll_opy_ (u"ࠢࠣᆎ"))
                if bstack1ll11ll11ll_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1llllll_opy_ (u"ࠣࡷࡶ࡭ࡳ࡭ࠢᆏ"): bstack1ll11ll11ll_opy_.locator_type,
                            bstack1llllll_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣᆐ"): bstack1ll11ll11ll_opy_.locator_value,
                        }
                    )
                    return bstack1ll11ll1111_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1llllll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡍࡤࡊࡅࡃࡗࡊࠦᆑ"), False):
                    self.logger.info(bstack1llll1ll1ll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹ࠳࡭ࡪࡵࡶ࡭ࡳ࡭࠺ࠡࡵ࡯ࡩࡪࡶࠨ࠴࠲ࠬࠤࡱ࡫ࡴࡵ࡫ࡱ࡫ࠥࡿ࡯ࡶࠢ࡬ࡲࡸࡶࡥࡤࡶࠣࡸ࡭࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡧࡻࡸࡪࡴࡳࡪࡱࡱࠤࡱࡵࡧࡴࠤᆒ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1llllll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳࡮ࡰ࠯ࡶࡧࡷ࡯ࡰࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࢁࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠽ࠣᆓ") + str(response) + bstack1llllll_opy_ (u"ࠨࠢᆔ"))
        except Exception as err:
            self.logger.warning(bstack1llllll_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡵࡩࡸࡻ࡬ࡵ࠼ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠦᆕ") + str(err) + bstack1llllll_opy_ (u"ࠣࠤᆖ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll11lll111_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
    def bstack1ll11ll1l1l_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1llllll_opy_ (u"ࠤ࠳ࠦᆗ"),
    ):
        self.bstack1ll1ll11lll_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1llllll_opy_ (u"ࠥࠦᆘ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1lllll1llll_opy_.AISelfHealStep(req)
            self.logger.info(bstack1llllll_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᆙ") + str(r) + bstack1llllll_opy_ (u"ࠧࠨᆚ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1llllll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᆛ") + str(e) + bstack1llllll_opy_ (u"ࠢࠣᆜ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll11ll1ll1_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
    def bstack1ll11l1llll_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1llllll_opy_ (u"ࠣ࠲ࠥᆝ")):
        self.bstack1ll1ll11lll_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1lllll1llll_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1llllll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᆞ") + str(r) + bstack1llllll_opy_ (u"ࠥࠦᆟ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1llllll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᆠ") + str(e) + bstack1llllll_opy_ (u"ࠧࠨᆡ"))
            traceback.print_exc()
            raise e