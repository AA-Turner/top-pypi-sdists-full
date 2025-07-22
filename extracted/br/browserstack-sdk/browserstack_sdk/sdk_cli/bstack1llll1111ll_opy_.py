# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
from browserstack_sdk.sdk_cli.bstack1lll1l1111l_opy_ import bstack1llll1l1l11_opy_
from browserstack_sdk.sdk_cli.bstack1llll1lll1l_opy_ import (
    bstack1lllllll11l_opy_,
    bstack1llllll1111_opy_,
    bstack1lllll1ll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll1l1111_opy_ import bstack1lll1l11l11_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll1l1111l_opy_ import bstack1llll1l1l11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1lll111111l_opy_(bstack1llll1l1l11_opy_):
    bstack1ll111lll1l_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1lll1l11l11_opy_.bstack1ll11l1l11l_opy_((bstack1lllllll11l_opy_.bstack1llllll11ll_opy_, bstack1llllll1111_opy_.PRE), self.bstack1ll11111l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11111l1l_opy_(
        self,
        f: bstack1lll1l11l11_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1ll11111lll_opy_(hub_url):
            if not bstack1lll111111l_opy_.bstack1ll111lll1l_opy_:
                self.logger.warning(bstack111l111_opy_ (u"ࠦࡱࡵࡣࡢ࡮ࠣࡷࡪࡲࡦ࠮ࡪࡨࡥࡱࠦࡦ࡭ࡱࡺࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢ࡬ࡲ࡫ࡸࡡࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧሞ") + str(hub_url) + bstack111l111_opy_ (u"ࠧࠨሟ"))
                bstack1lll111111l_opy_.bstack1ll111lll1l_opy_ = True
            return
        bstack1ll1l11l111_opy_ = f.bstack1ll11llllll_opy_(*args)
        bstack1ll1111l1ll_opy_ = f.bstack1ll111111ll_opy_(*args)
        if bstack1ll1l11l111_opy_ and bstack1ll1l11l111_opy_.lower() == bstack111l111_opy_ (u"ࠨࡦࡪࡰࡧࡩࡱ࡫࡭ࡦࡰࡷࠦሠ") and bstack1ll1111l1ll_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll1111l1ll_opy_.get(bstack111l111_opy_ (u"ࠢࡶࡵ࡬ࡲ࡬ࠨሡ"), None), bstack1ll1111l1ll_opy_.get(bstack111l111_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢሢ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack111l111_opy_ (u"ࠤࡾࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦࡿ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡵࡲࠡࡣࡵ࡫ࡸ࠴ࡵࡴ࡫ࡱ࡫ࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡯ࡳࠢࡤࡶ࡬ࡹ࠮ࡷࡣ࡯ࡹࡪࡃࠢሣ") + str(locator_value) + bstack111l111_opy_ (u"ࠥࠦሤ"))
                return
            def bstack1lllll11111_opy_(driver, bstack1ll1111l1l1_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll1111l1l1_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll11111ll1_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack111l111_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷ࠲ࡹࡣࡳ࡫ࡳࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࠢሥ") + str(locator_value) + bstack111l111_opy_ (u"ࠧࠨሦ"))
                    else:
                        self.logger.warning(bstack111l111_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹ࠭࡯ࡱ࠰ࡷࡨࡸࡩࡱࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠾ࠤሧ") + str(response) + bstack111l111_opy_ (u"ࠢࠣረ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll1111l11l_opy_(
                        driver, bstack1ll1111l1l1_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1lllll11111_opy_.__name__ = bstack1ll1l11l111_opy_
            return bstack1lllll11111_opy_
    def __1ll1111l11l_opy_(
        self,
        driver,
        bstack1ll1111l1l1_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1ll11111ll1_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack111l111_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡸࡷ࡯ࡧࡨࡧࡵࡩࡩࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࠣሩ") + str(locator_value) + bstack111l111_opy_ (u"ࠤࠥሪ"))
                bstack1ll1111l111_opy_ = self.bstack1ll11111l11_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack111l111_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡸࡥࡴࡷ࡯ࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫ࡽࠡࡪࡨࡥࡱ࡯࡮ࡨࡡࡵࡩࡸࡻ࡬ࡵ࠿ࠥራ") + str(bstack1ll1111l111_opy_) + bstack111l111_opy_ (u"ࠦࠧሬ"))
                if bstack1ll1111l111_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack111l111_opy_ (u"ࠧࡻࡳࡪࡰࡪࠦር"): bstack1ll1111l111_opy_.locator_type,
                            bstack111l111_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧሮ"): bstack1ll1111l111_opy_.locator_value,
                        }
                    )
                    return bstack1ll1111l1l1_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack111l111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡊࡡࡇࡉࡇ࡛ࡇࠣሯ"), False):
                    self.logger.info(bstack1lll11l11ll_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡶࡪࡹࡵ࡭ࡶ࠰ࡱ࡮ࡹࡳࡪࡰࡪ࠾ࠥࡹ࡬ࡦࡧࡳࠬ࠸࠶ࠩࠡ࡮ࡨࡸࡹ࡯࡮ࡨࠢࡼࡳࡺࠦࡩ࡯ࡵࡳࡩࡨࡺࠠࡵࡪࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࠡ࡮ࡲ࡫ࡸࠨሰ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack111l111_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰ࡲࡴ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࡁࠧሱ") + str(response) + bstack111l111_opy_ (u"ࠥࠦሲ"))
        except Exception as err:
            self.logger.warning(bstack111l111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹࡀࠠࡦࡴࡵࡳࡷࡀࠠࠣሳ") + str(err) + bstack111l111_opy_ (u"ࠧࠨሴ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll111111l1_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def bstack1ll11111ll1_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack111l111_opy_ (u"ࠨ࠰ࠣስ"),
    ):
        self.bstack1ll111l1l11_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack111l111_opy_ (u"ࠢࠣሶ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1lll1l11l1l_opy_.AISelfHealStep(req)
            self.logger.info(bstack111l111_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥሷ") + str(r) + bstack111l111_opy_ (u"ࠤࠥሸ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111l111_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣሹ") + str(e) + bstack111l111_opy_ (u"ࠦࠧሺ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll1111ll11_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def bstack1ll11111l11_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack111l111_opy_ (u"ࠧ࠶ࠢሻ")):
        self.bstack1ll111l1l11_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1lll1l11l1l_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack111l111_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣሼ") + str(r) + bstack111l111_opy_ (u"ࠢࠣሽ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111l111_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨሾ") + str(e) + bstack111l111_opy_ (u"ࠤࠥሿ"))
            traceback.print_exc()
            raise e