# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
from browserstack_sdk.sdk_cli.bstack1l11l1ll1ll_opy_ import bstack1l1l1111111_opy_
from browserstack_sdk.sdk_cli.bstack1l11ll1ll1_opy_ import (
    bstack1lll11l1l1_opy_,
    bstack1111llll1l_opy_,
    bstack1l1ll11l1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1l111lll1_opy_ import bstack1l1l111l111_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l11l1ll1ll_opy_ import bstack1l1l1111111_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack11l11lll_opy_ import bstack11lll1111_opy_
import traceback
import os
import threading
import time
class bstack1l1l11111l1_opy_(bstack1l1l1111111_opy_):
    bstack1l11111ll1l_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1l1l111l111_opy_.bstack1l1111lllll_opy_((bstack1lll11l1l1_opy_.bstack1ll1111ll1l_opy_, bstack1111llll1l_opy_.PRE), self.bstack11llll11l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11llll11l1l_opy_(
        self,
        f: bstack1l1l111l111_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack11llll1lll1_opy_(hub_url):
            if not bstack1l1l11111l1_opy_.bstack1l11111ll1l_opy_:
                self.logger.warning(bstack1l1111l_opy_ (u"ࠢ࡭ࡱࡦࡥࡱࠦࡳࡦ࡮ࡩ࠱࡭࡫ࡡ࡭ࠢࡩࡰࡴࡽࠠࡥ࡫ࡶࡥࡧࡲࡥࡥࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥ࡯࡮ࡧࡴࡤࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡨࡶࡤࡢࡹࡷࡲ࠽ࠣ᚝") + str(hub_url) + bstack1l1111l_opy_ (u"ࠣࠤ᚞"))
                bstack1l1l11111l1_opy_.bstack1l11111ll1l_opy_ = True
            return
        command_name = f.bstack1l1111l11l1_opy_(*args)
        bstack11llll1l1l1_opy_ = f.bstack11llll11ll1_opy_(*args)
        if command_name and command_name.lower() == bstack1l1111l_opy_ (u"ࠤࡩ࡭ࡳࡪࡥ࡭ࡧࡰࡩࡳࡺࠢ᚟") and bstack11llll1l1l1_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack11llll1l1l1_opy_.get(bstack1l1111l_opy_ (u"ࠥࡹࡸ࡯࡮ࡨࠤᚠ"), None), bstack11llll1l1l1_opy_.get(bstack1l1111l_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥᚡ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1l1111l_opy_ (u"ࠧࢁࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࢂࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠡࡱࡵࠤࡦࡸࡧࡴ࠰ࡸࡷ࡮ࡴࡧ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢࡲࡶࠥࡧࡲࡨࡵ࠱ࡺࡦࡲࡵࡦ࠿ࠥᚢ") + str(locator_value) + bstack1l1111l_opy_ (u"ࠨࠢᚣ"))
                return
            def bstack1l1ll111l1l_opy_(driver, bstack11llll1l111_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack11llll1l111_opy_(driver, *args, **kwargs)
                    response = self.bstack11llll11l11_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1l1111l_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳ࠮ࡵࡦࡶ࡮ࡶࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࠥᚤ") + str(locator_value) + bstack1l1111l_opy_ (u"ࠣࠤᚥ"))
                    else:
                        self.logger.warning(bstack1l1111l_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵ࠰ࡲࡴ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࡁࠧᚦ") + str(response) + bstack1l1111l_opy_ (u"ࠥࠦᚧ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__11llll1l11l_opy_(
                        driver, bstack11llll1l111_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1l1ll111l1l_opy_.__name__ = command_name
            return bstack1l1ll111l1l_opy_
    def __11llll1l11l_opy_(
        self,
        driver,
        bstack11llll1l111_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack11llll11l11_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1l1111l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡴࡳ࡫ࡪ࡫ࡪࡸࡥࡥ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࠦᚨ") + str(locator_value) + bstack1l1111l_opy_ (u"ࠧࠨᚩ"))
                bstack11llll11lll_opy_ = self.bstack11llll1ll1l_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1l1111l_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭ࡩࡧࡤࡰ࡮ࡴࡧ࠮ࡴࡨࡷࡺࡲࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࢀࠤ࡭࡫ࡡ࡭࡫ࡱ࡫ࡤࡸࡥࡴࡷ࡯ࡸࡂࠨᚪ") + str(bstack11llll11lll_opy_) + bstack1l1111l_opy_ (u"ࠢࠣᚫ"))
                if bstack11llll11lll_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1l1111l_opy_ (u"ࠣࡷࡶ࡭ࡳ࡭ࠢᚬ"): bstack11llll11lll_opy_.locator_type,
                            bstack1l1111l_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣᚭ"): bstack11llll11lll_opy_.locator_value,
                        }
                    )
                    return bstack11llll1l111_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1l1111l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡍࡤࡊࡅࡃࡗࡊࠦᚮ"), False):
                    self.logger.info(bstack1l1ll1l11l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹ࠳࡭ࡪࡵࡶ࡭ࡳ࡭࠺ࠡࡵ࡯ࡩࡪࡶࠨ࠴࠲ࠬࠤࡱ࡫ࡴࡵ࡫ࡱ࡫ࠥࡿ࡯ࡶࠢ࡬ࡲࡸࡶࡥࡤࡶࠣࡸ࡭࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡧࡻࡸࡪࡴࡳࡪࡱࡱࠤࡱࡵࡧࡴࠤᚯ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1l1111l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳࡮ࡰ࠯ࡶࡧࡷ࡯ࡰࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࢁࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠽ࠣᚰ") + str(response) + bstack1l1111l_opy_ (u"ࠨࠢᚱ"))
        except Exception as err:
            self.logger.warning(bstack1l1111l_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡵࡩࡸࡻ࡬ࡵ࠼ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠦᚲ") + str(err) + bstack1l1111l_opy_ (u"ࠣࠤᚳ"))
        raise exception
    @measure(event_name=EVENTS.bstack11llll1l1ll_opy_, stage=STAGE.bstack111ll11111_opy_)
    def bstack11llll11l11_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1l1111l_opy_ (u"ࠤ࠳ࠦᚴ"),
    ):
        self.bstack1l1111l1ll1_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1l1111l_opy_ (u"ࠥࠦᚵ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        req.client_worker_id = bstack1l1111l_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᚶ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack11l1ll1lll_opy_.AISelfHealStep(req)
            self.logger.info(bstack1l1111l_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᚷ") + str(r) + bstack1l1111l_opy_ (u"ࠨࠢᚸ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1111l_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᚹ") + str(e) + bstack1l1111l_opy_ (u"ࠣࠤᚺ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11llll1ll11_opy_, stage=STAGE.bstack111ll11111_opy_)
    def bstack11llll1ll1l_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1l1111l_opy_ (u"ࠤ࠳ࠦᚻ")):
        self.bstack1l1111l1ll1_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        req.client_worker_id = bstack1l1111l_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᚼ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack11l1ll1lll_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1l1111l_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᚽ") + str(r) + bstack1l1111l_opy_ (u"ࠧࠨᚾ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1111l_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᚿ") + str(e) + bstack1l1111l_opy_ (u"ࠢࠣᛀ"))
            traceback.print_exc()
            raise e