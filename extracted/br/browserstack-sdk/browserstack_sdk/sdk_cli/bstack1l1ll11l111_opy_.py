# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
from browserstack_sdk.sdk_cli.bstack1l1ll1l11ll_opy_ import bstack1l1lllllll1_opy_
from browserstack_sdk.sdk_cli.bstack1llll1ll1l_opy_ import (
    bstack111ll1lll1_opy_,
    bstack11lllll11l_opy_,
    bstack1ll11llllll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1ll1lllll_opy_ import bstack1ll111l11ll_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1ll1l11ll_opy_ import bstack1l1lllllll1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1lll11lll_opy_ import bstack1llll11l_opy_
import traceback
import os
import threading
import time
class bstack1l1ll1l1l1l_opy_(bstack1l1lllllll1_opy_):
    bstack1l11l1ll111_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1ll111l11ll_opy_.bstack1l1l111lll1_opy_((bstack111ll1lll1_opy_.bstack1ll1l11lll1_opy_, bstack11lllll11l_opy_.PRE), self.bstack1l11l1l11ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l1l11ll_opy_(
        self,
        f: bstack1ll111l11ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1l11l11ll1l_opy_(hub_url):
            if not bstack1l1ll1l1l1l_opy_.bstack1l11l1ll111_opy_:
                self.logger.warning(bstack11lll1_opy_ (u"ࠧࡲ࡯ࡤࡣ࡯ࠤࡸ࡫࡬ࡧ࠯࡫ࡩࡦࡲࠠࡧ࡮ࡲࡻࠥࡪࡩࡴࡣࡥࡰࡪࡪࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣ࡭ࡳ࡬ࡲࡢࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤ࡭ࡻࡢࡠࡷࡵࡰࡂࠨᔯ") + str(hub_url) + bstack11lll1_opy_ (u"ࠨࠢᔰ"))
                bstack1l1ll1l1l1l_opy_.bstack1l11l1ll111_opy_ = True
            return
        command_name = f.bstack1l11l1lll11_opy_(*args)
        bstack1l11l1l1l11_opy_ = f.bstack1l11l11llll_opy_(*args)
        if command_name and command_name.lower() == bstack11lll1_opy_ (u"ࠢࡧ࡫ࡱࡨࡪࡲࡥ࡮ࡧࡱࡸࠧᔱ") and bstack1l11l1l1l11_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1l11l1l1l11_opy_.get(bstack11lll1_opy_ (u"ࠣࡷࡶ࡭ࡳ࡭ࠢᔲ"), None), bstack1l11l1l1l11_opy_.get(bstack11lll1_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣᔳ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack11lll1_opy_ (u"ࠥࡿࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࢀ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠦ࡯ࡳࠢࡤࡶ࡬ࡹ࠮ࡶࡵ࡬ࡲ࡬ࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠࡰࡴࠣࡥࡷ࡭ࡳ࠯ࡸࡤࡰࡺ࡫࠽ࠣᔴ") + str(locator_value) + bstack11lll1_opy_ (u"ࠦࠧᔵ"))
                return
            def bstack1ll11l11l1l_opy_(driver, bstack1l11l1l11l1_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1l11l1l11l1_opy_(driver, *args, **kwargs)
                    response = self.bstack1l11l1l1l1l_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack11lll1_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࠣᔶ") + str(locator_value) + bstack11lll1_opy_ (u"ࠨࠢᔷ"))
                    else:
                        self.logger.warning(bstack11lll1_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳ࠮ࡰࡲ࠱ࡸࡩࡲࡪࡲࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࢃࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠿ࠥᔸ") + str(response) + bstack11lll1_opy_ (u"ࠣࠤᔹ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1l11l1l111l_opy_(
                        driver, bstack1l11l1l11l1_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1ll11l11l1l_opy_.__name__ = command_name
            return bstack1ll11l11l1l_opy_
    def __1l11l1l111l_opy_(
        self,
        driver,
        bstack1l11l1l11l1_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1l11l1l1l1l_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack11lll1_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡹࡸࡩࡨࡩࡨࡶࡪࡪ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࠤᔺ") + str(locator_value) + bstack11lll1_opy_ (u"ࠥࠦᔻ"))
                bstack1l11l11lll1_opy_ = self.bstack1l11l1l1111_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack11lll1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢ࡫ࡩࡦࡲࡩ࡯ࡩࡢࡶࡪࡹࡵ࡭ࡶࡀࠦᔼ") + str(bstack1l11l11lll1_opy_) + bstack11lll1_opy_ (u"ࠧࠨᔽ"))
                if bstack1l11l11lll1_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack11lll1_opy_ (u"ࠨࡵࡴ࡫ࡱ࡫ࠧᔾ"): bstack1l11l11lll1_opy_.locator_type,
                            bstack11lll1_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨᔿ"): bstack1l11l11lll1_opy_.locator_value,
                        }
                    )
                    return bstack1l11l1l11l1_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack11lll1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡋࡢࡈࡊࡈࡕࡈࠤᕀ"), False):
                    self.logger.info(bstack1ll11ll1ll1_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡷ࡫ࡳࡶ࡮ࡷ࠱ࡲ࡯ࡳࡴ࡫ࡱ࡫࠿ࠦࡳ࡭ࡧࡨࡴ࠭࠹࠰ࠪࠢ࡯ࡩࡹࡺࡩ࡯ࡩࠣࡽࡴࡻࠠࡪࡰࡶࡴࡪࡩࡴࠡࡶ࡫ࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࠢ࡯ࡳ࡬ࡹࠢᕁ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack11lll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱ࡳࡵ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣࡶࡪࡹࡰࡰࡰࡶࡩࡂࠨᕂ") + str(response) + bstack11lll1_opy_ (u"ࠦࠧᕃ"))
        except Exception as err:
            self.logger.warning(bstack11lll1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠺ࠡࡧࡵࡶࡴࡸ࠺ࠡࠤᕄ") + str(err) + bstack11lll1_opy_ (u"ࠨࠢᕅ"))
        raise exception
    @measure(event_name=EVENTS.bstack1l11l11ll11_opy_, stage=STAGE.bstack1lllllll11_opy_)
    def bstack1l11l1l1l1l_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack11lll1_opy_ (u"ࠢ࠱ࠤᕆ"),
    ):
        self.bstack1l1l1111l1l_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack11lll1_opy_ (u"ࠣࠤᕇ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        req.client_worker_id = bstack11lll1_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᕈ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1l1lll11l11_opy_.AISelfHealStep(req)
            self.logger.info(bstack11lll1_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᕉ") + str(r) + bstack11lll1_opy_ (u"ࠦࠧᕊ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11lll1_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᕋ") + str(e) + bstack11lll1_opy_ (u"ࠨࠢᕌ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11l1l1ll1_opy_, stage=STAGE.bstack1lllllll11_opy_)
    def bstack1l11l1l1111_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack11lll1_opy_ (u"ࠢ࠱ࠤᕍ")):
        self.bstack1l1l1111l1l_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        req.client_worker_id = bstack11lll1_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᕎ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1l1lll11l11_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack11lll1_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᕏ") + str(r) + bstack11lll1_opy_ (u"ࠥࠦᕐ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11lll1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᕑ") + str(e) + bstack11lll1_opy_ (u"ࠧࠨᕒ"))
            traceback.print_exc()
            raise e