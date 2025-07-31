# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
import os
import time
from bstack_utils.bstack11ll111l1ll_opy_ import bstack11ll11l111l_opy_
from bstack_utils.constants import bstack11l1lllllll_opy_
from bstack_utils.helper import get_host_info, bstack11l1111lll1_opy_
class bstack111l11llll1_opy_:
    bstack1l11l11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡊࡤࡲࡩࡲࡥࡴࠢࡷࡩࡸࡺࠠࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡷࡪࡸࡶࡦࡴ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ⁚")
    def __init__(self, config, logger):
        bstack1l11l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡥ࡫ࡦࡸ࠱ࠦࡴࡦࡵࡷࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡨࡵ࡮ࡧ࡫ࡪࠎࠥࠦࠠࠡࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡤࡹࡴࡳࡣࡷࡩ࡬ࡿ࠺ࠡࡵࡷࡶ࠱ࠦࡴࡦࡵࡷࠤࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡳࡵࡴࡤࡸࡪ࡭ࡹࠡࡰࡤࡱࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ⁛")
        self.config = config
        self.logger = logger
        self.bstack1lllll1l1111_opy_ = bstack1l11l11_opy_ (u"ࠥࡸࡪࡹࡴࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡲ࡯࡭ࡹ࠳ࡴࡦࡵࡷࡷࠧ⁜")
        self.bstack1lllll11ll11_opy_ = None
        self.bstack1lllll1l111l_opy_ = 60
        self.bstack1lllll1l11l1_opy_ = 5
        self.bstack1lllll11lll1_opy_ = 0
    def bstack111l11l1lll_opy_(self, test_files, orchestration_strategy, bstack111l11lll11_opy_={}):
        bstack1l11l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡋࡱ࡭ࡹ࡯ࡡࡵࡧࡶࠤࡹ࡮ࡥࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡲࡦࡳࡸࡩࡸࡺࠠࡢࡰࡧࠤࡸࡺ࡯ࡳࡧࡶࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡶ࡯࡭࡮࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⁝")
        self.logger.debug(bstack1l11l11_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡎࡴࡩࡵ࡫ࡤࡸ࡮ࡴࡧࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡷࡪࡶ࡫ࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࡀࠠࡼࡿࠥ⁞").format(orchestration_strategy))
        try:
            payload = {
                bstack1l11l11_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧ "): [{bstack1l11l11_opy_ (u"ࠢࡧ࡫࡯ࡩࡕࡧࡴࡩࠤ⁠"): f} for f in test_files],
                bstack1l11l11_opy_ (u"ࠣࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡔࡶࡵࡥࡹ࡫ࡧࡺࠤ⁡"): orchestration_strategy,
                bstack1l11l11_opy_ (u"ࠤࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡏࡨࡸࡦࡪࡡࡵࡣࠥ⁢"): bstack111l11lll11_opy_,
                bstack1l11l11_opy_ (u"ࠥࡲࡴࡪࡥࡊࡰࡧࡩࡽࠨ⁣"): int(os.environ.get(bstack1l11l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡋࡑࡈࡊ࡞ࠢ⁤")) or bstack1l11l11_opy_ (u"ࠧ࠶ࠢ⁥")),
                bstack1l11l11_opy_ (u"ࠨࡴࡰࡶࡤࡰࡓࡵࡤࡦࡵࠥ⁦"): int(os.environ.get(bstack1l11l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡐࡖࡄࡐࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤ⁧")) or bstack1l11l11_opy_ (u"ࠣ࠳ࠥ⁨")),
                bstack1l11l11_opy_ (u"ࠤࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠢ⁩"): self.config.get(bstack1l11l11_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ⁪"), bstack1l11l11_opy_ (u"ࠫࠬ⁫")),
                bstack1l11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠣ⁬"): self.config.get(bstack1l11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ⁭"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1l11l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧ⁮"): os.environ.get(bstack1l11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ⁯"), None),
                bstack1l11l11_opy_ (u"ࠤ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠦ⁰"): get_host_info(),
                bstack1l11l11_opy_ (u"ࠥࡴࡷࡊࡥࡵࡣ࡬ࡰࡸࠨⁱ"): bstack11l1111lll1_opy_()
            }
            self.logger.debug(bstack1l11l11_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡗࡪࡴࡤࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳ࠻ࠢࡾࢁࠧ⁲").format(payload))
            response = bstack11ll11l111l_opy_.bstack1lllllll1l11_opy_(self.bstack1lllll1l1111_opy_, payload)
            if response:
                self.bstack1lllll11ll11_opy_ = self._1lllll11l11l_opy_(response)
                self.logger.debug(bstack1l11l11_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡘࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣ⁳").format(self.bstack1lllll11ll11_opy_))
            else:
                self.logger.error(bstack1l11l11_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡩࡨࡸࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠳ࠨ⁴"))
        except Exception as e:
            self.logger.error(bstack1l11l11_opy_ (u"ࠢ࡜ࡵࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵ࠽࠾ࠥࢁࡽࠣ⁵").format(e))
    def _1lllll11l11l_opy_(self, response):
        bstack1l11l11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡅࡕࡏࠠࡳࡧࡶࡴࡴࡴࡳࡦࠢࡤࡲࡩࠦࡥࡹࡶࡵࡥࡨࡺࡳࠡࡴࡨࡰࡪࡼࡡ࡯ࡶࠣࡪ࡮࡫࡬ࡥࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ⁶")
        bstack1ll1l11l1l_opy_ = {}
        bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ⁷")] = response.get(bstack1l11l11_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦ⁸"), self.bstack1lllll1l111l_opy_)
        bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࡎࡴࡴࡦࡴࡹࡥࡱࠨ⁹")] = response.get(bstack1l11l11_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࡏ࡮ࡵࡧࡵࡺࡦࡲࠢ⁺"), self.bstack1lllll1l11l1_opy_)
        bstack1lllll11ll1l_opy_ = response.get(bstack1l11l11_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹ࡛ࡲ࡭ࠤ⁻"))
        bstack1lllll11l1ll_opy_ = response.get(bstack1l11l11_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡖࡴ࡯ࠦ⁼"))
        if bstack1lllll11ll1l_opy_:
            bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡖࡴ࡯ࠦ⁽")] = bstack1lllll11ll1l_opy_.split(bstack11l1lllllll_opy_ + bstack1l11l11_opy_ (u"ࠤ࠲ࠦ⁾"))[1] if bstack11l1lllllll_opy_ + bstack1l11l11_opy_ (u"ࠥ࠳ࠧⁿ") in bstack1lllll11ll1l_opy_ else bstack1lllll11ll1l_opy_
        else:
            bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢ₀")] = None
        if bstack1lllll11l1ll_opy_:
            bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹ࡛ࡲ࡭ࠤ₁")] = bstack1lllll11l1ll_opy_.split(bstack11l1lllllll_opy_ + bstack1l11l11_opy_ (u"ࠨ࠯ࠣ₂"))[1] if bstack11l1lllllll_opy_ + bstack1l11l11_opy_ (u"ࠢ࠰ࠤ₃") in bstack1lllll11l1ll_opy_ else bstack1lllll11l1ll_opy_
        else:
            bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧ₄")] = None
        if (
            response.get(bstack1l11l11_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ₅")) is None or
            response.get(bstack1l11l11_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࡍࡳࡺࡥࡳࡸࡤࡰࠧ₆")) is None or
            response.get(bstack1l11l11_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣ₇")) is None or
            response.get(bstack1l11l11_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣ₈")) is None
        ):
            self.logger.debug(bstack1l11l11_opy_ (u"ࠨ࡛ࡱࡴࡲࡧࡪࡹࡳࡠࡵࡳࡰ࡮ࡺ࡟ࡵࡧࡶࡸࡸࡥࡲࡦࡵࡳࡳࡳࡹࡥ࡞ࠢࡕࡩࡨ࡫ࡩࡷࡧࡧࠤࡳࡻ࡬࡭ࠢࡹࡥࡱࡻࡥࠩࡵࠬࠤ࡫ࡵࡲࠡࡵࡲࡱࡪࠦࡡࡵࡶࡵ࡭ࡧࡻࡴࡦࡵࠣ࡭ࡳࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡆࡖࡉࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠥ₉"))
        return bstack1ll1l11l1l_opy_
    def bstack111l1l11111_opy_(self):
        if not self.bstack1lllll11ll11_opy_:
            self.logger.error(bstack1l11l11_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡐࡲࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡪࡡࡵࡣࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡱࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸ࠴ࠢ₊"))
            return None
        bstack1lllll11l111_opy_ = None
        test_files = []
        bstack1lllll11llll_opy_ = int(time.time() * 1000) # bstack1lllll11l1l1_opy_ sec
        bstack1lllll111ll1_opy_ = int(self.bstack1lllll11ll11_opy_.get(bstack1l11l11_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡋࡱࡸࡪࡸࡶࡢ࡮ࠥ₋"), self.bstack1lllll1l11l1_opy_))
        bstack1lllll111lll_opy_ = int(self.bstack1lllll11ll11_opy_.get(bstack1l11l11_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ₌"), self.bstack1lllll1l111l_opy_)) * 1000
        bstack1lllll11l1ll_opy_ = self.bstack1lllll11ll11_opy_.get(bstack1l11l11_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷ࡙ࡷࡲࠢ₍"), None)
        bstack1lllll11ll1l_opy_ = self.bstack1lllll11ll11_opy_.get(bstack1l11l11_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢ₎"), None)
        if bstack1lllll11ll1l_opy_ is None and bstack1lllll11l1ll_opy_ is None:
            return None
        try:
            while bstack1lllll11ll1l_opy_ and (time.time() * 1000 - bstack1lllll11llll_opy_) < bstack1lllll111lll_opy_:
                response = bstack11ll11l111l_opy_.bstack1lllllll111l_opy_(bstack1lllll11ll1l_opy_, {})
                if response and response.get(bstack1l11l11_opy_ (u"ࠧࡺࡥࡴࡶࡶࠦ₏")):
                    bstack1lllll11l111_opy_ = response.get(bstack1l11l11_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧₐ"))
                self.bstack1lllll11lll1_opy_ += 1
                if bstack1lllll11l111_opy_:
                    break
                time.sleep(bstack1lllll111ll1_opy_)
                self.logger.debug(bstack1l11l11_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡈࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡳࡷࡪࡥࡳࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡪࡷࡵ࡭ࠡࡴࡨࡷࡺࡲࡴࠡࡗࡕࡐࠥࡧࡦࡵࡧࡵࠤࡼࡧࡩࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡾࢁࠥࡹࡥࡤࡱࡱࡨࡸ࠴ࠢₑ").format(bstack1lllll111ll1_opy_))
            if bstack1lllll11l1ll_opy_ and not bstack1lllll11l111_opy_:
                self.logger.debug(bstack1l11l11_opy_ (u"ࠣ࡝ࡪࡩࡹࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳ࡞ࠢࡉࡩࡹࡩࡨࡪࡰࡪࠤࡴࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡭ࡲ࡫࡯ࡶࡶ࡙ࠣࡗࡒࠢₒ"))
                response = bstack11ll11l111l_opy_.bstack1lllllll111l_opy_(bstack1lllll11l1ll_opy_, {})
                if response and response.get(bstack1l11l11_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣₓ")):
                    bstack1lllll11l111_opy_ = response.get(bstack1l11l11_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤₔ"))
            if bstack1lllll11l111_opy_ and len(bstack1lllll11l111_opy_) > 0:
                for bstack111ll1llll_opy_ in bstack1lllll11l111_opy_:
                    file_path = bstack111ll1llll_opy_.get(bstack1l11l11_opy_ (u"ࠦ࡫࡯࡬ࡦࡒࡤࡸ࡭ࠨₕ"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1lllll11l111_opy_:
                return None
            self.logger.debug(bstack1l11l11_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡏࡳࡦࡨࡶࡪࡪࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡷ࡫ࡣࡦ࡫ࡹࡩࡩࡀࠠࡼࡿࠥₖ").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack1l11l11_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡱࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࡀࠠࡼࡿࠥₗ").format(e))
            return None
    def bstack111l1l111ll_opy_(self):
        bstack1l11l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡺࡨࡦࠢࡦࡳࡺࡴࡴࠡࡱࡩࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡄࡔࡎࠦࡣࡢ࡮࡯ࡷࠥࡳࡡࡥࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣₘ")
        return self.bstack1lllll11lll1_opy_