# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import os
import time
from bstack_utils.bstack111llllll1l_opy_ import bstack111lllll1ll_opy_
from bstack_utils.constants import bstack111ll111lll_opy_
from bstack_utils.helper import get_host_info, bstack1111l1ll11l_opy_
class bstack11111111l11_opy_:
    bstack11l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡋࡥࡳࡪ࡬ࡦࡵࠣࡸࡪࡹࡴࠡࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡶ࡫ࡩࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡸ࡫ࡲࡷࡧࡵ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ⋟")
    def __init__(self, config, logger):
        bstack11l11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠࡤࡱࡱࡪ࡮࡭࠺ࠡࡦ࡬ࡧࡹ࠲ࠠࡵࡧࡶࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡩ࡯࡯ࡨ࡬࡫ࠏࠦࠠࠡࠢࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡥࡳࡵࡴࡤࡸࡪ࡭ࡹ࠻ࠢࡶࡸࡷ࠲ࠠࡵࡧࡶࡸࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡴࡶࡵࡥࡹ࡫ࡧࡺࠢࡱࡥࡲ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⋠")
        self.config = config
        self.logger = logger
        self.bstack1lll111l11ll_opy_ = bstack11l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡳࡰ࡮ࡺ࠭ࡵࡧࡶࡸࡸࠨ⋡")
        self.bstack1lll1111ll1l_opy_ = None
        self.bstack1lll111l1l1l_opy_ = 60
        self.bstack1lll111ll11l_opy_ = 5
        self.bstack1lll111l111l_opy_ = 0
    def bstack1lllllll1lll_opy_(self, test_files, orchestration_strategy, orchestration_metadata={}):
        bstack11l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡌࡲ࡮ࡺࡩࡢࡶࡨࡷࠥࡺࡨࡦࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡳࡧࡴࡹࡪࡹࡴࠡࡣࡱࡨࠥࡹࡴࡰࡴࡨࡷࠥࡺࡨࡦࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡰࡰ࡮࡯࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ⋢")
        self.logger.debug(bstack11l11_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡࠥࡏ࡮ࡪࡶ࡬ࡥࡹ࡯࡮ࡨࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡸ࡫ࡷ࡬ࠥࡹࡴࡳࡣࡷࡩ࡬ࡿ࠺ࠡࡽࢀࠦ⋣").format(orchestration_strategy))
        try:
            bstack1lll111l1111_opy_ = []
            bstack11l11_opy_ (u"ࠢࠣࠤ࡚ࡩࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡧࡧࡷࡧ࡭ࠦࡧࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥ࡯ࡳࠡࡵࡲࡹࡷࡩࡥࠡ࡫ࡶࠤࡹࡿࡰࡦࠢࡲࡪࠥࡧࡲࡳࡣࡼࠤࡦࡴࡤࠡ࡫ࡷࠫࡸࠦࡥ࡭ࡧࡰࡩࡳࡺࡳࠡࡣࡵࡩࠥࡵࡦࠡࡶࡼࡴࡪࠦࡤࡪࡥࡷࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡩࡨࡧࡵࡴࡧࠣ࡭ࡳࠦࡴࡩࡣࡷࠤࡨࡧࡳࡦ࠮ࠣࡹࡸ࡫ࡲࠡࡪࡤࡷࠥࡶࡲࡰࡸ࡬ࡨࡪࡪࠠ࡮ࡷ࡯ࡸ࡮࠳ࡲࡦࡲࡲࠤࡸࡵࡵࡳࡥࡨࠤࡼ࡯ࡴࡩࠢࡩࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࠢ࡬ࡲࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠦࠧࠨ⋤")
            source = orchestration_metadata[bstack11l11_opy_ (u"ࠨࡴࡸࡲࡤࡹ࡭ࡢࡴࡷࡣࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠧ⋥")].get(bstack11l11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ⋦"), [])
            bstack1lll1111ll11_opy_ = isinstance(source, list) and all(isinstance(src, dict) and src is not None for src in source) and len(source) > 0
            if orchestration_metadata[bstack11l11_opy_ (u"ࠪࡶࡺࡴ࡟ࡴ࡯ࡤࡶࡹࡥࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠩ⋧")].get(bstack11l11_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ⋨"), False) and not bstack1lll1111ll11_opy_:
                bstack1lll111l1111_opy_ = bstack1111l1ll11l_opy_(source) # bstack1lll111l11l1_opy_-repo is handled bstack1lll1111lll1_opy_
            payload = {
                bstack11l11_opy_ (u"ࠧࡺࡥࡴࡶࡶࠦ⋩"): [{bstack11l11_opy_ (u"ࠨࡦࡪ࡮ࡨࡔࡦࡺࡨࠣ⋪"): f} for f in test_files],
                bstack11l11_opy_ (u"ࠢࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡓࡵࡴࡤࡸࡪ࡭ࡹࠣ⋫"): orchestration_strategy,
                bstack11l11_opy_ (u"ࠣࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡎࡧࡷࡥࡩࡧࡴࡢࠤ⋬"): orchestration_metadata,
                bstack11l11_opy_ (u"ࠤࡱࡳࡩ࡫ࡉ࡯ࡦࡨࡼࠧ⋭"): int(os.environ.get(bstack11l11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡑࡓࡉࡋ࡟ࡊࡐࡇࡉ࡝ࠨ⋮")) or bstack11l11_opy_ (u"ࠦ࠵ࠨ⋯")),
                bstack11l11_opy_ (u"ࠧࡺ࡯ࡵࡣ࡯ࡒࡴࡪࡥࡴࠤ⋰"): int(os.environ.get(bstack11l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡏࡕࡃࡏࡣࡓࡕࡄࡆࡡࡆࡓ࡚ࡔࡔࠣ⋱")) or bstack11l11_opy_ (u"ࠢ࠲ࠤ⋲")),
                bstack11l11_opy_ (u"ࠣࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠨ⋳"): self.config.get(bstack11l11_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ⋴"), bstack11l11_opy_ (u"ࠪࠫ⋵")),
                bstack11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠢ⋶"): self.config.get(bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ⋷"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡗࡻ࡮ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦ⋸"): os.environ.get(bstack11l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗࠨ⋹"), bstack11l11_opy_ (u"ࠣࠤ⋺")),
                bstack11l11_opy_ (u"ࠤ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠦ⋻"): get_host_info(),
                bstack11l11_opy_ (u"ࠥࡴࡷࡊࡥࡵࡣ࡬ࡰࡸࠨ⋼"): bstack1lll111l1111_opy_
            }
            self.logger.debug(bstack11l11_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡗࡪࡴࡤࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳ࠻ࠢࡾࢁࠧ⋽").format(payload))
            response = bstack111lllll1ll_opy_.bstack1lll11ll1l1l_opy_(self.bstack1lll111l11ll_opy_, payload)
            if response:
                self.bstack1lll1111ll1l_opy_ = self._1lll1111l1l1_opy_(response)
                self.logger.debug(bstack11l11_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡘࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣ⋾").format(self.bstack1lll1111ll1l_opy_))
            else:
                self.logger.error(bstack11l11_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡩࡨࡸࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠳ࠨ⋿"))
        except Exception as e:
            self.logger.error(bstack11l11_opy_ (u"ࠢ࡜ࡵࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵ࠽࠾ࠥࢁࡽࠣ⌀").format(e))
    def _1lll1111l1l1_opy_(self, response):
        bstack11l11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡅࡕࡏࠠࡳࡧࡶࡴࡴࡴࡳࡦࠢࡤࡲࡩࠦࡥࡹࡶࡵࡥࡨࡺࡳࠡࡴࡨࡰࡪࡼࡡ࡯ࡶࠣࡪ࡮࡫࡬ࡥࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ⌁")
        bstack11lllll1_opy_ = {}
        bstack11lllll1_opy_[bstack11l11_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ⌂")] = response.get(bstack11l11_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦ⌃"), self.bstack1lll111l1l1l_opy_)
        bstack11lllll1_opy_[bstack11l11_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࡎࡴࡴࡦࡴࡹࡥࡱࠨ⌄")] = response.get(bstack11l11_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࡏ࡮ࡵࡧࡵࡺࡦࡲࠢ⌅"), self.bstack1lll111ll11l_opy_)
        bstack1lll111ll1l1_opy_ = response.get(bstack11l11_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹ࡛ࡲ࡭ࠤ⌆"))
        bstack1lll111l1ll1_opy_ = response.get(bstack11l11_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡖࡴ࡯ࠦ⌇"))
        if bstack1lll111ll1l1_opy_:
            bstack11lllll1_opy_[bstack11l11_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡖࡴ࡯ࠦ⌈")] = bstack1lll111ll1l1_opy_.split(bstack111ll111lll_opy_ + bstack11l11_opy_ (u"ࠤ࠲ࠦ⌉"))[1] if bstack111ll111lll_opy_ + bstack11l11_opy_ (u"ࠥ࠳ࠧ⌊") in bstack1lll111ll1l1_opy_ else bstack1lll111ll1l1_opy_
        else:
            bstack11lllll1_opy_[bstack11l11_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢ⌋")] = None
        if bstack1lll111l1ll1_opy_:
            bstack11lllll1_opy_[bstack11l11_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹ࡛ࡲ࡭ࠤ⌌")] = bstack1lll111l1ll1_opy_.split(bstack111ll111lll_opy_ + bstack11l11_opy_ (u"ࠨ࠯ࠣ⌍"))[1] if bstack111ll111lll_opy_ + bstack11l11_opy_ (u"ࠢ࠰ࠤ⌎") in bstack1lll111l1ll1_opy_ else bstack1lll111l1ll1_opy_
        else:
            bstack11lllll1_opy_[bstack11l11_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧ⌏")] = None
        if (
            response.get(bstack11l11_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ⌐")) is None or
            response.get(bstack11l11_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࡍࡳࡺࡥࡳࡸࡤࡰࠧ⌑")) is None or
            response.get(bstack11l11_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣ⌒")) is None or
            response.get(bstack11l11_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣ⌓")) is None
        ):
            self.logger.debug(bstack11l11_opy_ (u"ࠨ࡛ࡱࡴࡲࡧࡪࡹࡳࡠࡵࡳࡰ࡮ࡺ࡟ࡵࡧࡶࡸࡸࡥࡲࡦࡵࡳࡳࡳࡹࡥ࡞ࠢࡕࡩࡨ࡫ࡩࡷࡧࡧࠤࡳࡻ࡬࡭ࠢࡹࡥࡱࡻࡥࠩࡵࠬࠤ࡫ࡵࡲࠡࡵࡲࡱࡪࠦࡡࡵࡶࡵ࡭ࡧࡻࡴࡦࡵࠣ࡭ࡳࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡆࡖࡉࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠥ⌔"))
        return bstack11lllll1_opy_
    def bstack1llllllll111_opy_(self):
        if not self.bstack1lll1111ll1l_opy_:
            self.logger.error(bstack11l11_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡐࡲࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡪࡡࡵࡣࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡱࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸ࠴ࠢ⌕"))
            return None
        bstack1lll1111llll_opy_ = None
        test_files = []
        bstack1lll111ll111_opy_ = int(time.time() * 1000) # bstack1lll111l1l11_opy_ sec
        bstack1lll111l1lll_opy_ = int(self.bstack1lll1111ll1l_opy_.get(bstack11l11_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡋࡱࡸࡪࡸࡶࡢ࡮ࠥ⌖"), self.bstack1lll111ll11l_opy_))
        bstack1lll1111l1ll_opy_ = int(self.bstack1lll1111ll1l_opy_.get(bstack11l11_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ⌗"), self.bstack1lll111l1l1l_opy_)) * 1000
        bstack1lll111l1ll1_opy_ = self.bstack1lll1111ll1l_opy_.get(bstack11l11_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷ࡙ࡷࡲࠢ⌘"), None)
        bstack1lll111ll1l1_opy_ = self.bstack1lll1111ll1l_opy_.get(bstack11l11_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢ⌙"), None)
        if bstack1lll111ll1l1_opy_ is None and bstack1lll111l1ll1_opy_ is None:
            return None
        try:
            while bstack1lll111ll1l1_opy_ and (time.time() * 1000 - bstack1lll111ll111_opy_) < bstack1lll1111l1ll_opy_:
                response = bstack111lllll1ll_opy_.bstack1lll11lll1ll_opy_(bstack1lll111ll1l1_opy_, {})
                if response and response.get(bstack11l11_opy_ (u"ࠧࡺࡥࡴࡶࡶࠦ⌚")):
                    bstack1lll1111llll_opy_ = response.get(bstack11l11_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧ⌛"))
                self.bstack1lll111l111l_opy_ += 1
                if bstack1lll1111llll_opy_:
                    break
                time.sleep(bstack1lll111l1lll_opy_)
                self.logger.debug(bstack11l11_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡈࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡳࡷࡪࡥࡳࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡪࡷࡵ࡭ࠡࡴࡨࡷࡺࡲࡴࠡࡗࡕࡐࠥࡧࡦࡵࡧࡵࠤࡼࡧࡩࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡾࢁࠥࡹࡥࡤࡱࡱࡨࡸ࠴ࠢ⌜").format(bstack1lll111l1lll_opy_))
            if bstack1lll111l1ll1_opy_ and not bstack1lll1111llll_opy_:
                self.logger.debug(bstack11l11_opy_ (u"ࠣ࡝ࡪࡩࡹࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳ࡞ࠢࡉࡩࡹࡩࡨࡪࡰࡪࠤࡴࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡭ࡲ࡫࡯ࡶࡶ࡙ࠣࡗࡒࠢ⌝"))
                response = bstack111lllll1ll_opy_.bstack1lll11lll1ll_opy_(bstack1lll111l1ll1_opy_, {})
                if response and response.get(bstack11l11_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣ⌞")):
                    bstack1lll1111llll_opy_ = response.get(bstack11l11_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤ⌟"))
            if bstack1lll1111llll_opy_ and len(bstack1lll1111llll_opy_) > 0:
                for bstack11111lll1l_opy_ in bstack1lll1111llll_opy_:
                    file_path = bstack11111lll1l_opy_.get(bstack11l11_opy_ (u"ࠦ࡫࡯࡬ࡦࡒࡤࡸ࡭ࠨ⌠"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1lll1111llll_opy_:
                return None
            self.logger.debug(bstack11l11_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡏࡳࡦࡨࡶࡪࡪࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡷ࡫ࡣࡦ࡫ࡹࡩࡩࡀࠠࡼࡿࠥ⌡").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack11l11_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡱࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࡀࠠࡼࡿࠥ⌢").format(e))
            return None
    def bstack11111111111_opy_(self):
        bstack11l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡺࡨࡦࠢࡦࡳࡺࡴࡴࠡࡱࡩࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡄࡔࡎࠦࡣࡢ࡮࡯ࡷࠥࡳࡡࡥࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ⌣")
        return self.bstack1lll111l111l_opy_