# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import os
import time
from bstack_utils.bstack111l1lll11l_opy_ import bstack111l1llll11_opy_
from bstack_utils.constants import bstack111l11ll11l_opy_
from bstack_utils.helper import get_host_info, bstack1lllllllllll_opy_
class bstack1llll1llll1l_opy_:
    bstack1ll1lll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡉࡣࡱࡨࡱ࡫ࡳࠡࡶࡨࡷࡹࠦ࡯ࡳࡦࡨࡶ࡮ࡴࡧࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡴࡩࡧࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡶࡩࡷࡼࡥࡳ࠰ࠍࠤࠥࠦࠠࠣࠤࠥ┢")
    def __init__(self, config, logger):
        bstack1ll1lll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡤࡪࡥࡷ࠰ࠥࡺࡥࡴࡶࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡧࡴࡴࡦࡪࡩࠍࠤࠥࠦࠠࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡣࡸࡺࡲࡢࡶࡨ࡫ࡾࡀࠠࡴࡶࡵ࠰ࠥࡺࡥࡴࡶࠣࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡹࡴࡳࡣࡷࡩ࡬ࡿࠠ࡯ࡣࡰࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ┣")
        self.config = config
        self.logger = logger
        self.bstack1ll1ll1l1l1l_opy_ = bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡱ࡮࡬ࡸ࠲ࡺࡥࡴࡶࡶࠦ┤")
        self.bstack1ll1ll1l11ll_opy_ = None
        self.default_timeout = 60
        self.bstack1ll1ll1l1lll_opy_ = 5
        self.bstack1ll1ll1l1111_opy_ = 0
    def bstack1llll1ll1l1l_opy_(self, test_files, orchestration_strategy, orchestration_metadata={}):
        bstack1ll1lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡊࡰ࡬ࡸ࡮ࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡴࡲ࡯࡭ࡹࠦࡴࡦࡵࡷࡷࠥࡸࡥࡲࡷࡨࡷࡹࠦࡡ࡯ࡦࠣࡷࡹࡵࡲࡦࡵࠣࡸ࡭࡫ࠠࡳࡧࡶࡴࡴࡴࡳࡦࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡵࡵ࡬࡭࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ┥")
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡍࡳ࡯ࡴࡪࡣࡷ࡭ࡳ࡭ࠠࡴࡲ࡯࡭ࡹࠦࡴࡦࡵࡷࡷࠥࡽࡩࡵࡪࠣࡷࡹࡸࡡࡵࡧࡪࡽ࠿ࠦࡻࡾࠤ┦").format(orchestration_strategy))
        try:
            bstack1ll1ll11lll1_opy_ = []
            bstack1ll1lll_opy_ (u"ࠧࠨࠢࡘࡧࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥ࡬ࡥࡵࡥ࡫ࠤ࡬࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣ࡭ࡸࠦࡳࡰࡷࡵࡧࡪࠦࡩࡴࠢࡷࡽࡵ࡫ࠠࡰࡨࠣࡥࡷࡸࡡࡺࠢࡤࡲࡩࠦࡩࡵࠩࡶࠤࡪࡲࡥ࡮ࡧࡱࡸࡸࠦࡡࡳࡧࠣࡳ࡫ࠦࡴࡺࡲࡨࠤࡩ࡯ࡣࡵࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡧࡦࡥࡺࡹࡥࠡ࡫ࡱࠤࡹ࡮ࡡࡵࠢࡦࡥࡸ࡫ࠬࠡࡷࡶࡩࡷࠦࡨࡢࡵࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥࡳࡵ࡭ࡶ࡬࠱ࡷ࡫ࡰࡰࠢࡶࡳࡺࡸࡣࡦࠢࡺ࡭ࡹ࡮ࠠࡧࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࠠࡪࡰࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠤࠥࠦ┧")
            source = orchestration_metadata[bstack1ll1lll_opy_ (u"࠭ࡲࡶࡰࡢࡷࡲࡧࡲࡵࡡࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠬ┨")].get(bstack1ll1lll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ┩"), [])
            bstack1ll1ll1l11l1_opy_ = isinstance(source, list) and all(isinstance(src, dict) and src is not None for src in source) and len(source) > 0
            if orchestration_metadata[bstack1ll1lll_opy_ (u"ࠨࡴࡸࡲࡤࡹ࡭ࡢࡴࡷࡣࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠧ┪")].get(bstack1ll1lll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ┫"), False) and not bstack1ll1ll1l11l1_opy_:
                bstack1ll1ll11lll1_opy_ = bstack1lllllllllll_opy_(source) # bstack1ll1ll1l111l_opy_-repo is handled bstack1ll1ll11l1ll_opy_
            payload = {
                bstack1ll1lll_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤ┬"): [{bstack1ll1lll_opy_ (u"ࠦ࡫࡯࡬ࡦࡒࡤࡸ࡭ࠨ┭"): f} for f in test_files],
                bstack1ll1lll_opy_ (u"ࠧࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡘࡺࡲࡢࡶࡨ࡫ࡾࠨ┮"): orchestration_strategy,
                bstack1ll1lll_opy_ (u"ࠨ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡓࡥࡵࡣࡧࡥࡹࡧࠢ┯"): orchestration_metadata,
                bstack1ll1lll_opy_ (u"ࠢ࡯ࡱࡧࡩࡎࡴࡤࡦࡺࠥ┰"): int(os.environ.get(bstack1ll1lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡏࡎࡅࡇ࡛ࠦ┱")) or bstack1ll1lll_opy_ (u"ࠤ࠳ࠦ┲")),
                bstack1ll1lll_opy_ (u"ࠥࡸࡴࡺࡡ࡭ࡐࡲࡨࡪࡹࠢ┳"): int(os.environ.get(bstack1ll1lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡔ࡚ࡁࡍࡡࡑࡓࡉࡋ࡟ࡄࡑࡘࡒ࡙ࠨ┴")) or bstack1ll1lll_opy_ (u"ࠧ࠷ࠢ┵")),
                bstack1ll1lll_opy_ (u"ࠨࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠦ┶"): self.config.get(bstack1ll1lll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ┷"), bstack1ll1lll_opy_ (u"ࠨࠩ┸")),
                bstack1ll1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠧ┹"): self.config.get(bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭┺"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1ll1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡕࡹࡳࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤ┻"): os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠦ┼"), bstack1ll1lll_opy_ (u"ࠨࠢ┽")),
                bstack1ll1lll_opy_ (u"ࠢࡩࡱࡶࡸࡎࡴࡦࡰࠤ┾"): get_host_info(),
                bstack1ll1lll_opy_ (u"ࠣࡲࡵࡈࡪࡺࡡࡪ࡮ࡶࠦ┿"): bstack1ll1ll11lll1_opy_
            }
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤ࡞ࡷࡵࡲࡩࡵࡖࡨࡷࡹࡹ࡝ࠡࡕࡨࡲࡩ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࡀࠠࡼࡿࠥ╀").format(payload))
            response = bstack111l1llll11_opy_.bstack1ll1llllll11_opy_(self.bstack1ll1ll1l1l1l_opy_, payload)
            if response:
                self.bstack1ll1ll1l11ll_opy_ = self._1ll1ll1ll1l1_opy_(response)
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡖࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ╁").format(self.bstack1ll1ll1l11ll_opy_))
            else:
                self.logger.error(bstack1ll1lll_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡶࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࠦ╂"))
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡴࡤࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳ࠻࠼ࠣࡿࢂࠨ╃").format(e))
    def _1ll1ll1ll1l1_opy_(self, response):
        bstack1ll1lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡃࡓࡍࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠠࡢࡰࡧࠤࡪࡾࡴࡳࡣࡦࡸࡸࠦࡲࡦ࡮ࡨࡺࡦࡴࡴࠡࡨ࡬ࡩࡱࡪࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ╄")
        bstack11lll11l1l_opy_ = {}
        bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣ╅")] = response.get(bstack1ll1lll_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ╆"), self.default_timeout)
        bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡌࡲࡹ࡫ࡲࡷࡣ࡯ࠦ╇")] = response.get(bstack1ll1lll_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࡍࡳࡺࡥࡳࡸࡤࡰࠧ╈"), self.bstack1ll1ll1l1lll_opy_)
        bstack1ll1ll1l1ll1_opy_ = response.get(bstack1ll1lll_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢ╉"))
        bstack1ll1ll1l1l11_opy_ = response.get(bstack1ll1lll_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹ࡛ࡲ࡭ࠤ╊"))
        if bstack1ll1ll1l1ll1_opy_:
            bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹ࡛ࡲ࡭ࠤ╋")] = bstack1ll1ll1l1ll1_opy_.split(bstack111l11ll11l_opy_ + bstack1ll1lll_opy_ (u"ࠢ࠰ࠤ╌"))[1] if bstack111l11ll11l_opy_ + bstack1ll1lll_opy_ (u"ࠣ࠱ࠥ╍") in bstack1ll1ll1l1ll1_opy_ else bstack1ll1ll1l1ll1_opy_
        else:
            bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡗࡵࡰࠧ╎")] = None
        if bstack1ll1ll1l1l11_opy_:
            bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷ࡙ࡷࡲࠢ╏")] = bstack1ll1ll1l1l11_opy_.split(bstack111l11ll11l_opy_ + bstack1ll1lll_opy_ (u"ࠦ࠴ࠨ═"))[1] if bstack111l11ll11l_opy_ + bstack1ll1lll_opy_ (u"ࠧ࠵ࠢ║") in bstack1ll1ll1l1l11_opy_ else bstack1ll1ll1l1l11_opy_
        else:
            bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡕࡳ࡮ࠥ╒")] = None
        if (
            response.get(bstack1ll1lll_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣ╓")) is None or
            response.get(bstack1ll1lll_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡋࡱࡸࡪࡸࡶࡢ࡮ࠥ╔")) is None or
            response.get(bstack1ll1lll_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡘࡶࡱࠨ╕")) is None or
            response.get(bstack1ll1lll_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡘࡶࡱࠨ╖")) is None
        ):
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡠࡶࡲࡰࡥࡨࡷࡸࡥࡳࡱ࡮࡬ࡸࡤࡺࡥࡴࡶࡶࡣࡷ࡫ࡳࡱࡱࡱࡷࡪࡣࠠࡓࡧࡦࡩ࡮ࡼࡥࡥࠢࡱࡹࡱࡲࠠࡷࡣ࡯ࡹࡪ࠮ࡳࠪࠢࡩࡳࡷࠦࡳࡰ࡯ࡨࠤࡦࡺࡴࡳ࡫ࡥࡹࡹ࡫ࡳࠡ࡫ࡱࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡄࡔࡎࠦࡲࡦࡵࡳࡳࡳࡹࡥࠣ╗"))
        return bstack11lll11l1l_opy_
    def bstack1lllll111111_opy_(self):
        if not self.bstack1ll1ll1l11ll_opy_:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡎࡰࠢࡵࡩࡶࡻࡥࡴࡶࠣࡨࡦࡺࡡࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦ࡯ࡳࡦࡨࡶࡪࡪࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶ࠲ࠧ╘"))
            return None
        bstack1ll1ll1ll11l_opy_ = None
        test_files = []
        bstack1ll1ll1ll111_opy_ = int(time.time() * 1000) # bstack1ll1ll11ll11_opy_ sec
        bstack1ll1ll11ll1l_opy_ = int(self.bstack1ll1ll1l11ll_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠣ╙"), self.bstack1ll1ll1l1lll_opy_))
        bstack1ll1ll11llll_opy_ = int(self.bstack1ll1ll1l11ll_opy_.get(bstack1ll1lll_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣ╚"), self.default_timeout)) * 1000
        bstack1ll1ll1l1l11_opy_ = self.bstack1ll1ll1l11ll_opy_.get(bstack1ll1lll_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧ╛"), None)
        bstack1ll1ll1l1ll1_opy_ = self.bstack1ll1ll1l11ll_opy_.get(bstack1ll1lll_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡗࡵࡰࠧ╜"), None)
        if bstack1ll1ll1l1ll1_opy_ is None and bstack1ll1ll1l1l11_opy_ is None:
            return None
        try:
            while bstack1ll1ll1l1ll1_opy_ and (time.time() * 1000 - bstack1ll1ll1ll111_opy_) < bstack1ll1ll11llll_opy_:
                response = bstack111l1llll11_opy_.bstack1ll1lllll1ll_opy_(bstack1ll1ll1l1ll1_opy_, {})
                if response and response.get(bstack1ll1lll_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤ╝")):
                    bstack1ll1ll1ll11l_opy_ = response.get(bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࠥ╞"))
                self.bstack1ll1ll1l1111_opy_ += 1
                if bstack1ll1ll1ll11l_opy_:
                    break
                time.sleep(bstack1ll1ll11ll1l_opy_)
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡆࡦࡶࡦ࡬࡮ࡴࡧࠡࡱࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࡳࠡࡨࡵࡳࡲࠦࡲࡦࡵࡸࡰࡹࠦࡕࡓࡎࠣࡥ࡫ࡺࡥࡳࠢࡺࡥ࡮ࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡼࡿࠣࡷࡪࡩ࡯࡯ࡦࡶ࠲ࠧ╟").format(bstack1ll1ll11ll1l_opy_))
            if bstack1ll1ll1l1l11_opy_ and not bstack1ll1ll1ll11l_opy_:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡇࡧࡷࡧ࡭࡯࡮ࡨࠢࡲࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࡴࠢࡩࡶࡴࡳࠠࡵ࡫ࡰࡩࡴࡻࡴࠡࡗࡕࡐࠧ╠"))
                response = bstack111l1llll11_opy_.bstack1ll1lllll1ll_opy_(bstack1ll1ll1l1l11_opy_, {})
                if response and response.get(bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡸࠨ╡")):
                    bstack1ll1ll1ll11l_opy_ = response.get(bstack1ll1lll_opy_ (u"ࠣࡶࡨࡷࡹࡹࠢ╢"))
            if bstack1ll1ll1ll11l_opy_ and len(bstack1ll1ll1ll11l_opy_) > 0:
                for test_data in bstack1ll1ll1ll11l_opy_:
                    file_path = test_data.get(bstack1ll1lll_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡐࡢࡶ࡫ࠦ╣"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1ll1ll1ll11l_opy_:
                return None
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥ࡟࡬࡫ࡴࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡠࠤࡔࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡵࡩࡨ࡫ࡩࡷࡧࡧ࠾ࠥࢁࡽࠣ╤").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦ࡯ࡳࡦࡨࡶࡪࡪࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶ࠾ࠥࢁࡽࠣ╥").format(e))
            return None
    def bstack1llll1lll1ll_opy_(self):
        bstack1ll1lll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡸ࡭࡫ࠠࡤࡱࡸࡲࡹࠦ࡯ࡧࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡂࡒࡌࠤࡨࡧ࡬࡭ࡵࠣࡱࡦࡪࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ╦")
        return self.bstack1ll1ll1l1111_opy_