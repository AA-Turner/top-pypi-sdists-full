# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1llllll1ll_opy_ = {}
        bstack1111ll1lll_opy_ = os.environ.get(bstack1lll1l_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭ྔ"), bstack1lll1l_opy_ (u"࠭ࠧྕ"))
        if not bstack1111ll1lll_opy_:
            return bstack1llllll1ll_opy_
        try:
            bstack1111lll111_opy_ = json.loads(bstack1111ll1lll_opy_)
            if bstack1lll1l_opy_ (u"ࠢࡰࡵࠥྖ") in bstack1111lll111_opy_:
                bstack1llllll1ll_opy_[bstack1lll1l_opy_ (u"ࠣࡱࡶࠦྗ")] = bstack1111lll111_opy_[bstack1lll1l_opy_ (u"ࠤࡲࡷࠧ྘")]
            if bstack1lll1l_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢྙ") in bstack1111lll111_opy_ or bstack1lll1l_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢྚ") in bstack1111lll111_opy_:
                bstack1llllll1ll_opy_[bstack1lll1l_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣྛ")] = bstack1111lll111_opy_.get(bstack1lll1l_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥྜ"), bstack1111lll111_opy_.get(bstack1lll1l_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥྜྷ")))
            if bstack1lll1l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤྞ") in bstack1111lll111_opy_ or bstack1lll1l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢྟ") in bstack1111lll111_opy_:
                bstack1llllll1ll_opy_[bstack1lll1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣྠ")] = bstack1111lll111_opy_.get(bstack1lll1l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧྡ"), bstack1111lll111_opy_.get(bstack1lll1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥྡྷ")))
            if bstack1lll1l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣྣ") in bstack1111lll111_opy_ or bstack1lll1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣྤ") in bstack1111lll111_opy_:
                bstack1llllll1ll_opy_[bstack1lll1l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤྥ")] = bstack1111lll111_opy_.get(bstack1lll1l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦྦ"), bstack1111lll111_opy_.get(bstack1lll1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦྦྷ")))
            if bstack1lll1l_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦྨ") in bstack1111lll111_opy_ or bstack1lll1l_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤྩ") in bstack1111lll111_opy_:
                bstack1llllll1ll_opy_[bstack1lll1l_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥྪ")] = bstack1111lll111_opy_.get(bstack1lll1l_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࠢྫ"), bstack1111lll111_opy_.get(bstack1lll1l_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧྫྷ")))
            if bstack1lll1l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦྭ") in bstack1111lll111_opy_ or bstack1lll1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤྮ") in bstack1111lll111_opy_:
                bstack1llllll1ll_opy_[bstack1lll1l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥྯ")] = bstack1111lll111_opy_.get(bstack1lll1l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢྰ"), bstack1111lll111_opy_.get(bstack1lll1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧྱ")))
            if bstack1lll1l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠥྲ") in bstack1111lll111_opy_ or bstack1lll1l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥླ") in bstack1111lll111_opy_:
                bstack1llllll1ll_opy_[bstack1lll1l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦྴ")] = bstack1111lll111_opy_.get(bstack1lll1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠨྵ"), bstack1111lll111_opy_.get(bstack1lll1l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨྶ")))
            if bstack1lll1l_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢྷ") in bstack1111lll111_opy_:
                bstack1llllll1ll_opy_[bstack1lll1l_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣྸ")] = bstack1111lll111_opy_[bstack1lll1l_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤྐྵ")]
        except Exception as error:
            logger.error(bstack1lll1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡨࡻࡲࡳࡧࡱࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡣࡷࡥ࠿ࠦࠢྺ") +  str(error))
        return bstack1llllll1ll_opy_