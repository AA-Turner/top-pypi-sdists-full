# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack111ll1l111_opy_ = {}
        bstack1lllll1llll_opy_ = os.environ.get(bstack1ll11_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫႇ"), bstack1ll11_opy_ (u"ࠫࠬႈ"))
        if not bstack1lllll1llll_opy_:
            return bstack111ll1l111_opy_
        try:
            bstack1llllll1111_opy_ = json.loads(bstack1lllll1llll_opy_)
            if bstack1ll11_opy_ (u"ࠧࡵࡳࠣႉ") in bstack1llllll1111_opy_:
                bstack111ll1l111_opy_[bstack1ll11_opy_ (u"ࠨ࡯ࡴࠤႊ")] = bstack1llllll1111_opy_[bstack1ll11_opy_ (u"ࠢࡰࡵࠥႋ")]
            if bstack1ll11_opy_ (u"ࠣࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧႌ") in bstack1llllll1111_opy_ or bstack1ll11_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲႍࠧ") in bstack1llllll1111_opy_:
                bstack111ll1l111_opy_[bstack1ll11_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨႎ")] = bstack1llllll1111_opy_.get(bstack1ll11_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣႏ"), bstack1llllll1111_opy_.get(bstack1ll11_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣ႐")))
            if bstack1ll11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࠢ႑") in bstack1llllll1111_opy_ or bstack1ll11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧ႒") in bstack1llllll1111_opy_:
                bstack111ll1l111_opy_[bstack1ll11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨ႓")] = bstack1llllll1111_opy_.get(bstack1ll11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥ႔"), bstack1llllll1111_opy_.get(bstack1ll11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣ႕")))
            if bstack1ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ႖") in bstack1llllll1111_opy_ or bstack1ll11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨ႗") in bstack1llllll1111_opy_:
                bstack111ll1l111_opy_[bstack1ll11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢ႘")] = bstack1llllll1111_opy_.get(bstack1ll11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ႙"), bstack1llllll1111_opy_.get(bstack1ll11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤႚ")))
            if bstack1ll11_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࠤႛ") in bstack1llllll1111_opy_ or bstack1ll11_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢႜ") in bstack1llllll1111_opy_:
                bstack111ll1l111_opy_[bstack1ll11_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣႝ")] = bstack1llllll1111_opy_.get(bstack1ll11_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࠧ႞"), bstack1llllll1111_opy_.get(bstack1ll11_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥ႟")))
            if bstack1ll11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤႠ") in bstack1llllll1111_opy_ or bstack1ll11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢႡ") in bstack1llllll1111_opy_:
                bstack111ll1l111_opy_[bstack1ll11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣႢ")] = bstack1llllll1111_opy_.get(bstack1ll11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧႣ"), bstack1llllll1111_opy_.get(bstack1ll11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥႤ")))
            if bstack1ll11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣႥ") in bstack1llllll1111_opy_ or bstack1ll11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣႦ") in bstack1llllll1111_opy_:
                bstack111ll1l111_opy_[bstack1ll11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤႧ")] = bstack1llllll1111_opy_.get(bstack1ll11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠦႨ"), bstack1llllll1111_opy_.get(bstack1ll11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦႩ")))
            if bstack1ll11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧႪ") in bstack1llllll1111_opy_:
                bstack111ll1l111_opy_[bstack1ll11_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨႫ")] = bstack1llllll1111_opy_[bstack1ll11_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢႬ")]
        except Exception as error:
            logger.error(bstack1ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡡࡵࡣ࠽ࠤࠧႭ") +  str(error))
        return bstack111ll1l111_opy_