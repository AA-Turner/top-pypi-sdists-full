# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import os
import time
from bstack_utils.bstack1111l111l11_opy_ import bstack1111l111l1l_opy_
from bstack_utils.constants import bstack111111llll1_opy_
from bstack_utils.helper import get_host_info, bstack1llll1l1lll1_opy_
class bstack1lll1l111lll_opy_:
    bstack1l111l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡌࡦࡴࡤ࡭ࡧࡶࠤࡹ࡫ࡳࡵࠢࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡷ࡬ࡪࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡹࡥࡳࡸࡨࡶ࠳ࠐࠠࠡࠢࠣࠦࠧࠨ❇")
    def __init__(self, config, logger):
        bstack1l111l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡ࠼ࡳࡥࡷࡧ࡭ࠡࡥࡲࡲ࡫࡯ࡧ࠻ࠢࡧ࡭ࡨࡺࠬࠡࡶࡨࡷࡹࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡣࡰࡰࡩ࡭࡬ࠐࠠࠡࠢࠣࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࡟ࡴࡶࡵࡥࡹ࡫ࡧࡺ࠼ࠣࡷࡹࡸࠬࠡࡶࡨࡷࡹࠦ࡯ࡳࡦࡨࡶ࡮ࡴࡧࠡࡵࡷࡶࡦࡺࡥࡨࡻࠣࡲࡦࡳࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ❈")
        self.config = config
        self.logger = logger
        self.bstack1ll11l1l1l1l_opy_ = bstack1l111l_opy_ (u"ࠧࡺࡥࡴࡶࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡴࡱ࡯ࡴ࠮ࡶࡨࡷࡹࡹࠢ❉")
        self.bstack1ll11l1lll1l_opy_ = None
        self.default_timeout = 60
        self.bstack1ll11l1ll1l1_opy_ = 5
        self.bstack1ll11l1l1ll1_opy_ = 0
    def bstack1lll1l111l11_opy_(self, test_files, orchestration_strategy, orchestration_metadata={}):
        bstack1l111l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡍࡳ࡯ࡴࡪࡣࡷࡩࡸࠦࡴࡩࡧࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡤࡲࡩࠦࡳࡵࡱࡵࡩࡸࠦࡴࡩࡧࠣࡶࡪࡹࡰࡰࡰࡶࡩࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡱࡱ࡯ࡰ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ❊")
        self.logger.debug(bstack1l111l_opy_ (u"ࠢ࡜ࡵࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࡢࠦࡉ࡯࡫ࡷ࡭ࡦࡺࡩ࡯ࡩࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡹ࡬ࡸ࡭ࠦࡳࡵࡴࡤࡸࡪ࡭ࡹ࠻ࠢࡾࢁࠧ❋").format(orchestration_strategy))
        try:
            bstack1ll11l1l11l1_opy_ = []
            bstack1l111l_opy_ (u"ࠣࠤ࡛ࠥࡪࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡨࡨࡸࡨ࡮ࠠࡨ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡩࡴࠢࡶࡳࡺࡸࡣࡦࠢ࡬ࡷࠥࡺࡹࡱࡧࠣࡳ࡫ࠦࡡࡳࡴࡤࡽࠥࡧ࡮ࡥࠢ࡬ࡸࠬࡹࠠࡦ࡮ࡨࡱࡪࡴࡴࡴࠢࡤࡶࡪࠦ࡯ࡧࠢࡷࡽࡵ࡫ࠠࡥ࡫ࡦࡸࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡪࡩࡡࡶࡵࡨࠤ࡮ࡴࠠࡵࡪࡤࡸࠥࡩࡡࡴࡧ࠯ࠤࡺࡹࡥࡳࠢ࡫ࡥࡸࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡ࡯ࡸࡰࡹ࡯࠭ࡳࡧࡳࡳࠥࡹ࡯ࡶࡴࡦࡩࠥࡽࡩࡵࡪࠣࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࠣ࡭ࡳࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠧࠨࠢ❌")
            source = orchestration_metadata[bstack1l111l_opy_ (u"ࠩࡵࡹࡳࡥࡳ࡮ࡣࡵࡸࡤࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠨ❍")].get(bstack1l111l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ❎"), [])
            bstack1ll11l1lllll_opy_ = isinstance(source, list) and all(isinstance(src, dict) and src is not None for src in source) and len(source) > 0
            if orchestration_metadata[bstack1l111l_opy_ (u"ࠫࡷࡻ࡮ࡠࡵࡰࡥࡷࡺ࡟ࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠪ❏")].get(bstack1l111l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭❐"), False) and not bstack1ll11l1lllll_opy_:
                bstack1ll11l1l11l1_opy_ = bstack1llll1l1lll1_opy_(source) # bstack1ll11ll11111_opy_-repo is handled bstack1ll11l1llll1_opy_
            payload = {
                bstack1l111l_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧ❑"): [{bstack1l111l_opy_ (u"ࠢࡧ࡫࡯ࡩࡕࡧࡴࡩࠤ❒"): f} for f in test_files],
                bstack1l111l_opy_ (u"ࠣࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡔࡶࡵࡥࡹ࡫ࡧࡺࠤ❓"): orchestration_strategy,
                bstack1l111l_opy_ (u"ࠤࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡏࡨࡸࡦࡪࡡࡵࡣࠥ❔"): orchestration_metadata,
                bstack1l111l_opy_ (u"ࠥࡲࡴࡪࡥࡊࡰࡧࡩࡽࠨ❕"): int(os.environ.get(bstack1l111l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡋࡑࡈࡊ࡞ࠢ❖")) or bstack1l111l_opy_ (u"ࠧ࠶ࠢ❗")),
                bstack1l111l_opy_ (u"ࠨࡴࡰࡶࡤࡰࡓࡵࡤࡦࡵࠥ❘"): int(os.environ.get(bstack1l111l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡐࡖࡄࡐࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤ❙")) or bstack1l111l_opy_ (u"ࠣ࠳ࠥ❚")),
                bstack1l111l_opy_ (u"ࠤࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠢ❛"): self.config.get(bstack1l111l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ❜"), bstack1l111l_opy_ (u"ࠫࠬ❝")),
                bstack1l111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠣ❞"): self.config.get(bstack1l111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ❟"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1l111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧ❠"): os.environ.get(bstack1l111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠢ❡"), bstack1l111l_opy_ (u"ࠤࠥ❢")),
                bstack1l111l_opy_ (u"ࠥ࡬ࡴࡹࡴࡊࡰࡩࡳࠧ❣"): get_host_info(),
                bstack1l111l_opy_ (u"ࠦࡵࡸࡄࡦࡶࡤ࡭ࡱࡹࠢ❤"): bstack1ll11l1l11l1_opy_
            }
            self.logger.debug(bstack1l111l_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡘ࡫࡮ࡥ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴ࠼ࠣࡿࢂࠨ❥").format(payload))
            response = bstack1111l111l1l_opy_.bstack1ll1l11111l1_opy_(self.bstack1ll11l1l1l1l_opy_, payload)
            if response:
                self.bstack1ll11l1lll1l_opy_ = self._1ll11ll1111l_opy_(response)
                self.logger.debug(bstack1l111l_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡ࡙ࠥࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤ❦").format(self.bstack1ll11l1lll1l_opy_))
            else:
                self.logger.error(bstack1l111l_opy_ (u"ࠢ࡜ࡵࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࡢࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡪࡩࡹࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢ❧"))
        except Exception as e:
            self.logger.error(bstack1l111l_opy_ (u"ࠣ࡝ࡶࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࡣࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶ࠾࠿ࠦࡻࡾࠤ❨").format(e))
    def _1ll11ll1111l_opy_(self, response):
        bstack1l111l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡳࡱࡦࡩࡸࡹࡥࡴࠢࡷ࡬ࡪࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡆࡖࡉࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡥࡳࡪࠠࡦࡺࡷࡶࡦࡩࡴࡴࠢࡵࡩࡱ࡫ࡶࡢࡰࡷࠤ࡫࡯ࡥ࡭ࡦࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ❩")
        bstack1lllll1ll1l_opy_ = {}
        bstack1lllll1ll1l_opy_[bstack1l111l_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦ❪")] = response.get(bstack1l111l_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࠧ❫"), self.default_timeout)
        bstack1lllll1ll1l_opy_[bstack1l111l_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࡏ࡮ࡵࡧࡵࡺࡦࡲࠢ❬")] = response.get(bstack1l111l_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠣ❭"), self.bstack1ll11l1ll1l1_opy_)
        bstack1ll11l1l1l11_opy_ = response.get(bstack1l111l_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡕࡳ࡮ࠥ❮"))
        bstack1ll11l1ll11l_opy_ = response.get(bstack1l111l_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧ❯"))
        if bstack1ll11l1l1l11_opy_:
            bstack1lllll1ll1l_opy_[bstack1l111l_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡗࡵࡰࠧ❰")] = bstack1ll11l1l1l11_opy_.split(bstack111111llll1_opy_ + bstack1l111l_opy_ (u"ࠥ࠳ࠧ❱"))[1] if bstack111111llll1_opy_ + bstack1l111l_opy_ (u"ࠦ࠴ࠨ❲") in bstack1ll11l1l1l11_opy_ else bstack1ll11l1l1l11_opy_
        else:
            bstack1lllll1ll1l_opy_[bstack1l111l_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣ❳")] = None
        if bstack1ll11l1ll11l_opy_:
            bstack1lllll1ll1l_opy_[bstack1l111l_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡕࡳ࡮ࠥ❴")] = bstack1ll11l1ll11l_opy_.split(bstack111111llll1_opy_ + bstack1l111l_opy_ (u"ࠢ࠰ࠤ❵"))[1] if bstack111111llll1_opy_ + bstack1l111l_opy_ (u"ࠣ࠱ࠥ❶") in bstack1ll11l1ll11l_opy_ else bstack1ll11l1ll11l_opy_
        else:
            bstack1lllll1ll1l_opy_[bstack1l111l_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡘࡶࡱࠨ❷")] = None
        if (
            response.get(bstack1l111l_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦ❸")) is None or
            response.get(bstack1l111l_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࡎࡴࡴࡦࡴࡹࡥࡱࠨ❹")) is None or
            response.get(bstack1l111l_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹ࡛ࡲ࡭ࠤ❺")) is None or
            response.get(bstack1l111l_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹ࡛ࡲ࡭ࠤ❻")) is None
        ):
            self.logger.debug(bstack1l111l_opy_ (u"ࠢ࡜ࡲࡵࡳࡨ࡫ࡳࡴࡡࡶࡴࡱ࡯ࡴࡠࡶࡨࡷࡹࡹ࡟ࡳࡧࡶࡴࡴࡴࡳࡦ࡟ࠣࡖࡪࡩࡥࡪࡸࡨࡨࠥࡴࡵ࡭࡮ࠣࡺࡦࡲࡵࡦࠪࡶ࠭ࠥ࡬࡯ࡳࠢࡶࡳࡲ࡫ࠠࡢࡶࡷࡶ࡮ࡨࡵࡵࡧࡶࠤ࡮ࡴࠠࡴࡲ࡯࡭ࡹࠦࡴࡦࡵࡷࡷࠥࡇࡐࡊࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠦ❼"))
        return bstack1lllll1ll1l_opy_
    def bstack1lll1l11111l_opy_(self):
        if not self.bstack1ll11l1lll1l_opy_:
            self.logger.error(bstack1l111l_opy_ (u"ࠣ࡝ࡪࡩࡹࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳ࡞ࠢࡑࡳࠥࡸࡥࡲࡷࡨࡷࡹࠦࡤࡢࡶࡤࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡲࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹ࠮ࠣ❽"))
            return None
        bstack1ll11l1ll1ll_opy_ = None
        test_files = []
        bstack1ll11l1ll111_opy_ = int(time.time() * 1000) # bstack1ll11l1l11ll_opy_ sec
        bstack1ll11l1lll11_opy_ = int(self.bstack1ll11l1lll1l_opy_.get(bstack1l111l_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡌࡲࡹ࡫ࡲࡷࡣ࡯ࠦ❾"), self.bstack1ll11l1ll1l1_opy_))
        bstack1ll11l1l1lll_opy_ = int(self.bstack1ll11l1lll1l_opy_.get(bstack1l111l_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦ❿"), self.default_timeout)) * 1000
        bstack1ll11l1ll11l_opy_ = self.bstack1ll11l1lll1l_opy_.get(bstack1l111l_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣ➀"), None)
        bstack1ll11l1l1l11_opy_ = self.bstack1ll11l1lll1l_opy_.get(bstack1l111l_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣ➁"), None)
        if bstack1ll11l1l1l11_opy_ is None and bstack1ll11l1ll11l_opy_ is None:
            return None
        try:
            while bstack1ll11l1l1l11_opy_ and (time.time() * 1000 - bstack1ll11l1ll111_opy_) < bstack1ll11l1l1lll_opy_:
                response = bstack1111l111l1l_opy_.bstack1ll11llllll1_opy_(bstack1ll11l1l1l11_opy_, {})
                if response and response.get(bstack1l111l_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧ➂")):
                    bstack1ll11l1ll1ll_opy_ = response.get(bstack1l111l_opy_ (u"ࠢࡵࡧࡶࡸࡸࠨ➃"))
                self.bstack1ll11l1l1ll1_opy_ += 1
                if bstack1ll11l1ll1ll_opy_:
                    break
                time.sleep(bstack1ll11l1lll11_opy_)
                self.logger.debug(bstack1l111l_opy_ (u"ࠣ࡝ࡪࡩࡹࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳ࡞ࠢࡉࡩࡹࡩࡨࡪࡰࡪࠤࡴࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡵࡩࡸࡻ࡬ࡵࠢࡘࡖࡑࠦࡡࡧࡶࡨࡶࠥࡽࡡࡪࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡿࢂࠦࡳࡦࡥࡲࡲࡩࡹ࠮ࠣ➄").format(bstack1ll11l1lll11_opy_))
            if bstack1ll11l1ll11l_opy_ and not bstack1ll11l1ll1ll_opy_:
                self.logger.debug(bstack1l111l_opy_ (u"ࠤ࡞࡫ࡪࡺࡏࡳࡦࡨࡶࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴ࡟ࠣࡊࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡵࡲࡥࡧࡵࡩࡩࠦࡴࡦࡵࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡮ࡳࡥࡰࡷࡷࠤ࡚ࡘࡌࠣ➅"))
                response = bstack1111l111l1l_opy_.bstack1ll11llllll1_opy_(bstack1ll11l1ll11l_opy_, {})
                if response and response.get(bstack1l111l_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤ➆")):
                    bstack1ll11l1ll1ll_opy_ = response.get(bstack1l111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࠥ➇"))
            if bstack1ll11l1ll1ll_opy_ and len(bstack1ll11l1ll1ll_opy_) > 0:
                for bstack1llll1l11ll_opy_ in bstack1ll11l1ll1ll_opy_:
                    file_path = bstack1llll1l11ll_opy_.get(bstack1l111l_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡓࡥࡹ࡮ࠢ➈"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1ll11l1ll1ll_opy_:
                return None
            self.logger.debug(bstack1l111l_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡐࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡸࡥࡤࡧ࡬ࡺࡪࡪ࠺ࠡࡽࢀࠦ➉").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack1l111l_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡲࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹ࠺ࠡࡽࢀࠦ➊").format(e))
            return None
    def bstack1lll1l111111_opy_(self):
        bstack1l111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠣࡧࡴࡻ࡮ࡵࠢࡲࡪࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡅࡕࡏࠠࡤࡣ࡯ࡰࡸࠦ࡭ࡢࡦࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ➋")
        return self.bstack1ll11l1l1ll1_opy_