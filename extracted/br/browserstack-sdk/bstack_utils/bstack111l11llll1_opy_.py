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
import time
from bstack_utils.bstack11ll11l1l11_opy_ import bstack11ll11l1111_opy_
from bstack_utils.constants import bstack11ll111111l_opy_
from bstack_utils.helper import get_host_info, bstack111ll1ll11l_opy_
class bstack111l11lll11_opy_:
    bstack11l1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡋࡥࡳࡪ࡬ࡦࡵࠣࡸࡪࡹࡴࠡࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡶ࡫ࡩࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡸ࡫ࡲࡷࡧࡵ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ⁛")
    def __init__(self, config, logger):
        bstack11l1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠࡤࡱࡱࡪ࡮࡭࠺ࠡࡦ࡬ࡧࡹ࠲ࠠࡵࡧࡶࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡩ࡯࡯ࡨ࡬࡫ࠏࠦࠠࠡࠢࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡥࡳࡵࡴࡤࡸࡪ࡭ࡹ࠻ࠢࡶࡸࡷ࠲ࠠࡵࡧࡶࡸࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡴࡶࡵࡥࡹ࡫ࡧࡺࠢࡱࡥࡲ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⁜")
        self.config = config
        self.logger = logger
        self.bstack1lllll1l1l11_opy_ = bstack11l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡳࡰ࡮ࡺ࠭ࡵࡧࡶࡸࡸࠨ⁝")
        self.bstack1lllll11ll1l_opy_ = None
        self.bstack1lllll1l1l1l_opy_ = 60
        self.bstack1lllll11llll_opy_ = 5
        self.bstack1lllll1l1ll1_opy_ = 0
    def bstack111l11ll1l1_opy_(self, test_files, orchestration_strategy, bstack111l1l11ll1_opy_={}):
        bstack11l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡌࡲ࡮ࡺࡩࡢࡶࡨࡷࠥࡺࡨࡦࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡳࡧࡴࡹࡪࡹࡴࠡࡣࡱࡨࠥࡹࡴࡰࡴࡨࡷࠥࡺࡨࡦࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡰࡰ࡮࡯࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ⁞")
        self.logger.debug(bstack11l1_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡࠥࡏ࡮ࡪࡶ࡬ࡥࡹ࡯࡮ࡨࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡸ࡫ࡷ࡬ࠥࡹࡴࡳࡣࡷࡩ࡬ࡿ࠺ࠡࡽࢀࠦ ").format(orchestration_strategy))
        try:
            payload = {
                bstack11l1_opy_ (u"ࠢࡵࡧࡶࡸࡸࠨ⁠"): [{bstack11l1_opy_ (u"ࠣࡨ࡬ࡰࡪࡖࡡࡵࡪࠥ⁡"): f} for f in test_files],
                bstack11l1_opy_ (u"ࠤࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡕࡷࡶࡦࡺࡥࡨࡻࠥ⁢"): orchestration_strategy,
                bstack11l1_opy_ (u"ࠥࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡐࡩࡹࡧࡤࡢࡶࡤࠦ⁣"): bstack111l1l11ll1_opy_,
                bstack11l1_opy_ (u"ࠦࡳࡵࡤࡦࡋࡱࡨࡪࡾࠢ⁤"): int(os.environ.get(bstack11l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡓࡕࡄࡆࡡࡌࡒࡉࡋࡘࠣ⁥")) or bstack11l1_opy_ (u"ࠨ࠰ࠣ⁦")),
                bstack11l1_opy_ (u"ࠢࡵࡱࡷࡥࡱࡔ࡯ࡥࡧࡶࠦ⁧"): int(os.environ.get(bstack11l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡑࡗࡅࡑࡥࡎࡐࡆࡈࡣࡈࡕࡕࡏࡖࠥ⁨")) or bstack11l1_opy_ (u"ࠤ࠴ࠦ⁩")),
                bstack11l1_opy_ (u"ࠥࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠣ⁪"): self.config.get(bstack11l1_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ⁫"), bstack11l1_opy_ (u"ࠬ࠭⁬")),
                bstack11l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠤ⁭"): self.config.get(bstack11l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ⁮"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack11l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡒࡶࡰࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠨ⁯"): os.environ.get(bstack11l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ⁰"), None),
                bstack11l1_opy_ (u"ࠥ࡬ࡴࡹࡴࡊࡰࡩࡳࠧⁱ"): get_host_info(),
                bstack11l1_opy_ (u"ࠦࡵࡸࡄࡦࡶࡤ࡭ࡱࡹࠢ⁲"): bstack111ll1ll11l_opy_()
            }
            self.logger.debug(bstack11l1_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡘ࡫࡮ࡥ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴ࠼ࠣࡿࢂࠨ⁳").format(payload))
            response = bstack11ll11l1111_opy_.bstack1llllllll111_opy_(self.bstack1lllll1l1l11_opy_, payload)
            if response:
                self.bstack1lllll11ll1l_opy_ = self._1lllll11l1l1_opy_(response)
                self.logger.debug(bstack11l1_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡ࡙ࠥࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤ⁴").format(self.bstack1lllll11ll1l_opy_))
            else:
                self.logger.error(bstack11l1_opy_ (u"ࠢ࡜ࡵࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࡢࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡪࡩࡹࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢ⁵"))
        except Exception as e:
            self.logger.error(bstack11l1_opy_ (u"ࠣ࡝ࡶࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࡣࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶ࠾࠿ࠦࡻࡾࠤ⁶").format(e))
    def _1lllll11l1l1_opy_(self, response):
        bstack11l1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡳࡱࡦࡩࡸࡹࡥࡴࠢࡷ࡬ࡪࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡆࡖࡉࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡥࡳࡪࠠࡦࡺࡷࡶࡦࡩࡴࡴࠢࡵࡩࡱ࡫ࡶࡢࡰࡷࠤ࡫࡯ࡥ࡭ࡦࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ⁷")
        bstack1l111llll1_opy_ = {}
        bstack1l111llll1_opy_[bstack11l1_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦ⁸")] = response.get(bstack11l1_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࠧ⁹"), self.bstack1lllll1l1l1l_opy_)
        bstack1l111llll1_opy_[bstack11l1_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࡏ࡮ࡵࡧࡵࡺࡦࡲࠢ⁺")] = response.get(bstack11l1_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠣ⁻"), self.bstack1lllll11llll_opy_)
        bstack1lllll11ll11_opy_ = response.get(bstack11l1_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡕࡳ࡮ࠥ⁼"))
        bstack1lllll1l11l1_opy_ = response.get(bstack11l1_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧ⁽"))
        if bstack1lllll11ll11_opy_:
            bstack1l111llll1_opy_[bstack11l1_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡗࡵࡰࠧ⁾")] = bstack1lllll11ll11_opy_.split(bstack11ll111111l_opy_ + bstack11l1_opy_ (u"ࠥ࠳ࠧⁿ"))[1] if bstack11ll111111l_opy_ + bstack11l1_opy_ (u"ࠦ࠴ࠨ₀") in bstack1lllll11ll11_opy_ else bstack1lllll11ll11_opy_
        else:
            bstack1l111llll1_opy_[bstack11l1_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣ₁")] = None
        if bstack1lllll1l11l1_opy_:
            bstack1l111llll1_opy_[bstack11l1_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡕࡳ࡮ࠥ₂")] = bstack1lllll1l11l1_opy_.split(bstack11ll111111l_opy_ + bstack11l1_opy_ (u"ࠢ࠰ࠤ₃"))[1] if bstack11ll111111l_opy_ + bstack11l1_opy_ (u"ࠣ࠱ࠥ₄") in bstack1lllll1l11l1_opy_ else bstack1lllll1l11l1_opy_
        else:
            bstack1l111llll1_opy_[bstack11l1_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡘࡶࡱࠨ₅")] = None
        if (
            response.get(bstack11l1_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦ₆")) is None or
            response.get(bstack11l1_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࡎࡴࡴࡦࡴࡹࡥࡱࠨ₇")) is None or
            response.get(bstack11l1_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹ࡛ࡲ࡭ࠤ₈")) is None or
            response.get(bstack11l1_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹ࡛ࡲ࡭ࠤ₉")) is None
        ):
            self.logger.debug(bstack11l1_opy_ (u"ࠢ࡜ࡲࡵࡳࡨ࡫ࡳࡴࡡࡶࡴࡱ࡯ࡴࡠࡶࡨࡷࡹࡹ࡟ࡳࡧࡶࡴࡴࡴࡳࡦ࡟ࠣࡖࡪࡩࡥࡪࡸࡨࡨࠥࡴࡵ࡭࡮ࠣࡺࡦࡲࡵࡦࠪࡶ࠭ࠥ࡬࡯ࡳࠢࡶࡳࡲ࡫ࠠࡢࡶࡷࡶ࡮ࡨࡵࡵࡧࡶࠤ࡮ࡴࠠࡴࡲ࡯࡭ࡹࠦࡴࡦࡵࡷࡷࠥࡇࡐࡊࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠦ₊"))
        return bstack1l111llll1_opy_
    def bstack111l11ll1ll_opy_(self):
        if not self.bstack1lllll11ll1l_opy_:
            self.logger.error(bstack11l1_opy_ (u"ࠣ࡝ࡪࡩࡹࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳ࡞ࠢࡑࡳࠥࡸࡥࡲࡷࡨࡷࡹࠦࡤࡢࡶࡤࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡲࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹ࠮ࠣ₋"))
            return None
        bstack1lllll1l111l_opy_ = None
        test_files = []
        bstack1lllll11l1ll_opy_ = int(time.time() * 1000) # bstack1lllll11lll1_opy_ sec
        bstack1lllll1l11ll_opy_ = int(self.bstack1lllll11ll1l_opy_.get(bstack11l1_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡌࡲࡹ࡫ࡲࡷࡣ࡯ࠦ₌"), self.bstack1lllll11llll_opy_))
        bstack1lllll1l1111_opy_ = int(self.bstack1lllll11ll1l_opy_.get(bstack11l1_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦ₍"), self.bstack1lllll1l1l1l_opy_)) * 1000
        bstack1lllll1l11l1_opy_ = self.bstack1lllll11ll1l_opy_.get(bstack11l1_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣ₎"), None)
        bstack1lllll11ll11_opy_ = self.bstack1lllll11ll1l_opy_.get(bstack11l1_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣ₏"), None)
        if bstack1lllll11ll11_opy_ is None and bstack1lllll1l11l1_opy_ is None:
            return None
        try:
            while bstack1lllll11ll11_opy_ and (time.time() * 1000 - bstack1lllll11l1ll_opy_) < bstack1lllll1l1111_opy_:
                response = bstack11ll11l1111_opy_.bstack1lllllll1l11_opy_(bstack1lllll11ll11_opy_, {})
                if response and response.get(bstack11l1_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧₐ")):
                    bstack1lllll1l111l_opy_ = response.get(bstack11l1_opy_ (u"ࠢࡵࡧࡶࡸࡸࠨₑ"))
                self.bstack1lllll1l1ll1_opy_ += 1
                if bstack1lllll1l111l_opy_:
                    break
                time.sleep(bstack1lllll1l11ll_opy_)
                self.logger.debug(bstack11l1_opy_ (u"ࠣ࡝ࡪࡩࡹࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳ࡞ࠢࡉࡩࡹࡩࡨࡪࡰࡪࠤࡴࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡵࡩࡸࡻ࡬ࡵࠢࡘࡖࡑࠦࡡࡧࡶࡨࡶࠥࡽࡡࡪࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡿࢂࠦࡳࡦࡥࡲࡲࡩࡹ࠮ࠣₒ").format(bstack1lllll1l11ll_opy_))
            if bstack1lllll1l11l1_opy_ and not bstack1lllll1l111l_opy_:
                self.logger.debug(bstack11l1_opy_ (u"ࠤ࡞࡫ࡪࡺࡏࡳࡦࡨࡶࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴ࡟ࠣࡊࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡵࡲࡥࡧࡵࡩࡩࠦࡴࡦࡵࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡮ࡳࡥࡰࡷࡷࠤ࡚ࡘࡌࠣₓ"))
                response = bstack11ll11l1111_opy_.bstack1lllllll1l11_opy_(bstack1lllll1l11l1_opy_, {})
                if response and response.get(bstack11l1_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤₔ")):
                    bstack1lllll1l111l_opy_ = response.get(bstack11l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࠥₕ"))
            if bstack1lllll1l111l_opy_ and len(bstack1lllll1l111l_opy_) > 0:
                for bstack111lll11ll_opy_ in bstack1lllll1l111l_opy_:
                    file_path = bstack111lll11ll_opy_.get(bstack11l1_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡓࡥࡹ࡮ࠢₖ"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1lllll1l111l_opy_:
                return None
            self.logger.debug(bstack11l1_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡐࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡸࡥࡤࡧ࡬ࡺࡪࡪ࠺ࠡࡽࢀࠦₗ").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack11l1_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡲࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹ࠺ࠡࡽࢀࠦₘ").format(e))
            return None
    def bstack111l1l1l111_opy_(self):
        bstack11l1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠣࡧࡴࡻ࡮ࡵࠢࡲࡪࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡅࡕࡏࠠࡤࡣ࡯ࡰࡸࠦ࡭ࡢࡦࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤₙ")
        return self.bstack1lllll1l1ll1_opy_