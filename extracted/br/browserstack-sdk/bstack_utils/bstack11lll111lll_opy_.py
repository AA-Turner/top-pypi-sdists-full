# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import os
import time
from bstack_utils.bstack11l111l1l1l_opy_ import bstack11l111ll111_opy_
from bstack_utils.constants import bstack11l11111lll_opy_
from bstack_utils.helper import get_host_info
class bstack11ll1lll1l1_opy_:
    bstack11l1111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡋࡥࡳࡪ࡬ࡦࡵࠣࡸࡪࡹࡴࠡࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡶ࡫ࡩࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡸ࡫ࡲࡷࡧࡵ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ῏")
    def __init__(self, config, logger):
        bstack11l1111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠࡤࡱࡱࡪ࡮࡭࠺ࠡࡦ࡬ࡧࡹ࠲ࠠࡵࡧࡶࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡩ࡯࡯ࡨ࡬࡫ࠏࠦࠠࠡࠢࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡥࡳࡵࡴࡤࡸࡪ࡭ࡹ࠻ࠢࡶࡸࡷ࠲ࠠࡵࡧࡶࡸࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡴࡶࡵࡥࡹ࡫ࡧࡺࠢࡱࡥࡲ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦῐ")
        self.config = config
        self.logger = logger
        self.bstack1llllll1ll11_opy_ = bstack11l1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡳࡰ࡮ࡺ࠭ࡵࡧࡶࡸࡸࠨῑ")
        self.bstack1llllll1l111_opy_ = None
        self.bstack1llllll11ll1_opy_ = 60
        self.bstack1llllll11l1l_opy_ = 5
        self.bstack1llllll1l1ll_opy_ = 0
    def bstack11lll111111_opy_(self, test_files, orchestration_strategy):
        bstack11l1111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡌࡲ࡮ࡺࡩࡢࡶࡨࡷࠥࡺࡨࡦࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡳࡧࡴࡹࡪࡹࡴࠡࡣࡱࡨࠥࡹࡴࡰࡴࡨࡷࠥࡺࡨࡦࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡰࡰ࡮࡯࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧῒ")
        self.logger.debug(bstack11l1111_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡࠥࡏ࡮ࡪࡶ࡬ࡥࡹ࡯࡮ࡨࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡸ࡫ࡷ࡬ࠥࡹࡴࡳࡣࡷࡩ࡬ࡿ࠺ࠡࡽࢀࠦΐ").format(orchestration_strategy))
        try:
            payload = {
                bstack11l1111_opy_ (u"ࠢࡵࡧࡶࡸࡸࠨ῔"): [{bstack11l1111_opy_ (u"ࠣࡨ࡬ࡰࡪࡖࡡࡵࡪࠥ῕"): f} for f in test_files],
                bstack11l1111_opy_ (u"ࠤࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡕࡷࡶࡦࡺࡥࡨࡻࠥῖ"): orchestration_strategy,
                bstack11l1111_opy_ (u"ࠥࡲࡴࡪࡥࡊࡰࡧࡩࡽࠨῗ"): int(os.environ.get(bstack11l1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡋࡑࡈࡊ࡞ࠢῘ")) or bstack11l1111_opy_ (u"ࠧ࠶ࠢῙ")),
                bstack11l1111_opy_ (u"ࠨࡴࡰࡶࡤࡰࡓࡵࡤࡦࡵࠥῚ"): int(os.environ.get(bstack11l1111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡐࡖࡄࡐࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤΊ")) or bstack11l1111_opy_ (u"ࠣ࠳ࠥ῜")),
                bstack11l1111_opy_ (u"ࠤࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠢ῝"): self.config.get(bstack11l1111_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ῞"), bstack11l1111_opy_ (u"ࠫࠬ῟")),
                bstack11l1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠣῠ"): self.config.get(bstack11l1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩῡ"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack11l1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧῢ"): os.environ.get(bstack11l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧΰ"), None),
                bstack11l1111_opy_ (u"ࠤ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠦῤ"): get_host_info(),
            }
            self.logger.debug(bstack11l1111_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡖࡩࡳࡪࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹ࠺ࠡࡽࢀࠦῥ").format(payload))
            response = bstack11l111ll111_opy_.bstack1111111llll_opy_(self.bstack1llllll1ll11_opy_, payload)
            if response:
                self.bstack1llllll1l111_opy_ = self._1llllll1lll1_opy_(response)
                self.logger.debug(bstack11l1111_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡗࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢῦ").format(self.bstack1llllll1l111_opy_))
            else:
                self.logger.error(bstack11l1111_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡨࡧࡷࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠲ࠧῧ"))
        except Exception as e:
            self.logger.error(bstack11l1111_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴ࠼࠽ࠤࢀࢃࠢῨ").format(e))
    def _1llllll1lll1_opy_(self, response):
        bstack11l1111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡵࡪࡨࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡄࡔࡎࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡࡣࡱࡨࠥ࡫ࡸࡵࡴࡤࡧࡹࡹࠠࡳࡧ࡯ࡩࡻࡧ࡮ࡵࠢࡩ࡭ࡪࡲࡤࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢῩ")
        bstack11l11l11_opy_ = {}
        bstack11l11l11_opy_[bstack11l1111_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤῪ")] = response.get(bstack11l1111_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥΎ"), self.bstack1llllll11ll1_opy_)
        bstack11l11l11_opy_[bstack11l1111_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࡍࡳࡺࡥࡳࡸࡤࡰࠧῬ")] = response.get(bstack11l1111_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࡎࡴࡴࡦࡴࡹࡥࡱࠨ῭"), self.bstack1llllll11l1l_opy_)
        bstack1llllll1l1l1_opy_ = response.get(bstack11l1111_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣ΅"))
        bstack1llllll1ll1l_opy_ = response.get(bstack11l1111_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡕࡳ࡮ࠥ`"))
        if bstack1llllll1l1l1_opy_:
            bstack11l11l11_opy_[bstack11l1111_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡕࡳ࡮ࠥ῰")] = bstack1llllll1l1l1_opy_.split(bstack11l11111lll_opy_ + bstack11l1111_opy_ (u"ࠣ࠱ࠥ῱"))[1] if bstack11l11111lll_opy_ + bstack11l1111_opy_ (u"ࠤ࠲ࠦῲ") in bstack1llllll1l1l1_opy_ else bstack1llllll1l1l1_opy_
        else:
            bstack11l11l11_opy_[bstack11l1111_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡘࡶࡱࠨῳ")] = None
        if bstack1llllll1ll1l_opy_:
            bstack11l11l11_opy_[bstack11l1111_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣῴ")] = bstack1llllll1ll1l_opy_.split(bstack11l11111lll_opy_ + bstack11l1111_opy_ (u"ࠧ࠵ࠢ῵"))[1] if bstack11l11111lll_opy_ + bstack11l1111_opy_ (u"ࠨ࠯ࠣῶ") in bstack1llllll1ll1l_opy_ else bstack1llllll1ll1l_opy_
        else:
            bstack11l11l11_opy_[bstack11l1111_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡖࡴ࡯ࠦῷ")] = None
        if (
            response.get(bstack11l1111_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤῸ")) is None or
            response.get(bstack11l1111_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡌࡲࡹ࡫ࡲࡷࡣ࡯ࠦΌ")) is None or
            response.get(bstack11l1111_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷ࡙ࡷࡲࠢῺ")) is None or
            response.get(bstack11l1111_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢΏ")) is None
        ):
            self.logger.debug(bstack11l1111_opy_ (u"ࠧࡡࡰࡳࡱࡦࡩࡸࡹ࡟ࡴࡲ࡯࡭ࡹࡥࡴࡦࡵࡷࡷࡤࡸࡥࡴࡲࡲࡲࡸ࡫࡝ࠡࡔࡨࡧࡪ࡯ࡶࡦࡦࠣࡲࡺࡲ࡬ࠡࡸࡤࡰࡺ࡫ࠨࡴࠫࠣࡪࡴࡸࠠࡴࡱࡰࡩࠥࡧࡴࡵࡴ࡬ࡦࡺࡺࡥࡴࠢ࡬ࡲࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡅࡕࡏࠠࡳࡧࡶࡴࡴࡴࡳࡦࠤῼ"))
        return bstack11l11l11_opy_
    def bstack11ll1lll1ll_opy_(self):
        if not self.bstack1llllll1l111_opy_:
            self.logger.error(bstack11l1111_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡏࡱࠣࡶࡪࡷࡵࡦࡵࡷࠤࡩࡧࡴࡢࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡰࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷ࠳ࠨ´"))
            return None
        bstack1llllll11l11_opy_ = None
        test_files = []
        bstack1llllll1l11l_opy_ = int(time.time() * 1000) # bstack1lllllll1111_opy_ sec
        bstack1llllll1llll_opy_ = int(self.bstack1llllll1l111_opy_.get(bstack11l1111_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡊࡰࡷࡩࡷࡼࡡ࡭ࠤ῾"), self.bstack1llllll11l1l_opy_))
        bstack1llllll11lll_opy_ = int(self.bstack1llllll1l111_opy_.get(bstack11l1111_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ῿"), self.bstack1llllll11ll1_opy_)) * 1000
        bstack1llllll1ll1l_opy_ = self.bstack1llllll1l111_opy_.get(bstack11l1111_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡘࡶࡱࠨ "), None)
        bstack1llllll1l1l1_opy_ = self.bstack1llllll1l111_opy_.get(bstack11l1111_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡘࡶࡱࠨ "), None)
        if bstack1llllll1l1l1_opy_ is None and bstack1llllll1ll1l_opy_ is None:
            return None
        try:
            while bstack1llllll1l1l1_opy_ and (time.time() * 1000 - bstack1llllll1l11l_opy_) < bstack1llllll11lll_opy_:
                response = bstack11l111ll111_opy_.bstack1111111ll11_opy_(bstack1llllll1l1l1_opy_, {})
                if response and response.get(bstack11l1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࠥ ")):
                    bstack1llllll11l11_opy_ = response.get(bstack11l1111_opy_ (u"ࠧࡺࡥࡴࡶࡶࠦ "))
                self.bstack1llllll1l1ll_opy_ += 1
                if bstack1llllll11l11_opy_:
                    break
                time.sleep(bstack1llllll1llll_opy_)
                self.logger.debug(bstack11l1111_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡇࡧࡷࡧ࡭࡯࡮ࡨࠢࡲࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࡴࠢࡩࡶࡴࡳࠠࡳࡧࡶࡹࡱࡺࠠࡖࡔࡏࠤࡦ࡬ࡴࡦࡴࠣࡻࡦ࡯ࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡽࢀࠤࡸ࡫ࡣࡰࡰࡧࡷ࠳ࠨ ").format(bstack1llllll1llll_opy_))
            if bstack1llllll1ll1l_opy_ and not bstack1llllll11l11_opy_:
                self.logger.debug(bstack11l1111_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡈࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡳࡷࡪࡥࡳࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡬ࡱࡪࡵࡵࡵࠢࡘࡖࡑࠨ "))
                response = bstack11l111ll111_opy_.bstack1111111ll11_opy_(bstack1llllll1ll1l_opy_, {})
                if response and response.get(bstack11l1111_opy_ (u"ࠣࡶࡨࡷࡹࡹࠢ ")):
                    bstack1llllll11l11_opy_ = response.get(bstack11l1111_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣ "))
            if bstack1llllll11l11_opy_ and len(bstack1llllll11l11_opy_) > 0:
                for bstack111ll1ll1l_opy_ in bstack1llllll11l11_opy_:
                    file_path = bstack111ll1ll1l_opy_.get(bstack11l1111_opy_ (u"ࠥࡪ࡮ࡲࡥࡑࡣࡷ࡬ࠧ "))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1llllll11l11_opy_:
                return None
            self.logger.debug(bstack11l1111_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡕࡲࡥࡧࡵࡩࡩࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡶࡪࡩࡥࡪࡸࡨࡨ࠿ࠦࡻࡾࠤ ").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack11l1111_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡰࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷ࠿ࠦࡻࡾࠤ ").format(e))
            return None
    def bstack11ll1llll11_opy_(self):
        bstack11l1111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡࡥࡲࡹࡳࡺࠠࡰࡨࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡃࡓࡍࠥࡩࡡ࡭࡮ࡶࠤࡲࡧࡤࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ​")
        return self.bstack1llllll1l1ll_opy_