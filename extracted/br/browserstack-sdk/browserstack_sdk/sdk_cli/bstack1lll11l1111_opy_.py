# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
from browserstack_sdk.sdk_cli.bstack1ll1lll11l1_opy_ import bstack1lll1l11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1111_opy_ import (
    bstack1111111111_opy_,
    bstack11111l1ll1_opy_,
    bstack1llllll111l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1lll1l11_opy_ import bstack1llll111lll_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll1lll11l1_opy_ import bstack1lll1l11ll1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1ll1lll1ll1_opy_(bstack1lll1l11ll1_opy_):
    bstack1ll11lllll1_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1llll111lll_opy_.bstack1ll11ll1l1l_opy_((bstack1111111111_opy_.bstack111111lll1_opy_, bstack11111l1ll1_opy_.PRE), self.bstack1ll11l111ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11l111ll_opy_(
        self,
        f: bstack1llll111lll_opy_,
        driver: object,
        exec: Tuple[bstack1llllll111l_opy_, str],
        bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1ll111llll1_opy_(hub_url):
            if not bstack1ll1lll1ll1_opy_.bstack1ll11lllll1_opy_:
                self.logger.warning(bstack111lll_opy_ (u"ࠧࡲ࡯ࡤࡣ࡯ࠤࡸ࡫࡬ࡧ࠯࡫ࡩࡦࡲࠠࡧ࡮ࡲࡻࠥࡪࡩࡴࡣࡥࡰࡪࡪࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣ࡭ࡳ࡬ࡲࡢࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤ࡭ࡻࡢࡠࡷࡵࡰࡂࠨᆶ") + str(hub_url) + bstack111lll_opy_ (u"ࠨࠢᆷ"))
                bstack1ll1lll1ll1_opy_.bstack1ll11lllll1_opy_ = True
            return
        bstack1ll1l11111l_opy_ = f.bstack1ll1l111lll_opy_(*args)
        bstack1ll11l11ll1_opy_ = f.bstack1ll11l11lll_opy_(*args)
        if bstack1ll1l11111l_opy_ and bstack1ll1l11111l_opy_.lower() == bstack111lll_opy_ (u"ࠢࡧ࡫ࡱࡨࡪࡲࡥ࡮ࡧࡱࡸࠧᆸ") and bstack1ll11l11ll1_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll11l11ll1_opy_.get(bstack111lll_opy_ (u"ࠣࡷࡶ࡭ࡳ࡭ࠢᆹ"), None), bstack1ll11l11ll1_opy_.get(bstack111lll_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣᆺ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack111lll_opy_ (u"ࠥࡿࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࢀ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠦ࡯ࡳࠢࡤࡶ࡬ࡹ࠮ࡶࡵ࡬ࡲ࡬ࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠࡰࡴࠣࡥࡷ࡭ࡳ࠯ࡸࡤࡰࡺ࡫࠽ࠣᆻ") + str(locator_value) + bstack111lll_opy_ (u"ࠦࠧᆼ"))
                return
            def bstack1llllll11ll_opy_(driver, bstack1ll11l1111l_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll11l1111l_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll11l11111_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack111lll_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࠣᆽ") + str(locator_value) + bstack111lll_opy_ (u"ࠨࠢᆾ"))
                    else:
                        self.logger.warning(bstack111lll_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳ࠮ࡰࡲ࠱ࡸࡩࡲࡪࡲࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࢃࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠿ࠥᆿ") + str(response) + bstack111lll_opy_ (u"ࠣࠤᇀ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll111lllll_opy_(
                        driver, bstack1ll11l1111l_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1llllll11ll_opy_.__name__ = bstack1ll1l11111l_opy_
            return bstack1llllll11ll_opy_
    def __1ll111lllll_opy_(
        self,
        driver,
        bstack1ll11l1111l_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1ll11l11111_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack111lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡹࡸࡩࡨࡩࡨࡶࡪࡪ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࠤᇁ") + str(locator_value) + bstack111lll_opy_ (u"ࠥࠦᇂ"))
                bstack1ll111lll1l_opy_ = self.bstack1ll11l11l1l_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack111lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢ࡫ࡩࡦࡲࡩ࡯ࡩࡢࡶࡪࡹࡵ࡭ࡶࡀࠦᇃ") + str(bstack1ll111lll1l_opy_) + bstack111lll_opy_ (u"ࠧࠨᇄ"))
                if bstack1ll111lll1l_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack111lll_opy_ (u"ࠨࡵࡴ࡫ࡱ࡫ࠧᇅ"): bstack1ll111lll1l_opy_.locator_type,
                            bstack111lll_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨᇆ"): bstack1ll111lll1l_opy_.locator_value,
                        }
                    )
                    return bstack1ll11l1111l_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack111lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡋࡢࡈࡊࡈࡕࡈࠤᇇ"), False):
                    self.logger.info(bstack1lllll111l1_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡷ࡫ࡳࡶ࡮ࡷ࠱ࡲ࡯ࡳࡴ࡫ࡱ࡫࠿ࠦࡳ࡭ࡧࡨࡴ࠭࠹࠰ࠪࠢ࡯ࡩࡹࡺࡩ࡯ࡩࠣࡽࡴࡻࠠࡪࡰࡶࡴࡪࡩࡴࠡࡶ࡫ࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࠢ࡯ࡳ࡬ࡹࠢᇈ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack111lll_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱ࡳࡵ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣࡶࡪࡹࡰࡰࡰࡶࡩࡂࠨᇉ") + str(response) + bstack111lll_opy_ (u"ࠦࠧᇊ"))
        except Exception as err:
            self.logger.warning(bstack111lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠺ࠡࡧࡵࡶࡴࡸ࠺ࠡࠤᇋ") + str(err) + bstack111lll_opy_ (u"ࠨࠢᇌ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll11l11l11_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack1ll11l11111_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack111lll_opy_ (u"ࠢ࠱ࠤᇍ"),
    ):
        self.bstack1ll11ll1l11_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack111lll_opy_ (u"ࠣࠤᇎ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1lll1ll1l11_opy_.AISelfHealStep(req)
            self.logger.info(bstack111lll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᇏ") + str(r) + bstack111lll_opy_ (u"ࠥࠦᇐ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111lll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᇑ") + str(e) + bstack111lll_opy_ (u"ࠧࠨᇒ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll11l111l1_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack1ll11l11l1l_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack111lll_opy_ (u"ࠨ࠰ࠣᇓ")):
        self.bstack1ll11ll1l11_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1lll1ll1l11_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack111lll_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᇔ") + str(r) + bstack111lll_opy_ (u"ࠣࠤᇕ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111lll_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᇖ") + str(e) + bstack111lll_opy_ (u"ࠥࠦᇗ"))
            traceback.print_exc()
            raise e