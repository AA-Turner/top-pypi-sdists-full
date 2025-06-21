# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
from browserstack_sdk.bstack11lll1111l_opy_ import bstack1l1l1l11_opy_
from browserstack_sdk.bstack111l1l1ll1_opy_ import RobotHandler
def bstack1llll1lll_opy_(framework):
    if framework.lower() == bstack1l1l1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭᪅"):
        return bstack1l1l1l11_opy_.version()
    elif framework.lower() == bstack1l1l1l1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭᪆"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l1l1l1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ᪇"):
        import behave
        return behave.__version__
    else:
        return bstack1l1l1l1_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࠪ᪈")
def bstack1ll1l1111_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1l1l1l1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬ᪉"))
        framework_version.append(importlib.metadata.version(bstack1l1l1l1_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨ᪊")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1l1l1l1_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩ᪋"))
        framework_version.append(importlib.metadata.version(bstack1l1l1l1_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ᪌")))
    except:
        pass
    return {
        bstack1l1l1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ᪍"): bstack1l1l1l1_opy_ (u"ࠨࡡࠪ᪎").join(framework_name),
        bstack1l1l1l1_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪ᪏"): bstack1l1l1l1_opy_ (u"ࠪࡣࠬ᪐").join(framework_version)
    }