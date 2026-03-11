# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack11l1l11111_opy_ = {}
        bstack1111l11111_opy_ = os.environ.get(bstack1ll111_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭࿽"), bstack1ll111_opy_ (u"࠭ࠧ࿾"))
        if not bstack1111l11111_opy_:
            return bstack11l1l11111_opy_
        try:
            bstack1111l1111l_opy_ = json.loads(bstack1111l11111_opy_)
            if bstack1ll111_opy_ (u"ࠢࡰࡵࠥ࿿") in bstack1111l1111l_opy_:
                bstack11l1l11111_opy_[bstack1ll111_opy_ (u"ࠣࡱࡶࠦက")] = bstack1111l1111l_opy_[bstack1ll111_opy_ (u"ࠤࡲࡷࠧခ")]
            if bstack1ll111_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢဂ") in bstack1111l1111l_opy_ or bstack1ll111_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢဃ") in bstack1111l1111l_opy_:
                bstack11l1l11111_opy_[bstack1ll111_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣင")] = bstack1111l1111l_opy_.get(bstack1ll111_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥစ"), bstack1111l1111l_opy_.get(bstack1ll111_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥဆ")))
            if bstack1ll111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤဇ") in bstack1111l1111l_opy_ or bstack1ll111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢဈ") in bstack1111l1111l_opy_:
                bstack11l1l11111_opy_[bstack1ll111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣဉ")] = bstack1111l1111l_opy_.get(bstack1ll111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧည"), bstack1111l1111l_opy_.get(bstack1ll111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥဋ")))
            if bstack1ll111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣဌ") in bstack1111l1111l_opy_ or bstack1ll111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣဍ") in bstack1111l1111l_opy_:
                bstack11l1l11111_opy_[bstack1ll111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤဎ")] = bstack1111l1111l_opy_.get(bstack1ll111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦဏ"), bstack1111l1111l_opy_.get(bstack1ll111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦတ")))
            if bstack1ll111_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦထ") in bstack1111l1111l_opy_ or bstack1ll111_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤဒ") in bstack1111l1111l_opy_:
                bstack11l1l11111_opy_[bstack1ll111_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥဓ")] = bstack1111l1111l_opy_.get(bstack1ll111_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࠢန"), bstack1111l1111l_opy_.get(bstack1ll111_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧပ")))
            if bstack1ll111_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦဖ") in bstack1111l1111l_opy_ or bstack1ll111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤဗ") in bstack1111l1111l_opy_:
                bstack11l1l11111_opy_[bstack1ll111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥဘ")] = bstack1111l1111l_opy_.get(bstack1ll111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢမ"), bstack1111l1111l_opy_.get(bstack1ll111_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧယ")))
            if bstack1ll111_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠥရ") in bstack1111l1111l_opy_ or bstack1ll111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥလ") in bstack1111l1111l_opy_:
                bstack11l1l11111_opy_[bstack1ll111_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦဝ")] = bstack1111l1111l_opy_.get(bstack1ll111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠨသ"), bstack1111l1111l_opy_.get(bstack1ll111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨဟ")))
            if bstack1ll111_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢဠ") in bstack1111l1111l_opy_:
                bstack11l1l11111_opy_[bstack1ll111_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣအ")] = bstack1111l1111l_opy_[bstack1ll111_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤဢ")]
        except Exception as error:
            logger.error(bstack1ll111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡨࡻࡲࡳࡧࡱࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡣࡷࡥ࠿ࠦࠢဣ") +  str(error))
        return bstack11l1l11111_opy_