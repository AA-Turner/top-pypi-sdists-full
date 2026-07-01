# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1ll11ll1_opy_ = {}
        bstack1ll11l1l_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪࢦ"), bstack1l1llll_opy_ (u"ࠪࠫࢧ"))
        if not bstack1ll11l1l_opy_:
            return bstack1ll11ll1_opy_
        try:
            bstack1ll1l111_opy_ = json.loads(bstack1ll11l1l_opy_)
            if bstack1l1llll_opy_ (u"ࠦࡴࡹࠢࢨ") in bstack1ll1l111_opy_:
                bstack1ll11ll1_opy_[bstack1l1llll_opy_ (u"ࠧࡵࡳࠣࢩ")] = bstack1ll1l111_opy_[bstack1l1llll_opy_ (u"ࠨ࡯ࡴࠤࢪ")]
            if bstack1l1llll_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦࢫ") in bstack1ll1l111_opy_ or bstack1l1llll_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦࢬ") in bstack1ll1l111_opy_:
                bstack1ll11ll1_opy_[bstack1l1llll_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧࢭ")] = bstack1ll1l111_opy_.get(bstack1l1llll_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢࢮ"), bstack1ll1l111_opy_.get(bstack1l1llll_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢࢯ")))
            if bstack1l1llll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨࢰ") in bstack1ll1l111_opy_ or bstack1l1llll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦࢱ") in bstack1ll1l111_opy_:
                bstack1ll11ll1_opy_[bstack1l1llll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧࢲ")] = bstack1ll1l111_opy_.get(bstack1l1llll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤࢳ"), bstack1ll1l111_opy_.get(bstack1l1llll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢࢴ")))
            if bstack1l1llll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧࢵ") in bstack1ll1l111_opy_ or bstack1l1llll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧࢶ") in bstack1ll1l111_opy_:
                bstack1ll11ll1_opy_[bstack1l1llll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨࢷ")] = bstack1ll1l111_opy_.get(bstack1l1llll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣࢸ"), bstack1ll1l111_opy_.get(bstack1l1llll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣࢹ")))
            if bstack1l1llll_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࠣࢺ") in bstack1ll1l111_opy_ or bstack1l1llll_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨࢻ") in bstack1ll1l111_opy_:
                bstack1ll11ll1_opy_[bstack1l1llll_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢࢼ")] = bstack1ll1l111_opy_.get(bstack1l1llll_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦࢽ"), bstack1ll1l111_opy_.get(bstack1l1llll_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤࢾ")))
            if bstack1l1llll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣࢿ") in bstack1ll1l111_opy_ or bstack1l1llll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨࣀ") in bstack1ll1l111_opy_:
                bstack1ll11ll1_opy_[bstack1l1llll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢࣁ")] = bstack1ll1l111_opy_.get(bstack1l1llll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦࣂ"), bstack1ll1l111_opy_.get(bstack1l1llll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤࣃ")))
            if bstack1l1llll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢࣄ") in bstack1ll1l111_opy_ or bstack1l1llll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢࣅ") in bstack1ll1l111_opy_:
                bstack1ll11ll1_opy_[bstack1l1llll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣࣆ")] = bstack1ll1l111_opy_.get(bstack1l1llll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠥࣇ"), bstack1ll1l111_opy_.get(bstack1l1llll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥࣈ")))
            if bstack1l1llll_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦࣉ") in bstack1ll1l111_opy_:
                bstack1ll11ll1_opy_[bstack1l1llll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧ࣊")] = bstack1ll1l111_opy_[bstack1l1llll_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨ࣋")]
        except Exception as error:
            logger.error(bstack1l1llll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩࡧࡴࡢ࠼ࠣࠦ࣌") +  str(error))
        return bstack1ll11ll1_opy_