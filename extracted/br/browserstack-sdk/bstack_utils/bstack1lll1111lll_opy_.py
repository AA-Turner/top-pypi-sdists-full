# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
def bstack1ll1llll1l1_opy_(package_name):
    bstack1ll1lll_opy_ (u"ࠨࠢࠣࡅ࡫ࡩࡨࡱࠠࡪࡨࠣࡥࠥࡶࡡࡤ࡭ࡤ࡫ࡪࠦࡩࡴࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠥ࡯࡮ࠡࡶ࡫ࡩࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡱࡣࡦ࡯ࡦ࡭ࡥࡠࡰࡤࡱࡪࡀࠠࡏࡣࡰࡩࠥࡵࡦࠡࡶ࡫ࡩࠥࡶࡡࡤ࡭ࡤ࡫ࡪࠦࡴࡰࠢࡦ࡬ࡪࡩ࡫ࠡࠪࡨ࠲࡬࠴ࠬࠡࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡥࡷࡧ࡬࡭ࡧ࡯ࠫ࠮ࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡢࡰࡱ࡯࠾࡚ࠥࡲࡶࡧࠣ࡭࡫ࠦࡰࡢࡥ࡮ࡥ࡬࡫ࠠࡪࡵࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩ࠲ࠠࡇࡣ࡯ࡷࡪࠦ࡯ࡵࡪࡨࡶࡼ࡯ࡳࡦࠌࠣࠤࠥࠦࠢࠣࠤ⍽")
    try:
        import importlib
        import importlib.util
        if hasattr(importlib.util, bstack1ll1lll_opy_ (u"ࠧࡧ࡫ࡱࡨࡤࡹࡰࡦࡥࠪ⍾")):
            bstack1lll1lll1111_opy_ = importlib.util.find_spec(package_name)
            return bstack1lll1lll1111_opy_ is not None and bstack1lll1lll1111_opy_.loader is not None
        elif hasattr(importlib, bstack1ll1lll_opy_ (u"ࠨࡨ࡬ࡲࡩࡥ࡬ࡰࡣࡧࡩࡷ࠭⍿")):
            bstack1lll1ll1llll_opy_ = importlib.find_loader(package_name)
            return bstack1lll1ll1llll_opy_ is not None
    except (ImportError, ModuleNotFoundError, ValueError):
        pass
    return False