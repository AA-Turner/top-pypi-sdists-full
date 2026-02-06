# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
from browserstack_sdk.sdk_cli.bstack1lll1lll1l1_opy_ import bstack1lll1l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1ll11_opy_ import (
    bstack1lll1l1ll1l_opy_,
    bstack1lll1ll11ll_opy_,
    bstack1lll1l1l11l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l11ll1_opy_ import bstack1lll11lllll_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll1lll1l1_opy_ import bstack1lll1l1l1l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack11lll1l11l_opy_ import bstack1lll11l1ll_opy_
import traceback
import os
import threading
import time
class bstack1ll1l1ll11l_opy_(bstack1lll1l1l1l1_opy_):
    bstack1l1l1lll1l1_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1lll11lllll_opy_.bstack1lll1l1l1ll_opy_((bstack1lll1l1ll1l_opy_.bstack1lll1ll111l_opy_, bstack1lll1ll11ll_opy_.PRE), self.bstack1l1l1l111ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1l111ll_opy_(
        self,
        f: bstack1lll11lllll_opy_,
        driver: object,
        exec: Tuple[bstack1lll1l1l11l_opy_, str],
        bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1lll1ll11l1_opy_(hub_url):
            if not bstack1ll1l1ll11l_opy_.bstack1l1l1lll1l1_opy_:
                self.logger.warning(bstack11lllll_opy_ (u"ࠧࡲ࡯ࡤࡣ࡯ࠤࡸ࡫࡬ࡧ࠯࡫ࡩࡦࡲࠠࡧ࡮ࡲࡻࠥࡪࡩࡴࡣࡥࡰࡪࡪࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣ࡭ࡳ࡬ࡲࡢࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤ࡭ࡻࡢࡠࡷࡵࡰࡂࠨጾ") + str(hub_url) + bstack11lllll_opy_ (u"ࠨࠢጿ"))
                bstack1ll1l1ll11l_opy_.bstack1l1l1lll1l1_opy_ = True
            return
        command_name = f.bstack1l1l1lll11l_opy_(*args)
        bstack1l1l1l11lll_opy_ = f.bstack1l1l1l11l11_opy_(*args)
        if command_name and command_name.lower() == bstack11lllll_opy_ (u"ࠢࡧ࡫ࡱࡨࡪࡲࡥ࡮ࡧࡱࡸࠧፀ") and bstack1l1l1l11lll_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1l1l1l11lll_opy_.get(bstack11lllll_opy_ (u"ࠣࡷࡶ࡭ࡳ࡭ࠢፁ"), None), bstack1l1l1l11lll_opy_.get(bstack11lllll_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣፂ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack11lllll_opy_ (u"ࠥࡿࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࢀ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠦ࡯ࡳࠢࡤࡶ࡬ࡹ࠮ࡶࡵ࡬ࡲ࡬ࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠࡰࡴࠣࡥࡷ࡭ࡳ࠯ࡸࡤࡰࡺ࡫࠽ࠣፃ") + str(locator_value) + bstack11lllll_opy_ (u"ࠦࠧፄ"))
                return
            def bstack1ll1lll1ll1_opy_(driver, bstack1l1l11lllll_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1l1l11lllll_opy_(driver, *args, **kwargs)
                    response = self.bstack1l1l1l1l111_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack11lllll_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࠣፅ") + str(locator_value) + bstack11lllll_opy_ (u"ࠨࠢፆ"))
                    else:
                        self.logger.warning(bstack11lllll_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳ࠮ࡰࡲ࠱ࡸࡩࡲࡪࡲࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࢃࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠿ࠥፇ") + str(response) + bstack11lllll_opy_ (u"ࠣࠤፈ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1l1l1l11ll1_opy_(
                        driver, bstack1l1l11lllll_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1ll1lll1ll1_opy_.__name__ = command_name
            return bstack1ll1lll1ll1_opy_
    def __1l1l1l11ll1_opy_(
        self,
        driver,
        bstack1l1l11lllll_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1l1l1l1l111_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack11lllll_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡹࡸࡩࡨࡩࡨࡶࡪࡪ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࠤፉ") + str(locator_value) + bstack11lllll_opy_ (u"ࠥࠦፊ"))
                bstack1l1l1l11111_opy_ = self.bstack1l1l1l11l1l_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack11lllll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢ࡫ࡩࡦࡲࡩ࡯ࡩࡢࡶࡪࡹࡵ࡭ࡶࡀࠦፋ") + str(bstack1l1l1l11111_opy_) + bstack11lllll_opy_ (u"ࠧࠨፌ"))
                if bstack1l1l1l11111_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack11lllll_opy_ (u"ࠨࡵࡴ࡫ࡱ࡫ࠧፍ"): bstack1l1l1l11111_opy_.locator_type,
                            bstack11lllll_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨፎ"): bstack1l1l1l11111_opy_.locator_value,
                        }
                    )
                    return bstack1l1l11lllll_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack11lllll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡋࡢࡈࡊࡈࡕࡈࠤፏ"), False):
                    self.logger.info(bstack1llll11111l_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡷ࡫ࡳࡶ࡮ࡷ࠱ࡲ࡯ࡳࡴ࡫ࡱ࡫࠿ࠦࡳ࡭ࡧࡨࡴ࠭࠹࠰ࠪࠢ࡯ࡩࡹࡺࡩ࡯ࡩࠣࡽࡴࡻࠠࡪࡰࡶࡴࡪࡩࡴࠡࡶ࡫ࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࠢ࡯ࡳ࡬ࡹࠢፐ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack11lllll_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱ࡳࡵ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣࡶࡪࡹࡰࡰࡰࡶࡩࡂࠨፑ") + str(response) + bstack11lllll_opy_ (u"ࠦࠧፒ"))
        except Exception as err:
            self.logger.warning(bstack11lllll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠺ࠡࡧࡵࡶࡴࡸ࠺ࠡࠤፓ") + str(err) + bstack11lllll_opy_ (u"ࠨࠢፔ"))
        raise exception
    @measure(event_name=EVENTS.bstack1l1l1l111l1_opy_, stage=STAGE.bstack1llll11111_opy_)
    def bstack1l1l1l1l111_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack11lllll_opy_ (u"ࠢ࠱ࠤፕ"),
    ):
        self.bstack1l1ll1l11ll_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack11lllll_opy_ (u"ࠣࠤፖ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        req.client_worker_id = bstack11lllll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣፗ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1ll1l1l1ll1_opy_.AISelfHealStep(req)
            self.logger.info(bstack11lllll_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧፘ") + str(r) + bstack11lllll_opy_ (u"ࠦࠧፙ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥፚ") + str(e) + bstack11lllll_opy_ (u"ࠨࠢ፛"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1l1111l_opy_, stage=STAGE.bstack1llll11111_opy_)
    def bstack1l1l1l11l1l_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack11lllll_opy_ (u"ࠢ࠱ࠤ፜")):
        self.bstack1l1ll1l11ll_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        req.client_worker_id = bstack11lllll_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢ፝").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1ll1l1l1ll1_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack11lllll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦ፞") + str(r) + bstack11lllll_opy_ (u"ࠥࠦ፟"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤ፠") + str(e) + bstack11lllll_opy_ (u"ࠧࠨ፡"))
            traceback.print_exc()
            raise e