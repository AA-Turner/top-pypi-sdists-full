# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
from browserstack_sdk.sdk_cli.bstack1l1ll11l111_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.sdk_cli.bstack111l11ll11_opy_ import (
    bstack11lll111_opy_,
    bstack1l11l11l1_opy_,
    bstack1ll11ll1l11_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1lll1l1ll_opy_ import bstack1ll111l1111_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1ll11l111_opy_ import bstack1ll111l11ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1l111ll111_opy_ import bstack1l1l11ll1_opy_
import traceback
import os
import threading
import time
class bstack1l1l1lll1l1_opy_(bstack1ll111l11ll_opy_):
    bstack1l11llll111_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1ll111l1111_opy_.bstack1l11ll11111_opy_((bstack11lll111_opy_.bstack1ll1l1lllll_opy_, bstack1l11l11l1_opy_.PRE), self.bstack1l11l11ll1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l11ll1l_opy_(
        self,
        f: bstack1ll111l1111_opy_,
        driver: object,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1l11l11l1ll_opy_(hub_url):
            if not bstack1l1l1lll1l1_opy_.bstack1l11llll111_opy_:
                self.logger.warning(bstack1ll1lll_opy_ (u"ࠦࡱࡵࡣࡢ࡮ࠣࡷࡪࡲࡦ࠮ࡪࡨࡥࡱࠦࡦ࡭ࡱࡺࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢ࡬ࡲ࡫ࡸࡡࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧᕃ") + str(hub_url) + bstack1ll1lll_opy_ (u"ࠧࠨᕄ"))
                bstack1l1l1lll1l1_opy_.bstack1l11llll111_opy_ = True
            return
        command_name = f.bstack1l11llll11l_opy_(*args)
        bstack1l11l111l1l_opy_ = f.bstack1l11l11l11l_opy_(*args)
        if command_name and command_name.lower() == bstack1ll1lll_opy_ (u"ࠨࡦࡪࡰࡧࡩࡱ࡫࡭ࡦࡰࡷࠦᕅ") and bstack1l11l111l1l_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1l11l111l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠢࡶࡵ࡬ࡲ࡬ࠨᕆ"), None), bstack1l11l111l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᕇ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1ll1lll_opy_ (u"ࠤࡾࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦࡿ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡵࡲࠡࡣࡵ࡫ࡸ࠴ࡵࡴ࡫ࡱ࡫ࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡯ࡳࠢࡤࡶ࡬ࡹ࠮ࡷࡣ࡯ࡹࡪࡃࠢᕈ") + str(locator_value) + bstack1ll1lll_opy_ (u"ࠥࠦᕉ"))
                return
            def bstack1ll11l11lll_opy_(driver, bstack1l11l111ll1_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1l11l111ll1_opy_(driver, *args, **kwargs)
                    response = self.bstack1l11l11ll11_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1ll1lll_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷ࠲ࡹࡣࡳ࡫ࡳࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࠢᕊ") + str(locator_value) + bstack1ll1lll_opy_ (u"ࠧࠨᕋ"))
                    else:
                        self.logger.warning(bstack1ll1lll_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹ࠭࡯ࡱ࠰ࡷࡨࡸࡩࡱࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠾ࠤᕌ") + str(response) + bstack1ll1lll_opy_ (u"ࠢࠣᕍ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1l11l11lll1_opy_(
                        driver, bstack1l11l111ll1_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1ll11l11lll_opy_.__name__ = command_name
            return bstack1ll11l11lll_opy_
    def __1l11l11lll1_opy_(
        self,
        driver,
        bstack1l11l111ll1_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1l11l11ll11_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1ll1lll_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡸࡷ࡯ࡧࡨࡧࡵࡩࡩࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࠣᕎ") + str(locator_value) + bstack1ll1lll_opy_ (u"ࠤࠥᕏ"))
                bstack1l11l11l1l1_opy_ = self.bstack1l11l111l11_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1ll1lll_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡸࡥࡴࡷ࡯ࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫ࡽࠡࡪࡨࡥࡱ࡯࡮ࡨࡡࡵࡩࡸࡻ࡬ࡵ࠿ࠥᕐ") + str(bstack1l11l11l1l1_opy_) + bstack1ll1lll_opy_ (u"ࠦࠧᕑ"))
                if bstack1l11l11l1l1_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1ll1lll_opy_ (u"ࠧࡻࡳࡪࡰࡪࠦᕒ"): bstack1l11l11l1l1_opy_.locator_type,
                            bstack1ll1lll_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧᕓ"): bstack1l11l11l1l1_opy_.locator_value,
                        }
                    )
                    return bstack1l11l111ll1_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1ll1lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡊࡡࡇࡉࡇ࡛ࡇࠣᕔ"), False):
                    self.logger.info(bstack1ll11l1ll11_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡶࡪࡹࡵ࡭ࡶ࠰ࡱ࡮ࡹࡳࡪࡰࡪ࠾ࠥࡹ࡬ࡦࡧࡳࠬ࠸࠶ࠩࠡ࡮ࡨࡸࡹ࡯࡮ࡨࠢࡼࡳࡺࠦࡩ࡯ࡵࡳࡩࡨࡺࠠࡵࡪࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࠡ࡮ࡲ࡫ࡸࠨᕕ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1ll1lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰ࡲࡴ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࡁࠧᕖ") + str(response) + bstack1ll1lll_opy_ (u"ࠥࠦᕗ"))
        except Exception as err:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹࡀࠠࡦࡴࡵࡳࡷࡀࠠࠣᕘ") + str(err) + bstack1ll1lll_opy_ (u"ࠧࠨᕙ"))
        raise exception
    @measure(event_name=EVENTS.bstack1l11l111lll_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def bstack1l11l11ll11_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1ll1lll_opy_ (u"ࠨ࠰ࠣᕚ"),
    ):
        self.bstack1l11l1l111l_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1ll1lll_opy_ (u"ࠢࠣᕛ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᕜ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1l1llll1lll_opy_.AISelfHealStep(req)
            self.logger.info(bstack1ll1lll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᕝ") + str(r) + bstack1ll1lll_opy_ (u"ࠥࠦᕞ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᕟ") + str(e) + bstack1ll1lll_opy_ (u"ࠧࠨᕠ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11l11l111_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def bstack1l11l111l11_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1ll1lll_opy_ (u"ࠨ࠰ࠣᕡ")):
        self.bstack1l11l1l111l_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᕢ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1l1llll1lll_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1ll1lll_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᕣ") + str(r) + bstack1ll1lll_opy_ (u"ࠤࠥᕤ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᕥ") + str(e) + bstack1ll1lll_opy_ (u"ࠦࠧᕦ"))
            traceback.print_exc()
            raise e