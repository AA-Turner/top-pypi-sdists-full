# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
def bstack1lllll1l11l_opy_(package_name):
    bstack11lllll_opy_ (u"ࠤࠥࠦࡈ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡡࠡࡲࡤࡧࡰࡧࡧࡦࠢ࡬ࡷࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡴࡦࡩ࡫ࡢࡩࡨࡣࡳࡧ࡭ࡦ࠼ࠣࡒࡦࡳࡥࠡࡱࡩࠤࡹ࡮ࡥࠡࡲࡤࡧࡰࡧࡧࡦࠢࡷࡳࠥࡩࡨࡦࡥ࡮ࠤ࠭࡫࠮ࡨ࠰࠯ࠤࠬࡶࡹࡵࡧࡶࡸࡤࡶࡡࡳࡣ࡯ࡰࡪࡲࠧࠪࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡥࡳࡴࡲ࠺ࠡࡖࡵࡹࡪࠦࡩࡧࠢࡳࡥࡨࡱࡡࡨࡧࠣ࡭ࡸࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥ࠮ࠣࡊࡦࡲࡳࡦࠢࡲࡸ࡭࡫ࡲࡸ࡫ࡶࡩࠏࠦࠠࠡࠢࠥࠦࠧ⁍")
    try:
        import importlib
        import importlib.util
        if hasattr(importlib.util, bstack11lllll_opy_ (u"ࠪࡪ࡮ࡴࡤࡠࡵࡳࡩࡨ࠭⁎")):
            bstack1llllll1lll1_opy_ = importlib.util.find_spec(package_name)
            return bstack1llllll1lll1_opy_ is not None and bstack1llllll1lll1_opy_.loader is not None
        elif hasattr(importlib, bstack11lllll_opy_ (u"ࠫ࡫࡯࡮ࡥࡡ࡯ࡳࡦࡪࡥࡳࠩ⁏")):
            bstack1llllll1llll_opy_ = importlib.find_loader(package_name)
            return bstack1llllll1llll_opy_ is not None
    except (ImportError, ModuleNotFoundError, ValueError):
        pass
    return False