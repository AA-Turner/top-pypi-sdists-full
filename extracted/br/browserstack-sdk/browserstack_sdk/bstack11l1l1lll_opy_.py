# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1l111l1l_opy_ = {}
        bstack111lll1l11_opy_ = os.environ.get(bstack1ll11ll_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩ༒"), bstack1ll11ll_opy_ (u"ࠩࠪ༓"))
        if not bstack111lll1l11_opy_:
            return bstack1l111l1l_opy_
        try:
            bstack111lll1l1l_opy_ = json.loads(bstack111lll1l11_opy_)
            if bstack1ll11ll_opy_ (u"ࠥࡳࡸࠨ༔") in bstack111lll1l1l_opy_:
                bstack1l111l1l_opy_[bstack1ll11ll_opy_ (u"ࠦࡴࡹࠢ༕")] = bstack111lll1l1l_opy_[bstack1ll11ll_opy_ (u"ࠧࡵࡳࠣ༖")]
            if bstack1ll11ll_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥ༗") in bstack111lll1l1l_opy_ or bstack1ll11ll_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰ༘ࠥ") in bstack111lll1l1l_opy_:
                bstack1l111l1l_opy_[bstack1ll11ll_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱ༙ࠦ")] = bstack111lll1l1l_opy_.get(bstack1ll11ll_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ༚"), bstack111lll1l1l_opy_.get(bstack1ll11ll_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨ༛")))
            if bstack1ll11ll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧ༜") in bstack111lll1l1l_opy_ or bstack1ll11ll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥ༝") in bstack111lll1l1l_opy_:
                bstack1l111l1l_opy_[bstack1ll11ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦ༞")] = bstack111lll1l1l_opy_.get(bstack1ll11ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣ༟"), bstack111lll1l1l_opy_.get(bstack1ll11ll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨ༠")))
            if bstack1ll11ll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦ༡") in bstack111lll1l1l_opy_ or bstack1ll11ll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦ༢") in bstack111lll1l1l_opy_:
                bstack1l111l1l_opy_[bstack1ll11ll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧ༣")] = bstack111lll1l1l_opy_.get(bstack1ll11ll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ༤"), bstack111lll1l1l_opy_.get(bstack1ll11ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢ༥")))
            if bstack1ll11ll_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࠢ༦") in bstack111lll1l1l_opy_ or bstack1ll11ll_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧ༧") in bstack111lll1l1l_opy_:
                bstack1l111l1l_opy_[bstack1ll11ll_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨ༨")] = bstack111lll1l1l_opy_.get(bstack1ll11ll_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࠥ༩"), bstack111lll1l1l_opy_.get(bstack1ll11ll_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣ༪")))
            if bstack1ll11ll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢ༫") in bstack111lll1l1l_opy_ or bstack1ll11ll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧ༬") in bstack111lll1l1l_opy_:
                bstack1l111l1l_opy_[bstack1ll11ll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨ༭")] = bstack111lll1l1l_opy_.get(bstack1ll11ll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥ༮"), bstack111lll1l1l_opy_.get(bstack1ll11ll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ༯")))
            if bstack1ll11ll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ༰") in bstack111lll1l1l_opy_ or bstack1ll11ll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨ༱") in bstack111lll1l1l_opy_:
                bstack1l111l1l_opy_[bstack1ll11ll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢ༲")] = bstack111lll1l1l_opy_.get(bstack1ll11ll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ༳"), bstack111lll1l1l_opy_.get(bstack1ll11ll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ༴")))
            if bstack1ll11ll_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵ༵ࠥ") in bstack111lll1l1l_opy_:
                bstack1l111l1l_opy_[bstack1ll11ll_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦ༶")] = bstack111lll1l1l_opy_[bstack1ll11ll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷ༷ࠧ")]
        except Exception as error:
            logger.error(bstack1ll11ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡦࡺࡡ࠻ࠢࠥ༸") +  str(error))
        return bstack1l111l1l_opy_