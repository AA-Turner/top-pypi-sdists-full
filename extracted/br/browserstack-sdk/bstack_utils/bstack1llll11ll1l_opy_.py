# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
def bstack1llll1ll1ll_opy_(package_name):
    bstack11l1l11_opy_ (u"ࠢࠣࠤࡆ࡬ࡪࡩ࡫ࠡ࡫ࡩࠤࡦࠦࡰࡢࡥ࡮ࡥ࡬࡫ࠠࡪࡵࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡲࡤࡧࡰࡧࡧࡦࡡࡱࡥࡲ࡫࠺ࠡࡐࡤࡱࡪࠦ࡯ࡧࠢࡷ࡬ࡪࠦࡰࡢࡥ࡮ࡥ࡬࡫ࠠࡵࡱࠣࡧ࡭࡫ࡣ࡬ࠢࠫࡩ࠳࡭࠮࠭ࠢࠪࡴࡾࡺࡥࡴࡶࡢࡴࡦࡸࡡ࡭࡮ࡨࡰࠬ࠯ࠊࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡣࡱࡲࡰ࠿ࠦࡔࡳࡷࡨࠤ࡮࡬ࠠࡱࡣࡦ࡯ࡦ࡭ࡥࠡ࡫ࡶࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠬࠡࡈࡤࡰࡸ࡫ࠠࡰࡶ࡫ࡩࡷࡽࡩࡴࡧࠍࠤࠥࠦࠠࠣࠤࠥℤ")
    try:
        import importlib
        import importlib.util
        if hasattr(importlib.util, bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡲࡩࡥࡳࡱࡧࡦࠫ℥")):
            bstack1lllll11l1ll_opy_ = importlib.util.find_spec(package_name)
            return bstack1lllll11l1ll_opy_ is not None and bstack1lllll11l1ll_opy_.loader is not None
        elif hasattr(importlib, bstack11l1l11_opy_ (u"ࠩࡩ࡭ࡳࡪ࡟࡭ࡱࡤࡨࡪࡸࠧΩ")):
            bstack1lllll11ll11_opy_ = importlib.find_loader(package_name)
            return bstack1lllll11ll11_opy_ is not None
    except (ImportError, ModuleNotFoundError, ValueError):
        pass
    return False