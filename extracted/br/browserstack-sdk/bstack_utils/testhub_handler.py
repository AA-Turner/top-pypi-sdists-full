# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1111l1l111l_opy_, bstack1111ll1l11l_opy_, bstack1l1111l111_opy_, error_handler, bstack1lllll111l11_opy_, bstack1ll1llll1l1_opy_, bstack1lllll1lll1l_opy_, bstack11l1ll1ll_opy_, bstack1llll1lll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1ll1l111ll11_opy_ import bstack1ll1l111ll1l_opy_
import bstack_utils.bstack1l11llll11_opy_ as TestHubUtils
from bstack_utils.bstack1l1l11l1_opy_ import bstack111l111ll1_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.bstack1llll11l111_opy_ import bstack1lll11l1ll1_opy_
from bstack_utils.constants import bstack1lll1ll11l_opy_
bstack1ll111llll11_opy_ = bstack1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡣࡰ࡮࡯ࡩࡨࡺ࡯ࡳ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ❳")
logger = logging.getLogger(__name__)
class TestHubHandler:
    bstack1ll1l111ll11_opy_ = None
    bs_config = None
    bstack11ll1ll11_opy_ = None
    _1ll11l111ll1_opy_ = False
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11111l11ll1_opy_, stage=STAGE.bstack11llll111l_opy_)
    def launch(cls, bs_config, bstack11ll1ll11_opy_):
        cls._1ll11l111ll1_opy_ = True
        cls.bs_config = bs_config
        cls.bstack11ll1ll11_opy_ = bstack11ll1ll11_opy_
        try:
            cls.bstack1ll11l1111l1_opy_()
            bstack1111ll11l1l_opy_ = bstack1111l1l111l_opy_(bs_config)
            bstack1111lll1l1l_opy_ = bstack1111ll1l11l_opy_(bs_config)
            data = TestHubUtils.bstack1ll11l1l1111_opy_(bs_config, bstack11ll1ll11_opy_)
            config = {
                bstack1ll_opy_ (u"࠭ࡡࡶࡶ࡫ࠫ❴"): (bstack1111ll11l1l_opy_, bstack1111lll1l1l_opy_),
                bstack1ll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ❵"): cls.default_headers()
            }
            response = bstack1l1111l111_opy_(bstack1ll_opy_ (u"ࠨࡒࡒࡗ࡙࠭❶"), cls.request_url(bstack1ll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠳࠱ࡥࡹ࡮ࡲࡤࡴࠩ❷")), data, config)
            if response.status_code != 200:
                bstack11lllllll1_opy_ = response.json()
                if bstack11lllllll1_opy_[bstack1ll_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ❸")] == False:
                    cls.bstack1ll11l11ll1l_opy_(bstack11lllllll1_opy_)
                    return
                cls.bstack1ll11l11llll_opy_(bstack11lllllll1_opy_[bstack1ll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ❹")])
                cls.bstack1ll11l111l11_opy_(bstack11lllllll1_opy_[bstack1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ❺")])
                return None
            bstack1ll11l111lll_opy_ = cls.bstack1ll11l1l111l_opy_(response)
            return bstack1ll11l111lll_opy_, response.json()
        except Exception as error:
            logger.error(bstack1ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࡽࢀࠦ❻").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111111l1lll_opy_, stage=STAGE.bstack11llll111l_opy_)
    def stop(cls, bstack1ll11l11l11l_opy_=None):
        if not bstack111l111ll1_opy_.on() and not a11y.on():
            return
        if not cls._1ll11l111ll1_opy_:
            logger.info(bstack1ll_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࠦࡩࡴࠢࡆࡐࡎ࠳࡭ࡢࡰࡤ࡫ࡪࡪࠠࠩ࡮ࡤࡹࡳࡩࡨࠡࡰࡲࡸࠥࡩࡡ࡭࡮ࡨࡨࠥࡨࡹࠡࡕࡇࡏ࠮ࠦ࠭ࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡷࡹࡵࡰࠡࡃࡓࡍࠥࡸࡥࡲࡷࡨࡷࡹࠨ❼"))
            if cls.bstack1ll1l111ll11_opy_ is not None:
                logger.info(bstack1ll_opy_ (u"ࠣࡕ࡫ࡹࡹࡺࡩ࡯ࡩࠣࡨࡴࡽ࡮ࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡴࡹࡪࡻࡥࠣ❽"))
                cls.bstack1ll1l111ll11_opy_.shutdown()
            else:
                logger.info(bstack1ll_opy_ (u"ࠤࡑࡳࠥࡸࡥࡲࡷࡨࡷࡹࠦࡱࡶࡧࡸࡩࠥࡺ࡯ࠡࡵ࡫ࡹࡹࡪ࡯ࡸࡰࠥ❾"))
            return
        if os.environ.get(bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ❿")) == bstack1ll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ➀") or os.environ.get(bstack1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ➁")) == bstack1ll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ➂"):
            logger.error(bstack1ll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡳࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡥࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤࡹࡵ࡫ࡦࡰࠪ➃"))
            return {
                bstack1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ➄"): bstack1ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ➅"),
                bstack1ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ➆"): bstack1ll_opy_ (u"࡙ࠫࡵ࡫ࡦࡰ࠲ࡦࡺ࡯࡬ࡥࡋࡇࠤ࡮ࡹࠠࡶࡰࡧࡩ࡫࡯࡮ࡦࡦ࠯ࠤࡧࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥࡳࡩࡨࡪࡷࠤ࡭ࡧࡶࡦࠢࡩࡥ࡮ࡲࡥࡥࠩ➇")
            }
        try:
            cls.bstack1ll1l111ll11_opy_.shutdown()
            data = {
                bstack1ll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ➈"): bstack11l1ll1ll_opy_()
            }
            if not bstack1ll11l11l11l_opy_ is None:
                data[bstack1ll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠪ➉")] = [{
                    bstack1ll_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ➊"): bstack1ll_opy_ (u"ࠨࡷࡶࡩࡷࡥ࡫ࡪ࡮࡯ࡩࡩ࠭➋"),
                    bstack1ll_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭ࠩ➌"): bstack1ll11l11l11l_opy_
                }]
            config = {
                bstack1ll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫ➍"): cls.default_headers()
            }
            bstack1111l11l11l_opy_ = bstack1ll_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡴࡶࡲࡴࠬ➎").format(os.environ[bstack1ll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥ➏")])
            bstack1ll111llllll_opy_ = cls.request_url(bstack1111l11l11l_opy_)
            response = bstack1l1111l111_opy_(bstack1ll_opy_ (u"࠭ࡐࡖࡖࠪ➐"), bstack1ll111llllll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1ll_opy_ (u"ࠢࡔࡶࡲࡴࠥࡸࡥࡲࡷࡨࡷࡹࠦ࡮ࡰࡶࠣࡳࡰࠨ➑"))
        except Exception as error:
            logger.error(bstack1ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡴࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡖࡨࡷࡹࡎࡵࡣ࠼࠽ࠤࠧ➒") + str(error))
            return {
                bstack1ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ➓"): bstack1ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ➔"),
                bstack1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ➕"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll11l1l111l_opy_(cls, response):
        bstack11lllllll1_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1ll11l111lll_opy_ = {}
        if bstack11lllllll1_opy_.get(bstack1ll_opy_ (u"ࠬࡰࡷࡵࠩ➖")) is None:
            os.environ[bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ➗")] = bstack1ll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ➘")
        else:
            os.environ[bstack1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ➙")] = bstack11lllllll1_opy_.get(bstack1ll_opy_ (u"ࠩ࡭ࡻࡹ࠭➚"), bstack1ll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ➛"))
        os.environ[bstack1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ➜")] = bstack11lllllll1_opy_.get(bstack1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ➝"), bstack1ll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ➞"))
        logger.info(bstack1ll_opy_ (u"ࠧࡕࡧࡶࡸ࡭ࡻࡢࠡࡵࡷࡥࡷࡺࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡪࡦ࠽ࠤࠬ➟") + os.getenv(bstack1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭➠")));
        if bstack111l111ll1_opy_.bstack1ll111lllll1_opy_(cls.bs_config, cls.bstack11ll1ll11_opy_.get(bstack1ll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪ➡"), bstack1ll_opy_ (u"ࠪࠫ➢"))) is True:
            bstack1ll1l1111l11_opy_, build_hashed_id, allow_screenshots = cls.bstack1ll111lll1ll_opy_(bstack11lllllll1_opy_)
            if bstack1ll1l1111l11_opy_ != None and build_hashed_id != None:
                bstack1ll11l111lll_opy_[bstack1ll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ➣")] = {
                    bstack1ll_opy_ (u"ࠬࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠨ➤"): bstack1ll1l1111l11_opy_,
                    bstack1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ➥"): build_hashed_id,
                    bstack1ll_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ➦"): allow_screenshots
                }
            else:
                bstack1ll11l111lll_opy_[bstack1ll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ➧")] = {}
        else:
            bstack1ll11l111lll_opy_[bstack1ll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ➨")] = {}
        bstack1ll11l1l11ll_opy_, build_hashed_id = cls.bstack1ll11l11l1l1_opy_(bstack11lllllll1_opy_)
        if bstack1ll11l1l11ll_opy_ != None and build_hashed_id != None:
            bstack1ll11l111lll_opy_[bstack1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ➩")] = {
                bstack1ll_opy_ (u"ࠫࡦࡻࡴࡩࡡࡷࡳࡰ࡫࡮ࠨ➪"): bstack1ll11l1l11ll_opy_,
                bstack1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ➫"): build_hashed_id,
            }
        else:
            bstack1ll11l111lll_opy_[bstack1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭➬")] = {}
        if bstack1ll11l111lll_opy_[bstack1ll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ➭")].get(bstack1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ➮")) != None or bstack1ll11l111lll_opy_[bstack1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ➯")].get(bstack1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ➰")) != None:
            cls.bstack1ll11l11lll1_opy_(bstack11lllllll1_opy_.get(bstack1ll_opy_ (u"ࠫ࡯ࡽࡴࠨ➱")), bstack11lllllll1_opy_.get(bstack1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ➲")))
        return bstack1ll11l111lll_opy_
    @classmethod
    def bstack1ll111lll1ll_opy_(cls, bstack11lllllll1_opy_):
        if bstack11lllllll1_opy_.get(bstack1ll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭➳")) == None:
            cls.bstack1ll11l11llll_opy_()
            return [None, None, None]
        if bstack11lllllll1_opy_[bstack1ll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ➴")][bstack1ll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ➵")] != True:
            cls.bstack1ll11l11llll_opy_(bstack11lllllll1_opy_[bstack1ll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ➶")])
            return [None, None, None]
        logger.debug(bstack1ll_opy_ (u"ࠪࡿࢂࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠥࠬ➷").format(bstack1lll1ll11l_opy_))
        os.environ[bstack1ll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪ➸")] = bstack1ll_opy_ (u"ࠬࡺࡲࡶࡧࠪ➹")
        if bstack11lllllll1_opy_.get(bstack1ll_opy_ (u"࠭ࡪࡸࡶࠪ➺")):
            os.environ[bstack1ll_opy_ (u"ࠧࡄࡔࡈࡈࡊࡔࡔࡊࡃࡏࡗࡤࡌࡏࡓࡡࡆࡖࡆ࡙ࡈࡠࡔࡈࡔࡔࡘࡔࡊࡐࡊࠫ➻")] = json.dumps({
                bstack1ll_opy_ (u"ࠨࡷࡶࡩࡷࡴࡡ࡮ࡧࠪ➼"): bstack1111l1l111l_opy_(cls.bs_config),
                bstack1ll_opy_ (u"ࠩࡳࡥࡸࡹࡷࡰࡴࡧࠫ➽"): bstack1111ll1l11l_opy_(cls.bs_config)
            })
        if bstack11lllllll1_opy_.get(bstack1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ➾")):
            os.environ[bstack1ll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪ➿")] = bstack11lllllll1_opy_[bstack1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⟀")]
        if bstack11lllllll1_opy_[bstack1ll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⟁")].get(bstack1ll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ⟂"), {}).get(bstack1ll_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ⟃")):
            os.environ[bstack1ll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ⟄")] = str(bstack11lllllll1_opy_[bstack1ll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⟅")][bstack1ll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ⟆")][bstack1ll_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ⟇")])
        else:
            os.environ[bstack1ll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧ⟈")] = bstack1ll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ⟉")
        return [bstack11lllllll1_opy_[bstack1ll_opy_ (u"ࠨ࡬ࡺࡸࠬ⟊")], bstack11lllllll1_opy_[bstack1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⟋")], os.environ[bstack1ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫ⟌")]]
    @classmethod
    def bstack1ll11l11l1l1_opy_(cls, bstack11lllllll1_opy_):
        if bstack11lllllll1_opy_.get(bstack1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⟍")) == None:
            cls.bstack1ll11l111l11_opy_()
            return [None, None]
        if bstack11lllllll1_opy_[bstack1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⟎")][bstack1ll_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ⟏")] != True:
            cls.bstack1ll11l111l11_opy_(bstack11lllllll1_opy_[bstack1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⟐")])
            return [None, None]
        if bstack11lllllll1_opy_[bstack1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⟑")].get(bstack1ll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ⟒")):
            logger.debug(bstack1ll_opy_ (u"ࠪࡘࡪࡹࡴࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࠧࠧ⟓"))
            parsed = json.loads(os.getenv(bstack1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ⟔"), bstack1ll_opy_ (u"ࠬࢁࡽࠨ⟕")))
            capabilities = TestHubUtils.bstack1ll11l111l1l_opy_(bstack11lllllll1_opy_[bstack1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⟖")][bstack1ll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ⟗")][bstack1ll_opy_ (u"ࠨࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ⟘")], bstack1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⟙"), bstack1ll_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩ⟚"))
            bstack1ll11l1l11ll_opy_ = capabilities[bstack1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩ⟛")]
            os.environ[bstack1ll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ⟜")] = bstack1ll11l1l11ll_opy_
            if capabilities.get(bstack1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫ⟝")):
                os.environ[bstack1ll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡖࡈࡗ࡙ࡥࡒࡖࡐࡢࡍࡉ࠭⟞")] = str(capabilities[bstack1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢ࡭ࡩ࠭⟟")])
            if capabilities.get(bstack1ll_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡢࡦࡺ࡯࡬ࡥࡡࡸࡹ࡮ࡪࠧ⟠")):
                os.environ[bstack1ll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡇ࡛ࡉࡍࡆࡢ࡙࡚ࡏࡄࠨ⟡")] = str(capabilities[bstack1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡤࡨࡵࡪ࡮ࡧࡣࡺࡻࡩࡥࠩ⟢")])
            if bstack1ll_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫ࠢ⟣") in bstack11lllllll1_opy_ and bstack11lllllll1_opy_.get(bstack1ll_opy_ (u"ࠨࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠧ⟤")) is None:
                parsed[bstack1ll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⟥")] = capabilities[bstack1ll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ⟦")]
            os.environ[bstack1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ⟧")] = json.dumps(parsed)
            scripts = TestHubUtils.bstack1ll11l111l1l_opy_(bstack11lllllll1_opy_[bstack1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⟨")][bstack1ll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ⟩")][bstack1ll_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭⟪")], bstack1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⟫"), bstack1ll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࠨ⟬"))
            accessibility_scripts.bstack11lll1l1_opy_(scripts)
            commands_to_wrap = bstack11lllllll1_opy_[bstack1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⟭")][bstack1ll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ⟮")][bstack1ll_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷ࡙ࡵࡗࡳࡣࡳࠫ⟯")]
            commands = commands_to_wrap.get(bstack1ll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭⟰"))
            accessibility_scripts.bstack1l1l1l1l111_opy_(commands)
            scripts_to_run = commands_to_wrap.get(bstack1ll_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࡚࡯ࡓࡷࡱࠫ⟱"))
            accessibility_scripts.bstack1111l11ll11_opy_(scripts_to_run)
            bstack1111ll11l11_opy_ = capabilities.get(bstack1ll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ⟲"))
            accessibility_scripts.bstack1111l11lll1_opy_(bstack1111ll11l11_opy_)
            accessibility_scripts.store()
        return [bstack1ll11l1l11ll_opy_, bstack11lllllll1_opy_[bstack1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ⟳")]]
    @classmethod
    def bstack1ll11l11llll_opy_(cls, response=None):
        os.environ[bstack1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⟴")] = bstack1ll_opy_ (u"ࠩࡱࡹࡱࡲࠧ⟵")
        os.environ[bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⟶")] = bstack1ll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ⟷")
        os.environ[bstack1ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡅࡒࡑࡕࡒࡅࡕࡇࡇࠫ⟸")] = bstack1ll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ⟹")
        os.environ[bstack1ll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭⟺")] = bstack1ll_opy_ (u"ࠣࡰࡸࡰࡱࠨ⟻")
        os.environ[bstack1ll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ⟼")] = bstack1ll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ⟽")
        cls.bstack1ll11l11ll1l_opy_(response, bstack1ll_opy_ (u"ࠦࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠦ⟾"))
        return [None, None, None]
    @classmethod
    def bstack1ll11l111l11_opy_(cls, response=None):
        os.environ[bstack1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⟿")] = bstack1ll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ⠀")
        os.environ[bstack1ll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ⠁")] = bstack1ll_opy_ (u"ࠨࡰࡸࡰࡱ࠭⠂")
        os.environ[bstack1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⠃")] = bstack1ll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ⠄")
        cls.bstack1ll11l11ll1l_opy_(response, bstack1ll_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦ⠅"))
        return [None, None, None]
    @classmethod
    def bstack1ll11l11lll1_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⠆")] = jwt
        os.environ[bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⠇")] = build_hashed_id
    @classmethod
    def bstack1ll11l11ll1l_opy_(cls, response=None, product=bstack1ll_opy_ (u"ࠢࠣ⠈")):
        if response == None or response.get(bstack1ll_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨ⠉")) == None:
            logger.error(product + bstack1ll_opy_ (u"ࠤࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠦ⠊"))
            return
        for error in response[bstack1ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪ⠋")]:
            bstack1llll1l1l111_opy_ = error[bstack1ll_opy_ (u"ࠫࡰ࡫ࡹࠨ⠌")]
            error_message = error[bstack1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⠍")]
            if error_message:
                if bstack1llll1l1l111_opy_ == bstack1ll_opy_ (u"ࠨࡅࡓࡔࡒࡖࡤࡇࡃࡄࡇࡖࡗࡤࡊࡅࡏࡋࡈࡈࠧ⠎"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1ll_opy_ (u"ࠢࡅࡣࡷࡥࠥࡻࡰ࡭ࡱࡤࡨࠥࡺ࡯ࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࠣ⠏") + product + bstack1ll_opy_ (u"ࠣࠢࡩࡥ࡮ࡲࡥࡥࠢࡧࡹࡪࠦࡴࡰࠢࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨ⠐"))
    @classmethod
    def bstack1ll11l1111l1_opy_(cls):
        if cls.bstack1ll1l111ll11_opy_ is not None:
            return
        cls.bstack1ll1l111ll11_opy_ = bstack1ll1l111ll1l_opy_(cls.post_data)
        cls.bstack1ll1l111ll11_opy_.start()
    @classmethod
    def bstack1lll11l1lll_opy_(cls):
        if cls.bstack1ll1l111ll11_opy_ is None:
            return
        cls.bstack1ll1l111ll11_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def post_data(cls, bstack1lll1llll11_opy_, event_url=bstack1ll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨ⠑")):
        config = {
            bstack1ll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫ⠒"): cls.default_headers()
        }
        logger.debug(bstack1ll_opy_ (u"ࠦࡵࡵࡳࡵࡡࡧࡥࡹࡧ࠺ࠡࡕࡨࡲࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡵࡱࠣࡸࡪࡹࡴࡩࡷࡥࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺࡳࠡࡽࢀࠦ⠓").format(bstack1ll_opy_ (u"ࠬ࠲ࠠࠨ⠔").join([event[bstack1ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⠕")] for event in bstack1lll1llll11_opy_])))
        response = bstack1l1111l111_opy_(bstack1ll_opy_ (u"ࠧࡑࡑࡖࡘࠬ⠖"), cls.request_url(event_url), bstack1lll1llll11_opy_, config)
        bstack1111ll1ll11_opy_ = response.json()
    @classmethod
    def bstack111llll1ll_opy_(cls, bstack1lll1llll11_opy_, event_url=bstack1ll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧ⠗")):
        logger.debug(bstack1ll_opy_ (u"ࠤࡶࡩࡳࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡡࡥࡦࠣࡨࡦࡺࡡࠡࡶࡲࠤࡧࡧࡴࡤࡪࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤ⠘").format(bstack1lll1llll11_opy_[bstack1ll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⠙")]))
        if not TestHubUtils.bstack1ll11l1111ll_opy_(bstack1lll1llll11_opy_[bstack1ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⠚")]):
            logger.debug(bstack1ll_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡑࡳࡹࠦࡡࡥࡦ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࡀࠠࡼࡿࠥ⠛").format(bstack1lll1llll11_opy_[bstack1ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⠜")]))
            return
        bstack111ll1l1ll_opy_ = TestHubUtils.bstack1ll11l11l111_opy_(bstack1lll1llll11_opy_[bstack1ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⠝")], bstack1lll1llll11_opy_.get(bstack1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ⠞")))
        if bstack111ll1l1ll_opy_ != None:
            if bstack1lll1llll11_opy_.get(bstack1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ⠟")) != None:
                bstack1lll1llll11_opy_[bstack1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ⠠")][bstack1ll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩ⠡")] = bstack111ll1l1ll_opy_
            else:
                bstack1lll1llll11_opy_[bstack1ll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪ⠢")] = bstack111ll1l1ll_opy_
        if event_url == bstack1ll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬ⠣"):
            cls.bstack1ll11l1111l1_opy_()
            logger.debug(bstack1ll_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡆࡪࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡷࡳࠥࡨࡡࡵࡥ࡫ࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࡀࠠࡼࡿࠥ⠤").format(bstack1lll1llll11_opy_[bstack1ll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⠥")]))
            cls.bstack1ll1l111ll11_opy_.add(bstack1lll1llll11_opy_)
        elif event_url == bstack1ll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ⠦"):
            cls.post_data([bstack1lll1llll11_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack111l11l1_opy_(cls, logs):
        for log in logs:
            bstack1ll11l11111l_opy_ = {
                bstack1ll_opy_ (u"ࠪ࡯࡮ࡴࡤࠨ⠧"): bstack1ll_opy_ (u"࡙ࠫࡋࡓࡕࡡࡏࡓࡌ࠭⠨"),
                bstack1ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⠩"): log[bstack1ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ⠪")],
                bstack1ll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ⠫"): log[bstack1ll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ⠬")],
                bstack1ll_opy_ (u"ࠩ࡫ࡸࡹࡶ࡟ࡳࡧࡶࡴࡴࡴࡳࡦࠩ⠭"): {},
                bstack1ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⠮"): log[bstack1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⠯")],
            }
            if bstack1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⠰") in log:
                bstack1ll11l11111l_opy_[bstack1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⠱")] = log[bstack1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⠲")]
            elif bstack1ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⠳") in log:
                bstack1ll11l11111l_opy_[bstack1ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⠴")] = log[bstack1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⠵")]
            cls.bstack111llll1ll_opy_({
                bstack1ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⠶"): bstack1ll_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ⠷"),
                bstack1ll_opy_ (u"࠭࡬ࡰࡩࡶࠫ⠸"): [bstack1ll11l11111l_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll111llll1l_opy_(cls, steps):
        bstack1ll11l11ll11_opy_ = []
        for step in steps:
            bstack1ll11l111111_opy_ = {
                bstack1ll_opy_ (u"ࠧ࡬࡫ࡱࡨࠬ⠹"): bstack1ll_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡕࡇࡓࠫ⠺"),
                bstack1ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⠻"): step[bstack1ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⠼")],
                bstack1ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ⠽"): step[bstack1ll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ⠾")],
                bstack1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⠿"): step[bstack1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⡀")],
                bstack1ll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪ⡁"): step[bstack1ll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ⡂")]
            }
            if bstack1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⡃") in step:
                bstack1ll11l111111_opy_[bstack1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⡄")] = step[bstack1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⡅")]
            elif bstack1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⡆") in step:
                bstack1ll11l111111_opy_[bstack1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⡇")] = step[bstack1ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⡈")]
            bstack1ll11l11ll11_opy_.append(bstack1ll11l111111_opy_)
        cls.bstack111llll1ll_opy_({
            bstack1ll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⡉"): bstack1ll_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ⡊"),
            bstack1ll_opy_ (u"ࠫࡱࡵࡧࡴࠩ⡋"): bstack1ll11l11ll11_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack1llllll11ll_opy_, stage=STAGE.bstack11llll111l_opy_)
    def bstack11l1l1l111_opy_(cls, screenshot):
        cls.bstack111llll1ll_opy_({
            bstack1ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⡌"): bstack1ll_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ⡍"),
            bstack1ll_opy_ (u"ࠧ࡭ࡱࡪࡷࠬ⡎"): [{
                bstack1ll_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭⡏"): bstack1ll_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠫ⡐"),
                bstack1ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭⡑"): datetime.datetime.utcnow().isoformat() + bstack1ll_opy_ (u"ࠫ࡟࠭⡒"),
                bstack1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⡓"): screenshot[bstack1ll_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬ⡔")],
                bstack1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⡕"): screenshot[bstack1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⡖")]
            }]
        }, event_url=bstack1ll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ⡗"))
    @classmethod
    @error_handler(class_method=True)
    def send_cbt_info(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack111llll1ll_opy_({
            bstack1ll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⡘"): bstack1ll_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨ⡙"),
            bstack1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ⡚"): {
                bstack1ll_opy_ (u"ࠨࡵࡶ࡫ࡧࠦ⡛"): cls.current_test_uuid(),
                bstack1ll_opy_ (u"ࠢࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸࠨ⡜"): cls.bstack1llll111lll_opy_(driver)
            }
        })
    @classmethod
    def bstack1llll1l1111_opy_(cls, event: str, bstack1lll1llll11_opy_: bstack1lll11l1ll1_opy_):
        bstack1llll11111l_opy_ = {
            bstack1ll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⡝"): event,
            bstack1lll1llll11_opy_.bstack1lll1l1ll1l_opy_(): bstack1lll1llll11_opy_.bstack1lll1l1ll11_opy_(event)
        }
        cls.bstack111llll1ll_opy_(bstack1llll11111l_opy_)
        result = getattr(bstack1lll1llll11_opy_, bstack1ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⡞"), None)
        if event == bstack1ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⡟"):
            threading.current_thread().bstackTestMeta = {bstack1ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⡠"): bstack1ll_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭⡡")}
        elif event == bstack1ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⡢"):
            threading.current_thread().bstackTestMeta = {bstack1ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⡣"): getattr(result, bstack1ll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⡤"), bstack1ll_opy_ (u"ࠩࠪ⡥"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⡦"), None) is None or os.environ[bstack1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⡧")] == bstack1ll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ⡨")) and (os.environ.get(bstack1ll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ⡩"), None) is None or os.environ[bstack1ll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ⡪")] == bstack1ll_opy_ (u"ࠣࡰࡸࡰࡱࠨ⡫")):
            return False
        return True
    @staticmethod
    def bstack1ll11l11l1ll_opy_(func):
        def wrap(*args, **kwargs):
            if TestHubHandler.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ⡬"): bstack1ll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭⡭"),
            bstack1ll_opy_ (u"ࠫ࡝࠳ࡂࡔࡖࡄࡇࡐ࠳ࡔࡆࡕࡗࡓࡕ࡙ࠧ⡮"): bstack1ll_opy_ (u"ࠬࡺࡲࡶࡧࠪ⡯")
        }
        if os.environ.get(bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⡰"), None):
            headers[bstack1ll_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧ⡱")] = bstack1ll_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫ⡲").format(os.environ[bstack1ll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙ࠨ⡳")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1ll_opy_ (u"ࠪࡿࢂ࠵ࡻࡾࠩ⡴").format(bstack1ll111llll11_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ⡵"), None)
    @staticmethod
    def bstack1llll111lll_opy_(driver):
        return {
            bstack1lllll111l11_opy_(): bstack1ll1llll1l1_opy_(driver)
        }
    @staticmethod
    def bstack1ll11l1l11l1_opy_(exception_info, report):
        return [{bstack1ll_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ⡶"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1ll111l1lll_opy_(typename):
        if bstack1ll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤ⡷") in typename:
            return bstack1ll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣ⡸")
        return bstack1ll_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤ⡹")