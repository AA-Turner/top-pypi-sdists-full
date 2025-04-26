# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
from browserstack_sdk.sdk_cli.bstack1lll11lll1l_opy_ import bstack1llll111111_opy_
from browserstack_sdk.sdk_cli.bstack11111111l1_opy_ import (
    bstack111111lll1_opy_,
    bstack111111l1l1_opy_,
    bstack11111111ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll1l11ll_opy_ import bstack1lll1lll1l1_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll11lll1l_opy_ import bstack1llll111111_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1llll111lll_opy_(bstack1llll111111_opy_):
    bstack1ll1ll1111l_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1lll1lll1l1_opy_.bstack1ll1ll11l1l_opy_((bstack111111lll1_opy_.bstack1111l11ll1_opy_, bstack111111l1l1_opy_.PRE), self.bstack1ll11ll11ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11ll11ll_opy_(
        self,
        f: bstack1lll1lll1l1_opy_,
        driver: object,
        exec: Tuple[bstack11111111ll_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111lll1_opy_, bstack111111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1ll11lll111_opy_(hub_url):
            if not bstack1llll111lll_opy_.bstack1ll1ll1111l_opy_:
                self.logger.warning(bstack1l11lll_opy_ (u"ࠢ࡭ࡱࡦࡥࡱࠦࡳࡦ࡮ࡩ࠱࡭࡫ࡡ࡭ࠢࡩࡰࡴࡽࠠࡥ࡫ࡶࡥࡧࡲࡥࡥࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥ࡯࡮ࡧࡴࡤࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡨࡶࡤࡢࡹࡷࡲ࠽ࠣᆀ") + str(hub_url) + bstack1l11lll_opy_ (u"ࠣࠤᆁ"))
                bstack1llll111lll_opy_.bstack1ll1ll1111l_opy_ = True
            return
        bstack1ll11lll11l_opy_ = f.bstack1ll1l111111_opy_(*args)
        bstack1ll11ll1ll1_opy_ = f.bstack1ll11l1lll1_opy_(*args)
        if bstack1ll11lll11l_opy_ and bstack1ll11lll11l_opy_.lower() == bstack1l11lll_opy_ (u"ࠤࡩ࡭ࡳࡪࡥ࡭ࡧࡰࡩࡳࡺࠢᆂ") and bstack1ll11ll1ll1_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll11ll1ll1_opy_.get(bstack1l11lll_opy_ (u"ࠥࡹࡸ࡯࡮ࡨࠤᆃ"), None), bstack1ll11ll1ll1_opy_.get(bstack1l11lll_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥᆄ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1l11lll_opy_ (u"ࠧࢁࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࢂࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠡࡱࡵࠤࡦࡸࡧࡴ࠰ࡸࡷ࡮ࡴࡧ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢࡲࡶࠥࡧࡲࡨࡵ࠱ࡺࡦࡲࡵࡦ࠿ࠥᆅ") + str(locator_value) + bstack1l11lll_opy_ (u"ࠨࠢᆆ"))
                return
            def bstack111111ll11_opy_(driver, bstack1ll11l1llll_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll11l1llll_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll11ll1l11_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1l11lll_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳ࠮ࡵࡦࡶ࡮ࡶࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࠥᆇ") + str(locator_value) + bstack1l11lll_opy_ (u"ࠣࠤᆈ"))
                    else:
                        self.logger.warning(bstack1l11lll_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵ࠰ࡲࡴ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࡁࠧᆉ") + str(response) + bstack1l11lll_opy_ (u"ࠥࠦᆊ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll11ll1111_opy_(
                        driver, bstack1ll11l1llll_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack111111ll11_opy_.__name__ = bstack1ll11lll11l_opy_
            return bstack111111ll11_opy_
    def __1ll11ll1111_opy_(
        self,
        driver,
        bstack1ll11l1llll_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1ll11ll1l11_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1l11lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡴࡳ࡫ࡪ࡫ࡪࡸࡥࡥ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࠦᆋ") + str(locator_value) + bstack1l11lll_opy_ (u"ࠧࠨᆌ"))
                bstack1ll11ll111l_opy_ = self.bstack1ll11ll11l1_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1l11lll_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭ࡩࡧࡤࡰ࡮ࡴࡧ࠮ࡴࡨࡷࡺࡲࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࢀࠤ࡭࡫ࡡ࡭࡫ࡱ࡫ࡤࡸࡥࡴࡷ࡯ࡸࡂࠨᆍ") + str(bstack1ll11ll111l_opy_) + bstack1l11lll_opy_ (u"ࠢࠣᆎ"))
                if bstack1ll11ll111l_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1l11lll_opy_ (u"ࠣࡷࡶ࡭ࡳ࡭ࠢᆏ"): bstack1ll11ll111l_opy_.locator_type,
                            bstack1l11lll_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣᆐ"): bstack1ll11ll111l_opy_.locator_value,
                        }
                    )
                    return bstack1ll11l1llll_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1l11lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡍࡤࡊࡅࡃࡗࡊࠦᆑ"), False):
                    self.logger.info(bstack1lll1l1111l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹ࠳࡭ࡪࡵࡶ࡭ࡳ࡭࠺ࠡࡵ࡯ࡩࡪࡶࠨ࠴࠲ࠬࠤࡱ࡫ࡴࡵ࡫ࡱ࡫ࠥࡿ࡯ࡶࠢ࡬ࡲࡸࡶࡥࡤࡶࠣࡸ࡭࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡧࡻࡸࡪࡴࡳࡪࡱࡱࠤࡱࡵࡧࡴࠤᆒ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1l11lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳࡮ࡰ࠯ࡶࡧࡷ࡯ࡰࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࢁࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠽ࠣᆓ") + str(response) + bstack1l11lll_opy_ (u"ࠨࠢᆔ"))
        except Exception as err:
            self.logger.warning(bstack1l11lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡵࡩࡸࡻ࡬ࡵ࠼ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠦᆕ") + str(err) + bstack1l11lll_opy_ (u"ࠣࠤᆖ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll11ll1l1l_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
    def bstack1ll11ll1l11_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1l11lll_opy_ (u"ࠤ࠳ࠦᆗ"),
    ):
        self.bstack1ll1ll1l11l_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1l11lll_opy_ (u"ࠥࠦᆘ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1lll1ll11ll_opy_.AISelfHealStep(req)
            self.logger.info(bstack1l11lll_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᆙ") + str(r) + bstack1l11lll_opy_ (u"ࠧࠨᆚ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l11lll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᆛ") + str(e) + bstack1l11lll_opy_ (u"ࠢࠣᆜ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll11ll1lll_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
    def bstack1ll11ll11l1_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1l11lll_opy_ (u"ࠣ࠲ࠥᆝ")):
        self.bstack1ll1ll1l11l_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1lll1ll11ll_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1l11lll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᆞ") + str(r) + bstack1l11lll_opy_ (u"ࠥࠦᆟ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l11lll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᆠ") + str(e) + bstack1l11lll_opy_ (u"ࠧࠨᆡ"))
            traceback.print_exc()
            raise e