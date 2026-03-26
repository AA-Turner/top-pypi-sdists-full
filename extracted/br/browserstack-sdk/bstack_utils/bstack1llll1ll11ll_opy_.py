# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import os
import time
from bstack_utils.bstack111l1ll11ll_opy_ import bstack111l1ll11l1_opy_
from bstack_utils.constants import bstack111l11l11ll_opy_
from bstack_utils.helper import get_host_info, bstack1111l1l1l11_opy_
class bstack1llll1l1l1ll_opy_:
    bstack1ll1lll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡎࡡ࡯ࡦ࡯ࡩࡸࠦࡴࡦࡵࡷࠤࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡹ࡮ࡥࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡴࡧࡵࡺࡪࡸ࠮ࠋࠢࠣࠤࠥࠨࠢࠣ╃")
    def __init__(self, config, logger):
        bstack1ll1lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣࡧࡴࡴࡦࡪࡩ࠽ࠤࡩ࡯ࡣࡵ࠮ࠣࡸࡪࡹࡴࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡥࡲࡲ࡫࡯ࡧࠋࠢࠣࠤࠥࠦࠠࠡࠢ࠽ࡴࡦࡸࡡ࡮ࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡡࡶࡸࡷࡧࡴࡦࡩࡼ࠾ࠥࡹࡴࡳ࠮ࠣࡸࡪࡹࡴࠡࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡷࡹࡸࡡࡵࡧࡪࡽࠥࡴࡡ࡮ࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ╄")
        self.config = config
        self.logger = logger
        self.bstack1ll1ll111l1l_opy_ = bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠳ࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡶ࡬ࡪࡶ࠰ࡸࡪࡹࡴࡴࠤ╅")
        self.bstack1ll1ll1l111l_opy_ = None
        self.default_timeout = 60
        self.bstack1ll1ll11ll1l_opy_ = 5
        self.bstack1ll1ll11l11l_opy_ = 0
    def bstack1llll1l1llll_opy_(self, test_files, orchestration_strategy, orchestration_metadata={}):
        bstack1ll1lll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡏ࡮ࡪࡶ࡬ࡥࡹ࡫ࡳࠡࡶ࡫ࡩࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡶࡪࡷࡵࡦࡵࡷࠤࡦࡴࡤࠡࡵࡷࡳࡷ࡫ࡳࠡࡶ࡫ࡩࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡳࡳࡱࡲࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ╆")
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠤ࡞ࡷࡵࡲࡩࡵࡖࡨࡷࡹࡹ࡝ࠡࡋࡱ࡭ࡹ࡯ࡡࡵ࡫ࡱ࡫ࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡻ࡮ࡺࡨࠡࡵࡷࡶࡦࡺࡥࡨࡻ࠽ࠤࢀࢃࠢ╇").format(orchestration_strategy))
        try:
            bstack1ll1ll11l1l1_opy_ = []
            bstack1ll1lll_opy_ (u"ࠥࠦࠧ࡝ࡥࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡪࡪࡺࡣࡩࠢࡪ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡ࡫ࡶࠤࡸࡵࡵࡳࡥࡨࠤ࡮ࡹࠠࡵࡻࡳࡩࠥࡵࡦࠡࡣࡵࡶࡦࡿࠠࡢࡰࡧࠤ࡮ࡺࠧࡴࠢࡨࡰࡪࡳࡥ࡯ࡶࡶࠤࡦࡸࡥࠡࡱࡩࠤࡹࡿࡰࡦࠢࡧ࡭ࡨࡺࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡥࡤࡣࡸࡷࡪࠦࡩ࡯ࠢࡷ࡬ࡦࡺࠠࡤࡣࡶࡩ࠱ࠦࡵࡴࡧࡵࠤ࡭ࡧࡳࠡࡲࡵࡳࡻ࡯ࡤࡦࡦࠣࡱࡺࡲࡴࡪ࠯ࡵࡩࡵࡵࠠࡴࡱࡸࡶࡨ࡫ࠠࡸ࡫ࡷ࡬ࠥ࡬ࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࠥ࡯࡮ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠢࠣࠤ╈")
            source = orchestration_metadata[bstack1ll1lll_opy_ (u"ࠫࡷࡻ࡮ࡠࡵࡰࡥࡷࡺ࡟ࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠪ╉")].get(bstack1ll1lll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ╊"), [])
            bstack1ll1ll1l1111_opy_ = isinstance(source, list) and all(isinstance(src, dict) and src is not None for src in source) and len(source) > 0
            if orchestration_metadata[bstack1ll1lll_opy_ (u"࠭ࡲࡶࡰࡢࡷࡲࡧࡲࡵࡡࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠬ╋")].get(bstack1ll1lll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ╌"), False) and not bstack1ll1ll1l1111_opy_:
                bstack1ll1ll11l1l1_opy_ = bstack1111l1l1l11_opy_(source) # bstack1ll1ll11l1ll_opy_-repo is handled bstack1ll1ll111ll1_opy_
            payload = {
                bstack1ll1lll_opy_ (u"ࠣࡶࡨࡷࡹࡹࠢ╍"): [{bstack1ll1lll_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡐࡢࡶ࡫ࠦ╎"): f} for f in test_files],
                bstack1ll1lll_opy_ (u"ࠥࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡖࡸࡷࡧࡴࡦࡩࡼࠦ╏"): orchestration_strategy,
                bstack1ll1lll_opy_ (u"ࠦࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡑࡪࡺࡡࡥࡣࡷࡥࠧ═"): orchestration_metadata,
                bstack1ll1lll_opy_ (u"ࠧࡴ࡯ࡥࡧࡌࡲࡩ࡫ࡸࠣ║"): int(os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡍࡓࡊࡅ࡙ࠤ╒")) or bstack1ll1lll_opy_ (u"ࠢ࠱ࠤ╓")),
                bstack1ll1lll_opy_ (u"ࠣࡶࡲࡸࡦࡲࡎࡰࡦࡨࡷࠧ╔"): int(os.environ.get(bstack1ll1lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡒࡘࡆࡒ࡟ࡏࡑࡇࡉࡤࡉࡏࡖࡐࡗࠦ╕")) or bstack1ll1lll_opy_ (u"ࠥ࠵ࠧ╖")),
                bstack1ll1lll_opy_ (u"ࠦࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠤ╗"): self.config.get(bstack1ll1lll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ╘"), bstack1ll1lll_opy_ (u"࠭ࠧ╙")),
                bstack1ll1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠥ╚"): self.config.get(bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ╛"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1ll1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡓࡷࡱࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢ╜"): os.environ.get(bstack1ll1lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠤ╝"), bstack1ll1lll_opy_ (u"ࠦࠧ╞")),
                bstack1ll1lll_opy_ (u"ࠧ࡮࡯ࡴࡶࡌࡲ࡫ࡵࠢ╟"): get_host_info(),
                bstack1ll1lll_opy_ (u"ࠨࡰࡳࡆࡨࡸࡦ࡯࡬ࡴࠤ╠"): bstack1ll1ll11l1l1_opy_
            }
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢ࡜ࡵࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࡢࠦࡓࡦࡰࡧ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶ࠾ࠥࢁࡽࠣ╡").format(payload))
            response = bstack111l1ll11l1_opy_.bstack1ll1llll11l1_opy_(self.bstack1ll1ll111l1l_opy_, payload)
            if response:
                self.bstack1ll1ll1l111l_opy_ = self._1ll1ll11lll1_opy_(response)
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠣ࡝ࡶࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࡣࠠࡔࡲ࡯࡭ࡹࠦࡴࡦࡵࡷࡷࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦ╢").format(self.bstack1ll1ll1l111l_opy_))
            else:
                self.logger.error(bstack1ll1lll_opy_ (u"ࠤ࡞ࡷࡵࡲࡩࡵࡖࡨࡷࡹࡹ࡝ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡬࡫ࡴࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠯ࠤ╣"))
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࡀ࠺ࠡࡽࢀࠦ╤").format(e))
    def _1ll1ll11lll1_opy_(self, response):
        bstack1ll1lll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡹ࡮ࡥࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡁࡑࡋࠣࡶࡪࡹࡰࡰࡰࡶࡩࠥࡧ࡮ࡥࠢࡨࡼࡹࡸࡡࡤࡶࡶࠤࡷ࡫࡬ࡦࡸࡤࡲࡹࠦࡦࡪࡧ࡯ࡨࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ╥")
        bstack1ll111l1l1_opy_ = {}
        bstack1ll111l1l1_opy_[bstack1ll1lll_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࠨ╦")] = response.get(bstack1ll1lll_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢ╧"), self.default_timeout)
        bstack1ll111l1l1_opy_[bstack1ll1lll_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡊࡰࡷࡩࡷࡼࡡ࡭ࠤ╨")] = response.get(bstack1ll1lll_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡋࡱࡸࡪࡸࡶࡢ࡮ࠥ╩"), self.bstack1ll1ll11ll1l_opy_)
        bstack1ll1ll11l111_opy_ = response.get(bstack1ll1lll_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡗࡵࡰࠧ╪"))
        bstack1ll1ll111lll_opy_ = response.get(bstack1ll1lll_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷ࡙ࡷࡲࠢ╫"))
        if bstack1ll1ll11l111_opy_:
            bstack1ll111l1l1_opy_[bstack1ll1lll_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢ╬")] = bstack1ll1ll11l111_opy_.split(bstack111l11l11ll_opy_ + bstack1ll1lll_opy_ (u"ࠧ࠵ࠢ╭"))[1] if bstack111l11l11ll_opy_ + bstack1ll1lll_opy_ (u"ࠨ࠯ࠣ╮") in bstack1ll1ll11l111_opy_ else bstack1ll1ll11l111_opy_
        else:
            bstack1ll111l1l1_opy_[bstack1ll1lll_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡕࡳ࡮ࠥ╯")] = None
        if bstack1ll1ll111lll_opy_:
            bstack1ll111l1l1_opy_[bstack1ll1lll_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧ╰")] = bstack1ll1ll111lll_opy_.split(bstack111l11l11ll_opy_ + bstack1ll1lll_opy_ (u"ࠤ࠲ࠦ╱"))[1] if bstack111l11l11ll_opy_ + bstack1ll1lll_opy_ (u"ࠥ࠳ࠧ╲") in bstack1ll1ll111lll_opy_ else bstack1ll1ll111lll_opy_
        else:
            bstack1ll111l1l1_opy_[bstack1ll1lll_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣ╳")] = None
        if (
            response.get(bstack1ll1lll_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࠨ╴")) is None or
            response.get(bstack1ll1lll_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠣ╵")) is None or
            response.get(bstack1ll1lll_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡖࡴ࡯ࠦ╶")) is None or
            response.get(bstack1ll1lll_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡖࡴ࡯ࠦ╷")) is None
        ):
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤ࡞ࡴࡷࡵࡣࡦࡵࡶࡣࡸࡶ࡬ࡪࡶࡢࡸࡪࡹࡴࡴࡡࡵࡩࡸࡶ࡯࡯ࡵࡨࡡࠥࡘࡥࡤࡧ࡬ࡺࡪࡪࠠ࡯ࡷ࡯ࡰࠥࡼࡡ࡭ࡷࡨࠬࡸ࠯ࠠࡧࡱࡵࠤࡸࡵ࡭ࡦࠢࡤࡸࡹࡸࡩࡣࡷࡷࡩࡸࠦࡩ࡯ࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡂࡒࡌࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨ╸"))
        return bstack1ll111l1l1_opy_
    def bstack1llll1ll1l1l_opy_(self):
        if not self.bstack1ll1ll1l111l_opy_:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠥ࡟࡬࡫ࡴࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡠࠤࡓࡵࠠࡳࡧࡴࡹࡪࡹࡴࠡࡦࡤࡸࡦࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡴࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴ࠰ࠥ╹"))
            return None
        bstack1ll1ll1111ll_opy_ = None
        test_files = []
        bstack1ll1ll11ll11_opy_ = int(time.time() * 1000) # bstack1ll1ll11llll_opy_ sec
        bstack1ll1ll1111l1_opy_ = int(self.bstack1ll1ll1l111l_opy_.get(bstack1ll1lll_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࡎࡴࡴࡦࡴࡹࡥࡱࠨ╺"), self.bstack1ll1ll11ll1l_opy_))
        bstack1ll1ll111l11_opy_ = int(self.bstack1ll1ll1l111l_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࠨ╻"), self.default_timeout)) * 1000
        bstack1ll1ll111lll_opy_ = self.bstack1ll1ll1l111l_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡕࡳ࡮ࠥ╼"), None)
        bstack1ll1ll11l111_opy_ = self.bstack1ll1ll1l111l_opy_.get(bstack1ll1lll_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡕࡳ࡮ࠥ╽"), None)
        if bstack1ll1ll11l111_opy_ is None and bstack1ll1ll111lll_opy_ is None:
            return None
        try:
            while bstack1ll1ll11l111_opy_ and (time.time() * 1000 - bstack1ll1ll11ll11_opy_) < bstack1ll1ll111l11_opy_:
                response = bstack111l1ll11l1_opy_.bstack1ll1lll1ll11_opy_(bstack1ll1ll11l111_opy_, {})
                if response and response.get(bstack1ll1lll_opy_ (u"ࠣࡶࡨࡷࡹࡹࠢ╾")):
                    bstack1ll1ll1111ll_opy_ = response.get(bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣ╿"))
                self.bstack1ll1ll11l11l_opy_ += 1
                if bstack1ll1ll1111ll_opy_:
                    break
                time.sleep(bstack1ll1ll1111l1_opy_)
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠥ࡟࡬࡫ࡴࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡠࠤࡋ࡫ࡴࡤࡪ࡬ࡲ࡬ࠦ࡯ࡳࡦࡨࡶࡪࡪࠠࡵࡧࡶࡸࡸࠦࡦࡳࡱࡰࠤࡷ࡫ࡳࡶ࡮ࡷࠤ࡚ࡘࡌࠡࡣࡩࡸࡪࡸࠠࡸࡣ࡬ࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࢁࡽࠡࡵࡨࡧࡴࡴࡤࡴ࠰ࠥ▀").format(bstack1ll1ll1111l1_opy_))
            if bstack1ll1ll111lll_opy_ and not bstack1ll1ll1111ll_opy_:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡌࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡰࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࡹࠠࡧࡴࡲࡱࠥࡺࡩ࡮ࡧࡲࡹࡹࠦࡕࡓࡎࠥ▁"))
                response = bstack111l1ll11l1_opy_.bstack1ll1lll1ll11_opy_(bstack1ll1ll111lll_opy_, {})
                if response and response.get(bstack1ll1lll_opy_ (u"ࠧࡺࡥࡴࡶࡶࠦ▂")):
                    bstack1ll1ll1111ll_opy_ = response.get(bstack1ll1lll_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧ▃"))
            if bstack1ll1ll1111ll_opy_ and len(bstack1ll1ll1111ll_opy_) > 0:
                for test_data in bstack1ll1ll1111ll_opy_:
                    file_path = test_data.get(bstack1ll1lll_opy_ (u"ࠢࡧ࡫࡯ࡩࡕࡧࡴࡩࠤ▄"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1ll1ll1111ll_opy_:
                return None
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠣ࡝ࡪࡩࡹࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳ࡞ࠢࡒࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡳࡧࡦࡩ࡮ࡼࡥࡥ࠼ࠣࡿࢂࠨ▅").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠤ࡞࡫ࡪࡺࡏࡳࡦࡨࡶࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴ࡟ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤࡴࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴ࠼ࠣࡿࢂࠨ▆").format(e))
            return None
    def bstack1llll1lll11l_opy_(self):
        bstack1ll1lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡶ࡫ࡩࠥࡩ࡯ࡶࡰࡷࠤࡴ࡬ࠠࡴࡲ࡯࡭ࡹࠦࡴࡦࡵࡷࡷࠥࡇࡐࡊࠢࡦࡥࡱࡲࡳࠡ࡯ࡤࡨࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ▇")
        return self.bstack1ll1ll11l11l_opy_