# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack11ll1l1lll_opy_ = {}
        bstack11l11111ll_opy_ = os.environ.get(bstack111lll_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩ໌"), bstack111lll_opy_ (u"ࠩࠪໍ"))
        if not bstack11l11111ll_opy_:
            return bstack11ll1l1lll_opy_
        try:
            bstack11l1111l11_opy_ = json.loads(bstack11l11111ll_opy_)
            if bstack111lll_opy_ (u"ࠥࡳࡸࠨ໎") in bstack11l1111l11_opy_:
                bstack11ll1l1lll_opy_[bstack111lll_opy_ (u"ࠦࡴࡹࠢ໏")] = bstack11l1111l11_opy_[bstack111lll_opy_ (u"ࠧࡵࡳࠣ໐")]
            if bstack111lll_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥ໑") in bstack11l1111l11_opy_ or bstack111lll_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥ໒") in bstack11l1111l11_opy_:
                bstack11ll1l1lll_opy_[bstack111lll_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦ໓")] = bstack11l1111l11_opy_.get(bstack111lll_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ໔"), bstack11l1111l11_opy_.get(bstack111lll_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨ໕")))
            if bstack111lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧ໖") in bstack11l1111l11_opy_ or bstack111lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥ໗") in bstack11l1111l11_opy_:
                bstack11ll1l1lll_opy_[bstack111lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦ໘")] = bstack11l1111l11_opy_.get(bstack111lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣ໙"), bstack11l1111l11_opy_.get(bstack111lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨ໚")))
            if bstack111lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦ໛") in bstack11l1111l11_opy_ or bstack111lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦໜ") in bstack11l1111l11_opy_:
                bstack11ll1l1lll_opy_[bstack111lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧໝ")] = bstack11l1111l11_opy_.get(bstack111lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢໞ"), bstack11l1111l11_opy_.get(bstack111lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢໟ")))
            if bstack111lll_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࠢ໠") in bstack11l1111l11_opy_ or bstack111lll_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧ໡") in bstack11l1111l11_opy_:
                bstack11ll1l1lll_opy_[bstack111lll_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨ໢")] = bstack11l1111l11_opy_.get(bstack111lll_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࠥ໣"), bstack11l1111l11_opy_.get(bstack111lll_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣ໤")))
            if bstack111lll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢ໥") in bstack11l1111l11_opy_ or bstack111lll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧ໦") in bstack11l1111l11_opy_:
                bstack11ll1l1lll_opy_[bstack111lll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨ໧")] = bstack11l1111l11_opy_.get(bstack111lll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥ໨"), bstack11l1111l11_opy_.get(bstack111lll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ໩")))
            if bstack111lll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ໪") in bstack11l1111l11_opy_ or bstack111lll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨ໫") in bstack11l1111l11_opy_:
                bstack11ll1l1lll_opy_[bstack111lll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢ໬")] = bstack11l1111l11_opy_.get(bstack111lll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ໭"), bstack11l1111l11_opy_.get(bstack111lll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ໮")))
            if bstack111lll_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥ໯") in bstack11l1111l11_opy_:
                bstack11ll1l1lll_opy_[bstack111lll_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦ໰")] = bstack11l1111l11_opy_[bstack111lll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧ໱")]
        except Exception as error:
            logger.error(bstack111lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡦࡺࡡ࠻ࠢࠥ໲") +  str(error))
        return bstack11ll1l1lll_opy_