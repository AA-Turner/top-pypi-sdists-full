# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack11l111l1_opy_ = {}
        bstack111llll1l1_opy_ = os.environ.get(bstackl_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭༈"), bstackl_opy_ (u"࠭ࠧ༉"))
        if not bstack111llll1l1_opy_:
            return bstack11l111l1_opy_
        try:
            bstack111llll1ll_opy_ = json.loads(bstack111llll1l1_opy_)
            if bstackl_opy_ (u"ࠢࡰࡵࠥ༊") in bstack111llll1ll_opy_:
                bstack11l111l1_opy_[bstackl_opy_ (u"ࠣࡱࡶࠦ་")] = bstack111llll1ll_opy_[bstackl_opy_ (u"ࠤࡲࡷࠧ༌")]
            if bstackl_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ།") in bstack111llll1ll_opy_ or bstackl_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢ༎") in bstack111llll1ll_opy_:
                bstack11l111l1_opy_[bstackl_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣ༏")] = bstack111llll1ll_opy_.get(bstackl_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥ༐"), bstack111llll1ll_opy_.get(bstackl_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥ༑")))
            if bstackl_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤ༒") in bstack111llll1ll_opy_ or bstackl_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢ༓") in bstack111llll1ll_opy_:
                bstack11l111l1_opy_[bstackl_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣ༔")] = bstack111llll1ll_opy_.get(bstackl_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧ༕"), bstack111llll1ll_opy_.get(bstackl_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥ༖")))
            if bstackl_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ༗") in bstack111llll1ll_opy_ or bstackl_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮༘ࠣ") in bstack111llll1ll_opy_:
                bstack11l111l1_opy_[bstackl_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤ༙")] = bstack111llll1ll_opy_.get(bstackl_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦ༚"), bstack111llll1ll_opy_.get(bstackl_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦ༛")))
            if bstackl_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦ༜") in bstack111llll1ll_opy_ or bstackl_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤ༝") in bstack111llll1ll_opy_:
                bstack11l111l1_opy_[bstackl_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥ༞")] = bstack111llll1ll_opy_.get(bstackl_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࠢ༟"), bstack111llll1ll_opy_.get(bstackl_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧ༠")))
            if bstackl_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦ༡") in bstack111llll1ll_opy_ or bstackl_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤ༢") in bstack111llll1ll_opy_:
                bstack11l111l1_opy_[bstackl_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥ༣")] = bstack111llll1ll_opy_.get(bstackl_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢ༤"), bstack111llll1ll_opy_.get(bstackl_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧ༥")))
            if bstackl_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠥ༦") in bstack111llll1ll_opy_ or bstackl_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥ༧") in bstack111llll1ll_opy_:
                bstack11l111l1_opy_[bstackl_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦ༨")] = bstack111llll1ll_opy_.get(bstackl_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ༩"), bstack111llll1ll_opy_.get(bstackl_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨ༪")))
            if bstackl_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢ༫") in bstack111llll1ll_opy_:
                bstack11l111l1_opy_[bstackl_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣ༬")] = bstack111llll1ll_opy_[bstackl_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤ༭")]
        except Exception as error:
            logger.error(bstackl_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡨࡻࡲࡳࡧࡱࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡣࡷࡥ࠿ࠦࠢ༮") +  str(error))
        return bstack11l111l1_opy_