# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
from browserstack_sdk.sdk_cli.bstack1l1l1l11111_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1l11111ll_opy_ import (
    bstack1ll1l1ll11_opy_,
    bstack1ll11ll1ll_opy_,
    bstack1ll111lllll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll111111l1_opy_ import bstack1ll11111111_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1l1l11111_opy_ import bstack1ll111l11ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1ll1lll11l_opy_ import bstack11ll11l1ll_opy_
import traceback
import os
import threading
import time
class bstack1l1l1lll1ll_opy_(bstack1ll111l11ll_opy_):
    bstack1l1l11111ll_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1ll11111111_opy_.bstack1l11lll1lll_opy_((bstack1ll1l1ll11_opy_.bstack1ll1l1l1ll1_opy_, bstack1ll11ll1ll_opy_.PRE), self.bstack1l11l111l11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l111l11_opy_(
        self,
        f: bstack1ll11111111_opy_,
        driver: object,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1l11l1111l1_opy_(hub_url):
            if not bstack1l1l1lll1ll_opy_.bstack1l1l11111ll_opy_:
                self.logger.warning(bstack1ll11_opy_ (u"ࠢ࡭ࡱࡦࡥࡱࠦࡳࡦ࡮ࡩ࠱࡭࡫ࡡ࡭ࠢࡩࡰࡴࡽࠠࡥ࡫ࡶࡥࡧࡲࡥࡥࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥ࡯࡮ࡧࡴࡤࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡨࡶࡤࡢࡹࡷࡲ࠽ࠣᕔ") + str(hub_url) + bstack1ll11_opy_ (u"ࠣࠤᕕ"))
                bstack1l1l1lll1ll_opy_.bstack1l1l11111ll_opy_ = True
            return
        command_name = f.bstack1l1l111ll11_opy_(*args)
        bstack1l11l1111ll_opy_ = f.bstack1l11l11l1ll_opy_(*args)
        if command_name and command_name.lower() == bstack1ll11_opy_ (u"ࠤࡩ࡭ࡳࡪࡥ࡭ࡧࡰࡩࡳࡺࠢᕖ") and bstack1l11l1111ll_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1l11l1111ll_opy_.get(bstack1ll11_opy_ (u"ࠥࡹࡸ࡯࡮ࡨࠤᕗ"), None), bstack1l11l1111ll_opy_.get(bstack1ll11_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥᕘ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1ll11_opy_ (u"ࠧࢁࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࢂࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠡࡱࡵࠤࡦࡸࡧࡴ࠰ࡸࡷ࡮ࡴࡧ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢࡲࡶࠥࡧࡲࡨࡵ࠱ࡺࡦࡲࡵࡦ࠿ࠥᕙ") + str(locator_value) + bstack1ll11_opy_ (u"ࠨࠢᕚ"))
                return
            def bstack1ll11l1l111_opy_(driver, bstack1l11l11l11l_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1l11l11l11l_opy_(driver, *args, **kwargs)
                    response = self.bstack1l11l111ll1_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1ll11_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳ࠮ࡵࡦࡶ࡮ࡶࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࠥᕛ") + str(locator_value) + bstack1ll11_opy_ (u"ࠣࠤᕜ"))
                    else:
                        self.logger.warning(bstack1ll11_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵ࠰ࡲࡴ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࡁࠧᕝ") + str(response) + bstack1ll11_opy_ (u"ࠥࠦᕞ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1l11l111lll_opy_(
                        driver, bstack1l11l11l11l_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1ll11l1l111_opy_.__name__ = command_name
            return bstack1ll11l1l111_opy_
    def __1l11l111lll_opy_(
        self,
        driver,
        bstack1l11l11l11l_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1l11l111ll1_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1ll11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡴࡳ࡫ࡪ࡫ࡪࡸࡥࡥ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࠦᕟ") + str(locator_value) + bstack1ll11_opy_ (u"ࠧࠨᕠ"))
                bstack1l11l11ll11_opy_ = self.bstack1l11l11l1l1_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1ll11_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭ࡩࡧࡤࡰ࡮ࡴࡧ࠮ࡴࡨࡷࡺࡲࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࢀࠤ࡭࡫ࡡ࡭࡫ࡱ࡫ࡤࡸࡥࡴࡷ࡯ࡸࡂࠨᕡ") + str(bstack1l11l11ll11_opy_) + bstack1ll11_opy_ (u"ࠢࠣᕢ"))
                if bstack1l11l11ll11_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1ll11_opy_ (u"ࠣࡷࡶ࡭ࡳ࡭ࠢᕣ"): bstack1l11l11ll11_opy_.locator_type,
                            bstack1ll11_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣᕤ"): bstack1l11l11ll11_opy_.locator_value,
                        }
                    )
                    return bstack1l11l11l11l_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡍࡤࡊࡅࡃࡗࡊࠦᕥ"), False):
                    self.logger.info(bstack1ll11l1ll11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹ࠳࡭ࡪࡵࡶ࡭ࡳ࡭࠺ࠡࡵ࡯ࡩࡪࡶࠨ࠴࠲ࠬࠤࡱ࡫ࡴࡵ࡫ࡱ࡫ࠥࡿ࡯ࡶࠢ࡬ࡲࡸࡶࡥࡤࡶࠣࡸ࡭࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡧࡻࡸࡪࡴࡳࡪࡱࡱࠤࡱࡵࡧࡴࠤᕦ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳࡮ࡰ࠯ࡶࡧࡷ࡯ࡰࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࢁࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠽ࠣᕧ") + str(response) + bstack1ll11_opy_ (u"ࠨࠢᕨ"))
        except Exception as err:
            self.logger.warning(bstack1ll11_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡵࡩࡸࡻ࡬ࡵ࠼ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠦᕩ") + str(err) + bstack1ll11_opy_ (u"ࠣࠤᕪ"))
        raise exception
    @measure(event_name=EVENTS.bstack1l11l11l111_opy_, stage=STAGE.bstack11111llll_opy_)
    def bstack1l11l111ll1_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1ll11_opy_ (u"ࠤ࠳ࠦᕫ"),
    ):
        self.bstack1l1l1111l11_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1ll11_opy_ (u"ࠥࠦᕬ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        req.client_worker_id = bstack1ll11_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᕭ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1l1ll1ll111_opy_.AISelfHealStep(req)
            self.logger.info(bstack1ll11_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᕮ") + str(r) + bstack1ll11_opy_ (u"ࠨࠢᕯ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᕰ") + str(e) + bstack1ll11_opy_ (u"ࠣࠤᕱ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11l111l1l_opy_, stage=STAGE.bstack11111llll_opy_)
    def bstack1l11l11l1l1_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1ll11_opy_ (u"ࠤ࠳ࠦᕲ")):
        self.bstack1l1l1111l11_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        req.client_worker_id = bstack1ll11_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᕳ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1l1ll1ll111_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1ll11_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᕴ") + str(r) + bstack1ll11_opy_ (u"ࠧࠨᕵ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᕶ") + str(e) + bstack1ll11_opy_ (u"ࠢࠣᕷ"))
            traceback.print_exc()
            raise e