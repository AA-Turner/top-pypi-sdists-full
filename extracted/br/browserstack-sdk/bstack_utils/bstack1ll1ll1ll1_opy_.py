# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
from browserstack_sdk.bstack1l11l11l11_opy_ import bstack11lllll1l_opy_
from browserstack_sdk.bstack1llllll1lll_opy_ import RobotHandler
def bstack1lll1l1l11_opy_(framework):
    if framework.lower() == bstack1lll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭Ṓ"):
        return bstack11lllll1l_opy_.version()
    elif framework.lower() == bstack1lll1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ṓ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1lll1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨṔ"):
        import behave
        return behave.__version__
    else:
        return bstack1lll1l_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࠪṕ")
def bstack111l11111_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1lll1l_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬṖ"))
        framework_version.append(importlib.metadata.version(bstack1lll1l_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨṗ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1lll1l_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩṘ"))
        framework_version.append(importlib.metadata.version(bstack1lll1l_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥṙ")))
    except:
        pass
    return {
        bstack1lll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬṚ"): bstack1lll1l_opy_ (u"ࠨࡡࠪṛ").join(framework_name),
        bstack1lll1l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪṜ"): bstack1lll1l_opy_ (u"ࠪࡣࠬṝ").join(framework_version)
    }