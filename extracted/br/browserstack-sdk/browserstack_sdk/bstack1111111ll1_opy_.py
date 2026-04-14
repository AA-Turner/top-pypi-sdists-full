# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1lllll11lll_opy_ = {}
        bstack1llll1ll11l_opy_ = os.environ.get(bstack1l111l_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫႱ"), bstack1l111l_opy_ (u"ࠫࠬႲ"))
        if not bstack1llll1ll11l_opy_:
            return bstack1lllll11lll_opy_
        try:
            bstack1llll1ll111_opy_ = json.loads(bstack1llll1ll11l_opy_)
            if bstack1l111l_opy_ (u"ࠧࡵࡳࠣႳ") in bstack1llll1ll111_opy_:
                bstack1lllll11lll_opy_[bstack1l111l_opy_ (u"ࠨ࡯ࡴࠤႴ")] = bstack1llll1ll111_opy_[bstack1l111l_opy_ (u"ࠢࡰࡵࠥႵ")]
            if bstack1l111l_opy_ (u"ࠣࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧႶ") in bstack1llll1ll111_opy_ or bstack1l111l_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧႷ") in bstack1llll1ll111_opy_:
                bstack1lllll11lll_opy_[bstack1l111l_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨႸ")] = bstack1llll1ll111_opy_.get(bstack1l111l_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣႹ"), bstack1llll1ll111_opy_.get(bstack1l111l_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣႺ")))
            if bstack1l111l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࠢႻ") in bstack1llll1ll111_opy_ or bstack1l111l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧႼ") in bstack1llll1ll111_opy_:
                bstack1lllll11lll_opy_[bstack1l111l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨႽ")] = bstack1llll1ll111_opy_.get(bstack1l111l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥႾ"), bstack1llll1ll111_opy_.get(bstack1l111l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣႿ")))
            if bstack1l111l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࠨჀ") in bstack1llll1ll111_opy_ or bstack1l111l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨჁ") in bstack1llll1ll111_opy_:
                bstack1lllll11lll_opy_[bstack1l111l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢჂ")] = bstack1llll1ll111_opy_.get(bstack1l111l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤჃ"), bstack1llll1ll111_opy_.get(bstack1l111l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤჄ")))
            if bstack1l111l_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࠤჅ") in bstack1llll1ll111_opy_ or bstack1l111l_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢ჆") in bstack1llll1ll111_opy_:
                bstack1lllll11lll_opy_[bstack1l111l_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣჇ")] = bstack1llll1ll111_opy_.get(bstack1l111l_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࠧ჈"), bstack1llll1ll111_opy_.get(bstack1l111l_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥ჉")))
            if bstack1l111l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤ჊") in bstack1llll1ll111_opy_ or bstack1l111l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ჋") in bstack1llll1ll111_opy_:
                bstack1lllll11lll_opy_[bstack1l111l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ჌")] = bstack1llll1ll111_opy_.get(bstack1l111l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧჍ"), bstack1llll1ll111_opy_.get(bstack1l111l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥ჎")))
            if bstack1l111l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ჏") in bstack1llll1ll111_opy_ or bstack1l111l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣა") in bstack1llll1ll111_opy_:
                bstack1lllll11lll_opy_[bstack1l111l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤბ")] = bstack1llll1ll111_opy_.get(bstack1l111l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠦგ"), bstack1llll1ll111_opy_.get(bstack1l111l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦდ")))
            if bstack1l111l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧე") in bstack1llll1ll111_opy_:
                bstack1lllll11lll_opy_[bstack1l111l_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨვ")] = bstack1llll1ll111_opy_[bstack1l111l_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢზ")]
        except Exception as error:
            logger.error(bstack1l111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡡࡵࡣ࠽ࠤࠧთ") +  str(error))
        return bstack1lllll11lll_opy_