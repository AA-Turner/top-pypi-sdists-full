# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
def bstack1lllll1l1l1_opy_(package_name):
    bstack11l1ll1_opy_ (u"ࠧࠨࠢࡄࡪࡨࡧࡰࠦࡩࡧࠢࡤࠤࡵࡧࡣ࡬ࡣࡪࡩࠥ࡯ࡳࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡰࡢࡥ࡮ࡥ࡬࡫࡟࡯ࡣࡰࡩ࠿ࠦࡎࡢ࡯ࡨࠤࡴ࡬ࠠࡵࡪࡨࠤࡵࡧࡣ࡬ࡣࡪࡩࠥࡺ࡯ࠡࡥ࡫ࡩࡨࡱࠠࠩࡧ࠱࡫࠳࠲ࠠࠨࡲࡼࡸࡪࡹࡴࡠࡲࡤࡶࡦࡲ࡬ࡦ࡮ࠪ࠭ࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡨ࡯ࡰ࡮࠽ࠤ࡙ࡸࡵࡦࠢ࡬ࡪࠥࡶࡡࡤ࡭ࡤ࡫ࡪࠦࡩࡴࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨ࠱ࠦࡆࡢ࡮ࡶࡩࠥࡵࡴࡩࡧࡵࡻ࡮ࡹࡥࠋࠢࠣࠤࠥࠨࠢࠣ‭")
    try:
        import importlib
        import importlib.util
        if hasattr(importlib.util, bstack11l1ll1_opy_ (u"࠭ࡦࡪࡰࡧࡣࡸࡶࡥࡤࠩ‮")):
            bstack1lllllll1l1l_opy_ = importlib.util.find_spec(package_name)
            return bstack1lllllll1l1l_opy_ is not None and bstack1lllllll1l1l_opy_.loader is not None
        elif hasattr(importlib, bstack11l1ll1_opy_ (u"ࠧࡧ࡫ࡱࡨࡤࡲ࡯ࡢࡦࡨࡶࠬ ")):
            bstack1lllllll1ll1_opy_ = importlib.find_loader(package_name)
            return bstack1lllllll1ll1_opy_ is not None
    except (ImportError, ModuleNotFoundError, ValueError):
        pass
    return False