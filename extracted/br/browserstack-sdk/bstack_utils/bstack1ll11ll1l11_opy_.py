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
def bstack1ll11l111l1_opy_(package_name):
    bstack111ll_opy_ (u"ࠣࠤࠥࡇ࡭࡫ࡣ࡬ࠢ࡬ࡪࠥࡧࠠࡱࡣࡦ࡯ࡦ࡭ࡥࠡ࡫ࡶࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠠࡪࡰࠣࡸ࡭࡫ࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡳࡥࡨࡱࡡࡨࡧࡢࡲࡦࡳࡥ࠻ࠢࡑࡥࡲ࡫ࠠࡰࡨࠣࡸ࡭࡫ࠠࡱࡣࡦ࡯ࡦ࡭ࡥࠡࡶࡲࠤࡨ࡮ࡥࡤ࡭ࠣࠬࡪ࠴ࡧ࠯࠮ࠣࠫࡵࡿࡴࡦࡵࡷࡣࡵࡧࡲࡢ࡮࡯ࡩࡱ࠭ࠩࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡤࡲࡳࡱࡀࠠࡕࡴࡸࡩࠥ࡯ࡦࠡࡲࡤࡧࡰࡧࡧࡦࠢ࡬ࡷࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤ࠭ࠢࡉࡥࡱࡹࡥࠡࡱࡷ࡬ࡪࡸࡷࡪࡵࡨࠎࠥࠦࠠࠡࠤࠥࠦ◧")
    try:
        import importlib
        import importlib.util
        if hasattr(importlib.util, bstack111ll_opy_ (u"ࠩࡩ࡭ࡳࡪ࡟ࡴࡲࡨࡧࠬ◨")):
            bstack1ll1lll1llll_opy_ = importlib.util.find_spec(package_name)
            return bstack1ll1lll1llll_opy_ is not None and bstack1ll1lll1llll_opy_.loader is not None
        elif hasattr(importlib, bstack111ll_opy_ (u"ࠪࡪ࡮ࡴࡤࡠ࡮ࡲࡥࡩ࡫ࡲࠨ◩")):
            bstack1ll1lll1lll1_opy_ = importlib.find_loader(package_name)
            return bstack1ll1lll1lll1_opy_ is not None
    except (ImportError, ModuleNotFoundError, ValueError):
        pass
    return False