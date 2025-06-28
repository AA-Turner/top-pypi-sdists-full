# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
from browserstack_sdk.sdk_cli.bstack1ll1llll1l1_opy_ import bstack1llll1111ll_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll11l_opy_ import (
    bstack1lllll1lll1_opy_,
    bstack1111111ll1_opy_,
    bstack1111111l1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1ll111ll_opy_ import bstack1lll1l1l1ll_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll1llll1l1_opy_ import bstack1llll1111ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1ll1ll11l11_opy_(bstack1llll1111ll_opy_):
    bstack1ll11ll1ll1_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1lll1l1l1ll_opy_.bstack1ll11llll11_opy_((bstack1lllll1lll1_opy_.bstack1llllllll11_opy_, bstack1111111ll1_opy_.PRE), self.bstack1ll11111lll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11111lll_opy_(
        self,
        f: bstack1lll1l1l1ll_opy_,
        driver: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllll1111_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1111111ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1ll1111lll1_opy_(hub_url):
            if not bstack1ll1ll11l11_opy_.bstack1ll11ll1ll1_opy_:
                self.logger.warning(bstack1l1ll1_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࠢࡶࡩࡱ࡬࠭ࡩࡧࡤࡰࠥ࡬࡬ࡰࡹࠣࡨ࡮ࡹࡡࡣ࡮ࡨࡨࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡ࡫ࡱࡪࡷࡧࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠢ࡫ࡹࡧࡥࡵࡳ࡮ࡀࠦᇥ") + str(hub_url) + bstack1l1ll1_opy_ (u"ࠦࠧᇦ"))
                bstack1ll1ll11l11_opy_.bstack1ll11ll1ll1_opy_ = True
            return
        bstack1ll111l111l_opy_ = f.bstack1ll1l1l111l_opy_(*args)
        bstack1ll1111llll_opy_ = f.bstack1ll11111ll1_opy_(*args)
        if bstack1ll111l111l_opy_ and bstack1ll111l111l_opy_.lower() == bstack1l1ll1_opy_ (u"ࠧ࡬ࡩ࡯ࡦࡨࡰࡪࡳࡥ࡯ࡶࠥᇧ") and bstack1ll1111llll_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll1111llll_opy_.get(bstack1l1ll1_opy_ (u"ࠨࡵࡴ࡫ࡱ࡫ࠧᇨ"), None), bstack1ll1111llll_opy_.get(bstack1l1ll1_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨᇩ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1l1ll1_opy_ (u"ࠣࡽࡦࡳࡲࡳࡡ࡯ࡦࡢࡲࡦࡳࡥࡾ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠤࡴࡸࠠࡢࡴࡪࡷ࠳ࡻࡳࡪࡰࡪࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡵࡲࠡࡣࡵ࡫ࡸ࠴ࡶࡢ࡮ࡸࡩࡂࠨᇪ") + str(locator_value) + bstack1l1ll1_opy_ (u"ࠤࠥᇫ"))
                return
            def bstack1lllll11lll_opy_(driver, bstack1ll1111l111_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll1111l111_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll111l1111_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1l1ll1_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶ࠱ࡸࡩࡲࡪࡲࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࠨᇬ") + str(locator_value) + bstack1l1ll1_opy_ (u"ࠦࠧᇭ"))
                    else:
                        self.logger.warning(bstack1l1ll1_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸ࠳࡮ࡰ࠯ࡶࡧࡷ࡯ࡰࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࢁࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠽ࠣᇮ") + str(response) + bstack1l1ll1_opy_ (u"ࠨࠢᇯ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll1111l1ll_opy_(
                        driver, bstack1ll1111l111_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1lllll11lll_opy_.__name__ = bstack1ll111l111l_opy_
            return bstack1lllll11lll_opy_
    def __1ll1111l1ll_opy_(
        self,
        driver,
        bstack1ll1111l111_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1ll111l1111_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1l1ll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡷࡶ࡮࡭ࡧࡦࡴࡨࡨ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࠢᇰ") + str(locator_value) + bstack1l1ll1_opy_ (u"ࠣࠤᇱ"))
                bstack1ll1111ll11_opy_ = self.bstack1ll1111ll1l_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1l1ll1_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡷ࡫ࡳࡶ࡮ࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࢃࠠࡩࡧࡤࡰ࡮ࡴࡧࡠࡴࡨࡷࡺࡲࡴ࠾ࠤᇲ") + str(bstack1ll1111ll11_opy_) + bstack1l1ll1_opy_ (u"ࠥࠦᇳ"))
                if bstack1ll1111ll11_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1l1ll1_opy_ (u"ࠦࡺࡹࡩ࡯ࡩࠥᇴ"): bstack1ll1111ll11_opy_.locator_type,
                            bstack1l1ll1_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᇵ"): bstack1ll1111ll11_opy_.locator_value,
                        }
                    )
                    return bstack1ll1111l111_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1l1ll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡉࡠࡆࡈࡆ࡚ࡍࠢᇶ"), False):
                    self.logger.info(bstack1lll1l11ll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡵࡩࡸࡻ࡬ࡵ࠯ࡰ࡭ࡸࡹࡩ࡯ࡩ࠽ࠤࡸࡲࡥࡦࡲࠫ࠷࠵࠯ࠠ࡭ࡧࡷࡸ࡮ࡴࡧࠡࡻࡲࡹࠥ࡯࡮ࡴࡲࡨࡧࡹࠦࡴࡩࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࠠ࡭ࡱࡪࡷࠧᇷ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1l1ll1_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯ࡱࡳ࠲ࡹࡣࡳ࡫ࡳࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫ࡽࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࡀࠦᇸ") + str(response) + bstack1l1ll1_opy_ (u"ࠤࠥᇹ"))
        except Exception as err:
            self.logger.warning(bstack1l1ll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡸࡥࡴࡷ࡯ࡸ࠿ࠦࡥࡳࡴࡲࡶ࠿ࠦࠢᇺ") + str(err) + bstack1l1ll1_opy_ (u"ࠦࠧᇻ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll1111l1l1_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
    def bstack1ll111l1111_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1l1ll1_opy_ (u"ࠧ࠶ࠢᇼ"),
    ):
        self.bstack1ll111ll1ll_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1l1ll1_opy_ (u"ࠨࠢᇽ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1lll1l111l1_opy_.AISelfHealStep(req)
            self.logger.info(bstack1l1ll1_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᇾ") + str(r) + bstack1l1ll1_opy_ (u"ࠣࠤᇿ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1ll1_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢሀ") + str(e) + bstack1l1ll1_opy_ (u"ࠥࠦሁ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll1111l11l_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
    def bstack1ll1111ll1l_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1l1ll1_opy_ (u"ࠦ࠵ࠨሂ")):
        self.bstack1ll111ll1ll_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1lll1l111l1_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1l1ll1_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢሃ") + str(r) + bstack1l1ll1_opy_ (u"ࠨࠢሄ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1ll1_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧህ") + str(e) + bstack1l1ll1_opy_ (u"ࠣࠤሆ"))
            traceback.print_exc()
            raise e