# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
from browserstack_sdk.sdk_cli.bstack1ll11ll11l1_opy_ import bstack1ll1l1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import (
    bstack1ll1ll1l1l1_opy_,
    bstack1lll111l1l1_opy_,
    bstack1ll1lll1111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1llll11l1_opy_ import bstack1ll1111ll11_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll11ll11l1_opy_ import bstack1ll1l1l11l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack11111111l_opy_ import bstack1111l1l1l_opy_
import traceback
import os
import threading
import time
class bstack1ll11l11l11_opy_(bstack1ll1l1l11l1_opy_):
    bstack1l1l1ll1ll1_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1ll1111ll11_opy_.bstack1l1l1lll11l_opy_((bstack1ll1ll1l1l1_opy_.bstack1ll1ll1l11l_opy_, bstack1lll111l1l1_opy_.PRE), self.bstack1l1l11l1ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11l1ll1_opy_(
        self,
        f: bstack1ll1111ll11_opy_,
        driver: object,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1l1l11l111l_opy_(hub_url):
            if not bstack1ll11l11l11_opy_.bstack1l1l1ll1ll1_opy_:
                self.logger.warning(bstack11ll111_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࠢࡶࡩࡱ࡬࠭ࡩࡧࡤࡰࠥ࡬࡬ࡰࡹࠣࡨ࡮ࡹࡡࡣ࡮ࡨࡨࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡ࡫ࡱࡪࡷࡧࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠢ࡫ࡹࡧࡥࡵࡳ࡮ࡀࠦᏈ") + str(hub_url) + bstack11ll111_opy_ (u"ࠦࠧᏉ"))
                bstack1ll11l11l11_opy_.bstack1l1l1ll1ll1_opy_ = True
            return
        command_name = f.bstack1l1l11ll111_opy_(*args)
        bstack1l1l111lll1_opy_ = f.bstack1l1l111llll_opy_(*args)
        if command_name and command_name.lower() == bstack11ll111_opy_ (u"ࠧ࡬ࡩ࡯ࡦࡨࡰࡪࡳࡥ࡯ࡶࠥᏊ") and bstack1l1l111lll1_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1l1l111lll1_opy_.get(bstack11ll111_opy_ (u"ࠨࡵࡴ࡫ࡱ࡫ࠧᏋ"), None), bstack1l1l111lll1_opy_.get(bstack11ll111_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨᏌ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack11ll111_opy_ (u"ࠣࡽࡦࡳࡲࡳࡡ࡯ࡦࡢࡲࡦࡳࡥࡾ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠤࡴࡸࠠࡢࡴࡪࡷ࠳ࡻࡳࡪࡰࡪࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡵࡲࠡࡣࡵ࡫ࡸ࠴ࡶࡢ࡮ࡸࡩࡂࠨᏍ") + str(locator_value) + bstack11ll111_opy_ (u"ࠤࠥᏎ"))
                return
            def bstack1lll1111l1l_opy_(driver, bstack1l1l111ll11_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1l1l111ll11_opy_(driver, *args, **kwargs)
                    response = self.bstack1l1l111ll1l_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack11ll111_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶ࠱ࡸࡩࡲࡪࡲࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࠨᏏ") + str(locator_value) + bstack11ll111_opy_ (u"ࠦࠧᏐ"))
                    else:
                        self.logger.warning(bstack11ll111_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸ࠳࡮ࡰ࠯ࡶࡧࡷ࡯ࡰࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࢁࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠽ࠣᏑ") + str(response) + bstack11ll111_opy_ (u"ࠨࠢᏒ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1l1l11l11l1_opy_(
                        driver, bstack1l1l111ll11_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1lll1111l1l_opy_.__name__ = command_name
            return bstack1lll1111l1l_opy_
    def __1l1l11l11l1_opy_(
        self,
        driver,
        bstack1l1l111ll11_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1l1l111ll1l_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack11ll111_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡷࡶ࡮࡭ࡧࡦࡴࡨࡨ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࠢᏓ") + str(locator_value) + bstack11ll111_opy_ (u"ࠣࠤᏔ"))
                bstack1l1l11l11ll_opy_ = self.bstack1l1l11l1l1l_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack11ll111_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡷ࡫ࡳࡶ࡮ࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࢃࠠࡩࡧࡤࡰ࡮ࡴࡧࡠࡴࡨࡷࡺࡲࡴ࠾ࠤᏕ") + str(bstack1l1l11l11ll_opy_) + bstack11ll111_opy_ (u"ࠥࠦᏖ"))
                if bstack1l1l11l11ll_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack11ll111_opy_ (u"ࠦࡺࡹࡩ࡯ࡩࠥᏗ"): bstack1l1l11l11ll_opy_.locator_type,
                            bstack11ll111_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᏘ"): bstack1l1l11l11ll_opy_.locator_value,
                        }
                    )
                    return bstack1l1l111ll11_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack11ll111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡉࡠࡆࡈࡆ࡚ࡍࠢᏙ"), False):
                    self.logger.info(bstack1lll11111l1_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡵࡩࡸࡻ࡬ࡵ࠯ࡰ࡭ࡸࡹࡩ࡯ࡩ࠽ࠤࡸࡲࡥࡦࡲࠫ࠷࠵࠯ࠠ࡭ࡧࡷࡸ࡮ࡴࡧࠡࡻࡲࡹࠥ࡯࡮ࡴࡲࡨࡧࡹࠦࡴࡩࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࠠ࡭ࡱࡪࡷࠧᏚ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack11ll111_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯ࡱࡳ࠲ࡹࡣࡳ࡫ࡳࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫ࡽࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࡀࠦᏛ") + str(response) + bstack11ll111_opy_ (u"ࠤࠥᏜ"))
        except Exception as err:
            self.logger.warning(bstack11ll111_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡸࡥࡴࡷ࡯ࡸ࠿ࠦࡥࡳࡴࡲࡶ࠿ࠦࠢᏝ") + str(err) + bstack11ll111_opy_ (u"ࠦࠧᏞ"))
        raise exception
    @measure(event_name=EVENTS.bstack1l1l11l1111_opy_, stage=STAGE.bstack1111l1111_opy_)
    def bstack1l1l111ll1l_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack11ll111_opy_ (u"ࠧ࠶ࠢᏟ"),
    ):
        self.bstack1l1l11llll1_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack11ll111_opy_ (u"ࠨࠢᏠ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        req.client_worker_id = bstack11ll111_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᏡ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1l1llllll1l_opy_.AISelfHealStep(req)
            self.logger.info(bstack11ll111_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᏢ") + str(r) + bstack11ll111_opy_ (u"ࠤࠥᏣ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᏤ") + str(e) + bstack11ll111_opy_ (u"ࠦࠧᏥ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l11l1l11_opy_, stage=STAGE.bstack1111l1111_opy_)
    def bstack1l1l11l1l1l_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack11ll111_opy_ (u"ࠧ࠶ࠢᏦ")):
        self.bstack1l1l11llll1_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        req.client_worker_id = bstack11ll111_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᏧ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1l1llllll1l_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack11ll111_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᏨ") + str(r) + bstack11ll111_opy_ (u"ࠣࠤᏩ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᏪ") + str(e) + bstack11ll111_opy_ (u"ࠥࠦᏫ"))
            traceback.print_exc()
            raise e