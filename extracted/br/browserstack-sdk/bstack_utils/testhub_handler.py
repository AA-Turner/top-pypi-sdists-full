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
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1111lll1l1l_opy_, bstack1111ll1llll_opy_, bstack11111l1ll_opy_, error_handler, bstack1lllll1lll1l_opy_, bstack1ll1ll1ll11_opy_, bstack1lllllll1l11_opy_, bstack1lllllllll_opy_, bstack1llll11111_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1ll1l111llll_opy_ import bstack1ll1l11l1111_opy_
import bstack_utils.bstack11llll1ll1_opy_ as TestHubUtils
from bstack_utils.bstack1l1l1111_opy_ import bstack111l1l1l11_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.bstack1llll1ll111_opy_ import bstack1lll11ll1ll_opy_
from bstack_utils.constants import bstack1111l1ll_opy_
bstack1ll11l111ll1_opy_ = bstack111l_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡦࡳࡱࡲࡥࡤࡶࡲࡶ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ❯")
logger = logging.getLogger(__name__)
class TestHubHandler:
    bstack1ll1l111llll_opy_ = None
    bs_config = None
    bstack1l1111l11l_opy_ = None
    _1ll11l11111l_opy_ = False
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11111l111ll_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def launch(cls, bs_config, bstack1l1111l11l_opy_):
        cls._1ll11l11111l_opy_ = True
        cls.bs_config = bs_config
        cls.bstack1l1111l11l_opy_ = bstack1l1111l11l_opy_
        try:
            cls.bstack1ll11l1l1ll1_opy_()
            bstack1111ll111ll_opy_ = bstack1111lll1l1l_opy_(bs_config)
            bstack1111lll1ll1_opy_ = bstack1111ll1llll_opy_(bs_config)
            data = TestHubUtils.bstack1ll11l11llll_opy_(bs_config, bstack1l1111l11l_opy_)
            config = {
                bstack111l_opy_ (u"ࠩࡤࡹࡹ࡮ࠧ❰"): (bstack1111ll111ll_opy_, bstack1111lll1ll1_opy_),
                bstack111l_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫ❱"): cls.default_headers()
            }
            response = bstack11111l1ll_opy_(bstack111l_opy_ (u"ࠫࡕࡕࡓࡕࠩ❲"), cls.request_url(bstack111l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠶࠴ࡨࡵࡪ࡮ࡧࡷࠬ❳")), data, config)
            if response.status_code != 200:
                bstack11l1l1l1l1_opy_ = response.json()
                if bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ❴")] == False:
                    cls.bstack1ll11l1ll11l_opy_(bstack11l1l1l1l1_opy_)
                    return
                cls.bstack1ll11l11l111_opy_(bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ❵")])
                cls.bstack1ll11l11ll11_opy_(bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ❶")])
                return None
            bstack1ll11l11ll1l_opy_ = cls.bstack1ll11l11l11l_opy_(response)
            return bstack1ll11l11ll1l_opy_, response.json()
        except Exception as error:
            logger.error(bstack111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࢀࢃࠢ❷").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111111ll1l1_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def stop(cls, bstack1ll11l1l1l11_opy_=None):
        if not bstack111l1l1l11_opy_.on() and not a11y.on():
            return
        if not cls._1ll11l11111l_opy_:
            logger.info(bstack111l_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࠢ࡬ࡷࠥࡉࡌࡊ࠯ࡰࡥࡳࡧࡧࡦࡦࠣࠬࡱࡧࡵ࡯ࡥ࡫ࠤࡳࡵࡴࠡࡥࡤࡰࡱ࡫ࡤࠡࡤࡼࠤࡘࡊࡋࠪࠢ࠰ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡳࡵࡱࡳࠤࡆࡖࡉࠡࡴࡨࡵࡺ࡫ࡳࡵࠤ❸"))
            if cls.bstack1ll1l111llll_opy_ is not None:
                logger.info(bstack111l_opy_ (u"ࠦࡘ࡮ࡵࡵࡶ࡬ࡲ࡬ࠦࡤࡰࡹࡱࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡷࡵࡦࡷࡨࠦ❹"))
                cls.bstack1ll1l111llll_opy_.shutdown()
            else:
                logger.info(bstack111l_opy_ (u"ࠧࡔ࡯ࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡴࡹࡪࡻࡥࠡࡶࡲࠤࡸ࡮ࡵࡵࡦࡲࡻࡳࠨ❺"))
            return
        if os.environ.get(bstack111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ❻")) == bstack111l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ❼") or os.environ.get(bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭❽")) == bstack111l_opy_ (u"ࠤࡱࡹࡱࡲࠢ❾"):
            logger.error(bstack111l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡶࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭❿"))
            return {
                bstack111l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ➀"): bstack111l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ➁"),
                bstack111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ➂"): bstack111l_opy_ (u"ࠧࡕࡱ࡮ࡩࡳ࠵ࡢࡶ࡫࡯ࡨࡎࡊࠠࡪࡵࠣࡹࡳࡪࡥࡧ࡫ࡱࡩࡩ࠲ࠠࡣࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡ࡯࡬࡫࡭ࡺࠠࡩࡣࡹࡩࠥ࡬ࡡࡪ࡮ࡨࡨࠬ➃")
            }
        try:
            cls.bstack1ll1l111llll_opy_.shutdown()
            data = {
                bstack111l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭➄"): bstack1lllllllll_opy_()
            }
            if not bstack1ll11l1l1l11_opy_ is None:
                data[bstack111l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡲ࡫ࡴࡢࡦࡤࡸࡦ࠭➅")] = [{
                    bstack111l_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ➆"): bstack111l_opy_ (u"ࠫࡺࡹࡥࡳࡡ࡮࡭ࡱࡲࡥࡥࠩ➇"),
                    bstack111l_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰࠬ➈"): bstack1ll11l1l1l11_opy_
                }]
            config = {
                bstack111l_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ➉"): cls.default_headers()
            }
            bstack1111l11llll_opy_ = bstack111l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡹࡵࡰࠨ➊").format(os.environ[bstack111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨ➋")])
            bstack1ll11l111lll_opy_ = cls.request_url(bstack1111l11llll_opy_)
            response = bstack11111l1ll_opy_(bstack111l_opy_ (u"ࠩࡓ࡙࡙࠭➌"), bstack1ll11l111lll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack111l_opy_ (u"ࠥࡗࡹࡵࡰࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡱࡳࡹࠦ࡯࡬ࠤ➍"))
        except Exception as error:
            logger.error(bstack111l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡰࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࡀࠠࠣ➎") + str(error))
            return {
                bstack111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ➏"): bstack111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ➐"),
                bstack111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ➑"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll11l11l11l_opy_(cls, response):
        bstack11l1l1l1l1_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1ll11l11ll1l_opy_ = {}
        if bstack11l1l1l1l1_opy_.get(bstack111l_opy_ (u"ࠨ࡬ࡺࡸࠬ➒")) is None:
            os.environ[bstack111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭➓")] = bstack111l_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ➔")
        else:
            os.environ[bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ➕")] = bstack11l1l1l1l1_opy_.get(bstack111l_opy_ (u"ࠬࡰࡷࡵࠩ➖"), bstack111l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ➗"))
        os.environ[bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ➘")] = bstack11l1l1l1l1_opy_.get(bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ➙"), bstack111l_opy_ (u"ࠩࡱࡹࡱࡲࠧ➚"))
        logger.info(bstack111l_opy_ (u"ࠪࡘࡪࡹࡴࡩࡷࡥࠤࡸࡺࡡࡳࡶࡨࡨࠥࡽࡩࡵࡪࠣ࡭ࡩࡀࠠࠨ➛") + os.getenv(bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ➜")));
        if bstack111l1l1l11_opy_.bstack1ll11l1ll111_opy_(cls.bs_config, cls.bstack1l1111l11l_opy_.get(bstack111l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭➝"), bstack111l_opy_ (u"࠭ࠧ➞"))) is True:
            bstack1ll1l111l1l1_opy_, build_hashed_id, allow_screenshots = cls.bstack1ll11l1l1lll_opy_(bstack11l1l1l1l1_opy_)
            if bstack1ll1l111l1l1_opy_ != None and build_hashed_id != None:
                bstack1ll11l11ll1l_opy_[bstack111l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ➟")] = {
                    bstack111l_opy_ (u"ࠨ࡬ࡺࡸࡤࡺ࡯࡬ࡧࡱࠫ➠"): bstack1ll1l111l1l1_opy_,
                    bstack111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ➡"): build_hashed_id,
                    bstack111l_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ➢"): allow_screenshots
                }
            else:
                bstack1ll11l11ll1l_opy_[bstack111l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ➣")] = {}
        else:
            bstack1ll11l11ll1l_opy_[bstack111l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ➤")] = {}
        bstack1ll11l1l1l1l_opy_, build_hashed_id = cls.bstack1ll11l11l1l1_opy_(bstack11l1l1l1l1_opy_)
        if bstack1ll11l1l1l1l_opy_ != None and build_hashed_id != None:
            bstack1ll11l11ll1l_opy_[bstack111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭➥")] = {
                bstack111l_opy_ (u"ࠧࡢࡷࡷ࡬ࡤࡺ࡯࡬ࡧࡱࠫ➦"): bstack1ll11l1l1l1l_opy_,
                bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ➧"): build_hashed_id,
            }
        else:
            bstack1ll11l11ll1l_opy_[bstack111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ➨")] = {}
        if bstack1ll11l11ll1l_opy_[bstack111l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ➩")].get(bstack111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭➪")) != None or bstack1ll11l11ll1l_opy_[bstack111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ➫")].get(bstack111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ➬")) != None:
            cls.bstack1ll11l11l1ll_opy_(bstack11l1l1l1l1_opy_.get(bstack111l_opy_ (u"ࠧ࡫ࡹࡷࠫ➭")), bstack11l1l1l1l1_opy_.get(bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ➮")))
        return bstack1ll11l11ll1l_opy_
    @classmethod
    def bstack1ll11l1l1lll_opy_(cls, bstack11l1l1l1l1_opy_):
        if bstack11l1l1l1l1_opy_.get(bstack111l_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ➯")) == None:
            cls.bstack1ll11l11l111_opy_()
            return [None, None, None]
        if bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ➰")][bstack111l_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ➱")] != True:
            cls.bstack1ll11l11l111_opy_(bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ➲")])
            return [None, None, None]
        logger.debug(bstack111l_opy_ (u"࠭ࡻࡾࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠡࠨ➳").format(bstack1111l1ll_opy_))
        os.environ[bstack111l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭➴")] = bstack111l_opy_ (u"ࠨࡶࡵࡹࡪ࠭➵")
        if bstack11l1l1l1l1_opy_.get(bstack111l_opy_ (u"ࠩ࡭ࡻࡹ࠭➶")):
            os.environ[bstack111l_opy_ (u"ࠪࡇࡗࡋࡄࡆࡐࡗࡍࡆࡒࡓࡠࡈࡒࡖࡤࡉࡒࡂࡕࡋࡣࡗࡋࡐࡐࡔࡗࡍࡓࡍࠧ➷")] = json.dumps({
                bstack111l_opy_ (u"ࠫࡺࡹࡥࡳࡰࡤࡱࡪ࠭➸"): bstack1111lll1l1l_opy_(cls.bs_config),
                bstack111l_opy_ (u"ࠬࡶࡡࡴࡵࡺࡳࡷࡪࠧ➹"): bstack1111ll1llll_opy_(cls.bs_config)
            })
        if bstack11l1l1l1l1_opy_.get(bstack111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ➺")):
            os.environ[bstack111l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭➻")] = bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ➼")]
        if bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ➽")].get(bstack111l_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ➾"), {}).get(bstack111l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ➿")):
            os.environ[bstack111l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭⟀")] = str(bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⟁")][bstack111l_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ⟂")][bstack111l_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ⟃")])
        else:
            os.environ[bstack111l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ⟄")] = bstack111l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ⟅")
        return [bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"ࠫ࡯ࡽࡴࠨ⟆")], bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⟇")], os.environ[bstack111l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧ⟈")]]
    @classmethod
    def bstack1ll11l11l1l1_opy_(cls, bstack11l1l1l1l1_opy_):
        if bstack11l1l1l1l1_opy_.get(bstack111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⟉")) == None:
            cls.bstack1ll11l11ll11_opy_()
            return [None, None]
        if bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⟊")][bstack111l_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ⟋")] != True:
            cls.bstack1ll11l11ll11_opy_(bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⟌")])
            return [None, None]
        if bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⟍")].get(bstack111l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭⟎")):
            logger.debug(bstack111l_opy_ (u"࠭ࡔࡦࡵࡷࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪ⟏"))
            parsed = json.loads(os.getenv(bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ⟐"), bstack111l_opy_ (u"ࠨࡽࢀࠫ⟑")))
            capabilities = TestHubUtils.bstack1ll11l1l111l_opy_(bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⟒")][bstack111l_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ⟓")][bstack111l_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ⟔")], bstack111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⟕"), bstack111l_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬ⟖"))
            bstack1ll11l1l1l1l_opy_ = capabilities[bstack111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬ⟗")]
            os.environ[bstack111l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭⟘")] = bstack1ll11l1l1l1l_opy_
            if capabilities.get(bstack111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡮ࡪࠧ⟙")):
                os.environ[bstack111l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣ࡙ࡋࡓࡕࡡࡕ࡙ࡓࡥࡉࡅࠩ⟚")] = str(capabilities[bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩ⟛")])
            if capabilities.get(bstack111l_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡥࡢࡶ࡫࡯ࡨࡤࡻࡵࡪࡦࠪ⟜")):
                os.environ[bstack111l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡃࡗࡌࡐࡉࡥࡕࡖࡋࡇࠫ⟝")] = str(capabilities[bstack111l_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡠࡤࡸ࡭ࡱࡪ࡟ࡶࡷ࡬ࡨࠬ⟞")])
            if bstack111l_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࠥ⟟") in bstack11l1l1l1l1_opy_ and bstack11l1l1l1l1_opy_.get(bstack111l_opy_ (u"ࠤࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠣ⟠")) is None:
                parsed[bstack111l_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ⟡")] = capabilities[bstack111l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ⟢")]
            os.environ[bstack111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭⟣")] = json.dumps(parsed)
            scripts = TestHubUtils.bstack1ll11l1l111l_opy_(bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⟤")][bstack111l_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ⟥")][bstack111l_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩ⟦")], bstack111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⟧"), bstack111l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࠫ⟨"))
            accessibility_scripts.bstack1l11l1l1_opy_(scripts)
            commands_to_wrap = bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⟩")][bstack111l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭⟪")][bstack111l_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࡕࡱ࡚ࡶࡦࡶࠧ⟫")]
            commands = commands_to_wrap.get(bstack111l_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩ⟬"))
            accessibility_scripts.bstack1l11l11l1l1_opy_(commands)
            scripts_to_run = commands_to_wrap.get(bstack111l_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࡖࡲࡖࡺࡴࠧ⟭"))
            accessibility_scripts.bstack1111l1l111l_opy_(scripts_to_run)
            bstack1111ll1ll1l_opy_ = capabilities.get(bstack111l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ⟮"))
            accessibility_scripts.bstack1111l1l1ll1_opy_(bstack1111ll1ll1l_opy_)
            accessibility_scripts.store()
        return [bstack1ll11l1l1l1l_opy_, bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ⟯")]]
    @classmethod
    def bstack1ll11l11l111_opy_(cls, response=None):
        os.environ[bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ⟰")] = bstack111l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ⟱")
        os.environ[bstack111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⟲")] = bstack111l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ⟳")
        os.environ[bstack111l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧ⟴")] = bstack111l_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ⟵")
        os.environ[bstack111l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩ⟶")] = bstack111l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ⟷")
        os.environ[bstack111l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭⟸")] = bstack111l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ⟹")
        cls.bstack1ll11l1ll11l_opy_(response, bstack111l_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢ⟺"))
        return [None, None, None]
    @classmethod
    def bstack1ll11l11ll11_opy_(cls, response=None):
        os.environ[bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⟻")] = bstack111l_opy_ (u"ࠩࡱࡹࡱࡲࠧ⟼")
        os.environ[bstack111l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ⟽")] = bstack111l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ⟾")
        os.environ[bstack111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⟿")] = bstack111l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ⠀")
        cls.bstack1ll11l1ll11l_opy_(response, bstack111l_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢ⠁"))
        return [None, None, None]
    @classmethod
    def bstack1ll11l11l1ll_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⠂")] = jwt
        os.environ[bstack111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⠃")] = build_hashed_id
    @classmethod
    def bstack1ll11l1ll11l_opy_(cls, response=None, product=bstack111l_opy_ (u"ࠥࠦ⠄")):
        if response == None or response.get(bstack111l_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫ⠅")) == None:
            logger.error(product + bstack111l_opy_ (u"ࠧࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠢ⠆"))
            return
        for error in response[bstack111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭⠇")]:
            bstack1lllllll111l_opy_ = error[bstack111l_opy_ (u"ࠧ࡬ࡧࡼࠫ⠈")]
            error_message = error[bstack111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⠉")]
            if error_message:
                if bstack1lllllll111l_opy_ == bstack111l_opy_ (u"ࠤࡈࡖࡗࡕࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡆࡈࡒࡎࡋࡄࠣ⠊"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack111l_opy_ (u"ࠥࡈࡦࡺࡡࠡࡷࡳࡰࡴࡧࡤࠡࡶࡲࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࠦ⠋") + product + bstack111l_opy_ (u"ࠦࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡪࡵࡦࠢࡷࡳࠥࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤ⠌"))
    @classmethod
    def bstack1ll11l1l1ll1_opy_(cls):
        if cls.bstack1ll1l111llll_opy_ is not None:
            return
        cls.bstack1ll1l111llll_opy_ = bstack1ll1l11l1111_opy_(cls.post_data)
        cls.bstack1ll1l111llll_opy_.start()
    @classmethod
    def bstack1lll1ll111l_opy_(cls):
        if cls.bstack1ll1l111llll_opy_ is None:
            return
        cls.bstack1ll1l111llll_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def post_data(cls, bstack1lll1l11l1l_opy_, event_url=bstack111l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫ⠍")):
        config = {
            bstack111l_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ⠎"): cls.default_headers()
        }
        logger.debug(bstack111l_opy_ (u"ࠢࡱࡱࡶࡸࡤࡪࡡࡵࡣ࠽ࠤࡘ࡫࡮ࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡸࡴࠦࡴࡦࡵࡷ࡬ࡺࡨࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࡶࠤࢀࢃࠢ⠏").format(bstack111l_opy_ (u"ࠨ࠮ࠣࠫ⠐").join([event[bstack111l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⠑")] for event in bstack1lll1l11l1l_opy_])))
        response = bstack11111l1ll_opy_(bstack111l_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ⠒"), cls.request_url(event_url), bstack1lll1l11l1l_opy_, config)
        bstack1111l1ll11l_opy_ = response.json()
    @classmethod
    def bstack1ll1l11111_opy_(cls, bstack1lll1l11l1l_opy_, event_url=bstack111l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪ⠓")):
        logger.debug(bstack111l_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡄࡸࡹ࡫࡭ࡱࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡤࡨࡩࠦࡤࡢࡶࡤࠤࡹࡵࠠࡣࡣࡷࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧ⠔").format(bstack1lll1l11l1l_opy_[bstack111l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⠕")]))
        if not TestHubUtils.bstack1ll11l1l11l1_opy_(bstack1lll1l11l1l_opy_[bstack111l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⠖")]):
            logger.debug(bstack111l_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡔ࡯ࡵࠢࡤࡨࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨ⠗").format(bstack1lll1l11l1l_opy_[bstack111l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⠘")]))
            return
        bstack11lll1ll1l_opy_ = TestHubUtils.bstack1ll11l1l11ll_opy_(bstack1lll1l11l1l_opy_[bstack111l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⠙")], bstack1lll1l11l1l_opy_.get(bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭⠚")))
        if bstack11lll1ll1l_opy_ != None:
            if bstack1lll1l11l1l_opy_.get(bstack111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ⠛")) != None:
                bstack1lll1l11l1l_opy_[bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ⠜")][bstack111l_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬ⠝")] = bstack11lll1ll1l_opy_
            else:
                bstack1lll1l11l1l_opy_[bstack111l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭⠞")] = bstack11lll1ll1l_opy_
        if event_url == bstack111l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨ⠟"):
            cls.bstack1ll11l1l1ll1_opy_()
            logger.debug(bstack111l_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡂࡦࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡤࡤࡸࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨ⠠").format(bstack1lll1l11l1l_opy_[bstack111l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⠡")]))
            cls.bstack1ll1l111llll_opy_.add(bstack1lll1l11l1l_opy_)
        elif event_url == bstack111l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ⠢"):
            cls.post_data([bstack1lll1l11l1l_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack1llll11ll1_opy_(cls, logs):
        for log in logs:
            bstack1ll11l1111ll_opy_ = {
                bstack111l_opy_ (u"࠭࡫ࡪࡰࡧࠫ⠣"): bstack111l_opy_ (u"ࠧࡕࡇࡖࡘࡤࡒࡏࡈࠩ⠤"),
                bstack111l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ⠥"): log[bstack111l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⠦")],
                bstack111l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭⠧"): log[bstack111l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ⠨")],
                bstack111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡢࡶࡪࡹࡰࡰࡰࡶࡩࠬ⠩"): {},
                bstack111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⠪"): log[bstack111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⠫")],
            }
            if bstack111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⠬") in log:
                bstack1ll11l1111ll_opy_[bstack111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⠭")] = log[bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⠮")]
            elif bstack111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⠯") in log:
                bstack1ll11l1111ll_opy_[bstack111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⠰")] = log[bstack111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⠱")]
            cls.bstack1ll1l11111_opy_({
                bstack111l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⠲"): bstack111l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ⠳"),
                bstack111l_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧ⠴"): [bstack1ll11l1111ll_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll11l111l1l_opy_(cls, steps):
        bstack1ll11l1l1111_opy_ = []
        for step in steps:
            bstack1ll11l1111l1_opy_ = {
                bstack111l_opy_ (u"ࠪ࡯࡮ࡴࡤࠨ⠵"): bstack111l_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡘࡊࡖࠧ⠶"),
                bstack111l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⠷"): step[bstack111l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ⠸")],
                bstack111l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ⠹"): step[bstack111l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ⠺")],
                bstack111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⠻"): step[bstack111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⠼")],
                bstack111l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭⠽"): step[bstack111l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ⠾")]
            }
            if bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⠿") in step:
                bstack1ll11l1111l1_opy_[bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⡀")] = step[bstack111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⡁")]
            elif bstack111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⡂") in step:
                bstack1ll11l1111l1_opy_[bstack111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⡃")] = step[bstack111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⡄")]
            bstack1ll11l1l1111_opy_.append(bstack1ll11l1111l1_opy_)
        cls.bstack1ll1l11111_opy_({
            bstack111l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⡅"): bstack111l_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ⡆"),
            bstack111l_opy_ (u"ࠧ࡭ࡱࡪࡷࠬ⡇"): bstack1ll11l1l1111_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11ll11111_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def bstack1111111l1_opy_(cls, screenshot):
        cls.bstack1ll1l11111_opy_({
            bstack111l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⡈"): bstack111l_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭⡉"),
            bstack111l_opy_ (u"ࠪࡰࡴ࡭ࡳࠨ⡊"): [{
                bstack111l_opy_ (u"ࠫࡰ࡯࡮ࡥࠩ⡋"): bstack111l_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠧ⡌"),
                bstack111l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ⡍"): datetime.datetime.utcnow().isoformat() + bstack111l_opy_ (u"࡛ࠧࠩ⡎"),
                bstack111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⡏"): screenshot[bstack111l_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨ⡐")],
                bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⡑"): screenshot[bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⡒")]
            }]
        }, event_url=bstack111l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ⡓"))
    @classmethod
    @error_handler(class_method=True)
    def send_cbt_info(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1ll1l11111_opy_({
            bstack111l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⡔"): bstack111l_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫ⡕"),
            bstack111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ⡖"): {
                bstack111l_opy_ (u"ࠤࡸࡹ࡮ࡪࠢ⡗"): cls.current_test_uuid(),
                bstack111l_opy_ (u"ࠥ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠤ⡘"): cls.bstack1llll1l11l1_opy_(driver)
            }
        })
    @classmethod
    def bstack1llll1l1lll_opy_(cls, event: str, bstack1lll1l11l1l_opy_: bstack1lll11ll1ll_opy_):
        bstack1lll1l11lll_opy_ = {
            bstack111l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⡙"): event,
            bstack1lll1l11l1l_opy_.bstack1lll1llllll_opy_(): bstack1lll1l11l1l_opy_.bstack1lll1l1l1l1_opy_(event)
        }
        cls.bstack1ll1l11111_opy_(bstack1lll1l11lll_opy_)
        result = getattr(bstack1lll1l11l1l_opy_, bstack111l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⡚"), None)
        if event == bstack111l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⡛"):
            threading.current_thread().bstackTestMeta = {bstack111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⡜"): bstack111l_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ⡝")}
        elif event == bstack111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⡞"):
            threading.current_thread().bstackTestMeta = {bstack111l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⡟"): getattr(result, bstack111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⡠"), bstack111l_opy_ (u"ࠬ࠭⡡"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⡢"), None) is None or os.environ[bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⡣")] == bstack111l_opy_ (u"ࠣࡰࡸࡰࡱࠨ⡤")) and (os.environ.get(bstack111l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ⡥"), None) is None or os.environ[bstack111l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ⡦")] == bstack111l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ⡧")):
            return False
        return True
    @staticmethod
    def bstack1ll11l111l11_opy_(func):
        def wrap(*args, **kwargs):
            if TestHubHandler.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack111l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ⡨"): bstack111l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ⡩"),
            bstack111l_opy_ (u"࡙ࠧ࠯ࡅࡗ࡙ࡇࡃࡌ࠯ࡗࡉࡘ࡚ࡏࡑࡕࠪ⡪"): bstack111l_opy_ (u"ࠨࡶࡵࡹࡪ࠭⡫")
        }
        if os.environ.get(bstack111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⡬"), None):
            headers[bstack111l_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪ⡭")] = bstack111l_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧ⡮").format(os.environ[bstack111l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠤ⡯")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack111l_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬ⡰").format(bstack1ll11l111ll1_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⡱"), None)
    @staticmethod
    def bstack1llll1l11l1_opy_(driver):
        return {
            bstack1lllll1lll1l_opy_(): bstack1ll1ll1ll11_opy_(driver)
        }
    @staticmethod
    def bstack1ll11l11lll1_opy_(exception_info, report):
        return [{bstack111l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ⡲"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1ll111l1l1l_opy_(typename):
        if bstack111l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧ⡳") in typename:
            return bstack111l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦ⡴")
        return bstack111l_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧ⡵")