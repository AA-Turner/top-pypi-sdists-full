# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack1lll1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import (
    bstack1lll1llllll_opy_,
    bstack1llllll1l1l_opy_,
    bstack1lll1llll11_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l11l1l_opy_ import bstack1lll1ll1l1l_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack1lll1lllll1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1lll111111l_opy_(bstack1lll1lllll1_opy_):
    bstack1lll111ll11_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1lll1ll1l1l_opy_.bstack1lllll1llll_opy_((bstack1lll1llllll_opy_.bstack1llll1lll11_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1lll111l1ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1lll111l1ll_opy_(
        self,
        f: bstack1lll1ll1l1l_opy_,
        driver: object,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1lll1111l11_opy_(hub_url):
            if not bstack1lll111111l_opy_.bstack1lll111ll11_opy_:
                self.logger.warning(bstack11l1111_opy_ (u"ࠣ࡮ࡲࡧࡦࡲࠠࡴࡧ࡯ࡪ࠲࡮ࡥࡢ࡮ࠣࡪࡱࡵࡷࠡࡦ࡬ࡷࡦࡨ࡬ࡦࡦࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡩ࡯ࡨࡵࡥࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡩࡷࡥࡣࡺࡸ࡬࠾ࠤᄟ") + str(hub_url) + bstack11l1111_opy_ (u"ࠤࠥᄠ"))
                bstack1lll111111l_opy_.bstack1lll111ll11_opy_ = True
            return
        bstack1lll1111ll1_opy_ = f.bstack1lllll1ll11_opy_(*args)
        bstack1lll1111111_opy_ = f.bstack1lll111llll_opy_(*args)
        if bstack1lll1111ll1_opy_ and bstack1lll1111ll1_opy_.lower() == bstack11l1111_opy_ (u"ࠥࡪ࡮ࡴࡤࡦ࡮ࡨࡱࡪࡴࡴࠣᄡ") and bstack1lll1111111_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1lll1111111_opy_.get(bstack11l1111_opy_ (u"ࠦࡺࡹࡩ࡯ࡩࠥᄢ"), None), bstack1lll1111111_opy_.get(bstack11l1111_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᄣ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack11l1111_opy_ (u"ࠨࡻࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࢃ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡲࡶࠥࡧࡲࡨࡵ࠱ࡹࡸ࡯࡮ࡨ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡳࡷࠦࡡࡳࡩࡶ࠲ࡻࡧ࡬ࡶࡧࡀࠦᄤ") + str(locator_value) + bstack11l1111_opy_ (u"ࠢࠣᄥ"))
                return
            def bstack1lll11111l1_opy_(driver, bstack1lll111ll1l_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1lll111ll1l_opy_(driver, *args, **kwargs)
                    response = self.bstack1lll111l11l_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack11l1111_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴ࠯ࡶࡧࡷ࡯ࡰࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࠦᄦ") + str(locator_value) + bstack11l1111_opy_ (u"ࠤࠥᄧ"))
                    else:
                        self.logger.warning(bstack11l1111_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶ࠱ࡳࡵ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣࡶࡪࡹࡰࡰࡰࡶࡩࡂࠨᄨ") + str(response) + bstack11l1111_opy_ (u"ࠦࠧᄩ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1lll111l111_opy_(
                        driver, bstack1lll111ll1l_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1lll11111l1_opy_.__name__ = bstack1lll1111ll1_opy_
            return bstack1lll11111l1_opy_
    def __1lll111l111_opy_(
        self,
        driver,
        bstack1lll111ll1l_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1lll111l11l_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack11l1111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡵࡴ࡬࡫࡬࡫ࡲࡦࡦ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࠧᄪ") + str(locator_value) + bstack11l1111_opy_ (u"ࠨࠢᄫ"))
                bstack1lll11111ll_opy_ = self.bstack1lll1111l1l_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack11l1111_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡵࡩࡸࡻ࡬ࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࢁࠥ࡮ࡥࡢ࡮࡬ࡲ࡬ࡥࡲࡦࡵࡸࡰࡹࡃࠢᄬ") + str(bstack1lll11111ll_opy_) + bstack11l1111_opy_ (u"ࠣࠤᄭ"))
                if bstack1lll11111ll_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack11l1111_opy_ (u"ࠤࡸࡷ࡮ࡴࡧࠣᄮ"): bstack1lll11111ll_opy_.locator_type,
                            bstack11l1111_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤᄯ"): bstack1lll11111ll_opy_.locator_value,
                        }
                    )
                    return bstack1lll111ll1l_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack11l1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡎࡥࡄࡆࡄࡘࡋࠧᄰ"), False):
                    self.logger.info(bstack1lll1111lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠭࡮࡫ࡶࡷ࡮ࡴࡧ࠻ࠢࡶࡰࡪ࡫ࡰࠩ࠵࠳࠭ࠥࡲࡥࡵࡶ࡬ࡲ࡬ࠦࡹࡰࡷࠣ࡭ࡳࡹࡰࡦࡥࡷࠤࡹ࡮ࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࠥࡲ࡯ࡨࡵࠥᄱ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack11l1111_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭࡯ࡱ࠰ࡷࡨࡸࡩࡱࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠾ࠤᄲ") + str(response) + bstack11l1111_opy_ (u"ࠢࠣᄳ"))
        except Exception as err:
            self.logger.warning(bstack11l1111_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡶࡪࡹࡵ࡭ࡶ࠽ࠤࡪࡸࡲࡰࡴ࠽ࠤࠧᄴ") + str(err) + bstack11l1111_opy_ (u"ࠤࠥᄵ"))
        raise exception
    @measure(event_name=EVENTS.bstack1lll11l1111_opy_, stage=STAGE.bstack1111llll1_opy_)
    def bstack1lll111l11l_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack11l1111_opy_ (u"ࠥ࠴ࠧᄶ"),
    ):
        self.bstack1lll1lll1l1_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack11l1111_opy_ (u"ࠦࠧᄷ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1lll1llll1l_opy_.AISelfHealStep(req)
            self.logger.info(bstack11l1111_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᄸ") + str(r) + bstack11l1111_opy_ (u"ࠨࠢᄹ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1111_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᄺ") + str(e) + bstack11l1111_opy_ (u"ࠣࠤᄻ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1lll111l1l1_opy_, stage=STAGE.bstack1111llll1_opy_)
    def bstack1lll1111l1l_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack11l1111_opy_ (u"ࠤ࠳ࠦᄼ")):
        self.bstack1lll1lll1l1_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1lll1llll1l_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack11l1111_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᄽ") + str(r) + bstack11l1111_opy_ (u"ࠦࠧᄾ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1111_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᄿ") + str(e) + bstack11l1111_opy_ (u"ࠨࠢᅀ"))
            traceback.print_exc()
            raise e