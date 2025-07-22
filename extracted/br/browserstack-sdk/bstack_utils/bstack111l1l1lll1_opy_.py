# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import os
import time
from bstack_utils.bstack11ll111llll_opy_ import bstack11ll111lll1_opy_
from bstack_utils.constants import bstack11l1lllll1l_opy_
from bstack_utils.helper import get_host_info
class bstack111l1l1l1ll_opy_:
    bstack111l111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡈࡢࡰࡧࡰࡪࡹࠠࡵࡧࡶࡸࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡺࡨࡦࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡵࡨࡶࡻ࡫ࡲ࠯ࠌࠣࠤࠥࠦࠢࠣࠤΐ")
    def __init__(self, config, logger):
        bstack111l111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࡪࡩࡤࡶ࠯ࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡦࡳࡳ࡬ࡩࡨࠌࠣࠤࠥࠦࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡢࡷࡹࡸࡡࡵࡧࡪࡽ࠿ࠦࡳࡵࡴ࠯ࠤࡹ࡫ࡳࡵࠢࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࠦ࡮ࡢ࡯ࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ῔")
        self.config = config
        self.logger = logger
        self.bstack1llllll1l1l1_opy_ = bstack111l111_opy_ (u"ࠣࡶࡨࡷࡹࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡰ࡭࡫ࡷ࠱ࡹ࡫ࡳࡵࡵࠥ῕")
        self.bstack1llllll11l1l_opy_ = None
        self.bstack1llllll11ll1_opy_ = 60
        self.bstack1llllll1ll1l_opy_ = 5
        self.bstack1llllll111l1_opy_ = 0
    def bstack111l1l11lll_opy_(self, test_files, orchestration_strategy):
        bstack111l111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡉ࡯࡫ࡷ࡭ࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡧ࡮ࡥࠢࡶࡸࡴࡸࡥࡴࠢࡷ࡬ࡪࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡴࡴࡲ࡬ࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤῖ")
        self.logger.debug(bstack111l111_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡌࡲ࡮ࡺࡩࡢࡶ࡬ࡲ࡬ࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡼ࡯ࡴࡩࠢࡶࡸࡷࡧࡴࡦࡩࡼ࠾ࠥࢁࡽࠣῗ").format(orchestration_strategy))
        try:
            payload = {
                bstack111l111_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࠥῘ"): [{bstack111l111_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡓࡥࡹ࡮ࠢῙ"): f} for f in test_files],
                bstack111l111_opy_ (u"ࠨ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࡙ࡴࡳࡣࡷࡩ࡬ࡿࠢῚ"): orchestration_strategy,
                bstack111l111_opy_ (u"ࠢ࡯ࡱࡧࡩࡎࡴࡤࡦࡺࠥΊ"): int(os.environ.get(bstack111l111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡏࡎࡅࡇ࡛ࠦ῜")) or bstack111l111_opy_ (u"ࠤ࠳ࠦ῝")),
                bstack111l111_opy_ (u"ࠥࡸࡴࡺࡡ࡭ࡐࡲࡨࡪࡹࠢ῞"): int(os.environ.get(bstack111l111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡔ࡚ࡁࡍࡡࡑࡓࡉࡋ࡟ࡄࡑࡘࡒ࡙ࠨ῟")) or bstack111l111_opy_ (u"ࠧ࠷ࠢῠ")),
                bstack111l111_opy_ (u"ࠨࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠦῡ"): self.config.get(bstack111l111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬῢ"), bstack111l111_opy_ (u"ࠨࠩΰ")),
                bstack111l111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠧῤ"): self.config.get(bstack111l111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ῥ"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack111l111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡕࡹࡳࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤῦ"): os.environ.get(bstack111l111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫῧ"), None),
                bstack111l111_opy_ (u"ࠨࡨࡰࡵࡷࡍࡳ࡬࡯ࠣῨ"): get_host_info(),
            }
            self.logger.debug(bstack111l111_opy_ (u"ࠢ࡜ࡵࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࡢࠦࡓࡦࡰࡧ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶ࠾ࠥࢁࡽࠣῩ").format(payload))
            response = bstack11ll111lll1_opy_.bstack1111111l1l1_opy_(self.bstack1llllll1l1l1_opy_, payload)
            if response:
                self.bstack1llllll11l1l_opy_ = self._1llllll11l11_opy_(response)
                self.logger.debug(bstack111l111_opy_ (u"ࠣ࡝ࡶࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࡣࠠࡔࡲ࡯࡭ࡹࠦࡴࡦࡵࡷࡷࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦῪ").format(self.bstack1llllll11l1l_opy_))
            else:
                self.logger.error(bstack111l111_opy_ (u"ࠤ࡞ࡷࡵࡲࡩࡵࡖࡨࡷࡹࡹ࡝ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡬࡫ࡴࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠯ࠤΎ"))
        except Exception as e:
            self.logger.error(bstack111l111_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࡀ࠺ࠡࡽࢀࠦῬ").format(e))
    def _1llllll11l11_opy_(self, response):
        bstack111l111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡹ࡮ࡥࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡁࡑࡋࠣࡶࡪࡹࡰࡰࡰࡶࡩࠥࡧ࡮ࡥࠢࡨࡼࡹࡸࡡࡤࡶࡶࠤࡷ࡫࡬ࡦࡸࡤࡲࡹࠦࡦࡪࡧ࡯ࡨࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ῭")
        bstack11l1111l11_opy_ = {}
        bstack11l1111l11_opy_[bstack111l111_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࠨ΅")] = response.get(bstack111l111_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢ`"), self.bstack1llllll11ll1_opy_)
        bstack11l1111l11_opy_[bstack111l111_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡊࡰࡷࡩࡷࡼࡡ࡭ࠤ῰")] = response.get(bstack111l111_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡋࡱࡸࡪࡸࡶࡢ࡮ࠥ῱"), self.bstack1llllll1ll1l_opy_)
        bstack1llllll1ll11_opy_ = response.get(bstack111l111_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡗࡵࡰࠧῲ"))
        bstack1llllll11lll_opy_ = response.get(bstack111l111_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷ࡙ࡷࡲࠢῳ"))
        if bstack1llllll1ll11_opy_:
            bstack11l1111l11_opy_[bstack111l111_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢῴ")] = bstack1llllll1ll11_opy_.split(bstack11l1lllll1l_opy_ + bstack111l111_opy_ (u"ࠧ࠵ࠢ῵"))[1] if bstack11l1lllll1l_opy_ + bstack111l111_opy_ (u"ࠨ࠯ࠣῶ") in bstack1llllll1ll11_opy_ else bstack1llllll1ll11_opy_
        else:
            bstack11l1111l11_opy_[bstack111l111_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡕࡳ࡮ࠥῷ")] = None
        if bstack1llllll11lll_opy_:
            bstack11l1111l11_opy_[bstack111l111_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧῸ")] = bstack1llllll11lll_opy_.split(bstack11l1lllll1l_opy_ + bstack111l111_opy_ (u"ࠤ࠲ࠦΌ"))[1] if bstack11l1lllll1l_opy_ + bstack111l111_opy_ (u"ࠥ࠳ࠧῺ") in bstack1llllll11lll_opy_ else bstack1llllll11lll_opy_
        else:
            bstack11l1111l11_opy_[bstack111l111_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣΏ")] = None
        if (
            response.get(bstack111l111_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࠨῼ")) is None or
            response.get(bstack111l111_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠣ´")) is None or
            response.get(bstack111l111_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡖࡴ࡯ࠦ῾")) is None or
            response.get(bstack111l111_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡖࡴ࡯ࠦ῿")) is None
        ):
            self.logger.debug(bstack111l111_opy_ (u"ࠤ࡞ࡴࡷࡵࡣࡦࡵࡶࡣࡸࡶ࡬ࡪࡶࡢࡸࡪࡹࡴࡴࡡࡵࡩࡸࡶ࡯࡯ࡵࡨࡡࠥࡘࡥࡤࡧ࡬ࡺࡪࡪࠠ࡯ࡷ࡯ࡰࠥࡼࡡ࡭ࡷࡨࠬࡸ࠯ࠠࡧࡱࡵࠤࡸࡵ࡭ࡦࠢࡤࡸࡹࡸࡩࡣࡷࡷࡩࡸࠦࡩ࡯ࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡂࡒࡌࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨ "))
        return bstack11l1111l11_opy_
    def bstack111l1l1ll1l_opy_(self):
        if not self.bstack1llllll11l1l_opy_:
            self.logger.error(bstack111l111_opy_ (u"ࠥ࡟࡬࡫ࡴࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡠࠤࡓࡵࠠࡳࡧࡴࡹࡪࡹࡴࠡࡦࡤࡸࡦࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡴࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴ࠰ࠥ "))
            return None
        bstack1llllll111ll_opy_ = None
        test_files = []
        bstack1llllll1l1ll_opy_ = int(time.time() * 1000) # bstack1llllll1lll1_opy_ sec
        bstack1llllll1l111_opy_ = int(self.bstack1llllll11l1l_opy_.get(bstack111l111_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࡎࡴࡴࡦࡴࡹࡥࡱࠨ "), self.bstack1llllll1ll1l_opy_))
        bstack1llllll1l11l_opy_ = int(self.bstack1llllll11l1l_opy_.get(bstack111l111_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࠨ "), self.bstack1llllll11ll1_opy_)) * 1000
        bstack1llllll11lll_opy_ = self.bstack1llllll11l1l_opy_.get(bstack111l111_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡕࡳ࡮ࠥ "), None)
        bstack1llllll1ll11_opy_ = self.bstack1llllll11l1l_opy_.get(bstack111l111_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡕࡳ࡮ࠥ "), None)
        if bstack1llllll1ll11_opy_ is None and bstack1llllll11lll_opy_ is None:
            return None
        try:
            while bstack1llllll1ll11_opy_ and (time.time() * 1000 - bstack1llllll1l1ll_opy_) < bstack1llllll1l11l_opy_:
                response = bstack11ll111lll1_opy_.bstack1111111ll11_opy_(bstack1llllll1ll11_opy_, {})
                if response and response.get(bstack111l111_opy_ (u"ࠣࡶࡨࡷࡹࡹࠢ ")):
                    bstack1llllll111ll_opy_ = response.get(bstack111l111_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣ "))
                self.bstack1llllll111l1_opy_ += 1
                if bstack1llllll111ll_opy_:
                    break
                time.sleep(bstack1llllll1l111_opy_)
                self.logger.debug(bstack111l111_opy_ (u"ࠥ࡟࡬࡫ࡴࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡠࠤࡋ࡫ࡴࡤࡪ࡬ࡲ࡬ࠦ࡯ࡳࡦࡨࡶࡪࡪࠠࡵࡧࡶࡸࡸࠦࡦࡳࡱࡰࠤࡷ࡫ࡳࡶ࡮ࡷࠤ࡚ࡘࡌࠡࡣࡩࡸࡪࡸࠠࡸࡣ࡬ࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࢁࡽࠡࡵࡨࡧࡴࡴࡤࡴ࠰ࠥ ").format(bstack1llllll1l111_opy_))
            if bstack1llllll11lll_opy_ and not bstack1llllll111ll_opy_:
                self.logger.debug(bstack111l111_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡌࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡰࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࡹࠠࡧࡴࡲࡱࠥࡺࡩ࡮ࡧࡲࡹࡹࠦࡕࡓࡎࠥ "))
                response = bstack11ll111lll1_opy_.bstack1111111ll11_opy_(bstack1llllll11lll_opy_, {})
                if response and response.get(bstack111l111_opy_ (u"ࠧࡺࡥࡴࡶࡶࠦ ")):
                    bstack1llllll111ll_opy_ = response.get(bstack111l111_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧ​"))
            if bstack1llllll111ll_opy_ and len(bstack1llllll111ll_opy_) > 0:
                for bstack111ll1ll1l_opy_ in bstack1llllll111ll_opy_:
                    file_path = bstack111ll1ll1l_opy_.get(bstack111l111_opy_ (u"ࠢࡧ࡫࡯ࡩࡕࡧࡴࡩࠤ‌"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1llllll111ll_opy_:
                return None
            self.logger.debug(bstack111l111_opy_ (u"ࠣ࡝ࡪࡩࡹࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳ࡞ࠢࡒࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡳࡧࡦࡩ࡮ࡼࡥࡥ࠼ࠣࡿࢂࠨ‍").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack111l111_opy_ (u"ࠤ࡞࡫ࡪࡺࡏࡳࡦࡨࡶࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴ࡟ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤࡴࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴ࠼ࠣࡿࢂࠨ‎").format(e))
            return None
    def bstack111l1l1llll_opy_(self):
        bstack111l111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡶ࡫ࡩࠥࡩ࡯ࡶࡰࡷࠤࡴ࡬ࠠࡴࡲ࡯࡭ࡹࠦࡴࡦࡵࡷࡷࠥࡇࡐࡊࠢࡦࡥࡱࡲࡳࠡ࡯ࡤࡨࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ‏")
        return self.bstack1llllll111l1_opy_