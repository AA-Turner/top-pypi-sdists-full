# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
from browserstack_sdk.sdk_cli.bstack1llll111111_opy_ import bstack1llll11l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1llll1ll1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1lllll1llll_opy_,
    bstack1111111111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1ll111ll_opy_ import bstack1llll111lll_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll111111_opy_ import bstack1llll11l1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1llll11lll1_opy_(bstack1llll11l1ll_opy_):
    bstack1ll11l1llll_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1llll111lll_opy_.bstack1ll111lll1l_opy_((bstack1lllll1l111_opy_.bstack1lllll11111_opy_, bstack1lllll1llll_opy_.PRE), self.bstack1ll111l1111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll111l1111_opy_(
        self,
        f: bstack1llll111lll_opy_,
        driver: object,
        exec: Tuple[bstack1111111111_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1ll111l1l1l_opy_(hub_url):
            if not bstack1llll11lll1_opy_.bstack1ll11l1llll_opy_:
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࠥࡹࡥ࡭ࡨ࠰࡬ࡪࡧ࡬ࠡࡨ࡯ࡳࡼࠦࡤࡪࡵࡤࡦࡱ࡫ࡤࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤ࡮ࡴࡦࡳࡣࠣࡷࡪࡹࡳࡪࡱࡱࡷࠥ࡮ࡵࡣࡡࡸࡶࡱࡃࠢᇅ") + str(hub_url) + bstack1l1l1l1_opy_ (u"ࠢࠣᇆ"))
                bstack1llll11lll1_opy_.bstack1ll11l1llll_opy_ = True
            return
        bstack1ll11lll1l1_opy_ = f.bstack1ll11l1ll11_opy_(*args)
        bstack1ll111l11ll_opy_ = f.bstack1ll111l11l1_opy_(*args)
        if bstack1ll11lll1l1_opy_ and bstack1ll11lll1l1_opy_.lower() == bstack1l1l1l1_opy_ (u"ࠣࡨ࡬ࡲࡩ࡫࡬ࡦ࡯ࡨࡲࡹࠨᇇ") and bstack1ll111l11ll_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll111l11ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠤࡸࡷ࡮ࡴࡧࠣᇈ"), None), bstack1ll111l11ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤᇉ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠦࢀࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࢁ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠠࡰࡴࠣࡥࡷ࡭ࡳ࠯ࡷࡶ࡭ࡳ࡭࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡࡱࡵࠤࡦࡸࡧࡴ࠰ࡹࡥࡱࡻࡥ࠾ࠤᇊ") + str(locator_value) + bstack1l1l1l1_opy_ (u"ࠧࠨᇋ"))
                return
            def bstack1lllll11lll_opy_(driver, bstack1ll111ll111_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll111ll111_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll1111llll_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1l1l1l1_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࠤᇌ") + str(locator_value) + bstack1l1l1l1_opy_ (u"ࠢࠣᇍ"))
                    else:
                        self.logger.warning(bstack1l1l1l1_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴ࠯ࡱࡳ࠲ࡹࡣࡳ࡫ࡳࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫ࡽࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࡀࠦᇎ") + str(response) + bstack1l1l1l1_opy_ (u"ࠤࠥᇏ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll111l111l_opy_(
                        driver, bstack1ll111ll111_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1lllll11lll_opy_.__name__ = bstack1ll11lll1l1_opy_
            return bstack1lllll11lll_opy_
    def __1ll111l111l_opy_(
        self,
        driver,
        bstack1ll111ll111_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1ll1111llll_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1l1l1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡺࡲࡪࡩࡪࡩࡷ࡫ࡤ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࠥᇐ") + str(locator_value) + bstack1l1l1l1_opy_ (u"ࠦࠧᇑ"))
                bstack1ll111l1ll1_opy_ = self.bstack1ll1111lll1_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1l1l1l1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣ࡬ࡪࡧ࡬ࡪࡰࡪࡣࡷ࡫ࡳࡶ࡮ࡷࡁࠧᇒ") + str(bstack1ll111l1ll1_opy_) + bstack1l1l1l1_opy_ (u"ࠨࠢᇓ"))
                if bstack1ll111l1ll1_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1l1l1l1_opy_ (u"ࠢࡶࡵ࡬ࡲ࡬ࠨᇔ"): bstack1ll111l1ll1_opy_.locator_type,
                            bstack1l1l1l1_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᇕ"): bstack1ll111l1ll1_opy_.locator_value,
                        }
                    )
                    return bstack1ll111ll111_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1l1l1l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡌࡣࡉࡋࡂࡖࡉࠥᇖ"), False):
                    self.logger.info(bstack1llll1l11l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡸࡥࡴࡷ࡯ࡸ࠲ࡳࡩࡴࡵ࡬ࡲ࡬ࡀࠠࡴ࡮ࡨࡩࡵ࠮࠳࠱ࠫࠣࡰࡪࡺࡴࡪࡰࡪࠤࡾࡵࡵࠡ࡫ࡱࡷࡵ࡫ࡣࡵࠢࡷ࡬ࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡦࡺࡷࡩࡳࡹࡩࡰࡰࠣࡰࡴ࡭ࡳࠣᇗ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲ࡴ࡯࠮ࡵࡦࡶ࡮ࡶࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࢀࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡃࠢᇘ") + str(response) + bstack1l1l1l1_opy_ (u"ࠧࠨᇙ"))
        except Exception as err:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭ࡩࡧࡤࡰ࡮ࡴࡧ࠮ࡴࡨࡷࡺࡲࡴ࠻ࠢࡨࡶࡷࡵࡲ࠻ࠢࠥᇚ") + str(err) + bstack1l1l1l1_opy_ (u"ࠢࠣᇛ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll111l1l11_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
    def bstack1ll1111llll_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1l1l1l1_opy_ (u"ࠣ࠲ࠥᇜ"),
    ):
        self.bstack1ll11l1l1ll_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1l1l1l1_opy_ (u"ࠤࠥᇝ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1ll1ll111l1_opy_.AISelfHealStep(req)
            self.logger.info(bstack1l1l1l1_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᇞ") + str(r) + bstack1l1l1l1_opy_ (u"ࠦࠧᇟ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᇠ") + str(e) + bstack1l1l1l1_opy_ (u"ࠨࠢᇡ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll111l1lll_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
    def bstack1ll1111lll1_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1l1l1l1_opy_ (u"ࠢ࠱ࠤᇢ")):
        self.bstack1ll11l1l1ll_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1ll1ll111l1_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1l1l1l1_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᇣ") + str(r) + bstack1l1l1l1_opy_ (u"ࠤࠥᇤ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᇥ") + str(e) + bstack1l1l1l1_opy_ (u"ࠦࠧᇦ"))
            traceback.print_exc()
            raise e