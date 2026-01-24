# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
from browserstack_sdk.sdk_cli.bstack1ll111l111l_opy_ import bstack1ll1ll111l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11ll1l1_opy_ import (
    bstack1lll111lll1_opy_,
    bstack1lll1l1ll1l_opy_,
    bstack1lll1l1111l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1l1l1l11_opy_ import bstack1ll1l111l1l_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll111l111l_opy_ import bstack1ll1ll111l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import threading
import time
class bstack1ll1111ll1l_opy_(bstack1ll1ll111l1_opy_):
    bstack1l1ll111lll_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1ll1l111l1l_opy_.bstack1l1lll1ll11_opy_((bstack1lll111lll1_opy_.bstack1lll11l11l1_opy_, bstack1lll1l1ll1l_opy_.PRE), self.bstack1l1l1ll11l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1ll11l1_opy_(
        self,
        f: bstack1ll1l111l1l_opy_,
        driver: object,
        exec: Tuple[bstack1lll1l1111l_opy_, str],
        bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1l1l1ll1lll_opy_(hub_url):
            if not bstack1ll1111ll1l_opy_.bstack1l1ll111lll_opy_:
                self.logger.warning(bstack1l1111_opy_ (u"ࠦࡱࡵࡣࡢ࡮ࠣࡷࡪࡲࡦ࠮ࡪࡨࡥࡱࠦࡦ࡭ࡱࡺࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢ࡬ࡲ࡫ࡸࡡࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧጚ") + str(hub_url) + bstack1l1111_opy_ (u"ࠧࠨጛ"))
                bstack1ll1111ll1l_opy_.bstack1l1ll111lll_opy_ = True
            return
        command_name = f.bstack1l1ll111ll1_opy_(*args)
        bstack1l1l1ll1l1l_opy_ = f.bstack1l1l1ll11ll_opy_(*args)
        if command_name and command_name.lower() == bstack1l1111_opy_ (u"ࠨࡦࡪࡰࡧࡩࡱ࡫࡭ࡦࡰࡷࠦጜ") and bstack1l1l1ll1l1l_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1l1l1ll1l1l_opy_.get(bstack1l1111_opy_ (u"ࠢࡶࡵ࡬ࡲ࡬ࠨጝ"), None), bstack1l1l1ll1l1l_opy_.get(bstack1l1111_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢጞ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1l1111_opy_ (u"ࠤࡾࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦࡿ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡵࡲࠡࡣࡵ࡫ࡸ࠴ࡵࡴ࡫ࡱ࡫ࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡯ࡳࠢࡤࡶ࡬ࡹ࠮ࡷࡣ࡯ࡹࡪࡃࠢጟ") + str(locator_value) + bstack1l1111_opy_ (u"ࠥࠦጠ"))
                return
            def bstack1lll1ll11l1_opy_(driver, bstack1l1l1ll111l_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1l1l1ll111l_opy_(driver, *args, **kwargs)
                    response = self.bstack1l1l1ll1l11_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1l1111_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷ࠲ࡹࡣࡳ࡫ࡳࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࠢጡ") + str(locator_value) + bstack1l1111_opy_ (u"ࠧࠨጢ"))
                    else:
                        self.logger.warning(bstack1l1111_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹ࠭࡯ࡱ࠰ࡷࡨࡸࡩࡱࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠾ࠤጣ") + str(response) + bstack1l1111_opy_ (u"ࠢࠣጤ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1l1l1lll11l_opy_(
                        driver, bstack1l1l1ll111l_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1lll1ll11l1_opy_.__name__ = command_name
            return bstack1lll1ll11l1_opy_
    def __1l1l1lll11l_opy_(
        self,
        driver,
        bstack1l1l1ll111l_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1l1l1ll1l11_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1l1111_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡸࡷ࡯ࡧࡨࡧࡵࡩࡩࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࠣጥ") + str(locator_value) + bstack1l1111_opy_ (u"ࠤࠥጦ"))
                bstack1l1l1lll1l1_opy_ = self.bstack1l1l1ll1ll1_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1l1111_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡸࡥࡴࡷ࡯ࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫ࡽࠡࡪࡨࡥࡱ࡯࡮ࡨࡡࡵࡩࡸࡻ࡬ࡵ࠿ࠥጧ") + str(bstack1l1l1lll1l1_opy_) + bstack1l1111_opy_ (u"ࠦࠧጨ"))
                if bstack1l1l1lll1l1_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1l1111_opy_ (u"ࠧࡻࡳࡪࡰࡪࠦጩ"): bstack1l1l1lll1l1_opy_.locator_type,
                            bstack1l1111_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧጪ"): bstack1l1l1lll1l1_opy_.locator_value,
                        }
                    )
                    return bstack1l1l1ll111l_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1l1111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡊࡡࡇࡉࡇ࡛ࡇࠣጫ"), False):
                    self.logger.info(bstack1ll1ll1l1ll_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡶࡪࡹࡵ࡭ࡶ࠰ࡱ࡮ࡹࡳࡪࡰࡪ࠾ࠥࡹ࡬ࡦࡧࡳࠬ࠸࠶ࠩࠡ࡮ࡨࡸࡹ࡯࡮ࡨࠢࡼࡳࡺࠦࡩ࡯ࡵࡳࡩࡨࡺࠠࡵࡪࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࠡ࡮ࡲ࡫ࡸࠨጬ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1l1111_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰ࡲࡴ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࡁࠧጭ") + str(response) + bstack1l1111_opy_ (u"ࠥࠦጮ"))
        except Exception as err:
            self.logger.warning(bstack1l1111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹࡀࠠࡦࡴࡵࡳࡷࡀࠠࠣጯ") + str(err) + bstack1l1111_opy_ (u"ࠧࠨጰ"))
        raise exception
    @measure(event_name=EVENTS.bstack1l1l1lll111_opy_, stage=STAGE.bstack1111lll11_opy_)
    def bstack1l1l1ll1l11_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1l1111_opy_ (u"ࠨ࠰ࠣጱ"),
    ):
        self.bstack1l1lllllll1_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1l1111_opy_ (u"ࠢࠣጲ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        req.client_worker_id = bstack1l1111_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢጳ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1ll1111l1ll_opy_.AISelfHealStep(req)
            self.logger.info(bstack1l1111_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦጴ") + str(r) + bstack1l1111_opy_ (u"ࠥࠦጵ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤጶ") + str(e) + bstack1l1111_opy_ (u"ࠧࠨጷ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1lll1ll_opy_, stage=STAGE.bstack1111lll11_opy_)
    def bstack1l1l1ll1ll1_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1l1111_opy_ (u"ࠨ࠰ࠣጸ")):
        self.bstack1l1lllllll1_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        req.client_worker_id = bstack1l1111_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨጹ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1ll1111l1ll_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1l1111_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥጺ") + str(r) + bstack1l1111_opy_ (u"ࠤࠥጻ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣጼ") + str(e) + bstack1l1111_opy_ (u"ࠦࠧጽ"))
            traceback.print_exc()
            raise e