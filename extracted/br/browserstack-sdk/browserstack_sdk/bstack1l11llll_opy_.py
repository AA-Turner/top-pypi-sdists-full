# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack1lll1l_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1l1_opy_ (bstack1lll_opy_):
    global bstack111l1l_opy_
    bstack1l11lll_opy_ = ord (bstack1lll_opy_ [-1])
    bstack1l11ll1_opy_ = bstack1lll_opy_ [:-1]
    bstack11llll1_opy_ = bstack1l11lll_opy_ % len (bstack1l11ll1_opy_)
    bstack1l1ll11_opy_ = bstack1l11ll1_opy_ [:bstack11llll1_opy_] + bstack1l11ll1_opy_ [bstack11llll1_opy_:]
    if bstack1111l11_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    return eval (bstack11l1ll_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack11lllll11_opy_ = {}
        bstack111llll1ll_opy_ = os.environ.get(bstack1l1_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ༅"), bstack1l1_opy_ (u"ࠪࠫ༆"))
        if not bstack111llll1ll_opy_:
            return bstack11lllll11_opy_
        try:
            bstack111llll1l1_opy_ = json.loads(bstack111llll1ll_opy_)
            if bstack1l1_opy_ (u"ࠦࡴࡹࠢ༇") in bstack111llll1l1_opy_:
                bstack11lllll11_opy_[bstack1l1_opy_ (u"ࠧࡵࡳࠣ༈")] = bstack111llll1l1_opy_[bstack1l1_opy_ (u"ࠨ࡯ࡴࠤ༉")]
            if bstack1l1_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦ༊") in bstack111llll1l1_opy_ or bstack1l1_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦ་") in bstack111llll1l1_opy_:
                bstack11lllll11_opy_[bstack1l1_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧ༌")] = bstack111llll1l1_opy_.get(bstack1l1_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ།"), bstack111llll1l1_opy_.get(bstack1l1_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢ༎")))
            if bstack1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨ༏") in bstack111llll1l1_opy_ or bstack1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦ༐") in bstack111llll1l1_opy_:
                bstack11lllll11_opy_[bstack1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧ༑")] = bstack111llll1l1_opy_.get(bstack1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤ༒"), bstack111llll1l1_opy_.get(bstack1l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢ༓")))
            if bstack1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ༔") in bstack111llll1l1_opy_ or bstack1l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧ༕") in bstack111llll1l1_opy_:
                bstack11lllll11_opy_[bstack1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨ༖")] = bstack111llll1l1_opy_.get(bstack1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ༗"), bstack111llll1l1_opy_.get(bstack1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮༘ࠣ")))
            if bstack1l1_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥ༙ࠣ") in bstack111llll1l1_opy_ or bstack1l1_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨ༚") in bstack111llll1l1_opy_:
                bstack11lllll11_opy_[bstack1l1_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢ༛")] = bstack111llll1l1_opy_.get(bstack1l1_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦ༜"), bstack111llll1l1_opy_.get(bstack1l1_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤ༝")))
            if bstack1l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣ༞") in bstack111llll1l1_opy_ or bstack1l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨ༟") in bstack111llll1l1_opy_:
                bstack11lllll11_opy_[bstack1l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ༠")] = bstack111llll1l1_opy_.get(bstack1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦ༡"), bstack111llll1l1_opy_.get(bstack1l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤ༢")))
            if bstack1l1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ༣") in bstack111llll1l1_opy_ or bstack1l1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢ༤") in bstack111llll1l1_opy_:
                bstack11lllll11_opy_[bstack1l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣ༥")] = bstack111llll1l1_opy_.get(bstack1l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠥ༦"), bstack111llll1l1_opy_.get(bstack1l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥ༧")))
            if bstack1l1_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦ༨") in bstack111llll1l1_opy_:
                bstack11lllll11_opy_[bstack1l1_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧ༩")] = bstack111llll1l1_opy_[bstack1l1_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨ༪")]
        except Exception as error:
            logger.error(bstack1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩࡧࡴࡢ࠼ࠣࠦ༫") +  str(error))
        return bstack11lllll11_opy_