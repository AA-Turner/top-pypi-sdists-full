# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11ll1l1111l_opy_, bstack11ll1l1l11l_opy_, bstack11llll1l1l_opy_, bstack111l1lll11_opy_, bstack111lll11lll_opy_, bstack11l11lll11l_opy_, bstack111lllllll1_opy_, bstack1lll111111_opy_, bstack11ll1111ll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack111111l1111_opy_ import bstack111111l1l1l_opy_
import bstack_utils.bstack1111llll1_opy_ as bstack11111l111_opy_
from bstack_utils.bstack111lll1111_opy_ import bstack1l11l1l1l1_opy_
import bstack_utils.accessibility as bstack11ll1ll11_opy_
from bstack_utils.bstack1l111l111_opy_ import bstack1l111l111_opy_
from bstack_utils.bstack111ll1llll_opy_ import bstack1111ll1l1l_opy_
bstack1lllll1lllll_opy_ = bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡣࡰ࡮࡯ࡩࡨࡺ࡯ࡳ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ‑")
logger = logging.getLogger(__name__)
class bstack1l1lll1lll_opy_:
    bstack111111l1111_opy_ = None
    bs_config = None
    bstack1l11ll1l11_opy_ = None
    @classmethod
    @bstack111l1lll11_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11l1lll1l11_opy_, stage=STAGE.bstack1l1111ll1_opy_)
    def launch(cls, bs_config, bstack1l11ll1l11_opy_):
        cls.bs_config = bs_config
        cls.bstack1l11ll1l11_opy_ = bstack1l11ll1l11_opy_
        try:
            cls.bstack1lllll1lll1l_opy_()
            bstack11ll1lllll1_opy_ = bstack11ll1l1111l_opy_(bs_config)
            bstack11ll1llll11_opy_ = bstack11ll1l1l11l_opy_(bs_config)
            data = bstack11111l111_opy_.bstack1lllll1lll11_opy_(bs_config, bstack1l11ll1l11_opy_)
            config = {
                bstackl_opy_ (u"࠭ࡡࡶࡶ࡫ࠫ‒"): (bstack11ll1lllll1_opy_, bstack11ll1llll11_opy_),
                bstackl_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ–"): cls.default_headers()
            }
            response = bstack11llll1l1l_opy_(bstackl_opy_ (u"ࠨࡒࡒࡗ࡙࠭—"), cls.request_url(bstackl_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠳࠱ࡥࡹ࡮ࡲࡤࡴࠩ―")), data, config)
            if response.status_code != 200:
                bstack1llll11ll_opy_ = response.json()
                if bstack1llll11ll_opy_[bstackl_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ‖")] == False:
                    cls.bstack1lllll1l11ll_opy_(bstack1llll11ll_opy_)
                    return
                cls.bstack1lllll11l1ll_opy_(bstack1llll11ll_opy_[bstackl_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ‗")])
                cls.bstack1lllll1ll1l1_opy_(bstack1llll11ll_opy_[bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ‘")])
                return None
            bstack1lllll11l11l_opy_ = cls.bstack1lllll1l1lll_opy_(response)
            return bstack1lllll11l11l_opy_, response.json()
        except Exception as error:
            logger.error(bstackl_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࡽࢀࠦ’").format(str(error)))
            return None
    @classmethod
    @bstack111l1lll11_opy_(class_method=True)
    def stop(cls, bstack1lllll11ll11_opy_=None):
        if not bstack1l11l1l1l1_opy_.on() and not bstack11ll1ll11_opy_.on():
            return
        if os.environ.get(bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ‚")) == bstackl_opy_ (u"ࠣࡰࡸࡰࡱࠨ‛") or os.environ.get(bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ“")) == bstackl_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ”"):
            logger.error(bstackl_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡰࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧ„"))
            return {
                bstackl_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ‟"): bstackl_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ†"),
                bstackl_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ‡"): bstackl_opy_ (u"ࠨࡖࡲ࡯ࡪࡴ࠯ࡣࡷ࡬ࡰࡩࡏࡄࠡ࡫ࡶࠤࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠬࠡࡤࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡰ࡭࡬࡮ࡴࠡࡪࡤࡺࡪࠦࡦࡢ࡫࡯ࡩࡩ࠭•")
            }
        try:
            cls.bstack111111l1111_opy_.shutdown()
            data = {
                bstackl_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ‣"): bstack1lll111111_opy_()
            }
            if not bstack1lllll11ll11_opy_ is None:
                data[bstackl_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡳࡥࡵࡣࡧࡥࡹࡧࠧ․")] = [{
                    bstackl_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫ‥"): bstackl_opy_ (u"ࠬࡻࡳࡦࡴࡢ࡯࡮ࡲ࡬ࡦࡦࠪ…"),
                    bstackl_opy_ (u"࠭ࡳࡪࡩࡱࡥࡱ࠭‧"): bstack1lllll11ll11_opy_
                }]
            config = {
                bstackl_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ "): cls.default_headers()
            }
            bstack11ll11l1ll1_opy_ = bstackl_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸࡺ࡯ࡱࠩ ").format(os.environ[bstackl_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ‪")])
            bstack1lllll1ll111_opy_ = cls.request_url(bstack11ll11l1ll1_opy_)
            response = bstack11llll1l1l_opy_(bstackl_opy_ (u"ࠪࡔ࡚࡚ࠧ‫"), bstack1lllll1ll111_opy_, data, config)
            if not response.ok:
                raise Exception(bstackl_opy_ (u"ࠦࡘࡺ࡯ࡱࠢࡵࡩࡶࡻࡥࡴࡶࠣࡲࡴࡺࠠࡰ࡭ࠥ‬"))
        except Exception as error:
            logger.error(bstackl_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀ࠺ࠡࠤ‭") + str(error))
            return {
                bstackl_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭‮"): bstackl_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ "),
                bstackl_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ‰"): str(error)
            }
    @classmethod
    @bstack111l1lll11_opy_(class_method=True)
    def bstack1lllll1l1lll_opy_(cls, response):
        bstack1llll11ll_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1lllll11l11l_opy_ = {}
        if bstack1llll11ll_opy_.get(bstackl_opy_ (u"ࠩ࡭ࡻࡹ࠭‱")) is None:
            os.environ[bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ′")] = bstackl_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ″")
        else:
            os.environ[bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ‴")] = bstack1llll11ll_opy_.get(bstackl_opy_ (u"࠭ࡪࡸࡶࠪ‵"), bstackl_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ‶"))
        os.environ[bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭‷")] = bstack1llll11ll_opy_.get(bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ‸"), bstackl_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ‹"))
        logger.info(bstackl_opy_ (u"࡙ࠫ࡫ࡳࡵࡪࡸࡦࠥࡹࡴࡢࡴࡷࡩࡩࠦࡷࡪࡶ࡫ࠤ࡮ࡪ࠺ࠡࠩ›") + os.getenv(bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ※")));
        if bstack1l11l1l1l1_opy_.bstack1lllll11llll_opy_(cls.bs_config, cls.bstack1l11ll1l11_opy_.get(bstackl_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧ‼"), bstackl_opy_ (u"ࠧࠨ‽"))) is True:
            bstack11111111lll_opy_, build_hashed_id, bstack1lllll1l1l1l_opy_ = cls.bstack1lllll1l11l1_opy_(bstack1llll11ll_opy_)
            if bstack11111111lll_opy_ != None and build_hashed_id != None:
                bstack1lllll11l11l_opy_[bstackl_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ‾")] = {
                    bstackl_opy_ (u"ࠩ࡭ࡻࡹࡥࡴࡰ࡭ࡨࡲࠬ‿"): bstack11111111lll_opy_,
                    bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ⁀"): build_hashed_id,
                    bstackl_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ⁁"): bstack1lllll1l1l1l_opy_
                }
            else:
                bstack1lllll11l11l_opy_[bstackl_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⁂")] = {}
        else:
            bstack1lllll11l11l_opy_[bstackl_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⁃")] = {}
        bstack1lllll1llll1_opy_, build_hashed_id = cls.bstack1lllll11l111_opy_(bstack1llll11ll_opy_)
        if bstack1lllll1llll1_opy_ != None and build_hashed_id != None:
            bstack1lllll11l11l_opy_[bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⁄")] = {
                bstackl_opy_ (u"ࠨࡣࡸࡸ࡭ࡥࡴࡰ࡭ࡨࡲࠬ⁅"): bstack1lllll1llll1_opy_,
                bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⁆"): build_hashed_id,
            }
        else:
            bstack1lllll11l11l_opy_[bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⁇")] = {}
        if bstack1lllll11l11l_opy_[bstackl_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⁈")].get(bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⁉")) != None or bstack1lllll11l11l_opy_[bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⁊")].get(bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ⁋")) != None:
            cls.bstack1lllll11lll1_opy_(bstack1llll11ll_opy_.get(bstackl_opy_ (u"ࠨ࡬ࡺࡸࠬ⁌")), bstack1llll11ll_opy_.get(bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⁍")))
        return bstack1lllll11l11l_opy_
    @classmethod
    def bstack1lllll1l11l1_opy_(cls, bstack1llll11ll_opy_):
        if bstack1llll11ll_opy_.get(bstackl_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⁎")) == None:
            cls.bstack1lllll11l1ll_opy_()
            return [None, None, None]
        if bstack1llll11ll_opy_[bstackl_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⁏")][bstackl_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭⁐")] != True:
            cls.bstack1lllll11l1ll_opy_(bstack1llll11ll_opy_[bstackl_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⁑")])
            return [None, None, None]
        logger.debug(bstackl_opy_ (u"ࠧࡕࡧࡶࡸࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫ⁒"))
        os.environ[bstackl_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧ⁓")] = bstackl_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ⁔")
        if bstack1llll11ll_opy_.get(bstackl_opy_ (u"ࠪ࡮ࡼࡺࠧ⁕")):
            os.environ[bstackl_opy_ (u"ࠫࡈࡘࡅࡅࡇࡑࡘࡎࡇࡌࡔࡡࡉࡓࡗࡥࡃࡓࡃࡖࡌࡤࡘࡅࡑࡑࡕࡘࡎࡔࡇࠨ⁖")] = json.dumps({
                bstackl_opy_ (u"ࠬࡻࡳࡦࡴࡱࡥࡲ࡫ࠧ⁗"): bstack11ll1l1111l_opy_(cls.bs_config),
                bstackl_opy_ (u"࠭ࡰࡢࡵࡶࡻࡴࡸࡤࠨ⁘"): bstack11ll1l1l11l_opy_(cls.bs_config)
            })
        if bstack1llll11ll_opy_.get(bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ⁙")):
            os.environ[bstackl_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧ⁚")] = bstack1llll11ll_opy_[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⁛")]
        if bstack1llll11ll_opy_[bstackl_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⁜")].get(bstackl_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ⁝"), {}).get(bstackl_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ⁞")):
            os.environ[bstackl_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧ ")] = str(bstack1llll11ll_opy_[bstackl_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⁠")][bstackl_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ⁡")][bstackl_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭⁢")])
        else:
            os.environ[bstackl_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫ⁣")] = bstackl_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ⁤")
        return [bstack1llll11ll_opy_[bstackl_opy_ (u"ࠬࡰࡷࡵࠩ⁥")], bstack1llll11ll_opy_[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ⁦")], os.environ[bstackl_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ⁧")]]
    @classmethod
    def bstack1lllll11l111_opy_(cls, bstack1llll11ll_opy_):
        if bstack1llll11ll_opy_.get(bstackl_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⁨")) == None:
            cls.bstack1lllll1ll1l1_opy_()
            return [None, None]
        if bstack1llll11ll_opy_[bstackl_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⁩")][bstackl_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ⁪")] != True:
            cls.bstack1lllll1ll1l1_opy_(bstack1llll11ll_opy_[bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⁫")])
            return [None, None]
        if bstack1llll11ll_opy_[bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⁬")].get(bstackl_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ⁭")):
            logger.debug(bstackl_opy_ (u"ࠧࡕࡧࡶࡸࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫ⁮"))
            parsed = json.loads(os.getenv(bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ⁯"), bstackl_opy_ (u"ࠩࡾࢁࠬ⁰")))
            capabilities = bstack11111l111_opy_.bstack1lllll11l1l1_opy_(bstack1llll11ll_opy_[bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪⁱ")][bstackl_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ⁲")][bstackl_opy_ (u"ࠬࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ⁳")], bstackl_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⁴"), bstackl_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭⁵"))
            bstack1lllll1llll1_opy_ = capabilities[bstackl_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭⁶")]
            os.environ[bstackl_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ⁷")] = bstack1lllll1llll1_opy_
            if bstackl_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࠧ⁸") in bstack1llll11ll_opy_ and bstack1llll11ll_opy_.get(bstackl_opy_ (u"ࠦࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠥ⁹")) is None:
                parsed[bstackl_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⁺")] = capabilities[bstackl_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ⁻")]
            os.environ[bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ⁼")] = json.dumps(parsed)
            scripts = bstack11111l111_opy_.bstack1lllll11l1l1_opy_(bstack1llll11ll_opy_[bstackl_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⁽")][bstackl_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ⁾")][bstackl_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫⁿ")], bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ₀"), bstackl_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩ࠭₁"))
            bstack1l111l111_opy_.bstack111l1ll11_opy_(scripts)
            commands = bstack1llll11ll_opy_[bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭₂")][bstackl_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ₃")][bstackl_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࡗࡳ࡜ࡸࡡࡱࠩ₄")].get(bstackl_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫ₅"))
            bstack1l111l111_opy_.bstack11ll1lll111_opy_(commands)
            bstack11ll11llll1_opy_ = capabilities.get(bstackl_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ₆"))
            bstack1l111l111_opy_.bstack11ll11ll111_opy_(bstack11ll11llll1_opy_)
            bstack1l111l111_opy_.store()
        return [bstack1lllll1llll1_opy_, bstack1llll11ll_opy_[bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭₇")]]
    @classmethod
    def bstack1lllll11l1ll_opy_(cls, response=None):
        os.environ[bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ₈")] = bstackl_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ₉")
        os.environ[bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ₊")] = bstackl_opy_ (u"ࠨࡰࡸࡰࡱ࠭₋")
        os.environ[bstackl_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨ₌")] = bstackl_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ₍")
        os.environ[bstackl_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪ₎")] = bstackl_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ₏")
        os.environ[bstackl_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧₐ")] = bstackl_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧₑ")
        cls.bstack1lllll1l11ll_opy_(response, bstackl_opy_ (u"ࠣࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠣₒ"))
        return [None, None, None]
    @classmethod
    def bstack1lllll1ll1l1_opy_(cls, response=None):
        os.environ[bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧₓ")] = bstackl_opy_ (u"ࠪࡲࡺࡲ࡬ࠨₔ")
        os.environ[bstackl_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩₕ")] = bstackl_opy_ (u"ࠬࡴࡵ࡭࡮ࠪₖ")
        os.environ[bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪₗ")] = bstackl_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬₘ")
        cls.bstack1lllll1l11ll_opy_(response, bstackl_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠣₙ"))
        return [None, None, None]
    @classmethod
    def bstack1lllll11lll1_opy_(cls, jwt, build_hashed_id):
        os.environ[bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ₚ")] = jwt
        os.environ[bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨₛ")] = build_hashed_id
    @classmethod
    def bstack1lllll1l11ll_opy_(cls, response=None, product=bstackl_opy_ (u"ࠦࠧₜ")):
        if response == None or response.get(bstackl_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬ₝")) == None:
            logger.error(product + bstackl_opy_ (u"ࠨࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠣ₞"))
            return
        for error in response[bstackl_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧ₟")]:
            bstack11l1111l11l_opy_ = error[bstackl_opy_ (u"ࠨ࡭ࡨࡽࠬ₠")]
            error_message = error[bstackl_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ₡")]
            if error_message:
                if bstack11l1111l11l_opy_ == bstackl_opy_ (u"ࠥࡉࡗࡘࡏࡓࡡࡄࡇࡈࡋࡓࡔࡡࡇࡉࡓࡏࡅࡅࠤ₢"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstackl_opy_ (u"ࠦࡉࡧࡴࡢࠢࡸࡴࡱࡵࡡࡥࠢࡷࡳࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࠧ₣") + product + bstackl_opy_ (u"ࠧࠦࡦࡢ࡫࡯ࡩࡩࠦࡤࡶࡧࠣࡸࡴࠦࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥ₤"))
    @classmethod
    def bstack1lllll1lll1l_opy_(cls):
        if cls.bstack111111l1111_opy_ is not None:
            return
        cls.bstack111111l1111_opy_ = bstack111111l1l1l_opy_(cls.bstack1lllll1l1l11_opy_)
        cls.bstack111111l1111_opy_.start()
    @classmethod
    def bstack111l11lll1_opy_(cls):
        if cls.bstack111111l1111_opy_ is None:
            return
        cls.bstack111111l1111_opy_.shutdown()
    @classmethod
    @bstack111l1lll11_opy_(class_method=True)
    def bstack1lllll1l1l11_opy_(cls, bstack111l1l111l_opy_, event_url=bstackl_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬ₥")):
        config = {
            bstackl_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ₦"): cls.default_headers()
        }
        logger.debug(bstackl_opy_ (u"ࠣࡲࡲࡷࡹࡥࡤࡢࡶࡤ࠾࡙ࠥࡥ࡯ࡦ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤࡹࡵࠠࡵࡧࡶࡸ࡭ࡻࡢࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࡷࠥࢁࡽࠣ₧").format(bstackl_opy_ (u"ࠩ࠯ࠤࠬ₨").join([event[bstackl_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ₩")] for event in bstack111l1l111l_opy_])))
        response = bstack11llll1l1l_opy_(bstackl_opy_ (u"ࠫࡕࡕࡓࡕࠩ₪"), cls.request_url(event_url), bstack111l1l111l_opy_, config)
        bstack11lll1111ll_opy_ = response.json()
    @classmethod
    def bstack1l1lll1l_opy_(cls, bstack111l1l111l_opy_, event_url=bstackl_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫ₫")):
        logger.debug(bstackl_opy_ (u"ࠨࡳࡦࡰࡧࡣࡩࡧࡴࡢ࠼ࠣࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡥࡩࡪࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡤࡤࡸࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨ€").format(bstack111l1l111l_opy_[bstackl_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ₭")]))
        if not bstack11111l111_opy_.bstack1lllll1l1111_opy_(bstack111l1l111l_opy_[bstackl_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ₮")]):
            logger.debug(bstackl_opy_ (u"ࠤࡶࡩࡳࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡎࡰࡶࠣࡥࡩࡪࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢ₯").format(bstack111l1l111l_opy_[bstackl_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ₰")]))
            return
        bstack1l1l11l1_opy_ = bstack11111l111_opy_.bstack1lllll1ll1ll_opy_(bstack111l1l111l_opy_[bstackl_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ₱")], bstack111l1l111l_opy_.get(bstackl_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ₲")))
        if bstack1l1l11l1_opy_ != None:
            if bstack111l1l111l_opy_.get(bstackl_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ₳")) != None:
                bstack111l1l111l_opy_[bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ₴")][bstackl_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭₵")] = bstack1l1l11l1_opy_
            else:
                bstack111l1l111l_opy_[bstackl_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧ₶")] = bstack1l1l11l1_opy_
        if event_url == bstackl_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩ₷"):
            cls.bstack1lllll1lll1l_opy_()
            logger.debug(bstackl_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡃࡧࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡴࡰࠢࡥࡥࡹࡩࡨࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢ₸").format(bstack111l1l111l_opy_[bstackl_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ₹")]))
            cls.bstack111111l1111_opy_.add(bstack111l1l111l_opy_)
        elif event_url == bstackl_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ₺"):
            cls.bstack1lllll1l1l11_opy_([bstack111l1l111l_opy_], event_url)
    @classmethod
    @bstack111l1lll11_opy_(class_method=True)
    def bstack1l1l1l1ll1_opy_(cls, logs):
        for log in logs:
            bstack1lllll11ll1l_opy_ = {
                bstackl_opy_ (u"ࠧ࡬࡫ࡱࡨࠬ₻"): bstackl_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡌࡐࡉࠪ₼"),
                bstackl_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ₽"): log[bstackl_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ₾")],
                bstackl_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ₿"): log[bstackl_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ⃀")],
                bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡣࡷ࡫ࡳࡱࡱࡱࡷࡪ࠭⃁"): {},
                bstackl_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⃂"): log[bstackl_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⃃")],
            }
            if bstackl_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⃄") in log:
                bstack1lllll11ll1l_opy_[bstackl_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⃅")] = log[bstackl_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⃆")]
            elif bstackl_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⃇") in log:
                bstack1lllll11ll1l_opy_[bstackl_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⃈")] = log[bstackl_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⃉")]
            cls.bstack1l1lll1l_opy_({
                bstackl_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⃊"): bstackl_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭⃋"),
                bstackl_opy_ (u"ࠪࡰࡴ࡭ࡳࠨ⃌"): [bstack1lllll11ll1l_opy_]
            })
    @classmethod
    @bstack111l1lll11_opy_(class_method=True)
    def bstack1llllll11111_opy_(cls, steps):
        bstack1lllll1l1ll1_opy_ = []
        for step in steps:
            bstack1lllll1l111l_opy_ = {
                bstackl_opy_ (u"ࠫࡰ࡯࡮ࡥࠩ⃍"): bstackl_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗ࡙ࡋࡐࠨ⃎"),
                bstackl_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ⃏"): step[bstackl_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⃐")],
                bstackl_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ⃑"): step[bstackl_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴ⃒ࠬ")],
                bstackl_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨ⃓ࠫ"): step[bstackl_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⃔")],
                bstackl_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ⃕"): step[bstackl_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ⃖")]
            }
            if bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⃗") in step:
                bstack1lllll1l111l_opy_[bstackl_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⃘")] = step[bstackl_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥ⃙ࠩ")]
            elif bstackl_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦ⃚ࠪ") in step:
                bstack1lllll1l111l_opy_[bstackl_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⃛")] = step[bstackl_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⃜")]
            bstack1lllll1l1ll1_opy_.append(bstack1lllll1l111l_opy_)
        cls.bstack1l1lll1l_opy_({
            bstackl_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⃝"): bstackl_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ⃞"),
            bstackl_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭⃟"): bstack1lllll1l1ll1_opy_
        })
    @classmethod
    @bstack111l1lll11_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11lll1111_opy_, stage=STAGE.bstack1l1111ll1_opy_)
    def bstack111ll11l1_opy_(cls, screenshot):
        cls.bstack1l1lll1l_opy_({
            bstackl_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⃠"): bstackl_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ⃡"),
            bstackl_opy_ (u"ࠫࡱࡵࡧࡴࠩ⃢"): [{
                bstackl_opy_ (u"ࠬࡱࡩ࡯ࡦࠪ⃣"): bstackl_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠨ⃤"),
                bstackl_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲ⃥ࠪ"): datetime.datetime.utcnow().isoformat() + bstackl_opy_ (u"ࠨ࡜⃦ࠪ"),
                bstackl_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⃧"): screenshot[bstackl_opy_ (u"ࠪ࡭ࡲࡧࡧࡦ⃨ࠩ")],
                bstackl_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⃩"): screenshot[bstackl_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨ⃪ࠬ")]
            }]
        }, event_url=bstackl_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶ⃫ࠫ"))
    @classmethod
    @bstack111l1lll11_opy_(class_method=True)
    def bstack1l1ll11l11_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l1lll1l_opy_({
            bstackl_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ⃬ࠫ"): bstackl_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨ⃭ࠬ"),
            bstackl_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱ⃮ࠫ"): {
                bstackl_opy_ (u"ࠥࡹࡺ࡯ࡤ⃯ࠣ"): cls.current_test_uuid(),
                bstackl_opy_ (u"ࠦ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠥ⃰"): cls.bstack111ll1111l_opy_(driver)
            }
        })
    @classmethod
    def bstack111lll111l_opy_(cls, event: str, bstack111l1l111l_opy_: bstack1111ll1l1l_opy_):
        bstack111l1l1ll1_opy_ = {
            bstackl_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⃱"): event,
            bstack111l1l111l_opy_.bstack111l11l11l_opy_(): bstack111l1l111l_opy_.bstack111l111lll_opy_(event)
        }
        cls.bstack1l1lll1l_opy_(bstack111l1l1ll1_opy_)
        result = getattr(bstack111l1l111l_opy_, bstackl_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⃲"), None)
        if event == bstackl_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⃳"):
            threading.current_thread().bstackTestMeta = {bstackl_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⃴"): bstackl_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ⃵")}
        elif event == bstackl_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⃶"):
            threading.current_thread().bstackTestMeta = {bstackl_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⃷"): getattr(result, bstackl_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⃸"), bstackl_opy_ (u"࠭ࠧ⃹"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⃺"), None) is None or os.environ[bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⃻")] == bstackl_opy_ (u"ࠤࡱࡹࡱࡲࠢ⃼")) and (os.environ.get(bstackl_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ⃽"), None) is None or os.environ[bstackl_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ⃾")] == bstackl_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ⃿")):
            return False
        return True
    @staticmethod
    def bstack1lllll1ll11l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1lll1lll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstackl_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ℀"): bstackl_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ℁"),
            bstackl_opy_ (u"ࠨ࡚࠰ࡆࡘ࡚ࡁࡄࡍ࠰ࡘࡊ࡙ࡔࡐࡒࡖࠫℂ"): bstackl_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ℃")
        }
        if os.environ.get(bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ℄"), None):
            headers[bstackl_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ℅")] = bstackl_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨ℆").format(os.environ[bstackl_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠥℇ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstackl_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭℈").format(bstack1lllll1lllll_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstackl_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ℉"), None)
    @staticmethod
    def bstack111ll1111l_opy_(driver):
        return {
            bstack111lll11lll_opy_(): bstack11l11lll11l_opy_(driver)
        }
    @staticmethod
    def bstack1lllll111lll_opy_(exception_info, report):
        return [{bstackl_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬℊ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack111111ll11_opy_(typename):
        if bstackl_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨℋ") in typename:
            return bstackl_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧℌ")
        return bstackl_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨℍ")