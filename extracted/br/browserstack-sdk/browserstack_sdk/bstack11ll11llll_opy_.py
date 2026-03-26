# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack111l11l111_opy_ = {}
        bstack1llllll11l1_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨၶ"), bstack1ll1lll_opy_ (u"ࠨࠩၷ"))
        if not bstack1llllll11l1_opy_:
            return bstack111l11l111_opy_
        try:
            bstack1llllll111l_opy_ = json.loads(bstack1llllll11l1_opy_)
            if bstack1ll1lll_opy_ (u"ࠤࡲࡷࠧၸ") in bstack1llllll111l_opy_:
                bstack111l11l111_opy_[bstack1ll1lll_opy_ (u"ࠥࡳࡸࠨၹ")] = bstack1llllll111l_opy_[bstack1ll1lll_opy_ (u"ࠦࡴࡹࠢၺ")]
            if bstack1ll1lll_opy_ (u"ࠧࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠤၻ") in bstack1llllll111l_opy_ or bstack1ll1lll_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤၼ") in bstack1llllll111l_opy_:
                bstack111l11l111_opy_[bstack1ll1lll_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥၽ")] = bstack1llllll111l_opy_.get(bstack1ll1lll_opy_ (u"ࠣࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧၾ"), bstack1llllll111l_opy_.get(bstack1ll1lll_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧၿ")))
            if bstack1ll1lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦႀ") in bstack1llllll111l_opy_ or bstack1ll1lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤႁ") in bstack1llllll111l_opy_:
                bstack111l11l111_opy_[bstack1ll1lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥႂ")] = bstack1llllll111l_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࠢႃ"), bstack1llllll111l_opy_.get(bstack1ll1lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧႄ")))
            if bstack1ll1lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠥႅ") in bstack1llllll111l_opy_ or bstack1ll1lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥႆ") in bstack1llllll111l_opy_:
                bstack111l11l111_opy_[bstack1ll1lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦႇ")] = bstack1llllll111l_opy_.get(bstack1ll1lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࠨႈ"), bstack1llllll111l_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨႉ")))
            if bstack1ll1lll_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࠨႊ") in bstack1llllll111l_opy_ or bstack1ll1lll_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠦႋ") in bstack1llllll111l_opy_:
                bstack111l11l111_opy_[bstack1ll1lll_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧႌ")] = bstack1llllll111l_opy_.get(bstack1ll1lll_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࠤႍ"), bstack1llllll111l_opy_.get(bstack1ll1lll_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢႎ")))
            if bstack1ll1lll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨႏ") in bstack1llllll111l_opy_ or bstack1ll1lll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦ႐") in bstack1llllll111l_opy_:
                bstack111l11l111_opy_[bstack1ll1lll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧ႑")] = bstack1llllll111l_opy_.get(bstack1ll1lll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤ႒"), bstack1llllll111l_opy_.get(bstack1ll1lll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ႓")))
            if bstack1ll1lll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ႔") in bstack1llllll111l_opy_ or bstack1ll1lll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧ႕") in bstack1llllll111l_opy_:
                bstack111l11l111_opy_[bstack1ll1lll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨ႖")] = bstack1llllll111l_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ႗"), bstack1llllll111l_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣ႘")))
            if bstack1ll1lll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤ႙") in bstack1llllll111l_opy_:
                bstack111l11l111_opy_[bstack1ll1lll_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥႚ")] = bstack1llllll111l_opy_[bstack1ll1lll_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦႛ")]
        except Exception as error:
            logger.error(bstack1ll1lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡣࡶࡴࡵࡩࡳࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡥࡹࡧ࠺ࠡࠤႜ") +  str(error))
        return bstack111l11l111_opy_