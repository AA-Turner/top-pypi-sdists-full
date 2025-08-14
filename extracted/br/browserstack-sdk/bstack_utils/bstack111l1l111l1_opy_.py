# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import os
import time
from bstack_utils.bstack11ll11l1ll1_opy_ import bstack11ll11l1l1l_opy_
from bstack_utils.constants import bstack11l1ll11l11_opy_
from bstack_utils.helper import get_host_info, bstack11l111ll1l1_opy_
class bstack111l11lll11_opy_:
    bstack1l1l1ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡊࡤࡲࡩࡲࡥࡴࠢࡷࡩࡸࡺࠠࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡷࡪࡸࡶࡦࡴ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ⁨")
    def __init__(self, config, logger):
        bstack1l1l1ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡥ࡫ࡦࡸ࠱ࠦࡴࡦࡵࡷࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡨࡵ࡮ࡧ࡫ࡪࠎࠥࠦࠠࠡࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡤࡹࡴࡳࡣࡷࡩ࡬ࡿ࠺ࠡࡵࡷࡶ࠱ࠦࡴࡦࡵࡷࠤࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡳࡵࡴࡤࡸࡪ࡭ࡹࠡࡰࡤࡱࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ⁩")
        self.config = config
        self.logger = logger
        self.bstack1lllll11ll1l_opy_ = bstack1l1l1ll_opy_ (u"ࠥࡸࡪࡹࡴࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡲ࡯࡭ࡹ࠳ࡴࡦࡵࡷࡷࠧ⁪")
        self.bstack1lllll1l11l1_opy_ = None
        self.bstack1lllll11ll11_opy_ = 60
        self.bstack1lllll1l1l11_opy_ = 5
        self.bstack1lllll11l11l_opy_ = 0
    def bstack111l11lllll_opy_(self, test_files, orchestration_strategy, bstack111l1l11ll1_opy_={}):
        bstack1l1l1ll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡋࡱ࡭ࡹ࡯ࡡࡵࡧࡶࠤࡹ࡮ࡥࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡲࡦࡳࡸࡩࡸࡺࠠࡢࡰࡧࠤࡸࡺ࡯ࡳࡧࡶࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡶ࡯࡭࡮࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⁫")
        self.logger.debug(bstack1l1l1ll_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡎࡴࡩࡵ࡫ࡤࡸ࡮ࡴࡧࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡷࡪࡶ࡫ࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࡀࠠࡼࡿࠥ⁬").format(orchestration_strategy))
        try:
            payload = {
                bstack1l1l1ll_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧ⁭"): [{bstack1l1l1ll_opy_ (u"ࠢࡧ࡫࡯ࡩࡕࡧࡴࡩࠤ⁮"): f} for f in test_files],
                bstack1l1l1ll_opy_ (u"ࠣࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡔࡶࡵࡥࡹ࡫ࡧࡺࠤ⁯"): orchestration_strategy,
                bstack1l1l1ll_opy_ (u"ࠤࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡏࡨࡸࡦࡪࡡࡵࡣࠥ⁰"): bstack111l1l11ll1_opy_,
                bstack1l1l1ll_opy_ (u"ࠥࡲࡴࡪࡥࡊࡰࡧࡩࡽࠨⁱ"): int(os.environ.get(bstack1l1l1ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡋࡑࡈࡊ࡞ࠢ⁲")) or bstack1l1l1ll_opy_ (u"ࠧ࠶ࠢ⁳")),
                bstack1l1l1ll_opy_ (u"ࠨࡴࡰࡶࡤࡰࡓࡵࡤࡦࡵࠥ⁴"): int(os.environ.get(bstack1l1l1ll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡐࡖࡄࡐࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤ⁵")) or bstack1l1l1ll_opy_ (u"ࠣ࠳ࠥ⁶")),
                bstack1l1l1ll_opy_ (u"ࠤࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠢ⁷"): self.config.get(bstack1l1l1ll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ⁸"), bstack1l1l1ll_opy_ (u"ࠫࠬ⁹")),
                bstack1l1l1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠣ⁺"): self.config.get(bstack1l1l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ⁻"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1l1l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧ⁼"): os.environ.get(bstack1l1l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ⁽"), None),
                bstack1l1l1ll_opy_ (u"ࠤ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠦ⁾"): get_host_info(),
                bstack1l1l1ll_opy_ (u"ࠥࡴࡷࡊࡥࡵࡣ࡬ࡰࡸࠨⁿ"): bstack11l111ll1l1_opy_()
            }
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡗࡪࡴࡤࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳ࠻ࠢࡾࢁࠧ₀").format(payload))
            response = bstack11ll11l1l1l_opy_.bstack1llllll1llll_opy_(self.bstack1lllll11ll1l_opy_, payload)
            if response:
                self.bstack1lllll1l11l1_opy_ = self._1lllll1l111l_opy_(response)
                self.logger.debug(bstack1l1l1ll_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡘࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣ₁").format(self.bstack1lllll1l11l1_opy_))
            else:
                self.logger.error(bstack1l1l1ll_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡩࡨࡸࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠳ࠨ₂"))
        except Exception as e:
            self.logger.error(bstack1l1l1ll_opy_ (u"ࠢ࡜ࡵࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵ࠽࠾ࠥࢁࡽࠣ₃").format(e))
    def _1lllll1l111l_opy_(self, response):
        bstack1l1l1ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡅࡕࡏࠠࡳࡧࡶࡴࡴࡴࡳࡦࠢࡤࡲࡩࠦࡥࡹࡶࡵࡥࡨࡺࡳࠡࡴࡨࡰࡪࡼࡡ࡯ࡶࠣࡪ࡮࡫࡬ࡥࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ₄")
        bstack1111l1lll_opy_ = {}
        bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ₅")] = response.get(bstack1l1l1ll_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦ₆"), self.bstack1lllll11ll11_opy_)
        bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࡎࡴࡴࡦࡴࡹࡥࡱࠨ₇")] = response.get(bstack1l1l1ll_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࡏ࡮ࡵࡧࡵࡺࡦࡲࠢ₈"), self.bstack1lllll1l1l11_opy_)
        bstack1lllll11l1l1_opy_ = response.get(bstack1l1l1ll_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹ࡛ࡲ࡭ࠤ₉"))
        bstack1lllll11lll1_opy_ = response.get(bstack1l1l1ll_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡖࡴ࡯ࠦ₊"))
        if bstack1lllll11l1l1_opy_:
            bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡖࡴ࡯ࠦ₋")] = bstack1lllll11l1l1_opy_.split(bstack11l1ll11l11_opy_ + bstack1l1l1ll_opy_ (u"ࠤ࠲ࠦ₌"))[1] if bstack11l1ll11l11_opy_ + bstack1l1l1ll_opy_ (u"ࠥ࠳ࠧ₍") in bstack1lllll11l1l1_opy_ else bstack1lllll11l1l1_opy_
        else:
            bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢ₎")] = None
        if bstack1lllll11lll1_opy_:
            bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹ࡛ࡲ࡭ࠤ₏")] = bstack1lllll11lll1_opy_.split(bstack11l1ll11l11_opy_ + bstack1l1l1ll_opy_ (u"ࠨ࠯ࠣₐ"))[1] if bstack11l1ll11l11_opy_ + bstack1l1l1ll_opy_ (u"ࠢ࠰ࠤₑ") in bstack1lllll11lll1_opy_ else bstack1lllll11lll1_opy_
        else:
            bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧₒ")] = None
        if (
            response.get(bstack1l1l1ll_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥₓ")) is None or
            response.get(bstack1l1l1ll_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࡍࡳࡺࡥࡳࡸࡤࡰࠧₔ")) is None or
            response.get(bstack1l1l1ll_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣₕ")) is None or
            response.get(bstack1l1l1ll_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣₖ")) is None
        ):
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠨ࡛ࡱࡴࡲࡧࡪࡹࡳࡠࡵࡳࡰ࡮ࡺ࡟ࡵࡧࡶࡸࡸࡥࡲࡦࡵࡳࡳࡳࡹࡥ࡞ࠢࡕࡩࡨ࡫ࡩࡷࡧࡧࠤࡳࡻ࡬࡭ࠢࡹࡥࡱࡻࡥࠩࡵࠬࠤ࡫ࡵࡲࠡࡵࡲࡱࡪࠦࡡࡵࡶࡵ࡭ࡧࡻࡴࡦࡵࠣ࡭ࡳࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡆࡖࡉࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠥₗ"))
        return bstack1111l1lll_opy_
    def bstack111l1l11l11_opy_(self):
        if not self.bstack1lllll1l11l1_opy_:
            self.logger.error(bstack1l1l1ll_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡐࡲࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡪࡡࡵࡣࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡱࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸ࠴ࠢₘ"))
            return None
        bstack1lllll11llll_opy_ = None
        test_files = []
        bstack1lllll1l11ll_opy_ = int(time.time() * 1000) # bstack1lllll11l1ll_opy_ sec
        bstack1lllll11l111_opy_ = int(self.bstack1lllll1l11l1_opy_.get(bstack1l1l1ll_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡋࡱࡸࡪࡸࡶࡢ࡮ࠥₙ"), self.bstack1lllll1l1l11_opy_))
        bstack1lllll1l1111_opy_ = int(self.bstack1lllll1l11l1_opy_.get(bstack1l1l1ll_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥₚ"), self.bstack1lllll11ll11_opy_)) * 1000
        bstack1lllll11lll1_opy_ = self.bstack1lllll1l11l1_opy_.get(bstack1l1l1ll_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷ࡙ࡷࡲࠢₛ"), None)
        bstack1lllll11l1l1_opy_ = self.bstack1lllll1l11l1_opy_.get(bstack1l1l1ll_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢₜ"), None)
        if bstack1lllll11l1l1_opy_ is None and bstack1lllll11lll1_opy_ is None:
            return None
        try:
            while bstack1lllll11l1l1_opy_ and (time.time() * 1000 - bstack1lllll1l11ll_opy_) < bstack1lllll1l1111_opy_:
                response = bstack11ll11l1l1l_opy_.bstack1lllllll1111_opy_(bstack1lllll11l1l1_opy_, {})
                if response and response.get(bstack1l1l1ll_opy_ (u"ࠧࡺࡥࡴࡶࡶࠦ₝")):
                    bstack1lllll11llll_opy_ = response.get(bstack1l1l1ll_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧ₞"))
                self.bstack1lllll11l11l_opy_ += 1
                if bstack1lllll11llll_opy_:
                    break
                time.sleep(bstack1lllll11l111_opy_)
                self.logger.debug(bstack1l1l1ll_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡈࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡳࡷࡪࡥࡳࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡪࡷࡵ࡭ࠡࡴࡨࡷࡺࡲࡴࠡࡗࡕࡐࠥࡧࡦࡵࡧࡵࠤࡼࡧࡩࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡾࢁࠥࡹࡥࡤࡱࡱࡨࡸ࠴ࠢ₟").format(bstack1lllll11l111_opy_))
            if bstack1lllll11lll1_opy_ and not bstack1lllll11llll_opy_:
                self.logger.debug(bstack1l1l1ll_opy_ (u"ࠣ࡝ࡪࡩࡹࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳ࡞ࠢࡉࡩࡹࡩࡨࡪࡰࡪࠤࡴࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡭ࡲ࡫࡯ࡶࡶ࡙ࠣࡗࡒࠢ₠"))
                response = bstack11ll11l1l1l_opy_.bstack1lllllll1111_opy_(bstack1lllll11lll1_opy_, {})
                if response and response.get(bstack1l1l1ll_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣ₡")):
                    bstack1lllll11llll_opy_ = response.get(bstack1l1l1ll_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤ₢"))
            if bstack1lllll11llll_opy_ and len(bstack1lllll11llll_opy_) > 0:
                for bstack111lll1lll_opy_ in bstack1lllll11llll_opy_:
                    file_path = bstack111lll1lll_opy_.get(bstack1l1l1ll_opy_ (u"ࠦ࡫࡯࡬ࡦࡒࡤࡸ࡭ࠨ₣"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1lllll11llll_opy_:
                return None
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡏࡳࡦࡨࡶࡪࡪࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡷ࡫ࡣࡦ࡫ࡹࡩࡩࡀࠠࡼࡿࠥ₤").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack1l1l1ll_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡱࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࡀࠠࡼࡿࠥ₥").format(e))
            return None
    def bstack111l1l11111_opy_(self):
        bstack1l1l1ll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡺࡨࡦࠢࡦࡳࡺࡴࡴࠡࡱࡩࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡄࡔࡎࠦࡣࡢ࡮࡯ࡷࠥࡳࡡࡥࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ₦")
        return self.bstack1lllll11l11l_opy_