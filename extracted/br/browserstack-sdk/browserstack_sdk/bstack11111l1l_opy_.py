# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack11lllll1_opy_ = {}
        bstack111llllll1_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪໍ"), bstack11ll11_opy_ (u"ࠪࠫ໎"))
        if not bstack111llllll1_opy_:
            return bstack11lllll1_opy_
        try:
            bstack111lllllll_opy_ = json.loads(bstack111llllll1_opy_)
            if bstack11ll11_opy_ (u"ࠦࡴࡹࠢ໏") in bstack111lllllll_opy_:
                bstack11lllll1_opy_[bstack11ll11_opy_ (u"ࠧࡵࡳࠣ໐")] = bstack111lllllll_opy_[bstack11ll11_opy_ (u"ࠨ࡯ࡴࠤ໑")]
            if bstack11ll11_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦ໒") in bstack111lllllll_opy_ or bstack11ll11_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦ໓") in bstack111lllllll_opy_:
                bstack11lllll1_opy_[bstack11ll11_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧ໔")] = bstack111lllllll_opy_.get(bstack11ll11_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ໕"), bstack111lllllll_opy_.get(bstack11ll11_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢ໖")))
            if bstack11ll11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨ໗") in bstack111lllllll_opy_ or bstack11ll11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦ໘") in bstack111lllllll_opy_:
                bstack11lllll1_opy_[bstack11ll11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧ໙")] = bstack111lllllll_opy_.get(bstack11ll11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤ໚"), bstack111lllllll_opy_.get(bstack11ll11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢ໛")))
            if bstack11ll11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧໜ") in bstack111lllllll_opy_ or bstack11ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧໝ") in bstack111lllllll_opy_:
                bstack11lllll1_opy_[bstack11ll11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨໞ")] = bstack111lllllll_opy_.get(bstack11ll11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣໟ"), bstack111lllllll_opy_.get(bstack11ll11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣ໠")))
            if bstack11ll11_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࠣ໡") in bstack111lllllll_opy_ or bstack11ll11_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨ໢") in bstack111lllllll_opy_:
                bstack11lllll1_opy_[bstack11ll11_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢ໣")] = bstack111lllllll_opy_.get(bstack11ll11_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦ໤"), bstack111lllllll_opy_.get(bstack11ll11_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤ໥")))
            if bstack11ll11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣ໦") in bstack111lllllll_opy_ or bstack11ll11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨ໧") in bstack111lllllll_opy_:
                bstack11lllll1_opy_[bstack11ll11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ໨")] = bstack111lllllll_opy_.get(bstack11ll11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦ໩"), bstack111lllllll_opy_.get(bstack11ll11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤ໪")))
            if bstack11ll11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ໫") in bstack111lllllll_opy_ or bstack11ll11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢ໬") in bstack111lllllll_opy_:
                bstack11lllll1_opy_[bstack11ll11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣ໭")] = bstack111lllllll_opy_.get(bstack11ll11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠥ໮"), bstack111lllllll_opy_.get(bstack11ll11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥ໯")))
            if bstack11ll11_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦ໰") in bstack111lllllll_opy_:
                bstack11lllll1_opy_[bstack11ll11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧ໱")] = bstack111lllllll_opy_[bstack11ll11_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨ໲")]
        except Exception as error:
            logger.error(bstack11ll11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩࡧࡴࡢ࠼ࠣࠦ໳") +  str(error))
        return bstack11lllll1_opy_