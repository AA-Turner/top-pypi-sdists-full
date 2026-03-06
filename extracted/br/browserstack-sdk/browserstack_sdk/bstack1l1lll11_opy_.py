# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1lllll1l1l_opy_ = {}
        bstack1111ll1l1l_opy_ = os.environ.get(bstack1111_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧྕ"), bstack1111_opy_ (u"ࠧࠨྖ"))
        if not bstack1111ll1l1l_opy_:
            return bstack1lllll1l1l_opy_
        try:
            bstack1111ll1ll1_opy_ = json.loads(bstack1111ll1l1l_opy_)
            if bstack1111_opy_ (u"ࠣࡱࡶࠦྗ") in bstack1111ll1ll1_opy_:
                bstack1lllll1l1l_opy_[bstack1111_opy_ (u"ࠤࡲࡷࠧ྘")] = bstack1111ll1ll1_opy_[bstack1111_opy_ (u"ࠥࡳࡸࠨྙ")]
            if bstack1111_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣྚ") in bstack1111ll1ll1_opy_ or bstack1111_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣྛ") in bstack1111ll1ll1_opy_:
                bstack1lllll1l1l_opy_[bstack1111_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤྜ")] = bstack1111ll1ll1_opy_.get(bstack1111_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦྜྷ"), bstack1111ll1ll1_opy_.get(bstack1111_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦྞ")))
            if bstack1111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥྟ") in bstack1111ll1ll1_opy_ or bstack1111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣྠ") in bstack1111ll1ll1_opy_:
                bstack1lllll1l1l_opy_[bstack1111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤྡ")] = bstack1111ll1ll1_opy_.get(bstack1111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨྡྷ"), bstack1111ll1ll1_opy_.get(bstack1111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦྣ")))
            if bstack1111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤྤ") in bstack1111ll1ll1_opy_ or bstack1111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤྥ") in bstack1111ll1ll1_opy_:
                bstack1lllll1l1l_opy_[bstack1111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥྦ")] = bstack1111ll1ll1_opy_.get(bstack1111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧྦྷ"), bstack1111ll1ll1_opy_.get(bstack1111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧྨ")))
            if bstack1111_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࠧྩ") in bstack1111ll1ll1_opy_ or bstack1111_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥྪ") in bstack1111ll1ll1_opy_:
                bstack1lllll1l1l_opy_[bstack1111_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠦྫ")] = bstack1111ll1ll1_opy_.get(bstack1111_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࠣྫྷ"), bstack1111ll1ll1_opy_.get(bstack1111_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨྭ")))
            if bstack1111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧྮ") in bstack1111ll1ll1_opy_ or bstack1111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥྯ") in bstack1111ll1ll1_opy_:
                bstack1lllll1l1l_opy_[bstack1111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦྰ")] = bstack1111ll1ll1_opy_.get(bstack1111_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣྱ"), bstack1111ll1ll1_opy_.get(bstack1111_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨྲ")))
            if bstack1111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠦླ") in bstack1111ll1ll1_opy_ or bstack1111_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦྴ") in bstack1111ll1ll1_opy_:
                bstack1lllll1l1l_opy_[bstack1111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧྵ")] = bstack1111ll1ll1_opy_.get(bstack1111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢྶ"), bstack1111ll1ll1_opy_.get(bstack1111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢྷ")))
            if bstack1111_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣྸ") in bstack1111ll1ll1_opy_:
                bstack1lllll1l1l_opy_[bstack1111_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤྐྵ")] = bstack1111ll1ll1_opy_[bstack1111_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥྺ")]
        except Exception as error:
            logger.error(bstack1111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡩࡵࡳࡴࡨࡲࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡤࡸࡦࡀࠠࠣྻ") +  str(error))
        return bstack1lllll1l1l_opy_