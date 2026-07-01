# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11111ll111l_opy_, bstack1111l11111l_opy_, bstack1111ll1111_opy_, error_handler, bstack1lll11llllll_opy_, bstack1l1l11ll1_opy_, bstack1llll1l111ll_opy_, bstack1l1111ll_opy_, bstack11llll11_opy_, bstack11lll1l1l1_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1ll111l1ll1l_opy_ import bstack1ll111l1ll11_opy_
import bstack_utils.bstack11llll1ll1_opy_ as TestHubUtils
from bstack_utils.bstack11l111ll_opy_ import bstack1ll111ll_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.test_data import bstack1lll1l1ll_opy_
from bstack_utils.constants import bstack1lll11ll1l_opy_
bstack1l1lll1llll1_opy_ = bstack1l1llll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡦࡳࡱࡲࡥࡤࡶࡲࡶ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ⭭")
logger = logging.getLogger(__name__)
class TestHubHandler:
    bstack1ll111l1ll1l_opy_ = None
    bs_config = None
    bstack1111l11l1_opy_ = None
    _1l1llll1111l_opy_ = False
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack1111111l111_opy_, stage=STAGE.SINGLE)
    def launch(cls, bs_config, bstack1111l11l1_opy_):
        cls._1l1llll1111l_opy_ = True
        cls.bs_config = bs_config
        cls.bstack1111l11l1_opy_ = bstack1111l11l1_opy_
        try:
            cls.bstack1l1lll1ll111_opy_()
            bstack11111ll1l1l_opy_ = bstack11111ll111l_opy_(bs_config)
            bstack1111l1l1lll_opy_ = bstack1111l11111l_opy_(bs_config)
            data = TestHubUtils.bstack1l1lll1lllll_opy_(bs_config, bstack1111l11l1_opy_)
            config = {
                bstack1l1llll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧ⭮"): (bstack11111ll1l1l_opy_, bstack1111l1l1lll_opy_),
                bstack1l1llll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫ⭯"): cls.default_headers()
            }
            response = bstack1111ll1111_opy_(bstack1l1llll_opy_ (u"ࠫࡕࡕࡓࡕࠩ⭰"), cls.request_url(bstack1l1llll_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠶࠴ࡨࡵࡪ࡮ࡧࡷࠬ⭱")), data, config)
            if response.status_code != 200:
                bstack1ll11l11l1_opy_ = response.json()
                if bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ⭲")] == False:
                    cls.bstack1l1lll11l11l_opy_(bstack1ll11l11l1_opy_)
                    return
                cls.bstack1l1lll1l1lll_opy_(bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⭳")])
                cls.bstack1l1lll1ll1ll_opy_(bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⭴")])
                return None
            bstack1l1llll111l1_opy_ = cls.bstack1l1lll1l11ll_opy_(response)
            try:
                bstack1llll1ll1l11_opy_ = bstack11lll1l1l1_opy_(bs_config)
                if bstack1llll1ll1l11_opy_:
                    logger.info(bstack1l1llll_opy_ (u"ࠤࡗࡩࡸࡺࠠࡱ࡮ࡤࡲࠥ࡯ࡤࠡࡵࡨࡲࡹࠦࡴࡰࠢࡥࡹ࡮ࡲࡤࠡࡵࡷࡥࡷࡺ࠺ࠡࡽࢀࠦ⭵").format(bstack1llll1ll1l11_opy_))
            except Exception as error:
                logger.debug(bstack1l1llll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡲ࡯ࡨࡩ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡵࡲࡡ࡯ࠢ࡬ࡨ࠿ࠦࡻࡾࠤ⭶").format(str(error)))
            return bstack1l1llll111l1_opy_, response.json()
        except Exception as error:
            logger.error(bstack1l1llll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡻࡾࠤ⭷").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11111111lll_opy_, stage=STAGE.SINGLE)
    def stop(cls, bstack1l1llll11111_opy_=None):
        if not bstack1ll111ll_opy_.on() and not a11y.on():
            return
        if not cls._1l1llll1111l_opy_:
            logger.info(bstack1l1llll_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࠤ࡮ࡹࠠࡄࡎࡌ࠱ࡲࡧ࡮ࡢࡩࡨࡨࠥ࠮࡬ࡢࡷࡱࡧ࡭ࠦ࡮ࡰࡶࠣࡧࡦࡲ࡬ࡦࡦࠣࡦࡾࠦࡓࡅࡍࠬࠤ࠲ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡵࡷࡳࡵࠦࡁࡑࡋࠣࡶࡪࡷࡵࡦࡵࡷࠦ⭸"))
            if cls.bstack1ll111l1ll1l_opy_ is not None:
                logger.info(bstack1l1llll_opy_ (u"ࠨࡓࡩࡷࡷࡸ࡮ࡴࡧࠡࡦࡲࡻࡳࠦࡲࡦࡳࡸࡩࡸࡺࠠࡲࡷࡨࡹࡪࠨ⭹"))
                cls.bstack1ll111l1ll1l_opy_.shutdown()
            else:
                logger.info(bstack1l1llll_opy_ (u"ࠢࡏࡱࠣࡶࡪࡷࡵࡦࡵࡷࠤࡶࡻࡥࡶࡧࠣࡸࡴࠦࡳࡩࡷࡷࡨࡴࡽ࡮ࠣ⭺"))
            return
        if os.environ.get(bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⭻")) == bstack1l1llll_opy_ (u"ࠤࡱࡹࡱࡲࠢ⭼") or os.environ.get(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ⭽")) == bstack1l1llll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ⭾"):
            logger.error(bstack1l1llll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨ⭿"))
            return {
                bstack1l1llll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⮀"): bstack1l1llll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭⮁"),
                bstack1l1llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⮂"): bstack1l1llll_opy_ (u"ࠩࡗࡳࡰ࡫࡮࠰ࡤࡸ࡭ࡱࡪࡉࡅࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤ࠭ࠢࡥࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡱ࡮࡭ࡨࡵࠢ࡫ࡥࡻ࡫ࠠࡧࡣ࡬ࡰࡪࡪࠧ⮃")
            }
        try:
            cls.bstack1ll111l1ll1l_opy_.shutdown()
            data = {
                bstack1l1llll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⮄"): bstack1l1111ll_opy_()
            }
            if not bstack1l1llll11111_opy_ is None:
                data[bstack1l1llll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠨ⮅")] = [{
                    bstack1l1llll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ⮆"): bstack1l1llll_opy_ (u"࠭ࡵࡴࡧࡵࡣࡰ࡯࡬࡭ࡧࡧࠫ⮇"),
                    bstack1l1llll_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࠧ⮈"): bstack1l1llll11111_opy_
                }]
            config = {
                bstack1l1llll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ⮉"): cls.default_headers()
            }
            bstack11111l11lll_opy_ = bstack1l1llll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡴࡰࡲࠪ⮊").format(os.environ[bstack1l1llll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣ⮋")])
            bstack1l1lll1l1111_opy_ = cls.request_url(bstack11111l11lll_opy_)
            response = bstack1111ll1111_opy_(bstack1l1llll_opy_ (u"ࠫࡕ࡛ࡔࠨ⮌"), bstack1l1lll1l1111_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l1llll_opy_ (u"࡙ࠧࡴࡰࡲࠣࡶࡪࡷࡵࡦࡵࡷࠤࡳࡵࡴࠡࡱ࡮ࠦ⮍"))
        except Exception as error:
            logger.error(bstack1l1llll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡲࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡔࡦࡵࡷࡌࡺࡨ࠺࠻ࠢࠥ⮎") + str(error))
            return {
                bstack1l1llll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⮏"): bstack1l1llll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ⮐"),
                bstack1l1llll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⮑"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1l1lll1l11ll_opy_(cls, response):
        bstack1ll11l11l1_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1l1llll111l1_opy_ = {}
        if bstack1ll11l11l1_opy_.get(bstack1l1llll_opy_ (u"ࠪ࡮ࡼࡺࠧ⮒")) is None:
            os.environ[bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⮓")] = bstack1l1llll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ⮔")
        else:
            os.environ[bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⮕")] = bstack1ll11l11l1_opy_.get(bstack1l1llll_opy_ (u"ࠧ࡫ࡹࡷࠫ⮖"), bstack1l1llll_opy_ (u"ࠨࡰࡸࡰࡱ࠭⮗"))
        os.environ[bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⮘")] = bstack1ll11l11l1_opy_.get(bstack1l1llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ⮙"), bstack1l1llll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ⮚"))
        logger.info(bstack1l1llll_opy_ (u"࡚ࠬࡥࡴࡶ࡫ࡹࡧࠦࡳࡵࡣࡵࡸࡪࡪࠠࡸ࡫ࡷ࡬ࠥ࡯ࡤ࠻ࠢࠪ⮛") + os.getenv(bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⮜")));
        if bstack1ll111ll_opy_.bstack1l1lll1ll11l_opy_(cls.bs_config, cls.bstack1111l11l1_opy_.get(bstack1l1llll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨ⮝"), bstack1l1llll_opy_ (u"ࠨࠩ⮞"))) is True:
            bstack1ll111l11ll1_opy_, build_hashed_id, allow_screenshots = cls.bstack1l1lll1lll11_opy_(bstack1ll11l11l1_opy_)
            if bstack1ll111l11ll1_opy_ != None and build_hashed_id != None:
                bstack1l1llll111l1_opy_[bstack1l1llll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⮟")] = {
                    bstack1l1llll_opy_ (u"ࠪ࡮ࡼࡺ࡟ࡵࡱ࡮ࡩࡳ࠭⮠"): bstack1ll111l11ll1_opy_,
                    bstack1l1llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭⮡"): build_hashed_id,
                    bstack1l1llll_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ⮢"): allow_screenshots
                }
            else:
                bstack1l1llll111l1_opy_[bstack1l1llll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⮣")] = {}
        else:
            bstack1l1llll111l1_opy_[bstack1l1llll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⮤")] = {}
        bstack1l1lll11ll11_opy_, build_hashed_id = cls.bstack1l1lll11l1ll_opy_(bstack1ll11l11l1_opy_)
        if bstack1l1lll11ll11_opy_ != None and build_hashed_id != None:
            bstack1l1llll111l1_opy_[bstack1l1llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⮥")] = {
                bstack1l1llll_opy_ (u"ࠩࡤࡹࡹ࡮࡟ࡵࡱ࡮ࡩࡳ࠭⮦"): bstack1l1lll11ll11_opy_,
                bstack1l1llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ⮧"): build_hashed_id,
            }
        else:
            bstack1l1llll111l1_opy_[bstack1l1llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⮨")] = {}
        if bstack1l1llll111l1_opy_[bstack1l1llll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⮩")].get(bstack1l1llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ⮪")) != None or bstack1l1llll111l1_opy_[bstack1l1llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⮫")].get(bstack1l1llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ⮬")) != None:
            cls.bstack1l1lll11l111_opy_(bstack1ll11l11l1_opy_.get(bstack1l1llll_opy_ (u"ࠩ࡭ࡻࡹ࠭⮭")), bstack1ll11l11l1_opy_.get(bstack1l1llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ⮮")))
        return bstack1l1llll111l1_opy_
    @classmethod
    def bstack1l1lll1lll11_opy_(cls, bstack1ll11l11l1_opy_):
        if bstack1ll11l11l1_opy_.get(bstack1l1llll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⮯")) == None:
            cls.bstack1l1lll1l1lll_opy_()
            return [None, None, None]
        if bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⮰")][bstack1l1llll_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ⮱")] != True:
            cls.bstack1l1lll1l1lll_opy_(bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⮲")])
            return [None, None, None]
        logger.debug(bstack1l1llll_opy_ (u"ࠨࡽࢀࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪ⮳").format(bstack1lll11ll1l_opy_))
        os.environ[bstack1l1llll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨ⮴")] = bstack1l1llll_opy_ (u"ࠪࡸࡷࡻࡥࠨ⮵")
        if bstack1ll11l11l1_opy_.get(bstack1l1llll_opy_ (u"ࠫ࡯ࡽࡴࠨ⮶")):
            os.environ[bstack1l1llll_opy_ (u"ࠬࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࡢࡊࡔࡘ࡟ࡄࡔࡄࡗࡍࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩ⮷")] = json.dumps({
                bstack1l1llll_opy_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨ⮸"): bstack11111ll111l_opy_(cls.bs_config),
                bstack1l1llll_opy_ (u"ࠧࡱࡣࡶࡷࡼࡵࡲࡥࠩ⮹"): bstack1111l11111l_opy_(cls.bs_config)
            })
        if bstack1ll11l11l1_opy_.get(bstack1l1llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ⮺")):
            os.environ[bstack1l1llll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨ⮻")] = bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ⮼")]
        if bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⮽")].get(bstack1l1llll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭⮾"), {}).get(bstack1l1llll_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ⮿")):
            os.environ[bstack1l1llll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ⯀")] = str(bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⯁")][bstack1l1llll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ⯂")][bstack1l1llll_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ⯃")])
        else:
            os.environ[bstack1l1llll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬ⯄")] = bstack1l1llll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ⯅")
        return [bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"࠭ࡪࡸࡶࠪ⯆")], bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ⯇")], os.environ[bstack1l1llll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩ⯈")]]
    @classmethod
    def bstack1l1lll11l1ll_opy_(cls, bstack1ll11l11l1_opy_):
        if bstack1ll11l11l1_opy_.get(bstack1l1llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⯉")) == None:
            cls.bstack1l1lll1ll1ll_opy_()
            return [None, None]
        if bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⯊")][bstack1l1llll_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ⯋")] != True:
            cls.bstack1l1lll1ll1ll_opy_(bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⯌")])
            return [None, None]
        if bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⯍")].get(bstack1l1llll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ⯎")):
            logger.debug(bstack1l1llll_opy_ (u"ࠨࡖࡨࡷࡹࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠥࠬ⯏"))
            parsed = json.loads(os.getenv(bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ⯐"), bstack1l1llll_opy_ (u"ࠪࡿࢂ࠭⯑")))
            capabilities = TestHubUtils.bstack1l1lll1l11l1_opy_(bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⯒")][bstack1l1llll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭⯓")][bstack1l1llll_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ⯔")], bstack1l1llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⯕"), bstack1l1llll_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧ⯖"))
            bstack1l1lll11ll11_opy_ = capabilities[bstack1l1llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧ⯗")]
            os.environ[bstack1l1llll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ⯘")] = bstack1l1lll11ll11_opy_
            if capabilities.get(bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩ⯙")):
                os.environ[bstack1l1llll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡔࡆࡕࡗࡣࡗ࡛ࡎࡠࡋࡇࠫ⯚")] = str(capabilities[bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫ⯛")])
            if capabilities.get(bstack1l1llll_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡠࡤࡸ࡭ࡱࡪ࡟ࡶࡷ࡬ࡨࠬ⯜")):
                os.environ[bstack1l1llll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡅ࡙ࡎࡒࡄࡠࡗࡘࡍࡉ࠭⯝")] = str(capabilities[bstack1l1llll_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡢࡦࡺ࡯࡬ࡥࡡࡸࡹ࡮ࡪࠧ⯞")])
            if bstack1l1llll_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࠧ⯟") in bstack1ll11l11l1_opy_ and bstack1ll11l11l1_opy_.get(bstack1l1llll_opy_ (u"ࠦࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠥ⯠")) is None:
                parsed[bstack1l1llll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⯡")] = capabilities[bstack1l1llll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ⯢")]
            os.environ[bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ⯣")] = json.dumps(parsed)
            scripts = TestHubUtils.bstack1l1lll1l11l1_opy_(bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⯤")][bstack1l1llll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ⯥")][bstack1l1llll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫ⯦")], bstack1l1llll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⯧"), bstack1l1llll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩ࠭⯨"))
            accessibility_scripts.bstack1ll1l1ll1l_opy_(scripts)
            commands_to_wrap = bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⯩")][bstack1l1llll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ⯪")][bstack1l1llll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࡗࡳ࡜ࡸࡡࡱࠩ⯫")]
            commands = commands_to_wrap.get(bstack1l1llll_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫ⯬"))
            accessibility_scripts.bstack11lll1l1l1l_opy_(commands)
            scripts_to_run = commands_to_wrap.get(bstack1l1llll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࡘࡴࡘࡵ࡯ࠩ⯭"))
            accessibility_scripts.bstack11111l1ll11_opy_(scripts_to_run)
            bstack11111ll1lll_opy_ = capabilities.get(bstack1l1llll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⯮"))
            accessibility_scripts.bstack11111l1l1ll_opy_(bstack11111ll1lll_opy_)
            accessibility_scripts.store()
        return [bstack1l1lll11ll11_opy_, bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⯯")]]
    @classmethod
    def bstack1l1lll1l1lll_opy_(cls, response=None):
        os.environ[bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⯰")] = bstack1l1llll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ⯱")
        os.environ[bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⯲")] = bstack1l1llll_opy_ (u"ࠩࡱࡹࡱࡲࠧ⯳")
        os.environ[bstack1l1llll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩ⯴")] = bstack1l1llll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ⯵")
        os.environ[bstack1l1llll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫ⯶")] = bstack1l1llll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ⯷")
        os.environ[bstack1l1llll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ⯸")] = bstack1l1llll_opy_ (u"ࠣࡰࡸࡰࡱࠨ⯹")
        cls.bstack1l1lll11l11l_opy_(response, bstack1l1llll_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤ⯺"))
        return [None, None, None]
    @classmethod
    def bstack1l1lll1ll1ll_opy_(cls, response=None):
        try:
            from bstack_utils.helper import bstack11ll11lll1_opy_ as _111ll1l11l_opy_
            _1l1lll11lll1_opy_ = _111ll1l11l_opy_()
        except Exception:
            _1l1lll11lll1_opy_ = False
        if not _1l1lll11lll1_opy_:
            os.environ[bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ⯻")] = bstack1l1llll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ⯼")
            os.environ[bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⯽")] = bstack1l1llll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ⯾")
        os.environ[bstack1l1llll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ⯿")] = bstack1l1llll_opy_ (u"ࠨࡰࡸࡰࡱ࠭Ⰰ")
        cls.bstack1l1lll11l11l_opy_(response, bstack1l1llll_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤⰁ"))
        return [None, None, None]
    @classmethod
    def bstack1l1lll11l111_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧⰂ")] = jwt
        os.environ[bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩⰃ")] = build_hashed_id
    @classmethod
    def bstack1l1lll11l11l_opy_(cls, response=None, product=bstack1l1llll_opy_ (u"ࠧࠨⰄ")):
        if response == None or response.get(bstack1l1llll_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭Ⰵ")) == None:
            logger.error(product + bstack1l1llll_opy_ (u"ࠢࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠤⰆ"))
            return
        for error in response[bstack1l1llll_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨⰇ")]:
            bstack1lll11ll1l11_opy_ = error[bstack1l1llll_opy_ (u"ࠩ࡮ࡩࡾ࠭Ⰸ")]
            error_message = error[bstack1l1llll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫⰉ")]
            if error_message:
                if bstack1lll11ll1l11_opy_ == bstack1l1llll_opy_ (u"ࠦࡊࡘࡒࡐࡔࡢࡅࡈࡉࡅࡔࡕࡢࡈࡊࡔࡉࡆࡆࠥⰊ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l1llll_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࠨⰋ") + product + bstack1l1llll_opy_ (u"ࠨࠠࡧࡣ࡬ࡰࡪࡪࠠࡥࡷࡨࠤࡹࡵࠠࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦⰌ"))
    @classmethod
    def bstack1l1lll1ll111_opy_(cls):
        if cls.bstack1ll111l1ll1l_opy_ is not None:
            return
        cls.bstack1ll111l1ll1l_opy_ = bstack1ll111l1ll11_opy_(cls.post_data)
        cls.bstack1ll111l1ll1l_opy_.start()
    @classmethod
    def bstack1111111l_opy_(cls):
        if cls.bstack1ll111l1ll1l_opy_ is None:
            return
        cls.bstack1ll111l1ll1l_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def post_data(cls, bstack1llll1l11_opy_, event_url=bstack1l1llll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭Ⰽ")):
        config = {
            bstack1l1llll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩⰎ"): cls.default_headers()
        }
        logger.debug(bstack1l1llll_opy_ (u"ࠤࡳࡳࡸࡺ࡟ࡥࡣࡷࡥ࠿ࠦࡓࡦࡰࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡶࡨࡷࡹ࡮ࡵࡣࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࡸࠦࡻࡾࠤⰏ").format(bstack1l1llll_opy_ (u"ࠪ࠰ࠥ࠭Ⱀ").join([event[bstack1l1llll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨⰑ")] for event in bstack1llll1l11_opy_])))
        response = bstack1111ll1111_opy_(bstack1l1llll_opy_ (u"ࠬࡖࡏࡔࡖࠪⰒ"), cls.request_url(event_url), bstack1llll1l11_opy_, config)
        bstack1111l11l1ll_opy_ = response.json()
    @classmethod
    def bstack1lll11ll1_opy_(cls, bstack1llll1l11_opy_, event_url=bstack1l1llll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬⰓ")):
        logger.debug(bstack1l1llll_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡆࡺࡴࡦ࡯ࡳࡸ࡮ࡴࡧࠡࡶࡲࠤࡦࡪࡤࠡࡦࡤࡸࡦࠦࡴࡰࠢࡥࡥࡹࡩࡨࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢⰔ").format(bstack1llll1l11_opy_[bstack1l1llll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬⰕ")]))
        if not TestHubUtils.bstack1l1lll1l111l_opy_(bstack1llll1l11_opy_[bstack1l1llll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭Ⱆ")]):
            logger.debug(bstack1l1llll_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡏࡱࡷࠤࡦࡪࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣⰗ").format(bstack1llll1l11_opy_[bstack1l1llll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨⰘ")]))
            return
        bstack1l1l111lll_opy_ = TestHubUtils.bstack1l1lll1ll1l1_opy_(bstack1llll1l11_opy_[bstack1l1llll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩⰙ")], bstack1llll1l11_opy_.get(bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨⰚ")))
        if bstack1l1l111lll_opy_ != None:
            if bstack1llll1l11_opy_.get(bstack1l1llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩⰛ")) != None:
                bstack1llll1l11_opy_[bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪⰜ")][bstack1l1llll_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧⰝ")] = bstack1l1l111lll_opy_
            else:
                bstack1llll1l11_opy_[bstack1l1llll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨⰞ")] = bstack1l1l111lll_opy_
        if event_url == bstack1l1llll_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪⰟ"):
            cls.bstack1l1lll1ll111_opy_()
            logger.debug(bstack1l1llll_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡄࡨࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡵࡱࠣࡦࡦࡺࡣࡩࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣⰠ").format(bstack1llll1l11_opy_[bstack1l1llll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪⰡ")]))
            cls.bstack1ll111l1ll1l_opy_.add(bstack1llll1l11_opy_)
        elif event_url == bstack1l1llll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬⰢ"):
            cls.post_data([bstack1llll1l11_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll11111_opy_(cls, logs):
        for log in logs:
            bstack1l1lll1lll1l_opy_ = {
                bstack1l1llll_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭Ⱓ"): bstack1l1llll_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡍࡑࡊࠫⰤ"),
                bstack1l1llll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩⰥ"): log[bstack1l1llll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪⰦ")],
                bstack1l1llll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨⰧ"): log[bstack1l1llll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩⰨ")],
                bstack1l1llll_opy_ (u"ࠧࡩࡶࡷࡴࡤࡸࡥࡴࡲࡲࡲࡸ࡫ࠧⰩ"): {},
                bstack1l1llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩⰪ"): log[bstack1l1llll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪⰫ")],
            }
            if bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪⰬ") in log:
                bstack1l1lll1lll1l_opy_[bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫⰭ")] = log[bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬⰮ")]
            elif bstack1l1llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ⱟ") in log:
                bstack1l1lll1lll1l_opy_[bstack1l1llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧⰰ")] = log[bstack1l1llll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨⰱ")]
            cls.bstack1lll11ll1_opy_({
                bstack1l1llll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ⰲ"): bstack1l1llll_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧⰳ"),
                bstack1l1llll_opy_ (u"ࠫࡱࡵࡧࡴࠩⰴ"): [bstack1l1lll1lll1l_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1l1lll11ll1l_opy_(cls, steps):
        bstack1l1lll11l1l1_opy_ = []
        for step in steps:
            bstack1l1lll1l1l1l_opy_ = {
                bstack1l1llll_opy_ (u"ࠬࡱࡩ࡯ࡦࠪⰵ"): bstack1l1llll_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘ࡚ࡅࡑࠩⰶ"),
                bstack1l1llll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ⰷ"): step[bstack1l1llll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧⰸ")],
                bstack1l1llll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬⰹ"): step[bstack1l1llll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ⰺ")],
                bstack1l1llll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬⰻ"): step[bstack1l1llll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ⰼ")],
                bstack1l1llll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨⰽ"): step[bstack1l1llll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩⰾ")]
            }
            if bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨⰿ") in step:
                bstack1l1lll1l1l1l_opy_[bstack1l1llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩⱀ")] = step[bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪⱁ")]
            elif bstack1l1llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫⱂ") in step:
                bstack1l1lll1l1l1l_opy_[bstack1l1llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬⱃ")] = step[bstack1l1llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ⱄ")]
            bstack1l1lll11l1l1_opy_.append(bstack1l1lll1l1l1l_opy_)
        cls.bstack1lll11ll1_opy_({
            bstack1l1llll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫⱅ"): bstack1l1llll_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬⱆ"),
            bstack1l1llll_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧⱇ"): bstack1l1lll11l1l1_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11l1l111ll_opy_, stage=STAGE.SINGLE)
    def bstack1ll11ll1ll_opy_(cls, screenshot):
        cls.bstack1lll11ll1_opy_({
            bstack1l1llll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧⱈ"): bstack1l1llll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨⱉ"),
            bstack1l1llll_opy_ (u"ࠬࡲ࡯ࡨࡵࠪⱊ"): [{
                bstack1l1llll_opy_ (u"࠭࡫ࡪࡰࡧࠫⱋ"): bstack1l1llll_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࠩⱌ"),
                bstack1l1llll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫⱍ"): datetime.datetime.utcnow().isoformat() + bstack1l1llll_opy_ (u"ࠩ࡝ࠫⱎ"),
                bstack1l1llll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫⱏ"): screenshot[bstack1l1llll_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪⱐ")],
                bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬⱑ"): screenshot[bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ⱒ")]
            }]
        }, event_url=bstack1l1llll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬⱓ"))
    @classmethod
    @error_handler(class_method=True)
    def send_cbt_info(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1lll11ll1_opy_({
            bstack1l1llll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬⱔ"): bstack1l1llll_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭ⱕ"),
            bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬⱖ"): {
                bstack1l1llll_opy_ (u"ࠦࡺࡻࡩࡥࠤⱗ"): cls.current_test_uuid(),
                bstack1l1llll_opy_ (u"ࠧ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠦⱘ"): cls.bstack1l11111l_opy_(driver)
            }
        })
    @classmethod
    def bstack11lll1ll_opy_(cls, event: str, bstack1llll1l11_opy_: bstack1lll1l1ll_opy_):
        bstack111l1111_opy_ = {
            bstack1l1llll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪⱙ"): event,
            bstack1llll1l11_opy_.bstack1lll1l11l_opy_(): bstack1llll1l11_opy_.bstack1111l1ll_opy_(event)
        }
        cls.bstack1lll11ll1_opy_(bstack111l1111_opy_)
        result = getattr(bstack1llll1l11_opy_, bstack1l1llll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧⱚ"), None)
        if event == bstack1l1llll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩⱛ"):
            threading.current_thread().bstackTestMeta = {bstack1l1llll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩⱜ"): bstack1l1llll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫⱝ")}
        elif event == bstack1l1llll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ⱞ"):
            threading.current_thread().bstackTestMeta = {bstack1l1llll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬⱟ"): getattr(result, bstack1l1llll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭Ⱡ"), bstack1l1llll_opy_ (u"ࠧࠨⱡ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬⱢ"), None) is None or os.environ[bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭Ᵽ")] == bstack1l1llll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣⱤ")) and (os.environ.get(bstack1l1llll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩⱥ"), None) is None or os.environ[bstack1l1llll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪⱦ")] == bstack1l1llll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦⱧ")):
            return False
        return True
    @staticmethod
    def bstack1l1lll1l1ll1_opy_(func):
        def wrap(*args, **kwargs):
            if TestHubHandler.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1l1llll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ⱨ"): bstack1l1llll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫⱩ"),
            bstack1l1llll_opy_ (u"࡛ࠩ࠱ࡇ࡙ࡔࡂࡅࡎ࠱࡙ࡋࡓࡕࡑࡓࡗࠬⱪ"): bstack1l1llll_opy_ (u"ࠪࡸࡷࡻࡥࠨⱫ")
        }
        if os.environ.get(bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨⱬ"), None):
            headers[bstack1l1llll_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬⱭ")] = bstack1l1llll_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩⱮ").format(os.environ[bstack1l1llll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠦⱯ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1l1llll_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧⱰ").format(bstack1l1lll1llll1_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ⱱ"), None)
    @staticmethod
    def bstack1l11111l_opy_(driver):
        info = bstack1l1l11ll1_opy_(driver)
        try:
            from bstack_utils.helper import bstack11ll11lll1_opy_, bstack111lll111l1_opy_
            if bstack11ll11lll1_opy_():
                bstack1l1lll1l1l11_opy_ = bstack111lll111l1_opy_()
                if bstack1l1lll1l1l11_opy_:
                    info[bstack1l1llll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠧⱲ")] = bstack1l1lll1l1l11_opy_
                else:
                    logger.warning(bstack1l1llll_opy_ (u"ࠦ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࡢࡳࡧࡰࡥࡤࡶ࠽ࠤࡑ࡚ࡓࠡࡣࡦࡸ࡮ࡼࡥࠡࡤࡸࡸࠥࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑ࡚ࡓࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠥࡴ࡯ࡵࠢࡶࡩࡹࡁࠠࡶࡵ࡬ࡲ࡬ࠦࡤࡳ࡫ࡹࡩࡷࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡪࡦࠥⱳ"))
        except Exception as _e:
            logger.debug(bstack1l1llll_opy_ (u"ࠧ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࡣࡴࡨࡪࡦࡥࡷ࠾ࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡣࡳࡴࡱࡿࠠࡍࡖࡖࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡯ࡤ࠻ࠢࡾࢁࠧⱴ").format(_e))
        return {
            bstack1lll11llllll_opy_(): info
        }
    @staticmethod
    def bstack1l1lll11llll_opy_(exception_info, report):
        return [{bstack1l1llll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩⱵ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def failure_type(typename):
        if bstack1l1llll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥⱶ") in typename:
            return bstack1l1llll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤⱷ")
        return bstack1l1llll_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥⱸ")