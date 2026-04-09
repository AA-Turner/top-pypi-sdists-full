# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1l1ll1111_opy_ = {}
        bstack1llll1lll11_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩႚ"), bstack11ll11_opy_ (u"ࠩࠪႛ"))
        if not bstack1llll1lll11_opy_:
            return bstack1l1ll1111_opy_
        try:
            bstack1llll1ll1ll_opy_ = json.loads(bstack1llll1lll11_opy_)
            if bstack11ll11_opy_ (u"ࠥࡳࡸࠨႜ") in bstack1llll1ll1ll_opy_:
                bstack1l1ll1111_opy_[bstack11ll11_opy_ (u"ࠦࡴࡹࠢႝ")] = bstack1llll1ll1ll_opy_[bstack11ll11_opy_ (u"ࠧࡵࡳࠣ႞")]
            if bstack11ll11_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥ႟") in bstack1llll1ll1ll_opy_ or bstack11ll11_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥႠ") in bstack1llll1ll1ll_opy_:
                bstack1l1ll1111_opy_[bstack11ll11_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦႡ")] = bstack1llll1ll1ll_opy_.get(bstack11ll11_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨႢ"), bstack1llll1ll1ll_opy_.get(bstack11ll11_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨႣ")))
            if bstack11ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧႤ") in bstack1llll1ll1ll_opy_ or bstack11ll11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥႥ") in bstack1llll1ll1ll_opy_:
                bstack1l1ll1111_opy_[bstack11ll11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦႦ")] = bstack1llll1ll1ll_opy_.get(bstack11ll11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣႧ"), bstack1llll1ll1ll_opy_.get(bstack11ll11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨႨ")))
            if bstack11ll11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦႩ") in bstack1llll1ll1ll_opy_ or bstack11ll11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦႪ") in bstack1llll1ll1ll_opy_:
                bstack1l1ll1111_opy_[bstack11ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧႫ")] = bstack1llll1ll1ll_opy_.get(bstack11ll11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢႬ"), bstack1llll1ll1ll_opy_.get(bstack11ll11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢႭ")))
            if bstack11ll11_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࠢႮ") in bstack1llll1ll1ll_opy_ or bstack11ll11_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧႯ") in bstack1llll1ll1ll_opy_:
                bstack1l1ll1111_opy_[bstack11ll11_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨႰ")] = bstack1llll1ll1ll_opy_.get(bstack11ll11_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࠥႱ"), bstack1llll1ll1ll_opy_.get(bstack11ll11_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣႲ")))
            if bstack11ll11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢႳ") in bstack1llll1ll1ll_opy_ or bstack11ll11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧႴ") in bstack1llll1ll1ll_opy_:
                bstack1l1ll1111_opy_[bstack11ll11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨႵ")] = bstack1llll1ll1ll_opy_.get(bstack11ll11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥႶ"), bstack1llll1ll1ll_opy_.get(bstack11ll11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣႷ")))
            if bstack11ll11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠨႸ") in bstack1llll1ll1ll_opy_ or bstack11ll11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨႹ") in bstack1llll1ll1ll_opy_:
                bstack1l1ll1111_opy_[bstack11ll11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢႺ")] = bstack1llll1ll1ll_opy_.get(bstack11ll11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤႻ"), bstack1llll1ll1ll_opy_.get(bstack11ll11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤႼ")))
            if bstack11ll11_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥႽ") in bstack1llll1ll1ll_opy_:
                bstack1l1ll1111_opy_[bstack11ll11_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦႾ")] = bstack1llll1ll1ll_opy_[bstack11ll11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧႿ")]
        except Exception as error:
            logger.error(bstack11ll11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡦࡺࡡ࠻ࠢࠥჀ") +  str(error))
        return bstack1l1ll1111_opy_