# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
from browserstack_sdk.sdk_cli.bstack1ll1l1l1ll1_opy_ import bstack1ll1l1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lllll111ll_opy_ import (
    bstack1llllllllll_opy_,
    bstack1llllllll1l_opy_,
    bstack11111111l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll11lll11_opy_ import bstack1ll1l1lll11_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll1l1l1ll1_opy_ import bstack1ll1l1ll1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1llll1l1l1l_opy_(bstack1ll1l1ll1ll_opy_):
    bstack1ll111l11l1_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1ll1l1lll11_opy_.bstack1ll1l11ll1l_opy_((bstack1llllllllll_opy_.bstack1llllll1l11_opy_, bstack1llllllll1l_opy_.PRE), self.bstack1ll11111ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11111ll1_opy_(
        self,
        f: bstack1ll1l1lll11_opy_,
        driver: object,
        exec: Tuple[bstack11111111l1_opy_, str],
        bstack1lllll1l1ll_opy_: Tuple[bstack1llllllllll_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1ll111111l1_opy_(hub_url):
            if not bstack1llll1l1l1l_opy_.bstack1ll111l11l1_opy_:
                self.logger.warning(bstackl_opy_ (u"ࠧࡲ࡯ࡤࡣ࡯ࠤࡸ࡫࡬ࡧ࠯࡫ࡩࡦࡲࠠࡧ࡮ࡲࡻࠥࡪࡩࡴࡣࡥࡰࡪࡪࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣ࡭ࡳ࡬ࡲࡢࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤ࡭ࡻࡢࡠࡷࡵࡰࡂࠨሟ") + str(hub_url) + bstackl_opy_ (u"ࠨࠢሠ"))
                bstack1llll1l1l1l_opy_.bstack1ll111l11l1_opy_ = True
            return
        bstack1ll11l1llll_opy_ = f.bstack1ll11l1ll1l_opy_(*args)
        bstack1ll1111l11l_opy_ = f.bstack1ll1111111l_opy_(*args)
        if bstack1ll11l1llll_opy_ and bstack1ll11l1llll_opy_.lower() == bstackl_opy_ (u"ࠢࡧ࡫ࡱࡨࡪࡲࡥ࡮ࡧࡱࡸࠧሡ") and bstack1ll1111l11l_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll1111l11l_opy_.get(bstackl_opy_ (u"ࠣࡷࡶ࡭ࡳ࡭ࠢሢ"), None), bstack1ll1111l11l_opy_.get(bstackl_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣሣ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstackl_opy_ (u"ࠥࡿࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࢀ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠦ࡯ࡳࠢࡤࡶ࡬ࡹ࠮ࡶࡵ࡬ࡲ࡬ࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠࡰࡴࠣࡥࡷ࡭ࡳ࠯ࡸࡤࡰࡺ࡫࠽ࠣሤ") + str(locator_value) + bstackl_opy_ (u"ࠦࠧሥ"))
                return
            def bstack1lllll11ll1_opy_(driver, bstack1ll111111ll_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll111111ll_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll1111l1ll_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstackl_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࠣሦ") + str(locator_value) + bstackl_opy_ (u"ࠨࠢሧ"))
                    else:
                        self.logger.warning(bstackl_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳ࠮ࡰࡲ࠱ࡸࡩࡲࡪࡲࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࢃࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠿ࠥረ") + str(response) + bstackl_opy_ (u"ࠣࠤሩ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll1111l1l1_opy_(
                        driver, bstack1ll111111ll_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1lllll11ll1_opy_.__name__ = bstack1ll11l1llll_opy_
            return bstack1lllll11ll1_opy_
    def __1ll1111l1l1_opy_(
        self,
        driver,
        bstack1ll111111ll_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1ll1111l1ll_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstackl_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡹࡸࡩࡨࡩࡨࡶࡪࡪ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࠤሪ") + str(locator_value) + bstackl_opy_ (u"ࠥࠦራ"))
                bstack1ll1111l111_opy_ = self.bstack1ll11111l1l_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstackl_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢ࡫ࡩࡦࡲࡩ࡯ࡩࡢࡶࡪࡹࡵ࡭ࡶࡀࠦሬ") + str(bstack1ll1111l111_opy_) + bstackl_opy_ (u"ࠧࠨር"))
                if bstack1ll1111l111_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstackl_opy_ (u"ࠨࡵࡴ࡫ࡱ࡫ࠧሮ"): bstack1ll1111l111_opy_.locator_type,
                            bstackl_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨሯ"): bstack1ll1111l111_opy_.locator_value,
                        }
                    )
                    return bstack1ll111111ll_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstackl_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡋࡢࡈࡊࡈࡕࡈࠤሰ"), False):
                    self.logger.info(bstack1lll11l1l1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡷ࡫ࡳࡶ࡮ࡷ࠱ࡲ࡯ࡳࡴ࡫ࡱ࡫࠿ࠦࡳ࡭ࡧࡨࡴ࠭࠹࠰ࠪࠢ࡯ࡩࡹࡺࡩ࡯ࡩࠣࡽࡴࡻࠠࡪࡰࡶࡴࡪࡩࡴࠡࡶ࡫ࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࠢ࡯ࡳ࡬ࡹࠢሱ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstackl_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱ࡳࡵ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣࡶࡪࡹࡰࡰࡰࡶࡩࡂࠨሲ") + str(response) + bstackl_opy_ (u"ࠦࠧሳ"))
        except Exception as err:
            self.logger.warning(bstackl_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠺ࠡࡧࡵࡶࡴࡸ࠺ࠡࠤሴ") + str(err) + bstackl_opy_ (u"ࠨࠢስ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll11111l11_opy_, stage=STAGE.bstack1l1111ll1_opy_)
    def bstack1ll1111l1ll_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstackl_opy_ (u"ࠢ࠱ࠤሶ"),
    ):
        self.bstack1ll111llll1_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstackl_opy_ (u"ࠣࠤሷ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1lll1l1l1ll_opy_.AISelfHealStep(req)
            self.logger.info(bstackl_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦሸ") + str(r) + bstackl_opy_ (u"ࠥࠦሹ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstackl_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤሺ") + str(e) + bstackl_opy_ (u"ࠧࠨሻ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll11111lll_opy_, stage=STAGE.bstack1l1111ll1_opy_)
    def bstack1ll11111l1l_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstackl_opy_ (u"ࠨ࠰ࠣሼ")):
        self.bstack1ll111llll1_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1lll1l1l1ll_opy_.AISelfHealGetResult(req)
            self.logger.info(bstackl_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤሽ") + str(r) + bstackl_opy_ (u"ࠣࠤሾ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstackl_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢሿ") + str(e) + bstackl_opy_ (u"ࠥࠦቀ"))
            traceback.print_exc()
            raise e