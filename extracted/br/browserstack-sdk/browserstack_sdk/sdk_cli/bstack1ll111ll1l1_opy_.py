# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
from browserstack_sdk.sdk_cli.bstack1l1llllllll_opy_ import bstack1ll11111l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import (
    bstack1ll1l1l11l1_opy_,
    bstack1ll1l11ll1l_opy_,
    bstack1ll1l1l111l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll111llll1_opy_ import bstack1ll11lll111_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1llllllll_opy_ import bstack1ll11111l11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack11lll11l1l_opy_ import bstack111ll11111_opy_
import traceback
import os
import threading
import time
class bstack1ll111111l1_opy_(bstack1ll11111l11_opy_):
    bstack1l1l1l111l1_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1ll11lll111_opy_.bstack1l1l1111111_opy_((bstack1ll1l1l11l1_opy_.bstack1ll1l11l11l_opy_, bstack1ll1l11ll1l_opy_.PRE), self.bstack1l11ll111ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11ll111ll_opy_(
        self,
        f: bstack1ll11lll111_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1l111l_opy_, str],
        bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1l11ll1l1l1_opy_(hub_url):
            if not bstack1ll111111l1_opy_.bstack1l1l1l111l1_opy_:
                self.logger.warning(bstack1ll111_opy_ (u"ࠧࡲ࡯ࡤࡣ࡯ࠤࡸ࡫࡬ࡧ࠯࡫ࡩࡦࡲࠠࡧ࡮ࡲࡻࠥࡪࡩࡴࡣࡥࡰࡪࡪࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣ࡭ࡳ࡬ࡲࡢࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤ࡭ࡻࡢࡠࡷࡵࡰࡂࠨᒿ") + str(hub_url) + bstack1ll111_opy_ (u"ࠨࠢᓀ"))
                bstack1ll111111l1_opy_.bstack1l1l1l111l1_opy_ = True
            return
        command_name = f.bstack1l1l11l1l11_opy_(*args)
        bstack1l11ll1l1ll_opy_ = f.bstack1l11ll1l11l_opy_(*args)
        if command_name and command_name.lower() == bstack1ll111_opy_ (u"ࠢࡧ࡫ࡱࡨࡪࡲࡥ࡮ࡧࡱࡸࠧᓁ") and bstack1l11ll1l1ll_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1l11ll1l1ll_opy_.get(bstack1ll111_opy_ (u"ࠣࡷࡶ࡭ࡳ࡭ࠢᓂ"), None), bstack1l11ll1l1ll_opy_.get(bstack1ll111_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣᓃ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1ll111_opy_ (u"ࠥࡿࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࢀ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠦ࡯ࡳࠢࡤࡶ࡬ࡹ࠮ࡶࡵ࡬ࡲ࡬ࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠࡰࡴࠣࡥࡷ࡭ࡳ࠯ࡸࡤࡰࡺ࡫࠽ࠣᓄ") + str(locator_value) + bstack1ll111_opy_ (u"ࠦࠧᓅ"))
                return
            def bstack1ll1l11lll1_opy_(driver, bstack1l11ll1ll1l_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1l11ll1ll1l_opy_(driver, *args, **kwargs)
                    response = self.bstack1l11ll11ll1_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1ll111_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࠣᓆ") + str(locator_value) + bstack1ll111_opy_ (u"ࠨࠢᓇ"))
                    else:
                        self.logger.warning(bstack1ll111_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳ࠮ࡰࡲ࠱ࡸࡩࡲࡪࡲࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࢃࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠿ࠥᓈ") + str(response) + bstack1ll111_opy_ (u"ࠣࠤᓉ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1l11ll11l11_opy_(
                        driver, bstack1l11ll1ll1l_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1ll1l11lll1_opy_.__name__ = command_name
            return bstack1ll1l11lll1_opy_
    def __1l11ll11l11_opy_(
        self,
        driver,
        bstack1l11ll1ll1l_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1l11ll11ll1_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1ll111_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡹࡸࡩࡨࡩࡨࡶࡪࡪ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࠤᓊ") + str(locator_value) + bstack1ll111_opy_ (u"ࠥࠦᓋ"))
                bstack1l11ll1l111_opy_ = self.bstack1l11ll11lll_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1ll111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢ࡫ࡩࡦࡲࡩ࡯ࡩࡢࡶࡪࡹࡵ࡭ࡶࡀࠦᓌ") + str(bstack1l11ll1l111_opy_) + bstack1ll111_opy_ (u"ࠧࠨᓍ"))
                if bstack1l11ll1l111_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1ll111_opy_ (u"ࠨࡵࡴ࡫ࡱ࡫ࠧᓎ"): bstack1l11ll1l111_opy_.locator_type,
                            bstack1ll111_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨᓏ"): bstack1l11ll1l111_opy_.locator_value,
                        }
                    )
                    return bstack1l11ll1ll1l_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1ll111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡋࡢࡈࡊࡈࡕࡈࠤᓐ"), False):
                    self.logger.info(bstack1ll1l11llll_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡷ࡫ࡳࡶ࡮ࡷ࠱ࡲ࡯ࡳࡴ࡫ࡱ࡫࠿ࠦࡳ࡭ࡧࡨࡴ࠭࠹࠰ࠪࠢ࡯ࡩࡹࡺࡩ࡯ࡩࠣࡽࡴࡻࠠࡪࡰࡶࡴࡪࡩࡴࠡࡶ࡫ࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࠢ࡯ࡳ࡬ࡹࠢᓑ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1ll111_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱ࡳࡵ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣࡶࡪࡹࡰࡰࡰࡶࡩࡂࠨᓒ") + str(response) + bstack1ll111_opy_ (u"ࠦࠧᓓ"))
        except Exception as err:
            self.logger.warning(bstack1ll111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠺ࠡࡧࡵࡶࡴࡸ࠺ࠡࠤᓔ") + str(err) + bstack1ll111_opy_ (u"ࠨࠢᓕ"))
        raise exception
    @measure(event_name=EVENTS.bstack1l11ll1ll11_opy_, stage=STAGE.bstack11ll1111_opy_)
    def bstack1l11ll11ll1_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1ll111_opy_ (u"ࠢ࠱ࠤᓖ"),
    ):
        self.bstack1l11ll1llll_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1ll111_opy_ (u"ࠣࠤᓗ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        req.client_worker_id = bstack1ll111_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᓘ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1ll1lll11ll_opy_.AISelfHealStep(req)
            self.logger.info(bstack1ll111_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᓙ") + str(r) + bstack1ll111_opy_ (u"ࠦࠧᓚ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᓛ") + str(e) + bstack1ll111_opy_ (u"ࠨࠢᓜ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11ll11l1l_opy_, stage=STAGE.bstack11ll1111_opy_)
    def bstack1l11ll11lll_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1ll111_opy_ (u"ࠢ࠱ࠤᓝ")):
        self.bstack1l11ll1llll_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        req.client_worker_id = bstack1ll111_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᓞ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1ll1lll11ll_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1ll111_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᓟ") + str(r) + bstack1ll111_opy_ (u"ࠥࠦᓠ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᓡ") + str(e) + bstack1ll111_opy_ (u"ࠧࠨᓢ"))
            traceback.print_exc()
            raise e