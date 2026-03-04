# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
from browserstack_sdk.sdk_cli.bstack1ll11111111_opy_ import bstack1ll11l1ll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1ll1l_opy_ import (
    bstack1ll1l1l11ll_opy_,
    bstack1ll1llll111_opy_,
    bstack1ll1llll11l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll111lll1l_opy_ import bstack1ll11l11l11_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll11111111_opy_ import bstack1ll11l1ll11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1l1ll1l111_opy_ import bstack1l11l11ll1_opy_
import traceback
import os
import threading
import time
class bstack1ll11lll1ll_opy_(bstack1ll11l1ll11_opy_):
    bstack1l1l1l11ll1_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1ll11l11l11_opy_.bstack1l1l1lll1ll_opy_((bstack1ll1l1l11ll_opy_.bstack1ll1lll11l1_opy_, bstack1ll1llll111_opy_.PRE), self.bstack1l11llll1l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11llll1l1_opy_(
        self,
        f: bstack1ll11l11l11_opy_,
        driver: object,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1l1l111111l_opy_(hub_url):
            if not bstack1ll11lll1ll_opy_.bstack1l1l1l11ll1_opy_:
                self.logger.warning(bstack1lll1l_opy_ (u"ࠧࡲ࡯ࡤࡣ࡯ࠤࡸ࡫࡬ࡧ࠯࡫ࡩࡦࡲࠠࡧ࡮ࡲࡻࠥࡪࡩࡴࡣࡥࡰࡪࡪࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣ࡭ࡳ࡬ࡲࡢࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤ࡭ࡻࡢࡠࡷࡵࡰࡂࠨᑖ") + str(hub_url) + bstack1lll1l_opy_ (u"ࠨࠢᑗ"))
                bstack1ll11lll1ll_opy_.bstack1l1l1l11ll1_opy_ = True
            return
        command_name = f.bstack1l1l1llll1l_opy_(*args)
        bstack1l11lllllll_opy_ = f.bstack1l11llll1ll_opy_(*args)
        if command_name and command_name.lower() == bstack1lll1l_opy_ (u"ࠢࡧ࡫ࡱࡨࡪࡲࡥ࡮ࡧࡱࡸࠧᑘ") and bstack1l11lllllll_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1l11lllllll_opy_.get(bstack1lll1l_opy_ (u"ࠣࡷࡶ࡭ࡳ࡭ࠢᑙ"), None), bstack1l11lllllll_opy_.get(bstack1lll1l_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣᑚ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1lll1l_opy_ (u"ࠥࡿࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࢀ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠦ࡯ࡳࠢࡤࡶ࡬ࡹ࠮ࡶࡵ࡬ࡲ࡬ࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠࡰࡴࠣࡥࡷ࡭ࡳ࠯ࡸࡤࡰࡺ࡫࠽ࠣᑛ") + str(locator_value) + bstack1lll1l_opy_ (u"ࠦࠧᑜ"))
                return
            def bstack1ll1llll1ll_opy_(driver, bstack1l11llll11l_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1l11llll11l_opy_(driver, *args, **kwargs)
                    response = self.bstack1l1l11111ll_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1lll1l_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࠣᑝ") + str(locator_value) + bstack1lll1l_opy_ (u"ࠨࠢᑞ"))
                    else:
                        self.logger.warning(bstack1lll1l_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳ࠮ࡰࡲ࠱ࡸࡩࡲࡪࡲࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࢃࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠿ࠥᑟ") + str(response) + bstack1lll1l_opy_ (u"ࠣࠤᑠ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1l11lllll1l_opy_(
                        driver, bstack1l11llll11l_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1ll1llll1ll_opy_.__name__ = command_name
            return bstack1ll1llll1ll_opy_
    def __1l11lllll1l_opy_(
        self,
        driver,
        bstack1l11llll11l_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1l1l11111ll_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1lll1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡹࡸࡩࡨࡩࡨࡶࡪࡪ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࠤᑡ") + str(locator_value) + bstack1lll1l_opy_ (u"ࠥࠦᑢ"))
                bstack1l1l11111l1_opy_ = self.bstack1l1l1111111_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1lll1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢ࡫ࡩࡦࡲࡩ࡯ࡩࡢࡶࡪࡹࡵ࡭ࡶࡀࠦᑣ") + str(bstack1l1l11111l1_opy_) + bstack1lll1l_opy_ (u"ࠧࠨᑤ"))
                if bstack1l1l11111l1_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1lll1l_opy_ (u"ࠨࡵࡴ࡫ࡱ࡫ࠧᑥ"): bstack1l1l11111l1_opy_.locator_type,
                            bstack1lll1l_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨᑦ"): bstack1l1l11111l1_opy_.locator_value,
                        }
                    )
                    return bstack1l11llll11l_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1lll1l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡋࡢࡈࡊࡈࡕࡈࠤᑧ"), False):
                    self.logger.info(bstack1ll1l1ll11l_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡷ࡫ࡳࡶ࡮ࡷ࠱ࡲ࡯ࡳࡴ࡫ࡱ࡫࠿ࠦࡳ࡭ࡧࡨࡴ࠭࠹࠰ࠪࠢ࡯ࡩࡹࡺࡩ࡯ࡩࠣࡽࡴࡻࠠࡪࡰࡶࡴࡪࡩࡴࠡࡶ࡫ࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࠢ࡯ࡳ࡬ࡹࠢᑨ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1lll1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱ࡳࡵ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣࡶࡪࡹࡰࡰࡰࡶࡩࡂࠨᑩ") + str(response) + bstack1lll1l_opy_ (u"ࠦࠧᑪ"))
        except Exception as err:
            self.logger.warning(bstack1lll1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠺ࠡࡧࡵࡶࡴࡸ࠺ࠡࠤᑫ") + str(err) + bstack1lll1l_opy_ (u"ࠨࠢᑬ"))
        raise exception
    @measure(event_name=EVENTS.bstack1l11llllll1_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
    def bstack1l1l11111ll_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1lll1l_opy_ (u"ࠢ࠱ࠤᑭ"),
    ):
        self.bstack1l1l1111ll1_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1lll1l_opy_ (u"ࠣࠤᑮ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        req.client_worker_id = bstack1lll1l_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᑯ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1lll111lll1_opy_.AISelfHealStep(req)
            self.logger.info(bstack1lll1l_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᑰ") + str(r) + bstack1lll1l_opy_ (u"ࠦࠧᑱ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1lll1l_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᑲ") + str(e) + bstack1lll1l_opy_ (u"ࠨࠢᑳ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11lllll11_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
    def bstack1l1l1111111_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1lll1l_opy_ (u"ࠢ࠱ࠤᑴ")):
        self.bstack1l1l1111ll1_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        req.client_worker_id = bstack1lll1l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᑵ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1lll111lll1_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1lll1l_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᑶ") + str(r) + bstack1lll1l_opy_ (u"ࠥࠦᑷ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1lll1l_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᑸ") + str(e) + bstack1lll1l_opy_ (u"ࠧࠨᑹ"))
            traceback.print_exc()
            raise e