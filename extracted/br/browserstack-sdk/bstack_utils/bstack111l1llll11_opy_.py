# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import os
import time
from bstack_utils.bstack11ll11lll1l_opy_ import bstack11ll1l11111_opy_
from bstack_utils.constants import bstack11l1ll1ll11_opy_
from bstack_utils.helper import get_host_info
class bstack111l1llll1l_opy_:
    bstack11ll11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡊࡤࡲࡩࡲࡥࡴࠢࡷࡩࡸࡺࠠࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡷࡪࡸࡶࡦࡴ࠱ࠎࠥࠦࠠࠡࠤࠥࠦὬ")
    def __init__(self, config, logger):
        bstack11ll11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡥ࡫ࡦࡸ࠱ࠦࡴࡦࡵࡷࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡨࡵ࡮ࡧ࡫ࡪࠎࠥࠦࠠࠡࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡤࡹࡴࡳࡣࡷࡩ࡬ࡿ࠺ࠡࡵࡷࡶ࠱ࠦࡴࡦࡵࡷࠤࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡳࡵࡴࡤࡸࡪ࡭ࡹࠡࡰࡤࡱࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥὭ")
        self.config = config
        self.logger = logger
        self.bstack1lllllll1l1l_opy_ = bstack11ll11_opy_ (u"ࠥࡸࡪࡹࡴࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡲ࡯࡭ࡹ࠳ࡴࡦࡵࡷࡷࠧὮ")
        self.bstack1llllll1lll1_opy_ = None
        self.bstack1llllllll11l_opy_ = 60
        self.bstack1lllllll1lll_opy_ = 5
        self.bstack1llllllll1l1_opy_ = 0
    def bstack111l1lll111_opy_(self, test_files, orchestration_strategy):
        bstack11ll11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡋࡱ࡭ࡹ࡯ࡡࡵࡧࡶࠤࡹ࡮ࡥࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡲࡦࡳࡸࡩࡸࡺࠠࡢࡰࡧࠤࡸࡺ࡯ࡳࡧࡶࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡶ࡯࡭࡮࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦὯ")
        self.logger.debug(bstack11ll11_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡎࡴࡩࡵ࡫ࡤࡸ࡮ࡴࡧࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡷࡪࡶ࡫ࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࡀࠠࡼࡿࠥὰ").format(orchestration_strategy))
        try:
            payload = {
                bstack11ll11_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧά"): [{bstack11ll11_opy_ (u"ࠢࡧ࡫࡯ࡩࡕࡧࡴࡩࠤὲ"): f} for f in test_files],
                bstack11ll11_opy_ (u"ࠣࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡔࡶࡵࡥࡹ࡫ࡧࡺࠤέ"): orchestration_strategy,
                bstack11ll11_opy_ (u"ࠤࡱࡳࡩ࡫ࡉ࡯ࡦࡨࡼࠧὴ"): int(os.environ.get(bstack11ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡑࡓࡉࡋ࡟ࡊࡐࡇࡉ࡝ࠨή")) or bstack11ll11_opy_ (u"ࠦ࠵ࠨὶ")),
                bstack11ll11_opy_ (u"ࠧࡺ࡯ࡵࡣ࡯ࡒࡴࡪࡥࡴࠤί"): int(os.environ.get(bstack11ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡏࡕࡃࡏࡣࡓࡕࡄࡆࡡࡆࡓ࡚ࡔࡔࠣὸ")) or bstack11ll11_opy_ (u"ࠢ࠲ࠤό")),
                bstack11ll11_opy_ (u"ࠣࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠨὺ"): self.config.get(bstack11ll11_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧύ"), bstack11ll11_opy_ (u"ࠪࠫὼ")),
                bstack11ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠢώ"): self.config.get(bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ὾"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack11ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡗࡻ࡮ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦ὿"): os.environ.get(bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ᾀ"), None),
                bstack11ll11_opy_ (u"ࠣࡪࡲࡷࡹࡏ࡮ࡧࡱࠥᾁ"): get_host_info(),
            }
            self.logger.debug(bstack11ll11_opy_ (u"ࠤ࡞ࡷࡵࡲࡩࡵࡖࡨࡷࡹࡹ࡝ࠡࡕࡨࡲࡩ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࡀࠠࡼࡿࠥᾂ").format(payload))
            response = bstack11ll1l11111_opy_.bstack111111l1lll_opy_(self.bstack1lllllll1l1l_opy_, payload)
            if response:
                self.bstack1llllll1lll1_opy_ = self._1lllllll11ll_opy_(response)
                self.logger.debug(bstack11ll11_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡖࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨᾃ").format(self.bstack1llllll1lll1_opy_))
            else:
                self.logger.error(bstack11ll11_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡶࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࠦᾄ"))
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡴࡤࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳ࠻࠼ࠣࡿࢂࠨᾅ").format(e))
    def _1lllllll11ll_opy_(self, response):
        bstack11ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡃࡓࡍࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠠࡢࡰࡧࠤࡪࡾࡴࡳࡣࡦࡸࡸࠦࡲࡦ࡮ࡨࡺࡦࡴࡴࠡࡨ࡬ࡩࡱࡪࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᾆ")
        bstack1ll111lll_opy_ = {}
        bstack1ll111lll_opy_[bstack11ll11_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣᾇ")] = response.get(bstack11ll11_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤᾈ"), self.bstack1llllllll11l_opy_)
        bstack1ll111lll_opy_[bstack11ll11_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡌࡲࡹ࡫ࡲࡷࡣ࡯ࠦᾉ")] = response.get(bstack11ll11_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࡍࡳࡺࡥࡳࡸࡤࡰࠧᾊ"), self.bstack1lllllll1lll_opy_)
        bstack1lllllll1l11_opy_ = response.get(bstack11ll11_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢᾋ"))
        bstack1lllllll11l1_opy_ = response.get(bstack11ll11_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹ࡛ࡲ࡭ࠤᾌ"))
        if bstack1lllllll1l11_opy_:
            bstack1ll111lll_opy_[bstack11ll11_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹ࡛ࡲ࡭ࠤᾍ")] = bstack1lllllll1l11_opy_.split(bstack11l1ll1ll11_opy_ + bstack11ll11_opy_ (u"ࠢ࠰ࠤᾎ"))[1] if bstack11l1ll1ll11_opy_ + bstack11ll11_opy_ (u"ࠣ࠱ࠥᾏ") in bstack1lllllll1l11_opy_ else bstack1lllllll1l11_opy_
        else:
            bstack1ll111lll_opy_[bstack11ll11_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡗࡵࡰࠧᾐ")] = None
        if bstack1lllllll11l1_opy_:
            bstack1ll111lll_opy_[bstack11ll11_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷ࡙ࡷࡲࠢᾑ")] = bstack1lllllll11l1_opy_.split(bstack11l1ll1ll11_opy_ + bstack11ll11_opy_ (u"ࠦ࠴ࠨᾒ"))[1] if bstack11l1ll1ll11_opy_ + bstack11ll11_opy_ (u"ࠧ࠵ࠢᾓ") in bstack1lllllll11l1_opy_ else bstack1lllllll11l1_opy_
        else:
            bstack1ll111lll_opy_[bstack11ll11_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡕࡳ࡮ࠥᾔ")] = None
        if (
            response.get(bstack11ll11_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣᾕ")) is None or
            response.get(bstack11ll11_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡋࡱࡸࡪࡸࡶࡢ࡮ࠥᾖ")) is None or
            response.get(bstack11ll11_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡘࡶࡱࠨᾗ")) is None or
            response.get(bstack11ll11_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡘࡶࡱࠨᾘ")) is None
        ):
            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡠࡶࡲࡰࡥࡨࡷࡸࡥࡳࡱ࡮࡬ࡸࡤࡺࡥࡴࡶࡶࡣࡷ࡫ࡳࡱࡱࡱࡷࡪࡣࠠࡓࡧࡦࡩ࡮ࡼࡥࡥࠢࡱࡹࡱࡲࠠࡷࡣ࡯ࡹࡪ࠮ࡳࠪࠢࡩࡳࡷࠦࡳࡰ࡯ࡨࠤࡦࡺࡴࡳ࡫ࡥࡹࡹ࡫ࡳࠡ࡫ࡱࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡄࡔࡎࠦࡲࡦࡵࡳࡳࡳࡹࡥࠣᾙ"))
        return bstack1ll111lll_opy_
    def bstack111l1llllll_opy_(self):
        if not self.bstack1llllll1lll1_opy_:
            self.logger.error(bstack11ll11_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡎࡰࠢࡵࡩࡶࡻࡥࡴࡶࠣࡨࡦࡺࡡࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦ࡯ࡳࡦࡨࡶࡪࡪࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶ࠲ࠧᾚ"))
            return None
        bstack1lllllll1ll1_opy_ = None
        test_files = []
        bstack1lllllll111l_opy_ = int(time.time() * 1000) # bstack1llllllll111_opy_ sec
        bstack1lllllll1111_opy_ = int(self.bstack1llllll1lll1_opy_.get(bstack11ll11_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠣᾛ"), self.bstack1lllllll1lll_opy_))
        bstack1llllll1llll_opy_ = int(self.bstack1llllll1lll1_opy_.get(bstack11ll11_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣᾜ"), self.bstack1llllllll11l_opy_)) * 1000
        bstack1lllllll11l1_opy_ = self.bstack1llllll1lll1_opy_.get(bstack11ll11_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧᾝ"), None)
        bstack1lllllll1l11_opy_ = self.bstack1llllll1lll1_opy_.get(bstack11ll11_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡗࡵࡰࠧᾞ"), None)
        if bstack1lllllll1l11_opy_ is None and bstack1lllllll11l1_opy_ is None:
            return None
        try:
            while bstack1lllllll1l11_opy_ and (time.time() * 1000 - bstack1lllllll111l_opy_) < bstack1llllll1llll_opy_:
                response = bstack11ll1l11111_opy_.bstack111111ll1ll_opy_(bstack1lllllll1l11_opy_, {})
                if response and response.get(bstack11ll11_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤᾟ")):
                    bstack1lllllll1ll1_opy_ = response.get(bstack11ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࠥᾠ"))
                self.bstack1llllllll1l1_opy_ += 1
                if bstack1lllllll1ll1_opy_:
                    break
                time.sleep(bstack1lllllll1111_opy_)
                self.logger.debug(bstack11ll11_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡆࡦࡶࡦ࡬࡮ࡴࡧࠡࡱࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࡳࠡࡨࡵࡳࡲࠦࡲࡦࡵࡸࡰࡹࠦࡕࡓࡎࠣࡥ࡫ࡺࡥࡳࠢࡺࡥ࡮ࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡼࡿࠣࡷࡪࡩ࡯࡯ࡦࡶ࠲ࠧᾡ").format(bstack1lllllll1111_opy_))
            if bstack1lllllll11l1_opy_ and not bstack1lllllll1ll1_opy_:
                self.logger.debug(bstack11ll11_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡇࡧࡷࡧ࡭࡯࡮ࡨࠢࡲࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࡴࠢࡩࡶࡴࡳࠠࡵ࡫ࡰࡩࡴࡻࡴࠡࡗࡕࡐࠧᾢ"))
                response = bstack11ll1l11111_opy_.bstack111111ll1ll_opy_(bstack1lllllll11l1_opy_, {})
                if response and response.get(bstack11ll11_opy_ (u"ࠢࡵࡧࡶࡸࡸࠨᾣ")):
                    bstack1lllllll1ll1_opy_ = response.get(bstack11ll11_opy_ (u"ࠣࡶࡨࡷࡹࡹࠢᾤ"))
            if bstack1lllllll1ll1_opy_ and len(bstack1lllllll1ll1_opy_) > 0:
                for bstack111lll1ll1_opy_ in bstack1lllllll1ll1_opy_:
                    file_path = bstack111lll1ll1_opy_.get(bstack11ll11_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡐࡢࡶ࡫ࠦᾥ"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1lllllll1ll1_opy_:
                return None
            self.logger.debug(bstack11ll11_opy_ (u"ࠥ࡟࡬࡫ࡴࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡠࠤࡔࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡵࡩࡨ࡫ࡩࡷࡧࡧ࠾ࠥࢁࡽࠣᾦ").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦ࡯ࡳࡦࡨࡶࡪࡪࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶ࠾ࠥࢁࡽࠣᾧ").format(e))
            return None
    def bstack111l1ll1lll_opy_(self):
        bstack11ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡸ࡭࡫ࠠࡤࡱࡸࡲࡹࠦ࡯ࡧࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡂࡒࡌࠤࡨࡧ࡬࡭ࡵࠣࡱࡦࡪࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᾨ")
        return self.bstack1llllllll1l1_opy_