# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1ll1ll11_opy_ = {}
        bstack111lllll11_opy_ = os.environ.get(bstack11l1_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭༈"), bstack11l1_opy_ (u"࠭ࠧ༉"))
        if not bstack111lllll11_opy_:
            return bstack1ll1ll11_opy_
        try:
            bstack111lllll1l_opy_ = json.loads(bstack111lllll11_opy_)
            if bstack11l1_opy_ (u"ࠢࡰࡵࠥ༊") in bstack111lllll1l_opy_:
                bstack1ll1ll11_opy_[bstack11l1_opy_ (u"ࠣࡱࡶࠦ་")] = bstack111lllll1l_opy_[bstack11l1_opy_ (u"ࠤࡲࡷࠧ༌")]
            if bstack11l1_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ།") in bstack111lllll1l_opy_ or bstack11l1_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢ༎") in bstack111lllll1l_opy_:
                bstack1ll1ll11_opy_[bstack11l1_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣ༏")] = bstack111lllll1l_opy_.get(bstack11l1_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥ༐"), bstack111lllll1l_opy_.get(bstack11l1_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥ༑")))
            if bstack11l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤ༒") in bstack111lllll1l_opy_ or bstack11l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢ༓") in bstack111lllll1l_opy_:
                bstack1ll1ll11_opy_[bstack11l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣ༔")] = bstack111lllll1l_opy_.get(bstack11l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧ༕"), bstack111lllll1l_opy_.get(bstack11l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥ༖")))
            if bstack11l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ༗") in bstack111lllll1l_opy_ or bstack11l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮༘ࠣ") in bstack111lllll1l_opy_:
                bstack1ll1ll11_opy_[bstack11l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤ༙")] = bstack111lllll1l_opy_.get(bstack11l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦ༚"), bstack111lllll1l_opy_.get(bstack11l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦ༛")))
            if bstack11l1_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦ༜") in bstack111lllll1l_opy_ or bstack11l1_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤ༝") in bstack111lllll1l_opy_:
                bstack1ll1ll11_opy_[bstack11l1_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥ༞")] = bstack111lllll1l_opy_.get(bstack11l1_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࠢ༟"), bstack111lllll1l_opy_.get(bstack11l1_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧ༠")))
            if bstack11l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦ༡") in bstack111lllll1l_opy_ or bstack11l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤ༢") in bstack111lllll1l_opy_:
                bstack1ll1ll11_opy_[bstack11l1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥ༣")] = bstack111lllll1l_opy_.get(bstack11l1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢ༤"), bstack111lllll1l_opy_.get(bstack11l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧ༥")))
            if bstack11l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠥ༦") in bstack111lllll1l_opy_ or bstack11l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥ༧") in bstack111lllll1l_opy_:
                bstack1ll1ll11_opy_[bstack11l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦ༨")] = bstack111lllll1l_opy_.get(bstack11l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ༩"), bstack111lllll1l_opy_.get(bstack11l1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨ༪")))
            if bstack11l1_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢ༫") in bstack111lllll1l_opy_:
                bstack1ll1ll11_opy_[bstack11l1_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣ༬")] = bstack111lllll1l_opy_[bstack11l1_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤ༭")]
        except Exception as error:
            logger.error(bstack11l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡨࡻࡲࡳࡧࡱࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡣࡷࡥ࠿ࠦࠢ༮") +  str(error))
        return bstack1ll1ll11_opy_