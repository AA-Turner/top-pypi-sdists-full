# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
from browserstack_sdk.sdk_cli.bstack1llll1ll1l1_opy_ import bstack1lll1ll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import (
    bstack1lllll1ll11_opy_,
    bstack1llllll1ll1_opy_,
    bstack1111111l1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l111l1_opy_ import bstack1ll1lllllll_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll1ll1l1_opy_ import bstack1lll1ll1l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1ll1ll11lll_opy_(bstack1lll1ll1l1l_opy_):
    bstack1ll1l11ll11_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1ll1lllllll_opy_.bstack1ll11l11lll_opy_((bstack1lllll1ll11_opy_.bstack1llllllll11_opy_, bstack1llllll1ll1_opy_.PRE), self.bstack1ll1111l111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1111l111_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        driver: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1ll11111ll1_opy_(hub_url):
            if not bstack1ll1ll11lll_opy_.bstack1ll1l11ll11_opy_:
                self.logger.warning(bstack11ll1l1_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࠢࡶࡩࡱ࡬࠭ࡩࡧࡤࡰࠥ࡬࡬ࡰࡹࠣࡨ࡮ࡹࡡࡣ࡮ࡨࡨࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡ࡫ࡱࡪࡷࡧࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠢ࡫ࡹࡧࡥࡵࡳ࡮ࡀࠦᇥ") + str(hub_url) + bstack11ll1l1_opy_ (u"ࠦࠧᇦ"))
                bstack1ll1ll11lll_opy_.bstack1ll1l11ll11_opy_ = True
            return
        bstack1ll1l11lll1_opy_ = f.bstack1ll1l111ll1_opy_(*args)
        bstack1ll1111lll1_opy_ = f.bstack1ll1111ll11_opy_(*args)
        if bstack1ll1l11lll1_opy_ and bstack1ll1l11lll1_opy_.lower() == bstack11ll1l1_opy_ (u"ࠧ࡬ࡩ࡯ࡦࡨࡰࡪࡳࡥ࡯ࡶࠥᇧ") and bstack1ll1111lll1_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll1111lll1_opy_.get(bstack11ll1l1_opy_ (u"ࠨࡵࡴ࡫ࡱ࡫ࠧᇨ"), None), bstack1ll1111lll1_opy_.get(bstack11ll1l1_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨᇩ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack11ll1l1_opy_ (u"ࠣࡽࡦࡳࡲࡳࡡ࡯ࡦࡢࡲࡦࡳࡥࡾ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠤࡴࡸࠠࡢࡴࡪࡷ࠳ࡻࡳࡪࡰࡪࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡵࡲࠡࡣࡵ࡫ࡸ࠴ࡶࡢ࡮ࡸࡩࡂࠨᇪ") + str(locator_value) + bstack11ll1l1_opy_ (u"ࠤࠥᇫ"))
                return
            def bstack1lllll11lll_opy_(driver, bstack1ll1111ll1l_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll1111ll1l_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll1111l1l1_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack11ll1l1_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶ࠱ࡸࡩࡲࡪࡲࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࠨᇬ") + str(locator_value) + bstack11ll1l1_opy_ (u"ࠦࠧᇭ"))
                    else:
                        self.logger.warning(bstack11ll1l1_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸ࠳࡮ࡰ࠯ࡶࡧࡷ࡯ࡰࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࢁࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠽ࠣᇮ") + str(response) + bstack11ll1l1_opy_ (u"ࠨࠢᇯ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll11111l1l_opy_(
                        driver, bstack1ll1111ll1l_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1lllll11lll_opy_.__name__ = bstack1ll1l11lll1_opy_
            return bstack1lllll11lll_opy_
    def __1ll11111l1l_opy_(
        self,
        driver,
        bstack1ll1111ll1l_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1ll1111l1l1_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack11ll1l1_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡷࡶ࡮࡭ࡧࡦࡴࡨࡨ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࠢᇰ") + str(locator_value) + bstack11ll1l1_opy_ (u"ࠣࠤᇱ"))
                bstack1ll1111llll_opy_ = self.bstack1ll1111l1ll_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack11ll1l1_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡷ࡫ࡳࡶ࡮ࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࢃࠠࡩࡧࡤࡰ࡮ࡴࡧࡠࡴࡨࡷࡺࡲࡴ࠾ࠤᇲ") + str(bstack1ll1111llll_opy_) + bstack11ll1l1_opy_ (u"ࠥࠦᇳ"))
                if bstack1ll1111llll_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack11ll1l1_opy_ (u"ࠦࡺࡹࡩ࡯ࡩࠥᇴ"): bstack1ll1111llll_opy_.locator_type,
                            bstack11ll1l1_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᇵ"): bstack1ll1111llll_opy_.locator_value,
                        }
                    )
                    return bstack1ll1111ll1l_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack11ll1l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡉࡠࡆࡈࡆ࡚ࡍࠢᇶ"), False):
                    self.logger.info(bstack1llll1111l1_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡵࡩࡸࡻ࡬ࡵ࠯ࡰ࡭ࡸࡹࡩ࡯ࡩ࠽ࠤࡸࡲࡥࡦࡲࠫ࠷࠵࠯ࠠ࡭ࡧࡷࡸ࡮ࡴࡧࠡࡻࡲࡹࠥ࡯࡮ࡴࡲࡨࡧࡹࠦࡴࡩࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࠠ࡭ࡱࡪࡷࠧᇷ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack11ll1l1_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯ࡱࡳ࠲ࡹࡣࡳ࡫ࡳࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫ࡽࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࡀࠦᇸ") + str(response) + bstack11ll1l1_opy_ (u"ࠤࠥᇹ"))
        except Exception as err:
            self.logger.warning(bstack11ll1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡸࡥࡴࡷ࡯ࡸ࠿ࠦࡥࡳࡴࡲࡶ࠿ࠦࠢᇺ") + str(err) + bstack11ll1l1_opy_ (u"ࠦࠧᇻ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll11111lll_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
    def bstack1ll1111l1l1_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack11ll1l1_opy_ (u"ࠧ࠶ࠢᇼ"),
    ):
        self.bstack1ll11llllll_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack11ll1l1_opy_ (u"ࠨࠢᇽ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1lll1l1ll1l_opy_.AISelfHealStep(req)
            self.logger.info(bstack11ll1l1_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᇾ") + str(r) + bstack11ll1l1_opy_ (u"ࠣࠤᇿ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢሀ") + str(e) + bstack11ll1l1_opy_ (u"ࠥࠦሁ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll1111l11l_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
    def bstack1ll1111l1ll_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack11ll1l1_opy_ (u"ࠦ࠵ࠨሂ")):
        self.bstack1ll11llllll_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1lll1l1ll1l_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack11ll1l1_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢሃ") + str(r) + bstack11ll1l1_opy_ (u"ࠨࠢሄ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧህ") + str(e) + bstack11ll1l1_opy_ (u"ࠣࠤሆ"))
            traceback.print_exc()
            raise e