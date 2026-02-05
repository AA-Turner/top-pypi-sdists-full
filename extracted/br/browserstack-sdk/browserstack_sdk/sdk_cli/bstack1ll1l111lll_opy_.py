# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
from browserstack_sdk.sdk_cli.bstack1ll1ll11l11_opy_ import bstack1ll1l11l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import (
    bstack1lll111lll1_opy_,
    bstack1lll1ll1l11_opy_,
    bstack1lll11lll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1ll1l1l1_opy_ import bstack1ll1ll1lll1_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll1ll11l11_opy_ import bstack1ll1l11l1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack11ll1ll111_opy_ import bstack1ll1111ll_opy_
import traceback
import os
import threading
import time
class bstack1lll111l1ll_opy_(bstack1ll1l11l1ll_opy_):
    bstack1l1lllllll1_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1ll1ll1lll1_opy_.bstack1l1ll11llll_opy_((bstack1lll111lll1_opy_.bstack1lll1ll111l_opy_, bstack1lll1ll1l11_opy_.PRE), self.bstack1l1l1ll1111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1ll1111_opy_(
        self,
        f: bstack1ll1ll1lll1_opy_,
        driver: object,
        exec: Tuple[bstack1lll11lll1l_opy_, str],
        bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1l1l1ll11l1_opy_(hub_url):
            if not bstack1lll111l1ll_opy_.bstack1l1lllllll1_opy_:
                self.logger.warning(bstack11l1ll1_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࠢࡶࡩࡱ࡬࠭ࡩࡧࡤࡰࠥ࡬࡬ࡰࡹࠣࡨ࡮ࡹࡡࡣ࡮ࡨࡨࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡ࡫ࡱࡪࡷࡧࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠢ࡫ࡹࡧࡥࡵࡳ࡮ࡀࠦጠ") + str(hub_url) + bstack11l1ll1_opy_ (u"ࠦࠧጡ"))
                bstack1lll111l1ll_opy_.bstack1l1lllllll1_opy_ = True
            return
        command_name = f.bstack1l1llll11l1_opy_(*args)
        bstack1l1l1l1llll_opy_ = f.bstack1l1l1lll111_opy_(*args)
        if command_name and command_name.lower() == bstack11l1ll1_opy_ (u"ࠧ࡬ࡩ࡯ࡦࡨࡰࡪࡳࡥ࡯ࡶࠥጢ") and bstack1l1l1l1llll_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1l1l1l1llll_opy_.get(bstack11l1ll1_opy_ (u"ࠨࡵࡴ࡫ࡱ࡫ࠧጣ"), None), bstack1l1l1l1llll_opy_.get(bstack11l1ll1_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨጤ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack11l1ll1_opy_ (u"ࠣࡽࡦࡳࡲࡳࡡ࡯ࡦࡢࡲࡦࡳࡥࡾ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠤࡴࡸࠠࡢࡴࡪࡷ࠳ࡻࡳࡪࡰࡪࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡵࡲࠡࡣࡵ࡫ࡸ࠴ࡶࡢ࡮ࡸࡩࡂࠨጥ") + str(locator_value) + bstack11l1ll1_opy_ (u"ࠤࠥጦ"))
                return
            def bstack1lll1l11111_opy_(driver, bstack1l1l1l1lll1_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1l1l1l1lll1_opy_(driver, *args, **kwargs)
                    response = self.bstack1l1l1ll111l_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack11l1ll1_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶ࠱ࡸࡩࡲࡪࡲࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࠨጧ") + str(locator_value) + bstack11l1ll1_opy_ (u"ࠦࠧጨ"))
                    else:
                        self.logger.warning(bstack11l1ll1_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸ࠳࡮ࡰ࠯ࡶࡧࡷ࡯ࡰࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࢁࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠽ࠣጩ") + str(response) + bstack11l1ll1_opy_ (u"ࠨࠢጪ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1l1l1ll1lll_opy_(
                        driver, bstack1l1l1l1lll1_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1lll1l11111_opy_.__name__ = command_name
            return bstack1lll1l11111_opy_
    def __1l1l1ll1lll_opy_(
        self,
        driver,
        bstack1l1l1l1lll1_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1l1l1ll111l_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack11l1ll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡷࡶ࡮࡭ࡧࡦࡴࡨࡨ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࠢጫ") + str(locator_value) + bstack11l1ll1_opy_ (u"ࠣࠤጬ"))
                bstack1l1l1ll1l1l_opy_ = self.bstack1l1l1ll1ll1_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack11l1ll1_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡷ࡫ࡳࡶ࡮ࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࢃࠠࡩࡧࡤࡰ࡮ࡴࡧࡠࡴࡨࡷࡺࡲࡴ࠾ࠤጭ") + str(bstack1l1l1ll1l1l_opy_) + bstack11l1ll1_opy_ (u"ࠥࠦጮ"))
                if bstack1l1l1ll1l1l_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack11l1ll1_opy_ (u"ࠦࡺࡹࡩ࡯ࡩࠥጯ"): bstack1l1l1ll1l1l_opy_.locator_type,
                            bstack11l1ll1_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦጰ"): bstack1l1l1ll1l1l_opy_.locator_value,
                        }
                    )
                    return bstack1l1l1l1lll1_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack11l1ll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡉࡠࡆࡈࡆ࡚ࡍࠢጱ"), False):
                    self.logger.info(bstack1ll1ll11l1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡵࡩࡸࡻ࡬ࡵ࠯ࡰ࡭ࡸࡹࡩ࡯ࡩ࠽ࠤࡸࡲࡥࡦࡲࠫ࠷࠵࠯ࠠ࡭ࡧࡷࡸ࡮ࡴࡧࠡࡻࡲࡹࠥ࡯࡮ࡴࡲࡨࡧࡹࠦࡴࡩࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࠠ࡭ࡱࡪࡷࠧጲ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack11l1ll1_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯ࡱࡳ࠲ࡹࡣࡳ࡫ࡳࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫ࡽࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࡀࠦጳ") + str(response) + bstack11l1ll1_opy_ (u"ࠤࠥጴ"))
        except Exception as err:
            self.logger.warning(bstack11l1ll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡸࡥࡴࡷ࡯ࡸ࠿ࠦࡥࡳࡴࡲࡶ࠿ࠦࠢጵ") + str(err) + bstack11l1ll1_opy_ (u"ࠦࠧጶ"))
        raise exception
    @measure(event_name=EVENTS.bstack1l1l1ll1l11_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def bstack1l1l1ll111l_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack11l1ll1_opy_ (u"ࠧ࠶ࠢጷ"),
    ):
        self.bstack1l1lll1ll1l_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack11l1ll1_opy_ (u"ࠨࠢጸ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        req.client_worker_id = bstack11l1ll1_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨጹ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1ll1llll1ll_opy_.AISelfHealStep(req)
            self.logger.info(bstack11l1ll1_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥጺ") + str(r) + bstack11l1ll1_opy_ (u"ࠤࠥጻ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣጼ") + str(e) + bstack11l1ll1_opy_ (u"ࠦࠧጽ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1ll11ll_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def bstack1l1l1ll1ll1_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack11l1ll1_opy_ (u"ࠧ࠶ࠢጾ")):
        self.bstack1l1lll1ll1l_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        req.client_worker_id = bstack11l1ll1_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧጿ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1ll1llll1ll_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack11l1ll1_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤፀ") + str(r) + bstack11l1ll1_opy_ (u"ࠣࠤፁ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢፂ") + str(e) + bstack11l1ll1_opy_ (u"ࠥࠦፃ"))
            traceback.print_exc()
            raise e