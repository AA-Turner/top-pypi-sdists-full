# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
def bstack1lll11l1111_opy_(package_name):
    bstack1l1_opy_ (u"ࠨࠢࠣࡅ࡫ࡩࡨࡱࠠࡪࡨࠣࡥࠥࡶࡡࡤ࡭ࡤ࡫ࡪࠦࡩࡴࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠥ࡯࡮ࠡࡶ࡫ࡩࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡱࡣࡦ࡯ࡦ࡭ࡥࡠࡰࡤࡱࡪࡀࠠࡏࡣࡰࡩࠥࡵࡦࠡࡶ࡫ࡩࠥࡶࡡࡤ࡭ࡤ࡫ࡪࠦࡴࡰࠢࡦ࡬ࡪࡩ࡫ࠡࠪࡨ࠲࡬࠴ࠬࠡࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡥࡷࡧ࡬࡭ࡧ࡯ࠫ࠮ࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡢࡰࡱ࡯࠾࡚ࠥࡲࡶࡧࠣ࡭࡫ࠦࡰࡢࡥ࡮ࡥ࡬࡫ࠠࡪࡵࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩ࠲ࠠࡇࡣ࡯ࡷࡪࠦ࡯ࡵࡪࡨࡶࡼ࡯ࡳࡦࠌࠣࠤࠥࠦࠢࠣࠤ⍡")
    try:
        import importlib
        import importlib.util
        if hasattr(importlib.util, bstack1l1_opy_ (u"ࠧࡧ࡫ࡱࡨࡤࡹࡰࡦࡥࠪ⍢")):
            bstack1lll1llll111_opy_ = importlib.util.find_spec(package_name)
            return bstack1lll1llll111_opy_ is not None and bstack1lll1llll111_opy_.loader is not None
        elif hasattr(importlib, bstack1l1_opy_ (u"ࠨࡨ࡬ࡲࡩࡥ࡬ࡰࡣࡧࡩࡷ࠭⍣")):
            bstack1lll1lll1lll_opy_ = importlib.find_loader(package_name)
            return bstack1lll1lll1lll_opy_ is not None
    except (ImportError, ModuleNotFoundError, ValueError):
        pass
    return False