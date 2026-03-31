# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import os
import time
from bstack_utils.bstack111l1ll11l1_opy_ import bstack111l1ll1111_opy_
from bstack_utils.constants import bstack111l11ll1ll_opy_
from bstack_utils.helper import get_host_info, bstack11111lll1l1_opy_
class bstack1llll1ll1lll_opy_:
    bstack1ll11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡊࡤࡲࡩࡲࡥࡴࠢࡷࡩࡸࡺࠠࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡷࡪࡸࡶࡦࡴ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ╔")
    def __init__(self, config, logger):
        bstack1ll11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡥ࡫ࡦࡸ࠱ࠦࡴࡦࡵࡷࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡨࡵ࡮ࡧ࡫ࡪࠎࠥࠦࠠࠡࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡤࡹࡴࡳࡣࡷࡩ࡬ࡿ࠺ࠡࡵࡷࡶ࠱ࠦࡴࡦࡵࡷࠤࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡳࡵࡴࡤࡸࡪ࡭ࡹࠡࡰࡤࡱࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ╕")
        self.config = config
        self.logger = logger
        self.bstack1ll1ll11ll1l_opy_ = bstack1ll11_opy_ (u"ࠥࡸࡪࡹࡴࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡲ࡯࡭ࡹ࠳ࡴࡦࡵࡷࡷࠧ╖")
        self.bstack1ll1ll111l11_opy_ = None
        self.default_timeout = 60
        self.bstack1ll1ll1111ll_opy_ = 5
        self.bstack1ll1ll11l111_opy_ = 0
    def bstack1llll1ll1ll1_opy_(self, test_files, orchestration_strategy, orchestration_metadata={}):
        bstack1ll11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡋࡱ࡭ࡹ࡯ࡡࡵࡧࡶࠤࡹ࡮ࡥࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡲࡦࡳࡸࡩࡸࡺࠠࡢࡰࡧࠤࡸࡺ࡯ࡳࡧࡶࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡶ࡯࡭࡮࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ╗")
        self.logger.debug(bstack1ll11_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡎࡴࡩࡵ࡫ࡤࡸ࡮ࡴࡧࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡷࡪࡶ࡫ࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࡀࠠࡼࡿࠥ╘").format(orchestration_strategy))
        try:
            bstack1ll1ll11lll1_opy_ = []
            bstack1ll11_opy_ (u"ࠨ࡙ࠢࠣࡨࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡦࡦࡶࡦ࡬ࠥ࡭ࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤ࡮ࡹࠠࡴࡱࡸࡶࡨ࡫ࠠࡪࡵࠣࡸࡾࡶࡥࠡࡱࡩࠤࡦࡸࡲࡢࡻࠣࡥࡳࡪࠠࡪࡶࠪࡷࠥ࡫࡬ࡦ࡯ࡨࡲࡹࡹࠠࡢࡴࡨࠤࡴ࡬ࠠࡵࡻࡳࡩࠥࡪࡩࡤࡶࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡨࡧࡦࡻࡳࡦࠢ࡬ࡲࠥࡺࡨࡢࡶࠣࡧࡦࡹࡥ࠭ࠢࡸࡷࡪࡸࠠࡩࡣࡶࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦ࡭ࡶ࡮ࡷ࡭࠲ࡸࡥࡱࡱࠣࡷࡴࡻࡲࡤࡧࠣࡻ࡮ࡺࡨࠡࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠡ࡫ࡱࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠥࠦࠧ╙")
            source = orchestration_metadata[bstack1ll11_opy_ (u"ࠧࡳࡷࡱࡣࡸࡳࡡࡳࡶࡢࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠭╚")].get(bstack1ll11_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ╛"), [])
            bstack1ll1ll111l1l_opy_ = isinstance(source, list) and all(isinstance(src, dict) and src is not None for src in source) and len(source) > 0
            if orchestration_metadata[bstack1ll11_opy_ (u"ࠩࡵࡹࡳࡥࡳ࡮ࡣࡵࡸࡤࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠨ╜")].get(bstack1ll11_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ╝"), False) and not bstack1ll1ll111l1l_opy_:
                bstack1ll1ll11lll1_opy_ = bstack11111lll1l1_opy_(source) # bstack1ll1ll111lll_opy_-repo is handled bstack1ll1ll111111_opy_
            payload = {
                bstack1ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࠥ╞"): [{bstack1ll11_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡓࡥࡹ࡮ࠢ╟"): f} for f in test_files],
                bstack1ll11_opy_ (u"ࠨ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࡙ࡴࡳࡣࡷࡩ࡬ࡿࠢ╠"): orchestration_strategy,
                bstack1ll11_opy_ (u"ࠢࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡍࡦࡶࡤࡨࡦࡺࡡࠣ╡"): orchestration_metadata,
                bstack1ll11_opy_ (u"ࠣࡰࡲࡨࡪࡏ࡮ࡥࡧࡻࠦ╢"): int(os.environ.get(bstack1ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡉࡏࡆࡈ࡜ࠧ╣")) or bstack1ll11_opy_ (u"ࠥ࠴ࠧ╤")),
                bstack1ll11_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࡑࡳࡩ࡫ࡳࠣ╥"): int(os.environ.get(bstack1ll11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡕࡔࡂࡎࡢࡒࡔࡊࡅࡠࡅࡒ࡙ࡓ࡚ࠢ╦")) or bstack1ll11_opy_ (u"ࠨ࠱ࠣ╧")),
                bstack1ll11_opy_ (u"ࠢࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠧ╨"): self.config.get(bstack1ll11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭╩"), bstack1ll11_opy_ (u"ࠩࠪ╪")),
                bstack1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡐࡤࡱࡪࠨ╫"): self.config.get(bstack1ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ╬"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡖࡺࡴࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥ╭"): os.environ.get(bstack1ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠧ╮"), bstack1ll11_opy_ (u"ࠢࠣ╯")),
                bstack1ll11_opy_ (u"ࠣࡪࡲࡷࡹࡏ࡮ࡧࡱࠥ╰"): get_host_info(),
                bstack1ll11_opy_ (u"ࠤࡳࡶࡉ࡫ࡴࡢ࡫࡯ࡷࠧ╱"): bstack1ll1ll11lll1_opy_
            }
            self.logger.debug(bstack1ll11_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡖࡩࡳࡪࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹ࠺ࠡࡽࢀࠦ╲").format(payload))
            response = bstack111l1ll1111_opy_.bstack1ll1lll1l1ll_opy_(self.bstack1ll1ll11ll1l_opy_, payload)
            if response:
                self.bstack1ll1ll111l11_opy_ = self._1ll1ll11ll11_opy_(response)
                self.logger.debug(bstack1ll11_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡗࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢ╳").format(self.bstack1ll1ll111l11_opy_))
            else:
                self.logger.error(bstack1ll11_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡨࡧࡷࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠲ࠧ╴"))
        except Exception as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴ࠼࠽ࠤࢀࢃࠢ╵").format(e))
    def _1ll1ll11ll11_opy_(self, response):
        bstack1ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡵࡪࡨࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡄࡔࡎࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡࡣࡱࡨࠥ࡫ࡸࡵࡴࡤࡧࡹࡹࠠࡳࡧ࡯ࡩࡻࡧ࡮ࡵࠢࡩ࡭ࡪࡲࡤࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ╶")
        bstack1ll1lllll1_opy_ = {}
        bstack1ll1lllll1_opy_[bstack1ll11_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ╷")] = response.get(bstack1ll11_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ╸"), self.default_timeout)
        bstack1ll1lllll1_opy_[bstack1ll11_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࡍࡳࡺࡥࡳࡸࡤࡰࠧ╹")] = response.get(bstack1ll11_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࡎࡴࡴࡦࡴࡹࡥࡱࠨ╺"), self.bstack1ll1ll1111ll_opy_)
        bstack1ll1ll11llll_opy_ = response.get(bstack1ll11_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣ╻"))
        bstack1ll1ll11l1ll_opy_ = response.get(bstack1ll11_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡕࡳ࡮ࠥ╼"))
        if bstack1ll1ll11llll_opy_:
            bstack1ll1lllll1_opy_[bstack1ll11_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡕࡳ࡮ࠥ╽")] = bstack1ll1ll11llll_opy_.split(bstack111l11ll1ll_opy_ + bstack1ll11_opy_ (u"ࠣ࠱ࠥ╾"))[1] if bstack111l11ll1ll_opy_ + bstack1ll11_opy_ (u"ࠤ࠲ࠦ╿") in bstack1ll1ll11llll_opy_ else bstack1ll1ll11llll_opy_
        else:
            bstack1ll1lllll1_opy_[bstack1ll11_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡘࡶࡱࠨ▀")] = None
        if bstack1ll1ll11l1ll_opy_:
            bstack1ll1lllll1_opy_[bstack1ll11_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣ▁")] = bstack1ll1ll11l1ll_opy_.split(bstack111l11ll1ll_opy_ + bstack1ll11_opy_ (u"ࠧ࠵ࠢ▂"))[1] if bstack111l11ll1ll_opy_ + bstack1ll11_opy_ (u"ࠨ࠯ࠣ▃") in bstack1ll1ll11l1ll_opy_ else bstack1ll1ll11l1ll_opy_
        else:
            bstack1ll1lllll1_opy_[bstack1ll11_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡖࡴ࡯ࠦ▄")] = None
        if (
            response.get(bstack1ll11_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ▅")) is None or
            response.get(bstack1ll11_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡌࡲࡹ࡫ࡲࡷࡣ࡯ࠦ▆")) is None or
            response.get(bstack1ll11_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷ࡙ࡷࡲࠢ▇")) is None or
            response.get(bstack1ll11_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢ█")) is None
        ):
            self.logger.debug(bstack1ll11_opy_ (u"ࠧࡡࡰࡳࡱࡦࡩࡸࡹ࡟ࡴࡲ࡯࡭ࡹࡥࡴࡦࡵࡷࡷࡤࡸࡥࡴࡲࡲࡲࡸ࡫࡝ࠡࡔࡨࡧࡪ࡯ࡶࡦࡦࠣࡲࡺࡲ࡬ࠡࡸࡤࡰࡺ࡫ࠨࡴࠫࠣࡪࡴࡸࠠࡴࡱࡰࡩࠥࡧࡴࡵࡴ࡬ࡦࡺࡺࡥࡴࠢ࡬ࡲࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡅࡕࡏࠠࡳࡧࡶࡴࡴࡴࡳࡦࠤ▉"))
        return bstack1ll1lllll1_opy_
    def bstack1llll1ll111l_opy_(self):
        if not self.bstack1ll1ll111l11_opy_:
            self.logger.error(bstack1ll11_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡏࡱࠣࡶࡪࡷࡵࡦࡵࡷࠤࡩࡧࡴࡢࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡰࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷ࠳ࠨ▊"))
            return None
        bstack1ll1ll11l1l1_opy_ = None
        test_files = []
        bstack1ll1ll1111l1_opy_ = int(time.time() * 1000) # bstack1ll1ll111ll1_opy_ sec
        bstack1ll1ll11111l_opy_ = int(self.bstack1ll1ll111l11_opy_.get(bstack1ll11_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡊࡰࡷࡩࡷࡼࡡ࡭ࠤ▋"), self.bstack1ll1ll1111ll_opy_))
        bstack1ll1ll11l11l_opy_ = int(self.bstack1ll1ll111l11_opy_.get(bstack1ll11_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ▌"), self.default_timeout)) * 1000
        bstack1ll1ll11l1ll_opy_ = self.bstack1ll1ll111l11_opy_.get(bstack1ll11_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡘࡶࡱࠨ▍"), None)
        bstack1ll1ll11llll_opy_ = self.bstack1ll1ll111l11_opy_.get(bstack1ll11_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡘࡶࡱࠨ▎"), None)
        if bstack1ll1ll11llll_opy_ is None and bstack1ll1ll11l1ll_opy_ is None:
            return None
        try:
            while bstack1ll1ll11llll_opy_ and (time.time() * 1000 - bstack1ll1ll1111l1_opy_) < bstack1ll1ll11l11l_opy_:
                response = bstack111l1ll1111_opy_.bstack1ll1lll1ll1l_opy_(bstack1ll1ll11llll_opy_, {})
                if response and response.get(bstack1ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࠥ▏")):
                    bstack1ll1ll11l1l1_opy_ = response.get(bstack1ll11_opy_ (u"ࠧࡺࡥࡴࡶࡶࠦ▐"))
                self.bstack1ll1ll11l111_opy_ += 1
                if bstack1ll1ll11l1l1_opy_:
                    break
                time.sleep(bstack1ll1ll11111l_opy_)
                self.logger.debug(bstack1ll11_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡇࡧࡷࡧ࡭࡯࡮ࡨࠢࡲࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࡴࠢࡩࡶࡴࡳࠠࡳࡧࡶࡹࡱࡺࠠࡖࡔࡏࠤࡦ࡬ࡴࡦࡴࠣࡻࡦ࡯ࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡽࢀࠤࡸ࡫ࡣࡰࡰࡧࡷ࠳ࠨ░").format(bstack1ll1ll11111l_opy_))
            if bstack1ll1ll11l1ll_opy_ and not bstack1ll1ll11l1l1_opy_:
                self.logger.debug(bstack1ll11_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡈࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡳࡷࡪࡥࡳࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡬ࡱࡪࡵࡵࡵࠢࡘࡖࡑࠨ▒"))
                response = bstack111l1ll1111_opy_.bstack1ll1lll1ll1l_opy_(bstack1ll1ll11l1ll_opy_, {})
                if response and response.get(bstack1ll11_opy_ (u"ࠣࡶࡨࡷࡹࡹࠢ▓")):
                    bstack1ll1ll11l1l1_opy_ = response.get(bstack1ll11_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣ▔"))
            if bstack1ll1ll11l1l1_opy_ and len(bstack1ll1ll11l1l1_opy_) > 0:
                for test_data in bstack1ll1ll11l1l1_opy_:
                    file_path = test_data.get(bstack1ll11_opy_ (u"ࠥࡪ࡮ࡲࡥࡑࡣࡷ࡬ࠧ▕"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1ll1ll11l1l1_opy_:
                return None
            self.logger.debug(bstack1ll11_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡕࡲࡥࡧࡵࡩࡩࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡶࡪࡩࡥࡪࡸࡨࡨ࠿ࠦࡻࡾࠤ▖").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡰࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷ࠿ࠦࡻࡾࠤ▗").format(e))
            return None
    def bstack1llll1l1llll_opy_(self):
        bstack1ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡࡥࡲࡹࡳࡺࠠࡰࡨࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡃࡓࡍࠥࡩࡡ࡭࡮ࡶࠤࡲࡧࡤࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ▘")
        return self.bstack1ll1ll11l111_opy_