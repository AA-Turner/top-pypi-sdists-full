# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
from browserstack_sdk.sdk_cli.bstack1ll111111l1_opy_ import bstack1l1ll1lll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1111l1l_opy_ import (
    bstack1ll1lllllll_opy_,
    bstack1ll1l1llll1_opy_,
    bstack1ll1l1ll1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1lll1llll_opy_ import bstack1l1llllllll_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll111111l1_opy_ import bstack1l1ll1lll11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack11ll11ll1l_opy_ import bstack111l1lllll_opy_
import traceback
import os
import threading
import time
class bstack1ll1l11l11l_opy_(bstack1l1ll1lll11_opy_):
    bstack1l1l1lll1ll_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1l1llllllll_opy_.bstack1l1l1l111ll_opy_((bstack1ll1lllllll_opy_.bstack1ll1ll1l11l_opy_, bstack1ll1l1llll1_opy_.PRE), self.bstack1l1l1111l11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1111l11_opy_(
        self,
        f: bstack1l1llllllll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1ll1ll_opy_, str],
        bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1l1l1111lll_opy_(hub_url):
            if not bstack1ll1l11l11l_opy_.bstack1l1l1lll1ll_opy_:
                self.logger.warning(bstack11l11_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࠢࡶࡩࡱ࡬࠭ࡩࡧࡤࡰࠥ࡬࡬ࡰࡹࠣࡨ࡮ࡹࡡࡣ࡮ࡨࡨࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡ࡫ࡱࡪࡷࡧࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠢ࡫ࡹࡧࡥࡵࡳ࡮ࡀࠦᏁ") + str(hub_url) + bstack11l11_opy_ (u"ࠦࠧᏂ"))
                bstack1ll1l11l11l_opy_.bstack1l1l1lll1ll_opy_ = True
            return
        command_name = f.bstack1l1l11ll11l_opy_(*args)
        bstack1l11lllllll_opy_ = f.bstack1l1l1111111_opy_(*args)
        if command_name and command_name.lower() == bstack11l11_opy_ (u"ࠧ࡬ࡩ࡯ࡦࡨࡰࡪࡳࡥ࡯ࡶࠥᏃ") and bstack1l11lllllll_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1l11lllllll_opy_.get(bstack11l11_opy_ (u"ࠨࡵࡴ࡫ࡱ࡫ࠧᏄ"), None), bstack1l11lllllll_opy_.get(bstack11l11_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨᏅ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack11l11_opy_ (u"ࠣࡽࡦࡳࡲࡳࡡ࡯ࡦࡢࡲࡦࡳࡥࡾ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠤࡴࡸࠠࡢࡴࡪࡷ࠳ࡻࡳࡪࡰࡪࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡵࡲࠡࡣࡵ࡫ࡸ࠴ࡶࡢ࡮ࡸࡩࡂࠨᏆ") + str(locator_value) + bstack11l11_opy_ (u"ࠤࠥᏇ"))
                return
            def bstack1ll1lllll1l_opy_(driver, bstack1l1l111111l_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1l1l111111l_opy_(driver, *args, **kwargs)
                    response = self.bstack1l1l111l111_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack11l11_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶ࠱ࡸࡩࡲࡪࡲࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࠨᏈ") + str(locator_value) + bstack11l11_opy_ (u"ࠦࠧᏉ"))
                    else:
                        self.logger.warning(bstack11l11_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸ࠳࡮ࡰ࠯ࡶࡧࡷ࡯ࡰࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࢁࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠽ࠣᏊ") + str(response) + bstack11l11_opy_ (u"ࠨࠢᏋ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1l1l11111l1_opy_(
                        driver, bstack1l1l111111l_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1ll1lllll1l_opy_.__name__ = command_name
            return bstack1ll1lllll1l_opy_
    def __1l1l11111l1_opy_(
        self,
        driver,
        bstack1l1l111111l_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1l1l111l111_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack11l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡷࡶ࡮࡭ࡧࡦࡴࡨࡨ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࠢᏌ") + str(locator_value) + bstack11l11_opy_ (u"ࠣࠤᏍ"))
                bstack1l1l11111ll_opy_ = self.bstack1l1l1111l1l_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack11l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡷ࡫ࡳࡶ࡮ࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࢃࠠࡩࡧࡤࡰ࡮ࡴࡧࡠࡴࡨࡷࡺࡲࡴ࠾ࠤᏎ") + str(bstack1l1l11111ll_opy_) + bstack11l11_opy_ (u"ࠥࠦᏏ"))
                if bstack1l1l11111ll_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack11l11_opy_ (u"ࠦࡺࡹࡩ࡯ࡩࠥᏐ"): bstack1l1l11111ll_opy_.locator_type,
                            bstack11l11_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᏑ"): bstack1l1l11111ll_opy_.locator_value,
                        }
                    )
                    return bstack1l1l111111l_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack11l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡉࡠࡆࡈࡆ࡚ࡍࠢᏒ"), False):
                    self.logger.info(bstack1ll1lllll11_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡵࡩࡸࡻ࡬ࡵ࠯ࡰ࡭ࡸࡹࡩ࡯ࡩ࠽ࠤࡸࡲࡥࡦࡲࠫ࠷࠵࠯ࠠ࡭ࡧࡷࡸ࡮ࡴࡧࠡࡻࡲࡹࠥ࡯࡮ࡴࡲࡨࡧࡹࠦࡴࡩࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࠠ࡭ࡱࡪࡷࠧᏓ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack11l11_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯ࡱࡳ࠲ࡹࡣࡳ࡫ࡳࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫ࡽࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࡀࠦᏔ") + str(response) + bstack11l11_opy_ (u"ࠤࠥᏕ"))
        except Exception as err:
            self.logger.warning(bstack11l11_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡸࡥࡴࡷ࡯ࡸ࠿ࠦࡥࡳࡴࡲࡶ࠿ࠦࠢᏖ") + str(err) + bstack11l11_opy_ (u"ࠦࠧᏗ"))
        raise exception
    @measure(event_name=EVENTS.bstack1l11llllll1_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack1l1l111l111_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack11l11_opy_ (u"ࠧ࠶ࠢᏘ"),
    ):
        self.bstack1l1l11l1111_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack11l11_opy_ (u"ࠨࠢᏙ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        req.client_worker_id = bstack11l11_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᏚ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1ll1l1l1lll_opy_.AISelfHealStep(req)
            self.logger.info(bstack11l11_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᏛ") + str(r) + bstack11l11_opy_ (u"ࠤࠥᏜ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l11_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᏝ") + str(e) + bstack11l11_opy_ (u"ࠦࠧᏞ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1111ll1_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack1l1l1111l1l_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack11l11_opy_ (u"ࠧ࠶ࠢᏟ")):
        self.bstack1l1l11l1111_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        req.client_worker_id = bstack11l11_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᏠ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1ll1l1l1lll_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack11l11_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᏡ") + str(r) + bstack11l11_opy_ (u"ࠣࠤᏢ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l11_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᏣ") + str(e) + bstack11l11_opy_ (u"ࠥࠦᏤ"))
            traceback.print_exc()
            raise e