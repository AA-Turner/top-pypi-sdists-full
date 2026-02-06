# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
from browserstack_sdk.bstack1l1lll11l_opy_ import bstack1l1ll111_opy_
from browserstack_sdk.bstack1111l11ll1_opy_ import RobotHandler
def bstack1llllll11l_opy_(framework):
    if framework.lower() == bstack11lllll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ᱕"):
        return bstack1l1ll111_opy_.version()
    elif framework.lower() == bstack11lllll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ᱖"):
        return RobotHandler.version()
    elif framework.lower() == bstack11lllll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ᱗"):
        import behave
        return behave.__version__
    else:
        return bstack11lllll_opy_ (u"ࠫࡺࡴ࡫࡯ࡱࡺࡲࠬ᱘")
def bstack1l1l1lll11_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack11lllll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧ᱙"))
        framework_version.append(importlib.metadata.version(bstack11lllll_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᱚ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᱛ"))
        framework_version.append(importlib.metadata.version(bstack11lllll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᱜ")))
    except:
        pass
    return {
        bstack11lllll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᱝ"): bstack11lllll_opy_ (u"ࠪࡣࠬᱞ").join(framework_name),
        bstack11lllll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬᱟ"): bstack11lllll_opy_ (u"ࠬࡥࠧᱠ").join(framework_version)
    }