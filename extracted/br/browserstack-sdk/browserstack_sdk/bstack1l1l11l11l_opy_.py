# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack11ll1l111_opy_ = {}
        bstack111lllllll_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫ໎"), bstack1l1l1l1_opy_ (u"ࠫࠬ໏"))
        if not bstack111lllllll_opy_:
            return bstack11ll1l111_opy_
        try:
            bstack111llllll1_opy_ = json.loads(bstack111lllllll_opy_)
            if bstack1l1l1l1_opy_ (u"ࠧࡵࡳࠣ໐") in bstack111llllll1_opy_:
                bstack11ll1l111_opy_[bstack1l1l1l1_opy_ (u"ࠨ࡯ࡴࠤ໑")] = bstack111llllll1_opy_[bstack1l1l1l1_opy_ (u"ࠢࡰࡵࠥ໒")]
            if bstack1l1l1l1_opy_ (u"ࠣࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ໓") in bstack111llllll1_opy_ or bstack1l1l1l1_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧ໔") in bstack111llllll1_opy_:
                bstack11ll1l111_opy_[bstack1l1l1l1_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨ໕")] = bstack111llllll1_opy_.get(bstack1l1l1l1_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ໖"), bstack111llllll1_opy_.get(bstack1l1l1l1_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣ໗")))
            if bstack1l1l1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࠢ໘") in bstack111llllll1_opy_ or bstack1l1l1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧ໙") in bstack111llllll1_opy_:
                bstack11ll1l111_opy_[bstack1l1l1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨ໚")] = bstack111llllll1_opy_.get(bstack1l1l1l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥ໛"), bstack111llllll1_opy_.get(bstack1l1l1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣໜ")))
            if bstack1l1l1l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࠨໝ") in bstack111llllll1_opy_ or bstack1l1l1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨໞ") in bstack111llllll1_opy_:
                bstack11ll1l111_opy_[bstack1l1l1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢໟ")] = bstack111llllll1_opy_.get(bstack1l1l1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ໠"), bstack111llllll1_opy_.get(bstack1l1l1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤ໡")))
            if bstack1l1l1l1_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࠤ໢") in bstack111llllll1_opy_ or bstack1l1l1l1_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢ໣") in bstack111llllll1_opy_:
                bstack11ll1l111_opy_[bstack1l1l1l1_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣ໤")] = bstack111llllll1_opy_.get(bstack1l1l1l1_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࠧ໥"), bstack111llllll1_opy_.get(bstack1l1l1l1_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥ໦")))
            if bstack1l1l1l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤ໧") in bstack111llllll1_opy_ or bstack1l1l1l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ໨") in bstack111llllll1_opy_:
                bstack11ll1l111_opy_[bstack1l1l1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ໩")] = bstack111llllll1_opy_.get(bstack1l1l1l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧ໪"), bstack111llllll1_opy_.get(bstack1l1l1l1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥ໫")))
            if bstack1l1l1l1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ໬") in bstack111llllll1_opy_ or bstack1l1l1l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣ໭") in bstack111llllll1_opy_:
                bstack11ll1l111_opy_[bstack1l1l1l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ໮")] = bstack111llllll1_opy_.get(bstack1l1l1l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠦ໯"), bstack111llllll1_opy_.get(bstack1l1l1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦ໰")))
            if bstack1l1l1l1_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧ໱") in bstack111llllll1_opy_:
                bstack11ll1l111_opy_[bstack1l1l1l1_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨ໲")] = bstack111llllll1_opy_[bstack1l1l1l1_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢ໳")]
        except Exception as error:
            logger.error(bstack1l1l1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡡࡵࡣ࠽ࠤࠧ໴") +  str(error))
        return bstack11ll1l111_opy_