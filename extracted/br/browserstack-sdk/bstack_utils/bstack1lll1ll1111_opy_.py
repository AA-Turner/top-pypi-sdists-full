# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
def bstack1lll1lll11l_opy_(package_name):
    bstack1ll111_opy_ (u"ࠣࠤࠥࡇ࡭࡫ࡣ࡬ࠢ࡬ࡪࠥࡧࠠࡱࡣࡦ࡯ࡦ࡭ࡥࠡ࡫ࡶࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠠࡪࡰࠣࡸ࡭࡫ࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡳࡥࡨࡱࡡࡨࡧࡢࡲࡦࡳࡥ࠻ࠢࡑࡥࡲ࡫ࠠࡰࡨࠣࡸ࡭࡫ࠠࡱࡣࡦ࡯ࡦ࡭ࡥࠡࡶࡲࠤࡨ࡮ࡥࡤ࡭ࠣࠬࡪ࠴ࡧ࠯࠮ࠣࠫࡵࡿࡴࡦࡵࡷࡣࡵࡧࡲࡢ࡮࡯ࡩࡱ࠭ࠩࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡤࡲࡳࡱࡀࠠࡕࡴࡸࡩࠥ࡯ࡦࠡࡲࡤࡧࡰࡧࡧࡦࠢ࡬ࡷࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤ࠭ࠢࡉࡥࡱࡹࡥࠡࡱࡷ࡬ࡪࡸࡷࡪࡵࡨࠎࠥࠦࠠࠡࠤࠥࠦᵻ")
    try:
        import importlib
        import importlib.util
        if hasattr(importlib.util, bstack1ll111_opy_ (u"ࠩࡩ࡭ࡳࡪ࡟ࡴࡲࡨࡧࠬᵼ")):
            bstack111111111l1_opy_ = importlib.util.find_spec(package_name)
            return bstack111111111l1_opy_ is not None and bstack111111111l1_opy_.loader is not None
        elif hasattr(importlib, bstack1ll111_opy_ (u"ࠪࡪ࡮ࡴࡤࡠ࡮ࡲࡥࡩ࡫ࡲࠨᵽ")):
            bstack111111111ll_opy_ = importlib.find_loader(package_name)
            return bstack111111111ll_opy_ is not None
    except (ImportError, ModuleNotFoundError, ValueError):
        pass
    return False