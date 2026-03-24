# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
from browserstack_sdk.sdk_cli.bstack1ll111llll1_opy_ import bstack1l1llll1l11_opy_
from browserstack_sdk.sdk_cli.bstack1ll11ll1_opy_ import (
    bstack111l11ll_opy_,
    bstack1lll1ll11_opy_,
    bstack1ll11l1l111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1111l1ll_opy_ import bstack1l1llll1111_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll111llll1_opy_ import bstack1l1llll1l11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1ll11111_opy_ import bstack1lll1lll11_opy_
import traceback
import os
import threading
import time
class bstack1ll1111111l_opy_(bstack1l1llll1l11_opy_):
    bstack1l1l1111lll_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1l1llll1111_opy_.bstack1l11l1lllll_opy_((bstack111l11ll_opy_.bstack1ll1ll111l1_opy_, bstack1lll1ll11_opy_.PRE), self.bstack1l11l1l1l11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l1l1l11_opy_(
        self,
        f: bstack1l1llll1111_opy_,
        driver: object,
        exec: Tuple[bstack1ll11l1l111_opy_, str],
        bstack1ll11l1ll11_opy_: Tuple[bstack111l11ll_opy_, bstack1lll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1l11l1l11l1_opy_(hub_url):
            if not bstack1ll1111111l_opy_.bstack1l1l1111lll_opy_:
                self.logger.warning(bstack1ll1lll_opy_ (u"ࠣ࡮ࡲࡧࡦࡲࠠࡴࡧ࡯ࡪ࠲࡮ࡥࡢ࡮ࠣࡪࡱࡵࡷࠡࡦ࡬ࡷࡦࡨ࡬ࡦࡦࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡩ࡯ࡨࡵࡥࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡩࡷࡥࡣࡺࡸ࡬࠾ࠤᔫ") + str(hub_url) + bstack1ll1lll_opy_ (u"ࠤࠥᔬ"))
                bstack1ll1111111l_opy_.bstack1l1l1111lll_opy_ = True
            return
        command_name = f.bstack1l1l1111l1l_opy_(*args)
        bstack1l11l1l11ll_opy_ = f.bstack1l11l11lll1_opy_(*args)
        if command_name and command_name.lower() == bstack1ll1lll_opy_ (u"ࠥࡪ࡮ࡴࡤࡦ࡮ࡨࡱࡪࡴࡴࠣᔭ") and bstack1l11l1l11ll_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1l11l1l11ll_opy_.get(bstack1ll1lll_opy_ (u"ࠦࡺࡹࡩ࡯ࡩࠥᔮ"), None), bstack1l11l1l11ll_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᔯ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1ll1lll_opy_ (u"ࠨࡻࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࢃ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡲࡶࠥࡧࡲࡨࡵ࠱ࡹࡸ࡯࡮ࡨ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡳࡷࠦࡡࡳࡩࡶ࠲ࡻࡧ࡬ࡶࡧࡀࠦᔰ") + str(locator_value) + bstack1ll1lll_opy_ (u"ࠢࠣᔱ"))
                return
            def bstack1ll1l1111ll_opy_(driver, bstack1l11l11ll1l_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1l11l11ll1l_opy_(driver, *args, **kwargs)
                    response = self.bstack1l11l11llll_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1ll1lll_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴ࠯ࡶࡧࡷ࡯ࡰࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࠦᔲ") + str(locator_value) + bstack1ll1lll_opy_ (u"ࠤࠥᔳ"))
                    else:
                        self.logger.warning(bstack1ll1lll_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶ࠱ࡳࡵ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣࡶࡪࡹࡰࡰࡰࡶࡩࡂࠨᔴ") + str(response) + bstack1ll1lll_opy_ (u"ࠦࠧᔵ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1l11l11ll11_opy_(
                        driver, bstack1l11l11ll1l_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1ll1l1111ll_opy_.__name__ = command_name
            return bstack1ll1l1111ll_opy_
    def __1l11l11ll11_opy_(
        self,
        driver,
        bstack1l11l11ll1l_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1l11l11llll_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1ll1lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡵࡴ࡬࡫࡬࡫ࡲࡦࡦ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࠧᔶ") + str(locator_value) + bstack1ll1lll_opy_ (u"ࠨࠢᔷ"))
                bstack1l11l1l1ll1_opy_ = self.bstack1l11l1l1l1l_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1ll1lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡵࡩࡸࡻ࡬ࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࢁࠥ࡮ࡥࡢ࡮࡬ࡲ࡬ࡥࡲࡦࡵࡸࡰࡹࡃࠢᔸ") + str(bstack1l11l1l1ll1_opy_) + bstack1ll1lll_opy_ (u"ࠣࠤᔹ"))
                if bstack1l11l1l1ll1_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1ll1lll_opy_ (u"ࠤࡸࡷ࡮ࡴࡧࠣᔺ"): bstack1l11l1l1ll1_opy_.locator_type,
                            bstack1ll1lll_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤᔻ"): bstack1l11l1l1ll1_opy_.locator_value,
                        }
                    )
                    return bstack1l11l11ll1l_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1ll1lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡎࡥࡄࡆࡄࡘࡋࠧᔼ"), False):
                    self.logger.info(bstack1ll11ll11l1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠭࡮࡫ࡶࡷ࡮ࡴࡧ࠻ࠢࡶࡰࡪ࡫ࡰࠩ࠵࠳࠭ࠥࡲࡥࡵࡶ࡬ࡲ࡬ࠦࡹࡰࡷࠣ࡭ࡳࡹࡰࡦࡥࡷࠤࡹ࡮ࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࠥࡲ࡯ࡨࡵࠥᔽ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1ll1lll_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭࡯ࡱ࠰ࡷࡨࡸࡩࡱࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠾ࠤᔾ") + str(response) + bstack1ll1lll_opy_ (u"ࠢࠣᔿ"))
        except Exception as err:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡶࡪࡹࡵ࡭ࡶ࠽ࠤࡪࡸࡲࡰࡴ࠽ࠤࠧᕀ") + str(err) + bstack1ll1lll_opy_ (u"ࠤࠥᕁ"))
        raise exception
    @measure(event_name=EVENTS.bstack1l11l1l1111_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def bstack1l11l11llll_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1ll1lll_opy_ (u"ࠥ࠴ࠧᕂ"),
    ):
        self.bstack1l11l1ll111_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1ll1lll_opy_ (u"ࠦࠧᕃ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᕄ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1l1ll1l1ll1_opy_.AISelfHealStep(req)
            self.logger.info(bstack1ll1lll_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᕅ") + str(r) + bstack1ll1lll_opy_ (u"ࠢࠣᕆ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᕇ") + str(e) + bstack1ll1lll_opy_ (u"ࠤࠥᕈ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11l1l111l_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def bstack1l11l1l1l1l_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1ll1lll_opy_ (u"ࠥ࠴ࠧᕉ")):
        self.bstack1l11l1ll111_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᕊ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1l1ll1l1ll1_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1ll1lll_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᕋ") + str(r) + bstack1ll1lll_opy_ (u"ࠨࠢᕌ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᕍ") + str(e) + bstack1ll1lll_opy_ (u"ࠣࠤᕎ"))
            traceback.print_exc()
            raise e