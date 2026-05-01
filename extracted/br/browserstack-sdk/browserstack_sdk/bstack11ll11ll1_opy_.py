# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack11llllllll_opy_ = {}
        bstack1llll1l1l1l_opy_ = os.environ.get(bstack111ll_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫႿ"), bstack111ll_opy_ (u"ࠫࠬჀ"))
        if not bstack1llll1l1l1l_opy_:
            return bstack11llllllll_opy_
        try:
            bstack1llll1l1l11_opy_ = json.loads(bstack1llll1l1l1l_opy_)
            if bstack111ll_opy_ (u"ࠧࡵࡳࠣჁ") in bstack1llll1l1l11_opy_:
                bstack11llllllll_opy_[bstack111ll_opy_ (u"ࠨ࡯ࡴࠤჂ")] = bstack1llll1l1l11_opy_[bstack111ll_opy_ (u"ࠢࡰࡵࠥჃ")]
            if bstack111ll_opy_ (u"ࠣࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧჄ") in bstack1llll1l1l11_opy_ or bstack111ll_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧჅ") in bstack1llll1l1l11_opy_:
                bstack11llllllll_opy_[bstack111ll_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨ჆")] = bstack1llll1l1l11_opy_.get(bstack111ll_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣჇ"), bstack1llll1l1l11_opy_.get(bstack111ll_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣ჈")))
            if bstack111ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࠢ჉") in bstack1llll1l1l11_opy_ or bstack111ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧ჊") in bstack1llll1l1l11_opy_:
                bstack11llllllll_opy_[bstack111ll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨ჋")] = bstack1llll1l1l11_opy_.get(bstack111ll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥ჌"), bstack1llll1l1l11_opy_.get(bstack111ll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣჍ")))
            if bstack111ll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ჎") in bstack1llll1l1l11_opy_ or bstack111ll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨ჏") in bstack1llll1l1l11_opy_:
                bstack11llllllll_opy_[bstack111ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢა")] = bstack1llll1l1l11_opy_.get(bstack111ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤბ"), bstack1llll1l1l11_opy_.get(bstack111ll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤგ")))
            if bstack111ll_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࠤდ") in bstack1llll1l1l11_opy_ or bstack111ll_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢე") in bstack1llll1l1l11_opy_:
                bstack11llllllll_opy_[bstack111ll_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣვ")] = bstack1llll1l1l11_opy_.get(bstack111ll_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࠧზ"), bstack1llll1l1l11_opy_.get(bstack111ll_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥთ")))
            if bstack111ll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤი") in bstack1llll1l1l11_opy_ or bstack111ll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢკ") in bstack1llll1l1l11_opy_:
                bstack11llllllll_opy_[bstack111ll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣლ")] = bstack1llll1l1l11_opy_.get(bstack111ll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧმ"), bstack1llll1l1l11_opy_.get(bstack111ll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥნ")))
            if bstack111ll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣო") in bstack1llll1l1l11_opy_ or bstack111ll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣპ") in bstack1llll1l1l11_opy_:
                bstack11llllllll_opy_[bstack111ll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤჟ")] = bstack1llll1l1l11_opy_.get(bstack111ll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠦრ"), bstack1llll1l1l11_opy_.get(bstack111ll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦს")))
            if bstack111ll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧტ") in bstack1llll1l1l11_opy_:
                bstack11llllllll_opy_[bstack111ll_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨუ")] = bstack1llll1l1l11_opy_[bstack111ll_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢფ")]
        except Exception as error:
            logger.error(bstack111ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡡࡵࡣ࠽ࠤࠧქ") +  str(error))
        return bstack11llllllll_opy_