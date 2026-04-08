# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
from browserstack_sdk.sdk_cli.bstack1l11l1l1l11_opy_ import bstack1l111111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111111_opy_ import (
    bstack11l1ll1l1_opy_,
    bstack1lll1l11l1_opy_,
    bstack1l1l111l1l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1111lllll_opy_ import bstack1l11l11l11l_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l11l1l1l11_opy_ import bstack1l111111l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack111111lll1_opy_ import bstack11lll11111_opy_
import traceback
import os
import threading
import time
class bstack1l11111llll_opy_(bstack1l111111l1l_opy_):
    bstack11llll1llll_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1l11l11l11l_opy_.bstack11llll1l1l1_opy_((bstack11l1ll1l1_opy_.bstack1ll1111l1l1_opy_, bstack1lll1l11l1_opy_.PRE), self.bstack11ll1l1llll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11ll1l1llll_opy_(
        self,
        f: bstack1l11l11l11l_opy_,
        driver: object,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack11ll1l1lll1_opy_(hub_url):
            if not bstack1l11111llll_opy_.bstack11llll1llll_opy_:
                self.logger.warning(bstack111l_opy_ (u"ࠤ࡯ࡳࡨࡧ࡬ࠡࡵࡨࡰ࡫࠳ࡨࡦࡣ࡯ࠤ࡫ࡲ࡯ࡸࠢࡧ࡭ࡸࡧࡢ࡭ࡧࡧࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡪࡰࡩࡶࡦࠦࡳࡦࡵࡶ࡭ࡴࡴࡳࠡࡪࡸࡦࡤࡻࡲ࡭࠿ࠥ᜖") + str(hub_url) + bstack111l_opy_ (u"ࠥࠦ᜗"))
                bstack1l11111llll_opy_.bstack11llll1llll_opy_ = True
            return
        command_name = f.bstack11lll1ll11l_opy_(*args)
        bstack11ll1l1l1l1_opy_ = f.bstack11ll1l1ll11_opy_(*args)
        if command_name and command_name.lower() == bstack111l_opy_ (u"ࠦ࡫࡯࡮ࡥࡧ࡯ࡩࡲ࡫࡮ࡵࠤ᜘") and bstack11ll1l1l1l1_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack11ll1l1l1l1_opy_.get(bstack111l_opy_ (u"ࠧࡻࡳࡪࡰࡪࠦ᜙"), None), bstack11ll1l1l1l1_opy_.get(bstack111l_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧ᜚"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack111l_opy_ (u"ࠢࡼࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫ࡽ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠣࡳࡷࠦࡡࡳࡩࡶ࠲ࡺࡹࡩ࡯ࡩࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡴࡸࠠࡢࡴࡪࡷ࠳ࡼࡡ࡭ࡷࡨࡁࠧ᜛") + str(locator_value) + bstack111l_opy_ (u"ࠣࠤ᜜"))
                return
            def bstack1l1l111llll_opy_(driver, bstack11ll1l1l1ll_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack11ll1l1l1ll_opy_(driver, *args, **kwargs)
                    response = self.bstack11ll1l1ll1l_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack111l_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵ࠰ࡷࡨࡸࡩࡱࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࠧ᜝") + str(locator_value) + bstack111l_opy_ (u"ࠥࠦ᜞"))
                    else:
                        self.logger.warning(bstack111l_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷ࠲ࡴ࡯࠮ࡵࡦࡶ࡮ࡶࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࢀࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡃࠢᜟ") + str(response) + bstack111l_opy_ (u"ࠧࠨᜠ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__11ll1l1l111_opy_(
                        driver, bstack11ll1l1l1ll_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1l1l111llll_opy_.__name__ = command_name
            return bstack1l1l111llll_opy_
    def __11ll1l1l111_opy_(
        self,
        driver,
        bstack11ll1l1l1ll_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack11ll1l1ll1l_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack111l_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭ࡩࡧࡤࡰ࡮ࡴࡧ࠮ࡶࡵ࡭࡬࡭ࡥࡳࡧࡧ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࠨᜡ") + str(locator_value) + bstack111l_opy_ (u"ࠢࠣᜢ"))
                bstack11ll1l1l11l_opy_ = self.bstack11ll1ll11l1_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack111l_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡶࡪࡹࡵ࡭ࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࢂࠦࡨࡦࡣ࡯࡭ࡳ࡭࡟ࡳࡧࡶࡹࡱࡺ࠽ࠣᜣ") + str(bstack11ll1l1l11l_opy_) + bstack111l_opy_ (u"ࠤࠥᜤ"))
                if bstack11ll1l1l11l_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack111l_opy_ (u"ࠥࡹࡸ࡯࡮ࡨࠤᜥ"): bstack11ll1l1l11l_opy_.locator_type,
                            bstack111l_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥᜦ"): bstack11ll1l1l11l_opy_.locator_value,
                        }
                    )
                    return bstack11ll1l1l1ll_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack111l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡏ࡟ࡅࡇࡅ࡙ࡌࠨᜧ"), False):
                    self.logger.info(bstack1l11lll11ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭ࡩࡧࡤࡰ࡮ࡴࡧ࠮ࡴࡨࡷࡺࡲࡴ࠮࡯࡬ࡷࡸ࡯࡮ࡨ࠼ࠣࡷࡱ࡫ࡥࡱࠪ࠶࠴࠮ࠦ࡬ࡦࡶࡷ࡭ࡳ࡭ࠠࡺࡱࡸࠤ࡮ࡴࡳࡱࡧࡦࡸࠥࡺࡨࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࠦ࡬ࡰࡩࡶࠦᜨ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack111l_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡰࡲ࠱ࡸࡩࡲࡪࡲࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࢃࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠿ࠥᜩ") + str(response) + bstack111l_opy_ (u"ࠣࠤᜪ"))
        except Exception as err:
            self.logger.warning(bstack111l_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡷ࡫ࡳࡶ࡮ࡷ࠾ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠨᜫ") + str(err) + bstack111l_opy_ (u"ࠥࠦᜬ"))
        raise exception
    @measure(event_name=EVENTS.bstack11ll1ll1111_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def bstack11ll1l1ll1l_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack111l_opy_ (u"ࠦ࠵ࠨᜭ"),
    ):
        self.bstack11lllll1111_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack111l_opy_ (u"ࠧࠨᜮ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        req.client_worker_id = bstack111l_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᜯ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack11l11lll11_opy_.AISelfHealStep(req)
            self.logger.info(bstack111l_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᜰ") + str(r) + bstack111l_opy_ (u"ࠣࠤᜱ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111l_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᜲ") + str(e) + bstack111l_opy_ (u"ࠥࠦᜳ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11ll1ll111l_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def bstack11ll1ll11l1_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack111l_opy_ (u"ࠦ࠵ࠨ᜴")):
        self.bstack11lllll1111_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        req.client_worker_id = bstack111l_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦ᜵").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack11l11lll11_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack111l_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣ᜶") + str(r) + bstack111l_opy_ (u"ࠢࠣ᜷"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111l_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨ᜸") + str(e) + bstack111l_opy_ (u"ࠤࠥ᜹"))
            traceback.print_exc()
            raise e