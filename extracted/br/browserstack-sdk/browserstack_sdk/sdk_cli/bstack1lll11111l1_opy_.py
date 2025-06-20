# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1ll1ll1llll_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1lll1_opy_ import (
    bstack1111111l11_opy_,
    bstack1llllll1111_opy_,
    bstack1llll1ll1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1ll1l1ll_opy_ import bstack1llll11l111_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1ll1ll1llll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1lll1ll111l_opy_(bstack1ll1ll1llll_opy_):
    bstack1ll111lll1l_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1llll11l111_opy_.bstack1ll1l11l1l1_opy_((bstack1111111l11_opy_.bstack1lllll11lll_opy_, bstack1llllll1111_opy_.PRE), self.bstack1ll111l1l11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll111l1l11_opy_(
        self,
        f: bstack1llll11l111_opy_,
        driver: object,
        exec: Tuple[bstack1llll1ll1ll_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1111111l11_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1ll111l1l1l_opy_(hub_url):
            if not bstack1lll1ll111l_opy_.bstack1ll111lll1l_opy_:
                self.logger.warning(bstack11ll11_opy_ (u"ࠧࡲ࡯ࡤࡣ࡯ࠤࡸ࡫࡬ࡧ࠯࡫ࡩࡦࡲࠠࡧ࡮ࡲࡻࠥࡪࡩࡴࡣࡥࡰࡪࡪࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣ࡭ࡳ࡬ࡲࡢࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤ࡭ࡻࡢࡠࡷࡵࡰࡂࠨᇄ") + str(hub_url) + bstack11ll11_opy_ (u"ࠨࠢᇅ"))
                bstack1lll1ll111l_opy_.bstack1ll111lll1l_opy_ = True
            return
        bstack1ll11ll1lll_opy_ = f.bstack1ll11l1ll1l_opy_(*args)
        bstack1ll1111lll1_opy_ = f.bstack1ll111l1ll1_opy_(*args)
        if bstack1ll11ll1lll_opy_ and bstack1ll11ll1lll_opy_.lower() == bstack11ll11_opy_ (u"ࠢࡧ࡫ࡱࡨࡪࡲࡥ࡮ࡧࡱࡸࠧᇆ") and bstack1ll1111lll1_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll1111lll1_opy_.get(bstack11ll11_opy_ (u"ࠣࡷࡶ࡭ࡳ࡭ࠢᇇ"), None), bstack1ll1111lll1_opy_.get(bstack11ll11_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣᇈ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack11ll11_opy_ (u"ࠥࡿࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࢀ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠦ࡯ࡳࠢࡤࡶ࡬ࡹ࠮ࡶࡵ࡬ࡲ࡬ࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠࡰࡴࠣࡥࡷ࡭ࡳ࠯ࡸࡤࡰࡺ࡫࠽ࠣᇉ") + str(locator_value) + bstack11ll11_opy_ (u"ࠦࠧᇊ"))
                return
            def bstack1llll1llll1_opy_(driver, bstack1ll111l1111_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll111l1111_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll1111llll_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack11ll11_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࠣᇋ") + str(locator_value) + bstack11ll11_opy_ (u"ࠨࠢᇌ"))
                    else:
                        self.logger.warning(bstack11ll11_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳ࠮ࡰࡲ࠱ࡸࡩࡲࡪࡲࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࢃࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠿ࠥᇍ") + str(response) + bstack11ll11_opy_ (u"ࠣࠤᇎ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll111l11l1_opy_(
                        driver, bstack1ll111l1111_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1llll1llll1_opy_.__name__ = bstack1ll11ll1lll_opy_
            return bstack1llll1llll1_opy_
    def __1ll111l11l1_opy_(
        self,
        driver,
        bstack1ll111l1111_opy_: Callable,
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
                self.logger.info(bstack11ll11_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡹࡸࡩࡨࡩࡨࡶࡪࡪ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࠤᇏ") + str(locator_value) + bstack11ll11_opy_ (u"ࠥࠦᇐ"))
                bstack1ll111ll111_opy_ = self.bstack1ll111l111l_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack11ll11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢ࡫ࡩࡦࡲࡩ࡯ࡩࡢࡶࡪࡹࡵ࡭ࡶࡀࠦᇑ") + str(bstack1ll111ll111_opy_) + bstack11ll11_opy_ (u"ࠧࠨᇒ"))
                if bstack1ll111ll111_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack11ll11_opy_ (u"ࠨࡵࡴ࡫ࡱ࡫ࠧᇓ"): bstack1ll111ll111_opy_.locator_type,
                            bstack11ll11_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨᇔ"): bstack1ll111ll111_opy_.locator_value,
                        }
                    )
                    return bstack1ll111l1111_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack11ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡋࡢࡈࡊࡈࡕࡈࠤᇕ"), False):
                    self.logger.info(bstack1lll11ll111_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡷ࡫ࡳࡶ࡮ࡷ࠱ࡲ࡯ࡳࡴ࡫ࡱ࡫࠿ࠦࡳ࡭ࡧࡨࡴ࠭࠹࠰ࠪࠢ࡯ࡩࡹࡺࡩ࡯ࡩࠣࡽࡴࡻࠠࡪࡰࡶࡴࡪࡩࡴࠡࡶ࡫ࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࠢ࡯ࡳ࡬ࡹࠢᇖ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack11ll11_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱ࡳࡵ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣࡶࡪࡹࡰࡰࡰࡶࡩࡂࠨᇗ") + str(response) + bstack11ll11_opy_ (u"ࠦࠧᇘ"))
        except Exception as err:
            self.logger.warning(bstack11ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠺ࠡࡧࡵࡶࡴࡸ࠺ࠡࠤᇙ") + str(err) + bstack11ll11_opy_ (u"ࠨࠢᇚ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll111l11ll_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def bstack1ll1111llll_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack11ll11_opy_ (u"ࠢ࠱ࠤᇛ"),
    ):
        self.bstack1ll1l1l1111_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack11ll11_opy_ (u"ࠣࠤᇜ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1llll1l1l11_opy_.AISelfHealStep(req)
            self.logger.info(bstack11ll11_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᇝ") + str(r) + bstack11ll11_opy_ (u"ࠥࠦᇞ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᇟ") + str(e) + bstack11ll11_opy_ (u"ࠧࠨᇠ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll111l1lll_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def bstack1ll111l111l_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack11ll11_opy_ (u"ࠨ࠰ࠣᇡ")):
        self.bstack1ll1l1l1111_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1llll1l1l11_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack11ll11_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᇢ") + str(r) + bstack11ll11_opy_ (u"ࠣࠤᇣ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᇤ") + str(e) + bstack11ll11_opy_ (u"ࠥࠦᇥ"))
            traceback.print_exc()
            raise e