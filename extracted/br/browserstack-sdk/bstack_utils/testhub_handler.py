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
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1111ll11lll_opy_, bstack1111l1l1111_opy_, bstack1ll11l11l_opy_, error_handler, bstack1llll111l1ll_opy_, bstack1ll1ll111ll_opy_, bstack1lllll11llll_opy_, bstack1111l1l1l_opy_, bstack1ll11l1ll1_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1ll11lll1l11_opy_ import bstack1ll11lllll11_opy_
import bstack_utils.bstack1l1l1lll_opy_ as TestHubUtils
from bstack_utils.bstack111l1ll11_opy_ import bstack111ll111_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.bstack1lll1lllll1_opy_ import bstack1lll1ll11l1_opy_
from bstack_utils.constants import bstack1ll1ll1l1l_opy_
bstack1ll111l1l1l1_opy_ = bstack111ll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡤࡱ࡯ࡰࡪࡩࡴࡰࡴ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭⟲")
logger = logging.getLogger(__name__)
class TestHubHandler:
    bstack1ll11lll1l11_opy_ = None
    bs_config = None
    bstack1lll111l11_opy_ = None
    _1ll111lll11l_opy_ = False
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11111l11l1l_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
    def launch(cls, bs_config, bstack1lll111l11_opy_):
        cls._1ll111lll11l_opy_ = True
        cls.bs_config = bs_config
        cls.bstack1lll111l11_opy_ = bstack1lll111l11_opy_
        try:
            cls.bstack1ll11l111111_opy_()
            bstack1111l1l111l_opy_ = bstack1111ll11lll_opy_(bs_config)
            bstack1111ll1l111_opy_ = bstack1111l1l1111_opy_(bs_config)
            data = TestHubUtils.bstack1ll111l1ll11_opy_(bs_config, bstack1lll111l11_opy_)
            config = {
                bstack111ll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ⟳"): (bstack1111l1l111l_opy_, bstack1111ll1l111_opy_),
                bstack111ll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ⟴"): cls.default_headers()
            }
            response = bstack1ll11l11l_opy_(bstack111ll_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ⟵"), cls.request_url(bstack111ll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠴࠲ࡦࡺ࡯࡬ࡥࡵࠪ⟶")), data, config)
            if response.status_code != 200:
                bstack1ll1lll11_opy_ = response.json()
                if bstack1ll1lll11_opy_[bstack111ll_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ⟷")] == False:
                    cls.bstack1ll111llll11_opy_(bstack1ll1lll11_opy_)
                    return
                cls.bstack1ll111ll1111_opy_(bstack1ll1lll11_opy_[bstack111ll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⟸")])
                cls.bstack1ll111llll1l_opy_(bstack1ll1lll11_opy_[bstack111ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⟹")])
                return None
            bstack1ll111ll11ll_opy_ = cls.bstack1ll111lll111_opy_(response)
            return bstack1ll111ll11ll_opy_, response.json()
        except Exception as error:
            logger.error(bstack111ll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡾࢁࠧ⟺").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11111l1ll11_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
    def stop(cls, bstack1ll111l1lll1_opy_=None):
        if not bstack111ll111_opy_.on() and not a11y.on():
            return
        if not cls._1ll111lll11l_opy_:
            logger.info(bstack111ll_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࠠࡪࡵࠣࡇࡑࡏ࠭࡮ࡣࡱࡥ࡬࡫ࡤࠡࠪ࡯ࡥࡺࡴࡣࡩࠢࡱࡳࡹࠦࡣࡢ࡮࡯ࡩࡩࠦࡢࡺࠢࡖࡈࡐ࠯ࠠ࠮ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠤࡸࡺ࡯ࡱࠢࡄࡔࡎࠦࡲࡦࡳࡸࡩࡸࡺࠢ⟻"))
            if cls.bstack1ll11lll1l11_opy_ is not None:
                logger.info(bstack111ll_opy_ (u"ࠤࡖ࡬ࡺࡺࡴࡪࡰࡪࠤࡩࡵࡷ࡯ࠢࡵࡩࡶࡻࡥࡴࡶࠣࡵࡺ࡫ࡵࡦࠤ⟼"))
                cls.bstack1ll11lll1l11_opy_.shutdown()
            else:
                logger.info(bstack111ll_opy_ (u"ࠥࡒࡴࠦࡲࡦࡳࡸࡩࡸࡺࠠࡲࡷࡨࡹࡪࠦࡴࡰࠢࡶ࡬ࡺࡺࡤࡰࡹࡱࠦ⟽"))
            return
        if os.environ.get(bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⟾")) == bstack111ll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ⟿") or os.environ.get(bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⠀")) == bstack111ll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ⠁"):
            logger.error(bstack111ll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡴࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫ⠂"))
            return {
                bstack111ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⠃"): bstack111ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ⠄"),
                bstack111ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⠅"): bstack111ll_opy_ (u"࡚ࠬ࡯࡬ࡧࡱ࠳ࡧࡻࡩ࡭ࡦࡌࡈࠥ࡯ࡳࠡࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧ࠰ࠥࡨࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦ࡭ࡪࡩ࡫ࡸࠥ࡮ࡡࡷࡧࠣࡪࡦ࡯࡬ࡦࡦࠪ⠆")
            }
        try:
            cls.bstack1ll11lll1l11_opy_.shutdown()
            data = {
                bstack111ll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⠇"): bstack1111l1l1l_opy_()
            }
            if not bstack1ll111l1lll1_opy_ is None:
                data[bstack111ll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡰࡩࡹࡧࡤࡢࡶࡤࠫ⠈")] = [{
                    bstack111ll_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ⠉"): bstack111ll_opy_ (u"ࠩࡸࡷࡪࡸ࡟࡬࡫࡯ࡰࡪࡪࠧ⠊"),
                    bstack111ll_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࠪ⠋"): bstack1ll111l1lll1_opy_
                }]
            config = {
                bstack111ll_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬ⠌"): cls.default_headers()
            }
            bstack1111l1111l1_opy_ = bstack111ll_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡷࡳࡵ࠭⠍").format(os.environ[bstack111ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦ⠎")])
            bstack1ll111l1l1ll_opy_ = cls.request_url(bstack1111l1111l1_opy_)
            response = bstack1ll11l11l_opy_(bstack111ll_opy_ (u"ࠧࡑࡗࡗࠫ⠏"), bstack1ll111l1l1ll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack111ll_opy_ (u"ࠣࡕࡷࡳࡵࠦࡲࡦࡳࡸࡩࡸࡺࠠ࡯ࡱࡷࠤࡴࡱࠢ⠐"))
        except Exception as error:
            logger.error(bstack111ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡵࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡗࡩࡸࡺࡈࡶࡤ࠽࠾ࠥࠨ⠑") + str(error))
            return {
                bstack111ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⠒"): bstack111ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ⠓"),
                bstack111ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⠔"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll111lll111_opy_(cls, response):
        bstack1ll1lll11_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1ll111ll11ll_opy_ = {}
        if bstack1ll1lll11_opy_.get(bstack111ll_opy_ (u"࠭ࡪࡸࡶࠪ⠕")) is None:
            os.environ[bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⠖")] = bstack111ll_opy_ (u"ࠨࡰࡸࡰࡱ࠭⠗")
        else:
            os.environ[bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⠘")] = bstack1ll1lll11_opy_.get(bstack111ll_opy_ (u"ࠪ࡮ࡼࡺࠧ⠙"), bstack111ll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ⠚"))
        os.environ[bstack111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⠛")] = bstack1ll1lll11_opy_.get(bstack111ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ⠜"), bstack111ll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ⠝"))
        logger.info(bstack111ll_opy_ (u"ࠨࡖࡨࡷࡹ࡮ࡵࡣࠢࡶࡸࡦࡸࡴࡦࡦࠣࡻ࡮ࡺࡨࠡ࡫ࡧ࠾ࠥ࠭⠞") + os.getenv(bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⠟")));
        if bstack111ll111_opy_.bstack1ll111l1llll_opy_(cls.bs_config, cls.bstack1lll111l11_opy_.get(bstack111ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫ⠠"), bstack111ll_opy_ (u"ࠫࠬ⠡"))) is True:
            bstack1ll11ll1l1ll_opy_, build_hashed_id, allow_screenshots = cls.bstack1ll111ll1l1l_opy_(bstack1ll1lll11_opy_)
            if bstack1ll11ll1l1ll_opy_ != None and build_hashed_id != None:
                bstack1ll111ll11ll_opy_[bstack111ll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⠢")] = {
                    bstack111ll_opy_ (u"࠭ࡪࡸࡶࡢࡸࡴࡱࡥ࡯ࠩ⠣"): bstack1ll11ll1l1ll_opy_,
                    bstack111ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ⠤"): build_hashed_id,
                    bstack111ll_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ⠥"): allow_screenshots
                }
            else:
                bstack1ll111ll11ll_opy_[bstack111ll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⠦")] = {}
        else:
            bstack1ll111ll11ll_opy_[bstack111ll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⠧")] = {}
        bstack1ll111ll111l_opy_, build_hashed_id = cls.bstack1ll111ll11l1_opy_(bstack1ll1lll11_opy_)
        if bstack1ll111ll111l_opy_ != None and build_hashed_id != None:
            bstack1ll111ll11ll_opy_[bstack111ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⠨")] = {
                bstack111ll_opy_ (u"ࠬࡧࡵࡵࡪࡢࡸࡴࡱࡥ࡯ࠩ⠩"): bstack1ll111ll111l_opy_,
                bstack111ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ⠪"): build_hashed_id,
            }
        else:
            bstack1ll111ll11ll_opy_[bstack111ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⠫")] = {}
        if bstack1ll111ll11ll_opy_[bstack111ll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⠬")].get(bstack111ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⠭")) != None or bstack1ll111ll11ll_opy_[bstack111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⠮")].get(bstack111ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭⠯")) != None:
            cls.bstack1ll111ll1lll_opy_(bstack1ll1lll11_opy_.get(bstack111ll_opy_ (u"ࠬࡰࡷࡵࠩ⠰")), bstack1ll1lll11_opy_.get(bstack111ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ⠱")))
        return bstack1ll111ll11ll_opy_
    @classmethod
    def bstack1ll111ll1l1l_opy_(cls, bstack1ll1lll11_opy_):
        if bstack1ll1lll11_opy_.get(bstack111ll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⠲")) == None:
            cls.bstack1ll111ll1111_opy_()
            return [None, None, None]
        if bstack1ll1lll11_opy_[bstack111ll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⠳")][bstack111ll_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ⠴")] != True:
            cls.bstack1ll111ll1111_opy_(bstack1ll1lll11_opy_[bstack111ll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⠵")])
            return [None, None, None]
        logger.debug(bstack111ll_opy_ (u"ࠫࢀࢃࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭⠶").format(bstack1ll1ll1l1l_opy_))
        os.environ[bstack111ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡅࡒࡑࡕࡒࡅࡕࡇࡇࠫ⠷")] = bstack111ll_opy_ (u"࠭ࡴࡳࡷࡨࠫ⠸")
        if bstack1ll1lll11_opy_.get(bstack111ll_opy_ (u"ࠧ࡫ࡹࡷࠫ⠹")):
            os.environ[bstack111ll_opy_ (u"ࠨࡅࡕࡉࡉࡋࡎࡕࡋࡄࡐࡘࡥࡆࡐࡔࡢࡇࡗࡇࡓࡉࡡࡕࡉࡕࡕࡒࡕࡋࡑࡋࠬ⠺")] = json.dumps({
                bstack111ll_opy_ (u"ࠩࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ⠻"): bstack1111ll11lll_opy_(cls.bs_config),
                bstack111ll_opy_ (u"ࠪࡴࡦࡹࡳࡸࡱࡵࡨࠬ⠼"): bstack1111l1l1111_opy_(cls.bs_config)
            })
        if bstack1ll1lll11_opy_.get(bstack111ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭⠽")):
            os.environ[bstack111ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫ⠾")] = bstack1ll1lll11_opy_[bstack111ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ⠿")]
        if bstack1ll1lll11_opy_[bstack111ll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⡀")].get(bstack111ll_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ⡁"), {}).get(bstack111ll_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭⡂")):
            os.environ[bstack111ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫ⡃")] = str(bstack1ll1lll11_opy_[bstack111ll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⡄")][bstack111ll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭⡅")][bstack111ll_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ⡆")])
        else:
            os.environ[bstack111ll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ⡇")] = bstack111ll_opy_ (u"ࠣࡰࡸࡰࡱࠨ⡈")
        return [bstack1ll1lll11_opy_[bstack111ll_opy_ (u"ࠩ࡭ࡻࡹ࠭⡉")], bstack1ll1lll11_opy_[bstack111ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ⡊")], os.environ[bstack111ll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬ⡋")]]
    @classmethod
    def bstack1ll111ll11l1_opy_(cls, bstack1ll1lll11_opy_):
        if bstack1ll1lll11_opy_.get(bstack111ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⡌")) == None:
            cls.bstack1ll111llll1l_opy_()
            return [None, None]
        if bstack1ll1lll11_opy_[bstack111ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⡍")][bstack111ll_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨ⡎")] != True:
            cls.bstack1ll111llll1l_opy_(bstack1ll1lll11_opy_[bstack111ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⡏")])
            return [None, None]
        if bstack1ll1lll11_opy_[bstack111ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⡐")].get(bstack111ll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ⡑")):
            logger.debug(bstack111ll_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠡࠨ⡒"))
            parsed = json.loads(os.getenv(bstack111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭⡓"), bstack111ll_opy_ (u"࠭ࡻࡾࠩ⡔")))
            capabilities = TestHubUtils.bstack1ll111lll1ll_opy_(bstack1ll1lll11_opy_[bstack111ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⡕")][bstack111ll_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ⡖")][bstack111ll_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ⡗")], bstack111ll_opy_ (u"ࠪࡲࡦࡳࡥࠨ⡘"), bstack111ll_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪ⡙"))
            bstack1ll111ll111l_opy_ = capabilities[bstack111ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࡵ࡫ࡦࡰࠪ⡚")]
            os.environ[bstack111ll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ⡛")] = bstack1ll111ll111l_opy_
            if capabilities.get(bstack111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬ⡜")):
                os.environ[bstack111ll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡗࡉࡘ࡚࡟ࡓࡗࡑࡣࡎࡊࠧ⡝")] = str(capabilities[bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡮ࡪࠧ⡞")])
            if capabilities.get(bstack111ll_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡣࡧࡻࡩ࡭ࡦࡢࡹࡺ࡯ࡤࠨ⡟")):
                os.environ[bstack111ll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡈࡕࡊࡎࡇࡣ࡚࡛ࡉࡅࠩ⡠")] = str(capabilities[bstack111ll_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡥࡢࡶ࡫࡯ࡨࡤࡻࡵࡪࡦࠪ⡡")])
            if bstack111ll_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣ⡢") in bstack1ll1lll11_opy_ and bstack1ll1lll11_opy_.get(bstack111ll_opy_ (u"ࠢࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪࠨ⡣")) is None:
                parsed[bstack111ll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ⡤")] = capabilities[bstack111ll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ⡥")]
            os.environ[bstack111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ⡦")] = json.dumps(parsed)
            scripts = TestHubUtils.bstack1ll111lll1ll_opy_(bstack1ll1lll11_opy_[bstack111ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⡧")][bstack111ll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭⡨")][bstack111ll_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧ⡩")], bstack111ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⡪"), bstack111ll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࠩ⡫"))
            accessibility_scripts.bstack11ll111l11_opy_(scripts)
            commands_to_wrap = bstack1ll1lll11_opy_[bstack111ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⡬")][bstack111ll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ⡭")][bstack111ll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࡚࡯ࡘࡴࡤࡴࠬ⡮")]
            commands = commands_to_wrap.get(bstack111ll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧ⡯"))
            accessibility_scripts.bstack1l1l1111l11_opy_(commands)
            scripts_to_run = commands_to_wrap.get(bstack111ll_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࡔࡰࡔࡸࡲࠬ⡰"))
            accessibility_scripts.bstack1111l111l1l_opy_(scripts_to_run)
            bstack1111ll1l1ll_opy_ = capabilities.get(bstack111ll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ⡱"))
            accessibility_scripts.bstack1111l111ll1_opy_(bstack1111ll1l1ll_opy_)
            accessibility_scripts.store()
        return [bstack1ll111ll111l_opy_, bstack1ll1lll11_opy_[bstack111ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ⡲")]]
    @classmethod
    def bstack1ll111ll1111_opy_(cls, response=None):
        os.environ[bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⡳")] = bstack111ll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ⡴")
        os.environ[bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⡵")] = bstack111ll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ⡶")
        os.environ[bstack111ll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬ⡷")] = bstack111ll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭⡸")
        os.environ[bstack111ll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧ⡹")] = bstack111ll_opy_ (u"ࠤࡱࡹࡱࡲࠢ⡺")
        os.environ[bstack111ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫ⡻")] = bstack111ll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ⡼")
        cls.bstack1ll111llll11_opy_(response, bstack111ll_opy_ (u"ࠧࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠧ⡽"))
        return [None, None, None]
    @classmethod
    def bstack1ll111llll1l_opy_(cls, response=None):
        os.environ[bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⡾")] = bstack111ll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ⡿")
        os.environ[bstack111ll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭⢀")] = bstack111ll_opy_ (u"ࠩࡱࡹࡱࡲࠧ⢁")
        os.environ[bstack111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⢂")] = bstack111ll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ⢃")
        cls.bstack1ll111llll11_opy_(response, bstack111ll_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠧ⢄"))
        return [None, None, None]
    @classmethod
    def bstack1ll111ll1lll_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⢅")] = jwt
        os.environ[bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ⢆")] = build_hashed_id
    @classmethod
    def bstack1ll111llll11_opy_(cls, response=None, product=bstack111ll_opy_ (u"ࠣࠤ⢇")):
        if response == None or response.get(bstack111ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩ⢈")) == None:
            logger.error(product + bstack111ll_opy_ (u"ࠥࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠧ⢉"))
            return
        for error in response[bstack111ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫ⢊")]:
            bstack1lll1lll1l1l_opy_ = error[bstack111ll_opy_ (u"ࠬࡱࡥࡺࠩ⢋")]
            error_message = error[bstack111ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⢌")]
            if error_message:
                if bstack1lll1lll1l1l_opy_ == bstack111ll_opy_ (u"ࠢࡆࡔࡕࡓࡗࡥࡁࡄࡅࡈࡗࡘࡥࡄࡆࡐࡌࡉࡉࠨ⢍"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack111ll_opy_ (u"ࠣࡆࡤࡸࡦࠦࡵࡱ࡮ࡲࡥࡩࠦࡴࡰࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࠤ⢎") + product + bstack111ll_opy_ (u"ࠤࠣࡪࡦ࡯࡬ࡦࡦࠣࡨࡺ࡫ࠠࡵࡱࠣࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢ⢏"))
    @classmethod
    def bstack1ll11l111111_opy_(cls):
        if cls.bstack1ll11lll1l11_opy_ is not None:
            return
        cls.bstack1ll11lll1l11_opy_ = bstack1ll11lllll11_opy_(cls.post_data)
        cls.bstack1ll11lll1l11_opy_.start()
    @classmethod
    def bstack1lll11ll1ll_opy_(cls):
        if cls.bstack1ll11lll1l11_opy_ is None:
            return
        cls.bstack1ll11lll1l11_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def post_data(cls, bstack1lll11l111l_opy_, event_url=bstack111ll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩ⢐")):
        config = {
            bstack111ll_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬ⢑"): cls.default_headers()
        }
        logger.debug(bstack111ll_opy_ (u"ࠧࡶ࡯ࡴࡶࡢࡨࡦࡺࡡ࠻ࠢࡖࡩࡳࡪࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡶࡲࠤࡹ࡫ࡳࡵࡪࡸࡦࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࡴࠢࡾࢁࠧ⢒").format(bstack111ll_opy_ (u"࠭ࠬࠡࠩ⢓").join([event[bstack111ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⢔")] for event in bstack1lll11l111l_opy_])))
        response = bstack1ll11l11l_opy_(bstack111ll_opy_ (u"ࠨࡒࡒࡗ࡙࠭⢕"), cls.request_url(event_url), bstack1lll11l111l_opy_, config)
        bstack1111lll11l1_opy_ = response.json()
    @classmethod
    def bstack11lll1l11l_opy_(cls, bstack1lll11l111l_opy_, event_url=bstack111ll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨ⢖")):
        logger.debug(bstack111ll_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡂࡶࡷࡩࡲࡶࡴࡪࡰࡪࠤࡹࡵࠠࡢࡦࡧࠤࡩࡧࡴࡢࠢࡷࡳࠥࡨࡡࡵࡥ࡫ࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࡀࠠࡼࡿࠥ⢗").format(bstack1lll11l111l_opy_[bstack111ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⢘")]))
        if not TestHubUtils.bstack1ll111lll1l1_opy_(bstack1lll11l111l_opy_[bstack111ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⢙")]):
            logger.debug(bstack111ll_opy_ (u"ࠨࡳࡦࡰࡧࡣࡩࡧࡴࡢ࠼ࠣࡒࡴࡺࠠࡢࡦࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫࠺ࠡࡽࢀࠦ⢚").format(bstack1lll11l111l_opy_[bstack111ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⢛")]))
            return
        bstack11ll11l11_opy_ = TestHubUtils.bstack1ll11l11111l_opy_(bstack1lll11l111l_opy_[bstack111ll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⢜")], bstack1lll11l111l_opy_.get(bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ⢝")))
        if bstack11ll11l11_opy_ != None:
            if bstack1lll11l111l_opy_.get(bstack111ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ⢞")) != None:
                bstack1lll11l111l_opy_[bstack111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭⢟")][bstack111ll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪ⢠")] = bstack11ll11l11_opy_
            else:
                bstack1lll11l111l_opy_[bstack111ll_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫ⢡")] = bstack11ll11l11_opy_
        if event_url == bstack111ll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭⢢"):
            cls.bstack1ll11l111111_opy_()
            logger.debug(bstack111ll_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡇࡤࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡸࡴࠦࡢࡢࡶࡦ࡬ࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫࠺ࠡࡽࢀࠦ⢣").format(bstack1lll11l111l_opy_[bstack111ll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⢤")]))
            cls.bstack1ll11lll1l11_opy_.add(bstack1lll11l111l_opy_)
        elif event_url == bstack111ll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ⢥"):
            cls.post_data([bstack1lll11l111l_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack1lllll1l1_opy_(cls, logs):
        for log in logs:
            bstack1ll111l1ll1l_opy_ = {
                bstack111ll_opy_ (u"ࠫࡰ࡯࡮ࡥࠩ⢦"): bstack111ll_opy_ (u"࡚ࠬࡅࡔࡖࡢࡐࡔࡍࠧ⢧"),
                bstack111ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ⢨"): log[bstack111ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⢩")],
                bstack111ll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ⢪"): log[bstack111ll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ⢫")],
                bstack111ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡠࡴࡨࡷࡵࡵ࡮ࡴࡧࠪ⢬"): {},
                bstack111ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⢭"): log[bstack111ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⢮")],
            }
            if bstack111ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⢯") in log:
                bstack1ll111l1ll1l_opy_[bstack111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⢰")] = log[bstack111ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⢱")]
            elif bstack111ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⢲") in log:
                bstack1ll111l1ll1l_opy_[bstack111ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⢳")] = log[bstack111ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⢴")]
            cls.bstack11lll1l11l_opy_({
                bstack111ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⢵"): bstack111ll_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ⢶"),
                bstack111ll_opy_ (u"ࠧ࡭ࡱࡪࡷࠬ⢷"): [bstack1ll111l1ll1l_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll111ll1l11_opy_(cls, steps):
        bstack1ll111ll1ll1_opy_ = []
        for step in steps:
            bstack1ll111lllll1_opy_ = {
                bstack111ll_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭⢸"): bstack111ll_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡔࡖࡈࡔࠬ⢹"),
                bstack111ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⢺"): step[bstack111ll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ⢻")],
                bstack111ll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ⢼"): step[bstack111ll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ⢽")],
                bstack111ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⢾"): step[bstack111ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⢿")],
                bstack111ll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ⣀"): step[bstack111ll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ⣁")]
            }
            if bstack111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⣂") in step:
                bstack1ll111lllll1_opy_[bstack111ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⣃")] = step[bstack111ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⣄")]
            elif bstack111ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⣅") in step:
                bstack1ll111lllll1_opy_[bstack111ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⣆")] = step[bstack111ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⣇")]
            bstack1ll111ll1ll1_opy_.append(bstack1ll111lllll1_opy_)
        cls.bstack11lll1l11l_opy_({
            bstack111ll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⣈"): bstack111ll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ⣉"),
            bstack111ll_opy_ (u"ࠬࡲ࡯ࡨࡵࠪ⣊"): bstack1ll111ll1ll1_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack1lll1llll_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
    def bstack1lllll11lll_opy_(cls, screenshot):
        cls.bstack11lll1l11l_opy_({
            bstack111ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⣋"): bstack111ll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ⣌"),
            bstack111ll_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭⣍"): [{
                bstack111ll_opy_ (u"ࠩ࡮࡭ࡳࡪࠧ⣎"): bstack111ll_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࠬ⣏"),
                bstack111ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ⣐"): datetime.datetime.utcnow().isoformat() + bstack111ll_opy_ (u"ࠬࡠࠧ⣑"),
                bstack111ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⣒"): screenshot[bstack111ll_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭⣓")],
                bstack111ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⣔"): screenshot[bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⣕")]
            }]
        }, event_url=bstack111ll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ⣖"))
    @classmethod
    @error_handler(class_method=True)
    def send_cbt_info(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11lll1l11l_opy_({
            bstack111ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⣗"): bstack111ll_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩ⣘"),
            bstack111ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ⣙"): {
                bstack111ll_opy_ (u"ࠢࡶࡷ࡬ࡨࠧ⣚"): cls.current_test_uuid(),
                bstack111ll_opy_ (u"ࠣ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠢ⣛"): cls.bstack1llll11lll1_opy_(driver)
            }
        })
    @classmethod
    def bstack1llll11ll11_opy_(cls, event: str, bstack1lll11l111l_opy_: bstack1lll1ll11l1_opy_):
        bstack1lll1lll111_opy_ = {
            bstack111ll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⣜"): event,
            bstack1lll11l111l_opy_.bstack1lll11lll11_opy_(): bstack1lll11l111l_opy_.bstack1lll1l111ll_opy_(event)
        }
        cls.bstack11lll1l11l_opy_(bstack1lll1lll111_opy_)
        result = getattr(bstack1lll11l111l_opy_, bstack111ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⣝"), None)
        if event == bstack111ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⣞"):
            threading.current_thread().bstackTestMeta = {bstack111ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⣟"): bstack111ll_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ⣠")}
        elif event == bstack111ll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⣡"):
            threading.current_thread().bstackTestMeta = {bstack111ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⣢"): getattr(result, bstack111ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⣣"), bstack111ll_opy_ (u"ࠪࠫ⣤"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⣥"), None) is None or os.environ[bstack111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⣦")] == bstack111ll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ⣧")) and (os.environ.get(bstack111ll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ⣨"), None) is None or os.environ[bstack111ll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭⣩")] == bstack111ll_opy_ (u"ࠤࡱࡹࡱࡲࠢ⣪")):
            return False
        return True
    @staticmethod
    def bstack1ll111llllll_opy_(func):
        def wrap(*args, **kwargs):
            if TestHubHandler.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack111ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ⣫"): bstack111ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ⣬"),
            bstack111ll_opy_ (u"ࠬ࡞࠭ࡃࡕࡗࡅࡈࡑ࠭ࡕࡇࡖࡘࡔࡖࡓࠨ⣭"): bstack111ll_opy_ (u"࠭ࡴࡳࡷࡨࠫ⣮")
        }
        if os.environ.get(bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⣯"), None):
            headers[bstack111ll_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨ⣰")] = bstack111ll_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬ⣱").format(os.environ[bstack111ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠢ⣲")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack111ll_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪ⣳").format(bstack1ll111l1l1l1_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack111ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⣴"), None)
    @staticmethod
    def bstack1llll11lll1_opy_(driver):
        return {
            bstack1llll111l1ll_opy_(): bstack1ll1ll111ll_opy_(driver)
        }
    @staticmethod
    def bstack1ll111l1l11l_opy_(exception_info, report):
        return [{bstack111ll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ⣵"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1ll111l111l_opy_(typename):
        if bstack111ll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥ⣶") in typename:
            return bstack111ll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤ⣷")
        return bstack111ll_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥ⣸")