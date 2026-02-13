# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
def bstack1llll11l1ll_opy_(package_name):
    bstack11l11_opy_ (u"ࠥࠦࠧࡉࡨࡦࡥ࡮ࠤ࡮࡬ࠠࡢࠢࡳࡥࡨࡱࡡࡨࡧࠣ࡭ࡸࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠢ࡬ࡲࠥࡺࡨࡦࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡵࡧࡣ࡬ࡣࡪࡩࡤࡴࡡ࡮ࡧ࠽ࠤࡓࡧ࡭ࡦࠢࡲࡪࠥࡺࡨࡦࠢࡳࡥࡨࡱࡡࡨࡧࠣࡸࡴࠦࡣࡩࡧࡦ࡯ࠥ࠮ࡥ࠯ࡩ࠱࠰ࠥ࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡢࡴࡤࡰࡱ࡫࡬ࠨࠫࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡦࡴࡵ࡬࠻ࠢࡗࡶࡺ࡫ࠠࡪࡨࠣࡴࡦࡩ࡫ࡢࡩࡨࠤ࡮ࡹࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦ࠯ࠤࡋࡧ࡬ࡴࡧࠣࡳࡹ࡮ࡥࡳࡹ࡬ࡷࡪࠐࠠࠡࠢࠣࠦࠧࠨℙ")
    try:
        import importlib
        import importlib.util
        if hasattr(importlib.util, bstack11l11_opy_ (u"ࠫ࡫࡯࡮ࡥࡡࡶࡴࡪࡩࠧℚ")):
            bstack1llll1lll1ll_opy_ = importlib.util.find_spec(package_name)
            return bstack1llll1lll1ll_opy_ is not None and bstack1llll1lll1ll_opy_.loader is not None
        elif hasattr(importlib, bstack11l11_opy_ (u"ࠬ࡬ࡩ࡯ࡦࡢࡰࡴࡧࡤࡦࡴࠪℛ")):
            bstack1llll1lll1l1_opy_ = importlib.find_loader(package_name)
            return bstack1llll1lll1l1_opy_ is not None
    except (ImportError, ModuleNotFoundError, ValueError):
        pass
    return False