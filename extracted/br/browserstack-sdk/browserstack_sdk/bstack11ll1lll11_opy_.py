# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1llll11ll1_opy_ = {}
        bstack1llll1lll11_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩႚ"), bstack1ll1l11_opy_ (u"ࠩࠪႛ"))
        if not bstack1llll1lll11_opy_:
            return bstack1llll11ll1_opy_
        try:
            bstack1llll1ll1ll_opy_ = json.loads(bstack1llll1lll11_opy_)
            if bstack1ll1l11_opy_ (u"ࠥࡳࡸࠨႜ") in bstack1llll1ll1ll_opy_:
                bstack1llll11ll1_opy_[bstack1ll1l11_opy_ (u"ࠦࡴࡹࠢႝ")] = bstack1llll1ll1ll_opy_[bstack1ll1l11_opy_ (u"ࠧࡵࡳࠣ႞")]
            if bstack1ll1l11_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥ႟") in bstack1llll1ll1ll_opy_ or bstack1ll1l11_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥႠ") in bstack1llll1ll1ll_opy_:
                bstack1llll11ll1_opy_[bstack1ll1l11_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦႡ")] = bstack1llll1ll1ll_opy_.get(bstack1ll1l11_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨႢ"), bstack1llll1ll1ll_opy_.get(bstack1ll1l11_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨႣ")))
            if bstack1ll1l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧႤ") in bstack1llll1ll1ll_opy_ or bstack1ll1l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥႥ") in bstack1llll1ll1ll_opy_:
                bstack1llll11ll1_opy_[bstack1ll1l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦႦ")] = bstack1llll1ll1ll_opy_.get(bstack1ll1l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣႧ"), bstack1llll1ll1ll_opy_.get(bstack1ll1l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨႨ")))
            if bstack1ll1l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦႩ") in bstack1llll1ll1ll_opy_ or bstack1ll1l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦႪ") in bstack1llll1ll1ll_opy_:
                bstack1llll11ll1_opy_[bstack1ll1l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧႫ")] = bstack1llll1ll1ll_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢႬ"), bstack1llll1ll1ll_opy_.get(bstack1ll1l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢႭ")))
            if bstack1ll1l11_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࠢႮ") in bstack1llll1ll1ll_opy_ or bstack1ll1l11_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧႯ") in bstack1llll1ll1ll_opy_:
                bstack1llll11ll1_opy_[bstack1ll1l11_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨႰ")] = bstack1llll1ll1ll_opy_.get(bstack1ll1l11_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࠥႱ"), bstack1llll1ll1ll_opy_.get(bstack1ll1l11_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣႲ")))
            if bstack1ll1l11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢႳ") in bstack1llll1ll1ll_opy_ or bstack1ll1l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧႴ") in bstack1llll1ll1ll_opy_:
                bstack1llll11ll1_opy_[bstack1ll1l11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨႵ")] = bstack1llll1ll1ll_opy_.get(bstack1ll1l11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥႶ"), bstack1llll1ll1ll_opy_.get(bstack1ll1l11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣႷ")))
            if bstack1ll1l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠨႸ") in bstack1llll1ll1ll_opy_ or bstack1ll1l11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨႹ") in bstack1llll1ll1ll_opy_:
                bstack1llll11ll1_opy_[bstack1ll1l11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢႺ")] = bstack1llll1ll1ll_opy_.get(bstack1ll1l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤႻ"), bstack1llll1ll1ll_opy_.get(bstack1ll1l11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤႼ")))
            if bstack1ll1l11_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥႽ") in bstack1llll1ll1ll_opy_:
                bstack1llll11ll1_opy_[bstack1ll1l11_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦႾ")] = bstack1llll1ll1ll_opy_[bstack1ll1l11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧႿ")]
        except Exception as error:
            logger.error(bstack1ll1l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡦࡺࡡ࠻ࠢࠥჀ") +  str(error))
        return bstack1llll11ll1_opy_