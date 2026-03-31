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
import glob
import time
from bstack_utils.bstack11ll1l1l_opy_ import bstack1ll1ll11l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
class bstack111ll1l11_opy_:
    def __init__(self, args, logger, bstack1lllllll11l_opy_, bstack1llllll11ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lllllll11l_opy_ = bstack1lllllll11l_opy_
        self.bstack1llllll11ll_opy_ = bstack1llllll11ll_opy_
        self.bstack1l1ll1l1_opy_ = []
    def _1lllllll111_opy_(self, bstack1l1ll1l1_opy_):
        bstack1ll11_opy_ (u"ࠣࠤࠥࡉࡽࡶࡡ࡯ࡦࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡡ࡯ࡦࠣ࡫ࡱࡵࡢ࠮ࡲࡤࡸࡹ࡫ࡲ࡯ࠢࡨࡲࡹࡸࡩࡦࡵࠣ࡭ࡳࠦࡳࡱࡧࡦࡣ࡫࡯࡬ࡦࡵࠣࡸࡴࠦࡩ࡯ࡦ࡬ࡺ࡮ࡪࡵࡢ࡮ࠣ࠲࡫࡫ࡡࡵࡷࡵࡩࠥ࡬ࡩ࡭ࡧࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡈࡢࡰࡧࡰࡪࡹࠠࡵࡪࡵࡩࡪࠦࡣࡢࡵࡨࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠ࠲࠰ࠣࡈ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࠨࡦ࠰ࡪ࠲ࠥ࠭ࡦࡦࡣࡷࡹࡷ࡫ࡳࠨࠫࠣ⠘ࠥࡽࡡ࡭࡭ࡶࠤࡷ࡫ࡣࡶࡴࡶ࡭ࡻ࡫࡬ࡺࠢࡩࡳࡷࠦࠪ࠯ࡨࡨࡥࡹࡻࡲࡦࠢࡩ࡭ࡱ࡫ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࠶࠳ࠦࡇ࡭ࡱࡥࠤࡵࡧࡴࡵࡧࡵࡲࠥ࠮ࡥ࠯ࡩ࠱ࠤࠬ࡬ࡥࡢࡶࡸࡶࡪࡹ࠯ࠫ࠰ࡩࡩࡦࡺࡵࡳࡧࠪ࠭ࠥ⠚ࠠࡦࡺࡳࡥࡳࡪࡳࠡࡸ࡬ࡥࠥ࡭࡬ࡰࡤ࠱࡫ࡱࡵࡢࠩࠫ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࠹࠮ࠡࡒ࡯ࡥ࡮ࡴࠠࡧ࡫࡯ࡩࠥࡶࡡࡵࡪࠣ⠘ࠥࡱࡥࡱࡶࠣࡥࡸ࠳ࡩࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘ࡫࡮ࡥ࡫ࡱ࡫ࠥࡧࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡳࡷࠦࡵ࡯ࡧࡻࡴࡦࡴࡤࡦࡦࠣ࡫ࡱࡵࡢࠡࡶࡲࠤࡹ࡮ࡥࠡࡖࡒࠤࡸࡶ࡬ࡪࡶ࠰ࡸࡪࡹࡴࡴࠢࡄࡔࡎࠦ࡭ࡦࡣࡱࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࡴࡩࡧࠣࡷࡪࡸࡶࡦࡴࠣ࡬ࡦࡹࠠ࡯ࡱࠣࡺ࡮ࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡪࡰࡷࡳࠥ࡯࡮ࡥ࡫ࡹ࡭ࡩࡻࡡ࡭ࠢࡶࡴࡪࡩࡳࠡࡣࡱࡨࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡰࡴࡧࡩࡷࠐࠠࠡࠢࠣࠤࠥࠦࠠࡵࡪࡨࡱࠥࡳࡥࡢࡰ࡬ࡲ࡬࡬ࡵ࡭࡮ࡼ࠲࡚ࠥࡨࡪࡵࠣࡱࡪࡺࡨࡰࡦࠣࡩࡳࡹࡵࡳࡧࡶࠤ࡬ࡸࡡ࡯ࡷ࡯ࡥࡷࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩࡵࠣࡥࡷ࡫ࠠࡴࡧࡱࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥၷ")
        expanded = []
        for entry in bstack1l1ll1l1_opy_:
            if os.path.isdir(entry):
                bstack11ll1l11l1_opy_ = sorted(
                    glob.glob(os.path.join(entry, bstack1ll11_opy_ (u"ࠩ࠭࠮ࠬၸ"), bstack1ll11_opy_ (u"ࠪ࠮࠳࡬ࡥࡢࡶࡸࡶࡪ࠭ၹ")), recursive=True)
                )
                if bstack11ll1l11l1_opy_:
                    expanded.extend(bstack11ll1l11l1_opy_)
                else:
                    expanded.append(entry)
            elif any(c in entry for c in (bstack1ll11_opy_ (u"ࠫ࠯࠭ၺ"), bstack1ll11_opy_ (u"ࠬࡅࠧၻ"), bstack1ll11_opy_ (u"࡛࠭ࠨၼ"))):
                bstack11ll1l11l1_opy_ = sorted(glob.glob(entry, recursive=True))
                if bstack11ll1l11l1_opy_:
                    expanded.extend(bstack11ll1l11l1_opy_)
                else:
                    expanded.append(entry)
            else:
                expanded.append(entry)
        return expanded
    @measure(event_name=EVENTS.bstack1llllll111l_opy_, stage=STAGE.bstack11111llll_opy_)
    def bstack1l11111l1l_opy_(self):
        bstack1ll11_opy_ (u"ࠢࠣࠤࡄࡴࡵࡲࡹࠡࡶࡨࡷࡹࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡦࡰࡴࠣࡦࡪ࡮ࡡࡷࡧࠣ࡭࡫ࠦࡥ࡯ࡣࡥࡰࡪࡪࠢࠣࠤၽ")
        bstack11ll1l1l_opy_ = bstack1ll1ll11l1_opy_.get_instance(self.bstack1lllllll11l_opy_, self.logger)
        if bstack11ll1l1l_opy_ is None:
            self.logger.warn(bstack1ll11_opy_ (u"ࠣࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡪࡤࡲࡩࡲࡥࡳࠢ࡬ࡷࠥࡴ࡯ࡵࠢ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪࡪ࠮ࠡࡕ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦၾ"))
            return
        bstack1llllll1l1l_opy_ = False
        bstack11ll1l1l_opy_.bstack1llllll1lll_opy_(bstack1ll11_opy_ (u"ࠤࡨࡲࡦࡨ࡬ࡦࡦࠥၿ"), bstack11ll1l1l_opy_.bstack1ll11ll111_opy_())
        start_time = time.time()
        if bstack11ll1l1l_opy_.bstack1ll11ll111_opy_():
            test_files = self._1lllllll111_opy_(self.bstack1l1ll1l1_opy_)
            bstack1llllll1l1l_opy_ = True
            bstack1llllll11l1_opy_ = bstack11ll1l1l_opy_.bstack1llllll1ll1_opy_(test_files)
            if bstack1llllll11l1_opy_:
                self.bstack1l1ll1l1_opy_ = [item.replace(bstack1ll11_opy_ (u"ࠪࡠࡡ࠭ႀ"), bstack1ll11_opy_ (u"ࠫ࠴࠭ႁ")) for item in bstack1llllll11l1_opy_]
                bstack11ll1l1l_opy_.bstack1llllll1l11_opy_(bstack1llllll1l1l_opy_)
                self.logger.info(bstack1ll11_opy_ (u"࡚ࠧࡥࡴࡶࡶࠤࡷ࡫࡯ࡳࡦࡨࡶࡪࡪࠠࡶࡵ࡬ࡲ࡬ࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡀࠠࡼࡿࠥႂ").format(self.bstack1l1ll1l1_opy_))
            else:
                self.logger.info(bstack1ll11_opy_ (u"ࠨࡎࡰࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡷࡦࡴࡨࠤࡷ࡫࡯ࡳࡦࡨࡶࡪࡪࠠࡣࡻࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦႃ"))
        bstack11ll1l1l_opy_.bstack1llllll1lll_opy_(bstack1ll11_opy_ (u"ࠢࡵ࡫ࡰࡩ࡙ࡧ࡫ࡦࡰࡗࡳࡆࡶࡰ࡭ࡻࠥႄ"), int((time.time() - start_time) * 1000))
    def bstack111111l11l_opy_(self, bstack1l1ll1l1_opy_):
        bstack1ll11_opy_ (u"ࠣࠤࠥࡗࡪࡺࠠࡵࡪࡨࠤ࡫࡫ࡡࡵࡷࡵࡩࠥ࡬ࡩ࡭ࡧࡶࠤࡹࡵࠠࡣࡧࠣࡩࡽ࡫ࡣࡶࡶࡨࡨࠧࠨࠢႅ")
        self.bstack1l1ll1l1_opy_ = bstack1l1ll1l1_opy_
    def bstack1l1l1ll1_opy_(self):
        bstack1ll11_opy_ (u"ࠤࠥࠦࡌ࡫ࡴࠡࡶ࡫ࡩࠥ࡬ࡥࡢࡶࡸࡶࡪࠦࡦࡪ࡮ࡨࡷࠧࠨࠢႆ")
        return self.bstack1l1ll1l1_opy_