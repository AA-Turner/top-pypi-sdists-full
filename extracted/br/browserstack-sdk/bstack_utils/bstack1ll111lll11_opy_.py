# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
def bstack1ll11l1ll1l_opy_(package_name):
    bstack1ll_opy_ (u"ࠢࠣࠤࡆ࡬ࡪࡩ࡫ࠡ࡫ࡩࠤࡦࠦࡰࡢࡥ࡮ࡥ࡬࡫ࠠࡪࡵࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡲࡤࡧࡰࡧࡧࡦࡡࡱࡥࡲ࡫࠺ࠡࡐࡤࡱࡪࠦ࡯ࡧࠢࡷ࡬ࡪࠦࡰࡢࡥ࡮ࡥ࡬࡫ࠠࡵࡱࠣࡧ࡭࡫ࡣ࡬ࠢࠫࡩ࠳࡭࠮࠭ࠢࠪࡴࡾࡺࡥࡴࡶࡢࡴࡦࡸࡡ࡭࡮ࡨࡰࠬ࠯ࠊࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡣࡱࡲࡰ࠿ࠦࡔࡳࡷࡨࠤ࡮࡬ࠠࡱࡣࡦ࡯ࡦ࡭ࡥࠡ࡫ࡶࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠬࠡࡈࡤࡰࡸ࡫ࠠࡰࡶ࡫ࡩࡷࡽࡩࡴࡧࠍࠤࠥࠦࠠࠣࠤࠥ╨")
    try:
        import importlib
        import importlib.util
        if hasattr(importlib.util, bstack1ll_opy_ (u"ࠨࡨ࡬ࡲࡩࡥࡳࡱࡧࡦࠫ╩")):
            bstack1lll1111111l_opy_ = importlib.util.find_spec(package_name)
            return bstack1lll1111111l_opy_ is not None and bstack1lll1111111l_opy_.loader is not None
        elif hasattr(importlib, bstack1ll_opy_ (u"ࠩࡩ࡭ࡳࡪ࡟࡭ࡱࡤࡨࡪࡸࠧ╪")):
            bstack1lll11111111_opy_ = importlib.find_loader(package_name)
            return bstack1lll11111111_opy_ is not None
    except (ImportError, ModuleNotFoundError, ValueError):
        pass
    return False