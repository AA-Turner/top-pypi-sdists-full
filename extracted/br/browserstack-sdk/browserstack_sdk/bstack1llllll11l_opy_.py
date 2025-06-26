# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1l11llll1_opy_ = {}
        bstack111llllll1_opy_ = os.environ.get(bstack11ll1l1_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫ໎"), bstack11ll1l1_opy_ (u"ࠫࠬ໏"))
        if not bstack111llllll1_opy_:
            return bstack1l11llll1_opy_
        try:
            bstack111lllllll_opy_ = json.loads(bstack111llllll1_opy_)
            if bstack11ll1l1_opy_ (u"ࠧࡵࡳࠣ໐") in bstack111lllllll_opy_:
                bstack1l11llll1_opy_[bstack11ll1l1_opy_ (u"ࠨ࡯ࡴࠤ໑")] = bstack111lllllll_opy_[bstack11ll1l1_opy_ (u"ࠢࡰࡵࠥ໒")]
            if bstack11ll1l1_opy_ (u"ࠣࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ໓") in bstack111lllllll_opy_ or bstack11ll1l1_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧ໔") in bstack111lllllll_opy_:
                bstack1l11llll1_opy_[bstack11ll1l1_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨ໕")] = bstack111lllllll_opy_.get(bstack11ll1l1_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ໖"), bstack111lllllll_opy_.get(bstack11ll1l1_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣ໗")))
            if bstack11ll1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࠢ໘") in bstack111lllllll_opy_ or bstack11ll1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧ໙") in bstack111lllllll_opy_:
                bstack1l11llll1_opy_[bstack11ll1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨ໚")] = bstack111lllllll_opy_.get(bstack11ll1l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥ໛"), bstack111lllllll_opy_.get(bstack11ll1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣໜ")))
            if bstack11ll1l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࠨໝ") in bstack111lllllll_opy_ or bstack11ll1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨໞ") in bstack111lllllll_opy_:
                bstack1l11llll1_opy_[bstack11ll1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢໟ")] = bstack111lllllll_opy_.get(bstack11ll1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ໠"), bstack111lllllll_opy_.get(bstack11ll1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤ໡")))
            if bstack11ll1l1_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࠤ໢") in bstack111lllllll_opy_ or bstack11ll1l1_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢ໣") in bstack111lllllll_opy_:
                bstack1l11llll1_opy_[bstack11ll1l1_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣ໤")] = bstack111lllllll_opy_.get(bstack11ll1l1_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࠧ໥"), bstack111lllllll_opy_.get(bstack11ll1l1_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥ໦")))
            if bstack11ll1l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤ໧") in bstack111lllllll_opy_ or bstack11ll1l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ໨") in bstack111lllllll_opy_:
                bstack1l11llll1_opy_[bstack11ll1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ໩")] = bstack111lllllll_opy_.get(bstack11ll1l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧ໪"), bstack111lllllll_opy_.get(bstack11ll1l1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥ໫")))
            if bstack11ll1l1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ໬") in bstack111lllllll_opy_ or bstack11ll1l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣ໭") in bstack111lllllll_opy_:
                bstack1l11llll1_opy_[bstack11ll1l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ໮")] = bstack111lllllll_opy_.get(bstack11ll1l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠦ໯"), bstack111lllllll_opy_.get(bstack11ll1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦ໰")))
            if bstack11ll1l1_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧ໱") in bstack111lllllll_opy_:
                bstack1l11llll1_opy_[bstack11ll1l1_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨ໲")] = bstack111lllllll_opy_[bstack11ll1l1_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢ໳")]
        except Exception as error:
            logger.error(bstack11ll1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡡࡵࡣ࠽ࠤࠧ໴") +  str(error))
        return bstack1l11llll1_opy_