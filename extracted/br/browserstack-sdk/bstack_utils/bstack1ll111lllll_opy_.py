# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
def bstack1ll11l1l1ll_opy_(package_name):
    bstack1l1111l_opy_ (u"ࠦࠧࠨࡃࡩࡧࡦ࡯ࠥ࡯ࡦࠡࡣࠣࡴࡦࡩ࡫ࡢࡩࡨࠤ࡮ࡹࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠣ࡭ࡳࠦࡴࡩࡧࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡶࡡࡤ࡭ࡤ࡫ࡪࡥ࡮ࡢ࡯ࡨ࠾ࠥࡔࡡ࡮ࡧࠣࡳ࡫ࠦࡴࡩࡧࠣࡴࡦࡩ࡫ࡢࡩࡨࠤࡹࡵࠠࡤࡪࡨࡧࡰࠦࠨࡦ࠰ࡪ࠲࠱ࠦࠧࡱࡻࡷࡩࡸࡺ࡟ࡱࡣࡵࡥࡱࡲࡥ࡭ࠩࠬࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡧࡵ࡯࡭࠼ࠣࡘࡷࡻࡥࠡ࡫ࡩࠤࡵࡧࡣ࡬ࡣࡪࡩࠥ࡯ࡳࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧ࠰ࠥࡌࡡ࡭ࡵࡨࠤࡴࡺࡨࡦࡴࡺ࡭ࡸ࡫ࠊࠡࠢࠣࠤࠧࠨࠢ▝")
    try:
        import importlib
        import importlib.util
        if hasattr(importlib.util, bstack1l1111l_opy_ (u"ࠬ࡬ࡩ࡯ࡦࡢࡷࡵ࡫ࡣࠨ▞")):
            bstack1ll1llll11l1_opy_ = importlib.util.find_spec(package_name)
            return bstack1ll1llll11l1_opy_ is not None and bstack1ll1llll11l1_opy_.loader is not None
        elif hasattr(importlib, bstack1l1111l_opy_ (u"࠭ࡦࡪࡰࡧࡣࡱࡵࡡࡥࡧࡵࠫ▟")):
            bstack1ll1llll111l_opy_ = importlib.find_loader(package_name)
            return bstack1ll1llll111l_opy_ is not None
    except (ImportError, ModuleNotFoundError, ValueError):
        pass
    return False