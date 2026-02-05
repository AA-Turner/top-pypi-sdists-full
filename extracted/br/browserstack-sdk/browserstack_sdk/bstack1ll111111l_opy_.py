# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1ll1ll1ll_opy_ = {}
        bstack111l111l1l_opy_ = os.environ.get(bstack11l1ll1_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬཀྵ"), bstack11l1ll1_opy_ (u"ࠬ࠭ཪ"))
        if not bstack111l111l1l_opy_:
            return bstack1ll1ll1ll_opy_
        try:
            bstack111l111l11_opy_ = json.loads(bstack111l111l1l_opy_)
            if bstack11l1ll1_opy_ (u"ࠨ࡯ࡴࠤཫ") in bstack111l111l11_opy_:
                bstack1ll1ll1ll_opy_[bstack11l1ll1_opy_ (u"ࠢࡰࡵࠥཬ")] = bstack111l111l11_opy_[bstack11l1ll1_opy_ (u"ࠣࡱࡶࠦ཭")]
            if bstack11l1ll1_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ཮") in bstack111l111l11_opy_ or bstack11l1ll1_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨ཯") in bstack111l111l11_opy_:
                bstack1ll1ll1ll_opy_[bstack11l1ll1_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢ཰")] = bstack111l111l11_opy_.get(bstack11l1ll1_opy_ (u"ࠧࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠤཱ"), bstack111l111l11_opy_.get(bstack11l1ll1_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤི")))
            if bstack11l1ll1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲཱིࠣ") in bstack111l111l11_opy_ or bstack11l1ll1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨུ") in bstack111l111l11_opy_:
                bstack1ll1ll1ll_opy_[bstack11l1ll1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ཱུࠢ")] = bstack111l111l11_opy_.get(bstack11l1ll1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦྲྀ"), bstack111l111l11_opy_.get(bstack11l1ll1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤཷ")))
            if bstack11l1ll1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢླྀ") in bstack111l111l11_opy_ or bstack11l1ll1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢཹ") in bstack111l111l11_opy_:
                bstack1ll1ll1ll_opy_[bstack11l1ll1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ེࠣ")] = bstack111l111l11_opy_.get(bstack11l1ll1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰཻࠥ"), bstack111l111l11_opy_.get(bstack11l1ll1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰོࠥ")))
            if bstack11l1ll1_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧཽࠥ") in bstack111l111l11_opy_ or bstack11l1ll1_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣཾ") in bstack111l111l11_opy_:
                bstack1ll1ll1ll_opy_[bstack11l1ll1_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤཿ")] = bstack111l111l11_opy_.get(bstack11l1ll1_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࠨྀ"), bstack111l111l11_opy_.get(bstack11l1ll1_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨཱྀࠦ")))
            if bstack11l1ll1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥྂ") in bstack111l111l11_opy_ or bstack11l1ll1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣྃ") in bstack111l111l11_opy_:
                bstack1ll1ll1ll_opy_[bstack11l1ll1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤ྄")] = bstack111l111l11_opy_.get(bstack11l1ll1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨ྅"), bstack111l111l11_opy_.get(bstack11l1ll1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦ྆")))
            if bstack11l1ll1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ྇") in bstack111l111l11_opy_ or bstack11l1ll1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤྈ") in bstack111l111l11_opy_:
                bstack1ll1ll1ll_opy_[bstack11l1ll1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥྉ")] = bstack111l111l11_opy_.get(bstack11l1ll1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧྊ"), bstack111l111l11_opy_.get(bstack11l1ll1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧྋ")))
            if bstack11l1ll1_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨྌ") in bstack111l111l11_opy_:
                bstack1ll1ll1ll_opy_[bstack11l1ll1_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢྍ")] = bstack111l111l11_opy_[bstack11l1ll1_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣྎ")]
        except Exception as error:
            logger.error(bstack11l1ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡧࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡢࡶࡤ࠾ࠥࠨྏ") +  str(error))
        return bstack1ll1ll1ll_opy_