# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
from browserstack_sdk.sdk_cli.bstack1ll11l11l1l_opy_ import bstack1ll111l1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11lllll_opy_ import (
    bstack1ll1lll1ll1_opy_,
    bstack1ll1l1lll1l_opy_,
    bstack1ll1ll1l111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1lll1ll1l_opy_ import bstack1ll11l11111_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll11l11l1l_opy_ import bstack1ll111l1l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1ll1l11ll1_opy_ import bstack1l11l1ll_opy_
import traceback
import os
import threading
import time
class bstack1l1lll1lll1_opy_(bstack1ll111l1l1l_opy_):
    bstack1l1l1lll1ll_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1ll11l11111_opy_.bstack1l1ll1111ll_opy_((bstack1ll1lll1ll1_opy_.bstack1ll1ll1l1l1_opy_, bstack1ll1l1lll1l_opy_.PRE), self.bstack1l11llll1ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11llll1ll_opy_(
        self,
        f: bstack1ll11l11111_opy_,
        driver: object,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1l11llll11l_opy_(hub_url):
            if not bstack1l1lll1lll1_opy_.bstack1l1l1lll1ll_opy_:
                self.logger.warning(bstack1111_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࠥࡹࡥ࡭ࡨ࠰࡬ࡪࡧ࡬ࠡࡨ࡯ࡳࡼࠦࡤࡪࡵࡤࡦࡱ࡫ࡤࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤ࡮ࡴࡦࡳࡣࠣࡷࡪࡹࡳࡪࡱࡱࡷࠥ࡮ࡵࡣࡡࡸࡶࡱࡃࠢᑗ") + str(hub_url) + bstack1111_opy_ (u"ࠢࠣᑘ"))
                bstack1l1lll1lll1_opy_.bstack1l1l1lll1ll_opy_ = True
            return
        command_name = f.bstack1l1l1l11lll_opy_(*args)
        bstack1l1l1111111_opy_ = f.bstack1l11lllllll_opy_(*args)
        if command_name and command_name.lower() == bstack1111_opy_ (u"ࠣࡨ࡬ࡲࡩ࡫࡬ࡦ࡯ࡨࡲࡹࠨᑙ") and bstack1l1l1111111_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1l1l1111111_opy_.get(bstack1111_opy_ (u"ࠤࡸࡷ࡮ࡴࡧࠣᑚ"), None), bstack1l1l1111111_opy_.get(bstack1111_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤᑛ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1111_opy_ (u"ࠦࢀࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࢁ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠠࡰࡴࠣࡥࡷ࡭ࡳ࠯ࡷࡶ࡭ࡳ࡭࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡࡱࡵࠤࡦࡸࡧࡴ࠰ࡹࡥࡱࡻࡥ࠾ࠤᑜ") + str(locator_value) + bstack1111_opy_ (u"ࠧࠨᑝ"))
                return
            def bstack1ll1lll1111_opy_(driver, bstack1l11lllll11_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1l11lllll11_opy_(driver, *args, **kwargs)
                    response = self.bstack1l1l111111l_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1111_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࠤᑞ") + str(locator_value) + bstack1111_opy_ (u"ࠢࠣᑟ"))
                    else:
                        self.logger.warning(bstack1111_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴ࠯ࡱࡳ࠲ࡹࡣࡳ࡫ࡳࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫ࡽࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࡀࠦᑠ") + str(response) + bstack1111_opy_ (u"ࠤࠥᑡ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1l11llllll1_opy_(
                        driver, bstack1l11lllll11_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1ll1lll1111_opy_.__name__ = command_name
            return bstack1ll1lll1111_opy_
    def __1l11llllll1_opy_(
        self,
        driver,
        bstack1l11lllll11_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1l1l111111l_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1111_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡺࡲࡪࡩࡪࡩࡷ࡫ࡤ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࠥᑢ") + str(locator_value) + bstack1111_opy_ (u"ࠦࠧᑣ"))
                bstack1l11llll111_opy_ = self.bstack1l11lllll1l_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣ࡬ࡪࡧ࡬ࡪࡰࡪࡣࡷ࡫ࡳࡶ࡮ࡷࡁࠧᑤ") + str(bstack1l11llll111_opy_) + bstack1111_opy_ (u"ࠨࠢᑥ"))
                if bstack1l11llll111_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1111_opy_ (u"ࠢࡶࡵ࡬ࡲ࡬ࠨᑦ"): bstack1l11llll111_opy_.locator_type,
                            bstack1111_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᑧ"): bstack1l11llll111_opy_.locator_value,
                        }
                    )
                    return bstack1l11lllll11_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡌࡣࡉࡋࡂࡖࡉࠥᑨ"), False):
                    self.logger.info(bstack1ll1l1l11l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡸࡥࡴࡷ࡯ࡸ࠲ࡳࡩࡴࡵ࡬ࡲ࡬ࡀࠠࡴ࡮ࡨࡩࡵ࠮࠳࠱ࠫࠣࡰࡪࡺࡴࡪࡰࡪࠤࡾࡵࡵࠡ࡫ࡱࡷࡵ࡫ࡣࡵࠢࡷ࡬ࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡦࡺࡷࡩࡳࡹࡩࡰࡰࠣࡰࡴ࡭ࡳࠣᑩ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲ࡴ࡯࠮ࡵࡦࡶ࡮ࡶࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࢀࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡃࠢᑪ") + str(response) + bstack1111_opy_ (u"ࠧࠨᑫ"))
        except Exception as err:
            self.logger.warning(bstack1111_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭ࡩࡧࡤࡰ࡮ࡴࡧ࠮ࡴࡨࡷࡺࡲࡴ࠻ࠢࡨࡶࡷࡵࡲ࠻ࠢࠥᑬ") + str(err) + bstack1111_opy_ (u"ࠢࠣᑭ"))
        raise exception
    @measure(event_name=EVENTS.bstack1l11lll1lll_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def bstack1l1l111111l_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1111_opy_ (u"ࠣ࠲ࠥᑮ"),
    ):
        self.bstack1l1l111ll1l_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1111_opy_ (u"ࠤࠥᑯ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        req.client_worker_id = bstack1111_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᑰ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1lll111l111_opy_.AISelfHealStep(req)
            self.logger.info(bstack1111_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᑱ") + str(r) + bstack1111_opy_ (u"ࠧࠨᑲ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᑳ") + str(e) + bstack1111_opy_ (u"ࠢࠣᑴ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11llll1l1_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def bstack1l11lllll1l_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1111_opy_ (u"ࠣ࠲ࠥᑵ")):
        self.bstack1l1l111ll1l_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        req.client_worker_id = bstack1111_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᑶ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1lll111l111_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1111_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᑷ") + str(r) + bstack1111_opy_ (u"ࠦࠧᑸ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᑹ") + str(e) + bstack1111_opy_ (u"ࠨࠢᑺ"))
            traceback.print_exc()
            raise e