# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
import os
import time
from bstack_utils.bstack11ll11l1lll_opy_ import bstack11ll11ll11l_opy_
from bstack_utils.constants import bstack11ll1111lll_opy_
from bstack_utils.helper import get_host_info
class bstack111l1lll1ll_opy_:
    bstack1l1ll1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡈࡢࡰࡧࡰࡪࡹࠠࡵࡧࡶࡸࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡺࡨࡦࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡵࡨࡶࡻ࡫ࡲ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᾍ")
    def __init__(self, config, logger):
        bstack1l1ll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࡪࡩࡤࡶ࠯ࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡦࡳࡳ࡬ࡩࡨࠌࠣࠤࠥࠦࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡢࡷࡹࡸࡡࡵࡧࡪࡽ࠿ࠦࡳࡵࡴ࠯ࠤࡹ࡫ࡳࡵࠢࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࠦ࡮ࡢ࡯ࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᾎ")
        self.config = config
        self.logger = logger
        self.bstack1llllll1ll11_opy_ = bstack1l1ll1_opy_ (u"ࠣࡶࡨࡷࡹࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡰ࡭࡫ࡷ࠱ࡹ࡫ࡳࡵࡵࠥᾏ")
        self.bstack1lllllll1l11_opy_ = None
        self.bstack1llllll1l1l1_opy_ = 60
        self.bstack1llllll1l1ll_opy_ = 5
        self.bstack1lllllll11ll_opy_ = 0
    def bstack111l1ll11ll_opy_(self, test_files, orchestration_strategy):
        bstack1l1ll1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡉ࡯࡫ࡷ࡭ࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡧ࡮ࡥࠢࡶࡸࡴࡸࡥࡴࠢࡷ࡬ࡪࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡴࡴࡲ࡬ࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᾐ")
        self.logger.debug(bstack1l1ll1_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡌࡲ࡮ࡺࡩࡢࡶ࡬ࡲ࡬ࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡼ࡯ࡴࡩࠢࡶࡸࡷࡧࡴࡦࡩࡼ࠾ࠥࢁࡽࠣᾑ").format(orchestration_strategy))
        try:
            payload = {
                bstack1l1ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࠥᾒ"): [{bstack1l1ll1_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡓࡥࡹ࡮ࠢᾓ"): f} for f in test_files],
                bstack1l1ll1_opy_ (u"ࠨ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࡙ࡴࡳࡣࡷࡩ࡬ࡿࠢᾔ"): orchestration_strategy,
                bstack1l1ll1_opy_ (u"ࠢ࡯ࡱࡧࡩࡎࡴࡤࡦࡺࠥᾕ"): int(os.environ.get(bstack1l1ll1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡏࡎࡅࡇ࡛ࠦᾖ")) or bstack1l1ll1_opy_ (u"ࠤ࠳ࠦᾗ")),
                bstack1l1ll1_opy_ (u"ࠥࡸࡴࡺࡡ࡭ࡐࡲࡨࡪࡹࠢᾘ"): int(os.environ.get(bstack1l1ll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡔ࡚ࡁࡍࡡࡑࡓࡉࡋ࡟ࡄࡑࡘࡒ࡙ࠨᾙ")) or bstack1l1ll1_opy_ (u"ࠧ࠷ࠢᾚ")),
                bstack1l1ll1_opy_ (u"ࠨࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠦᾛ"): self.config.get(bstack1l1ll1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᾜ"), bstack1l1ll1_opy_ (u"ࠨࠩᾝ")),
                bstack1l1ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠧᾞ"): self.config.get(bstack1l1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᾟ"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1l1ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡕࡹࡳࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤᾠ"): os.environ.get(bstack1l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫᾡ"), None),
                bstack1l1ll1_opy_ (u"ࠨࡨࡰࡵࡷࡍࡳ࡬࡯ࠣᾢ"): get_host_info(),
            }
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠢ࡜ࡵࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࡢࠦࡓࡦࡰࡧ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶ࠾ࠥࢁࡽࠣᾣ").format(payload))
            response = bstack11ll11ll11l_opy_.bstack111111l11ll_opy_(self.bstack1llllll1ll11_opy_, payload)
            if response:
                self.bstack1lllllll1l11_opy_ = self._1llllll1lll1_opy_(response)
                self.logger.debug(bstack1l1ll1_opy_ (u"ࠣ࡝ࡶࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࡣࠠࡔࡲ࡯࡭ࡹࠦࡴࡦࡵࡷࡷࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦᾤ").format(self.bstack1lllllll1l11_opy_))
            else:
                self.logger.error(bstack1l1ll1_opy_ (u"ࠤ࡞ࡷࡵࡲࡩࡵࡖࡨࡷࡹࡹ࡝ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡬࡫ࡴࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠯ࠤᾥ"))
        except Exception as e:
            self.logger.error(bstack1l1ll1_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࡀ࠺ࠡࡽࢀࠦᾦ").format(e))
    def _1llllll1lll1_opy_(self, response):
        bstack1l1ll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡹ࡮ࡥࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡁࡑࡋࠣࡶࡪࡹࡰࡰࡰࡶࡩࠥࡧ࡮ࡥࠢࡨࡼࡹࡸࡡࡤࡶࡶࠤࡷ࡫࡬ࡦࡸࡤࡲࡹࠦࡦࡪࡧ࡯ࡨࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᾧ")
        bstack111lll1l_opy_ = {}
        bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࠨᾨ")] = response.get(bstack1l1ll1_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢᾩ"), self.bstack1llllll1l1l1_opy_)
        bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡊࡰࡷࡩࡷࡼࡡ࡭ࠤᾪ")] = response.get(bstack1l1ll1_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡋࡱࡸࡪࡸࡶࡢ࡮ࠥᾫ"), self.bstack1llllll1l1ll_opy_)
        bstack1llllll1ll1l_opy_ = response.get(bstack1l1ll1_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡗࡵࡰࠧᾬ"))
        bstack1lllllll111l_opy_ = response.get(bstack1l1ll1_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷ࡙ࡷࡲࠢᾭ"))
        if bstack1llllll1ll1l_opy_:
            bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢᾮ")] = bstack1llllll1ll1l_opy_.split(bstack11ll1111lll_opy_ + bstack1l1ll1_opy_ (u"ࠧ࠵ࠢᾯ"))[1] if bstack11ll1111lll_opy_ + bstack1l1ll1_opy_ (u"ࠨ࠯ࠣᾰ") in bstack1llllll1ll1l_opy_ else bstack1llllll1ll1l_opy_
        else:
            bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡕࡳ࡮ࠥᾱ")] = None
        if bstack1lllllll111l_opy_:
            bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧᾲ")] = bstack1lllllll111l_opy_.split(bstack11ll1111lll_opy_ + bstack1l1ll1_opy_ (u"ࠤ࠲ࠦᾳ"))[1] if bstack11ll1111lll_opy_ + bstack1l1ll1_opy_ (u"ࠥ࠳ࠧᾴ") in bstack1lllllll111l_opy_ else bstack1lllllll111l_opy_
        else:
            bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣ᾵")] = None
        if (
            response.get(bstack1l1ll1_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࠨᾶ")) is None or
            response.get(bstack1l1ll1_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠣᾷ")) is None or
            response.get(bstack1l1ll1_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡖࡴ࡯ࠦᾸ")) is None or
            response.get(bstack1l1ll1_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡖࡴ࡯ࠦᾹ")) is None
        ):
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠤ࡞ࡴࡷࡵࡣࡦࡵࡶࡣࡸࡶ࡬ࡪࡶࡢࡸࡪࡹࡴࡴࡡࡵࡩࡸࡶ࡯࡯ࡵࡨࡡࠥࡘࡥࡤࡧ࡬ࡺࡪࡪࠠ࡯ࡷ࡯ࡰࠥࡼࡡ࡭ࡷࡨࠬࡸ࠯ࠠࡧࡱࡵࠤࡸࡵ࡭ࡦࠢࡤࡸࡹࡸࡩࡣࡷࡷࡩࡸࠦࡩ࡯ࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡂࡒࡌࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨᾺ"))
        return bstack111lll1l_opy_
    def bstack111l1ll111l_opy_(self):
        if not self.bstack1lllllll1l11_opy_:
            self.logger.error(bstack1l1ll1_opy_ (u"ࠥ࡟࡬࡫ࡴࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡠࠤࡓࡵࠠࡳࡧࡴࡹࡪࡹࡴࠡࡦࡤࡸࡦࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡴࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴ࠰ࠥΆ"))
            return None
        bstack1llllll1l11l_opy_ = None
        test_files = []
        bstack1llllll1llll_opy_ = int(time.time() * 1000) # bstack1lllllll11l1_opy_ sec
        bstack1lllllll1l1l_opy_ = int(self.bstack1lllllll1l11_opy_.get(bstack1l1ll1_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࡎࡴࡴࡦࡴࡹࡥࡱࠨᾼ"), self.bstack1llllll1l1ll_opy_))
        bstack1lllllll1111_opy_ = int(self.bstack1lllllll1l11_opy_.get(bstack1l1ll1_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࠨ᾽"), self.bstack1llllll1l1l1_opy_)) * 1000
        bstack1lllllll111l_opy_ = self.bstack1lllllll1l11_opy_.get(bstack1l1ll1_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡕࡳ࡮ࠥι"), None)
        bstack1llllll1ll1l_opy_ = self.bstack1lllllll1l11_opy_.get(bstack1l1ll1_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡕࡳ࡮ࠥ᾿"), None)
        if bstack1llllll1ll1l_opy_ is None and bstack1lllllll111l_opy_ is None:
            return None
        try:
            while bstack1llllll1ll1l_opy_ and (time.time() * 1000 - bstack1llllll1llll_opy_) < bstack1lllllll1111_opy_:
                response = bstack11ll11ll11l_opy_.bstack111111l1lll_opy_(bstack1llllll1ll1l_opy_, {})
                if response and response.get(bstack1l1ll1_opy_ (u"ࠣࡶࡨࡷࡹࡹࠢ῀")):
                    bstack1llllll1l11l_opy_ = response.get(bstack1l1ll1_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣ῁"))
                self.bstack1lllllll11ll_opy_ += 1
                if bstack1llllll1l11l_opy_:
                    break
                time.sleep(bstack1lllllll1l1l_opy_)
                self.logger.debug(bstack1l1ll1_opy_ (u"ࠥ࡟࡬࡫ࡴࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡠࠤࡋ࡫ࡴࡤࡪ࡬ࡲ࡬ࠦ࡯ࡳࡦࡨࡶࡪࡪࠠࡵࡧࡶࡸࡸࠦࡦࡳࡱࡰࠤࡷ࡫ࡳࡶ࡮ࡷࠤ࡚ࡘࡌࠡࡣࡩࡸࡪࡸࠠࡸࡣ࡬ࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࢁࡽࠡࡵࡨࡧࡴࡴࡤࡴ࠰ࠥῂ").format(bstack1lllllll1l1l_opy_))
            if bstack1lllllll111l_opy_ and not bstack1llllll1l11l_opy_:
                self.logger.debug(bstack1l1ll1_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡌࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡰࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࡹࠠࡧࡴࡲࡱࠥࡺࡩ࡮ࡧࡲࡹࡹࠦࡕࡓࡎࠥῃ"))
                response = bstack11ll11ll11l_opy_.bstack111111l1lll_opy_(bstack1lllllll111l_opy_, {})
                if response and response.get(bstack1l1ll1_opy_ (u"ࠧࡺࡥࡴࡶࡶࠦῄ")):
                    bstack1llllll1l11l_opy_ = response.get(bstack1l1ll1_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧ῅"))
            if bstack1llllll1l11l_opy_ and len(bstack1llllll1l11l_opy_) > 0:
                for bstack111llll1l1_opy_ in bstack1llllll1l11l_opy_:
                    file_path = bstack111llll1l1_opy_.get(bstack1l1ll1_opy_ (u"ࠢࡧ࡫࡯ࡩࡕࡧࡴࡩࠤῆ"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1llllll1l11l_opy_:
                return None
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠣ࡝ࡪࡩࡹࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳ࡞ࠢࡒࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡳࡧࡦࡩ࡮ࡼࡥࡥ࠼ࠣࡿࢂࠨῇ").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack1l1ll1_opy_ (u"ࠤ࡞࡫ࡪࡺࡏࡳࡦࡨࡶࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴ࡟ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤࡴࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴ࠼ࠣࡿࢂࠨῈ").format(e))
            return None
    def bstack111l1ll1ll1_opy_(self):
        bstack1l1ll1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡶ࡫ࡩࠥࡩ࡯ࡶࡰࡷࠤࡴ࡬ࠠࡴࡲ࡯࡭ࡹࠦࡴࡦࡵࡷࡷࠥࡇࡐࡊࠢࡦࡥࡱࡲࡳࠡ࡯ࡤࡨࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦΈ")
        return self.bstack1lllllll11ll_opy_