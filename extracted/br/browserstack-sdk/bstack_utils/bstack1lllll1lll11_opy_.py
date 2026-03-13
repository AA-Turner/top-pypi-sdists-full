# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import os
import time
from bstack_utils.bstack111ll1l1ll1_opy_ import bstack111ll1ll1ll_opy_
from bstack_utils.constants import bstack111ll111l1l_opy_
from bstack_utils.helper import get_host_info, bstack1111lll11l1_opy_
class bstack1lllll1l1111_opy_:
    bstack1111l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡌࡦࡴࡤ࡭ࡧࡶࠤࡹ࡫ࡳࡵࠢࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡷ࡬ࡪࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡹࡥࡳࡸࡨࡶ࠳ࠐࠠࠡࠢࠣࠦࠧࠨⓑ")
    def __init__(self, config, logger):
        bstack1111l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡ࠼ࡳࡥࡷࡧ࡭ࠡࡥࡲࡲ࡫࡯ࡧ࠻ࠢࡧ࡭ࡨࡺࠬࠡࡶࡨࡷࡹࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡣࡰࡰࡩ࡭࡬ࠐࠠࠡࠢࠣࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࡟ࡴࡶࡵࡥࡹ࡫ࡧࡺ࠼ࠣࡷࡹࡸࠬࠡࡶࡨࡷࡹࠦ࡯ࡳࡦࡨࡶ࡮ࡴࡧࠡࡵࡷࡶࡦࡺࡥࡨࡻࠣࡲࡦࡳࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧⓒ")
        self.config = config
        self.logger = logger
        self.bstack1ll1llll111l_opy_ = bstack1111l_opy_ (u"ࠧࡺࡥࡴࡶࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡴࡱ࡯ࡴ࠮ࡶࡨࡷࡹࡹࠢⓓ")
        self.bstack1ll1lll1ll1l_opy_ = None
        self.default_timeout = 60
        self.bstack1ll1lll1l111_opy_ = 5
        self.bstack1ll1lll1l1l1_opy_ = 0
    def bstack1lllll1l11ll_opy_(self, test_files, orchestration_strategy, orchestration_metadata={}):
        bstack1111l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡍࡳ࡯ࡴࡪࡣࡷࡩࡸࠦࡴࡩࡧࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡤࡲࡩࠦࡳࡵࡱࡵࡩࡸࠦࡴࡩࡧࠣࡶࡪࡹࡰࡰࡰࡶࡩࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡱࡱ࡯ࡰ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨⓔ")
        self.logger.debug(bstack1111l_opy_ (u"ࠢ࡜ࡵࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࡢࠦࡉ࡯࡫ࡷ࡭ࡦࡺࡩ࡯ࡩࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡹ࡬ࡸ࡭ࠦࡳࡵࡴࡤࡸࡪ࡭ࡹ࠻ࠢࡾࢁࠧⓕ").format(orchestration_strategy))
        try:
            bstack1ll1lll11lll_opy_ = []
            bstack1111l_opy_ (u"ࠣࠤ࡛ࠥࡪࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡨࡨࡸࡨ࡮ࠠࡨ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡩࡴࠢࡶࡳࡺࡸࡣࡦࠢ࡬ࡷࠥࡺࡹࡱࡧࠣࡳ࡫ࠦࡡࡳࡴࡤࡽࠥࡧ࡮ࡥࠢ࡬ࡸࠬࡹࠠࡦ࡮ࡨࡱࡪࡴࡴࡴࠢࡤࡶࡪࠦ࡯ࡧࠢࡷࡽࡵ࡫ࠠࡥ࡫ࡦࡸࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡪࡩࡡࡶࡵࡨࠤ࡮ࡴࠠࡵࡪࡤࡸࠥࡩࡡࡴࡧ࠯ࠤࡺࡹࡥࡳࠢ࡫ࡥࡸࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡ࡯ࡸࡰࡹ࡯࠭ࡳࡧࡳࡳࠥࡹ࡯ࡶࡴࡦࡩࠥࡽࡩࡵࡪࠣࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࠣ࡭ࡳࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠧࠨࠢⓖ")
            source = orchestration_metadata[bstack1111l_opy_ (u"ࠩࡵࡹࡳࡥࡳ࡮ࡣࡵࡸࡤࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠨⓗ")].get(bstack1111l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪⓘ"), [])
            bstack1ll1lll1llll_opy_ = isinstance(source, list) and all(isinstance(src, dict) and src is not None for src in source) and len(source) > 0
            if orchestration_metadata[bstack1111l_opy_ (u"ࠫࡷࡻ࡮ࡠࡵࡰࡥࡷࡺ࡟ࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠪⓙ")].get(bstack1111l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭ⓚ"), False) and not bstack1ll1lll1llll_opy_:
                bstack1ll1lll11lll_opy_ = bstack1111lll11l1_opy_(source) # bstack1ll1lll1ll11_opy_-repo is handled bstack1ll1llll1ll1_opy_
            payload = {
                bstack1111l_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧⓛ"): [{bstack1111l_opy_ (u"ࠢࡧ࡫࡯ࡩࡕࡧࡴࡩࠤⓜ"): f} for f in test_files],
                bstack1111l_opy_ (u"ࠣࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡔࡶࡵࡥࡹ࡫ࡧࡺࠤⓝ"): orchestration_strategy,
                bstack1111l_opy_ (u"ࠤࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡏࡨࡸࡦࡪࡡࡵࡣࠥⓞ"): orchestration_metadata,
                bstack1111l_opy_ (u"ࠥࡲࡴࡪࡥࡊࡰࡧࡩࡽࠨⓟ"): int(os.environ.get(bstack1111l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡋࡑࡈࡊ࡞ࠢⓠ")) or bstack1111l_opy_ (u"ࠧ࠶ࠢⓡ")),
                bstack1111l_opy_ (u"ࠨࡴࡰࡶࡤࡰࡓࡵࡤࡦࡵࠥⓢ"): int(os.environ.get(bstack1111l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡐࡖࡄࡐࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤⓣ")) or bstack1111l_opy_ (u"ࠣ࠳ࠥⓤ")),
                bstack1111l_opy_ (u"ࠤࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠢⓥ"): self.config.get(bstack1111l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨⓦ"), bstack1111l_opy_ (u"ࠫࠬⓧ")),
                bstack1111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠣⓨ"): self.config.get(bstack1111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩⓩ"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧ⓪"): os.environ.get(bstack1111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠢ⓫"), bstack1111l_opy_ (u"ࠤࠥ⓬")),
                bstack1111l_opy_ (u"ࠥ࡬ࡴࡹࡴࡊࡰࡩࡳࠧ⓭"): get_host_info(),
                bstack1111l_opy_ (u"ࠦࡵࡸࡄࡦࡶࡤ࡭ࡱࡹࠢ⓮"): bstack1ll1lll11lll_opy_
            }
            self.logger.debug(bstack1111l_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡘ࡫࡮ࡥ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴ࠼ࠣࡿࢂࠨ⓯").format(payload))
            response = bstack111ll1ll1ll_opy_.bstack1lll111ll111_opy_(self.bstack1ll1llll111l_opy_, payload)
            if response:
                self.bstack1ll1lll1ll1l_opy_ = self._1ll1llll1l1l_opy_(response)
                self.logger.debug(bstack1111l_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡ࡙ࠥࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤ⓰").format(self.bstack1ll1lll1ll1l_opy_))
            else:
                self.logger.error(bstack1111l_opy_ (u"ࠢ࡜ࡵࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࡢࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡪࡩࡹࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢ⓱"))
        except Exception as e:
            self.logger.error(bstack1111l_opy_ (u"ࠣ࡝ࡶࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࡣࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶ࠾࠿ࠦࡻࡾࠤ⓲").format(e))
    def _1ll1llll1l1l_opy_(self, response):
        bstack1111l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡳࡱࡦࡩࡸࡹࡥࡴࠢࡷ࡬ࡪࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡆࡖࡉࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡥࡳࡪࠠࡦࡺࡷࡶࡦࡩࡴࡴࠢࡵࡩࡱ࡫ࡶࡢࡰࡷࠤ࡫࡯ࡥ࡭ࡦࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ⓳")
        bstack11111ll11_opy_ = {}
        bstack11111ll11_opy_[bstack1111l_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦ⓴")] = response.get(bstack1111l_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࠧ⓵"), self.default_timeout)
        bstack11111ll11_opy_[bstack1111l_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࡏ࡮ࡵࡧࡵࡺࡦࡲࠢ⓶")] = response.get(bstack1111l_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠣ⓷"), self.bstack1ll1lll1l111_opy_)
        bstack1ll1llll1111_opy_ = response.get(bstack1111l_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡕࡳ࡮ࠥ⓸"))
        bstack1ll1llll1l11_opy_ = response.get(bstack1111l_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧ⓹"))
        if bstack1ll1llll1111_opy_:
            bstack11111ll11_opy_[bstack1111l_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡗࡵࡰࠧ⓺")] = bstack1ll1llll1111_opy_.split(bstack111ll111l1l_opy_ + bstack1111l_opy_ (u"ࠥ࠳ࠧ⓻"))[1] if bstack111ll111l1l_opy_ + bstack1111l_opy_ (u"ࠦ࠴ࠨ⓼") in bstack1ll1llll1111_opy_ else bstack1ll1llll1111_opy_
        else:
            bstack11111ll11_opy_[bstack1111l_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣ⓽")] = None
        if bstack1ll1llll1l11_opy_:
            bstack11111ll11_opy_[bstack1111l_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡕࡳ࡮ࠥ⓾")] = bstack1ll1llll1l11_opy_.split(bstack111ll111l1l_opy_ + bstack1111l_opy_ (u"ࠢ࠰ࠤ⓿"))[1] if bstack111ll111l1l_opy_ + bstack1111l_opy_ (u"ࠣ࠱ࠥ─") in bstack1ll1llll1l11_opy_ else bstack1ll1llll1l11_opy_
        else:
            bstack11111ll11_opy_[bstack1111l_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡘࡶࡱࠨ━")] = None
        if (
            response.get(bstack1111l_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦ│")) is None or
            response.get(bstack1111l_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࡎࡴࡴࡦࡴࡹࡥࡱࠨ┃")) is None or
            response.get(bstack1111l_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹ࡛ࡲ࡭ࠤ┄")) is None or
            response.get(bstack1111l_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹ࡛ࡲ࡭ࠤ┅")) is None
        ):
            self.logger.debug(bstack1111l_opy_ (u"ࠢ࡜ࡲࡵࡳࡨ࡫ࡳࡴࡡࡶࡴࡱ࡯ࡴࡠࡶࡨࡷࡹࡹ࡟ࡳࡧࡶࡴࡴࡴࡳࡦ࡟ࠣࡖࡪࡩࡥࡪࡸࡨࡨࠥࡴࡵ࡭࡮ࠣࡺࡦࡲࡵࡦࠪࡶ࠭ࠥ࡬࡯ࡳࠢࡶࡳࡲ࡫ࠠࡢࡶࡷࡶ࡮ࡨࡵࡵࡧࡶࠤ࡮ࡴࠠࡴࡲ࡯࡭ࡹࠦࡴࡦࡵࡷࡷࠥࡇࡐࡊࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠦ┆"))
        return bstack11111ll11_opy_
    def bstack1lllll1l1ll1_opy_(self):
        if not self.bstack1ll1lll1ll1l_opy_:
            self.logger.error(bstack1111l_opy_ (u"ࠣ࡝ࡪࡩࡹࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳ࡞ࠢࡑࡳࠥࡸࡥࡲࡷࡨࡷࡹࠦࡤࡢࡶࡤࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡲࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹ࠮ࠣ┇"))
            return None
        bstack1ll1llll11ll_opy_ = None
        test_files = []
        bstack1ll1lll1l1ll_opy_ = int(time.time() * 1000) # bstack1ll1lll1l11l_opy_ sec
        bstack1ll1lll1lll1_opy_ = int(self.bstack1ll1lll1ll1l_opy_.get(bstack1111l_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡌࡲࡹ࡫ࡲࡷࡣ࡯ࠦ┈"), self.bstack1ll1lll1l111_opy_))
        bstack1ll1llll11l1_opy_ = int(self.bstack1ll1lll1ll1l_opy_.get(bstack1111l_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦ┉"), self.default_timeout)) * 1000
        bstack1ll1llll1l11_opy_ = self.bstack1ll1lll1ll1l_opy_.get(bstack1111l_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣ┊"), None)
        bstack1ll1llll1111_opy_ = self.bstack1ll1lll1ll1l_opy_.get(bstack1111l_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣ┋"), None)
        if bstack1ll1llll1111_opy_ is None and bstack1ll1llll1l11_opy_ is None:
            return None
        try:
            while bstack1ll1llll1111_opy_ and (time.time() * 1000 - bstack1ll1lll1l1ll_opy_) < bstack1ll1llll11l1_opy_:
                response = bstack111ll1ll1ll_opy_.bstack1lll111l111l_opy_(bstack1ll1llll1111_opy_, {})
                if response and response.get(bstack1111l_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧ┌")):
                    bstack1ll1llll11ll_opy_ = response.get(bstack1111l_opy_ (u"ࠢࡵࡧࡶࡸࡸࠨ┍"))
                self.bstack1ll1lll1l1l1_opy_ += 1
                if bstack1ll1llll11ll_opy_:
                    break
                time.sleep(bstack1ll1lll1lll1_opy_)
                self.logger.debug(bstack1111l_opy_ (u"ࠣ࡝ࡪࡩࡹࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳ࡞ࠢࡉࡩࡹࡩࡨࡪࡰࡪࠤࡴࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡵࡩࡸࡻ࡬ࡵࠢࡘࡖࡑࠦࡡࡧࡶࡨࡶࠥࡽࡡࡪࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡿࢂࠦࡳࡦࡥࡲࡲࡩࡹ࠮ࠣ┎").format(bstack1ll1lll1lll1_opy_))
            if bstack1ll1llll1l11_opy_ and not bstack1ll1llll11ll_opy_:
                self.logger.debug(bstack1111l_opy_ (u"ࠤ࡞࡫ࡪࡺࡏࡳࡦࡨࡶࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴ࡟ࠣࡊࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡵࡲࡥࡧࡵࡩࡩࠦࡴࡦࡵࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡮ࡳࡥࡰࡷࡷࠤ࡚ࡘࡌࠣ┏"))
                response = bstack111ll1ll1ll_opy_.bstack1lll111l111l_opy_(bstack1ll1llll1l11_opy_, {})
                if response and response.get(bstack1111l_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤ┐")):
                    bstack1ll1llll11ll_opy_ = response.get(bstack1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࠥ┑"))
            if bstack1ll1llll11ll_opy_ and len(bstack1ll1llll11ll_opy_) > 0:
                for test_data in bstack1ll1llll11ll_opy_:
                    file_path = test_data.get(bstack1111l_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡓࡥࡹ࡮ࠢ┒"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1ll1llll11ll_opy_:
                return None
            self.logger.debug(bstack1111l_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡐࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡸࡥࡤࡧ࡬ࡺࡪࡪ࠺ࠡࡽࢀࠦ┓").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack1111l_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡲࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹ࠺ࠡࡽࢀࠦ└").format(e))
            return None
    def bstack1lllll1ll11l_opy_(self):
        bstack1111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠣࡧࡴࡻ࡮ࡵࠢࡲࡪࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡅࡕࡏࠠࡤࡣ࡯ࡰࡸࠦ࡭ࡢࡦࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ┕")
        return self.bstack1ll1lll1l1l1_opy_