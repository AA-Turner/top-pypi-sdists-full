# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
def bstack1lllll1ll11_opy_(package_name):
    bstack1l1111_opy_ (u"ࠦࠧࠨࡃࡩࡧࡦ࡯ࠥ࡯ࡦࠡࡣࠣࡴࡦࡩ࡫ࡢࡩࡨࠤ࡮ࡹࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠣ࡭ࡳࠦࡴࡩࡧࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡶࡡࡤ࡭ࡤ࡫ࡪࡥ࡮ࡢ࡯ࡨ࠾ࠥࡔࡡ࡮ࡧࠣࡳ࡫ࠦࡴࡩࡧࠣࡴࡦࡩ࡫ࡢࡩࡨࠤࡹࡵࠠࡤࡪࡨࡧࡰࠦࠨࡦ࠰ࡪ࠲࠱ࠦࠧࡱࡻࡷࡩࡸࡺ࡟ࡱࡣࡵࡥࡱࡲࡥ࡭ࠩࠬࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡧࡵ࡯࡭࠼ࠣࡘࡷࡻࡥࠡ࡫ࡩࠤࡵࡧࡣ࡬ࡣࡪࡩࠥ࡯ࡳࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧ࠰ࠥࡌࡡ࡭ࡵࡨࠤࡴࡺࡨࡦࡴࡺ࡭ࡸ࡫ࠊࠡࠢࠣࠤࠧࠨࠢ‥")
    try:
        import importlib
        import importlib.util
        if hasattr(importlib.util, bstack1l1111_opy_ (u"ࠬ࡬ࡩ࡯ࡦࡢࡷࡵ࡫ࡣࠨ…")):
            bstack1llllllll1l1_opy_ = importlib.util.find_spec(package_name)
            return bstack1llllllll1l1_opy_ is not None and bstack1llllllll1l1_opy_.loader is not None
        elif hasattr(importlib, bstack1l1111_opy_ (u"࠭ࡦࡪࡰࡧࡣࡱࡵࡡࡥࡧࡵࠫ‧")):
            bstack1llllllll11l_opy_ = importlib.find_loader(package_name)
            return bstack1llllllll11l_opy_ is not None
    except (ImportError, ModuleNotFoundError, ValueError):
        pass
    return False