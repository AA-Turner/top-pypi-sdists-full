# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1l11l1ll_opy_ = {}
        bstack111l111l1l_opy_ = os.environ.get(bstack1l1111_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧཤ"), bstack1l1111_opy_ (u"ࠧࠨཥ"))
        if not bstack111l111l1l_opy_:
            return bstack1l11l1ll_opy_
        try:
            bstack111l111ll1_opy_ = json.loads(bstack111l111l1l_opy_)
            if bstack1l1111_opy_ (u"ࠣࡱࡶࠦས") in bstack111l111ll1_opy_:
                bstack1l11l1ll_opy_[bstack1l1111_opy_ (u"ࠤࡲࡷࠧཧ")] = bstack111l111ll1_opy_[bstack1l1111_opy_ (u"ࠥࡳࡸࠨཨ")]
            if bstack1l1111_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣཀྵ") in bstack111l111ll1_opy_ or bstack1l1111_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣཪ") in bstack111l111ll1_opy_:
                bstack1l11l1ll_opy_[bstack1l1111_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤཫ")] = bstack111l111ll1_opy_.get(bstack1l1111_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦཬ"), bstack111l111ll1_opy_.get(bstack1l1111_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦ཭")))
            if bstack1l1111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥ཮") in bstack111l111ll1_opy_ or bstack1l1111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣ཯") in bstack111l111ll1_opy_:
                bstack1l11l1ll_opy_[bstack1l1111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤ཰")] = bstack111l111ll1_opy_.get(bstack1l1111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨཱ"), bstack111l111ll1_opy_.get(bstack1l1111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨིࠦ")))
            if bstack1l1111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤཱི") in bstack111l111ll1_opy_ or bstack1l1111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤུ") in bstack111l111ll1_opy_:
                bstack1l11l1ll_opy_[bstack1l1111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰཱུࠥ")] = bstack111l111ll1_opy_.get(bstack1l1111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧྲྀ"), bstack111l111ll1_opy_.get(bstack1l1111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧཷ")))
            if bstack1l1111_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࠧླྀ") in bstack111l111ll1_opy_ or bstack1l1111_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥཹ") in bstack111l111ll1_opy_:
                bstack1l11l1ll_opy_[bstack1l1111_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨེࠦ")] = bstack111l111ll1_opy_.get(bstack1l1111_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥཻࠣ"), bstack111l111ll1_opy_.get(bstack1l1111_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨོ")))
            if bstack1l1111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱཽࠧ") in bstack111l111ll1_opy_ or bstack1l1111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥཾ") in bstack111l111ll1_opy_:
                bstack1l11l1ll_opy_[bstack1l1111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦཿ")] = bstack111l111ll1_opy_.get(bstack1l1111_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ྀࠣ"), bstack111l111ll1_opy_.get(bstack1l1111_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨཱྀ")))
            if bstack1l1111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠦྂ") in bstack111l111ll1_opy_ or bstack1l1111_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦྃ") in bstack111l111ll1_opy_:
                bstack1l11l1ll_opy_[bstack1l1111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲ྄ࠧ")] = bstack111l111ll1_opy_.get(bstack1l1111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ྅"), bstack111l111ll1_opy_.get(bstack1l1111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢ྆")))
            if bstack1l1111_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣ྇") in bstack111l111ll1_opy_:
                bstack1l11l1ll_opy_[bstack1l1111_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤྈ")] = bstack111l111ll1_opy_[bstack1l1111_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥྉ")]
        except Exception as error:
            logger.error(bstack1l1111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡩࡵࡳࡴࡨࡲࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡤࡸࡦࡀࠠࠣྊ") +  str(error))
        return bstack1l11l1ll_opy_