# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import os
import time
from bstack_utils.bstack11ll1l111l1_opy_ import bstack11ll11lllll_opy_
from bstack_utils.constants import bstack11l1ll1ll11_opy_
from bstack_utils.helper import get_host_info
class bstack111l1ll1lll_opy_:
    bstack1l1l1l1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡋࡥࡳࡪ࡬ࡦࡵࠣࡸࡪࡹࡴࠡࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡶ࡫ࡩࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡸ࡫ࡲࡷࡧࡵ࠲ࠏࠦࠠࠡࠢࠥࠦࠧὭ")
    def __init__(self, config, logger):
        bstack1l1l1l1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠࡤࡱࡱࡪ࡮࡭࠺ࠡࡦ࡬ࡧࡹ࠲ࠠࡵࡧࡶࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡩ࡯࡯ࡨ࡬࡫ࠏࠦࠠࠡࠢࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡥࡳࡵࡴࡤࡸࡪ࡭ࡹ࠻ࠢࡶࡸࡷ࠲ࠠࡵࡧࡶࡸࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡴࡶࡵࡥࡹ࡫ࡧࡺࠢࡱࡥࡲ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦὮ")
        self.config = config
        self.logger = logger
        self.bstack1lllllll1l1l_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡳࡰ࡮ࡺ࠭ࡵࡧࡶࡸࡸࠨὯ")
        self.bstack1lllllll1l11_opy_ = None
        self.bstack1lllllll111l_opy_ = 60
        self.bstack1llllllll111_opy_ = 5
        self.bstack1llllll1lll1_opy_ = 0
    def bstack111l1llllll_opy_(self, test_files, orchestration_strategy):
        bstack1l1l1l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡌࡲ࡮ࡺࡩࡢࡶࡨࡷࠥࡺࡨࡦࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡳࡧࡴࡹࡪࡹࡴࠡࡣࡱࡨࠥࡹࡴࡰࡴࡨࡷࠥࡺࡨࡦࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡰࡰ࡮࡯࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧὰ")
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡࠥࡏ࡮ࡪࡶ࡬ࡥࡹ࡯࡮ࡨࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡸ࡫ࡷ࡬ࠥࡹࡴࡳࡣࡷࡩ࡬ࡿ࠺ࠡࡽࢀࠦά").format(orchestration_strategy))
        try:
            payload = {
                bstack1l1l1l1_opy_ (u"ࠢࡵࡧࡶࡸࡸࠨὲ"): [{bstack1l1l1l1_opy_ (u"ࠣࡨ࡬ࡰࡪࡖࡡࡵࡪࠥέ"): f} for f in test_files],
                bstack1l1l1l1_opy_ (u"ࠤࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡕࡷࡶࡦࡺࡥࡨࡻࠥὴ"): orchestration_strategy,
                bstack1l1l1l1_opy_ (u"ࠥࡲࡴࡪࡥࡊࡰࡧࡩࡽࠨή"): int(os.environ.get(bstack1l1l1l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡋࡑࡈࡊ࡞ࠢὶ")) or bstack1l1l1l1_opy_ (u"ࠧ࠶ࠢί")),
                bstack1l1l1l1_opy_ (u"ࠨࡴࡰࡶࡤࡰࡓࡵࡤࡦࡵࠥὸ"): int(os.environ.get(bstack1l1l1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡐࡖࡄࡐࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤό")) or bstack1l1l1l1_opy_ (u"ࠣ࠳ࠥὺ")),
                bstack1l1l1l1_opy_ (u"ࠤࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠢύ"): self.config.get(bstack1l1l1l1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨὼ"), bstack1l1l1l1_opy_ (u"ࠫࠬώ")),
                bstack1l1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠣ὾"): self.config.get(bstack1l1l1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ὿"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1l1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧᾀ"): os.environ.get(bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧᾁ"), None),
                bstack1l1l1l1_opy_ (u"ࠤ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠦᾂ"): get_host_info(),
            }
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡖࡩࡳࡪࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹ࠺ࠡࡽࢀࠦᾃ").format(payload))
            response = bstack11ll11lllll_opy_.bstack111111ll1l1_opy_(self.bstack1lllllll1l1l_opy_, payload)
            if response:
                self.bstack1lllllll1l11_opy_ = self._1lllllll11ll_opy_(response)
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡗࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢᾄ").format(self.bstack1lllllll1l11_opy_))
            else:
                self.logger.error(bstack1l1l1l1_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡨࡧࡷࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠲ࠧᾅ"))
        except Exception as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴ࠼࠽ࠤࢀࢃࠢᾆ").format(e))
    def _1lllllll11ll_opy_(self, response):
        bstack1l1l1l1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡵࡪࡨࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡄࡔࡎࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡࡣࡱࡨࠥ࡫ࡸࡵࡴࡤࡧࡹࡹࠠࡳࡧ࡯ࡩࡻࡧ࡮ࡵࠢࡩ࡭ࡪࡲࡤࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᾇ")
        bstack11l1l111ll_opy_ = {}
        bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤᾈ")] = response.get(bstack1l1l1l1_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥᾉ"), self.bstack1lllllll111l_opy_)
        bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࡍࡳࡺࡥࡳࡸࡤࡰࠧᾊ")] = response.get(bstack1l1l1l1_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࡎࡴࡴࡦࡴࡹࡥࡱࠨᾋ"), self.bstack1llllllll111_opy_)
        bstack1lllllll1ll1_opy_ = response.get(bstack1l1l1l1_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣᾌ"))
        bstack1lllllll1lll_opy_ = response.get(bstack1l1l1l1_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡕࡳ࡮ࠥᾍ"))
        if bstack1lllllll1ll1_opy_:
            bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡕࡳ࡮ࠥᾎ")] = bstack1lllllll1ll1_opy_.split(bstack11l1ll1ll11_opy_ + bstack1l1l1l1_opy_ (u"ࠣ࠱ࠥᾏ"))[1] if bstack11l1ll1ll11_opy_ + bstack1l1l1l1_opy_ (u"ࠤ࠲ࠦᾐ") in bstack1lllllll1ll1_opy_ else bstack1lllllll1ll1_opy_
        else:
            bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡘࡶࡱࠨᾑ")] = None
        if bstack1lllllll1lll_opy_:
            bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣᾒ")] = bstack1lllllll1lll_opy_.split(bstack11l1ll1ll11_opy_ + bstack1l1l1l1_opy_ (u"ࠧ࠵ࠢᾓ"))[1] if bstack11l1ll1ll11_opy_ + bstack1l1l1l1_opy_ (u"ࠨ࠯ࠣᾔ") in bstack1lllllll1lll_opy_ else bstack1lllllll1lll_opy_
        else:
            bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡖࡴ࡯ࠦᾕ")] = None
        if (
            response.get(bstack1l1l1l1_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤᾖ")) is None or
            response.get(bstack1l1l1l1_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡌࡲࡹ࡫ࡲࡷࡣ࡯ࠦᾗ")) is None or
            response.get(bstack1l1l1l1_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷ࡙ࡷࡲࠢᾘ")) is None or
            response.get(bstack1l1l1l1_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢᾙ")) is None
        ):
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡡࡰࡳࡱࡦࡩࡸࡹ࡟ࡴࡲ࡯࡭ࡹࡥࡴࡦࡵࡷࡷࡤࡸࡥࡴࡲࡲࡲࡸ࡫࡝ࠡࡔࡨࡧࡪ࡯ࡶࡦࡦࠣࡲࡺࡲ࡬ࠡࡸࡤࡰࡺ࡫ࠨࡴࠫࠣࡪࡴࡸࠠࡴࡱࡰࡩࠥࡧࡴࡵࡴ࡬ࡦࡺࡺࡥࡴࠢ࡬ࡲࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡅࡕࡏࠠࡳࡧࡶࡴࡴࡴࡳࡦࠤᾚ"))
        return bstack11l1l111ll_opy_
    def bstack111l1ll1ll1_opy_(self):
        if not self.bstack1lllllll1l11_opy_:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡏࡱࠣࡶࡪࡷࡵࡦࡵࡷࠤࡩࡧࡴࡢࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡰࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷ࠳ࠨᾛ"))
            return None
        bstack1llllllll1l1_opy_ = None
        test_files = []
        bstack1lllllll11l1_opy_ = int(time.time() * 1000) # bstack1llllllll11l_opy_ sec
        bstack1lllllll1111_opy_ = int(self.bstack1lllllll1l11_opy_.get(bstack1l1l1l1_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡊࡰࡷࡩࡷࡼࡡ࡭ࠤᾜ"), self.bstack1llllllll111_opy_))
        bstack1llllll1llll_opy_ = int(self.bstack1lllllll1l11_opy_.get(bstack1l1l1l1_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤᾝ"), self.bstack1lllllll111l_opy_)) * 1000
        bstack1lllllll1lll_opy_ = self.bstack1lllllll1l11_opy_.get(bstack1l1l1l1_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡘࡶࡱࠨᾞ"), None)
        bstack1lllllll1ll1_opy_ = self.bstack1lllllll1l11_opy_.get(bstack1l1l1l1_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡘࡶࡱࠨᾟ"), None)
        if bstack1lllllll1ll1_opy_ is None and bstack1lllllll1lll_opy_ is None:
            return None
        try:
            while bstack1lllllll1ll1_opy_ and (time.time() * 1000 - bstack1lllllll11l1_opy_) < bstack1llllll1llll_opy_:
                response = bstack11ll11lllll_opy_.bstack111111lll11_opy_(bstack1lllllll1ll1_opy_, {})
                if response and response.get(bstack1l1l1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࠥᾠ")):
                    bstack1llllllll1l1_opy_ = response.get(bstack1l1l1l1_opy_ (u"ࠧࡺࡥࡴࡶࡶࠦᾡ"))
                self.bstack1llllll1lll1_opy_ += 1
                if bstack1llllllll1l1_opy_:
                    break
                time.sleep(bstack1lllllll1111_opy_)
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡇࡧࡷࡧ࡭࡯࡮ࡨࠢࡲࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࡴࠢࡩࡶࡴࡳࠠࡳࡧࡶࡹࡱࡺࠠࡖࡔࡏࠤࡦ࡬ࡴࡦࡴࠣࡻࡦ࡯ࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡽࢀࠤࡸ࡫ࡣࡰࡰࡧࡷ࠳ࠨᾢ").format(bstack1lllllll1111_opy_))
            if bstack1lllllll1lll_opy_ and not bstack1llllllll1l1_opy_:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡈࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡳࡷࡪࡥࡳࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡬ࡱࡪࡵࡵࡵࠢࡘࡖࡑࠨᾣ"))
                response = bstack11ll11lllll_opy_.bstack111111lll11_opy_(bstack1lllllll1lll_opy_, {})
                if response and response.get(bstack1l1l1l1_opy_ (u"ࠣࡶࡨࡷࡹࡹࠢᾤ")):
                    bstack1llllllll1l1_opy_ = response.get(bstack1l1l1l1_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣᾥ"))
            if bstack1llllllll1l1_opy_ and len(bstack1llllllll1l1_opy_) > 0:
                for bstack111lll1l1l_opy_ in bstack1llllllll1l1_opy_:
                    file_path = bstack111lll1l1l_opy_.get(bstack1l1l1l1_opy_ (u"ࠥࡪ࡮ࡲࡥࡑࡣࡷ࡬ࠧᾦ"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1llllllll1l1_opy_:
                return None
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡕࡲࡥࡧࡵࡩࡩࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡶࡪࡩࡥࡪࡸࡨࡨ࠿ࠦࡻࡾࠤᾧ").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡰࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷ࠿ࠦࡻࡾࠤᾨ").format(e))
            return None
    def bstack111ll11111l_opy_(self):
        bstack1l1l1l1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡࡥࡲࡹࡳࡺࠠࡰࡨࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡃࡓࡍࠥࡩࡡ࡭࡮ࡶࠤࡲࡧࡤࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᾩ")
        return self.bstack1llllll1lll1_opy_