# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
from browserstack_sdk.sdk_cli.bstack1l1l1l1ll1l_opy_ import bstack1l11llll11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l111_opy_ import (
    bstack11l111l1l_opy_,
    bstack1111111ll_opy_,
    bstack1l1ll1ll111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1l111l1l1_opy_ import bstack1l11l11111l_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1l1l1ll1l_opy_ import bstack1l11llll11l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1lll1l1ll1_opy_ import bstack1ll1l11l1_opy_
import traceback
import os
import threading
import time
class bstack1l1l1111lll_opy_(bstack1l11llll11l_opy_):
    bstack1l111111111_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1l11l11111l_opy_.bstack1l1111111ll_opy_((bstack11l111l1l_opy_.bstack1ll1111lll1_opy_, bstack1111111ll_opy_.PRE), self.bstack11llll1llll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11llll1llll_opy_(
        self,
        f: bstack1l11l11111l_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll1ll111_opy_, str],
        bstack1l1ll11l11l_opy_: Tuple[bstack11l111l1l_opy_, bstack1111111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack11llll1l1l1_opy_(hub_url):
            if not bstack1l1l1111lll_opy_.bstack1l111111111_opy_:
                self.logger.warning(bstack111ll11_opy_ (u"ࠧࡲ࡯ࡤࡣ࡯ࠤࡸ࡫࡬ࡧ࠯࡫ࡩࡦࡲࠠࡧ࡮ࡲࡻࠥࡪࡩࡴࡣࡥࡰࡪࡪࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣ࡭ࡳ࡬ࡲࡢࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤ࡭ࡻࡢࡠࡷࡵࡰࡂࠨ᚛") + str(hub_url) + bstack111ll11_opy_ (u"ࠨࠢ᚜"))
                bstack1l1l1111lll_opy_.bstack1l111111111_opy_ = True
            return
        command_name = f.bstack1l111l1l111_opy_(*args)
        bstack11llll11ll1_opy_ = f.bstack11llll1lll1_opy_(*args)
        if command_name and command_name.lower() == bstack111ll11_opy_ (u"ࠢࡧ࡫ࡱࡨࡪࡲࡥ࡮ࡧࡱࡸࠧ᚝") and bstack11llll11ll1_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack11llll11ll1_opy_.get(bstack111ll11_opy_ (u"ࠣࡷࡶ࡭ࡳ࡭ࠢ᚞"), None), bstack11llll11ll1_opy_.get(bstack111ll11_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣ᚟"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack111ll11_opy_ (u"ࠥࡿࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࢀ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠦ࡯ࡳࠢࡤࡶ࡬ࡹ࠮ࡶࡵ࡬ࡲ࡬ࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠࡰࡴࠣࡥࡷ࡭ࡳ࠯ࡸࡤࡰࡺ࡫࠽ࠣᚠ") + str(locator_value) + bstack111ll11_opy_ (u"ࠦࠧᚡ"))
                return
            def bstack1l1ll1l1ll1_opy_(driver, bstack11llll1ll1l_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack11llll1ll1l_opy_(driver, *args, **kwargs)
                    response = self.bstack11llll1l1ll_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack111ll11_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࠣᚢ") + str(locator_value) + bstack111ll11_opy_ (u"ࠨࠢᚣ"))
                    else:
                        self.logger.warning(bstack111ll11_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳ࠮ࡰࡲ࠱ࡸࡩࡲࡪࡲࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࢃࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠿ࠥᚤ") + str(response) + bstack111ll11_opy_ (u"ࠣࠤᚥ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__11llll1l111_opy_(
                        driver, bstack11llll1ll1l_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1l1ll1l1ll1_opy_.__name__ = command_name
            return bstack1l1ll1l1ll1_opy_
    def __11llll1l111_opy_(
        self,
        driver,
        bstack11llll1ll1l_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack11llll1l1ll_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack111ll11_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡹࡸࡩࡨࡩࡨࡶࡪࡪ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࠤᚦ") + str(locator_value) + bstack111ll11_opy_ (u"ࠥࠦᚧ"))
                bstack11llll1l11l_opy_ = self.bstack11llll1ll11_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack111ll11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢ࡫ࡩࡦࡲࡩ࡯ࡩࡢࡶࡪࡹࡵ࡭ࡶࡀࠦᚨ") + str(bstack11llll1l11l_opy_) + bstack111ll11_opy_ (u"ࠧࠨᚩ"))
                if bstack11llll1l11l_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack111ll11_opy_ (u"ࠨࡵࡴ࡫ࡱ࡫ࠧᚪ"): bstack11llll1l11l_opy_.locator_type,
                            bstack111ll11_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨᚫ"): bstack11llll1l11l_opy_.locator_value,
                        }
                    )
                    return bstack11llll1ll1l_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack111ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡋࡢࡈࡊࡈࡕࡈࠤᚬ"), False):
                    self.logger.info(bstack1l1ll1111ll_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡷ࡫ࡳࡶ࡮ࡷ࠱ࡲ࡯ࡳࡴ࡫ࡱ࡫࠿ࠦࡳ࡭ࡧࡨࡴ࠭࠹࠰ࠪࠢ࡯ࡩࡹࡺࡩ࡯ࡩࠣࡽࡴࡻࠠࡪࡰࡶࡴࡪࡩࡴࠡࡶ࡫ࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࠢ࡯ࡳ࡬ࡹࠢᚭ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack111ll11_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱ࡳࡵ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣࡶࡪࡹࡰࡰࡰࡶࡩࡂࠨᚮ") + str(response) + bstack111ll11_opy_ (u"ࠦࠧᚯ"))
        except Exception as err:
            self.logger.warning(bstack111ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠺ࠡࡧࡵࡶࡴࡸ࠺ࠡࠤᚰ") + str(err) + bstack111ll11_opy_ (u"ࠨࠢᚱ"))
        raise exception
    @measure(event_name=EVENTS.bstack11llll11lll_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
    def bstack11llll1l1ll_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack111ll11_opy_ (u"ࠢ࠱ࠤᚲ"),
    ):
        self.bstack1l1111lllll_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack111ll11_opy_ (u"ࠣࠤᚳ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        req.client_worker_id = bstack111ll11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᚴ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1l1l1l1l1l_opy_.AISelfHealStep(req)
            self.logger.info(bstack111ll11_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᚵ") + str(r) + bstack111ll11_opy_ (u"ࠦࠧᚶ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111ll11_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᚷ") + str(e) + bstack111ll11_opy_ (u"ࠨࠢᚸ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11lllll1111_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
    def bstack11llll1ll11_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack111ll11_opy_ (u"ࠢ࠱ࠤᚹ")):
        self.bstack1l1111lllll_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        req.client_worker_id = bstack111ll11_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᚺ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1l1l1l1l1l_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack111ll11_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᚻ") + str(r) + bstack111ll11_opy_ (u"ࠥࠦᚼ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111ll11_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᚽ") + str(e) + bstack111ll11_opy_ (u"ࠧࠨᚾ"))
            traceback.print_exc()
            raise e