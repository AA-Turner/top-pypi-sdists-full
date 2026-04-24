# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import os
import glob
import time
from bstack_utils.bstack1111111111_opy_ import bstack1l11l1ll11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
class bstack1ll11lll11_opy_:
    def __init__(self, args, logger, bstack1lllll111l1_opy_, bstack1llll1ll1ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lllll111l1_opy_ = bstack1lllll111l1_opy_
        self.bstack1llll1ll1ll_opy_ = bstack1llll1ll1ll_opy_
        self.bstack111l1l1l1l_opy_ = []
    def _1lllll1111l_opy_(self, bstack111l1l1l1l_opy_):
        bstack111ll11_opy_ (u"ࠣࠤࠥࡉࡽࡶࡡ࡯ࡦࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡡ࡯ࡦࠣ࡫ࡱࡵࡢ࠮ࡲࡤࡸࡹ࡫ࡲ࡯ࠢࡨࡲࡹࡸࡩࡦࡵࠣ࡭ࡳࠦࡳࡱࡧࡦࡣ࡫࡯࡬ࡦࡵࠣࡸࡴࠦࡩ࡯ࡦ࡬ࡺ࡮ࡪࡵࡢ࡮ࠣ࠲࡫࡫ࡡࡵࡷࡵࡩࠥ࡬ࡩ࡭ࡧࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡈࡢࡰࡧࡰࡪࡹࠠࡵࡪࡵࡩࡪࠦࡣࡢࡵࡨࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠ࠲࠰ࠣࡈ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࠨࡦ࠰ࡪ࠲ࠥ࠭ࡦࡦࡣࡷࡹࡷ࡫ࡳࠨࠫࠣ⠘ࠥࡽࡡ࡭࡭ࡶࠤࡷ࡫ࡣࡶࡴࡶ࡭ࡻ࡫࡬ࡺࠢࡩࡳࡷࠦࠪ࠯ࡨࡨࡥࡹࡻࡲࡦࠢࡩ࡭ࡱ࡫ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࠶࠳ࠦࡇ࡭ࡱࡥࠤࡵࡧࡴࡵࡧࡵࡲࠥ࠮ࡥ࠯ࡩ࠱ࠤࠬ࡬ࡥࡢࡶࡸࡶࡪࡹ࠯ࠫ࠰ࡩࡩࡦࡺࡵࡳࡧࠪ࠭ࠥ⠚ࠠࡦࡺࡳࡥࡳࡪࡳࠡࡸ࡬ࡥࠥ࡭࡬ࡰࡤ࠱࡫ࡱࡵࡢࠩࠫ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࠹࠮ࠡࡒ࡯ࡥ࡮ࡴࠠࡧ࡫࡯ࡩࠥࡶࡡࡵࡪࠣ⠘ࠥࡱࡥࡱࡶࠣࡥࡸ࠳ࡩࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘ࡫࡮ࡥ࡫ࡱ࡫ࠥࡧࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡳࡷࠦࡵ࡯ࡧࡻࡴࡦࡴࡤࡦࡦࠣ࡫ࡱࡵࡢࠡࡶࡲࠤࡹ࡮ࡥࠡࡖࡒࠤࡸࡶ࡬ࡪࡶ࠰ࡸࡪࡹࡴࡴࠢࡄࡔࡎࠦ࡭ࡦࡣࡱࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࡴࡩࡧࠣࡷࡪࡸࡶࡦࡴࠣ࡬ࡦࡹࠠ࡯ࡱࠣࡺ࡮ࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡪࡰࡷࡳࠥ࡯࡮ࡥ࡫ࡹ࡭ࡩࡻࡡ࡭ࠢࡶࡴࡪࡩࡳࠡࡣࡱࡨࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡰࡴࡧࡩࡷࠐࠠࠡࠢࠣࠤࠥࠦࠠࡵࡪࡨࡱࠥࡳࡥࡢࡰ࡬ࡲ࡬࡬ࡵ࡭࡮ࡼ࠲࡚ࠥࡨࡪࡵࠣࡱࡪࡺࡨࡰࡦࠣࡩࡳࡹࡵࡳࡧࡶࠤ࡬ࡸࡡ࡯ࡷ࡯ࡥࡷࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩࡵࠣࡥࡷ࡫ࠠࡴࡧࡱࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥႡ")
        expanded = []
        for entry in bstack111l1l1l1l_opy_:
            if os.path.isdir(entry):
                bstack1l11ll1l1_opy_ = sorted(
                    glob.glob(os.path.join(entry, bstack111ll11_opy_ (u"ࠩ࠭࠮ࠬႢ"), bstack111ll11_opy_ (u"ࠪ࠮࠳࡬ࡥࡢࡶࡸࡶࡪ࠭Ⴃ")), recursive=True)
                )
                if bstack1l11ll1l1_opy_:
                    expanded.extend(bstack1l11ll1l1_opy_)
                else:
                    expanded.append(entry)
            elif any(c in entry for c in (bstack111ll11_opy_ (u"ࠫ࠯࠭Ⴄ"), bstack111ll11_opy_ (u"ࠬࡅࠧႥ"), bstack111ll11_opy_ (u"࡛࠭ࠨႦ"))):
                bstack1l11ll1l1_opy_ = sorted(glob.glob(entry, recursive=True))
                if bstack1l11ll1l1_opy_:
                    expanded.extend(bstack1l11ll1l1_opy_)
                else:
                    expanded.append(entry)
            else:
                expanded.append(entry)
        return expanded
    @measure(event_name=EVENTS.bstack1llll1lll1l_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
    def bstack11111l111_opy_(self):
        bstack111ll11_opy_ (u"ࠢࠣࠤࡄࡴࡵࡲࡹࠡࡶࡨࡷࡹࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡦࡰࡴࠣࡦࡪ࡮ࡡࡷࡧࠣ࡭࡫ࠦࡥ࡯ࡣࡥࡰࡪࡪࠢࠣࠤႧ")
        bstack1111111111_opy_ = bstack1l11l1ll11_opy_.bstack1lllll1lll1_opy_(self.bstack1lllll111l1_opy_, self.logger)
        if bstack1111111111_opy_ is None:
            self.logger.warn(bstack111ll11_opy_ (u"ࠣࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡪࡤࡲࡩࡲࡥࡳࠢ࡬ࡷࠥࡴ࡯ࡵࠢ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪࡪ࠮ࠡࡕ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦႨ"))
            return
        bstack1llll1ll1l1_opy_ = False
        bstack1111111111_opy_.bstack1lllll11111_opy_(bstack111ll11_opy_ (u"ࠤࡨࡲࡦࡨ࡬ࡦࡦࠥႩ"), bstack1111111111_opy_.bstack1l111l1ll_opy_())
        start_time = time.time()
        if bstack1111111111_opy_.bstack1l111l1ll_opy_():
            test_files = self._1lllll1111l_opy_(self.bstack111l1l1l1l_opy_)
            bstack1llll1ll1l1_opy_ = True
            bstack1llll1lll11_opy_ = bstack1111111111_opy_.bstack1llll1llll1_opy_(test_files)
            if bstack1llll1lll11_opy_:
                self.bstack111l1l1l1l_opy_ = [item.replace(bstack111ll11_opy_ (u"ࠪࡠࡡ࠭Ⴊ"), bstack111ll11_opy_ (u"ࠫ࠴࠭Ⴋ")) for item in bstack1llll1lll11_opy_]
                bstack1111111111_opy_.bstack1llll1lllll_opy_(bstack1llll1ll1l1_opy_)
                self.logger.info(bstack111ll11_opy_ (u"࡚ࠧࡥࡴࡶࡶࠤࡷ࡫࡯ࡳࡦࡨࡶࡪࡪࠠࡶࡵ࡬ࡲ࡬ࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡀࠠࡼࡿࠥႬ").format(self.bstack111l1l1l1l_opy_))
            else:
                self.logger.info(bstack111ll11_opy_ (u"ࠨࡎࡰࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡷࡦࡴࡨࠤࡷ࡫࡯ࡳࡦࡨࡶࡪࡪࠠࡣࡻࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦႭ"))
        bstack1111111111_opy_.bstack1lllll11111_opy_(bstack111ll11_opy_ (u"ࠢࡵ࡫ࡰࡩ࡙ࡧ࡫ࡦࡰࡗࡳࡆࡶࡰ࡭ࡻࠥႮ"), int((time.time() - start_time) * 1000))
    def bstack11ll1111l_opy_(self, bstack111l1l1l1l_opy_):
        bstack111ll11_opy_ (u"ࠣࠤࠥࡗࡪࡺࠠࡵࡪࡨࠤ࡫࡫ࡡࡵࡷࡵࡩࠥ࡬ࡩ࡭ࡧࡶࠤࡹࡵࠠࡣࡧࠣࡩࡽ࡫ࡣࡶࡶࡨࡨࠧࠨࠢႯ")
        self.bstack111l1l1l1l_opy_ = bstack111l1l1l1l_opy_
    def bstack1ll1llll11_opy_(self):
        bstack111ll11_opy_ (u"ࠤࠥࠦࡌ࡫ࡴࠡࡶ࡫ࡩࠥ࡬ࡥࡢࡶࡸࡶࡪࠦࡦࡪ࡮ࡨࡷࠧࠨࠢႰ")
        return self.bstack111l1l1l1l_opy_