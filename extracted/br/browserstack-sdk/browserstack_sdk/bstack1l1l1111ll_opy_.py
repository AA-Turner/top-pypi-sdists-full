# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import os
import glob
import time
from bstack_utils.bstack1l11l11ll_opy_ import bstack111lll1l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
class bstack1ll1l111l1_opy_:
    def __init__(self, args, logger, bstack1llll1ll1l1_opy_, bstack1llll1lll11_opy_):
        self.args = args
        self.logger = logger
        self.bstack1llll1ll1l1_opy_ = bstack1llll1ll1l1_opy_
        self.bstack1llll1lll11_opy_ = bstack1llll1lll11_opy_
        self.bstack1lll1l111_opy_ = []
    def _1llll1ll11l_opy_(self, bstack1lll1l111_opy_):
        bstack111ll_opy_ (u"ࠣࠤࠥࡉࡽࡶࡡ࡯ࡦࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡡ࡯ࡦࠣ࡫ࡱࡵࡢ࠮ࡲࡤࡸࡹ࡫ࡲ࡯ࠢࡨࡲࡹࡸࡩࡦࡵࠣ࡭ࡳࠦࡳࡱࡧࡦࡣ࡫࡯࡬ࡦࡵࠣࡸࡴࠦࡩ࡯ࡦ࡬ࡺ࡮ࡪࡵࡢ࡮ࠣ࠲࡫࡫ࡡࡵࡷࡵࡩࠥ࡬ࡩ࡭ࡧࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡈࡢࡰࡧࡰࡪࡹࠠࡵࡪࡵࡩࡪࠦࡣࡢࡵࡨࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠ࠲࠰ࠣࡈ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࠨࡦ࠰ࡪ࠲ࠥ࠭ࡦࡦࡣࡷࡹࡷ࡫ࡳࠨࠫࠣ⠘ࠥࡽࡡ࡭࡭ࡶࠤࡷ࡫ࡣࡶࡴࡶ࡭ࡻ࡫࡬ࡺࠢࡩࡳࡷࠦࠪ࠯ࡨࡨࡥࡹࡻࡲࡦࠢࡩ࡭ࡱ࡫ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࠶࠳ࠦࡇ࡭ࡱࡥࠤࡵࡧࡴࡵࡧࡵࡲࠥ࠮ࡥ࠯ࡩ࠱ࠤࠬ࡬ࡥࡢࡶࡸࡶࡪࡹ࠯ࠫ࠰ࡩࡩࡦࡺࡵࡳࡧࠪ࠭ࠥ⠚ࠠࡦࡺࡳࡥࡳࡪࡳࠡࡸ࡬ࡥࠥ࡭࡬ࡰࡤ࠱࡫ࡱࡵࡢࠩࠫ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࠹࠮ࠡࡒ࡯ࡥ࡮ࡴࠠࡧ࡫࡯ࡩࠥࡶࡡࡵࡪࠣ⠘ࠥࡱࡥࡱࡶࠣࡥࡸ࠳ࡩࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘ࡫࡮ࡥ࡫ࡱ࡫ࠥࡧࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡳࡷࠦࡵ࡯ࡧࡻࡴࡦࡴࡤࡦࡦࠣ࡫ࡱࡵࡢࠡࡶࡲࠤࡹ࡮ࡥࠡࡖࡒࠤࡸࡶ࡬ࡪࡶ࠰ࡸࡪࡹࡴࡴࠢࡄࡔࡎࠦ࡭ࡦࡣࡱࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࡴࡩࡧࠣࡷࡪࡸࡶࡦࡴࠣ࡬ࡦࡹࠠ࡯ࡱࠣࡺ࡮ࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡪࡰࡷࡳࠥ࡯࡮ࡥ࡫ࡹ࡭ࡩࡻࡡ࡭ࠢࡶࡴࡪࡩࡳࠡࡣࡱࡨࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡰࡴࡧࡩࡷࠐࠠࠡࠢࠣࠤࠥࠦࠠࡵࡪࡨࡱࠥࡳࡥࡢࡰ࡬ࡲ࡬࡬ࡵ࡭࡮ࡼ࠲࡚ࠥࡨࡪࡵࠣࡱࡪࡺࡨࡰࡦࠣࡩࡳࡹࡵࡳࡧࡶࠤ࡬ࡸࡡ࡯ࡷ࡯ࡥࡷࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩࡵࠣࡥࡷ࡫ࠠࡴࡧࡱࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥႯ")
        expanded = []
        for entry in bstack1lll1l111_opy_:
            if os.path.isdir(entry):
                bstack11l1ll1l11_opy_ = sorted(
                    glob.glob(os.path.join(entry, bstack111ll_opy_ (u"ࠩ࠭࠮ࠬႰ"), bstack111ll_opy_ (u"ࠪ࠮࠳࡬ࡥࡢࡶࡸࡶࡪ࠭Ⴑ")), recursive=True)
                )
                if bstack11l1ll1l11_opy_:
                    expanded.extend(bstack11l1ll1l11_opy_)
                else:
                    expanded.append(entry)
            elif any(c in entry for c in (bstack111ll_opy_ (u"ࠫ࠯࠭Ⴒ"), bstack111ll_opy_ (u"ࠬࡅࠧႳ"), bstack111ll_opy_ (u"࡛࠭ࠨႴ"))):
                bstack11l1ll1l11_opy_ = sorted(glob.glob(entry, recursive=True))
                if bstack11l1ll1l11_opy_:
                    expanded.extend(bstack11l1ll1l11_opy_)
                else:
                    expanded.append(entry)
            else:
                expanded.append(entry)
        return expanded
    @measure(event_name=EVENTS.bstack1llll1ll111_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
    def bstack1l1l1l111l_opy_(self):
        bstack111ll_opy_ (u"ࠢࠣࠤࡄࡴࡵࡲࡹࠡࡶࡨࡷࡹࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡦࡰࡴࠣࡦࡪ࡮ࡡࡷࡧࠣ࡭࡫ࠦࡥ࡯ࡣࡥࡰࡪࡪࠢࠣࠤႵ")
        bstack1l11l11ll_opy_ = bstack111lll1l1l_opy_.bstack1l1l11ll1_opy_(self.bstack1llll1ll1l1_opy_, self.logger)
        if bstack1l11l11ll_opy_ is None:
            self.logger.warn(bstack111ll_opy_ (u"ࠣࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡪࡤࡲࡩࡲࡥࡳࠢ࡬ࡷࠥࡴ࡯ࡵࠢ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪࡪ࠮ࠡࡕ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦႶ"))
            return
        bstack1llll1l1lll_opy_ = False
        bstack1l11l11ll_opy_.bstack1llll1lll1l_opy_(bstack111ll_opy_ (u"ࠤࡨࡲࡦࡨ࡬ࡦࡦࠥႷ"), bstack1l11l11ll_opy_.bstack11lll11l1_opy_())
        start_time = time.time()
        if bstack1l11l11ll_opy_.bstack11lll11l1_opy_():
            test_files = self._1llll1ll11l_opy_(self.bstack1lll1l111_opy_)
            bstack1llll1l1lll_opy_ = True
            bstack1llll1l1ll1_opy_ = bstack1l11l11ll_opy_.bstack1llll1llll1_opy_(test_files)
            if bstack1llll1l1ll1_opy_:
                self.bstack1lll1l111_opy_ = [item.replace(bstack111ll_opy_ (u"ࠪࡠࡡ࠭Ⴘ"), bstack111ll_opy_ (u"ࠫ࠴࠭Ⴙ")) for item in bstack1llll1l1ll1_opy_]
                bstack1l11l11ll_opy_.bstack1llll1ll1ll_opy_(bstack1llll1l1lll_opy_)
                self.logger.info(bstack111ll_opy_ (u"࡚ࠧࡥࡴࡶࡶࠤࡷ࡫࡯ࡳࡦࡨࡶࡪࡪࠠࡶࡵ࡬ࡲ࡬ࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡀࠠࡼࡿࠥႺ").format(self.bstack1lll1l111_opy_))
            else:
                self.logger.info(bstack111ll_opy_ (u"ࠨࡎࡰࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡷࡦࡴࡨࠤࡷ࡫࡯ࡳࡦࡨࡶࡪࡪࠠࡣࡻࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦႻ"))
        bstack1l11l11ll_opy_.bstack1llll1lll1l_opy_(bstack111ll_opy_ (u"ࠢࡵ࡫ࡰࡩ࡙ࡧ࡫ࡦࡰࡗࡳࡆࡶࡰ࡭ࡻࠥႼ"), int((time.time() - start_time) * 1000))
    def bstack111ll1lll_opy_(self, bstack1lll1l111_opy_):
        bstack111ll_opy_ (u"ࠣࠤࠥࡗࡪࡺࠠࡵࡪࡨࠤ࡫࡫ࡡࡵࡷࡵࡩࠥ࡬ࡩ࡭ࡧࡶࠤࡹࡵࠠࡣࡧࠣࡩࡽ࡫ࡣࡶࡶࡨࡨࠧࠨࠢႽ")
        self.bstack1lll1l111_opy_ = bstack1lll1l111_opy_
    def bstack11ll1111ll_opy_(self):
        bstack111ll_opy_ (u"ࠤࠥࠦࡌ࡫ࡴࠡࡶ࡫ࡩࠥ࡬ࡥࡢࡶࡸࡶࡪࠦࡦࡪ࡮ࡨࡷࠧࠨࠢႾ")
        return self.bstack1lll1l111_opy_