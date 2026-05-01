# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
from browserstack_sdk.sdk_cli.bstack1l1l111l111_opy_ import bstack1l11l1l11ll_opy_
from browserstack_sdk.sdk_cli.bstack11l111l1l_opy_ import (
    bstack1ll1l1111l_opy_,
    bstack1l1l111lll_opy_,
    bstack1l1ll111lll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l11l11llll_opy_ import bstack1l11lll111l_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1l111l111_opy_ import bstack1l11l1l11ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack11ll1l1l_opy_ import bstack111l1l1l_opy_
import traceback
import os
import threading
import time
class bstack1l1l1l1ll11_opy_(bstack1l11l1l11ll_opy_):
    bstack1l1111ll11l_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1l11lll111l_opy_.bstack1l111l1111l_opy_((bstack1ll1l1111l_opy_.bstack1ll1111l111_opy_, bstack1l1l111lll_opy_.PRE), self.bstack11llll11l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11llll11l1l_opy_(
        self,
        f: bstack1l11lll111l_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack11llll11ll1_opy_(hub_url):
            if not bstack1l1l1l1ll11_opy_.bstack1l1111ll11l_opy_:
                self.logger.warning(bstack111ll_opy_ (u"ࠣ࡮ࡲࡧࡦࡲࠠࡴࡧ࡯ࡪ࠲࡮ࡥࡢ࡮ࠣࡪࡱࡵࡷࠡࡦ࡬ࡷࡦࡨ࡬ࡦࡦࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡩ࡯ࡨࡵࡥࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡩࡷࡥࡣࡺࡸ࡬࠾ࠤᚬ") + str(hub_url) + bstack111ll_opy_ (u"ࠤࠥᚭ"))
                bstack1l1l1l1ll11_opy_.bstack1l1111ll11l_opy_ = True
            return
        command_name = f.bstack1l111l1l1l1_opy_(*args)
        bstack11llll1111l_opy_ = f.bstack11llll1l1ll_opy_(*args)
        if command_name and command_name.lower() == bstack111ll_opy_ (u"ࠥࡪ࡮ࡴࡤࡦ࡮ࡨࡱࡪࡴࡴࠣᚮ") and bstack11llll1111l_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack11llll1111l_opy_.get(bstack111ll_opy_ (u"ࠦࡺࡹࡩ࡯ࡩࠥᚯ"), None), bstack11llll1111l_opy_.get(bstack111ll_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᚰ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack111ll_opy_ (u"ࠨࡻࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࢃ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡲࡶࠥࡧࡲࡨࡵ࠱ࡹࡸ࡯࡮ࡨ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡳࡷࠦࡡࡳࡩࡶ࠲ࡻࡧ࡬ࡶࡧࡀࠦᚱ") + str(locator_value) + bstack111ll_opy_ (u"ࠢࠣᚲ"))
                return
            def bstack1l1ll11l11l_opy_(driver, bstack11llll11l11_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack11llll11l11_opy_(driver, *args, **kwargs)
                    response = self.bstack11llll1l111_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack111ll_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴ࠯ࡶࡧࡷ࡯ࡰࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࠦᚳ") + str(locator_value) + bstack111ll_opy_ (u"ࠤࠥᚴ"))
                    else:
                        self.logger.warning(bstack111ll_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶ࠱ࡳࡵ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣࡶࡪࡹࡰࡰࡰࡶࡩࡂࠨᚵ") + str(response) + bstack111ll_opy_ (u"ࠦࠧᚶ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__11llll1l1l1_opy_(
                        driver, bstack11llll11l11_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1l1ll11l11l_opy_.__name__ = command_name
            return bstack1l1ll11l11l_opy_
    def __11llll1l1l1_opy_(
        self,
        driver,
        bstack11llll11l11_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack11llll1l111_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack111ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡵࡴ࡬࡫࡬࡫ࡲࡦࡦ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࠧᚷ") + str(locator_value) + bstack111ll_opy_ (u"ࠨࠢᚸ"))
                bstack11llll11lll_opy_ = self.bstack11llll111l1_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack111ll_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡵࡩࡸࡻ࡬ࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࢁࠥ࡮ࡥࡢ࡮࡬ࡲ࡬ࡥࡲࡦࡵࡸࡰࡹࡃࠢᚹ") + str(bstack11llll11lll_opy_) + bstack111ll_opy_ (u"ࠣࠤᚺ"))
                if bstack11llll11lll_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack111ll_opy_ (u"ࠤࡸࡷ࡮ࡴࡧࠣᚻ"): bstack11llll11lll_opy_.locator_type,
                            bstack111ll_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤᚼ"): bstack11llll11lll_opy_.locator_value,
                        }
                    )
                    return bstack11llll11l11_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack111ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡎࡥࡄࡆࡄࡘࡋࠧᚽ"), False):
                    self.logger.info(bstack1l1ll1l1111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠭࡮࡫ࡶࡷ࡮ࡴࡧ࠻ࠢࡶࡰࡪ࡫ࡰࠩ࠵࠳࠭ࠥࡲࡥࡵࡶ࡬ࡲ࡬ࠦࡹࡰࡷࠣ࡭ࡳࡹࡰࡦࡥࡷࠤࡹ࡮ࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࠥࡲ࡯ࡨࡵࠥᚾ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack111ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭࡯ࡱ࠰ࡷࡨࡸࡩࡱࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠾ࠤᚿ") + str(response) + bstack111ll_opy_ (u"ࠢࠣᛀ"))
        except Exception as err:
            self.logger.warning(bstack111ll_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡶࡪࡹࡵ࡭ࡶ࠽ࠤࡪࡸࡲࡰࡴ࠽ࠤࠧᛁ") + str(err) + bstack111ll_opy_ (u"ࠤࠥᛂ"))
        raise exception
    @measure(event_name=EVENTS.bstack11llll111ll_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
    def bstack11llll1l111_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack111ll_opy_ (u"ࠥ࠴ࠧᛃ"),
    ):
        self.bstack11llllll111_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack111ll_opy_ (u"ࠦࠧᛄ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        req.client_worker_id = bstack111ll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᛅ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack111111ll1l_opy_.AISelfHealStep(req)
            self.logger.info(bstack111ll_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᛆ") + str(r) + bstack111ll_opy_ (u"ࠢࠣᛇ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111ll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᛈ") + str(e) + bstack111ll_opy_ (u"ࠤࠥᛉ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11llll1l11l_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
    def bstack11llll111l1_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack111ll_opy_ (u"ࠥ࠴ࠧᛊ")):
        self.bstack11llllll111_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        req.client_worker_id = bstack111ll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᛋ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack111111ll1l_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack111ll_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᛌ") + str(r) + bstack111ll_opy_ (u"ࠨࠢᛍ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111ll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᛎ") + str(e) + bstack111ll_opy_ (u"ࠣࠤᛏ"))
            traceback.print_exc()
            raise e