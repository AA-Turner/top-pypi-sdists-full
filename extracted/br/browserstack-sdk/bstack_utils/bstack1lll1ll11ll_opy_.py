# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
def bstack1llll1111ll_opy_(package_name):
    bstack1111_opy_ (u"ࠤࠥࠦࡈ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡡࠡࡲࡤࡧࡰࡧࡧࡦࠢ࡬ࡷࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡴࡦࡩ࡫ࡢࡩࡨࡣࡳࡧ࡭ࡦ࠼ࠣࡒࡦࡳࡥࠡࡱࡩࠤࡹ࡮ࡥࠡࡲࡤࡧࡰࡧࡧࡦࠢࡷࡳࠥࡩࡨࡦࡥ࡮ࠤ࠭࡫࠮ࡨ࠰࠯ࠤࠬࡶࡹࡵࡧࡶࡸࡤࡶࡡࡳࡣ࡯ࡰࡪࡲࠧࠪࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡥࡳࡴࡲ࠺ࠡࡖࡵࡹࡪࠦࡩࡧࠢࡳࡥࡨࡱࡡࡨࡧࠣ࡭ࡸࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥ࠮ࠣࡊࡦࡲࡳࡦࠢࡲࡸ࡭࡫ࡲࡸ࡫ࡶࡩࠏࠦࠠࠡࠢࠥࠦࠧ≌")
    try:
        import importlib
        import importlib.util
        if hasattr(importlib.util, bstack1111_opy_ (u"ࠪࡪ࡮ࡴࡤࡠࡵࡳࡩࡨ࠭≍")):
            bstack1llll1l1l11l_opy_ = importlib.util.find_spec(package_name)
            return bstack1llll1l1l11l_opy_ is not None and bstack1llll1l1l11l_opy_.loader is not None
        elif hasattr(importlib, bstack1111_opy_ (u"ࠫ࡫࡯࡮ࡥࡡ࡯ࡳࡦࡪࡥࡳࠩ≎")):
            bstack1llll1l1l1l1_opy_ = importlib.find_loader(package_name)
            return bstack1llll1l1l1l1_opy_ is not None
    except (ImportError, ModuleNotFoundError, ValueError):
        pass
    return False