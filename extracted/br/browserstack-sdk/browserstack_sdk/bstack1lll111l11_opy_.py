# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack11l11l11l_opy_ = {}
        bstack11l1111111_opy_ = os.environ.get(bstack1l1ll1_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫ໎"), bstack1l1ll1_opy_ (u"ࠫࠬ໏"))
        if not bstack11l1111111_opy_:
            return bstack11l11l11l_opy_
        try:
            bstack111lllllll_opy_ = json.loads(bstack11l1111111_opy_)
            if bstack1l1ll1_opy_ (u"ࠧࡵࡳࠣ໐") in bstack111lllllll_opy_:
                bstack11l11l11l_opy_[bstack1l1ll1_opy_ (u"ࠨ࡯ࡴࠤ໑")] = bstack111lllllll_opy_[bstack1l1ll1_opy_ (u"ࠢࡰࡵࠥ໒")]
            if bstack1l1ll1_opy_ (u"ࠣࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ໓") in bstack111lllllll_opy_ or bstack1l1ll1_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧ໔") in bstack111lllllll_opy_:
                bstack11l11l11l_opy_[bstack1l1ll1_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨ໕")] = bstack111lllllll_opy_.get(bstack1l1ll1_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ໖"), bstack111lllllll_opy_.get(bstack1l1ll1_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣ໗")))
            if bstack1l1ll1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࠢ໘") in bstack111lllllll_opy_ or bstack1l1ll1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧ໙") in bstack111lllllll_opy_:
                bstack11l11l11l_opy_[bstack1l1ll1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨ໚")] = bstack111lllllll_opy_.get(bstack1l1ll1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥ໛"), bstack111lllllll_opy_.get(bstack1l1ll1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣໜ")))
            if bstack1l1ll1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࠨໝ") in bstack111lllllll_opy_ or bstack1l1ll1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨໞ") in bstack111lllllll_opy_:
                bstack11l11l11l_opy_[bstack1l1ll1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢໟ")] = bstack111lllllll_opy_.get(bstack1l1ll1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ໠"), bstack111lllllll_opy_.get(bstack1l1ll1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤ໡")))
            if bstack1l1ll1_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࠤ໢") in bstack111lllllll_opy_ or bstack1l1ll1_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢ໣") in bstack111lllllll_opy_:
                bstack11l11l11l_opy_[bstack1l1ll1_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣ໤")] = bstack111lllllll_opy_.get(bstack1l1ll1_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࠧ໥"), bstack111lllllll_opy_.get(bstack1l1ll1_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥ໦")))
            if bstack1l1ll1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤ໧") in bstack111lllllll_opy_ or bstack1l1ll1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ໨") in bstack111lllllll_opy_:
                bstack11l11l11l_opy_[bstack1l1ll1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ໩")] = bstack111lllllll_opy_.get(bstack1l1ll1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧ໪"), bstack111lllllll_opy_.get(bstack1l1ll1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥ໫")))
            if bstack1l1ll1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ໬") in bstack111lllllll_opy_ or bstack1l1ll1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣ໭") in bstack111lllllll_opy_:
                bstack11l11l11l_opy_[bstack1l1ll1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ໮")] = bstack111lllllll_opy_.get(bstack1l1ll1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠦ໯"), bstack111lllllll_opy_.get(bstack1l1ll1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦ໰")))
            if bstack1l1ll1_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧ໱") in bstack111lllllll_opy_:
                bstack11l11l11l_opy_[bstack1l1ll1_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨ໲")] = bstack111lllllll_opy_[bstack1l1ll1_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢ໳")]
        except Exception as error:
            logger.error(bstack1l1ll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡡࡵࡣ࠽ࠤࠧ໴") +  str(error))
        return bstack11l11l11l_opy_