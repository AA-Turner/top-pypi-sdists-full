# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
from browserstack_sdk.sdk_cli.bstack1ll1l1l11l1_opy_ import bstack1ll11llll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111l1_opy_ import (
    bstack1ll1lll1lll_opy_,
    bstack1lll11l111l_opy_,
    bstack1ll1llll111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1ll11lll_opy_ import bstack1l1lllll1l1_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll1l1l11l1_opy_ import bstack1ll11llll11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack111lll111l_opy_ import bstack11ll1l1l1_opy_
import traceback
import os
import threading
import time
class bstack1l1llll1l1l_opy_(bstack1ll11llll11_opy_):
    bstack1l1ll1ll11l_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1l1lllll1l1_opy_.bstack1l1l11lll1l_opy_((bstack1ll1lll1lll_opy_.bstack1lll11111ll_opy_, bstack1lll11l111l_opy_.PRE), self.bstack1l1l11l1l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11l1l1l_opy_(
        self,
        f: bstack1l1lllll1l1_opy_,
        driver: object,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1l1l11l11l1_opy_(hub_url):
            if not bstack1l1llll1l1l_opy_.bstack1l1ll1ll11l_opy_:
                self.logger.warning(bstack11l1l11_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࠥࡹࡥ࡭ࡨ࠰࡬ࡪࡧ࡬ࠡࡨ࡯ࡳࡼࠦࡤࡪࡵࡤࡦࡱ࡫ࡤࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤ࡮ࡴࡦࡳࡣࠣࡷࡪࡹࡳࡪࡱࡱࡷࠥ࡮ࡵࡣࡡࡸࡶࡱࡃࠢᏋ") + str(hub_url) + bstack11l1l11_opy_ (u"ࠢࠣᏌ"))
                bstack1l1llll1l1l_opy_.bstack1l1ll1ll11l_opy_ = True
            return
        command_name = f.bstack1l1l1l11lll_opy_(*args)
        bstack1l1l111llll_opy_ = f.bstack1l1l11l1l11_opy_(*args)
        if command_name and command_name.lower() == bstack11l1l11_opy_ (u"ࠣࡨ࡬ࡲࡩ࡫࡬ࡦ࡯ࡨࡲࡹࠨᏍ") and bstack1l1l111llll_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1l1l111llll_opy_.get(bstack11l1l11_opy_ (u"ࠤࡸࡷ࡮ࡴࡧࠣᏎ"), None), bstack1l1l111llll_opy_.get(bstack11l1l11_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤᏏ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack11l1l11_opy_ (u"ࠦࢀࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࢁ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠠࡰࡴࠣࡥࡷ࡭ࡳ࠯ࡷࡶ࡭ࡳ࡭࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡࡱࡵࠤࡦࡸࡧࡴ࠰ࡹࡥࡱࡻࡥ࠾ࠤᏐ") + str(locator_value) + bstack11l1l11_opy_ (u"ࠧࠨᏑ"))
                return
            def bstack1lll1111l1l_opy_(driver, bstack1l1l11l1lll_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1l1l11l1lll_opy_(driver, *args, **kwargs)
                    response = self.bstack1l1l111lll1_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack11l1l11_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࠤᏒ") + str(locator_value) + bstack11l1l11_opy_ (u"ࠢࠣᏓ"))
                    else:
                        self.logger.warning(bstack11l1l11_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴ࠯ࡱࡳ࠲ࡹࡣࡳ࡫ࡳࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫ࡽࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࡀࠦᏔ") + str(response) + bstack11l1l11_opy_ (u"ࠤࠥᏕ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1l1l111ll1l_opy_(
                        driver, bstack1l1l11l1lll_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1lll1111l1l_opy_.__name__ = command_name
            return bstack1lll1111l1l_opy_
    def __1l1l111ll1l_opy_(
        self,
        driver,
        bstack1l1l11l1lll_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1l1l111lll1_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack11l1l11_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡺࡲࡪࡩࡪࡩࡷ࡫ࡤ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࠥᏖ") + str(locator_value) + bstack11l1l11_opy_ (u"ࠦࠧᏗ"))
                bstack1l1l11l11ll_opy_ = self.bstack1l1l11l111l_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack11l1l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣ࡬ࡪࡧ࡬ࡪࡰࡪࡣࡷ࡫ࡳࡶ࡮ࡷࡁࠧᏘ") + str(bstack1l1l11l11ll_opy_) + bstack11l1l11_opy_ (u"ࠨࠢᏙ"))
                if bstack1l1l11l11ll_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack11l1l11_opy_ (u"ࠢࡶࡵ࡬ࡲ࡬ࠨᏚ"): bstack1l1l11l11ll_opy_.locator_type,
                            bstack11l1l11_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᏛ"): bstack1l1l11l11ll_opy_.locator_value,
                        }
                    )
                    return bstack1l1l11l1lll_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack11l1l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡌࡣࡉࡋࡂࡖࡉࠥᏜ"), False):
                    self.logger.info(bstack1lll11l11ll_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡸࡥࡴࡷ࡯ࡸ࠲ࡳࡩࡴࡵ࡬ࡲ࡬ࡀࠠࡴ࡮ࡨࡩࡵ࠮࠳࠱ࠫࠣࡰࡪࡺࡴࡪࡰࡪࠤࡾࡵࡵࠡ࡫ࡱࡷࡵ࡫ࡣࡵࠢࡷ࡬ࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡦࡺࡷࡩࡳࡹࡩࡰࡰࠣࡰࡴ࡭ࡳࠣᏝ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack11l1l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲ࡴ࡯࠮ࡵࡦࡶ࡮ࡶࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࢀࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡃࠢᏞ") + str(response) + bstack11l1l11_opy_ (u"ࠧࠨᏟ"))
        except Exception as err:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭ࡩࡧࡤࡰ࡮ࡴࡧ࠮ࡴࡨࡷࡺࡲࡴ࠻ࠢࡨࡶࡷࡵࡲ࠻ࠢࠥᏠ") + str(err) + bstack11l1l11_opy_ (u"ࠢࠣᏡ"))
        raise exception
    @measure(event_name=EVENTS.bstack1l1l11l1ll1_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def bstack1l1l111lll1_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack11l1l11_opy_ (u"ࠣ࠲ࠥᏢ"),
    ):
        self.bstack1l1l1ll1111_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack11l1l11_opy_ (u"ࠤࠥᏣ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        req.client_worker_id = bstack11l1l11_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᏤ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1ll1ll11111_opy_.AISelfHealStep(req)
            self.logger.info(bstack11l1l11_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᏥ") + str(r) + bstack11l1l11_opy_ (u"ࠧࠨᏦ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᏧ") + str(e) + bstack11l1l11_opy_ (u"ࠢࠣᏨ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l11l1111_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def bstack1l1l11l111l_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack11l1l11_opy_ (u"ࠣ࠲ࠥᏩ")):
        self.bstack1l1l1ll1111_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        req.client_worker_id = bstack11l1l11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᏪ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1ll1ll11111_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack11l1l11_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᏫ") + str(r) + bstack11l1l11_opy_ (u"ࠦࠧᏬ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᏭ") + str(e) + bstack11l1l11_opy_ (u"ࠨࠢᏮ"))
            traceback.print_exc()
            raise e