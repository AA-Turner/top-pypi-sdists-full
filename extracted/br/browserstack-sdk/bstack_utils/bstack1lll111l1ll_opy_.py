# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
def bstack1lll11l1lll_opy_(package_name):
    bstack1ll1lll_opy_ (u"ࠣࠤࠥࡇ࡭࡫ࡣ࡬ࠢ࡬ࡪࠥࡧࠠࡱࡣࡦ࡯ࡦ࡭ࡥࠡ࡫ࡶࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠠࡪࡰࠣࡸ࡭࡫ࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡳࡥࡨࡱࡡࡨࡧࡢࡲࡦࡳࡥ࠻ࠢࡑࡥࡲ࡫ࠠࡰࡨࠣࡸ࡭࡫ࠠࡱࡣࡦ࡯ࡦ࡭ࡥࠡࡶࡲࠤࡨ࡮ࡥࡤ࡭ࠣࠬࡪ࠴ࡧ࠯࠮ࠣࠫࡵࡿࡴࡦࡵࡷࡣࡵࡧࡲࡢ࡮࡯ࡩࡱ࠭ࠩࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡤࡲࡳࡱࡀࠠࡕࡴࡸࡩࠥ࡯ࡦࠡࡲࡤࡧࡰࡧࡧࡦࠢ࡬ࡷࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤ࠭ࠢࡉࡥࡱࡹࡥࠡࡱࡷ࡬ࡪࡸࡷࡪࡵࡨࠎࠥࠦࠠࠡࠤࠥࠦ⍜")
    try:
        import importlib
        import importlib.util
        if hasattr(importlib.util, bstack1ll1lll_opy_ (u"ࠩࡩ࡭ࡳࡪ࡟ࡴࡲࡨࡧࠬ⍝")):
            bstack1lll1llll111_opy_ = importlib.util.find_spec(package_name)
            return bstack1lll1llll111_opy_ is not None and bstack1lll1llll111_opy_.loader is not None
        elif hasattr(importlib, bstack1ll1lll_opy_ (u"ࠪࡪ࡮ࡴࡤࡠ࡮ࡲࡥࡩ࡫ࡲࠨ⍞")):
            bstack1lll1llll11l_opy_ = importlib.find_loader(package_name)
            return bstack1lll1llll11l_opy_ is not None
    except (ImportError, ModuleNotFoundError, ValueError):
        pass
    return False