# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
def bstack1lll11111l1_opy_(package_name):
    bstack11lll1_opy_ (u"ࠤࠥࠦࡈ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡡࠡࡲࡤࡧࡰࡧࡧࡦࠢ࡬ࡷࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡴࡦࡩ࡫ࡢࡩࡨࡣࡳࡧ࡭ࡦ࠼ࠣࡒࡦࡳࡥࠡࡱࡩࠤࡹ࡮ࡥࠡࡲࡤࡧࡰࡧࡧࡦࠢࡷࡳࠥࡩࡨࡦࡥ࡮ࠤ࠭࡫࠮ࡨ࠰࠯ࠤࠬࡶࡹࡵࡧࡶࡸࡤࡶࡡࡳࡣ࡯ࡰࡪࡲࠧࠪࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡥࡳࡴࡲ࠺ࠡࡖࡵࡹࡪࠦࡩࡧࠢࡳࡥࡨࡱࡡࡨࡧࠣ࡭ࡸࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥ࠮ࠣࡊࡦࡲࡳࡦࠢࡲࡸ࡭࡫ࡲࡸ࡫ࡶࡩࠏࠦࠠࠡࠢࠥࠦࠧ⍖")
    try:
        import importlib
        import importlib.util
        if hasattr(importlib.util, bstack11lll1_opy_ (u"ࠪࡪ࡮ࡴࡤࡠࡵࡳࡩࡨ࠭⍗")):
            bstack1lll1llll1ll_opy_ = importlib.util.find_spec(package_name)
            return bstack1lll1llll1ll_opy_ is not None and bstack1lll1llll1ll_opy_.loader is not None
        elif hasattr(importlib, bstack11lll1_opy_ (u"ࠫ࡫࡯࡮ࡥࡡ࡯ࡳࡦࡪࡥࡳࠩ⍘")):
            bstack1lll1lllll11_opy_ = importlib.find_loader(package_name)
            return bstack1lll1lllll11_opy_ is not None
    except (ImportError, ModuleNotFoundError, ValueError):
        pass
    return False