# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
from browserstack_sdk.sdk_cli.bstack1l1l1llll11_opy_ import bstack1ll1111l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1l11l_opy_ import (
    bstack1ll1l1l1lll_opy_,
    bstack1ll1ll1111l_opy_,
    bstack1ll1l1lll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1ll11l1l1_opy_ import bstack1ll111ll1ll_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1l1llll11_opy_ import bstack1ll1111l1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack111l1l1ll1_opy_ import bstack1l11ll1l1_opy_
import traceback
import os
import threading
import time
class bstack1l1llll111l_opy_(bstack1ll1111l1ll_opy_):
    bstack1l1l11l11l1_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1ll111ll1ll_opy_.bstack1l1l11llll1_opy_((bstack1ll1l1l1lll_opy_.bstack1ll11ll1lll_opy_, bstack1ll1ll1111l_opy_.PRE), self.bstack1l11ll1l111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11ll1l111_opy_(
        self,
        f: bstack1ll111ll1ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1lll1l_opy_, str],
        bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1l11ll1l1l1_opy_(hub_url):
            if not bstack1l1llll111l_opy_.bstack1l1l11l11l1_opy_:
                self.logger.warning(bstack1111l_opy_ (u"ࠣ࡮ࡲࡧࡦࡲࠠࡴࡧ࡯ࡪ࠲࡮ࡥࡢ࡮ࠣࡪࡱࡵࡷࠡࡦ࡬ࡷࡦࡨ࡬ࡦࡦࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡩ࡯ࡨࡵࡥࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡩࡷࡥࡣࡺࡸ࡬࠾ࠤᓺ") + str(hub_url) + bstack1111l_opy_ (u"ࠤࠥᓻ"))
                bstack1l1llll111l_opy_.bstack1l1l11l11l1_opy_ = True
            return
        command_name = f.bstack1l11llll1ll_opy_(*args)
        bstack1l11ll11l1l_opy_ = f.bstack1l11ll11lll_opy_(*args)
        if command_name and command_name.lower() == bstack1111l_opy_ (u"ࠥࡪ࡮ࡴࡤࡦ࡮ࡨࡱࡪࡴࡴࠣᓼ") and bstack1l11ll11l1l_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1l11ll11l1l_opy_.get(bstack1111l_opy_ (u"ࠦࡺࡹࡩ࡯ࡩࠥᓽ"), None), bstack1l11ll11l1l_opy_.get(bstack1111l_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᓾ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1111l_opy_ (u"ࠨࡻࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࢃ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡲࡶࠥࡧࡲࡨࡵ࠱ࡹࡸ࡯࡮ࡨ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡳࡷࠦࡡࡳࡩࡶ࠲ࡻࡧ࡬ࡶࡧࡀࠦᓿ") + str(locator_value) + bstack1111l_opy_ (u"ࠢࠣᔀ"))
                return
            def bstack1ll1l1l11l1_opy_(driver, bstack1l11ll1ll11_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1l11ll1ll11_opy_(driver, *args, **kwargs)
                    response = self.bstack1l11ll1l11l_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1111l_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴ࠯ࡶࡧࡷ࡯ࡰࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࠦᔁ") + str(locator_value) + bstack1111l_opy_ (u"ࠤࠥᔂ"))
                    else:
                        self.logger.warning(bstack1111l_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶ࠱ࡳࡵ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣࡶࡪࡹࡰࡰࡰࡶࡩࡂࠨᔃ") + str(response) + bstack1111l_opy_ (u"ࠦࠧᔄ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1l11ll111l1_opy_(
                        driver, bstack1l11ll1ll11_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1ll1l1l11l1_opy_.__name__ = command_name
            return bstack1ll1l1l11l1_opy_
    def __1l11ll111l1_opy_(
        self,
        driver,
        bstack1l11ll1ll11_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1l11ll1l11l_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1111l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡵࡴ࡬࡫࡬࡫ࡲࡦࡦ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࠧᔅ") + str(locator_value) + bstack1111l_opy_ (u"ࠨࠢᔆ"))
                bstack1l11ll1l1ll_opy_ = self.bstack1l11ll11ll1_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1111l_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡵࡩࡸࡻ࡬ࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࢁࠥ࡮ࡥࡢ࡮࡬ࡲ࡬ࡥࡲࡦࡵࡸࡰࡹࡃࠢᔇ") + str(bstack1l11ll1l1ll_opy_) + bstack1111l_opy_ (u"ࠣࠤᔈ"))
                if bstack1l11ll1l1ll_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1111l_opy_ (u"ࠤࡸࡷ࡮ࡴࡧࠣᔉ"): bstack1l11ll1l1ll_opy_.locator_type,
                            bstack1111l_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤᔊ"): bstack1l11ll1l1ll_opy_.locator_value,
                        }
                    )
                    return bstack1l11ll1ll11_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1111l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡎࡥࡄࡆࡄࡘࡋࠧᔋ"), False):
                    self.logger.info(bstack1ll1l11l1ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠭࡮࡫ࡶࡷ࡮ࡴࡧ࠻ࠢࡶࡰࡪ࡫ࡰࠩ࠵࠳࠭ࠥࡲࡥࡵࡶ࡬ࡲ࡬ࠦࡹࡰࡷࠣ࡭ࡳࡹࡰࡦࡥࡷࠤࡹ࡮ࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࠥࡲ࡯ࡨࡵࠥᔌ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1111l_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭࡯ࡱ࠰ࡷࡨࡸࡩࡱࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠾ࠤᔍ") + str(response) + bstack1111l_opy_ (u"ࠢࠣᔎ"))
        except Exception as err:
            self.logger.warning(bstack1111l_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡶࡪࡹࡵ࡭ࡶ࠽ࠤࡪࡸࡲࡰࡴ࠽ࠤࠧᔏ") + str(err) + bstack1111l_opy_ (u"ࠤࠥᔐ"))
        raise exception
    @measure(event_name=EVENTS.bstack1l11ll11l11_opy_, stage=STAGE.bstack11lll111l_opy_)
    def bstack1l11ll1l11l_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1111l_opy_ (u"ࠥ࠴ࠧᔑ"),
    ):
        self.bstack1l1l111l1ll_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1111l_opy_ (u"ࠦࠧᔒ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        req.client_worker_id = bstack1111l_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᔓ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1ll1ll1lll1_opy_.AISelfHealStep(req)
            self.logger.info(bstack1111l_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᔔ") + str(r) + bstack1111l_opy_ (u"ࠢࠣᔕ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111l_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᔖ") + str(e) + bstack1111l_opy_ (u"ࠤࠥᔗ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11ll111ll_opy_, stage=STAGE.bstack11lll111l_opy_)
    def bstack1l11ll11ll1_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1111l_opy_ (u"ࠥ࠴ࠧᔘ")):
        self.bstack1l1l111l1ll_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        req.client_worker_id = bstack1111l_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᔙ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1ll1ll1lll1_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1111l_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᔚ") + str(r) + bstack1111l_opy_ (u"ࠨࠢᔛ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111l_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᔜ") + str(e) + bstack1111l_opy_ (u"ࠣࠤᔝ"))
            traceback.print_exc()
            raise e