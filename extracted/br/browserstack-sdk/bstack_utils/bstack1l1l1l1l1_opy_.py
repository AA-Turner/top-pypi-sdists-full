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
from browserstack_sdk.bstack1l1ll11ll_opy_ import bstack1l1ll11l1l_opy_
from browserstack_sdk.bstack1llllllll11_opy_ import RobotHandler
def bstack1lll1l1l11_opy_(framework):
    if framework.lower() == bstack1ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ☟"):
        return bstack1l1ll11l1l_opy_.version()
    elif framework.lower() == bstack1ll111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ☠"):
        return RobotHandler.version()
    elif framework.lower() == bstack1ll111_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ☡"):
        import behave
        return behave.__version__
    else:
        return bstack1ll111_opy_ (u"ࠫࡺࡴ࡫࡯ࡱࡺࡲࠬ☢")
def bstack1lll11ll_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1ll111_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧ☣"))
        framework_version.append(importlib.metadata.version(bstack1ll111_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣ☤")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1ll111_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ☥"))
        framework_version.append(importlib.metadata.version(bstack1ll111_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ☦")))
    except:
        pass
    return {
        bstack1ll111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ☧"): bstack1ll111_opy_ (u"ࠪࡣࠬ☨").join(framework_name),
        bstack1ll111_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬ☩"): bstack1ll111_opy_ (u"ࠬࡥࠧ☪").join(framework_version)
    }