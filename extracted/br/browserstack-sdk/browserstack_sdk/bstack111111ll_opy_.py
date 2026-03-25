# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1ll111ll_opy_ = {}
        bstack1111111111_opy_ = os.environ.get(bstack1l1_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬၞ"), bstack1l1_opy_ (u"ࠬ࠭ၟ"))
        if not bstack1111111111_opy_:
            return bstack1ll111ll_opy_
        try:
            bstack111111111l_opy_ = json.loads(bstack1111111111_opy_)
            if bstack1l1_opy_ (u"ࠨ࡯ࡴࠤၠ") in bstack111111111l_opy_:
                bstack1ll111ll_opy_[bstack1l1_opy_ (u"ࠢࡰࡵࠥၡ")] = bstack111111111l_opy_[bstack1l1_opy_ (u"ࠣࡱࡶࠦၢ")]
            if bstack1l1_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨၣ") in bstack111111111l_opy_ or bstack1l1_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨၤ") in bstack111111111l_opy_:
                bstack1ll111ll_opy_[bstack1l1_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢၥ")] = bstack111111111l_opy_.get(bstack1l1_opy_ (u"ࠧࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠤၦ"), bstack111111111l_opy_.get(bstack1l1_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤၧ")))
            if bstack1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣၨ") in bstack111111111l_opy_ or bstack1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨၩ") in bstack111111111l_opy_:
                bstack1ll111ll_opy_[bstack1l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢၪ")] = bstack111111111l_opy_.get(bstack1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦၫ"), bstack111111111l_opy_.get(bstack1l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤၬ")))
            if bstack1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢၭ") in bstack111111111l_opy_ or bstack1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢၮ") in bstack111111111l_opy_:
                bstack1ll111ll_opy_[bstack1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣၯ")] = bstack111111111l_opy_.get(bstack1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠥၰ"), bstack111111111l_opy_.get(bstack1l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥၱ")))
            if bstack1l1_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࠥၲ") in bstack111111111l_opy_ or bstack1l1_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣၳ") in bstack111111111l_opy_:
                bstack1ll111ll_opy_[bstack1l1_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤၴ")] = bstack111111111l_opy_.get(bstack1l1_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࠨၵ"), bstack111111111l_opy_.get(bstack1l1_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠦၶ")))
            if bstack1l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥၷ") in bstack111111111l_opy_ or bstack1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣၸ") in bstack111111111l_opy_:
                bstack1ll111ll_opy_[bstack1l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤၹ")] = bstack111111111l_opy_.get(bstack1l1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨၺ"), bstack111111111l_opy_.get(bstack1l1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦၻ")))
            if bstack1l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤၼ") in bstack111111111l_opy_ or bstack1l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤၽ") in bstack111111111l_opy_:
                bstack1ll111ll_opy_[bstack1l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥၾ")] = bstack111111111l_opy_.get(bstack1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧၿ"), bstack111111111l_opy_.get(bstack1l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧႀ")))
            if bstack1l1_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨႁ") in bstack111111111l_opy_:
                bstack1ll111ll_opy_[bstack1l1_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢႂ")] = bstack111111111l_opy_[bstack1l1_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣႃ")]
        except Exception as error:
            logger.error(bstack1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡧࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡢࡶࡤ࠾ࠥࠨႄ") +  str(error))
        return bstack1ll111ll_opy_