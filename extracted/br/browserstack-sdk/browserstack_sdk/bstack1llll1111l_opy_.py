# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1ll111111_opy_ = {}
        bstack1111llll1l_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩྐ"), bstack11l1l11_opy_ (u"ࠩࠪྑ"))
        if not bstack1111llll1l_opy_:
            return bstack1ll111111_opy_
        try:
            bstack1111llll11_opy_ = json.loads(bstack1111llll1l_opy_)
            if bstack11l1l11_opy_ (u"ࠥࡳࡸࠨྒ") in bstack1111llll11_opy_:
                bstack1ll111111_opy_[bstack11l1l11_opy_ (u"ࠦࡴࡹࠢྒྷ")] = bstack1111llll11_opy_[bstack11l1l11_opy_ (u"ࠧࡵࡳࠣྔ")]
            if bstack11l1l11_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥྕ") in bstack1111llll11_opy_ or bstack11l1l11_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥྖ") in bstack1111llll11_opy_:
                bstack1ll111111_opy_[bstack11l1l11_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦྗ")] = bstack1111llll11_opy_.get(bstack11l1l11_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ྘"), bstack1111llll11_opy_.get(bstack11l1l11_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨྙ")))
            if bstack11l1l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧྚ") in bstack1111llll11_opy_ or bstack11l1l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥྛ") in bstack1111llll11_opy_:
                bstack1ll111111_opy_[bstack11l1l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦྜ")] = bstack1111llll11_opy_.get(bstack11l1l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣྜྷ"), bstack1111llll11_opy_.get(bstack11l1l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨྞ")))
            if bstack11l1l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦྟ") in bstack1111llll11_opy_ or bstack11l1l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦྠ") in bstack1111llll11_opy_:
                bstack1ll111111_opy_[bstack11l1l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧྡ")] = bstack1111llll11_opy_.get(bstack11l1l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢྡྷ"), bstack1111llll11_opy_.get(bstack11l1l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢྣ")))
            if bstack11l1l11_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࠢྤ") in bstack1111llll11_opy_ or bstack11l1l11_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧྥ") in bstack1111llll11_opy_:
                bstack1ll111111_opy_[bstack11l1l11_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨྦ")] = bstack1111llll11_opy_.get(bstack11l1l11_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࠥྦྷ"), bstack1111llll11_opy_.get(bstack11l1l11_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣྨ")))
            if bstack11l1l11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢྩ") in bstack1111llll11_opy_ or bstack11l1l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧྪ") in bstack1111llll11_opy_:
                bstack1ll111111_opy_[bstack11l1l11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨྫ")] = bstack1111llll11_opy_.get(bstack11l1l11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥྫྷ"), bstack1111llll11_opy_.get(bstack11l1l11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣྭ")))
            if bstack11l1l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠨྮ") in bstack1111llll11_opy_ or bstack11l1l11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨྯ") in bstack1111llll11_opy_:
                bstack1ll111111_opy_[bstack11l1l11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢྰ")] = bstack1111llll11_opy_.get(bstack11l1l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤྱ"), bstack1111llll11_opy_.get(bstack11l1l11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤྲ")))
            if bstack11l1l11_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥླ") in bstack1111llll11_opy_:
                bstack1ll111111_opy_[bstack11l1l11_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦྴ")] = bstack1111llll11_opy_[bstack11l1l11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧྵ")]
        except Exception as error:
            logger.error(bstack11l1l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡦࡺࡡ࠻ࠢࠥྶ") +  str(error))
        return bstack1ll111111_opy_